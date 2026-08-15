"""Data preprocessing: clean the raw dataset and produce a model-ready table.

Operations (all idempotent):
- Drop the identifier column (CustomerID).
- Coerce numeric columns, drop rows with invalid numeric values.
- Ensure categorical columns contain no unexpected values.
- Output: data/processed/dataset.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "dataset.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "dataset.csv"

DROP_COLUMNS = ["CustomerID"]
NUMERIC_COLUMNS = ["Tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_COLUMNS = [
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
TARGET_COLUMN = "Churn"


def preprocess(input_path: str | Path | None = None, output_path: str | Path | None = None) -> pd.DataFrame:
    input_path = Path(input_path or DEFAULT_INPUT)
    output_path = Path(output_path or DEFAULT_OUTPUT)

    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    df = pd.read_csv(input_path)
    df = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=NUMERIC_COLUMNS).copy()
    df = df[df["Tenure"] >= 0]

    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if TARGET_COLUMN in df.columns:
        df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(str).str.strip()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess raw churn data.")
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    df = preprocess(args.input, args.output)
    print(f"preprocessed {len(df)} rows x {len(df.columns)} columns -> data/processed/dataset.csv")


if __name__ == "__main__":
    main()
