# Sentry — Plateforme de Décision de Fraude au Paiement en Temps Réel

> Infrastructure MLOps complète et reproductible pour la **décision de fraude card-not-present en temps réel** : **Apache Airflow + DVC/MinIO + MLflow + FastAPI + Docker + GitHub Actions + Kubernetes + Prometheus/Grafana + Evidently + Redis + Kafka**.
>
> Produit cible : **Sentry** — décision de fraude en **moins de 100 ms (p99)**, à trois paliers (APPROUVER / RÉVISER / REFUSER), avec une boucle de réentraînement fermée construite autour de **labels retardés (chargebacks) et biaisés (boucle de feedback)**.

Cette plateforme illustre le cycle de vie complet d'un système de décision de fraude, de l'ingestion des transactions jusqu'à la détection de drift **adversarial** en production et au réentraînement automatique **vintage-aware**. Le dépôt démontre l'architecture sur un **jeu de données synthétique de substitution** (voir [Risques honnêtes](#risques-honnêtes)) : c'est une démonstration légitime de l'architecture, pas une revendication de performance de fraude de production.

La spécification technique complète est dans [`mlops-project-documentation.md`](mlops-project-documentation.md).

---

## Sommaire

- [Présentation](#présentation)
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Structure du dépôt](#structure-du-dépôt)
- [Démarrage rapide](#démarrage-rapide)
- [Pipeline ML et orchestration](#pipeline-ml-et-orchestration)
- [CI/CD](#cicd)
- [Déploiement Kubernetes](#déploiement-kubernetes)
- [Déploiement du modèle : shadow, puis canary](#déploiement-du-modèle--shadow-puis-canary)
- [Monitoring](#monitoring)
- [Risques honnêtes](#risques-honnêtes)
- [Documentation détaillée](#documentation-détaillée)
- [Dépannage](#dépannage)

---

## Présentation

Le projet démontre une boucle MLOps fermée et automatisée pour la décision de fraude :

1. **Décision en ligne** : le service FastAPI `/decide` retourne APPROUVER / RÉVISER / REFUSER à l'intérieur du flux d'autorisation de paiement, dans le **budget de latence de 100 ms à p99**. Les features de vélocité viennent du **store en ligne Redis** (sous 25 ms) ; le logging de décision est **asynchrone** (Kafka), hors chemin critique.
2. **Fail-open** : si le modèle est indisponible ou hors budget, le service **ne bloque jamais les paiements** — il dégrade vers une décision pilotée par le moteur de règles déterministes (`rules_engine.py`).
3. **Ledger de décisions** : chaque décision est enregistrée de façon immuable (version de modèle, snapshot de features, score, seuils, règles déclenchées, issue) — exigence de litige et de reconstruction des jeux d'entraînement.
4. **Réconciliation des labels** : les chargebacks, réclamations clients et résultats de revue sont joints aux décisions d'origine ; chaque transaction porte une `label_maturity_date`. Les **vintages non matures ne sont jamais labellisés négatifs**.
5. **Feature engineering point-in-time** : les features de vélocité (compteurs 1 h / 24 h / 7 j, `device_distinct_cards_24h`, …) sont reconstruites telles qu'au moment de la transaction — une fuite temporelle fait échouer le build (test dédié).
6. **Entraînement** : GBM avec tracking MLflow (coût attendu, capture de fraude, faux refus) et enregistrement dans le **MLflow Model Registry** (stage `Staging`). Les seuils `t_low` / `t_high` dérivent de la **matrice de coûts** et de la capacité de revue.
7. **Évaluation** : backtest sur vintages matures contre des *quality gates* (`MAX_EXPECTED_COST_PER_1K`, `MAX_FALSE_DECLINE_RATE`, `MIN_FRAUD_CAPTURE_RATE`, `MIN_REVIEW_PRECISION`) puis **promotion en Shadow**.
8. **Rollout staged** : shadow 7 jours → canary 5 % → 25 % → 100 %, avec garde-fous **agrégés et par segment** et rollback automatique en moins de 5 minutes.
9. **Monitoring** : technique (Prometheus/Grafana, p99 ≤ 100 ms), **métier** (coût net par 1 000 transactions, capture de fraude, faux refus, ratio de chargeback) et **adversarial** (frottement de frontière, rafales coordonnées, sondage, empoisonnement de features).
10. **Réentraînement automatique** : le drift (distributionnel et adversarial) déclenche un DAG Airflow qui relance le pipeline sur un **calendrier randomisé** et ne promeut un nouveau modèle qu'après shadow et canary.

Tout est automatisé par **4 DAGs Airflow**, **3 jobs GitHub Actions en CI** et **3 jobs en CD** (build, staging, production staged).

---

## Architecture

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

Flux de contrôle : le service de décision charge le modèle `Production` du registry MLflow et les features de vélocité depuis Redis ; ses décisions alimentent les métriques Prometheus, le ledger et la fenêtre de données `current` du drift Evidently ; si le drift (distributionnel ou signature adversarial) dépasse le seuil (`DRIFT_THRESHOLD`, défaut `0.3`), le DAG `retraining_pipeline` relance la boucle et ne promeut qu'un modèle passé par shadow et canary.

Déploiement : les images Docker construites par GitHub Actions (CD) sont déployées sur Kubernetes via **Kustomize** (base + overlays `staging` / `production`), avec HPA et rolling update sans interruption.

---

## Stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Orchestration | Apache Airflow 2.9.2 | Planification et enchaînement des DAGs (ingestion, réconciliation des labels, entraînement, réentraînement) |
| Streaming | Kafka | Événements de décision (asynchrones) + agrégation de vélocité |
| Store de features en ligne | Redis | Récupération des features de vélocité sous 25 ms |
| Versioning des données | DVC 3.x + remote MinIO (S3) | Snapshots versionnés — critique car les labels arrivent après l'entraînement |
| Stockage d'artefacts | MinIO | Bucket S3 pour le remote DVC, les artefacts MLflow et le ledger |
| Base de données | PostgreSQL 16 | Backend store MLflow, métadonnées Airflow, ledger de décisions |
| Tracking + Registry | MLflow 2.9+ | Expériences, artefacts, Model Registry (Staging / Shadow / Production / Archived) |
| Feature engineering | pandas / scikit-learn | Vélocité + correction point-in-time (pas de skew, pas de fuite) |
| Modèle | GBM (ensemble d'arbres à gradient boosté) | Score en quelques ms — contraint par le budget d'inférence de 20 ms |
| API de décision | FastAPI + Uvicorn (pydantic v2) | `/decide`, `/health`, `/metrics`, `/model-info` — fail-open, 100 ms p99 |
| Règles déterministes | `rules_engine.py` | Blocages, plafonds de vélocité, géographie — modifiables sans déploiement |
| Qualité des données | Great Expectations | Suite d'attentes déclarative (`dataset_suite`) |
| Monitoring infra | Prometheus + Grafana | Latence p99, débit, taux d'erreur, version servie, segments |
| Monitoring métier | Grafana | Coût net par 1 000 transactions, capture de fraude, faux refus |
| Monitoring modèle | Evidently + détecteurs adversariaux | Data drift, score drift, frottement de frontière, rafales, sondage |
| CI/CD | GitHub Actions | Lint, sécurité, validation, tests, build image, déploiement staged |
| Déploiement | Docker, Kubernetes + Kustomize | Base + overlays staging / production, HPA, shadow → canary → full |
| Conteneurisation | Docker (multi-stage) | Images `api`, `training`, `mlflow` |

---

## Structure du dépôt

```
.
├── airflow/
│   ├── dags/
│   │   ├── data_ingestion_dag.py       # ingestion + validation + DVC push (quotidien)
│   │   ├── label_reconciliation_dag.py # chargebacks/réclamations/revues → label_maturity_date
│   │   ├── training_pipeline.py        # validate → preprocess → features → train → threshold → evaluate → shadow → notify
│   │   └── retraining_pipeline.py      # short-circuit drift → réentraînement vintage-aware
│   └── plugins/
│       └── drift_sensor.py             # DriftDetectedSensor + plugin Airflow
├── docker/
│   ├── docker-compose.yml              # stack complète locale (MinIO, Postgres, Redis, Kafka, MLflow, Airflow, API, Prometheus, Grafana)
│   ├── Dockerfile.api                  # image de décision (multi-stage, non-root)
│   └── Dockerfile.training             # image de training (données montées, jamais intégrées)
├── mlflow/
│   ├── docker-compose.yml              # MLflow + Postgres + MinIO seuls
│   └── Dockerfile.mlflow               # serveur MLflow (tracking + registry)
├── k8s/
│   ├── base/                           # configmap, deployment (3 réplicas), hpa, service
│   └── overlays/
│       ├── staging/                    # 2 réplicas, namespace mlops-staging
│       └── production/                 # 5 réplicas, namespace mlops-production
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml              # scrape configs (job mlops-api)
│   │   └── alert_rules.yml             # règles d'alerte (latence p99, garde-fous, segments)
│   └── grafana/dashboards/
│       ├── business-metrics.json       # dashboard métier (coût net, capture, faux refus)
│       └── model-drift.json            # dashboard drift + signatures adversariales
├── .github/workflows/
│   ├── ci.yml                          # lint, security, data-validation, tests, docker-build
│   └── cd.yml                          # build+push GHCR, deploy staging, deploy production (staged)
├── src/
│   ├── api/                            # main.py, schemas.py, decision.py, rules_engine.py, metrics.py, model_loader.py
│   ├── data/                           # ingestion.py, preprocessing.py, validation.py
│   ├── features/                       # build_features.py, velocity_aggregator.py, point_in_time.py, feature_store.py
│   ├── models/                         # train.py, threshold.py, evaluate.py, promote.py, exploration.py
│   ├── streaming/                      # decision_consumer.py, label_reconciliation.py
│   └── monitoring/                     # drift_detection.py, adversarial_detectors.py, alerting.py
├── scripts/
│   └── generate_synthetic_data.py      # génération du dataset de fraude synthétique
├── great_expectations/expectations/
│   └── dataset_suite.json              # suite d'attentes déclarative
├── tests/                              # tests unitaires + intégration (dont test_point_in_time.py)
├── data/                               # raw / processed / features / training / monitoring (versionné DVC)
├── models/                             # model.pkl, artefacts, rapports d'évaluation
├── dvc.yaml                            # pipeline DVC : ingest → preprocess → build_features → build_training_set → train
├── dvc.lock                            # état verrouillé du pipeline DVC
├── Makefile                            # cibles de la plupart des commandes
├── requirements.txt                    # dépendances runtime
├── requirements-dev.txt                # dépendances dev/CI
├── .env.example                        # variables d'environnement (à copier en .env)
└── .pre-commit-config.yaml             # hooks pre-commit (ruff, black, bandit, …)
```

---

## Démarrage rapide

Prérequis : `python >= 3.10`, `make`, `docker` + `docker compose`, `git`.

### 1. Clone et installation

```bash
git clone <url-du-dépôt>
cd mlops-project-documentation
cp .env.example .env      # ajustez si besoin
make setup                # crée .venv et installe requirements-dev.txt + le package
```

### 2. Lancer la stack locale complète (docker compose)

```bash
make compose-up           # MinIO, Postgres, Redis, Kafka, MLflow, Airflow, API, Prometheus, Grafana
```

La commande est équivalente à :

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

| Service | URL | Identifiants par défaut |
|---|---|---|
| MinIO (S3) | http://localhost:9001 | `minio` / `minio123` |
| Redis (store de features) | `localhost:6379` | — |
| Kafka (événements de décision) | `localhost:9092` | — |
| MLflow (tracking + registry) | http://localhost:5000 | — |
| Airflow | http://localhost:8080 | `admin` / `admin` |
| API FastAPI | http://localhost:8000 | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | `admin` / `admin` |
| Postgres | `localhost:5432` | `mlflow` / `mlflow` |

> `make mlflow-up` démarre uniquement MLflow + Postgres + MinIO (voir `mlflow/docker-compose.yml`), utile en développement.

### 3. Pipeline de données et entraînement (sans Airflow)

```bash
make data                 # génère le dataset de fraude synthétique (data/external/transactions.parquet)
make ingest               # src/data/ingestion.py        → data/raw/transactions.parquet
make preprocess           # src/data/preprocessing.py    → data/processed/transactions.parquet
make validate             # src/data/validation.py       (Great Expectations)
make features             # src/features/build_features.py → data/features/*.parquet + config.json
make training-set         # src/features/point_in_time.py  (vintage-aware + test de fuite)
make train                # src/models/train.py          (tracking + registry → Staging)
make threshold            # src/models/threshold.py       (t_low / t_high depuis la matrice de coûts)
make evaluate             # src/models/evaluate.py       (backtest vintages matures, quality gates)
make promote              # src/models/promote.py        (Staging → Shadow)
```

Ou d'un seul coup avec DVC :

```bash
make dvc-repro            # dvc repro (rejoue uniquement les stages obsolètes)
```

Le pipeline DVC est déclaré dans `dvc.yaml` :

```
ingest  →  preprocess  →  build_features  →  build_training_set  →  train
```

Chaque stage produit des sorties versionnées : `data/raw/transactions.parquet`, `data/processed/transactions.parquet`, `data/features/features.parquet`, `data/features/features_config.json`, `data/training/train_vintage_aware.parquet`, `models/model.pkl`, `metrics.json`.

### 4. Versionner et pousser les données (DVC + MinIO)

Une fois la stack démarrée (MinIO accessible sur `localhost:9000`), le remote DVC est configuré dans `.dvc/config` (`s3://mlops-bucket/data`, endpoint `http://localhost:9000`) :

```bash
make dvc-push              # dvc push  → pousse les artefacts vers MinIO
make dvc-pull              # dvc pull  → les restaure localement
```

### 5. Tester l'API

```bash
make api                   # uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_8f3a1c", "timestamp": "2026-08-19T14:32:11Z",
    "card_hash": "a1b2c3d4e5f6", "card_bin": "424242",
    "device_id": "dev_77e1", "ip_address": "203.0.113.45",
    "merchant_id": "merchant_1042", "amount": 249.99, "currency": "EUR",
    "billing_country": "FR", "billing_zip": "75011",
    "shipping_country": "FR", "shipping_zip": "75011"
  }'
```

La référence complète de l'API est dans [`docs/api.md`](docs/api.md).

### 6. Qualité et tests

```bash
make test                  # pytest (tous les tests)
make lint                  # ruff check + black --check
make security              # bandit -r src -x tests
```

---

## Pipeline ML et orchestration

Détails complets dans [`docs/ml-pipeline.md`](docs/ml-pipeline.md).

| Étape | Script | Sortie principale |
|---|---|---|
| Validate | `src/data/validation.py` | Validité Great Expectations (`dataset_suite`) |
| Preprocess | `src/data/preprocessing.py` | `data/processed/transactions.parquet` |
| Build features | `src/features/build_features.py` | `data/features/features.parquet` + `features_config.json` (vélocité) |
| Build training set | `src/features/point_in_time.py` | `data/training/train_vintage_aware.parquet` (vintages + fuite) |
| Train | `src/models/train.py` | `models/model.pkl`, run MLflow, version registrée `Staging` |
| Threshold | `src/models/threshold.py` | `t_low` / `t_high` depuis la matrice de coûts + capacité de revue |
| Evaluate | `src/models/evaluate.py` | `models/evaluation/latest_report.json` (gates vintages matures) |
| Promote | `src/models/promote.py` | `models/evaluation/production_report.json`, version `Shadow` |

Les **4 DAGs Airflow** orchestrent cette boucle :

- `data_ingestion_dag` — quotidien à 02:00 (`0 2 * * *`) : `ingest_data → validate_data → version_data` (avec `dvc add` + `dvc push`).
- `label_reconciliation_dag` — quotidien à 03:00 : joint les chargebacks, réclamations et résultats de revue ; maintient `label_maturity_date`.
- `training_pipeline` — hebdomadaire (`@weekly`, **calendrier randomisé**) : `validate_data → preprocess → build_features → build_training_set → train_model → optimize_threshold → evaluate_model → deploy_shadow → notify_team` (le `run_id` MLflow passe par XCom).
- `retraining_pipeline` — déclenché par drift / signature adversarial (ou planifié randomisé) : `check_drift` (ShortCircuitOperator) → si drift détecté, relance le pipeline complet.

La promotion n'a lieu qu'après : gates sur vintages matures **et** 7 jours de shadow **et** canary avec garde-fous segmentés (`src/models/promote.py`). Les vintages non matures ne sont jamais labellisés négatifs.

---

## CI/CD

### CI — `.github/workflows/ci.yml`

Déclencheurs : push sur `main` et toute pull request. 6 jobs parallèles :

| Job | Commande / vérification |
|---|---|
| `lint` | `ruff check src airflow scripts` + `black --check --line-length 120` |
| `security` | `bandit -r src -x tests` — échec si une sévérité `HIGH` est trouvée |
| `data-validation` | `python src/data/validation.py` sur le dataset traité (fallback raw) |
| `unit-tests` | `pytest tests/unit` avec couverture (`--cov=src`) — **dont `test_point_in_time.py` : une tentative de fuite temporelle délibérée fait échouer le build** |
| `integration-tests` | pipeline E2E (ingest → … → evaluate) puis `pytest tests/integration -m integration` |
| `docker-build` | build des images `api` + `training`, scan **Trivy** (échec si `HIGH`/`CRITICAL`) |

### CD — `.github/workflows/cd.yml`

Déclencheur : push sur `main` limité aux chemins `src/**`, `docker/**`, `k8s/**`, `requirements*.txt`, `dvc.yaml`. 3 jobs :

1. **build-and-push** — tag d'image = SHA du commit (jamais `latest`) : `ghcr.io/<repo>-api:<sha>` et `ghcr.io/<repo>-training:<sha>`, poussées sur GHCR avec cache GHA.
2. **deploy-staging** — `kubectl apply -f` (via Kustomize, image injectée avec `kustomize edit set image`) dans l'environnement `staging`, attente du rollout, puis **smoke tests** (`/health` + une décision `/decide` sur l'endpoint staging).
3. **deploy-production** — environnement `production` avec **approbation manuelle** ; rollout en **shadow → canary → full** avec garde-fous et rollback automatique (voir [plus bas](#déploiement-du-modèle--shadow-puis-canary)) ; rolling update zéro-downtime puis vérification des pods et du HPA.

Secrets attendus dans GitHub : `KUBECONFIG_STAGING`, `KUBECONFIG_PRODUCTION`, `STAGING_API_URL` (plus `GITHUB_TOKEN` pour GHCR, automatique).

---

## Déploiement Kubernetes

Détails dans [`docs/deployment.md`](docs/deployment.md).

Structure Kustomize : `k8s/base` (ressources communes) + `k8s/overlays/{staging,production}`.

| Ressource | Valeurs `base` | `staging` | `production` |
|---|---|---|---|
| Réplicas | 3 | 2 | 5 |
| CPU request / limit | 200m / 1 | 200m / 1 | 500m / 2 |
| Mémoire request / limit | 512Mi / 1Gi | 512Mi / 1Gi | 1Gi / 2Gi |
| Namespace | — | `mlops-staging` | `mlops-production` |
| Tag d'image | `latest` | `staging` (remplacé en CD) | `production` (remplacé en CD) |

Le `base` comprend :
- un `Deployment` en RollingUpdate (`maxUnavailable: 0`, `maxSurge: 1`) avec probes de liveness/readiness sur `/health` (le mode `rules-only` ne fait pas échouer la readiness — fail-open), security context non-root, filesystem root en lecture seule ;
- un `Service` ClusterIP (port 80 → targetPort 8000) ;
- un **HPA** (`autoscaling/v2`) : 2 → 10 réplicas, CPU 70 %, mémoire 80 %, fenêtre de stabilisation du scale-down de 300 s ;
- un `ConfigMap` (`MLFLOW_TRACKING_URI=http://mlflow.mlops.svc.cluster.local:5000`, `MLFLOW_MODEL_NAME=fraud_model`, `REDIS_URL`, `KAFKA_BOOTSTRAP_SERVERS`, `RELOAD_INTERVAL=60`, `LOG_LEVEL=info`) et un `Secret` optionnel `mlops-secrets`.

> **Latence** : Redis et le service de décision doivent être co-localisés pour tenir le budget réseau de 10 ms. Le budget p99 de 100 ms est un **garde-fou de rollback** : p99 > 100 ms pendant 5 minutes → rollback immédiat.

Build manuel des images :

```bash
make docker-build-api        # docker build -f docker/Dockerfile.api -t mlops-api:local .
make docker-build-training    # docker build -f docker/Dockerfile.training -t mlops-training:local .
```

---

## Déploiement du modèle : shadow, puis canary

En fraude, les métriques hors ligne ne prédisent pas les performances en ligne : un modèle ne va jamais directement en production.

| Étape | Durée | Trafic | Condition de passage |
|---|---|---|---|
| Shadow | 7 jours | 100 % scoré, 0 % actionné | Distribution des scores saine ; accord de décision avec le champion dans la bande attendue ; latence dans le budget |
| Canary | 24 heures | 5 % | Taux d'approbation à ±2 % du champion ; pas de régression de latence ; pas d'effondrement de segment |
| Ramp | 48 heures | 25 % | Taux de fraude non élevé ; proxies de faux refus stables |
| Full | — | 100 % | Signature manuelle du responsable fraude |

**Déclencheurs de rollback automatique** (évalués en continu) :

```
chute du taux d'approbation > 3 points vs champion   → rollback immédiat
latence p99 > 100 ms pendant 5 minutes               → rollback immédiat
taux de refus d'un segment top-20 pays/BIN > 2×      → rollback immédiat
taux d'erreur > 0,5 %                                → rollback immédiat
```

Le déclencheur **par segment** est essentiel : un modèle peut tenir les métriques agrégées tout en refusant presque tout un pays à cause d'un bug d'encodage rare — le monitoring agrégé seul laisserait l'incident durer des jours.

---

## Monitoring

Détails dans [`docs/monitoring.md`](docs/monitoring.md).

- **Prometheus** (`monitoring/prometheus/prometheus.yml`) scrape le job `mlops-api` sur `/metrics` (`api:8000` et `host.docker.internal:8000` en local) toutes les 15 s.
- **Métriques** exposées par `src/api/metrics.py` : `http_requests_total`, `http_request_duration_seconds` (instrumentator FastAPI), `decision_latency_seconds` (p50/p95/**p99**), `decision_score` (histogramme des scores), `decisions_total` (par palier et version de modèle), `approval_rate_by_segment` / `decline_rate_by_segment` (garde-fous de canary), `model_mode` (fail-open actif), `mlops_model_version`.
- **Règles d'alerte** (`alert_rules.yml`) : `HighDecisionLatency` (**p99 > 100 ms, 5 min → rollback**), `HighAPIErrorRate` (**> 0,5 %, 5 min → rollback**), `ApprovalRateDrop` (> 3 points → rollback), `SegmentDeclineRate` (segment top-20 > 2× → rollback), `APIInstanceDown`, `ModelPredictionShift`, `FailOpenActive`.
- **Dashboards Grafana** : `business-metrics` (coût net par 1 000 transactions, capture de fraude, faux refus, ratio de chargeback, taux/précision de revue — le tableau de bord exécutif), `api-performance` (latence p50/p95/p99, débit par palier, taux d'erreur, segments), `model-drift` (score de drift global, seuil 0.3, distribution des scores, **frottement de frontière, rafales coordonnées, sondage**).
- **Drift Evidently** (`src/monitoring/drift_detection.py`) : compare la fenêtre de production (`data/monitoring/current.csv`) à la référence d'entraînement (`data/monitoring/reference.csv`). Score = fraction de features en drift ; `drift_detected` si score > `DRIFT_THRESHOLD` (0.3). Rapport JSON + HTML dans `data/monitoring/`.
- **Détecteurs adversariaux** (`src/monitoring/adversarial_detectors.py`) : le drift distributionnel est passif — en fraude, l'attaquant sonde activement la frontière. Détecteurs dédiés : frottement de frontière (densité de scores juste sous `t_low`), sondage, empoisonnement de features, rafales coordonnées.
- **Alerting** (`src/monitoring/alerting.py`) : écrit toujours un log local (`data/monitoring/alerts/alerts.jsonl`) et pousse vers Slack si `SLACK_WEBHOOK_URL` est défini.

```bash
make drift        # python src/monitoring/drift_detection.py
make monitor      # affiche l'URL Grafana
```

---

## Risques honnêtes

La spécification complète détaille les risques (§24 de `mlops-project-documentation.md`). L'essentiel :

- **L'accès aux données est le vrai blocage.** Les données de transactions de cartes sont dans le périmètre **PCI-DSS** — personne ne les confie pour un projet de ce type. Ce dépôt démontre l'architecture sur un **jeu synthétique de substitution** : légitime comme démonstration, mais n'importe qui du secteur des paiements reconnaîtra que l'équilibre des classes, les features disponibles et les dynamiques adversariales d'un dataset public ne représentent pas la production. Ne pas revendiquer de performances de fraude de production à partir de ce dépôt.
- **L'échantillon d'exploration coûte de l'argent, visiblement.** Approuver aléatoirement 0,5 % des refus (plafonné en valeur) achète des labels non biaisés dans la région de décision. Correct et nécessaire — et il sera toujours le premier poste questionné : accord écrit, ligne de reporting séparée, plafond dur.
- **Les règles ne disparaîtront jamais.** Le moteur de règles est construit dès le premier jour, versionné, testé, et l'équipe fraude peut le modifier sans déploiement — une entrée de liste de blocage doit être effective en secondes, pas dans un cycle de release.
- **Les faux refus sont invisibles sans instrumentation délibérée.** Les pertes de fraude arrivent comme chargebacks ; un client à tort refusé part simplement et n'est jamais compté. Mesure par proxy (retry, contacts service client, taux de commandes ultérieures, échantillon d'exploration) — un système qui ne mesure pas ce coût s'optimise vers le refus de tout.
- **Les adversaires s'adaptent à la défense**, y compris au calendrier de réentraînement : calendrier randomisé, architecture et seuils traités comme information sensible.

---

## Documentation détaillée

| Document | Contenu |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | Architecture en couches et flux de données complet |
| [`docs/deployment.md`](docs/deployment.md) | Déploiement local, remote DVC, Kubernetes, GitHub Actions, rollout staged |
| [`docs/ml-pipeline.md`](docs/ml-pipeline.md) | Pipeline ML : validate → preprocess → features point-in-time → vintage-aware → train → threshold → evaluate → promote |
| [`docs/api.md`](docs/api.md) | Référence API : `/decide` (3 paliers, fail-open), `/health`, `/metrics`, `/model-info` |
| [`docs/monitoring.md`](docs/monitoring.md) | Prometheus, alertes, garde-fous, dashboards, drift Evidently, détecteurs adversariaux |
| [`mlops-project-documentation.md`](mlops-project-documentation.md) | Spécification technique complète du projet (conception) |

---

## Dépannage

| Problème | Cause probable | Solution |
|---|---|---|
| `make compose-up` échoue | Port déjà occupé | `docker compose -f docker/docker-compose.yml down` puis relancer ; vérifier les ports 5000/8080/8000/9090/3000 |
| API renvoie `500 decision failed` | Modèle indisponible (registry vide ou `model.pkl` absent) | Lancer `make train` puis `make evaluate` et `make promote`, ou fournir `MLFLOW_MODEL_URI` — le service répond de toute façon en mode `rules-only` |
| `/health` renvoie `degraded` / `mode: rules-only` | Le modèle n'a pas pu être chargé au démarrage | Vérifier `MLFLOW_TRACKING_URI` et le registry ; relancer le conteneur API — les paiements ne sont pas bloqués (fail-open) |
| Latence p99 > 100 ms | Redis non démarré, features calculées dans la requête, ou HPA trop lent | Vérifier `REDIS_URL` ; vérifier que les compteurs de vélocité sont dans Redis et pas en base synchrone ; dimensionner le HPA |
| `dvc push` échoue | MinIO non démarré ou identifiants incohérents | Vérifier `.env` (`MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD`) et `.dvc/config` |
| Validation échoue en CI | Le dataset ne respecte pas `dataset_suite.json` | Exécuter `make validate` pour voir les expectations en échec |
| Airflow n'exécute pas les DAGs | DAGs non activés ou `dags_folder` incorrect | Activer les DAGs dans l'UI (http://localhost:8080) ; le folder est `/opt/airflow/dags` |
| Drift déclenché à tort | Seuil trop sensible | Augmenter `DRIFT_THRESHOLD` dans `.env` (défaut `0.3`) |
| `ruff` échoue sur une ligne | Ligne > 120 caractères | `ruff check --fix .` puis `black --line-length 120 .` |
| Conteneur API non healthy | Probe `/health` en échec (processus mort) | `docker logs mlops-api` ; vérifier `MLFLOW_TRACKING_URI` — le mode `rules-only` ne fait pas échouer la readiness |
| Grafana ne montre pas de données | Prometheus n'atteint pas l'API | Vérifier le job `mlops-api` dans Targets (http://localhost:9090/targets) |