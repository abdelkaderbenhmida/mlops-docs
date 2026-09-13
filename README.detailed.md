# MLOps — Plateforme de Prévision de la Demande (README détaillé)

> Documentation complète du code source : description du projet, outils, fonctionnement
> interne étape par étape, et procédure de test. Ce README complète la
> [README principale](./README.md) et la
> [spécification](./mlops-project-documentation.md).

---

## 1. Vue d'ensemble

Plateforme **MLOps à boucle fermée** pour la **prévision de la demande en distribution de
détail**. Elle couvre l'intégralité du cycle de vie d'un modèle : ingestion → versioning
des données → validation → feature engineering → entraînement → évaluation par portes →
promotion → service d'inférence → monitoring de drift → réentraînement automatique.

- **Tâche** : régression — prédire `units_sold` (unités vendues) par `(store_id, sku_id)`.
- **Modèle** : `RandomForestRegressor`.
- **Portes de qualité** : `R² ≥ 0,60` et `MAPE ≤ 25 %`.
- **Langue du code / docs** : français (nommage, commentaires, docs), code Python.

---

## 2. Stack technique et rôle de chaque outil

| Domaine | Outil | Rôle dans ce projet |
|---|---|---|
| Versioning des données | **DVC + MinIO** | `dvc.yaml` définit 4 étages (ingest→preprocess→build_features→train) ; MinIO est le remote S3-compatible |
| Validation des données | **Great Expectations** | Suites d'attentes sur le dataset ; exécutées en CI et dans Airflow avant entraînement |
| Tracking / Registry | **MLflow** (Postgres backend) | Log des runs, hyperparamètres, métriques, artefacts ; `demand_model` et promotion Staging→Production |
| Orchestration | **Apache Airflow** | 3 DAGs : ingestion nocturne, entraînement hebdomadaire, réentraînement quotidien par drift |
| Modèle | **scikit-learn RandomForestRegressor** | 300 arbres, profondeur 15 |
| Service d'inférence | **FastAPI + Pydantic** | `/predict`, `/health`, `/model-info`, `/metrics`, dashboard web |
| CI/CD | **GitHub Actions** | CI : lint, bandit, GE, tests ; CD : staging → production (approbation manuelle) |
| Déploiement | **Docker** (multi-stage) + **Kubernetes/Kustomize** | HPA, overlays staging/production |
| Monitoring | **Prometheus + Grafana** | Latence, erreurs, distribution des prévisions ; alertes |
| Détection de drift | **scipy (tests KS)** | Test de Kolmogorov-Smirnov par feature ; rapport + alerte Slack/journal |
| Backend DB | **PostgreSQL** | Backend MLflow et stockage des prédictions (via docker-compose) |
| Qualité / sécurité | **pytest, ruff, black, bandit** | 57 tests ; lint ; scan de sécurité |

---

## 3. Structure du dépôt (détaillée)

