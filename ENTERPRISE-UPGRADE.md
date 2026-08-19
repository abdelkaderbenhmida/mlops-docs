# Enterprise Upgrade — From "Automated Retraining Loop" to a Real-Time Payment Fraud Platform

> Target product name: **Sentry** — sub-100ms card fraud decisioning with a closed-loop
> retraining system built around delayed and biased labels.
>
> This document rewrites `mlops-project-documentation.md`. The stack survives almost intact:
> DVC, MinIO, Airflow, MLflow, Docker, GitHub Actions, Kubernetes, FastAPI, Prometheus,
> Grafana, Evidently, pytest, Great Expectations. What changes is the workload — from
> batch-scored, use-case-agnostic classification to a latency-bound, adversarial,
> label-delayed problem where the retraining loop the spec already describes stops being a
> nice demonstration and becomes structurally mandatory.

---

## 1. What the original does well, and what it lacks

The original is the most complete of the four documents: 830 lines, a genuine architecture
diagram, a stack table with justifications *and* considered alternatives, secret management,
a test pyramid, drift-triggered retraining with explicit guardrails, and a Definition of Done
that includes a five-minute rollback requirement. The engineering judgement is consistently
sound.

Its one weakness is stated openly in §1.2: the project is "designed to be use-case agnostic."
That is presented as flexibility, and for a teaching document it is. For an enterprise system
it is the core problem — because the hard parts of production ML are exactly the parts that
are *not* transferable between use cases. Latency budgets, label availability, adversarial
dynamics, feature freshness, and the cost asymmetry between error types are all use-case
specific, and they are what actually determine the architecture.

Pick the use case that most fully exercises the retraining loop the spec has already built,
then design for its specific constraints.

---

## 2. The enterprise problem

**Card-not-present payment fraud, decided in real time.**

Global payment fraud losses run into the tens of billions of dollars annually and continue to
grow with e-commerce volume. For any given merchant or payment service provider, three costs
run simultaneously:

| Cost | Mechanism |
|---|---|
| Fraud losses | The merchant bears chargebacks on fraudulent card-not-present transactions |
| Chargeback fees | Card networks charge a per-dispute fee on top of the disputed amount, and excessive chargeback ratios trigger monitoring programmes with escalating penalties and, ultimately, loss of processing rights |
| **False declines** | Legitimate customers wrongly blocked |

The third is the one nobody budgets for and it is frequently the largest. Industry studies
have repeatedly found that the value of falsely declined legitimate transactions exceeds
actual fraud losses, often by a wide margin. The second-order damage is worse than the lost
sale: a wrongly declined customer frequently abandons the merchant permanently, so the true
cost is lifetime value, not basket value.

This produces the defining property of the problem: **a sharply asymmetric, and knowable, cost
matrix.**

|  | Actually legitimate | Actually fraud |
|---|---|---|
| **Approved** | €0 (revenue earned) | −(transaction value + chargeback fee + handling cost) |
| **Declined** | −(margin on sale + P(churn) × customer LTV) | €0 (loss avoided) |

Once you can write that matrix, optimising for AUC or F1 becomes indefensible. The model must
minimise expected cost, and the decision threshold falls directly out of the matrix rather
than being set to 0.5 by default.

---

## 3. Why this use case validates the original architecture

| Original component | Generic justification | Fraud-specific necessity |
|---|---|---|
| Airflow retraining DAG | "demonstrates orchestration" | Fraud patterns shift in days; a stale model degrades measurably within weeks |
| Evidently drift detection | "monitoring skill" | Drift here is **adversarial** — an attacker is actively probing for the boundary |
| DVC | "data versioning" | Needed to reproduce which data a model saw, since labels arrive *after* training and change the historical dataset retroactively |
| Kubernetes + HPA | "scalability" | Traffic is spiky by construction: Black Friday, flash sales, and coordinated attacks all arrive as sudden step changes |
| Immutable image tags | "good practice" | Regulatory and dispute processes require knowing exactly which model version decided a specific transaction |
| 5-minute rollback | "good practice" | A bad model deployed at 2,000 transactions/second causes measurable financial damage per minute |
| Manual approval for prod | "good practice" | Auto-promoting a fraud model is how you decline every customer in a country because of a feature bug |

