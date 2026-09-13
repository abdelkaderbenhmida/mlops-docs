# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Data preprocessing for demand forecasting data.

Cleans raw demand data and produces a model-ready table.
Operations: coerce numeric columns, drop rows with invalid values, strip whitespace.
Output: data/processed/demand_data.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "dataset.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "demand_data.csv"

NUMERIC_COLUMNS = [
    "store_id", "sku_id", "day_of_week", "month", "is_holiday",
    "price", "promotion", "temperature", "inventory_level",
    "competitor_price", "store_traffic", "units_sold",
]


def resolve_output(output_path: str | Path | None = None) -> Path:
    """Resolve the output path the same way :func:`preprocess` does."""
    return Path(output_path or DEFAULT_OUTPUT)


def preprocess(input_path: str | Path | None = None, output_path: str | Path | None = None) -> pd.DataFrame:
    input_path = Path(input_path or DEFAULT_INPUT)
    output_path = resolve_output(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    df = pd.read_csv(input_path)

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=NUMERIC_COLUMNS).copy()
    df = df[df["units_sold"] >= 0]

    if "date" in df.columns:
        df["date"] = df["date"].astype(str).str.strip()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess raw demand data.")
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    df = preprocess(args.input, args.output)
    print(f"preprocessed {len(df)} rows x {len(df.columns)} columns -> {resolve_output(args.output)}")


if __name__ == "__main__":
    main()
