# Référence API d'inférence

L'API FastAPI (`src/api/main.py`) expose le modèle de churn en production. Elle est servie par Uvicorn (`make api`, ou l'image `mlops-api` sur le port 8000) et charge le modèle depuis le MLflow Model Registry (`models:/churn_model/Production`) via `src/api/model_loader.py`.

**Base URL** : `http://localhost:8000` (local) — `http://<endpoint-staging>/` ou `http://<endpoint-production>/` (Kubernetes).

---

## 1. Endpoints

| Méthode | Chemin | Description |
|---|---|---|
| `GET` | `/health` | Liveness/readiness : état du service et modèle chargé |
| `POST` | `/predict` | Prédiction de churn (une requête ou un lot) |
| `GET` | `/metrics` | Métriques Prometheus |
| `GET` | `/model-info` | Métadonnées du modèle servi (version, run, métriques de production) |
| `GET` | `/docs` | Documentation interactive OpenAPI (générée par FastAPI) |

---

## 2. `GET /health`

Probe de liveness/readiness utilisée par Kubernetes et le healthcheck Docker.

**Réponse `200 OK`** (modèle chargé) :

```json
{
  "status": "ok",
  "model_name": "churn_model",
  "model_version": "3"
}
```

**Réponse `200 OK`** (modèle indisponible — service dégradé mais vivant) :

```json
{
  "status": "degraded",
  "model_name": null,
  "model_version": null
}
```

> `/health` renvoie toujours `200` ; la dégradation est signalée par `"status": "degraded"`. Seule une panne du processus produit un échec de probe.

---

## 3. `POST /predict`

Prédit la probabilité de churn puis classe le client (`prediction = 1` si `probability >= 0.5`).

### 3.1 Requête — cas unitaire

Le corps est un objet JSON dont les clés correspondent **exactement aux colonnes d'entraînement** (aliases pydantic). Les noms snake_case sont aussi acceptés (`populate_by_name`), mais les alias sont recommandés pour éviter tout risque de *skew*.

```json
{
  "Gender": "Male",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "Tenure": 12,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 65.5,
  "TotalCharges": 786.0
}
```

**Réponse `200 OK`** :

```json
{
  "prediction": 1,
  "probability": 0.623,
  "model_name": "churn_model",
  "model_version": "3"
}
```

| Champ | Type | Description |
|---|---|---|
| `prediction` | int (0/1) | 1 si churn prédit, 0 sinon |
| `probability` | float [0,1] | Probabilité de churn |
| `model_name` | string | Nom du modèle dans le Registry |
| `model_version` | string | Version du modèle servi |

### 3.2 Requête — lot

Le corps est un **tableau JSON** d'objets (même schéma). Réponse : un tableau dans le même ordre.

```json
[
  { "Gender": "Male", "SeniorCitizen": 0, "Tenure": 12, "MonthlyCharges": 65.5, "TotalCharges": 786.0 },
  { "Gender": "Female", "SeniorCitizen": 1, "Tenure": 5, "MonthlyCharges": 99.0, "TotalCharges": 500.0 }
]
```

**Réponse `200 OK`** :

```json
[
  { "prediction": 1, "probability": 0.623, "model_name": "churn_model", "model_version": "3" },
  { "prediction": 0, "probability": 0.312, "model_name": "churn_model", "model_version": "3" }
]
```

### 3.3 Schéma des champs (Pydantic — `src/api/schemas.py`)

Contraintes et domaines appliqués par validation :

| Champ (alias) | Type | Contraintes |
|---|---|---|
| `Gender` | string | `Male` ou `Female` |
| `SeniorCitizen` | int | `0` ou `1` |
| `Partner`, `Dependents`, `PhoneService`, `PaperlessBilling` | string | `Yes` ou `No` |
| `MultipleLines` | string | `Yes`, `No`, `No phone service` |
| `InternetService` | string | `DSL`, `Fiber optic`, `No` |
| `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies` | string | `Yes`, `No`, `No internet service` |
| `Contract` | string | `Month-to-month`, `One year`, `Two year` |
| `PaymentMethod` | string | `Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)` |
| `Tenure` | int | `0 ≤ tenure ≤ 120` |
| `MonthlyCharges` | float | `0 ≤ monthly_charges ≤ 1000` |
| `TotalCharges` | float | `0 ≤ total_charges ≤ 100000` |