The original's guardrails were written as best practice. Here they are load-bearing.

---

## 4. The three constraints that reshape the design

### 4.1 Latency: a hard budget, not a target

The decision must return inside the payment authorisation flow. The realistic end-to-end
budget for the fraud decision component is **100ms at p99**, and it must be spent explicitly:

| Stage | Budget |
|---|---|
| Network in/out | 10ms |
| Feature retrieval (online store) | 25ms |
| Feature computation (in-request) | 15ms |
| Model inference | 20ms |
| Rules engine + decision logic | 10ms |
| Logging (asynchronous, off critical path) | 0ms |
| Headroom | 20ms |
| **Total p99** | **100ms** |

Three consequences follow immediately, and each contradicts a common default:

- **No synchronous database call for features.** The original's PostgreSQL-backed pattern
  cannot meet a 25ms p99 under load. Features must come from an in-memory online store
  (Redis) populated asynchronously.
- **Model complexity is capped by the inference budget.** A gradient-boosted tree ensemble
  scores in single-digit milliseconds. A large neural model does not, without dedicated
  serving infrastructure that adds its own operational cost.
- **Prediction logging must be asynchronous.** Writing to PostgreSQL synchronously before
  returning a decision — which the original's `/predict` design implies — puts the database
  on the critical path of every payment. Fire to a queue and return.

**Fail-open, not fail-closed.** If the model service is unavailable or exceeds its budget, the
transaction must fall through to a conservative rules-only decision. A fraud system that
blocks all payments during its own outage converts a component failure into a total revenue
outage. This single design rule is worth more than several points of model accuracy.

### 4.2 Label delay: the constraint that breaks naive MLOps

This is the deepest problem and the original spec — like most MLOps material — implicitly
assumes labels are available at training time. In fraud they are not.

**How labels actually arrive:**

| Signal | Latency | Reliability |
|---|---|---|
| 3-D Secure / issuer decline | Seconds | Weak signal, many causes |
| Customer-reported fraud | 2-30 days | Good |
| Chargeback filed | **30-120 days** | Authoritative |
| Manual review outcome | Hours-days | Good, but only on reviewed subset |

So on any given day, recent transactions are **unlabelled**, and will remain so for months.
Training only on fully-matured data means training on a model of the world that is at minimum
90 days old — in a domain where attack patterns turn over in weeks.

**The design response, in three parts:**

1. **Vintage-aware training sets.** Every transaction carries a `label_maturity_date`. The
   training pipeline explicitly declares which vintages are considered mature and which are
   censored, and never treats "no chargeback yet" as "legitimate." Treating unmatured
   transactions as negatives systematically teaches the model that recent fraud is fine — the
   single most common and most damaging bug in fraud modelling.

2. **A weak-label channel for recency.** Combine partially-matured signals (customer reports,
   manual review outcomes) into weighted labels, so the model can learn from the last 30 days
   at lower confidence rather than not at all.

3. **Correction for the feedback loop.** The model only sees the outcome of transactions it
   approved. Transactions it declined have no ground truth — you never learn whether they were
   actually fraud. Over successive retrains the model becomes progressively more confident
   about a region of the feature space it has stopped observing.

   The mitigation is deliberate and costs real money: **approve a small random sample of
   transactions the model would have declined** — for example 0.5% of the decline population,
   subject to a value cap. This purchases unbiased labels in the decline region. It is the
   fraud equivalent of an exploration budget in a bandit, it is standard practice at
   sophisticated operators, and it requires explicit business sign-off because the losses are
   real and attributable. Budget it as a line item: model-improvement cost, not fraud loss.

Point 3 is the detail that separates people who have run a fraud model in production from
people who have read about one.

### 4.3 Adversarial drift

Ordinary drift is passive: the world changes. Adversarial drift is active: an attacker
searches for the boundary and moves through it.

Signatures worth alerting on, which generic drift detection will not catch:

- **Probing:** a burst of low-value transactions from related cards or devices, characteristic
  of card testing against a stolen list.
