# Référence API de décision de fraude

Le service de décision FastAPI (`src/api/main.py`) décide chaque transaction de paiement en temps réel dans le cadre du produit **Sentry**. Il est servi par Uvicorn (`make api`, ou l'image `mlops-api` sur le port 8000) et charge le modèle depuis le MLflow Model Registry (`models:/fraud_model/Production`) via `src/api/model_loader.py`.

**Budget de latence** : la décision doit revenir en **100 ms à p99** de bout en bout (voir §1.3 de la spécification). Le logging de décision est **asynchrone** (émission vers Kafka), hors chemin critique.

**Fail-open** : si le modèle est indisponible ou dépasse son budget, le service ne bloque jamais le paiement — il retombe sur une décision conservatrice pilotée uniquement par le moteur de règles (`src/api/rules_engine.py`).

**Base URL** : `http://localhost:8000` (local) — `http://<endpoint-staging>/` ou `http://<endpoint-production>/` (Kubernetes).

---

## 1. Endpoints

| Méthode | Chemin | Description |
|---|---|---|
| `GET` | `/health` | Liveness/readiness : état du service et modèle chargé |
| `POST` | `/decide` | Décision de fraude (une transaction ou un lot) |
| `GET` | `/metrics` | Métriques Prometheus |
| `GET` | `/model-info` | Métadonnées du modèle servi (version, run, seuils, métriques de production) |
| `GET` | `/docs` | Documentation interactive OpenAPI (générée par FastAPI) |

---

## 2. `GET /health`

Probe de liveness/readiness utilisée par Kubernetes et le healthcheck Docker.

**Réponse `200 OK`** (modèle chargé) :

```json
{
  "status": "ok",
  "model_name": "fraud_model",
  "model_version": "3",
  "mode": "model+rules"
}
```

**Réponse `200 OK`** (modèle indisponible — service dégradé mais vivant) :

```json
{
  "status": "degraded",
  "model_name": null,
  "model_version": null,
  "mode": "rules-only"
}
```

> `/health` renvoie toujours `200` ; la dégradation est signalée par `"status": "degraded"` et `"mode": "rules-only"`. Seule une panne du processus produit un échec de probe. Le mode `rules-only` est le **chemin fail-open volontaire** : les paiements continuent d'être décidés par les règles seules, jamais bloqués par la panne du modèle.

---

## 3. `POST /decide`

Décide une transaction card-not-present selon la logique à trois paliers (`src/api/decision.py`) :

```
score < t_low          → APPROVE
t_low ≤ score < t_high → REVIEW   (file analyste, ou step-up 3-D Secure)
score ≥ t_high         → DECLINE
```

Les seuils `t_low` / `t_high` dérivent de la matrice de coûts et de la capacité de revue (voir §9.3 de la spécification).

### 3.1 Requête — cas unitaire

Le corps est un objet JSON décrivant la transaction. Les features de vélocité (compteurs 1 h / 24 h / 7 j, appareils distincts, etc.) sont **calculées par le service** à partir du store en ligne Redis et des données de la requête — elles ne sont pas fournies par le client.

```json
{
  "transaction_id": "txn_8f3a1c",
  "timestamp": "2026-08-19T14:32:11Z",
  "card_hash": "a1b2c3d4e5f6...",
  "card_bin": "424242",
  "device_id": "dev_77e1",
  "ip_address": "203.0.113.45",
  "merchant_id": "merchant_1042",
  "amount": 249.99,
  "currency": "EUR",
  "billing_country": "FR",
  "billing_zip": "75011",
  "shipping_country": "FR",
  "shipping_zip": "75011",
  "is_first_txn_at_merchant": false
}
```

**Réponse `200 OK`** :

```json
{
  "decision": "APPROVE",
  "score": 0.31,
  "threshold_low": 0.42,
  "threshold_high": 0.87,
  "rules_fired": [],
  "model_name": "fraud_model",
  "model_version": "3",
  "decision_id": "dec_9f2b7c1e"
}
```

| Champ | Type | Description |
|---|---|---|
| `decision` | string | `APPROVE`, `REVIEW` ou `DECLINE` |
| `score` | float [0,1] | Score de risque du modèle |
| `threshold_low` | float | Seuil inférieur (dérivé de la matrice de coûts + capacité de revue) |
| `threshold_high` | float | Seuil supérieur (idem) |
| `rules_fired` | array | Règles déterministes déclenchées (liste de blocage, plafonds de vélocité, géographie…) |
| `model_name` | string | Nom du modèle dans le Registry |
| `model_version` | string | Version du modèle servi |
| `decision_id` | string | Identifiant de la décision, reconstructible depuis le ledger de décisions |

**Réponse en mode fail-open** (modèle indisponible ou budget dépassé) :

```json
{
  "decision": "DECLINE",
  "score": null,
  "threshold_low": null,
  "threshold_high": null,
  "rules_fired": ["hard_velocity_cap", "blocklist_match"],
  "model_name": null,
  "model_version": null,
  "decision_id": "dec_1a2b3c4d"
}
```

> Le mode fail-open ne bloque jamais un paiement sans une règle déterministe : à score inconnu, une transaction qui ne déclenche **aucune** règle est approuvée. Le blocage n'a lieu que si une règle le justifie.

### 3.2 Requête — lot

Le corps est un **tableau JSON** d'objets (même schéma). Réponse : un tableau dans le même ordre.

```json
[
  { "transaction_id": "txn_8f3a1c", "timestamp": "2026-08-19T14:32:11Z", "card_hash": "a1b2...", "card_bin": "424242", "device_id": "dev_77e1", "ip_address": "203.0.113.45", "merchant_id": "merchant_1042", "amount": 249.99, "currency": "EUR", "billing_country": "FR", "billing_zip": "75011", "shipping_country": "FR", "shipping_zip": "75011" },
  { "transaction_id": "txn_4c9d0e", "timestamp": "2026-08-19T14:33:02Z", "card_hash": "f9e8...", "card_bin": "555555", "device_id": "dev_02aa", "ip_address": "198.51.100.9", "merchant_id": "merchant_1042", "amount": 1890.00, "currency": "EUR", "billing_country": "ES", "billing_zip": "28001", "shipping_country": "IT", "shipping_zip": "20121" }
]
```

**Réponse `200 OK`** :

```json
[
  { "decision": "APPROVE", "score": 0.31, "threshold_low": 0.42, "threshold_high": 0.87, "rules_fired": [], "model_name": "fraud_model", "model_version": "3", "decision_id": "dec_9f2b7c1e" },
  { "decision": "DECLINE", "score": 0.93, "threshold_low": 0.42, "threshold_high": 0.87, "rules_fired": ["high_risk_geo"], "model_name": "fraud_model", "model_version": "3", "decision_id": "dec_5a6b7c8d" }
]
```

### 3.3 Schéma des champs (Pydantic — `src/api/schemas.py`)

Contraintes et domaines appliqués par validation (exemple indicatif — aligné sur les colonnes d'entraînement du jeu de démonstration) :

| Champ | Type | Contraintes |
|---|---|---|
| `transaction_id` | string | Non vide, format `txn_*` |
| `timestamp` | datetime | Présent, cohérent (pas dans le futur au-delà de la tolérance) |
| `card_hash` | string | Haché côté acquéreur — **jamais** le PAN en clair |
| `card_bin` | string | 6 chiffres |
| `device_id` | string | Identifiant d'appareil haché |
| `ip_address` | string | IP valide |
| `merchant_id` | string | Identifiant marchand |
| `amount` | float | `0 < amount ≤ 1 000 000` |
| `currency` | string | ISO 4217 (3 lettres) |
| `billing_country` / `shipping_country` | string | ISO 3166-1 alpha-2 |
| `billing_zip` / `shipping_zip` | string | Code postal |
| `is_first_txn_at_merchant` | bool | Optionnel, défaut `false` |

Tout champ manquant, de mauvais type ou hors domaine produit une erreur `422` (voir §5).

---

## 4. `GET /model-info`

Métadonnées du modèle actuellement servi, dont les seuils de décision.

**Réponse `200 OK`** :

```json
{
  "model_name": "fraud_model",
  "model_version": "3",
  "run_id": "a1b2c3d4e5f6a7b8c9d0e1f2",
  "threshold_low": 0.42,
  "threshold_high": 0.87,
  "production_metrics": {
    "expected_cost_per_1k": 4.81,
    "fraud_capture_rate": 0.78,
    "false_decline_rate": 0.006,
    "review_precision": 0.34,
    "n_samples": 125000
  }
}
```

- `production_metrics` est lu depuis `models/evaluation/production_report.json` (écrit par `promote.py`) ; `null` si le rapport est absent.
- `run_id` peut être `null` si le modèle a été chargé depuis un chemin local.
- Les seuils sont des **informations sensibles** (voir §20.3 de la spécification) : l'accès à ce endpoint doit être restreint dans les environnements de production.

---

## 5. Codes d'erreur

| Code | Cas | Détail (`detail`) |
|---|---|---|
| `422` | Charge pydantic invalide | Message décrivant le champ et la contrainte violée |
| `422` | Lot vide | `"empty decision batch"` (`main.py`, `decide()`) |
| `500` | Échec interne de décision | `"decision failed: <exception>"` — **sauf** échec du modèle seul, qui bascule en fail-open et ne produit pas de 500 |
| `500` | Modèle introuvable au démarrage | Erreur levée par `model_loader.load()` (log au démarrage) ; l'API peut tourner en mode `rules-only`, `/decide` continue de répondre via le moteur de règles |
| `503` | Surcharge | Budget de latence dépassé sous charge extrême — le service refuse la requête plutôt que de casser le p99 ; la transaction est décidée par l'acquéreur selon ses propres règles de secours |
| `404` / `405` | Route inconnue / méthode non autorisée | Réponses standard FastAPI |

> **Note démarrage** : si le registry MLflow est injoignable et qu'aucun `MLFLOW_MODEL_URI` / `models/model.pkl` n'existe, le démarrage ne bloque **pas** le service : il démarre en mode `rules-only` (fail-open). Règle de résolution dans `model_loader._load_model()` : `MLFLOW_MODEL_URI` explicite → registry `Production` → pickle local.

---

## 6. Métriques Prometheus (`GET /metrics`)

Exposé par `src/api/metrics.py` via `prometheus-fastapi-instrumentator` :

- `http_requests_total{method,path,status}` et `http_request_duration_seconds_bucket` — métriques HTTP standard par endpoint et statut.
- `decision_latency_seconds_bucket` — histogramme de latence de décision (p50/p95/p99) ; **p99 > 100 ms pendant 5 minutes = déclencheur de rollback immédiat**.
- `decision_score_bucket` — histogramme de la distribution des scores (buckets 0.0 → 1.0 par pas de 0.1) ; alimente le dashboard `model-drift` et la détection de frottement de frontière.
- `decisions_total{decision,model_version}` — compteur cumulé de décisions par palier (`APPROVE` / `REVIEW` / `DECLINE`) et par version de modèle.
- `approval_rate_by_segment{country,bin}` — taux d'approbation par segment ; alimente les garde-fous de canary (chute > 3 points → rollback).
- `decline_rate_by_segment{country,bin}` — taux de refus par segment ; un segment top-20 > 2× la référence → rollback.
- `model_mode` — `model+rules` ou `rules-only` (fail-open actif).
- `mlops_model_version{model_name}` — version du modèle servi.

Consommées par Prometheus (job `mlops-api`, see `monitoring/prometheus/prometheus.yml`).

---

## 7. Exemples cURL

```bash
# Health
curl http://localhost:8000/health

# Décision unitaire
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"transaction_id":"txn_8f3a1c","timestamp":"2026-08-19T14:32:11Z","card_hash":"a1b2c3d4e5f6","card_bin":"424242","device_id":"dev_77e1","ip_address":"203.0.113.45","merchant_id":"merchant_1042","amount":249.99,"currency":"EUR","billing_country":"FR","billing_zip":"75011","shipping_country":"FR","shipping_zip":"75011"}'

# Lot de 2 décisions
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '[{"transaction_id":"txn_8f3a1c","timestamp":"2026-08-19T14:32:11Z","card_hash":"a1b2c3d4e5f6","card_bin":"424242","device_id":"dev_77e1","ip_address":"203.0.113.45","merchant_id":"merchant_1042","amount":249.99,"currency":"EUR","billing_country":"FR","billing_zip":"75011","shipping_country":"FR","shipping_zip":"75011"},{"transaction_id":"txn_4c9d0e","timestamp":"2026-08-19T14:33:02Z","card_hash":"f9e8d7c6b5a4","card_bin":"555555","device_id":"dev_02aa","ip_address":"198.51.100.9","merchant_id":"merchant_1042","amount":1890.00,"currency":"EUR","billing_country":"ES","billing_zip":"28001","shipping_country":"IT","shipping_zip":"20121"}]'

# Métadonnées du modèle
curl http://localhost:8000/model-info

# Métriques Prometheus
curl http://localhost:8000/metrics
```

> Le payload de décision ci-dessus est celui utilisé par les smoke tests du CD (`deploy-staging`).

---

## 8. Cycle de vie de la décision

```
/decide ──▶ décision + score + règles ──▶ réponse synchrone au flux d'autorisation (< 100 ms p99)
     │
     └──▶ Kafka (événement de décision, asynchrone)
              ├──▶ Ledger de décisions (S3 + PostgreSQL)   — reconstruction, litiges
              ├──▶ Agrégateur de vélocité → Redis          — features mises à jour
              └──▶ Monitoring temps réel                   — frottement de frontière, rafales, segments
```

Chaque événement de décision contient : `decision_id`, `transaction_id`, timestamp, features snapshot, score, seuils, règles déclenchées, version de modèle, résultat final (lorsqu'il est connu via la réconciliation des labels).