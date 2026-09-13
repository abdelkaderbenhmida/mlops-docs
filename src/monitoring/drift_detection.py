# TODO: high - Add alert rule for ingestion stalls
# TODO: medium - Implement dashboard for drift detection
# TODO: low - Add prediction distribution monitoring
"""Model and data drift detection for demand forecasting.

Compares current production data against training reference snapshot:
- data drift per feature (KS test for numeric)
- global drift score = fraction of drifted features
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"
DEFAULT_CURRENT = PROJECT_ROOT / "data" / "monitoring" / "current.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "monitoring"

NUMERIC_FEATURES = [
    "store_id", "sku_id", "day_of_week", "month", "is_holiday",
    "price", "promotion", "temperature", "inventory_level",
    "competitor_price", "store_traffic",
]
CATEGORICAL_FEATURES = []


def _features_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in NUMERIC_FEATURES if c in df.columns]


def _ks_fallback(reference: pd.DataFrame, current: pd.DataFrame) -> tuple[float, dict]:
    from scipy import stats

    drifted = 0
    total = 0
    per_column: dict[str, dict] = {}
    for col in _features_columns(reference):
        if col not in current.columns:
            continue
        ref_vals = pd.to_numeric(reference[col], errors="coerce").dropna()
        cur_vals = pd.to_numeric(current[col], errors="coerce").dropna()
        if ref_vals.empty or cur_vals.empty:
            continue
        stat, p_value = stats.ks_2samp(ref_vals, cur_vals)
        detected = bool(p_value < 0.05 and stat > 0.1)
        per_column[col] = {"drift_detected": detected, "test": "ks_2samp", "score": float(stat)}
        drifted += int(detected)
        total += 1
    return (drifted / total if total else 0.0), per_column


def detect_drift(
    reference_path: str | Path | None = None,
    current_path: str | Path | None = None,
    threshold: float | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    reference_path = Path(reference_path or os.environ.get("DRIFT_REFERENCE") or DEFAULT_REFERENCE)
    current_path = Path(current_path or os.environ.get("DRIFT_CURRENT") or DEFAULT_CURRENT)
    output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)
    threshold = float(threshold if threshold is not None else os.environ.get("DRIFT_THRESHOLD", "0.3"))

    if not reference_path.exists():
        raise FileNotFoundError(f"Reference dataset not found: {reference_path}")
    if not current_path.exists():
        raise FileNotFoundError(f"Current production data not found: {current_path}")

    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)

    drift_score, per_column = _ks_fallback(reference, current)

    report = {
        "engine": "scipy-fallback",
        "drift_score": drift_score,
        "threshold": threshold,
        "drift_detected": drift_score > threshold,
        "drifted_features": sorted(c for c, info in per_column.items() if info["drift_detected"]),
        "per_column": per_column,
        "reference": str(reference_path),
        "current": str(current_path),
        "generated_at": None,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "drift_report.json").open("w") as fh:
        json.dump(report, fh, indent=2, default=str)

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect drift between reference and current data.")
    parser.add_argument("--reference", type=str, default=None)
    parser.add_argument("--current", type=str, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args()

    report = detect_drift(args.reference, args.current, args.threshold, args.output_dir)
    print(
        f"drift engine={report['engine']} score={report['drift_score']:.3f} threshold={report['threshold']} "
        f"drift_detected={report['drift_detected']}"
    )
    if report["drift_detected"]:
        print(f"drifted features: {report['drifted_features']}")


if __name__ == "__main__":
    main()
