# Pipeline ML — Plateforme de prévision de la demande

Ce document décrit le pipeline ML détaillé de la plateforme de prévision de la demande : données, feature engineering, entraînement, évaluation avec portes de qualité, promotion, et orchestration.

---

## 1. Vue d'ensemble

```
data/external/dataset.csv  (source, ou URL)
        │  ingestion.py            (DVC stage: ingest)
        ▼
data/raw/dataset.csv
        │  preprocessing.py        (DVC stage: preprocess)
        ▼
data/processed/demand_data.csv
        │  validation.py (Great Expectations)
        │  build_features.py       (DVC stage: build_features)
        ▼
data/features/features.parquet  +  features_config.json  +  schéma (feature_store)
        │  train.py                (DVC stage: train)
        ▼
models/model.pkl  +  metrics.json  +  MLflow run + registry (demand_model)
        │  evaluate.py   →  latest_report.json  (portes R² ≥ 0,60 ; MAPE ≤ 25 %)
        ▼
        │  promote.py    →  production_report.json (Staging → Production)
        ▼
API FastAPI (src/api/)  +  monitoring (reference.csv, drift, alertes)
```

---

## 2. Données

| Fichier | Rôle |
|---|---|
| `data/external/dataset.csv` | Source d'ingestion (ou URL) |
| `data/raw/dataset.csv` | Données brutes normalisées (idempotent) |
| `data/raw/demand_data.csv` | Jeu de démonstration : ventes par magasin/SKU |
| `data/processed/demand_data.csv` | Données nettoyées |

Colonnes du jeu de demande : `store_id, sku_id, date, day_of_week, month, is_holiday, price, promotion, temperature, inventory_level, competitor_price, store_traffic, units_sold` — **cible : `units_sold`**.

Prétraitement (`preprocessing.py`) : coercition des colonnes numériques, suppression des lignes à valeurs manquantes, filtre `units_sold >= 0`, normalisation de `date` (chaîne nettoyée).

Validation (`validation.py`) : suite d'attentes Great Expectations (`great_expectations/expectations/dataset_suite.json`) — nombre de lignes, non-nullité, plages, types. Fallback intégré si la bibliothèque absente (la validation tourne toujours, y compris en CI). Code non nul si une attente échoue.

---

## 3. Feature engineering (`src/features/build_features.py`)

### 3.1 Features (11)

```python
FEATURE_ORDER = [
    "store_id", "sku_id", "day_of_week", "month", "is_holiday",
    "price", "promotion", "temperature", "inventory_level",
    "competitor_price", "store_traffic",
]
TARGET_FEATURE = "units_sold"
```

### 3.2 `FeatureTransformer`

- `fit(df)` : moyenne et écart-type (ddof=0) par feature numérique → `numeric_stats`
- `transform(df)` : coercition numérique (erreurs → 0.0), sélection `FEATURE_ORDER`
- `to_config()` / `from_config()` : sérialisation dans `data/features/features_config.json` (features, statistiques, ordre)

**Parité entraînement/inférence** : `train.py` et `model_loader.py` (API) consomment la même config — aucun training-serving skew. Testé par `tests/unit/test_features.py::test_train_inference_parity`.

### 3.3 Feature store (`src/features/feature_store.py`)

`data/features/features_v{N}.parquet` + schéma documenté (`features_store_schema.json` : nom, type, description, plage attendue), versionné par DVC. Tout modèle est traçable vers son snapshot de features.

---

## 4. Entraînement (`src/models/train.py`)

Modèle : **RandomForestRegressor** (scikit-learn).

```python
DEFAULT_PARAMS = {
    "n_estimators": 300,
    "max_depth": 15,
    "min_samples_leaf": 5,
    "max_features": "sqrt",
    "random_state": 42,
    "n_jobs": -1,
}
```

- Split **80/20** (`train_test_split(test_size=0.2, random_state=42)`)
- Métriques : `rmse`, `mae`, `r2`, `mape` (MAPE hors `y = 0`) + `train_size`/`test_size`
- MLflow (run `demand-forecasting-training`) : tags (`model_name=demand_model`, `task=demand_forecasting`), params, métriques, artefacts (`feature_importances.png` top-20, `predictions_vs_actual.png`, `features_config.json`)
- `mlflow.sklearn.log_model(…, registered_model_name="demand_model", input_example=X_test.iloc[[0]])`
- Persistance locale : `models/model.pkl` (joblib) + `metrics.json`
- Référence de drift : `data/monitoring/reference.csv` (features + `prediction` + `units_sold` du jeu de test)

