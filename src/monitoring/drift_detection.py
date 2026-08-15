"""Model and data drift detection with Evidently AI.

Compares the current production window (features + predictions logged by the
API) against the training reference snapshot:
- data drift per feature (Kolmogorov-Smirnov for numeric, chi-square /
  Jensen-Shannon for categorical)
- prediction drift (distribution of predicted probabilities)
- global drift score = fraction of drifted features

If the score exceeds the configured threshold (DRIFT_THRESHOLD, default 0.3),
`drift_detected` is set to true — the signal that triggers the Airflow
`retraining_pipeline`. When Evidently is not installed, a scipy-based
Kolmogorov-Smirnov fallback is used so the check still runs.
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

NUMERIC_FEATURES = ["Tenure", "MonthlyCharges", "TotalCharges", "charges_per_tenure", "tenure_years", "num_services"]
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


def _features_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in NUMERIC_FEATURES + CATEGORICAL_FEATURES if c in df.columns]


def _evidently_report(reference: pd.DataFrame, current: pd.DataFrame) -> dict:
    from evidently import ColumnMapping
    from evidently.metric_preset import DataDriftPreset
    from evidently.metrics import ColumnDriftMetric
    from evidently.report import Report

    features = _features_columns(reference)
    column_mapping = ColumnMapping(
        prediction="prediction" if "prediction" in reference.columns else None,
        target="label" if "label" in reference.columns else None,
        numerical_features=[c for c in NUMERIC_FEATURES if c in features],
        categorical_features=[c for c in CATEGORICAL_FEATURES if c in features],
    )

    metrics: list = [DataDriftPreset()]
    if "prediction" in reference.columns:
        metrics.append(ColumnDriftMetric("prediction"))

    report = Report(metrics=metrics)
    report.run(reference_data=reference, current_data=current, column_mapping=column_mapping)

    return report.as_dict()


def _extract_drift_score(payload: dict) -> tuple[float, dict]:
    drifted = 0
    total = 0
    per_column: dict[str, dict] = {}

    def walk(node: dict) -> None:
        nonlocal drifted, total
        result = node.get("result", {})
        if isinstance(result, dict):
            by_column = result.get("drift_by_columns") or result.get("drift_by_column")
            if isinstance(by_column, dict):
                for col, info in by_column.items():
                    detected = bool(info.get("drift_detected", False))
                    stats = info.get("drift_stat_test", {})
                    per_column[col] = {
                        "drift_detected": detected,
                        "test": stats.get("drift_stat_test_name", stats.get("name", "unknown")),
                        "score": stats.get("drift_score"),
                    }
                    drifted += int(detected)
                    total += 1
            if "number_of_drifted_columns" in result and "number_of_columns" in result:
                drifted = int(result["number_of_drifted_columns"])
                total = int(result["number_of_columns"])
        for value in node.values():
            if isinstance(value, dict):
                walk(value)
        for value in node.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        walk(item)

    walk(payload)
    score = drifted / total if total else 0.0
    return score, per_column


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

    try:
        payload = _evidently_report(reference, current)
        engine = "evidently"
    except Exception:  # noqa: BLE001
        payload = {}
        engine = "scipy-fallback"

    drift_score, per_column = _extract_drift_score(payload) if payload else _ks_fallback(reference, current)
    if not per_column and engine == "evidently":
        drift_score, per_column = _ks_fallback(reference, current)
        engine = "scipy-fallback"

    report = {
        "engine": engine,
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

    if engine == "evidently":
        try:
            from evidently import ColumnMapping
            from evidently.metric_preset import DataDriftPreset
            from evidently.report import Report

            html_report = Report(metrics=[DataDriftPreset()])
            html_report.run(
                reference_data=reference,
                current_data=current,
                column_mapping=ColumnMapping(
                    prediction="prediction" if "prediction" in reference.columns else None,
                    target="label" if "label" in reference.columns else None,
                ),
            )
            html_report.save_html(str(output_dir / "drift_report.html"))
        except Exception:  # noqa: BLE001  # nosec B110 - html report is best effort
            pass

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
