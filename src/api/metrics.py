"""Prometheus instrumentation for the FastAPI application.

Exposes:
- request count / latency histograms per endpoint and status (instrumentator)
- prediction value histogram (feeds the model drift dashboards)
- live model version gauge
"""

from __future__ import annotations

from prometheus_client import Gauge, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

MODEL_PREDICTION_VALUE = Histogram(
    "model_prediction_value",
    "Distribution of predicted churn probabilities",
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
)

PREDICTIONS_TOTAL = Gauge(
    "predictions_total",
    "Cumulative number of prediction requests",
    ["model_version"],
)

MODEL_VERSION = Gauge(
    "mlops_model_version",
    "Version of the model currently served",
    ["model_name"],
)


def setup_metrics(app) -> Instrumentator:
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_group_untemplated=True,
        should_respect_env_var=False,
    )
    instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)
    return instrumentator


def record_prediction(probability: float, model_version: str) -> None:
    MODEL_PREDICTION_VALUE.observe(probability)
    PREDICTIONS_TOTAL.labels(model_version=model_version).inc()


def set_model_version(model_name: str, model_version: str) -> None:
    MODEL_VERSION.labels(model_name=model_name).set(float(model_version) if model_version.isdigit() else 0.0)