```
.
├── airflow/
│   ├── dags/
│   │   ├── data_ingestion_dag.py      # ingère → valide → dvc add/push (quotidien 02:00)
│   │   ├── training_pipeline.py       # valide→preprocess→features→train→evaluate→promote→notify (hebdo)
│   │   └── retraining_pipeline.py     # check_drift (short-circuit) → retrain si drift (quotidien)
│   └── plugins/
│       └── drift_sensor.py            # DriftDetectedSensor + DriftAlertPlugin
├── src/
│   ├── data/
│   │   ├── ingestion.py               # ingest d'un CSV source vers data/raw (idempotent)
│   │   ├── preprocessing.py           # coercition numérique, suppression invalides, units_sold ≥ 0
│   │   └── validation.py              # GE (fallback natif), ValidationError, validate()
│   ├── features/
│   │   ├── build_features.py          # FeatureTransformer (moyenne/écart-type, ordre fixe), config sérialisée
│   │   └── feature_store.py           # FeatureStore versionné (features_v{N}.parquet)
│   ├── models/
│   │   ├── train.py                   # RF + tracking MLflow + registry + reference.csv
│   │   ├── evaluate.py                # portes R²/MAPE, écrit latest_report.json (exit non nul si échec)
│   │   └── promote.py                 # promotion Staging→Production si portes + meilleur que prod
│   ├── api/
│   │   ├── main.py                    # app FastAPI (src.api.main:app)
│   │   ├── schemas.py                 # Pydantic strict, bornes, buckets, DemandPredictionRequest
│   │   ├── model_loader.py            # 3 niveaux : MLFLOW_MODEL_URI → registry → local model.pkl ; rechargement périodique
│   │   └── metrics.py                 # Prometheus via prometheus_fastapi_instrumentator
│   └── monitoring/
│       ├── drift_detection.py         # KS two-sample par feature (p<0.05 ET stat>0.1), seuil 0.3
│       └── alerting.py                # Slack + journal data/monitoring/alerts/alerts.jsonl
├── api/main.py                        # app parallèle PBS (voir §6) — ne fait pas partie du chemin principal
├── tests/
│   ├── unit/                          # 41 tests (api, features, preprocessing, evaluate, monitoring)
│   ├── data/test_data_quality.py      # 14 tests (alignés sur la suite GE)
│   └── integration/                   # 2 tests (pipeline end-to-end)
├── docker/
│   ├── Dockerfile.api                 # image API multi-stage, non-root
│   ├── Dockerfile.training            # image entraînement
│   └── docker-compose.yml             # MinIO, Postgres, MLflow, Airflow, API, Prometheus, Grafana
├── k8s/
│   ├── base/                          # Deployment (3 replicas), Service, ConfigMap, HPA
│   └── overlays/ (staging/, production/)
├── monitoring/
│   ├── prometheus/ (prometheus.yml, alert_rules.yml)
│   └── grafana/dashboards/ (api-performance.json, model-drift.json)
├── data/                              # external, raw, processed, features, monitoring
├── models/                            # model.pkl, evaluation/, artifacts/
├── ui/index.html                      # dashboard de prévision (vanilla JS + Chart.js)
├── scripts/generate_synthetic_data.py # génère data/raw/demand_data.csv (50 000 lignes, seed 42)
├── ml/data/generate_demand_data.py    # parseur PBS (lags, moyennes mobiles)
├── dvc.yaml                           # pipeline DVC 4 étages
├── Makefile                           # targets make setup/data/ingest/.../test
└── .github/workflows/ (ci.yml, cd.yml)
```

---

## 4. Fonctionnement pas à pas

### 4.1 Pipeline de données (DVC)

`dvc.yaml` définit une chaîne d'états (tous avec `cache: false`, donc versionnés git via hash) :

1. **ingest** — `src/data/ingestion.py` copie `data/external/dataset.csv` → `data/raw/dataset.csv`.
2. **preprocess** — `src/data/preprocessing.py` convertit les types numériques, supprime les
   lignes invalides et les `units_sold < 0`, écrit `data/processed/demand_data.csv`.
3. **build_features** — `FeatureTransformer` calcule moyenne/écart-type par feature (ordre fixe),
   sérialise la config dans `features_config.json` (garantie de parité entraînement/inférence),
   écrit `data/features/features.parquet` + versionne via `FeatureStore`.
4. **train** — `src/models/train.py` entraîne le RF, logue tout dans MLflow (params, `rmse`
   /`mae`/`r2`/`mape`, artefacts `feature_importances.png`, `predictions_vs_actual.png`),
   enregistre `demand_model` au registry, écrit `models/model.pkl` + `metrics.json` +
   `data/monitoring/reference.csv`.

Les **11 features** : `store_id, sku_id, day_of_week, month, is_holiday, price, promotion,
temperature, inventory_level, competitor_price, store_traffic`. Cible : `units_sold`.

### 4.2 Évaluation et ports (via `make evaluate`)

`src/models/evaluate.py` :
- Charge le modèle (registry → local) et le jeu de test (`reference.csv` prioritaire, fallback
  échantillon parquet).
- Calcule `rmse`, `mae`, `r2`, `mape` (MAPE hors `y=0`).
- Applique les portes par défaut : `min_r2 ≥ 0.60`, `max_mape ≤ 25.0` (surchargeables
  `--min-r2`/`--max-mape`).
- Écrit `models/evaluation/latest_report.json` ; **exit non nul si les portes échouent**.

