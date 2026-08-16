# Guide de déploiement

Ce guide couvre les trois scénarios de déploiement de la plateforme : la **stack locale** (Docker Compose), la **configuration du remote DVC** (MinIO), et le **déploiement Kubernetes** via GitHub Actions + Kustomize.

---

## 1. Prérequis

| Outil | Version minimale | Rôle |
|---|---|---|
| Python | >= 3.10 | Scripts du pipeline (recommandé 3.11) |
| Docker + Docker Compose | Docker 24+, Compose v2 | Stack locale et build des images |
| make | — | Raccourcis du `Makefile` |
| git | — | Versioning du code et des données (avec DVC) |
| kubectl + kustomize | — | Déploiement Kubernetes (CD) |
| (option) DVC CLI | 3.x | Commandes données (`dvc repro/push/pull`) |

---

## 2. Stack locale (Docker Compose)

### 2.1 Stack complète

Le fichier `docker/docker-compose.yml` (projet `mlops-stack`) démarre **8 services** :

| Service | Image / build | Ports | Dépend de | Volume |
|---|---|---|---|---|
| `minio` | `minio/minio:RELEASE.2024-04-06T05-26-02Z` | 9000, 9001 | — | `minio-data` |
| `minio-init` | `minio/mc:RELEASE.2024-04-11T17-52-49Z` | — | minio (healthy) | — |
| `postgres` | `postgres:16-alpine` | 5432 | — | `postgres-data` |
| `mlflow` | build `mlflow/Dockerfile.mlflow` | 5000 | postgres, minio | `../mlflow` |
| `airflow` | `apache/airflow:2.9.2-python3.11` | 8080 | postgres, mlflow | DAGs, src, data, dvc.yaml, … |
| `api` | build `docker/Dockerfile.api` | 8000 | mlflow | — |
| `prometheus` | `prom/prometheus:v2.51.2` | 9090 | api (healthy) | `prometheus-data` |
| `grafana` | `grafana/grafana:11.0.0` | 3000 | prometheus | dashboards, `grafana-data` |

Démarrage :

```bash
cp .env.example .env     # variables par défaut, ajustables
make compose-up          # docker compose -f docker/docker-compose.yml up -d --build
```

Arrêt :

```bash
make compose-down        # docker compose -f docker/docker-compose.yml down
```

> Les volumes nommés conservent les données (MinIO, Postgres, Prometheus, Grafana) entre deux `up`. Utilisez `docker compose -f docker/docker-compose.yml down -v` pour tout réinitialiser.

### 2.2 Sous-stack MLflow (développement)

`mlflow/docker-compose.yml` (projet `mlflow-stack`) ne démarre que MinIO + Postgres + le serveur MLflow :

```bash
make mlflow-up           # docker compose -f mlflow/docker-compose.yml up -d --build
```

Utile pour développer le pipeline hors Airflow, l'UI MLflow restant disponible sur http://localhost:5000.

### 2.3 Points d'entrée

| Service | URL / accès | Identifiants par défaut |
|---|---|---|
| MinIO (API S3) | http://localhost:9000 | `minio` / `minio123` |
| MinIO (console) | http://localhost:9001 | `minio` / `minio123` |
| Postgres | `localhost:5432`, db `mlflow` | `mlflow` / `mlflow` |
| MLflow | http://localhost:5000 | — |
| Airflow | http://localhost:8080 | `admin` / `admin` |
| API FastAPI | http://localhost:8000 | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | `admin` / `admin` |

### 2.4 Initialisations au démarrage

- **`minio-init`** crée le bucket `mlops-bucket` (variable `MINIO_BUCKET`) puis le sous-dossier `data/` — il est idempotent (`mc mb --ignore-existing`).
- **`airflow`** installe `requirements.txt`, exécute `airflow db migrate`, crée l'utilisateur admin (`AIRFLOW_ADMIN_PASSWORD`, défaut `admin`) puis lance le scheduler et le webserver.
- **`api`** charge le modèle `models:/churn_model/Production` au démarrage et s'autovérifie via le healthcheck sur `/health` (important : un modèle doit être entraîné et promu avant, voir §3.2).

