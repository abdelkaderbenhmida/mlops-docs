"""Tests for data quality validation for demand forecasting data."""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "demand_data.csv"


class TestDataQuality:
    """Validate the demand dataset against quality expectations."""

    @pytest.fixture(scope="class")
    def dataset(self):
        """Load the raw demand dataset."""
        if not DATA_PATH.exists():
            pytest.skip(f"Dataset not found at {DATA_PATH}")
        return pd.read_csv(DATA_PATH)

    def test_dataset_exists(self, dataset):
        """Dataset file should exist and be readable."""
        assert len(dataset) > 0

    def test_row_count_sufficient(self, dataset):
        """Row count should be at least 1000."""
        assert len(dataset) >= 1000

    def test_critical_columns_not_null(self, dataset):
        """Critical columns should have no null values."""
        for col in ["store_id", "sku_id", "price", "units_sold"]:
            assert col in dataset.columns, f"Missing column: {col}"
            assert dataset[col].notna().all(), f"Column {col} has null values"

    def test_store_id_range(self, dataset):
        """store_id should be between 1 and 100."""
        assert dataset["store_id"].between(1, 100).all()

    def test_sku_id_range(self, dataset):
        """sku_id should be between 1 and 200."""
        assert dataset["sku_id"].between(1, 200).all()

    def test_price_positive(self, dataset):
        """price should be positive."""
        assert (dataset["price"] >= 0).all()

    def test_units_sold_non_negative(self, dataset):
        """units_sold should be non-negative."""
        assert (dataset["units_sold"] >= 0).all()

    def test_day_of_week_range(self, dataset):
        """day_of_week should be between 0 and 6."""
        assert dataset["day_of_week"].between(0, 6).all()

    def test_month_range(self, dataset):
        """month should be between 1 and 12."""
        assert dataset["month"].between(1, 12).all()

    def test_is_holiday_values(self, dataset):
        """is_holiday should only be 0 or 1."""
        assert set(dataset["is_holiday"].unique()).issubset({0, 1})

    def test_promotion_values(self, dataset):
        """promotion should only be 0 or 1."""
        assert set(dataset["promotion"].unique()).issubset({0, 1})

    def test_temperature_range(self, dataset):
        """temperature should be reasonable (-50 to 150)."""
        assert dataset["temperature"].between(-50, 150).all()

    def test_inventory_level_positive(self, dataset):
        """inventory_level should be positive."""
        assert (dataset["inventory_level"] >= 0).all()

    def test_store_traffic_positive(self, dataset):
        """store_traffic should be positive."""
        assert (dataset["store_traffic"] >= 0).all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
