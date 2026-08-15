"""Feature engineering: transform processed data into model features.

Encapsulated in `FeatureTransformer` so the exact same transformations are
applied at training time and at inference time (no training/serving skew).
The fitted state (category mappings, numeric statistics, column order) is
persisted as a JSON config and shipped with the model as an MLflow artifact.

Outputs:
- data/features/features.parquet       (training features + target)
- data/features/features_config.json   (fitted transformer state)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "dataset.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "features" / "features.parquet"
DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config.json"

TARGET_COLUMN = "Churn"
TARGET_FEATURE = "churn_target"

NUMERIC_FEATURES = ["Tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_FEATURES = [
    "Gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
ENGINEERED_FEATURES = ["charges_per_tenure", "tenure_years", "num_services"]

SERVICE_COLUMNS = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]

FEATURE_ORDER = NUMERIC_FEATURES + ENGINEERED_FEATURES + CATEGORICAL_FEATURES


def _engineer(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["charges_per_tenure"] = out["TotalCharges"] / (out["Tenure"] + 1)
    out["tenure_years"] = out["Tenure"] / 12.0
    out["num_services"] = sum((out[c].astype(str) == "Yes").astype(int) for c in SERVICE_COLUMNS)
    return out


class FeatureTransformer:
    def __init__(self, numeric_features: list[str] | None = None, categorical_features: list[str] | None = None):
        self.numeric_features = numeric_features or NUMERIC_FEATURES
        self.categorical_features = categorical_features or CATEGORICAL_FEATURES
        self.category_mappings: dict[str, dict[str, int]] = {}
        self.numeric_stats: dict[str, dict[str, float]] = {}

    def fit(self, df: pd.DataFrame) -> FeatureTransformer:
        data = _engineer(df)
        for col in self.categorical_features:
            categories = sorted(data[col].astype(str).unique())
            self.category_mappings[col] = {cat: i for i, cat in enumerate(categories)}
        for col in self.numeric_features:
            self.numeric_stats[col] = {"mean": float(data[col].mean()), "std": float(data[col].std(ddof=0))}
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        data = _engineer(df).copy()
        for col in self.categorical_features:
            mapping = self.category_mappings.get(col, {})
            data[col] = data[col].astype(str).map(mapping).fillna(-1).astype(int)
        for col in self.numeric_features:
            data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0).astype(float)
        for col in ENGINEERED_FEATURES:
            data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0).astype(float)
        return data[FEATURE_ORDER]

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def to_config(self) -> dict:
        return {
            "numeric_features": self.numeric_features,
            "categorical_features": self.categorical_features,
            "category_mappings": self.category_mappings,
            "numeric_stats": self.numeric_stats,
            "feature_order": FEATURE_ORDER,
        }

    @classmethod
    def from_config(cls, config: dict) -> FeatureTransformer:
        transformer = cls(config["numeric_features"], config["categorical_features"])
        transformer.category_mappings = config["category_mappings"]
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
    transformer = FeatureTransformer().fit(df)
    features = transformer.fit_transform(df)
    if TARGET_COLUMN in df.columns:
        features[TARGET_FEATURE] = (df[TARGET_COLUMN].astype(str).str.lower() == "yes").astype(int)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(output_path, index=False)
    with config_path.open("w") as fh:
        json.dump(transformer.to_config(), fh, indent=2)
    return features


def main() -> None:
    parser = argparse.ArgumentParser(description="Build features from processed data.")
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()

    features = build_features(args.input, args.output, args.config)
    print(f"built {features.shape[0]} rows x {features.shape[1]} features -> data/features/features.parquet")


if __name__ == "__main__":
    main()