### 4.3 Promotion conditionnelle (via `make promote`)

`src/models/promote.py` ne promeut un candidat **Staging → Production** que si :
- `gates_passed == true`
- `R² candidat ≥ R² production` (même jeu de test)
- l'ancienne version Production est archivée.
Écrit `models/evaluation/production_report.json`.

### 4.4 Service d'inférence (src API)

`src/api/main.py` (uvicorn `src.api.main:app`) :
- **`POST /predict`** — unitaire ou par lot ; validation Pydantic stricte (bornes), 422 si invalide ;
  réponse `{"predicted_units", "demand_bucket", "model_name", "model_version"}`. Buckets :
  `low ≤ 15`, `medium ≤ 35`, `high ≤ 60`, `very_high > 60`.
- **`GET /health`** — `{"status":"ok"|"degraded", model_name, model_version}`.
- **`GET /model-info`** — nom, version, métriques de production.
- **`GET /metrics`** — métriques Prometheus (`http_*`, `model_prediction_value`,
  `predictions_total`, `mlops_model_version`).
- **`GET /`** — dashboard web (`ui/index.html`).

**Chargement du modèle** (`model_loader.py`) — 3 niveaux, avec rechargement périodique
(`RELOAD_INTERVAL`, secondes) :
1. `MLFLOW_MODEL_URI` explicite si défini
2. Registry `models:/demand_model/Production`
3. Fallback local `models/model.pkl` (`version = "local"`)
Le modèle n'est jamais embarqué dans l'image.

### 4.5 Monitoring et drift (via `make drift`)

`src/monitoring/drift_detection.py` :
- Test **Kolmogorov-Smirnov à deux échantillons** par feature sur `reference.csv` vs données
  courantes.
- Drift par feature si `p < 0.05` **ET** `stat > 0.1`.
- Score global = fraction de features en dérive ; seuil `DRIFT_THRESHOLD` (défaut `0.3`).
- Écrit `data/monitoring/drift_report.json`.

`alerting.py` : `send_slack` (si `SLACK_WEBHOOK_URL`) + écrit toujours dans
`data/monitoring/alerts/alerts.jsonl`.

**Prometheus** scrape `/metrics` (15 s) ; règles dans `monitoring/prometheus/alert_rules.yml` :
`HighAPILatency` (p95 > 500 ms), `HighAPIErrorRate` (> 5 % 5xx), `APIInstanceDown`,
`ModelPredictionShift`. **Grafana** : dashboards provisionnés `api-performance.json` et
`model-drift.json`.

### 4.6 Boucle de réentraînement (Airflow)

| DAG | Planification | Étapes |
|---|---|---|
| `data_ingestion_dag` | quotidien 02:00 | ingest → validate (GE) → `dvc add` + `dvc push` (MinIO) |
| `training_pipeline` | hebdomadaire | validate → preprocess → features → train → evaluate → promote → notify |
| `retraining_pipeline` | quotidien | `check_drift` (short-circuit si pas de drift) → preprocess → features → train → evaluate → promote-si-meilleur → notify |

`DriftDetectedSensor` (airflow/plugins/drift_sensor.py) sonde `drift_report.json` et réussit
quand `drift_detected=true`.

---

## 5. Procédure de test

### 5.1 Tests automatisés (pytest)

```bash
make test          # ou : python -m pytest
# 57 tests : 41 unit, 14 data quality, 2 integration
```

Répartition des suites :
- `tests/unit/test_api.py` — health, predict (valide/lot/vide/absent → 422), metrics,
  model-info, schémas (bornes), buckets.
- `tests/unit/test_features.py` — `FeatureTransformer` (forme, numérique, round-trip config,
  parité train/inférence, ordre), `build_features`.
- `tests/unit/test_preprocessing.py` — coercition, suppression négatifs, colonnes, chemins.
- `tests/unit/test_evaluate.py` — métriques, rapport/portes, seuils par défaut, écriture
  fichier, priorité reference.csv.
- `tests/unit/test_monitoring.py` — détection KS (shift détecté / identique / end-to-end),
  colonnes features.
- `tests/data/test_data_quality.py` — 14 attentes alignées sur la suite GE.
- `tests/integration/test_pipeline_end_to_end.py` — pipeline complet + pipeline avec échec
  d'évaluation.

