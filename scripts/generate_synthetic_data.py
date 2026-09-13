# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Generate the synthetic retail demand dataset used across this project.

Writes ``data/raw/demand_data.csv`` (the committed demo dataset) and a copy
under ``data/external/dataset.csv`` so the DVC ``ingest`` stage has a
realistic upstream source. Deterministic seed, so the dataset is reproducible.

The data is synthetic and small: seasonality, price elasticity and noise are
injected deliberately and are not representative of a real supply chain. No
production performance can be claimed from it.
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

N_ROWS_DEFAULT = 50000
SEED = 42

N_STORES = 50
N_SKUS = 200
START_DATE = date(2023, 1, 1)

# Australian-style public holidays are not modelled precisely; a fixed set of
# calendar days is flagged so the model has a holiday signal to learn.
HOLIDAY_MONTH_DAYS = {(1, 1), (4, 7), (4, 10), (6, 12), (12, 25), (12, 26)}


def generate(n_rows: int = N_ROWS_DEFAULT, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    store_id = rng.integers(1, N_STORES + 1, size=n_rows)
    sku_id = rng.integers(1, N_SKUS + 1, size=n_rows)

    day_offset = rng.integers(0, 730, size=n_rows)
    dates = np.array([START_DATE + timedelta(days=int(d)) for d in day_offset])
    day_of_week = np.array([d.weekday() for d in dates])
    month = np.array([d.month for d in dates])
    is_holiday = np.array(
        [1 if (d.month, d.day) in HOLIDAY_MONTH_DAYS else 0 for d in dates],
        dtype=np.int64,
    )

    # Each SKU has a stable base price; observed price jitters around it.
    sku_base_price = rng.uniform(3.0, 80.0, size=N_SKUS + 1)
    price = (sku_base_price[sku_id] * rng.normal(1.0, 0.08, size=n_rows)).clip(1.0, 500.0)
    competitor_price = (price * rng.normal(1.0, 0.12, size=n_rows)).clip(1.0, 500.0)

    promotion = (rng.random(n_rows) < 0.18).astype(np.int64)
    temperature = rng.normal(18.0, 9.0, size=n_rows).clip(-10.0, 45.0)
    inventory_level = rng.integers(0, 3000, size=n_rows)
    store_traffic = rng.integers(50, 5000, size=n_rows)

    # Demand: base level driven by traffic, modulated by price elasticity,
    # promotions, weekend/holiday lift and a mild seasonal term.
    price_ratio = competitor_price / price
    seasonal = 1.0 + 0.15 * np.sin(2 * np.pi * (month - 1) / 12)
    weekend = np.where(day_of_week >= 5, 1.25, 1.0)
    holiday = np.where(is_holiday == 1, 1.4, 1.0)
    promo = np.where(promotion == 1, 1.35, 1.0)

    expected = (
        0.006 * store_traffic
        * price_ratio**1.3
        * seasonal
        * weekend
        * holiday
        * promo
        * (1.0 + 0.00005 * inventory_level)
    )
    units_sold = rng.poisson(np.clip(expected, 0.1, None)).astype(np.int64)

    return pd.DataFrame(
        {
            "store_id": store_id,
            "sku_id": sku_id,
            "date": [d.isoformat() for d in dates],
            "day_of_week": day_of_week,
            "month": month,
            "is_holiday": is_holiday,
            "price": price.round(2),
            "promotion": promotion,
            "temperature": temperature.round(1),
            "inventory_level": inventory_level,
            "competitor_price": competitor_price.round(2),
            "store_traffic": store_traffic,
            "units_sold": units_sold,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the synthetic demand dataset.")
    parser.add_argument("--n-rows", type=int, default=N_ROWS_DEFAULT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", type=Path, default=Path("data/raw/demand_data.csv"))
    parser.add_argument("--external", type=Path, default=Path("data/external/dataset.csv"))
    args = parser.parse_args()

    df = generate(args.n_rows, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.external.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    df.to_csv(args.external, index=False)
    print(f"Generated {len(df)} rows x {len(df.columns)} columns -> {args.output}")
    print(f"Mean units_sold: {df['units_sold'].mean():.2f}")


if __name__ == "__main__":
    main()
