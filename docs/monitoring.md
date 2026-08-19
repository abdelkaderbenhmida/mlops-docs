# Monitoring de la plateforme de décision de fraude

Le monitoring couvre trois niveaux : l'**observabilité technique** (Prometheus/Grafana sur le service de décision), le **monitoring métier** (coût net par 1 000 transactions, capture de fraude, faux refus — ce que le tableau de bord exécutif affiche) et le **monitoring du modèle** (dérive de données avec Evidently + signatures adversariales dédiées). Le tout est branché sur un système d'**alerting** (Slack + log local), des **garde-fous de rollback** (agrégés ET par segment) et la boucle de **réentraînement automatique** (Airflow).

---

## 1. Architecture de monitoring

```
                     ┌────────────────────────────┐
                     │  Service de décision (8000) │
                     │  /metrics (Prometheus)      │
                     └─────────────┬──────────────┘
                                   │ scrape toutes les 15 s
                                   ▼
                     ┌────────────────────────────┐
                     │  Prometheus (port 9090)    │
                     │  prometheus.yml            │
                     │  alert_rules.yml           │
                     └───────┬────────┬───────────┘
                             │        │
                             ▼        ▼
                  ┌───────────────┐  ┌──────────────────────────┐
                  │   Grafana     │  │  Alertes (règles)         │
                  │  (port 3000)  │  │  → rollback automatique   │
                  │  dashboards   │  │  → Slack / log local      │
                  └───────────────┘  └──────────────────────────┘

 Modèle de données (drift) :
   data/monitoring/reference.csv  (référence d'entraînement, vintages matures)
   data/monitoring/current.csv    (fenêtre de production)
   src/monitoring/drift_detection.py       →  drift_report.json / drift_report.html
   src/monitoring/adversarial_detectors.py →  frottement de frontière, rafales, sondage
   retraining_pipeline (Airflow)            →  réentraînement si drift
   src/monitoring/alerting.py              →  alerts.jsonl + Slack

 Garde-fous de canary (évalués en continu) :
   chute du taux d'approbation > 3 pts vs champion   → rollback immédiat
   latence p99 > 100 ms pendant 5 min               → rollback immédiat
   taux de refus d'un segment top-20 > 2×           → rollback immédiat
   taux d'erreur > 0,5 %                            → rollback immédiat
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
| `decision_latency_seconds_bucket` | histogramme | Latence de décision (p50/p95/**p99**) — le budget est **100 ms p99** |
| `decision_score_bucket` | histogramme | Distribution des scores (buckets 0.0–1.0, pas 0.1) ; alimente le drift et la détection de frottement de frontière |
| `decisions_total{decision,model_version}` | compteur | Décisions par palier (`APPROVE` / `REVIEW` / `DECLINE`) et par version de modèle |
| `approval_rate_by_segment{country,bin}` | jauge | Taux d'approbation par segment — garde-fou de canary |
| `decline_rate_by_segment{country,bin}` | jauge | Taux de refus par segment — garde-fou de canary (segment top-20 > 2× → rollback) |
| `model_mode` | jauge | `1` = modèle+règles, `0` = règles seules (fail-open actif) |
| `mlops_model_version{model_name}` | jauge | Version du modèle actuellement servi |

---

## 3. Règles d'alerte — `monitoring/prometheus/alert_rules.yml`

| Alerte | Expression | Durée | Sévérité | Sens |
|---|---|---|---|---|
| `HighDecisionLatency` | `histogram_quantile(0.99, rate(decision_latency_seconds_bucket[5m])) > 0.1` | 5 min | `critical` | **Latence p99 > 100 ms pendant 5 minutes → rollback immédiat** |
| `HighAPIErrorRate` | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.005` | 5 min | `critical` | Plus de 0,5 % d'erreurs → rollback immédiat |
| `ApprovalRateDrop` | chute du taux d'approbation global > 3 points de pourcentage vs champion | 5 min | `critical` | → rollback immédiat |
| `SegmentDeclineRate` | taux de refus d'un segment top-20 pays/BIN > 2× la référence | 5 min | `critical` | → rollback immédiat (rattrape les bugs d'encodage pays-spécifiques invisibles en agrégé) |
| `APIInstanceDown` | `up{job="mlops-api"} == 0` | 2 min | `critical` | Cible de scrape injoignable |
| `ModelPredictionShift` | p95(scores, 1 h) < 0.05 **et** médiane > 0.8 | 6 h | `warning` | Dérive de la distribution des scores par rapport à l'entraînement |
| `FailOpenActive` | `model_mode == 0` | 5 min | `warning` | Le service tourne en règles seules (modèle indisponible) — les paiements ne sont pas bloqués, mais la qualité de décision est dégradée |

