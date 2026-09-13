.PHONY: help setup install data preprocess features train evaluate promote api \
        validate test lint format security dvc-repro dvc-push dvc-pull compose-up \
        compose-down compose-build docker-build-api docker-build-training monitor \
        drift clean

PYTHON ?= python3
MLFLOW_TRACKING_URI ?= http://localhost:5000

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Create virtualenv and install all dependencies
	$(PYTHON) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/pip install -e .

install: ## Install runtime dependencies
	$(PYTHON) -m pip install -r requirements.txt

data: ## Generate the synthetic demand dataset
	$(PYTHON) scripts/generate_synthetic_data.py

ingest: ## Ingest raw data (DVC stage 1)
	$(PYTHON) src/data/ingestion.py

preprocess: ## Preprocess raw data (DVC stage 2)
	$(PYTHON) src/data/preprocessing.py

validate: ## Validate processed data with Great Expectations
	$(PYTHON) src/data/validation.py

features: ## Build features (DVC stage 3)
	$(PYTHON) src/features/build_features.py

train: ## Train + track + register model (DVC stage 4)
	MLFLOW_TRACKING_URI=$(MLFLOW_TRACKING_URI) $(PYTHON) src/models/train.py

evaluate: ## Evaluate candidate model against quality gates
	MLFLOW_TRACKING_URI=$(MLFLOW_TRACKING_URI) $(PYTHON) src/models/evaluate.py

promote: ## Promote validated model to production
	MLFLOW_TRACKING_URI=$(MLFLOW_TRACKING_URI) $(PYTHON) src/models/promote.py

api: ## Run the FastAPI inference service locally
	MLFLOW_TRACKING_URI=$(MLFLOW_TRACKING_URI) uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

drift: ## Run drift detection (reference vs current production data)
	$(PYTHON) src/monitoring/drift_detection.py

test: ## Run all tests
	$(PYTHON) -m pytest

test-unit: ## Run unit tests
	$(PYTHON) -m pytest tests/unit

lint: ## Lint with ruff
	ruff check src airflow scripts
	black --check --line-length 120 src airflow scripts

security: ## Security scan with bandit (fails on HIGH severity only)
	bandit -r src -x tests -lll

dvc-repro: ## Re-run the DVC pipeline end to end
	dvc repro

dvc-push: ## Push data to the DVC remote
	dvc push

dvc-pull: ## Pull data from the DVC remote
	dvc pull

compose-up: ## Start the full local stack
	docker compose -f docker/docker-compose.yml up -d --build

compose-down: ## Stop the local stack
	docker compose -f docker/docker-compose.yml down

compose-build: ## Build local images
	docker compose -f docker/docker-compose.yml build

mlflow-up: ## Start MLflow + Postgres + MinIO only
	docker compose -f mlflow/docker-compose.yml up -d --build

docker-build-api: ## Build the API image
	docker build -f docker/Dockerfile.api -t mlops-api:local .

docker-build-training: ## Build the training image
	docker build -f docker/Dockerfile.training -t mlops-training:local .

monitor: ## Open the Grafana dashboard
	@echo "Grafana: http://localhost:3000 (admin/admin)"

clean: ## Remove generated artifacts
	rm -rf data/processed data/features data/monitoring models/mlruns mlruns .pytest_cache
