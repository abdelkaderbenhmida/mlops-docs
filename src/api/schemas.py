"""Pydantic request/response schemas for the inference API.

Field aliases match the training columns exactly so the feature transformer
can be applied without training/serving skew. Pydantic rejects malformed
payloads with a 422 and a clear error message.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

YesNo = Literal["Yes", "No"]
NoService = Literal["Yes", "No", "No phone service"]
NoInternet = Literal["Yes", "No", "No internet service"]


class ChurnPredictionRequest(BaseModel):
    gender: Literal["Male", "Female"] = Field(alias="Gender")
    senior_citizen: Literal[0, 1] = Field(alias="SeniorCitizen")
    partner: YesNo = Field(alias="Partner")
    dependents: YesNo = Field(alias="Dependents")
    tenure: int = Field(alias="Tenure", ge=0, le=120)
    phone_service: YesNo = Field(alias="PhoneService")
    multiple_lines: NoService = Field(alias="MultipleLines")
    internet_service: Literal["DSL", "Fiber optic", "No"] = Field(alias="InternetService")
    online_security: NoInternet = Field(alias="OnlineSecurity")
    online_backup: NoInternet = Field(alias="OnlineBackup")
    device_protection: NoInternet = Field(alias="DeviceProtection")
    tech_support: NoInternet = Field(alias="TechSupport")
    streaming_tv: NoInternet = Field(alias="StreamingTV")
    streaming_movies: NoInternet = Field(alias="StreamingMovies")
    contract: Literal["Month-to-month", "One year", "Two year"] = Field(alias="Contract")
    paperless_billing: YesNo = Field(alias="PaperlessBilling")
    payment_method: Literal[
        "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
    ] = Field(alias="PaymentMethod")
    monthly_charges: float = Field(alias="MonthlyCharges", ge=0, le=1000)
    total_charges: float = Field(alias="TotalCharges", ge=0, le=100000)

    model_config = {"populate_by_name": True}

    def to_dataframe(self):
        import pandas as pd

        return pd.DataFrame([self.model_dump(by_alias=True)])


class PredictionResponse(BaseModel):
    prediction: int = Field(description="1 if the customer is predicted to churn, else 0")
    probability: float = Field(ge=0.0, le=1.0, description="Predicted churn probability")
    model_name: str
    model_version: str


PredictionRequest = ChurnPredictionRequest | list[ChurnPredictionRequest]
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
