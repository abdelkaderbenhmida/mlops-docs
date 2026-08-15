"""Model training with MLflow tracking and registration.

Trains a RandomForest churn classifier on the feature store snapshot:
1. start an MLflow run and log hyperparameters
2. train + evaluate on a held-out test split
3. log metrics, confusion matrix, feature importances and the fitted
   feature transformer config as artifacts
4. register the model in the MLflow Model Registry (stage: Staging)
5. persist a local model.pkl (DVC output) and metrics.json (DVC metrics)
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
import mlflow  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split  # noqa: E402

from src.features.build_features import TARGET_FEATURE, FEATURE_ORDER  # noqa: E402

DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"
DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config.json"
DEFAULT_MODEL_OUTPUT = PROJECT_ROOT / "models" / "model.pkl"
DEFAULT_METRICS = PROJECT_ROOT / "metrics.json"
DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"
MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "churn_model")
DEFAULT_PARAMS = {
    "n_estimators": 300,
    "max_depth": 15,
    "min_samples_leaf": 3,
    "max_features": "sqrt",
    "class_weight": "balanced",
    "random_state": 42,
}


def _save_confusion_matrix(y_true, y_pred, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=ax, cmap="Blues")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


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
    y = features[TARGET_FEATURE].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
    }

    run_id = None
    try:
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlruns/mlflow.db"))
        with mlflow.start_run(run_name="churn-training") as run:
            run_id = run.info.run_id
            mlflow.set_tag("model_name", model_name)
            mlflow.set_tag("git_commit", os.environ.get("GIT_COMMIT", "unknown"))
            mlflow.set_tag("data_version", os.environ.get("DVC_DATA_VERSION", "unknown"))
            mlflow.log_params(params)
            mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, float)})

            confusion_path = PROJECT_ROOT / "models" / "artifacts" / "confusion_matrix.png"
            importance_path = PROJECT_ROOT / "models" / "artifacts" / "feature_importances.png"
            confusion_path.parent.mkdir(parents=True, exist_ok=True)
            _save_confusion_matrix(y_test, y_pred, confusion_path)
            _save_feature_importances(model, list(X.columns), importance_path)
            mlflow.log_artifact(str(confusion_path))
            mlflow.log_artifact(str(importance_path))
            mlflow.log_artifact(str(config_path))

            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                registered_model_name=model_name,
                input_example=X_test.iloc[[0]],
            )
            try:
                client = mlflow.tracking.MlflowClient()
                version = client.get_latest_versions(model_name, stages=["None"])[0].version
                client.transition_model_version_stage(model_name, version, stage="Staging")
                mlflow.set_tag("registry_version", version)
                print(f"registered {model_name} version {version} -> Staging")
            except Exception as exc:  # noqa: BLE001
                print(f"warning: registry transition failed: {exc}")
    except Exception as exc:  # noqa: BLE001
        print(f"warning: MLflow tracking failed (continuing offline): {exc}")

    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_output)
    (PROJECT_ROOT / "metrics.json").write_text(json.dumps(metrics, indent=2))

    reference = X_test.copy()
    reference["prediction"] = y_prob
    reference["label"] = y_test.values
    DEFAULT_REFERENCE.parent.mkdir(parents=True, exist_ok=True)
    reference.to_csv(DEFAULT_REFERENCE, index=False)

    return {"run_id": run_id, "model_name": model_name, "metrics": metrics, "model_output": str(model_output)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train and register the churn model.")
    parser.add_argument("--data", type=str, default=None)
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--model-output", type=str, default=None)
    parser.add_argument("--model-name", type=str, default=MODEL_NAME)
    parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS["n_estimators"])
    parser.add_argument("--max-depth", type=int, default=DEFAULT_PARAMS["max_depth"])
    parser.add_argument("--min-samples-leaf", type=int, default=DEFAULT_PARAMS["min_samples_leaf"])
    parser.add_argument("--seed", type=int, default=DEFAULT_PARAMS["random_state"])
    args = parser.parse_args()

    params = {
        "n_estimators": args.n_estimators,
        "max_depth": args.max_depth,
        "min_samples_leaf": args.min_samples_leaf,
        "class_weight": DEFAULT_PARAMS["class_weight"],
        "random_state": args.seed,
    }
    result = train_model(args.data, args.config, args.model_output, args.model_name, params)
    print(f"run_id={result['run_id']} f1={result['metrics']['f1']:.4f} roc_auc={result['metrics']['roc_auc']:.4f}")


if __name__ == "__main__":
    main()