- **Boundary hugging:** a rising density of transactions scoring just below the decline
  threshold. A legitimate population does not concentrate there. This is one of the highest-
  value alerts in the entire system.
- **Feature poisoning:** an attacker deliberately manufacturing benign history on an account
  before the fraudulent transaction.
- **Coordinated bursts:** a sharp rise in transactions sharing a device fingerprint, BIN
  range, shipping address, or IP subnet.

Evidently handles distributional drift on features and predictions well. Add explicit
detectors for the above, because they are *directional* and adversarial rather than merely
distributional, and standard drift tests will not fire until the damage is done.

---

## 5. Architecture changes

```
                        Payment authorisation request
                                    │
                     ┌──────────────▼───────────────┐
                     │   Decision Service (FastAPI)  │   ◀── p99 budget: 100ms
                     │  ┌─────────────────────────┐  │
      Redis ◀────────┼──│ 1. fetch online features │  │
      online store   │  │ 2. compute in-request    │  │
                     │  │ 3. score (GBM ensemble)  │  │
                     │  │ 4. rules engine overlay  │  │
                     │  │ 5. expected-cost decide  │  │
                     │  └────────┬────────────────┘  │
                     └───────────┼───────────────────┘
                                 │ APPROVE / REVIEW / DECLINE
                                 │
                    ┌────────────▼─────────────┐
                    │  Kafka: decision events   │  ◀── async, off critical path
                    └──┬────────┬────────┬─────┘
                       │        │        │
        ┌──────────────▼─┐ ┌────▼─────┐ ┌▼──────────────────┐
        │ Feature        │ │ Decision │ │ Real-time monitor  │
        │ aggregator     │ │ ledger   │ │ (boundary-hugging, │
        │ (streaming)    │ │ (S3+PG)  │ │  burst detection)  │
        └────────┬───────┘ └────┬─────┘ └────────┬───────────┘
                 │              │                │
                 └──▶ Redis     │                │ alert
                                │                ▼
                    ┌───────────▼──────────┐  ┌──────────────┐
                    │ Label reconciliation │  │ Fraud analyst│
                    │ (chargebacks, claims,│◀─│ review queue │
                    │  review outcomes)    │  └──────────────┘
                    └───────────┬──────────┘
                                │ matured + weak labels
                    ┌───────────▼─────────────────────────────┐
                    │  Airflow: retraining DAG (weekly +      │
                    │  drift-triggered)                        │
                    │  GE → DVC → vintage-aware split → train  │
                    │  → cost-matrix threshold → backtest      │
                    │  → shadow deploy                         │
                    └───────────┬─────────────────────────────┘
                                │ never straight to production
                    ┌───────────▼─────────────────────────────┐
                    │  Shadow (7d) → Canary 5% → 25% → 100%   │
                    │  automatic rollback on guardrail breach  │
                    └─────────────────────────────────────────┘
```

### 5.1 New components

| Component | Purpose |
|---|---|
| **Redis online feature store** | Sub-25ms feature retrieval. Non-negotiable given the latency budget |
| **Kafka / streaming aggregator** | Maintains velocity features — count and sum over 1h/24h/7d windows per card, device, merchant, IP — updated continuously rather than computed per request |
| **Rules engine overlay** | Deterministic rules run alongside the model: sanctions and blocklist checks, hard velocity caps, high-risk geography. Some decisions must be explainable and instantly changeable without a retrain. Every fraud team requires this and every ML-only design gets it retrofitted under pressure during an incident |
| **Decision ledger** | Immutable record of every decision: model version, feature snapshot, score, threshold, rules fired, outcome. Required for dispute handling and for reconstructing training sets |
| **Label reconciliation service** | Joins chargebacks, customer claims, and review outcomes back to original decisions; maintains `label_maturity_date` |
| **Analyst review queue** | The REVIEW decision tier — transactions too uncertain to auto-decide. Human decisions are high-quality labels and should be treated as a primary training input |
| **Shadow deployment harness** | Runs the candidate model on live traffic without acting on it. The only honest way to evaluate a fraud model before it touches money |

### 5.2 Three decisions, not two

