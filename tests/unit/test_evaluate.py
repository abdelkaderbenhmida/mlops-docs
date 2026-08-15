"""Tests for src.models.evaluate module."""

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
    """Test model evaluation and validation gates."""

    def _create_mock_model(self, f1=0.8, accuracy=0.85, roc_auc=0.9):
        """Create a mock model with predictable predictions."""
        model = MagicMock()
        # For binary classification, predict_proba returns [prob_class_0, prob_class_1]
        # We'll make it so that class 1 (churn) probability is predictable
        def predict_proba(X):
            n = len(X)
            # Return probabilities that yield the desired metrics
            prob_class_1 = np.full(n, 0.7)  # High probability for class 1
            return np.column_stack([1 - prob_class_1, prob_class_1])
        
        def predict(X):
            n = len(X)
            # Return mostly 1s (churn)
            return np.ones(n, dtype=int)
        
        model.predict_proba = predict_proba
        model.predict = predict
        return model

    def _create_test_data(self, n=100):
        """Create test features and labels."""
        np.random.seed(42)
        features = pd.DataFrame({
            col: np.random.randn(n) for col in FEATURE_ORDER
        })
        labels = pd.Series(np.random.choice([0, 1], n, p=[0.7, 0.3]), name=TARGET_FEATURE)
        return features, labels

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_model_returns_metrics(self, mock_load_test, mock_resolve_model):
        """evaluate_model should return all expected metrics."""
        features, labels = self._create_test_data(50)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model()
        
        from src.models.evaluate import evaluate_model as em
        model = self._create_mock_model()
        metrics = em(model, features, labels)
        
        assert "f1" in metrics
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "roc_auc" in metrics
        assert "n_samples" in metrics
        assert metrics["n_samples"] == 50
        assert 0 <= metrics["f1"] <= 1
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["roc_auc"] <= 1

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_returns_report_with_gates(self, mock_load_test, mock_resolve_model):
        """evaluate should return a report with gates_passed."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model(f1=0.9, accuracy=0.9, roc_auc=0.95)
        
        report = evaluate(thresholds={"min_f1": 0.5, "min_accuracy": 0.7, "min_roc_auc": 0.7})
        
        assert "metrics" in report
        assert "thresholds" in report
        assert "gates" in report
        assert "gates_passed" in report
        assert isinstance(report["gates_passed"], bool)
        assert report["thresholds"]["min_f1"] == 0.5

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_gates_pass_when_metrics_above_threshold(self, mock_load_test, mock_resolve_model):
        """gates_passed should be True when all metrics exceed thresholds."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model(f1=0.9, accuracy=0.9, roc_auc=0.95)
        
        report = evaluate(thresholds={"min_f1": 0.5, "min_accuracy": 0.7, "min_roc_auc": 0.7})
        
        assert report["gates_passed"] is True
        for gate_name, gate_info in report["gates"].items():
            metric_name = gate_info["metric"]
            threshold = gate_info["value"]
            assert report["metrics"][metric_name] >= threshold

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_gates_fail_when_metrics_below_threshold(self, mock_load_test, mock_resolve_model):
        """gates_passed should be False when any metric is below threshold."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        # Model with low performance
        mock_resolve_model.return_value = self._create_mock_model(f1=0.2, accuracy=0.5, roc_auc=0.55)
        
        report = evaluate(thresholds={"min_f1": 0.5, "min_accuracy": 0.7, "min_roc_auc": 0.7})
        
        assert report["gates_passed"] is False
        # At least one gate should fail
        failed_gates = [
            name for name, info in report["gates"].items()
            if report["metrics"][info["metric"]] < info["value"]
        ]
        assert len(failed_gates) > 0

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_uses_default_thresholds(self, mock_load_test, mock_resolve_model):
        """evaluate should use DEFAULT_THRESHOLDS when none provided."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model(f1=0.9, accuracy=0.9, roc_auc=0.95)
        
        report = evaluate()
        
        assert report["thresholds"]["min_f1"] == DEFAULT_THRESHOLDS["min_f1"]
        assert report["thresholds"]["min_accuracy"] == DEFAULT_THRESHOLDS["min_accuracy"]
        assert report["thresholds"]["min_roc_auc"] == DEFAULT_THRESHOLDS["min_roc_auc"]

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_merges_custom_thresholds_with_defaults(self, mock_load_test, mock_resolve_model):
        """Custom thresholds should override defaults, others kept."""
        features, labels = self._create_test_data(100)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model()
        
        report = evaluate(thresholds={"min_f1": 0.99})  # Only override f1
        
        assert report["thresholds"]["min_f1"] == 0.99
        assert report["thresholds"]["min_accuracy"] == DEFAULT_THRESHOLDS["min_accuracy"]
        assert report["thresholds"]["min_roc_auc"] == DEFAULT_THRESHOLDS["min_roc_auc"]

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_writes_report_file(self, mock_load_test, mock_resolve_model, tmp_path):
        """evaluate should write report to LATEST_REPORT."""
        features, labels = self._create_test_data(50)
        mock_load_test.return_value = (features, labels)
        mock_resolve_model.return_value = self._create_mock_model()
        
        # Patch the report path
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
        # Create reference.csv with test data
        reference_dir = tmp_path / "data" / "monitoring"
        reference_dir.mkdir(parents=True)
        
        features = pd.DataFrame({
            col: np.random.randn(50) for col in FEATURE_ORDER
        })
        features["label"] = np.random.choice([0, 1], 50)
        features["prediction"] = np.random.uniform(0, 1, 50)
        
        ref_path = reference_dir / "reference.csv"
        features.to_csv(ref_path, index=False)
        
        # Mock PROJECT_ROOT to point to tmp_path
        with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):
            X_test, y_test = _load_test_set(tmp_path / "features.parquet")
        
        assert len(X_test) == 50
        assert len(y_test) == 50
        assert list(X_test.columns) == FEATURE_ORDER

    def test_load_test_set_fallback_to_parquet(self, tmp_path):
        """_load_test_set should fall back to parquet when no reference.csv."""
        # Create parquet file
        features_dir = tmp_path / "data" / "features"
        features_dir.mkdir(parents=True)
        
        features = pd.DataFrame({
            col: np.random.randn(100) for col in FEATURE_ORDER
        })
        features[TARGET_FEATURE] = np.random.choice([0, 1], 100)
        
        parquet_path = features_dir / "features.parquet"
        features.to_parquet(parquet_path, index=False)
        
        with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):
            with patch("src.models.evaluate.DEFAULT_DATA", parquet_path):
                X_test, y_test = _load_test_set(parquet_path)
        
        assert len(X_test) == 100
        assert len(y_test) == 100

    def test_load_test_set_samples_large_dataset(self, tmp_path):
        """_load_test_set should sample large datasets to 5000 rows."""
        features_dir = tmp_path / "data" / "features"
        features_dir.mkdir(parents=True)
        
        features = pd.DataFrame({
            col: np.random.randn(10000) for col in FEATURE_ORDER
        })
        features[TARGET_FEATURE] = np.random.choice([0, 1], 10000)
        
        parquet_path = features_dir / "features.parquet"
        features.to_parquet(parquet_path, index=False)
        
        with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):
            with patch("src.models.evaluate.DEFAULT_DATA", parquet_path):
                X_test, y_test = _load_test_set(parquet_path)
        
        assert len(X_test) == 5000
        assert len(y_test) == 5000

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_model_with_perfect_predictions(self, mock_load_test, mock_resolve_model):
        """evaluate_model should handle perfect predictions (f1=1.0)."""
        features, labels = self._create_test_data(50)
        mock_load_test.return_value = (features, labels)
        
        # Perfect model - predicts exactly the labels
        model = MagicMock()
        model.predict.return_value = labels.values
        model.predict_proba.return_value = np.column_stack([1 - labels.values, labels.values])
        mock_resolve_model.return_value = model
        
        metrics = evaluate_model(model, features, labels)
        
        assert metrics["f1"] == 1.0
        assert metrics["accuracy"] == 1.0
        assert metrics["precision"] == 1.0
        assert metrics["recall"] == 1.0

    @patch("src.models.evaluate._resolve_model")
    @patch("src.models.evaluate._load_test_set")
    def test_evaluate_model_with_worst_predictions(self, mock_load_test, mock_resolve_model):
        """evaluate_model should handle worst predictions (f1=0.0)."""
        features, labels = self._create_test_data(50)
        mock_load_test.return_value = (features, labels)
        
        # Worst model - predicts opposite of labels
        model = MagicMock()
        model.predict.return_value = 1 - labels.values
        model.predict_proba.return_value = np.column_stack([labels.values, 1 - labels.values])
        mock_resolve_model.return_value = model
        
        metrics = evaluate_model(model, features, labels)
        
        assert metrics["f1"] == 0.0
        assert metrics["accuracy"] == 0.0


class TestEvaluateIntegration:
    """Integration-style tests for evaluate.py with real models (skipped by default)."""

    @pytest.mark.skip(reason="Requires trained model and full environment")
    def test_evaluate_with_real_model(self):
        """Test evaluate with a real trained model from MLflow."""
        pytest.skip("Integration test - requires MLflow server and trained model")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])