# Pipeline ML — entraînement vintage-aware et seuil par coût attendu

Le pipeline ML exécute la chaîne **validate → preprocess → build_features (point-in-time) → build_training_set (vintage-aware) → train → threshold → evaluate (backtest) → promote (shadow)**. Il est déclaré dans `dvc.yaml` (stages `ingest`, `preprocess`, `build_features`, `build_training_set`, `train`) et orchestré de deux façons équivalentes : les cibles du `Makefile` en local, et les DAGs Airflow `training_pipeline` / `retraining_pipeline` en production.

Deux propriétés distinguent ce pipeline d'un pipeline MLOps générique, et elles sont structurellement nécessaires à la fraude :

1. **Correction point-in-time** : chaque ligne d'entraînement est construite avec les features telles qu'au moment de la transaction, jamais « aujourd'hui ». Une fuite temporelle fait échouer le build.
2. **Vintages et maturité des labels** : les transactions non matures ne sont jamais labellisées négatives. Le pipeline déclare explicitement quels vintages sont matures et lesquels sont censurés, et combine des labels faibles (signalements clients, revues) pour garder de la fraîcheur.

---

## 1. Vue d'ensemble

```
data/external/transactions.parquet  (jeu de démonstration — fraude card-not-present)
        │  Makefile: data  (scripts/generate_synthetic_data.py)
        ▼
 ingest (DVC stage)          src/data/ingestion.py
        ▼
 data/raw/transactions.parquet  ───────▶  versionné + poussé vers MinIO (dvc add/push)
        ▼
 preprocess (DVC stage)      src/data/preprocessing.py
        ▼
 data/processed/transactions.parquet
        ▼
 validate                    src/data/validation.py  (suite Great Expectations)
        ▼
 build_features (DVC stage)  src/features/build_features.py  (+ velocity_aggregator,
        ▼                     point_in_time, feature_store)
 data/features/features.parquet + features_config.json
        ▼
 build_training_set (DVC stage)  src/features/point_in_time.py
        ▼  (split vintage-aware : vintages matures vs censurés, labels faibles)
 data/training/train_vintage_aware.parquet
        ▼
 train (DVC stage)           src/models/train.py  →  MLflow Tracking + Registry (Staging)
        ▼  (GBM, coût attendu comme métrique primaire)
 models/model.pkl · metrics.json · data/monitoring/reference.csv
        ▼
 threshold                   src/models/threshold.py  →  t_low / t_high depuis la
        ▼                     matrice de coûts + capacité de revue
 backtest                    src/models/evaluate.py  →  models/evaluation/latest_report.json
        ▼   (gates : coût attendu, faux refus, capture de fraude — vintages matures)
 promote                     src/models/promote.py   →  Staging → Shadow → canary → Production
        ▼
 models/evaluation/production_report.json   (lu par l'API /model-info)
```

---

## 2. Les étapes en détail

### 2.1 Ingestion — `src/data/ingestion.py`

- Source résolue : argument `--source` > variable `INGESTION_SOURCE` > défaut `data/external/transactions.parquet`.
- Accepte un chemin local ou une URL (`http://`, `https://`, `s3://`).
- `normalize()` : nettoie les noms de colonnes, les chaînes, applique les types attendus et convertit les montants.
- Sortie : `data/raw/transactions.parquet`. Opération **idempotente**.
- DVC : stage `ingest` (`dvc.yaml`) / cible `make ingest`. Dans Airflow, la tâche `version_data` ajoute le fichier à DVC et pousse vers le remote.

### 2.2 Préprocessing — `src/data/preprocessing.py`

