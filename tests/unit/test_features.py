"""Tests for src.features.build_features module."""

import json
import pandas as pd
import pytest

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.features.build_features import (
    FeatureTransformer,
    build_features,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    ENGINEERED_FEATURES,
    FEATURE_ORDER,
    TARGET_FEATURE,
    TARGET_COLUMN,
    SERVICE_COLUMNS,
)


class TestFeatureTransformer:
    """Test FeatureTransformer fit/transform correctness."""

    def _sample_df(self, n=100):
        """Create sample dataframe with expected columns."""
        import numpy as np
        np.random.seed(42)
        return pd.DataFrame({
            "Gender": np.random.choice(["Male", "Female"], n),
            "SeniorCitizen": np.random.choice([0, 1], n),
            "Partner": np.random.choice(["Yes", "No"], n),
            "Dependents": np.random.choice(["Yes", "No"], n),
            "Tenure": np.random.randint(0, 72, n),
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
            "PaymentMethod": np.random.choice(["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], n),
            "MonthlyCharges": np.random.uniform(20, 120, n),
            "TotalCharges": np.random.uniform(100, 8000, n),
            "Churn": np.random.choice(["Yes", "No"], n),
        })

    def test_fit_transform_shape(self):
        """fit_transform should return expected feature columns."""
        df = self._sample_df(50)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        
        assert list(features.columns) == FEATURE_ORDER
        assert len(features) == 50

    def test_numeric_features_scaled(self):
        """Numeric features should be present in output."""
        df = self._sample_df(30)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        
        for col in NUMERIC_FEATURES:
            assert col in features.columns
            assert features[col].dtype in ("float64", "float32", "int64", "int32")

    def test_engineered_features_created(self):
        """Engineered features should be created."""
        df = self._sample_df(30)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        
        for col in ENGINEERED_FEATURES:
            assert col in features.columns

    def test_categorical_encoded_as_int(self):
        """Categorical features should be encoded as integers."""
        df = self._sample_df(30)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        
        for col in CATEGORICAL_FEATURES:
            assert col in features.columns
            assert features[col].dtype in ("int64", "int32")
            # Values should be >= -1 (unseen categories map to -1)
            assert (features[col] >= -1).all()

    def test_transform_unseen_categories_maps_to_minus_one(self):
        """Unseen categories during transform should map to -1."""
        df_train = self._sample_df(30)
        df_test = df_train.copy()
        # Add unseen category
        df_test.loc[0, "Gender"] = "UnknownGender"
        
        transformer = FeatureTransformer()
        transformer.fit(df_train)
        features = transformer.transform(df_test)
        
        assert features.loc[0, "Gender"] == -1

    def test_config_roundtrip(self):
        """to_config and from_config should preserve state."""
        df = self._sample_df(30)
        transformer = FeatureTransformer()
        transformer.fit(df)
        
        config = transformer.to_config()
        restored = FeatureTransformer.from_config(config)
        
        # Test that both produce identical transforms
        test_df = self._sample_df(10)
        out1 = transformer.transform(test_df)
        out2 = restored.transform(test_df)
        
        pd.testing.assert_frame_equal(out1, out2)

    def test_train_inference_parity(self):
        """Train-time fit_transform and inference-time transform should match on same data."""
        df = self._sample_df(50)
        
        # Train-time
        transformer_train = FeatureTransformer()
        features_train = transformer_train.fit_transform(df)
        
        # Inference-time (using saved config)
        config = transformer_train.to_config()
        transformer_infer = FeatureTransformer.from_config(config)
        features_infer = transformer_infer.transform(df)
        
        pd.testing.assert_frame_equal(features_train, features_infer)

    def test_feature_order_preserved(self):
        """Feature order should match FEATURE_ORDER exactly."""
        df = self._sample_df(20)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        
        assert list(features.columns) == FEATURE_ORDER

    def test_num_services_feature(self):
        """num_services should count Yes in SERVICE_COLUMNS."""
        df = pd.DataFrame({
            "Gender": ["Male"],
            "SeniorCitizen": [0],
            "Partner": ["Yes"],
            "Dependents": ["No"],
            "Tenure": [12],
            "PhoneService": ["Yes"],
            "MultipleLines": ["Yes"],
            "InternetService": ["DSL"],
            "OnlineSecurity": ["Yes"],
            "OnlineBackup": ["No"],
            "DeviceProtection": ["Yes"],
            "TechSupport": ["No"],
            "StreamingTV": ["Yes"],
            "StreamingMovies": ["No"],
            "Contract": ["Month-to-month"],
            "PaperlessBilling": ["No"],
            "PaymentMethod": ["Electronic check"],
            "MonthlyCharges": [50.0],
            "TotalCharges": [600.0],
            "Churn": ["No"],
        })
        
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        
        # OnlineSecurity=Yes, DeviceProtection=Yes, StreamingTV=Yes => 3 services
        # (OnlineBackup=No, TechSupport=No, StreamingMovies=No)
        assert features["num_services"].iloc[0] == 3


class TestBuildFeatures:
    """Test build_features end-to-end function."""

    def test_build_features_creates_output(self, tmp_path):
        """build_features should create parquet and config files."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "features.parquet"
        config_file = tmp_path / "config.json"
        
        df = pd.DataFrame({
            "Gender": ["Male", "Female"],
            "SeniorCitizen": [0, 1],
            "Partner": ["Yes", "No"],
            "Dependents": ["No", "Yes"],
            "Tenure": [12, 24],
            "PhoneService": ["Yes", "Yes"],
            "MultipleLines": ["No", "Yes"],
            "InternetService": ["DSL", "Fiber optic"],
            "OnlineSecurity": ["Yes", "No"],
            "OnlineBackup": ["No", "Yes"],
            "DeviceProtection": ["No", "No"],
            "TechSupport": ["Yes", "No"],
            "StreamingTV": ["No", "No"],
            "StreamingMovies": ["No", "No"],
            "Contract": ["Month-to-month", "One year"],
            "PaperlessBilling": ["No", "Yes"],
            "PaymentMethod": ["Electronic check", "Mailed check"],
            "MonthlyCharges": [50.0, 70.0],
            "TotalCharges": [600.0, 1680.0],
            "Churn": ["No", "Yes"],
        })
        df.to_csv(input_file, index=False)
        
        features = build_features(input_file, output_file, config_file)
        
        assert output_file.exists()
        assert config_file.exists()
        assert len(features) == 2
        assert TARGET_FEATURE in features.columns
        
        # Verify config can be loaded
        with config_file.open() as f:
            config = json.load(f)
        assert "category_mappings" in config
        assert "numeric_stats" in config
        assert "feature_order" in config

    def test_target_feature_created(self):
        """Target feature should be binary 0/1."""
        df = pd.DataFrame({
            "Gender": ["Male", "Female"],
            "SeniorCitizen": [0, 1],
            "Partner": ["Yes", "No"],
            "Dependents": ["No", "Yes"],
            "Tenure": [12, 24],
            "PhoneService": ["Yes", "Yes"],
            "MultipleLines": ["No", "Yes"],
            "InternetService": ["DSL", "Fiber optic"],
            "OnlineSecurity": ["Yes", "No"],
            "OnlineBackup": ["No", "Yes"],
            "DeviceProtection": ["No", "No"],
            "TechSupport": ["Yes", "No"],
            "StreamingTV": ["No", "No"],
            "StreamingMovies": ["No", "No"],
            "Contract": ["Month-to-month", "One year"],
            "PaperlessBilling": ["No", "Yes"],
            "PaymentMethod": ["Electronic check", "Mailed check"],
            "MonthlyCharges": [50.0, 70.0],
            "TotalCharges": [600.0, 1680.0],
            "Churn": ["No", "Yes"],
        })
        
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        features[TARGET_FEATURE] = (df[TARGET_COLUMN].astype(str).str.lower() == "yes").astype(int)
        
        assert set(features[TARGET_FEATURE].unique()) == {0, 1}
        assert features[TARGET_FEATURE].iloc[0] == 0  # No -> 0
        assert features[TARGET_FEATURE].iloc[1] == 1  # Yes -> 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])