Tout champ manquant, de mauvais type, hors domaine ou avec une valeur non listée produit une erreur `422` (voir §5).

---

## 4. `GET /model-info`

Métadonnées du modèle actuellement servi.

**Réponse `200 OK`** :

```json
{
  "model_name": "churn_model",
  "model_version": "3",
  "run_id": "a1b2c3d4e5f6a7b8c9d0e1f2",
  "production_metrics": {
    "f1": 0.81,
    "accuracy": 0.84,
    "precision": 0.78,
    "recall": 0.72,
    "roc_auc": 0.88,
    "n_samples": 1408
  }
}
```

- `production_metrics` est lu depuis `models/evaluation/production_report.json` (écrit par `promote.py`) ; `null` si le rapport est absent.
- `run_id` peut être `null` si le modèle a été chargé depuis un chemin local.

---

## 5. Codes d'erreur

| Code | Cas | Détail (`detail`) |
|---|---|---|
| `422` | Charge pydantic invalide | Message décrivant le champ et la contrainte violée (ex. : `Input should be 'Yes' or 'No'`, `Input should be less than or equal to 120`) |
| `422` | Lot vide | `"empty prediction batch"` (`main.py`, `predict()`) |
| `500` | Échec interne de prédiction | `"prediction failed: <exception>"` (`_predict_one`) |
| `500` | Modèle introuvable au démarrage | Erreur levée par `model_loader.load()` (log au démarrage) ; l'API peut tourner mais `/predict` échoue tant que le modèle n'est pas disponible |
| `404` / `405` | Route inconnue / méthode non autorisée | Réponses standard FastAPI |

**Exemple d'erreur 422** :

```json
{
  "detail": [
    {
      "type": "literal_error",
      "loc": ["body", "Gender"],
      "msg": "Input should be 'Male' or 'Female'",
      "input": "Other"
    }
  ]
}
```

> **Note démarrage** : si le registry MLflow est injoignable et qu'aucun `MLFLOW_MODEL_URI` / `models/model.pkl` n'existe, le démarrage échoue (log `model loading failed`). Règle de résolution dans `model_loader._load_model()` : `MLFLOW_MODEL_URI` explicite → registry `Production` → pickle local.

---

## 6. Métriques Prometheus (`GET /metrics`)

Exposé par `src/api/metrics.py` via `prometheus-fastapi-instrumentator` :

- `http_requests_total{method,path,status}` et `http_request_duration_seconds_bucket` — métriques HTTP standard par endpoint et statut.
- `model_prediction_value_bucket` — histogramme de la distribution des probabilités prédites (buckets 0.0 → 1.0 par pas de 0.1) ; alimente le dashboard `model-drift`.
- `predictions_total{model_version}` — jauge cumulative des prédictions par version de modèle.
- `mlops_model_version{model_name}` — version du modèle servi.

Consommées par Prometheus (job `mlops-api`, see `monitoring/prometheus/prometheus.yml`).

---

## 7. Exemples cURL

```bash
# Health
curl http://localhost:8000/health

# Prédiction unitaire
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Gender":"Male","SeniorCitizen":0,"Partner":"No","Dependents":"No","Tenure":12,"PhoneService":"Yes","MultipleLines":"No","InternetService":"DSL","OnlineSecurity":"No","OnlineBackup":"Yes","DeviceProtection":"No","TechSupport":"No","StreamingTV":"No","StreamingMovies":"No","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check","MonthlyCharges":65.5,"TotalCharges":786.0}'

# Lot de 2 prédictions
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '[{"Gender":"Male","Tenure":12,"MonthlyCharges":65.5,"TotalCharges":786.0},{"Gender":"Female","Tenure":5,"MonthlyCharges":99.0,"TotalCharges":500.0}]'

# Métadonnées du modèle
curl http://localhost:8000/model-info

# Métriques Prometheus
curl http://localhost:8000/metrics
```

> Le payload de prédiction ci-dessus est celui utilisé par les smoke tests du CD (`deploy-staging`).
