# Architecture de la plateforme de décision de fraude

Ce document décrit l'architecture en couches de la plateforme **Sentry** (décision de fraude au paiement en temps réel), le flux de données de bout en bout et le rôle de chaque composant. Il fait référence aux fichiers réels du dépôt et à la spécification `mlops-project-documentation.md`.

---

## 1. Vue d'ensemble

La plateforme est organisée en **couches** qui isolent les responsabilités :

```
┌─────────────────────────────────────────────────────────────────────────┐
│  COUCHE PRÉSENTATION / INTERFACES                                       │
│  - API FastAPI (src/api/) : décision de fraude en temps réel +          │
│    observabilité                                                        │
│  - UI Airflow (port 8080), UI MLflow (port 5000), UI MinIO (port 9001)  │
│  - Grafana (port 3000) : dashboards (métriques métier d'abord)          │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE ORCHESTRATION                                                   │
│  - Apache Airflow : 4 DAGs (ingestion, réconciliation des labels,       │
│    training, retraining)                                                │
│  - GitHub Actions : CI (ci.yml) et CD (cd.yml, shadow→canary→full)      │
│  - DVC : pipeline de données reproductible (dvc.yaml)                   │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE APPLICATION / SERVICES                                          │
│  - Service de décision (src/api/ : decision.py, rules_engine.py)        │
│  - Entraînement (src/models/ : train.py, threshold.py, evaluate.py,     │
│    promote.py, exploration.py)                                          │
│  - Feature engineering point-in-time (src/features/)                    │
│  - Streaming (src/streaming/ : decision_consumer.py,                    │
│    label_reconciliation.py)                                             │
│  - Monitoring drift + adversarial (src/monitoring/)                     │
│  - Kubernetes : Deployment + HPA + Service (k8s/)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE DONNÉES                                                         │
│  - Redis : store de features en ligne (sous 25 ms)                      │
│  - Kafka : événements de décision + agrégation de vélocité              │
│  - PostgreSQL 16 : backend store MLflow + métadonnées Airflow           │
│    + ledger de décisions                                                │
│  - MinIO (S3) : remote DVC + artefacts MLflow + ledger (objets)         │
│  - MLflow : tracking, Model Registry, artefacts                         │
│  - Feature store Parquet versionné (src/features/feature_store.py)      │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE OBSERVABILITÉ                                                   │
│  - Prometheus + Grafana (monitoring/)                                   │
│  - Alertes : règles Prometheus + alerting.py (Slack / log local)        │
│  - Garde-fous de canary : agrégés ET par segment (pays, BIN)            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Flux de données et de contrôle

### 2.1 Schéma complet

```
                       Requête d'autorisation de paiement
                                     │
                      ┌──────────────▼───────────────┐
                      │   Service de Décision (FastAPI)│   ◀── budget p99 : 100 ms
      Redis ◀─────────┼── 1. fetch features online    │
      store en ligne  │  2. calcul dans la requête    │
                      │  3. score (ensemble GBM)      │
                      │  4. surcouche de règles       │
                      │  5. décision coût attendu     │
                      └───────────┬───────────────────┘
                                  │ APPROUVER / RÉVISER / REFUSER
                                  │
                     ┌────────────▼─────────────┐
                     │  Kafka : événements de     │   ◀── asynchrone, hors chemin critique
                     │  décision                  │
                     └──┬────────┬────────┬─────┘
                        │        │        │
         ┌──────────────▼─┐ ┌────▼─────┐ ┌▼──────────────────┐
         │ Agrégateur de  │ │ Ledger de│ │ Monitoring temps  │
         │ features       │ │ décisions│ │ réel (frottement  │
         │ (streaming)    │ │ (S3+PG)  │ │  de frontière,    │
         └────────┬───────┘ └────┬─────┘ │  rafales)         │
                  │              │       └────────┬───────────┘
                  └──▶ Redis     │                │ alerte
                                 │                ▼
                     ┌───────────▼──────────┐  ┌──────────────┐
                     │ Réconciliation des   │  │ File de revue│
                     │ labels (chargebacks, │◀─│ analyste     │
                     │  réclamations,       │  │ fraude       │
                     │  résultats de revue) │  └──────────────┘
                     └───────────┬──────────┘
                                 │ labels matures + faibles
                     ┌───────────▼─────────────────────────────┐
                     │  Airflow : DAG de réentraînement        │
                     │  (hebdomadaire randomisé + drift)        │
                     │  GE → DVC → split vintage-aware → train  │
                     │  → seuil matrice de coûts → backtest     │
                     │  → déploiement shadow                    │
                     └───────────┬─────────────────────────────┘
                                 │ jamais directement en production
                     ┌───────────▼─────────────────────────────┐
                     │  Shadow (7 j) → Canary 5 % → 25 % → 100 %│
                     │  rollback automatique sur violation de   │
                     │  garde-fou                               │
                     └─────────────────────────────────────────┘
