# Pipeline ML

Le pipeline ML exécute la chaîne **validate → preprocess → build_features → train → evaluate → promote**. Il est déclaré dans `dvc.yaml` (stages `ingest`, `preprocess`, `build_features`, `train`) et orchestré de deux façons équivalentes : les cibles du `Makefile` en local, et les DAGs Airflow `training_pipeline` / `retraining_pipeline` en production.

---

## 1. Vue d'ensemble

```
data/external/dataset.csv
        │  Makefile: data  (scripts/generate_synthetic_data.py)
        ▼
 ingest (DVC stage)          src/data/ingestion.py
        ▼
 data/raw/dataset.csv  ───────▶  versionné + poussé vers MinIO (dvc add/push)
        ▼
 preprocess (DVC stage)      src/data/preprocessing.py
        ▼
 data/processed/dataset.csv
        ▼
 validate                    src/data/validation.py  (suite Great Expectations)
        ▼
 build_features (DVC stage)  src/features/build_features.py  (+ feature_store.py)
        ▼
 data/features/features.parquet + features_config.json
        ▼
 train (DVC stage)           src/models/train.py  →  MLflow Tracking + Registry (Staging)
        ▼
 models/model.pkl · metrics.json · data/monitoring/reference.csv
        ▼
 evaluate                    src/models/evaluate.py  →  models/evaluation/latest_report.json
        ▼   (gates: min_f1, min_accuracy, min_roc_auc)
 promote                     src/models/promote.py   →  Staging → Production
        ▼
 models/evaluation/production_report.json   (lu par l'API /model-info)
```

---

## 2. Les étapes en détail

### 2.1 Ingestion — `src/data/ingestion.py`

- Source résolue : argument `--source` > variable `INGESTION_SOURCE` > défaut `data/external/dataset.csv`.
- Accepte un chemin local ou une URL (`http://`, `https://`, `s3://`).
- `normalize()` : nettoie les noms de colonnes, les chaînes, applique les types attendus (`RAW_COLUMN_TYPES`) et convertit les montants (`$`, virgules, espaces).
- Sortie : `data/raw/dataset.csv`. Opération **idempotente**.
- DVC : stage `ingest` (`dvc.yaml`) / cible `make ingest`. Dans Airflow, la tâche `version_data` ajoute le fichier à DVC et pousse vers le remote.

### 2.2 Préprocessing — `src/data/preprocessing.py`

- Supprime l'identifiant `CustomerID` (`DROP_COLUMNS`).
- Force les types numériques (`NUMERIC_COLUMNS` : `Tenure`, `MonthlyCharges`, `TotalCharges`), supprime les lignes invalides (`dropna`) et filtre `Tenure >= 0`.
- Nettoie les colonnes catégorielles (`CATEGORICAL_COLUMNS`) et la cible `Churn`.
- Sortie : `data/processed/dataset.csv`. Idempotent. DVC stage `preprocess` / `make preprocess`.

### 2.3 Validation — `src/data/validation.py`

- Charge la suite déclarative `great_expectations/expectations/dataset_suite.json`.
- Exécute la validation via l'API Great Expectations (`from_pandas`), avec un **évaluateur léger intégré** en fallback pour que la validation tourne toujours (notamment en CI).
- Types d'expectations supportés : `expect_table_row_count_to_be_between`, `expect_column_values_to_not_be_null`, `expect_column_values_to_be_between`, `expect_column_values_to_be_in_set`, `expect_column_values_to_be_of_type`, `expect_column_values_to_not_match_regex`.
- Sortie : résumé `{total, passed, failed, results}`. **Quitte en erreur** (code 1) si au moins une expectation échoue (`ValidationError`).
- CLI : `python src/data/validation.py [--input data/processed/dataset.csv] [--suite ...] [--json-output ...]`.

### 2.4 Feature engineering — `src/features/build_features.py`

- Construit `FeatureTransformer` : 
  - features numériques : `Tenure`, `MonthlyCharges`, `TotalCharges` ;
  - features catégorielles encodées par mapping (`category_mappings`), valeurs inconnues → `-1` ;
  - features construites (`ENGINEERED_FEATURES`) : `charges_per_tenure = TotalCharges / (Tenure + 1)`, `tenure_years = Tenure / 12`, `num_services` (nombre de services à « Yes ») ;
  - statistiques numériques (moyenne, écart-type) pour la standardisation ultérieure.
- **Le même objet est réutilisé à l'inférence** (`ModelBundle.predict_proba` dans `src/api/model_loader.py`), ce qui garantit l'absence de *training/serving skew*.
- L'état ajusté est sérialisé dans `data/features/features_config.json` et loggé comme artefact MLflow (`mlflow.log_artifact`).
- Sorties (DVC stage `build_features`) : `data/features/features.parquet` + `features_config.json`. Cible : `make features`.
- Feature store : `src/features/feature_store.py` écrit des versions numérotées `features_v{N}.parquet` accompagnées d'un schéma documenté (`features_store_schema.json`), versionnées par DVC. CLI : `python src/features/feature_store.py --list-versions`.

### 2.5 Entraînement — `src/models/train.py`

