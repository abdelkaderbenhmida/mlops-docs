# Plateforme MLOps End-to-End

> Infrastructure MLOps complète et reproductible : **Apache Airflow + DVC/MinIO + MLflow + FastAPI + Docker + GitHub Actions + Kubernetes + Prometheus/Grafana + Evidently**.

Cette plateforme illustre le cycle de vie complet d'un modèle de Machine Learning, de l'ingestion des données jusqu'à la détection de drift en production et au réentraînement automatique. Le cas d'usage démonstratif est la **prédiction de churn client** (classification binaire sur données tabulaires), mais l'architecture est agnostique au domaine.

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
- [Monitoring](#monitoring)
- [Documentation détaillée](#documentation-détaillée)
- [Dépannage](#dépannage)

---

## Présentation

Le projet démontre une boucle MLOps fermée et automatisée :

1. **Ingestion** des données brutes (CSV local ou URL) et **versioning** via DVC vers un remote MinIO (compatible S3).
2. **Validation** des données avec Great Expectations (suite déclarative `great_expectations/expectations/dataset_suite.json`).
3. **Feature engineering** reproductible grâce à un `FeatureTransformer` dont l'état ajusté est sérialisé en JSON et expédié avec le modèle — élimine le *training/serving skew*.
4. **Entraînement** d'un `RandomForestClassifier` avec tracking MLflow (hyperparamètres, métriques, matrice de confusion, importances de features) et enregistrement dans le **MLflow Model Registry** (stage `Staging`).
5. **Évaluation** contre des *quality gates* (`MIN_F1`, `MIN_ACCURACY`, `MIN_ROC_AUC`) puis **promotion** en `Production` si le candidat bat le modèle en place.
6. **Inférence** via une API FastAPI qui charge `models:/churn_model/Production` depuis le registry.
7. **Monitoring** technique (Prometheus/Grafana) et **monitoring métier** (drift Evidently).
8. **Réentraînement automatique** : la détection de drift déclenche un DAG Airflow qui relance le pipeline et ne promeut un nouveau modèle que s'il est meilleur.

Tout est automatisé par **3 DAGs Airflow**, **3 jobs GitHub Actions en CI** et **3 jobs en CD** (build, staging, production).

---

## Architecture

```
                    ┌──────────────────────────────────────────────────────┐
                    │                      Apache Airflow                 │
                    │  data_ingestion_dag · training_pipeline ·           │
                    │  retraining_pipeline (déclenché par drift)          │
                    └───────┬──────────────┬───────────────┬──────────────┘
                            │              │               │
              ingestion +   │   validate    │  train +       │  evaluate +
              DVC version   │  / features   │  register      │  promote
                            ▼               ▼               ▼
                    ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
                    │  DVC / MinIO  │  │    MLflow     │  │ Model Registry │
                    │  (données     │  │  (tracking +  │  │ Staging → Prod │
                    │  versionnées) │  │  artifacts)   │  └───────┬───────┘
                    └───────────────┘  └───────────────┘          │
                                                                  ▼
                                          ┌──────────────────────────────┐
                                          │   API FastAPI (inférence)     │
                                          │  /predict · /health · /metrics│
                                          │  /model-info                  │
                                          └──────┬──────────────┬─────────┘
                                                 │              │
                                     ┌────────────▼─────┐   ┌────▼───────────────┐
                                     │   Prometheus     │   │   Evidently +      │
                                     │  (métriques API) │   │  détection drift   │
                                     └────────┬─────────┘   └────┬───────────────┘
                                              ▼                  │
                                        ┌─────────────┐          │  signal de
                                        │   Grafana   │◀─────────┘  réentraînement
                                        │ dashboards  │               (Airflow)
                                        └─────────────┘
```

Flux de contrôle : l'API charge le modèle `Production` du registry MLflow ; ses prédictions alimentent les métriques Prometheus et la fenêtre de données `current` du drift Evidently ; si le score de drift dépasse le seuil (`DRIFT_THRESHOLD`, défaut `0.3`), le DAG `retraining_pipeline` relance la boucle et ne promeut qu'un modèle meilleur que celui en production.

Déploiement : les images Docker construites par GitHub Actions (CD) sont déployées sur Kubernetes via **Kustomize** (base + overlays `staging` / `production`), avec HPA et rolling update sans interruption.

---

## Stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Orchestration | Apache Airflow 2.9.2 | Planification et enchaînement des DAGs (ingestion, entraînement, réentraînement) |
| Versioning des données | DVC 3.x + remote MinIO (S3) | Snapshots versionnés de chaque jeu de données |
| Stockage d'artefacts | MinIO | Bucket S3 pour le remote DVC et les artefacts MLflow |
| Base de données | PostgreSQL 16 | Backend store MLflow (et métadonnées Airflow) |
| Tracking + Registry | MLflow 2.9+ | Expériences, artefacts, Model Registry (Staging / Production / Archived) |
| Feature engineering | pandas / scikit-learn | `FeatureTransformer` sérialisé en JSON (pas de skew) |
| Modèle | RandomForestClassifier (scikit-learn) | Classifieur de churn binaire |
| API d'inférence | FastAPI + Uvicorn (pydantic v2) | `/predict`, `/health`, `/metrics`, `/model-info` |
| Qualité des données | Great Expectations | Suite d'attentes déclarative (`dataset_suite`) |
| Monitoring infra | Prometheus + Grafana | Latence, débit, taux d'erreur, version servie |
| Monitoring modèle | Evidently + scipy | Data drift & prediction drift, seuil `0.3` |
| CI/CD | GitHub Actions | Lint, sécurité, validation, tests, build image, déploiement |
| Déploiement | Docker, Kubernetes + Kustomize | Base + overlays staging / production, HPA |
| Conteneurisation | Docker (multi-stage) | Images `api`, `training`, `mlflow` |

---

## Structure du dépôt

```
.
├── airflow/
│   ├── dags/
│   │   ├── data_ingestion_dag.py   # ingestion + validation + DVC push (quotidien)
│   │   ├── training_pipeline.py    # validate → preprocess → features → train → evaluate → promote → notify
│   │   └── retraining_pipeline.py  # short-circuit drift → réentraînement complet
│   └── plugins/
│       └── drift_sensor.py         # DriftDetectedSensor + plugin Airflow
├── docker/
│   ├── docker-compose.yml          # stack complète locale (8 services)
│   ├── Dockerfile.api              # image d'inférence (multi-stage, non-root)
│   └── Dockerfile.training         # image de training (données montées, jamais intégrées)
├── mlflow/
│   ├── docker-compose.yml          # MLflow + Postgres + MinIO seuls
│   └── Dockerfile.mlflow           # serveur MLflow (tracking + registry)
├── k8s/
│   ├── base/                       # configmap, deployment (3 réplicas), hpa, service
│   └── overlays/
│       ├── staging/                # 2 réplicas, namespace mlops-staging
│       └── production/             # 5 réplicas, namespace mlops-production
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml          # scrape configs (job mlops-api)
│   │   └── alert_rules.yml         # 4 règles d'alerte
│   └── grafana/dashboards/
│       ├── api-performance.json    # dashboard performance API
│       └── model-drift.json        # dashboard drift modèle
├── .github/workflows/
│   ├── ci.yml                      # lint, security, data-validation, tests, docker-build
│   └── cd.yml                      # build+push GHCR, deploy staging, deploy production
├── src/
│   ├── api/                        # main.py, schemas.py, metrics.py, model_loader.py
│   ├── data/                       # ingestion.py, preprocessing.py, validation.py
│   ├── features/                   # build_features.py, feature_store.py
│   ├── models/                     # train.py, evaluate.py, promote.py
│   └── monitoring/                 # drift_detection.py, alerting.py
├── scripts/
│   └── generate_synthetic_data.py  # génération du dataset churn synthétique
├── great_expectations/expectations/
│   └── dataset_suite.json          # suite d'attentes déclarative
├── tests/                          # tests unitaires + intégration
├── data/                           # raw / processed / features / monitoring (versionné DVC)
├── models/                         # model.pkl, artefacts, rapports d'évaluation
├── dvc.yaml                        # pipeline DVC : ingest → preprocess → build_features → train
├── dvc.lock                        # état verrouillé du pipeline DVC
├── Makefile                        # cibles de la plupart des commandes
├── requirements.txt                # dépendances runtime
├── requirements-dev.txt            # dépendances dev/CI
├── .env.example                    # variables d'environnement (à copier en .env)
└── .pre-commit-config.yaml         # hooks pre-commit (ruff, black, bandit, …)
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
make compose-up           # MinIO, Postgres, MLflow, Airflow, API, Prometheus, Grafana
```

La commande est équivalente à :

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

| Service | URL | Identifiants par défaut |
|---|---|---|
| MinIO (S3) | http://localhost:9001 | `minio` / `minio123` |
| MLflow (tracking + registry) | http://localhost:5000 | — |
| Airflow | http://localhost:8080 | `admin` / `admin` |
| API FastAPI | http://localhost:8000 | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | `admin` / `admin` |
| Postgres | `localhost:5432` | `mlflow` / `mlflow` |

> `make mlflow-up` démarre uniquement MLflow + Postgres + MinIO (voir `mlflow/docker-compose.yml`), utile en développement.

### 3. Pipeline de données et entraînement (sans Airflow)

```bash
make data                 # génère le dataset churn synthétique (data/external/dataset.csv)
make ingest               # src/data/ingestion.py        → data/raw/dataset.csv
make preprocess           # src/data/preprocessing.py    → data/processed/dataset.csv
make validate             # src/data/validation.py       (Great Expectations)
make features             # src/features/build_features.py → data/features/*.parquet + config.json
make train                # src/models/train.py          (tracking + registry → Staging)
make evaluate             # src/models/evaluate.py       (quality gates)
make promote              # src/models/promote.py        (Staging → Production)
```

Ou d'un seul coup avec DVC :

```bash
make dvc-repro            # dvc repro (rejoue uniquement les stages obsolètes)
```

Le pipeline DVC est déclaré dans `dvc.yaml` :

```
ingest  →  preprocess  →  build_features  →  train
```

Chaque stage produit des sorties versionnées : `data/raw/dataset.csv`, `data/processed/dataset.csv`, `data/features/features.parquet`, `data/features/features_config.json`, `models/model.pkl`, `metrics.json`.

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
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Male", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
    "Tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
    "InternetService": "DSL", "OnlineSecurity": "No", "OnlineBackup": "Yes",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Month-to-month",
    "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check",
    "MonthlyCharges": 65.5, "TotalCharges": 786.0
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
| Preprocess | `src/data/preprocessing.py` | `data/processed/dataset.csv` |
| Build features | `src/features/build_features.py` | `data/features/features.parquet` + `features_config.json` |
| Train | `src/models/train.py` | `models/model.pkl`, run MLflow, version registrée `Staging` |
| Evaluate | `src/models/evaluate.py` | `models/evaluation/latest_report.json` (gates) |
| Promote | `src/models/promote.py` | `models/evaluation/production_report.json`, version `Production` |

Les **3 DAGs Airflow** orchestrent cette boucle :

- `data_ingestion_dag` — quotidien à 02:00 (`0 2 * * *`) : `ingest_data → validate_data → version_data` (avec `dvc add` + `dvc push`).
- `training_pipeline` — hebdomadaire (`@weekly`) : `validate_data → preprocess → build_features → train_model → evaluate_model → promote_model → notify_team` (le `run_id` MLflow passe par XCom).
- `retraining_pipeline` — quotidien (`@daily`) : `check_drift` (ShortCircuitOperator) → si drift détecté, relance `preprocess → build_features → train_model → evaluate_model → promote_model → notify_team`.

La promotion n'a lieu que si le candidat passe les gates **et** bat le modèle de production sur le même jeu de test (`src/models/promote.py`).

---

## CI/CD

### CI — `.github/workflows/ci.yml`

Déclencheurs : push sur `main` et toute pull request. 6 jobs parallèles :

| Job | Commande / vérification |
|---|---|
| `lint` | `ruff check src airflow scripts` + `black --check --line-length 120` |
| `security` | `bandit -r src -x tests` — échec si une sévérité `HIGH` est trouvée |
| `data-validation` | `python src/data/validation.py` sur le dataset traité (fallback raw) |
| `unit-tests` | `pytest tests/unit` avec couverture (`--cov=src`) |
| `integration-tests` | pipeline E2E (ingest → … → evaluate) puis `pytest tests/integration -m integration` |
| `docker-build` | build des images `api` + `training`, scan **Trivy** (échec si `HIGH`/`CRITICAL`) |

### CD — `.github/workflows/cd.yml`

Déclencheur : push sur `main` limité aux chemins `src/**`, `docker/**`, `k8s/**`, `requirements*.txt`, `dvc.yaml`. 3 jobs :

1. **build-and-push** — tag d'image = SHA du commit (jamais `latest`) : `ghcr.io/<repo>-api:<sha>` et `ghcr.io/<repo>-training:<sha>`, poussées sur GHCR avec cache GHA.
2. **deploy-staging** — `kubectl apply -f` (via Kustomize, image injectée avec `kustomize edit set image`) dans l'environnement `staging`, attente du rollout, puis **smoke tests** (`/health` + une prédiction `/predict` sur l'endpoint staging).
3. **deploy-production** — environnement `production` avec **approbation manuelle** ; rollout en rolling update zéro-downtime puis vérification des pods et du HPA.

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
- un `Deployment` en RollingUpdate (`maxUnavailable: 0`, `maxSurge: 1`) avec probes de liveness/readiness sur `/health`, security context non-root, filesystem root en lecture seule ;
- un `Service` ClusterIP (port 80 → targetPort 8000) ;
- un **HPA** (`autoscaling/v2`) : 2 → 10 réplicas, CPU 70 %, mémoire 80 %, fenêtre de stabilisation du scale-down de 300 s ;
- un `ConfigMap` (`MLFLOW_TRACKING_URI=http://mlflow.mlops.svc.cluster.local:5000`, `MLFLOW_MODEL_NAME=churn_model`, `RELOAD_INTERVAL=60`, `LOG_LEVEL=info`) et un `Secret` optionnel `mlops-secrets`.

Build manuel des images :

```bash
make docker-build-api        # docker build -f docker/Dockerfile.api -t mlops-api:local .
make docker-build-training    # docker build -f docker/Dockerfile.training -t mlops-training:local .
```

---

## Monitoring

Détails dans [`docs/monitoring.md`](docs/monitoring.md).

- **Prometheus** (`monitoring/prometheus/prometheus.yml`) scrape le job `mlops-api` sur `/metrics` (`api:8000` et `host.docker.internal:8000` en local) toutes les 15 s.
- **Métriques** exposées par `src/api/metrics.py` : `http_requests_total`, `http_request_duration_seconds` (instrumentator FastAPI), `model_prediction_value` (histogramme des probabilités prédites), `predictions_total` (jauge, par version de modèle), `mlops_model_version`.
- **Règles d'alerte** (`alert_rules.yml`) : `HighAPILatency` (p95 > 500 ms, 5 min), `HighAPIErrorRate` (> 5 % de 5xx, 5 min), `APIInstanceDown` (2 min), `ModelPredictionShift` (dérive de la distribution des prédictions, 6 h).
- **Dashboards Grafana** : `api-performance` (RPS, latence p50/p95/p99, taux d'erreur 5xx, version servie, débit par version) et `model-drift` (score de drift global, seuil 0.3, distribution cumulative des prédictions, taux de churn par seuil).
- **Drift Evidently** (`src/monitoring/drift_detection.py`) : compare la fenêtre de production (`data/monitoring/current.csv`) à la référence d'entraînement (`data/monitoring/reference.csv`). Score = fraction de features en drift ; `drift_detected` si score > `DRIFT_THRESHOLD` (0.3). Rapport JSON + HTML dans `data/monitoring/`.
- **Alerting** (`src/monitoring/alerting.py`) : écrit toujours un log local (`data/monitoring/alerts/alerts.jsonl`) et pousse vers Slack si `SLACK_WEBHOOK_URL` est défini.

```bash
make drift        # python src/monitoring/drift_detection.py
make monitor      # affiche l'URL Grafana
```

---

## Documentation détaillée

| Document | Contenu |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | Architecture en couches et flux de données complet |
| [`docs/deployment.md`](docs/deployment.md) | Déploiement local, remote DVC, Kubernetes, GitHub Actions |
| [`docs/ml-pipeline.md`](docs/ml-pipeline.md) | Pipeline ML : validate → preprocess → build_features → train → evaluate → promote |
| [`docs/api.md`](docs/api.md) | Référence API : `/predict`, `/health`, `/metrics`, `/model-info` |
| [`docs/monitoring.md`](docs/monitoring.md) | Prometheus, alertes, dashboards Grafana, drift Evidently, alerting |
| [`mlops-project-documentation.md`](mlops-project-documentation.md) | Spécification technique complète du projet (conception) |

---

## Dépannage

| Problème | Cause probable | Solution |
|---|---|---|
| `make compose-up` échoue | Port déjà occupé | `docker compose -f docker/docker-compose.yml down` puis relancer ; vérifier les ports 5000/8080/8000/9090/3000 |
| API renvoie `500 prediction failed` | Modèle non disponible (registry vide ou `model.pkl` absent) | Lancer `make train` puis `make evaluate` et `make promote`, ou fournir `MLFLOW_MODEL_URI` |
| `/health` renvoie `degraded` | Le modèle n'a pas pu être chargé au démarrage | Vérifier `MLFLOW_TRACKING_URI` et le registry ; relancer le conteneur API |
| `dvc push` échoue | MinIO non démarré ou identifiants incohérents | Vérifier `.env` (`MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD`) et `.dvc/config` |
| Validation échoue en CI | Le dataset ne respecte pas `dataset_suite.json` | Exécuter `make validate` pour voir les expectations en échec |
| Airflow n'exécute pas les DAGs | DAGs non activés ou `dags_folder` incorrect | Activer les DAGs dans l'UI (http://localhost:8080) ; le folder est `/opt/airflow/dags` |
| Drift déclenché à tort | Seuil trop sensible | Augmenter `DRIFT_THRESHOLD` dans `.env` (défaut `0.3`) |
| `ruff` échoue sur une ligne | Ligne > 120 caractères | `ruff check --fix .` puis `black --line-length 120 .` |
| Conteneur API non healthy | Probe `/health` en échec (modèle non chargé) | `docker logs mlops-api` ; vérifier `MLFLOW_TRACKING_URI` |
| Grafana ne montre pas de données | Prometheus n'atteint pas l'API | Vérifier le job `mlops-api` dans Targets (http://localhost:9090/targets) |
