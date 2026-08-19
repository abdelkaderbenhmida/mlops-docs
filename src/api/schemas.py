"""Pydantic request/response schemas for the demand forecasting API.

Fields match the training columns exactly for train/inference parity.
Pydantic rejects malformed payloads with a 422 and clear error message.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class DemandPredictionRequest(BaseModel):
    store_id: int = Field(alias="store_id", ge=1, le=100)
    sku_id: int = Field(alias="sku_id", ge=1, le=200)
    day_of_week: int = Field(alias="day_of_week", ge=0, le=6)
    month: int = Field(alias="month", ge=1, le=12)
    is_holiday: int = Field(alias="is_holiday", ge=0, le=1)
    price: float = Field(alias="price", ge=0.0, le=500.0)
    promotion: int = Field(alias="promotion", ge=0, le=1)
    temperature: float = Field(alias="temperature", ge=-50.0, le=150.0)
    inventory_level: int = Field(alias="inventory_level", ge=0, le=10000)
    competitor_price: float = Field(alias="competitor_price", ge=0.0, le=500.0)
    store_traffic: int = Field(alias="store_traffic", ge=0, le=50000)

    model_config = {"populate_by_name": True}

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame([self.model_dump()])


def _demand_bucket(units: int) -> Literal["low", "medium", "high", "very_high"]:
    if units <= 15:
        return "low"
    elif units <= 35:
        return "medium"
    elif units <= 60:
        return "high"
    else:
        return "very_high"


class PredictionResponse(BaseModel):
    predicted_units: int = Field(description="Predicted units_sold")
    demand_bucket: str = Field(description="Demand bucket: low, medium, high, very_high")
    model_name: str
    model_version: str


PredictionRequest = DemandPredictionRequest | list[DemandPredictionRequest]
PredictionResult = PredictionResponse | list[PredictionResponse]


class HealthResponse(BaseModel):
    status: str
    model_name: str | None = None
    model_version: str | None = None


class ModelInfoResponse(BaseModel):
    model_name: str
    model_version: str
    run_id: str | None = None
    production_metrics: dict | None = None
