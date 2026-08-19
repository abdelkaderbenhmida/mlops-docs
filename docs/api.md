# Référence API de prévision de la demande

Le service d'inférence FastAPI (`src/api/main.py`) sert le modèle de **prévision de la demande** (`demand_model`, RandomForestRegressor) : pour un couple magasin/SKU et un jour donné, il prédit le nombre d'unités vendues (`units_sold`). Il est servi par Uvicorn (`make api`, ou l'image `mlops-api` sur le port 8000).

Le modèle est chargé depuis le **MLflow Model Registry** (`models:/demand_model/Production`) via `src/api/model_loader.py`, avec fallback local `models/model.pkl` (version `local`). Les mêmes transformations de features qu'à l'entraînement sont appliquées à l'inférence, via le `FeatureTransformer` reconstruit depuis `data/features/features_config.json` (parité entraînement/inférence).

**Base URL** : `http://localhost:8000` (local) — `http://<endpoint-staging>/` ou `http://<endpoint-production>/` (Kubernetes).

---

## 1. Endpoints

| Méthode | Chemin | Description |
|---|---|---|
| `GET` | `/health` | Liveness/readiness : état du service et modèle chargé |
| `POST` | `/predict` | Prévision de la demande (une entrée ou un lot) |
| `GET` | `/metrics` | Métriques Prometheus |
| `GET` | `/model-info` | Métadonnées du modèle servi (nom, version, run, métriques de production) |
| `GET` | `/` | Dashboard web de prévision (`ui/index.html`) |
| `GET` | `/docs` | Documentation interactive OpenAPI (générée par FastAPI) |

---

## 2. `GET /health`

Probe de liveness/readiness utilisée par Kubernetes et le healthcheck Docker.

**Réponse `200 OK`** (modèle chargé) :

```json
{
  "status": "ok",
  "model_name": "demand_model",
  "model_version": "3"
}
```

**Réponse `200 OK`** (modèle non chargé — service dégradé mais vivant) :

```json
{
  "status": "degraded"
}
```

> `/health` renvoie toujours `200` ; la dégradation est signalée par `"status": "degraded"` (avec `model_name` et `model_version` nuls). Seule une panne du processus produit un échec de probe. Le service reste capable de répondre même si le modèle n'a pas pu être chargé.

---

## 3. `POST /predict`

Prévision unitaire ou par lot. Le corps est soit un objet `DemandPredictionRequest`, soit une **liste** d'objets (réponse alors en liste, même ordre). Champs identiques aux colonnes d'entraînement (parité entraînement/inférence).

### 3.1 Requête — cas unitaire

```json
{
  "store_id": 21,
  "sku_id": 77,
  "day_of_week": 5,
  "month": 5,
  "is_holiday": 0,
  "price": 14.58,
  "promotion": 1,
  "temperature": 84.9,
  "inventory_level": 59,
  "competitor_price": 16.91,
  "store_traffic": 758
}
```

### 3.2 Validation (Pydantic)

Toute valeur hors plage est rejetée en **`422`** avec un message d'erreur détaillé :

| Champ | Type | Plage valide |
|---|---|---|
| `store_id` | int | 1 – 100 |
| `sku_id` | int | 1 – 200 |
| `day_of_week` | int | 0 – 6 |
| `month` | int | 1 – 12 |
| `is_holiday` | int | 0 – 1 |
| `price` | float | 0 – 500 |
| `promotion` | int | 0 – 1 |
| `temperature` | float | −50 – 150 |
| `inventory_level` | int | 0 – 10 000 |
| `competitor_price` | float | 0 – 500 |
| `store_traffic` | int | 0 – 50 000 |

Un **lot vide** (`[]`) est rejeté en **`422`** avec `"empty prediction batch"`.

### 3.3 Réponse — cas unitaire

```json
{
  "predicted_units": 47,
  "demand_bucket": "high",
  "model_name": "demand_model",
  "model_version": "3"
}
```

| Champ | Type | Description |
|---|---|---|
| `predicted_units` | int | Prédiction arrondie de `units_sold` |
| `demand_bucket` | string | `low` · `medium` · `high` · `very_high` (voir §3.4) |
| `model_name` | string | Nom du modèle servi |
| `model_version` | string | Version (numéro de registry, URI explicite, ou `local` pour le fallback) |

### 3.4 Buckets de demande (`_demand_bucket` dans `schemas.py`)

| `predicted_units` | Bucket |
|---|---|
| ≤ 15 | `low` |
| ≤ 35 | `medium` |
| ≤ 60 | `high` |
| > 60 | `very_high` |

Les buckets alimentent le dashboard web (badges colorés) pour classer rapidement la prévision.

### 3.5 Requête — cas lot

```json
[
  { "store_id": 21, "sku_id": 77, "day_of_week": 5, "month": 5, "is_holiday": 0,
    "price": 14.58, "promotion": 1, "temperature": 84.9, "inventory_level": 59,
    "competitor_price": 16.91, "store_traffic": 758 },
  { "store_id": 5, "sku_id": 26, "day_of_week": 3, "month": 3, "is_holiday": 0,
    "price": 111.38, "promotion": 1, "temperature": 49.9, "inventory_level": 347,
    "competitor_price": 94.23, "store_traffic": 1963 }
]
```

**Réponse** :

```json
[
  { "predicted_units": 47, "demand_bucket": "high", "model_name": "demand_model", "model_version": "3" },
  { "predicted_units": 56, "demand_bucket": "high", "model_name": "demand_model", "model_version": "3" }
]
```

### 3.6 Erreurs

| Code | Cas |
|---|---|
| `422` | Champ manquant, hors plage, type incorrect, lot vide |
| `500` | Échec de la prédiction côté modèle (`{"detail": "prediction failed: …"}`) |
| `404` | `/` si `ui/index.html` absent |

---

## 4. `GET /model-info`

Métadonnées du modèle actuellement servi.

```json
{
  "model_name": "demand_model",
  "model_version": "3",
  "run_id": "f213a19e92c5486f83b4f65aab4534f5",
  "production_metrics": {
    "rmse": 22.85,
    "mae": 19.51,
    "r2": -0.12,
    "mape": 105.15
  }
}
```

| Champ | Description |
|---|---|
| `model_name` | Nom du modèle (défaut : `demand_model`, env `MLFLOW_MODEL_NAME`) |
| `model_version` | Version servie |
| `run_id` | Run MLflow d'origine (`null` si fallback local / URI explicite) |
| `production_metrics` | Métriques lues depuis `models/evaluation/production_report.json` si le fichier existe, sinon `null` |

---

## 5. `GET /metrics`

Métriques Prometheus (format texte Prometheus). Exposées par `src/api/metrics.py` (instrumentation `prometheus_fastapi_instrumentator` + métriques métier) :

| Métrique | Type | Description |
|---|---|---|
| `http_requests_total{method,path,status}` | compteur | Requêtes par endpoint et code de statut |
| `http_request_duration_seconds_bucket{method,path,le}` | histogramme | Latence par endpoint (p50/p95/p99 via `histogram_quantile`) |
| `model_prediction_value_bucket{le}` | histogramme | Distribution des `predicted_units` — buckets `(0, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150)` |
| `predictions_total{model_version}` | gauge | Nombre cumulé de requêtes de prévision par version du modèle |
| `mlops_model_version{model_name}` | gauge | Version du modèle actuellement servi (0 si version non numérique) |

La métrique `model_prediction_value` alimente le dashboard Grafana **Model Drift** et la règle d'alerte `ModelPredictionShift`.

---

## 6. `GET /`

Sert le dashboard web (`ui/index.html`) — « Demand Forecasting — Retail Supply Chain » : KPIs, graphiques (Chart.js) et badges de buckets (`low`/`medium`/`high`/`very_high`).

---

## 7. Chargement et rechargement du modèle

Ordre de résolution (`model_loader.py`) :

1. `MLFLOW_MODEL_URI` explicite (env) — si chargeable
2. **MLflow Model Registry** : `models:/demand_model/Production` — la version et le `run_id` sont lus via `MlflowClient.get_latest_versions(stages=["Production"])`
3. **Fallback local** : `models/model.pkl` (joblib) — version `local`

Le modèle est chargé **une fois au démarrage** (startup event). Si `RELOAD_INTERVAL` (env, secondes) est défini, le modèle est rechargé périodiquement ; un échec de rechargement conserve l'ancien bundle. Le `FeatureTransformer` est toujours reconstruit depuis `data/features/features_config.json` ; son absence fait échouer le chargement (`FileNotFoundError`).