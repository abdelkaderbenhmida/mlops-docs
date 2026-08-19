# Déploiement — Plateforme de prévision de la demande

Ce guide couvre les trois scénarios de déploiement de la plateforme de prévision de la demande : la **stack locale** (Docker Compose), la **configuration du remote DVC** (MinIO), et le **déploiement Kubernetes** via GitHub Actions + Kustomize.

---

## 1. Stack locale (Docker Compose)

`docker compose -f docker/docker-compose.yml up -d --build` lance toute la stack :

| Service | Image | Port | Rôle |
|---|---|---|---|
| `minio` | `minio/minio` | 9000 / 9001 | Stockage objet : remote DVC (`s3://mlops-bucket/data`), artefacts MLflow |
| `minio-init` | `minio/mc` | — | Crée le bucket (idempotent) |
| `postgres` | `postgres:16-alpine` | 5432 | Backend store MLflow + métadonnées Airflow |
| `mlflow` | `mlops-mlflow:local` | 5000 | Serveur tracking + Model Registry (artefacts sur MinIO) |
| `airflow` | `apache/airflow:2.9.2` | 8080 | Scheduler + webserver ; DAGs montés depuis `airflow/dags` ; code source monté depuis `src/` |
| `api` | `mlops-api:local` | 8000 | Service d'inférence FastAPI ; `RELOAD_INTERVAL=60` ; healthcheck `/health` |
| `prometheus` | `prom/prometheus` | 9090 | Scrape `/metrics` de l'API |
| `grafana` | `grafana/grafana:11.0.0` | 3000 | Dashboards provisionnés (lecture seule) |

Variables surchargeables via `.env` (copier `.env.example`) : `MLFLOW_TRACKING_URI`, `MLFLOW_MODEL_NAME` (défaut `churn_model` dans le compose — **définir `demand_model`**), `MINIO_ROOT_USER/PASSWORD`, `POSTGRES_*`, `AIRFLOW_ADMIN_PASSWORD`, `GRAFANA_*`.

> Note : le compose hérite d'une valeur par défaut historique `MLFLOW_MODEL_NAME=churn_model` pour l'API et Airflow. Le nom attendu par `train.py` et `model_loader.py` est **`demand_model`** — définir `MLFLOW_MODEL_NAME=demand_model` dans l'environnement de la stack.

### Image API (`docker/Dockerfile.api`)

Build multi-stage `python:3.11-slim` :
- `builder` : installe `requirements.txt` dans `/install`
- `runtime` : copie `/install`, `src/`, `models/`, `data/features/`, `great_expectations/` ; utilisateur non-root `appuser` (uid 1000) ; `EXPOSE 8000` ; healthcheck `GET /health` ; `CMD uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 2`

---

## 2. Remote DVC (MinIO)

```bash
dvc remote add -d storage s3://mlops-bucket/data
dvc remote modify storage endpointurl http://localhost:9000   # MinIO local
dvc push          # pousse les données versionnées vers le remote
dvc pull          # restaure les données sur une autre machine
```

Variables d'environnement requises (AWS S3-compatible) : `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ENDPOINT_URL` (voir `.env.example`).

---

## 3. Déploiement Kubernetes

### 3.1 Ressources (k8s/)

| Fichier | Contenu |
|---|---|
| `base/deployment.yaml` | 3 replicas ; RollingUpdate (`maxUnavailable: 0`, `maxSurge: 1`) ; liveness `/health` (30 s initial, 10 s période) ; readiness `/health` (10 s initial, 5 s période) ; requests 200m/512Mi, limits 1 CPU/1 Gi ; `runAsNonRoot: 1000` ; `allowPrivilegeEscalation: false` ; env depuis ConfigMap + secret optionnel `mlops-secrets` |
| `base/service.yaml` | ClusterIP, port 80 → 8000 |
| `base/configmap.yaml` | `MLFLOW_TRACKING_URI` (http://mlflow.mlops.svc.cluster.local:5000), `MLFLOW_MODEL_NAME`, `RELOAD_INTERVAL: "60"`, `LOG_LEVEL` |
| `base/hpa.yaml` | HPA autoscaling/v2 : min 2, max 10 ; CPU 70 %, mémoire 80 % ; scale-down stabilisé 300 s |
| `overlays/staging/` | 2 replicas, requests 200m/512Mi, limits 1 CPU/1 Gi |
| `overlays/production/` | 5 replicas, requests 500m/1 Gi, limits 2 CPU/2 Gi |

```bash
kubectl apply -k k8s/overlays/staging        # ou /production
kubectl rollout status deployment/mlops-api --namespace=mlops --timeout=300s
```

### 3.2 Déploiement d'une nouvelle version du modèle

Le modèle n'est **pas** embarqué dans l'image. Le service charge au démarrage la version `Production` du registry MLflow (`models:/demand_model/Production`) avec fallback local `models/model.pkl`.

1. Entraîner + enregistrer : `make train` (stage `None`/`Staging` via le registry)
2. Évaluer : `make evaluate` (portes R² ≥ 0,60 / MAPE ≤ 25 %)
3. Promouvoir : `make promote` (Staging → Production, si portes passées et candidat ≥ champion)
4. Redéployer l'image (nouvelle image = traçabilité immuable) — ou, pour les changements non structurants, attendre le rechargement via `RELOAD_INTERVAL`

---

## 4. CI/CD (GitHub Actions)

### 4.1 CI (`ci.yml`) — chaque push/PR

1. Lint : `ruff check` + `black --check` (src, airflow, scripts)
2. Sécurité : `bandit -r src` — échec sur finding HIGH
3. Validation des données : Great Expectations
4. Tests unitaires + intégration + données (57 tests)

### 4.2 CD (`cd.yml`) — merge vers `main` (déclencheurs : `src/**`, `docker/**`, `k8s/**`, `requirements*.txt`, `dvc.yaml`)

```
build-and-push (ghcr.io/<repo>-api:<git sha> — jamais latest)
      │
deploy-staging : kustomize edit set image + kubectl apply -k overlays/staging
      │          rollout status + smoke tests (GET /health)
      ▼
deploy-production : environment GitHub "production" → approbation manuelle
                    kubectl apply -k overlays/production
                    rollout status + vérification pods/HPA
```

Secrets requis : `KUBECONFIG_STAGING`, `KUBECONFIG_PRODUCTION`, `STAGING_API_URL` (GitHub Environments), `GITHUB_TOKEN` (GHCR).

---

## 5. Déploiement du modèle : parcours recommandé (roadmap)

Le dépôt déploie actuellement un nouveau modèle par **promotion dans le registry + redéploiement de l'image** (approbation manuelle en CD). Les mécanismes de **shadow puis canary** (évaluer un candidat sur du trafic réel avec garde-fous avant promotion complète) ne sont **pas encore implémentés dans le code** — ils figurent au plan de route (§24 de la spécification). La promotion reste donc protégée par : portes d'évaluation (R²/MAPE), comparaison au champion, et approbation manuelle de production.