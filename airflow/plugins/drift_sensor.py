# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Airflow plugin: drift sensor + shared DAG helpers.

`DriftDetectedSensor` polls the drift report produced by
src/monitoring/drift_detection.py and succeeds as soon as drift is detected,
which is how the retraining loop is triggered.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from airflow.plugins_manager import AirflowPlugin
from airflow.sensors.base import BaseSensorOperator


class DriftDetectedSensor(BaseSensorOperator):
    template_fields = ("drift_report_path",)

    def __init__(self, drift_report_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        default = Path(os.environ.get("DRIFT_REPORT_PATH", "data/monitoring/drift_report.json"))
        self.drift_report_path = drift_report_path or str(default)

    def poke(self, context: dict) -> bool:
        report = Path(self.drift_report_path)
        if not report.exists():
            self.log.info("drift report %s not found yet", report)
            return False
        with report.open() as fh:
            payload = json.load(fh)
        detected = bool(payload.get("drift_detected", False))
        self.log.info("drift_detected=%s score=%s", detected, payload.get("drift_score"))
        return detected


class DriftAlertPlugin(AirflowPlugin):
    name = "mlops_drift_plugin"
    sensors = [DriftDetectedSensor]
