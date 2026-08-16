# Monitoring de la plateforme

Le monitoring couvre deux niveaux : l'**observabilité technique** (Prometheus/Grafana sur l'API) et le **monitoring métier du modèle** (dérive de données et de prédictions avec Evidently). Le tout est branché sur un système d'**alerting** (Slack + log local) et la boucle de **réentraînement automatique** (Airflow).

---

## 1. Architecture de monitoring

```
                     ┌────────────────────────────┐
                     │  API FastAPI (port 8000)   │
                     │  /metrics (Prometheus)     │
                     └─────────────┬──────────────┘
                                   │ scrape toutes les 15 s
                                   ▼
                     ┌────────────────────────────┐
                     │  Prometheus (port 9090)    │
                     │  prometheus.yml            │
                     │  alert_rules.yml           │
                     └───────┬────────────┬───────┘
                             │            │
                             ▼            ▼
                  ┌───────────────┐  ┌──────────────────────────┐
                  │   Grafana     │  │  Alertes (règles)         │
                  │  (port 3000)  │  │  → inspection manuelle    │
                  │  dashboards   │  │  (Alertmanager optionnel) │
                  └───────────────┘  └──────────────────────────┘

 Modèle de données (drift) :
   data/monitoring/reference.csv  (référence d'entraînement, écrite par train.py)
   data/monitoring/current.csv    (fenêtre de production)
   src/monitoring/drift_detection.py  →  drift_report.json / drift_report.html
   retraining_pipeline (Airflow)       →  réentraînement si drift
   src/monitoring/alerting.py          →  alerts.jsonl + Slack
```

---

## 2. Prometheus

### 2.1 Configuration — `monitoring/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "mlops-api"
    metrics_path: /metrics
    static_configs:
      - targets: ["api:8000"]
        labels: { service: mlops-api }

  - job_name: "mlops-api-local"
    metrics_path: /metrics
    static_configs:
      - targets: ["host.docker.internal:8000"]
        labels: { service: mlops-api-local }

rule_files:
  - /etc/prometheus/alert_rules.yml
```

**Cibles** :

| Job | Cible | Usage |
|---|---|---|
| `mlops-api` | `api:8000` | Nom réseau du service API dans le compose (Docker) |
| `mlops-api-local` | `host.docker.internal:8000` | Accès à l'API exécutée sur l'hôte (développement) |

`prometheus.yml` et `alert_rules.yml` sont montés en lecture seule dans le conteneur (`docker/docker-compose.yml`). L'évaluation des règles est déclenchée toutes les 15 s.

### 2.2 Métriques exposées (`src/api/metrics.py`)

| Métrique | Type | Description |
|---|---|---|
| `http_requests_total{method,path,status}` | compteur | Requêtes HTTP par endpoint et statut (instrumentator) |
| `http_request_duration_seconds_bucket` | histogramme | Latence par endpoint (instrumentator) |
| `model_prediction_value_bucket` | histogramme | Distribution des probabilités prédites (buckets 0.0–1.0, pas 0.1) |
| `predictions_total{model_version}` | jauge | Nombre cumulé de prédictions par version de modèle |
| `mlops_model_version{model_name}` | jauge | Version du modèle actuellement servi |

---

## 3. Règles d'alerte — `monitoring/prometheus/alert_rules.yml`

| Alerte | Expression | Durée | Sévérité | Sens |
|---|---|---|---|---|
| `HighAPILatency` | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5` | 5 min | `warning` | Latence p95 > 500 ms sur un endpoint |
| `HighAPIErrorRate` | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05` | 5 min | `critical` | Plus de 5 % de réponses 5xx |
| `APIInstanceDown` | `up{job="mlops-api"} == 0` | 2 min | `critical` | Cible de scrape injoignable |
| `ModelPredictionShift` | p95(prédictions, 1 h) < 0.05 **et** médiane > 0.8 | 6 h | `warning` | Dérive de la distribution des prédictions par rapport à l'entraînement |

> L'intégration Alertmanager est **optionnelle** : les règles définissent la détection ; les alertes applicatives sont émises par `src/monitoring/alerting.py` (voir §5).

---

## 4. Dashboards Grafana — `monitoring/grafana/dashboards/`

Provisionnés en lecture seule dans `/var/lib/grafana/dashboards` (volume `../monitoring/grafana/dashboards`). UI : http://localhost:3000 (`admin` / `admin`, configurable via `.env`).

### 4.1 `api-performance.json` — performance de l'API

| Panneau | Type | Expression |
|---|---|---|
| Requests per second | stat | `sum(rate(http_requests_total[5m]))` |
| API latency p50 / p95 / p99 | timeseries | `histogram_quantile(0.50 / 0.95 / 0.99, rate(http_request_duration_seconds_bucket[5m]))` |
| API error rate (5xx) | timeseries | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` |
| Served model version | timeseries | `mlops_model_version` |
| Prediction throughput by model version | timeseries | `sum(rate(predictions_total[5m])) by (model_version)` |
| Request rate by HTTP status | timeseries | `sum(rate(http_requests_total[5m])) by (status)` |

### 4.2 `model-drift.json` — drift du modèle

