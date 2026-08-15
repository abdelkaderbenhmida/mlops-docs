"""Lightweight Parquet feature store, versioned by DVC.

Each `put_features` writes data/features/features_v{N}.parquet together with a
documented schema (name, type, description, expected range). DVC versions the
Parquet files; a Git commit pins the exact feature snapshot used for training,
so any production model can be traced back to its feature set.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = PROJECT_ROOT / "data" / "features"
SCHEMA_FILE = "features_store_schema.json"

FEATURE_SCHEMA = {
    "Tenure": {"type": "float64", "description": "Months the customer has stayed", "expected_range": [0, 120]},
    "MonthlyCharges": {"type": "float64", "description": "Monthly subscription charge", "expected_range": [0, 1000]},
    "TotalCharges": {"type": "float64", "description": "Total charges paid to date", "expected_range": [0, 100000]},
    "charges_per_tenure": {
        "type": "float64",
        "description": "TotalCharges / (Tenure + 1)",
        "expected_range": [0, 1000],
    },
    "tenure_years": {"type": "float64", "description": "Tenure expressed in years", "expected_range": [0, 10]},
    "num_services": {"type": "int64", "description": "Number of subscribed services", "expected_range": [0, 6]},
    "Gender": {"type": "int64", "description": "Encoded gender (0/1)", "expected_range": [0, 1]},
    "SeniorCitizen": {"type": "int64", "description": "1 if senior citizen", "expected_range": [0, 1]},
    "Partner": {"type": "int64", "description": "1 if has partner", "expected_range": [0, 1]},
    "Dependents": {"type": "int64", "description": "1 if has dependents", "expected_range": [0, 1]},
    "PhoneService": {"type": "int64", "description": "1 if has phone service", "expected_range": [0, 1]},
    "MultipleLines": {"type": "int64", "description": "Encoded multiple lines", "expected_range": [-1, 2]},
    "InternetService": {"type": "int64", "description": "Encoded internet service type", "expected_range": [-1, 2]},
    "OnlineSecurity": {"type": "int64", "description": "Encoded online security", "expected_range": [-1, 2]},
    "OnlineBackup": {"type": "int64", "description": "Encoded online backup", "expected_range": [-1, 2]},
    "DeviceProtection": {"type": "int64", "description": "Encoded device protection", "expected_range": [-1, 2]},
    "TechSupport": {"type": "int64", "description": "Encoded tech support", "expected_range": [-1, 2]},
    "StreamingTV": {"type": "int64", "description": "Encoded streaming TV", "expected_range": [-1, 2]},
    "StreamingMovies": {"type": "int64", "description": "Encoded streaming movies", "expected_range": [-1, 2]},
    "Contract": {"type": "int64", "description": "Encoded contract type", "expected_range": [-1, 2]},
    "PaperlessBilling": {"type": "int64", "description": "1 if paperless billing", "expected_range": [0, 1]},
    "PaymentMethod": {"type": "int64", "description": "Encoded payment method", "expected_range": [-1, 3]},
    "churn_target": {"type": "int64", "description": "Target: 1 if customer churned", "expected_range": [0, 1]},
}


class FeatureStore:
    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir or DEFAULT_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _version_file(self, version: int) -> Path:
        return self.base_dir / f"features_v{version}.parquet"

    def next_version(self) -> int:
        versions = [p.stem.split("_v")[-1] for p in self.base_dir.glob("features_v*.parquet")]
        return max((int(v) for v in versions), default=0) + 1

    def put_features(self, df: pd.DataFrame, version: int | None = None) -> int:
        version = version or self.next_version()
        df.to_parquet(self._version_file(version), index=False)
        self.write_schema(df)
        return version

    def get_features(self, version: int | None = None) -> pd.DataFrame:
        if version is None:
            version = max(1, self.next_version() - 1)
        path = self._version_file(version)
        if not path.exists():
            raise FileNotFoundError(f"Feature version not found: {path}")
        return pd.read_parquet(path)

    def list_versions(self) -> list[int]:
        return sorted(int(p.stem.split("_v")[-1]) for p in self.base_dir.glob("features_v*.parquet"))

    def write_schema(self, df: pd.DataFrame) -> None:
        schema = {"store": "lightweight-parquet", "versioned_by": "dvc", "features": {}}
        for col in df.columns:
            entry = dict(FEATURE_SCHEMA.get(col, {"type": str(df[col].dtype), "description": "", "expected_range": []}))
            entry["dtype"] = str(df[col].dtype)
            schema["features"][col] = entry
        with (self.base_dir / SCHEMA_FILE).open("w") as fh:
            json.dump(schema, fh, indent=2)

    def schema(self) -> dict:
        path = self.base_dir / SCHEMA_FILE
        if not path.exists():
            return {}
        with path.open() as fh:
            return json.load(fh)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect the lightweight feature store.")
    parser.add_argument("--list-versions", action="store_true")
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--show", type=int, default=None, help="Show head of a given version")
    args = parser.parse_args()

    store = FeatureStore()
    if args.list_versions:
        print(f"versions: {store.list_versions()}")
    if args.schema:
        print(json.dumps(store.schema(), indent=2))
    if args.show is not None:
        print(store.get_features(args.show).head(5).to_string())


if __name__ == "__main__":
    main()
