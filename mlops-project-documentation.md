# Plateforme de Décision de Fraude au Paiement en Temps Réel — Documentation Technique Complète

> Produit cible : **Sentry** — décision de fraude card-not-present en moins de 100 ms (p99), avec une boucle de réentraînement fermée construite autour de labels retardés et biaisés.
>
> Cette spécification est la version « entreprise » du projet : le cas d'usage n'est plus un démonstrateur agnostique, c'est un système de décision de fraude en temps réel où la boucle de réentraînement — déjà présente dans la conception d'origine — cesse d'être une démonstration pédagogique et devient structurellement indispensable.
>
> La stack d'origine survit presque intacte : **DVC, MinIO, Airflow, MLflow, Docker, GitHub Actions, Kubernetes, FastAPI, Prometheus, Grafana, Evidently, pytest, Great Expectations**. Ce qui change, c'est la charge de travail : de la classification par lot, agnostique au cas d'usage, vers un problème contraint par la latence, adversarial, à labels retardés, où les trois coûts (pertes fraudes, frais de chargeback, faux refus) sont asymétriques et connaissables.

---

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble-du-projet)
2. [Les trois contraintes qui redessinent le design](#2-les-trois-contraintes-qui-redessinent-le-design)
3. [Architecture globale](#3-architecture-globale)
4. [Stack technique détaillée](#4-stack-technique-détaillée)
5. [Structure du dépôt](#5-structure-du-dépôt)
6. [Composant : Gestion et versioning des données (DVC)](#6-composant--gestion-et-versioning-des-données-dvc)
7. [Composant : Feature Engineering](#7-composant--feature-engineering)
8. [Composant : Tracking d'expériences (MLflow)](#8-composant--tracking-dexpériences-mlflow)
9. [Composant : Model Registry](#9-composant--model-registry)
10. [Composant : Orchestration (Apache Airflow)](#10-composant--orchestration-apache-airflow)
11. [Composant : Service de décision (FastAPI)](#11-composant--service-de-décision-fastapi)
12. [Composant : Conteneurisation (Docker)](#12-composant--conteneurisation-docker)
13. [Composant : CI/CD (GitHub Actions)](#13-composant--cicd-github-actions)
14. [Composant : Déploiement (Kubernetes)](#14-composant--déploiement-kubernetes)
15. [Déploiement du modèle : shadow, puis canary, toujours](#15-déploiement-du-modèle--shadow-puis-canary-toujours)
16. [Composant : Monitoring infrastructure (Prometheus/Grafana)](#16-composant--monitoring-infrastructure-prometheusgrafana)
17. [Composant : Monitoring du modèle et Data Drift (Evidently)](#17-composant--monitoring-du-modèle-et-data-drift-evidently)
18. [Composant : Tests et qualité (pytest, Great Expectations)](#18-composant--tests-et-qualité-pytest-great-expectations)
19. [Boucle de réentraînement automatique](#19-boucle-de-réentraînement-automatique)
20. [Sécurité et gestion des secrets](#20-sécurité-et-gestion-des-secrets)
21. [Métriques de succès](#21-métriques-de-succès)
22. [Plan de mise en œuvre étape par étape](#22-plan-de-mise-en-œuvre-étape-par-étape)
23. [Critères de succès / Definition of Done](#23-critères-de-succès--definition-of-done)
24. [Risques honnêtes](#24-risques-honnêtes)
25. [Extensions possibles](#25-extensions-possibles)

---

## 1. Vue d'ensemble du projet

### 1.1 Objectif

Construire une plateforme MLOps complète, reproductible et automatisée pour la **décision de fraude au paiement card-not-present (CNP) en temps réel** : chaque transaction est décidée (APPROUVER / RÉVISER / REFUSER) à l'intérieur du flux d'autorisation de paiement, avec un budget de latence dur de **100 ms à p99**, et une boucle de réentraînement fermée qui compense explicitement le retard et le biais des labels de fraude.

Le système repose sur les composants MLOps éprouvés suivants, du stockage versionné des données jusqu'à la détection de drift adversarial en production et le réentraînement automatique — sans intervention manuelle une fois déployé :

- Ingestion et versioning des données (DVC + MinIO)
- Validation des données (Great Expectations)
- Feature engineering, dont features de vélocité temps réel (Redis + Kafka)
- Entraînement avec tracking (MLflow) et registry de modèles
- Service de décision en ligne (FastAPI) avec règles déterministes en surcouche
- Déploiement en shadow puis canary avec rollback automatique (Kubernetes + GitHub Actions)
- Monitoring technique (Prometheus/Grafana) et métier (Evidently + détecteurs adversariaux)

### 1.2 Le problème métier : la fraude au paiement card-not-present, décidée en temps réel

Les pertes mondiales dues à la fraude au paiement se chiffrent en dizaines de milliards de dollars par an et continuent de croître avec le volume du e-commerce. Pour un marchand ou un prestataire de services de paiement, **trois coûts courent simultanément** :

| Coût | Mécanisme |
|---|---|
| Pertes de fraude | Le marchand supporte les chargebacks sur les transactions card-not-present frauduleuses |
| Frais de chargeback | Les réseaux de cartes facturent un frais par litige, et des ratios de chargeback excessifs déclenchent des programmes de surveillance avec pénalités croissantes et, à terme, la perte du droit de traiter les paiements |
| **Faux refus** | Des clients légitimes bloqués à tort |

Le troisième coût est celui que personne ne budgète et il est fréquemment le plus important. Les études de l'industrie ont montré à plusieurs reprises que la valeur des transactions légitimes faussement refusées **dépasse les pertes de fraude réelles**, souvent de loin. Le dommage de second ordre est pire que la vente perdue : un client à tort refusé abandonne fréquemment le marchand définitivement — le vrai coût est la valeur à vie (LTV), pas la valeur du panier.

Cela produit la propriété définissante du problème : **une matrice de coûts fortement asymétrique, et connaissable**.

|  | Réellement légitime | Réellement frauduleux |
|---|---|---|
| **Approuvé** | €0 (revenu gagné) | −(valeur transaction + frais de chargeback + coût de traitement) |
| **Refusé** | −(marge sur la vente + P(churn) × LTV client) | €0 (perte évitée) |

Une fois cette matrice écrite, optimiser l'AUC ou le F1 devient indéfendable. Le modèle doit **minimiser le coût attendu**, et le seuil de décision découle directement de la matrice plutôt que d'être fixé à 0,5 par défaut.

### 1.3 Pourquoi ce cas d'usage valide l'architecture d'origine

La spécification d'origine (830 lignes) était volontairement « agnostique au cas d'usage ». C'est une force pour un document pédagogique, mais c'est le cœur du problème pour un système d'entreprise : les parties difficiles du ML en production sont exactement celles qui ne sont **pas** transférables d'un cas d'usage à l'autre — budgets de latence, disponibilité des labels, dynamiques adversariales, fraîcheur des features, asymétrie de coût entre types d'erreurs.

Le cas de la fraude au paiement exerce la boucle de réentraînement sous toutes ses coutures :

| Composant d'origine | Justification générique | Nécessité spécifique à la fraude |
|---|---|---|
| DAG de réentraînement Airflow | « démontre l'orchestration » | Les schémas de fraude évoluent en jours ; un modèle obsolète se dégrade mesurablement en quelques semaines |
| Détection de drift Evidently | « compétence de monitoring » | Le drift ici est **adversarial** — un attaquant sonde activement la frontière de décision |
| DVC | « versioning des données » | Nécessaire pour reproduire quelles données un modèle a vues, car les labels arrivent *après* l'entraînement et modifient rétroactivement le dataset historique |
| Kubernetes + HPA | « scalabilité » | Le trafic est spiky par construction : Black Friday, ventes flash et attaques coordonnées arrivent en changements brusques |
| Tags d'image immuables | « bonne pratique » | Les processus réglementaires et de litige exigent de savoir exactement quelle version de modèle a décidé une transaction donnée |
| Rollback en 5 minutes | « bonne pratique » | Un mauvais modèle déployé à 2 000 transactions/seconde cause des dommages financiers mesurables par minute |
| Approbation manuelle pour la prod | « bonne pratique » | Auto-promouvoir un modèle de fraude, c'est comment on refuse tous les clients d'un pays à cause d'un bug de feature |

Les garde-fous de l'architecture d'origine ont été écrits comme bonnes pratiques. Ici, ils sont **structurellement porteurs** (load-bearing).

### 1.4 Objectifs du projet

| Objectif | Ce que ça démontre |
|---|---|
| Reproductibilité | N'importe qui peut cloner et relancer avec une seule commande |
| Traçabilité | Chaque modèle en production est lié à un run MLflow, un commit Git, une version de dataset DVC — et chaque décision est reconstruisible depuis le ledger de décisions |
| Automatisation | Pipeline CI/CD réel, pas un notebook isolé |
| Boucle de feedback | Drift adversarial → réentraînement vintage-aware → shadow → canary → redéploiement |
| Observabilité | Monitoring technique (latence, erreurs) ET monitoring métier (coût net par 1 000 transactions, taux de capture de fraude, taux de faux refus) |
| Scalabilité | Déploiement Kubernetes avec autoscaling, trafic spiky par construction |
| Robustesse | Fail-open : une panne du modèle ne bloque jamais les paiements |

### 1.5 Principes directeurs

- **Infrastructure as Code** : tout est versionné (Dockerfiles, manifests K8s, workflows CI/CD)
- **Immutabilité** : chaque image Docker est taguée avec un hash de commit, jamais de `latest` en production
- **Séparation des environnements** : dev / staging / production clairement isolés
- **Fail fast** : les tests bloquent le pipeline avant tout déploiement — y compris le test de fuite temporelle (leakage)
- **Fail-open** : la décision ne doit jamais être bloquée par la panne du modèle ; on dégrade vers des règles, on ne bloque pas les paiements
- **Coût d'abord** : toutes les décisions de design sont arbitrées par la matrice de coûts, pas par l'accuracy

---

## 2. Les trois contraintes qui redessinent le design

Trois contraintes propres au problème de fraude redessinent l'architecture. Chacune contredit un défaut commun des designs MLOps génériques.

### 2.1 Latence : un budget dur, pas une cible

La décision doit revenir à l'intérieur du flux d'autorisation de paiement. Le budget réaliste de bout en bout pour le composant de décision de fraude est **100 ms à p99**, et il doit être dépensé explicitement :

| Étape | Budget |
|---|---|
| Réseau entrée/sortie | 10 ms |
| Récupération des features (store en ligne) | 25 ms |
| Calcul des features (dans la requête) | 15 ms |
| Inférence du modèle | 20 ms |
| Moteur de règles + logique de décision | 10 ms |
| Logging (asynchrone, hors chemin critique) | 0 ms |
| Marge | 20 ms |
| **Total p99** | **100 ms** |

Trois conséquences immédiates, qui contredisent chacune un défaut courant :

- **Aucun appel base de données synchrone pour les features.** Le pattern PostgreSQL de la conception générique ne peut pas tenir un p99 de 25 ms sous charge. Les features doivent venir d'un store en ligne en mémoire (Redis), alimenté de façon asynchrone.
- **La complexité du modèle est plafonnée par le budget d'inférence.** Un ensemble d'arbres à gradient boosté (GBM) score en quelques millisecondes. Un grand réseau de neurones non, sans infrastructure de serving dédiée qui ajoute son propre coût opérationnel.
- **Le logging des prédictions doit être asynchrone.** Écrire dans PostgreSQL de façon synchrone avant de retourner une décision — ce qu'implique le design `/predict` d'origine — met la base de données sur le chemin critique de chaque paiement. On émet vers une file (Kafka) et on retourne.

**Fail-open, pas fail-closed.** Si le service de modèle est indisponible ou dépasse son budget, la transaction doit retomber sur une décision conservatrice pilotée uniquement par les règles. Un système de fraude qui bloque tous les paiements pendant sa propre panne convertit une panne de composant en interruption totale de revenu. Cette règle de design vaut plus que plusieurs points d'accuracy.

### 2.2 Délai des labels : la contrainte qui casse le MLOps naïf

C'est le problème le plus profond, et la spécification d'origine — comme la plupart des matériaux MLOps — suppose implicitement que les labels sont disponibles au moment de l'entraînement. En fraude, ils ne le sont pas.

**Comment les labels arrivent réellement :**

| Signal | Latence | Fiabilité |
|---|---|---|
| Refus 3-D Secure / émetteur | Secondes | Signal faible, causes multiples |
| Fraude signalée par le client | 2-30 jours | Bonne |
| Chargeback déposé | **30-120 jours** | Fait autorité |
| Résultat de revue manuelle | Heures-jours | Bonne, mais uniquement sur le sous-ensemble revu |

Ainsi, un jour donné, les transactions récentes sont **non labellisées**, et le resteront pendant des mois. S'entraîner uniquement sur des données matures, c'est s'entraîner sur un modèle du monde vieux d'au moins 90 jours — dans un domaine où les schémas d'attaque évoluent en semaines.

**La réponse de design, en trois parties :**

1. **Jeux d'entraînement vintage-aware.** Chaque transaction porte une `label_maturity_date`. Le pipeline d'entraînement déclare explicitement quels vintages sont considérés matures et lesquels sont censurés, et ne traite jamais « pas encore de chargeback » comme « légitime ». Traiter des transactions non matures comme des négatifs apprend systématiquement au modèle que la fraude récente est sans conséquence — le bug le plus courant et le plus destructeur de la modélisation de fraude.
2. **Un canal de labels faibles pour la fraîcheur.** Combiner les signaux partiellement matures (signalements clients, résultats de revue) en labels pondérés, pour que le modèle apprenne des 30 derniers jours à plus faible confiance plutôt que pas du tout.
3. **Correction de la boucle de feedback.** Le modèle ne voit que le résultat des transactions qu'il a **approuvées**. Les transactions qu'il a refusées n'ont pas de ground truth — on n'apprend jamais si elles étaient réellement frauduleuses. À force de réentraînements, le modèle devient progressivement plus confiant sur une région de l'espace de features qu'il a cessé d'observer.

   L'atténuation est délibérée et coûte réellement de l'argent : **approuver un petit échantillon aléatoire des transactions que le modèle aurait refusées** — par exemple 0,5 % de la population des refus, plafonné en valeur. Cela achète des labels non biaisés dans la région des refus. C'est l'équivalent fraude d'un budget d'exploration dans un bandit, c'est une pratique standard chez les opérateurs sophistiqués, et cela exige un accord écrit de la direction parce que les pertes sont réelles et attribuables. À budgéter comme poste de ligne : coût d'amélioration du modèle, pas perte de fraude.

Le point 3 est le détail qui sépare ceux qui ont fait tourner un modèle de fraude en production de ceux qui en ont lu.

### 2.3 Drift adversarial

Le drift ordinaire est passif : le monde change. Le drift adversarial est actif : un attaquant cherche la frontière de décision et la traverse.

Des signatures qui méritent une alerte, et qu'une détection de drift générique ne rattrapera pas :

- **Sondage (probing) :** une rafale de transactions de faible valeur depuis des cartes ou appareils liés, caractéristique d'un test de cartes contre une liste volée.
- **Frottement de frontière (boundary hugging) :** une densité croissante de transactions scorées juste sous le seuil de refus. Une population légitime ne se concentre pas là. C'est l'une des alertes à plus forte valeur de tout le système.
- **Empoisonnement de features :** un attaquant qui fabrique délibérément un historique bénin sur un compte avant la transaction frauduleuse.
- **Rafales coordonnées :** une forte hausse de transactions partageant une empreinte d'appareil, une plage de BIN, une adresse de livraison ou un sous-réseau IP.

Evidently gère bien le drift distributionnel sur les features et les prédictions. Il faut **ajouter des détecteurs explicites pour les signatures ci-dessus**, car elles sont *directionnelles* et adversariales plutôt que simplement distributionnelles : les tests de drift standard ne se déclencheront pas avant que le dommage soit fait.

---

## 3. Architecture globale

### 3.1 Schéma du flux de données et de contrôle

```
                        Requête d'autorisation de paiement
                                    │
                     ┌──────────────▼───────────────┐
                     │   Service de Décision (FastAPI)│   ◀── budget p99 : 100 ms
                     │  ┌─────────────────────────┐  │
      Redis ◀────────┼──│ 1. fetch features online │  │
      store en ligne │  │ 2. calcul dans la requête│  │
                     │  │ 3. score (ensemble GBM)  │  │
                     │  │ 4. surcouche de règles   │  │
                     │  │ 5. décision coût attendu │  │
                     │  └────────┬────────────────┘  │
                     └───────────┼───────────────────┘
                                 │ APPROUVER / RÉVISER / REFUSER
                                 │
                    ┌────────────▼─────────────┐
                    │  Kafka : événements de     │   ◀── asynchrone, hors chemin critique
                    │  décision                  │
                    └──┬────────┬────────┬─────┘
                       │        │        │
        ┌──────────────▼─┐ ┌────▼─────┐ ┌▼──────────────────┐
        │ Agrégateur de  │ │ Ledger de│ │ Monitoring temps  │
        │ features       │ │ décisions│ │ réel (frottement  │
        │ (streaming)    │ │ (S3+PG)  │ │  de frontière,    │
        └────────┬───────┘ └────┬─────┘ │  rafales)         │
                 │              │       └────────┬───────────┘
                 └──▶ Redis     │                │ alerte
                                │                ▼
                    ┌───────────▼──────────┐  ┌──────────────┐
                    │ Réconciliation des   │  │ File de revue│
                    │ labels (chargebacks, │◀─│ analyste     │
                    │  réclamations,       │  │ fraude       │
                    │  résultats de revue) │  └──────────────┘
                    └───────────┬──────────┘
                                │ labels matures + faibles
                    ┌───────────▼─────────────────────────────┐
                    │  Airflow : DAG de réentraînement        │
                    │  (hebdomadaire + déclenché par drift)    │
                    │  GE → DVC → split vintage-aware → train  │
                    │  → seuil matrice de coûts → backtest     │
                    │  → déploiement shadow                    │
                    └───────────┬─────────────────────────────┘
                                │ jamais directement en production
                    ┌───────────▼─────────────────────────────┐
                    │  Shadow (7 j) → Canary 5 % → 25 % → 100 %│
                    │  rollback automatique sur violation de   │
                    │  garde-fou                               │
                    └─────────────────────────────────────────┘
```

### 3.2 Nouveaux composants

| Composant | Rôle |
|---|---|
| **Store de features en ligne Redis** | Récupération de features en moins de 25 ms. Non négociable vu le budget de latence |
| **Kafka / agrégateur streaming** | Maintient les features de vélocité — compteurs et sommes sur fenêtres 1 h / 24 h / 7 j par carte, appareil, marchand, IP — mises à jour en continu plutôt que calculées par requête |
| **Surcouche de règles** | Règles déterministes exécutées à côté du modèle : sanctions et listes de blocage, plafonds de vélocité durs, géographie à risque. Certaines décisions doivent être explicables et modifiables instantanément sans réentraînement. Toute équipe fraude l'exige, et tout design ML-only se la voit rétrofitée sous pression pendant un incident |
| **Ledger de décisions** | Enregistrement immuable de chaque décision : version de modèle, snapshot de features, score, seuils, règles déclenchées, issue. Requis pour la gestion des litiges et pour reconstruire les jeux d'entraînement |
| **Service de réconciliation des labels** | Joint les chargebacks, réclamations clients et résultats de revue aux décisions d'origine ; maintient `label_maturity_date` |
| **File de revue analyste** | Le palier de décision RÉVISER — des transactions trop incertaines pour être auto-décidées. Les décisions humaines sont des labels de haute qualité et doivent être traitées comme une entrée d'entraînement primaire |
| **Harness de déploiement shadow** | Fait tourner le modèle candidat sur le trafic live sans agir dessus. La seule façon honnête d'évaluer un modèle de fraude avant qu'il ne touche de l'argent |

### 3.3 Trois décisions, pas deux

Le `/predict` binaire d'origine (`0|1`) est insuffisant. Les systèmes de fraude ont **trois issues**, et celle du milieu concentre l'essentiel de la valeur :

```
score < t_low          → APPROUVER
t_low ≤ score < t_high → RÉVISER   (file analyste, ou step-up 3-D Secure)
score ≥ t_high         → REFUSER
```

Les deux seuils dérivent de la matrice de coûts **et de la capacité de revue**. Si les analystes peuvent traiter 400 revues/heure, `t_low` est réglé pour que la bande RÉVISER produise à peu près ce volume. C'est le même cadrage contraint par la capacité que dans toute implémentation réelle : le modèle produit un classement, et la contrainte métier détermine où tombent les coupes.

L'alternative step-up — défier le client avec 3-D Secure plutôt que de refuser — est strictement meilleure qu'un refus pour les cas limites : elle transfère la responsabilité à l'émetteur et donne au client un chemin pour finaliser l'achat. Tout design de fraude sans palier step-up laisse de l'argent sur la table.

### 3.4 Description des couches

| Couche | Responsabilité |
|---|---|
| **Ingestion** | Récupérer les données brutes depuis la source (flux d'événements, fichiers, API) |
| **Stockage versionné** | Garder une trace de chaque version du dataset — critique car les labels arrivent après l'entraînement et modifient rétroactivement l'historique |
| **Feature engineering** | Transformer les données brutes en features exploitables, dont la vélocité (fenêtres temporelles), avec correction point-in-time |
| **Entraînement** | Entraîner un ou plusieurs modèles candidats sur des vintages matures déclarés, avec seuil dérivé de la matrice de coûts |
| **Tracking** | Logger hyperparamètres, métriques, artefacts de chaque run |
| **Registry** | Stocker les versions de modèles et gérer leur cycle de vie (staging → shadow → production → archivé) |
| **CI** | Vérifier automatiquement la qualité du code, des données et la correction point-in-time à chaque changement |
| **CD** | Construire et déployer automatiquement une nouvelle version validée |
| **Service de décision** | Exposer le modèle via une API REST, dans le budget de latence, avec surcouche de règles et fail-open |
| **Monitoring infra** | Surveiller la santé technique du service (latence p99, erreurs, charge) |
| **Monitoring modèle** | Surveiller le drift distributionnel ET adversarial, et les métriques métier de fraude |
| **Boucle de réentraînement** | Réagir automatiquement au drift et au vieillissement des vintages, avec correction du biais de la boucle de feedback |

---

## 4. Stack technique détaillée

| Domaine | Outil choisi | Alternatives possibles | Justification du choix |
|---|---|---|---|
| Versioning des données | **DVC** | LakeFS, Pachyderm | Léger, s'intègre nativement à Git, large adoption ; indispensable pour reproduire les datasets à labels rétroactifs |
| Stockage objet | **MinIO** | AWS S3, GCS | S3-compatible, peut tourner localement en Docker |
| Orchestration | **Apache Airflow** | Prefect, Dagster | Standard de l'industrie, écosystème riche |
| Streaming / files d'événements | **Kafka** | RabbitMQ, NATS, Redpanda | Agrégation de vélocité en continu et logging asynchrone des décisions hors chemin critique |
| Store de features en ligne | **Redis** | Memcached, Feast (online store) | Récupération sous les 25 ms exigées par le budget de latence |
| Tracking d'expériences | **MLflow** | Weights & Biases, Neptune | Open source, auto-hébergeable, registry intégré |
| Registry de modèles | **MLflow Model Registry** | Seldon Core, BentoML | Intégré nativement à MLflow |
| Conteneurisation | **Docker** | Podman | Standard incontesté |
| CI/CD | **GitHub Actions** | GitLab CI, Jenkins | Gratuit pour projets publics, intégré à GitHub |
| Orchestration de conteneurs | **Kubernetes** | Docker Swarm, Nomad | Standard de l'industrie pour la scalabilité ; HPA pour le trafic spiky |
| Framework API | **FastAPI** | Flask, Django REST | Performant, typage natif, documentation auto-générée |
| Monitoring infra | **Prometheus + Grafana** | Datadog, New Relic | Open source, standard Kubernetes |
| Monitoring modèle | **Evidently AI + détecteurs adversariaux dédiés** | WhyLabs, Arize | Open source ; les signatures adversariales (frottement de frontière, rafales, sondage) exigent des détecteurs explicites au-delà du drift distributionnel |
| Tests unitaires | **pytest** | unittest | Standard Python, plugins riches |
| Tests de données | **Great Expectations** | Deequ, Soda | Déclaratif, intégration facile aux pipelines |
| Gestion des secrets | **Kubernetes Secrets + Sealed Secrets** | HashiCorp Vault | Suffisant pour ce périmètre, extensible vers Vault ; périmètre PCI-DSS si données réelles |
| Modèle | **GBM (ensemble d'arbres à gradient boosté)** | Réseau de neurones profond | Score en quelques millisecondes — contraint par le budget d'inférence de 20 ms |

---

## 5. Structure du dépôt

```
mlops-project/
│
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Tests, lint, validation données, test de fuite temporelle
│       └── cd.yml                      # Build image + push + déploiement shadow/canary
│
├── airflow/
│   ├── dags/
│   │   ├── training_pipeline.py        # DAG d'entraînement complet (vintage-aware)
│   │   ├── retraining_pipeline.py      # DAG déclenché par drift / planifié
│   │   ├── label_reconciliation_dag.py # DAG de jointure des labels (chargebacks, revues)
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
│   │   ├── build_features.py           # vélocité + features dans la requête
│   │   ├── velocity_aggregator.py      # agrégation streaming (fenêtres 1h/24h/7j)
│   │   ├── point_in_time.py            # correction point-in-time + test de fuite
│   │   └── feature_store.py            # store en ligne Redis + versioning offline
│   │
│   ├── models/
│   │   ├── train.py                    # GBM, split vintage-aware
│   │   ├── threshold.py                # seuils t_low/t_high depuis la matrice de coûts
│   │   ├── evaluate.py                 # backtest sur vintages matures
│   │   ├── promote.py                  # logique staging → shadow → production
│   │   └── exploration.py              # échantillon d'exploration (0,5 % des refus)
│   │
│   ├── api/
│   │   ├── main.py                     # App FastAPI — service de décision
│   │   ├── schemas.py                  # Modèles Pydantic (transaction entrante)
│   │   ├── decision.py                 # logique 3 paliers + fail-open
│   │   ├── rules_engine.py             # surcouche de règles déterministes
│   │   ├── model_loader.py             # Chargement depuis MLflow Registry
│   │   └── metrics.py                  # Instrumentation Prometheus
│   │
│   ├── streaming/
│   │   ├── decision_consumer.py        # consomme les événements de décision
│   │   └── label_reconciliation.py     # jointure chargebacks/réclamations/revues
│   │
│   └── monitoring/
│       ├── drift_detection.py          # Evidently (drift distributionnel)
│       ├── adversarial_detectors.py    # frottement de frontière, rafales, sondage
│       └── alerting.py
│
├── tests/
│   ├── unit/
│   │   ├── test_preprocessing.py
│   │   ├── test_features.py
│   │   ├── test_point_in_time.py       # tente une fuite délibérée → doit échouer
│   │   ├── test_threshold.py
│   │   ├── test_rules_engine.py
│   │   └── test_api.py                 # décisions 3 paliers, fail-open
│   ├── integration/
│   │   └── test_pipeline_end_to_end.py
│   └── data/
│       └── test_data_quality.py        # Great Expectations suites
│
├── docker/
│   ├── Dockerfile.api                  # Image API légère (multi-stage)
│   ├── Dockerfile.training             # Image pour jobs d'entraînement
│   └── docker-compose.yml              # Stack locale complète (+ Redis, Kafka)
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
│           ├── business-metrics.json   # coût net, capture fraude, faux refus
│           └── model-drift.json        # drift + signatures adversariales
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

## 6. Composant : Gestion et versioning des données (DVC)

### 6.1 Rôle

DVC (Data Version Control) permet de versionner des fichiers de données volumineux en parallèle du code Git, sans stocker les données directement dans le dépôt.

### 6.2 Fonctionnement

- Git suit un petit fichier `.dvc` (pointeur/métadonnées + hash)
- Les données réelles sont stockées dans un **remote** (ici MinIO, compatible S3)
- Chaque `dvc add` ou étape de pipeline génère un hash reproductible

### 6.3 Pourquoi c'est critique en fraude

Les labels arrivent **après** l'entraînement et modifient le dataset historique rétroactivement : une transaction d'il y a 60 jours, non labellisée au moment de l'entraînement, devient un chargeback confirmé la semaine suivante. DVC est ce qui permet de :

- reproduire exactement ce qu'un modèle a vu (snapshot à la date d'entraînement) ;
- rejouer un entraînement sur un dataset enrichi rétroactivement et comparer ;
- répondre à un litige réglementaire : « quelle version de données ce modèle a-t-il reçue ? ».

### 6.4 Pipeline DVC (`dvc.yaml`)

```
stages:
  ingest:
    cmd: python src/data/ingestion.py
    outs: [data/raw/transactions.parquet]

  preprocess:
    cmd: python src/data/preprocessing.py
    deps: [data/raw/transactions.parquet]
    outs: [data/processed/transactions.parquet]

  build_features:
    cmd: python src/features/build_features.py
    deps: [data/processed/transactions.parquet]
    outs: [data/features/features.parquet]

  build_training_set:
    cmd: python src/features/point_in_time.py
    deps: [data/features/features.parquet]
    outs: [data/training/train_vintage_aware.parquet]

  train:
    cmd: python src/models/train.py
    deps: [data/training/train_vintage_aware.parquet]
    outs: [models/model.pkl]
    metrics: [metrics.json]
```

### 6.5 Commandes clés

| Commande | Effet |
|---|---|
| `dvc init` | Initialise DVC dans le dépôt |
| `dvc remote add -d storage s3://mlops-bucket` | Configure MinIO comme stockage distant |
| `dvc add data/raw/transactions.parquet` | Commence à suivre un fichier |
| `dvc repro` | Rejoue le pipeline si des dépendances ont changé |
| `dvc push` / `dvc pull` | Synchronise les données avec le remote |
| `dvc metrics diff` | Compare les métriques entre deux versions |

### 6.6 Bénéfice concret

Si un modèle en production se comporte mal, on peut retrouver **exactement** quel dataset a servi à l'entraîner (y compris quels vintages étaient matures et quels labels étaient présents), en checkoutant le commit Git correspondant puis en faisant `dvc pull`.

---

## 7. Composant : Feature Engineering

### 7.1 Rôle

Transformer les données brutes/nettoyées en variables exploitables par le modèle, de façon **identique** à l'entraînement et à l'inférence (éviter le "training-serving skew").

### 7.2 Les features de vélocité sont le modèle

La famille de features la plus prédictive de la fraude à la carte est la **vélocité** — le comportement sur des fenêtres temporelles relativement à la ligne de base propre de l'entité :

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

`device_distinct_cards_24h` mérite une mention spécifique : un appareil qui transacte avec de nombreuses cartes est l'un des indicateurs uniques les plus forts disponibles, et il n'est calculable que si la couche d'agrégation streaming existe. C'est précisément pourquoi l'agrégateur Kafka n'est pas une décoration d'infrastructure optionnelle.

### 7.3 Correction point-in-time : critique et facile à rater

Lors de la construction d'une ligne d'entraînement pour une transaction au temps T, chaque feature de vélocité doit refléter l'état **à T**, pas l'état à aujourd'hui. Calculer `card_txn_count_24h` aujourd'hui pour une transaction vieille de six mois fuit de l'information future et produit un modèle excellent hors ligne qui s'effondre en production. C'est le bug silencieux le plus courant de la modélisation de fraude, et il doit être verrouillé par **un test qui tente délibérément une fuite et vérifie que le pipeline la rejette** (voir §18).

### 7.4 Bonnes pratiques appliquées

- Les transformations sont encapsulées dans des classes/fonctions réutilisables, importées à la fois par `train.py` et par le service de décision (`model_loader.py`)
- Aucune transformation "à la main" dans un notebook qui ne serait pas répliquée en production
- Les statistiques utilisées pour la normalisation (moyenne, écart-type, catégories vues) sont sauvegardées comme artefacts avec le modèle

### 7.5 Store de features en ligne (Redis) et offline (Parquet versionné)

- **Offline** : Parquet versionné par DVC, schéma documenté (nom, type, description, plage attendue) — sert à l'entraînement.
- **Online** : Redis, alimenté en continu par l'agrégateur streaming — sert à l'inférence sous 25 ms.
- La cohérence entre les deux est garantie par la même logique de calcul des fenêtres et vérifiée par les tests d'intégration.

---

## 8. Composant : Tracking d'expériences (MLflow)

### 8.1 Rôle

MLflow Tracking enregistre chaque run d'entraînement : hyperparamètres, métriques, artefacts (modèle, courbes, matrices de confusion), et le code/commit associé.

### 8.2 Architecture du serveur MLflow

```
docker-compose (mlflow/docker-compose.yml) :
  - mlflow-server   (UI + API tracking, port 5000)
  - postgres        (backend store : métadonnées des runs)
  - minio           (artifact store : modèles, fichiers)
```

### 8.3 Exemple d'utilisation dans `train.py`

Le script d'entraînement :
1. Démarre un run MLflow (`mlflow.start_run()`)
2. Logue les hyperparamètres (`mlflow.log_param`)
3. Entraîne le modèle (GBM) sur les vintages matures déclarés
4. Logue les métriques (`mlflow.log_metric` — **coût attendu, taux de capture de fraude, taux de faux refus**, AUC à titre diagnostique)
5. Logue les seuils `t_low` / `t_high` dérivés de la matrice de coûts
6. Logue le modèle lui-même (`mlflow.sklearn.log_model` ou équivalent)
7. Logue des artefacts additionnels (matrice de confusion, feature importance, rapport de vintages)

### 8.4 Ce que ça apporte

- Comparaison visuelle de tous les runs dans l'UI MLflow
- Reproductibilité : chaque run est lié à un commit Git, une version DVC des données **et la déclaration des vintages matures/censurés**
- Base pour la promotion automatique vers le Model Registry et le harness shadow

---

## 9. Composant : Model Registry

### 9.1 Rôle

Le Model Registry gère le cycle de vie des modèles au-delà du simple tracking : versions numérotées, stages (`None`, `Staging`, `Shadow`, `Production`, `Archived`), et annotations.

### 9.2 Cycle de vie d'un modèle

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
  Tests de validation automatiques (evaluate.py :
  backtest vintage-aware, coût attendu, capture, faux refus)
        │
   ┌────┴────┐
   ▼         ▼
 Échec     Succès
   │         │
   ▼         ▼
Rejeté   Stage = "Shadow"
              │  (7 jours sur 100 % du trafic, 0 % d'action)
              │
              ▼
        Canary 5 % → 25 % → 100 %
              │  (garde-fous segmentés, rollback auto)
              ▼
      Stage = "Production"
              │
              ▼
     Ancienne version → "Archived"
```

### 9.3 Critères de promotion (`promote.py`)

Un modèle candidat n'est promu que s'il :
- Passe le backtest sur les vintages matures (coût attendu inférieur au champion, taux de faux refus sous le plafond, capture de fraude au-dessus du minimum)
- Fait mieux que le modèle actuellement en production sur le même jeu de test mature
- Réussit les 7 jours d'évaluation shadow (distribution de scores saine, accord de décision avec le champion dans la bande attendue, latence dans le budget)

### 9.4 Lien avec le service de décision

Le service FastAPI charge toujours le modèle marqué `Production` via l'URI `models:/nom_du_modele/Production`, ce qui permet de changer de modèle sans redéployer l'API — un simple changement de stage dans le Registry suffit (bien qu'en pratique, on redéploie quand même pour garder une image immuable et traçable). La version de modèle exacte est enregistrée dans le ledger de décisions pour chaque transaction.

---

## 10. Composant : Orchestration (Apache Airflow)

### 10.1 Rôle

Airflow orchestre les pipelines sous forme de DAGs (Directed Acyclic Graphs), gère la planification, les dépendances entre tâches, les retries, et les alertes en cas d'échec.

### 10.2 DAGs du projet

| DAG | Déclencheur | Rôle |
|---|---|---|
| `data_ingestion_dag` | Planifié (ex : toutes les nuits) | Récupère les nouvelles transactions, les valide, les versionne avec DVC |
| `label_reconciliation_dag` | Planifié (ex : quotidien) | Joint les chargebacks, réclamations clients et résultats de revue aux décisions d'origine ; met à jour `label_maturity_date` |
| `training_pipeline` | Manuel ou après ingestion | Exécute tout le pipeline : préprocessing → features point-in-time → split vintage-aware → entraînement → seuil matrice de coûts → backtest → enregistrement MLflow |
| `retraining_pipeline` | **Planifié hebdomadaire sur un calendrier randomisé** + déclenché par drift | Relance l'entraînement, évalue en shadow, puis canary |

> **Calendrier randomisé.** Un réentraînement hebdomadaire sur un rythme prévisible est lui-même exploitable par un attaquant qui connaît le calendrier. La planification doit être randomisée (fenêtre aléatoire autour d'une cadence nominale), et l'architecture et les seuils du modèle traités comme information sensible plutôt que comme documentation publique.

### 10.3 Structure type du DAG (`retraining_pipeline.py`)

```
with DAG("retraining_pipeline", schedule_interval=None, ...) as dag:

    check_drift = PythonOperator(task_id="check_drift", ...)          # drift distributionnel + adversarial
    reconcile_labels = PythonOperator(task_id="reconcile_labels", ...) # chargebacks, réclamations, revues
    preprocess = PythonOperator(task_id="preprocess", ...)
    build_features = PythonOperator(task_id="build_features", ...)
    build_training_set = PythonOperator(task_id="build_training_set", ...) # vintages + test de fuite
    train_model = PythonOperator(task_id="train_model", ...)
    optimize_threshold = PythonOperator(task_id="optimize_threshold", ...) # t_low / t_high depuis la matrice de coûts
    evaluate_model = PythonOperator(task_id="evaluate_model", ...)          # backtest vintages matures
    deploy_shadow = PythonOperator(task_id="deploy_shadow", ...)            # jamais directement en prod
    notify = PythonOperator(task_id="notify_team", ...)

    check_drift >> reconcile_labels >> preprocess >> build_features >> build_training_set \
        >> train_model >> optimize_threshold >> evaluate_model >> deploy_shadow >> notify
```

### 10.4 Bonnes pratiques Airflow appliquées

- Chaque tâche est idempotente (peut être relancée sans effet de bord)
- Utilisation de `XCom` pour passer les identifiants de run MLflow entre tâches
- Alertes Slack/e-mail en cas d'échec (`on_failure_callback`)
- Séparation claire entre logique métier (dans `src/`) et orchestration (dans `airflow/dags/`)

---

## 11. Composant : Service de décision (FastAPI)

### 11.1 Rôle

Exposer le modèle de décision de fraude via une API REST performante, typée et documentée automatiquement, dans le budget de latence de **100 ms à p99**, avec surcouche de règles et chemin fail-open.

### 11.2 Endpoints principaux

| Endpoint | Méthode | Rôle |
|---|---|---|
| `/decide` | POST | Décide une ou plusieurs transactions (APPROUVER / RÉVISER / REFUSER) |
| `/health` | GET | Healthcheck pour Kubernetes (liveness/readiness probes) |
| `/metrics` | GET | Expose les métriques au format Prometheus |
| `/model-info` | GET | Retourne la version du modèle actuellement chargé |

### 11.3 Budget de latence (p99)

| Étape | Budget |
|---|---|
| Réseau entrée/sortie | 10 ms |
| Feature retrieval (Redis) | 25 ms |
| Feature computation (in-request) | 15 ms |
| Inférence modèle | 20 ms |
| Règles + logique de décision | 10 ms |
| Logging (asynchrone, hors chemin critique) | 0 ms |
| Marge | 20 ms |
| **Total p99** | **100 ms** |

### 11.4 Chargement du modèle (`model_loader.py`)

Le modèle est chargé une seule fois au démarrage de l'application (pas à chaque requête), directement depuis le MLflow Model Registry via son URI (`models:/nom_du_modele/Production`). Un rechargement périodique ou déclenché par webhook peut être ajouté pour prendre en compte les nouvelles promotions sans redémarrage complet.

### 11.5 Logique de décision (`decision.py`)

```
score = modèle(features)
règles déclenchées = rules_engine(transaction, features)

si modèle indisponible ou budget dépassé :
    → décision basée uniquement sur les règles (fail-open, conservateur)

sinon :
    score < t_low          → APPROUVER
    t_low ≤ score < t_high → RÉVISER   (file analyste, ou step-up 3-D Secure)
    score ≥ t_high         → REFUSER
```

La décision est émise vers **Kafka de façon asynchrone** (événement de décision) : ledger, agrégateur de features et monitoring en sont alimentés sans être sur le chemin critique.

### 11.6 Validation des entrées (`schemas.py`)

Utilisation de **Pydantic** pour définir strictement le schéma attendu en entrée (types, plages de valeurs, champs obligatoires), ce qui rejette automatiquement les requêtes malformées avec un code 422 et un message clair.

### 11.7 Instrumentation (`metrics.py`)

L'API expose nativement :
- Nombre de requêtes par endpoint et code de statut
- Latence des décisions (histogramme, p50/p95/p99)
- Taux d'approbation / révision / refus par segment (pays, BIN) — alimente les garde-fous de canary
- Distribution des scores (alimente la détection de frottement de frontière)
- Version du modèle servi

---

## 12. Composant : Conteneurisation (Docker)

### 12.1 Stratégie multi-stage

Le `Dockerfile.api` utilise un build multi-stage pour réduire la taille finale de l'image :

```
Stage 1 (builder)  : installe les dépendances, compile si nécessaire
Stage 2 (runtime)  : copie uniquement le nécessaire depuis le builder,
                      utilise une image de base slim (python:3.11-slim),
                      exécute en tant qu'utilisateur non-root
```

### 12.2 Bonnes pratiques appliquées

- Image de base minimale (`slim` ou `distroless`)
- Un seul processus par conteneur (principe de responsabilité unique)
- `.dockerignore` pour exclure notebooks, données, `.git`
- Healthcheck défini dans le Dockerfile
- Utilisateur non-root pour la sécurité
- Tag d'image basé sur le hash du commit Git, jamais `latest` en production

### 12.3 `docker-compose.yml` (environnement local complet)

Permet de lancer toute la stack en une commande pour le développement :
- Service de décision FastAPI
- Redis (store de features en ligne) + Kafka (événements de décision, agrégation)
- MLflow server + Postgres + MinIO
- Prometheus + Grafana
- (Optionnel) Airflow en mode standalone

---

## 13. Composant : CI/CD (GitHub Actions)

### 13.1 Pipeline CI (`ci.yml`) — déclenché à chaque push/PR

Étapes exécutées :
1. **Lint** : `ruff` ou `flake8` + `black --check`
2. **Tests unitaires** : `pytest tests/unit` — dont `test_point_in_time.py` : **tente une fuite temporelle délibérée et exige que le pipeline la rejette**
3. **Tests de qualité des données** : suites Great Expectations
4. **Tests d'intégration** : pipeline complet sur un échantillon de données
5. **Scan de sécurité** : `bandit` (code) + `trivy` (image Docker)
6. **Build de test** : vérifie que l'image Docker se construit sans erreur

### 13.2 Pipeline CD (`cd.yml`) — déclenché sur merge vers `main`

Étapes exécutées :
1. Build de l'image Docker taguée avec le hash du commit
2. Push vers GitHub Container Registry (GHCR)
3. Mise à jour du manifest Kubernetes (nouveau tag d'image) via Kustomize
4. Déploiement en **staging** automatique
5. Tests de fumée (smoke tests) sur staging
6. Déploiement en **production** (approbation manuelle via GitHub Environments)
7. **Rollout staged : shadow → canary 5 % → 25 % → 100 %** avec garde-fous et rollback automatique (voir §15)

### 13.3 Exemple de structure du workflow CD

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

  deploy-production-shadow:
    needs: deploy-staging
    environment: production
    - deploy model en mode shadow (100 % score, 0 % action)
    - gate : distribution des scores saine, latence dans le budget

  deploy-production-canary:
    needs: deploy-production-shadow
    - canary 5 % → 25 % (garde-fous segmentés)
    - gate : taux d'approbation ±2 %, pas de régression de latence

  deploy-production-full:
    needs: deploy-production-canary
    - 100 % + signature manuelle du responsable fraude
```

---

## 14. Composant : Déploiement (Kubernetes)

### 14.1 Ressources principales

| Fichier | Rôle |
|---|---|
| `deployment.yaml` | Définit les pods du service de décision (replicas, image, ressources CPU/RAM, probes) |
| `service.yaml` | Expose les pods en interne (ClusterIP) ou en externe (LoadBalancer) |
| `configmap.yaml` | Variables de configuration non sensibles (URL MLflow, nom du modèle, seuils) |
| `hpa.yaml` | Horizontal Pod Autoscaler — scale automatiquement selon CPU/latence |

### 14.2 Exemple conceptuel de `deployment.yaml`

- `replicas: 3` (haute disponibilité)
- `livenessProbe` sur `/health` (redémarre le pod s'il est bloqué)
- `readinessProbe` sur `/health` (retire le pod du load balancer s'il n'est pas prêt)
- `resources.requests` / `resources.limits` définis pour éviter la sur-consommation
- Stratégie de déploiement `RollingUpdate` avec `maxUnavailable: 0` pour zéro downtime

### 14.3 Organisation avec Kustomize

- `base/` : configuration commune
- `overlays/staging/` et `overlays/production/` : surcharges spécifiques (nombre de replicas, ressources, variables d'environnement)

### 14.4 Autoscaling (`hpa.yaml`)

Le HPA ajuste le nombre de pods entre un minimum et un maximum en fonction de l'utilisation CPU moyenne (ou d'une métrique custom comme la latence p99 via Prometheus Adapter). Le trafic de paiement est **spiky par construction** — Black Friday, ventes flash et attaques coordonnées arrivent en changements brusques — le HPA doit être configuré en conséquence (scale-up rapide, stabilisation du scale-down).

### 14.5 Exigences de latence et de disponibilité

- Redis et le service de décision doivent être co-localisés pour tenir le budget réseau de 10 ms
- Le chemin fail-open (règles uniquement) doit être testé en conditions réelles : une panne simulée du service de modèle ne doit jamais bloquer les paiements

---

## 15. Déploiement du modèle : shadow, puis canary, toujours

Remplacer le « approbation manuelle puis déploiement » d'origine par un rollout staged, parce qu'en fraude **les métriques hors ligne ne prédisent pas réellement les performances en ligne** :

| Étape | Durée | Trafic | Condition de passage |
|---|---|---|---|
| Shadow | 7 jours | 100 % scoré, 0 % actionné | Distribution des scores saine ; accord de décision avec le champion dans la bande attendue ; latence dans le budget |
| Canary | 24 heures | 5 % | Taux d'approbation à ±2 % du champion ; pas de régression de latence ; pas d'effondrement de segment |
| Ramp | 48 heures | 25 % | Taux de fraude non élevé ; proxies de faux refus stables |
| Full | — | 100 % | Signature manuelle du responsable fraude |

**Déclencheurs de rollback automatique**, évalués en continu à chaque étape :

```
le taux d'approbation chute de plus de 3 points vs champion → rollback immédiat
latence p99 > 100 ms pendant 5 minutes consécutives         → rollback immédiat
taux de refus d'un segment top-20 pays/BIN > 2×             → rollback immédiat
taux d'erreur > 0,5 %                                       → rollback immédiat
```

Le déclencheur **par segment** est essentiel. Un modèle peut tenir des métriques agrégées stables tout en refusant presque toutes les transactions d'un pays à cause d'un bug d'encodage dans une valeur de catégorie rare. Le monitoring agrégé ne rattrapera pas ça ; le monitoring par segment oui — et c'est la version agrégée seule de cet alerting qui fait durer ces incidents des jours.

---

## 16. Composant : Monitoring infrastructure (Prometheus/Grafana)

### 16.1 Rôle

Surveiller la santé technique du système : disponibilité, latence, taux d'erreur, charge.

### 16.2 Flux de collecte

```
FastAPI (/metrics) ──scrape──▶ Prometheus ──requête──▶ Grafana (dashboards)
                                     │
                                     ▼
                              Alertmanager (alertes Slack/e-mail)
```

### 16.3 Métriques clés suivies

- `http_requests_total` (par endpoint, par code de statut)
- `http_request_duration_seconds` (histogramme de latence — **p99 ≤ 100 ms est un garde-fou de rollback**)
- `decision_score_distribution` (distribution des scores — alimente la détection de frottement de frontière)
- `approval_rate` / `review_rate` / `decline_rate` par segment (pays, BIN, appareil)
- `decision_latency_p99`
- Métriques infra standard (CPU, mémoire des pods) via `kube-state-metrics`

### 16.4 Dashboards Grafana fournis

- **Business metrics** : coût net par 1 000 transactions (le chiffre du tableau de bord exécutif), taux de capture de fraude, taux de faux refus, ratio de chargeback, taux de revue et précision de revue
- **API Performance** : latence p50/p95/p99, taux d'erreur, requêtes/seconde
- **Model Drift** : drift distributionnel + signatures adversariales (frottement de frontière, rafales, sondage)

### 16.5 Alertes types configurées

| Alerte | Condition |
|---|---|
| Latence de décision | p99 > 100 ms pendant 5 minutes → **rollback immédiat** |
| Taux d'erreur | > 0,5 % d'erreurs pendant 5 minutes → **rollback immédiat** |
| Taux d'approbation | chute > 3 points de pourcentage vs champion → **rollback immédiat** |
| Refus par segment | taux de refus d'un segment top-20 pays/BIN > 2× → **rollback immédiat** |
| Pod en crash loop | Redémarrages répétés détectés |

---

## 17. Composant : Monitoring du modèle et Data Drift (Evidently)

### 17.1 Rôle

Détecter quand les données reçues en production divergent significativement des données d'entraînement (data drift), quand les performances du modèle se dégradent (concept drift), et — spécifiquement en fraude — quand un **attaquant** sonde ou traverse la frontière de décision.

### 17.2 Fonctionnement (`drift_detection.py`)

1. Un échantillon des décisions de production est loggé (features + score) via le flux Kafka
2. Périodiquement (ex : chaque jour via un DAG Airflow dédié), Evidently compare ce jeu de données récent au jeu de données de référence (celui utilisé à l'entraînement, vintages matures)
3. Un rapport est généré (HTML + JSON) avec des tests statistiques par feature (ex : test de Kolmogorov-Smirnov pour les variables numériques, chi carré pour les catégorielles)
4. Un score global de drift est calculé

### 17.3 Détecteurs adversariaux (`adversarial_detectors.py`)

Le drift distributionnel ne suffit pas : les signatures adversariales sont *directionnelles* et les tests standards ne se déclencheront pas avant que le dommage soit fait. Ajouter des détecteurs explicites :

| Détecteur | Signature | Valeur |
|---|---|---|
| **Sondage (probing)** | Rafale de transactions de faible valeur depuis des cartes/appareils liés | Caractéristique du test de cartes contre une liste volée |
| **Frottement de frontière (boundary hugging)** | Densité croissante de transactions scorées juste sous le seuil de refus | Une population légitime ne se concentre pas là — **l'une des alertes à plus forte valeur du système** |
| **Empoisonnement de features** | Historique bénin fabriqué délibérément sur un compte avant la transaction frauduleuse | Attaque active sur l'espace de features |
| **Rafales coordonnées** | Hausse forte de transactions partageant empreinte d'appareil, plage BIN, adresse de livraison ou sous-réseau IP | Attaque coordonnée en cours |

### 17.4 Déclenchement du réentraînement

Si le score de drift dépasse un seuil défini (ex : plus de 30 % des features montrent une dérive significative), ou si un détecteur adversarial se déclenche, Airflow déclenche automatiquement le DAG `retraining_pipeline`.

### 17.5 Ce que ça démontre

C'est la brique qui transforme un simple pipeline de déploiement en véritable **système MLOps auto-adaptatif face à un adversaire actif** — le modèle ne se dégrade pas silencieusement en production, et les attaques en cours sont vues avant que le dommage soit fait.

---

## 18. Composant : Tests et qualité (pytest, Great Expectations)

### 18.1 Pyramide de tests du projet

```
        ┌─────────────────────┐
        │  Tests end-to-end   │   (pipeline complet sur échantillon)
        ├─────────────────────┤
        │  Tests d'intégration│   (interaction entre composants)
        ├─────────────────────┤
        │  Tests unitaires    │   (fonctions individuelles)
        └─────────────────────┘
```

### 18.2 Tests unitaires (`tests/unit/`)

- `test_preprocessing.py` : vérifie que le nettoyage produit le schéma attendu
- `test_features.py` : vérifie les transformations de features (valeurs limites, NaN, types)
- **`test_point_in_time.py` : construit une ligne d'entraînement en injectant délibérément des features calculées « aujourd'hui » pour une transaction passée et vérifie que le pipeline de construction la rejette** — la fuite temporelle est un échec de build
- `test_threshold.py` : vérifie que `t_low` / `t_high` dérivent correctement de la matrice de coûts et de la capacité de revue
- `test_rules_engine.py` : vérifie les règles déterministes (blocages, plafonds de vélocité, géographie) et l'ordre de priorité modèle/règles
- `test_api.py` : teste les endpoints FastAPI avec `TestClient` (décisions 3 paliers, cas invalides, **chemin fail-open quand le modèle est indisponible**)

### 18.3 Tests de qualité des données (Great Expectations)

Suites d'attentes déclaratives, par exemple :
- Une colonne ne doit jamais contenir de valeurs nulles
- Une colonne numérique doit rester dans une plage définie
- Le nombre de lignes du dataset doit être supérieur à un seuil minimal
- Les types de colonnes doivent correspondre au schéma attendu
- `label_maturity_date` doit être présente et cohérente avec la date de transaction

Ces tests s'exécutent **avant** l'entraînement, pour éviter d'entraîner un modèle sur des données corrompues.

### 18.4 Tests d'intégration

Vérifient que le pipeline complet (ingestion → features point-in-time → split vintage → entraînement → seuil → backtest → enregistrement MLflow) fonctionne de bout en bout sur un petit échantillon, en environnement CI. Un test d'intégration dédié vérifie le chemin fail-open du service de décision.

---

## 19. Boucle de réentraînement automatique

### 19.1 Vue d'ensemble

C'est la caractéristique qui distingue un projet MLOps "complet" d'un simple pipeline de déploiement — et en fraude, elle est **structurellement obligatoire** : les schémas d'attaque évoluent en jours, et un modèle obsolète se dégrade mesurablement en quelques semaines.

### 19.2 Déclencheurs possibles

| Déclencheur | Description |
|---|---|
| **Planifié** | Réentraînement périodique sur un **calendrier randomisé** (cadence hebdomadaire nominale, fenêtre aléatoire) — un rythme prévisible est exploitable |
| **Basé sur le drift** | Déclenché par Evidently quand le score de drift dépasse un seuil |
| **Basé sur les signatures adversariales** | Déclenché par la détection de frottement de frontière, rafales coordonnées ou sondage |
| **Basé sur la performance** | Déclenché si les métriques métier (capture de fraude, faux refus) chutent sous un seuil, quand les labels matures deviennent disponibles |
| **Manuel** | Déclenchement depuis l'UI Airflow par un data scientist |

### 19.3 Séquence complète

```
1. Détection (drift, signature adversarial, planning)
        ↓
2. Airflow déclenche retraining_pipeline
        ↓
3. Réconciliation des labels (chargebacks, réclamations, résultats de revue)
        ↓
4. Récupération des transactions récentes (versionnées via DVC)
        ↓
5. Construction du jeu vintage-aware : vintages matures vs censurés,
   labels faibles pondérés pour la fraîcheur — jamais « pas de chargeback » = légitime
        ↓
6. Réentraînement (GBM, même code que train.py, nouvelles données)
        ↓
7. Optimisation des seuils t_low/t_high depuis la matrice de coûts
   et la capacité de revue
        ↓
8. Backtest comparatif vs modèle en production (vintages matures)
        ↓
9. Si meilleur → promotion en Staging → déploiement SHADOW (7 jours)
        ↓
10. Canary 5 % → 25 % avec garde-fous → 100 % (signature fraude lead)
        ↓
11. Monitoring renforcé : métriques agrégées ET par segment
```

### 19.4 Garde-fous importants

- Un modèle réentraîné n'est **jamais** promu automatiquement sans passer les mêmes seuils de qualité que lors du déploiement initial, et **jamais** sans 7 jours d'évaluation shadow
- Les transactions non matures ne sont **jamais** labellisées négatives ; les vintages sont suivis explicitement
- Le **budget d'exploration** (échantillon aléatoire de 0,5 % des refus, plafonné en valeur) tourne en continu pour acheter des labels non biaisés dans la région des refus — il est budgété comme coût d'amélioration du modèle, avec accord écrit de la direction
- Conservation systématique des N dernières versions en production pour un rollback rapide (< 5 minutes, démontré en game day)
- Notification de l'équipe à chaque promotion automatique (traçabilité humaine même dans un système automatisé)
- Les décisions de revue des analystes reviennent automatiquement dans le jeu d'entraînement comme labels de haute qualité

---

## 20. Sécurité et gestion des secrets

### 20.1 Principes appliqués

- Aucun secret (mots de passe, clés API, credentials MinIO/S3) n'est commité dans le dépôt
- `.env.example` documente les variables nécessaires sans valeurs réelles
- En Kubernetes : utilisation de `Secrets` natifs, idéalement chiffrés avec **Sealed Secrets** ou gérés via **HashiCorp Vault** pour un contexte entreprise
- Scan automatique des images Docker (`trivy`) et du code (`bandit`) dans la CI
- Communication interne entre services via réseau privé Kubernetes (pas d'exposition inutile)
- Principe du moindre privilège pour les comptes de service (RBAC Kubernetes)

### 20.2 Spécificité PCI-DSS

Les données de transactions de cartes réelles sont dans le périmètre **PCI-DSS** : chiffrement au repos et en transit, segmentation réseau, contrôle d'accès strict, journalisation d'audit. Ce projet est conçu pour être **prêt PCI-DSS par construction** (pas de données de carte persistées au-delà des besoins, tokenisation/hashage des identifiants de carte dans le ledger), mais toute mise en production avec des données réelles doit passer une validation PCI-DSS formelle. Une démonstration sur dataset public est légitime — elle n'est pas une preuve de conformité.

### 20.3 Informations sensibles

L'architecture du modèle et les valeurs de seuil sont des **informations sensibles** : un attaquant qui connaît la frontière de décision et le calendrier de réentraînement peut les exploiter. À traiter comme tel dans la documentation interne.

### 20.4 Exemple de flux de secret en production

```
Secret créé manuellement/via Vault
        ↓
Monté comme variable d'environnement ou volume dans le pod
        ↓
Jamais loggé, jamais exposé dans /metrics ou /health
```

---

## 21. Métriques de succès

Remplacer accuracy et F1 par les métriques qu'une organisation de paiement rapporte déjà :

| Métrique | Définition | Cible |
|---|---|---|
| Taux de capture de fraude | Valeur de fraude bloquée / valeur totale de fraude tentée | > 75 % |
| Taux de faux refus | Transactions légitimes refusées / total légitime | < 0,8 % |
| Ratio de chargeback | Chargebacks / transactions | Sous les seuils de surveillance des réseaux |
| Taux de revue | Transactions envoyées aux analystes / total | Dans la capacité des analystes |
| Précision de revue | Fraude confirmée / revues | > 30 % |
| Latence de décision p99 | De bout en bout | < 100 ms |
| **Coût net par 1 000 transactions** | Coût attendu depuis la matrice | **Cible d'optimisation primaire** |

La dernière ligne est celle qui doit apparaître sur le tableau de bord exécutif. C'est un nombre unique, libellé en euros, qui trade correctement les pertes de fraude contre les faux refus. Chaque autre métrique est diagnostique.

---

## 22. Plan de mise en œuvre étape par étape

| Phase | Livrable | Jours |
|---|---|---|
| 0 | Matrice de coûts validée avec le métier ; seuils dérivés | 3 |
| 1 | Ledger de décisions + schéma d'événements + topics Kafka | 4 |
| 2 | Agrégateur de vélocité streaming → store en ligne Redis | 6 |
| 3 | Constructeur de jeux d'entraînement point-in-time + test de fuite | 5 |
| 4 | Service de réconciliation des labels + gestion vintage/maturité | 5 |
| 5 | GBM de base + optimisation du seuil par coût attendu | 4 |
| 6 | Service de décision : sortie 3 paliers, surcouche de règles, chemin fail-open | 5 |
| 7 | Durcissement de la latence jusqu'au budget p99 sous charge | 4 |
| 8 | File de revue analyste + capture des labels depuis les résultats de revue | 5 |
| 9 | Détecteurs de drift adversarial (frottement de frontière, rafales, sondage) | 4 |
| 10 | DAG de réentraînement Airflow, déclenché par drift et planifié (calendrier randomisé) | 4 |
| 11 | Harness de déploiement shadow | 3 |
| 12 | Canary + rollback automatique avec garde-fous par segment | 4 |
| 13 | Échantillon d'exploration aléatoire (0,5 % des refus), avec accord écrit du métier | 2 |
| 14 | Dashboards Grafana : métriques métier d'abord, techniques ensuite | 3 |
| 15 | Runbooks d'incident + game day (attaque simulée, mauvais modèle simulé) | 4 |

**Durée totale estimée : ~65 jours.**

---

## 23. Critères de succès / Definition of Done

- [ ] Latence de décision p99 < 100 ms à 3× le pic de charge attendu
- [ ] La panne du service de modèle dégrade vers des règles uniquement, ne bloque jamais les paiements
- [ ] Correction point-in-time appliquée ; une tentative de fuite délibérée fait échouer le build
- [ ] Les transactions non matures ne sont jamais labellisées négatives ; les vintages suivis explicitement
- [ ] L'échantillon d'exploration aléatoire tourne, est budgété et signé par écrit
- [ ] Chaque décision est reconstruisible depuis le ledger avec sa version de modèle exacte
- [ ] Les détecteurs de frottement de frontière et de rafales se déclenchent sur du trafic d'attaque simulé
- [ ] Aucun modèle n'atteint la production sans 7 jours d'évaluation shadow
- [ ] Les déclencheurs de rollback par segment rattrapent un bug pays-spécifique injecté délibérément
- [ ] Rollback en moins de 5 minutes, démontré en game day
- [ ] Les décisions de revue des analystes reviennent automatiquement dans le jeu d'entraînement
- [ ] Le tableau de bord exécutif rapporte le coût net par 1 000 transactions, pas l'accuracy

---

## 24. Risques honnêtes

**L'accès aux données est le vrai blocage.** Les données de transactions de cartes sont dans le périmètre PCI-DSS. Personne ne les confie pour un projet de ce type. Construire ce système contre un dataset public est une démonstration légitime de l'architecture, mais il ne faut pas revendiquer des performances de fraude de production depuis un dataset public — l'équilibre des classes, la disponibilité des features et les dynamiques adversariales y sont tous non représentatifs, et n'importe qui du secteur des paiements le verra immédiatement.

**L'échantillon d'exploration coûte de l'argent, visiblement.** Approuver délibérément des transactions que le modèle a signalées est correct, et ce sera quand même la première chose questionnée quand quelqu'un examinera les pertes de fraude. Il faut un accord écrit, une ligne de reporting séparée et un plafond de valeur dur. Sans cela, il sera annulé lors du premier mauvais mois, et le biais de boucle de feedback reviendra.

**Les adversaires s'adaptent à la défense, y compris au calendrier de réentraînement.** Un réentraînement hebdomadaire sur une cadence prévisible est lui-même exploitable. Randomiser le calendrier, et traiter l'architecture du modèle et les valeurs de seuil comme des informations sensibles plutôt que comme de la documentation.

**Les règles ne disparaîtront jamais, et c'est correct.** Tout design de fraude pur-ML réintroduit des règles sous la pression d'un incident, généralement au pire moment et sans tests. Construire le moteur de règles dès le premier jour, le versionner, le tester, et donner à l'équipe fraude la capacité de le modifier sans déploiement. Une entrée de liste de blocage doit être effective en secondes, pas dans un cycle de release.

**Les faux refus sont invisibles sans instrumentation délibérée.** Les pertes de fraude arrivent comme chargebacks ; un client à tort refusé part simplement et n'est jamais compté. La mesure par proxy — comportement de nouvelle tentative, contacts du service client, taux de commandes ultérieures des clients refusés, et l'échantillon d'exploration — est le seul moyen de voir ce coût. Un système qui ne le mesure pas s'optimisera vers le refus de tout, et chaque tableau de bord aura l'air excellent pendant que le revenu tombera silencieusement.

---

## 25. Extensions possibles (pour aller plus loin)

| Extension | Valeur ajoutée |
|---|---|
| **Step-up 3-D Secure automatisé** | Le palier RÉVISER déclenche un challenge 3DS au lieu d'une revue humaine pour les cas limites — transfère la responsabilité à l'émetteur, donne au client un chemin d'achat |
| **Feast** (feature store complet) | Cohérence garantie entre features online/offline au-delà du couple Redis/Parquet |
| **Seldon Core / KServe** | Serving avancé (A/B testing, canary, explainability intégrée) |
| **HashiCorp Vault** | Gestion de secrets de niveau entreprise (et trajectoire PCI-DSS) |
| **Argo CD** | GitOps pour le déploiement Kubernetes (au lieu de `kubectl apply` en CI) |
| **Explainability (SHAP)** | Endpoint `/explain` pour justifier chaque décision (et chaque litige) |
| **Tests de biais/équité** | Vérification automatique de fairness avant promotion |
| **Chaos engineering (Chaos Mesh)** | Valider la résilience du chemin fail-open en production |
| **Multi-modèles / Champion-Challenger** | Comparer plusieurs modèles en production simultanément — déjà structurellement prévu par le shadow/canary |
| **Consortium data** | Échange de signatures de fraude entre opérateurs (réseaux de confiance) pour enrichir les features sans partager de données de carte |

---

## Annexe : Glossaire rapide

| Terme | Définition |
|---|---|
| **Data drift** | Changement dans la distribution des données d'entrée en production par rapport à l'entraînement |
| **Drift adversarial** | Drift causé par un attaquant qui sonde ou traverse activement la frontière de décision |
| **Concept drift** | Changement dans la relation entre les features et la cible à prédire |
| **Vintage** | Cohorte de transactions par période (ex : mois de transaction) ; un vintage est mature quand tous ses labels potentiels sont arrivés |
| **Label maturity** | Date à partir de laquelle une transaction peut être considérée comme labellisée (ex : 120 jours pour les chargebacks) |
| **Censure** | Transactions dont le label n'est pas encore arrivé ; les traiter comme négatives est le bug le plus destructeur de la modélisation de fraude |
| **Point-in-time correctness** | Construction de chaque ligne d'entraînement avec les features telles qu'elles étaient au moment de la transaction, jamais « aujourd'hui » |
| **Frottement de frontière (boundary hugging)** | Concentration anormale de transactions scorées juste sous le seuil de refus — signature d'adaptation adversarial |
| **Fail-open** | Le service de décision dégrade vers des règles uniquement en cas de panne du modèle, au lieu de bloquer tous les paiements |
| **Échantillon d'exploration** | Approbation aléatoire d'une fraction des refus (ex : 0,5 %, plafonnée) pour acheter des labels non biaisés dans la région de décision |
| **Shadow deployment** | Le modèle candidat score 100 % du trafic sans agir sur aucune décision |
| **Canary deployment** | Déploiement progressif d'une nouvelle version sur un sous-ensemble du trafic, avec garde-fous et rollback automatique |
| **Rolling update** | Mise à jour progressive des pods sans interruption de service |
| **Coût net par 1 000 transactions** | Métrique exécutive unique, libellée en euros, qui trade pertes de fraude contre faux refus via la matrice de coûts |
| **Idempotence** | Propriété d'une opération pouvant être répétée sans changer le résultat au-delà de la première exécution |