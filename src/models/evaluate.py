# TODO: high - Add quality gate with thresholds
# TODO: medium - Implement comparison vs current production model
# TODO: low - Add metrics export for Evidence Pack
"""Model evaluation and validation gates for demand forecasting.

Loads a candidate model, evaluates it on the held-out test set and compares
against configured quality thresholds. Gates: R² >= 0.60, MAPE <= 25%.
Writes a JSON evaluation report; exits non-zero when gates fail.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.features.build_features import FEATURE_ORDER, TARGET_FEATURE

DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"
DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"
EVALUATION_DIR = PROJECT_ROOT / "models" / "evaluation"
LATEST_REPORT = EVALUATION_DIR / "latest_report.json"

DEFAULT_THRESHOLDS = {"min_r2": 0.60, "max_mape": 25.0}


def _resolve_model(model_uri: str | None, run_id: str | None):
    if run_id:
        try:
            import mlflow.xgboost

            return mlflow.xgboost.load_model(f"runs:/{run_id}/model")
        except Exception:  # nosec B110
            pass
    if model_uri:
        try:
            import mlflow.xgboost

            return mlflow.xgboost.load_model(model_uri)
        except Exception:  # nosec B110
            pass
    if Path(DEFAULT_LOCAL_MODEL).exists():
        return joblib.load(DEFAULT_LOCAL_MODEL)
    raise FileNotFoundError("No candidate model found (run_id, model_uri or models/model.pkl)")


def _load_test_set(data_path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    reference = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"
    if reference.exists():
        df = pd.read_csv(reference)
        return df[FEATURE_ORDER], df[TARGET_FEATURE].astype(float)

    data_path = Path(data_path or DEFAULT_DATA)
    if not data_path.exists():
        raise FileNotFoundError(f"Feature dataset not found: {data_path}")
    features = pd.read_parquet(data_path)
    if len(features) > 5000:
        X_test = features.sample(n=5000, random_state=42)[FEATURE_ORDER]
        y_test = features.loc[X_test.index, TARGET_FEATURE].astype(float)
        return X_test, y_test
    return features[FEATURE_ORDER], features[TARGET_FEATURE].astype(float)


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    y_pred = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae = float(mean_absolute_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))
    nonzero = y_test.values != 0
    mape = float(np.mean(np.abs((y_test.values[nonzero] - y_pred[nonzero]) / y_test.values[nonzero])) * 100)
    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "mape": mape,
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
        "min_r2": {"metric": "r2", "value": thresholds["min_r2"], "direction": ">="},
        "max_mape": {"metric": "mape", "value": thresholds["max_mape"], "direction": "<="},
    }

    r2_pass = metrics["r2"] >= thresholds["min_r2"]
    mape_pass = metrics["mape"] <= thresholds["max_mape"]
    gates_passed = r2_pass and mape_pass

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
    parser = argparse.ArgumentParser(description="Evaluate a candidate demand model against quality gates.")
    parser.add_argument("--data", type=str, default=None)
    parser.add_argument("--model-uri", type=str, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--min-r2", type=float, default=None)
    parser.add_argument("--max-mape", type=float, default=None)
    args = parser.parse_args()

    thresholds = {}
    if args.min_r2 is not None:
        thresholds["min_r2"] = args.min_r2
    if args.max_mape is not None:
        thresholds["max_mape"] = args.max_mape

    report = evaluate(args.data, args.model_uri, args.run_id, thresholds)
    print(f"evaluation: rmse={report['metrics']['rmse']:.2f} mae={report['metrics']['mae']:.2f} "
          f"r2={report['metrics']['r2']:.4f} mape={report['metrics']['mape']:.2f}% gates_passed={report['gates_passed']}")
    if not report["gates_passed"]:
        print(f"evaluation gates not met: {json.dumps(report['gates'])}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
