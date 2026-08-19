# Architecture de la plateforme de prévision de la demande

Ce document décrit l'architecture en couches de la plateforme **MLOps de prévision de la demande** (prédiction de `units_sold` par magasin/SKU), le flux de données de bout en bout et le rôle de chaque composant. Il fait référence aux fichiers réels du dépôt et à la spécification `mlops-project-documentation.md`.

---

## 1. Vue d'ensemble

La plateforme est organisée en **couches** qui isolent les responsabilités :

```
┌─────────────────────────────────────────────────────────────────────────┐
│  COUCHE PRÉSENTATION / INTERFACES                                       │
│  - API FastAPI (src/api/) : prévision de la demande (unitaire / lot) +  │
│    observabilité                                                        │
│  - Dashboard web (ui/index.html, servi par GET /)                       │
│  - UI Airflow (8080), UI MLflow (5000), UI MinIO (9001), Grafana (3000) │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE ORCHESTRATION                                                   │
│  - Apache Airflow : 3 DAGs (ingestion, training hebdo, retraining drift)│
│  - GitHub Actions : CI (ci.yml) et CD (cd.yml, staging → production)    │
│  - DVC : pipeline de données reproductible (dvc.yaml)                   │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE APPLICATION / SERVICES                                          │
│  - Service d'inférence (src/api/ : main.py, schemas.py, model_loader.py,│
│    metrics.py)                                                          │
│  - Entraînement (src/models/ : train.py, evaluate.py, promote.py)       │
│  - Feature engineering (src/features/ : build_features.py,              │
│    feature_store.py)                                                    │
│  - Monitoring drift + alerting (src/monitoring/)                        │
│  - Kubernetes : Deployment + HPA + Service (k8s/)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE DONNÉES                                                         │
│  - data/external, data/raw, data/processed (CSV)                        │
│  - data/features : Parquet + features_config.json + schéma (DVC)        │
│  - data/monitoring : reference.csv, current.csv, drift_report.json,     │
│    alerts.jsonl                                                         │
│  - MinIO (S3) : remote DVC + artefacts MLflow                           │
│  - PostgreSQL 16 : backend store MLflow + métadonnées Airflow           │
│  - MLflow : tracking, Model Registry, artefacts                         │
├─────────────────────────────────────────────────────────────────────────┤
│  COUCHE OBSERVABILITÉ                                                   │
│  - Prometheus + Grafana (monitoring/)                                   │
│  - Règles d'alerte (monitoring/prometheus/alert_rules.yml)              │
│  - Alertes : alerting.py (Slack / journal local alerts.jsonl)           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Flux de données et de contrôle

### 2.1 Schéma complet

```
                    Données brutes (data/external/dataset.csv ou URL)
                                     │
                    ┌────────────────▼────────────────┐
                    │  ingestion.py (DVC stage ingest) │  idempotent, CSV/URL
                    │  → data/raw/                     │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  preprocessing.py               │  coercition numérique,
                    │  → data/processed/demand_data.csv│  dropna, units_sold ≥ 0
                    └────────────────┬────────────────┘
                                     │  validation.py (Great Expectations)
                    ┌────────────────▼────────────────┐
                    │  build_features.py              │  FeatureTransformer
                    │  → features.parquet + config    │  (mean/std par feature,
                    │    + feature_store (schéma)     │   FEATURE_ORDER fixe)
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  train.py (RandomForestRegressor)│  split 80/20 (seed 42)
                    │  → models/model.pkl, metrics.json│  MLflow tracking + registry
                    │  → data/monitoring/reference.csv │  (demand_model, version N)
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  evaluate.py                    │  portes : R² ≥ 0,60 ;
                    │  → latest_report.json           │  MAPE ≤ 25 % ; code ≠ 0
                    └────────────────┬────────────────┘  si portes non passées
                                     │
                    ┌────────────────▼────────────────┐
                    │  promote.py                     │  Staging → Production si
                    │  → production_report.json       │  portes OK et candidat ≥
                    └────────────────┬────────────────┘  champion ; ancienne
                                     │                   version → Archived
                    ┌────────────────▼────────────────┐
                    │  FastAPI (src/api/)             │  POST /predict (unitaire/lot)
                    │  model_loader : registry → local│  GET /health, /model-info,
                    │                                 │  /metrics, / (UI)
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  Monitoring                     │
                    │  Prometheus /metrics (15 s)     │  Grafana : api-performance,
                    │  drift KS vs reference.csv      │  model-drift
                    │  alerting : Slack + alerts.jsonl│
                    └────────────────┬────────────────┘
                                     │ drift_detected
                    ┌────────────────▼────────────────┐
                    │  Airflow retraining_pipeline    │  @daily, short-circuit
                    │  preprocess → features → train  │  → evaluate → promote si
                    │  (idem training_pipeline @weekly)│  meilleur → notify
                    └─────────────────────────────────┘
