# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Tests for src.data.preprocessing module (demand forecasting)."""

import pandas as pd
import pytest

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocessing import preprocess, NUMERIC_COLUMNS


class TestPreprocessing:
    """Test preprocessing correctness for demand data."""

    def _run(self, df, tmp_path):
        """Write df to a CSV and run preprocess with file paths."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"
        df.to_csv(input_file, index=False)
        return preprocess(input_file, output_file)

    def test_numeric_columns_coerced(self, tmp_path):
        """Numeric columns should be coerced, invalid rows dropped."""
        df = pd.DataFrame({
            "store_id": [1, 2, 3],
            "sku_id": [10, 20, 30],
            "day_of_week": [0, 3, 5],
            "month": [6, 12, 3],
            "is_holiday": [0, 1, 0],
            "price": [29.99, "bad", 19.99],
            "promotion": [1, 0, 1],
            "temperature": [75.0, 35.0, 60.0],
            "inventory_level": [200, 150, 300],
            "competitor_price": [32.99, 52.99, 22.99],
            "store_traffic": [500, 300, 800],
            "units_sold": [45, 12, 78],
        })
        result = self._run(df, tmp_path)
        assert len(result) == 2
        assert result["price"].dtype in ("int64", "float64")

    def test_negative_units_sold_dropped(self, tmp_path):
        """Rows with negative units_sold should be dropped."""
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
            "units_sold": [-5, 12],
        })
        result = self._run(df, tmp_path)
        assert len(result) == 1
        assert result["units_sold"].iloc[0] == 12

    def test_output_columns_match_expected(self, tmp_path):
        """Output should have all expected columns."""
        df = pd.DataFrame({
            "store_id": [1],
            "sku_id": [10],
            "day_of_week": [0],
            "month": [6],
            "is_holiday": [0],
            "price": [29.99],
            "promotion": [1],
            "temperature": [75.0],
            "inventory_level": [200],
            "competitor_price": [32.99],
            "store_traffic": [500],
            "units_sold": [45],
        })
        result = self._run(df, tmp_path)
        expected_cols = set(NUMERIC_COLUMNS + ["date"] if "date" in df.columns else NUMERIC_COLUMNS)
        assert set(result.columns) == expected_cols

    def test_preprocess_with_file_paths(self, tmp_path):
        """Test preprocess with file input/output paths."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        df = pd.DataFrame({
            "store_id": [1],
            "sku_id": [10],
            "day_of_week": [0],
            "month": [6],
            "is_holiday": [0],
            "price": [29.99],
            "promotion": [1],
            "temperature": [75.0],
            "inventory_level": [200],
            "competitor_price": [32.99],
            "store_traffic": [500],
            "units_sold": [45],
        })
        df.to_csv(input_file, index=False)

        result = preprocess(input_file, output_file)

        assert output_file.exists()
        assert len(result) == 1

    def test_missing_input_raises_error(self, tmp_path):
        """Missing input file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            preprocess(tmp_path / "nonexistent.csv", tmp_path / "output.csv")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
