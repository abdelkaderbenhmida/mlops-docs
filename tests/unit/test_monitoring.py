"""Tests for src.monitoring.drift_detection module (demand forecasting)."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.monitoring.drift_detection import detect_drift, _ks_fallback, NUMERIC_FEATURES


class TestDriftDetection:
    """Test drift detection logic with synthetic demand data."""

    def _create_reference_data(self, n=1000):
        """Create a reference dataset with known distributions."""
        np.random.seed(42)
        return pd.DataFrame({
            "store_id": np.random.randint(1, 31, n),
            "sku_id": np.random.randint(1, 101, n),
            "day_of_week": np.random.randint(0, 7, n),
            "month": np.random.randint(1, 13, n),
            "is_holiday": np.random.choice([0, 1], n),
            "price": np.random.uniform(5, 150, n),
            "promotion": np.random.choice([0, 1], n),
            "temperature": np.random.uniform(20, 100, n),
            "inventory_level": np.random.randint(10, 500, n),
            "competitor_price": np.random.uniform(5, 180, n),
            "store_traffic": np.random.randint(50, 2000, n),
            "prediction": np.random.uniform(10, 80, n),
            "units_sold": np.random.uniform(10, 80, n),
        })

    def _create_drifted_data(self, reference_df, drift_magnitude=0.5):
        """Create a drifted dataset by shifting distributions."""
        drifted = reference_df.copy()
        np.random.seed(123)

        for col in NUMERIC_FEATURES:
            if col in drifted.columns:
                shift = reference_df[col].std() * drift_magnitude
                drifted[col] = drifted[col] + shift

        return drifted

    def test_ks_fallback_detects_drift_on_shifted_numeric(self):
        """_ks_fallback should detect drift when numeric columns are shifted."""
        reference = self._create_reference_data(500)
        current = self._create_drifted_data(reference, drift_magnitude=1.0)

        drift_score, per_column = _ks_fallback(reference, current)

        assert drift_score > 0
        drifted_numeric = [c for c in NUMERIC_FEATURES if c in per_column and per_column[c]["drift_detected"]]
        assert len(drifted_numeric) > 0

    def test_ks_fallback_no_drift_on_identical_data(self):
        """_ks_fallback should not detect drift on identical data."""
        reference = self._create_reference_data(500)
        current = reference.copy()

        drift_score, per_column = _ks_fallback(reference, current)

        assert drift_score == 0.0
        for col, info in per_column.items():
            assert info["drift_detected"] is False

    def test_detect_drift_identical_data_no_drift(self, tmp_path):
        """detect_drift should not detect drift on identical data."""
        reference = self._create_reference_data(200)
        current = reference.copy()

        ref_path = tmp_path / "reference.csv"
        cur_path = tmp_path / "current.csv"
        reference.to_csv(ref_path, index=False)
        current.to_csv(cur_path, index=False)

        report = detect_drift(
            reference_path=ref_path,
            current_path=cur_path,
            threshold=0.3,
            output_dir=tmp_path / "output"
        )

        assert report["drift_score"] == 0.0
        assert report["drift_detected"] is False
        assert report["drifted_features"] == []

    def test_detect_drift_missing_reference_raises(self, tmp_path):
        """detect_drift should raise FileNotFoundError for missing reference."""
        current = self._create_reference_data(100)
        cur_path = tmp_path / "current.csv"
        current.to_csv(cur_path, index=False)

        with pytest.raises(FileNotFoundError, match="Reference dataset not found"):
            detect_drift(
                reference_path=tmp_path / "nonexistent.csv",
                current_path=cur_path,
            )

    def test_detect_drift_missing_current_raises(self, tmp_path):
        """detect_drift should raise FileNotFoundError for missing current."""
        reference = self._create_reference_data(100)
        ref_path = tmp_path / "reference.csv"
        reference.to_csv(ref_path, index=False)

        with pytest.raises(FileNotFoundError, match="Current production data not found"):
            detect_drift(
                reference_path=ref_path,
                current_path=tmp_path / "nonexistent.csv",
            )

    def test_detect_drift_with_env_vars(self, tmp_path, monkeypatch):
        """detect_drift should read from environment variables."""
        reference = self._create_reference_data(100)
        current = reference.copy()

        ref_path = tmp_path / "reference.csv"
        cur_path = tmp_path / "current.csv"
        reference.to_csv(ref_path, index=False)
        current.to_csv(cur_path, index=False)

        monkeypatch.setenv("DRIFT_REFERENCE", str(ref_path))
        monkeypatch.setenv("DRIFT_CURRENT", str(cur_path))
        monkeypatch.setenv("DRIFT_THRESHOLD", "0.5")

        report = detect_drift(output_dir=tmp_path)

        assert report["threshold"] == 0.5
        assert report["reference"] == str(ref_path)
        assert report["current"] == str(cur_path)


class TestFeatureColumns:
    """Test that feature column lists match the actual data."""

    def test_numeric_features_not_empty(self):
        assert len(NUMERIC_FEATURES) > 0
        assert all(isinstance(c, str) for c in NUMERIC_FEATURES)

    def test_no_duplicate_features(self):
        assert len(NUMERIC_FEATURES) == len(set(NUMERIC_FEATURES))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
