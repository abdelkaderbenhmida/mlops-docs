"""End-to-end integration test for the demand forecasting MLOps pipeline.

Tests the full pipeline: generate data -> preprocess -> features -> training -> evaluation
using SQLite MLflow backend and monkeypatched environment.
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

from src.data.preprocessing import preprocess
from src.features.build_features import build_features, FeatureTransformer
from src.models.train import train_model
from src.models.evaluate import evaluate


class TestPipelineEndToEnd:
    """End-to-end pipeline test with minimal data and fast model."""

    @pytest.fixture(autouse=True)
    def setup_env(self, tmp_path, monkeypatch):
        """Set up isolated environment for each test."""
        self.tmp_path = tmp_path
        self.data_dir = tmp_path / "data"
        self.data_dir.mkdir()
        self.models_dir = tmp_path / "models"
        self.models_dir.mkdir()
        self.mlruns_dir = tmp_path / "mlruns"
        self.mlruns_dir.mkdir()

        monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{self.mlruns_dir}/mlflow.db")
        monkeypatch.setenv("MLFLOW_MODEL_NAME", "test_demand_model")
        monkeypatch.setenv("DRIFT_THRESHOLD", "0.3")

        self.sample_csv = self.data_dir / "raw" / "demand_data.csv"
        self.sample_csv.parent.mkdir(parents=True)
        self._create_sample_data()

    def _create_sample_data(self):
        """Create a small sample dataset for fast testing."""
        import numpy as np
        rng = np.random.default_rng(42)
        n = 200
        df = pd.DataFrame({
            "store_id": rng.integers(1, 11, n),
            "sku_id": rng.integers(1, 21, n),
            "day_of_week": rng.integers(0, 7, n),
            "month": rng.integers(1, 13, n),
            "is_holiday": rng.integers(0, 2, n),
            "price": np.round(rng.uniform(5, 100, n), 2),
            "promotion": rng.integers(0, 2, n),
            "temperature": np.round(rng.uniform(20, 100, n), 1),
            "inventory_level": rng.integers(10, 300, n),
            "competitor_price": np.round(rng.uniform(5, 120, n), 2),
            "store_traffic": rng.integers(50, 1500, n),
            "units_sold": rng.integers(5, 80, n),
        })
        df.to_csv(self.sample_csv, index=False)

    def _override_default_paths(self, monkeypatch):
        """Override default paths in modules to use temp directories."""
        monkeypatch.setattr("src.data.preprocessing.DEFAULT_INPUT", self.sample_csv)
        monkeypatch.setattr("src.data.preprocessing.DEFAULT_OUTPUT", self.data_dir / "processed" / "demand_data.csv")

        monkeypatch.setattr("src.features.build_features.DEFAULT_INPUT", self.data_dir / "processed" / "demand_data.csv")
        monkeypatch.setattr("src.features.build_features.DEFAULT_OUTPUT", self.data_dir / "features" / "features.parquet")
        monkeypatch.setattr("src.features.build_features.DEFAULT_CONFIG", self.data_dir / "features" / "features_config.json")

        monkeypatch.setattr("src.models.train.DEFAULT_DATA", self.data_dir / "features" / "features.parquet")
        monkeypatch.setattr("src.models.train.DEFAULT_CONFIG", self.data_dir / "features" / "features_config.json")
        monkeypatch.setattr("src.models.train.DEFAULT_MODEL_OUTPUT", self.models_dir / "model.pkl")
        monkeypatch.setattr("src.models.train.DEFAULT_METRICS", self.models_dir / "metrics.json")
        monkeypatch.setattr("src.models.train.DEFAULT_ARTIFACT_DIR", self.models_dir / "artifacts")
        monkeypatch.setattr("src.models.train.DEFAULT_REFERENCE", self.data_dir / "monitoring" / "reference.csv")
        monkeypatch.setattr("src.models.train.MODEL_NAME", "test_demand_model")

        monkeypatch.setattr("src.models.evaluate.DEFAULT_DATA", self.data_dir / "features" / "features.parquet")
        monkeypatch.setattr("src.models.evaluate.DEFAULT_LOCAL_MODEL", self.models_dir / "model.pkl")
        monkeypatch.setattr("src.models.evaluate.EVALUATION_DIR", self.models_dir / "evaluation")
        monkeypatch.setattr("src.models.evaluate.LATEST_REPORT", self.models_dir / "evaluation" / "latest_report.json")

    def test_full_pipeline(self, monkeypatch):
        """Run the complete pipeline end-to-end."""
        self._override_default_paths(monkeypatch)

        processed_path = self.data_dir / "processed" / "demand_data.csv"
        processed_path.parent.mkdir(parents=True)
        processed_df = preprocess(self.sample_csv, processed_path)
        assert processed_path.exists()
        assert len(processed_df) > 0
        assert "units_sold" in processed_df.columns

        features_path = self.data_dir / "features" / "features.parquet"
        config_path = self.data_dir / "features" / "features_config.json"
        features_path.parent.mkdir(parents=True)
        features_df = build_features(processed_path, features_path, config_path)
        assert features_path.exists()
        assert config_path.exists()
        assert len(features_df) == len(processed_df)
        assert "units_sold" in features_df.columns

        train_params = {
            "n_estimators": 10,
            "max_depth": 5,
            "min_samples_leaf": 3,
            "random_state": 42,
        }
        train_result = train_model(
            data_path=features_path,
            config_path=config_path,
            model_output=self.models_dir / "model.pkl",
            model_name="test_demand_model",
            params=train_params,
        )
        assert train_result["run_id"] is not None
        assert (self.models_dir / "model.pkl").exists()
        assert (self.data_dir / "monitoring" / "reference.csv").exists()

        eval_report = evaluate(
            data_path=features_path,
            model_uri=None,
            run_id=train_result["run_id"],
        )
        assert eval_report["gates_passed"] is not None
        assert "metrics" in eval_report
        assert "rmse" in eval_report["metrics"]
        assert "r2" in eval_report["metrics"]
        assert (self.models_dir / "evaluation" / "latest_report.json").exists()

    def test_pipeline_with_evaluation_failure(self, monkeypatch):
        """Test pipeline when evaluation gates fail."""
        self._override_default_paths(monkeypatch)

        processed_path = self.data_dir / "processed" / "demand_data.csv"
        processed_path.parent.mkdir(parents=True)
        preprocess(self.sample_csv, processed_path)

        features_path = self.data_dir / "features" / "features.parquet"
        config_path = self.data_dir / "features" / "features_config.json"
        features_path.parent.mkdir(parents=True)
        build_features(processed_path, features_path, config_path)

        train_params = {
            "n_estimators": 10,
            "max_depth": 3,
            "min_samples_leaf": 3,
            "random_state": 42,
        }
        train_result = train_model(
            data_path=features_path,
            config_path=config_path,
            model_output=self.models_dir / "model.pkl",
            model_name="test_demand_model",
            params=train_params,
        )

        eval_report = evaluate(
            data_path=features_path,
            run_id=train_result["run_id"],
            thresholds={"min_r2": 0.99, "max_mape": 1.0},
        )
        assert eval_report["gates_passed"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
