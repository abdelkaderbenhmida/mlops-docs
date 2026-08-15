"""Promotion logic: Staging -> Production in the MLflow Model Registry.

A candidate (the latest evaluation report) is promoted only if:
- it passed the evaluation gates (evaluate.py), and
- it beats the currently deployed production model on the same test set.

The previous production version is archived. The promotion is recorded in
models/evaluation/production_report.json so the API and dashboards can report
which model is live and why.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LATEST_REPORT = PROJECT_ROOT / "models" / "evaluation" / "latest_report.json"
PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "production_report.json"

MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "churn_model")


def _client():
    import mlflow

    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlruns/mlflow.db"))
    return mlflow.tracking.MlflowClient()


def current_production(model_name: str = MODEL_NAME) -> dict | None:
    try:
        client = _client()
        versions = client.get_latest_versions(model_name, stages=["Production"])
        if not versions:
            return None
        version = versions[0]
        report = {}
        if PRODUCTION_REPORT.exists():
            report = json.loads(PRODUCTION_REPORT.read_text())
        return {"version": int(version.version), "run_id": version.run_id, "report": report}
    except Exception as exc:  # noqa: BLE001
        print(f"warning: could not read production model from registry: {exc}")
        return None


def promote_candidate(model_name: str = MODEL_NAME, force: bool = False) -> dict:
    if not LATEST_REPORT.exists():
        raise FileNotFoundError(f"No candidate report found at {LATEST_REPORT}. Run evaluate.py first.")

    candidate = json.loads(LATEST_REPORT.read_text())
    if not candidate.get("gates_passed") and not force:
        raise RuntimeError("Candidate did not pass evaluation gates; refusing to promote (use --force to override).")

    client = _client()
    versions = client.get_latest_versions(model_name, stages=["Staging"])
    if not versions:
        raise RuntimeError(f"No Staging version found for model '{model_name}' in the registry.")
    version = versions[0]

    production = current_production(model_name)
    if production and not force:
        candidate_f1 = candidate["metrics"]["f1"]
        production_f1 = production["report"].get("metrics", {}).get("f1")
        if production_f1 is not None and candidate_f1 < production_f1:
            raise RuntimeError(
                f"Candidate f1={candidate_f1:.4f} < production f1={production_f1:.4f}; refusing to promote "
                "(use --force to override)."
            )

    for previous in client.search_model_versions(f"name='{model_name}'"):
        if previous.current_stage == "Production":
            client.transition_model_version_stage(model_name, previous.version, stage="Archived")
            print(f"archived {model_name} version {previous.version}")

    client.transition_model_version_stage(model_name, version.version, stage="Production")
    client.update_model_version(
        model_name,
        version.version,
        description=f"Promoted by promote.py | f1={candidate['metrics']['f1']:.4f} | run={candidate.get('run_id')}",
    )

    production_report = {
        "model_name": model_name,
        "version": int(version.version),
        "run_id": version.run_id or candidate.get("run_id"),
        "promoted_at": None,
        "metrics": candidate["metrics"],
    }
    PRODUCTION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    PRODUCTION_REPORT.write_text(json.dumps(production_report, indent=2))

    print(f"promoted {model_name} version {version.version} -> Production")
    return production_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote the latest validated model to Production.")
    parser.add_argument("--model-name", type=str, default=MODEL_NAME)
    parser.add_argument("--force", action="store_true", help="Skip production comparison gate")
    args = parser.parse_args()

    try:
        report = promote_candidate(args.model_name, args.force)
        print(json.dumps(report, indent=2))
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"promotion failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
