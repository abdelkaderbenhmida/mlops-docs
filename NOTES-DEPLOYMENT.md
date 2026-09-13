# Project Documentation — Deployment Notes (Azure Live)

## Objective
- Get all 4 MLOps projects working **in Azure** (real public endpoints, no local resource use).
- Fix previously-found problems, add auto-retrain triggers, audit every tool/feature per project.

## Important Details
- All 4 projects are separate git repos under `/home/gadour/Desktop/new_project/other/`.
- Live Azure access: subscription `e9fc4cf7-b074-4f13-b215-3de898f125a9`, tenant `supcom.tn` (user `abdelkader.benhmida@supcom.tn`). `az` 2.89.1, terraform, docker, kubectl installed.
- Projects use **already-provisioned Azure VMs** (not AKS). Deploy onto existing VMs, one project at a time.

## VM / IP / SSH-Key Inventory
| Project | IP | Region | SSH Key | User | Ports |
|---------|----|--------|---------|------|-------|
| platform-spec | `20.16.127.15` | westeurope | `.worktrees/proj2/infra/terraform/id_rsa` | `azureuser` | 8000 (API) + 5000 (MLflow) |
| spec-detailed | `10.3.0.10` | westeurope (**no public IP**, reached via ProxyCommand through platform-spec VM) | spec's RSA key via azure run-command | `azureuser` | — |
| full-mlops | `20.64.210.229` | westus2 | `.worktrees/proj1/infra/terraform/.ssh/id_ed25519` | `azureuser` | 8000 (NSG `AllowAPI-8000` added) |
| project-documentation | `20.230.188.197` | eastus | `.worktrees/proj4/infra/.ssh/id_rsa` | **ubuntu** (root blocked) | 8000/5000 NSG allow rules present |

## Model / Domain Notes
- spec-detailed canonical domain: predictive maintenance (AI4I), but live training uses **telco churn** (`churn-model`, target `churn`).
- project-documentation live stack uses **telco churn** (`churn_model`), Postgres backend, MinIO S3 artifact store, feature engineering mismatch (22 features vs model 20).

## Networking / Quota
- VNet peerings `spec-to-detailed` + `detailed-to-spec` created (Connected).
- westeurope vCPU quota 4/4 (2x Standard_D2), ~2 VMs max simultaneously in that region.
- `/tmp/opencode/datasets/telco_churn.csv` exists (real 7043-row dataset).
- full-mlops NSG allowed 22, 3000, 5000; port 8000 added as `AllowAPI-8000` (priority 1003).

## Work State

### Completed
- **platform-spec VM live**: MLflow 2.10.0 container, Postgres backend, `credit-risk-model` v4 Staging, drift 0.333 fires, retrain loop passes (AUC 0.843, KS 0.531). Drift + retrain deployed.
- **spec-detailed VM live** (via jump): containers `mlops-postgres`, `mlops-mlflow`, `mlops-fastapi` (network `mlops-net`). Trained `churn-model` v3 → Production. `/predict` works. Drift + retrain trigger deployed.
- **full-mlops VM live**: RandomForest fraud model on synthetic creditcard.csv, `fraud_model` v2 Production. FastAPI serving layer created. Drift + retrain trigger deployed.
- **project-documentation VM: mostly live**: Postgres + MinIO + MLflow + API on `mlops-stack_mlops`. MLflow config fixed. Trained + registered `churn_model` v2 Production. API health OK.

### Active / Blocked
- project-documentation `/predict` fails: `X has 22 features, but RandomForestClassifier is expecting 20 features`. Attempted fixes (monkey-patching model predict, patching loader) did not persist because model is reloaded fresh each request.

## Next Moves
1. **Retrain** churn model with full 22-feature `FEATURE_ORDER` + re-register/promote to Production. ✅ Model retrained (accuracy 0.74, f1 0.447, roc_auc 0.755), but registration hit MLflow artifact-store permission error (`/mlflow`).
2. Fix MLflow container to use S3/MinIO artifact store properly and register the new model version.

## Relevant Files
- `src/api/model_loader.py`, `src/api/main.py`, `src/features/build_features.py` (FEATURE_ORDER = 22), `src/models/train.py`
- `docker/docker-compose.yml`, `mlflow/Dockerfile.mlflow`
- `.worktrees/proj4/infra/.ssh/id_rsa` (SSH key, user ubuntu, IP 20.230.188.197)
- Other projects' keys/monitoring files listed in Workspace summary.

## Current Fix in Progress (MLflow S3 artifact store)
Restarted `mlops-mlflow` container with:
```
mlflow server --host 0.0.0.0 --port 5000 \
  --backend-store-uri postgresql+psycopg2://mlflow:mlflow@mlops-postgres:5432/mlflow \
  --default-artifact-root s3://mlops-bucket/mlflow-artifacts \
  --artifacts-destination s3://mlops-bucket/mlflow-artifacts
```
Next: register the retrained 22-feature model to Production, then verify `/predict`.
