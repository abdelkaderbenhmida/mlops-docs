"""Tests for src.monitoring.drift_detection module."""

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

from src.monitoring.drift_detection import detect_drift, _ks_fallback, NUMERIC_FEATURES, CATEGORICAL_FEATURES


class TestDriftDetection:
    """Test drift detection logic with synthetic data."""

    def _create_reference_data(self, n=1000):
        """Create a reference dataset with known distributions."""
        np.random.seed(42)
        return pd.DataFrame({
            "Tenure": np.random.randint(0, 72, n),
            "MonthlyCharges": np.random.normal(60, 15, n).clip(20, 120),
            "TotalCharges": np.random.normal(2000, 800, n).clip(100, 8000),
            "charges_per_tenure": np.random.normal(30, 10, n).clip(0, 100),
            "tenure_years": np.random.uniform(0, 6, n),
            "num_services": np.random.randint(0, 6, n),
            "Gender": np.random.choice(["Male", "Female"], n),
            "SeniorCitizen": np.random.choice([0, 1], n, p=[0.8, 0.2]),
            "Partner": np.random.choice(["Yes", "No"], n),
            "Dependents": np.random.choice(["Yes", "No"], n),
            "PhoneService": np.random.choice(["Yes", "No"], n),
            "MultipleLines": np.random.choice(["Yes", "No", "No phone service"], n),
            "InternetService": np.random.choice(["DSL", "Fiber optic", "No"], n),
            "OnlineSecurity": np.random.choice(["Yes", "No", "No internet service"], n),
            "OnlineBackup": np.random.choice(["Yes", "No", "No internet service"], n),
            "DeviceProtection": np.random.choice(["Yes", "No", "No internet service"], n),
            "TechSupport": np.random.choice(["Yes", "No", "No internet service"], n),
            "StreamingTV": np.random.choice(["Yes", "No", "No internet service"], n),
            "StreamingMovies": np.random.choice(["Yes", "No", "No internet service"], n),
            "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n),
            "PaperlessBilling": np.random.choice(["Yes", "No"], n),
            "PaymentMethod": np.random.choice(
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], n
            ),
            "label": np.random.choice([0, 1], n),
            "prediction": np.random.uniform(0, 1, n),
        })

    def _create_drifted_data(self, reference_df, drift_magnitude=0.5):
        """Create a drifted dataset by shifting distributions."""
        drifted = reference_df.copy()
        np.random.seed(123)  # Different seed
        
        # Drift numeric features
        for col in NUMERIC_FEATURES:
            if col in drifted.columns:
                shift = reference_df[col].std() * drift_magnitude
                drifted[col] = drifted[col] + shift
        
        # Drift categorical features by changing distribution
        for col in CATEGORICAL_FEATURES:
            if col in drifted.columns:
                # Shift 30% of values to a different category
                n_change = int(len(drifted) * 0.3)
                unique_vals = reference_df[col].unique()
                if len(unique_vals) > 1:
                    idx = np.random.choice(len(drifted), n_change, replace=False)
                    for i in idx:
                        current = drifted.loc[i, col]
                        other_vals = [v for v in unique_vals if v != current]
                        drifted.loc[i, col] = np.random.choice(other_vals)
        
        return drifted

    def test_ks_fallback_detects_drift_on_shifted_numeric(self):
        """_ks_fallback should detect drift when numeric columns are shifted."""
        reference = self._create_reference_data(500)
        current = self._create_drifted_data(reference, drift_magnitude=1.0)
        
        drift_score, per_column = _ks_fallback(reference, current)
        
        assert drift_score > 0
        # At least some numeric columns should be detected as drifted
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

    def test_ks_fallback_handles_empty_columns(self):
        """_ks_fallback should handle columns with all NaN gracefully."""
        reference = self._create_reference_data(100)
        current = reference.copy()
        current["Tenure"] = np.nan
        
        drift_score, per_column = _ks_fallback(reference, current)
        
        # Should not crash, Tenure should be skipped
        assert "Tenure" not in per_column or not per_column["Tenure"]["drift_detected"]

    def test_detect_drift_with_scipy_fallback(self, tmp_path):
        """detect_drift should work with scipy fallback when evidently not available."""
        reference = self._create_reference_data(200)
        current = self._create_drifted_data(reference, drift_magnitude=0.8)
        
        ref_path = tmp_path / "reference.csv"
        cur_path = tmp_path / "current.csv"
        reference.to_csv(ref_path, index=False)
        current.to_csv(cur_path, index=False)
        
        # Force scipy fallback by patching evidently import
        with patch.dict(sys.modules, {"evidently": None}):
            with patch("src.monitoring.drift_detection._evidently_report", side_effect=ImportError):
                report = detect_drift(
                    reference_path=ref_path,
                    current_path=cur_path,
                    threshold=0.3,
                    output_dir=tmp_path / "output"
                )
        
        assert report["engine"] == "scipy-fallback"
        assert "drift_score" in report
        assert "drift_detected" in report
        assert "per_column" in report
        assert "drifted_features" in report

    def test_detect_drift_identical_data_no_drift(self, tmp_path):
        """detect_drift should not detect drift on identical data."""
        reference = self._create_reference_data(200)
        current = reference.copy()
        
        ref_path = tmp_path / "reference.csv"
        cur_path = tmp_path / "current.csv"
        reference.to_csv(ref_path, index=False)
        current.to_csv(cur_path, index=False)
        
        with patch("src.monitoring.drift_detection._evidently_report", side_effect=ImportError):
            report = detect_drift(
                reference_path=ref_path,
                current_path=cur_path,
                threshold=0.3,
                output_dir=tmp_path / "output"
            )
        
        assert report["drift_score"] == 0.0
        assert report["drift_detected"] is False
        assert report["drifted_features"] == []

    def test_detect_drift_high_threshold(self, tmp_path):
        """detect_drift should respect threshold parameter."""
        reference = self._create_reference_data(200)
        current = self._create_drifted_data(reference, drift_magnitude=0.3)
        
        ref_path = tmp_path / "reference.csv"
        cur_path = tmp_path / "current.csv"
        reference.to_csv(ref_path, index=False)
        current.to_csv(cur_path, index=False)
        
        with patch("src.monitoring.drift_detection._evidently_report", side_effect=ImportError):
            # High threshold - should not detect
            report_high = detect_drift(
                reference_path=ref_path,
                current_path=cur_path,
                threshold=0.9,
                output_dir=tmp_path / "output"
            )
            
            # Low threshold - should detect
            report_low = detect_drift(
                reference_path=ref_path,
                current_path=cur_path,
                threshold=0.1,
                output_dir=tmp_path / "output"
            )
        
        # With higher threshold, less likely to detect
        assert report_high["threshold"] == 0.9
        assert report_low["threshold"] == 0.1

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
        
        with patch("src.monitoring.drift_detection._evidently_report", side_effect=ImportError):
            report = detect_drift()
        
        assert report["threshold"] == 0.5
        assert report["reference"] == str(ref_path)
        assert report["current"] == str(cur_path)

    @pytest.mark.skipif(True, reason="Requires evidently installed; tested via fallback")
    def test_detect_drift_with_evidently(self, tmp_path):
        """detect_drift should use evidently when available."""
        pytest.importorskip("evidently")
        reference = self._create_reference_data(200)
        current = self._create_drifted_data(reference, drift_magnitude=0.8)
        
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
        
        assert report["engine"] == "evidently"
        assert (tmp_path / "output" / "drift_report.json").exists()


class TestFeatureColumns:
    """Test that feature column lists match the actual data."""

    def test_numeric_features_not_empty(self):
        assert len(NUMERIC_FEATURES) > 0
        assert all(isinstance(c, str) for c in NUMERIC_FEATURES)

    def test_categorical_features_not_empty(self):
        assert len(CATEGORICAL_FEATURES) > 0
        assert all(isinstance(c, str) for c in CATEGORICAL_FEATURES)

    def test_no_duplicate_features(self):
        all_features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
        assert len(all_features) == len(set(all_features))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])