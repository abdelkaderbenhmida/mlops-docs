"""Tests for FastAPI inference API."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api.main import app
from src.api.schemas import ChurnPredictionRequest, PredictionResponse


client = TestClient(app)


def _valid_payload() -> dict:
    return {
        "Gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "Tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "Yes",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "No",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 50.0,
        "TotalCharges": 600.0,
    }


class TestHealthEndpoint:
    """Test /health endpoint."""

    def test_health_returns_200(self):
        """GET /health should return 200 with status ok or degraded."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ("ok", "degraded")


class TestPredictEndpoint:
    """Test /predict endpoint."""

    @patch("src.api.main.loader.get_bundle")
    def test_predict_valid_payload_returns_prediction_and_probability(self, mock_get_bundle):
        """POST /predict with valid payload returns prediction (0/1) and probability [0,1]."""
        mock_bundle = MagicMock()
        mock_bundle.model_name = "churn_model"
        mock_bundle.version = "1"
        mock_bundle.predict_proba.return_value = [[0.3, 0.7]]  # [prob_class_0, prob_class_1]
        mock_get_bundle.return_value = mock_bundle

        response = client.post("/predict", json=_valid_payload())
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "probability" in data
        assert data["prediction"] in (0, 1)
        assert 0.0 <= data["probability"] <= 1.0
        assert data["model_name"] == "churn_model"
        assert data["model_version"] == "1"

    @patch("src.api.main.loader.get_bundle")
    def test_predict_batch_returns_list(self, mock_get_bundle):
        """POST /predict with list payload returns list of predictions."""
        mock_bundle = MagicMock()
        mock_bundle.model_name = "churn_model"
        mock_bundle.version = "1"
        mock_bundle.predict_proba.return_value = [[0.3, 0.7], [0.8, 0.2]]
        mock_get_bundle.return_value = mock_bundle

        payload = [_valid_payload(), _valid_payload()]
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        for item in data:
            assert "prediction" in item
            assert "probability" in item
            assert item["prediction"] in (0, 1)
            assert 0.0 <= item["probability"] <= 1.0

    def test_predict_invalid_payload_returns_422(self):
        """POST /predict with invalid payload returns 422."""
        invalid_payload = _valid_payload()
        invalid_payload["Gender"] = "Invalid"  # not in Literal
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 422

    def test_predict_empty_batch_returns_422(self):
        """POST /predict with empty list returns 422."""
        response = client.post("/predict", json=[])
        assert response.status_code == 422

    def test_predict_missing_fields_returns_422(self):
        """POST /predict with missing required fields returns 422."""
        response = client.post("/predict", json={})
        assert response.status_code == 422


class TestMetricsEndpoint:
    """Test /metrics endpoint."""

    def test_metrics_exposes_prometheus_metrics(self):
        """GET /metrics should return Prometheus metrics text."""
        response = client.get("/metrics")
        assert response.status_code == 200
        content = response.text
        # Check for standard prometheus-fastapi-instrumentator metrics
        assert "http_requests_total" in content or "http_request_duration_seconds" in content
        # Check for our custom metrics
        assert "model_prediction_value" in content or "predictions_total" in content


class TestModelInfoEndpoint:
    """Test /model-info endpoint."""

    @patch("src.api.main.loader.get_bundle")
    def test_model_info_returns_metadata(self, mock_get_bundle):
        """GET /model-info should return model metadata."""
        mock_bundle = MagicMock()
        mock_bundle.model_name = "churn_model"
        mock_bundle.version = "3"
        mock_bundle.run_id = "abc123"
        mock_get_bundle.return_value = mock_bundle

        response = client.get("/model-info")
        assert response.status_code == 200
        data = response.json()
        assert data["model_name"] == "churn_model"
        assert data["model_version"] == "3"
        assert data["run_id"] == "abc123"


class TestSchemas:
    """Test Pydantic request/response schemas."""

    def test_churn_prediction_request_valid(self):
        """Valid payload should create ChurnPredictionRequest."""
        payload = _valid_payload()
        request = ChurnPredictionRequest(**payload)
        df = request.to_dataframe()
        assert len(df) == 1
        assert list(df.columns) == list(payload.keys())

    def test_churn_prediction_request_invalid_gender(self):
        """Invalid gender should raise validation error."""
        payload = _valid_payload()
        payload["Gender"] = "Invalid"
        with pytest.raises(Exception):
            ChurnPredictionRequest(**payload)

    def test_churn_prediction_request_invalid_tenure(self):
        """Negative tenure should raise validation error."""
        payload = _valid_payload()
        payload["Tenure"] = -5
        with pytest.raises(Exception):
            ChurnPredictionRequest(**payload)

    def test_churn_prediction_request_invalid_monthly_charges(self):
        """Negative monthly charges should raise validation error."""
        payload = _valid_payload()
        payload["MonthlyCharges"] = -10.0
        with pytest.raises(Exception):
            ChurnPredictionRequest(**payload)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])