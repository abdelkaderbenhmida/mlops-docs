"""End-to-end integration test for the MLOps pipeline.

Tests the full pipeline: preprocessing -> features -> training -> evaluation -> promotion
using SQLite MLflow backend and monkeypatched environment (no external servers needed).
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import all pipeline modules
from src.data.preprocessing import preprocess
from src.features.build_features import build_features, FeatureTransformer
from src.models.train import train_model
from src.models.evaluate import evaluate
from src.models.promote import promote_candidate, current_production


class TestPipelineEndToEnd:
    """End-to-end pipeline test with minimal data and fast model."""

    @pytest.fixture(autouse=True)
    def setup_env(self, tmp_path, monkeypatch):
        """Set up isolated environment for each test."""
        # Use temporary directories
        self.tmp_path = tmp_path
        self.data_dir = tmp_path / "data"
        self.data_dir.mkdir()
        self.models_dir = tmp_path / "models"
        self.models_dir.mkdir()
        self.mlruns_dir = tmp_path / "mlruns"
        self.mlruns_dir.mkdir()

        # Monkeypatch environment
        monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{self.mlruns_dir}/mlflow.db")
        monkeypatch.setenv("MLFLOW_MODEL_NAME", "test_churn_model")
        monkeypatch.setenv("DRIFT_THRESHOLD", "0.3")
        monkeypatch.setenv("DRIFT_REFERENCE", str(self.data_dir / "monitoring" / "reference.csv"))
        monkeypatch.setenv("DRIFT_CURRENT", str(self.data_dir / "monitoring" / "current.csv"))

        # Create minimal sample data
        self.sample_csv = self.data_dir / "raw" / "sample.csv"
        self.sample_csv.parent.mkdir(parents=True)
        self._create_sample_data()

    def _create_sample_data(self):
        """Create a small sample dataset for fast testing."""
        df = pd.DataFrame({
            "CustomerID": [f"C{i:04d}" for i in range(100)],
            "Gender": ["Male", "Female"] * 50,
            "SeniorCitizen": [0, 1] * 50,
            "Partner": ["Yes", "No"] * 50,
            "Dependents": ["No", "Yes"] * 50,
            "Tenure": list(range(1, 101)),
            "PhoneService": ["Yes"] * 100,
            "MultipleLines": ["No", "Yes", "No phone service"] * 33 + ["No"],
            "InternetService": ["DSL", "Fiber optic", "No"] * 33 + ["DSL"],
            "OnlineSecurity": ["Yes", "No", "No internet service"] * 33 + ["Yes"],
            "OnlineBackup": ["Yes", "No", "No internet service"] * 33 + ["No"],
            "DeviceProtection": ["Yes", "No", "No internet service"] * 33 + ["Yes"],
            "TechSupport": ["Yes", "No", "No internet service"] * 33 + ["No"],
            "StreamingTV": ["Yes", "No", "No internet service"] * 33 + ["Yes"],
            "StreamingMovies": ["Yes", "No", "No internet service"] * 33 + ["No"],
            "Contract": ["Month-to-month", "One year", "Two year"] * 33 + ["Month-to-month"],
            "PaperlessBilling": ["Yes", "No"] * 50,
            "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"] * 25,
            "MonthlyCharges": [float(20 + i * 0.5) for i in range(100)],
            "TotalCharges": [float(100 + i * 10) for i in range(100)],
            "Churn": ["No", "Yes"] * 50,
        })
        df.to_csv(self.sample_csv, index=False)

    def _override_default_paths(self, monkeypatch):
        """Override default paths in modules to use temp directories."""
        # Preprocessing
        monkeypatch.setattr("src.data.preprocessing.DROP_COLUMNS", ["CustomerID"])
        monkeypatch.setattr("src.data.preprocessing.NUMERIC_COLUMNS", [
            "Tenure", "MonthlyCharges", "TotalCharges"
        ])
        monkeypatch.setattr("src.data.preprocessing.CATEGORICAL_COLUMNS", [
            "Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
            "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
            "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
            "Contract", "PaperlessBilling", "PaymentMethod"
        ])
        monkeypatch.setattr("src.data.preprocessing.TARGET_COLUMN", "Churn")

        # Features
        from src.features.build_features import (
            NUMERIC_FEATURES, CATEGORICAL_FEATURES, ENGINEERED_FEATURES,
            FEATURE_ORDER, TARGET_FEATURE, TARGET_COLUMN, SERVICE_COLUMNS
        )
        monkeypatch.setattr("src.features.build_features.NUMERIC_FEATURES", [
            "Tenure", "MonthlyCharges", "TotalCharges"
        ])
        monkeypatch.setattr("src.features.build_features.CATEGORICAL_FEATURES", [
            "Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
            "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
            "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
            "Contract", "PaperlessBilling", "PaymentMethod"
        ])
        monkeypatch.setattr("src.features.build_features.ENGINEERED_FEATURES", [
            "charges_per_tenure", "tenure_years", "num_services"
        ])
        monkeypatch.setattr("src.features.build_features.FEATURE_ORDER", [
            "Tenure", "MonthlyCharges", "TotalCharges",
            "Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
            "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
            "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
            "Contract", "PaperlessBilling", "PaymentMethod",
            "charges_per_tenure", "tenure_years", "num_services"
        ])
        monkeypatch.setattr("src.features.build_features.TARGET_FEATURE", "target")
        monkeypatch.setattr("src.features.build_features.TARGET_COLUMN", "Churn")
        monkeypatch.setattr("src.features.build_features.SERVICE_COLUMNS", [
            "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
            "StreamingTV", "StreamingMovies"
        ])

        # Train
        monkeypatch.setattr("src.models.train.DEFAULT_DATA", self.data_dir / "features" / "features.parquet")
        monkeypatch.setattr("src.models.train.DEFAULT_CONFIG", self.data_dir / "features" / "features_config.json")
        monkeypatch.setattr("src.models.train.DEFAULT_MODEL_OUTPUT", self.models_dir / "model.pkl")
        monkeypatch.setattr("src.models.train.DEFAULT_REFERENCE", self.data_dir / "monitoring" / "reference.csv")
        monkeypatch.setattr("src.models.train.MODEL_NAME", "test_churn_model")

        # Evaluate
        monkeypatch.setattr("src.models.evaluate.DEFAULT_DATA", self.data_dir / "features" / "features.parquet")
        monkeypatch.setattr("src.models.evaluate.DEFAULT_CONFIG", self.data_dir / "features" / "features_config.json")
        monkeypatch.setattr("src.models.evaluate.DEFAULT_LOCAL_MODEL", self.models_dir / "model.pkl")
        monkeypatch.setattr("src.models.evaluate.EVALUATION_DIR", self.models_dir / "evaluation")
        monkeypatch.setattr("src.models.evaluate.LATEST_REPORT", self.models_dir / "evaluation" / "latest_report.json")

        # Promote
        monkeypatch.setattr("src.models.promote.LATEST_REPORT", self.models_dir / "evaluation" / "latest_report.json")
        monkeypatch.setattr("src.models.promote.PRODUCTION_REPORT", self.models_dir / "evaluation" / "production_report.json")

    def test_full_pipeline(self, monkeypatch):
        """Run the complete pipeline end-to-end."""
        self._override_default_paths(monkeypatch)

        # Step 1: Preprocessing
        processed_path = self.data_dir / "processed" / "clean.csv"
        processed_path.parent.mkdir(parents=True)
        processed_df = preprocess(self.sample_csv, processed_path)
        assert processed_path.exists()
        assert len(processed_df) > 0
        assert "CustomerID" not in processed_df.columns
        assert "Churn" in processed_df.columns

        # Step 2: Feature Engineering
        features_path = self.data_dir / "features" / "features.parquet"
        config_path = self.data_dir / "features" / "features_config.json"
        features_path.parent.mkdir(parents=True)
        features_df = build_features(processed_path, features_path, config_path)
        assert features_path.exists()
        assert config_path.exists()
        assert len(features_df) == len(processed_df)
        assert "target" in features_df.columns

        # Step 3: Training (with tiny model for speed)
        train_params = {
            "n_estimators": 10,  # Very small for fast testing
            "max_depth": 3,
            "min_samples_leaf": 2,
            "max_features": "sqrt",
            "class_weight": "balanced",
            "random_state": 42,
        }
        train_result = train_model(
            data_path=features_path,
            config_path=config_path,
            model_output=self.models_dir / "model.pkl",
            model_name="test_churn_model",
            params=train_params,
        )
        assert train_result["run_id"] is not None
        assert (self.models_dir / "model.pkl").exists()
        assert (self.data_dir / "monitoring" / "reference.csv").exists()

        # Step 4: Evaluation
        eval_report = evaluate(
            data_path=features_path,
            model_uri=None,
            run_id=train_result["run_id"],
        )
        assert eval_report["gates_passed"] is not None
        assert "metrics" in eval_report
        assert (self.models_dir / "evaluation" / "latest_report.json").exists()

        # Step 5: Promotion
        # First, need to transition model to Staging (train does this)
        # Then promote
        # Note: In this test, the model is already in Staging from train.py
        # But we need to check if it's there
        production_report = promote_candidate(model_name="test_churn_model", force=True)
        assert production_report["model_name"] == "test_churn_model"
        assert production_report["version"] >= 1
        assert (self.models_dir / "evaluation" / "production_report.json").exists()

        # Verify production model is accessible
        current = current_production(model_name="test_churn_model")
        assert current is not None
        assert current["version"] == production_report["version"]

    def test_pipeline_with_evaluation_failure(self, monkeypatch):
        """Test pipeline when evaluation gates fail."""
        self._override_default_paths(monkeypatch)

        # Run through training
        processed_path = self.data_dir / "processed" / "clean.csv"
        processed_path.parent.mkdir(parents=True)
        processed_df = preprocess(self.sample_csv, processed_path)

        features_path = self.data_dir / "features" / "features.parquet"
        config_path = self.data_dir / "features" / "features_config.json"
        features_path.parent.mkdir(parents=True)
        features_df = build_features(processed_path, features_path, config_path)

        train_params = {
            "n_estimators": 10,
            "max_depth": 3,
            "min_samples_leaf": 2,
            "max_features": "sqrt",
            "class_weight": "balanced",
            "random_state": 42,
        }
        train_result = train_model(
            data_path=features_path,
            config_path=config_path,
            model_output=self.models_dir / "model.pkl",
            model_name="test_churn_model",
            params=train_params,
        )

        # Evaluate with impossible thresholds
        eval_report = evaluate(
            data_path=features_path,
            run_id=train_result["run_id"],
            thresholds={"min_f1": 0.99, "min_accuracy": 0.99, "min_roc_auc": 0.99},
        )
        assert eval_report["gates_passed"] is False

        # Promotion should fail without --force
        with pytest.raises(RuntimeError, match="did not pass evaluation gates"):
            promote_candidate(model_name="test_churn_model", force=False)

        # But should succeed with --force
        production_report = promote_candidate(model_name="test_churn_model", force=True)
        assert production_report is not None

    def test_pipeline_reproducibility(self, monkeypatch):
        """Test that running pipeline twice with same seed produces same results."""
        self._override_default_paths(monkeypatch)

        def run_once():
            processed_path = self.data_dir / "processed" / "clean.csv"
            processed_path.parent.mkdir(parents=True)
            processed_df = preprocess(self.sample_csv, processed_path)

            features_path = self.data_dir / "features" / "features.parquet"
            config_path = self.data_dir / "features" / "features_config.json"
            features_path.parent.mkdir(parents=True)
            build_features(processed_path, features_path, config_path)

            train_params = {
                "n_estimators": 10,
                "max_depth": 3,
                "min_samples_leaf": 2,
                "max_features": "sqrt",
                "class_weight": "balanced",
                "random_state": 42,
            }
            train_result = train_model(
                data_path=features_path,
                config_path=config_path,
                model_output=self.models_dir / "model.pkl",
                model_name="test_churn_model",
                params=train_params,
            )
            return train_result["metrics"]

        metrics1 = run_once()
        # Clear mlruns for second run
        import shutil
        if (self.mlruns_dir / "mlflow.db").exists():
            (self.mlruns_dir / "mlflow.db").unlink()
        metrics2 = run_once()

        # With same random_state, metrics should be identical
        assert metrics1["f1"] == metrics2["f1"]
        assert metrics1["accuracy"] == metrics2["accuracy"]
        assert metrics1["roc_auc"] == metrics2["roc_auc"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])