The original's binary `/predict` returning `0|1` is insufficient. Fraud systems have three
outcomes, and the middle one is where most of the value lives:

```
score < t_low          → APPROVE
t_low ≤ score < t_high → REVIEW   (analyst queue, or step-up 3-D Secure challenge)
score ≥ t_high         → DECLINE
```

Both thresholds derive from the cost matrix and from **review capacity**. If analysts can
handle 400 reviews/hour, `t_low` is set so the REVIEW band produces roughly that volume. This
is the same capacity-constrained framing that appears in any real deployment: the model
produces a ranking, and the business constraint determines where the cuts fall.

The step-up alternative — challenging the customer with 3-D Secure rather than declining — is
strictly better than a decline for borderline cases, since it shifts liability to the issuer
and gives the customer a path to complete the purchase. Any fraud design that lacks a step-up
tier is leaving money on the table.

### 5.3 Feature engineering: velocity features are the model

The single most predictive feature family in card fraud is velocity — behaviour over time
windows relative to an entity's own baseline:

```
card_txn_count_1h, card_txn_count_24h, card_txn_count_7d
card_amount_sum_24h / card_amount_avg_30d          # ratio to own baseline
card_distinct_merchants_24h
card_distinct_countries_24h
device_distinct_cards_24h                          # very strong fraud signal
ip_distinct_cards_1h
merchant_decline_rate_1h
time_since_last_txn_seconds
amount_zscore_vs_card_history
is_first_txn_at_merchant
billing_shipping_distance_km
hour_of_day_zscore_vs_card_history
```

`device_distinct_cards_24h` deserves specific mention: one device transacting with many cards
is one of the strongest single indicators available, and it is only computable if the
streaming aggregation layer exists. This is precisely why the Kafka aggregator is not
optional infrastructure decoration.

**Point-in-time correctness is critical and easy to get wrong.** When constructing a training
row for a transaction at time T, every velocity feature must reflect state as of T, not as of
now. Computing `card_txn_count_24h` today for a transaction from six months ago leaks future
information and produces a model that performs beautifully offline and collapses in
production. This is the most common silent bug in fraud modelling, and it must be enforced by
a test that deliberately attempts a leak and asserts the pipeline rejects it.

---

## 6. Deployment: shadow, then canary, always

Replace the original's "manual approval then deploy" with a staged rollout, because in fraud
the offline metrics genuinely do not predict online performance:

| Stage | Duration | Traffic | Gate to proceed |
|---|---|---|---|
| Shadow | 7 days | 100% scored, 0% acted upon | Score distribution sane; decision agreement with champion within expected band; latency within budget |
| Canary | 24 hours | 5% | Approval rate within ±2% of champion; no latency regression; no segment collapse |
| Ramp | 48 hours | 25% | Fraud rate not elevated; false-decline proxy metrics stable |
| Full | — | 100% | Manual sign-off from the fraud lead |

**Automatic rollback triggers**, evaluated continuously at every stage:

```
approval_rate drops > 3 percentage points vs. champion  → immediate rollback
p99 latency > 100ms for 5 consecutive minutes           → immediate rollback
decline rate for any top-20 country/BIN segment > 2×    → immediate rollback
error rate > 0.5%                                       → immediate rollback
```

The per-segment trigger is essential. A model can hold aggregate metrics steady while
declining nearly every transaction from one country because of an encoding bug in a rarely
seen category value. Aggregate monitoring will not catch that; segment monitoring will, and
the aggregate-only version of this alerting is how these incidents run for days.

---

## 7. Success metrics

Replace accuracy and F1 with metrics a payments organisation already reports on:

| Metric | Definition | Target |
|---|---|---|
| Fraud capture rate | Fraud value blocked / total fraud value attempted | > 75% |
| False decline rate | Legitimate transactions declined / total legitimate | < 0.8% |
| Chargeback ratio | Chargebacks / transactions | Below network monitoring thresholds |
| Review rate | Transactions sent to analysts / total | Within analyst capacity |
| Review precision | Confirmed fraud / reviewed | > 30% |
| Decision latency p99 | End-to-end | < 100ms |
| Net cost per 1,000 transactions | Expected cost from the matrix | Primary optimisation target |

