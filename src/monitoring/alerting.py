"""Alerting helpers used by the monitoring loop and the Airflow DAGs.

Channels (in order of preference):
1. Slack webhook (SLACK_WEBHOOK_URL)
2. Local alert log file (data/monitoring/alerts/alerts.jsonl) — always written

No secrets are ever logged: only the webhook URL prefix is shown.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALERT_LOG = PROJECT_ROOT / "data" / "monitoring" / "alerts" / "alerts.jsonl"

SEVERITY_LEVELS = {"debug": 10, "info": 20, "warning": 30, "critical": 40}


def send_slack(message: str, severity: str = "info", webhook_url: str | None = None) -> bool:
    webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return False
    emoji = {
        "debug": ":mag:",
        "info": ":information_source:",
        "warning": ":warning:",
        "critical": ":red_circle:",
    }.get(severity, ":bell:")
    try:
        response = requests.post(webhook_url, json={"text": f"{emoji} `[{severity}]` {message}"}, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def send_alert(message: str, severity: str = "info", **extra: Any) -> dict:
    entry = {
        "timestamp": time.time(),
        "severity": severity,
        "message": message,
        "extra": extra,
    }
    ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ALERT_LOG.open("a") as fh:
        fh.write(json.dumps(entry) + "\n")

    delivered = send_slack(message, severity)
    entry["slack_delivered"] = delivered
    print(f"[alert:{severity}] {message}" + (" (slack)" if delivered else " (local only)"))
    return entry
