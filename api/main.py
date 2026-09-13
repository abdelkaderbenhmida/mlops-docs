# TODO: high - Add request validation and error handling
# TODO: medium - Implement request/response logging
# TODO: low - Add health check endpoint improvement
"""FastAPI app for Demand Forecasting (P4) — self-contained, trains on real PBS data at startup."""

import os
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

UI_DIR = Path(__file__).parent.parent / "ui"
DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "pbs_demand_data.csv"
MODEL = None
FEATURE_COLS = None
MODEL_METRICS = {"r2": None, "mae": None}
PREDICTION_LOG = []
LOG_CAP = 500
BUCKET_KEYS = ["low", "medium", "high", "very_high"]
CONCESSION_TYPES = []
DRUG_IDS = []


class PredictRequest(BaseModel):
    drug_id: str = Field(default="CONCESSIONAL SAFETY NET_A03_DRUGS FOR FUNCTIONAL GASTROINTESTINAL DISORDERS")
    concession: str = Field(default="CONCESSIONAL SAFETY NET")
    month: int = Field(default=6, ge=1, le=12)
    year: int = Field(default=2005, ge=1991, le=2006)
    lag_1: float = Field(default=5000, ge=0)
    lag_12: float = Field(default=4800, ge=0)
    rolling_mean_3: float = Field(default=4900, ge=0)
    rolling_mean_6: float = Field(default=4850, ge=0)


class PredictResponse(BaseModel):
    predicted_units: float
    forecast_bucket: str
    confidence: str


def load_pbs_data() -> pd.DataFrame:
    """Load and prepare PBS demand data for training."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"PBS data not found at {DATA_PATH}. Run ml/data/generate_demand_data.py first.")

    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} rows from PBS data")

    global CONCESSION_TYPES, DRUG_IDS
    CONCESSION_TYPES = sorted(df["concession_type"].unique().tolist())
    DRUG_IDS = sorted(df["drug_id"].unique().tolist())

    feature_cols = ["month", "lag_1", "lag_12", "rolling_mean_3", "rolling_mean_6"]
    X = df[feature_cols]
    y = df["target"]

    return X, y, feature_cols


def train_model():
    """Train RandomForestRegressor on PBS data."""
    global MODEL, FEATURE_COLS, MODEL_METRICS

    X, y, feature_cols = load_pbs_data()
    FEATURE_COLS = feature_cols

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    MODEL = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
    MODEL.fit(X_train, y_train)

    preds = MODEL.predict(X_test)
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    MODEL_METRICS["r2"] = round(r2, 4)
    MODEL_METRICS["mae"] = round(mae, 4)
    print(f"P4: Trained on {len(X_train)} samples, R²={r2:.4f}, MAE={mae:.2f}")
    print(f"P4: Features: {feature_cols}")
    print(f"P4: Concession types: {CONCESSION_TYPES}")
    print(f"P4: Drug series: {len(DRUG_IDS)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    train_model()
    yield

app = FastAPI(title="Demand Forecasting API (PBS)", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": MODEL is not None, "data_source": "PBS (Australian Pharmaceutical Benefits Scheme)"}


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    t0 = time.perf_counter()
    df = pd.DataFrame([{
        "month": req.month,
        "lag_1": req.lag_1,
        "lag_12": req.lag_12,
        "rolling_mean_3": req.rolling_mean_3,
        "rolling_mean_6": req.rolling_mean_6,
    }])[FEATURE_COLS]
    units = float(MODEL.predict(df)[0])
    latency_ms = (time.perf_counter() - t0) * 1000.0

    if units > 10000:
        bucket = "very_high"
    elif units > 5000:
        bucket = "high"
    elif units > 1000:
        bucket = "medium"
    else:
        bucket = "low"

    confidence = "high" if 500 < units < 50000 else "medium"

    result = PredictResponse(predicted_units=round(units, 1), forecast_bucket=bucket, confidence=confidence)

    PREDICTION_LOG.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "latency_ms": round(latency_ms, 2),
        "input": req.model_dump(),
        "result": result.model_dump(),
    })
    if len(PREDICTION_LOG) > LOG_CAP:
        del PREDICTION_LOG[: len(PREDICTION_LOG) - LOG_CAP]
    return result


@app.get("/history")
async def history(limit: int = 50):
    n = max(0, min(limit, len(PREDICTION_LOG)))
    return {"count": n, "total": len(PREDICTION_LOG), "entries": list(reversed(PREDICTION_LOG[-n:]))}


@app.get("/stats")
async def stats():
    total = len(PREDICTION_LOG)
    empty = {
        "total_forecasts": 0,
        "avg_demand": 0,
        "bucket_distribution": {k: 0 for k in BUCKET_KEYS},
        "max_forecast": 0,
        "avg_latency_ms": 0,
    }
    if total == 0:
        return empty
    demands = [e["result"]["predicted_units"] for e in PREDICTION_LOG]
    buckets = {k: 0 for k in BUCKET_KEYS}
    for e in PREDICTION_LOG:
        buckets[e["result"]["forecast_bucket"]] += 1
    return {
        "total_forecasts": total,
        "avg_demand": round(sum(demands) / total, 2),
        "bucket_distribution": buckets,
        "max_forecast": max(demands),
        "avg_latency_ms": round(sum(e["latency_ms"] for e in PREDICTION_LOG) / total, 2),
    }


@app.get("/model-info")
async def model_info():
    if MODEL is None:
        return {"model_loaded": False}
    fi = [
        {"feature": f, "importance": round(float(i), 4)}
        for f, i in zip(FEATURE_COLS, MODEL.feature_importances_)
    ]
    fi.sort(key=lambda x: x["importance"], reverse=True)
    return {
        "model_loaded": True,
        "model_name": type(MODEL).__name__,
        "n_estimators": MODEL.n_estimators,
        "max_depth": MODEL.max_depth,
        "n_features": len(FEATURE_COLS),
        "r2": MODEL_METRICS["r2"],
        "mae": MODEL_METRICS["mae"],
        "feature_importance": fi,
        "data_source": "PBS (Australian Pharmaceutical Benefits Scheme)",
        "n_series": len(DRUG_IDS),
        "concession_types": CONCESSION_TYPES,
    }


@app.get("/")
async def serve_ui():
    return FileResponse(UI_DIR / "index.html")


if UI_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(UI_DIR)), name="ui")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8103)