> L'intégration Alertmanager est **optionnelle** : les règles définissent la détection ; les alertes applicatives sont émises par `src/monitoring/alerting.py` (voir §6).

---

## 4. Dashboards Grafana — `monitoring/grafana/dashboards/`

Provisionnés en lecture seule dans `/var/lib/grafana/dashboards` (volume `../monitoring/grafana/dashboards`). UI : http://localhost:3000 (`admin` / `admin`, configurable via `.env`).

### 4.1 `business-metrics.json` — métriques métier d'abord (tableau de bord exécutif)

| Panneau | Type | Source |
|---|---|---|
| Coût net par 1 000 transactions | stat | Coût attendu depuis la matrice (pertes fraude − marge sauvée + frais, rapporté au volume) — **la métrique du tableau de bord exécutif** |
| Taux de capture de fraude | stat | Fraude bloquée / fraude tentée (via réconciliation des labels) — cible > 75 % |
| Taux de faux refus | stat | Légitimes refusés / légitimes — cible < 0,8 % |
| Ratio de chargeback | stat | Chargebacks / transactions — sous les seuils de surveillance des réseaux |
| Taux de revue | stat | Transactions RÉVISER / total — dans la capacité des analystes |
| Précision de revue | stat | Fraude confirmée / revues — cible > 30 % |
| Pannes fail-open | timeseries | `model_mode` — le service n'a jamais bloqué un paiement |

### 4.2 `api-performance.json` — performance du service de décision

