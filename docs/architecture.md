# Architecture de la plateforme MLOps

Ce document décrit l'architecture en couches de la plateforme, le flux de données de bout en bout et le rôle de chaque composant. Il fait référence aux fichiers réels du dépôt.

---

## 1. Vue d'ensemble

La plateforme est organisée en **couches** qui isolent les responsabilités :

```
┌─────────────────────────────────────────────────────────────────────────┐
│  COUCHE PRÉSENTATION / INTERFACES                                       │
│  - API FastAPI (src/api/) : inférence et observabilité                  │
│  - UI Airflow (port 8080), UI MLflow (port 5000), UI MinIO (port 9001)  │
│  - Grafana (port 3000) : dashboards                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE ORCHESTRATION                                                   │
│  - Apache Airflow : 3 DAGs (ingestion, training, retraining)            │
│  - GitHub Actions : CI (ci.yml) et CD (cd.yml)                          │
│  - DVC : pipeline de données reproductible (dvc.yaml)                    │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE APPLICATION / SERVICES                                          │
│  - Entraînement (src/models/train.py, evaluate.py, promote.py)          │
│  - Feature engineering (src/features/)                                  │
│  - Monitoring drift (src/monitoring/)                                   │
│  - Kubernetes : Deployment + HPA + Service (k8s/)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE DONNÉES                                                         │
│  - PostgreSQL 16 : backend store MLflow + métadonnées Airflow           │
│  - MinIO (S3) : remote DVC + artefacts MLflow                           │
│  - MLflow : tracking, Model Registry, artefacts                         │
│  - Feature store Parquet versionné (src/features/feature_store.py)      │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE OBSERVABILITÉ                                                   │
│  - Prometheus + Grafana (monitoring/)                                   │
│  - Alertes : règles Prometheus + alerting.py (Slack / log local)        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Flux de données et de contrôle

### 2.1 Schéma complet

```
 1. INGESTION                     ┌─────────────────┐
                                 │ Source          │
 ┌─────────────────┐   ────────▶ │ data/external/  │
 │ Airflow         │             │ dataset.csv     │
 │ data_ingestion_ │             └────────┬────────┘
 │ dag (02:00)     │                      ▼
 └────────┬────────┘             ┌─────────────────┐
          │ ingest_data          │ data/raw/       │ ◀──── DVC stage « ingest »
          │                      │ dataset.csv     │      (dvc.yaml, Makefile: ingest)
          ▼                      └────────┬────────┘
 ┌─────────────────┐             ┌─────────────────┐
 │ validate_data   │ ──────────▶ │ Great           │
 │ (Great          │             │ Expectations    │
 │  Expectations)  │             │ dataset_suite   │
 └────────┬────────┘             └─────────────────┘
          │ version_data
          │ (dvc add + dvc push)
          ▼
 ┌────────────────────────────────────────────────┐
 │ 2. STOCKAGE VERSIONNÉ   MinIO remote (S3)     │
 │    s3://mlops-bucket/data  (.dvc/config)      │
 └────────────────────────────────────────────────┘
          │
 3. PRÉPROCESSING        ┌────────────────────────────┐
          └────────────▶ │ preprocessing.py           │  DVC stage « preprocess »
                         │ → data/processed/dataset.csv│  (Makefile: preprocess)
                         └────────────┬───────────────┘
                                      ▼
 4. FEATURE ENGINEERING ┌────────────────────────────┐
                        │ build_features.py          │  DVC stage « build_features »
                        │ → features.parquet +       │  (Makefile: features)
                        │   features_config.json     │
                        │ FeatureStore versionné     │
                        └────────────┬───────────────┘
                                     ▼
 5. ENTRAÎNEMENT       ┌────────────────────────────┐   ┌─────────────────────┐
                       │ train.py                   │──▶│ MLflow Tracking     │
                       │ RandomForest, split 80/20  │   │ params, metrics,     │
                       │ → models/model.pkl,        │   │ artefacts, confusion │
                       │   metrics.json             │   │ matrix, importances  │
                       └────────────┬───────────────┘   └──────────┬──────────┘
                                    │                              ▼
                                    │                ┌─────────────────────┐
                                    │                │ Model Registry      │
                                    └────────────────▶│ version → Staging   │
                                                     └──────────┬──────────┘
                                                                │
 6. ÉVALUATION / PROMOTION   ┌───────────────────────────────────┤
                             │                                   │
                             ▼                                   ▼
                ┌─────────────────────────┐          ┌──────────────────────────┐
                │ evaluate.py             │          │ promote.py               │
                │ gates: min_f1,          │          │ candidate > production ? │
                │ min_accuracy,           │          │ Staging → Production     │
                │ min_roc_auc             │          │ → production_report.json │
                │ → latest_report.json    │          └────────────┬─────────────┘
                └─────────────────────────┘                       │
                                                                  ▼
 7. CI/CD   ┌─────────────────────────┐               ┌──────────────────────────┐
            │ ci.yml (lint, security, │               │ cd.yml                   │
            │ tests, trivy)           │               │ build+push GHCR → staging│
            │ cd.yml                  │               │ → production (approbation)│
            └─────────────────────────┘               └────────────┬─────────────┘
                                                                   │
                                                                   ▼
 8. API FastAPI   ┌─────────────────────────┐          ┌──────────────────────────┐
                  │ model_loader.py         │          │ main.py                  │
                  │ charge models:/churn_   │─────────▶│ /predict /health         │
                  │ model/Production        │          │ /metrics /model-info     │
                  └─────────────────────────┘          └────────────┬─────────────┘
                                                                   │
                                                                   ▼
 9. MONITORING   ┌─────────────────────────┐          ┌──────────────────────────┐
                 │ Prometheus scrape       │          │ Evidently drift          │
                 │ /metrics toutes les 15s │          │ reference.csv vs         │
                 │ → alert_rules.yml       │          │ current.csv (DRIFT_      │
                 │ → dashboards Grafana    │          │ THRESHOLD=0.3)           │
                 └─────────────────────────┘          └────────────┬─────────────┘
                                                                   │
                                                                   ▼
