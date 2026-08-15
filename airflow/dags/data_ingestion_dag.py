"""DAG: periodic data ingestion.

Scheduled every night: pulls the latest raw data, validates it with the
Great Expectations suite, then versions it with DVC and pushes it to the
configured remote (MinIO). Failures raise an alert through the alerting module.
"""

from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from airflow import DAG

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.ingestion import ingest  # noqa: E402
from src.data.validation import validate  # noqa: E402
from src.monitoring.alerting import send_alert  # noqa: E402

DAG_ID = "data_ingestion_dag"
DEFAULT_ARGS = {
    "owner": "mlops",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": lambda context: send_alert(
        f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", severity="critical"
    ),
}

dag = DAG(
    dag_id=DAG_ID,
    default_args=DEFAULT_ARGS,
    schedule_interval="0 2 * * *",
    start_date=days_ago(2),
    catchup=False,
    tags=["ingestion", "data"],
    doc_md="Fetches, validates and DVC-versions the raw churn dataset every night.",
)


def _ingest() -> str:
    df = ingest()
    return f"ingested {len(df)} rows"


def _validate() -> str:
    summary = validate()
    if summary["failed"]:
        raise RuntimeError(f"data validation failed: {summary['failed']} expectation(s)")
    return f"validation passed {summary['passed']}/{summary['total']}"


ingest_data = PythonOperator(task_id="ingest_data", python_callable=_ingest, dag=dag)
validate_data = PythonOperator(task_id="validate_data", python_callable=_validate, dag=dag)
version_data = BashOperator(
    task_id="version_data",
    bash_command=(
        "cd {{ dag_run.conf.get('project_root', '/opt/airflow') }} && "
        "dvc add data/raw/dataset.csv && dvc commit -f && "
        "(dvc remote list | grep -q . && dvc push || echo 'no dvc remote configured, skipping push')"
    ),
    dag=dag,
)

ingest_data >> validate_data >> version_data