CLI : `python src/models/train.py [--data …] [--config …] [--model-output …] [--model-name …] [--n-estimators …] [--max-depth …] [--min-samples-leaf …] [--seed …]`

> MLflow est **optionnel** : serveur injoignable → entraînement offline (avertissement), persistance locale intacte.

---

## 5. Évaluation (`src/models/evaluate.py`)

### 5.1 Jeu de test

1. `data/monitoring/reference.csv` (prioritaire, s'il existe) — même jeu que l'entraînement
2. Sinon : échantillon aléatoire du dataset de features (max 5 000 lignes, seed 42)

### 5.2 Métriques

`rmse`, `mae`, `r2`, `mape` (MAPE calculé sur `y ≠ 0`), `n_samples`.

### 5.3 Portes de qualité

| Porte | Seuil | Direction |
|---|---|---|
| `min_r2` | 0,60 | `r2 >= 0.60` |
| `max_mape` | 25,0 | `mape <= 25.0` |

Surchargeables en CLI (`--min-r2`, `--max-mape`). Rapport écrit dans `models/evaluation/latest_report.json` :

```json
{
  "model_uri": "local:models/model.pkl",
  "run_id": null,
  "metrics": { "rmse": 25.1, "mae": 21.12, "r2": -0.68, "mape": 49.42, "n_samples": 100 },
  "thresholds": { "min_r2": 0.6, "max_mape": 25.0 },
  "gates": { "min_r2": { "metric": "r2", "value": 0.6, "direction": ">=" },
             "max_mape": { "metric": "mape", "value": 25.0, "direction": "<=" } },
  "gates_passed": false
}
```

`gates_passed=false` → **code de sortie non nul** (bloque le pipeline/CI). Le dernier rapport du dépôt ne passe pas les portes (voir [état actuel](#8-état-actuel)).

---

## 6. Promotion (`src/models/promote.py`)

Conditions de promotion Staging → Production :

1. `latest_report.json` existe et `gates_passed=true` — sinon `RuntimeError` (contournable `--force`, déconseillé)
2. Une version `Staging` existe dans le registry pour `demand_model`
3. Le candidat **bat le modèle en production** sur le même jeu de test — sinon refus (contournable `--force`)
4. L'ancienne version Production est archivée (`Archived`)
5. `models/evaluation/production_report.json` est écrit (nom, version, run_id, métriques) — lu par `/model-info` et les dashboards

---

## 7. Orchestration (Airflow)

| DAG | Planification | Tâches |
|---|---|---|
| `data_ingestion_dag` | `0 2 * * *` | `ingest` → `validate` (GE) → `dvc add` + `dvc commit` + `dvc push` (si remote configuré) |
| `training_pipeline` | `@weekly` | `validate` → `preprocess` → `build_features` → `train` → `evaluate` → `promote` → `notify` |
| `retraining_pipeline` | `@daily` | `check_drift` (short-circuit) → si drift : `preprocess` → `build_features` → `train` → `evaluate` → `promote-si-meilleur` → `notify` |

Mécanismes :
- `run_id` MLflow transmis de `train` à `evaluate` via **XCom**
- Échec de tâche → `send_alert(severity="critical")` (Slack si configuré + journal local)
- Plugin `DriftDetectedSensor` (`airflow/plugins/drift_sensor.py`) : sonde `drift_report.json` (env `DRIFT_REPORT_PATH`), réussit si `drift_detected=true`
- Le DAG `retraining_pipeline` n'exécute le réentraînement **que** si le drift est détecté (short-circuit)

---

## 8. État actuel

Le dernier run d'entraînement (`metrics.json`) : `rmse=22.85, mae=19.51, r2=-0.12, mape=105.15, train_size=160, test_size=40`. Le dernier rapport d'évaluation (`latest_report.json`) : `rmse=25.10, mae=21.12, r2=-0.68, mape=49.42, n_samples=100, gates_passed=false`.

Le mécanisme de portes **bloque donc correctement** la promotion du modèle actuel : le pipeline est fonctionnel de bout en bout, mais le pouvoir prédictif du modèle doit être amélioré (features temporelles, hyperparamètres, modèle alternatif — voir la roadmap de la spécification) avant qu'un modèle ne passe en production.