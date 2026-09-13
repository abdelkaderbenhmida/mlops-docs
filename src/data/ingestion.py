# TODO: high - Add tag mapping version control
# TODO: medium - Implement store-and-forward buffer health checks
# TODO: low - Add unmapped tag alerting
"""Data ingestion: pull raw data from a source (CSV file or URL) into data/raw/.

Idempotent: re-running produces the same normalized raw dataset.
Source is resolved as: --source CLI arg > INGESTION_SOURCE env > default.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = PROJECT_ROOT / "data" / "external" / "dataset.csv"
DEFAULT_DESTINATION = PROJECT_ROOT / "data" / "raw" / "dataset.csv"

RAW_COLUMN_TYPES: dict[str, str] = {
    "store_id": "int64",
    "sku_id": "int64",
    "date": "object",
    "day_of_week": "int64",
    "month": "int64",
    "is_holiday": "int64",
    "price": "float64",
    "promotion": "int64",
    "temperature": "float64",
    "inventory_level": "int64",
    "competitor_price": "float64",
    "store_traffic": "int64",
    "units_sold": "int64",
}


def _read_source(source: str | Path) -> pd.DataFrame:
    source = str(source)
    if source.startswith(("http://", "https://", "s3://")):
        return pd.read_csv(source)
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Ingestion source not found: {source}")
    return pd.read_csv(path)


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    for col, dtype in RAW_COLUMN_TYPES.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except (ValueError, TypeError):
                df[col] = pd.to_numeric(df[col].str.replace(r"[$, ]", "", regex=True), errors="coerce")
    return df


def resolve_destination(destination: str | Path | None = None) -> Path:
    """Resolve the output path the same way :func:`ingest` does."""
    return Path(destination or os.environ.get("INGESTION_DESTINATION") or DEFAULT_DESTINATION)


def ingest(source: str | Path | None = None, destination: str | Path | None = None) -> pd.DataFrame:
    source = source or os.environ.get("INGESTION_SOURCE") or DEFAULT_SOURCE
    destination = resolve_destination(destination)

    resolved = Path(source) if not str(source).startswith(("http", "s3")) else source
    if isinstance(resolved, Path) and not resolved.exists():
        fallback = DEFAULT_DESTINATION if resolved != DEFAULT_DESTINATION else None
        if fallback is not None and fallback.exists():
            resolved = fallback
        else:
            raise FileNotFoundError(f"Ingestion source not found: {source}")

    df = _read_source(resolved)
    df = normalize(df)

    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest the raw demand dataset.")
    parser.add_argument("--source", type=str, default=None, help="CSV path or URL (default: $INGESTION_SOURCE or data/external/dataset.csv)")
    parser.add_argument("--destination", type=str, default=None, help="Output path (default: data/raw/dataset.csv)")
    args = parser.parse_args()

    df = ingest(args.source, args.destination)
    destination = resolve_destination(args.destination)
    print(f"ingested {len(df)} rows x {len(df.columns)} columns -> {destination}")


if __name__ == "__main__":
    main()