10. RÉENTRAÎNEMENT  ┌─────────────────────────┐
                    │ retraining_pipeline     │
                    │ check_drift (short-     │
                    │ circuit) → relance la   │
                    │ boucle 3→6              │
                    └─────────────────────────┘
```

### 2.2 Chemin du flux

1. **Ingestion** — `src/data/ingestion.py`, DAG `data_ingestion_dag` (quotidien 02:00). Source résolue : `--source` > `INGESTION_SOURCE` > `data/external/dataset.csv`. Sortie normalisée : `data/raw/dataset.csv` (DVC stage `ingest`).
2. **Stockage versionné (DVC/MinIO)** — `dvc add data/raw/dataset.csv && dvc commit -f && dvc push` (tâche `version_data` du DAG). Le remote est défini dans `.dvc/config` (`s3://mlops-bucket/data`, endpoint `http://localhost:9000`). Chaque commit Git épingle un snapshot de données.
3. **Feature engineering** — `src/features/build_features.py` construit le `FeatureTransformer` (mappings catégoriels, statistiques numériques, colonnes `charges_per_tenure`, `tenure_years`, `num_services`). Son état est sérialisé dans `data/features/features_config.json` et embarqué comme artefact MLflow. `src/features/feature_store.py` versionne les jeux de features en Parquet (`features_v{N}.parquet` + schéma).
4. **Entraînement** — `src/models/train.py` : RandomForest 300 arbres, split stratifié 80/20, métriques loggées dans MLflow, modèle enregistré au stage `Staging`, référence d'entraînement écrite dans `data/monitoring/reference.csv`.
5. **Évaluation** — `src/models/evaluate.py` : gates configurables (`MIN_F1=0.35`, `MIN_ACCURACY=0.70`, `MIN_ROC_AUC=0.72`). Sortie : `models/evaluation/latest_report.json`.
6. **Promotion** — `src/models/promote.py` : ne promeut que si gates passées **et** `f1` candidat ≥ `f1` production. La version précédente passe en `Archived`. Sortie : `models/evaluation/production_report.json` (utilisé par `/model-info` et le dashboard `Served model version`).
7. **CI/CD** — GitHub Actions construit les images Docker taguées au SHA du commit, les pousse sur GHCR, déploie en staging (smoke tests) puis en production (approbation manuelle).
8. **API FastAPI** — `src/api/model_loader.py` charge `models:/churn_model/Production` au démarrage (fallback : `MLFLOW_MODEL_URI`, puis `models/model.pkl` local). Reload périodique si `RELOAD_INTERVAL > 0`.
9. **Monitoring** — Prometheus scrape `/metrics` (instrumentator FastAPI + histogrammes personnalisés) ; Evidently compare `reference.csv` vs `current.csv` et produit `data/monitoring/drift_report.json` (+ HTML).
10. **Réentraînement** — `retraining_pipeline` (@daily) : `check_drift` court-circuite le pipeline si aucun drift ; sinon il relance préprocess → features → train → evaluate → promote → notify.

