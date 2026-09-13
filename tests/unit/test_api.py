# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Tests for FastAPI demand forecasting inference API."""

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
from src.api.schemas import DemandPredictionRequest, PredictionResponse


client = TestClient(app)


def _valid_payload() -> dict:
    return {
        "store_id": 1,
        "sku_id": 1,
        "day_of_week": 0,
        "month": 12,
        "is_holiday": 1,
        "price": 29.99,
        "promotion": 1,
        "temperature": 35.0,
        "inventory_level": 200,
        "competitor_price": 32.99,
        "store_traffic": 500,
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
    def test_predict_valid_payload_returns_prediction(self, mock_get_bundle):
        """POST /predict with valid payload returns predicted units and bucket."""
        mock_bundle = MagicMock()
        mock_bundle.model_name = "demand_model"
        mock_bundle.version = "1"
        mock_bundle.predict.return_value = [42.5]
        mock_get_bundle.return_value = mock_bundle

        response = client.post("/predict", json=_valid_payload())
        assert response.status_code == 200
        data = response.json()
        assert "predicted_units" in data
        assert "demand_bucket" in data
        assert isinstance(data["predicted_units"], int)
        assert data["demand_bucket"] in ("low", "medium", "high", "very_high")
        assert data["model_name"] == "demand_model"
        assert data["model_version"] == "1"

    @patch("src.api.main.loader.get_bundle")
    def test_predict_batch_returns_list(self, mock_get_bundle):
        """POST /predict with list payload returns list of predictions."""
        mock_bundle = MagicMock()
        mock_bundle.model_name = "demand_model"
        mock_bundle.version = "1"
        mock_bundle.predict.return_value = [42.5, 15.3]
        mock_get_bundle.return_value = mock_bundle

        payload = [_valid_payload(), _valid_payload()]
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        for item in data:
            assert "predicted_units" in item
            assert "demand_bucket" in item

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
        assert "http_requests_total" in content or "http_request_duration_seconds" in content


class TestModelInfoEndpoint:
    """Test /model-info endpoint."""

    @patch("src.api.main.loader.get_bundle")
    def test_model_info_returns_metadata(self, mock_get_bundle):
        """GET /model-info should return model metadata."""
        mock_bundle = MagicMock()
        mock_bundle.model_name = "demand_model"
        mock_bundle.version = "3"
        mock_bundle.run_id = "abc123"
        mock_get_bundle.return_value = mock_bundle

        response = client.get("/model-info")
        assert response.status_code == 200
        data = response.json()
        assert data["model_name"] == "demand_model"
        assert data["model_version"] == "3"
        assert data["run_id"] == "abc123"


class TestSchemas:
    """Test Pydantic request/response schemas."""

    def test_demand_prediction_request_valid(self):
        """Valid payload should create DemandPredictionRequest."""
        payload = _valid_payload()
        request = DemandPredictionRequest(**payload)
        df = request.to_dataframe()
        assert len(df) == 1
        assert list(df.columns) == list(payload.keys())

    def test_demand_prediction_request_invalid_store_id(self):
        """Invalid store_id should raise validation error."""
        payload = _valid_payload()
        payload["store_id"] = 0
        with pytest.raises(Exception):
            DemandPredictionRequest(**payload)

    def test_demand_prediction_request_invalid_price(self):
        """Negative price should raise validation error."""
        payload = _valid_payload()
        payload["price"] = -10.0
        with pytest.raises(Exception):
            DemandPredictionRequest(**payload)

    def test_demand_prediction_request_invalid_temperature(self):
        """Temperature out of range should raise validation error."""
        payload = _valid_payload()
        payload["temperature"] = 200.0
        with pytest.raises(Exception):
            DemandPredictionRequest(**payload)


class TestDemandBuckets:
    """Test demand bucket classification."""

    def test_low_bucket(self):
        from src.api.schemas import _demand_bucket
        assert _demand_bucket(10) == "low"
        assert _demand_bucket(15) == "low"

    def test_medium_bucket(self):
        from src.api.schemas import _demand_bucket
        assert _demand_bucket(20) == "medium"
        assert _demand_bucket(35) == "medium"

    def test_high_bucket(self):
        from src.api.schemas import _demand_bucket
        assert _demand_bucket(40) == "high"
        assert _demand_bucket(60) == "high"

    def test_very_high_bucket(self):
        from src.api.schemas import _demand_bucket
        assert _demand_bucket(65) == "very_high"
        assert _demand_bucket(100) == "very_high"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
