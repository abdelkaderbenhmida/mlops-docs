# Plateforme MLOps de Prévision de la Demande — Documentation Technique Complète

> Produit cible : **plateforme de prévision de la demande (demand forecasting)** pour la distribution de détail — prédiction des unités vendues (`units_sold`) par magasin et par SKU, avec une boucle de réentraînement fermée : ingestion → validation → features → entraînement → évaluation avec portes de qualité → promotion → monitoring de drift → réentraînement déclenché.
>
> Cette spécification décrit l'état réel du dépôt : un système MLOps complet d'entraînement et de service d'un **RandomForestRegressor** pour la prévision de la demande, orchestré par Airflow, versionné par DVC, tracé par MLflow, servi par FastAPI, déployé sur Kubernetes et surveillé par Prometheus/Grafana.

---

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble-du-projet)
2. [Le problème métier : la prévision de la demande](#2-le-problème-métier--la-prévision-de-la-demande)
3. [Architecture globale](#3-architecture-globale)
4. [Stack technique détaillée](#4-stack-technique-détaillée)
5. [Structure du dépôt](#5-structure-du-dépôt)
6. [Composant : Gestion et versioning des données (DVC)](#6-composant--gestion-et-versioning-des-données-dvc)
7. [Composant : Feature Engineering](#7-composant--feature-engineering)
8. [Composant : Tracking d'expériences (MLflow)](#8-composant--tracking-dexpériences-mlflow)
9. [Composant : Model Registry](#9-composant--model-registry)
10. [Composant : Orchestration (Apache Airflow)](#10-composant--orchestration-apache-airflow)
11. [Composant : Service d'inférence (FastAPI)](#11-composant--service-dinférence-fastapi)
12. [Composant : Conteneurisation (Docker)](#12-composant--conteneurisation-docker)
13. [Composant : CI/CD (GitHub Actions)](#13-composant--cicd-github-actions)
14. [Composant : Déploiement (Kubernetes)](#14-composant--déploiement-kubernetes)
15. [Composant : Monitoring infrastructure (Prometheus/Grafana)](#15-composant--monitoring-infrastructure-prometheusgrafana)
16. [Composant : Monitoring du modèle et Data Drift](#16-composant--monitoring-du-modèle-et-data-drift)
17. [Composant : Tests et qualité (pytest, Great Expectations)](#17-composant--tests-et-qualité-pytest-great-expectations)
18. [Boucle de réentraînement automatique](#18-boucle-de-réentraînement-automatique)
19. [Sécurité et gestion des secrets](#19-sécurité-et-gestion-des-secrets)
20. [Métriques de succès](#20-métriques-de-succès)
21. [Plan de mise en œuvre étape par étape](#21-plan-de-mise-en-œuvre-étape-par-étape)
22. [Critères de succès / Definition of Done](#22-critères-de-succès--definition-of-done)
23. [Risques honnêtes](#23-risques-honnêtes)
24. [Extensions possibles (roadmap)](#24-extensions-possibles-roadmap)
25. [Annexe : Glossaire rapide](#annexe--glossaire-rapide)

---

## 1. Vue d'ensemble du projet

### 1.1 Objectif

Construire une plateforme MLOps complète, reproductible et automatisée pour la **prévision de la demande en distribution de détail** : pour un couple magasin/SKU et un jour donné, le modèle prédit le nombre d'unités vendues (`units_sold`). La boucle est fermée : les données sont ingérées, validées, transformées en features, entraînées avec tracking, évaluées contre des portes de qualité, promues en production si elles passent, servies via une API REST, et surveillées pour détecter le drift avant qu'il ne dégrade les prévisions.

Le système repose sur les composants MLOps suivants, tous présents dans le dépôt :

- Ingestion et versioning des données (DVC + MinIO)
- Validation des données (Great Expectations)
- Feature engineering avec parité entraînement/inférence (`FeatureTransformer`)
- Entraînement avec tracking (MLflow) et Model Registry
- Évaluation avec portes de qualité (R² ≥ 0,60, MAPE ≤ 25 %) et promotion conditionnelle
- Service d'inférence en ligne (FastAPI) avec prévision unitaire ou par lot
- Monitoring technique (Prometheus/Grafana) et de drift des données (tests de Kolmogorov-Smirnov)
- Orchestration des pipelines (Airflow) : ingestion, entraînement hebdomadaire, réentraînement déclenché par drift

### 1.2 Le problème métier : la prévision de la demande

Une chaîne de distribution doit décider chaque jour **combien d'unités réapprovisionner par magasin et par SKU**. Deux erreurs opposées coûtent cher :

| Erreur | Mécanisme | Coût |
|---|---|---|
| **Surstock (overstock)** | Prévision trop haute → marchandise immobilisée, coût de stockage, démarques, péremption | Marge détruite, capital bloqué |
| **Rupture (stockout)** | Prévision trop basse → rayon vide, vente perdue, client passé chez le concurrent | Revenu perdu, fidélité érodée |

La décision est **continue** (combien d'unités ?) et non binaire — d'où un problème de **régression**, pas de classification. Les métriques doivent refléter ce coût : l'**RMSE** (erreur quadratique moyenne) pénalise les grosses erreurs (une rupture sur un article très demandé coûte plus qu'une petite erreur), le **MAPE** donne une lecture interprétable en pourcentage d'écart par rapport aux ventes réelles, et le **R²** mesure le pouvoir explicatif par rapport à la moyenne naïve.

### 1.3 Pourquoi ce cas d'usage valide l'architecture

| Composant | Rôle dans la prévision de la demande |
|---|---|
| DAG de réentraînement Airflow | La saisonnalité (jour de semaine, mois, fériés) et les promotions changent la relation features → demande ; un modèle obsolète se dégrade en quelques semaines |
| Détection de drift (KS) | Les habitudes d'achat, les assortiments et les prix évoluent ; les distributions de features en production dérivent de la référence d'entraînement |
| DVC | Reproduire exactement quel snapshot de données a servi à entraîner chaque modèle |
| Kubernetes + HPA | Le trafic de prévision est variable (campagnes, fin de mois) ; autoscaling sur CPU/mémoire |
| Tags d'image immuables | Savoir quelle version de modèle a produit quelle prévision — exigence de traçabilité |
| RollingUpdate | Un mauvais modèle déployé produit des prévisions fausses immédiatement visibles ; retour arrière sans interruption |
| Approbation manuelle pour la prod | Auto-promouvoir un modèle qui n'a pas passé les portes de qualité, c'est dégrader les prévisions de toute une chaîne |

### 1.4 Objectifs du projet

| Objectif | Ce que ça démontre |
|---|---|
| Reproductibilité | `dvc repro` + `make train` relancent le pipeline complet sur le même snapshot |
| Traçabilité | Chaque modèle en production est lié à un run MLflow, un commit Git, une version de dataset DVC |
| Automatisation | Pipeline CI/CD réel, pas un notebook isolé |
| Boucle de feedback | Drift détecté → réentraînement déclenché → évaluation → promotion conditionnelle |
| Observabilité | Monitoring technique (latence, erreurs) ET monitoring modèle (drift, distribution des prévisions) |
| Scalabilité | Déploiement Kubernetes avec Horizontal Pod Autoscaler |
| Qualité | Portes d'évaluation (R² ≥ 0,60 ; MAPE ≤ 25 %) bloquent la promotion des modèles faibles |

### 1.5 Principes directeurs

- **Infrastructure as Code** : tout est versionné (Dockerfiles, manifests K8s, workflows CI/CD)
- **Immutabilité** : chaque image Docker est taguée avec le hash de commit, jamais de `latest` en production
- **Séparation des environnements** : staging / production isolés, promotion via approbation manuelle (GitHub Environments)
- **Fail fast** : les tests bloquent le pipeline avant tout déploiement
- **Parité entraînement/inférence** : le même `FeatureTransformer` (config sérialisée dans `features_config.json`) est appliqué à l'entraînement et à l'inférence — zéro training-serving skew
- **Portes de qualité avant promotion** : un candidat ne devient production que s'il passe l'évaluation (R², MAPE) et bat le modèle en place

---

## 2. Le problème métier : la prévision de la demande

### 2.1 Le jeu de données

Le dépôt contient un jeu de données synthétique de démonstration (`data/raw/demand_data.csv`) : ventes quotidiennes par magasin et par SKU. Colonnes :

| Colonne | Type | Rôle |
|---|---|---|
| `store_id` | int (1–100) | Identifiant du magasin |
| `sku_id` | int (1–200) | Identifiant du produit |
| `date` | str | Date de la vente (conservée, non utilisée par le modèle) |
| `day_of_week` | int (0–6) | Jour de la semaine |
| `month` | int (1–12) | Mois |
| `is_holiday` | int (0/1) | Jour férié |
| `price` | float | Prix de vente |
| `promotion` | int (0/1) | Produit en promotion |
| `temperature` | float | Température extérieure |
| `inventory_level` | int | Niveau de stock |
| `competitor_price` | float | Prix du concurrent |
| `store_traffic` | int | Fréquentation du magasin |
| `units_sold` | int | **Cible** : unités vendues |

Le prétraitement (`src/data/preprocessing.py`) :
1. Coercition de toutes les colonnes numériques (les valeurs non convertibles deviennent `NaN`)
2. Suppression des lignes avec valeurs numériques manquantes
3. Filtrage des lignes où `units_sold < 0`
4. Normalisation de la colonne `date` en chaîne nettoyée
5. Sortie : `data/processed/demand_data.csv`

### 2.2 Le modèle

Un **RandomForestRegressor** (scikit-learn) est entraîné sur les 11 features (`src/models/train.py`) :

```python
params = {
    "n_estimators": 300,
    "max_depth": 15,
    "min_samples_leaf": 5,
    "max_features": "sqrt",
    "random_state": 42,
    "n_jobs": -1,
}
```

Split **80/20** (`train_test_split(test_size=0.2, random_state=42)`). Cible : `units_sold`.

**Pourquoi une forêt aléatoire ?** Robuste aux non-linéarités et interactions (prix × promotion × férié), pas de normalisation requise, peu d'hyperparamètres sensibles, inférence en millisecondes, et `feature_importances_` fourni nativement pour analyser l'influence de chaque variable.

### 2.3 Métriques et portes de qualité

| Métrique | Définition | Rôle |
|---|---|---|
| **RMSE** | √(moyenne((ŷ − y)²)) | Erreur principale, en unités vendues ; pénalise les grosses erreurs |
| **MAE** | moyenne(\|ŷ − y\|) | Erreur moyenne absolue, robuste aux outliers |
| **R²** | 1 − Σ(ŷ−y)² / Σ(ȳ−y)² | Pouvoir explicatif vs la moyenne naïve |
| **MAPE** | moyenne(\|ŷ − y\| / y) × 100 % (y ≠ 0) | Erreur relative en pourcentage, interprétable métier |

Le MAPE est calculé **exclusivement sur les lignes où `y ≠ 0`** (division par zéro évitée).

**Portes de qualité** (`src/models/evaluate.py`, `DEFAULT_THRESHOLDS`) :

| Porte | Seuil | Direction |
|---|---|---|
| `min_r2` | 0,60 | R² ≥ 0,60 |
| `max_mape` | 25,0 | MAPE ≤ 25 % |

Le rapport d'évaluation est écrit dans `models/evaluation/latest_report.json` ; si les portes ne sont pas franchies, `evaluate.py` **sort en code d'erreur non nul** (bloque le pipeline). Le rapport actuel (voir [Risques honnêtes](#23-risques-honnêtes)) montre un candidat qui **ne passe pas** les portes — comportement correct et attendu du mécanisme.

---

## 3. Architecture globale

### 3.1 Schéma du flux de données et de contrôle
```mermaid
flowchart TD
    raw_data[/Données brutes (data/external/dataset.csv)/] -->|DVC stage: ingest| ingest[DVC stage: ingest]
    ingest -->|preprocessing| preprocess[DVC stage: preprocess]
    preprocess -->|Great Expectations validation| ge[Great Expectations validation]
    ge -->|build features| features[DVC stage: build_features]
    features -->|train| train[Entraînement]
    train -->|evaluate| evaluate[Évaluation]
    evaluate -->|promotion| promote[Promotion]
    promote -->|service| api[Service d'inférence FastAPI]
    api -->|monitoring| monitoring[Monitoring infrastructure]
    monitoring -->|drift detection| drift[Détection de drift KS]
    drift -->|retraining pipeline| airflow[Airflow: retraining_pipeline]
    airflow -->|new model| registry[Model Registry]
```
        Données brutes (data/external/dataset.csv)
                        │
        ┌───────────────▼───────────────┐
        │ DVC stage: ingest             │  python src/data/ingestion.py
        │ (CSV ou URL → data/raw/)      │
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ DVC stage: preprocess         │  python src/data/preprocessing.py
        │ nettoyage numérique           │  → data/processed/demand_data.csv
        └───────────────┬───────────────┘
                        │   Great Expectations (validation.py)
                        ▼
        ┌───────────────────────────────┐
        │ DVC stage: build_features     │  python src/features/build_features.py
        │ FeatureTransformer (mean/std) │  → data/features/features.parquet
        │ + features_config.json        │      + schéma documenté (feature_store.py)
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ DVC stage: train              │  python src/models/train.py
        │ RandomForestRegressor 80/20   │  → models/model.pkl, metrics.json
        │ + MLflow tracking + registry  │  → data/monitoring/reference.csv
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ Évaluation (evaluate.py)      │  portes : R² ≥ 0,60 ; MAPE ≤ 25 %
        │ → latest_report.json          │  → code non nul si portes non passées
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ Promotion (promote.py)        │  Staging → Production (registry)
        │ si portes passées ET candidat │  → production_report.json
        │ ≥ production sur le même test │
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ Service d'inférence FastAPI   │  POST /predict (unitaire ou lot)
        │ model_loader: registry →      │  GET /health, /model-info, /metrics
        │ local model.pkl (fallback)    │  UI : GET / (ui/index.html)
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │ Monitoring                    │
        │ Prometheus (/metrics)         │  Grafana (api-performance, model-drift)
        │ Drift KS vs reference.csv     │  alerting.py (Slack + alerts.jsonl)
        └───────────────┬───────────────┘
                        │ drift_detected
                        ▼
        ┌───────────────────────────────┐
        │ Airflow: retraining_pipeline  │  @daily, short-circuit si pas de drift
        │ preprocess → features → train │  → evaluate → promote si meilleur
        │ + training_pipeline @weekly   │
        └───────────────────────────────┘
```

### 3.2 Description des couches

| Couche | Responsabilité |
|---|---|
| **Ingestion** | Récupérer les données brutes depuis une source (fichier CSV ou URL), idempotent, vers `data/raw/` |
| **Prétraitement** | Nettoyage numérique, suppression des lignes invalides, filtre `units_sold ≥ 0` |
| **Validation des données** | Suites d'attentes Great Expectations, exécutées avant entraînement |
| **Feature engineering** | `FeatureTransformer` : statistiques numériques (moyenne, écart-type), ordre de features fixe, config sérialisée pour parité entraînement/inférence |
| **Feature store** | Parquet versionné par DVC + schéma documenté (nom, type, description, plage attendue) |
| **Entraînement** | RandomForestRegressor, split 80/20, tracking MLflow, enregistrement au registry |
| **Évaluation** | Métriques rmse/mae/r2/mape sur le jeu de test, portes R² ≥ 0,60 et MAPE ≤ 25 % |
| **Promotion** | Staging → Production si portes passées et candidat ≥ champion ; archivage de l'ancienne version |
| **Service d'inférence** | FastAPI : `/predict` unitaire ou par lot, bucket de demande, validation Pydantic stricte |
| **Orchestration** | Airflow : ingestion nocturne, entraînement hebdomadaire, réentraînement quotidien déclenché par drift |
| **Monitoring infra** | Prometheus/Grafana : latence, erreurs, disponibilité, alertes |
| **Monitoring modèle** | Drift par test de Kolmogorov-Smirnov par feature, score global, déclenchement du réentraînement |
| **Boucle de réentraînement** | Réagir automatiquement au drift, avec promotion conditionnelle et notification |

---

## 4. Stack technique détaillée

| Domaine | Outil choisi | Alternatives possibles | Justification du choix |
|---|---|---|---|
| Versioning des données | **DVC** | LakeFS, Pachyderm | Léger, s'intègre nativement à Git |
| Stockage objet | **MinIO** | AWS S3, GCS | S3-compatible, tourne localement en Docker |
| Orchestration | **Apache Airflow** | Prefect, Dagster | Standard de l'industrie ; DAGs ingestion/training/retraining |
| Tracking d'expériences | **MLflow** | Weights & Biases, Neptune | Open source, auto-hébergeable, registry intégré |
| Registry de modèles | **MLflow Model Registry** | Seldon Core, BentoML | Intégré nativement à MLflow |
| Conteneurisation | **Docker** | Podman | Standard incontesté |
| CI/CD | **GitHub Actions** | GitLab CI, Jenkins | Intégré à GitHub ; CI (lint, sécurité, données, tests) + CD (staging → production) |
| Orchestration de conteneurs | **Kubernetes + Kustomize** | Docker Swarm, Nomad | Standard industriel ; HPA sur CPU/mémoire, overlays staging/production |
| Framework API | **FastAPI** | Flask, Django REST | Performant, typage natif (Pydantic), documentation auto-générée |
| Monitoring infra | **Prometheus + Grafana** | Datadog, New Relic | Open source, standard Kubernetes |
| Monitoring modèle | **Tests de Kolmogorov-Smirnov (scipy)** | Evidently, WhyLabs | Test statistique par feature ; score de drift = fraction de features dérivées |
| Alerting | **Slack webhook + journal local** (`alerts.jsonl`) | e-mail, PagerDuty | Zéro dépendance ; le journal local est toujours écrit |
| Tests unitaires | **pytest** | unittest | Standard Python, 57 tests |
| Tests de données | **Great Expectations** | Deequ, Soda | Déclaratif, fallback intégré si la bibliothèque absente |
| Modèle | **RandomForestRegressor** | GBM, XGBoost | Robuste, non-linéaire, inférence rapide, importances natives |
| Gestion des secrets | **GitHub Secrets + Kubernetes Secrets (optionnel)** | HashiCorp Vault | Suffisant pour ce périmètre |

---

## 5. Structure du dépôt

```
mlops-project/
│
├── .github/workflows/
│   ├── ci.yml                      # Lint, sécurité, validation données, tests
│   └── cd.yml                      # Build image (tag = sha) + staging + production (approbation)
│
├── airflow/
│   ├── dags/
│   │   ├── data_ingestion_dag.py   # Ingestion nocturne + validation + DVC push (MinIO)
│   │   ├── training_pipeline.py    # Pipeline complet hebdomadaire (validate → … → promote)
│   │   └── retraining_pipeline.py  # Quotidien, short-circuit si pas de drift
│   └── plugins/
│       └── drift_sensor.py         # DriftDetectedSensor (polls drift_report.json)
│
├── src/
│   ├── data/
│   │   ├── ingestion.py            # Ingestion CSV/URL → data/raw/
│   │   ├── preprocessing.py        # Nettoyage → data/processed/demand_data.csv
│   │   └── validation.py           # Great Expectations (fallback intégré)
│   │
│   ├── features/
│   │   ├── build_features.py       # FeatureTransformer + FEATURE_ORDER + TARGET
│   │   └── feature_store.py        # Parquet versionné + schéma documenté
│   │
│   ├── models/
│   │   ├── train.py                # RandomForestRegressor + MLflow + registry
│   │   ├── evaluate.py             # Métriques + portes (R² ≥ 0,60 ; MAPE ≤ 25 %)
│   │   └── promote.py              # Staging → Production conditionnel
│   │
│   ├── api/
│   │   ├── main.py                 # App FastAPI — service d'inférence
│   │   ├── schemas.py              # Pydantic : requête/réponse, buckets de demande
│   │   ├── model_loader.py         # Chargement registry → fallback local
│   │   └── metrics.py              # Instrumentation Prometheus
│   │
│   └── monitoring/
│       ├── drift_detection.py      # KS par feature + score global + rapport JSON
│       └── alerting.py             # Slack + alerts.jsonl
│
├── tests/
│   ├── unit/                       # 41 tests (api, features, preprocessing, evaluate, monitoring)
│   ├── integration/                # 2 tests (pipeline de bout en bout)
│   └── data/                       # 14 tests de qualité de données (GE)
│
├── docker/
│   ├── Dockerfile.api              # Image API multi-stage, non-root, 2 workers
│   ├── Dockerfile.training         # Image pour jobs d'entraînement
│   └── docker-compose.yml          # Stack locale : MinIO, Postgres, MLflow, Airflow, API, Prometheus, Grafana
│
├── k8s/
│   ├── base/                       # deployment (3 replicas), service, configmap, hpa
│   ├── overlays/staging/           # 2 replicas, ressources réduites
│   ├── overlays/production/        # 5 replicas, ressources augmentées
│   └── kustomization.yaml
│
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml          # Scrapes api:8000 + local
│   │   └── alert_rules.yml         # Latence, erreurs, instance down, dérive des prévisions
│   └── grafana/dashboards/
│       ├── api-performance.json    # Latence/erreurs de l'API
│       └── model-drift.json        # Drift + distribution des prévisions
│
├── mlflow/
│   └── docker-compose.yml          # Serveur MLflow
│
├── great_expectations/
│   └── expectations/dataset_suite.json
│
├── data/
│   ├── external/dataset.csv        # Source d'ingestion
│   ├── raw/demand_data.csv         # Jeu brut (store/sku/units_sold)
│   ├── processed/demand_data.csv   # Nettoyé
│   ├── features/                   # features.parquet + features_config.json + schéma
│   └── monitoring/                 # reference.csv, current.csv, drift_report.json, alerts.jsonl
│
├── models/
│   ├── model.pkl                   # Modèle entraîné local
│   ├── artifacts/                  # feature_importances.png, predictions_vs_actual.png
│   └── evaluation/                 # latest_report.json, production_report.json
│
├── ui/
│   └── index.html                  # Dashboard « Demand Forecasting — Retail Supply Chain »
│
├── dvc.yaml                        # Pipeline DVC : ingest → preprocess → features → train
├── Makefile                        # Cibles : data, ingest, preprocess, validate, features, train, evaluate, promote, api, drift, test…
├── scripts/generate_synthetic_data.py
├── notebooks/exploration.ipynb
├── requirements.txt / requirements-dev.txt
├── pyproject.toml
├── .pre-commit-config.yaml
├── .env.example
└── README.md
```---

## 6. Composant : Gestion et versioning des données (DVC)

### 6.1 Rôle

DVC versionne les fichiers de données volumineux en parallèle du code Git, sans stocker les données dans le dépôt.

### 6.2 Fonctionnement

- Git suit les métadonnées (hash) ; les données réelles vivent dans un **remote** (MinIO, S3-compatible)
- Chaque étape de pipeline produit un hash reproductible
- `dvc repro` rejoue les étapes dont les dépendances ont changé

### 6.3 Pourquoi c'est important

Chaque modèle de production doit être traçable vers le snapshot de données exact qui l'a entraîné : `dvc pull` sur le commit Git correspondant restitue le dataset identique. C'est la base de la reproductibilité et des audits.

### 6.4 Pipeline DVC (`dvc.yaml`)

```yaml
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
    outs: [data/features/features.parquet, data/features/features_config.json]

  train:
    cmd: python src/models/train.py
    deps: [data/features/features.parquet, data/features/features_config.json]
    outs: [models/model.pkl]
    metrics: [metrics.json]
```

### 6.5 Commandes clés

| Commande | Effet |
|---|---|
| `dvc repro` | Rejoue le pipeline si des dépendances ont changé |
| `dvc push` / `dvc pull` | Synchronise les données avec le remote (MinIO) |
| `dvc metrics diff` | Compare les métriques entre deux versions |
| `dvc add data/…` | Commence à suivre un fichier |

### 6.6 Bénéfice concret

Si un modèle en production se comporte mal, on retrouve **exactement** le dataset qui a servi à l'entraîner : checkout du commit Git + `dvc pull`.

---

## 7. Composant : Feature Engineering

### 7.1 Rôle

Transformer les données nettoyées en variables exploitables, de façon **identique** à l'entraînement et à l'inférence (parité, zéro training-serving skew).

### 7.2 Les features

11 features numériques, ordre fixe (`FEATURE_ORDER` dans `build_features.py`) :

```
store_id, sku_id, day_of_week, month, is_holiday,
price, promotion, temperature, inventory_level,
competitor_price, store_traffic
```

La cible est `units_sold` (`TARGET_FEATURE`).

### 7.3 Le `FeatureTransformer`

- `fit(df)` : calcule la moyenne et l'écart-type (ddof=0) de chaque feature numérique
- `transform(df)` : coercition numérique (`pd.to_numeric`, erreurs → 0.0), sélection dans `FEATURE_ORDER`
- `to_config()` / `from_config()` : les statistiques et l'ordre des features sont sérialisés dans `data/features/features_config.json`

```json
{
  "numeric_features": ["store_id", "sku_id", "day_of_week", "month", "is_holiday",
                       "price", "promotion", "temperature", "inventory_level",
                       "competitor_price", "store_traffic"],
  "numeric_stats": { "price": { "mean": 77.43, "std": 41.86 }, "…": "…" },
  "feature_order": ["store_id", "…"]
}
```

C'est ce fichier que `model_loader.py` charge à l'inférence pour appliquer **exactement** les mêmes transformations qu'à l'entraînement.

### 7.4 Feature store offline

`src/features/feature_store.py` écrit `data/features/features_v{N}.parquet` avec un schéma documenté (`features_store_schema.json` : nom, type, description, plage attendue), versionné par DVC. Tout modèle de production est traçable vers son snapshot de features.

---

## 8. Composant : Tracking d'expériences (MLflow)

### 8.1 Rôle

MLflow Tracking enregistre chaque run d'entraînement : hyperparamètres, métriques, artefacts, modèle.

### 8.2 Architecture du serveur MLflow

```
docker-compose (mlflow/docker-compose.yml) :
  - mlflow-server   (UI + API tracking, port 5000)
  - postgres        (backend store : métadonnées des runs)
  - minio           (artifact store : modèles, fichiers)
```

### 8.3 Ce que fait `train.py` (run `demand-forecasting-training`)

1. `mlflow.start_run()` — tags `model_name=demand_model`, `task=demand_forecasting`
2. Log des hyperparamètres : `n_estimators=300`, `max_depth=15`, `min_samples_leaf=5`, `max_features=sqrt`, `random_state=42`, `n_jobs=-1`
3. Log des métriques : `rmse`, `mae`, `r2`, `mape`
4. Log des artefacts :
   - `models/artifacts/feature_importances.png` (top 20 features)
   - `models/artifacts/predictions_vs_actual.png` (scatter réel vs prédit)
   - `data/features/features_config.json`
5. `mlflow.sklearn.log_model(…, registered_model_name="demand_model", input_example=X_test.iloc[[0]])`
6. Persistance locale : `models/model.pkl` (joblib) + `metrics.json`
7. Écriture du snapshot de test : `data/monitoring/reference.csv` (features + `prediction` + `units_sold`) — la référence de drift

> MLflow reste **optionnel au runtime** : si le serveur est injoignable, `train.py` continue en mode offline (avertissement) et persiste modèle et métriques localement. Même comportement côté API (voir §11.4).

### 8.4 Ce que ça apporte

- Comparaison de tous les runs dans l'UI MLflow
- Reproductibilité : chaque run est lié à un commit Git et une version DVC des données
- Base pour la promotion automatique vers le Model Registry

---

## 9. Composant : Model Registry

### 9.1 Rôle

Le Model Registry gère le cycle de vie des modèles : versions numérotées et stages (`None`, `Staging`, `Production`, `Archived`).

### 9.2 Cycle de vie d'un modèle

```
Nouveau run MLflow
        │
        ▼
  Enregistré dans le Registry (demand_model, version N)
        │
        ▼
  Stage = "Staging"
        │
        ▼
  Évaluation (evaluate.py) : portes R² ≥ 0,60 et MAPE ≤ 25 %
  sur le jeu de test (reference.csv prioritaire)
        │
   ┌────┴────┐
   ▼         ▼
 Échec     Succès
   │         │
   ▼         ▼
Rejeté   Comparaison vs production (promote.py)
         │   (candidat ≥ champion sur le même test)
         │
    ┌────┴────┐
    ▼         ▼
  Meilleur   Moins bon
    │         │
    ▼         ▼
  → Production  Refusé (sauf --force)

  Ancienne version → "Archived"
```

### 9.3 Critères de promotion (`promote.py`)

Un candidat n'est promu que si :
- Il a passé les portes d'évaluation (`latest_report.json`, `gates_passed=true`), sinon erreur — `--force` pour outrepasser
- Il bat le modèle actuellement en production sur le même jeu de test

La promotion est enregistrée dans `models/evaluation/production_report.json` (nom, version, run_id, métriques), lue par l'endpoint `/model-info` et les dashboards.

---

## 10. Composant : Orchestration (Apache Airflow)

### 10.1 Rôle

Airflow orchestre les pipelines en DAGs, gère la planification, les dépendances, les retries et les alertes d'échec.

### 10.2 DAGs du projet

| DAG | Déclencheur | Rôle |
|---|---|---|
| `data_ingestion_dag` | Quotidien, 02:00 | Ingestion → validation GE → versioning DVC → push remote MinIO |
| `training_pipeline` | Hebdomadaire (`@weekly`) | validate → preprocess → build_features → train → evaluate → promote → notify |
| `retraining_pipeline` | Quotidien (`@daily`) | `check_drift` (short-circuit) → si drift : preprocess → features → train → evaluate → promote-si-meilleur → notify |

### 10.3 Bonnes pratiques appliquées

- Tâches idempotentes (relançables sans effet de bord)
- `XCom` pour passer le `run_id` MLflow entre tâches (train → evaluate)
- Alertes via `send_alert` (`on_failure_callback`, sévérité `critical`) : Slack si webhook configuré, journal local `data/monitoring/alerts/alerts.jsonl` toujours écrit
- Plugin `DriftDetectedSensor` : sensor qui attend que `data/monitoring/drift_report.json` signale `drift_detected=true` — mécanisme de déclenchement du réentraînement
- Séparation claire entre logique métier (`src/`) et orchestration (`airflow/dags/`)

---

## 11. Composant : Service d'inférence (FastAPI)

### 11.1 Rôle

Exposer le modèle de prévision de la demande via une API REST typée, avec documentation automatique.

### 11.2 Endpoints

| Endpoint | Méthode | Rôle |
|---|---|---|
| `/predict` | POST | Prévision unitaire **ou par lot** (liste) |
| `/health` | GET | Liveness/readiness (Kubernetes, healthcheck Docker) |
| `/metrics` | GET | Métriques Prometheus |
| `/model-info` | GET | Métadonnées du modèle chargé (nom, version, run, métriques de production) |
| `/` | GET | UI dashboard (index.html) |
| `/docs` | GET | Documentation OpenAPI générée par FastAPI |

### 11.3 Requête `/predict` — `DemandPredictionRequest` (Pydantic strict)

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

Contraintes de validation (rejet automatique en **422** avec message clair) :

| Champ | Plage |
|---|---|
| `store_id` | 1 – 100 |
| `sku_id` | 1 – 200 |
| `day_of_week` | 0 – 6 |
| `month` | 1 – 12 |
| `is_holiday`, `promotion` | 0 – 1 |
| `price`, `competitor_price` | 0 – 500 |
| `temperature` | −50 – 150 |
| `inventory_level` | 0 – 10 000 |
| `store_traffic` | 0 – 50 000 |

Un lot vide renvoie **422**. Les champs correspondent exactement aux colonnes d'entraînement (parité entraînement/inférence).

### 11.4 Chargement du modèle (`model_loader.py`)

Ordre de résolution au démarrage et au rechargement :

1. `MLFLOW_MODEL_URI` explicite (si défini et chargeable)
2. **MLflow Model Registry** : `models:/demand_model/Production` (version et run_id lus depuis le registry)
3. **Fallback local** : `models/model.pkl` (version `local`)

Le `FeatureTransformer` est toujours reconstruit depuis `data/features/features_config.json`. `RELOAD_INTERVAL` (env, secondes) permet le rechargement périodique du modèle sans redémarrage ; en cas d'échec de rechargement, l'ancien bundle reste servi. Le modèle est chargé **une fois** au démarrage (pas à chaque requête).

### 11.5 Réponse `/predict`

```json
{
  "predicted_units": 47,
  "demand_bucket": "high",
  "model_name": "demand_model",
  "model_version": "3"
}
```

**Buckets de demande** (`_demand_bucket` dans `schemas.py`) — utilisés par l'UI pour classer la prévision :

| `predicted_units` | Bucket |
|---|---|
| ≤ 15 | `low` |
| ≤ 35 | `medium` |
| ≤ 60 | `high` |
| > 60 | `very_high` |

En mode lot, la réponse est une **liste** de ces objets, dans l'ordre de la requête.

### 11.6 `GET /health`

```json
{ "status": "ok", "model_name": "demand_model", "model_version": "3" }
```

Si le modèle n'est pas chargé : `{ "status": "degraded" }` — le service reste vivant (les probes Kubernetes ne tuent pas le pod), seul le chargement du modèle a échoué.

### 11.7 `GET /model-info`

```json
{
  "model_name": "demand_model",
  "model_version": "3",
  "run_id": "f213a19e92c5486f83b4f65aab4534f5",
  "production_metrics": { "rmse": 22.85, "mae": 19.51, "r2": -0.12, "mape": 105.15 }
}
```

`production_metrics` est lu depuis `models/evaluation/production_report.json` quand le fichier existe ; sinon `null`.

### 11.8 Instrumentation (`metrics.py`)

Métriques Prometheus exposées sur `/metrics` :

| Métrique | Type | Description |
|---|---|---|
| `http_requests_total`, `http_request_duration_seconds` | compteur/histogramme | Trafic et latence par endpoint (via `prometheus_fastapi_instrumentator`) |
| `model_prediction_value` | histogramme | Distribution des `predicted_units` (buckets 0, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150) — alimente le dashboard de drift |
| `predictions_total{model_version}` | gauge | Nombre cumulé de requêtes de prévision par version |
| `mlops_model_version{model_name}` | gauge | Version du modèle actuellement servi |

---

## 12. Composant : Conteneurisation (Docker)

### 12.1 Stratégie multi-stage (`Dockerfile.api`)

```
Stage 1 (builder)  : python:3.11-slim, installe les dépendances (pip install --prefix=/install)
Stage 2 (runtime)  : python:3.11-slim, copie /install, src/, models/, data/features/,
                     great_expectations/ — utilisateur non-root (appuser, uid 1000)
CMD: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 2
HEALTHCHECK : GET /health
```

### 12.2 Bonnes pratiques appliquées

- Image de base `slim`, un seul processus par conteneur
- Utilisateur non-root, `PYTHONDONTWRITEBYTECODE`, healthcheck dans le Dockerfile
- Tag d'image = hash du commit Git, jamais `latest` en production

### 12.3 `docker-compose.yml` (stack locale complète)

`docker compose -f docker/docker-compose.yml up -d --build` :

| Service | Rôle |
|---|---|
| `minio` | Stockage objet (remote DVC, artefacts MLflow) |
| `postgres` | Backend store MLflow + métadonnées Airflow |
| `mlflow` | Serveur tracking + registry (port 5000) |
| `airflow` | Scheduler + webserver (port 8080) |
| `api` | Service d'inférence FastAPI (port 8000), `RELOAD_INTERVAL=60` |
| `prometheus` | Scraping `/metrics` (port 9090) |
| `grafana` | Dashboards provisionnés (port 3000) |---

## 13. Composant : CI/CD (GitHub Actions)

### 13.1 CI (`ci.yml`) — chaque push/PR

1. **Lint** : `ruff check` + `black --check` (src, airflow, scripts)
2. **Sécurité** : `bandit -r src` — échec si finding de sévérité HIGH
3. **Validation des données** : Great Expectations sur le dataset
4. **Tests unitaires** : `pytest tests/unit`
5. **Tests d'intégration** : pipeline complet sur échantillon
6. **Tests de qualité des données** : `pytest tests/data`

### 13.2 CD (`cd.yml`) — merge vers `main`, déclenché sur changement de `src/`, `docker/`, `k8s/`, `requirements*.txt`, `dvc.yaml`

```
build-and-push    → image GHCR taguée au sha du commit (jamais latest)
      │
deploy-staging    → kustomize edit set image + kubectl apply -k overlays/staging
      │              rollout status + smoke tests (GET /health)
      ▼
deploy-production → environnement GitHub "production" : approbation manuelle requise
                     kubectl apply -k overlays/production + rollout + vérification pods/HPA
```

### 13.3 Exemple de structure du workflow CD

```yaml
jobs:
  build-and-push:
    - build Docker image (tag = git sha)
    - push to GHCR

  deploy-staging:
    needs: build-and-push
    environment: staging
    - kubectl apply -k k8s/overlays/staging
    - kubectl rollout status deployment/mlops-api
    - smoke tests (GET /health)

  deploy-production:
    needs: deploy-staging
    environment: production        # approbation manuelle requise
    - kubectl apply -k k8s/overlays/production
    - kubectl rollout status + kubectl get pods/hpa
```

---

## 14. Composant : Déploiement (Kubernetes)

### 14.1 Ressources principales

| Fichier | Rôle |
|---|---|
| `k8s/base/deployment.yaml` | 3 replicas, RollingUpdate (`maxUnavailable: 0`, `maxSurge: 1`), probes `/health` (liveness 30 s/10 s, readiness 10 s/5 s), resources, non-root |
| `k8s/base/service.yaml` | ClusterIP, port 80 → 8000 |
| `k8s/base/configmap.yaml` | `MLFLOW_TRACKING_URI`, `MLFLOW_MODEL_NAME`, `RELOAD_INTERVAL=60`, `LOG_LEVEL` |
| `k8s/base/hpa.yaml` | HPA autoscaling/v2 : min 2, max 10 pods ; CPU 70 %, mémoire 80 % ; stabilisation du scale-down 300 s |
| `k8s/overlays/staging/` | 2 replicas, requests 200m/512Mi, limits 1 CPU/1 Gi |
| `k8s/overlays/production/` | 5 replicas, requests 500m/1 Gi, limits 2 CPU/2 Gi |

### 14.2 Points de conception

- **Zéro downtime** : `maxUnavailable: 0` — un pod n'est retiré qu'une fois le nouveau prêt
- **Probes** : liveness redémarre un pod bloqué ; readiness retire un pod non prêt du service
- **Autoscaling** : HPA dimensionne le service selon CPU/mémoire, avec stabilisation pour éviter le flapping
- **Kustomize** : base commune + overlays par environnement

### 14.3 Déploiement du modèle (changement de version)

Le modèle n'est **pas** embarqué dans l'image : l'API charge la version `Production` du registry MLflow au démarrage (avec fallback local `models/model.pkl`). Changer de modèle = promouvoir une nouvelle version dans le registry puis redéployer l'image (traçabilité immuable), ou recharger via `RELOAD_INTERVAL` pour les changements non structurants.

---

## 15. Composant : Monitoring infrastructure (Prometheus/Grafana)

### 15.1 Flux de collecte

```
FastAPI (/metrics) ──scrape (15 s)──▶ Prometheus ──requête──▶ Grafana (dashboards)
                                          │
                                          ▼
                                   alert_rules.yml (alertes)
```

### 15.2 Règles d'alerte (`monitoring/prometheus/alert_rules.yml`)

| Alerte | Condition | Sévérité |
|---|---|---|
| `HighAPILatency` | p95 de latence HTTP > 500 ms pendant 5 min (par chemin/méthode) | warning |
| `HighAPIErrorRate` | > 5 % de réponses 5xx par chemin pendant 5 min | critical |
| `APIInstanceDown` | cible de scrape injoignable pendant 2 min | critical |
| `ModelPredictionShift` | La distribution des prévisions en production dérive de celle de l'entraînement (quantiles p50/p95 comparés sur 1 h vs 6 h) | warning |

### 15.3 Dashboards Grafana provisionnés

- **API Performance** (`api-performance.json`) : latence, erreurs, requêtes par seconde
- **Model Drift** (`model-drift.json`) : score de drift, features dérivées, distribution des prévisions (`model_prediction_value`)

---

## 16. Composant : Monitoring du modèle et Data Drift

### 16.1 Rôle

Détecter quand les données reçues en production divergent significativement des données d'entraînement (data drift), et déclencher le réentraînement.

### 16.2 Fonctionnement (`drift_detection.py`)

1. **Référence** : `data/monitoring/reference.csv` — le snapshot de test écrit par `train.py` (features + `prediction` + `units_sold`)
2. **Courant** : `data/monitoring/current.csv` — échantillon de données de production (chemins configurables via env `DRIFT_REFERENCE` / `DRIFT_CURRENT`)
3. Par feature numérique, **test de Kolmogorov-Smirnov à deux échantillons** (`scipy.stats.ks_2samp`) : drift détecté si `p_value < 0.05` **et** `statistic > 0.1`
4. **Score de drift global** = fraction de features dérivées (`drifted / total`)
5. `drift_detected = score > threshold` — seuil par défaut **0,3** (env `DRIFT_THRESHOLD`)
6. Rapport écrit dans `data/monitoring/drift_report.json` :

```json
{
  "engine": "scipy-fallback",
  "drift_score": 0.09,
  "threshold": 0.3,
  "drift_detected": false,
  "drifted_features": [],
  "per_column": { "price": { "drift_detected": false, "test": "ks_2samp", "score": 0.05 } }
}
```

### 16.3 Alerting (`alerting.py`)

- Canal préféré : **Slack** (env `SLACK_WEBHOOK_URL`) — sévérités `debug`, `info`, `warning`, `critical`
- **Toujours** : journal local `data/monitoring/alerts/alerts.jsonl`
- Aucun secret loggé (seul le préfixe de l'URL du webhook est affichable)

### 16.4 Déclenchement du réentraînement

- Le DAG `retraining_pipeline` (quotidien) exécute `detect_drift()` en première tâche
- Pas de drift → `ShortCircuitOperator` arrête le DAG (rien à faire)
- Drift détecté → alerte (`warning`) puis enchaîne preprocess → features → train → evaluate → promote-si-meilleur → notify

---

## 17. Composant : Tests et qualité (pytest, Great Expectations)

### 17.1 Pyramide de tests — 57 tests

```
        ┌────────────────────────┐
        │  Tests end-to-end (2)  │  tests/integration/test_pipeline_end_to_end.py
        ├────────────────────────┤
        │  Tests de données (14) │  tests/data/test_data_quality.py (Great Expectations)
        ├────────────────────────┤
        │  Tests unitaires (41)  │  tests/unit/ (api 15, features 7, preprocessing 5,
        │                        │   evaluate 6, monitoring 8)
        └────────────────────────┘
```

### 17.2 Tests unitaires (`tests/unit/`)

- `test_api.py` (15) : `/health`, `/predict` unitaire et par lot, lot vide → 422, champs manquants → 422, `/metrics` Prometheus, `/model-info`, validation Pydantic (store_id, price, temperature hors plage → 422), buckets `low`/`medium`/`high`/`very_high`
- `test_features.py` (7) : forme du transform, features numériques présentes, round-trip de config, **parité entraînement/inférence**, ordre des features préservé, sortie du build, cible numérique
- `test_preprocessing.py` (5) : nettoyage, schéma attendu, filtres
- `test_evaluate.py` (6) : métriques calculées, rapport avec portes, seuils par défaut, écriture du rapport, priorité `reference.csv` pour le jeu de test
- `test_monitoring.py` (8) : KS détecte un drift décalé, pas de drift sur données identiques, `detect_drift` end-to-end, fichiers manquants → erreur, variables d'environnement, features cohérentes

### 17.3 Tests de qualité des données (Great Expectations)

Suites d'attentes déclaratives (`great_expectations/expectations/dataset_suite.json`) :
- Nombre de lignes dans une plage minimale
- Colonnes sans valeurs nulles
- Valeurs numériques dans des plages définies
- Types de colonnes conformes au schéma

Ces tests s'exécutent **avant** l'entraînement, pour éviter d'entraîner un modèle sur des données corrompues. `validation.py` a un fallback intégré pour les mêmes types d'attente si la bibliothèque Great Expectations n'est pas installée — la validation tourne toujours en CI.

### 17.4 Tests d'intégration

Vérifient que le pipeline complet (préprocessing → features → entraînement → évaluation → monitoring) fonctionne de bout en bout sur un petit échantillon, en environnement CI.

---

## 18. Boucle de réentraînement automatique

### 18.1 Vue d'ensemble

C'est la caractéristique qui distingue un projet MLOps « complet » d'un simple pipeline de déploiement : le système réagit seul à la dérive des données de production.

### 18.2 Déclencheurs

| Déclencheur | Description |
|---|---|
| **Planifié** | `training_pipeline` hebdomadaire (`@weekly`) : entraînement complet systématique |
| **Basé sur le drift** | `retraining_pipeline` quotidien (`@daily`) : `detect_drift()` en short-circuit — si le score de drift dépasse le seuil (0,3 par défaut), le réentraînement s'exécute |
| **Manuel** | Déclenchement depuis l'UI Airflow par un data scientist |

### 18.3 Séquence complète (déclenché par drift)

```
1. Détection : detect_drift() (KS par feature, score global)
        ↓
2. Score > seuil → alerte (warning, Slack + journal)
        ↓
3. preprocess → build_features (nouvelles données)
        ↓
4. train (RandomForestRegressor, même code que train.py, nouvelles données)
        ↓
5. Évaluation : portes R² ≥ 0,60 et MAPE ≤ 25 % — si non passées : arrêt
        ↓
6. Si portes passées : comparaison vs modèle en production sur le même test
        ↓
7. Si meilleur → promotion Staging → Production (archivage de l'ancienne version)
        ↓
8. Notification de l'équipe (send_alert)
```

### 18.4 Garde-fous importants

- Un modèle réentraîné n'est **jamais** promu automatiquement sans passer les mêmes portes que lors du déploiement initial
- Le DAG quotidien ne consomme aucune ressource quand il n'y a pas de drift (short-circuit)
- Conservation des versions précédentes dans le registry (`Archived`) pour un retour arrière rapide
- Notification à chaque promotion automatique (traçabilité humaine même dans un système automatisé)

---

## 19. Sécurité et gestion des secrets

### 19.1 Principes appliqués

- Aucun secret (mots de passe, clés API, credentials MinIO/S3, webhook Slack) n'est commité dans le dépôt
- `.env.example` documente les variables nécessaires sans valeurs réelles
- En Kubernetes : `configMapRef` pour la configuration non sensible, `secretRef` optionnel (`mlops-secrets`) — le secret n'est jamais requis au démarrage
- Scan automatique du code (`bandit`) dans la CI, échec sur finding HIGH
- Image conteneur exécutée en non-root (uid 1000), `runAsNonRoot: true`, `allowPrivilegeEscalation: false`
- Aucun secret loggé : `alerting.py` n'affiche que le préfixe de l'URL du webhook

### 19.2 Exemple de flux de secret en production

```
Secret créé dans GitHub Secrets / Kubernetes (optionnel)
        ↓
Monté comme variable d'environnement ou volume dans le pod
        ↓
Jamais loggé, jamais exposé dans /metrics ou /health
```

---

## 20. Métriques de succès

| Métrique | Définition | Cible |
|---|---|---|
| **RMSE** | Erreur quadratique moyenne, en unités vendues | Minimiser (actuel : ~22,8 sur le dernier run) |
| **MAE** | Erreur absolue moyenne, en unités vendues | Minimiser (actuel : ~19,5) |
| **R²** | Pouvoir explicatif vs moyenne naïve | **≥ 0,60** (porte) |
| **MAPE** | Erreur relative moyenne, en % | **≤ 25 %** (porte) |
| Drift de données | Fraction de features ayant dérivé (KS) | < 0,3 (pas de réentraînement déclenché) |
| Latence API p95 | Temps de réponse de `/predict` | < 500 ms (alerte au-delà) |
| Taux d'erreur API | Part de réponses 5xx | < 5 % |

Les portes R² ≥ 0,60 et MAPE ≤ 25 % sont les chiffres qui décident de la mise en production d'un modèle. Chaque autre métrique est diagnostique.

---

## 21. Plan de mise en œuvre étape par étape

| Phase | Livrable | Statut |
|---|---|---|
| 0 | Ingestion + prétraitement + validation GE (`preprocessing.py`, `validation.py`) | ✅ Fait |
| 1 | Feature engineering avec parité entraînement/inférence (`build_features.py`) | ✅ Fait |
| 2 | Feature store Parquet versionné DVC (`feature_store.py`) | ✅ Fait |
| 3 | Entraînement RandomForest + tracking MLflow + registry (`train.py`) | ✅ Fait |
| 4 | Évaluation avec portes + rapport (`evaluate.py`) | ✅ Fait |
| 5 | Promotion conditionnelle Staging → Production (`promote.py`) | ✅ Fait |
| 6 | API d'inférence /predict + /health + /model-info + /metrics (`api/`) | ✅ Fait |
| 7 | Monitoring drift KS + alerting Slack/journal (`monitoring/`) | ✅ Fait |
| 8 | Airflow : ingestion, training hebdomadaire, retraining par drift | ✅ Fait |
| 9 | Docker Compose + Dockerfile multi-stage + Kubernetes + Kustomize | ✅ Fait |
| 10 | CI (lint, bandit, GE, tests) + CD (staging → production approuvée) | ✅ Fait |
| 11 | Dashboard UI de prévision (`ui/index.html`) | ✅ Fait |
| 12 | **Modèle répondant aux portes de qualité** (R² ≥ 0,60 ; MAPE ≤ 25 %) | ⏳ **En cours — voir risques** |
| 13 | Déploiement shadow puis canary avec garde-fous (roadmap) | 🔜 Planifié |
| 14 | Features temporelles (lags, moyennes mobiles) et store en ligne | 🔜 Planifié |

---

## 22. Critères de succès / Definition of Done

- [ ] `dvc repro` reproduit le pipeline complet à l'identique
- [ ] Le modèle candidat passe les portes d'évaluation (R² ≥ 0,60 ; MAPE ≤ 25 %) sur le jeu de test
- [ ] `evaluate.py` sort en code non nul quand les portes ne sont pas passées (bloqué en CI)
- [ ] La promotion exige portes passées + candidat ≥ production ; le refus est explicite
- [ ] `/predict` accepte unitaire et lot, rejette les payloads invalides en 422
- [ ] Parité entraînement/inférence garantie par `features_config.json` (testé)
- [ ] Le drift est détecté par test KS par feature ; le rapport JSON est écrit
- [ ] `retraining_pipeline` se déclenche sur drift et ne consomme rien sinon (short-circuit)
- [ ] 57 tests verts en CI (41 unitaires, 14 données, 2 intégration)
- [ ] Déploiement Kubernetes zéro downtime (RollingUpdate, probes, HPA)
- [ ] CD production derrière approbation manuelle (GitHub Environments)
- [ ] Aucun secret committé ; image non-root ; bandit sans finding HIGH

---

## 23. Risques honnêtes

**Le modèle actuel ne passe pas ses propres portes de qualité.** Le dernier rapport d'évaluation (`models/evaluation/latest_report.json`) donne R² ≈ −0,68, MAPE ≈ 49,4 % (n=100) — bien en dessous des portes R² ≥ 0,60 et MAPE ≤ 25 %. Le dernier run d'entraînement (`metrics.json`) donne R² ≈ −0,12, RMSE ≈ 22,8, MAPE ≈ 105 %. Le pipeline fonctionne, mais le **pouvoir prédictif du modèle est encore faible**. C'est le risque n°1 : sans un modèle qui passe les portes, la boucle entière démontre le mécanisme sans livrer de valeur prédictive.

**Les données sont synthétiques et petites.** `data/raw/demand_data.csv` est un jeu de démonstration généré (`scripts/generate_synthetic_data.py`). L'équilibre des features, la saisonnalité et le bruit n'y sont pas représentatifs d'une chaîne réelle. Aucune performance de production ne peut être revendiquée depuis ce jeu.

**Le feature engineering est volontairement minimal.** La colonne `date` est conservée mais non utilisée ; il n'y a ni lags, ni moyennes mobiles, ni features croisées. L'essentiel du signal temporel de la demande (saisonnalité lisse, tendances, effets différés de promotion) n'est pas encore capturé — c'est la piste la plus prometteuse pour passer les portes (voir §24).

**La comparaison de promotion dans `promote.py` est partiellement héritée.** Le mécanisme (portes + candidat ≥ champion) est en place, mais certains chemins de code conservent des références historiques ; toute promotion en production doit être vérifiée manuellement avant d'être considérée fiable.

**Le réentraînement automatique peut promouvoir un mauvais modèle.** Les portes protègent, mais un drift lent et une métrique de champion faible peuvent verrouiller la boucle sur des modèles médiocres. La surveillance humaine des dashboards reste indispensable.

---

## 24. Extensions possibles (roadmap)

| Extension | Valeur ajoutée |
|---|---|
| **Features temporelles** (lags, moyennes mobiles 7/30 j, indicateurs de tendance) | Capter la saisonnalité réelle de la demande — la piste n°1 pour passer les portes |
| **GBM / XGBoost** en alternative au RandomForest | Souvent meilleur sur les données tabulaires hétérogènes |
| **Recherche d'hyperparamètres** (Optuna, MLflow param search) | Améliorer R²/MAPE du champion |
| **Store de features en ligne** | Si le cas d'usage passe au temps réel (points de vente, e-commerce) |
| **Déploiement shadow puis canary** avec garde-fous par segment | Valider un modèle sur du trafic réel avant promotion complète |
| **Evidently** pour un drift plus riche (tests multi-familles, HTML reports) | Au-delà du test KS actuel |
| **Explainability (SHAP)** | Justifier chaque prévision ; identifier les features dominantes |
| **Tests de biais/équité** | Vérifier que les prévisions ne désavantagent pas certains magasins/SKUs |
| **Argo CD / GitOps** | Déploiement Kubernetes déclaratif au lieu de `kubectl apply` en CI |
| **Serving avancé (KServe/Seldon)** | A/B testing, canary, explainability intégrée |

---

## 25. Annexe : Glossaire rapide

| Terme | Définition |
|---|---|
| **Demand forecasting** | Prévision des ventes futures (ici `units_sold`) par magasin/SKU |
| **Data drift** | Changement dans la distribution des données d'entrée en production par rapport à l'entraînement |
| **Concept drift** | Changement dans la relation entre les features et la cible à prédire |
| **RMSE** | Racine de l'erreur quadratique moyenne — pénalise les grosses erreurs |
| **MAPE** | Erreur absolue moyenne en pourcentage (hors `y = 0`) |
| **R²** | Fraction de variance expliquée vs la moyenne naïve |
| **Portes de qualité (gates)** | Seuils minimaux (R² ≥ 0,60 ; MAPE ≤ 25 %) qu'un candidat doit franchir pour être promu |
| **Parité entraînement/inférence** | Les mêmes transformations de features appliquées aux deux moments, via config sérialisée |
| **Feature store** | Couche de stockage des features (Parquet versionné par DVC, schéma documenté) |
| **Training-serving skew** | Divergence entre les données vues à l'entraînement et celles servies en production |
| **Short-circuit** | Tâche Airflow qui arrête le DAG si une condition n'est pas remplie (ici : pas de drift) |
| **Test de Kolmogorov-Smirnov** | Test statistique comparant deux distributions (référence vs production) |
| **Bucket de demande** | Classification de la prévision en `low` / `medium` / `high` / `very_high` |
| **RollingUpdate** | Mise à jour progressive des pods sans interruption de service |
| **HPA** | Horizontal Pod Autoscaler : dimensionne automatiquement le nombre de pods |
| **Idempotence** | Propriété d'une opération pouvant être répétée sans changer le résultat au-delà de la première exécution |