The last row is the one that should appear on the executive dashboard. It is a single number,
denominated in euros, that correctly trades fraud losses against false declines. Every other
metric is diagnostic.

---

## 8. Implementation plan

| Phase | Deliverable | Days |
|---|---|---|
| 0 | Cost matrix agreed with the business; thresholds derived from it | 3 |
| 1 | Decision ledger + event schema + Kafka topics | 4 |
| 2 | Streaming velocity aggregator → Redis online store | 6 |
| 3 | Point-in-time-correct training set builder + leakage test | 5 |
| 4 | Label reconciliation service + vintage/maturity handling | 5 |
| 5 | Baseline GBM + expected-cost threshold optimisation | 4 |
| 6 | Decision service: 3-tier output, rules overlay, fail-open path | 5 |
| 7 | Latency hardening to the p99 budget under load | 4 |
| 8 | Analyst review queue + label capture from review outcomes | 5 |
| 9 | Adversarial drift detectors (boundary hugging, bursts, probing) | 4 |
| 10 | Airflow retraining DAG, drift-triggered and scheduled | 4 |
| 11 | Shadow deployment harness | 3 |
| 12 | Canary + automatic rollback with segment-level guardrails | 4 |
| 13 | Random-approval exploration sample, with business sign-off | 2 |
| 14 | Grafana dashboards: business metrics first, technical second | 3 |
| 15 | Incident runbooks + game day (simulated attack, simulated bad model) | 4 |

**Total: ~65 days.**

---

## 9. Definition of Done

- [ ] p99 decision latency under 100ms at 3× peak expected load
- [ ] Model service failure degrades to rules-only, never blocks payments
- [ ] Point-in-time correctness enforced; a deliberate leakage attempt fails the build
- [ ] Unmatured transactions are never labelled negative; vintages tracked explicitly
- [ ] Random exploration sample runs, is budgeted, and is signed off in writing
- [ ] Every decision is reconstructible from the ledger with its exact model version
- [ ] Boundary-hugging and burst detectors fire on simulated attack traffic
- [ ] No model reaches production without 7 days of shadow evaluation
- [ ] Segment-level rollback triggers catch a deliberately injected country-specific bug
- [ ] Rollback completes in under 5 minutes, demonstrated in a game day
- [ ] Analyst review decisions flow back into the training set automatically
- [ ] Executive dashboard reports net cost per 1,000 transactions, not accuracy

---

## 10. Honest risks

**Data access is the real blocker.** Card transaction data is PCI-DSS scoped. Nobody hands it
over for a project of this kind. Building this against a public dataset is a legitimate
demonstration of the architecture, but do not claim production fraud performance from a
public dataset — the class balance, the feature availability, and the adversarial dynamics are
all unrepresentative, and anyone from the payments industry will know it immediately.

**The exploration sample costs money, visibly.** Deliberately approving transactions the model
flagged is correct and will still be the first thing questioned when someone reviews fraud
losses. It needs written sign-off, a separate reporting line, and a hard value cap. Without
those it gets cancelled in the first bad month, and the feedback-loop bias returns.

**Adversaries adapt to the defence, including to the retraining schedule.** A weekly retrain on
a predictable cadence is itself exploitable. Randomise the schedule, and treat model
architecture and threshold values as sensitive information rather than as documentation.

**Rules will never go away, and that is correct.** Every ML-purist fraud design eventually
reintroduces rules under incident pressure, usually at the worst possible moment and without
tests. Build the rules engine in from day one, version it, test it, and give the fraud team
the ability to change it without a deployment. A blocklist entry must be effective in seconds,
not in a release cycle.

**False declines are invisible without deliberate instrumentation.** Fraud losses arrive as
chargebacks; a falsely declined customer simply leaves and is never counted. Proxy
measurement — retry behaviour, customer service contacts, subsequent-order rate for declined
customers, and the exploration sample — is the only way to see this cost at all. A system that
does not measure it will optimise itself into declining everything, and every dashboard will
look excellent while revenue quietly falls.
