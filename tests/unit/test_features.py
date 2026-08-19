"""Tests for src.features.build_features module (demand forecasting)."""

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
    FEATURE_ORDER,
    TARGET_FEATURE,
    TARGET_COLUMN,
)


class TestFeatureTransformer:
    """Test FeatureTransformer fit/transform correctness for demand data."""

    def _sample_df(self, n=100):
        """Create sample dataframe with demand columns."""
        import numpy as np
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
            "units_sold": np.random.randint(0, 100, n),
        })

    def test_fit_transform_shape(self):
        """fit_transform should return expected feature columns."""
        df = self._sample_df(50)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)

        assert list(features.columns) == FEATURE_ORDER
        assert len(features) == 50

    def test_numeric_features_present(self):
        """Numeric features should be present in output."""
        df = self._sample_df(30)
        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)

        for col in FEATURE_ORDER:
            assert col in features.columns
            assert features[col].dtype in ("float64", "float32", "int64", "int32")

    def test_config_roundtrip(self):
        """to_config and from_config should preserve state."""
        df = self._sample_df(30)
        transformer = FeatureTransformer()
        transformer.fit(df)

        config = transformer.to_config()
        restored = FeatureTransformer.from_config(config)

        test_df = self._sample_df(10)
        out1 = transformer.transform(test_df)
        out2 = restored.transform(test_df)

        pd.testing.assert_frame_equal(out1, out2)

    def test_train_inference_parity(self):
        """Train-time fit_transform and inference-time transform should match."""
        df = self._sample_df(50)

        transformer_train = FeatureTransformer()
        features_train = transformer_train.fit_transform(df)

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


class TestBuildFeatures:
    """Test build_features end-to-end function for demand data."""

    def test_build_features_creates_output(self, tmp_path):
        """build_features should create parquet and config files."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "features.parquet"
        config_file = tmp_path / "config.json"

        df = pd.DataFrame({
            "store_id": [1, 2],
            "sku_id": [10, 20],
            "day_of_week": [0, 3],
            "month": [6, 12],
            "is_holiday": [0, 1],
            "price": [29.99, 49.99],
            "promotion": [1, 0],
            "temperature": [75.0, 35.0],
            "inventory_level": [200, 150],
            "competitor_price": [32.99, 52.99],
            "store_traffic": [500, 300],
            "units_sold": [45, 12],
        })
        df.to_csv(input_file, index=False)

        features = build_features(input_file, output_file, config_file)

        assert output_file.exists()
        assert config_file.exists()
        assert len(features) == 2
        assert TARGET_FEATURE in features.columns

        with config_file.open() as f:
            config = json.load(f)
        assert "numeric_features" in config
        assert "numeric_stats" in config
        assert "feature_order" in config

    def test_target_feature_is_numeric(self):
        """Target feature should be numeric for regression."""
        df = pd.DataFrame({
            "store_id": [1, 2, 3],
            "sku_id": [10, 20, 30],
            "day_of_week": [0, 3, 5],
            "month": [6, 12, 3],
            "is_holiday": [0, 1, 0],
            "price": [29.99, 49.99, 19.99],
            "promotion": [1, 0, 1],
            "temperature": [75.0, 35.0, 60.0],
            "inventory_level": [200, 150, 300],
            "competitor_price": [32.99, 52.99, 22.99],
            "store_traffic": [500, 300, 800],
            "units_sold": [45, 12, 78],
        })

        transformer = FeatureTransformer()
        features = transformer.fit_transform(df)
        features[TARGET_FEATURE] = df[TARGET_COLUMN].astype(float)

        assert features[TARGET_FEATURE].dtype in ("float64", "float32")
        assert set(features[TARGET_FEATURE].unique()).issubset({12.0, 45.0, 78.0})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
