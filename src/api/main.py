"""FastAPI inference service for the churn model.

Endpoints:
- POST /predict        single or batch prediction
- GET  /health         liveness/readiness probe for Kubernetes
- GET  /metrics        Prometheus metrics
- GET  /model-info     metadata of the loaded model
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException

from src.api import metrics
from src.api.model_loader import loader
from src.api.schemas import (
    ChurnPredictionRequest,
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
    PredictionResult,
)

logger = logging.getLogger("mlops-api")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "production_report.json"

app = FastAPI(
    title="MLOps Churn Inference API",
    description="Serves the production churn model from the MLflow Model Registry.",
    version="1.0.0",
)


@app.on_event("startup")
def _startup() -> None:
    try:
        bundle = loader.load()
        metrics.set_model_version(bundle.model_name, bundle.version)
        logger.info("model loaded: %s version %s", bundle.model_name, bundle.version)
    except Exception as exc:  # noqa: BLE001
        logger.error("model loading failed: %s", exc)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    try:
        bundle = loader.get_bundle()
        return HealthResponse(status="ok", model_name=bundle.model_name, model_version=bundle.version)
    except Exception:  # noqa: BLE001
        return HealthResponse(status="degraded")


@app.get("/model-info", response_model=ModelInfoResponse, tags=["health"])
def model_info() -> ModelInfoResponse:
    bundle = loader.get_bundle()
    production_metrics = None
    if PRODUCTION_REPORT.exists():
        production_metrics = json.loads(PRODUCTION_REPORT.read_text()).get("metrics")
    return ModelInfoResponse(
        model_name=bundle.model_name,
        model_version=bundle.version,
        run_id=bundle.run_id,
        production_metrics=production_metrics,
    )


def _predict_one(request: ChurnPredictionRequest) -> PredictionResponse:
    bundle = loader.get_bundle()
    df = request.to_dataframe()
    try:
        probabilities = np.asarray(bundle.predict_proba(df))[:, 1]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"prediction failed: {exc}") from exc
    probability = float(probabilities[0])
    metrics.record_prediction(probability, bundle.version)
    return PredictionResponse(
        prediction=int(probability >= 0.5),
        probability=probability,
        model_name=bundle.model_name,
        model_version=bundle.version,
    )


@app.post("/predict", response_model=PredictionResult, tags=["inference"])
def predict(payload: PredictionRequest) -> PredictionResult:
    if isinstance(payload, list):
        if not payload:
            raise HTTPException(status_code=422, detail="empty prediction batch")
        return [_predict_one(request) for request in payload]
    return _predict_one(payload)


metrics.setup_metrics(app)