---

## 3. Configuration du remote DVC (MinIO)

### 3.1 Fichier `.dvc/config`

Le remote est déclaré dans `.dvc/config` :

```ini
[core]
    remote = storage
    analytics = false

['remote "storage"']
    url = s3://mlops-bucket/data
    endpointurl = http://localhost:9000
    access_key_id = minio
    secret_access_key = minio123
```

En local, ces valeurs correspondent aux identifiants MinIO du `.env` (`MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`). Pour un autre remote S3 compatible, adapter `endpointurl`, `access_key_id` et `secret_access_key` (ou utiliser `dvc remote modify storage <option>`).

### 3.2 Pousser / récupérer les données

```bash
make dvc-push      # dvc push  → pousse les artefacts versionnés vers MinIO
make dvc-pull      # dvc pull  → les restaure localement
```

> Dans Airflow, la tâche `version_data` du DAG `data_ingestion_dag` exécute `dvc add data/raw/dataset.csv && dvc commit -f && dvc push` (le push est sauté si aucun remote n'est configuré).

### 3.3 Reproduire le pipeline

```bash
make dvc-repro     # dvc repro — rejoue les stages obsolètes selon dvc.yaml
```

---

## 4. Déploiement Kubernetes

### 4.1 Structure Kustomize

```
k8s/
├── base/
│   ├── configmap.yaml       # MLFLOW_TRACKING_URI, MLFLOW_MODEL_NAME, RELOAD_INTERVAL, LOG_LEVEL
│   ├── deployment.yaml      # Deployment mlops-api (RollingUpdate, probes, security context)
│   ├── hpa.yaml             # HorizontalPodAutoscaler (2→10 réplicas)
│   └── service.yaml         # Service ClusterIP (port 80 → targetPort http 8000)
├── overlays/
│   ├── staging/kustomization.yaml      # namespace mlops-staging, 2 réplicas
│   └── production/kustomization.yaml   # namespace mlops-production, 5 réplicas
└── kustomization.yaml                   # racine : pointe vers base
```

### 4.2 Ressources de la base (`k8s/base/`)

**ConfigMap `mlops-api-config`**

| Variable | Valeur |
|---|---|
| `MLFLOW_TRACKING_URI` | `http://mlflow.mlops.svc.cluster.local:5000` |
| `MLFLOW_MODEL_NAME` | `churn_model` |
| `RELOAD_INTERVAL` | `60` (rechargement périodique du modèle) |
| `LOG_LEVEL` | `info` |

**Deployment `mlops-api`**

- 3 réplicas ; stratégie **RollingUpdate** : `maxUnavailable: 0`, `maxSurge: 1` (zéro interruption).
- Container `api` sur le port 8000, image `ghcr.io/mlops-project/mlops-api` (remplacée en CD), `imagePullPolicy: IfNotPresent`.
- Env : `envFrom` du ConfigMap + du Secret optionnel `mlops-secrets`.
- **Probes** : liveness `/health` (initialDelay 30 s, period 10 s) et readiness `/health` (initialDelay 10 s, period 5 s).
- **Ressources** : requests 200m CPU / 512 Mi mémoire ; limits 1 CPU / 1 Gi mémoire.
- **Security context** : `runAsNonRoot`, `runAsUser: 1000`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`.

**HorizontalPodAutoscaler `mlops-api`**

- `minReplicas: 2`, `maxReplicas: 10`.
- Métriques : CPU à 70 % d'utilisation moyenne, mémoire à 80 %.
- Scale-down stabilisé sur 300 s (`stabilizationWindowSeconds`).

**Service `mlops-api`**

- `type: ClusterIP`, sélecteur `app=mlops-api`, port `80` → `targetPort: http` (8000).

### 4.3 Overlays

| Paramètre | Staging (`mlops-staging`) | Production (`mlops-production`) |
|---|---|---|
| Réplicas | 2 | 5 |
| CPU requests / limits | 200m / 1 | 500m / 2 |
| Mémoire requests / limits | 512Mi / 1Gi | 1Gi / 2Gi |
| Tag d'image par défaut | `staging` | `production` |
| Labels communs | `environment: staging` | `environment: production` |

Les tags sont surchargés au moment du déploiement par `kustomize edit set image` (CD). Le déploiement manuel d'un environnement :

```bash
kubectl create namespace mlops-staging --dry-run=client -o yaml | kubectl apply -f -
kustomize build k8s/overlays/staging | kubectl apply -f -
kubectl rollout status deployment/mlops-api --namespace=mlops-staging --timeout=300s
kubectl get hpa --namespace=mlops-staging
```

---

## 5. GitHub Actions

### 5.1 CI — `.github/workflows/ci.yml`

Déclenchée sur push `main` et toutes les PR. Jobs : `lint`, `security` (bandit, échec si sévérité HIGH), `data-validation` (Great Expectations), `unit-tests` (pytest + couverture), `integration-tests` (pipeline E2E puis `pytest -m integration`), `docker-build` (build API + training, scan **Trivy** avec `exit-code: "1"` sur `HIGH,CRITICAL`).

### 5.2 CD — `.github/workflows/cd.yml`

Déclenchée sur push `main` si les chemins `src/**`, `docker/**`, `k8s/**`, `requirements*.txt` ou `dvc.yaml` changent.

**Job 1 — build-and-push**

- Login GHCR via `GITHUB_TOKEN`, buildx multi-platform avec cache `type=gha`.
- Tag API : `ghcr.io/<repository>-api:<sha du commit>` (jamais `latest`).
- Tag training : `ghcr.io/<repository>-training:<sha du commit>`.
- Le tag est transmis au job suivant via `outputs.image_tag`.

**Job 2 — deploy-staging**

- Environnement GitHub `staging` ; kubeconfig fourni par le secret `KUBECONFIG_STAGING`.
- `kustomize edit set image ghcr.io/mlops-project/mlops-api=<image_tag>` puis `kustomize build k8s/overlays/staging | kubectl apply -f -`.
- Attente du rollout (namespace `mlops`, timeout 300 s).
- **Smoke tests** sur `STAGING_API_URL` : `GET /health` puis `POST /predict` avec un payload complet de churn.

**Job 3 — deploy-production**

- Environnement GitHub `production` (protection : **approbation manuelle** requise).
- Même procédure Kustomize sur `k8s/overlays/production`, namespace `mlops`.
- Vérifications finales : `kubectl get pods`, `kubectl get hpa`.

**Secrets GitHub requis** : `KUBECONFIG_STAGING`, `KUBECONFIG_PRODUCTION`, `STAGING_API_URL`. Les images sont stockées dans le registre GHCR du dépôt (permission `packages: write`).

### 5.3 Build manuel des images

```bash
make docker-build-api         # docker build -f docker/Dockerfile.api -t mlops-api:local .
make docker-build-training    # docker build -f docker/Dockerfile.training -t mlops-training:local .
```

---

## 6. Ordre de déploiement recommandé

1. **Développement local** : `make setup`, `make mlflow-up`, entraîner et promouvoir un modèle (`make train && make evaluate && make promote`).
2. **Stack complète locale** : `make compose-up` — l'API charge alors le modèle depuis le registry.
3. **Données versionnées** : `make dvc-push` vers MinIO.
4. **CI** : valider lint/security/tests/scan Trivy sur une PR.
5. **Images** : pousser sur `main` → CD build-and-push sur GHCR.
6. **Staging** : CD déploie l'overlay staging et exécute les smoke tests.
7. **Production** : approbation manuelle → CD déploie l'overlay production.