| Panneau | Type | Expression |
|---|---|---|
| Decisions per second | stat | `sum(rate(decisions_total[5m]))` |
| Decision latency p50 / p95 / p99 | timeseries | `histogram_quantile(0.50 / 0.95 / 0.99, rate(decision_latency_seconds_bucket[5m]))` — **référence 0.1 s (p99)** |
| Decision rate by outcome | timeseries | `sum(rate(decisions_total[5m])) by (decision)` |
| Error rate | timeseries | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` — référence 0,5 % |
| Approval rate by top-20 country | timeseries | `approval_rate_by_segment` — garde-fou par segment |
| Served model version | timeseries | `mlops_model_version` |

### 4.3 `model-drift.json` — drift du modèle

| Panneau | Type | Expression / source |
|---|---|---|
| Drift detected | stat | `model_drift_detected` |
| Global drift score (threshold 0.3) | stat | `model_drift_score` |
| Global drift score over time | timeseries | `model_drift_score` + référence `0.3` |
| Score distribution (cumulative histogram) | timeseries | `sum(rate(decision_score_bucket[1h])) by (le)` |
| **Frottement de frontière** | timeseries | Densité de transactions scorées juste sous `t_low` (bande [t_low−0.05, t_low)) — **une population légitime ne s'y concentre pas** |
| **Rafales coordonnées** | stat/table | Hausse de transactions partageant appareil, BIN, adresse ou sous-réseau IP |
| **Sondage (probing)** | stat | Rafale de transactions de faible valeur depuis cartes/appareils liés |

---

## 5. Détection de drift et signatures adversariales

### 5.1 Références de données

| Fichier | Rôle | Écrit par |
|---|---|---|
| `data/monitoring/reference.csv` | Référence d'entraînement : features du jeu de test mature + colonnes `score` et `label` | `src/models/train.py` |
| `data/monitoring/current.csv` | Fenêtre de données de production | Charge externe (scores + features loggées via le flux Kafka) |
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
- **Score drift** : dérive de la distribution des scores (`ColumnDriftMetric("score")`).
- **Score global** = fraction de features en drift (`number_of_drifted_columns / number_of_columns`).
- `drift_detected = drift_score > threshold`.
- **Fallback scipy** : si Evidently n'est pas installé, test `ks_2samp` par colonne (p < 0.05 et stat > 0.1) — la détection reste fonctionnelle.
- Sortie : rapport JSON + rapport HTML Evidently.

```bash
make drift          # python src/monitoring/drift_detection.py
```

### 5.3 Détecteurs adversariaux — `src/monitoring/adversarial_detectors.py`

Le drift distributionnel est **passif** : il décrit le monde qui change. En fraude, le drift est **actif** : un attaquant cherche la frontière de décision et la traverse. Les tests standards ne se déclencheront pas avant que le dommage soit fait — des détecteurs dédiés sont nécessaires :

| Détecteur | Signature surveillée | Pourquoi |
|---|---|---|
| **Frottement de frontière** | Densité croissante de transactions scorées juste sous `t_low` | Une population légitime ne se concentre pas là ; l'attaquant s'adapte au seuil. **L'une des alertes à plus forte valeur du système** |
| **Sondage (probing)** | Rafale de transactions de faible valeur depuis des cartes ou appareils liés | Caractéristique du test de cartes contre une liste volée |
| **Empoisonnement de features** | Historique bénin fabriqué délibérément avant une transaction frauduleuse | Attaque active sur l'espace de features |
| **Rafales coordonnées** | Hausse forte de transactions partageant empreinte d'appareil, plage de BIN, adresse de livraison ou sous-réseau IP | Attaque coordonnée en cours |

Ces détecteurs sont **directionnels** (ils surveillent une signature précise), pas seulement distributionnels. Ils alimentent le même canal d'alerte et le déclenchement du réentraînement que le drift Evidently.

### 5.4 Boucle de réentraînement

- Le DAG `retraining_pipeline` (planifié hebdomadaire **randomisé** + déclenché par drift/signature) débute par `check_drift` (`ShortCircuitOperator`) qui appelle `detect_drift()` et les détecteurs adversariaux.
- Si drift ou signature détectée : alerte `warning` envoyée, puis `preprocess → build_features → build_training_set (vintage-aware) → train_model → optimize_threshold → evaluate_model (backtest vintages matures) → deploy_shadow → notify_team`.
- La promotion ne s'effectue qu'après **7 jours de shadow** puis canary avec garde-fous segmentés (`promote.py`), évitant les régressions.
- Les décisions de revue des analystes reviennent automatiquement dans le jeu d'entraînement comme labels de haute qualité (via la réconciliation des labels).

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
| Détecteurs adversariaux | `boundary hugging detected (density=…, band=[t_low−0.05, t_low))` / `coordinated burst detected` / `probing detected` | `critical` |
| Garde-fous de canary | `approval rate dropped >3pp vs champion` / `segment decline rate >2x (country=…, bin=…)` | `critical` |
| Fail-open | `model unavailable - running rules-only (fail-open)` | `warning` |
| `retraining_pipeline` après promotion | `retraining promoted model version N to shadow (expected_cost=…)` | `info` |

**Configuration** (`.env.example`) :

```dotenv
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
# ALERT_EMAIL_TO=
DRIFT_THRESHOLD=0.3
LATENCY_BUDGET_MS=100
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
| Mode du service | `curl http://localhost:8000/health` (`mode`: `model+rules` ou `rules-only`) |
| Dernière décision au ledger | Kafka topic `decisions` / requête PostgreSQL sur le ledger |