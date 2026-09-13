# TODO: high - Add data validation before training
# TODO: medium - Implement hyperparameter logging
# TODO: low - Add model explainability integration
"""DAG: full training pipeline.

Runs the complete model lifecycle on the current data snapshot:
validate -> preprocess -> build_features -> train -> evaluate -> promote -> notify.
The MLflow run_id produced by training is passed to the evaluation task via XCom.
"""

from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from airflow import DAG

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocessing import preprocess  # noqa: E402
from src.data.validation import validate  # noqa: E402
from src.features.build_features import build_features  # noqa: E402
from src.models.evaluate import evaluate  # noqa: E402
from src.models.promote import promote_candidate  # noqa: E402
from src.models.train import train_model  # noqa: E402
from src.monitoring.alerting import send_alert  # noqa: E402

DAG_ID = "training_pipeline"
DEFAULT_ARGS = {
    "owner": "mlops",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": lambda context: send_alert(
        f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", severity="critical"
    ),
}
dag = DAG(
    dag_id=DAG_ID,
    default_args=DEFAULT_ARGS,
    schedule_interval="@weekly",
    start_date=days_ago(2),
    catchup=False,
    tags=["training", "mlflow"],
    doc_md=(
        "Validates data, rebuilds features, trains and registers a new churn model, "
        "then promotes it if it passes the gates."
    ),
)


def _validate() -> str:
    summary = validate()
    if summary["failed"]:
        raise RuntimeError(f"data validation failed: {summary['failed']} expectation(s)")
    return f"validation passed {summary['passed']}/{summary['total']}"


def _preprocess() -> str:
    df = preprocess()
    return f"preprocessed {len(df)} rows"


def _build_features() -> str:
    features = build_features()
    return f"built {features.shape[0]} rows x {features.shape[1]} features"


def _train(**context) -> str:
    result = train_model()
    context["task_instance"].xcom_push(key="run_id", value=result["run_id"])
    context["task_instance"].xcom_push(key="r2", value=result["metrics"]["r2"])
    return f"training completed run_id={result['run_id']} r2={result['metrics']['r2']:.4f}"


def _evaluate(**context) -> str:
    run_id = context["task_instance"].xcom_pull(task_ids="train_model", key="run_id")
    report = evaluate(run_id=run_id)
    if not report["gates_passed"]:
        raise RuntimeError("evaluation gates not met; stopping before promotion")
    return f"evaluation passed r2={report['metrics']['r2']:.4f}"


def _promote() -> str:
    production = promote_candidate()
    return f"promoted version {production['version']} to production"


def _notify(**context) -> str:
    r2 = context["task_instance"].xcom_pull(task_ids="train_model", key="r2")
    send_alert(f"training_pipeline completed | r2={r2:.4f}", severity="info", dag=DAG_ID)
    return "notification sent"


validate_data = PythonOperator(task_id="validate_data", python_callable=_validate, dag=dag)
preprocess_data = PythonOperator(task_id="preprocess", python_callable=_preprocess, dag=dag)
build_features_task = PythonOperator(task_id="build_features", python_callable=_build_features, dag=dag)
train_task = PythonOperator(task_id="train_model", python_callable=_train, dag=dag)
evaluate_task = PythonOperator(task_id="evaluate_model", python_callable=_evaluate, dag=dag)
promote_task = PythonOperator(task_id="promote_model", python_callable=_promote, dag=dag)
notify_task = PythonOperator(task_id="notify_team", python_callable=_notify, dag=dag)

validate_data >> preprocess_data >> build_features_task >> train_task >> evaluate_task >> promote_task >> notify_task
