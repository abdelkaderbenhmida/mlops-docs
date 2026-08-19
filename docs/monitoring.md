# Monitoring — Plateforme de prévision de la demande

Ce document décrit le monitoring de la plateforme : collecte Prometheus, règles d'alerte, dashboards Grafana, **détection de drift** (tests de Kolmogorov-Smirnov par feature) et alerting (Slack + journal local).

---

## 1. Vue d'ensemble

```
                        ┌────────────────────┐
   API FastAPI ────────▶│ Prometheus         │
   GET /metrics         │ scrape 15 s        │──▶ Grafana (dashboards)
                        │                    │      api-performance.json
                        │  alert_rules.yml   │      model-drift.json
                        └─────────┬──────────┘
                                  │ alertes
                                  ▼
                     Slack (SLACK_WEBHOOK_URL) + journal alerts.jsonl
```

Deux familles de monitoring :

1. **Technique** : santé du service d'inférence (latence, erreurs, disponibilité) — Prometheus/Grafana.
2. **Modèle** : drift des données de production vs la référence d'entraînement — `drift_detection.py`, et distribution des prévisions (`model_prediction_value`).

---

## 2. Métriques Prometheus

Exposées par `src/api/metrics.py` (instrumentation `prometheus_fastapi_instrumentator` + métriques métier) :

| Métrique | Type | Description |
|---|---|---|
| `http_requests_total{method,path,status}` | compteur | Requêtes par endpoint et code |
| `http_request_duration_seconds` | histogramme | Latence par endpoint (p95 via `histogram_quantile`) |
| `model_prediction_value` | histogramme | Distribution des `predicted_units` — buckets (0, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150) |
| `predictions_total{model_version}` | gauge | Nombre cumulé de requêtes de prévision par version |
| `mlops_model_version{model_name}` | gauge | Version du modèle servi |

Configuration de scrape : `monitoring/prometheus/prometheus.yml` — cibles `api:8000` (docker compose) et `host.docker.internal:8000` (local), intervalle 15 s.

---

## 3. Règles d'alerte (`monitoring/prometheus/alert_rules.yml`)

| Alerte | Expression | Condition de déclenchement | Sévérité |
|---|---|---|---|
| `HighAPILatency` | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5` par path/méthode | p95 > 500 ms pendant 5 min | warning |
| `HighAPIErrorRate` | taux de 5xx > 0,05 par path | > 5 % d'erreurs pendant 5 min | critical |
| `APIInstanceDown` | `up{job="mlops-api"} == 0` | cible injoignable pendant 2 min | critical |
| `ModelPredictionShift` | quantile p95 < 0,05 **et** p50 > 0,8 de la distribution `model_prediction_value` | distribution des prévisions dérivée pendant 6 h | warning |

---

## 4. Dashboards Grafana

Provisionnés en lecture seule dans le conteneur Grafana (`monitoring/grafana/dashboards/`) :

- **API Performance** (`api-performance.json`) : latence (p50/p95/p99), taux d'erreur, requêtes par seconde.
- **Model Drift** (`model-drift.json`) : score de drift, features dérivées, distribution des prévisions (`model_prediction_value`) vs référence d'entraînement.

---

## 5. Détection de drift (`src/monitoring/drift_detection.py`)

### 5.1 Principe

Compare les données de **production courantes** (`data/monitoring/current.csv`, chemins via env `DRIFT_REFERENCE` / `DRIFT_CURRENT`) au **snapshot de référence** écrit par `train.py` à l'entraînement (`data/monitoring/reference.csv` : features + `prediction` + `units_sold` du jeu de test).

### 5.2 Méthode

1. Pour chaque feature numérique (les 11 features d'entraînement), **test de Kolmogorov-Smirnov à deux échantillons** (`scipy.stats.ks_2samp`) entre référence et courant
2. Feature dérivée si `p_value < 0.05` **et** `statistic > 0.1`
3. **Score de drift global** = fraction de features dérivées (`drifted / total`)
4. `drift_detected = score > threshold` — seuil par défaut **0,3** (env `DRIFT_THRESHOLD`, surchargeable en CLI `--threshold`)
5. Rapport écrit dans `data/monitoring/drift_report.json`

```json
{
  "engine": "scipy-fallback",
  "drift_score": 0.09,
  "threshold": 0.3,
  "drift_detected": false,
  "drifted_features": [],
  "per_column": {
    "price": { "drift_detected": false, "test": "ks_2samp", "score": 0.05 },
    "store_traffic": { "drift_detected": true, "test": "ks_2samp", "score": 0.35 }
  }
}
```

Erreurs si la référence ou le courant n'existent pas (`FileNotFoundError`). Usage direct : `make drift` ou `python src/monitoring/drift_detection.py [--reference …] [--current …] [--threshold …]`.

### 5.3 Limite assumée

Le moteur actuel est le **fallback scipy** (`engine: "scipy-fallback"`) : un test KS par feature numérique, sans rapport HTML. Une intégration **Evidently** (rapports riches, familles de tests supplémentaires) figure au plan de route.

---

## 6. Alerting (`src/monitoring/alerting.py`)

| Canal | Condition | Détail |
|---|---|---|
| **Slack** | env `SLACK_WEBHOOK_URL` définie | Message avec emoji de sévérité ; `delivered=true` si HTTP 200 |
| **Journal local** | toujours | `data/monitoring/alerts/alerts.jsonl` — horodatage, sévérité, message, extras |

Sévérités : `debug`, `info`, `warning`, `critical`. Aucun secret loggé (seul le préfixe de l'URL du webhook est affichable).

Utilisation :
- `on_failure_callback` des DAGs Airflow → alerte `critical` à chaque tâche en échec
- `retraining_pipeline` → alerte `warning` quand le drift est détecté, avant le réentraînement

---

## 7. Boucle de réentraînement déclenchée par le drift

```
detect_drift() (retraining_pipeline, @daily)
        │
   score > seuil ?
   │          │ non
   oui        ▼
   │      ShortCircuitOperator → DAG arrêté (rien à faire)
   ▼
alerte warning (Slack + journal)
   ▼
preprocess → build_features → train → evaluate (portes R²/MAPE)
   → promote si portes passées ET candidat ≥ champion → notify
```

Le plugin `DriftDetectedSensor` (`airflow/plugins/drift_sensor.py`) sonde `data/monitoring/drift_report.json` (path via env `DRIFT_REPORT_PATH`) et réussit dès que `drift_detected=true` — utilisable pour déclencher d'autres workflows.

---

## 8. État actuel et limites

- Le rapport `data/monitoring/drift_report.json` est écrit à chaque exécution de `detect_drift()` ; en l'absence de flux de production réel, `current.csv` doit être alimenté par l'opérateur (batch) ou un job.
- Le monitoring modèle couvre le **data drift** (distribution des features) et la **dérive de la distribution des prévisions** (`ModelPredictionShift`) ; il n'y a pas encore de surveillance de la dérive des métriques de performance en ligne (nécessiterait un ground truth en continu) — plan de route.
- Les alertes Prometheus (`alert_rules.yml`) sont définies ; l'intégration **Alertmanager** (livraison e-mail/PagerDuty) n'est pas configurée dans le dépôt.