| Panneau | Type | Expression / source |
|---|---|---|
| Drift detected | stat | `model_drift_detected` |
| Global drift score (threshold 0.3) | stat | `model_drift_score` |
| Global drift score over time | timeseries | `model_drift_score` + référence `0.3` |
| Prediction distribution (cumulative histogram) | timeseries | `sum(rate(model_prediction_value_bucket[1h])) by (le)` |
| Churn prediction rate by threshold | timeseries | `rate(model_prediction_value_bucket{le="0.5"}[5m])` / `{le="0.9"}` / `{le="1.0"}` |

> Les métriques `model_drift_detected` et `model_drift_score` sont destinées à être publiées par le pipeline de drift ; le score et le seuil figurent aussi dans `data/monitoring/drift_report.json`.

---

## 5. Détection de drift avec Evidently

### 5.1 Références de données

| Fichier | Rôle | Écrit par |
|---|---|---|
| `data/monitoring/reference.csv` | Référence d'entraînement : features du jeu de test + colonnes `prediction` et `label` | `src/models/train.py` |
| `data/monitoring/current.csv` | Fenêtre de données de production | Charge externe (prédictions + features loggées par l'API) |
| `data/monitoring/drift_report.json` | Résultat de la détection (JSON, consommé par Airflow) | `drift_detection.py` |
| `data/monitoring/drift_report.html` | Rapport visuel Evidently (best effort) | `drift_detection.py` |

Variables (`drift_detection.py`, surchargeables en CLI) :

| Variable | Défaut |
|---|---|
| `DRIFT_REFERENCE` | `data/monitoring/reference.csv` |
| `DRIFT_CURRENT` | `data/monitoring/current.csv` |
| `DRIFT_THRESHOLD` | `0.3` |
| `DRIFT_REPORT_PATH` (plugin Airflow) | `data/monitoring/drift_report.json` |

### 5.2 Algorithme — `src/monitoring/drift_detection.py`

- **Data drift** par feature : Kolmogorov-Smirnov pour les features numériques, chi-square / Jensen-Shannon pour les catégorielles (via `DataDriftPreset` d'Evidently).
- **Prediction drift** : dérive de la distribution des probabilités prédites (`ColumnDriftMetric("prediction")`).
- **Score global** = fraction de features en drift (`number_of_drifted_columns / number_of_columns`).
- `drift_detected = drift_score > threshold`.
- **Fallback scipy** : si Evidently n'est pas installé, test `ks_2samp` par colonne (p < 0.05 et stat > 0.1) — la détection reste fonctionnelle.
- Sortie : rapport JSON + rapport HTML Evidently.

```bash
make drift          # python src/monitoring/drift_detection.py
```

### 5.3 Boucle de réentraînement

- Le DAG `retraining_pipeline` (quotidien) débute par `check_drift` (`ShortCircuitOperator`) qui appelle `detect_drift()`. 
- Si `drift_detected` : alerte `warning` envoyée, puis `preprocess → build_features → train_model → evaluate_model → promote_model → notify_team`.
- Le plugin `airflow/plugins/drift_sensor.py` expose aussi `DriftDetectedSensor`, qui sonde `drift_report.json` et succède dès que le drift est détecté.
- La promotion ne s'effectue que si le candidat bat le modèle en production (`promote.py`), évitant les régressions.

---

## 6. Alerting — `src/monitoring/alerting.py`

Canaux, par ordre de préférence :

1. **Slack** — si `SLACK_WEBHOOK_URL` est défini, envoi d'un message formaté avec emoji et sévérité (`send_slack`).
2. **Log local** — toujours écrit : `data/monitoring/alerts/alerts.jsonl` (ligne JSON par alerte : `timestamp`, `severity`, `message`, `extra`).

Sévérités : `debug` (10), `info` (20), `warning` (30), `critical` (40).

`send_alert(message, severity, **extra)` écrit le log local puis tente Slack et renvoie l'entrée avec le champ `slack_delivered`.

**Déclencheurs dans le code** :

| Source | Message | Sévérité |
|---|---|---|
| `data_ingestion_dag` / `training_pipeline` / `retraining_pipeline` (`on_failure_callback`) | `DAG <id> task <task> failed` | `critical` |
| `retraining_pipeline` `check_drift` | `drift detected (score=…, threshold=…) - triggering retraining` | `warning` |
| `retraining_pipeline` après promotion | `retraining promoted model version N to production (f1=…)` | `info` |
| `training_pipeline` après promotion | `training_pipeline completed | f1=…` | `info` |

**Configuration** (`.env.example`) :

```dotenv
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
# ALERT_EMAIL_TO=
DRIFT_THRESHOLD=0.3
```

---

## 7. Supervision rapide

| Vérification | Commandes |
|---|---|
| Targets Prometheus | http://localhost:9090/targets (job `mlops-api`) |
| Règles / alertes actives | http://localhost:9090/rules |
| Dashboards | `make monitor` → http://localhost:3000 |
| Métriques brutes de l'API | `curl http://localhost:8000/metrics` |
| Dernier rapport de drift | `python -m json.tool data/monitoring/drift_report.json` |
| Alertes émises | `tail data/monitoring/alerts/alerts.jsonl` |