- Supprime les identifiants non prédictifs (`DROP_COLUMNS` — y compris tout champ permettant de reconstruire le PAN ; la carte n'apparaît que sous forme hachée).
- Force les types numériques (montants, fenêtres), supprime les lignes invalides (`dropna`) et filtre les valeurs hors domaine.
- Sortie : `data/processed/transactions.parquet`. Idempotent. DVC stage `preprocess` / `make preprocess`.

### 2.3 Validation — `src/data/validation.py`

- Charge la suite déclarative `great_expectations/expectations/dataset_suite.json`.
- Exécute la validation via l'API Great Expectations (`from_pandas`), avec un **évaluateur léger intégré** en fallback pour que la validation tourne toujours (notamment en CI).
- Expectations spécifiques au contexte fraude : `label_maturity_date` présente et cohérente avec la date de transaction, `card_hash` non nul, montants dans le domaine, BIN à 6 chiffres.
- Sortie : résumé `{total, passed, failed, results}`. **Quitte en erreur** (code 1) si au moins une expectation échoue (`ValidationError`).
- CLI : `python src/data/validation.py [--input data/processed/transactions.parquet] [--suite ...] [--json-output ...]`.

### 2.4 Feature engineering — `src/features/build_features.py`

- Construit les features de vélocité (fenêtres 1 h / 24 h / 7 j par carte, appareil, marchand, IP) :

```
card_txn_count_1h, card_txn_count_24h, card_txn_count_7d
card_amount_sum_24h / card_amount_avg_30d          # ratio à sa propre ligne de base
card_distinct_merchants_24h
card_distinct_countries_24h
device_distinct_cards_24h                          # signal de fraude très fort
ip_distinct_cards_1h
merchant_decline_rate_1h
time_since_last_txn_seconds
amount_zscore_vs_card_history
is_first_txn_at_merchant
billing_shipping_distance_km
hour_of_day_zscore_vs_card_history
```

- En production, les compteurs de vélocité sont maintenus en continu par l'agrégateur streaming (`src/features/velocity_aggregator.py`) et lus depuis le store en ligne Redis ; à l'entraînement, ils sont recalculés avec la correction point-in-time.
- **Le même objet est réutilisé à l'inférence** (`ModelBundle.predict_proba` dans `src/api/model_loader.py`), ce qui garantit l'absence de *training/serving skew*.
- L'état ajusté est sérialisé dans `data/features/features_config.json` et loggé comme artefact MLflow (`mlflow.log_artifact`).
- Sorties (DVC stage `build_features`) : `data/features/features.parquet` + `features_config.json`. Cible : `make features`.
- Feature store : `src/features/feature_store.py` écrit des versions numérotées `features_v{N}.parquet` (offline, versionnées par DVC) et alimente le store en ligne Redis (online). CLI : `python src/features/feature_store.py --list-versions`.

### 2.5 Correction point-in-time — `src/features/point_in_time.py`

- Pour chaque transaction au temps T, les features de vélocité reflètent l'état **à T** — jamais l'état à aujourd'hui.
- Calcule `label_maturity_date` et partitionne les transactions en **vintages matures** (labels autoritaires arrivés) et **vintages censurés** (labels encore possibles — ex : < 120 jours).
- **Règle d'or** : « pas encore de chargeback » ≠ « légitime ». Les vintages censurés ne sont jamais utilisés comme négatifs purs ; ils peuvent contribuer via le canal de labels faibles pondérés.
- **Test de fuite intégré** : `tests/unit/test_point_in_time.py` construit délibérément une ligne d'entraînement en injectant des features calculées « aujourd'hui » pour une transaction passée — le pipeline doit la rejeter, sinon le build échoue.
- Sortie (DVC stage `build_training_set`) : `data/training/train_vintage_aware.parquet`. Cible : `make training-set`.

### 2.6 Entraînement — `src/models/train.py`

- Modèle : **ensemble d'arbres à gradient boosté (GBM)** — score en quelques millisecondes, contraint par le budget d'inférence de 20 ms. Hyperparamètres par défaut surchargeables en CLI.
- Split **vintage-aware** : train/test découpés sur les vintages matures déclarés (pas de fuite de labels entre les deux).
- Labels : matures (chargebacks, décisions de revue) + **labels faibles pondérés** (signalements clients, résultats de revue récents) pour la fraîcheur.
- Métriques primaires : **coût attendu** (depuis la matrice de coûts), taux de capture de fraude, taux de faux refus. AUC/F1 en diagnostique seulement.
- **MLflow** (si un serveur est joignable) :
  - run `fraud-training`, tags `model_name`, `git_commit`, `data_version` (`DVC_DATA_VERSION`), `vintages_mature`, `vintages_censored`, `registry_version` ;
  - log des params et des métriques ;
  - artefacts : matrice de confusion PNG, importances de features PNG, config du transformer, rapport de vintages ;
  - `mlflow.sklearn.log_model(..., registered_model_name="fraud_model", input_example=...)` ;
  - transition de la version enregistrée vers le stage **Staging**.
- Sorties locales : `models/model.pkl` (DVC output), `metrics.json` (métrique DVC), et `data/monitoring/reference.csv` (jeu de test mature + scores + labels, base de référence du drift).
- En mode hors-ligne (pas de serveur MLflow), l'entraînement continue et ne fait que l'enregistrement local.

### 2.7 Seuils de décision — `src/models/threshold.py`

- Dérive `t_low` et `t_high` de la **matrice de coûts** (pertes de fraude vs faux refus, voir §1.2 de la spécification) et de la **capacité de revue** :

```
score < t_low          → APPROUVER
t_low ≤ score < t_high → RÉVISER   (file analyste, ou step-up 3-D Secure)
score ≥ t_high         → REFUSER
```

- Si les analystes peuvent traiter 400 revues/heure, `t_low` est réglé pour que la bande RÉVISER produise à peu près ce volume. Le modèle produit un classement ; la contrainte métier détermine où tombent les coupes.
- Les seuils sont loggés dans MLflow avec le run et **traités comme information sensible** (un attaquant qui connaît la frontière peut l'exploiter).

### 2.8 Backtest — `src/models/evaluate.py`

- Résout le modèle candidat : `--run-id` (`runs:/<run_id>/model`) > `--model-uri` > `models/model.pkl` local.
- Charge le jeu de test : `data/monitoring/reference.csv` (vintages matures retenus par `train.py`).
- Recalcule les métriques et compare aux **quality gates** :

| Gate | Variable d'env | Défaut |
|---|---|---|
| Coût attendu par 1 000 transactions ≤ | `MAX_EXPECTED_COST_PER_1K` | `5.0` |
| Taux de faux refus < | `MAX_FALSE_DECLINE_RATE` | `0.008` |
| Taux de capture de fraude ≥ | `MIN_FRAUD_CAPTURE_RATE` | `0.75` |
| Précision de revue ≥ | `MIN_REVIEW_PRECISION` | `0.30` |

- Écrit `models/evaluation/latest_report.json` avec `gates_passed`. **Quitte en erreur (code 1)** si `gates_passed` est faux — le pipeline s'arrête avant la promotion.
- Un backtest séparé vérifie que le candidat bat le champion sur le coût attendu, **pas** sur l'AUC.

### 2.9 Promotion — `src/models/promote.py`

- Lit `latest_report.json` ; refuse de promouvoir si `gates_passed` est faux (sauf `--force`).
- Récupère la version `Staging` du registry et la compare au modèle `Production` courant (lecture de `production_report.json`) : le candidat doit avoir un **coût attendu ≤ coût de production** (sauf `--force`).
- **Jamais directement en production** : la promotion mène au stage **Shadow** (7 jours sur 100 % du trafic, 0 % actionné). Le passage shadow → canary 5 % → 25 % → 100 % est contrôlé par les garde-fous (§6 de `docs/deployment.md`) et la signature manuelle du responsable fraude.
- Transition : l'ancienne version `Production` passe en **Archived**, le candidat passe en **Production** après le rollout staged.
- Écrit `models/evaluation/production_report.json` — consommé par `/model-info` de l'API et par le dashboard Grafana (version servie).

### 2.10 Échantillon d'exploration — `src/models/exploration.py`

- Approuve un échantillon **aléatoire** de la population que le modèle aurait refusée (ex : 0,5 %, plafonné en valeur), pour acheter des labels non biaisés dans la région des refus.
- C'est la correction du **biais de boucle de feedback** : le modèle ne voit que les résultats des transactions qu'il a approuvées ; sans exploration, il devient progressivement plus confiant sur une région qu'il a cessé d'observer.
- Budgété comme **coût d'amélioration du modèle**, pas comme perte de fraude — avec accord écrit de la direction et plafond de valeur dur.

---

## 3. Exécution

### 3.1 En local (Makefile / DVC)

```bash
make data                 # génère le dataset synthétique de fraude
make ingest               # stage 1
make preprocess           # stage 2
make validate             # qualité des données
make features             # stage 3
make training-set         # stage 4 (vintage-aware + test de fuite)
MLFLOW_TRACKING_URI=http://localhost:5000 make train     # stage 5
MLFLOW_TRACKING_URI=http://localhost:5000 make threshold
MLFLOW_TRACKING_URI=http://localhost:5000 make evaluate
MLFLOW_TRACKING_URI=http://localhost:5000 make promote
```

Ou équivalent DVC :

```bash
make dvc-repro            # dvc repro (stages obsolètes uniquement)
```

> `make setup` crée le venv et installe `requirements-dev.txt` ; `make install` installe `requirements.txt`.

### 3.2 Via Airflow

| DAG | Planification | Tâches |
|---|---|---|
| `data_ingestion_dag` | `0 2 * * *` (quotidien 02:00) | `ingest_data → validate_data → version_data` |
| `label_reconciliation_dag` | `0 3 * * *` (quotidien 03:00) | `join_chargebacks → join_claims → join_reviews → update_maturity` |
| `training_pipeline` | `@weekly` (calendrier randomisé) | `validate_data → preprocess → build_features → build_training_set → train_model → optimize_threshold → evaluate_model → deploy_shadow → notify_team` |
| `retraining_pipeline` | déclenché par drift / signature adversarial (+ planifié randomisé) | `check_drift` (ShortCircuit) → si drift : `reconcile_labels → preprocess → build_features → build_training_set → train_model → optimize_threshold → evaluate_model → deploy_shadow → notify_team` |

Points d'attention :
- Dans `training_pipeline`, le `run_id` est transmis de `train_model` à `evaluate_model` via **XCom**.
- `evaluate_model` lève une erreur si les gates échouent → arrêt avant promotion.
- Chaque tâche en échec déclenche `send_alert(..., severity="critical")` (`on_failure_callback`).
- La boucle de réentraînement est pilotée par le DAG `retraining_pipeline` et le plugin `DriftDetectedSensor` (`airflow/plugins/drift_sensor.py`) qui sonde `data/monitoring/drift_report.json`.
- Le calendrier de réentraînement est **randomisé** (fenêtre aléatoire autour d'une cadence hebdomadaire nominale) : un rythme prévisible est exploitable par un attaquant.

---

## 4. Traçabilité

Un modèle en production est relié à :

| Référence | Source |
|---|---|
| `run_id` MLflow | `train.py`, repris dans `production_report.json` |
| `model_version` (Registry) | `promote.py` |
| Commit Git | tag `git_commit` du run MLflow (`GIT_COMMIT`) |
| Version des données | tag `data_version` du run (`DVC_DATA_VERSION`), snapshot DVC épingle par commit Git |
| **Vintages utilisés** | tags `vintages_mature` / `vintages_censored` du run — reproduit la maturité des labels au moment de l'entraînement |
| Config des features | artefact `features_config.json` loggé dans le run |
| Seuils de décision | `t_low` / `t_high` loggés avec le run |
| Jeu d'évaluation | `data/monitoring/reference.csv` (vintages matures, identique pour comparer candidat vs production) |
| Décisions en production | ledger de décisions (version de modèle, snapshot de features, score, seuils, règles, issue) — chaque décision est reconstruisible |