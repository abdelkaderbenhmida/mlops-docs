# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Generate demand forecasting data from real PBS (Pharmaceutical Benefits Scheme) data.

Parses Australian PBS monthly scripts data (683 series × 206 months, Jul 1991 - Jun 2006).
Creates features for demand forecasting: drug_id, concession_type, month, year,
lag_1, lag_12, rolling_mean_3, rolling_mean_6. Target: next month's scripts.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
PBS_PATH = Path(os.getenv("PBS_DATA_PATH", "/tmp/realdata/PBS.csv"))
OUTPUT_PATH = Path("data/raw/pbs_demand_data.csv")


def parse_pbs(pbs_path: Path = PBS_PATH) -> pd.DataFrame:
    """Parse PBS.csv: skip 8 header rows, reshape wide (206 months) to long format."""
    if not pbs_path.exists():
        raise SystemExit(
            f"Raw PBS data not found at {pbs_path}.\n"
            "Download the PBS monthly scripts export and set PBS_DATA_PATH to it. "
            "The generated data/raw/pbs_demand_data.csv is already versioned, so "
            "this script is only needed to regenerate it from source."
        )
    df = pd.read_csv(pbs_path, header=None, skiprows=8)

    month_cols = [f"m_{i}" for i in range(1, 205)]
    df.columns = ["concession_type", "atc_code", "drug_class"] + month_cols

    df = df.dropna(subset=["concession_type", "atc_code", "drug_class"])
    df = df[df["concession_type"].astype(str).str.strip() != ""]

    for col in month_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce"
        ).fillna(0)

    df = df[(df[month_cols] != 0).any(axis=1)]

    id_vars = ["concession_type", "atc_code", "drug_class"]
    long_df = df.melt(id_vars=id_vars, value_vars=month_cols, var_name="month_idx", value_name="scripts")
    long_df["month_idx"] = long_df["month_idx"].str.replace("m_", "").astype(int)

    long_df["year"] = 1991 + (long_df["month_idx"] - 1) // 12
    long_df["month"] = ((long_df["month_idx"] - 1) % 12) + 1
    long_df["date"] = pd.to_datetime(dict(year=long_df["year"], month=long_df["month"], day=1))

    long_df["drug_id"] = (
        long_df["concession_type"].astype(str)
        + "_"
        + long_df["atc_code"].astype(str)
        + "_"
        + long_df["drug_class"].astype(str).str.replace(r"[^A-Z0-9]", "", regex=True).str[:20]
    )

    return long_df[["drug_id", "concession_type", "atc_code", "drug_class", "year", "month", "date", "scripts"]]


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create lag and rolling features for each drug series."""
    df = df.sort_values(["drug_id", "date"]).copy()

    df["lag_1"] = df.groupby("drug_id")["scripts"].shift(1)
    df["lag_12"] = df.groupby("drug_id")["scripts"].shift(12)
    df["rolling_mean_3"] = df.groupby("drug_id")["scripts"].transform(lambda x: x.rolling(3, min_periods=1).mean().shift(1))
    df["rolling_mean_6"] = df.groupby("drug_id")["scripts"].transform(lambda x: x.rolling(6, min_periods=1).mean().shift(1))

    df["target"] = df.groupby("drug_id")["scripts"].shift(-1)

    df = df.dropna(subset=["lag_1", "lag_12", "rolling_mean_3", "rolling_mean_6", "target"])

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate demand forecasting data from PBS.")
    parser.add_argument("--pbs-path", type=Path, default=PBS_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    np.random.seed(args.seed)

    print("Parsing PBS data...")
    long_df = parse_pbs(args.pbs_path)
    print(f"Parsed {len(long_df)} monthly observations across {long_df['drug_id'].nunique()} drug series")

    print("Creating features...")
    feat_df = create_features(long_df)
    print(f"Created {len(feat_df)} training rows with features")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    feat_df.to_csv(args.output, index=False)
    print(f"Saved to {args.output}")
    print(f"Target stats: mean={feat_df['target'].mean():.1f}, median={feat_df['target'].median():.1f}")
    print(f"Features: {list(feat_df.columns)}")


if __name__ == "__main__":
    main()