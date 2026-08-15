"""DAG: retraining triggered by drift detection.

Runs daily. The `check_drift` task short-circuits the pipeline: if no drift
was detected by Evidently since the last run, nothing is retrained. On drift,
the full loop executes: preprocess -> features -> train -> evaluate ->
promote-if-better -> notify. Promotion only happens when the candidate beats
the current production model on the same test set.
"""

from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.utils.dates import days_ago

from airflow import DAG

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocessing import preprocess  # noqa: E402
from src.features.build_features import build_features  # noqa: E402
from src.models.evaluate import evaluate  # noqa: E402
from src.models.promote import promote_candidate  # noqa: E402
from src.models.train import train_model  # noqa: E402
from src.monitoring.alerting import send_alert  # noqa: E402
from src.monitoring.drift_detection import detect_drift  # noqa: E402

DAG_ID = "retraining_pipeline"
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
    schedule_interval="@daily",
    start_date=days_ago(2),
    catchup=False,
    tags=["retraining", "drift"],
    doc_md="Retrains the model when Evidently detects drift on the production data.",
)


def _check_drift() -> bool:
    report = detect_drift()
    if report["drift_detected"]:
        send_alert(
            "drift detected "
            f"(score={report['drift_score']:.3f}, threshold={report['threshold']}) - triggering retraining",
            severity="warning",
            dag=DAG_ID,
        )
        return True
    return False


def _preprocess() -> str:
    df = preprocess()
    return f"preprocessed {len(df)} rows"


def _build_features() -> str:
    features = build_features()
    return f"built {features.shape[0]} rows x {features.shape[1]} features"


def _train(**context) -> str:
    result = train_model()
    context["task_instance"].xcom_push(key="run_id", value=result["run_id"])
    return f"retraining completed run_id={result['run_id']} f1={result['metrics']['f1']:.4f}"


def _evaluate(**context) -> str:
    run_id = context["task_instance"].xcom_pull(task_ids="train_model", key="run_id")
    report = evaluate(run_id=run_id)
    if not report["gates_passed"]:
        raise RuntimeError("evaluation gates not met; stopping before promotion")
    return f"evaluation passed f1={report['metrics']['f1']:.4f}"


def _promote() -> str:
    production = promote_candidate()
    send_alert(
        f"retraining promoted model version {production['version']} to production "
        f"(f1={production['metrics']['f1']:.4f})",
        severity="info",
        dag=DAG_ID,
    )
    return f"promoted version {production['version']}"


def _notify() -> str:
    send_alert("retraining_pipeline completed", severity="info", dag=DAG_ID)
    return "notification sent"


check_drift = ShortCircuitOperator(task_id="check_drift", python_callable=_check_drift, dag=dag)
preprocess_task = PythonOperator(task_id="preprocess", python_callable=_preprocess, dag=dag)
build_features_task = PythonOperator(task_id="build_features", python_callable=_build_features, dag=dag)
train_task = PythonOperator(task_id="train_model", python_callable=_train, dag=dag)
evaluate_task = PythonOperator(task_id="evaluate_model", python_callable=_evaluate, dag=dag)
promote_task = PythonOperator(task_id="promote_model", python_callable=_promote, dag=dag)
notify_task = PythonOperator(task_id="notify_team", python_callable=_notify, dag=dag)

check_drift >> preprocess_task >> build_features_task >> train_task >> evaluate_task >> promote_task >> notify_task