### 5.2 Validation de données (GE)

```bash
python src/data/validation.py --input data/raw/dataset.csv
# consortium : exécute la suite GE (fallback natif si la lib est absente)
```

### 5.3 Lint et sécurité

```bash
make lint          # ruff + black (limité à 120 colonnes)
make security      # bandit -r src -x tests -f json ; échec si HIGH
```

### 5.4 CI/CD (GitHub Actions)

- **`ci.yml`** (push/PR) : lint → security (bandit) → data-validation (GE) → unit-tests →
  integration-tests → docker-build (+ Trivy HIGH/CRITICAL).
- **`cd.yml`** (merge sur `main` + chemins src/docker/k8s/requirements/dvc) : build GHCR
  taguée au sha (jamais `latest`) → déploiement **staging** (Kustomize, rollout, smoke
  `/health`) → déploiement **production** derrière **approbation manuelle**.

### 5.5 Test manuel de l'API

```bash
make api                    # uvicorn src.api.main:app :8000
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"store_id":21,"sku_id":77,"day_of_week":5,"month":5,"is_holiday":0,
       "price":14.58,"promotion":1,"temperature":84.9,"inventory_level":59,
       "competitor_price":16.91,"store_traffic":758}'
# → {"predicted_units":52,"demand_bucket":"high","model_name":"demand_model","model_version":"local"}
```

### 5.6 Stack locale complète (Docker)

```bash
docker compose -f docker/docker-compose.yml up -d --build
# MinIO :9000/9001 · MLflow :5000 · Airflow :8080 · API :8000 · Prometheus :9090 · Grafana :3000
```

---

## 6. Points d'attention / risques connus

> Résultats d'un audit approfondi du code — à vérifier pour tout travail futur.

1. **Contradiction porte/artefacts** : la spécification §23 déclare que le modèle **échoue**
   aux portes (`R² ≈ −0.68`, `MAPE ≈ 49 %`), mais les artefacts committés
   (`models/evaluation/latest_report.json`) montrent `R² 0.747`, `MAPE 14.77`,
   `gates_passed: true`. Vérifier la cohérence avant toute conclusion.
2. **Pollution "churn classification"** : des artefacts de classification churn coexistent
   avec la plateforme régression (prévision) — `models/evaluation/production_report.json`
   (model_name `churn_model`, métriques f1/accuracy/roc_auc), `data/monitoring/current.csv`
   et `drift_report.html` en forme churn, defaults Docker `MLFLOW_MODEL_NAME=churn_model`,
   `.env.example` avec `MIN_F1/MIN_ACCURACY/MIN_ROC_AUC`, panneau Grafana "Churn prediction
   rate". Le chemin **principal** (`src/`) est bien la régression de demande.
3. **Deux moteurs de drift** : `drift_report.json` (scipy KS, seuil 0.3) et `drift_report.html`
   (Evidently, seuil 0.5) utilisent des algorithmes et seuils différents.
4. **Deux APIs documentées** : `src/api` (registry MLflow + `production_report`) et
   `api/main.py` racine (app PBS autonome, buckets 10000/5000/1000, port 8103). L'UI et
   certains docs ciblent l'app PBS, pas `src/api`.
5. **Secrets** : une clé privée SSH (`infra/.ssh/id_rsa`) est présente dans le worktree
   `.worktrees/proj4/` — ne jamais commiter de tels secrets.

---

## 7. Références

- [README principale](./README.md) — vue d'ensemble et démarrage rapide.
- [`mlops-project-documentation.md`](./mlops-project-documentation.md) — spécification
  technique complète (architecture, composants, DoD, risques, roadmap).
- [`docs/api.md`](./docs/api.md) — référence complète de l'API.
- [`docs/architecture.md`](./docs/architecture.md) — architecture en couches.
- [`docs/deployment.md`](./docs/deployment.md) — déploiement Docker/K8s/CI-CD.
- [`docs/monitoring.md`](./docs/monitoring.md) — monitoring, drift, alerting.
- [`docs/ml-pipeline.md`](./docs/ml-pipeline.md) — pipeline ML détaillé.
