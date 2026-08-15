"""Generate a realistic synthetic telecom churn dataset (Telco-Churn-like).

Writes data/raw/dataset.csv (and a copy under data/external/ so the
ingestion stage has a realistic upstream source). Deterministic seed so the
dataset is reproducible.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd

N_ROWS_DEFAULT = 7000
SEED = 42

CONTRACT_TYPES = ["Month-to-month", "One year", "Two year"]
INTERNET_SERVICES = ["DSL", "Fiber optic", "No"]
PAYMENT_METHODS = [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)",
]


def _pick(rng: random.Random, options: list[str], weights: list[float] | None = None) -> str:
    if weights is None:
        return rng.choice(options)
    return rng.choices(options, weights=weights, k=1)[0]


def _churn_probability(row: dict) -> float:
    p = 0.12
    if row["Contract"] == "Month-to-month":
        p += 0.28
    elif row["Contract"] == "One year":
        p += 0.06
    if row["InternetService"] == "Fiber optic":
        p += 0.10
    p -= min(0.30, row["Tenure"] * 0.006)
    if row["PaymentMethod"] == "Electronic check":
        p += 0.08
    if row["TechSupport"] == "No":
        p += 0.05
    if row["OnlineSecurity"] == "No" and row["InternetService"] != "No":
        p += 0.04
    return float(np.clip(p, 0.01, 0.95))


def generate(n_rows: int = N_ROWS_DEFAULT, seed: int = SEED) -> pd.DataFrame:
    rng = random.Random(seed)
    base = np.random.default_rng(seed)
    rows: list[dict] = []

    for _ in range(n_rows):
        tenure = int(rng.randint(1, 72))
        monthly = float(round(rng.uniform(19.0, 118.0), 2))
        row = {
            "CustomerID": f"{rng.randrange(1000, 9999)}-{rng.randrange(10000, 99999)}",
            "Gender": _pick(rng, ["Male", "Female"]),
            "SeniorCitizen": rng.randint(0, 1),
            "Partner": _pick(rng, ["Yes", "No"]),
            "Dependents": _pick(rng, ["Yes", "No"], weights=[0.3, 0.7]),
            "Tenure": tenure,
            "PhoneService": _pick(rng, ["Yes", "No"], weights=[0.9, 0.1]),
            "MultipleLines": _pick(rng, ["Yes", "No", "No phone service"]),
            "InternetService": _pick(rng, INTERNET_SERVICES, weights=[0.44, 0.42, 0.14]),
            "OnlineSecurity": _pick(rng, ["Yes", "No", "No internet service"]),
            "OnlineBackup": _pick(rng, ["Yes", "No", "No internet service"]),
            "DeviceProtection": _pick(rng, ["Yes", "No", "No internet service"]),
            "TechSupport": _pick(rng, ["Yes", "No", "No internet service"]),
            "StreamingTV": _pick(rng, ["Yes", "No", "No internet service"]),
            "StreamingMovies": _pick(rng, ["Yes", "No", "No internet service"]),
            "Contract": _pick(rng, CONTRACT_TYPES, weights=[0.55, 0.25, 0.20]),
            "PaperlessBilling": _pick(rng, ["Yes", "No"]),
            "PaymentMethod": _pick(rng, PAYMENT_METHODS, weights=[0.33, 0.23, 0.22, 0.22]),
            "MonthlyCharges": monthly,
        }
        row["TotalCharges"] = float(round(monthly * tenure * (1 + rng.uniform(-0.05, 0.05)), 2))
        row["Churn"] = "Yes" if base.random() < _churn_probability(row) else "No"
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic churn dataset.")
    parser.add_argument("--n-rows", type=int, default=N_ROWS_DEFAULT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", type=Path, default=Path("data/raw/dataset.csv"))
    parser.add_argument("--external", type=Path, default=Path("data/external/dataset.csv"))
    args = parser.parse_args()

    df = generate(args.n_rows, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.external.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    df.to_csv(args.external, index=False)
    print(f"Generated {len(df)} rows x {len(df.columns)} columns -> {args.output}")
    print(f"Churn rate: {float((df['Churn'] == 'Yes').mean()):.3f}")


if __name__ == "__main__":
    main()