```

### 2.2 Chemin du flux

1. **Décision en ligne** — `src/api/main.py` (`/decide`) : récupère les features de vélocité depuis Redis, calcule les features dans la requête, score le modèle (GBM), applique la surcouche de règles, décide à trois paliers selon les seuils de la matrice de coûts. Réponse synchrone dans le budget 100 ms p99. Décision émise vers Kafka de façon **asynchrone** (jamais sur le chemin critique).
2. **Fail-open** — si le modèle est indisponible ou hors budget, `/decide` bascule en mode `rules-only` : les règles déterministes seules décident, le paiement n'est jamais bloqué par la panne du modèle.
3. **Streaming** — `src/streaming/decision_consumer.py` consomme les événements de décision : met à jour les compteurs de vélocité (fenêtres 1 h / 24 h / 7 j par carte, appareil, marchand, IP) dans Redis, écrit le **ledger de décisions** (version de modèle, snapshot de features, score, seuils, règles, issue).
4. **Réconciliation des labels** — `label_reconciliation_dag` (quotidien) : `src/streaming/label_reconciliation.py` joint les chargebacks, réclamations clients et résultats de revue aux décisions d'origine et maintient `label_maturity_date`. Les vintages matures alimentent l'entraînement ; les vintages censurés ne sont jamais traités comme « légitimes ».
5. **Ingestion** — `src/data/ingestion.py`, DAG `data_ingestion_dag` (quotidien 02:00). Sortie normalisée : `data/raw/transactions.parquet` (DVC stage `ingest`).
6. **Stockage versionné (DVC/MinIO)** — `dvc add` + `dvc push` (tâche `version_data`). Chaque commit Git épingle un snapshot de données — critique car les labels arrivent après l'entraînement et modifient rétroactivement l'historique.
7. **Feature engineering point-in-time** — `src/features/build_features.py` construit les features de vélocité ; `src/features/point_in_time.py` applique la correction point-in-time (features telles qu'au moment de la transaction, jamais « aujourd'hui ») et inclut le test de fuite. Son état est sérialisé dans `data/features/features_config.json` et embarqué comme artefact MLflow.
8. **Entraînement** — `src/models/train.py` : GBM, split **vintage-aware** (vintages matures déclarés, censure explicite), labels faibles pondérés pour la fraîcheur. Métriques loggées dans MLflow (coût attendu, capture de fraude, faux refus), modèle enregistré au stage `Staging`. `src/models/threshold.py` dérive `t_low` / `t_high` de la matrice de coûts et de la capacité de revue.
9. **Évaluation / backtest** — `src/models/evaluate.py` : backtest sur vintages matures uniquement ; gates sur coût attendu, taux de faux refus, capture de fraude. Sortie : `models/evaluation/latest_report.json`.
10. **Promotion staged** — `src/models/promote.py` : Staging → **Shadow** (7 jours, 100 % du trafic scoré, 0 % actionné) → canary 5 % → 25 % → 100 %. Garde-fous agrégés **et par segment** avec rollback automatique en moins de 5 minutes.
11. **CI/CD** — GitHub Actions construit les images Docker taguées au SHA du commit, les pousse sur GHCR, déploie en staging (smoke tests) puis en production (shadow → canary → full).
12. **Monitoring** — Prometheus scrape `/metrics` ; Evidently compare la fenêtre de production à la référence d'entraînement ; les détecteurs adversariaux (`src/monitoring/adversarial_detectors.py`) surveillent le frottement de frontière, les rafales coordonnées et le sondage.
13. **Réentraînement** — `retraining_pipeline` : déclenché par drift distributionnel, signature adversarial, ou planification hebdomadaire **randomisée** ; passe toujours par shadow avant tout trafic réel.

---

## 3. Couches en détail

### 3.1 Couche données

| Élément | Fichier | Rôle |
|---|---|---|
| Transactions brutes synthétiques | `scripts/generate_synthetic_data.py` | Génère le dataset de démonstration (fraude card-not-present) |
| Raw versionné | `data/raw/transactions.parquet` | DVC stage `ingest`, poussé vers MinIO |
| Processed | `data/processed/transactions.parquet` | DVC stage `preprocess` |
| Features | `data/features/features.parquet` + `features_config.json` | DVC stage `build_features` — vélocité + features point-in-time |
| Jeu vintage-aware | `data/training/train_vintage_aware.parquet` | DVC stage `build_training_set` — vintages matures/censurés déclarés |
| Feature store | `src/features/feature_store.py` | Versions Parquet `features_v{N}.parquet` (offline) + store en ligne Redis |
| Référence drift | `data/monitoring/reference.csv` | Jeu de test mature retenu par `train.py` |
| Fenêtre courante | `data/monitoring/current.csv` | Décisions de production comparées par Evidently |
| Ledger de décisions | Kafka → S3 + PostgreSQL | Enregistrement immuable de chaque décision (version de modèle, features, score, seuils, règles, issue) |

### 3.2 Couche stockage

- **MinIO** (`docker/docker-compose.yml`, service `minio`) — bucket `mlops-bucket` avec sous-dossiers `data/` (remote DVC), `mlflow-artifacts/` et `decision-ledger/`. Console sur le port 9001.
- **PostgreSQL 16** (service `postgres`) — backend store du serveur MLflow (base `mlflow`) et ledger de décisions (index de recherche). Airflow utilise aussi cette base via `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`.
- **Redis** (service `redis`) — store de features en ligne : compteurs de vélocité à lecture sous 25 ms.
- **Kafka** (service `kafka`) — événements de décision (topic `decisions`), agrégation streaming, logging asynchrone.
- **MLflow** (`mlflow/Dockerfile.mlflow`) — serveur sur le port 5000 : tracking des runs et Model Registry.

### 3.3 Couche orchestration

- **Airflow 2.9.2** (`docker/docker-compose.yml`, service `airflow`) — exécuteur LocalExecutor, DAGs montés depuis `airflow/dags`, code source monté depuis `src/`. Le conteneur installe `requirements.txt` au démarrage.
- **DVC** — `dvc.yaml` déclare les stages `ingest`, `preprocess`, `build_features`, `build_training_set`, `train` ; `Makefile` expose les commandes équivalentes pour l'exécution hors Airflow.
- **GitHub Actions** — `ci.yml` et `cd.yml` orchestrent qualité, build et déploiement staged (voir `docs/deployment.md`).

### 3.4 Couche application

- **Service de décision FastAPI** (`src/api/`) — endpoint `/decide` (mono et batch), `/health`, `/metrics`, `/model-info`. Logique à trois paliers dans `src/api/decision.py`, surcouche de règles dans `src/api/rules_engine.py`, chemin fail-open intégré. Schémas pydantic dans `src/api/schemas.py`.
- **Services ML** — `src/models/` (train/threshold/evaluate/promote/exploration), `src/features/` (build_features/velocity_aggregator/point_in_time/feature_store), `src/data/` (ingestion/preprocessing/validation).
- **Streaming** — `src/streaming/` (decision_consumer, label_reconciliation).
- **Monitoring** — `src/monitoring/` (drift_detection, adversarial_detectors, alerting).

### 3.5 Couche observabilité

- **Prometheus** (`monitoring/prometheus/prometheus.yml`) — job `mlops-api` (cible `api:8000`) et `mlops-api-local` (cible `host.docker.internal:8000`). Règles dans `alert_rules.yml`.
- **Grafana** (`monitoring/grafana/dashboards/`) — `business-metrics.json` (coût net par 1 000 transactions, capture de fraude, faux refus, ratio de chargeback, revue) et `model-drift.json`, provisionnés en lecture seule dans le conteneur.

---

## 4. Garanties transverses

- **Pas de training/serving skew** : le même `FeatureTransformer` (état sérialisé dans `features_config.json`) est appliqué à l'entraînement (`build_features.py`) et à l'inférence (`model_loader.py` → `ModelBundle.predict_proba`).
- **Correction point-in-time** : chaque ligne d'entraînement est construite avec les features telles qu'au moment de la transaction. Une tentative de fuite temporelle est rejetée par un test dédié (`tests/unit/test_point_in_time.py`).
- **Vintages explicites** : les transactions non matures ne sont jamais labellisées négatives ; `label_maturity_date` est suivie par le pipeline.
- **Traçabilité de bout en bout** : un modèle de production est relié à son `run_id` MLflow, son commit Git (`git_commit`), sa version de données (`DVC_DATA_VERSION`) et son rapport d'évaluation. **Chaque décision** est reconstruisible depuis le ledger avec sa version de modèle exacte (exigence réglementaire et de litige).
- **Immutabilité** : images taguées au SHA du commit (CD), jamais de `latest` en production.
- **Promotion sous contrainte** : gates de qualité sur vintages matures **et** 7 jours de shadow, puis canary avec garde-fous segmentés ; l'ancienne version est archivée.
- **Fail-open** : une panne du modèle dégrade vers les règles seules, ne bloque jamais les paiements.
- **Automatisation de la boucle** : drift/signature adversarial → réentraînement vintage-aware → shadow → canary → nouvelle fenêtre de référence.

---

## 5. Environnements

| Environnement | Outils | Caractéristiques |
|---|---|---|
| Local | `docker/docker-compose.yml`, `mlflow/docker-compose.yml` | Toute la stack en un `docker compose up` (dont Redis + Kafka) |
| CI | GitHub Actions (`ci.yml`) | Pipeline qualité + build + scan Trivy + test de fuite temporelle |
| Staging | K8s `k8s/overlays/staging`, GitHub Actions (`cd.yml`) | 2 réplicas, smoke tests automatisés |
| Production | K8s `k8s/overlays/production` | 5 réplicas, HPA, approbation manuelle, **shadow → canary → full**, rolling update |