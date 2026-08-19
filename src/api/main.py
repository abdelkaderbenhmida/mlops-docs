"""FastAPI inference service for the demand forecasting model.

Endpoints:
- POST /predict        single or batch prediction
- GET  /health         liveness/readiness probe
- GET  /metrics        Prometheus metrics
- GET  /model-info     metadata of the loaded model
- GET  /               serves the UI dashboard
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from src.api import metrics
from src.api.model_loader import loader
from src.api.schemas import (
    DemandPredictionRequest,
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
    PredictionResult,
    _demand_bucket,
)

logger = logging.getLogger("mlops-api")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "production_report.json"
UI_DIR = PROJECT_ROOT / "ui"

app = FastAPI(
    title="MLOps Demand Forecasting API",
    description="Serves the production demand forecasting model from the MLflow Model Registry.",
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


def _predict_one(request: DemandPredictionRequest) -> PredictionResponse:
    bundle = loader.get_bundle()
    df = request.to_dataframe()
    try:
        predictions = bundle.predict(df)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"prediction failed: {exc}") from exc
    predicted_units = int(round(predictions[0]))
    bucket = _demand_bucket(predicted_units)
    metrics.record_prediction(float(predicted_units), bundle.version)
    return PredictionResponse(
        predicted_units=predicted_units,
        demand_bucket=bucket,
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


@app.get("/", tags=["ui"])
def serve_ui():
    index_path = UI_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    raise HTTPException(status_code=404, detail="UI not found")


metrics.setup_metrics(app)
