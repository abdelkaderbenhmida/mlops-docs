# TODO: high - Add data validation before training
# TODO: medium - Implement hyperparameter logging
# TODO: low - Add model explainability integration
"""Model training for demand forecasting with MLflow tracking.

Trains an XGBRegressor (GPU-accelerated with CPU fallback) on the feature store snapshot:
1. start an MLflow run and log hyperparameters
2. train + evaluate on a held-out test split
3. log metrics, feature importances, and model artifacts
4. register the model in the MLflow Model Registry
5. persist local model.pkl and metrics.json
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
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import mlflow.xgboost  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from xgboost import XGBRegressor  # noqa: E402

import mlflow  # noqa: E402
from src.features.build_features import FEATURE_ORDER, TARGET_FEATURE  # noqa: E402

DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"
DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config.json"
DEFAULT_MODEL_OUTPUT = PROJECT_ROOT / "models" / "model.pkl"
DEFAULT_METRICS = PROJECT_ROOT / "metrics.json"
DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"
DEFAULT_ARTIFACT_DIR = PROJECT_ROOT / "models" / "artifacts"
MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "demand_model")

# Local fallback tracking store: the repository's sqlite backend (the same one
# promote.py uses), not a temp dir that disappears on reboot. Docker/K8s
# override this with MLFLOW_TRACKING_URI pointing at the MLflow server.
DEFAULT_TRACKING_URI = f"sqlite:///{PROJECT_ROOT / 'mlruns' / 'mlflow.db'}"

DEFAULT_PARAMS = {
    "n_estimators": 300,
    "max_depth": 15,
    "learning_rate": 0.05,
    "min_child_weight": 5,
    "colsample_bytree": 0.9,
    "subsample": 0.9,
    "random_state": 42,
    "n_jobs": -1,
}


def _to_xgb_params(params: dict) -> dict:
    """Map sklearn-style hyperparameter names to XGBoost equivalents."""
    out = {}
    for key, value in params.items():
        if key == "min_samples_leaf":
            out["min_child_weight"] = int(value)
        elif key == "max_features":
            out["colsample_bytree"] = 0.8 if value == "sqrt" else float(value)
        else:
            out[key] = value
    return out


def _build_model(params: dict, *, gpu: bool) -> XGBRegressor:
    kwargs = _to_xgb_params(params)
    if gpu:
        kwargs["device"] = "cuda"
        kwargs["tree_method"] = "hist"
    else:
        kwargs["device"] = "cpu"
        kwargs["tree_method"] = "hist"
    return XGBRegressor(**kwargs)


def _save_feature_importances(model, feature_names: list[str], path: Path) -> None:
    importances = model.feature_importances_
    order = np.argsort(importances)[::-1]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh([feature_names[i] for i in order][:20], importances[order][:20])
    ax.invert_yaxis()
    ax.set_xlabel("feature importance")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _save_predictions_plot(y_true, y_pred, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(y_true, y_pred, alpha=0.3, s=10)
    lims = [0, max(y_true.max(), y_pred.max()) * 1.05]
    ax.plot(lims, lims, "--", color="red", linewidth=1, label="perfect")
    ax.set_xlabel("actual units_sold")
    ax.set_ylabel("predicted units_sold")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def train_model(
    data_path: str | Path | None = None,
    config_path: str | Path | None = None,
    model_output: str | Path | None = None,
    model_name: str = MODEL_NAME,
    params: dict | None = None,
) -> dict:
    data_path = Path(data_path or DEFAULT_DATA)
    config_path = Path(config_path or DEFAULT_CONFIG)
    model_output = Path(model_output or DEFAULT_MODEL_OUTPUT)
    params = {**DEFAULT_PARAMS, **(params or {})}

    if not data_path.exists():
        raise FileNotFoundError(f"Feature dataset not found: {data_path}")

    features = pd.read_parquet(data_path)
    if TARGET_FEATURE not in features.columns:
        raise ValueError(f"Target column '{TARGET_FEATURE}' missing from feature dataset")

    X = features[FEATURE_ORDER]
    y = features[TARGET_FEATURE].astype(float)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    try:
        model = _build_model(params, gpu=True)
        model.fit(X_train, y_train)
    except Exception as exc:  # noqa: BLE001
        print(f"warning: GPU training unavailable ({exc}); falling back to CPU (tree_method=hist)")
        model = _build_model(params, gpu=False)
        model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae = float(mean_absolute_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))
    nonzero = y_test.values != 0
    mape = float(np.mean(np.abs((y_test.values[nonzero] - y_pred[nonzero]) / y_test.values[nonzero])) * 100)

    metrics = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "mape": mape,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
    }

    run_id = None
    try:
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", DEFAULT_TRACKING_URI))
        with mlflow.start_run(run_name="demand-forecasting-training") as run:
            run_id = run.info.run_id
            mlflow.set_tag("model_name", model_name)
            mlflow.set_tag("task", "demand_forecasting")
            mlflow.log_params(params)
            mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, float)})

            importance_path = DEFAULT_ARTIFACT_DIR / "feature_importances.png"
            pred_path = DEFAULT_ARTIFACT_DIR / "predictions_vs_actual.png"
            importance_path.parent.mkdir(parents=True, exist_ok=True)
            _save_feature_importances(model, list(X.columns), importance_path)
            _save_predictions_plot(y_test.values, y_pred, pred_path)
            mlflow.log_artifact(str(importance_path))
            mlflow.log_artifact(str(pred_path))
            mlflow.log_artifact(str(config_path))

            mlflow.xgboost.log_model(
                model,
                artifact_path="model",
                registered_model_name=model_name,
                input_example=X_test.iloc[[0]],
            )
    except Exception as exc:  # noqa: BLE001
        print(f"warning: MLflow tracking failed (continuing offline): {exc}")

    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_output)
    DEFAULT_METRICS.write_text(json.dumps(metrics, indent=2))

    reference = X_test.copy()
    reference["prediction"] = y_pred
    reference[TARGET_FEATURE] = y_test.values
    DEFAULT_REFERENCE.parent.mkdir(parents=True, exist_ok=True)
    reference.to_csv(DEFAULT_REFERENCE, index=False)

    return {"run_id": run_id, "model_name": model_name, "metrics": metrics, "model_output": str(model_output)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train and register the demand forecasting model.")
    parser.add_argument("--data", type=str, default=None)
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--model-output", type=str, default=None)
    parser.add_argument("--model-name", type=str, default=MODEL_NAME)
    parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS["n_estimators"])
    parser.add_argument("--max-depth", type=int, default=DEFAULT_PARAMS["max_depth"])
    parser.add_argument("--min-samples-leaf", type=int, default=DEFAULT_PARAMS["min_child_weight"])
    parser.add_argument("--seed", type=int, default=DEFAULT_PARAMS["random_state"])
    args = parser.parse_args()

    params = {
        "n_estimators": args.n_estimators,
        "max_depth": args.max_depth,
        "min_samples_leaf": args.min_samples_leaf,
        "random_state": args.seed,
    }
    result = train_model(args.data, args.config, args.model_output, args.model_name, params)
    print(f"run_id={result['run_id']} rmse={result['metrics']['rmse']:.2f} r2={result['metrics']['r2']:.4f} mape={result['metrics']['mape']:.2f}%")


if __name__ == "__main__":
    main()