```

### 2.2 Étapes détaillées

1. **Ingestion** — `src/data/ingestion.py` : source résolue `--source` > env `INGESTION_SOURCE` > `data/external/dataset.csv` ; idempotent ; sortie `data/raw/dataset.csv`.
2. **Prétraitement** — `src/data/preprocessing.py` : coercition des colonnes numériques (`NUMERIC_COLUMNS`), suppression des lignes à valeurs numériques manquantes, filtre `units_sold >= 0`, normalisation de `date` ; sortie `data/processed/demand_data.csv`.
3. **Validation** — `src/data/validation.py` : suite d'attentes Great Expectations (`great_expectations/expectations/dataset_suite.json`), avec fallback intégré si la bibliothèque est absente ; code non nul si une attente échoue.
4. **Feature engineering** — `src/features/build_features.py` : `FeatureTransformer` calcule moyenne/écart-type (ddof=0) par feature ; transforme (coercition numérique, erreurs → 0.0) et sélectionne `FEATURE_ORDER` (11 features) ; cible `units_sold` ajoutée ; sorties `data/features/features.parquet` + `data/features/features_config.json`.
5. **Feature store** — `src/features/feature_store.py` : écrit `features_v{N}.parquet` + schéma documenté (`features_store_schema.json` : nom, type, description, plage attendue) ; versionné par DVC.
6. **Entraînement** — `src/models/train.py` : `RandomForestRegressor` (n_estimators=300, max_depth=15, min_samples_leaf=5, max_features=sqrt, random_state=42, n_jobs=-1) sur split 80/20 ; métriques `rmse`/`mae`/`r2`/`mape` ; run MLflow `demand-forecasting-training` (tags, params, métriques, artefacts `feature_importances.png` + `predictions_vs_actual.png` + config) ; `mlflow.sklearn.log_model(…, registered_model_name="demand_model")` ; persistance locale `models/model.pkl` + `metrics.json` ; écriture de la référence de drift `data/monitoring/reference.csv` (features + `prediction` + `units_sold` du jeu de test).
7. **Évaluation** — `src/models/evaluate.py` : jeu de test = `reference.csv` (prioritaire) sinon échantillon du dataset ; portes `min_r2=0.60` (`>=`) et `max_mape=25.0` (`<=`) ; rapport `models/evaluation/latest_report.json` ; sortie non nulle si portes non passées.
8. **Promotion** — `src/models/promote.py` : refuse si `gates_passed=false` (sauf `--force`) ; refuse si le candidat ne bat pas le modèle en production sur le même jeu de test ; archive l'ancienne version Production ; écrit `models/evaluation/production_report.json`.
9. **Service d'inférence** — `src/api/` : chargement unique au démarrage (`models:/demand_model/Production`, ou `MLFLOW_MODEL_URI`, ou fallback `models/model.pkl`) ; `FeatureTransformer` depuis `features_config.json` ; `POST /predict` (objet ou liste, 422 si invalide/vide) ; réponse `predicted_units` + `demand_bucket` (low ≤15 / medium ≤35 / high ≤60 / very_high >60) + modèle/version ; métriques Prometheus (`model_prediction_value`, `predictions_total{model_version}`, `mlops_model_version{model_name}`).
10. **Monitoring drift** — `src/monitoring/drift_detection.py` : test KS à deux échantillons par feature numérique (`p < 0.05` et `stat > 0.1`), score = fraction dérivée, seuil 0,3 (env `DRIFT_THRESHOLD`), rapport `data/monitoring/drift_report.json`. **Alerting** — `src/monitoring/alerting.py` : Slack (env `SLACK_WEBHOOK_URL`) + journal `data/monitoring/alerts/alerts.jsonl` toujours écrit.
11. **Orchestration** — Airflow : `data_ingestion_dag` (quotidien 02:00 : ingest → validate → DVC add/commit/push MinIO), `training_pipeline` (@weekly : validate → preprocess → features → train → evaluate → promote → notify), `retraining_pipeline` (@daily : `check_drift` short-circuit → si drift : preprocess → features → train → evaluate → promote-si-meilleur → notify) ; plugin `DriftDetectedSensor` sonde `drift_report.json`.

---

## 3. Composants du dépôt

| Composant | Fichiers | Rôle |
|---|---|---|
| Ingestion | `src/data/ingestion.py` | Récupère les données brutes (CSV/URL), idempotent |
| Prétraitement | `src/data/preprocessing.py` | Nettoyage du jeu de demande |
| Validation | `src/data/validation.py` + `great_expectations/` | Suites d'attentes déclaratives |
| Features | `src/features/build_features.py` | `FeatureTransformer`, `FEATURE_ORDER`, config sérialisée |
| Feature store | `src/features/feature_store.py` | Parquet versionné + schéma documenté |
| Entraînement | `src/models/train.py` | RandomForestRegressor + MLflow + registry |
| Évaluation | `src/models/evaluate.py` | Métriques + portes R²/MAPE |
| Promotion | `src/models/promote.py` | Staging → Production conditionnelle |
| API | `src/api/main.py`, `schemas.py`, `model_loader.py`, `metrics.py` | Service d'inférence + observabilité |
| Drift | `src/monitoring/drift_detection.py` | KS par feature + score global |
| Alerting | `src/monitoring/alerting.py` | Slack + journal local |
| Orchestration | `airflow/dags/`, `airflow/plugins/` | 3 DAGs + sensor de drift |
| Conteneurisation | `docker/` | Image API multi-stage non-root + stack complète |
| Kubernetes | `k8s/` | Deployment/Service/ConfigMap/HPA + overlays |
| CI/CD | `.github/workflows/` | CI qualité + CD staging → production approuvée |
| Monitoring | `monitoring/` | Prometheus (config + alert rules), dashboards Grafana |
| UI | `ui/index.html` | Dashboard de prévision servi par l'API |
| Données | `data/` | external → raw → processed → features → monitoring |
| Modèles | `models/` | `model.pkl`, artefacts, rapports d'évaluation |

---

## 4. Notes de conception

- **Parité entraînement/inférence** : le `FeatureTransformer` et son ordre de features sont sérialisés dans `features_config.json` ; `train.py` et `model_loader.py` le consomment tous deux. Testé (`test_train_inference_parity`).
- **MLflow optionnel au runtime** : entraînement et chargement API continuent en mode offline (modèle local + avertissement) si le serveur est injoignable.
- **Fallback local** : si le registry est injoignable, l'API sert `models/model.pkl` (version `local`) — le service ne tombe pas.
- **Zéro downtime** : RollingUpdate `maxUnavailable: 0`, probes `/health`, HPA 2–10 pods.
- **Sécurité** : secrets via `.env.example` (jamais commités), `secretRef` optionnel en Kubernetes, image non-root, bandit en CI.