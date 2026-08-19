"""Model loading for the demand forecasting inference API.

Loads the production model once at startup from the MLflow Model Registry
and applies the same fitted feature transformer that was used at training time.
Falls back to a local pickle when the registry is unreachable.
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

import joblib
import pandas as pd

from src.features.build_features import FeatureTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "data" / "features" / "features_config.json"
DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"

MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "demand_model")


class ModelBundle:
    def __init__(
        self,
        model,
        transformer: FeatureTransformer,
        model_name: str,
        version: str,
        run_id: str | None = None,
    ):
        self.model = model
        self.transformer = transformer
        self.model_name = model_name
        self.version = version
        self.run_id = run_id

    def predict(self, df: pd.DataFrame) -> list[float]:
        features = self.transformer.transform(df)
        return self.model.predict(features).tolist()


class ModelLoader:
    def __init__(self, model_name: str = MODEL_NAME, config_path: str | Path | None = None):
        self.model_name = model_name
        self.config_path = Path(config_path or os.environ.get("FEATURES_CONFIG_PATH") or DEFAULT_CONFIG_PATH)
        self._bundle: ModelBundle | None = None
        self._lock = threading.Lock()
        self._loaded_at: float = 0.0

    def load(self) -> ModelBundle:
        with self._lock:
            bundle, version, run_id = self._load_model()
            self._bundle = bundle
            self._bundle.version = version
            self._bundle.run_id = run_id
            self._loaded_at = time.time()
            return self._bundle

    def _load_model(self) -> tuple[ModelBundle, str, str | None]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Features config not found: {self.config_path}")

        config = json.loads(self.config_path.read_text())
        transformer = FeatureTransformer.from_config(config)

        explicit_uri = os.environ.get("MLFLOW_MODEL_URI")
        if explicit_uri:
            try:
                import mlflow
                mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "file:///tmp/p4mlruns"))
                model = mlflow.sklearn.load_model(explicit_uri)
                return ModelBundle(model, transformer, self.model_name, explicit_uri, None), explicit_uri, None
            except Exception:  # noqa: BLE001
                pass

        registry_uri = f"models:/{self.model_name}/Production"
        try:
            import mlflow
            mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "file:///tmp/p4mlruns"))
            client = mlflow.tracking.MlflowClient()
            model = mlflow.sklearn.load_model(registry_uri)
            version = client.get_latest_versions(self.model_name, stages=["Production"])[0]
            return (
                ModelBundle(model, transformer, self.model_name, str(version.version), version.run_id),
                str(version.version),
                version.run_id,
            )
        except Exception:  # noqa: BLE001
            pass

        if DEFAULT_LOCAL_MODEL.exists():
            model = joblib.load(DEFAULT_LOCAL_MODEL)
            return ModelBundle(model, transformer, self.model_name, "local"), "local", None

        raise RuntimeError(f"Model '{self.model_name}' unavailable: no registry, explicit URI or local pickle found")

    def get_bundle(self) -> ModelBundle:
        if self._bundle is None:
            return self.load()
        interval = int(os.environ.get("RELOAD_INTERVAL", "0") or 0)
        if interval > 0 and time.time() - self._loaded_at > interval:
            try:
                return self.load()
            except Exception:  # noqa: BLE001
                return self._bundle
        return self._bundle


loader = ModelLoader()
