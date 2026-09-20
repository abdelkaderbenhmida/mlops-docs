#!/bin/bash
# Init script (runs on first postgres volume init): create the Airflow
# database. Airflow and MLflow must NOT share one database — both use
# alembic and clobber each other's alembic_version table.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE airflow;
    GRANT ALL PRIVILEGES ON DATABASE airflow TO $POSTGRES_USER;
EOSQL
