# Plateforme MLOps End-to-End — Documentation Technique Complète

> Système de prédiction en production avec pipeline automatisé d'entraînement, de déploiement, de monitoring et de réentraînement.

---

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble-du-projet)
2. [Architecture globale](#2-architecture-globale)
3. [Stack technique détaillée](#3-stack-technique-détaillée)
4. [Structure du dépôt](#4-structure-du-dépôt)
5. [Composant : Gestion et versioning des données (DVC)](#5-composant--gestion-et-versioning-des-données-dvc)
6. [Composant : Feature Engineering](#6-composant--feature-engineering)
7. [Composant : Tracking d'expériences (MLflow)](#7-composant--tracking-dexpériences-mlflow)
8. [Composant : Model Registry](#8-composant--model-registry)
9. [Composant : Orchestration (Apache Airflow)](#9-composant--orchestration-apache-airflow)
10. [Composant : API d'inférence (FastAPI)](#10-composant--api-dinférence-fastapi)
11. [Composant : Conteneurisation (Docker)](#11-composant--conteneurisation-docker)
12. [Composant : CI/CD (GitHub Actions)](#12-composant--cicd-github-actions)
13. [Composant : Déploiement (Kubernetes)](#13-composant--déploiement-kubernetes)
14. [Composant : Monitoring infrastructure (Prometheus/Grafana)](#14-composant--monitoring-infrastructure-prometheusgrafana)
15. [Composant : Monitoring du modèle et Data Drift (Evidently)](#15-composant--monitoring-du-modèle-et-data-drift-evidently)
16. [Composant : Tests et qualité (pytest, Great Expectations)](#16-composant--tests-et-qualité-pytest-great-expectations)
17. [Boucle de réentraînement automatique](#17-boucle-de-réentraînement-automatique)
18. [Sécurité et gestion des secrets](#18-sécurité-et-gestion-des-secrets)
19. [Plan de mise en œuvre étape par étape](#19-plan-de-mise-en-œuvre-étape-par-étape)
20. [Critères de succès / Definition of Done](#20-critères-de-succès--definition-of-done)
21. [Extensions possibles](#21-extensions-possibles)

---

## 1. Vue d'ensemble du projet

### 1.1 Objectif

Construire une plateforme MLOps complète, reproductible et automatisée, illustrant le cycle de vie complet d'un modèle de Machine Learning, depuis l'ingestion des données jusqu'à la détection de drift en production et le réentraînement automatique — sans intervention manuelle une fois le système déployé.

### 1.2 Cas d'usage type

Le projet est conçu pour être agnostique au cas d'usage, mais fonctionne particulièrement bien avec :
- **Détection de fraude** (classification binaire, données tabulaires, drift fréquent)
- **Prévision de la demande** (régression, séries temporelles, réentraînement périodique naturel)
- **Churn client** (classification binaire, bon pour démontrer le monitoring métier)

### 1.3 Objectifs pédagogiques et professionnels

| Objectif | Ce que ça démontre |
|---|---|
| Reproductibilité | N'importe qui peut cloner et relancer avec une seule commande |
| Traçabilité | Chaque modèle en production est lié à un run MLflow, un commit Git, une version de dataset DVC |
| Automatisation | Pipeline CI/CD réel, pas un notebook isolé |
| Boucle de feedback | Détection de drift → réentraînement → redéploiement automatique |
| Observabilité | Monitoring technique (latence, erreurs) ET monitoring métier (dérive du modèle) |
| Scalabilité | Déploiement Kubernetes avec autoscaling |

### 1.4 Principes directeurs

- **Infrastructure as Code** : tout est versionné (Dockerfiles, manifests K8s, workflows CI/CD)
- **Immutabilité** : chaque image Docker est taguée avec un hash de commit, jamais de `latest` en production
- **Séparation des environnements** : dev / staging / production clairement isolés
- **Fail fast** : les tests bloquent le pipeline avant tout déploiement

---

## 2. Architecture globale

### 2.1 Schéma du flux de données et de contrôle

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ Source de   │────▶│   Airflow    │────▶│  DVC / MinIO   │
│ données     │     │ (ingestion)  │     │ (stockage      │
│ (CSV/API/DB)│     │              │     │  versionné)    │
└─────────────┘     └──────────────┘     └───────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Feature          │
                    │ Engineering      │
                    └──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐      ┌─────────────────┐
                    │  Entraînement    │─────▶│  MLflow Tracking │
                    │  (train.py)      │      │  Server          │
                    └──────────────────┘      └─────────────────┘
                             │                          │
                             ▼                          ▼
                    ┌──────────────────┐      ┌─────────────────┐
                    │ Évaluation       │      │ Model Registry   │
                    │ (evaluate.py)    │─────▶│ (staging/prod)   │
                    └──────────────────┘      └─────────────────┘
                                                        │
                                                        ▼
                    ┌──────────────────┐      ┌─────────────────┐
                    │ GitHub Actions   │─────▶│ Build image      │
                    │ (CI)             │      │ Docker           │
                    └──────────────────┘      └─────────────────┘
                                                        │
                                                        ▼
                    ┌──────────────────┐      ┌─────────────────┐
                    │ GitHub Actions   │─────▶│ Déploiement      │
                    │ (CD)             │      │ Kubernetes        │
                    └──────────────────┘      └─────────────────┘
                                                        │
                                                        ▼
                    ┌──────────────────┐      ┌─────────────────┐
                    │ FastAPI          │◀────▶│ Prometheus /     │
                    │ (inférence)      │      │ Grafana          │
                    └──────────────────┘      └─────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Evidently AI     │
                    │ (drift detection)│
                    └──────────────────┘
                             │
                             ▼ (si drift détecté)
                    ┌──────────────────┐
                    │ Airflow déclenche│
                    │ réentraînement   │
                    └──────────────────┘
                             │
                             └──────────▶ (retour en haut du cycle)
```

### 2.2 Description des couches

| Couche | Responsabilité |
|---|---|
| **Ingestion** | Récupérer les données brutes depuis la source (fichier, API, base) |
| **Stockage versionné** | Garder une trace de chaque version du dataset utilisé |
| **Feature Engineering** | Transformer les données brutes en features exploitables |
| **Entraînement** | Entraîner un ou plusieurs modèles candidats |
| **Tracking** | Logger hyperparamètres, métriques, artefacts de chaque run |
| **Registry** | Stocker les versions de modèles et gérer leur cycle de vie (staging → production → archivé) |
| **CI** | Vérifier automatiquement la qualité du code et des données à chaque changement |
| **CD** | Construire et déployer automatiquement une nouvelle version validée |
| **Service d'inférence** | Exposer le modèle via une API REST |
| **Monitoring infra** | Surveiller la santé technique du service (latence, erreurs, charge) |
| **Monitoring modèle** | Surveiller la dérive des données et la dégradation des performances |
| **Boucle de réentraînement** | Réagir automatiquement à la dérive détectée |

---

## 3. Stack technique détaillée

| Domaine | Outil choisi | Alternatives possibles | Justification du choix |
|---|---|---|---|
| Versioning des données | **DVC** | LakeFS, Pachyderm | Léger, s'intègre nativement à Git, large adoption |
| Stockage objet | **MinIO** | AWS S3, GCS | S3-compatible, peut tourner localement en Docker |
| Orchestration | **Apache Airflow** | Prefect, Dagster | Standard de l'industrie, écosystème riche |
| Tracking d'expériences | **MLflow** | Weights & Biases, Neptune | Open source, auto-hébergeable, registry intégré |
| Registry de modèles | **MLflow Model Registry** | Seldon Core, BentoML | Intégré nativement à MLflow |
| Conteneurisation | **Docker** | Podman | Standard incontesté |
| CI/CD | **GitHub Actions** | GitLab CI, Jenkins | Gratuit pour projets publics, intégré à GitHub |
| Orchestration de conteneurs | **Kubernetes** | Docker Swarm, Nomad | Standard de l'industrie pour la scalabilité |
| Framework API | **FastAPI** | Flask, Django REST | Performant, typage natif, documentation auto-générée |
| Monitoring infra | **Prometheus + Grafana** | Datadog, New Relic | Open source, standard Kubernetes |
| Monitoring modèle | **Evidently AI** | WhyLabs, Arize | Open source, rapports HTML/JSON prêts à l'emploi |
| Tests unitaires | **pytest** | unittest | Standard Python, plugins riches |
| Tests de données | **Great Expectations** | Deequ, Soda | Déclaratif, intégration facile aux pipelines |
| Gestion des secrets | **Kubernetes Secrets + Sealed Secrets** | HashiCorp Vault | Suffisant pour ce périmètre, extensible vers Vault |

---

## 4. Structure du dépôt

```
mlops-project/
│
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Tests, lint, validation données
│       └── cd.yml                      # Build image + push + déploiement
│
├── airflow/
│   ├── dags/
│   │   ├── training_pipeline.py        # DAG d'entraînement complet
│   │   ├── retraining_pipeline.py      # DAG déclenché par le drift
│   │   └── data_ingestion_dag.py       # DAG d'ingestion périodique
│   └── plugins/
│
├── src/
│   ├── data/
│   │   ├── ingestion.py
│   │   ├── preprocessing.py
│   │   └── validation.py               # Great Expectations
│   │
│   ├── features/
│   │   ├── build_features.py
│   │   └── feature_store.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── promote.py                  # Logique staging → production
│   │
│   ├── api/
│   │   ├── main.py                     # App FastAPI
│   │   ├── schemas.py                  # Modèles Pydantic
│   │   ├── model_loader.py             # Chargement depuis MLflow Registry
│   │   └── metrics.py                  # Instrumentation Prometheus
│   │
│   └── monitoring/
│       ├── drift_detection.py          # Evidently
│       └── alerting.py
│
├── tests/
│   ├── unit/
│   │   ├── test_preprocessing.py
│   │   ├── test_features.py
│   │   └── test_api.py
│   ├── integration/
│   │   └── test_pipeline_end_to_end.py
│   └── data/
│       └── test_data_quality.py        # Great Expectations suites
│
├── docker/
│   ├── Dockerfile.api                  # Image API légère (multi-stage)
│   ├── Dockerfile.training             # Image pour jobs d'entraînement
│   └── docker-compose.yml              # Stack locale complète
│
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── hpa.yaml                    # Horizontal Pod Autoscaler
│   ├── overlays/
│   │   ├── staging/
│   │   └── production/
│   └── kustomization.yaml
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       └── dashboards/
│           ├── api-performance.json
│           └── model-drift.json
│
├── mlflow/
│   └── docker-compose.yml              # MLflow server + Postgres + MinIO
│
├── great_expectations/
│   └── expectations/
│       └── dataset_suite.json
│
├── notebooks/
│   └── exploration.ipynb               # EDA, hors pipeline de prod
│
├── dvc.yaml                            # Définition du pipeline DVC
├── dvc.lock
├── .dvc/
│   └── config
│
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── .pre-commit-config.yaml
├── .env.example
├── Makefile
└── README.md
```

---

## 5. Composant : Gestion et versioning des données (DVC)

### 5.1 Rôle

DVC (Data Version Control) permet de versionner des fichiers de données volumineux en parallèle du code Git, sans stocker les données directement dans le dépôt.

### 5.2 Fonctionnement

- Git suit un petit fichier `.dvc` (pointeur/métadonnées + hash)
- Les données réelles sont stockées dans un **remote** (ici MinIO, compatible S3)
- Chaque `dvc add` ou étape de pipeline génère un hash reproductible

### 5.3 Pipeline DVC (`dvc.yaml`)

Le pipeline définit des étapes chaînées, chacune avec ses dépendances et sorties :

```
stages:
  ingest:
    cmd: python src/data/ingestion.py
    outs: [data/raw/dataset.csv]

  preprocess:
    cmd: python src/data/preprocessing.py
    deps: [data/raw/dataset.csv]
    outs: [data/processed/dataset.csv]

  build_features:
    cmd: python src/features/build_features.py
    deps: [data/processed/dataset.csv]
    outs: [data/features/features.parquet]

  train:
    cmd: python src/models/train.py
    deps: [data/features/features.parquet]
    outs: [models/model.pkl]
    metrics: [metrics.json]
```

### 5.4 Commandes clés

| Commande | Effet |
|---|---|
| `dvc init` | Initialise DVC dans le dépôt |
| `dvc remote add -d storage s3://mlops-bucket` | Configure MinIO comme stockage distant |
| `dvc add data/raw/dataset.csv` | Commence à suivre un fichier |
| `dvc repro` | Rejoue le pipeline si des dépendances ont changé |
| `dvc push` / `dvc pull` | Synchronise les données avec le remote |
| `dvc metrics diff` | Compare les métriques entre deux versions |

### 5.5 Bénéfice concret

Si un modèle en production se comporte mal, on peut retrouver **exactement** quel dataset a servi à l'entraîner, en checkoutant le commit Git correspondant puis en faisant `dvc pull`.

---

## 6. Composant : Feature Engineering

### 6.1 Rôle

Transformer les données brutes/nettoyées en variables numériques exploitables par le modèle, de façon **identique** à l'entraînement et à l'inférence (éviter le "training-serving skew").

### 6.2 Bonnes pratiques appliquées

- Les transformations sont encapsulées dans des classes/fonctions réutilisables, importées à la fois par `train.py` et par l'API d'inférence (`model_loader.py`)
- Aucune transformation "à la main" dans un notebook qui ne serait pas répliquée en production
- Les statistiques utilisées pour la normalisation (moyenne, écart-type, catégories vues) sont sauvegardées comme artefacts avec le modèle

### 6.3 Feature Store léger

Pour ce projet, un "feature store" simplifié est un fichier Parquet versionné par DVC, avec un schéma documenté (nom, type, description, plage de valeurs attendue). Une évolution possible est d'utiliser **Feast** pour un vrai feature store en production.

---

## 7. Composant : Tracking d'expériences (MLflow)

### 7.1 Rôle

MLflow Tracking enregistre chaque run d'entraînement : hyperparamètres, métriques, artefacts (modèle, courbes, matrices de confusion), et le code/commit associé.

### 7.2 Architecture du serveur MLflow

```
docker-compose (mlflow/docker-compose.yml) :
  - mlflow-server   (UI + API tracking, port 5000)
  - postgres        (backend store : métadonnées des runs)
  - minio           (artifact store : modèles, fichiers)
```

### 7.3 Exemple d'utilisation dans `train.py`

Le script d'entraînement :
1. Démarre un run MLflow (`mlflow.start_run()`)
2. Logue les hyperparamètres (`mlflow.log_param`)
3. Entraîne le modèle
4. Logue les métriques (`mlflow.log_metric` — accuracy, F1, AUC, etc.)
5. Logue le modèle lui-même (`mlflow.sklearn.log_model` ou équivalent)
6. Logue des artefacts additionnels (matrice de confusion, feature importance)

### 7.4 Ce que ça apporte

- Comparaison visuelle de tous les runs dans l'UI MLflow
- Reproductibilité : chaque run est lié à un commit Git et une version DVC des données
- Base pour la promotion automatique vers le Model Registry

---

## 8. Composant : Model Registry

### 8.1 Rôle

Le Model Registry gère le cycle de vie des modèles au-delà du simple tracking : versions numérotées, stages (`None`, `Staging`, `Production`, `Archived`), et annotations.

### 8.2 Cycle de vie d'un modèle

```
Nouveau run MLflow
        │
        ▼
  Enregistré dans le Registry (version N)
        │
        ▼
  Stage = "Staging"
        │
        ▼
  Tests de validation automatiques (evaluate.py)
        │
   ┌────┴────┐
   ▼         ▼
 Échec     Succès
   │         │
   ▼         ▼
Rejeté   Stage = "Production"
              │
              ▼
     Ancienne version → "Archived"
```

### 8.3 Critères de promotion (`promote.py`)

Un modèle candidat n'est promu en production que s'il :
- Dépasse un seuil de performance minimal (ex : F1 > 0.85)
- Fait mieux que le modèle actuellement en production sur le même jeu de test
- Passe les tests de biais/équité définis (si applicable)

### 8.4 Lien avec l'API

L'API FastAPI charge toujours le modèle marqué `Production` via l'URI `models:/nom_du_modele/Production`, ce qui permet de changer de modèle sans redéployer l'API — un simple changement de stage dans le Registry suffit (bien qu'en pratique, on redéploie quand même pour garder une image immuable et traçable).

---

## 9. Composant : Orchestration (Apache Airflow)

### 9.1 Rôle

Airflow orchestre les pipelines sous forme de DAGs (Directed Acyclic Graphs), gère la planification, les dépendances entre tâches, les retries, et les alertes en cas d'échec.

### 9.2 DAGs du projet

| DAG | Déclencheur | Rôle |
|---|---|---|
| `data_ingestion_dag` | Planifié (ex : toutes les nuits) | Récupère les nouvelles données, les valide, les versionne avec DVC |
| `training_pipeline` | Manuel ou après ingestion | Exécute tout le pipeline : préprocessing → features → entraînement → évaluation → enregistrement MLflow |
| `retraining_pipeline` | Déclenché par détection de drift | Relance l'entraînement avec les données récentes, compare au modèle en prod, promeut si meilleur |

### 9.3 Structure type d'un DAG (`training_pipeline.py`)

```
with DAG("training_pipeline", schedule_interval="@weekly", ...) as dag:

    validate_data = PythonOperator(task_id="validate_data", ...)
    preprocess = PythonOperator(task_id="preprocess", ...)
    build_features = PythonOperator(task_id="build_features", ...)
    train_model = PythonOperator(task_id="train_model", ...)
    evaluate_model = PythonOperator(task_id="evaluate_model", ...)
    promote_model = PythonOperator(task_id="promote_model", ...)
    notify = PythonOperator(task_id="notify_team", ...)

    validate_data >> preprocess >> build_features >> train_model >> evaluate_model >> promote_model >> notify
```

### 9.4 Bonnes pratiques Airflow appliquées

- Chaque tâche est idempotente (peut être relancée sans effet de bord)
- Utilisation de `XCom` pour passer les identifiants de run MLflow entre tâches
- Alertes Slack/e-mail en cas d'échec (`on_failure_callback`)
- Séparation claire entre logique métier (dans `src/`) et orchestration (dans `airflow/dags/`) — les DAGs appellent des fonctions, ils ne contiennent pas de logique lourde

---

## 10. Composant : API d'inférence (FastAPI)

### 10.1 Rôle

Exposer le modèle en production via une API REST performante, typée et documentée automatiquement.

### 10.2 Endpoints principaux

| Endpoint | Méthode | Rôle |
|---|---|---|
| `/predict` | POST | Retourne une prédiction pour un ou plusieurs enregistrements |
| `/health` | GET | Healthcheck pour Kubernetes (liveness/readiness probes) |
| `/metrics` | GET | Expose les métriques au format Prometheus |
| `/model-info` | GET | Retourne la version du modèle actuellement chargé |

### 10.3 Chargement du modèle (`model_loader.py`)

Le modèle est chargé une seule fois au démarrage de l'application (pas à chaque requête), directement depuis le MLflow Model Registry via son URI (`models:/nom_du_modele/Production`). Un rechargement périodique ou déclenché par webhook peut être ajouté pour prendre en compte les nouvelles promotions sans redémarrage complet.

### 10.4 Validation des entrées (`schemas.py`)

Utilisation de **Pydantic** pour définir strictement le schéma attendu en entrée (types, plages de valeurs, champs obligatoires), ce qui rejette automatiquement les requêtes malformées avec un code 422 et un message clair.

### 10.5 Instrumentation (`metrics.py`)

L'API expose nativement :
- Nombre de requêtes par endpoint et code de statut
- Latence des prédictions (histogramme)
- Distribution des valeurs prédites (pour alimenter le monitoring de drift)

---

## 11. Composant : Conteneurisation (Docker)

### 11.1 Stratégie multi-stage

Le `Dockerfile.api` utilise un build multi-stage pour réduire la taille finale de l'image :

```
Stage 1 (builder)  : installe les dépendances, compile si nécessaire
Stage 2 (runtime)  : copie uniquement le nécessaire depuis le builder,
                      utilise une image de base slim (python:3.11-slim),
                      exécute en tant qu'utilisateur non-root
```

### 11.2 Bonnes pratiques appliquées

- Image de base minimale (`slim` ou `distroless`)
- Un seul processus par conteneur (principe de responsabilité unique)
- `.dockerignore` pour exclure notebooks, données, `.git`
- Healthcheck défini dans le Dockerfile
- Utilisateur non-root pour la sécurité
- Tag d'image basé sur le hash du commit Git, jamais `latest` en production

### 11.3 `docker-compose.yml` (environnement local complet)

Permet de lancer toute la stack en une commande pour le développement :
- API FastAPI
- MLflow server + Postgres + MinIO
- Prometheus + Grafana
- (Optionnel) Airflow en mode standalone

---

## 12. Composant : CI/CD (GitHub Actions)

### 12.1 Pipeline CI (`ci.yml`) — déclenché à chaque push/PR

Étapes exécutées :
1. **Lint** : `ruff` ou `flake8` + `black --check`
2. **Tests unitaires** : `pytest tests/unit`
3. **Tests de qualité des données** : suites Great Expectations
4. **Tests d'intégration** : pipeline complet sur un échantillon de données
5. **Scan de sécurité** : `bandit` (code) + `trivy` (image Docker)
6. **Build de test** : vérifie que l'image Docker se construit sans erreur

### 12.2 Pipeline CD (`cd.yml`) — déclenché sur merge vers `main`

Étapes exécutées :
1. Build de l'image Docker taguée avec le hash du commit
2. Push vers GitHub Container Registry (GHCR)
3. Mise à jour du manifest Kubernetes (nouveau tag d'image) via Kustomize
4. Déploiement en **staging** automatique
5. Tests de fumée (smoke tests) sur staging
6. Déploiement en **production** (approbation manuelle via GitHub Environments, recommandé pour un projet "pro")
7. Rolling update Kubernetes avec vérification de santé avant bascule complète

### 12.3 Exemple de structure du workflow CD

```
jobs:
  build-and-push:
    - checkout
    - build Docker image (tag = git sha)
    - push to GHCR

  deploy-staging:
    needs: build-and-push
    - kubectl apply -k k8s/overlays/staging
    - run smoke tests

  deploy-production:
    needs: deploy-staging
    environment: production   # nécessite approbation manuelle
    - kubectl apply -k k8s/overlays/production
    - verify rollout status
```

---

## 13. Composant : Déploiement (Kubernetes)

### 13.1 Ressources principales

| Fichier | Rôle |
|---|---|
| `deployment.yaml` | Définit les pods de l'API (replicas, image, ressources CPU/RAM, probes) |
| `service.yaml` | Expose les pods en interne (ClusterIP) ou en externe (LoadBalancer) |
| `configmap.yaml` | Variables de configuration non sensibles (URL MLflow, nom du modèle) |
| `hpa.yaml` | Horizontal Pod Autoscaler — scale automatiquement selon CPU/latence |

### 13.2 Exemple conceptuel de `deployment.yaml`

- `replicas: 3` (haute disponibilité)
- `livenessProbe` sur `/health` (redémarre le pod s'il est bloqué)
- `readinessProbe` sur `/health` (retire le pod du load balancer s'il n'est pas prêt)
- `resources.requests` / `resources.limits` définis pour éviter la sur-consommation
- Stratégie de déploiement `RollingUpdate` avec `maxUnavailable: 0` pour zéro downtime

### 13.3 Organisation avec Kustomize

- `base/` : configuration commune
- `overlays/staging/` et `overlays/production/` : surcharges spécifiques (nombre de replicas, ressources, variables d'environnement)

### 13.4 Autoscaling (`hpa.yaml`)

Le HPA ajuste le nombre de pods entre un minimum et un maximum en fonction de l'utilisation CPU moyenne (ou d'une métrique custom comme la latence via Prometheus Adapter).

---

## 14. Composant : Monitoring infrastructure (Prometheus/Grafana)

### 14.1 Rôle

Surveiller la santé technique du système : disponibilité, latence, taux d'erreur, charge.

### 14.2 Flux de collecte

```
FastAPI (/metrics) ──scrape──▶ Prometheus ──requête──▶ Grafana (dashboards)
                                     │
                                     ▼
                              Alertmanager (alertes Slack/e-mail)
```

### 14.3 Métriques clés suivies

- `http_requests_total` (par endpoint, par code de statut)
- `http_request_duration_seconds` (histogramme de latence)
- `model_prediction_value` (distribution des prédictions — utile pour le drift)
- Métriques infra standard (CPU, mémoire des pods) via `kube-state-metrics`

### 14.4 Dashboards Grafana fournis

- **API Performance** : latence p50/p95/p99, taux d'erreur, requêtes/seconde
- **Model Drift** : évolution de la distribution des prédictions et des features dans le temps

### 14.5 Alertes types configurées

| Alerte | Condition |
|---|---|
| Latence élevée | p95 > 500ms pendant 5 minutes |
| Taux d'erreur élevé | > 5% de 5xx pendant 5 minutes |
| Pod en crash loop | Redémarrages répétés détectés |

---

## 15. Composant : Monitoring du modèle et Data Drift (Evidently)

### 15.1 Rôle

Détecter quand les données reçues en production divergent significativement des données d'entraînement (data drift), ou quand les performances du modèle se dégradent (concept drift).

### 15.2 Fonctionnement (`drift_detection.py`)

1. Un échantillon des requêtes de production est loggé (features + prédiction)
2. Périodiquement (ex : chaque jour via un DAG Airflow dédié), Evidently compare ce jeu de données récent au jeu de données de référence (celui utilisé à l'entraînement)
3. Un rapport est généré (HTML + JSON) avec des tests statistiques par feature (ex : test de Kolmogorov-Smirnov pour les variables numériques, chi carré pour les catégorielles)
4. Un score global de drift est calculé

### 15.3 Déclenchement du réentraînement

Si le score de drift dépasse un seuil défini (ex : plus de 30% des features montrent une dérive significative), Airflow déclenche automatiquement le DAG `retraining_pipeline`.

### 15.4 Ce que ça démontre

C'est la brique qui transforme un simple pipeline de déploiement en véritable **système MLOps auto-adaptatif** — le modèle ne se dégrade pas silencieusement en production.

---

## 16. Composant : Tests et qualité (pytest, Great Expectations)

### 16.1 Pyramide de tests du projet

```
        ┌─────────────────────┐
        │  Tests end-to-end   │   (pipeline complet sur échantillon)
        ├─────────────────────┤
        │  Tests d'intégration│   (interaction entre composants)
        ├─────────────────────┤
        │  Tests unitaires    │   (fonctions individuelles)
        └─────────────────────┘
```

### 16.2 Tests unitaires (`tests/unit/`)

- `test_preprocessing.py` : vérifie que le nettoyage produit le schéma attendu
- `test_features.py` : vérifie les transformations de features (valeurs limites, NaN, types)
- `test_api.py` : teste les endpoints FastAPI avec `TestClient` (cas valides et invalides)

### 16.3 Tests de qualité des données (Great Expectations)

Suites d'attentes déclaratives, par exemple :
- Une colonne ne doit jamais contenir de valeurs nulles
- Une colonne numérique doit rester dans une plage définie
- Le nombre de lignes du dataset doit être supérieur à un seuil minimal
- Les types de colonnes doivent correspondre au schéma attendu

Ces tests s'exécutent **avant** l'entraînement, pour éviter d'entraîner un modèle sur des données corrompues.

### 16.4 Tests d'intégration

Vérifient que le pipeline complet (ingestion → features → entraînement → enregistrement MLflow) fonctionne de bout en bout sur un petit échantillon, en environnement CI.

---

## 17. Boucle de réentraînement automatique

### 17.1 Vue d'ensemble

C'est la caractéristique qui distingue un projet MLOps "complet" d'un simple pipeline de déploiement.

### 17.2 Déclencheurs possibles

| Déclencheur | Description |
|---|---|
| **Planifié** | Réentraînement périodique systématique (ex : chaque semaine) |
| **Basé sur le drift** | Déclenché par Evidently quand le score de drift dépasse un seuil |
| **Basé sur la performance** | Déclenché si les métriques de performance réelles (si le label devient disponible a posteriori) chutent sous un seuil |
| **Manuel** | Déclenchement depuis l'UI Airflow par un data scientist |

### 17.3 Séquence complète

```
1. Détection (drift ou planning) 
        ↓
2. Airflow déclenche retraining_pipeline
        ↓
3. Récupération des données les plus récentes (versionnées via DVC)
        ↓
4. Réentraînement (même code que train.py, nouvelles données)
        ↓
5. Évaluation comparative vs modèle en production actuel
        ↓
6. Si meilleur → promotion automatique en Staging
        ↓
7. Tests de validation automatiques supplémentaires
        ↓
8. Si validé → promotion en Production dans MLflow Registry
        ↓
9. Déclenchement du pipeline CD → nouvelle image → déploiement K8s
        ↓
10. Monitoring renforcé pendant 24-48h (canary implicite)
```

### 17.4 Garde-fous importants

- Un modèle réentraîné n'est **jamais** promu automatiquement sans passer les mêmes seuils de qualité que lors du déploiement initial
- Conservation systématique des N dernières versions en production pour un rollback rapide
- Notification de l'équipe à chaque promotion automatique (traçabilité humaine même dans un système automatisé)

---

## 18. Sécurité et gestion des secrets

### 18.1 Principes appliqués

- Aucun secret (mots de passe, clés API, credentials MinIO/S3) n'est commité dans le dépôt
- `.env.example` documente les variables nécessaires sans valeurs réelles
- En Kubernetes : utilisation de `Secrets` natifs, idéalement chiffrés avec **Sealed Secrets** ou gérés via **HashiCorp Vault** pour un contexte entreprise
- Scan automatique des images Docker (`trivy`) et du code (`bandit`) dans la CI
- Communication interne entre services via réseau privé Kubernetes (pas d'exposition inutile)
- Principe du moindre privilège pour les comptes de service (RBAC Kubernetes)

### 18.2 Exemple de flux de secret en production

```
Secret créé manuellement/via Vault
        ↓
Monté comme variable d'environnement ou volume dans le pod
        ↓
Jamais loggé, jamais exposé dans /metrics ou /health
```

---

## 19. Plan de mise en œuvre étape par étape

| Étape | Livrable | Durée indicative |
|---|---|---|
| 1 | Setup infra locale (docker-compose : MLflow + MinIO + Postgres) | 0.5 jour |
| 2 | Pipeline de données + DVC | 1 jour |
| 3 | Feature engineering + tests unitaires associés | 1 jour |
| 4 | Script d'entraînement + tracking MLflow | 1 jour |
| 5 | Model Registry + logique de promotion | 0.5 jour |
| 6 | API FastAPI + chargement depuis Registry | 1 jour |
| 7 | Dockerisation (multi-stage) | 0.5 jour |
| 8 | CI GitHub Actions (lint, tests, scan) | 1 jour |
| 9 | Manifests Kubernetes (local avec kind/minikube) | 1 jour |
| 10 | CD GitHub Actions (build, push, déploiement) | 1 jour |
| 11 | DAGs Airflow (ingestion, training, retraining) | 1.5 jour |
| 12 | Monitoring Prometheus/Grafana | 1 jour |
| 13 | Détection de drift avec Evidently | 1 jour |
| 14 | Intégration de la boucle de réentraînement complète | 1 jour |
| 15 | Documentation finale + README + démo | 0.5 jour |

**Durée totale estimée : ~13-14 jours** pour une implémentation complète et soignée.

---

## 20. Critères de succès / Definition of Done

- [ ] `docker-compose up` lance toute la stack locale sans erreur
- [ ] Un `dvc repro` complet reproduit exactement les mêmes métriques
- [ ] Chaque run d'entraînement apparaît dans l'UI MLflow avec tous ses paramètres
- [ ] Un modèle peut être promu de Staging à Production via `promote.py`
- [ ] L'API répond correctement sur `/predict`, `/health`, `/metrics`
- [ ] Un push sur `main` déclenche automatiquement CI puis CD jusqu'en staging
- [ ] Le déploiement en production nécessite une approbation manuelle (bonne pratique)
- [ ] Les dashboards Grafana affichent des données en temps réel
- [ ] Un rapport Evidently peut être généré manuellement et détecte un drift simulé
- [ ] Le DAG `retraining_pipeline` se déclenche correctement sur un drift simulé
- [ ] Rollback possible en moins de 5 minutes en cas de problème (retour à l'image précédente)

---

## 21. Extensions possibles (pour aller plus loin)

| Extension | Valeur ajoutée |
|---|---|
| **Feast** (feature store complet) | Cohérence garantie entre features online/offline |
| **Seldon Core / KServe** | Serving avancé (A/B testing, canary, explainability intégrée) |
| **HashiCorp Vault** | Gestion de secrets de niveau entreprise |
| **Argo CD** | GitOps pour le déploiement Kubernetes (au lieu de `kubectl apply` en CI) |
| **Explainability (SHAP)** | Endpoint `/explain` pour justifier chaque prédiction |
| **Tests de biais/équité** | Vérification automatique de fairness avant promotion |
| **Chaos engineering (Chaos Mesh)** | Valider la résilience du système en production |
| **Multi-modèles / Champion-Challenger** | Comparer plusieurs modèles en production simultanément |

---

## Annexe : Glossaire rapide

| Terme | Définition |
|---|---|
| **Data drift** | Changement dans la distribution des données d'entrée en production par rapport à l'entraînement |
| **Concept drift** | Changement dans la relation entre les features et la cible à prédire |
| **Model Registry** | Système de gestion des versions de modèles et de leur cycle de vie |
| **Canary deployment** | Déploiement progressif d'une nouvelle version sur un sous-ensemble du trafic |
| **Rolling update** | Mise à jour progressive des pods sans interruption de service |
| **Idempotence** | Propriété d'une opération pouvant être répétée sans changer le résultat au-delà de la première exécution |