- Hyperparamètres par défaut (`DEFAULT_PARAMS`) : `RandomForestClassifier(n_estimators=300, max_depth=15, min_samples_leaf=3, max_features="sqrt", class_weight="balanced", random_state=42)`. Surchargeables en CLI (`--n-estimators`, `--max-depth`, `--min-samples-leaf`, `--seed`).
- Split stratifié 80/20 (`train_test_split`, `random_state=42`).
- Métriques calculées : `accuracy`, `f1`, `precision`, `recall`, `roc_auc` + tailles train/test.
- **MLflow** (si un serveur est joignable) :
  - run `churn-training`, tags `model_name`, `git_commit`, `data_version` (`DVC_DATA_VERSION`), `registry_version` ;
  - log des params et des métriques ;
  - artefacts : matrice de confusion PNG, importances de features PNG, config du transformer ;
  - `mlflow.sklearn.log_model(..., registered_model_name="churn_model", input_example=...)` ;
  - transition de la version enregistrée vers le stage **Staging**.
- Sorties locales : `models/model.pkl` (DVC output), `metrics.json` (métrique DVC), et `data/monitoring/reference.csv` (jeu de test + prédictions + labels, base de référence du drift).
- En mode hors-ligne (pas de serveur MLflow), l'entraînement continue et ne fait que l'enregistrement local.

### 2.6 Évaluation — `src/models/evaluate.py`

- Résout le modèle candidat : `--run-id` (`runs:/<run_id>/model`) > `--model-uri` > `models/model.pkl` local.
- Charge le jeu de test : préfère `data/monitoring/reference.csv` (jeu retenu par `train.py`), sinon échantillon de 5000 lignes du dataset de features.
- Recalcule les 5 métriques et compare aux **quality gates** (`DEFAULT_THRESHOLDS`) :

| Gate | Variable d'env | Défaut |
|---|---|---|
| F1 ≥ | `MIN_F1` | `0.35` |
| Accuracy ≥ | `MIN_ACCURACY` | `0.70` |
| ROC-AUC ≥ | `MIN_ROC_AUC` | `0.72` |

- Écrit `models/evaluation/latest_report.json` avec `gates_passed`. **Quitte en erreur (code 1)** si `gates_passed` est faux — le pipeline s'arrête avant la promotion.

### 2.7 Promotion — `src/models/promote.py`

- Lit `latest_report.json` ; refuse de promouvoir si `gates_passed` est faux (sauf `--force`).
- Récupère la version `Staging` du registry et la compare au modèle `Production` courant (lecture de `production_report.json`) : le candidat doit avoir un **f1 ≥ f1 de production** (sauf `--force`).
- Transition : l'ancienne version `Production` passe en **Archived**, le candidat passe en **Production**, description mise à jour (f1 + run).
- Écrit `models/evaluation/production_report.json` — consommé par `/model-info` de l'API et par le dashboard Grafana (version servie).

---

## 3. Exécution

### 3.1 En local (Makefile / DVC)

```bash
make data                 # génère le dataset synthétique
make ingest               # stage 1
make preprocess           # stage 2
make validate             # qualité des données
make features             # stage 3
MLFLOW_TRACKING_URI=http://localhost:5000 make train     # stage 4
MLFLOW_TRACKING_URI=http://localhost:5000 make evaluate
MLFLOW_TRACKING_URI=http://localhost:5000 make promote
```

Ou équivalent DVC :

```bash
make dvc-repro            # dvc repro (stages obsolètes uniquement)
```

> `make setup` crée le venv et installe `requirements-dev.txt` ; `make install` installe `requirements.txt`.

### 3.2 Via Airflow

| DAG | Planification | Tâches |
|---|---|---|
| `data_ingestion_dag` | `0 2 * * *` (quotidien 02:00) | `ingest_data → validate_data → version_data` |
| `training_pipeline` | `@weekly` | `validate_data → preprocess → build_features → train_model → evaluate_model → promote_model → notify_team` |
| `retraining_pipeline` | `@daily` | `check_drift` (ShortCircuit) → si drift : `preprocess → build_features → train_model → evaluate_model → promote_model → notify_team` |

Points d'attention :
- Dans `training_pipeline`, le `run_id` est transmis de `train_model` à `evaluate_model` via **XCom**.
- `evaluate_model` lève une erreur si les gates échouent → arrêt avant promotion.
- Chaque tâche en échec déclenche `send_alert(..., severity="critical")` (`on_failure_callback`).
- La boucle de réentraînement est pilotée par le DAG `retraining_pipeline` et le plugin `DriftDetectedSensor` (`airflow/plugins/drift_sensor.py`) qui sonde `data/monitoring/drift_report.json`.

---

## 4. Traçabilité

Un modèle en production est relié à :

| Référence | Source |
|---|---|
| `run_id` MLflow | `train.py`, repris dans `production_report.json` |
| `model_version` (Registry) | `promote.py` |
| Commit Git | tag `git_commit` du run MLflow (`GIT_COMMIT`) |
| Version des données | tag `data_version` du run (`DVC_DATA_VERSION`), snapshot DVC épingle par commit Git |
| Config des features | artefact `features_config.json` loggé dans le run |
| Jeu d'évaluation | `data/monitoring/reference.csv` (identique pour comparer candidat vs production) |
