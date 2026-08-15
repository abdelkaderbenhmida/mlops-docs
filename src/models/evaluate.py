"""Model evaluation and validation gate.

Loads a candidate model (from an MLflow run or a local pickle), evaluates it
on the held-out test features and compares it against configured quality
thresholds. Writes a JSON evaluation report; exits non-zero when the candidate
does not meet the gate so the pipeline stops before promotion.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.features.build_features import TARGET_FEATURE, FEATURE_ORDER

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"
DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config.json"
DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"
EVALUATION_DIR = PROJECT_ROOT / "models" / "evaluation"
LATEST_REPORT = EVALUATION_DIR / "latest_report.json"

DEFAULT_THRESHOLDS = {"min_f1": 0.35, "min_accuracy": 0.70, "min_roc_auc": 0.72}


def _resolve_model(model_uri: str | None, run_id: str | None):
    if run_id:
        try:
            import mlflow

            return mlflow.sklearn.load_model(f"runs:/{run_id}/model")
        except Exception:  # nosec B110 - fallback to next source
            pass
    if model_uri:
        try:
            import mlflow

            return mlflow.sklearn.load_model(model_uri)
        except Exception:  # nosec B110 - fallback to local pickle
            pass
    if Path(DEFAULT_LOCAL_MODEL).exists():
        return joblib.load(DEFAULT_LOCAL_MODEL)
    raise FileNotFoundError("No candidate model found (run_id, model_uri or models/model.pkl)")


def _load_test_set(data_path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    """Prefer the held-out test set written by train.py (data/monitoring/reference.csv);
    fall back to the full feature dataset when it is not available."""
    reference = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"
    if reference.exists():
        df = pd.read_csv(reference)
        return df[FEATURE_ORDER], df["label"].astype(int)

    data_path = Path(data_path or DEFAULT_DATA)
    if not data_path.exists():
        raise FileNotFoundError(f"Feature dataset not found: {data_path}")
    features = pd.read_parquet(data_path)
    if len(features) > 5000:
        X_test = features.sample(n=5000, random_state=42)[FEATURE_ORDER]
        y_test = features.loc[X_test.index, TARGET_FEATURE].astype(int)
        return X_test, y_test
    return features[FEATURE_ORDER], features[TARGET_FEATURE].astype(int)


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    return {
        "f1": float(f1_score(y_test, y_pred)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "n_samples": int(len(y_test)),
    }


def evaluate(
    data_path: str | Path | None = None,
    model_uri: str | None = None,
    run_id: str | None = None,
    thresholds: dict | None = None,
) -> dict:
    X_test, y_test = _load_test_set(data_path)

    model = _resolve_model(model_uri, run_id)
    metrics = evaluate_model(model, X_test, y_test)

    thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    gates = {
        "min_f1": {"metric": "f1", "value": thresholds["min_f1"]},
        "min_accuracy": {"metric": "accuracy", "value": thresholds["min_accuracy"]},
        "min_roc_auc": {"metric": "roc_auc", "value": thresholds["min_roc_auc"]},
    }
    gates_passed = all(metrics[gate["metric"]] >= gate["value"] for gate in gates.values())

    report = {
        "model_uri": model_uri or (f"runs:/{run_id}/model" if run_id else "local:models/model.pkl"),
        "run_id": run_id,
        "metrics": metrics,
        "thresholds": thresholds,
        "gates": gates,
        "gates_passed": gates_passed,
    }
    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
    with LATEST_REPORT.open("w") as fh:
        json.dump(report, fh, indent=2)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a candidate model against quality gates.")
    parser.add_argument("--data", type=str, default=None)
    parser.add_argument("--model-uri", type=str, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--min-f1", type=float, default=None)
    parser.add_argument("--min-accuracy", type=float, default=None)
    parser.add_argument("--min-roc-auc", type=float, default=None)
    args = parser.parse_args()

    thresholds = {}
    for name, cli_arg in (("min_f1", args.min_f1), ("min_accuracy", args.min_accuracy), ("min_roc_auc", args.min_roc_auc)):
        if cli_arg is not None:
            thresholds[name] = cli_arg

    report = evaluate(args.data, args.model_uri, args.run_id, thresholds)
    print(f"evaluation: f1={report['metrics']['f1']:.4f} accuracy={report['metrics']['accuracy']:.4f} "
          f"roc_auc={report['metrics']['roc_auc']:.4f} gates_passed={report['gates_passed']}")
    if not report["gates_passed"]:
        print(f"evaluation gates not met: {json.dumps(report['gates'])}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