---

## 3. Couches en détail

### 3.1 Couche données

| Élément | Fichier | Rôle |
|---|---|---|
| Dataset brut synthétique | `scripts/generate_synthetic_data.py` | Génère `data/external/dataset.csv` (télécom churn) |
| Raw versionné | `data/raw/dataset.csv` | DVC stage `ingest`, poussé vers MinIO |
| Processed | `data/processed/dataset.csv` | DVC stage `preprocess` (nettoyage, colonnes typées) |
| Features | `data/features/features.parquet` + `features_config.json` | DVC stage `build_features` |
| Feature store | `src/features/feature_store.py` | Versions Parquet `features_v{N}.parquet`, schéma documenté |
| Référence drift | `data/monitoring/reference.csv` | Jeu de test retenu par `train.py` (prédictions + labels) |
| Fenêtre courante | `data/monitoring/current.csv` | Données de production comparées par Evidently |

### 3.2 Couche stockage

- **MinIO** (`docker/docker-compose.yml`, service `minio`) — bucket `mlops-bucket` avec sous-dossiers `data/` (remote DVC) et `mlflow-artifacts/`. Console sur le port 9001.
- **PostgreSQL 16** (service `postgres`) — backend store du serveur MLflow (base `mlflow`). Airflow utilise aussi cette base via `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`.
- **MLflow** (`mlflow/Dockerfile.mlflow`) — serveur sur le port 5000 : tracking des runs et Model Registry.

### 3.3 Couche orchestration

- **Airflow 2.9.2** (`docker/docker-compose.yml`, service `airflow`) — exécuteur LocalExecutor, DAGs montés depuis `airflow/dags`, code source monté depuis `src/`. Le conteneur installe `requirements.txt` au démarrage.
- **DVC** — `dvc.yaml` déclare 4 stages ; `Makefile` expose les commandes équivalentes (`ingest`, `preprocess`, `features`, `train`) pour l'exécution hors Airflow.
- **GitHub Actions** — `ci.yml` et `cd.yml` orchestrent qualité, build et déploiement (voir `docs/deployment.md`).

### 3.4 Couche application

- **API FastAPI** (`src/api/`) — endpoints `/predict` (mono et batch), `/health`, `/metrics`, `/model-info`. Schémas pydantic avec alias identiques aux colonnes d'entraînement (`src/api/schemas.py`).
- **Services ML** — `src/models/` (train/evaluate/promote), `src/features/` (build_features/feature_store), `src/data/` (ingestion/preprocessing/validation).
- **Monitoring drift** — `src/monitoring/` (drift_detection, alerting).

### 3.5 Couche observabilité

- **Prometheus** (`monitoring/prometheus/prometheus.yml`) — job `mlops-api` (cible `api:8000`) et `mlops-api-local` (cible `host.docker.internal:8000`). Règles dans `alert_rules.yml`.
- **Grafana** (`monitoring/grafana/dashboards/`) — `api-performance.json` et `model-drift.json`, provisionnés en lecture seule dans le conteneur.

---

## 4. Garanties transverses

- **Pas de training/serving skew** : le même `FeatureTransformer` (état sérialisé dans `features_config.json`) est appliqué à l'entraînement (`build_features.py`) et à l'inférence (`model_loader.py` → `ModelBundle.predict_proba`).
- **Traçabilité de bout en bout** : un modèle de production est relié à son `run_id` MLflow, son commit Git (`git_commit`), sa version de données (`DVC_DATA_VERSION`) et son rapport d'évaluation.
- **Immutabilité** : images taguées au SHA du commit (CD), jamais de `latest` en production.
- **Promotion sous contrainte** : gates de qualité **et** comparaison au modèle en place (`promote.py`), avec archivage de l'ancienne version.
- **Automatisation de la boucle** : drift → réentraînement → promotion uniquement si meilleur → nouvelle fenêtre de référence.

---

## 5. Environnements

| Environnement | Outils | Caractéristiques |
|---|---|---|
| Local | `docker/docker-compose.yml`, `mlflow/docker-compose.yml` | Toute la stack en un `docker compose up` |
| CI | GitHub Actions (`ci.yml`) | Pipeline qualité + build + scan Trivy |
| Staging | K8s `k8s/overlays/staging`, GitHub Actions (`cd.yml`) | 2 réplicas, smoke tests automatisés |
| Production | K8s `k8s/overlays/production` | 5 réplicas, HPA, approbation manuelle, rolling update |
