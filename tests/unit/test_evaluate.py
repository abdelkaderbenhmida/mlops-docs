# TODO: high - Add quality gate with thresholds
# TODO: medium - Implement comparison vs current production model
# TODO: low - Add metrics export for Evidence Pack
"""Tests for src.models.evaluate module (demand forecasting)."""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.evaluate import evaluate, evaluate_model, DEFAULT_THRESHOLDS, _load_test_set
from src.features.build_features import FEATURE_ORDER, TARGET_FEATURE


class TestEvaluate:
    """Test model evaluation and validation gates for demand forecasting."""

    def _create_mock_model(self, perfect=False):
        """Create a mock model with predictable predictions."""
        model = MagicMock()
        if perfect:
            def predict(X):
                np.random.seed(42)
                return np.random.uniform(20, 60, size=len(X))
            model.predict = predict
        else:
            def predict(X):
                return np.full(len(X), 30.0)
            model.predict = predict
        return model

    def _create_test_data(self, n=100):
        """Create test features and labels."""
        np.random.seed(42)
        features = pd.DataFrame({
            col: np.random.randn(n) for col in FEATURE_ORDER
        })
        labels = pd.Series(np.random.uniform(10, 80, n), name=TARGET_FEATURE)
        return features, labels

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_model_returns_metrics(self, mock_load_test, mock_resolve_model):
        """evaluate_model should return all expected metrics."""
        features, labels = self._create_test_data(50)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model()

        model = self._create_mock_model()
        metrics = evaluate_model(model, features, labels)

        assert "rmse" in metrics
        assert "mae" in metrics
        assert "r2" in metrics
        assert "mape" in metrics
        assert "n_samples" in metrics
        assert metrics["n_samples"] == 50
        assert metrics["rmse"] >= 0
        assert metrics["mae"] >= 0
        assert metrics["r2"] <= 1.0
        assert metrics["mape"] >= 0

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_returns_report_with_gates(self, mock_load_test, mock_resolve_model, tmp_path):
        """evaluate should return a report with gates_passed."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model(perfect=True)

        with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_report.json"):
            with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):
                report = evaluate(thresholds={"min_r2": 0.5, "max_mape": 30.0})

        assert "metrics" in report
        assert "thresholds" in report
        assert "gates" in report
        assert "gates_passed" in report
        assert isinstance(report["gates_passed"], bool)

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_uses_default_thresholds(self, mock_load_test, mock_resolve_model, tmp_path):
        """evaluate should use DEFAULT_THRESHOLDS when none provided."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model()

        with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_report.json"):
            with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):
                report = evaluate()

        assert report["thresholds"]["min_r2"] == DEFAULT_THRESHOLDS["min_r2"]
        assert report["thresholds"]["max_mape"] == DEFAULT_THRESHOLDS["max_mape"]

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_writes_report_file(self, mock_load_test, mock_resolve_model, tmp_path):
        """evaluate should write report to LATEST_REPORT."""
        features, labels = self._create_test_data(50)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model()

        with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_report.json"):
            with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):
                report = evaluate()

        report_file = tmp_path / "latest_report.json"
        assert report_file.exists()

        with report_file.open() as f:
            saved_report = json.load(f)
        assert saved_report["gates_passed"] == report["gates_passed"]

    def test_load_test_set_prefers_reference_csv(self, tmp_path, monkeypatch):
        """_load_test_set should prefer reference.csv when available."""
        reference_dir = tmp_path / "data" / "monitoring"
        reference_dir.mkdir(parents=True)

        features = pd.DataFrame({
            col: np.random.randn(50) for col in FEATURE_ORDER
        })
        features[TARGET_FEATURE] = np.random.uniform(10, 80, 50)
        features["prediction"] = np.random.uniform(10, 80, 50)

        ref_path = reference_dir / "reference.csv"
        features.to_csv(ref_path, index=False)

        with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):
            X_test, y_test = _load_test_set(tmp_path / "features.parquet")

        assert len(X_test) == 50
        assert len(y_test) == 50
        assert list(X_test.columns) == FEATURE_ORDER

    def test_load_test_set_fallback_to_parquet(self, tmp_path):
        """_load_test_set should fall back to parquet when no reference.csv."""
        features_dir = tmp_path / "data" / "features"
        features_dir.mkdir(parents=True)

        features = pd.DataFrame({
            col: np.random.randn(100) for col in FEATURE_ORDER
        })
        features[TARGET_FEATURE] = np.random.uniform(10, 80, 100)

        parquet_path = features_dir / "features.parquet"
        features.to_parquet(parquet_path, index=False)

        with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):
            with patch("src.models.evaluate.DEFAULT_DATA", parquet_path):
                X_test, y_test = _load_test_set(parquet_path)

        assert len(X_test) == 100
        assert len(y_test) == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
