# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
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
    "store_id": {"type": "int64", "description": "Store identifier", "expected_range": [1, 100]},
    "sku_id": {"type": "int64", "description": "Product (SKU) identifier", "expected_range": [1, 200]},
    "day_of_week": {"type": "int64", "description": "Day of week (0=Monday)", "expected_range": [0, 6]},
    "month": {"type": "int64", "description": "Calendar month", "expected_range": [1, 12]},
    "is_holiday": {"type": "int64", "description": "1 if the day is a public holiday", "expected_range": [0, 1]},
    "price": {"type": "float64", "description": "Selling price", "expected_range": [0, 500]},
    "promotion": {"type": "int64", "description": "1 if the product is on promotion", "expected_range": [0, 1]},
    "temperature": {"type": "float64", "description": "Outside temperature (C)", "expected_range": [-50, 150]},
    "inventory_level": {"type": "int64", "description": "Stock on hand", "expected_range": [0, 10000]},
    "competitor_price": {"type": "float64", "description": "Competitor selling price", "expected_range": [0, 500]},
    "store_traffic": {"type": "int64", "description": "Store footfall for the day", "expected_range": [0, 50000]},
    "units_sold": {"type": "int64", "description": "Target: units sold", "expected_range": [0, 100000]},
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
