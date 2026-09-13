# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Feature engineering for demand forecasting.

Transforms raw demand data into model features with a FeatureTransformer
for train/inference parity. Outputs:
- data/features/features.parquet
- data/features/features_config.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "demand_data.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "features" / "features.parquet"
DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config.json"

TARGET_COLUMN = "units_sold"
TARGET_FEATURE = "units_sold"

FEATURE_ORDER = [
    "store_id",
    "sku_id",
    "day_of_week",
    "month",
    "is_holiday",
    "price",
    "promotion",
    "temperature",
    "inventory_level",
    "competitor_price",
    "store_traffic",
]


class FeatureTransformer:
    def __init__(self, numeric_features: list[str] | None = None):
        self.numeric_features = numeric_features or [
            "store_id", "sku_id", "day_of_week", "month", "is_holiday",
            "price", "promotion", "temperature", "inventory_level",
            "competitor_price", "store_traffic",
        ]
        self.numeric_stats: dict[str, dict[str, float]] = {}

    def fit(self, df: pd.DataFrame) -> FeatureTransformer:
        for col in self.numeric_features:
            self.numeric_stats[col] = {
                "mean": float(df[col].mean()),
                "std": float(df[col].std(ddof=0)) or 1.0,
            }
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        for col in self.numeric_features:
            data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0).astype(float)
        return data[FEATURE_ORDER]

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def to_config(self) -> dict:
        return {
            "numeric_features": self.numeric_features,
            "numeric_stats": self.numeric_stats,
            "feature_order": FEATURE_ORDER,
        }

    @classmethod
    def from_config(cls, config: dict) -> FeatureTransformer:
        transformer = cls(config["numeric_features"])
        transformer.numeric_stats = config["numeric_stats"]
        return transformer


def build_features(
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
    config_path: str | Path | None = None,
) -> pd.DataFrame:
    input_path = Path(input_path or DEFAULT_INPUT)
    output_path = Path(output_path or DEFAULT_OUTPUT)
    config_path = Path(config_path or DEFAULT_CONFIG)

    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    df = pd.read_csv(input_path)
    transformer = FeatureTransformer()
    features = transformer.fit_transform(df)

    if TARGET_COLUMN in df.columns:
        features[TARGET_FEATURE] = df[TARGET_COLUMN].astype(float)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(output_path, index=False)
    with config_path.open("w") as fh:
        json.dump(transformer.to_config(), fh, indent=2)
    return features


def main() -> None:
    parser = argparse.ArgumentParser(description="Build features from demand data.")
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()

    features = build_features(args.input, args.output, args.config)
    print(f"built {features.shape[0]} rows x {features.shape[1]} features -> data/features/features.parquet")


if __name__ == "__main__":
    main()
