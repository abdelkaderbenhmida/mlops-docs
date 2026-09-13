# mlops-project-documentation: generate_synthetic_data.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/scripts/generate_synthetic_data.py`
- **Total lines:** 117
- **File size:** 4410 bytes

## Line Type Summary
- **Code:** 87
- **Comment:** 5
- **Empty:** 22
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Generate the synthetic retail demand dataset used across this proje...`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Writes ``data/raw/demand_data.csv`` (the committed demo dataset) and a...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `under ``data/external/dataset.csv`` so the DVC ``ingest`` stage has a`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `realistic upstream source. Deterministic seed, so the dataset is repro...`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `The data is synthetic and small: seasonality, price elasticity and noi...`
> **Type:** Logical operation

### Line  11
> **Code:** `injected deliberately and are not representative of a real supply chai...`
> **Type:** Logical operation

### Line  12
> **Code:** `production performance can be claimed from it.`
> **Type:** Logical operation

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `from datetime import date, timedelta`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  22
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `N_ROWS_DEFAULT = 50000`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `SEED = 42`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `N_STORES = 50`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `N_SKUS = 200`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `START_DATE = date(2023, 1, 1)`
> **Type:** Assignment/comparison

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `# Australian-style public holidays are not modelled precisely; a fixed...`
> **Type:** Comment: Australian-style public holidays are not modelled precisely; a fixed set of

### Line  32
> **Code:** `# calendar days is flagged so the model has a holiday signal to learn.`
> **Type:** Comment: calendar days is flagged so the model has a holiday signal to learn.

### Line  33
> **Code:** `HOLIDAY_MONTH_DAYS = {(1, 1), (4, 7), (4, 10), (6, 12), (12, 25), (12,...`
> **Type:** Assignment/comparison

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def generate(n_rows: int = N_ROWS_DEFAULT, seed: int = SEED) -> pd.Dat...`
> **Type:** Function definition

### Line  37
> **Code:** `rng = np.random.default_rng(seed)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `store_id = rng.integers(1, N_STORES + 1, size=n_rows)`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `sku_id = rng.integers(1, N_SKUS + 1, size=n_rows)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `day_offset = rng.integers(0, 730, size=n_rows)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `dates = np.array([START_DATE + timedelta(days=int(d)) for d in day_off...`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `day_of_week = np.array([d.weekday() for d in dates])`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `month = np.array([d.month for d in dates])`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `is_holiday = np.array(`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `[1 if (d.month, d.day) in HOLIDAY_MONTH_DAYS else 0 for d in dates],`
> **Type:** Logical operation

### Line  48
> **Code:** `dtype=np.int64,`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `)`
> **Type:** Code statement

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `# Each SKU has a stable base price; observed price jitters around it.`
> **Type:** Comment: Each SKU has a stable base price; observed price jitters around it.

### Line  52
> **Code:** `sku_base_price = rng.uniform(3.0, 80.0, size=N_SKUS + 1)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `price = (sku_base_price[sku_id] * rng.normal(1.0, 0.08, size=n_rows))....`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `competitor_price = (price * rng.normal(1.0, 0.12, size=n_rows)).clip(1...`
> **Type:** Assignment/comparison

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `promotion = (rng.random(n_rows) < 0.18).astype(np.int64)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `temperature = rng.normal(18.0, 9.0, size=n_rows).clip(-10.0, 45.0)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `inventory_level = rng.integers(0, 3000, size=n_rows)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `store_traffic = rng.integers(50, 5000, size=n_rows)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `# Demand: base level driven by traffic, modulated by price elasticity,`
> **Type:** Comment: Demand: base level driven by traffic, modulated by price elasticity,

### Line  62
> **Code:** `# promotions, weekend/holiday lift and a mild seasonal term.`
> **Type:** Comment: promotions, weekend/holiday lift and a mild seasonal term.

### Line  63
> **Code:** `price_ratio = competitor_price / price`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `seasonal = 1.0 + 0.15 * np.sin(2 * np.pi * (month - 1) / 12)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `weekend = np.where(day_of_week >= 5, 1.25, 1.0)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `holiday = np.where(is_holiday == 1, 1.4, 1.0)`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `promo = np.where(promotion == 1, 1.35, 1.0)`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `expected = (`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `0.006 * store_traffic`
> **Type:** Arithmetic operation

### Line  71
> **Code:** `* price_ratio**1.3`
> **Type:** Arithmetic operation

### Line  72
> **Code:** `* seasonal`
> **Type:** Arithmetic operation

### Line  73
> **Code:** `* weekend`
> **Type:** Arithmetic operation

### Line  74
> **Code:** `* holiday`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `* promo`
> **Type:** Arithmetic operation

### Line  76
> **Code:** `* (1.0 + 0.00005 * inventory_level)`
> **Type:** Arithmetic operation

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** `units_sold = rng.poisson(np.clip(expected, 0.1, None)).astype(np.int64...`
> **Type:** Assignment/comparison

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `return pd.DataFrame(`
> **Type:** Returns a value from a function

### Line  81
> **Code:** `{`
> **Type:** Data structure operation

### Line  82
> **Code:** `"store_id": store_id,`
> **Type:** Logical operation

### Line  83
> **Code:** `"sku_id": sku_id,`
> **Type:** Code statement

### Line  84
> **Code:** `"date": [d.isoformat() for d in dates],`
> **Type:** Logical operation

### Line  85
> **Code:** `"day_of_week": day_of_week,`
> **Type:** Code statement

### Line  86
> **Code:** `"month": month,`
> **Type:** Code statement

### Line  87
> **Code:** `"is_holiday": is_holiday,`
> **Type:** Code statement

### Line  88
> **Code:** `"price": price.round(2),`
> **Type:** Code statement

### Line  89
> **Code:** `"promotion": promotion,`
> **Type:** Code statement

### Line  90
> **Code:** `"temperature": temperature.round(1),`
> **Type:** Code statement

### Line  91
> **Code:** `"inventory_level": inventory_level,`
> **Type:** Logical operation

### Line  92
> **Code:** `"competitor_price": competitor_price.round(2),`
> **Type:** Logical operation

### Line  93
> **Code:** `"store_traffic": store_traffic,`
> **Type:** Logical operation

### Line  94
> **Code:** `"units_sold": units_sold,`
> **Type:** Code statement

### Line  95
> **Code:** `}`
> **Type:** Code statement

### Line  96
> **Code:** `)`
> **Type:** Code statement

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 100
> **Code:** `parser = argparse.ArgumentParser(description="Generate the synthetic d...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `parser.add_argument("--n-rows", type=int, default=N_ROWS_DEFAULT)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `parser.add_argument("--seed", type=int, default=SEED)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `parser.add_argument("--output", type=Path, default=Path("data/raw/dema...`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `parser.add_argument("--external", type=Path, default=Path("data/extern...`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `df = generate(args.n_rows, args.seed)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `args.output.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `args.external.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `df.to_csv(args.output, index=False)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `df.to_csv(args.external, index=False)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `print(f"Generated {len(df)} rows x {len(df.columns)} columns -> {args....`
> **Type:** Prints output to console

### Line 113
> **Code:** `print(f"Mean units_sold: {df['units_sold'].mean():.2f}")`
> **Type:** Prints output to console

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 117
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 117
- **Code lines:** 87
- **Comments:** 5
- **TODO items:** 3
- **Empty lines:** 22

---
*Documentation generated for: mlops-project-documentation*
*File: generate_synthetic_data.py*
---

# mlops-project-documentation: test_pipeline_end_to_end.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/integration/test_pipeline_end_to_end.py`
- **Total lines:** 180
- **File size:** 7776 bytes

## Line Type Summary
- **Code:** 150
- **Comment:** 0
- **Empty:** 27
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""End-to-end integration test for the demand forecasting MLOps pipeli...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Tests the full pipeline: generate data -> preprocess -> features -> tr...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `using SQLite MLflow backend and monkeypatched environment.`
> **Type:** Logical operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import json`
> **Type:** Imports a module

### Line  11
> **Code:** `import os`
> **Type:** Imports a module

### Line  12
> **Code:** `import sys`
> **Type:** Imports a module

### Line  13
> **Code:** `import tempfile`
> **Type:** Imports a module

### Line  14
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from unittest.mock import patch, MagicMock`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  18
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  22
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `from src.features.build_features import build_features, FeatureTransfo...`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from src.models.train import train_model`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from src.models.evaluate import evaluate`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `@pytest.mark.integration`
> **Type:** Code statement

### Line  31
> **Code:** `class TestPipelineEndToEnd:`
> **Type:** Class definition

### Line  32
> **Code:** `"""End-to-end pipeline test with minimal data and fast model."""`
> **Type:** Arithmetic operation

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `@pytest.fixture(autouse=True)`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `def setup_env(self, tmp_path, monkeypatch):`
> **Type:** Function definition

### Line  36
> **Code:** `"""Set up isolated environment for each test."""`
> **Type:** Logical operation

### Line  37
> **Code:** `self.tmp_path = tmp_path`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `self.data_dir = tmp_path / "data"`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `self.data_dir.mkdir()`
> **Type:** Function call

### Line  40
> **Code:** `self.models_dir = tmp_path / "models"`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `self.models_dir.mkdir()`
> **Type:** Function call

### Line  42
> **Code:** `self.mlruns_dir = tmp_path / "mlruns"`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `self.mlruns_dir.mkdir()`
> **Type:** Function call

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{self.mlruns_dir...`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `monkeypatch.setenv("MLFLOW_MODEL_NAME", "test_demand_model")`
> **Type:** Logical operation

### Line  47
> **Code:** `monkeypatch.setenv("DRIFT_THRESHOLD", "0.3")`
> **Type:** Function call

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `self.sample_csv = self.data_dir / "raw" / "demand_data.csv"`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `self.sample_csv.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `self._create_sample_data()`
> **Type:** Function call

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def _create_sample_data(self):`
> **Type:** Function definition

### Line  54
> **Code:** `"""Create a small sample dataset for fast testing."""`
> **Type:** Logical operation

### Line  55
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  56
> **Code:** `rng = np.random.default_rng(42)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `n = 200`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `"store_id": rng.integers(1, 11, n),`
> **Type:** Logical operation

### Line  60
> **Code:** `"sku_id": rng.integers(1, 21, n),`
> **Type:** Code statement

### Line  61
> **Code:** `"day_of_week": rng.integers(0, 7, n),`
> **Type:** Code statement

### Line  62
> **Code:** `"month": rng.integers(1, 13, n),`
> **Type:** Code statement

### Line  63
> **Code:** `"is_holiday": rng.integers(0, 2, n),`
> **Type:** Code statement

### Line  64
> **Code:** `"price": np.round(rng.uniform(5, 100, n), 2),`
> **Type:** Logical operation

### Line  65
> **Code:** `"promotion": rng.integers(0, 2, n),`
> **Type:** Code statement

### Line  66
> **Code:** `"temperature": np.round(rng.uniform(20, 100, n), 1),`
> **Type:** Logical operation

### Line  67
> **Code:** `"inventory_level": rng.integers(10, 300, n),`
> **Type:** Logical operation

### Line  68
> **Code:** `"competitor_price": np.round(rng.uniform(5, 120, n), 2),`
> **Type:** Logical operation

### Line  69
> **Code:** `"store_traffic": rng.integers(50, 1500, n),`
> **Type:** Logical operation

### Line  70
> **Code:** `"units_sold": rng.integers(5, 80, n),`
> **Type:** Code statement

### Line  71
> **Code:** `})`
> **Type:** Code statement

### Line  72
> **Code:** `df.to_csv(self.sample_csv, index=False)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `def _override_default_paths(self, monkeypatch):`
> **Type:** Function definition

### Line  75
> **Code:** `"""Override default paths in modules to use temp directories."""`
> **Type:** Logical operation

### Line  76
> **Code:** `monkeypatch.setattr("src.data.preprocessing.DEFAULT_INPUT", self.sampl...`
> **Type:** Function call

### Line  77
> **Code:** `monkeypatch.setattr("src.data.preprocessing.DEFAULT_OUTPUT", self.data...`
> **Type:** Arithmetic operation

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `monkeypatch.setattr("src.features.build_features.DEFAULT_INPUT", self....`
> **Type:** Arithmetic operation

### Line  80
> **Code:** `monkeypatch.setattr("src.features.build_features.DEFAULT_OUTPUT", self...`
> **Type:** Arithmetic operation

### Line  81
> **Code:** `monkeypatch.setattr("src.features.build_features.DEFAULT_CONFIG", self...`
> **Type:** Arithmetic operation

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_DATA", self.data_dir / "...`
> **Type:** Arithmetic operation

### Line  84
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_CONFIG", self.data_dir /...`
> **Type:** Arithmetic operation

### Line  85
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_MODEL_OUTPUT", self.mode...`
> **Type:** Arithmetic operation

### Line  86
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_METRICS", self.models_di...`
> **Type:** Arithmetic operation

### Line  87
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_ARTIFACT_DIR", self.mode...`
> **Type:** Arithmetic operation

### Line  88
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_REFERENCE", self.data_di...`
> **Type:** Arithmetic operation

### Line  89
> **Code:** `monkeypatch.setattr("src.models.train.MODEL_NAME", "test_demand_model"...`
> **Type:** Logical operation

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `monkeypatch.setattr("src.models.evaluate.DEFAULT_DATA", self.data_dir ...`
> **Type:** Arithmetic operation

### Line  92
> **Code:** `monkeypatch.setattr("src.models.evaluate.DEFAULT_LOCAL_MODEL", self.mo...`
> **Type:** Arithmetic operation

### Line  93
> **Code:** `monkeypatch.setattr("src.models.evaluate.EVALUATION_DIR", self.models_...`
> **Type:** Arithmetic operation

### Line  94
> **Code:** `monkeypatch.setattr("src.models.evaluate.LATEST_REPORT", self.models_d...`
> **Type:** Arithmetic operation

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `def test_full_pipeline(self, monkeypatch):`
> **Type:** Function definition

### Line  97
> **Code:** `"""Run the complete pipeline end-to-end."""`
> **Type:** Arithmetic operation

### Line  98
> **Code:** `self._override_default_paths(monkeypatch)`
> **Type:** Function call

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `processed_path = self.data_dir / "processed" / "demand_data.csv"`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `processed_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `processed_df = preprocess(self.sample_csv, processed_path)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `assert processed_path.exists()`
> **Type:** Enforces a condition

### Line 104
> **Code:** `assert len(processed_df) > 0`
> **Type:** Enforces a condition

### Line 105
> **Code:** `assert "units_sold" in processed_df.columns`
> **Type:** Enforces a condition

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `features_path = self.data_dir / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `config_path = self.data_dir / "features" / "features_config.json"`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `features_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `features_df = build_features(processed_path, features_path, config_pat...`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `assert features_path.exists()`
> **Type:** Enforces a condition

### Line 112
> **Code:** `assert config_path.exists()`
> **Type:** Enforces a condition

### Line 113
> **Code:** `assert len(features_df) == len(processed_df)`
> **Type:** Enforces a condition

### Line 114
> **Code:** `assert "units_sold" in features_df.columns`
> **Type:** Enforces a condition

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `train_params = {`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `"n_estimators": 10,`
> **Type:** Logical operation

### Line 118
> **Code:** `"max_depth": 5,`
> **Type:** Code statement

### Line 119
> **Code:** `"min_samples_leaf": 3,`
> **Type:** Code statement

### Line 120
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line 121
> **Code:** `}`
> **Type:** Code statement

### Line 122
> **Code:** `train_result = train_model(`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `config_path=config_path,`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `model_output=self.models_dir / "model.pkl",`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `model_name="test_demand_model",`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `params=train_params,`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `)`
> **Type:** Code statement

### Line 129
> **Code:** `assert train_result["run_id"] is not None`
> **Type:** Enforces a condition

### Line 130
> **Code:** `assert (self.models_dir / "model.pkl").exists()`
> **Type:** Enforces a condition

### Line 131
> **Code:** `assert (self.data_dir / "monitoring" / "reference.csv").exists()`
> **Type:** Enforces a condition

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `eval_report = evaluate(`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `model_uri=None,`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `run_id=train_result["run_id"],`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `)`
> **Type:** Code statement

### Line 138
> **Code:** `assert eval_report["gates_passed"] is not None`
> **Type:** Enforces a condition

### Line 139
> **Code:** `assert "metrics" in eval_report`
> **Type:** Enforces a condition

### Line 140
> **Code:** `assert "rmse" in eval_report["metrics"]`
> **Type:** Enforces a condition

### Line 141
> **Code:** `assert "r2" in eval_report["metrics"]`
> **Type:** Enforces a condition

### Line 142
> **Code:** `assert (self.models_dir / "evaluation" / "latest_report.json").exists(...`
> **Type:** Enforces a condition

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `def test_pipeline_with_evaluation_failure(self, monkeypatch):`
> **Type:** Function definition

### Line 145
> **Code:** `"""Test pipeline when evaluation gates fail."""`
> **Type:** Code statement

### Line 146
> **Code:** `self._override_default_paths(monkeypatch)`
> **Type:** Function call

### Line 147
> **Code:** ``
> **Type:** Empty line

### Line 148
> **Code:** `processed_path = self.data_dir / "processed" / "demand_data.csv"`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `processed_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `preprocess(self.sample_csv, processed_path)`
> **Type:** Function call

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `features_path = self.data_dir / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `config_path = self.data_dir / "features" / "features_config.json"`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `features_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 155
> **Code:** `build_features(processed_path, features_path, config_path)`
> **Type:** Function call

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `train_params = {`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `"n_estimators": 10,`
> **Type:** Logical operation

### Line 159
> **Code:** `"max_depth": 3,`
> **Type:** Code statement

### Line 160
> **Code:** `"min_samples_leaf": 3,`
> **Type:** Code statement

### Line 161
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line 162
> **Code:** `}`
> **Type:** Code statement

### Line 163
> **Code:** `train_result = train_model(`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `config_path=config_path,`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `model_output=self.models_dir / "model.pkl",`
> **Type:** Assignment/comparison

### Line 167
> **Code:** `model_name="test_demand_model",`
> **Type:** Assignment/comparison

### Line 168
> **Code:** `params=train_params,`
> **Type:** Assignment/comparison

### Line 169
> **Code:** `)`
> **Type:** Code statement

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `eval_report = evaluate(`
> **Type:** Assignment/comparison

### Line 172
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 173
> **Code:** `run_id=train_result["run_id"],`
> **Type:** Assignment/comparison

### Line 174
> **Code:** `thresholds={"min_r2": 0.99, "max_mape": 1.0},`
> **Type:** Assignment/comparison

### Line 175
> **Code:** `)`
> **Type:** Code statement

### Line 176
> **Code:** `assert eval_report["gates_passed"] is False`
> **Type:** Enforces a condition

### Line 177
> **Code:** ``
> **Type:** Empty line

### Line 178
> **Code:** ``
> **Type:** Empty line

### Line 179
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 180
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 180
- **Code lines:** 150
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 27

---
*Documentation generated for: mlops-project-documentation*
*File: test_pipeline_end_to_end.py*
---

# mlops-project-documentation: test_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/unit/test_features.py`
- **Total lines:** 168
- **File size:** 5886 bytes

## Line Type Summary
- **Code:** 132
- **Comment:** 0
- **Empty:** 33
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for src.features.build_features module (demand forecasting)."...`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   8
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from src.features.build_features import (`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `FeatureTransformer,`
> **Type:** Logical operation

### Line  19
> **Code:** `build_features,`
> **Type:** Code statement

### Line  20
> **Code:** `FEATURE_ORDER,`
> **Type:** Code statement

### Line  21
> **Code:** `TARGET_FEATURE,`
> **Type:** Code statement

### Line  22
> **Code:** `TARGET_COLUMN,`
> **Type:** Code statement

### Line  23
> **Code:** `)`
> **Type:** Code statement

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `class TestFeatureTransformer:`
> **Type:** Class definition

### Line  27
> **Code:** `"""Test FeatureTransformer fit/transform correctness for demand data."...`
> **Type:** Arithmetic operation

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def _sample_df(self, n=100):`
> **Type:** Function definition

### Line  30
> **Code:** `"""Create sample dataframe with demand columns."""`
> **Type:** Logical operation

### Line  31
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  32
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  33
> **Code:** `return pd.DataFrame({`
> **Type:** Returns a value from a function

### Line  34
> **Code:** `"store_id": np.random.randint(1, 31, n),`
> **Type:** Logical operation

### Line  35
> **Code:** `"sku_id": np.random.randint(1, 101, n),`
> **Type:** Logical operation

### Line  36
> **Code:** `"day_of_week": np.random.randint(0, 7, n),`
> **Type:** Logical operation

### Line  37
> **Code:** `"month": np.random.randint(1, 13, n),`
> **Type:** Logical operation

### Line  38
> **Code:** `"is_holiday": np.random.choice([0, 1], n),`
> **Type:** Logical operation

### Line  39
> **Code:** `"price": np.random.uniform(5, 150, n),`
> **Type:** Logical operation

### Line  40
> **Code:** `"promotion": np.random.choice([0, 1], n),`
> **Type:** Logical operation

### Line  41
> **Code:** `"temperature": np.random.uniform(20, 100, n),`
> **Type:** Logical operation

### Line  42
> **Code:** `"inventory_level": np.random.randint(10, 500, n),`
> **Type:** Logical operation

### Line  43
> **Code:** `"competitor_price": np.random.uniform(5, 180, n),`
> **Type:** Logical operation

### Line  44
> **Code:** `"store_traffic": np.random.randint(50, 2000, n),`
> **Type:** Logical operation

### Line  45
> **Code:** `"units_sold": np.random.randint(0, 100, n),`
> **Type:** Logical operation

### Line  46
> **Code:** `})`
> **Type:** Code statement

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def test_fit_transform_shape(self):`
> **Type:** Function definition

### Line  49
> **Code:** `"""fit_transform should return expected feature columns."""`
> **Type:** Logical operation

### Line  50
> **Code:** `df = self._sample_df(50)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `assert list(features.columns) == FEATURE_ORDER`
> **Type:** Enforces a condition

### Line  55
> **Code:** `assert len(features) == 50`
> **Type:** Enforces a condition

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def test_numeric_features_present(self):`
> **Type:** Function definition

### Line  58
> **Code:** `"""Numeric features should be present in output."""`
> **Type:** Code statement

### Line  59
> **Code:** `df = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `for col in FEATURE_ORDER:`
> **Type:** For loop

### Line  64
> **Code:** `assert col in features.columns`
> **Type:** Enforces a condition

### Line  65
> **Code:** `assert features[col].dtype in ("float64", "float32", "int64", "int32")`
> **Type:** Enforces a condition

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** `def test_config_roundtrip(self):`
> **Type:** Function definition

### Line  68
> **Code:** `"""to_config and from_config should preserve state."""`
> **Type:** Logical operation

### Line  69
> **Code:** `df = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `transformer.fit(df)`
> **Type:** Logical operation

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `config = transformer.to_config()`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `restored = FeatureTransformer.from_config(config)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `test_df = self._sample_df(10)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `out1 = transformer.transform(test_df)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `out2 = restored.transform(test_df)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `pd.testing.assert_frame_equal(out1, out2)`
> **Type:** Function call

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `def test_train_inference_parity(self):`
> **Type:** Function definition

### Line  83
> **Code:** `"""Train-time fit_transform and inference-time transform should match....`
> **Type:** Arithmetic operation

### Line  84
> **Code:** `df = self._sample_df(50)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `transformer_train = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `features_train = transformer_train.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `config = transformer_train.to_config()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `transformer_infer = FeatureTransformer.from_config(config)`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `features_infer = transformer_infer.transform(df)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `pd.testing.assert_frame_equal(features_train, features_infer)`
> **Type:** Function call

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `def test_feature_order_preserved(self):`
> **Type:** Function definition

### Line  96
> **Code:** `"""Feature order should match FEATURE_ORDER exactly."""`
> **Type:** Logical operation

### Line  97
> **Code:** `df = self._sample_df(20)`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `assert list(features.columns) == FEATURE_ORDER`
> **Type:** Enforces a condition

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `class TestBuildFeatures:`
> **Type:** Class definition

### Line 105
> **Code:** `"""Test build_features end-to-end function for demand data."""`
> **Type:** Arithmetic operation

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `def test_build_features_creates_output(self, tmp_path):`
> **Type:** Function definition

### Line 108
> **Code:** `"""build_features should create parquet and config files."""`
> **Type:** Logical operation

### Line 109
> **Code:** `input_file = tmp_path / "input.csv"`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `output_file = tmp_path / "features.parquet"`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `config_file = tmp_path / "config.json"`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `"store_id": [1, 2],`
> **Type:** Logical operation

### Line 115
> **Code:** `"sku_id": [10, 20],`
> **Type:** Data structure operation

### Line 116
> **Code:** `"day_of_week": [0, 3],`
> **Type:** Data structure operation

### Line 117
> **Code:** `"month": [6, 12],`
> **Type:** Data structure operation

### Line 118
> **Code:** `"is_holiday": [0, 1],`
> **Type:** Data structure operation

### Line 119
> **Code:** `"price": [29.99, 49.99],`
> **Type:** Data structure operation

### Line 120
> **Code:** `"promotion": [1, 0],`
> **Type:** Data structure operation

### Line 121
> **Code:** `"temperature": [75.0, 35.0],`
> **Type:** Data structure operation

### Line 122
> **Code:** `"inventory_level": [200, 150],`
> **Type:** Logical operation

### Line 123
> **Code:** `"competitor_price": [32.99, 52.99],`
> **Type:** Logical operation

### Line 124
> **Code:** `"store_traffic": [500, 300],`
> **Type:** Logical operation

### Line 125
> **Code:** `"units_sold": [45, 12],`
> **Type:** Data structure operation

### Line 126
> **Code:** `})`
> **Type:** Code statement

### Line 127
> **Code:** `df.to_csv(input_file, index=False)`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `features = build_features(input_file, output_file, config_file)`
> **Type:** Assignment/comparison

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `assert output_file.exists()`
> **Type:** Enforces a condition

### Line 132
> **Code:** `assert config_file.exists()`
> **Type:** Enforces a condition

### Line 133
> **Code:** `assert len(features) == 2`
> **Type:** Enforces a condition

### Line 134
> **Code:** `assert TARGET_FEATURE in features.columns`
> **Type:** Enforces a condition

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `with config_file.open() as f:`
> **Type:** Context manager

### Line 137
> **Code:** `config = json.load(f)`
> **Type:** Assignment/comparison

### Line 138
> **Code:** `assert "numeric_features" in config`
> **Type:** Enforces a condition

### Line 139
> **Code:** `assert "numeric_stats" in config`
> **Type:** Enforces a condition

### Line 140
> **Code:** `assert "feature_order" in config`
> **Type:** Enforces a condition

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `def test_target_feature_is_numeric(self):`
> **Type:** Function definition

### Line 143
> **Code:** `"""Target feature should be numeric for regression."""`
> **Type:** Logical operation

### Line 144
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `"store_id": [1, 2, 3],`
> **Type:** Logical operation

### Line 146
> **Code:** `"sku_id": [10, 20, 30],`
> **Type:** Data structure operation

### Line 147
> **Code:** `"day_of_week": [0, 3, 5],`
> **Type:** Data structure operation

### Line 148
> **Code:** `"month": [6, 12, 3],`
> **Type:** Data structure operation

### Line 149
> **Code:** `"is_holiday": [0, 1, 0],`
> **Type:** Data structure operation

### Line 150
> **Code:** `"price": [29.99, 49.99, 19.99],`
> **Type:** Data structure operation

### Line 151
> **Code:** `"promotion": [1, 0, 1],`
> **Type:** Data structure operation

### Line 152
> **Code:** `"temperature": [75.0, 35.0, 60.0],`
> **Type:** Data structure operation

### Line 153
> **Code:** `"inventory_level": [200, 150, 300],`
> **Type:** Logical operation

### Line 154
> **Code:** `"competitor_price": [32.99, 52.99, 22.99],`
> **Type:** Logical operation

### Line 155
> **Code:** `"store_traffic": [500, 300, 800],`
> **Type:** Logical operation

### Line 156
> **Code:** `"units_sold": [45, 12, 78],`
> **Type:** Data structure operation

### Line 157
> **Code:** `})`
> **Type:** Code statement

### Line 158
> **Code:** ``
> **Type:** Empty line

### Line 159
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 161
> **Code:** `features[TARGET_FEATURE] = df[TARGET_COLUMN].astype(float)`
> **Type:** Assignment/comparison

### Line 162
> **Code:** ``
> **Type:** Empty line

### Line 163
> **Code:** `assert features[TARGET_FEATURE].dtype in ("float64", "float32")`
> **Type:** Enforces a condition

### Line 164
> **Code:** `assert set(features[TARGET_FEATURE].unique()).issubset({12.0, 45.0, 78...`
> **Type:** Enforces a condition

### Line 165
> **Code:** ``
> **Type:** Empty line

### Line 166
> **Code:** ``
> **Type:** Empty line

### Line 167
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 168
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 168
- **Code lines:** 132
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 33

---
*Documentation generated for: mlops-project-documentation*
*File: test_features.py*
---

# mlops-project-documentation: test_monitoring.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/unit/test_monitoring.py`
- **Total lines:** 157
- **File size:** 5963 bytes

## Line Type Summary
- **Code:** 119
- **Comment:** 0
- **Empty:** 35
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""Tests for src.monitoring.drift_detection module (demand forecasting...`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import os`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `import tempfile`
> **Type:** Imports a module

### Line   9
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** `from unittest.mock import patch, MagicMock`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  13
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  14
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  18
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from src.monitoring.drift_detection import detect_drift, _ks_fallback,...`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `class TestDriftDetection:`
> **Type:** Class definition

### Line  24
> **Code:** `"""Test drift detection logic with synthetic demand data."""`
> **Type:** Logical operation

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `def _create_reference_data(self, n=1000):`
> **Type:** Function definition

### Line  27
> **Code:** `"""Create a reference dataset with known distributions."""`
> **Type:** Code statement

### Line  28
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  29
> **Code:** `return pd.DataFrame({`
> **Type:** Returns a value from a function

### Line  30
> **Code:** `"store_id": np.random.randint(1, 31, n),`
> **Type:** Logical operation

### Line  31
> **Code:** `"sku_id": np.random.randint(1, 101, n),`
> **Type:** Logical operation

### Line  32
> **Code:** `"day_of_week": np.random.randint(0, 7, n),`
> **Type:** Logical operation

### Line  33
> **Code:** `"month": np.random.randint(1, 13, n),`
> **Type:** Logical operation

### Line  34
> **Code:** `"is_holiday": np.random.choice([0, 1], n),`
> **Type:** Logical operation

### Line  35
> **Code:** `"price": np.random.uniform(5, 150, n),`
> **Type:** Logical operation

### Line  36
> **Code:** `"promotion": np.random.choice([0, 1], n),`
> **Type:** Logical operation

### Line  37
> **Code:** `"temperature": np.random.uniform(20, 100, n),`
> **Type:** Logical operation

### Line  38
> **Code:** `"inventory_level": np.random.randint(10, 500, n),`
> **Type:** Logical operation

### Line  39
> **Code:** `"competitor_price": np.random.uniform(5, 180, n),`
> **Type:** Logical operation

### Line  40
> **Code:** `"store_traffic": np.random.randint(50, 2000, n),`
> **Type:** Logical operation

### Line  41
> **Code:** `"prediction": np.random.uniform(10, 80, n),`
> **Type:** Logical operation

### Line  42
> **Code:** `"units_sold": np.random.uniform(10, 80, n),`
> **Type:** Logical operation

### Line  43
> **Code:** `})`
> **Type:** Code statement

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `def _create_drifted_data(self, reference_df, drift_magnitude=0.5):`
> **Type:** Function definition

### Line  46
> **Code:** `"""Create a drifted dataset by shifting distributions."""`
> **Type:** Code statement

### Line  47
> **Code:** `drifted = reference_df.copy()`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `np.random.seed(123)`
> **Type:** Logical operation

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `for col in NUMERIC_FEATURES:`
> **Type:** For loop

### Line  51
> **Code:** `if col in drifted.columns:`
> **Type:** Conditional statement

### Line  52
> **Code:** `shift = reference_df[col].std() * drift_magnitude`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `drifted[col] = drifted[col] + shift`
> **Type:** Assignment/comparison

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `return drifted`
> **Type:** Returns a value from a function

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def test_ks_fallback_detects_drift_on_shifted_numeric(self):`
> **Type:** Function definition

### Line  58
> **Code:** `"""_ks_fallback should detect drift when numeric columns are shifted."...`
> **Type:** Code statement

### Line  59
> **Code:** `reference = self._create_reference_data(500)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `current = self._create_drifted_data(reference, drift_magnitude=1.0)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `assert drift_score > 0`
> **Type:** Enforces a condition

### Line  65
> **Code:** `drifted_numeric = [c for c in NUMERIC_FEATURES if c in per_column and ...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `assert len(drifted_numeric) > 0`
> **Type:** Enforces a condition

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def test_ks_fallback_no_drift_on_identical_data(self):`
> **Type:** Function definition

### Line  69
> **Code:** `"""_ks_fallback should not detect drift on identical data."""`
> **Type:** Logical operation

### Line  70
> **Code:** `reference = self._create_reference_data(500)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `assert drift_score == 0.0`
> **Type:** Enforces a condition

### Line  76
> **Code:** `for col, info in per_column.items():`
> **Type:** For loop

### Line  77
> **Code:** `assert info["drift_detected"] is False`
> **Type:** Enforces a condition

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `def test_detect_drift_identical_data_no_drift(self, tmp_path):`
> **Type:** Function definition

### Line  80
> **Code:** `"""detect_drift should not detect drift on identical data."""`
> **Type:** Logical operation

### Line  81
> **Code:** `reference = self._create_reference_data(200)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `report = detect_drift(`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `threshold=0.3,`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `output_dir=tmp_path / "output"`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `)`
> **Type:** Code statement

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `assert report["drift_score"] == 0.0`
> **Type:** Enforces a condition

### Line  97
> **Code:** `assert report["drift_detected"] is False`
> **Type:** Enforces a condition

### Line  98
> **Code:** `assert report["drifted_features"] == []`
> **Type:** Enforces a condition

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `def test_detect_drift_missing_reference_raises(self, tmp_path):`
> **Type:** Function definition

### Line 101
> **Code:** `"""detect_drift should raise FileNotFoundError for missing reference."...`
> **Type:** Logical operation

### Line 102
> **Code:** `current = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `with pytest.raises(FileNotFoundError, match="Reference dataset not fou...`
> **Type:** Context manager

### Line 107
> **Code:** `detect_drift(`
> **Type:** Code statement

### Line 108
> **Code:** `reference_path=tmp_path / "nonexistent.csv",`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `)`
> **Type:** Code statement

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `def test_detect_drift_missing_current_raises(self, tmp_path):`
> **Type:** Function definition

### Line 113
> **Code:** `"""detect_drift should raise FileNotFoundError for missing current."""`
> **Type:** Logical operation

### Line 114
> **Code:** `reference = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 117
> **Code:** ``
> **Type:** Empty line

### Line 118
> **Code:** `with pytest.raises(FileNotFoundError, match="Current production data n...`
> **Type:** Context manager

### Line 119
> **Code:** `detect_drift(`
> **Type:** Code statement

### Line 120
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `current_path=tmp_path / "nonexistent.csv",`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `)`
> **Type:** Code statement

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `def test_detect_drift_with_env_vars(self, tmp_path, monkeypatch):`
> **Type:** Function definition

### Line 125
> **Code:** `"""detect_drift should read from environment variables."""`
> **Type:** Code statement

### Line 126
> **Code:** `reference = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 130
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 131
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 132
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 133
> **Code:** ``
> **Type:** Empty line

### Line 134
> **Code:** `monkeypatch.setenv("DRIFT_REFERENCE", str(ref_path))`
> **Type:** Function call

### Line 135
> **Code:** `monkeypatch.setenv("DRIFT_CURRENT", str(cur_path))`
> **Type:** Function call

### Line 136
> **Code:** `monkeypatch.setenv("DRIFT_THRESHOLD", "0.5")`
> **Type:** Function call

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `report = detect_drift(output_dir=tmp_path)`
> **Type:** Assignment/comparison

### Line 139
> **Code:** ``
> **Type:** Empty line

### Line 140
> **Code:** `assert report["threshold"] == 0.5`
> **Type:** Enforces a condition

### Line 141
> **Code:** `assert report["reference"] == str(ref_path)`
> **Type:** Enforces a condition

### Line 142
> **Code:** `assert report["current"] == str(cur_path)`
> **Type:** Enforces a condition

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** ``
> **Type:** Empty line

### Line 145
> **Code:** `class TestFeatureColumns:`
> **Type:** Class definition

### Line 146
> **Code:** `"""Test that feature column lists match the actual data."""`
> **Type:** Code statement

### Line 147
> **Code:** ``
> **Type:** Empty line

### Line 148
> **Code:** `def test_numeric_features_not_empty(self):`
> **Type:** Function definition

### Line 149
> **Code:** `assert len(NUMERIC_FEATURES) > 0`
> **Type:** Enforces a condition

### Line 150
> **Code:** `assert all(isinstance(c, str) for c in NUMERIC_FEATURES)`
> **Type:** Enforces a condition

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `def test_no_duplicate_features(self):`
> **Type:** Function definition

### Line 153
> **Code:** `assert len(NUMERIC_FEATURES) == len(set(NUMERIC_FEATURES))`
> **Type:** Enforces a condition

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 157
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 157
- **Code lines:** 119
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 35

---
*Documentation generated for: mlops-project-documentation*
*File: test_monitoring.py*
---

# mlops-project-documentation: test_preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/unit/test_preprocessing.py`
- **Total lines:** 122
- **File size:** 4214 bytes

## Line Type Summary
- **Code:** 102
- **Comment:** 0
- **Empty:** 17
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for src.data.preprocessing module (demand forecasting)."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   7
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import sys`
> **Type:** Imports a module

### Line  10
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  14
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `from src.data.preprocessing import preprocess, NUMERIC_COLUMNS`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `class TestPreprocessing:`
> **Type:** Class definition

### Line  20
> **Code:** `"""Test preprocessing correctness for demand data."""`
> **Type:** Logical operation

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `def _run(self, df, tmp_path):`
> **Type:** Function definition

### Line  23
> **Code:** `"""Write df to a CSV and run preprocess with file paths."""`
> **Type:** Logical operation

### Line  24
> **Code:** `input_file = tmp_path / "input.csv"`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `output_file = tmp_path / "output.csv"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `df.to_csv(input_file, index=False)`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `return preprocess(input_file, output_file)`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def test_numeric_columns_coerced(self, tmp_path):`
> **Type:** Function definition

### Line  30
> **Code:** `"""Numeric columns should be coerced, invalid rows dropped."""`
> **Type:** Code statement

### Line  31
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `"store_id": [1, 2, 3],`
> **Type:** Logical operation

### Line  33
> **Code:** `"sku_id": [10, 20, 30],`
> **Type:** Data structure operation

### Line  34
> **Code:** `"day_of_week": [0, 3, 5],`
> **Type:** Data structure operation

### Line  35
> **Code:** `"month": [6, 12, 3],`
> **Type:** Data structure operation

### Line  36
> **Code:** `"is_holiday": [0, 1, 0],`
> **Type:** Data structure operation

### Line  37
> **Code:** `"price": [29.99, "bad", 19.99],`
> **Type:** Data structure operation

### Line  38
> **Code:** `"promotion": [1, 0, 1],`
> **Type:** Data structure operation

### Line  39
> **Code:** `"temperature": [75.0, 35.0, 60.0],`
> **Type:** Data structure operation

### Line  40
> **Code:** `"inventory_level": [200, 150, 300],`
> **Type:** Logical operation

### Line  41
> **Code:** `"competitor_price": [32.99, 52.99, 22.99],`
> **Type:** Logical operation

### Line  42
> **Code:** `"store_traffic": [500, 300, 800],`
> **Type:** Logical operation

### Line  43
> **Code:** `"units_sold": [45, 12, 78],`
> **Type:** Data structure operation

### Line  44
> **Code:** `})`
> **Type:** Code statement

### Line  45
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `assert len(result) == 2`
> **Type:** Enforces a condition

### Line  47
> **Code:** `assert result["price"].dtype in ("int64", "float64")`
> **Type:** Enforces a condition

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def test_negative_units_sold_dropped(self, tmp_path):`
> **Type:** Function definition

### Line  50
> **Code:** `"""Rows with negative units_sold should be dropped."""`
> **Type:** Code statement

### Line  51
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `"store_id": [1, 2],`
> **Type:** Logical operation

### Line  53
> **Code:** `"sku_id": [10, 20],`
> **Type:** Data structure operation

### Line  54
> **Code:** `"day_of_week": [0, 3],`
> **Type:** Data structure operation

### Line  55
> **Code:** `"month": [6, 12],`
> **Type:** Data structure operation

### Line  56
> **Code:** `"is_holiday": [0, 1],`
> **Type:** Data structure operation

### Line  57
> **Code:** `"price": [29.99, 49.99],`
> **Type:** Data structure operation

### Line  58
> **Code:** `"promotion": [1, 0],`
> **Type:** Data structure operation

### Line  59
> **Code:** `"temperature": [75.0, 35.0],`
> **Type:** Data structure operation

### Line  60
> **Code:** `"inventory_level": [200, 150],`
> **Type:** Logical operation

### Line  61
> **Code:** `"competitor_price": [32.99, 52.99],`
> **Type:** Logical operation

### Line  62
> **Code:** `"store_traffic": [500, 300],`
> **Type:** Logical operation

### Line  63
> **Code:** `"units_sold": [-5, 12],`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `})`
> **Type:** Code statement

### Line  65
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `assert len(result) == 1`
> **Type:** Enforces a condition

### Line  67
> **Code:** `assert result["units_sold"].iloc[0] == 12`
> **Type:** Enforces a condition

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def test_output_columns_match_expected(self, tmp_path):`
> **Type:** Function definition

### Line  70
> **Code:** `"""Output should have all expected columns."""`
> **Type:** Code statement

### Line  71
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `"store_id": [1],`
> **Type:** Logical operation

### Line  73
> **Code:** `"sku_id": [10],`
> **Type:** Data structure operation

### Line  74
> **Code:** `"day_of_week": [0],`
> **Type:** Data structure operation

### Line  75
> **Code:** `"month": [6],`
> **Type:** Data structure operation

### Line  76
> **Code:** `"is_holiday": [0],`
> **Type:** Data structure operation

### Line  77
> **Code:** `"price": [29.99],`
> **Type:** Data structure operation

### Line  78
> **Code:** `"promotion": [1],`
> **Type:** Data structure operation

### Line  79
> **Code:** `"temperature": [75.0],`
> **Type:** Data structure operation

### Line  80
> **Code:** `"inventory_level": [200],`
> **Type:** Logical operation

### Line  81
> **Code:** `"competitor_price": [32.99],`
> **Type:** Logical operation

### Line  82
> **Code:** `"store_traffic": [500],`
> **Type:** Logical operation

### Line  83
> **Code:** `"units_sold": [45],`
> **Type:** Data structure operation

### Line  84
> **Code:** `})`
> **Type:** Code statement

### Line  85
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `expected_cols = set(NUMERIC_COLUMNS + ["date"] if "date" in df.columns...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `assert set(result.columns) == expected_cols`
> **Type:** Enforces a condition

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def test_preprocess_with_file_paths(self, tmp_path):`
> **Type:** Function definition

### Line  90
> **Code:** `"""Test preprocess with file input/output paths."""`
> **Type:** Arithmetic operation

### Line  91
> **Code:** `input_file = tmp_path / "input.csv"`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `output_file = tmp_path / "output.csv"`
> **Type:** Assignment/comparison

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `"store_id": [1],`
> **Type:** Logical operation

### Line  96
> **Code:** `"sku_id": [10],`
> **Type:** Data structure operation

### Line  97
> **Code:** `"day_of_week": [0],`
> **Type:** Data structure operation

### Line  98
> **Code:** `"month": [6],`
> **Type:** Data structure operation

### Line  99
> **Code:** `"is_holiday": [0],`
> **Type:** Data structure operation

### Line 100
> **Code:** `"price": [29.99],`
> **Type:** Data structure operation

### Line 101
> **Code:** `"promotion": [1],`
> **Type:** Data structure operation

### Line 102
> **Code:** `"temperature": [75.0],`
> **Type:** Data structure operation

### Line 103
> **Code:** `"inventory_level": [200],`
> **Type:** Logical operation

### Line 104
> **Code:** `"competitor_price": [32.99],`
> **Type:** Logical operation

### Line 105
> **Code:** `"store_traffic": [500],`
> **Type:** Logical operation

### Line 106
> **Code:** `"units_sold": [45],`
> **Type:** Data structure operation

### Line 107
> **Code:** `})`
> **Type:** Code statement

### Line 108
> **Code:** `df.to_csv(input_file, index=False)`
> **Type:** Assignment/comparison

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `result = preprocess(input_file, output_file)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `assert output_file.exists()`
> **Type:** Enforces a condition

### Line 113
> **Code:** `assert len(result) == 1`
> **Type:** Enforces a condition

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `def test_missing_input_raises_error(self, tmp_path):`
> **Type:** Function definition

### Line 116
> **Code:** `"""Missing input file should raise FileNotFoundError."""`
> **Type:** Logical operation

### Line 117
> **Code:** `with pytest.raises(FileNotFoundError):`
> **Type:** Context manager

### Line 118
> **Code:** `preprocess(tmp_path / "nonexistent.csv", tmp_path / "output.csv")`
> **Type:** Arithmetic operation

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 122
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 122
- **Code lines:** 102
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 17

---
*Documentation generated for: mlops-project-documentation*
*File: test_preprocessing.py*
---

# mlops-project-documentation: test_evaluate.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/unit/test_evaluate.py`
- **Total lines:** 168
- **File size:** 6791 bytes

## Line Type Summary
- **Code:** 132
- **Comment:** 0
- **Empty:** 33
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add quality gate with thresholds`
> **Type:** TODO: high - Add quality gate with thresholds

### Line   2
> **Code:** `# TODO: medium - Implement comparison vs current production model`
> **Type:** TODO: medium - Implement comparison vs current production model

### Line   3
> **Code:** `# TODO: low - Add metrics export for Evidence Pack`
> **Type:** TODO: low - Add metrics export for Evidence Pack

### Line   4
> **Code:** `"""Tests for src.models.evaluate module (demand forecasting)."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import os`
> **Type:** Imports a module

### Line   8
> **Code:** `import sys`
> **Type:** Imports a module

### Line   9
> **Code:** `import tempfile`
> **Type:** Imports a module

### Line  10
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** `from unittest.mock import MagicMock, patch, PropertyMock`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  14
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  15
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  19
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `from src.models.evaluate import evaluate, evaluate_model, DEFAULT_THRE...`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from src.features.build_features import FEATURE_ORDER, TARGET_FEATURE`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `class TestEvaluate:`
> **Type:** Class definition

### Line  26
> **Code:** `"""Test model evaluation and validation gates for demand forecasting."...`
> **Type:** Logical operation

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `def _create_mock_model(self, perfect=False):`
> **Type:** Function definition

### Line  29
> **Code:** `"""Create a mock model with predictable predictions."""`
> **Type:** Code statement

### Line  30
> **Code:** `model = MagicMock()`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `if perfect:`
> **Type:** Conditional statement

### Line  32
> **Code:** `def predict(X):`
> **Type:** Function definition

### Line  33
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  34
> **Code:** `return np.random.uniform(20, 60, size=len(X))`
> **Type:** Returns a value from a function

### Line  35
> **Code:** `model.predict = predict`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `else:`
> **Type:** Else block

### Line  37
> **Code:** `def predict(X):`
> **Type:** Function definition

### Line  38
> **Code:** `return np.full(len(X), 30.0)`
> **Type:** Returns a value from a function

### Line  39
> **Code:** `model.predict = predict`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `return model`
> **Type:** Returns a value from a function

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `def _create_test_data(self, n=100):`
> **Type:** Function definition

### Line  43
> **Code:** `"""Create test features and labels."""`
> **Type:** Logical operation

### Line  44
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  45
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `col: np.random.randn(n) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line  47
> **Code:** `})`
> **Type:** Code statement

### Line  48
> **Code:** `labels = pd.Series(np.random.uniform(10, 80, n), name=TARGET_FEATURE)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `return features, labels`
> **Type:** Returns a value from a function

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line  52
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line  53
> **Code:** `def test_evaluate_model_returns_metrics(self, mock_load_test, mock_res...`
> **Type:** Function definition

### Line  54
> **Code:** `"""evaluate_model should return all expected metrics."""`
> **Type:** Code statement

### Line  55
> **Code:** `features, labels = self._create_test_data(50)`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `mock_resolve_model.return_value = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `model = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `metrics = evaluate_model(model, features, labels)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `assert "rmse" in metrics`
> **Type:** Enforces a condition

### Line  63
> **Code:** `assert "mae" in metrics`
> **Type:** Enforces a condition

### Line  64
> **Code:** `assert "r2" in metrics`
> **Type:** Enforces a condition

### Line  65
> **Code:** `assert "mape" in metrics`
> **Type:** Enforces a condition

### Line  66
> **Code:** `assert "n_samples" in metrics`
> **Type:** Enforces a condition

### Line  67
> **Code:** `assert metrics["n_samples"] == 50`
> **Type:** Enforces a condition

### Line  68
> **Code:** `assert metrics["rmse"] >= 0`
> **Type:** Enforces a condition

### Line  69
> **Code:** `assert metrics["mae"] >= 0`
> **Type:** Enforces a condition

### Line  70
> **Code:** `assert metrics["r2"] <= 1.0`
> **Type:** Enforces a condition

### Line  71
> **Code:** `assert metrics["mape"] >= 0`
> **Type:** Enforces a condition

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line  74
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line  75
> **Code:** `def test_evaluate_returns_report_with_gates(self, mock_load_test, mock...`
> **Type:** Function definition

### Line  76
> **Code:** `"""evaluate should return a report with gates_passed."""`
> **Type:** Logical operation

### Line  77
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `mock_resolve_model.return_value = self._create_mock_model(perfect=True...`
> **Type:** Assignment/comparison

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_rep...`
> **Type:** Context manager

### Line  82
> **Code:** `with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):`
> **Type:** Context manager

### Line  83
> **Code:** `report = evaluate(thresholds={"min_r2": 0.5, "max_mape": 30.0})`
> **Type:** Assignment/comparison

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `assert "metrics" in report`
> **Type:** Enforces a condition

### Line  86
> **Code:** `assert "thresholds" in report`
> **Type:** Enforces a condition

### Line  87
> **Code:** `assert "gates" in report`
> **Type:** Enforces a condition

### Line  88
> **Code:** `assert "gates_passed" in report`
> **Type:** Enforces a condition

### Line  89
> **Code:** `assert isinstance(report["gates_passed"], bool)`
> **Type:** Enforces a condition

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line  92
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line  93
> **Code:** `def test_evaluate_uses_default_thresholds(self, mock_load_test, mock_r...`
> **Type:** Function definition

### Line  94
> **Code:** `"""evaluate should use DEFAULT_THRESHOLDS when none provided."""`
> **Type:** Code statement

### Line  95
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `mock_resolve_model.return_value = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_rep...`
> **Type:** Context manager

### Line 100
> **Code:** `with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):`
> **Type:** Context manager

### Line 101
> **Code:** `report = evaluate()`
> **Type:** Assignment/comparison

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `assert report["thresholds"]["min_r2"] == DEFAULT_THRESHOLDS["min_r2"]`
> **Type:** Enforces a condition

### Line 104
> **Code:** `assert report["thresholds"]["max_mape"] == DEFAULT_THRESHOLDS["max_map...`
> **Type:** Enforces a condition

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 107
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 108
> **Code:** `def test_evaluate_writes_report_file(self, mock_load_test, mock_resolv...`
> **Type:** Function definition

### Line 109
> **Code:** `"""evaluate should write report to LATEST_REPORT."""`
> **Type:** Logical operation

### Line 110
> **Code:** `features, labels = self._create_test_data(50)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `mock_resolve_model.return_value = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_rep...`
> **Type:** Context manager

### Line 115
> **Code:** `with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):`
> **Type:** Context manager

### Line 116
> **Code:** `report = evaluate()`
> **Type:** Assignment/comparison

### Line 117
> **Code:** ``
> **Type:** Empty line

### Line 118
> **Code:** `report_file = tmp_path / "latest_report.json"`
> **Type:** Assignment/comparison

### Line 119
> **Code:** `assert report_file.exists()`
> **Type:** Enforces a condition

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `with report_file.open() as f:`
> **Type:** Context manager

### Line 122
> **Code:** `saved_report = json.load(f)`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `assert saved_report["gates_passed"] == report["gates_passed"]`
> **Type:** Enforces a condition

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `def test_load_test_set_prefers_reference_csv(self, tmp_path, monkeypat...`
> **Type:** Function definition

### Line 126
> **Code:** `"""_load_test_set should prefer reference.csv when available."""`
> **Type:** Code statement

### Line 127
> **Code:** `reference_dir = tmp_path / "data" / "monitoring"`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `reference_dir.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 129
> **Code:** ``
> **Type:** Empty line

### Line 130
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 131
> **Code:** `col: np.random.randn(50) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line 132
> **Code:** `})`
> **Type:** Code statement

### Line 133
> **Code:** `features[TARGET_FEATURE] = np.random.uniform(10, 80, 50)`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `features["prediction"] = np.random.uniform(10, 80, 50)`
> **Type:** Assignment/comparison

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `ref_path = reference_dir / "reference.csv"`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `features.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 138
> **Code:** ``
> **Type:** Empty line

### Line 139
> **Code:** `with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):`
> **Type:** Context manager

### Line 140
> **Code:** `X_test, y_test = _load_test_set(tmp_path / "features.parquet")`
> **Type:** Assignment/comparison

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `assert len(X_test) == 50`
> **Type:** Enforces a condition

### Line 143
> **Code:** `assert len(y_test) == 50`
> **Type:** Enforces a condition

### Line 144
> **Code:** `assert list(X_test.columns) == FEATURE_ORDER`
> **Type:** Enforces a condition

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** `def test_load_test_set_fallback_to_parquet(self, tmp_path):`
> **Type:** Function definition

### Line 147
> **Code:** `"""_load_test_set should fall back to parquet when no reference.csv.""...`
> **Type:** Code statement

### Line 148
> **Code:** `features_dir = tmp_path / "data" / "features"`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `features_dir.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `col: np.random.randn(100) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line 153
> **Code:** `})`
> **Type:** Code statement

### Line 154
> **Code:** `features[TARGET_FEATURE] = np.random.uniform(10, 80, 100)`
> **Type:** Assignment/comparison

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** `parquet_path = features_dir / "features.parquet"`
> **Type:** Assignment/comparison

### Line 157
> **Code:** `features.to_parquet(parquet_path, index=False)`
> **Type:** Assignment/comparison

### Line 158
> **Code:** ``
> **Type:** Empty line

### Line 159
> **Code:** `with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):`
> **Type:** Context manager

### Line 160
> **Code:** `with patch("src.models.evaluate.DEFAULT_DATA", parquet_path):`
> **Type:** Context manager

### Line 161
> **Code:** `X_test, y_test = _load_test_set(parquet_path)`
> **Type:** Assignment/comparison

### Line 162
> **Code:** ``
> **Type:** Empty line

### Line 163
> **Code:** `assert len(X_test) == 100`
> **Type:** Enforces a condition

### Line 164
> **Code:** `assert len(y_test) == 100`
> **Type:** Enforces a condition

### Line 165
> **Code:** ``
> **Type:** Empty line

### Line 166
> **Code:** ``
> **Type:** Empty line

### Line 167
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 168
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 168
- **Code lines:** 132
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 33

---
*Documentation generated for: mlops-project-documentation*
*File: test_evaluate.py*
---

# mlops-project-documentation: test_api.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/unit/test_api.py`
- **Total lines:** 194
- **File size:** 6649 bytes

## Line Type Summary
- **Code:** 151
- **Comment:** 0
- **Empty:** 40
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for FastAPI demand forecasting inference API."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** `from unittest.mock import MagicMock, patch`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  12
> **Code:** `from fastapi.testclient import TestClient`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  16
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `from src.api.main import app`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from src.api.schemas import DemandPredictionRequest, PredictionRespons...`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `client = TestClient(app)`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `def _valid_payload() -> dict:`
> **Type:** Function definition

### Line  26
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  27
> **Code:** `"store_id": 1,`
> **Type:** Logical operation

### Line  28
> **Code:** `"sku_id": 1,`
> **Type:** Code statement

### Line  29
> **Code:** `"day_of_week": 0,`
> **Type:** Code statement

### Line  30
> **Code:** `"month": 12,`
> **Type:** Code statement

### Line  31
> **Code:** `"is_holiday": 1,`
> **Type:** Code statement

### Line  32
> **Code:** `"price": 29.99,`
> **Type:** Code statement

### Line  33
> **Code:** `"promotion": 1,`
> **Type:** Code statement

### Line  34
> **Code:** `"temperature": 35.0,`
> **Type:** Code statement

### Line  35
> **Code:** `"inventory_level": 200,`
> **Type:** Logical operation

### Line  36
> **Code:** `"competitor_price": 32.99,`
> **Type:** Logical operation

### Line  37
> **Code:** `"store_traffic": 500,`
> **Type:** Logical operation

### Line  38
> **Code:** `}`
> **Type:** Code statement

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `class TestHealthEndpoint:`
> **Type:** Class definition

### Line  42
> **Code:** `"""Test /health endpoint."""`
> **Type:** Arithmetic operation

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `def test_health_returns_200(self):`
> **Type:** Function definition

### Line  45
> **Code:** `"""GET /health should return 200 with status ok or degraded."""`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `response = client.get("/health")`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line  48
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `assert "status" in data`
> **Type:** Enforces a condition

### Line  50
> **Code:** `assert data["status"] in ("ok", "degraded")`
> **Type:** Enforces a condition

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `class TestPredictEndpoint:`
> **Type:** Class definition

### Line  54
> **Code:** `"""Test /predict endpoint."""`
> **Type:** Arithmetic operation

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `@patch("src.api.main.loader.get_bundle")`
> **Type:** Function call

### Line  57
> **Code:** `def test_predict_valid_payload_returns_prediction(self, mock_get_bundl...`
> **Type:** Function definition

### Line  58
> **Code:** `"""POST /predict with valid payload returns predicted units and bucket...`
> **Type:** Arithmetic operation

### Line  59
> **Code:** `mock_bundle = MagicMock()`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `mock_bundle.model_name = "demand_model"`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `mock_bundle.version = "1"`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `mock_bundle.predict.return_value = [42.5]`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `mock_get_bundle.return_value = mock_bundle`
> **Type:** Assignment/comparison

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `response = client.post("/predict", json=_valid_payload())`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line  67
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `assert "predicted_units" in data`
> **Type:** Enforces a condition

### Line  69
> **Code:** `assert "demand_bucket" in data`
> **Type:** Enforces a condition

### Line  70
> **Code:** `assert isinstance(data["predicted_units"], int)`
> **Type:** Enforces a condition

### Line  71
> **Code:** `assert data["demand_bucket"] in ("low", "medium", "high", "very_high")`
> **Type:** Enforces a condition

### Line  72
> **Code:** `assert data["model_name"] == "demand_model"`
> **Type:** Enforces a condition

### Line  73
> **Code:** `assert data["model_version"] == "1"`
> **Type:** Enforces a condition

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `@patch("src.api.main.loader.get_bundle")`
> **Type:** Function call

### Line  76
> **Code:** `def test_predict_batch_returns_list(self, mock_get_bundle):`
> **Type:** Function definition

### Line  77
> **Code:** `"""POST /predict with list payload returns list of predictions."""`
> **Type:** Arithmetic operation

### Line  78
> **Code:** `mock_bundle = MagicMock()`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `mock_bundle.model_name = "demand_model"`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `mock_bundle.version = "1"`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `mock_bundle.predict.return_value = [42.5, 15.3]`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `mock_get_bundle.return_value = mock_bundle`
> **Type:** Assignment/comparison

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `payload = [_valid_payload(), _valid_payload()]`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `response = client.post("/predict", json=payload)`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line  87
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `assert isinstance(data, list)`
> **Type:** Enforces a condition

### Line  89
> **Code:** `assert len(data) == 2`
> **Type:** Enforces a condition

### Line  90
> **Code:** `for item in data:`
> **Type:** For loop

### Line  91
> **Code:** `assert "predicted_units" in item`
> **Type:** Enforces a condition

### Line  92
> **Code:** `assert "demand_bucket" in item`
> **Type:** Enforces a condition

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `def test_predict_empty_batch_returns_422(self):`
> **Type:** Function definition

### Line  95
> **Code:** `"""POST /predict with empty list returns 422."""`
> **Type:** Arithmetic operation

### Line  96
> **Code:** `response = client.post("/predict", json=[])`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `assert response.status_code == 422`
> **Type:** Enforces a condition

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def test_predict_missing_fields_returns_422(self):`
> **Type:** Function definition

### Line 100
> **Code:** `"""POST /predict with missing required fields returns 422."""`
> **Type:** Arithmetic operation

### Line 101
> **Code:** `response = client.post("/predict", json={})`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `assert response.status_code == 422`
> **Type:** Enforces a condition

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `class TestMetricsEndpoint:`
> **Type:** Class definition

### Line 106
> **Code:** `"""Test /metrics endpoint."""`
> **Type:** Arithmetic operation

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `def test_metrics_exposes_prometheus_metrics(self):`
> **Type:** Function definition

### Line 109
> **Code:** `"""GET /metrics should return Prometheus metrics text."""`
> **Type:** Arithmetic operation

### Line 110
> **Code:** `response = client.get("/metrics")`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line 112
> **Code:** `content = response.text`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `assert "http_requests_total" in content or "http_request_duration_seco...`
> **Type:** Enforces a condition

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `class TestModelInfoEndpoint:`
> **Type:** Class definition

### Line 117
> **Code:** `"""Test /model-info endpoint."""`
> **Type:** Arithmetic operation

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** `@patch("src.api.main.loader.get_bundle")`
> **Type:** Function call

### Line 120
> **Code:** `def test_model_info_returns_metadata(self, mock_get_bundle):`
> **Type:** Function definition

### Line 121
> **Code:** `"""GET /model-info should return model metadata."""`
> **Type:** Arithmetic operation

### Line 122
> **Code:** `mock_bundle = MagicMock()`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `mock_bundle.model_name = "demand_model"`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `mock_bundle.version = "3"`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `mock_bundle.run_id = "abc123"`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `mock_get_bundle.return_value = mock_bundle`
> **Type:** Assignment/comparison

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** `response = client.get("/model-info")`
> **Type:** Assignment/comparison

### Line 129
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line 130
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line 131
> **Code:** `assert data["model_name"] == "demand_model"`
> **Type:** Enforces a condition

### Line 132
> **Code:** `assert data["model_version"] == "3"`
> **Type:** Enforces a condition

### Line 133
> **Code:** `assert data["run_id"] == "abc123"`
> **Type:** Enforces a condition

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `class TestSchemas:`
> **Type:** Class definition

### Line 137
> **Code:** `"""Test Pydantic request/response schemas."""`
> **Type:** Arithmetic operation

### Line 138
> **Code:** ``
> **Type:** Empty line

### Line 139
> **Code:** `def test_demand_prediction_request_valid(self):`
> **Type:** Function definition

### Line 140
> **Code:** `"""Valid payload should create DemandPredictionRequest."""`
> **Type:** Logical operation

### Line 141
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `request = DemandPredictionRequest(**payload)`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `df = request.to_dataframe()`
> **Type:** Assignment/comparison

### Line 144
> **Code:** `assert len(df) == 1`
> **Type:** Enforces a condition

### Line 145
> **Code:** `assert list(df.columns) == list(payload.keys())`
> **Type:** Enforces a condition

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `def test_demand_prediction_request_invalid_store_id(self):`
> **Type:** Function definition

### Line 148
> **Code:** `"""Invalid store_id should raise validation error."""`
> **Type:** Logical operation

### Line 149
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `payload["store_id"] = 0`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `with pytest.raises(Exception):`
> **Type:** Context manager

### Line 152
> **Code:** `DemandPredictionRequest(**payload)`
> **Type:** Arithmetic operation

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** `def test_demand_prediction_request_invalid_price(self):`
> **Type:** Function definition

### Line 155
> **Code:** `"""Negative price should raise validation error."""`
> **Type:** Logical operation

### Line 156
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 157
> **Code:** `payload["price"] = -10.0`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `with pytest.raises(Exception):`
> **Type:** Context manager

### Line 159
> **Code:** `DemandPredictionRequest(**payload)`
> **Type:** Arithmetic operation

### Line 160
> **Code:** ``
> **Type:** Empty line

### Line 161
> **Code:** `def test_demand_prediction_request_invalid_temperature(self):`
> **Type:** Function definition

### Line 162
> **Code:** `"""Temperature out of range should raise validation error."""`
> **Type:** Logical operation

### Line 163
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `payload["temperature"] = 200.0`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `with pytest.raises(Exception):`
> **Type:** Context manager

### Line 166
> **Code:** `DemandPredictionRequest(**payload)`
> **Type:** Arithmetic operation

### Line 167
> **Code:** ``
> **Type:** Empty line

### Line 168
> **Code:** ``
> **Type:** Empty line

### Line 169
> **Code:** `class TestDemandBuckets:`
> **Type:** Class definition

### Line 170
> **Code:** `"""Test demand bucket classification."""`
> **Type:** Logical operation

### Line 171
> **Code:** ``
> **Type:** Empty line

### Line 172
> **Code:** `def test_low_bucket(self):`
> **Type:** Function definition

### Line 173
> **Code:** `from src.api.schemas import _demand_bucket`
> **Type:** Imports specific names from a module

### Line 174
> **Code:** `assert _demand_bucket(10) == "low"`
> **Type:** Enforces a condition

### Line 175
> **Code:** `assert _demand_bucket(15) == "low"`
> **Type:** Enforces a condition

### Line 176
> **Code:** ``
> **Type:** Empty line

### Line 177
> **Code:** `def test_medium_bucket(self):`
> **Type:** Function definition

### Line 178
> **Code:** `from src.api.schemas import _demand_bucket`
> **Type:** Imports specific names from a module

### Line 179
> **Code:** `assert _demand_bucket(20) == "medium"`
> **Type:** Enforces a condition

### Line 180
> **Code:** `assert _demand_bucket(35) == "medium"`
> **Type:** Enforces a condition

### Line 181
> **Code:** ``
> **Type:** Empty line

### Line 182
> **Code:** `def test_high_bucket(self):`
> **Type:** Function definition

### Line 183
> **Code:** `from src.api.schemas import _demand_bucket`
> **Type:** Imports specific names from a module

### Line 184
> **Code:** `assert _demand_bucket(40) == "high"`
> **Type:** Enforces a condition

### Line 185
> **Code:** `assert _demand_bucket(60) == "high"`
> **Type:** Enforces a condition

### Line 186
> **Code:** ``
> **Type:** Empty line

### Line 187
> **Code:** `def test_very_high_bucket(self):`
> **Type:** Function definition

### Line 188
> **Code:** `from src.api.schemas import _demand_bucket`
> **Type:** Imports specific names from a module

### Line 189
> **Code:** `assert _demand_bucket(65) == "very_high"`
> **Type:** Enforces a condition

### Line 190
> **Code:** `assert _demand_bucket(100) == "very_high"`
> **Type:** Enforces a condition

### Line 191
> **Code:** ``
> **Type:** Empty line

### Line 192
> **Code:** ``
> **Type:** Empty line

### Line 193
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 194
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 194
- **Code lines:** 151
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 40

---
*Documentation generated for: mlops-project-documentation*
*File: test_api.py*
---

# mlops-project-documentation: test_data_quality.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/tests/data/test_data_quality.py`
- **Total lines:** 90
- **File size:** 3171 bytes

## Line Type Summary
- **Code:** 64
- **Comment:** 0
- **Empty:** 23
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for data quality validation for demand forecasting data."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  11
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `DATA_PATH = PROJECT_ROOT / "data" / "raw" / "demand_data.csv"`
> **Type:** Assignment/comparison

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `class TestDataQuality:`
> **Type:** Class definition

### Line  21
> **Code:** `"""Validate the demand dataset against quality expectations."""`
> **Type:** Logical operation

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `@pytest.fixture(scope="class")`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `def dataset(self):`
> **Type:** Function definition

### Line  25
> **Code:** `"""Load the raw demand dataset."""`
> **Type:** Logical operation

### Line  26
> **Code:** `if not DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  27
> **Code:** `pytest.skip(f"Dataset not found at {DATA_PATH}")`
> **Type:** Logical operation

### Line  28
> **Code:** `return pd.read_csv(DATA_PATH)`
> **Type:** Returns a value from a function

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def test_dataset_exists(self, dataset):`
> **Type:** Function definition

### Line  31
> **Code:** `"""Dataset file should exist and be readable."""`
> **Type:** Logical operation

### Line  32
> **Code:** `assert len(dataset) > 0`
> **Type:** Enforces a condition

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `def test_row_count_sufficient(self, dataset):`
> **Type:** Function definition

### Line  35
> **Code:** `"""Row count should be at least 1000."""`
> **Type:** Code statement

### Line  36
> **Code:** `assert len(dataset) >= 1000`
> **Type:** Enforces a condition

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `def test_critical_columns_not_null(self, dataset):`
> **Type:** Function definition

### Line  39
> **Code:** `"""Critical columns should have no null values."""`
> **Type:** Code statement

### Line  40
> **Code:** `for col in ["store_id", "sku_id", "price", "units_sold"]:`
> **Type:** For loop

### Line  41
> **Code:** `assert col in dataset.columns, f"Missing column: {col}"`
> **Type:** Enforces a condition

### Line  42
> **Code:** `assert dataset[col].notna().all(), f"Column {col} has null values"`
> **Type:** Enforces a condition

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `def test_store_id_range(self, dataset):`
> **Type:** Function definition

### Line  45
> **Code:** `"""store_id should be between 1 and 100."""`
> **Type:** Logical operation

### Line  46
> **Code:** `assert dataset["store_id"].between(1, 100).all()`
> **Type:** Enforces a condition

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def test_sku_id_range(self, dataset):`
> **Type:** Function definition

### Line  49
> **Code:** `"""sku_id should be between 1 and 200."""`
> **Type:** Logical operation

### Line  50
> **Code:** `assert dataset["sku_id"].between(1, 200).all()`
> **Type:** Enforces a condition

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def test_price_positive(self, dataset):`
> **Type:** Function definition

### Line  53
> **Code:** `"""price should be positive."""`
> **Type:** Code statement

### Line  54
> **Code:** `assert (dataset["price"] >= 0).all()`
> **Type:** Enforces a condition

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `def test_units_sold_non_negative(self, dataset):`
> **Type:** Function definition

### Line  57
> **Code:** `"""units_sold should be non-negative."""`
> **Type:** Arithmetic operation

### Line  58
> **Code:** `assert (dataset["units_sold"] >= 0).all()`
> **Type:** Enforces a condition

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `def test_day_of_week_range(self, dataset):`
> **Type:** Function definition

### Line  61
> **Code:** `"""day_of_week should be between 0 and 6."""`
> **Type:** Logical operation

### Line  62
> **Code:** `assert dataset["day_of_week"].between(0, 6).all()`
> **Type:** Enforces a condition

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def test_month_range(self, dataset):`
> **Type:** Function definition

### Line  65
> **Code:** `"""month should be between 1 and 12."""`
> **Type:** Logical operation

### Line  66
> **Code:** `assert dataset["month"].between(1, 12).all()`
> **Type:** Enforces a condition

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def test_is_holiday_values(self, dataset):`
> **Type:** Function definition

### Line  69
> **Code:** `"""is_holiday should only be 0 or 1."""`
> **Type:** Logical operation

### Line  70
> **Code:** `assert set(dataset["is_holiday"].unique()).issubset({0, 1})`
> **Type:** Enforces a condition

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `def test_promotion_values(self, dataset):`
> **Type:** Function definition

### Line  73
> **Code:** `"""promotion should only be 0 or 1."""`
> **Type:** Logical operation

### Line  74
> **Code:** `assert set(dataset["promotion"].unique()).issubset({0, 1})`
> **Type:** Enforces a condition

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `def test_temperature_range(self, dataset):`
> **Type:** Function definition

### Line  77
> **Code:** `"""temperature should be reasonable (-50 to 150)."""`
> **Type:** Arithmetic operation

### Line  78
> **Code:** `assert dataset["temperature"].between(-50, 150).all()`
> **Type:** Enforces a condition

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def test_inventory_level_positive(self, dataset):`
> **Type:** Function definition

### Line  81
> **Code:** `"""inventory_level should be positive."""`
> **Type:** Logical operation

### Line  82
> **Code:** `assert (dataset["inventory_level"] >= 0).all()`
> **Type:** Enforces a condition

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `def test_store_traffic_positive(self, dataset):`
> **Type:** Function definition

### Line  85
> **Code:** `"""store_traffic should be positive."""`
> **Type:** Logical operation

### Line  86
> **Code:** `assert (dataset["store_traffic"] >= 0).all()`
> **Type:** Enforces a condition

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  90
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 90
- **Code lines:** 64
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 23

---
*Documentation generated for: mlops-project-documentation*
*File: test_data_quality.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/airflow/__init__.py`
- **Total lines:** 4
- **File size:** 208 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""airflow package: DAGs and operators for the churn MLOps pipeline.""...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: training_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/airflow/dags/training_pipeline.py`
- **Total lines:** 108
- **File size:** 4047 bytes

## Line Type Summary
- **Code:** 80
- **Comment:** 0
- **Empty:** 25
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add data validation before training`
> **Type:** TODO: high - Add data validation before training

### Line   2
> **Code:** `# TODO: medium - Implement hyperparameter logging`
> **Type:** TODO: medium - Implement hyperparameter logging

### Line   3
> **Code:** `# TODO: low - Add model explainability integration`
> **Type:** TODO: low - Add model explainability integration

### Line   4
> **Code:** `"""DAG: full training pipeline.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Runs the complete model lifecycle on the current data snapshot:`
> **Type:** Code statement

### Line   7
> **Code:** `validate -> preprocess -> build_features -> train -> evaluate -> promo...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `The MLflow run_id produced by training is passed to the evaluation tas...`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import sys`
> **Type:** Imports a module

### Line  14
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from airflow.operators.python import PythonOperator`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from airflow.utils.dates import days_ago`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from airflow import DAG`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.data.preprocessing import preprocess  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from src.data.validation import validate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from src.features.build_features import build_features  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.models.evaluate import evaluate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** `from src.models.promote import promote_candidate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from src.models.train import train_model  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `from src.monitoring.alerting import send_alert  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `DAG_ID = "training_pipeline"`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `DEFAULT_ARGS = {`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `"owner": "mlops",`
> **Type:** Code statement

### Line  36
> **Code:** `"depends_on_past": False,`
> **Type:** Code statement

### Line  37
> **Code:** `"retries": 1,`
> **Type:** Code statement

### Line  38
> **Code:** `"retry_delay": timedelta(minutes=5),`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `"on_failure_callback": lambda context: send_alert(`
> **Type:** Code statement

### Line  40
> **Code:** `f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", se...`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `),`
> **Type:** Code statement

### Line  42
> **Code:** `}`
> **Type:** Code statement

### Line  43
> **Code:** `dag = DAG(`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `dag_id=DAG_ID,`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `default_args=DEFAULT_ARGS,`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `schedule_interval="@weekly",`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `start_date=days_ago(2),`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `catchup=False,`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `tags=["training", "mlflow"],`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `doc_md=(`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `"Validates data, rebuilds features, trains and registers a new churn m...`
> **Type:** Logical operation

### Line  52
> **Code:** `"then promotes it if it passes the gates."`
> **Type:** Code statement

### Line  53
> **Code:** `),`
> **Type:** Code statement

### Line  54
> **Code:** `)`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def _validate() -> str:`
> **Type:** Function definition

### Line  58
> **Code:** `summary = validate()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if summary["failed"]:`
> **Type:** Conditional statement

### Line  60
> **Code:** `raise RuntimeError(f"data validation failed: {summary['failed']} expec...`
> **Type:** Raises an exception

### Line  61
> **Code:** `return f"validation passed {summary['passed']}/{summary['total']}"`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def _preprocess() -> str:`
> **Type:** Function definition

### Line  65
> **Code:** `df = preprocess()`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `return f"preprocessed {len(df)} rows"`
> **Type:** Returns a value from a function

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def _build_features() -> str:`
> **Type:** Function definition

### Line  70
> **Code:** `features = build_features()`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `return f"built {features.shape[0]} rows x {features.shape[1]} features...`
> **Type:** Returns a value from a function

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `def _train(**context) -> str:`
> **Type:** Function definition

### Line  75
> **Code:** `result = train_model()`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `context["task_instance"].xcom_push(key="run_id", value=result["run_id"...`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `context["task_instance"].xcom_push(key="r2", value=result["metrics"]["...`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `return f"training completed run_id={result['run_id']} r2={result['metr...`
> **Type:** Returns a value from a function

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `def _evaluate(**context) -> str:`
> **Type:** Function definition

### Line  82
> **Code:** `run_id = context["task_instance"].xcom_pull(task_ids="train_model", ke...`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `report = evaluate(run_id=run_id)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `if not report["gates_passed"]:`
> **Type:** Conditional statement

### Line  85
> **Code:** `raise RuntimeError("evaluation gates not met; stopping before promotio...`
> **Type:** Raises an exception

### Line  86
> **Code:** `return f"evaluation passed r2={report['metrics']['r2']:.4f}"`
> **Type:** Returns a value from a function

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def _promote() -> str:`
> **Type:** Function definition

### Line  90
> **Code:** `production = promote_candidate()`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `return f"promoted version {production['version']} to production"`
> **Type:** Returns a value from a function

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `def _notify(**context) -> str:`
> **Type:** Function definition

### Line  95
> **Code:** `r2 = context["task_instance"].xcom_pull(task_ids="train_model", key="r...`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `send_alert(f"training_pipeline completed | r2={r2:.4f}", severity="inf...`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `return "notification sent"`
> **Type:** Returns a value from a function

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `validate_data = PythonOperator(task_id="validate_data", python_callabl...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `preprocess_data = PythonOperator(task_id="preprocess", python_callable...`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `build_features_task = PythonOperator(task_id="build_features", python_...`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `train_task = PythonOperator(task_id="train_model", python_callable=_tr...`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `evaluate_task = PythonOperator(task_id="evaluate_model", python_callab...`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `promote_task = PythonOperator(task_id="promote_model", python_callable...`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `notify_task = PythonOperator(task_id="notify_team", python_callable=_n...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `validate_data >> preprocess_data >> build_features_task >> train_task ...`
> **Type:** Comparison operation

## Summary
- **Total lines:** 108
- **Code lines:** 80
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 25

---
*Documentation generated for: mlops-project-documentation*
*File: training_pipeline.py*
---

# mlops-project-documentation: retraining_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/airflow/dags/retraining_pipeline.py`
- **Total lines:** 118
- **File size:** 4284 bytes

## Line Type Summary
- **Code:** 89
- **Comment:** 0
- **Empty:** 26
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add data validation before training`
> **Type:** TODO: high - Add data validation before training

### Line   2
> **Code:** `# TODO: medium - Implement hyperparameter logging`
> **Type:** TODO: medium - Implement hyperparameter logging

### Line   3
> **Code:** `# TODO: low - Add model explainability integration`
> **Type:** TODO: low - Add model explainability integration

### Line   4
> **Code:** `"""DAG: retraining triggered by drift detection.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Runs daily. The `check_drift` task short-circuits the pipeline: if no ...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `was detected by Evidently since the last run, nothing is retrained. On...`
> **Type:** Logical operation

### Line   8
> **Code:** `the full loop executes: preprocess -> features -> train -> evaluate ->`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `promote-if-better -> notify. Promotion only happens when the candidate...`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `the current production model on the same test set.`
> **Type:** Code statement

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import sys`
> **Type:** Imports a module

### Line  16
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `from airflow.operators.python import PythonOperator, ShortCircuitOpera...`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** `from airflow.utils.dates import days_ago`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `from airflow import DAG`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `from src.data.preprocessing import preprocess  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.features.build_features import build_features  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** `from src.models.evaluate import evaluate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from src.models.promote import promote_candidate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `from src.models.train import train_model  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** `from src.monitoring.alerting import send_alert  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  33
> **Code:** `from src.monitoring.drift_detection import detect_drift  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `DAG_ID = "retraining_pipeline"`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `DEFAULT_ARGS = {`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `"owner": "mlops",`
> **Type:** Code statement

### Line  38
> **Code:** `"depends_on_past": False,`
> **Type:** Code statement

### Line  39
> **Code:** `"retries": 1,`
> **Type:** Code statement

### Line  40
> **Code:** `"retry_delay": timedelta(minutes=5),`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `"on_failure_callback": lambda context: send_alert(`
> **Type:** Code statement

### Line  42
> **Code:** `f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", se...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `),`
> **Type:** Code statement

### Line  44
> **Code:** `}`
> **Type:** Code statement

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `dag = DAG(`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `dag_id=DAG_ID,`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `default_args=DEFAULT_ARGS,`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `schedule_interval="@daily",`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `start_date=days_ago(2),`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `catchup=False,`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `tags=["retraining", "drift"],`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `doc_md="Retrains the model when Evidently detects drift on the product...`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `)`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def _check_drift() -> bool:`
> **Type:** Function definition

### Line  58
> **Code:** `report = detect_drift()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if report["drift_detected"]:`
> **Type:** Conditional statement

### Line  60
> **Code:** `send_alert(`
> **Type:** Code statement

### Line  61
> **Code:** `"drift detected "`
> **Type:** Code statement

### Line  62
> **Code:** `f"(score={report['drift_score']:.3f}, threshold={report['threshold']})...`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `severity="warning",`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `dag=DAG_ID,`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `)`
> **Type:** Code statement

### Line  66
> **Code:** `return True`
> **Type:** Returns a value from a function

### Line  67
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `def _preprocess() -> str:`
> **Type:** Function definition

### Line  71
> **Code:** `df = preprocess()`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `return f"preprocessed {len(df)} rows"`
> **Type:** Returns a value from a function

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `def _build_features() -> str:`
> **Type:** Function definition

### Line  76
> **Code:** `features = build_features()`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `return f"built {features.shape[0]} rows x {features.shape[1]} features...`
> **Type:** Returns a value from a function

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def _train(**context) -> str:`
> **Type:** Function definition

### Line  81
> **Code:** `result = train_model()`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `context["task_instance"].xcom_push(key="run_id", value=result["run_id"...`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `return f"retraining completed run_id={result['run_id']} r2={result['me...`
> **Type:** Returns a value from a function

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def _evaluate(**context) -> str:`
> **Type:** Function definition

### Line  87
> **Code:** `run_id = context["task_instance"].xcom_pull(task_ids="train_model", ke...`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `report = evaluate(run_id=run_id)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `if not report["gates_passed"]:`
> **Type:** Conditional statement

### Line  90
> **Code:** `raise RuntimeError("evaluation gates not met; stopping before promotio...`
> **Type:** Raises an exception

### Line  91
> **Code:** `return f"evaluation passed r2={report['metrics']['r2']:.4f}"`
> **Type:** Returns a value from a function

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `def _promote() -> str:`
> **Type:** Function definition

### Line  95
> **Code:** `production = promote_candidate()`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `send_alert(`
> **Type:** Code statement

### Line  97
> **Code:** `f"retraining promoted model version {production['version']} to product...`
> **Type:** Data structure operation

### Line  98
> **Code:** `f"(r2={production['metrics']['r2']:.4f})",`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `severity="info",`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `dag=DAG_ID,`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `)`
> **Type:** Code statement

### Line 102
> **Code:** `return f"promoted version {production['version']}"`
> **Type:** Returns a value from a function

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `def _notify() -> str:`
> **Type:** Function definition

### Line 106
> **Code:** `send_alert("retraining_pipeline completed", severity="info", dag=DAG_I...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `return "notification sent"`
> **Type:** Returns a value from a function

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `check_drift = ShortCircuitOperator(task_id="check_drift", python_calla...`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `preprocess_task = PythonOperator(task_id="preprocess", python_callable...`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `build_features_task = PythonOperator(task_id="build_features", python_...`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `train_task = PythonOperator(task_id="train_model", python_callable=_tr...`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `evaluate_task = PythonOperator(task_id="evaluate_model", python_callab...`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `promote_task = PythonOperator(task_id="promote_model", python_callable...`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `notify_task = PythonOperator(task_id="notify_team", python_callable=_n...`
> **Type:** Assignment/comparison

### Line 117
> **Code:** ``
> **Type:** Empty line

### Line 118
> **Code:** `check_drift >> preprocess_task >> build_features_task >> train_task >>...`
> **Type:** Comparison operation

## Summary
- **Total lines:** 118
- **Code lines:** 89
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 26

---
*Documentation generated for: mlops-project-documentation*
*File: retraining_pipeline.py*
---

# mlops-project-documentation: data_ingestion_dag.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/airflow/dags/data_ingestion_dag.py`
- **Total lines:** 76
- **File size:** 2404 bytes

## Line Type Summary
- **Code:** 57
- **Comment:** 0
- **Empty:** 16
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add tag mapping version control`
> **Type:** TODO: high - Add tag mapping version control

### Line   2
> **Code:** `# TODO: medium - Implement store-and-forward buffer health checks`
> **Type:** TODO: medium - Implement store-and-forward buffer health checks

### Line   3
> **Code:** `# TODO: low - Add unmapped tag alerting`
> **Type:** TODO: low - Add unmapped tag alerting

### Line   4
> **Code:** `"""DAG: periodic data ingestion.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Scheduled every night: pulls the latest raw data, validates it with th...`
> **Type:** Code statement

### Line   7
> **Code:** `Great Expectations suite, then versions it with DVC and pushes it to t...`
> **Type:** Logical operation

### Line   8
> **Code:** `configured remote (MinIO). Failures raise an alert through the alertin...`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import sys`
> **Type:** Imports a module

### Line  14
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from airflow.operators.bash import BashOperator`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from airflow.operators.python import PythonOperator`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from airflow.utils.dates import days_ago`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `from airflow import DAG`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `from src.data.ingestion import ingest  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from src.data.validation import validate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.monitoring.alerting import send_alert  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `DAG_ID = "data_ingestion_dag"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `DEFAULT_ARGS = {`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `"owner": "mlops",`
> **Type:** Code statement

### Line  33
> **Code:** `"depends_on_past": False,`
> **Type:** Code statement

### Line  34
> **Code:** `"retries": 2,`
> **Type:** Code statement

### Line  35
> **Code:** `"retry_delay": timedelta(minutes=5),`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `"on_failure_callback": lambda context: send_alert(`
> **Type:** Code statement

### Line  37
> **Code:** `f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", se...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `),`
> **Type:** Code statement

### Line  39
> **Code:** `}`
> **Type:** Code statement

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `dag = DAG(`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `dag_id=DAG_ID,`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `default_args=DEFAULT_ARGS,`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `schedule_interval="0 2 * * *",`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `start_date=days_ago(2),`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `catchup=False,`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `tags=["ingestion", "data"],`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `doc_md="Fetches, validates and DVC-versions the raw churn dataset ever...`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `)`
> **Type:** Code statement

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _ingest() -> str:`
> **Type:** Function definition

### Line  53
> **Code:** `df = ingest()`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `return f"ingested {len(df)} rows"`
> **Type:** Returns a value from a function

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def _validate() -> str:`
> **Type:** Function definition

### Line  58
> **Code:** `summary = validate()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if summary["failed"]:`
> **Type:** Conditional statement

### Line  60
> **Code:** `raise RuntimeError(f"data validation failed: {summary['failed']} expec...`
> **Type:** Raises an exception

### Line  61
> **Code:** `return f"validation passed {summary['passed']}/{summary['total']}"`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `ingest_data = PythonOperator(task_id="ingest_data", python_callable=_i...`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `validate_data = PythonOperator(task_id="validate_data", python_callabl...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `version_data = BashOperator(`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `task_id="version_data",`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `bash_command=(`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `"cd {{ dag_run.conf.get('project_root', '/opt/airflow') }} && "`
> **Type:** Arithmetic operation

### Line  70
> **Code:** `"dvc add data/raw/dataset.csv && dvc commit -f && "`
> **Type:** Arithmetic operation

### Line  71
> **Code:** `"(dvc remote list | grep -q . && dvc push || echo 'no dvc remote confi...`
> **Type:** Arithmetic operation

### Line  72
> **Code:** `),`
> **Type:** Code statement

### Line  73
> **Code:** `dag=dag,`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `)`
> **Type:** Code statement

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `ingest_data >> validate_data >> version_data`
> **Type:** Comparison operation

## Summary
- **Total lines:** 76
- **Code lines:** 57
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 16

---
*Documentation generated for: mlops-project-documentation*
*File: data_ingestion_dag.py*
---

# mlops-project-documentation: drift_sensor.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/airflow/plugins/drift_sensor.py`
- **Total lines:** 43
- **File size:** 1498 bytes

## Line Type Summary
- **Code:** 30
- **Comment:** 0
- **Empty:** 10
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Airflow plugin: drift sensor + shared DAG helpers.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** ``DriftDetectedSensor` polls the drift report produced by`
> **Type:** Logical operation

### Line   7
> **Code:** `src/monitoring/drift_detection.py and succeeds as soon as drift is det...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `which is how the retraining loop is triggered.`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import json`
> **Type:** Imports a module

### Line  14
> **Code:** `import os`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from airflow.plugins_manager import AirflowPlugin`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from airflow.sensors.base import BaseSensorOperator`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `class DriftDetectedSensor(BaseSensorOperator):`
> **Type:** Class definition

### Line  22
> **Code:** `template_fields = ("drift_report_path",)`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def __init__(self, drift_report_path: str | None = None, **kwargs):`
> **Type:** Function definition

### Line  25
> **Code:** `super().__init__(**kwargs)`
> **Type:** Arithmetic operation

### Line  26
> **Code:** `default = Path(os.environ.get("DRIFT_REPORT_PATH", "data/monitoring/dr...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `self.drift_report_path = drift_report_path or str(default)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def poke(self, context: dict) -> bool:`
> **Type:** Function definition

### Line  30
> **Code:** `report = Path(self.drift_report_path)`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `if not report.exists():`
> **Type:** Conditional statement

### Line  32
> **Code:** `self.log.info("drift report %s not found yet", report)`
> **Type:** Arithmetic operation

### Line  33
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  34
> **Code:** `with report.open() as fh:`
> **Type:** Context manager

### Line  35
> **Code:** `payload = json.load(fh)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `detected = bool(payload.get("drift_detected", False))`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `self.log.info("drift_detected=%s score=%s", detected, payload.get("dri...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `return detected`
> **Type:** Returns a value from a function

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `class DriftAlertPlugin(AirflowPlugin):`
> **Type:** Class definition

### Line  42
> **Code:** `name = "mlops_drift_plugin"`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `sensors = [DriftDetectedSensor]`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 43
- **Code lines:** 30
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 10

---
*Documentation generated for: mlops-project-documentation*
*File: drift_sensor.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/airflow/plugins/__init__.py`
- **Total lines:** 4
- **File size:** 195 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""airflow plugins package: custom hooks and operators."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: main.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/api/main.py`
- **Total lines:** 210
- **File size:** 6695 bytes

## Line Type Summary
- **Code:** 165
- **Comment:** 0
- **Empty:** 42
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add request validation and error handling`
> **Type:** TODO: high - Add request validation and error handling

### Line   2
> **Code:** `# TODO: medium - Implement request/response logging`
> **Type:** TODO: medium - Implement request/response logging

### Line   3
> **Code:** `# TODO: low - Add health check endpoint improvement`
> **Type:** TODO: low - Add health check endpoint improvement

### Line   4
> **Code:** `"""FastAPI app for Demand Forecasting (P4) — self-contained, trains on...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import os`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `import time`
> **Type:** Imports a module

### Line   9
> **Code:** `from contextlib import asynccontextmanager`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** `from datetime import datetime`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  14
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  15
> **Code:** `from fastapi import FastAPI`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** `from fastapi.responses import FileResponse`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** `from fastapi.staticfiles import StaticFiles`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from pydantic import BaseModel, Field`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from sklearn.ensemble import RandomForestRegressor`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** `from sklearn.metrics import mean_absolute_error, r2_score`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `UI_DIR = Path(__file__).parent.parent / "ui"`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "pbs_deman...`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `MODEL = None`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `FEATURE_COLS = None`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `MODEL_METRICS = {"r2": None, "mae": None}`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `PREDICTION_LOG = []`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `LOG_CAP = 500`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `BUCKET_KEYS = ["low", "medium", "high", "very_high"]`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `CONCESSION_TYPES = []`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `DRUG_IDS = []`
> **Type:** Assignment/comparison

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `class PredictRequest(BaseModel):`
> **Type:** Class definition

### Line  36
> **Code:** `drug_id: str = Field(default="CONCESSIONAL SAFETY NET_A03_DRUGS FOR FU...`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `concession: str = Field(default="CONCESSIONAL SAFETY NET")`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `month: int = Field(default=6, ge=1, le=12)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `year: int = Field(default=2005, ge=1991, le=2006)`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `lag_1: float = Field(default=5000, ge=0)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `lag_12: float = Field(default=4800, ge=0)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `rolling_mean_3: float = Field(default=4900, ge=0)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `rolling_mean_6: float = Field(default=4850, ge=0)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `class PredictResponse(BaseModel):`
> **Type:** Class definition

### Line  47
> **Code:** `predicted_units: float`
> **Type:** Code statement

### Line  48
> **Code:** `forecast_bucket: str`
> **Type:** Logical operation

### Line  49
> **Code:** `confidence: str`
> **Type:** Code statement

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def load_pbs_data() -> pd.DataFrame:`
> **Type:** Function definition

### Line  53
> **Code:** `"""Load and prepare PBS demand data for training."""`
> **Type:** Logical operation

### Line  54
> **Code:** `if not DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  55
> **Code:** `raise FileNotFoundError(f"PBS data not found at {DATA_PATH}. Run ml/da...`
> **Type:** Raises an exception

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `df = pd.read_csv(DATA_PATH)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `print(f"Loaded {len(df)} rows from PBS data")`
> **Type:** Prints output to console

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `global CONCESSION_TYPES, DRUG_IDS`
> **Type:** Code statement

### Line  61
> **Code:** `CONCESSION_TYPES = sorted(df["concession_type"].unique().tolist())`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `DRUG_IDS = sorted(df["drug_id"].unique().tolist())`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `feature_cols = ["month", "lag_1", "lag_12", "rolling_mean_3", "rolling...`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `X = df[feature_cols]`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `y = df["target"]`
> **Type:** Assignment/comparison

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `return X, y, feature_cols`
> **Type:** Returns a value from a function

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `def train_model():`
> **Type:** Function definition

### Line  72
> **Code:** `"""Train RandomForestRegressor on PBS data."""`
> **Type:** Logical operation

### Line  73
> **Code:** `global MODEL, FEATURE_COLS, MODEL_METRICS`
> **Type:** Code statement

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `X, y, feature_cols = load_pbs_data()`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `FEATURE_COLS = feature_cols`
> **Type:** Assignment/comparison

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0....`
> **Type:** Assignment/comparison

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `MODEL = RandomForestRegressor(n_estimators=200, max_depth=15, random_s...`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `MODEL.fit(X_train, y_train)`
> **Type:** Function call

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `preds = MODEL.predict(X_test)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `r2 = r2_score(y_test, preds)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `mae = mean_absolute_error(y_test, preds)`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `MODEL_METRICS["r2"] = round(r2, 4)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `MODEL_METRICS["mae"] = round(mae, 4)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `print(f"P4: Trained on {len(X_train)} samples, R²={r2:.4f}, MAE={mae:....`
> **Type:** Prints output to console

### Line  89
> **Code:** `print(f"P4: Features: {feature_cols}")`
> **Type:** Prints output to console

### Line  90
> **Code:** `print(f"P4: Concession types: {CONCESSION_TYPES}")`
> **Type:** Prints output to console

### Line  91
> **Code:** `print(f"P4: Drug series: {len(DRUG_IDS)}")`
> **Type:** Prints output to console

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `@asynccontextmanager`
> **Type:** Code statement

### Line  95
> **Code:** `async def lifespan(app: FastAPI):`
> **Type:** Code statement

### Line  96
> **Code:** `train_model()`
> **Type:** Function call

### Line  97
> **Code:** `yield`
> **Type:** Code statement

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `app = FastAPI(title="Demand Forecasting API (PBS)", version="1.0.0", l...`
> **Type:** Assignment/comparison

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `@app.get("/health")`
> **Type:** Arithmetic operation

### Line 103
> **Code:** `async def health():`
> **Type:** Code statement

### Line 104
> **Code:** `return {"status": "healthy", "model_loaded": MODEL is not None, "data_...`
> **Type:** Returns a value from a function

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `@app.post("/predict", response_model=PredictResponse)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `async def predict(req: PredictRequest):`
> **Type:** Code statement

### Line 109
> **Code:** `t0 = time.perf_counter()`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `df = pd.DataFrame([{`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `"month": req.month,`
> **Type:** Code statement

### Line 112
> **Code:** `"lag_1": req.lag_1,`
> **Type:** Code statement

### Line 113
> **Code:** `"lag_12": req.lag_12,`
> **Type:** Code statement

### Line 114
> **Code:** `"rolling_mean_3": req.rolling_mean_3,`
> **Type:** Code statement

### Line 115
> **Code:** `"rolling_mean_6": req.rolling_mean_6,`
> **Type:** Code statement

### Line 116
> **Code:** `}])[FEATURE_COLS]`
> **Type:** Data structure operation

### Line 117
> **Code:** `units = float(MODEL.predict(df)[0])`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `latency_ms = (time.perf_counter() - t0) * 1000.0`
> **Type:** Assignment/comparison

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `if units > 10000:`
> **Type:** Conditional statement

### Line 121
> **Code:** `bucket = "very_high"`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `elif units > 5000:`
> **Type:** Else-if branch

### Line 123
> **Code:** `bucket = "high"`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `elif units > 1000:`
> **Type:** Else-if branch

### Line 125
> **Code:** `bucket = "medium"`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `else:`
> **Type:** Else block

### Line 127
> **Code:** `bucket = "low"`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `confidence = "high" if 500 < units < 50000 else "medium"`
> **Type:** Assignment/comparison

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `result = PredictResponse(predicted_units=round(units, 1), forecast_buc...`
> **Type:** Assignment/comparison

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `PREDICTION_LOG.append({`
> **Type:** Code statement

### Line 134
> **Code:** `"timestamp": datetime.now().isoformat(timespec="seconds"),`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `"latency_ms": round(latency_ms, 2),`
> **Type:** Code statement

### Line 136
> **Code:** `"input": req.model_dump(),`
> **Type:** Code statement

### Line 137
> **Code:** `"result": result.model_dump(),`
> **Type:** Code statement

### Line 138
> **Code:** `})`
> **Type:** Code statement

### Line 139
> **Code:** `if len(PREDICTION_LOG) > LOG_CAP:`
> **Type:** Conditional statement

### Line 140
> **Code:** `del PREDICTION_LOG[: len(PREDICTION_LOG) - LOG_CAP]`
> **Type:** Arithmetic operation

### Line 141
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `@app.get("/history")`
> **Type:** Arithmetic operation

### Line 145
> **Code:** `async def history(limit: int = 50):`
> **Type:** Assignment/comparison

### Line 146
> **Code:** `n = max(0, min(limit, len(PREDICTION_LOG)))`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `return {"count": n, "total": len(PREDICTION_LOG), "entries": list(reve...`
> **Type:** Returns a value from a function

### Line 148
> **Code:** ``
> **Type:** Empty line

### Line 149
> **Code:** ``
> **Type:** Empty line

### Line 150
> **Code:** `@app.get("/stats")`
> **Type:** Arithmetic operation

### Line 151
> **Code:** `async def stats():`
> **Type:** Code statement

### Line 152
> **Code:** `total = len(PREDICTION_LOG)`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `empty = {`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `"total_forecasts": 0,`
> **Type:** Logical operation

### Line 155
> **Code:** `"avg_demand": 0,`
> **Type:** Logical operation

### Line 156
> **Code:** `"bucket_distribution": {k: 0 for k in BUCKET_KEYS},`
> **Type:** Logical operation

### Line 157
> **Code:** `"max_forecast": 0,`
> **Type:** Logical operation

### Line 158
> **Code:** `"avg_latency_ms": 0,`
> **Type:** Code statement

### Line 159
> **Code:** `}`
> **Type:** Code statement

### Line 160
> **Code:** `if total == 0:`
> **Type:** Conditional statement

### Line 161
> **Code:** `return empty`
> **Type:** Returns a value from a function

### Line 162
> **Code:** `demands = [e["result"]["predicted_units"] for e in PREDICTION_LOG]`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `buckets = {k: 0 for k in BUCKET_KEYS}`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `for e in PREDICTION_LOG:`
> **Type:** For loop

### Line 165
> **Code:** `buckets[e["result"]["forecast_bucket"]] += 1`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 167
> **Code:** `"total_forecasts": total,`
> **Type:** Logical operation

### Line 168
> **Code:** `"avg_demand": round(sum(demands) / total, 2),`
> **Type:** Arithmetic operation

### Line 169
> **Code:** `"bucket_distribution": buckets,`
> **Type:** Code statement

### Line 170
> **Code:** `"max_forecast": max(demands),`
> **Type:** Logical operation

### Line 171
> **Code:** `"avg_latency_ms": round(sum(e["latency_ms"] for e in PREDICTION_LOG) /...`
> **Type:** Arithmetic operation

### Line 172
> **Code:** `}`
> **Type:** Code statement

### Line 173
> **Code:** ``
> **Type:** Empty line

### Line 174
> **Code:** ``
> **Type:** Empty line

### Line 175
> **Code:** `@app.get("/model-info")`
> **Type:** Arithmetic operation

### Line 176
> **Code:** `async def model_info():`
> **Type:** Code statement

### Line 177
> **Code:** `if MODEL is None:`
> **Type:** Conditional statement

### Line 178
> **Code:** `return {"model_loaded": False}`
> **Type:** Returns a value from a function

### Line 179
> **Code:** `fi = [`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `{"feature": f, "importance": round(float(i), 4)}`
> **Type:** Logical operation

### Line 181
> **Code:** `for f, i in zip(FEATURE_COLS, MODEL.feature_importances_)`
> **Type:** For loop

### Line 182
> **Code:** `]`
> **Type:** Code statement

### Line 183
> **Code:** `fi.sort(key=lambda x: x["importance"], reverse=True)`
> **Type:** Assignment/comparison

### Line 184
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 185
> **Code:** `"model_loaded": True,`
> **Type:** Code statement

### Line 186
> **Code:** `"model_name": type(MODEL).__name__,`
> **Type:** Code statement

### Line 187
> **Code:** `"n_estimators": MODEL.n_estimators,`
> **Type:** Logical operation

### Line 188
> **Code:** `"max_depth": MODEL.max_depth,`
> **Type:** Code statement

### Line 189
> **Code:** `"n_features": len(FEATURE_COLS),`
> **Type:** Code statement

### Line 190
> **Code:** `"r2": MODEL_METRICS["r2"],`
> **Type:** Data structure operation

### Line 191
> **Code:** `"mae": MODEL_METRICS["mae"],`
> **Type:** Data structure operation

### Line 192
> **Code:** `"feature_importance": fi,`
> **Type:** Logical operation

### Line 193
> **Code:** `"data_source": "PBS (Australian Pharmaceutical Benefits Scheme)",`
> **Type:** Code statement

### Line 194
> **Code:** `"n_series": len(DRUG_IDS),`
> **Type:** Code statement

### Line 195
> **Code:** `"concession_types": CONCESSION_TYPES,`
> **Type:** Code statement

### Line 196
> **Code:** `}`
> **Type:** Code statement

### Line 197
> **Code:** ``
> **Type:** Empty line

### Line 198
> **Code:** ``
> **Type:** Empty line

### Line 199
> **Code:** `@app.get("/")`
> **Type:** Arithmetic operation

### Line 200
> **Code:** `async def serve_ui():`
> **Type:** Code statement

### Line 201
> **Code:** `return FileResponse(UI_DIR / "index.html")`
> **Type:** Returns a value from a function

### Line 202
> **Code:** ``
> **Type:** Empty line

### Line 203
> **Code:** ``
> **Type:** Empty line

### Line 204
> **Code:** `if UI_DIR.exists():`
> **Type:** Conditional statement

### Line 205
> **Code:** `app.mount("/ui", StaticFiles(directory=str(UI_DIR)), name="ui")`
> **Type:** Assignment/comparison

### Line 206
> **Code:** ``
> **Type:** Empty line

### Line 207
> **Code:** ``
> **Type:** Empty line

### Line 208
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 209
> **Code:** `import uvicorn`
> **Type:** Imports a module

### Line 210
> **Code:** `uvicorn.run(app, host="0.0.0.0", port=8103)`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 210
- **Code lines:** 165
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 42

---
*Documentation generated for: mlops-project-documentation*
*File: main.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/__init__.py`
- **Total lines:** 4
- **File size:** 214 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""src package: core source code for the demand forecasting MLOps proj...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/models/__init__.py`
- **Total lines:** 4
- **File size:** 230 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""models package: training, evaluation, and MLflow registry logic for...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: evaluate.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/models/evaluate.py`
- **Total lines:** 148
- **File size:** 5385 bytes

## Line Type Summary
- **Code:** 118
- **Comment:** 0
- **Empty:** 27
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add quality gate with thresholds`
> **Type:** TODO: high - Add quality gate with thresholds

### Line   2
> **Code:** `# TODO: medium - Implement comparison vs current production model`
> **Type:** TODO: medium - Implement comparison vs current production model

### Line   3
> **Code:** `# TODO: low - Add metrics export for Evidence Pack`
> **Type:** TODO: low - Add metrics export for Evidence Pack

### Line   4
> **Code:** `"""Model evaluation and validation gates for demand forecasting.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Loads a candidate model, evaluates it on the held-out test set and com...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `against configured quality thresholds. Gates: R² >= 0.60, MAPE <= 25%.`
> **Type:** Assignment/comparison

### Line   8
> **Code:** `Writes a JSON evaluation report; exits non-zero when gates fail.`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `import json`
> **Type:** Imports a module

### Line  15
> **Code:** `import os`
> **Type:** Imports a module

### Line  16
> **Code:** `import sys`
> **Type:** Imports a module

### Line  17
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  21
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  24
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  25
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  26
> **Code:** `from sklearn.metrics import mean_absolute_error, mean_squared_error, r...`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `from src.features.build_features import TARGET_FEATURE, FEATURE_ORDER`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `EVALUATION_DIR = PROJECT_ROOT / "models" / "evaluation"`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `LATEST_REPORT = EVALUATION_DIR / "latest_report.json"`
> **Type:** Assignment/comparison

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `DEFAULT_THRESHOLDS = {"min_r2": 0.60, "max_mape": 25.0}`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `def _resolve_model(model_uri: str | None, run_id: str | None):`
> **Type:** Function definition

### Line  39
> **Code:** `if run_id:`
> **Type:** Conditional statement

### Line  40
> **Code:** `try:`
> **Type:** Code statement

### Line  41
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  42
> **Code:** `return mlflow.sklearn.load_model(f"runs:/{run_id}/model")`
> **Type:** Returns a value from a function

### Line  43
> **Code:** `except Exception:  # nosec B110`
> **Type:** Code statement

### Line  44
> **Code:** `pass`
> **Type:** Code statement

### Line  45
> **Code:** `if model_uri:`
> **Type:** Conditional statement

### Line  46
> **Code:** `try:`
> **Type:** Code statement

### Line  47
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  48
> **Code:** `return mlflow.sklearn.load_model(model_uri)`
> **Type:** Returns a value from a function

### Line  49
> **Code:** `except Exception:  # nosec B110`
> **Type:** Code statement

### Line  50
> **Code:** `pass`
> **Type:** Code statement

### Line  51
> **Code:** `if Path(DEFAULT_LOCAL_MODEL).exists():`
> **Type:** Conditional statement

### Line  52
> **Code:** `return joblib.load(DEFAULT_LOCAL_MODEL)`
> **Type:** Returns a value from a function

### Line  53
> **Code:** `raise FileNotFoundError("No candidate model found (run_id, model_uri o...`
> **Type:** Raises an exception

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `def _load_test_set(data_path: str | Path) -> tuple[pd.DataFrame, pd.Se...`
> **Type:** Function definition

### Line  57
> **Code:** `reference = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `if reference.exists():`
> **Type:** Conditional statement

### Line  59
> **Code:** `df = pd.read_csv(reference)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `return df[FEATURE_ORDER], df[TARGET_FEATURE].astype(float)`
> **Type:** Returns a value from a function

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `data_path = Path(data_path or DEFAULT_DATA)`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `if not data_path.exists():`
> **Type:** Conditional statement

### Line  64
> **Code:** `raise FileNotFoundError(f"Feature dataset not found: {data_path}")`
> **Type:** Raises an exception

### Line  65
> **Code:** `features = pd.read_parquet(data_path)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `if len(features) > 5000:`
> **Type:** Conditional statement

### Line  67
> **Code:** `X_test = features.sample(n=5000, random_state=42)[FEATURE_ORDER]`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `y_test = features.loc[X_test.index, TARGET_FEATURE].astype(float)`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `return X_test, y_test`
> **Type:** Returns a value from a function

### Line  70
> **Code:** `return features[FEATURE_ORDER], features[TARGET_FEATURE].astype(float)`
> **Type:** Returns a value from a function

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> ...`
> **Type:** Function definition

### Line  74
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `mae = float(mean_absolute_error(y_test, y_pred))`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `r2 = float(r2_score(y_test, y_pred))`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `nonzero = y_test.values != 0`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `mape = float(np.mean(np.abs((y_test.values[nonzero] - y_pred[nonzero])...`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  81
> **Code:** `"rmse": rmse,`
> **Type:** Code statement

### Line  82
> **Code:** `"mae": mae,`
> **Type:** Code statement

### Line  83
> **Code:** `"r2": r2,`
> **Type:** Code statement

### Line  84
> **Code:** `"mape": mape,`
> **Type:** Code statement

### Line  85
> **Code:** `"n_samples": int(len(y_test)),`
> **Type:** Code statement

### Line  86
> **Code:** `}`
> **Type:** Code statement

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def evaluate(`
> **Type:** Function definition

### Line  90
> **Code:** `data_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `model_uri: str | None = None,`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `run_id: str | None = None,`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `thresholds: dict | None = None,`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  95
> **Code:** `X_test, y_test = _load_test_set(data_path)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `model = _resolve_model(model_uri, run_id)`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `metrics = evaluate_model(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `gates = {`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `"min_r2": {"metric": "r2", "value": thresholds["min_r2"], "direction":...`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `"max_mape": {"metric": "mape", "value": thresholds["max_mape"], "direc...`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `}`
> **Type:** Code statement

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `r2_pass = metrics["r2"] >= thresholds["min_r2"]`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `mape_pass = metrics["mape"] <= thresholds["max_mape"]`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `gates_passed = r2_pass and mape_pass`
> **Type:** Assignment/comparison

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `report = {`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `"model_uri": model_uri or (f"runs:/{run_id}/model" if run_id else "loc...`
> **Type:** Arithmetic operation

### Line 112
> **Code:** `"run_id": run_id,`
> **Type:** Code statement

### Line 113
> **Code:** `"metrics": metrics,`
> **Type:** Code statement

### Line 114
> **Code:** `"thresholds": thresholds,`
> **Type:** Code statement

### Line 115
> **Code:** `"gates": gates,`
> **Type:** Code statement

### Line 116
> **Code:** `"gates_passed": gates_passed,`
> **Type:** Code statement

### Line 117
> **Code:** `}`
> **Type:** Code statement

### Line 118
> **Code:** `EVALUATION_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 119
> **Code:** `with LATEST_REPORT.open("w") as fh:`
> **Type:** Context manager

### Line 120
> **Code:** `json.dump(report, fh, indent=2)`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `return report`
> **Type:** Returns a value from a function

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 125
> **Code:** `parser = argparse.ArgumentParser(description="Evaluate a candidate dem...`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `parser.add_argument("--data", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `parser.add_argument("--model-uri", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `parser.add_argument("--run-id", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 129
> **Code:** `parser.add_argument("--min-r2", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 130
> **Code:** `parser.add_argument("--max-mape", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 131
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `thresholds = {}`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `if args.min_r2 is not None:`
> **Type:** Conditional statement

### Line 135
> **Code:** `thresholds["min_r2"] = args.min_r2`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `if args.max_mape is not None:`
> **Type:** Conditional statement

### Line 137
> **Code:** `thresholds["max_mape"] = args.max_mape`
> **Type:** Assignment/comparison

### Line 138
> **Code:** ``
> **Type:** Empty line

### Line 139
> **Code:** `report = evaluate(args.data, args.model_uri, args.run_id, thresholds)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `print(f"evaluation: rmse={report['metrics']['rmse']:.2f} mae={report['...`
> **Type:** Prints output to console

### Line 141
> **Code:** `f"r2={report['metrics']['r2']:.4f} mape={report['metrics']['mape']:.2f...`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `if not report["gates_passed"]:`
> **Type:** Conditional statement

### Line 143
> **Code:** `print(f"evaluation gates not met: {json.dumps(report['gates'])}", file...`
> **Type:** Prints output to console

### Line 144
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 148
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 148
- **Code lines:** 118
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 27

---
*Documentation generated for: mlops-project-documentation*
*File: evaluate.py*
---

# mlops-project-documentation: train.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/models/train.py`
- **Total lines:** 195
- **File size:** 7657 bytes

## Line Type Summary
- **Code:** 155
- **Comment:** 3
- **Empty:** 34
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add data validation before training`
> **Type:** TODO: high - Add data validation before training

### Line   2
> **Code:** `# TODO: medium - Implement hyperparameter logging`
> **Type:** TODO: medium - Implement hyperparameter logging

### Line   3
> **Code:** `# TODO: low - Add model explainability integration`
> **Type:** TODO: low - Add model explainability integration

### Line   4
> **Code:** `"""Model training for demand forecasting with MLflow tracking.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Trains a RandomForestRegressor on the feature store snapshot:`
> **Type:** Logical operation

### Line   7
> **Code:** `1. start an MLflow run and log hyperparameters`
> **Type:** Logical operation

### Line   8
> **Code:** `2. train + evaluate on a held-out test split`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `3. log metrics, feature importances, and model artifacts`
> **Type:** Logical operation

### Line  10
> **Code:** `4. register the model in the MLflow Model Registry`
> **Type:** Code statement

### Line  11
> **Code:** `5. persist local model.pkl and metrics.json`
> **Type:** Logical operation

### Line  12
> **Code:** `"""`
> **Type:** Code statement

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  17
> **Code:** `import json`
> **Type:** Imports a module

### Line  18
> **Code:** `import os`
> **Type:** Imports a module

### Line  19
> **Code:** `import sys`
> **Type:** Imports a module

### Line  20
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  24
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  27
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `import matplotlib.pyplot as plt  # noqa: E402`
> **Type:** Imports a module

### Line  32
> **Code:** `import mlflow  # noqa: E402`
> **Type:** Imports a module

### Line  33
> **Code:** `import numpy as np  # noqa: E402`
> **Type:** Imports a module

### Line  34
> **Code:** `import pandas as pd  # noqa: E402`
> **Type:** Imports a module

### Line  35
> **Code:** `from sklearn.ensemble import RandomForestRegressor  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  36
> **Code:** `from sklearn.metrics import mean_absolute_error, mean_squared_error, r...`
> **Type:** Imports specific names from a module

### Line  37
> **Code:** `from sklearn.model_selection import train_test_split  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `from src.features.build_features import TARGET_FEATURE, FEATURE_ORDER ...`
> **Type:** Imports specific names from a module

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `DEFAULT_MODEL_OUTPUT = PROJECT_ROOT / "models" / "model.pkl"`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `DEFAULT_METRICS = PROJECT_ROOT / "metrics.json"`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference....`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `DEFAULT_ARTIFACT_DIR = PROJECT_ROOT / "models" / "artifacts"`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "demand_model")`
> **Type:** Assignment/comparison

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `# Local fallback tracking store: the repository's sqlite backend (the ...`
> **Type:** Comment: Local fallback tracking store: the repository's sqlite backend (the same one

### Line  50
> **Code:** `# promote.py uses), not a temp dir that disappears on reboot. Docker/K...`
> **Type:** Comment: promote.py uses), not a temp dir that disappears on reboot. Docker/K8s

### Line  51
> **Code:** `# override this with MLFLOW_TRACKING_URI pointing at the MLflow server...`
> **Type:** Comment: override this with MLFLOW_TRACKING_URI pointing at the MLflow server.

### Line  52
> **Code:** `DEFAULT_TRACKING_URI = f"sqlite:///{PROJECT_ROOT / 'mlruns' / 'mlflow....`
> **Type:** Assignment/comparison

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `DEFAULT_PARAMS = {`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `"n_estimators": 300,`
> **Type:** Logical operation

### Line  56
> **Code:** `"max_depth": 15,`
> **Type:** Code statement

### Line  57
> **Code:** `"min_samples_leaf": 5,`
> **Type:** Code statement

### Line  58
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line  59
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line  60
> **Code:** `"n_jobs": -1,`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `}`
> **Type:** Code statement

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def _save_feature_importances(model, feature_names: list[str], path: P...`
> **Type:** Function definition

### Line  65
> **Code:** `importances = model.feature_importances_`
> **Type:** Imports a module

### Line  66
> **Code:** `order = np.argsort(importances)[::-1]`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `fig, ax = plt.subplots(figsize=(9, 6))`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `ax.barh([feature_names[i] for i in order][:20], importances[order][:20...`
> **Type:** Logical operation

### Line  69
> **Code:** `ax.invert_yaxis()`
> **Type:** Function call

### Line  70
> **Code:** `ax.set_xlabel("feature importance")`
> **Type:** Logical operation

### Line  71
> **Code:** `fig.tight_layout()`
> **Type:** Function call

### Line  72
> **Code:** `fig.savefig(path, dpi=120)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `def _save_predictions_plot(y_true, y_pred, path: Path) -> None:`
> **Type:** Function definition

### Line  77
> **Code:** `fig, ax = plt.subplots(figsize=(7, 6))`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `ax.scatter(y_true, y_pred, alpha=0.3, s=10)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `lims = [0, max(y_true.max(), y_pred.max()) * 1.05]`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `ax.plot(lims, lims, "--", color="red", linewidth=1, label="perfect")`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `ax.set_xlabel("actual units_sold")`
> **Type:** Function call

### Line  82
> **Code:** `ax.set_ylabel("predicted units_sold")`
> **Type:** Function call

### Line  83
> **Code:** `ax.legend()`
> **Type:** Function call

### Line  84
> **Code:** `fig.tight_layout()`
> **Type:** Function call

### Line  85
> **Code:** `fig.savefig(path, dpi=120)`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def train_model(`
> **Type:** Function definition

### Line  90
> **Code:** `data_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `config_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `model_output: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `model_name: str = MODEL_NAME,`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `params: dict | None = None,`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  96
> **Code:** `data_path = Path(data_path or DEFAULT_DATA)`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `config_path = Path(config_path or DEFAULT_CONFIG)`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `model_output = Path(model_output or DEFAULT_MODEL_OUTPUT)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `params = {**DEFAULT_PARAMS, **(params or {})}`
> **Type:** Assignment/comparison

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `if not data_path.exists():`
> **Type:** Conditional statement

### Line 102
> **Code:** `raise FileNotFoundError(f"Feature dataset not found: {data_path}")`
> **Type:** Raises an exception

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `features = pd.read_parquet(data_path)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `if TARGET_FEATURE not in features.columns:`
> **Type:** Conditional statement

### Line 106
> **Code:** `raise ValueError(f"Target column '{TARGET_FEATURE}' missing from featu...`
> **Type:** Raises an exception

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `X = features[FEATURE_ORDER]`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `y = features[TARGET_FEATURE].astype(float)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0....`
> **Type:** Assignment/comparison

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `model = RandomForestRegressor(**params)`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `model.fit(X_train, y_train)`
> **Type:** Function call

### Line 114
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `mae = float(mean_absolute_error(y_test, y_pred))`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `r2 = float(r2_score(y_test, y_pred))`
> **Type:** Assignment/comparison

### Line 119
> **Code:** `nonzero = y_test.values != 0`
> **Type:** Assignment/comparison

### Line 120
> **Code:** `mape = float(np.mean(np.abs((y_test.values[nonzero] - y_pred[nonzero])...`
> **Type:** Assignment/comparison

### Line 121
> **Code:** ``
> **Type:** Empty line

### Line 122
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `"rmse": rmse,`
> **Type:** Code statement

### Line 124
> **Code:** `"mae": mae,`
> **Type:** Code statement

### Line 125
> **Code:** `"r2": r2,`
> **Type:** Code statement

### Line 126
> **Code:** `"mape": mape,`
> **Type:** Code statement

### Line 127
> **Code:** `"train_size": int(len(X_train)),`
> **Type:** Code statement

### Line 128
> **Code:** `"test_size": int(len(X_test)),`
> **Type:** Code statement

### Line 129
> **Code:** `}`
> **Type:** Code statement

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `run_id = None`
> **Type:** Assignment/comparison

### Line 132
> **Code:** `try:`
> **Type:** Code statement

### Line 133
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", DEFAULT_...`
> **Type:** Function call

### Line 134
> **Code:** `with mlflow.start_run(run_name="demand-forecasting-training") as run:`
> **Type:** Context manager

### Line 135
> **Code:** `run_id = run.info.run_id`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `mlflow.set_tag("model_name", model_name)`
> **Type:** Function call

### Line 137
> **Code:** `mlflow.set_tag("task", "demand_forecasting")`
> **Type:** Logical operation

### Line 138
> **Code:** `mlflow.log_params(params)`
> **Type:** Function call

### Line 139
> **Code:** `mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, ...`
> **Type:** Logical operation

### Line 140
> **Code:** ``
> **Type:** Empty line

### Line 141
> **Code:** `importance_path = DEFAULT_ARTIFACT_DIR / "feature_importances.png"`
> **Type:** Imports a module

### Line 142
> **Code:** `pred_path = DEFAULT_ARTIFACT_DIR / "predictions_vs_actual.png"`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `importance_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Imports a module

### Line 144
> **Code:** `_save_feature_importances(model, list(X.columns), importance_path)`
> **Type:** Logical operation

### Line 145
> **Code:** `_save_predictions_plot(y_test.values, y_pred, pred_path)`
> **Type:** Function call

### Line 146
> **Code:** `mlflow.log_artifact(str(importance_path))`
> **Type:** Logical operation

### Line 147
> **Code:** `mlflow.log_artifact(str(pred_path))`
> **Type:** Function call

### Line 148
> **Code:** `mlflow.log_artifact(str(config_path))`
> **Type:** Function call

### Line 149
> **Code:** ``
> **Type:** Empty line

### Line 150
> **Code:** `mlflow.sklearn.log_model(`
> **Type:** Code statement

### Line 151
> **Code:** `model,`
> **Type:** Code statement

### Line 152
> **Code:** `artifact_path="model",`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `registered_model_name=model_name,`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `input_example=X_test.iloc[[0]],`
> **Type:** Assignment/comparison

### Line 155
> **Code:** `)`
> **Type:** Code statement

### Line 156
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line 157
> **Code:** `print(f"warning: MLflow tracking failed (continuing offline): {exc}")`
> **Type:** Prints output to console

### Line 158
> **Code:** ``
> **Type:** Empty line

### Line 159
> **Code:** `model_output.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `joblib.dump(model, model_output)`
> **Type:** Function call

### Line 161
> **Code:** `DEFAULT_METRICS.write_text(json.dumps(metrics, indent=2))`
> **Type:** Assignment/comparison

### Line 162
> **Code:** ``
> **Type:** Empty line

### Line 163
> **Code:** `reference = X_test.copy()`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `reference["prediction"] = y_pred`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `reference[TARGET_FEATURE] = y_test.values`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `DEFAULT_REFERENCE.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 167
> **Code:** `reference.to_csv(DEFAULT_REFERENCE, index=False)`
> **Type:** Assignment/comparison

### Line 168
> **Code:** ``
> **Type:** Empty line

### Line 169
> **Code:** `return {"run_id": run_id, "model_name": model_name, "metrics": metrics...`
> **Type:** Returns a value from a function

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** ``
> **Type:** Empty line

### Line 172
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 173
> **Code:** `parser = argparse.ArgumentParser(description="Train and register the d...`
> **Type:** Assignment/comparison

### Line 174
> **Code:** `parser.add_argument("--data", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 175
> **Code:** `parser.add_argument("--config", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 176
> **Code:** `parser.add_argument("--model-output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 177
> **Code:** `parser.add_argument("--model-name", type=str, default=MODEL_NAME)`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS...`
> **Type:** Assignment/comparison

### Line 179
> **Code:** `parser.add_argument("--max-depth", type=int, default=DEFAULT_PARAMS["m...`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `parser.add_argument("--min-samples-leaf", type=int, default=DEFAULT_PA...`
> **Type:** Assignment/comparison

### Line 181
> **Code:** `parser.add_argument("--seed", type=int, default=DEFAULT_PARAMS["random...`
> **Type:** Assignment/comparison

### Line 182
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 183
> **Code:** ``
> **Type:** Empty line

### Line 184
> **Code:** `params = {`
> **Type:** Assignment/comparison

### Line 185
> **Code:** `"n_estimators": args.n_estimators,`
> **Type:** Logical operation

### Line 186
> **Code:** `"max_depth": args.max_depth,`
> **Type:** Code statement

### Line 187
> **Code:** `"min_samples_leaf": args.min_samples_leaf,`
> **Type:** Code statement

### Line 188
> **Code:** `"random_state": args.seed,`
> **Type:** Logical operation

### Line 189
> **Code:** `}`
> **Type:** Code statement

### Line 190
> **Code:** `result = train_model(args.data, args.config, args.model_output, args.m...`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `print(f"run_id={result['run_id']} rmse={result['metrics']['rmse']:.2f}...`
> **Type:** Prints output to console

### Line 192
> **Code:** ``
> **Type:** Empty line

### Line 193
> **Code:** ``
> **Type:** Empty line

### Line 194
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 195
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 195
- **Code lines:** 155
- **Comments:** 3
- **TODO items:** 3
- **Empty lines:** 34

---
*Documentation generated for: mlops-project-documentation*
*File: train.py*
---

# mlops-project-documentation: promote.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/models/promote.py`
- **Total lines:** 125
- **File size:** 4940 bytes

## Line Type Summary
- **Code:** 95
- **Comment:** 1
- **Empty:** 26
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add promotion gate with evidence pack requirement`
> **Type:** TODO: high - Add promotion gate with evidence pack requirement

### Line   2
> **Code:** `# TODO: medium - Implement human approval recording`
> **Type:** TODO: medium - Implement human approval recording

### Line   3
> **Code:** `# TODO: low - Add rollback capability documentation`
> **Type:** TODO: low - Add rollback capability documentation

### Line   4
> **Code:** `"""Promotion logic: Staging -> Production in the MLflow Model Registry...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `A candidate (the latest evaluation report) is promoted only if:`
> **Type:** Logical operation

### Line   7
> **Code:** `- it passed the evaluation gates (evaluate.py), and`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- it beats the currently deployed production model on the same test se...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `The previous production version is archived. The promotion is recorded...`
> **Type:** Logical operation

### Line  11
> **Code:** `models/evaluation/production_report.json so the API and dashboards can...`
> **Type:** Arithmetic operation

### Line  12
> **Code:** `which model is live and why.`
> **Type:** Logical operation

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `import json`
> **Type:** Imports a module

### Line  19
> **Code:** `import os`
> **Type:** Imports a module

### Line  20
> **Code:** `import sys`
> **Type:** Imports a module

### Line  21
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `LATEST_REPORT = PROJECT_ROOT / "models" / "evaluation" / "latest_repor...`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "producti...`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "demand_model")`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `# The model is a regressor: r2 (higher is better) is the comparison me...`
> **Type:** Comment: The model is a regressor: r2 (higher is better) is the comparison metric.

### Line  30
> **Code:** `COMPARISON_METRIC = "r2"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `def _client():`
> **Type:** Function definition

### Line  34
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:...`
> **Type:** Arithmetic operation

### Line  37
> **Code:** `return mlflow.tracking.MlflowClient()`
> **Type:** Returns a value from a function

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `def current_production(model_name: str = MODEL_NAME) -> dict | None:`
> **Type:** Function definition

### Line  41
> **Code:** `try:`
> **Type:** Code statement

### Line  42
> **Code:** `client = _client()`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `versions = client.get_latest_versions(model_name, stages=["Production"...`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `if not versions:`
> **Type:** Conditional statement

### Line  45
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  46
> **Code:** `version = versions[0]`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `report = {}`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `if PRODUCTION_REPORT.exists():`
> **Type:** Conditional statement

### Line  49
> **Code:** `report = json.loads(PRODUCTION_REPORT.read_text())`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `return {"version": int(version.version), "run_id": version.run_id, "re...`
> **Type:** Returns a value from a function

### Line  51
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line  52
> **Code:** `print(f"warning: could not read production model from registry: {exc}"...`
> **Type:** Prints output to console

### Line  53
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `def promote_candidate(model_name: str = MODEL_NAME, force: bool = Fals...`
> **Type:** Function definition

### Line  57
> **Code:** `if not LATEST_REPORT.exists():`
> **Type:** Conditional statement

### Line  58
> **Code:** `raise FileNotFoundError(f"No candidate report found at {LATEST_REPORT}...`
> **Type:** Raises an exception

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `candidate = json.loads(LATEST_REPORT.read_text())`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `if not candidate.get("gates_passed") and not force:`
> **Type:** Conditional statement

### Line  62
> **Code:** `raise RuntimeError("Candidate did not pass evaluation gates; refusing ...`
> **Type:** Raises an exception

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `client = _client()`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `versions = client.get_latest_versions(model_name, stages=["Staging"])`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `if not versions:`
> **Type:** Conditional statement

### Line  67
> **Code:** `raise RuntimeError(f"No Staging version found for model '{model_name}'...`
> **Type:** Raises an exception

### Line  68
> **Code:** `version = versions[0]`
> **Type:** Assignment/comparison

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `production = current_production(model_name)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `if production and not force:`
> **Type:** Conditional statement

### Line  72
> **Code:** `candidate_score = candidate["metrics"][COMPARISON_METRIC]`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `production_score = production["report"].get("metrics", {}).get(COMPARI...`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `if production_score is not None and candidate_score < production_score...`
> **Type:** Conditional statement

### Line  75
> **Code:** `raise RuntimeError(`
> **Type:** Raises an exception

### Line  76
> **Code:** `f"Candidate {COMPARISON_METRIC}={candidate_score:.4f} < production "`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `f"{COMPARISON_METRIC}={production_score:.4f}; refusing to promote "`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `"(use --force to override)."`
> **Type:** Arithmetic operation

### Line  79
> **Code:** `)`
> **Type:** Code statement

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `for previous in client.search_model_versions(f"name='{model_name}'"):`
> **Type:** For loop

### Line  82
> **Code:** `if previous.current_stage == "Production":`
> **Type:** Conditional statement

### Line  83
> **Code:** `client.transition_model_version_stage(model_name, previous.version, st...`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `print(f"archived {model_name} version {previous.version}")`
> **Type:** Prints output to console

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `client.transition_model_version_stage(model_name, version.version, sta...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `client.update_model_version(`
> **Type:** Code statement

### Line  88
> **Code:** `model_name,`
> **Type:** Code statement

### Line  89
> **Code:** `version.version,`
> **Type:** Code statement

### Line  90
> **Code:** `description=(`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `f"Promoted by promote.py | {COMPARISON_METRIC}="`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `f"{candidate['metrics'][COMPARISON_METRIC]:.4f} | run={candidate.get('...`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `),`
> **Type:** Code statement

### Line  94
> **Code:** `)`
> **Type:** Code statement

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `production_report = {`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `"model_name": model_name,`
> **Type:** Code statement

### Line  98
> **Code:** `"version": int(version.version),`
> **Type:** Code statement

### Line  99
> **Code:** `"run_id": version.run_id or candidate.get("run_id"),`
> **Type:** Logical operation

### Line 100
> **Code:** `"promoted_at": None,`
> **Type:** Code statement

### Line 101
> **Code:** `"metrics": candidate["metrics"],`
> **Type:** Logical operation

### Line 102
> **Code:** `}`
> **Type:** Code statement

### Line 103
> **Code:** `PRODUCTION_REPORT.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `PRODUCTION_REPORT.write_text(json.dumps(production_report, indent=2))`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `print(f"promoted {model_name} version {version.version} -> Production"...`
> **Type:** Prints output to console

### Line 107
> **Code:** `return production_report`
> **Type:** Returns a value from a function

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 111
> **Code:** `parser = argparse.ArgumentParser(description="Promote the latest valid...`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `parser.add_argument("--model-name", type=str, default=MODEL_NAME)`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `parser.add_argument("--force", action="store_true", help="Skip product...`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `try:`
> **Type:** Code statement

### Line 117
> **Code:** `report = promote_candidate(args.model_name, args.force)`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `print(json.dumps(report, indent=2))`
> **Type:** Prints output to console

### Line 119
> **Code:** `except (RuntimeError, FileNotFoundError) as exc:`
> **Type:** Logical operation

### Line 120
> **Code:** `print(f"promotion failed: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line 121
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 125
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 125
- **Code lines:** 95
- **Comments:** 1
- **TODO items:** 3
- **Empty lines:** 26

---
*Documentation generated for: mlops-project-documentation*
*File: promote.py*
---

# mlops-project-documentation: model_loader.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/api/model_loader.py`
- **Total lines:** 120
- **File size:** 4376 bytes

## Line Type Summary
- **Code:** 94
- **Comment:** 0
- **Empty:** 23
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Model loading for the demand forecasting inference API.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Loads the production model once at startup from the MLflow Model Regis...`
> **Type:** Code statement

### Line   7
> **Code:** `and applies the same fitted feature transformer that was used at train...`
> **Type:** Logical operation

### Line   8
> **Code:** `Falls back to a local pickle when the registry is unreachable.`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import json`
> **Type:** Imports a module

### Line  14
> **Code:** `import os`
> **Type:** Imports a module

### Line  15
> **Code:** `import threading`
> **Type:** Imports a module

### Line  16
> **Code:** `import time`
> **Type:** Imports a module

### Line  17
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  20
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `from src.features.build_features import FeatureTransformer`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `DEFAULT_TRACKING_URI = f"sqlite:///{PROJECT_ROOT / 'mlruns' / 'mlflow....`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `DEFAULT_CONFIG_PATH = PROJECT_ROOT / "data" / "features" / "features_c...`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "demand_model")`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `class ModelBundle:`
> **Type:** Class definition

### Line  34
> **Code:** `def __init__(`
> **Type:** Function definition

### Line  35
> **Code:** `self,`
> **Type:** Code statement

### Line  36
> **Code:** `model,`
> **Type:** Code statement

### Line  37
> **Code:** `transformer: FeatureTransformer,`
> **Type:** Logical operation

### Line  38
> **Code:** `model_name: str,`
> **Type:** Code statement

### Line  39
> **Code:** `version: str,`
> **Type:** Code statement

### Line  40
> **Code:** `run_id: str | None = None,`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `):`
> **Type:** Code statement

### Line  42
> **Code:** `self.model = model`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `self.transformer = transformer`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `self.model_name = model_name`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `self.version = version`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `self.run_id = run_id`
> **Type:** Assignment/comparison

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def predict(self, df: pd.DataFrame) -> list[float]:`
> **Type:** Function definition

### Line  49
> **Code:** `features = self.transformer.transform(df)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `return self.model.predict(features).tolist()`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `class ModelLoader:`
> **Type:** Class definition

### Line  54
> **Code:** `def __init__(self, model_name: str = MODEL_NAME, config_path: str | Pa...`
> **Type:** Function definition

### Line  55
> **Code:** `self.model_name = model_name`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `self.config_path = Path(config_path or os.environ.get("FEATURES_CONFIG...`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `self._bundle: ModelBundle | None = None`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `self._lock = threading.Lock()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `self._loaded_at: float = 0.0`
> **Type:** Assignment/comparison

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `def load(self) -> ModelBundle:`
> **Type:** Function definition

### Line  62
> **Code:** `with self._lock:`
> **Type:** Context manager

### Line  63
> **Code:** `bundle, version, run_id = self._load_model()`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `self._bundle = bundle`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `self._bundle.version = version`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `self._bundle.run_id = run_id`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `self._loaded_at = time.time()`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `return self._bundle`
> **Type:** Returns a value from a function

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `def _load_model(self) -> tuple[ModelBundle, str, str | None]:`
> **Type:** Function definition

### Line  71
> **Code:** `if not self.config_path.exists():`
> **Type:** Conditional statement

### Line  72
> **Code:** `raise FileNotFoundError(f"Features config not found: {self.config_path...`
> **Type:** Raises an exception

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `config = json.loads(self.config_path.read_text())`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `transformer = FeatureTransformer.from_config(config)`
> **Type:** Assignment/comparison

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `explicit_uri = os.environ.get("MLFLOW_MODEL_URI")`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `if explicit_uri:`
> **Type:** Conditional statement

### Line  79
> **Code:** `try:`
> **Type:** Code statement

### Line  80
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  81
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", DEFAULT_...`
> **Type:** Function call

### Line  82
> **Code:** `model = mlflow.sklearn.load_model(explicit_uri)`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `return ModelBundle(model, transformer, self.model_name, explicit_uri, ...`
> **Type:** Returns a value from a function

### Line  84
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line  85
> **Code:** `pass`
> **Type:** Code statement

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** `registry_uri = f"models:/{self.model_name}/Production"`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `try:`
> **Type:** Code statement

### Line  89
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  90
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", DEFAULT_...`
> **Type:** Function call

### Line  91
> **Code:** `client = mlflow.tracking.MlflowClient()`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `model = mlflow.sklearn.load_model(registry_uri)`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `version = client.get_latest_versions(self.model_name, stages=["Product...`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `return (`
> **Type:** Returns a value from a function

### Line  95
> **Code:** `ModelBundle(model, transformer, self.model_name, str(version.version),...`
> **Type:** Logical operation

### Line  96
> **Code:** `str(version.version),`
> **Type:** Code statement

### Line  97
> **Code:** `version.run_id,`
> **Type:** Code statement

### Line  98
> **Code:** `)`
> **Type:** Code statement

### Line  99
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line 100
> **Code:** `pass`
> **Type:** Code statement

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `if DEFAULT_LOCAL_MODEL.exists():`
> **Type:** Conditional statement

### Line 103
> **Code:** `model = joblib.load(DEFAULT_LOCAL_MODEL)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `return ModelBundle(model, transformer, self.model_name, "local"), "loc...`
> **Type:** Returns a value from a function

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `raise RuntimeError(f"Model '{self.model_name}' unavailable: no registr...`
> **Type:** Raises an exception

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `def get_bundle(self) -> ModelBundle:`
> **Type:** Function definition

### Line 109
> **Code:** `if self._bundle is None:`
> **Type:** Conditional statement

### Line 110
> **Code:** `return self.load()`
> **Type:** Returns a value from a function

### Line 111
> **Code:** `interval = int(os.environ.get("RELOAD_INTERVAL", "0") or 0)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `if interval > 0 and time.time() - self._loaded_at > interval:`
> **Type:** Conditional statement

### Line 113
> **Code:** `try:`
> **Type:** Code statement

### Line 114
> **Code:** `return self.load()`
> **Type:** Returns a value from a function

### Line 115
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line 116
> **Code:** `return self._bundle`
> **Type:** Returns a value from a function

### Line 117
> **Code:** `return self._bundle`
> **Type:** Returns a value from a function

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `loader = ModelLoader()`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 120
- **Code lines:** 94
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 23

---
*Documentation generated for: mlops-project-documentation*
*File: model_loader.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/api/__init__.py`
- **Total lines:** 4
- **File size:** 216 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""api package: FastAPI application exposing the demand prediction end...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: metrics.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/api/metrics.py`
- **Total lines:** 52
- **File size:** 1599 bytes

## Line Type Summary
- **Code:** 37
- **Comment:** 0
- **Empty:** 12
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Prometheus instrumentation for the demand forecasting API.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Exposes:`
> **Type:** Code statement

### Line   7
> **Code:** `- request count / latency histograms per endpoint`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- prediction value histogram (feeds drift dashboards)`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `- live model version gauge`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from prometheus_client import Gauge, Histogram`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from prometheus_fastapi_instrumentator import Instrumentator`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `MODEL_PREDICTION_VALUE = Histogram(`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `"model_prediction_value",`
> **Type:** Code statement

### Line  19
> **Code:** `"Distribution of predicted units_sold",`
> **Type:** Code statement

### Line  20
> **Code:** `buckets=(0, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150),`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `)`
> **Type:** Code statement

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PREDICTIONS_TOTAL = Gauge(`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `"predictions_total",`
> **Type:** Code statement

### Line  25
> **Code:** `"Cumulative number of prediction requests",`
> **Type:** Code statement

### Line  26
> **Code:** `["model_version"],`
> **Type:** Data structure operation

### Line  27
> **Code:** `)`
> **Type:** Code statement

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `MODEL_VERSION = Gauge(`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `"mlops_model_version",`
> **Type:** Code statement

### Line  31
> **Code:** `"Version of the model currently served",`
> **Type:** Code statement

### Line  32
> **Code:** `["model_name"],`
> **Type:** Data structure operation

### Line  33
> **Code:** `)`
> **Type:** Code statement

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def setup_metrics(app) -> Instrumentator:`
> **Type:** Function definition

### Line  37
> **Code:** `instrumentator = Instrumentator(`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `should_group_status_codes=False,`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `should_group_untemplated=True,`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `should_respect_env_var=False,`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `)`
> **Type:** Code statement

### Line  42
> **Code:** `instrumentator.instrument(app).expose(app, endpoint="/metrics", includ...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `return instrumentator`
> **Type:** Returns a value from a function

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def record_prediction(predicted_units: float, model_version: str) -> N...`
> **Type:** Function definition

### Line  47
> **Code:** `MODEL_PREDICTION_VALUE.observe(predicted_units)`
> **Type:** Function call

### Line  48
> **Code:** `PREDICTIONS_TOTAL.labels(model_version=model_version).inc()`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `def set_model_version(model_name: str, model_version: str) -> None:`
> **Type:** Function definition

### Line  52
> **Code:** `MODEL_VERSION.labels(model_name=model_name).set(float(model_version) i...`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 52
- **Code lines:** 37
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 12

---
*Documentation generated for: mlops-project-documentation*
*File: metrics.py*
---

# mlops-project-documentation: schemas.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/api/schemas.py`
- **Total lines:** 69
- **File size:** 2260 bytes

## Line Type Summary
- **Code:** 48
- **Comment:** 0
- **Empty:** 18
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Pydantic request/response schemas for the demand forecasting API.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Fields match the training columns exactly for train/inference parity.`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `Pydantic rejects malformed payloads with a 422 and clear error message...`
> **Type:** Logical operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from typing import Literal`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from pydantic import BaseModel, Field`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `class DemandPredictionRequest(BaseModel):`
> **Type:** Class definition

### Line  18
> **Code:** `store_id: int = Field(alias="store_id", ge=1, le=100)`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `sku_id: int = Field(alias="sku_id", ge=1, le=200)`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `day_of_week: int = Field(alias="day_of_week", ge=0, le=6)`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `month: int = Field(alias="month", ge=1, le=12)`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `is_holiday: int = Field(alias="is_holiday", ge=0, le=1)`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `price: float = Field(alias="price", ge=0.0, le=500.0)`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `promotion: int = Field(alias="promotion", ge=0, le=1)`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `temperature: float = Field(alias="temperature", ge=-50.0, le=150.0)`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `inventory_level: int = Field(alias="inventory_level", ge=0, le=10000)`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `competitor_price: float = Field(alias="competitor_price", ge=0.0, le=5...`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `store_traffic: int = Field(alias="store_traffic", ge=0, le=50000)`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `model_config = {"populate_by_name": True}`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def to_dataframe(self):`
> **Type:** Function definition

### Line  33
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  34
> **Code:** `return pd.DataFrame([self.model_dump()])`
> **Type:** Returns a value from a function

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `def _demand_bucket(units: int) -> Literal["low", "medium", "high", "ve...`
> **Type:** Function definition

### Line  38
> **Code:** `if units <= 15:`
> **Type:** Conditional statement

### Line  39
> **Code:** `return "low"`
> **Type:** Returns a value from a function

### Line  40
> **Code:** `elif units <= 35:`
> **Type:** Else-if branch

### Line  41
> **Code:** `return "medium"`
> **Type:** Returns a value from a function

### Line  42
> **Code:** `elif units <= 60:`
> **Type:** Else-if branch

### Line  43
> **Code:** `return "high"`
> **Type:** Returns a value from a function

### Line  44
> **Code:** `else:`
> **Type:** Else block

### Line  45
> **Code:** `return "very_high"`
> **Type:** Returns a value from a function

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `class PredictionResponse(BaseModel):`
> **Type:** Class definition

### Line  49
> **Code:** `predicted_units: int = Field(description="Predicted units_sold")`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `demand_bucket: str = Field(description="Demand bucket: low, medium, hi...`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `model_name: str`
> **Type:** Code statement

### Line  52
> **Code:** `model_version: str`
> **Type:** Code statement

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `PredictionRequest = DemandPredictionRequest | list[DemandPredictionReq...`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `PredictionResult = PredictionResponse | list[PredictionResponse]`
> **Type:** Assignment/comparison

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `class HealthResponse(BaseModel):`
> **Type:** Class definition

### Line  60
> **Code:** `status: str`
> **Type:** Code statement

### Line  61
> **Code:** `model_name: str | None = None`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `model_version: str | None = None`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `class ModelInfoResponse(BaseModel):`
> **Type:** Class definition

### Line  66
> **Code:** `model_name: str`
> **Type:** Code statement

### Line  67
> **Code:** `model_version: str`
> **Type:** Code statement

### Line  68
> **Code:** `run_id: str | None = None`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `production_metrics: dict | None = None`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 69
- **Code lines:** 48
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 18

---
*Documentation generated for: mlops-project-documentation*
*File: schemas.py*
---

# mlops-project-documentation: main.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/api/main.py`
- **Total lines:** 115
- **File size:** 3772 bytes

## Line Type Summary
- **Code:** 91
- **Comment:** 0
- **Empty:** 21
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add request validation and error handling`
> **Type:** TODO: high - Add request validation and error handling

### Line   2
> **Code:** `# TODO: medium - Implement request/response logging`
> **Type:** TODO: medium - Implement request/response logging

### Line   3
> **Code:** `# TODO: low - Add health check endpoint improvement`
> **Type:** TODO: low - Add health check endpoint improvement

### Line   4
> **Code:** `"""FastAPI inference service for the demand forecasting model.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Endpoints:`
> **Type:** Code statement

### Line   7
> **Code:** `- POST /predict        single or batch prediction`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- GET  /health         liveness/readiness probe`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `- GET  /metrics        Prometheus metrics`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `- GET  /model-info     metadata of the loaded model`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `- GET  /               serves the UI dashboard`
> **Type:** Arithmetic operation

### Line  12
> **Code:** `"""`
> **Type:** Code statement

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import json`
> **Type:** Imports a module

### Line  17
> **Code:** `import logging`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from fastapi import FastAPI, HTTPException`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** `from fastapi.responses import FileResponse`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `from src.api import metrics`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from src.api.model_loader import loader`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `from src.api.schemas import (`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `DemandPredictionRequest,`
> **Type:** Logical operation

### Line  27
> **Code:** `HealthResponse,`
> **Type:** Code statement

### Line  28
> **Code:** `ModelInfoResponse,`
> **Type:** Code statement

### Line  29
> **Code:** `PredictionRequest,`
> **Type:** Code statement

### Line  30
> **Code:** `PredictionResponse,`
> **Type:** Code statement

### Line  31
> **Code:** `PredictionResult,`
> **Type:** Code statement

### Line  32
> **Code:** `_demand_bucket,`
> **Type:** Logical operation

### Line  33
> **Code:** `)`
> **Type:** Code statement

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `logger = logging.getLogger("mlops-api")`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "producti...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `UI_DIR = PROJECT_ROOT / "ui"`
> **Type:** Assignment/comparison

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `app = FastAPI(`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `title="MLOps Demand Forecasting API",`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `description="Serves the production demand forecasting model from the M...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `version="1.0.0",`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `)`
> **Type:** Code statement

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `@app.on_event("startup")`
> **Type:** Function call

### Line  48
> **Code:** `def _startup() -> None:`
> **Type:** Function definition

### Line  49
> **Code:** `try:`
> **Type:** Code statement

### Line  50
> **Code:** `bundle = loader.load()`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `metrics.set_model_version(bundle.model_name, bundle.version)`
> **Type:** Function call

### Line  52
> **Code:** `logger.info("model loaded: %s version %s", bundle.model_name, bundle.v...`
> **Type:** Arithmetic operation

### Line  53
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line  54
> **Code:** `logger.error("model loading failed: %s", exc)`
> **Type:** Arithmetic operation

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `@app.get("/health", response_model=HealthResponse, tags=["health"])`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `def health() -> HealthResponse:`
> **Type:** Function definition

### Line  59
> **Code:** `try:`
> **Type:** Code statement

### Line  60
> **Code:** `bundle = loader.get_bundle()`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `return HealthResponse(status="ok", model_name=bundle.model_name, model...`
> **Type:** Returns a value from a function

### Line  62
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line  63
> **Code:** `return HealthResponse(status="degraded")`
> **Type:** Returns a value from a function

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `@app.get("/model-info", response_model=ModelInfoResponse, tags=["healt...`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `def model_info() -> ModelInfoResponse:`
> **Type:** Function definition

### Line  68
> **Code:** `bundle = loader.get_bundle()`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `production_metrics = None`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `if PRODUCTION_REPORT.exists():`
> **Type:** Conditional statement

### Line  71
> **Code:** `production_metrics = json.loads(PRODUCTION_REPORT.read_text()).get("me...`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `return ModelInfoResponse(`
> **Type:** Returns a value from a function

### Line  73
> **Code:** `model_name=bundle.model_name,`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `model_version=bundle.version,`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `run_id=bundle.run_id,`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `production_metrics=production_metrics,`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def _predict_one(request: DemandPredictionRequest) -> PredictionRespon...`
> **Type:** Function definition

### Line  81
> **Code:** `bundle = loader.get_bundle()`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `df = request.to_dataframe()`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `try:`
> **Type:** Code statement

### Line  84
> **Code:** `predictions = bundle.predict(df)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line  86
> **Code:** `raise HTTPException(status_code=500, detail=f"prediction failed: {exc}...`
> **Type:** Raises an exception

### Line  87
> **Code:** `predicted_units = int(round(predictions[0]))`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `bucket = _demand_bucket(predicted_units)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `metrics.record_prediction(float(predicted_units), bundle.version)`
> **Type:** Logical operation

### Line  90
> **Code:** `return PredictionResponse(`
> **Type:** Returns a value from a function

### Line  91
> **Code:** `predicted_units=predicted_units,`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `demand_bucket=bucket,`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `model_name=bundle.model_name,`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `model_version=bundle.version,`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `)`
> **Type:** Code statement

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** `@app.post("/predict", response_model=PredictionResult, tags=["inferenc...`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `def predict(payload: PredictionRequest) -> PredictionResult:`
> **Type:** Function definition

### Line 100
> **Code:** `if isinstance(payload, list):`
> **Type:** Conditional statement

### Line 101
> **Code:** `if not payload:`
> **Type:** Conditional statement

### Line 102
> **Code:** `raise HTTPException(status_code=422, detail="empty prediction batch")`
> **Type:** Raises an exception

### Line 103
> **Code:** `return [_predict_one(request) for request in payload]`
> **Type:** Returns a value from a function

### Line 104
> **Code:** `return _predict_one(payload)`
> **Type:** Returns a value from a function

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `@app.get("/", tags=["ui"])`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `def serve_ui():`
> **Type:** Function definition

### Line 109
> **Code:** `index_path = UI_DIR / "index.html"`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `if index_path.exists():`
> **Type:** Conditional statement

### Line 111
> **Code:** `return FileResponse(str(index_path))`
> **Type:** Returns a value from a function

### Line 112
> **Code:** `raise HTTPException(status_code=404, detail="UI not found")`
> **Type:** Raises an exception

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `metrics.setup_metrics(app)`
> **Type:** Function call

## Summary
- **Total lines:** 115
- **Code lines:** 91
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 21

---
*Documentation generated for: mlops-project-documentation*
*File: main.py*
---

# mlops-project-documentation: alerting.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/monitoring/alerting.py`
- **Total lines:** 60
- **File size:** 1950 bytes

## Line Type Summary
- **Code:** 45
- **Comment:** 0
- **Empty:** 12
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""Alerting helpers used by the monitoring loop and the Airflow DAGs.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Channels (in order of preference):`
> **Type:** Logical operation

### Line   7
> **Code:** `1. Slack webhook (SLACK_WEBHOOK_URL)`
> **Type:** Function call

### Line   8
> **Code:** `2. Local alert log file (data/monitoring/alerts/alerts.jsonl) — always...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `No secrets are ever logged: only the webhook URL prefix is shown.`
> **Type:** Code statement

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `import os`
> **Type:** Imports a module

### Line  17
> **Code:** `import time`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from typing import Any`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import requests`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `ALERT_LOG = PROJECT_ROOT / "data" / "monitoring" / "alerts" / "alerts....`
> **Type:** Assignment/comparison

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `SEVERITY_LEVELS = {"debug": 10, "info": 20, "warning": 30, "critical":...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def send_slack(message: str, severity: str = "info", webhook_url: str ...`
> **Type:** Function definition

### Line  30
> **Code:** `webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `if not webhook_url:`
> **Type:** Conditional statement

### Line  32
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  33
> **Code:** `emoji = {`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `"debug": ":mag:",`
> **Type:** Code statement

### Line  35
> **Code:** `"info": ":information_source:",`
> **Type:** Logical operation

### Line  36
> **Code:** `"warning": ":warning:",`
> **Type:** Code statement

### Line  37
> **Code:** `"critical": ":red_circle:",`
> **Type:** Code statement

### Line  38
> **Code:** `}.get(severity, ":bell:")`
> **Type:** Function call

### Line  39
> **Code:** `try:`
> **Type:** Code statement

### Line  40
> **Code:** `response = requests.post(webhook_url, json={"text": f"{emoji} `[{sever...`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `return response.status_code == 200`
> **Type:** Returns a value from a function

### Line  42
> **Code:** `except requests.RequestException:`
> **Type:** Code statement

### Line  43
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def send_alert(message: str, severity: str = "info", **extra: Any) -> ...`
> **Type:** Function definition

### Line  47
> **Code:** `entry = {`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `"timestamp": time.time(),`
> **Type:** Code statement

### Line  49
> **Code:** `"severity": severity,`
> **Type:** Code statement

### Line  50
> **Code:** `"message": message,`
> **Type:** Code statement

### Line  51
> **Code:** `"extra": extra,`
> **Type:** Code statement

### Line  52
> **Code:** `}`
> **Type:** Code statement

### Line  53
> **Code:** `ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `with ALERT_LOG.open("a") as fh:`
> **Type:** Context manager

### Line  55
> **Code:** `fh.write(json.dumps(entry) + "\n")`
> **Type:** Arithmetic operation

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `delivered = send_slack(message, severity)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `entry["slack_delivered"] = delivered`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `print(f"[alert:{severity}] {message}" + (" (slack)" if delivered else ...`
> **Type:** Prints output to console

### Line  60
> **Code:** `return entry`
> **Type:** Returns a value from a function

## Summary
- **Total lines:** 60
- **Code lines:** 45
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 12

---
*Documentation generated for: mlops-project-documentation*
*File: alerting.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/monitoring/__init__.py`
- **Total lines:** 4
- **File size:** 252 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""monitoring package: drift detection and monitoring utilities for de...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: drift_detection.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/monitoring/drift_detection.py`
- **Total lines:** 116
- **File size:** 4286 bytes

## Line Type Summary
- **Code:** 89
- **Comment:** 0
- **Empty:** 24
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""Model and data drift detection for demand forecasting.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Compares current production data against training reference snapshot:`
> **Type:** Code statement

### Line   7
> **Code:** `- data drift per feature (KS test for numeric)`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- global drift score = fraction of drifted features`
> **Type:** Assignment/comparison

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `import json`
> **Type:** Imports a module

### Line  15
> **Code:** `import os`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference....`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `DEFAULT_CURRENT = PROJECT_ROOT / "data" / "monitoring" / "current.csv"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "monitoring"`
> **Type:** Assignment/comparison

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `NUMERIC_FEATURES = [`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `"store_id", "sku_id", "day_of_week", "month", "is_holiday",`
> **Type:** Logical operation

### Line  27
> **Code:** `"price", "promotion", "temperature", "inventory_level",`
> **Type:** Logical operation

### Line  28
> **Code:** `"competitor_price", "store_traffic",`
> **Type:** Logical operation

### Line  29
> **Code:** `]`
> **Type:** Code statement

### Line  30
> **Code:** `CATEGORICAL_FEATURES = []`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `def _features_columns(df: pd.DataFrame) -> list[str]:`
> **Type:** Function definition

### Line  34
> **Code:** `return [c for c in NUMERIC_FEATURES if c in df.columns]`
> **Type:** Returns a value from a function

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `def _ks_fallback(reference: pd.DataFrame, current: pd.DataFrame) -> tu...`
> **Type:** Function definition

### Line  38
> **Code:** `from scipy import stats`
> **Type:** Imports specific names from a module

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `drifted = 0`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `total = 0`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `per_column: dict[str, dict] = {}`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `for col in _features_columns(reference):`
> **Type:** For loop

### Line  44
> **Code:** `if col not in current.columns:`
> **Type:** Conditional statement

### Line  45
> **Code:** `continue`
> **Type:** Code statement

### Line  46
> **Code:** `ref_vals = pd.to_numeric(reference[col], errors="coerce").dropna()`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `cur_vals = pd.to_numeric(current[col], errors="coerce").dropna()`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `if ref_vals.empty or cur_vals.empty:`
> **Type:** Conditional statement

### Line  49
> **Code:** `continue`
> **Type:** Code statement

### Line  50
> **Code:** `stat, p_value = stats.ks_2samp(ref_vals, cur_vals)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `detected = bool(p_value < 0.05 and stat > 0.1)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `per_column[col] = {"drift_detected": detected, "test": "ks_2samp", "sc...`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `drifted += int(detected)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `total += 1`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `return (drifted / total if total else 0.0), per_column`
> **Type:** Returns a value from a function

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `def detect_drift(`
> **Type:** Function definition

### Line  59
> **Code:** `reference_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `current_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `threshold: float | None = None,`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `output_dir: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `reference_path = Path(reference_path or os.environ.get("DRIFT_REFERENC...`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `current_path = Path(current_path or os.environ.get("DRIFT_CURRENT") or...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `threshold = float(threshold if threshold is not None else os.environ.g...`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `if not reference_path.exists():`
> **Type:** Conditional statement

### Line  70
> **Code:** `raise FileNotFoundError(f"Reference dataset not found: {reference_path...`
> **Type:** Raises an exception

### Line  71
> **Code:** `if not current_path.exists():`
> **Type:** Conditional statement

### Line  72
> **Code:** `raise FileNotFoundError(f"Current production data not found: {current_...`
> **Type:** Raises an exception

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `reference = pd.read_csv(reference_path)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `current = pd.read_csv(current_path)`
> **Type:** Assignment/comparison

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `report = {`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `"engine": "scipy-fallback",`
> **Type:** Arithmetic operation

### Line  81
> **Code:** `"drift_score": drift_score,`
> **Type:** Logical operation

### Line  82
> **Code:** `"threshold": threshold,`
> **Type:** Code statement

### Line  83
> **Code:** `"drift_detected": drift_score > threshold,`
> **Type:** Comparison operation

### Line  84
> **Code:** `"drifted_features": sorted(c for c, info in per_column.items() if info...`
> **Type:** Logical operation

### Line  85
> **Code:** `"per_column": per_column,`
> **Type:** Code statement

### Line  86
> **Code:** `"reference": str(reference_path),`
> **Type:** Code statement

### Line  87
> **Code:** `"current": str(current_path),`
> **Type:** Code statement

### Line  88
> **Code:** `"generated_at": None,`
> **Type:** Code statement

### Line  89
> **Code:** `}`
> **Type:** Code statement

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `output_dir.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `with (output_dir / "drift_report.json").open("w") as fh:`
> **Type:** Context manager

### Line  93
> **Code:** `json.dump(report, fh, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `return report`
> **Type:** Returns a value from a function

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  99
> **Code:** `parser = argparse.ArgumentParser(description="Detect drift between ref...`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `parser.add_argument("--reference", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `parser.add_argument("--current", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `parser.add_argument("--threshold", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `parser.add_argument("--output-dir", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `report = detect_drift(args.reference, args.current, args.threshold, ar...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `print(`
> **Type:** Prints output to console

### Line 108
> **Code:** `f"drift engine={report['engine']} score={report['drift_score']:.3f} th...`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `f"drift_detected={report['drift_detected']}"`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `)`
> **Type:** Code statement

### Line 111
> **Code:** `if report["drift_detected"]:`
> **Type:** Conditional statement

### Line 112
> **Code:** `print(f"drifted features: {report['drifted_features']}")`
> **Type:** Prints output to console

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 116
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 116
- **Code lines:** 89
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 24

---
*Documentation generated for: mlops-project-documentation*
*File: drift_detection.py*
---

# mlops-project-documentation: validation.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/data/validation.py`
- **Total lines:** 190
- **File size:** 7455 bytes

## Line Type Summary
- **Code:** 148
- **Comment:** 0
- **Empty:** 39
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Data validation with Great Expectations.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Loads a declarative expectation suite (great_expectations/expectations...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `and validates a pandas DataFrame against it. Uses the Great Expectatio...`
> **Type:** Logical operation

### Line   8
> **Code:** `available, and falls back to a lightweight built-in evaluator for the ...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `expectation types so validation always runs in CI.`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `Exits non-zero if any expectation fails.`
> **Type:** Arithmetic operation

### Line  12
> **Code:** `"""`
> **Type:** Code statement

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  17
> **Code:** `import json`
> **Type:** Imports a module

### Line  18
> **Code:** `import sys`
> **Type:** Imports a module

### Line  19
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `DEFAULT_SUITE = PROJECT_ROOT / "great_expectations" / "expectations" /...`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "demand_data.csv...`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `SUPPORTED_EXPECTATIONS = [`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `"expect_table_row_count_to_be_between",`
> **Type:** Code statement

### Line  29
> **Code:** `"expect_column_values_to_not_be_null",`
> **Type:** Logical operation

### Line  30
> **Code:** `"expect_column_values_to_be_between",`
> **Type:** Code statement

### Line  31
> **Code:** `"expect_column_values_to_be_in_set",`
> **Type:** Code statement

### Line  32
> **Code:** `"expect_column_values_to_be_of_type",`
> **Type:** Code statement

### Line  33
> **Code:** `"expect_column_values_to_not_match_regex",`
> **Type:** Logical operation

### Line  34
> **Code:** `]`
> **Type:** Code statement

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `class ValidationError(RuntimeError):`
> **Type:** Class definition

### Line  38
> **Code:** `pass`
> **Type:** Code statement

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `def load_suite(path: str | Path) -> dict:`
> **Type:** Function definition

### Line  42
> **Code:** `path = Path(path)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  44
> **Code:** `raise FileNotFoundError(f"Expectation suite not found: {path}")`
> **Type:** Raises an exception

### Line  45
> **Code:** `with path.open() as fh:`
> **Type:** Context manager

### Line  46
> **Code:** `return json.load(fh)`
> **Type:** Returns a value from a function

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def _check_expectation(df: pd.DataFrame, expectation: dict) -> tuple[b...`
> **Type:** Function definition

### Line  50
> **Code:** `kind = expectation["expectation_type"]`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `kwargs = expectation.get("kwargs", {})`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `column = kwargs.get("column")`
> **Type:** Assignment/comparison

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `if kind == "expect_table_row_count_to_be_between":`
> **Type:** Conditional statement

### Line  55
> **Code:** `return kwargs["min_value"] <= len(df) <= kwargs["max_value"], f"row co...`
> **Type:** Returns a value from a function

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `if column is None or column not in df.columns:`
> **Type:** Conditional statement

### Line  58
> **Code:** `return False, f"column '{column}' missing"`
> **Type:** Returns a value from a function

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `if kind == "expect_column_values_to_not_be_null":`
> **Type:** Conditional statement

### Line  61
> **Code:** `bad = int(df[column].isna().sum())`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `return bad == 0, f"{bad} null values in {column}"`
> **Type:** Returns a value from a function

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `if kind == "expect_column_values_to_be_between":`
> **Type:** Conditional statement

### Line  65
> **Code:** `if not pd.api.types.is_numeric_dtype(df[column]):`
> **Type:** Conditional statement

### Line  66
> **Code:** `return False, f"{column} not numeric"`
> **Type:** Returns a value from a function

### Line  67
> **Code:** `vals = df[column].dropna()`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `lo, hi = kwargs.get("min_value", -float("inf")), kwargs.get("max_value...`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `bad = int(((vals < lo) | (vals > hi)).sum())`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `return bad == 0, f"{bad} values outside [{lo}, {hi}] in {column}"`
> **Type:** Returns a value from a function

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `if kind == "expect_column_values_to_be_in_set":`
> **Type:** Conditional statement

### Line  73
> **Code:** `allowed = set(kwargs.get("value_set", []))`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `vals = df[column].dropna().astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `bad = int((~vals.isin(allowed)).sum())`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `return bad == 0, f"{bad} unexpected values in {column}"`
> **Type:** Returns a value from a function

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `if kind == "expect_column_values_to_be_of_type":`
> **Type:** Conditional statement

### Line  79
> **Code:** `actual = str(df[column].dtype)`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `expected = kwargs.get("type_")`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `return actual == expected, f"{column} dtype {actual} != {expected}"`
> **Type:** Returns a value from a function

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `if kind == "expect_column_values_to_not_match_regex":`
> **Type:** Conditional statement

### Line  84
> **Code:** `pattern = kwargs.get("regex")`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `matches = df[column].dropna().astype(str).str.contains(pattern, regex=...`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `bad = int(matches.sum())`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `return bad == 0, f"{bad} rows match forbidden regex in {column}"`
> **Type:** Returns a value from a function

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `return True, f"unsupported expectation {kind} ignored"`
> **Type:** Returns a value from a function

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `def validate_dataframe(df: pd.DataFrame, suite: dict) -> dict:`
> **Type:** Function definition

### Line  93
> **Code:** `results = []`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `failures = 0`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `for expectation in suite.get("expectations", []):`
> **Type:** For loop

### Line  96
> **Code:** `kind = expectation["expectation_type"]`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `if kind not in SUPPORTED_EXPECTATIONS:`
> **Type:** Conditional statement

### Line  98
> **Code:** `continue`
> **Type:** Code statement

### Line  99
> **Code:** `try:`
> **Type:** Code statement

### Line 100
> **Code:** `success, detail = _check_expectation(df, expectation)`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line 102
> **Code:** `success, detail = False, str(exc)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `results.append({"expectation_type": kind, "kwargs": expectation.get("k...`
> **Type:** Function call

### Line 104
> **Code:** `failures += 0 if success else 1`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `summary = {`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `"suite": suite.get("expectation_suite_name", "dataset_suite"),`
> **Type:** Code statement

### Line 108
> **Code:** `"total": len(results),`
> **Type:** Code statement

### Line 109
> **Code:** `"passed": len(results) - failures,`
> **Type:** Arithmetic operation

### Line 110
> **Code:** `"failed": failures,`
> **Type:** Code statement

### Line 111
> **Code:** `"results": results,`
> **Type:** Code statement

### Line 112
> **Code:** `}`
> **Type:** Code statement

### Line 113
> **Code:** `return summary`
> **Type:** Returns a value from a function

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `def _to_ge_suite(suite: dict):`
> **Type:** Function definition

### Line 117
> **Code:** `from great_expectations.core import ExpectationSuite`
> **Type:** Imports specific names from a module

### Line 118
> **Code:** `from great_expectations.expectations.expectation import ExpectationCon...`
> **Type:** Imports specific names from a module

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `ge_suite = ExpectationSuite(expectation_suite_name=suite.get("expectat...`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `for expectation in suite.get("expectations", []):`
> **Type:** For loop

### Line 122
> **Code:** `if expectation["expectation_type"] in SUPPORTED_EXPECTATIONS:`
> **Type:** Conditional statement

### Line 123
> **Code:** `ge_suite.add_expectation(`
> **Type:** Code statement

### Line 124
> **Code:** `ExpectationConfiguration(expectation_type=expectation["expectation_typ...`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `)`
> **Type:** Code statement

### Line 126
> **Code:** `return ge_suite`
> **Type:** Returns a value from a function

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `def validate_expectations_suite(df: pd.DataFrame, suite: dict) -> dict...`
> **Type:** Function definition

### Line 130
> **Code:** `try:`
> **Type:** Code statement

### Line 131
> **Code:** `from great_expectations import from_pandas  # type: ignore`
> **Type:** Imports specific names from a module

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `ge_result = from_pandas(df, expectation_suite=_to_ge_suite(suite)).val...`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `summary = {`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `"suite": suite.get("expectation_suite_name", "dataset_suite"),`
> **Type:** Code statement

### Line 136
> **Code:** `"total": int(ge_result.statistics["evaluated_expectations"]),`
> **Type:** Data structure operation

### Line 137
> **Code:** `"passed": int(ge_result.statistics["successful_expectations"]),`
> **Type:** Data structure operation

### Line 138
> **Code:** `"failed": int(ge_result.statistics["evaluated_expectations"] - ge_resu...`
> **Type:** Arithmetic operation

### Line 139
> **Code:** `"engine": "great_expectations",`
> **Type:** Code statement

### Line 140
> **Code:** `}`
> **Type:** Code statement

### Line 141
> **Code:** `if not ge_result.success:`
> **Type:** Conditional statement

### Line 142
> **Code:** `summary["failures"] = [`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `{"expectation_type": r.expectation_config.expectation_type, "detail": ...`
> **Type:** Logical operation

### Line 144
> **Code:** `for r in ge_result.results`
> **Type:** For loop

### Line 145
> **Code:** `if not r.success`
> **Type:** Conditional statement

### Line 146
> **Code:** `]`
> **Type:** Code statement

### Line 147
> **Code:** `return summary`
> **Type:** Returns a value from a function

### Line 148
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line 149
> **Code:** `return validate_dataframe(df, suite)`
> **Type:** Returns a value from a function

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `def validate(input_path: str | Path | None = None, suite_path: str | P...`
> **Type:** Function definition

### Line 153
> **Code:** `input_path = Path(input_path or DEFAULT_INPUT)`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `suite = load_suite(suite_path or DEFAULT_SUITE)`
> **Type:** Assignment/comparison

### Line 155
> **Code:** `if not input_path.exists():`
> **Type:** Conditional statement

### Line 156
> **Code:** `raise FileNotFoundError(f"Input dataset not found: {input_path}")`
> **Type:** Raises an exception

### Line 157
> **Code:** `df = pd.read_csv(input_path)`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `return validate_expectations_suite(df, suite)`
> **Type:** Returns a value from a function

### Line 159
> **Code:** ``
> **Type:** Empty line

### Line 160
> **Code:** ``
> **Type:** Empty line

### Line 161
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 162
> **Code:** `parser = argparse.ArgumentParser(description="Validate dataset against...`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `parser.add_argument("--input", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `parser.add_argument("--suite", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `parser.add_argument("--json-output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 167
> **Code:** ``
> **Type:** Empty line

### Line 168
> **Code:** `summary = validate(args.input, args.suite)`
> **Type:** Assignment/comparison

### Line 169
> **Code:** `print(f"suite={summary['suite']} passed={summary['passed']}/{summary['...`
> **Type:** Prints output to console

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `if args.json_output:`
> **Type:** Conditional statement

### Line 172
> **Code:** `Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 173
> **Code:** `with Path(args.json_output).open("w") as fh:`
> **Type:** Context manager

### Line 174
> **Code:** `json.dump(summary, fh, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 175
> **Code:** ``
> **Type:** Empty line

### Line 176
> **Code:** `if summary["failed"]:`
> **Type:** Conditional statement

### Line 177
> **Code:** `for failure in summary.get("failures", []):`
> **Type:** For loop

### Line 178
> **Code:** `print(f"  FAIL {failure.get('expectation_type')}: {failure.get('detail...`
> **Type:** Prints output to console

### Line 179
> **Code:** `raise ValidationError(f"Data validation failed: {summary['failed']} ex...`
> **Type:** Raises an exception

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** ``
> **Type:** Empty line

### Line 182
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 183
> **Code:** `try:`
> **Type:** Code statement

### Line 184
> **Code:** `main()`
> **Type:** Function call

### Line 185
> **Code:** `except ValidationError as exc:`
> **Type:** Logical operation

### Line 186
> **Code:** `print(f"validation error: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line 187
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line 188
> **Code:** `except (FileNotFoundError, OSError) as exc:`
> **Type:** Logical operation

### Line 189
> **Code:** `print(f"validation error: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line 190
> **Code:** `sys.exit(2)`
> **Type:** Function call

## Summary
- **Total lines:** 190
- **Code lines:** 148
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 39

---
*Documentation generated for: mlops-project-documentation*
*File: validation.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/data/__init__.py`
- **Total lines:** 4
- **File size:** 236 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""data package: data loading, preprocessing, and DVC-managed versioni...`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: ingestion.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/data/ingestion.py`
- **Total lines:** 100
- **File size:** 3595 bytes

## Line Type Summary
- **Code:** 75
- **Comment:** 0
- **Empty:** 22
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add tag mapping version control`
> **Type:** TODO: high - Add tag mapping version control

### Line   2
> **Code:** `# TODO: medium - Implement store-and-forward buffer health checks`
> **Type:** TODO: medium - Implement store-and-forward buffer health checks

### Line   3
> **Code:** `# TODO: low - Add unmapped tag alerting`
> **Type:** TODO: low - Add unmapped tag alerting

### Line   4
> **Code:** `"""Data ingestion: pull raw data from a source (CSV file or URL) into ...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Idempotent: re-running produces the same normalized raw dataset.`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `Source is resolved as: --source CLI arg > INGESTION_SOURCE env > defau...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  13
> **Code:** `import os`
> **Type:** Imports a module

### Line  14
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `DEFAULT_SOURCE = PROJECT_ROOT / "data" / "external" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `DEFAULT_DESTINATION = PROJECT_ROOT / "data" / "raw" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `RAW_COLUMN_TYPES: dict[str, str] = {`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `"store_id": "int64",`
> **Type:** Logical operation

### Line  24
> **Code:** `"sku_id": "int64",`
> **Type:** Code statement

### Line  25
> **Code:** `"date": "object",`
> **Type:** Code statement

### Line  26
> **Code:** `"day_of_week": "int64",`
> **Type:** Code statement

### Line  27
> **Code:** `"month": "int64",`
> **Type:** Code statement

### Line  28
> **Code:** `"is_holiday": "int64",`
> **Type:** Code statement

### Line  29
> **Code:** `"price": "float64",`
> **Type:** Code statement

### Line  30
> **Code:** `"promotion": "int64",`
> **Type:** Code statement

### Line  31
> **Code:** `"temperature": "float64",`
> **Type:** Code statement

### Line  32
> **Code:** `"inventory_level": "int64",`
> **Type:** Logical operation

### Line  33
> **Code:** `"competitor_price": "float64",`
> **Type:** Logical operation

### Line  34
> **Code:** `"store_traffic": "int64",`
> **Type:** Logical operation

### Line  35
> **Code:** `"units_sold": "int64",`
> **Type:** Code statement

### Line  36
> **Code:** `}`
> **Type:** Code statement

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def _read_source(source: str | Path) -> pd.DataFrame:`
> **Type:** Function definition

### Line  40
> **Code:** `source = str(source)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `if source.startswith(("http://", "https://", "s3://")):`
> **Type:** Conditional statement

### Line  42
> **Code:** `return pd.read_csv(source)`
> **Type:** Returns a value from a function

### Line  43
> **Code:** `path = Path(source)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  45
> **Code:** `raise FileNotFoundError(f"Ingestion source not found: {source}")`
> **Type:** Raises an exception

### Line  46
> **Code:** `return pd.read_csv(path)`
> **Type:** Returns a value from a function

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def normalize(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  50
> **Code:** `df = df.copy()`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `df.columns = [c.strip() for c in df.columns]`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `for col in df.select_dtypes(include="object").columns:`
> **Type:** For loop

### Line  53
> **Code:** `df[col] = df[col].astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `for col, dtype in RAW_COLUMN_TYPES.items():`
> **Type:** For loop

### Line  55
> **Code:** `if col in df.columns:`
> **Type:** Conditional statement

### Line  56
> **Code:** `try:`
> **Type:** Code statement

### Line  57
> **Code:** `df[col] = df[col].astype(dtype)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `except (ValueError, TypeError):`
> **Type:** Logical operation

### Line  59
> **Code:** `df[col] = pd.to_numeric(df[col].str.replace(r"[$, ]", "", regex=True),...`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `def resolve_destination(destination: str | Path | None = None) -> Path...`
> **Type:** Function definition

### Line  64
> **Code:** `"""Resolve the output path the same way :func:`ingest` does."""`
> **Type:** Code statement

### Line  65
> **Code:** `return Path(destination or os.environ.get("INGESTION_DESTINATION") or ...`
> **Type:** Returns a value from a function

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def ingest(source: str | Path | None = None, destination: str | Path |...`
> **Type:** Function definition

### Line  69
> **Code:** `source = source or os.environ.get("INGESTION_SOURCE") or DEFAULT_SOURC...`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `destination = resolve_destination(destination)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `resolved = Path(source) if not str(source).startswith(("http", "s3")) ...`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `if isinstance(resolved, Path) and not resolved.exists():`
> **Type:** Conditional statement

### Line  74
> **Code:** `fallback = DEFAULT_DESTINATION if resolved != DEFAULT_DESTINATION else...`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `if fallback is not None and fallback.exists():`
> **Type:** Conditional statement

### Line  76
> **Code:** `resolved = fallback`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `else:`
> **Type:** Else block

### Line  78
> **Code:** `raise FileNotFoundError(f"Ingestion source not found: {source}")`
> **Type:** Raises an exception

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `df = _read_source(resolved)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `df = normalize(df)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `destination.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `df.to_csv(destination, index=False)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  89
> **Code:** `parser = argparse.ArgumentParser(description="Ingest the raw demand da...`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `parser.add_argument("--source", type=str, default=None, help="CSV path...`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `parser.add_argument("--destination", type=str, default=None, help="Out...`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `df = ingest(args.source, args.destination)`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `destination = resolve_destination(args.destination)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `print(f"ingested {len(df)} rows x {len(df.columns)} columns -> {destin...`
> **Type:** Prints output to console

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 100
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 100
- **Code lines:** 75
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 22

---
*Documentation generated for: mlops-project-documentation*
*File: ingestion.py*
---

# mlops-project-documentation: preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/data/preprocessing.py`
- **Total lines:** 69
- **File size:** 2249 bytes

## Line Type Summary
- **Code:** 45
- **Comment:** 0
- **Empty:** 21
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Data preprocessing for demand forecasting data.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Cleans raw demand data and produces a model-ready table.`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `Operations: coerce numeric columns, drop rows with invalid values, str...`
> **Type:** Code statement

### Line   8
> **Code:** `Output: data/processed/demand_data.csv`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "demand_data.cs...`
> **Type:** Assignment/comparison

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `NUMERIC_COLUMNS = [`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `"store_id", "sku_id", "day_of_week", "month", "is_holiday",`
> **Type:** Logical operation

### Line  24
> **Code:** `"price", "promotion", "temperature", "inventory_level",`
> **Type:** Logical operation

### Line  25
> **Code:** `"competitor_price", "store_traffic", "units_sold",`
> **Type:** Logical operation

### Line  26
> **Code:** `]`
> **Type:** Code statement

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def resolve_output(output_path: str | Path | None = None) -> Path:`
> **Type:** Function definition

### Line  30
> **Code:** `"""Resolve the output path the same way :func:`preprocess` does."""`
> **Type:** Code statement

### Line  31
> **Code:** `return Path(output_path or DEFAULT_OUTPUT)`
> **Type:** Returns a value from a function

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `def preprocess(input_path: str | Path | None = None, output_path: str ...`
> **Type:** Function definition

### Line  35
> **Code:** `input_path = Path(input_path or DEFAULT_INPUT)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `output_path = resolve_output(output_path)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `if not input_path.exists():`
> **Type:** Conditional statement

### Line  39
> **Code:** `raise FileNotFoundError(f"Input dataset not found: {input_path}")`
> **Type:** Raises an exception

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `df = pd.read_csv(input_path)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `for col in NUMERIC_COLUMNS:`
> **Type:** For loop

### Line  44
> **Code:** `if col in df.columns:`
> **Type:** Conditional statement

### Line  45
> **Code:** `df[col] = pd.to_numeric(df[col], errors="coerce")`
> **Type:** Assignment/comparison

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `df = df.dropna(subset=NUMERIC_COLUMNS).copy()`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `df = df[df["units_sold"] >= 0]`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `if "date" in df.columns:`
> **Type:** Conditional statement

### Line  51
> **Code:** `df["date"] = df["date"].astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `df.to_csv(output_path, index=False)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  59
> **Code:** `parser = argparse.ArgumentParser(description="Preprocess raw demand da...`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `parser.add_argument("--input", type=str, default=None)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `parser.add_argument("--output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `df = preprocess(args.input, args.output)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `print(f"preprocessed {len(df)} rows x {len(df.columns)} columns -> {re...`
> **Type:** Prints output to console

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  69
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 69
- **Code lines:** 45
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 21

---
*Documentation generated for: mlops-project-documentation*
*File: preprocessing.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/features/__init__.py`
- **Total lines:** 4
- **File size:** 213 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""features package: feature engineering pipeline for demand forecasti...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: build_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/features/build_features.py`
- **Total lines:** 121
- **File size:** 3928 bytes

## Line Type Summary
- **Code:** 93
- **Comment:** 0
- **Empty:** 25
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Feature engineering for demand forecasting.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Transforms raw demand data into model features with a FeatureTransform...`
> **Type:** Logical operation

### Line   7
> **Code:** `for train/inference parity. Outputs:`
> **Type:** For loop

### Line   8
> **Code:** `- data/features/features.parquet`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `- data/features/features_config.json`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "demand_data.csv...`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "features" / "features.parque...`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config...`
> **Type:** Assignment/comparison

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `TARGET_COLUMN = "units_sold"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `TARGET_FEATURE = "units_sold"`
> **Type:** Assignment/comparison

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `FEATURE_ORDER = [`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `"store_id",`
> **Type:** Logical operation

### Line  30
> **Code:** `"sku_id",`
> **Type:** Code statement

### Line  31
> **Code:** `"day_of_week",`
> **Type:** Code statement

### Line  32
> **Code:** `"month",`
> **Type:** Code statement

### Line  33
> **Code:** `"is_holiday",`
> **Type:** Code statement

### Line  34
> **Code:** `"price",`
> **Type:** Code statement

### Line  35
> **Code:** `"promotion",`
> **Type:** Code statement

### Line  36
> **Code:** `"temperature",`
> **Type:** Code statement

### Line  37
> **Code:** `"inventory_level",`
> **Type:** Logical operation

### Line  38
> **Code:** `"competitor_price",`
> **Type:** Logical operation

### Line  39
> **Code:** `"store_traffic",`
> **Type:** Logical operation

### Line  40
> **Code:** `]`
> **Type:** Code statement

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `class FeatureTransformer:`
> **Type:** Class definition

### Line  44
> **Code:** `def __init__(self, numeric_features: list[str] | None = None):`
> **Type:** Function definition

### Line  45
> **Code:** `self.numeric_features = numeric_features or [`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `"store_id", "sku_id", "day_of_week", "month", "is_holiday",`
> **Type:** Logical operation

### Line  47
> **Code:** `"price", "promotion", "temperature", "inventory_level",`
> **Type:** Logical operation

### Line  48
> **Code:** `"competitor_price", "store_traffic",`
> **Type:** Logical operation

### Line  49
> **Code:** `]`
> **Type:** Code statement

### Line  50
> **Code:** `self.numeric_stats: dict[str, dict[str, float]] = {}`
> **Type:** Assignment/comparison

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def fit(self, df: pd.DataFrame) -> FeatureTransformer:`
> **Type:** Function definition

### Line  53
> **Code:** `for col in self.numeric_features:`
> **Type:** For loop

### Line  54
> **Code:** `self.numeric_stats[col] = {`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `"mean": float(df[col].mean()),`
> **Type:** Data structure operation

### Line  56
> **Code:** `"std": float(df[col].std(ddof=0)) or 1.0,`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `}`
> **Type:** Code statement

### Line  58
> **Code:** `return self`
> **Type:** Returns a value from a function

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `def transform(self, df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  61
> **Code:** `data = df.copy()`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `for col in self.numeric_features:`
> **Type:** For loop

### Line  63
> **Code:** `data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0).asty...`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `return data[FEATURE_ORDER]`
> **Type:** Returns a value from a function

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  67
> **Code:** `return self.fit(df).transform(df)`
> **Type:** Returns a value from a function

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def to_config(self) -> dict:`
> **Type:** Function definition

### Line  70
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  71
> **Code:** `"numeric_features": self.numeric_features,`
> **Type:** Code statement

### Line  72
> **Code:** `"numeric_stats": self.numeric_stats,`
> **Type:** Code statement

### Line  73
> **Code:** `"feature_order": FEATURE_ORDER,`
> **Type:** Logical operation

### Line  74
> **Code:** `}`
> **Type:** Code statement

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `@classmethod`
> **Type:** Code statement

### Line  77
> **Code:** `def from_config(cls, config: dict) -> FeatureTransformer:`
> **Type:** Function definition

### Line  78
> **Code:** `transformer = cls(config["numeric_features"])`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `transformer.numeric_stats = config["numeric_stats"]`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `return transformer`
> **Type:** Returns a value from a function

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `def build_features(`
> **Type:** Function definition

### Line  84
> **Code:** `input_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `output_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `config_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `) -> pd.DataFrame:`
> **Type:** Arithmetic operation

### Line  88
> **Code:** `input_path = Path(input_path or DEFAULT_INPUT)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `output_path = Path(output_path or DEFAULT_OUTPUT)`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `config_path = Path(config_path or DEFAULT_CONFIG)`
> **Type:** Assignment/comparison

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `if not input_path.exists():`
> **Type:** Conditional statement

### Line  93
> **Code:** `raise FileNotFoundError(f"Input dataset not found: {input_path}")`
> **Type:** Raises an exception

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `df = pd.read_csv(input_path)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `if TARGET_COLUMN in df.columns:`
> **Type:** Conditional statement

### Line 100
> **Code:** `features[TARGET_FEATURE] = df[TARGET_COLUMN].astype(float)`
> **Type:** Assignment/comparison

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `features.to_parquet(output_path, index=False)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `with config_path.open("w") as fh:`
> **Type:** Context manager

### Line 105
> **Code:** `json.dump(transformer.to_config(), fh, indent=2)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `return features`
> **Type:** Returns a value from a function

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 110
> **Code:** `parser = argparse.ArgumentParser(description="Build features from dema...`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `parser.add_argument("--input", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `parser.add_argument("--output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `parser.add_argument("--config", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `features = build_features(args.input, args.output, args.config)`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `print(f"built {features.shape[0]} rows x {features.shape[1]} features ...`
> **Type:** Prints output to console

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 121
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 121
- **Code lines:** 93
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 25

---
*Documentation generated for: mlops-project-documentation*
*File: build_features.py*
---

# mlops-project-documentation: feature_store.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/src/features/feature_store.py`
- **Total lines:** 103
- **File size:** 4634 bytes

## Line Type Summary
- **Code:** 80
- **Comment:** 0
- **Empty:** 20
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Lightweight Parquet feature store, versioned by DVC.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Each `put_features` writes data/features/features_v{N}.parquet togethe...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `documented schema (name, type, description, expected range). DVC versi...`
> **Type:** Code statement

### Line   8
> **Code:** `Parquet files; a Git commit pins the exact feature snapshot used for t...`
> **Type:** Logical operation

### Line   9
> **Code:** `so any production model can be traced back to its feature set.`
> **Type:** Code statement

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `DEFAULT_DIR = PROJECT_ROOT / "data" / "features"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `SCHEMA_FILE = "features_store_schema.json"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `FEATURE_SCHEMA = {`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `"store_id": {"type": "int64", "description": "Store identifier", "expe...`
> **Type:** Logical operation

### Line  26
> **Code:** `"sku_id": {"type": "int64", "description": "Product (SKU) identifier",...`
> **Type:** Data structure operation

### Line  27
> **Code:** `"day_of_week": {"type": "int64", "description": "Day of week (0=Monday...`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `"month": {"type": "int64", "description": "Calendar month", "expected_...`
> **Type:** Data structure operation

### Line  29
> **Code:** `"is_holiday": {"type": "int64", "description": "1 if the day is a publ...`
> **Type:** Data structure operation

### Line  30
> **Code:** `"price": {"type": "float64", "description": "Selling price", "expected...`
> **Type:** Data structure operation

### Line  31
> **Code:** `"promotion": {"type": "int64", "description": "1 if the product is on ...`
> **Type:** Data structure operation

### Line  32
> **Code:** `"temperature": {"type": "float64", "description": "Outside temperature...`
> **Type:** Arithmetic operation

### Line  33
> **Code:** `"inventory_level": {"type": "int64", "description": "Stock on hand", "...`
> **Type:** Logical operation

### Line  34
> **Code:** `"competitor_price": {"type": "float64", "description": "Competitor sel...`
> **Type:** Logical operation

### Line  35
> **Code:** `"store_traffic": {"type": "int64", "description": "Store footfall for ...`
> **Type:** Logical operation

### Line  36
> **Code:** `"units_sold": {"type": "int64", "description": "Target: units sold", "...`
> **Type:** Data structure operation

### Line  37
> **Code:** `}`
> **Type:** Code statement

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `class FeatureStore:`
> **Type:** Class definition

### Line  41
> **Code:** `def __init__(self, base_dir: str | Path | None = None):`
> **Type:** Function definition

### Line  42
> **Code:** `self.base_dir = Path(base_dir or DEFAULT_DIR)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `self.base_dir.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `def _version_file(self, version: int) -> Path:`
> **Type:** Function definition

### Line  46
> **Code:** `return self.base_dir / f"features_v{version}.parquet"`
> **Type:** Returns a value from a function

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def next_version(self) -> int:`
> **Type:** Function definition

### Line  49
> **Code:** `versions = [p.stem.split("_v")[-1] for p in self.base_dir.glob("featur...`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `return max((int(v) for v in versions), default=0) + 1`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def put_features(self, df: pd.DataFrame, version: int | None = None) -...`
> **Type:** Function definition

### Line  53
> **Code:** `version = version or self.next_version()`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `df.to_parquet(self._version_file(version), index=False)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `self.write_schema(df)`
> **Type:** Function call

### Line  56
> **Code:** `return version`
> **Type:** Returns a value from a function

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `def get_features(self, version: int | None = None) -> pd.DataFrame:`
> **Type:** Function definition

### Line  59
> **Code:** `if version is None:`
> **Type:** Conditional statement

### Line  60
> **Code:** `version = max(1, self.next_version() - 1)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `path = self._version_file(version)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  63
> **Code:** `raise FileNotFoundError(f"Feature version not found: {path}")`
> **Type:** Raises an exception

### Line  64
> **Code:** `return pd.read_parquet(path)`
> **Type:** Returns a value from a function

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `def list_versions(self) -> list[int]:`
> **Type:** Function definition

### Line  67
> **Code:** `return sorted(int(p.stem.split("_v")[-1]) for p in self.base_dir.glob(...`
> **Type:** Returns a value from a function

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def write_schema(self, df: pd.DataFrame) -> None:`
> **Type:** Function definition

### Line  70
> **Code:** `schema = {"store": "lightweight-parquet", "versioned_by": "dvc", "feat...`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `for col in df.columns:`
> **Type:** For loop

### Line  72
> **Code:** `entry = dict(FEATURE_SCHEMA.get(col, {"type": str(df[col].dtype), "des...`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `entry["dtype"] = str(df[col].dtype)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `schema["features"][col] = entry`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `with (self.base_dir / SCHEMA_FILE).open("w") as fh:`
> **Type:** Context manager

### Line  76
> **Code:** `json.dump(schema, fh, indent=2)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `def schema(self) -> dict:`
> **Type:** Function definition

### Line  79
> **Code:** `path = self.base_dir / SCHEMA_FILE`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  81
> **Code:** `return {}`
> **Type:** Returns a value from a function

### Line  82
> **Code:** `with path.open() as fh:`
> **Type:** Context manager

### Line  83
> **Code:** `return json.load(fh)`
> **Type:** Returns a value from a function

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  87
> **Code:** `parser = argparse.ArgumentParser(description="Inspect the lightweight ...`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `parser.add_argument("--list-versions", action="store_true")`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `parser.add_argument("--schema", action="store_true")`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `parser.add_argument("--show", type=int, default=None, help="Show head ...`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `store = FeatureStore()`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `if args.list_versions:`
> **Type:** Conditional statement

### Line  95
> **Code:** `print(f"versions: {store.list_versions()}")`
> **Type:** Prints output to console

### Line  96
> **Code:** `if args.schema:`
> **Type:** Conditional statement

### Line  97
> **Code:** `print(json.dumps(store.schema(), indent=2))`
> **Type:** Prints output to console

### Line  98
> **Code:** `if args.show is not None:`
> **Type:** Conditional statement

### Line  99
> **Code:** `print(store.get_features(args.show).head(5).to_string())`
> **Type:** Prints output to console

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 103
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 103
- **Code lines:** 80
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 20

---
*Documentation generated for: mlops-project-documentation*
*File: feature_store.py*
---

# mlops-project-documentation: generate_demand_data.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/ml/data/generate_demand_data.py`
- **Total lines:** 109
- **File size:** 4348 bytes

## Line Type Summary
- **Code:** 77
- **Comment:** 0
- **Empty:** 29
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Generate demand forecasting data from real PBS (Pharmaceutical Bene...`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Parses Australian PBS monthly scripts data (683 series × 206 months, J...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `Creates features for demand forecasting: drug_id, concession_type, mon...`
> **Type:** Logical operation

### Line   8
> **Code:** `lag_1, lag_12, rolling_mean_3, rolling_mean_6. Target: next month's sc...`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `import os`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `SEED = 42`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `PBS_PATH = Path(os.getenv("PBS_DATA_PATH", "/tmp/realdata/PBS.csv"))`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `OUTPUT_PATH = Path("data/raw/pbs_demand_data.csv")`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `def parse_pbs(pbs_path: Path = PBS_PATH) -> pd.DataFrame:`
> **Type:** Function definition

### Line  26
> **Code:** `"""Parse PBS.csv: skip 8 header rows, reshape wide (206 months) to lon...`
> **Type:** Logical operation

### Line  27
> **Code:** `if not pbs_path.exists():`
> **Type:** Conditional statement

### Line  28
> **Code:** `raise SystemExit(`
> **Type:** Raises an exception

### Line  29
> **Code:** `f"Raw PBS data not found at {pbs_path}.\n"`
> **Type:** Logical operation

### Line  30
> **Code:** `"Download the PBS monthly scripts export and set PBS_DATA_PATH to it. ...`
> **Type:** Logical operation

### Line  31
> **Code:** `"The generated data/raw/pbs_demand_data.csv is already versioned, so "`
> **Type:** Arithmetic operation

### Line  32
> **Code:** `"this script is only needed to regenerate it from source."`
> **Type:** Code statement

### Line  33
> **Code:** `)`
> **Type:** Code statement

### Line  34
> **Code:** `df = pd.read_csv(pbs_path, header=None, skiprows=8)`
> **Type:** Assignment/comparison

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `month_cols = [f"m_{i}" for i in range(1, 205)]`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `df.columns = ["concession_type", "atc_code", "drug_class"] + month_col...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `df = df.dropna(subset=["concession_type", "atc_code", "drug_class"])`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `df = df[df["concession_type"].astype(str).str.strip() != ""]`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `for col in month_cols:`
> **Type:** For loop

### Line  43
> **Code:** `df[col] = pd.to_numeric(`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce"`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `).fillna(0)`
> **Type:** Function call

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `df = df[(df[month_cols] != 0).any(axis=1)]`
> **Type:** Assignment/comparison

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `id_vars = ["concession_type", "atc_code", "drug_class"]`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `long_df = df.melt(id_vars=id_vars, value_vars=month_cols, var_name="mo...`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `long_df["month_idx"] = long_df["month_idx"].str.replace("m_", "").asty...`
> **Type:** Assignment/comparison

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `long_df["year"] = 1991 + (long_df["month_idx"] - 1) // 12`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `long_df["month"] = ((long_df["month_idx"] - 1) % 12) + 1`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `long_df["date"] = pd.to_datetime(dict(year=long_df["year"], month=long...`
> **Type:** Assignment/comparison

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `long_df["drug_id"] = (`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `long_df["concession_type"].astype(str)`
> **Type:** Function call

### Line  59
> **Code:** `+ "_"`
> **Type:** Arithmetic operation

### Line  60
> **Code:** `+ long_df["atc_code"].astype(str)`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `+ "_"`
> **Type:** Arithmetic operation

### Line  62
> **Code:** `+ long_df["drug_class"].astype(str).str.replace(r"[^A-Z0-9]", "", rege...`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `)`
> **Type:** Code statement

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `return long_df[["drug_id", "concession_type", "atc_code", "drug_class"...`
> **Type:** Returns a value from a function

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def create_features(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  69
> **Code:** `"""Create lag and rolling features for each drug series."""`
> **Type:** Logical operation

### Line  70
> **Code:** `df = df.sort_values(["drug_id", "date"]).copy()`
> **Type:** Assignment/comparison

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `df["lag_1"] = df.groupby("drug_id")["scripts"].shift(1)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `df["lag_12"] = df.groupby("drug_id")["scripts"].shift(12)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `df["rolling_mean_3"] = df.groupby("drug_id")["scripts"].transform(lamb...`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `df["rolling_mean_6"] = df.groupby("drug_id")["scripts"].transform(lamb...`
> **Type:** Assignment/comparison

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `df["target"] = df.groupby("drug_id")["scripts"].shift(-1)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `df = df.dropna(subset=["lag_1", "lag_12", "rolling_mean_3", "rolling_m...`
> **Type:** Assignment/comparison

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  85
> **Code:** `parser = argparse.ArgumentParser(description="Generate demand forecast...`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `parser.add_argument("--pbs-path", type=Path, default=PBS_PATH)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `parser.add_argument("--output", type=Path, default=OUTPUT_PATH)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `parser.add_argument("--seed", type=int, default=SEED)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `np.random.seed(args.seed)`
> **Type:** Logical operation

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `print("Parsing PBS data...")`
> **Type:** Prints output to console

### Line  94
> **Code:** `long_df = parse_pbs(args.pbs_path)`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `print(f"Parsed {len(long_df)} monthly observations across {long_df['dr...`
> **Type:** Prints output to console

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `print("Creating features...")`
> **Type:** Prints output to console

### Line  98
> **Code:** `feat_df = create_features(long_df)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `print(f"Created {len(feat_df)} training rows with features")`
> **Type:** Prints output to console

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `args.output.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `feat_df.to_csv(args.output, index=False)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `print(f"Saved to {args.output}")`
> **Type:** Prints output to console

### Line 104
> **Code:** `print(f"Target stats: mean={feat_df['target'].mean():.1f}, median={fea...`
> **Type:** Prints output to console

### Line 105
> **Code:** `print(f"Features: {list(feat_df.columns)}")`
> **Type:** Prints output to console

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 109
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 109
- **Code lines:** 77
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 29

---
*Documentation generated for: mlops-project-documentation*
*File: generate_demand_data.py*
---

# mlops-project-documentation: generate_synthetic_data.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/scripts/generate_synthetic_data.py`
- **Total lines:** 113
- **File size:** 4402 bytes

## Line Type Summary
- **Code:** 91
- **Comment:** 0
- **Empty:** 19
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Generate a realistic synthetic telecom churn dataset (Telco-Churn-l...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Writes data/raw/dataset.csv (and a copy under data/external/ so the`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `ingestion stage has a realistic upstream source). Deterministic seed s...`
> **Type:** Code statement

### Line   8
> **Code:** `dataset is reproducible.`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `import random`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `N_ROWS_DEFAULT = 7000`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `SEED = 42`
> **Type:** Assignment/comparison

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `CONTRACT_TYPES = ["Month-to-month", "One year", "Two year"]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `INTERNET_SERVICES = ["DSL", "Fiber optic", "No"]`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `PAYMENT_METHODS = [`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `"Electronic check",`
> **Type:** Code statement

### Line  27
> **Code:** `"Mailed check",`
> **Type:** Code statement

### Line  28
> **Code:** `"Bank transfer (automatic)",`
> **Type:** Code statement

### Line  29
> **Code:** `"Credit card (automatic)",`
> **Type:** Code statement

### Line  30
> **Code:** `]`
> **Type:** Code statement

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `def _pick(rng: random.Random, options: list[str], weights: list[float]...`
> **Type:** Function definition

### Line  34
> **Code:** `if weights is None:`
> **Type:** Conditional statement

### Line  35
> **Code:** `return rng.choice(options)`
> **Type:** Returns a value from a function

### Line  36
> **Code:** `return rng.choices(options, weights=weights, k=1)[0]`
> **Type:** Returns a value from a function

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def _churn_probability(row: dict) -> float:`
> **Type:** Function definition

### Line  40
> **Code:** `p = 0.12`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `if row["Contract"] == "Month-to-month":`
> **Type:** Conditional statement

### Line  42
> **Code:** `p += 0.28`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `elif row["Contract"] == "One year":`
> **Type:** Else-if branch

### Line  44
> **Code:** `p += 0.06`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `if row["InternetService"] == "Fiber optic":`
> **Type:** Conditional statement

### Line  46
> **Code:** `p += 0.10`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `p -= min(0.30, row["Tenure"] * 0.006)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `if row["PaymentMethod"] == "Electronic check":`
> **Type:** Conditional statement

### Line  49
> **Code:** `p += 0.08`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `if row["TechSupport"] == "No":`
> **Type:** Conditional statement

### Line  51
> **Code:** `p += 0.05`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `if row["OnlineSecurity"] == "No" and row["InternetService"] != "No":`
> **Type:** Conditional statement

### Line  53
> **Code:** `p += 0.04`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `return float(np.clip(p, 0.01, 0.95))`
> **Type:** Returns a value from a function

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def generate(n_rows: int = N_ROWS_DEFAULT, seed: int = SEED) -> pd.Dat...`
> **Type:** Function definition

### Line  58
> **Code:** `rng = random.Random(seed)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `base = np.random.default_rng(seed)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `rows: list[dict] = []`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `for _ in range(n_rows):`
> **Type:** For loop

### Line  63
> **Code:** `tenure = int(rng.randint(1, 72))`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `monthly = float(round(rng.uniform(19.0, 118.0), 2))`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `row = {`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `"CustomerID": f"{rng.randrange(1000, 9999)}-{rng.randrange(10000, 9999...`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `"Gender": _pick(rng, ["Male", "Female"]),`
> **Type:** Data structure operation

### Line  68
> **Code:** `"SeniorCitizen": rng.randint(0, 1),`
> **Type:** Logical operation

### Line  69
> **Code:** `"Partner": _pick(rng, ["Yes", "No"]),`
> **Type:** Data structure operation

### Line  70
> **Code:** `"Dependents": _pick(rng, ["Yes", "No"], weights=[0.3, 0.7]),`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `"Tenure": tenure,`
> **Type:** Code statement

### Line  72
> **Code:** `"PhoneService": _pick(rng, ["Yes", "No"], weights=[0.9, 0.1]),`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `"MultipleLines": _pick(rng, ["Yes", "No", "No phone service"]),`
> **Type:** Data structure operation

### Line  74
> **Code:** `"InternetService": _pick(rng, INTERNET_SERVICES, weights=[0.44, 0.42, ...`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `"OnlineSecurity": _pick(rng, ["Yes", "No", "No internet service"]),`
> **Type:** Data structure operation

### Line  76
> **Code:** `"OnlineBackup": _pick(rng, ["Yes", "No", "No internet service"]),`
> **Type:** Data structure operation

### Line  77
> **Code:** `"DeviceProtection": _pick(rng, ["Yes", "No", "No internet service"]),`
> **Type:** Data structure operation

### Line  78
> **Code:** `"TechSupport": _pick(rng, ["Yes", "No", "No internet service"]),`
> **Type:** Logical operation

### Line  79
> **Code:** `"StreamingTV": _pick(rng, ["Yes", "No", "No internet service"]),`
> **Type:** Data structure operation

### Line  80
> **Code:** `"StreamingMovies": _pick(rng, ["Yes", "No", "No internet service"]),`
> **Type:** Data structure operation

### Line  81
> **Code:** `"Contract": _pick(rng, CONTRACT_TYPES, weights=[0.55, 0.25, 0.20]),`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `"PaperlessBilling": _pick(rng, ["Yes", "No"]),`
> **Type:** Data structure operation

### Line  83
> **Code:** `"PaymentMethod": _pick(rng, PAYMENT_METHODS, weights=[0.33, 0.23, 0.22...`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `"MonthlyCharges": monthly,`
> **Type:** Code statement

### Line  85
> **Code:** `}`
> **Type:** Code statement

### Line  86
> **Code:** `row["TotalCharges"] = float(round(monthly * tenure * (1 + rng.uniform(...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `row["Churn"] = "Yes" if base.random() < _churn_probability(row) else "...`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `rows.append(row)`
> **Type:** Function call

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `df = pd.DataFrame(rows)`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  96
> **Code:** `parser = argparse.ArgumentParser(description="Generate synthetic churn...`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `parser.add_argument("--n-rows", type=int, default=N_ROWS_DEFAULT)`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `parser.add_argument("--seed", type=int, default=SEED)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `parser.add_argument("--output", type=Path, default=Path("data/raw/data...`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `parser.add_argument("--external", type=Path, default=Path("data/extern...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `df = generate(args.n_rows, args.seed)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `args.output.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `args.external.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `df.to_csv(args.output, index=False)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `df.to_csv(args.external, index=False)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `print(f"Generated {len(df)} rows x {len(df.columns)} columns -> {args....`
> **Type:** Prints output to console

### Line 109
> **Code:** `print(f"Churn rate: {float((df['Churn'] == 'Yes').mean()):.3f}")`
> **Type:** Prints output to console

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 113
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 113
- **Code lines:** 91
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 19

---
*Documentation generated for: mlops-project-documentation*
*File: generate_synthetic_data.py*
---

# mlops-project-documentation: test_pipeline_end_to_end.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/integration/test_pipeline_end_to_end.py`
- **Total lines:** 312
- **File size:** 14493 bytes

## Line Type Summary
- **Code:** 246
- **Comment:** 25
- **Empty:** 38
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""End-to-end integration test for the MLOps pipeline.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Tests the full pipeline: preprocessing -> features -> training -> eval...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `using SQLite MLflow backend and monkeypatched environment (no external...`
> **Type:** Logical operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import json`
> **Type:** Imports a module

### Line  11
> **Code:** `import os`
> **Type:** Imports a module

### Line  12
> **Code:** `import sys`
> **Type:** Imports a module

### Line  13
> **Code:** `import tempfile`
> **Type:** Imports a module

### Line  14
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from unittest.mock import patch, MagicMock`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  18
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[3]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  22
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `# Import all pipeline modules`
> **Type:** Comment: Import all pipeline modules

### Line  25
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from src.features.build_features import build_features, FeatureTransfo...`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from src.models.train import train_model`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.models.evaluate import evaluate`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** `from src.models.promote import promote_candidate, current_production`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `class TestPipelineEndToEnd:`
> **Type:** Class definition

### Line  33
> **Code:** `"""End-to-end pipeline test with minimal data and fast model."""`
> **Type:** Arithmetic operation

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `@pytest.fixture(autouse=True)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `def setup_env(self, tmp_path, monkeypatch):`
> **Type:** Function definition

### Line  37
> **Code:** `"""Set up isolated environment for each test."""`
> **Type:** Logical operation

### Line  38
> **Code:** `# Use temporary directories`
> **Type:** Comment: Use temporary directories

### Line  39
> **Code:** `self.tmp_path = tmp_path`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `self.data_dir = tmp_path / "data"`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `self.data_dir.mkdir()`
> **Type:** Function call

### Line  42
> **Code:** `self.models_dir = tmp_path / "models"`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `self.models_dir.mkdir()`
> **Type:** Function call

### Line  44
> **Code:** `self.mlruns_dir = tmp_path / "mlruns"`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `self.mlruns_dir.mkdir()`
> **Type:** Function call

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `# Monkeypatch environment`
> **Type:** Comment: Monkeypatch environment

### Line  48
> **Code:** `monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{self.mlruns_dir...`
> **Type:** Arithmetic operation

### Line  49
> **Code:** `monkeypatch.setenv("MLFLOW_MODEL_NAME", "test_churn_model")`
> **Type:** Function call

### Line  50
> **Code:** `monkeypatch.setenv("DRIFT_THRESHOLD", "0.3")`
> **Type:** Function call

### Line  51
> **Code:** `monkeypatch.setenv("DRIFT_REFERENCE", str(self.data_dir / "monitoring"...`
> **Type:** Arithmetic operation

### Line  52
> **Code:** `monkeypatch.setenv("DRIFT_CURRENT", str(self.data_dir / "monitoring" /...`
> **Type:** Arithmetic operation

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `# Create minimal sample data`
> **Type:** Comment: Create minimal sample data

### Line  55
> **Code:** `self.sample_csv = self.data_dir / "raw" / "sample.csv"`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `self.sample_csv.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `self._create_sample_data()`
> **Type:** Function call

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `def _create_sample_data(self):`
> **Type:** Function definition

### Line  60
> **Code:** `"""Create a small sample dataset for fast testing."""`
> **Type:** Logical operation

### Line  61
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `"CustomerID": [f"C{i:04d}" for i in range(100)],`
> **Type:** Logical operation

### Line  63
> **Code:** `"Gender": ["Male", "Female"] * 50,`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `"SeniorCitizen": [0, 1] * 50,`
> **Type:** Arithmetic operation

### Line  65
> **Code:** `"Partner": ["Yes", "No"] * 50,`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `"Dependents": ["No", "Yes"] * 50,`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `"Tenure": list(range(1, 101)),`
> **Type:** Code statement

### Line  68
> **Code:** `"PhoneService": ["Yes"] * 100,`
> **Type:** Arithmetic operation

### Line  69
> **Code:** `"MultipleLines": ["No", "Yes", "No phone service"] * 33 + ["No"],`
> **Type:** Arithmetic operation

### Line  70
> **Code:** `"InternetService": ["DSL", "Fiber optic", "No"] * 33 + ["DSL"],`
> **Type:** Arithmetic operation

### Line  71
> **Code:** `"OnlineSecurity": ["Yes", "No", "No internet service"] * 33 + ["Yes"],`
> **Type:** Arithmetic operation

### Line  72
> **Code:** `"OnlineBackup": ["Yes", "No", "No internet service"] * 33 + ["No"],`
> **Type:** Arithmetic operation

### Line  73
> **Code:** `"DeviceProtection": ["Yes", "No", "No internet service"] * 33 + ["Yes"...`
> **Type:** Arithmetic operation

### Line  74
> **Code:** `"TechSupport": ["Yes", "No", "No internet service"] * 33 + ["No"],`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `"StreamingTV": ["Yes", "No", "No internet service"] * 33 + ["Yes"],`
> **Type:** Arithmetic operation

### Line  76
> **Code:** `"StreamingMovies": ["Yes", "No", "No internet service"] * 33 + ["No"],`
> **Type:** Arithmetic operation

### Line  77
> **Code:** `"Contract": ["Month-to-month", "One year", "Two year"] * 33 + ["Month-...`
> **Type:** Arithmetic operation

### Line  78
> **Code:** `"PaperlessBilling": ["Yes", "No"] * 50,`
> **Type:** Arithmetic operation

### Line  79
> **Code:** `"PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (...`
> **Type:** Arithmetic operation

### Line  80
> **Code:** `"MonthlyCharges": [float(20 + i * 0.5) for i in range(100)],`
> **Type:** Arithmetic operation

### Line  81
> **Code:** `"TotalCharges": [float(100 + i * 10) for i in range(100)],`
> **Type:** Arithmetic operation

### Line  82
> **Code:** `"Churn": ["No", "Yes"] * 50,`
> **Type:** Arithmetic operation

### Line  83
> **Code:** `})`
> **Type:** Code statement

### Line  84
> **Code:** `df.to_csv(self.sample_csv, index=False)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def _override_default_paths(self, monkeypatch):`
> **Type:** Function definition

### Line  87
> **Code:** `"""Override default paths in modules to use temp directories."""`
> **Type:** Logical operation

### Line  88
> **Code:** `# Preprocessing`
> **Type:** Comment: Preprocessing

### Line  89
> **Code:** `monkeypatch.setattr("src.data.preprocessing.DROP_COLUMNS", ["CustomerI...`
> **Type:** Function call

### Line  90
> **Code:** `monkeypatch.setattr("src.data.preprocessing.NUMERIC_COLUMNS", [`
> **Type:** Code statement

### Line  91
> **Code:** `"Tenure", "MonthlyCharges", "TotalCharges"`
> **Type:** Code statement

### Line  92
> **Code:** `])`
> **Type:** Code statement

### Line  93
> **Code:** `monkeypatch.setattr("src.data.preprocessing.CATEGORICAL_COLUMNS", [`
> **Type:** Code statement

### Line  94
> **Code:** `"Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",`
> **Type:** Logical operation

### Line  95
> **Code:** `"MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",`
> **Type:** Code statement

### Line  96
> **Code:** `"DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",`
> **Type:** Logical operation

### Line  97
> **Code:** `"Contract", "PaperlessBilling", "PaymentMethod"`
> **Type:** Code statement

### Line  98
> **Code:** `])`
> **Type:** Code statement

### Line  99
> **Code:** `monkeypatch.setattr("src.data.preprocessing.TARGET_COLUMN", "Churn")`
> **Type:** Function call

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `# Features`
> **Type:** Comment: Features

### Line 102
> **Code:** `from src.features.build_features import (`
> **Type:** Imports specific names from a module

### Line 103
> **Code:** `NUMERIC_FEATURES, CATEGORICAL_FEATURES, ENGINEERED_FEATURES,`
> **Type:** Code statement

### Line 104
> **Code:** `FEATURE_ORDER, TARGET_FEATURE, TARGET_COLUMN, SERVICE_COLUMNS`
> **Type:** Code statement

### Line 105
> **Code:** `)`
> **Type:** Code statement

### Line 106
> **Code:** `monkeypatch.setattr("src.features.build_features.NUMERIC_FEATURES", [`
> **Type:** Code statement

### Line 107
> **Code:** `"Tenure", "MonthlyCharges", "TotalCharges"`
> **Type:** Code statement

### Line 108
> **Code:** `])`
> **Type:** Code statement

### Line 109
> **Code:** `monkeypatch.setattr("src.features.build_features.CATEGORICAL_FEATURES"...`
> **Type:** Code statement

### Line 110
> **Code:** `"Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",`
> **Type:** Logical operation

### Line 111
> **Code:** `"MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",`
> **Type:** Code statement

### Line 112
> **Code:** `"DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",`
> **Type:** Logical operation

### Line 113
> **Code:** `"Contract", "PaperlessBilling", "PaymentMethod"`
> **Type:** Code statement

### Line 114
> **Code:** `])`
> **Type:** Code statement

### Line 115
> **Code:** `monkeypatch.setattr("src.features.build_features.ENGINEERED_FEATURES",...`
> **Type:** Code statement

### Line 116
> **Code:** `"charges_per_tenure", "tenure_years", "num_services"`
> **Type:** Code statement

### Line 117
> **Code:** `])`
> **Type:** Code statement

### Line 118
> **Code:** `monkeypatch.setattr("src.features.build_features.FEATURE_ORDER", [`
> **Type:** Code statement

### Line 119
> **Code:** `"Tenure", "MonthlyCharges", "TotalCharges",`
> **Type:** Code statement

### Line 120
> **Code:** `"Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",`
> **Type:** Logical operation

### Line 121
> **Code:** `"MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",`
> **Type:** Code statement

### Line 122
> **Code:** `"DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",`
> **Type:** Logical operation

### Line 123
> **Code:** `"Contract", "PaperlessBilling", "PaymentMethod",`
> **Type:** Code statement

### Line 124
> **Code:** `"charges_per_tenure", "tenure_years", "num_services"`
> **Type:** Code statement

### Line 125
> **Code:** `])`
> **Type:** Code statement

### Line 126
> **Code:** `monkeypatch.setattr("src.features.build_features.TARGET_FEATURE", "tar...`
> **Type:** Function call

### Line 127
> **Code:** `monkeypatch.setattr("src.features.build_features.TARGET_COLUMN", "Chur...`
> **Type:** Function call

### Line 128
> **Code:** `monkeypatch.setattr("src.models.train.TARGET_FEATURE", "target")`
> **Type:** Function call

### Line 129
> **Code:** `monkeypatch.setattr("src.models.evaluate.TARGET_FEATURE", "target")`
> **Type:** Function call

### Line 130
> **Code:** `monkeypatch.setattr("src.features.build_features.SERVICE_COLUMNS", [`
> **Type:** Code statement

### Line 131
> **Code:** `"OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",`
> **Type:** Logical operation

### Line 132
> **Code:** `"StreamingTV", "StreamingMovies"`
> **Type:** Code statement

### Line 133
> **Code:** `])`
> **Type:** Code statement

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** `# Train`
> **Type:** Comment: Train

### Line 136
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_DATA", self.data_dir / "...`
> **Type:** Arithmetic operation

### Line 137
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_CONFIG", self.data_dir /...`
> **Type:** Arithmetic operation

### Line 138
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_MODEL_OUTPUT", self.mode...`
> **Type:** Arithmetic operation

### Line 139
> **Code:** `monkeypatch.setattr("src.models.train.DEFAULT_REFERENCE", self.data_di...`
> **Type:** Arithmetic operation

### Line 140
> **Code:** `monkeypatch.setattr("src.models.train.MODEL_NAME", "test_churn_model")`
> **Type:** Function call

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `# Evaluate`
> **Type:** Comment: Evaluate

### Line 143
> **Code:** `monkeypatch.setattr("src.models.evaluate.DEFAULT_DATA", self.data_dir ...`
> **Type:** Arithmetic operation

### Line 144
> **Code:** `monkeypatch.setattr("src.models.evaluate.DEFAULT_CONFIG", self.data_di...`
> **Type:** Arithmetic operation

### Line 145
> **Code:** `monkeypatch.setattr("src.models.evaluate.DEFAULT_LOCAL_MODEL", self.mo...`
> **Type:** Arithmetic operation

### Line 146
> **Code:** `monkeypatch.setattr("src.models.evaluate.EVALUATION_DIR", self.models_...`
> **Type:** Arithmetic operation

### Line 147
> **Code:** `monkeypatch.setattr("src.models.evaluate.LATEST_REPORT", self.models_d...`
> **Type:** Arithmetic operation

### Line 148
> **Code:** ``
> **Type:** Empty line

### Line 149
> **Code:** `# Promote`
> **Type:** Comment: Promote

### Line 150
> **Code:** `monkeypatch.setattr("src.models.promote.LATEST_REPORT", self.models_di...`
> **Type:** Arithmetic operation

### Line 151
> **Code:** `monkeypatch.setattr("src.models.promote.PRODUCTION_REPORT", self.model...`
> **Type:** Arithmetic operation

### Line 152
> **Code:** ``
> **Type:** Empty line

### Line 153
> **Code:** `def test_full_pipeline(self, monkeypatch):`
> **Type:** Function definition

### Line 154
> **Code:** `"""Run the complete pipeline end-to-end."""`
> **Type:** Arithmetic operation

### Line 155
> **Code:** `self._override_default_paths(monkeypatch)`
> **Type:** Function call

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `# Step 1: Preprocessing`
> **Type:** Comment: Step 1: Preprocessing

### Line 158
> **Code:** `processed_path = self.data_dir / "processed" / "clean.csv"`
> **Type:** Assignment/comparison

### Line 159
> **Code:** `processed_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `processed_df = preprocess(self.sample_csv, processed_path)`
> **Type:** Assignment/comparison

### Line 161
> **Code:** `assert processed_path.exists()`
> **Type:** Enforces a condition

### Line 162
> **Code:** `assert len(processed_df) > 0`
> **Type:** Enforces a condition

### Line 163
> **Code:** `assert "CustomerID" not in processed_df.columns`
> **Type:** Enforces a condition

### Line 164
> **Code:** `assert "Churn" in processed_df.columns`
> **Type:** Enforces a condition

### Line 165
> **Code:** ``
> **Type:** Empty line

### Line 166
> **Code:** `# Step 2: Feature Engineering`
> **Type:** Comment: Step 2: Feature Engineering

### Line 167
> **Code:** `features_path = self.data_dir / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line 168
> **Code:** `config_path = self.data_dir / "features" / "features_config.json"`
> **Type:** Assignment/comparison

### Line 169
> **Code:** `features_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 170
> **Code:** `features_df = build_features(processed_path, features_path, config_pat...`
> **Type:** Assignment/comparison

### Line 171
> **Code:** `assert features_path.exists()`
> **Type:** Enforces a condition

### Line 172
> **Code:** `assert config_path.exists()`
> **Type:** Enforces a condition

### Line 173
> **Code:** `assert len(features_df) == len(processed_df)`
> **Type:** Enforces a condition

### Line 174
> **Code:** `assert "target" in features_df.columns`
> **Type:** Enforces a condition

### Line 175
> **Code:** ``
> **Type:** Empty line

### Line 176
> **Code:** `# Step 3: Training (with tiny model for speed)`
> **Type:** Comment: Step 3: Training (with tiny model for speed)

### Line 177
> **Code:** `train_params = {`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `"n_estimators": 10,  # Very small for fast testing`
> **Type:** Logical operation

### Line 179
> **Code:** `"max_depth": 3,`
> **Type:** Code statement

### Line 180
> **Code:** `"min_samples_leaf": 2,`
> **Type:** Code statement

### Line 181
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line 182
> **Code:** `"class_weight": "balanced",`
> **Type:** Code statement

### Line 183
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line 184
> **Code:** `}`
> **Type:** Code statement

### Line 185
> **Code:** `train_result = train_model(`
> **Type:** Assignment/comparison

### Line 186
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 187
> **Code:** `config_path=config_path,`
> **Type:** Assignment/comparison

### Line 188
> **Code:** `model_output=self.models_dir / "model.pkl",`
> **Type:** Assignment/comparison

### Line 189
> **Code:** `model_name="test_churn_model",`
> **Type:** Assignment/comparison

### Line 190
> **Code:** `params=train_params,`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `)`
> **Type:** Code statement

### Line 192
> **Code:** `assert train_result["run_id"] is not None`
> **Type:** Enforces a condition

### Line 193
> **Code:** `assert (self.models_dir / "model.pkl").exists()`
> **Type:** Enforces a condition

### Line 194
> **Code:** `assert (self.data_dir / "monitoring" / "reference.csv").exists()`
> **Type:** Enforces a condition

### Line 195
> **Code:** ``
> **Type:** Empty line

### Line 196
> **Code:** `# Step 4: Evaluation`
> **Type:** Comment: Step 4: Evaluation

### Line 197
> **Code:** `eval_report = evaluate(`
> **Type:** Assignment/comparison

### Line 198
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 199
> **Code:** `model_uri=None,`
> **Type:** Assignment/comparison

### Line 200
> **Code:** `run_id=train_result["run_id"],`
> **Type:** Assignment/comparison

### Line 201
> **Code:** `)`
> **Type:** Code statement

### Line 202
> **Code:** `assert eval_report["gates_passed"] is not None`
> **Type:** Enforces a condition

### Line 203
> **Code:** `assert "metrics" in eval_report`
> **Type:** Enforces a condition

### Line 204
> **Code:** `assert (self.models_dir / "evaluation" / "latest_report.json").exists(...`
> **Type:** Enforces a condition

### Line 205
> **Code:** ``
> **Type:** Empty line

### Line 206
> **Code:** `# Step 5: Promotion`
> **Type:** Comment: Step 5: Promotion

### Line 207
> **Code:** `# First, need to transition model to Staging (train does this)`
> **Type:** Comment: First, need to transition model to Staging (train does this)

### Line 208
> **Code:** `# Then promote`
> **Type:** Comment: Then promote

### Line 209
> **Code:** `# Note: In this test, the model is already in Staging from train.py`
> **Type:** Comment: Note: In this test, the model is already in Staging from train.py

### Line 210
> **Code:** `# But we need to check if it's there`
> **Type:** Comment: But we need to check if it's there

### Line 211
> **Code:** `production_report = promote_candidate(model_name="test_churn_model", f...`
> **Type:** Assignment/comparison

### Line 212
> **Code:** `assert production_report["model_name"] == "test_churn_model"`
> **Type:** Enforces a condition

### Line 213
> **Code:** `assert production_report["version"] >= 1`
> **Type:** Enforces a condition

### Line 214
> **Code:** `assert (self.models_dir / "evaluation" / "production_report.json").exi...`
> **Type:** Enforces a condition

### Line 215
> **Code:** ``
> **Type:** Empty line

### Line 216
> **Code:** `# Verify production model is accessible`
> **Type:** Comment: Verify production model is accessible

### Line 217
> **Code:** `current = current_production(model_name="test_churn_model")`
> **Type:** Assignment/comparison

### Line 218
> **Code:** `assert current is not None`
> **Type:** Enforces a condition

### Line 219
> **Code:** `assert current["version"] == production_report["version"]`
> **Type:** Enforces a condition

### Line 220
> **Code:** ``
> **Type:** Empty line

### Line 221
> **Code:** `def test_pipeline_with_evaluation_failure(self, monkeypatch):`
> **Type:** Function definition

### Line 222
> **Code:** `"""Test pipeline when evaluation gates fail."""`
> **Type:** Code statement

### Line 223
> **Code:** `self._override_default_paths(monkeypatch)`
> **Type:** Function call

### Line 224
> **Code:** ``
> **Type:** Empty line

### Line 225
> **Code:** `# Run through training`
> **Type:** Comment: Run through training

### Line 226
> **Code:** `processed_path = self.data_dir / "processed" / "clean.csv"`
> **Type:** Assignment/comparison

### Line 227
> **Code:** `processed_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 228
> **Code:** `processed_df = preprocess(self.sample_csv, processed_path)`
> **Type:** Assignment/comparison

### Line 229
> **Code:** ``
> **Type:** Empty line

### Line 230
> **Code:** `features_path = self.data_dir / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line 231
> **Code:** `config_path = self.data_dir / "features" / "features_config.json"`
> **Type:** Assignment/comparison

### Line 232
> **Code:** `features_path.parent.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 233
> **Code:** `features_df = build_features(processed_path, features_path, config_pat...`
> **Type:** Assignment/comparison

### Line 234
> **Code:** ``
> **Type:** Empty line

### Line 235
> **Code:** `train_params = {`
> **Type:** Assignment/comparison

### Line 236
> **Code:** `"n_estimators": 10,`
> **Type:** Logical operation

### Line 237
> **Code:** `"max_depth": 3,`
> **Type:** Code statement

### Line 238
> **Code:** `"min_samples_leaf": 2,`
> **Type:** Code statement

### Line 239
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line 240
> **Code:** `"class_weight": "balanced",`
> **Type:** Code statement

### Line 241
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line 242
> **Code:** `}`
> **Type:** Code statement

### Line 243
> **Code:** `train_result = train_model(`
> **Type:** Assignment/comparison

### Line 244
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 245
> **Code:** `config_path=config_path,`
> **Type:** Assignment/comparison

### Line 246
> **Code:** `model_output=self.models_dir / "model.pkl",`
> **Type:** Assignment/comparison

### Line 247
> **Code:** `model_name="test_churn_model",`
> **Type:** Assignment/comparison

### Line 248
> **Code:** `params=train_params,`
> **Type:** Assignment/comparison

### Line 249
> **Code:** `)`
> **Type:** Code statement

### Line 250
> **Code:** ``
> **Type:** Empty line

### Line 251
> **Code:** `# Evaluate with impossible thresholds`
> **Type:** Comment: Evaluate with impossible thresholds

### Line 252
> **Code:** `eval_report = evaluate(`
> **Type:** Assignment/comparison

### Line 253
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 254
> **Code:** `run_id=train_result["run_id"],`
> **Type:** Assignment/comparison

### Line 255
> **Code:** `thresholds={"min_f1": 0.99, "min_accuracy": 0.99, "min_roc_auc": 0.99}...`
> **Type:** Assignment/comparison

### Line 256
> **Code:** `)`
> **Type:** Code statement

### Line 257
> **Code:** `assert eval_report["gates_passed"] is False`
> **Type:** Enforces a condition

### Line 258
> **Code:** ``
> **Type:** Empty line

### Line 259
> **Code:** `# Promotion should fail without --force`
> **Type:** Comment: Promotion should fail without --force

### Line 260
> **Code:** `with pytest.raises(RuntimeError, match="did not pass evaluation gates"...`
> **Type:** Context manager

### Line 261
> **Code:** `promote_candidate(model_name="test_churn_model", force=False)`
> **Type:** Assignment/comparison

### Line 262
> **Code:** ``
> **Type:** Empty line

### Line 263
> **Code:** `# But should succeed with --force`
> **Type:** Comment: But should succeed with --force

### Line 264
> **Code:** `production_report = promote_candidate(model_name="test_churn_model", f...`
> **Type:** Assignment/comparison

### Line 265
> **Code:** `assert production_report is not None`
> **Type:** Enforces a condition

### Line 266
> **Code:** ``
> **Type:** Empty line

### Line 267
> **Code:** `def test_pipeline_reproducibility(self, monkeypatch):`
> **Type:** Function definition

### Line 268
> **Code:** `"""Test that running pipeline twice with same seed produces same resul...`
> **Type:** Code statement

### Line 269
> **Code:** `self._override_default_paths(monkeypatch)`
> **Type:** Function call

### Line 270
> **Code:** ``
> **Type:** Empty line

### Line 271
> **Code:** `def run_once():`
> **Type:** Function definition

### Line 272
> **Code:** `processed_path = self.data_dir / "processed" / "clean.csv"`
> **Type:** Assignment/comparison

### Line 273
> **Code:** `processed_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 274
> **Code:** `processed_df = preprocess(self.sample_csv, processed_path)`
> **Type:** Assignment/comparison

### Line 275
> **Code:** ``
> **Type:** Empty line

### Line 276
> **Code:** `features_path = self.data_dir / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line 277
> **Code:** `config_path = self.data_dir / "features" / "features_config.json"`
> **Type:** Assignment/comparison

### Line 278
> **Code:** `features_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 279
> **Code:** `build_features(processed_path, features_path, config_path)`
> **Type:** Function call

### Line 280
> **Code:** ``
> **Type:** Empty line

### Line 281
> **Code:** `train_params = {`
> **Type:** Assignment/comparison

### Line 282
> **Code:** `"n_estimators": 10,`
> **Type:** Logical operation

### Line 283
> **Code:** `"max_depth": 3,`
> **Type:** Code statement

### Line 284
> **Code:** `"min_samples_leaf": 2,`
> **Type:** Code statement

### Line 285
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line 286
> **Code:** `"class_weight": "balanced",`
> **Type:** Code statement

### Line 287
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line 288
> **Code:** `}`
> **Type:** Code statement

### Line 289
> **Code:** `train_result = train_model(`
> **Type:** Assignment/comparison

### Line 290
> **Code:** `data_path=features_path,`
> **Type:** Assignment/comparison

### Line 291
> **Code:** `config_path=config_path,`
> **Type:** Assignment/comparison

### Line 292
> **Code:** `model_output=self.models_dir / "model.pkl",`
> **Type:** Assignment/comparison

### Line 293
> **Code:** `model_name="test_churn_model",`
> **Type:** Assignment/comparison

### Line 294
> **Code:** `params=train_params,`
> **Type:** Assignment/comparison

### Line 295
> **Code:** `)`
> **Type:** Code statement

### Line 296
> **Code:** `return train_result["metrics"]`
> **Type:** Returns a value from a function

### Line 297
> **Code:** ``
> **Type:** Empty line

### Line 298
> **Code:** `metrics1 = run_once()`
> **Type:** Assignment/comparison

### Line 299
> **Code:** `# Clear mlruns for second run`
> **Type:** Comment: Clear mlruns for second run

### Line 300
> **Code:** `import shutil`
> **Type:** Imports a module

### Line 301
> **Code:** `if (self.mlruns_dir / "mlflow.db").exists():`
> **Type:** Conditional statement

### Line 302
> **Code:** `(self.mlruns_dir / "mlflow.db").unlink()`
> **Type:** Arithmetic operation

### Line 303
> **Code:** `metrics2 = run_once()`
> **Type:** Assignment/comparison

### Line 304
> **Code:** ``
> **Type:** Empty line

### Line 305
> **Code:** `# With same random_state, metrics should be identical`
> **Type:** Comment: With same random_state, metrics should be identical

### Line 306
> **Code:** `assert metrics1["f1"] == metrics2["f1"]`
> **Type:** Enforces a condition

### Line 307
> **Code:** `assert metrics1["accuracy"] == metrics2["accuracy"]`
> **Type:** Enforces a condition

### Line 308
> **Code:** `assert metrics1["roc_auc"] == metrics2["roc_auc"]`
> **Type:** Enforces a condition

### Line 309
> **Code:** ``
> **Type:** Empty line

### Line 310
> **Code:** ``
> **Type:** Empty line

### Line 311
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 312
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 312
- **Code lines:** 246
- **Comments:** 25
- **TODO items:** 3
- **Empty lines:** 38

---
*Documentation generated for: mlops-project-documentation*
*File: test_pipeline_end_to_end.py*
---

# mlops-project-documentation: test_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/unit/test_features.py`
- **Total lines:** 267
- **File size:** 10486 bytes

## Line Type Summary
- **Code:** 213
- **Comment:** 8
- **Empty:** 43
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for src.features.build_features module."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   8
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from src.features.build_features import (`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `FeatureTransformer,`
> **Type:** Logical operation

### Line  19
> **Code:** `build_features,`
> **Type:** Code statement

### Line  20
> **Code:** `NUMERIC_FEATURES,`
> **Type:** Code statement

### Line  21
> **Code:** `CATEGORICAL_FEATURES,`
> **Type:** Code statement

### Line  22
> **Code:** `ENGINEERED_FEATURES,`
> **Type:** Code statement

### Line  23
> **Code:** `FEATURE_ORDER,`
> **Type:** Code statement

### Line  24
> **Code:** `TARGET_FEATURE,`
> **Type:** Code statement

### Line  25
> **Code:** `TARGET_COLUMN,`
> **Type:** Code statement

### Line  26
> **Code:** `SERVICE_COLUMNS,`
> **Type:** Code statement

### Line  27
> **Code:** `)`
> **Type:** Code statement

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `class TestFeatureTransformer:`
> **Type:** Class definition

### Line  31
> **Code:** `"""Test FeatureTransformer fit/transform correctness."""`
> **Type:** Arithmetic operation

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `def _sample_df(self, n=100):`
> **Type:** Function definition

### Line  34
> **Code:** `"""Create sample dataframe with expected columns."""`
> **Type:** Code statement

### Line  35
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  36
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  37
> **Code:** `return pd.DataFrame({`
> **Type:** Returns a value from a function

### Line  38
> **Code:** `"Gender": np.random.choice(["Male", "Female"], n),`
> **Type:** Logical operation

### Line  39
> **Code:** `"SeniorCitizen": np.random.choice([0, 1], n),`
> **Type:** Logical operation

### Line  40
> **Code:** `"Partner": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  41
> **Code:** `"Dependents": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  42
> **Code:** `"Tenure": np.random.randint(0, 72, n),`
> **Type:** Logical operation

### Line  43
> **Code:** `"PhoneService": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  44
> **Code:** `"MultipleLines": np.random.choice(["Yes", "No", "No phone service"], n...`
> **Type:** Logical operation

### Line  45
> **Code:** `"InternetService": np.random.choice(["DSL", "Fiber optic", "No"], n),`
> **Type:** Logical operation

### Line  46
> **Code:** `"OnlineSecurity": np.random.choice(["Yes", "No", "No internet service"...`
> **Type:** Logical operation

### Line  47
> **Code:** `"OnlineBackup": np.random.choice(["Yes", "No", "No internet service"],...`
> **Type:** Logical operation

### Line  48
> **Code:** `"DeviceProtection": np.random.choice(["Yes", "No", "No internet servic...`
> **Type:** Logical operation

### Line  49
> **Code:** `"TechSupport": np.random.choice(["Yes", "No", "No internet service"], ...`
> **Type:** Logical operation

### Line  50
> **Code:** `"StreamingTV": np.random.choice(["Yes", "No", "No internet service"], ...`
> **Type:** Logical operation

### Line  51
> **Code:** `"StreamingMovies": np.random.choice(["Yes", "No", "No internet service...`
> **Type:** Logical operation

### Line  52
> **Code:** `"Contract": np.random.choice(["Month-to-month", "One year", "Two year"...`
> **Type:** Arithmetic operation

### Line  53
> **Code:** `"PaperlessBilling": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  54
> **Code:** `"PaymentMethod": np.random.choice(["Electronic check", "Mailed check",...`
> **Type:** Logical operation

### Line  55
> **Code:** `"MonthlyCharges": np.random.uniform(20, 120, n),`
> **Type:** Logical operation

### Line  56
> **Code:** `"TotalCharges": np.random.uniform(100, 8000, n),`
> **Type:** Logical operation

### Line  57
> **Code:** `"Churn": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  58
> **Code:** `})`
> **Type:** Code statement

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `def test_fit_transform_shape(self):`
> **Type:** Function definition

### Line  61
> **Code:** `"""fit_transform should return expected feature columns."""`
> **Type:** Logical operation

### Line  62
> **Code:** `df = self._sample_df(50)`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `assert list(features.columns) == FEATURE_ORDER`
> **Type:** Enforces a condition

### Line  67
> **Code:** `assert len(features) == 50`
> **Type:** Enforces a condition

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def test_numeric_features_scaled(self):`
> **Type:** Function definition

### Line  70
> **Code:** `"""Numeric features should be present in output."""`
> **Type:** Code statement

### Line  71
> **Code:** `df = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `for col in NUMERIC_FEATURES:`
> **Type:** For loop

### Line  76
> **Code:** `assert col in features.columns`
> **Type:** Enforces a condition

### Line  77
> **Code:** `assert features[col].dtype in ("float64", "float32", "int64", "int32")`
> **Type:** Enforces a condition

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `def test_engineered_features_created(self):`
> **Type:** Function definition

### Line  80
> **Code:** `"""Engineered features should be created."""`
> **Type:** Code statement

### Line  81
> **Code:** `df = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `for col in ENGINEERED_FEATURES:`
> **Type:** For loop

### Line  86
> **Code:** `assert col in features.columns`
> **Type:** Enforces a condition

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `def test_categorical_encoded_as_int(self):`
> **Type:** Function definition

### Line  89
> **Code:** `"""Categorical features should be encoded as integers."""`
> **Type:** Logical operation

### Line  90
> **Code:** `df = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `for col in CATEGORICAL_FEATURES:`
> **Type:** For loop

### Line  95
> **Code:** `assert col in features.columns`
> **Type:** Enforces a condition

### Line  96
> **Code:** `assert features[col].dtype in ("int64", "int32")`
> **Type:** Enforces a condition

### Line  97
> **Code:** `# Values should be >= -1 (unseen categories map to -1)`
> **Type:** Comment: Values should be >= -1 (unseen categories map to -1)

### Line  98
> **Code:** `assert (features[col] >= -1).all()`
> **Type:** Enforces a condition

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `def test_transform_unseen_categories_maps_to_minus_one(self):`
> **Type:** Function definition

### Line 101
> **Code:** `"""Unseen categories during transform should map to -1."""`
> **Type:** Arithmetic operation

### Line 102
> **Code:** `df_train = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `df_test = df_train.copy()`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `# Add unseen category`
> **Type:** Comment: Add unseen category

### Line 105
> **Code:** `df_test.loc[0, "Gender"] = "UnknownGender"`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `transformer.fit(df_train)`
> **Type:** Logical operation

### Line 109
> **Code:** `features = transformer.transform(df_test)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `assert features.loc[0, "Gender"] == -1`
> **Type:** Enforces a condition

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `def test_config_roundtrip(self):`
> **Type:** Function definition

### Line 114
> **Code:** `"""to_config and from_config should preserve state."""`
> **Type:** Logical operation

### Line 115
> **Code:** `df = self._sample_df(30)`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `transformer.fit(df)`
> **Type:** Logical operation

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** `config = transformer.to_config()`
> **Type:** Assignment/comparison

### Line 120
> **Code:** `restored = FeatureTransformer.from_config(config)`
> **Type:** Assignment/comparison

### Line 121
> **Code:** ``
> **Type:** Empty line

### Line 122
> **Code:** `# Test that both produce identical transforms`
> **Type:** Comment: Test that both produce identical transforms

### Line 123
> **Code:** `test_df = self._sample_df(10)`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `out1 = transformer.transform(test_df)`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `out2 = restored.transform(test_df)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** ``
> **Type:** Empty line

### Line 127
> **Code:** `pd.testing.assert_frame_equal(out1, out2)`
> **Type:** Function call

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `def test_train_inference_parity(self):`
> **Type:** Function definition

### Line 130
> **Code:** `"""Train-time fit_transform and inference-time transform should match ...`
> **Type:** Arithmetic operation

### Line 131
> **Code:** `df = self._sample_df(50)`
> **Type:** Assignment/comparison

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `# Train-time`
> **Type:** Comment: Train-time

### Line 134
> **Code:** `transformer_train = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `features_train = transformer_train.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 136
> **Code:** ``
> **Type:** Empty line

### Line 137
> **Code:** `# Inference-time (using saved config)`
> **Type:** Comment: Inference-time (using saved config)

### Line 138
> **Code:** `config = transformer_train.to_config()`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `transformer_infer = FeatureTransformer.from_config(config)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `features_infer = transformer_infer.transform(df)`
> **Type:** Assignment/comparison

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `pd.testing.assert_frame_equal(features_train, features_infer)`
> **Type:** Function call

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `def test_feature_order_preserved(self):`
> **Type:** Function definition

### Line 145
> **Code:** `"""Feature order should match FEATURE_ORDER exactly."""`
> **Type:** Logical operation

### Line 146
> **Code:** `df = self._sample_df(20)`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 149
> **Code:** ``
> **Type:** Empty line

### Line 150
> **Code:** `assert list(features.columns) == FEATURE_ORDER`
> **Type:** Enforces a condition

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `def test_num_services_feature(self):`
> **Type:** Function definition

### Line 153
> **Code:** `"""num_services should count Yes in SERVICE_COLUMNS."""`
> **Type:** Code statement

### Line 154
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 155
> **Code:** `"Gender": ["Male"],`
> **Type:** Data structure operation

### Line 156
> **Code:** `"SeniorCitizen": [0],`
> **Type:** Logical operation

### Line 157
> **Code:** `"Partner": ["Yes"],`
> **Type:** Data structure operation

### Line 158
> **Code:** `"Dependents": ["No"],`
> **Type:** Data structure operation

### Line 159
> **Code:** `"Tenure": [12],`
> **Type:** Data structure operation

### Line 160
> **Code:** `"PhoneService": ["Yes"],`
> **Type:** Data structure operation

### Line 161
> **Code:** `"MultipleLines": ["Yes"],`
> **Type:** Data structure operation

### Line 162
> **Code:** `"InternetService": ["DSL"],`
> **Type:** Data structure operation

### Line 163
> **Code:** `"OnlineSecurity": ["Yes"],`
> **Type:** Data structure operation

### Line 164
> **Code:** `"OnlineBackup": ["No"],`
> **Type:** Data structure operation

### Line 165
> **Code:** `"DeviceProtection": ["Yes"],`
> **Type:** Data structure operation

### Line 166
> **Code:** `"TechSupport": ["No"],`
> **Type:** Logical operation

### Line 167
> **Code:** `"StreamingTV": ["Yes"],`
> **Type:** Data structure operation

### Line 168
> **Code:** `"StreamingMovies": ["No"],`
> **Type:** Data structure operation

### Line 169
> **Code:** `"Contract": ["Month-to-month"],`
> **Type:** Arithmetic operation

### Line 170
> **Code:** `"PaperlessBilling": ["No"],`
> **Type:** Data structure operation

### Line 171
> **Code:** `"PaymentMethod": ["Electronic check"],`
> **Type:** Data structure operation

### Line 172
> **Code:** `"MonthlyCharges": [50.0],`
> **Type:** Data structure operation

### Line 173
> **Code:** `"TotalCharges": [600.0],`
> **Type:** Data structure operation

### Line 174
> **Code:** `"Churn": ["No"],`
> **Type:** Data structure operation

### Line 175
> **Code:** `})`
> **Type:** Code statement

### Line 176
> **Code:** ``
> **Type:** Empty line

### Line 177
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 179
> **Code:** ``
> **Type:** Empty line

### Line 180
> **Code:** `# OnlineSecurity=Yes, DeviceProtection=Yes, StreamingTV=Yes => 3 servi...`
> **Type:** Comment: OnlineSecurity=Yes, DeviceProtection=Yes, StreamingTV=Yes => 3 services

### Line 181
> **Code:** `# (OnlineBackup=No, TechSupport=No, StreamingMovies=No)`
> **Type:** Comment: (OnlineBackup=No, TechSupport=No, StreamingMovies=No)

### Line 182
> **Code:** `assert features["num_services"].iloc[0] == 3`
> **Type:** Enforces a condition

### Line 183
> **Code:** ``
> **Type:** Empty line

### Line 184
> **Code:** ``
> **Type:** Empty line

### Line 185
> **Code:** `class TestBuildFeatures:`
> **Type:** Class definition

### Line 186
> **Code:** `"""Test build_features end-to-end function."""`
> **Type:** Arithmetic operation

### Line 187
> **Code:** ``
> **Type:** Empty line

### Line 188
> **Code:** `def test_build_features_creates_output(self, tmp_path):`
> **Type:** Function definition

### Line 189
> **Code:** `"""build_features should create parquet and config files."""`
> **Type:** Logical operation

### Line 190
> **Code:** `input_file = tmp_path / "input.csv"`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `output_file = tmp_path / "features.parquet"`
> **Type:** Assignment/comparison

### Line 192
> **Code:** `config_file = tmp_path / "config.json"`
> **Type:** Assignment/comparison

### Line 193
> **Code:** ``
> **Type:** Empty line

### Line 194
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 195
> **Code:** `"Gender": ["Male", "Female"],`
> **Type:** Data structure operation

### Line 196
> **Code:** `"SeniorCitizen": [0, 1],`
> **Type:** Logical operation

### Line 197
> **Code:** `"Partner": ["Yes", "No"],`
> **Type:** Data structure operation

### Line 198
> **Code:** `"Dependents": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 199
> **Code:** `"Tenure": [12, 24],`
> **Type:** Data structure operation

### Line 200
> **Code:** `"PhoneService": ["Yes", "Yes"],`
> **Type:** Data structure operation

### Line 201
> **Code:** `"MultipleLines": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 202
> **Code:** `"InternetService": ["DSL", "Fiber optic"],`
> **Type:** Data structure operation

### Line 203
> **Code:** `"OnlineSecurity": ["Yes", "No"],`
> **Type:** Data structure operation

### Line 204
> **Code:** `"OnlineBackup": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 205
> **Code:** `"DeviceProtection": ["No", "No"],`
> **Type:** Data structure operation

### Line 206
> **Code:** `"TechSupport": ["Yes", "No"],`
> **Type:** Logical operation

### Line 207
> **Code:** `"StreamingTV": ["No", "No"],`
> **Type:** Data structure operation

### Line 208
> **Code:** `"StreamingMovies": ["No", "No"],`
> **Type:** Data structure operation

### Line 209
> **Code:** `"Contract": ["Month-to-month", "One year"],`
> **Type:** Arithmetic operation

### Line 210
> **Code:** `"PaperlessBilling": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 211
> **Code:** `"PaymentMethod": ["Electronic check", "Mailed check"],`
> **Type:** Data structure operation

### Line 212
> **Code:** `"MonthlyCharges": [50.0, 70.0],`
> **Type:** Data structure operation

### Line 213
> **Code:** `"TotalCharges": [600.0, 1680.0],`
> **Type:** Data structure operation

### Line 214
> **Code:** `"Churn": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 215
> **Code:** `})`
> **Type:** Code statement

### Line 216
> **Code:** `df.to_csv(input_file, index=False)`
> **Type:** Assignment/comparison

### Line 217
> **Code:** ``
> **Type:** Empty line

### Line 218
> **Code:** `features = build_features(input_file, output_file, config_file)`
> **Type:** Assignment/comparison

### Line 219
> **Code:** ``
> **Type:** Empty line

### Line 220
> **Code:** `assert output_file.exists()`
> **Type:** Enforces a condition

### Line 221
> **Code:** `assert config_file.exists()`
> **Type:** Enforces a condition

### Line 222
> **Code:** `assert len(features) == 2`
> **Type:** Enforces a condition

### Line 223
> **Code:** `assert TARGET_FEATURE in features.columns`
> **Type:** Enforces a condition

### Line 224
> **Code:** ``
> **Type:** Empty line

### Line 225
> **Code:** `# Verify config can be loaded`
> **Type:** Comment: Verify config can be loaded

### Line 226
> **Code:** `with config_file.open() as f:`
> **Type:** Context manager

### Line 227
> **Code:** `config = json.load(f)`
> **Type:** Assignment/comparison

### Line 228
> **Code:** `assert "category_mappings" in config`
> **Type:** Enforces a condition

### Line 229
> **Code:** `assert "numeric_stats" in config`
> **Type:** Enforces a condition

### Line 230
> **Code:** `assert "feature_order" in config`
> **Type:** Enforces a condition

### Line 231
> **Code:** ``
> **Type:** Empty line

### Line 232
> **Code:** `def test_target_feature_created(self):`
> **Type:** Function definition

### Line 233
> **Code:** `"""Target feature should be binary 0/1."""`
> **Type:** Arithmetic operation

### Line 234
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 235
> **Code:** `"Gender": ["Male", "Female"],`
> **Type:** Data structure operation

### Line 236
> **Code:** `"SeniorCitizen": [0, 1],`
> **Type:** Logical operation

### Line 237
> **Code:** `"Partner": ["Yes", "No"],`
> **Type:** Data structure operation

### Line 238
> **Code:** `"Dependents": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 239
> **Code:** `"Tenure": [12, 24],`
> **Type:** Data structure operation

### Line 240
> **Code:** `"PhoneService": ["Yes", "Yes"],`
> **Type:** Data structure operation

### Line 241
> **Code:** `"MultipleLines": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 242
> **Code:** `"InternetService": ["DSL", "Fiber optic"],`
> **Type:** Data structure operation

### Line 243
> **Code:** `"OnlineSecurity": ["Yes", "No"],`
> **Type:** Data structure operation

### Line 244
> **Code:** `"OnlineBackup": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 245
> **Code:** `"DeviceProtection": ["No", "No"],`
> **Type:** Data structure operation

### Line 246
> **Code:** `"TechSupport": ["Yes", "No"],`
> **Type:** Logical operation

### Line 247
> **Code:** `"StreamingTV": ["No", "No"],`
> **Type:** Data structure operation

### Line 248
> **Code:** `"StreamingMovies": ["No", "No"],`
> **Type:** Data structure operation

### Line 249
> **Code:** `"Contract": ["Month-to-month", "One year"],`
> **Type:** Arithmetic operation

### Line 250
> **Code:** `"PaperlessBilling": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 251
> **Code:** `"PaymentMethod": ["Electronic check", "Mailed check"],`
> **Type:** Data structure operation

### Line 252
> **Code:** `"MonthlyCharges": [50.0, 70.0],`
> **Type:** Data structure operation

### Line 253
> **Code:** `"TotalCharges": [600.0, 1680.0],`
> **Type:** Data structure operation

### Line 254
> **Code:** `"Churn": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 255
> **Code:** `})`
> **Type:** Code statement

### Line 256
> **Code:** ``
> **Type:** Empty line

### Line 257
> **Code:** `transformer = FeatureTransformer()`
> **Type:** Assignment/comparison

### Line 258
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 259
> **Code:** `features[TARGET_FEATURE] = (df[TARGET_COLUMN].astype(str).str.lower() ...`
> **Type:** Assignment/comparison

### Line 260
> **Code:** ``
> **Type:** Empty line

### Line 261
> **Code:** `assert set(features[TARGET_FEATURE].unique()) == {0, 1}`
> **Type:** Enforces a condition

### Line 262
> **Code:** `assert features[TARGET_FEATURE].iloc[0] == 0  # No -> 0`
> **Type:** Enforces a condition

### Line 263
> **Code:** `assert features[TARGET_FEATURE].iloc[1] == 1  # Yes -> 1`
> **Type:** Enforces a condition

### Line 264
> **Code:** ``
> **Type:** Empty line

### Line 265
> **Code:** ``
> **Type:** Empty line

### Line 266
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 267
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 267
- **Code lines:** 213
- **Comments:** 8
- **TODO items:** 3
- **Empty lines:** 43

---
*Documentation generated for: mlops-project-documentation*
*File: test_features.py*
---

# mlops-project-documentation: test_monitoring.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/unit/test_monitoring.py`
- **Total lines:** 281
- **File size:** 12095 bytes

## Line Type Summary
- **Code:** 216
- **Comment:** 9
- **Empty:** 53
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""Tests for src.monitoring.drift_detection module."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import os`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `import tempfile`
> **Type:** Imports a module

### Line   9
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** `from unittest.mock import patch, MagicMock`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  13
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  14
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  18
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from src.monitoring.drift_detection import detect_drift, _ks_fallback,...`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `class TestDriftDetection:`
> **Type:** Class definition

### Line  24
> **Code:** `"""Test drift detection logic with synthetic data."""`
> **Type:** Code statement

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `def _create_reference_data(self, n=1000):`
> **Type:** Function definition

### Line  27
> **Code:** `"""Create a reference dataset with known distributions."""`
> **Type:** Code statement

### Line  28
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  29
> **Code:** `return pd.DataFrame({`
> **Type:** Returns a value from a function

### Line  30
> **Code:** `"Tenure": np.random.randint(0, 72, n),`
> **Type:** Logical operation

### Line  31
> **Code:** `"MonthlyCharges": np.random.normal(60, 15, n).clip(20, 120),`
> **Type:** Logical operation

### Line  32
> **Code:** `"TotalCharges": np.random.normal(2000, 800, n).clip(100, 8000),`
> **Type:** Logical operation

### Line  33
> **Code:** `"charges_per_tenure": np.random.normal(30, 10, n).clip(0, 100),`
> **Type:** Logical operation

### Line  34
> **Code:** `"tenure_years": np.random.uniform(0, 6, n),`
> **Type:** Logical operation

### Line  35
> **Code:** `"num_services": np.random.randint(0, 6, n),`
> **Type:** Logical operation

### Line  36
> **Code:** `"Gender": np.random.choice(["Male", "Female"], n),`
> **Type:** Logical operation

### Line  37
> **Code:** `"SeniorCitizen": np.random.choice([0, 1], n, p=[0.8, 0.2]),`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `"Partner": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  39
> **Code:** `"Dependents": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  40
> **Code:** `"PhoneService": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  41
> **Code:** `"MultipleLines": np.random.choice(["Yes", "No", "No phone service"], n...`
> **Type:** Logical operation

### Line  42
> **Code:** `"InternetService": np.random.choice(["DSL", "Fiber optic", "No"], n),`
> **Type:** Logical operation

### Line  43
> **Code:** `"OnlineSecurity": np.random.choice(["Yes", "No", "No internet service"...`
> **Type:** Logical operation

### Line  44
> **Code:** `"OnlineBackup": np.random.choice(["Yes", "No", "No internet service"],...`
> **Type:** Logical operation

### Line  45
> **Code:** `"DeviceProtection": np.random.choice(["Yes", "No", "No internet servic...`
> **Type:** Logical operation

### Line  46
> **Code:** `"TechSupport": np.random.choice(["Yes", "No", "No internet service"], ...`
> **Type:** Logical operation

### Line  47
> **Code:** `"StreamingTV": np.random.choice(["Yes", "No", "No internet service"], ...`
> **Type:** Logical operation

### Line  48
> **Code:** `"StreamingMovies": np.random.choice(["Yes", "No", "No internet service...`
> **Type:** Logical operation

### Line  49
> **Code:** `"Contract": np.random.choice(["Month-to-month", "One year", "Two year"...`
> **Type:** Arithmetic operation

### Line  50
> **Code:** `"PaperlessBilling": np.random.choice(["Yes", "No"], n),`
> **Type:** Logical operation

### Line  51
> **Code:** `"PaymentMethod": np.random.choice(`
> **Type:** Logical operation

### Line  52
> **Code:** `["Electronic check", "Mailed check", "Bank transfer (automatic)", "Cre...`
> **Type:** Data structure operation

### Line  53
> **Code:** `),`
> **Type:** Code statement

### Line  54
> **Code:** `"label": np.random.choice([0, 1], n),`
> **Type:** Logical operation

### Line  55
> **Code:** `"prediction": np.random.uniform(0, 1, n),`
> **Type:** Logical operation

### Line  56
> **Code:** `})`
> **Type:** Code statement

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `def _create_drifted_data(self, reference_df, drift_magnitude=0.5):`
> **Type:** Function definition

### Line  59
> **Code:** `"""Create a drifted dataset by shifting distributions."""`
> **Type:** Code statement

### Line  60
> **Code:** `drifted = reference_df.copy()`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `np.random.seed(123)  # Different seed`
> **Type:** Logical operation

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `# Drift numeric features`
> **Type:** Comment: Drift numeric features

### Line  64
> **Code:** `for col in NUMERIC_FEATURES:`
> **Type:** For loop

### Line  65
> **Code:** `if col in drifted.columns:`
> **Type:** Conditional statement

### Line  66
> **Code:** `shift = reference_df[col].std() * drift_magnitude`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `drifted[col] = drifted[col] + shift`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `# Drift categorical features by changing distribution`
> **Type:** Comment: Drift categorical features by changing distribution

### Line  70
> **Code:** `for col in CATEGORICAL_FEATURES:`
> **Type:** For loop

### Line  71
> **Code:** `if col in drifted.columns:`
> **Type:** Conditional statement

### Line  72
> **Code:** `# Shift 30% of values to a different category`
> **Type:** Comment: Shift 30% of values to a different category

### Line  73
> **Code:** `n_change = int(len(drifted) * 0.3)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `unique_vals = reference_df[col].unique()`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `if len(unique_vals) > 1:`
> **Type:** Conditional statement

### Line  76
> **Code:** `idx = np.random.choice(len(drifted), n_change, replace=False)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `for i in idx:`
> **Type:** For loop

### Line  78
> **Code:** `current = drifted.loc[i, col]`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `other_vals = [v for v in unique_vals if v != current]`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `drifted.loc[i, col] = np.random.choice(other_vals)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `return drifted`
> **Type:** Returns a value from a function

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `def test_ks_fallback_detects_drift_on_shifted_numeric(self):`
> **Type:** Function definition

### Line  85
> **Code:** `"""_ks_fallback should detect drift when numeric columns are shifted."...`
> **Type:** Code statement

### Line  86
> **Code:** `reference = self._create_reference_data(500)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `current = self._create_drifted_data(reference, drift_magnitude=1.0)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `assert drift_score > 0`
> **Type:** Enforces a condition

### Line  92
> **Code:** `# At least some numeric columns should be detected as drifted`
> **Type:** Comment: At least some numeric columns should be detected as drifted

### Line  93
> **Code:** `drifted_numeric = [c for c in NUMERIC_FEATURES if c in per_column and ...`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `assert len(drifted_numeric) > 0`
> **Type:** Enforces a condition

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `def test_ks_fallback_no_drift_on_identical_data(self):`
> **Type:** Function definition

### Line  97
> **Code:** `"""_ks_fallback should not detect drift on identical data."""`
> **Type:** Logical operation

### Line  98
> **Code:** `reference = self._create_reference_data(500)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `assert drift_score == 0.0`
> **Type:** Enforces a condition

### Line 104
> **Code:** `for col, info in per_column.items():`
> **Type:** For loop

### Line 105
> **Code:** `assert info["drift_detected"] is False`
> **Type:** Enforces a condition

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `def test_ks_fallback_handles_empty_columns(self):`
> **Type:** Function definition

### Line 108
> **Code:** `"""_ks_fallback should handle columns with all NaN gracefully."""`
> **Type:** Logical operation

### Line 109
> **Code:** `reference = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `current["Tenure"] = np.nan`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `# Should not crash, Tenure should be skipped`
> **Type:** Comment: Should not crash, Tenure should be skipped

### Line 116
> **Code:** `assert "Tenure" not in per_column or not per_column["Tenure"]["drift_d...`
> **Type:** Enforces a condition

### Line 117
> **Code:** ``
> **Type:** Empty line

### Line 118
> **Code:** `def test_detect_drift_with_scipy_fallback(self, tmp_path):`
> **Type:** Function definition

### Line 119
> **Code:** `"""detect_drift should work with scipy fallback when evidently not ava...`
> **Type:** Logical operation

### Line 120
> **Code:** `reference = self._create_reference_data(200)`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `current = self._create_drifted_data(reference, drift_magnitude=0.8)`
> **Type:** Assignment/comparison

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** `# Force scipy fallback by patching evidently import`
> **Type:** Comment: Force scipy fallback by patching evidently import

### Line 129
> **Code:** `with patch.dict(sys.modules, {"evidently": None}):`
> **Type:** Context manager

### Line 130
> **Code:** `with patch("src.monitoring.drift_detection._evidently_report", side_ef...`
> **Type:** Context manager

### Line 131
> **Code:** `report = detect_drift(`
> **Type:** Assignment/comparison

### Line 132
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `threshold=0.3,`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `output_dir=tmp_path / "output"`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `)`
> **Type:** Code statement

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `assert report["engine"] == "scipy-fallback"`
> **Type:** Enforces a condition

### Line 139
> **Code:** `assert "drift_score" in report`
> **Type:** Enforces a condition

### Line 140
> **Code:** `assert "drift_detected" in report`
> **Type:** Enforces a condition

### Line 141
> **Code:** `assert "per_column" in report`
> **Type:** Enforces a condition

### Line 142
> **Code:** `assert "drifted_features" in report`
> **Type:** Enforces a condition

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `def test_detect_drift_identical_data_no_drift(self, tmp_path):`
> **Type:** Function definition

### Line 145
> **Code:** `"""detect_drift should not detect drift on identical data."""`
> **Type:** Logical operation

### Line 146
> **Code:** `reference = self._create_reference_data(200)`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line 148
> **Code:** ``
> **Type:** Empty line

### Line 149
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** `with patch("src.monitoring.drift_detection._evidently_report", side_ef...`
> **Type:** Context manager

### Line 155
> **Code:** `report = detect_drift(`
> **Type:** Assignment/comparison

### Line 156
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 157
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `threshold=0.3,`
> **Type:** Assignment/comparison

### Line 159
> **Code:** `output_dir=tmp_path / "output"`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `)`
> **Type:** Code statement

### Line 161
> **Code:** ``
> **Type:** Empty line

### Line 162
> **Code:** `assert report["drift_score"] == 0.0`
> **Type:** Enforces a condition

### Line 163
> **Code:** `assert report["drift_detected"] is False`
> **Type:** Enforces a condition

### Line 164
> **Code:** `assert report["drifted_features"] == []`
> **Type:** Enforces a condition

### Line 165
> **Code:** ``
> **Type:** Empty line

### Line 166
> **Code:** `def test_detect_drift_high_threshold(self, tmp_path):`
> **Type:** Function definition

### Line 167
> **Code:** `"""detect_drift should respect threshold parameter."""`
> **Type:** Code statement

### Line 168
> **Code:** `reference = self._create_reference_data(200)`
> **Type:** Assignment/comparison

### Line 169
> **Code:** `current = self._create_drifted_data(reference, drift_magnitude=0.3)`
> **Type:** Assignment/comparison

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 172
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 173
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 174
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 175
> **Code:** ``
> **Type:** Empty line

### Line 176
> **Code:** `with patch("src.monitoring.drift_detection._evidently_report", side_ef...`
> **Type:** Context manager

### Line 177
> **Code:** `# High threshold - should not detect`
> **Type:** Comment: High threshold - should not detect

### Line 178
> **Code:** `report_high = detect_drift(`
> **Type:** Assignment/comparison

### Line 179
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 181
> **Code:** `threshold=0.9,`
> **Type:** Assignment/comparison

### Line 182
> **Code:** `output_dir=tmp_path / "output"`
> **Type:** Assignment/comparison

### Line 183
> **Code:** `)`
> **Type:** Code statement

### Line 184
> **Code:** ``
> **Type:** Empty line

### Line 185
> **Code:** `# Low threshold - should detect`
> **Type:** Comment: Low threshold - should detect

### Line 186
> **Code:** `report_low = detect_drift(`
> **Type:** Assignment/comparison

### Line 187
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 188
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 189
> **Code:** `threshold=0.1,`
> **Type:** Assignment/comparison

### Line 190
> **Code:** `output_dir=tmp_path / "output"`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `)`
> **Type:** Code statement

### Line 192
> **Code:** ``
> **Type:** Empty line

### Line 193
> **Code:** `# With higher threshold, less likely to detect`
> **Type:** Comment: With higher threshold, less likely to detect

### Line 194
> **Code:** `assert report_high["threshold"] == 0.9`
> **Type:** Enforces a condition

### Line 195
> **Code:** `assert report_low["threshold"] == 0.1`
> **Type:** Enforces a condition

### Line 196
> **Code:** ``
> **Type:** Empty line

### Line 197
> **Code:** `def test_detect_drift_missing_reference_raises(self, tmp_path):`
> **Type:** Function definition

### Line 198
> **Code:** `"""detect_drift should raise FileNotFoundError for missing reference."...`
> **Type:** Logical operation

### Line 199
> **Code:** `current = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 200
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 201
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 202
> **Code:** ``
> **Type:** Empty line

### Line 203
> **Code:** `with pytest.raises(FileNotFoundError, match="Reference dataset not fou...`
> **Type:** Context manager

### Line 204
> **Code:** `detect_drift(`
> **Type:** Code statement

### Line 205
> **Code:** `reference_path=tmp_path / "nonexistent.csv",`
> **Type:** Assignment/comparison

### Line 206
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 207
> **Code:** `)`
> **Type:** Code statement

### Line 208
> **Code:** ``
> **Type:** Empty line

### Line 209
> **Code:** `def test_detect_drift_missing_current_raises(self, tmp_path):`
> **Type:** Function definition

### Line 210
> **Code:** `"""detect_drift should raise FileNotFoundError for missing current."""`
> **Type:** Logical operation

### Line 211
> **Code:** `reference = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 212
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 213
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 214
> **Code:** ``
> **Type:** Empty line

### Line 215
> **Code:** `with pytest.raises(FileNotFoundError, match="Current production data n...`
> **Type:** Context manager

### Line 216
> **Code:** `detect_drift(`
> **Type:** Code statement

### Line 217
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 218
> **Code:** `current_path=tmp_path / "nonexistent.csv",`
> **Type:** Assignment/comparison

### Line 219
> **Code:** `)`
> **Type:** Code statement

### Line 220
> **Code:** ``
> **Type:** Empty line

### Line 221
> **Code:** `def test_detect_drift_with_env_vars(self, tmp_path, monkeypatch):`
> **Type:** Function definition

### Line 222
> **Code:** `"""detect_drift should read from environment variables."""`
> **Type:** Code statement

### Line 223
> **Code:** `reference = self._create_reference_data(100)`
> **Type:** Assignment/comparison

### Line 224
> **Code:** `current = reference.copy()`
> **Type:** Assignment/comparison

### Line 225
> **Code:** ``
> **Type:** Empty line

### Line 226
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 227
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 228
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 229
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 230
> **Code:** ``
> **Type:** Empty line

### Line 231
> **Code:** `monkeypatch.setenv("DRIFT_REFERENCE", str(ref_path))`
> **Type:** Function call

### Line 232
> **Code:** `monkeypatch.setenv("DRIFT_CURRENT", str(cur_path))`
> **Type:** Function call

### Line 233
> **Code:** `monkeypatch.setenv("DRIFT_THRESHOLD", "0.5")`
> **Type:** Function call

### Line 234
> **Code:** ``
> **Type:** Empty line

### Line 235
> **Code:** `with patch("src.monitoring.drift_detection._evidently_report", side_ef...`
> **Type:** Context manager

### Line 236
> **Code:** `report = detect_drift()`
> **Type:** Assignment/comparison

### Line 237
> **Code:** ``
> **Type:** Empty line

### Line 238
> **Code:** `assert report["threshold"] == 0.5`
> **Type:** Enforces a condition

### Line 239
> **Code:** `assert report["reference"] == str(ref_path)`
> **Type:** Enforces a condition

### Line 240
> **Code:** `assert report["current"] == str(cur_path)`
> **Type:** Enforces a condition

### Line 241
> **Code:** ``
> **Type:** Empty line

### Line 242
> **Code:** `def test_detect_drift_with_evidently(self, tmp_path):`
> **Type:** Function definition

### Line 243
> **Code:** `"""detect_drift should use evidently when available."""`
> **Type:** Code statement

### Line 244
> **Code:** `pytest.importorskip("evidently")`
> **Type:** Logical operation

### Line 245
> **Code:** `reference = self._create_reference_data(200)`
> **Type:** Assignment/comparison

### Line 246
> **Code:** `current = self._create_drifted_data(reference, drift_magnitude=0.8)`
> **Type:** Assignment/comparison

### Line 247
> **Code:** ``
> **Type:** Empty line

### Line 248
> **Code:** `ref_path = tmp_path / "reference.csv"`
> **Type:** Assignment/comparison

### Line 249
> **Code:** `cur_path = tmp_path / "current.csv"`
> **Type:** Assignment/comparison

### Line 250
> **Code:** `reference.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 251
> **Code:** `current.to_csv(cur_path, index=False)`
> **Type:** Assignment/comparison

### Line 252
> **Code:** ``
> **Type:** Empty line

### Line 253
> **Code:** `report = detect_drift(`
> **Type:** Assignment/comparison

### Line 254
> **Code:** `reference_path=ref_path,`
> **Type:** Assignment/comparison

### Line 255
> **Code:** `current_path=cur_path,`
> **Type:** Assignment/comparison

### Line 256
> **Code:** `threshold=0.3,`
> **Type:** Assignment/comparison

### Line 257
> **Code:** `output_dir=tmp_path / "output"`
> **Type:** Assignment/comparison

### Line 258
> **Code:** `)`
> **Type:** Code statement

### Line 259
> **Code:** ``
> **Type:** Empty line

### Line 260
> **Code:** `assert report["engine"] == "evidently"`
> **Type:** Enforces a condition

### Line 261
> **Code:** `assert (tmp_path / "output" / "drift_report.json").exists()`
> **Type:** Enforces a condition

### Line 262
> **Code:** ``
> **Type:** Empty line

### Line 263
> **Code:** ``
> **Type:** Empty line

### Line 264
> **Code:** `class TestFeatureColumns:`
> **Type:** Class definition

### Line 265
> **Code:** `"""Test that feature column lists match the actual data."""`
> **Type:** Code statement

### Line 266
> **Code:** ``
> **Type:** Empty line

### Line 267
> **Code:** `def test_numeric_features_not_empty(self):`
> **Type:** Function definition

### Line 268
> **Code:** `assert len(NUMERIC_FEATURES) > 0`
> **Type:** Enforces a condition

### Line 269
> **Code:** `assert all(isinstance(c, str) for c in NUMERIC_FEATURES)`
> **Type:** Enforces a condition

### Line 270
> **Code:** ``
> **Type:** Empty line

### Line 271
> **Code:** `def test_categorical_features_not_empty(self):`
> **Type:** Function definition

### Line 272
> **Code:** `assert len(CATEGORICAL_FEATURES) > 0`
> **Type:** Enforces a condition

### Line 273
> **Code:** `assert all(isinstance(c, str) for c in CATEGORICAL_FEATURES)`
> **Type:** Enforces a condition

### Line 274
> **Code:** ``
> **Type:** Empty line

### Line 275
> **Code:** `def test_no_duplicate_features(self):`
> **Type:** Function definition

### Line 276
> **Code:** `all_features = NUMERIC_FEATURES + CATEGORICAL_FEATURES`
> **Type:** Assignment/comparison

### Line 277
> **Code:** `assert len(all_features) == len(set(all_features))`
> **Type:** Enforces a condition

### Line 278
> **Code:** ``
> **Type:** Empty line

### Line 279
> **Code:** ``
> **Type:** Empty line

### Line 280
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 281
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 281
- **Code lines:** 216
- **Comments:** 9
- **TODO items:** 3
- **Empty lines:** 53

---
*Documentation generated for: mlops-project-documentation*
*File: test_monitoring.py*
---

# mlops-project-documentation: test_preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/unit/test_preprocessing.py`
- **Total lines:** 244
- **File size:** 9456 bytes

## Line Type Summary
- **Code:** 222
- **Comment:** 0
- **Empty:** 19
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for src.data.preprocessing module."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   7
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import sys`
> **Type:** Imports a module

### Line  10
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  14
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `from src.data.preprocessing import preprocess, DROP_COLUMNS, NUMERIC_C...`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `class TestPreprocessing:`
> **Type:** Class definition

### Line  20
> **Code:** `"""Test preprocessing correctness."""`
> **Type:** Logical operation

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `def _run(self, df, tmp_path):`
> **Type:** Function definition

### Line  23
> **Code:** `"""Write df to a CSV and run preprocess with file paths."""`
> **Type:** Logical operation

### Line  24
> **Code:** `input_file = tmp_path / "input.csv"`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `output_file = tmp_path / "output.csv"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `df.to_csv(input_file, index=False)`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `return preprocess(input_file, output_file)`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def test_drop_customer_id(self, tmp_path):`
> **Type:** Function definition

### Line  30
> **Code:** `"""CustomerID column should be dropped."""`
> **Type:** Code statement

### Line  31
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `"CustomerID": ["123", "456"],`
> **Type:** Data structure operation

### Line  33
> **Code:** `"Gender": ["Male", "Female"],`
> **Type:** Data structure operation

### Line  34
> **Code:** `"SeniorCitizen": [0, 1],`
> **Type:** Logical operation

### Line  35
> **Code:** `"Partner": ["Yes", "No"],`
> **Type:** Data structure operation

### Line  36
> **Code:** `"Dependents": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  37
> **Code:** `"Tenure": [12, 24],`
> **Type:** Data structure operation

### Line  38
> **Code:** `"PhoneService": ["Yes", "Yes"],`
> **Type:** Data structure operation

### Line  39
> **Code:** `"MultipleLines": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  40
> **Code:** `"InternetService": ["DSL", "Fiber optic"],`
> **Type:** Data structure operation

### Line  41
> **Code:** `"OnlineSecurity": ["Yes", "No"],`
> **Type:** Data structure operation

### Line  42
> **Code:** `"OnlineBackup": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  43
> **Code:** `"DeviceProtection": ["No", "No"],`
> **Type:** Data structure operation

### Line  44
> **Code:** `"TechSupport": ["Yes", "No"],`
> **Type:** Logical operation

### Line  45
> **Code:** `"StreamingTV": ["No", "No"],`
> **Type:** Data structure operation

### Line  46
> **Code:** `"StreamingMovies": ["No", "No"],`
> **Type:** Data structure operation

### Line  47
> **Code:** `"Contract": ["Month-to-month", "One year"],`
> **Type:** Arithmetic operation

### Line  48
> **Code:** `"PaperlessBilling": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  49
> **Code:** `"PaymentMethod": ["Electronic check", "Mailed check"],`
> **Type:** Data structure operation

### Line  50
> **Code:** `"MonthlyCharges": [50.0, 70.0],`
> **Type:** Data structure operation

### Line  51
> **Code:** `"TotalCharges": [600.0, 1680.0],`
> **Type:** Data structure operation

### Line  52
> **Code:** `"Churn": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  53
> **Code:** `})`
> **Type:** Code statement

### Line  54
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `assert "CustomerID" not in result.columns`
> **Type:** Enforces a condition

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def test_numeric_columns_coerced(self, tmp_path):`
> **Type:** Function definition

### Line  58
> **Code:** `"""Numeric columns should be coerced, invalid rows dropped."""`
> **Type:** Code statement

### Line  59
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `"CustomerID": ["1", "2", "3"],`
> **Type:** Data structure operation

### Line  61
> **Code:** `"Gender": ["Male", "Female", "Male"],`
> **Type:** Data structure operation

### Line  62
> **Code:** `"SeniorCitizen": [0, 1, 0],`
> **Type:** Logical operation

### Line  63
> **Code:** `"Partner": ["Yes", "No", "Yes"],`
> **Type:** Data structure operation

### Line  64
> **Code:** `"Dependents": ["No", "Yes", "No"],`
> **Type:** Data structure operation

### Line  65
> **Code:** `"Tenure": [12, "invalid", 24],`
> **Type:** Data structure operation

### Line  66
> **Code:** `"PhoneService": ["Yes", "Yes", "Yes"],`
> **Type:** Data structure operation

### Line  67
> **Code:** `"MultipleLines": ["No", "Yes", "No"],`
> **Type:** Data structure operation

### Line  68
> **Code:** `"InternetService": ["DSL", "Fiber optic", "DSL"],`
> **Type:** Data structure operation

### Line  69
> **Code:** `"OnlineSecurity": ["Yes", "No", "Yes"],`
> **Type:** Data structure operation

### Line  70
> **Code:** `"OnlineBackup": ["No", "Yes", "No"],`
> **Type:** Data structure operation

### Line  71
> **Code:** `"DeviceProtection": ["No", "No", "Yes"],`
> **Type:** Data structure operation

### Line  72
> **Code:** `"TechSupport": ["Yes", "No", "Yes"],`
> **Type:** Logical operation

### Line  73
> **Code:** `"StreamingTV": ["No", "No", "No"],`
> **Type:** Data structure operation

### Line  74
> **Code:** `"StreamingMovies": ["No", "No", "No"],`
> **Type:** Data structure operation

### Line  75
> **Code:** `"Contract": ["Month-to-month", "One year", "Two year"],`
> **Type:** Arithmetic operation

### Line  76
> **Code:** `"PaperlessBilling": ["No", "Yes", "No"],`
> **Type:** Data structure operation

### Line  77
> **Code:** `"PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (...`
> **Type:** Data structure operation

### Line  78
> **Code:** `"MonthlyCharges": [50.0, 70.0, 90.0],`
> **Type:** Data structure operation

### Line  79
> **Code:** `"TotalCharges": [600.0, "bad", 2160.0],`
> **Type:** Data structure operation

### Line  80
> **Code:** `"Churn": ["No", "Yes", "No"],`
> **Type:** Data structure operation

### Line  81
> **Code:** `})`
> **Type:** Code statement

### Line  82
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `assert len(result) == 2`
> **Type:** Enforces a condition

### Line  84
> **Code:** `assert result["Tenure"].dtype in ("int64", "float64")`
> **Type:** Enforces a condition

### Line  85
> **Code:** `assert result["TotalCharges"].dtype in ("int64", "float64")`
> **Type:** Enforces a condition

### Line  86
> **Code:** `assert result["MonthlyCharges"].dtype in ("int64", "float64")`
> **Type:** Enforces a condition

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `def test_negative_tenure_dropped(self, tmp_path):`
> **Type:** Function definition

### Line  89
> **Code:** `"""Rows with negative Tenure should be dropped."""`
> **Type:** Code statement

### Line  90
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `"CustomerID": ["1", "2"],`
> **Type:** Data structure operation

### Line  92
> **Code:** `"Gender": ["Male", "Female"],`
> **Type:** Data structure operation

### Line  93
> **Code:** `"SeniorCitizen": [0, 1],`
> **Type:** Logical operation

### Line  94
> **Code:** `"Partner": ["Yes", "No"],`
> **Type:** Data structure operation

### Line  95
> **Code:** `"Dependents": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  96
> **Code:** `"Tenure": [-5, 10],`
> **Type:** Arithmetic operation

### Line  97
> **Code:** `"PhoneService": ["Yes", "Yes"],`
> **Type:** Data structure operation

### Line  98
> **Code:** `"MultipleLines": ["No", "Yes"],`
> **Type:** Data structure operation

### Line  99
> **Code:** `"InternetService": ["DSL", "Fiber optic"],`
> **Type:** Data structure operation

### Line 100
> **Code:** `"OnlineSecurity": ["Yes", "No"],`
> **Type:** Data structure operation

### Line 101
> **Code:** `"OnlineBackup": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 102
> **Code:** `"DeviceProtection": ["No", "No"],`
> **Type:** Data structure operation

### Line 103
> **Code:** `"TechSupport": ["Yes", "No"],`
> **Type:** Logical operation

### Line 104
> **Code:** `"StreamingTV": ["No", "No"],`
> **Type:** Data structure operation

### Line 105
> **Code:** `"StreamingMovies": ["No", "No"],`
> **Type:** Data structure operation

### Line 106
> **Code:** `"Contract": ["Month-to-month", "One year"],`
> **Type:** Arithmetic operation

### Line 107
> **Code:** `"PaperlessBilling": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 108
> **Code:** `"PaymentMethod": ["Electronic check", "Mailed check"],`
> **Type:** Data structure operation

### Line 109
> **Code:** `"MonthlyCharges": [50.0, 70.0],`
> **Type:** Data structure operation

### Line 110
> **Code:** `"TotalCharges": [600.0, 700.0],`
> **Type:** Data structure operation

### Line 111
> **Code:** `"Churn": ["No", "Yes"],`
> **Type:** Data structure operation

### Line 112
> **Code:** `})`
> **Type:** Code statement

### Line 113
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `assert len(result) == 1`
> **Type:** Enforces a condition

### Line 115
> **Code:** `assert result["Tenure"].iloc[0] == 10`
> **Type:** Enforces a condition

### Line 116
> **Code:** ``
> **Type:** Empty line

### Line 117
> **Code:** `def test_categorical_stripped(self, tmp_path):`
> **Type:** Function definition

### Line 118
> **Code:** `"""Categorical columns should be stripped of whitespace."""`
> **Type:** Logical operation

### Line 119
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 120
> **Code:** `"CustomerID": ["1"],`
> **Type:** Data structure operation

### Line 121
> **Code:** `"Gender": [" Male "],`
> **Type:** Data structure operation

### Line 122
> **Code:** `"SeniorCitizen": [0],`
> **Type:** Logical operation

### Line 123
> **Code:** `"Partner": [" Yes "],`
> **Type:** Data structure operation

### Line 124
> **Code:** `"Dependents": ["No "],`
> **Type:** Data structure operation

### Line 125
> **Code:** `"Tenure": [12],`
> **Type:** Data structure operation

### Line 126
> **Code:** `"PhoneService": ["Yes"],`
> **Type:** Data structure operation

### Line 127
> **Code:** `"MultipleLines": ["No"],`
> **Type:** Data structure operation

### Line 128
> **Code:** `"InternetService": [" DSL "],`
> **Type:** Data structure operation

### Line 129
> **Code:** `"OnlineSecurity": ["Yes"],`
> **Type:** Data structure operation

### Line 130
> **Code:** `"OnlineBackup": ["No"],`
> **Type:** Data structure operation

### Line 131
> **Code:** `"DeviceProtection": ["No"],`
> **Type:** Data structure operation

### Line 132
> **Code:** `"TechSupport": ["Yes"],`
> **Type:** Logical operation

### Line 133
> **Code:** `"StreamingTV": ["No"],`
> **Type:** Data structure operation

### Line 134
> **Code:** `"StreamingMovies": ["No"],`
> **Type:** Data structure operation

### Line 135
> **Code:** `"Contract": ["Month-to-month"],`
> **Type:** Arithmetic operation

### Line 136
> **Code:** `"PaperlessBilling": ["No"],`
> **Type:** Data structure operation

### Line 137
> **Code:** `"PaymentMethod": ["Electronic check"],`
> **Type:** Data structure operation

### Line 138
> **Code:** `"MonthlyCharges": [50.0],`
> **Type:** Data structure operation

### Line 139
> **Code:** `"TotalCharges": [600.0],`
> **Type:** Data structure operation

### Line 140
> **Code:** `"Churn": [" No "],`
> **Type:** Data structure operation

### Line 141
> **Code:** `})`
> **Type:** Code statement

### Line 142
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `assert result["Gender"].iloc[0] == "Male"`
> **Type:** Enforces a condition

### Line 144
> **Code:** `assert result["Partner"].iloc[0] == "Yes"`
> **Type:** Enforces a condition

### Line 145
> **Code:** `assert result["InternetService"].iloc[0] == "DSL"`
> **Type:** Enforces a condition

### Line 146
> **Code:** `assert result["Churn"].iloc[0] == "No"`
> **Type:** Enforces a condition

### Line 147
> **Code:** ``
> **Type:** Empty line

### Line 148
> **Code:** `def test_target_column_preserved(self, tmp_path):`
> **Type:** Function definition

### Line 149
> **Code:** `"""Target column (Churn) should be preserved and stripped."""`
> **Type:** Logical operation

### Line 150
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `"CustomerID": ["1"],`
> **Type:** Data structure operation

### Line 152
> **Code:** `"Gender": ["Male"],`
> **Type:** Data structure operation

### Line 153
> **Code:** `"SeniorCitizen": [0],`
> **Type:** Logical operation

### Line 154
> **Code:** `"Partner": ["Yes"],`
> **Type:** Data structure operation

### Line 155
> **Code:** `"Dependents": ["No"],`
> **Type:** Data structure operation

### Line 156
> **Code:** `"Tenure": [12],`
> **Type:** Data structure operation

### Line 157
> **Code:** `"PhoneService": ["Yes"],`
> **Type:** Data structure operation

### Line 158
> **Code:** `"MultipleLines": ["No"],`
> **Type:** Data structure operation

### Line 159
> **Code:** `"InternetService": ["DSL"],`
> **Type:** Data structure operation

### Line 160
> **Code:** `"OnlineSecurity": ["Yes"],`
> **Type:** Data structure operation

### Line 161
> **Code:** `"OnlineBackup": ["No"],`
> **Type:** Data structure operation

### Line 162
> **Code:** `"DeviceProtection": ["No"],`
> **Type:** Data structure operation

### Line 163
> **Code:** `"TechSupport": ["Yes"],`
> **Type:** Logical operation

### Line 164
> **Code:** `"StreamingTV": ["No"],`
> **Type:** Data structure operation

### Line 165
> **Code:** `"StreamingMovies": ["No"],`
> **Type:** Data structure operation

### Line 166
> **Code:** `"Contract": ["Month-to-month"],`
> **Type:** Arithmetic operation

### Line 167
> **Code:** `"PaperlessBilling": ["No"],`
> **Type:** Data structure operation

### Line 168
> **Code:** `"PaymentMethod": ["Electronic check"],`
> **Type:** Data structure operation

### Line 169
> **Code:** `"MonthlyCharges": [50.0],`
> **Type:** Data structure operation

### Line 170
> **Code:** `"TotalCharges": [600.0],`
> **Type:** Data structure operation

### Line 171
> **Code:** `"Churn": [" Yes "],`
> **Type:** Data structure operation

### Line 172
> **Code:** `})`
> **Type:** Code statement

### Line 173
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line 174
> **Code:** `assert TARGET_COLUMN in result.columns`
> **Type:** Enforces a condition

### Line 175
> **Code:** `assert result[TARGET_COLUMN].iloc[0] == "Yes"`
> **Type:** Enforces a condition

### Line 176
> **Code:** ``
> **Type:** Empty line

### Line 177
> **Code:** `def test_output_columns_match_expected(self, tmp_path):`
> **Type:** Function definition

### Line 178
> **Code:** `"""Output should have all expected columns except CustomerID."""`
> **Type:** Code statement

### Line 179
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `"CustomerID": ["1"],`
> **Type:** Data structure operation

### Line 181
> **Code:** `"Gender": ["Male"],`
> **Type:** Data structure operation

### Line 182
> **Code:** `"SeniorCitizen": [0],`
> **Type:** Logical operation

### Line 183
> **Code:** `"Partner": ["Yes"],`
> **Type:** Data structure operation

### Line 184
> **Code:** `"Dependents": ["No"],`
> **Type:** Data structure operation

### Line 185
> **Code:** `"Tenure": [12],`
> **Type:** Data structure operation

### Line 186
> **Code:** `"PhoneService": ["Yes"],`
> **Type:** Data structure operation

### Line 187
> **Code:** `"MultipleLines": ["No"],`
> **Type:** Data structure operation

### Line 188
> **Code:** `"InternetService": ["DSL"],`
> **Type:** Data structure operation

### Line 189
> **Code:** `"OnlineSecurity": ["Yes"],`
> **Type:** Data structure operation

### Line 190
> **Code:** `"OnlineBackup": ["No"],`
> **Type:** Data structure operation

### Line 191
> **Code:** `"DeviceProtection": ["No"],`
> **Type:** Data structure operation

### Line 192
> **Code:** `"TechSupport": ["Yes"],`
> **Type:** Logical operation

### Line 193
> **Code:** `"StreamingTV": ["No"],`
> **Type:** Data structure operation

### Line 194
> **Code:** `"StreamingMovies": ["No"],`
> **Type:** Data structure operation

### Line 195
> **Code:** `"Contract": ["Month-to-month"],`
> **Type:** Arithmetic operation

### Line 196
> **Code:** `"PaperlessBilling": ["No"],`
> **Type:** Data structure operation

### Line 197
> **Code:** `"PaymentMethod": ["Electronic check"],`
> **Type:** Data structure operation

### Line 198
> **Code:** `"MonthlyCharges": [50.0],`
> **Type:** Data structure operation

### Line 199
> **Code:** `"TotalCharges": [600.0],`
> **Type:** Data structure operation

### Line 200
> **Code:** `"Churn": ["No"],`
> **Type:** Data structure operation

### Line 201
> **Code:** `})`
> **Type:** Code statement

### Line 202
> **Code:** `result = self._run(df, tmp_path)`
> **Type:** Assignment/comparison

### Line 203
> **Code:** `expected_cols = set(NUMERIC_COLUMNS + CATEGORICAL_COLUMNS + [TARGET_CO...`
> **Type:** Assignment/comparison

### Line 204
> **Code:** `assert set(result.columns) == expected_cols`
> **Type:** Enforces a condition

### Line 205
> **Code:** ``
> **Type:** Empty line

### Line 206
> **Code:** `def test_preprocess_with_file_paths(self, tmp_path):`
> **Type:** Function definition

### Line 207
> **Code:** `"""Test preprocess with file input/output paths."""`
> **Type:** Arithmetic operation

### Line 208
> **Code:** `input_file = tmp_path / "input.csv"`
> **Type:** Assignment/comparison

### Line 209
> **Code:** `output_file = tmp_path / "output.csv"`
> **Type:** Assignment/comparison

### Line 210
> **Code:** ``
> **Type:** Empty line

### Line 211
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 212
> **Code:** `"CustomerID": ["1"],`
> **Type:** Data structure operation

### Line 213
> **Code:** `"Gender": ["Male"],`
> **Type:** Data structure operation

### Line 214
> **Code:** `"SeniorCitizen": [0],`
> **Type:** Logical operation

### Line 215
> **Code:** `"Partner": ["Yes"],`
> **Type:** Data structure operation

### Line 216
> **Code:** `"Dependents": ["No"],`
> **Type:** Data structure operation

### Line 217
> **Code:** `"Tenure": [12],`
> **Type:** Data structure operation

### Line 218
> **Code:** `"PhoneService": ["Yes"],`
> **Type:** Data structure operation

### Line 219
> **Code:** `"MultipleLines": ["No"],`
> **Type:** Data structure operation

### Line 220
> **Code:** `"InternetService": ["DSL"],`
> **Type:** Data structure operation

### Line 221
> **Code:** `"OnlineSecurity": ["Yes"],`
> **Type:** Data structure operation

### Line 222
> **Code:** `"OnlineBackup": ["No"],`
> **Type:** Data structure operation

### Line 223
> **Code:** `"DeviceProtection": ["No"],`
> **Type:** Data structure operation

### Line 224
> **Code:** `"TechSupport": ["Yes"],`
> **Type:** Logical operation

### Line 225
> **Code:** `"StreamingTV": ["No"],`
> **Type:** Data structure operation

### Line 226
> **Code:** `"StreamingMovies": ["No"],`
> **Type:** Data structure operation

### Line 227
> **Code:** `"Contract": ["Month-to-month"],`
> **Type:** Arithmetic operation

### Line 228
> **Code:** `"PaperlessBilling": ["No"],`
> **Type:** Data structure operation

### Line 229
> **Code:** `"PaymentMethod": ["Electronic check"],`
> **Type:** Data structure operation

### Line 230
> **Code:** `"MonthlyCharges": [50.0],`
> **Type:** Data structure operation

### Line 231
> **Code:** `"TotalCharges": [600.0],`
> **Type:** Data structure operation

### Line 232
> **Code:** `"Churn": ["No"],`
> **Type:** Data structure operation

### Line 233
> **Code:** `})`
> **Type:** Code statement

### Line 234
> **Code:** `df.to_csv(input_file, index=False)`
> **Type:** Assignment/comparison

### Line 235
> **Code:** ``
> **Type:** Empty line

### Line 236
> **Code:** `result = preprocess(input_file, output_file)`
> **Type:** Assignment/comparison

### Line 237
> **Code:** ``
> **Type:** Empty line

### Line 238
> **Code:** `assert output_file.exists()`
> **Type:** Enforces a condition

### Line 239
> **Code:** `assert len(result) == 1`
> **Type:** Enforces a condition

### Line 240
> **Code:** `assert "CustomerID" not in result.columns`
> **Type:** Enforces a condition

### Line 241
> **Code:** ``
> **Type:** Empty line

### Line 242
> **Code:** ``
> **Type:** Empty line

### Line 243
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 244
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 244
- **Code lines:** 222
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 19

---
*Documentation generated for: mlops-project-documentation*
*File: test_preprocessing.py*
---

# mlops-project-documentation: test_evaluate.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/unit/test_evaluate.py`
- **Total lines:** 294
- **File size:** 12814 bytes

## Line Type Summary
- **Code:** 219
- **Comment:** 12
- **Empty:** 60
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add quality gate with thresholds`
> **Type:** TODO: high - Add quality gate with thresholds

### Line   2
> **Code:** `# TODO: medium - Implement comparison vs current production model`
> **Type:** TODO: medium - Implement comparison vs current production model

### Line   3
> **Code:** `# TODO: low - Add metrics export for Evidence Pack`
> **Type:** TODO: low - Add metrics export for Evidence Pack

### Line   4
> **Code:** `"""Tests for src.models.evaluate module."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import os`
> **Type:** Imports a module

### Line   8
> **Code:** `import sys`
> **Type:** Imports a module

### Line   9
> **Code:** `import tempfile`
> **Type:** Imports a module

### Line  10
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** `from unittest.mock import MagicMock, patch, PropertyMock`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  14
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  15
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  19
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `from src.models.evaluate import evaluate, evaluate_model, DEFAULT_THRE...`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from src.features.build_features import FEATURE_ORDER, TARGET_FEATURE`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `class TestEvaluate:`
> **Type:** Class definition

### Line  26
> **Code:** `"""Test model evaluation and validation gates."""`
> **Type:** Logical operation

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `def _create_mock_model(self, labels=None, f1=0.8, accuracy=0.85, roc_a...`
> **Type:** Function definition

### Line  29
> **Code:** `"""Create a mock model with predictable predictions."""`
> **Type:** Code statement

### Line  30
> **Code:** `model = MagicMock()`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `if labels is not None:`
> **Type:** Conditional statement

### Line  32
> **Code:** `# Perfect predictions: match the provided labels -> all metrics = 1.0`
> **Type:** Comment: Perfect predictions: match the provided labels -> all metrics = 1.0

### Line  33
> **Code:** `y = np.asarray(labels)`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `model.predict.return_value = y`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `model.predict_proba.return_value = np.column_stack([1 - y, y])`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `return model`
> **Type:** Returns a value from a function

### Line  37
> **Code:** `# Otherwise: predict everything as class 1 (churn) -> low accuracy on`
> **Type:** Comment: Otherwise: predict everything as class 1 (churn) -> low accuracy on

### Line  38
> **Code:** `# imbalanced data, useful for gate-failure tests.`
> **Type:** Comment: imbalanced data, useful for gate-failure tests.

### Line  39
> **Code:** `def predict_proba(X):`
> **Type:** Function definition

### Line  40
> **Code:** `n = len(X)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `prob_class_1 = np.full(n, 0.7)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `return np.column_stack([1 - prob_class_1, prob_class_1])`
> **Type:** Returns a value from a function

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `def predict(X):`
> **Type:** Function definition

### Line  45
> **Code:** `n = len(X)`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `return np.ones(n, dtype=int)`
> **Type:** Returns a value from a function

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `model.predict_proba = predict_proba`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `model.predict = predict`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `return model`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _create_test_data(self, n=100):`
> **Type:** Function definition

### Line  53
> **Code:** `"""Create test features and labels."""`
> **Type:** Logical operation

### Line  54
> **Code:** `np.random.seed(42)`
> **Type:** Logical operation

### Line  55
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `col: np.random.randn(n) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line  57
> **Code:** `})`
> **Type:** Code statement

### Line  58
> **Code:** `labels = pd.Series(np.random.choice([0, 1], n, p=[0.7, 0.3]), name=TAR...`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `return features, labels`
> **Type:** Returns a value from a function

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line  62
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line  63
> **Code:** `def test_evaluate_model_returns_metrics(self, mock_load_test, mock_res...`
> **Type:** Function definition

### Line  64
> **Code:** `"""evaluate_model should return all expected metrics."""`
> **Type:** Code statement

### Line  65
> **Code:** `features, labels = self._create_test_data(50)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `mock_resolve_model.return_value = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `from src.models.evaluate import evaluate_model as em`
> **Type:** Imports specific names from a module

### Line  70
> **Code:** `model = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `metrics = em(model, features, labels)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `assert "f1" in metrics`
> **Type:** Enforces a condition

### Line  74
> **Code:** `assert "accuracy" in metrics`
> **Type:** Enforces a condition

### Line  75
> **Code:** `assert "precision" in metrics`
> **Type:** Enforces a condition

### Line  76
> **Code:** `assert "recall" in metrics`
> **Type:** Enforces a condition

### Line  77
> **Code:** `assert "roc_auc" in metrics`
> **Type:** Enforces a condition

### Line  78
> **Code:** `assert "n_samples" in metrics`
> **Type:** Enforces a condition

### Line  79
> **Code:** `assert metrics["n_samples"] == 50`
> **Type:** Enforces a condition

### Line  80
> **Code:** `assert 0 <= metrics["f1"] <= 1`
> **Type:** Enforces a condition

### Line  81
> **Code:** `assert 0 <= metrics["accuracy"] <= 1`
> **Type:** Enforces a condition

### Line  82
> **Code:** `assert 0 <= metrics["roc_auc"] <= 1`
> **Type:** Enforces a condition

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line  85
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line  86
> **Code:** `def test_evaluate_returns_report_with_gates(self, mock_load_test, mock...`
> **Type:** Function definition

### Line  87
> **Code:** `"""evaluate should return a report with gates_passed."""`
> **Type:** Logical operation

### Line  88
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `mock_resolve_model.return_value = self._create_mock_model(f1=0.9, accu...`
> **Type:** Assignment/comparison

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `report = evaluate(thresholds={"min_f1": 0.5, "min_accuracy": 0.7, "min...`
> **Type:** Assignment/comparison

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `assert "metrics" in report`
> **Type:** Enforces a condition

### Line  95
> **Code:** `assert "thresholds" in report`
> **Type:** Enforces a condition

### Line  96
> **Code:** `assert "gates" in report`
> **Type:** Enforces a condition

### Line  97
> **Code:** `assert "gates_passed" in report`
> **Type:** Enforces a condition

### Line  98
> **Code:** `assert isinstance(report["gates_passed"], bool)`
> **Type:** Enforces a condition

### Line  99
> **Code:** `assert report["thresholds"]["min_f1"] == 0.5`
> **Type:** Enforces a condition

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 102
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 103
> **Code:** `def test_evaluate_gates_pass_when_metrics_above_threshold(self, mock_l...`
> **Type:** Function definition

### Line 104
> **Code:** `"""gates_passed should be True when all metrics exceed thresholds."""`
> **Type:** Code statement

### Line 105
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `# Perfect model: every metric = 1.0, above all thresholds`
> **Type:** Comment: Perfect model: every metric = 1.0, above all thresholds

### Line 108
> **Code:** `mock_resolve_model.return_value = self._create_mock_model(labels=label...`
> **Type:** Assignment/comparison

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `report = evaluate(thresholds={"min_f1": 0.5, "min_accuracy": 0.7, "min...`
> **Type:** Assignment/comparison

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `assert report["gates_passed"] is True`
> **Type:** Enforces a condition

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 115
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 116
> **Code:** `def test_evaluate_gates_fail_when_metrics_below_threshold(self, mock_l...`
> **Type:** Function definition

### Line 117
> **Code:** `"""gates_passed should be False when any metric is below threshold."""`
> **Type:** Code statement

### Line 118
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line 119
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 120
> **Code:** `# Model with low performance`
> **Type:** Comment: Model with low performance

### Line 121
> **Code:** `mock_resolve_model.return_value = self._create_mock_model(f1=0.2, accu...`
> **Type:** Assignment/comparison

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** `report = evaluate(thresholds={"min_f1": 0.5, "min_accuracy": 0.7, "min...`
> **Type:** Assignment/comparison

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `assert report["gates_passed"] is False`
> **Type:** Enforces a condition

### Line 126
> **Code:** `# At least one gate should fail`
> **Type:** Comment: At least one gate should fail

### Line 127
> **Code:** `failed_gates = [`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `name for name, info in report["gates"].items()`
> **Type:** Logical operation

### Line 129
> **Code:** `if report["metrics"][info["metric"]] < info["value"]`
> **Type:** Conditional statement

### Line 130
> **Code:** `]`
> **Type:** Code statement

### Line 131
> **Code:** `assert len(failed_gates) > 0`
> **Type:** Enforces a condition

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 134
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 135
> **Code:** `def test_evaluate_uses_default_thresholds(self, mock_load_test, mock_r...`
> **Type:** Function definition

### Line 136
> **Code:** `"""evaluate should use DEFAULT_THRESHOLDS when none provided."""`
> **Type:** Code statement

### Line 137
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line 138
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `mock_resolve_model.return_value = self._create_mock_model(f1=0.9, accu...`
> **Type:** Assignment/comparison

### Line 140
> **Code:** ``
> **Type:** Empty line

### Line 141
> **Code:** `report = evaluate()`
> **Type:** Assignment/comparison

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** `assert report["thresholds"]["min_f1"] == DEFAULT_THRESHOLDS["min_f1"]`
> **Type:** Enforces a condition

### Line 144
> **Code:** `assert report["thresholds"]["min_accuracy"] == DEFAULT_THRESHOLDS["min...`
> **Type:** Enforces a condition

### Line 145
> **Code:** `assert report["thresholds"]["min_roc_auc"] == DEFAULT_THRESHOLDS["min_...`
> **Type:** Enforces a condition

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 148
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 149
> **Code:** `def test_evaluate_merges_custom_thresholds_with_defaults(self, mock_lo...`
> **Type:** Function definition

### Line 150
> **Code:** `"""Custom thresholds should override defaults, others kept."""`
> **Type:** Code statement

### Line 151
> **Code:** `features, labels = self._create_test_data(100)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `mock_resolve_model.return_value = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `report = evaluate(thresholds={"min_f1": 0.99})  # Only override f1`
> **Type:** Assignment/comparison

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `assert report["thresholds"]["min_f1"] == 0.99`
> **Type:** Enforces a condition

### Line 158
> **Code:** `assert report["thresholds"]["min_accuracy"] == DEFAULT_THRESHOLDS["min...`
> **Type:** Enforces a condition

### Line 159
> **Code:** `assert report["thresholds"]["min_roc_auc"] == DEFAULT_THRESHOLDS["min_...`
> **Type:** Enforces a condition

### Line 160
> **Code:** ``
> **Type:** Empty line

### Line 161
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 162
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 163
> **Code:** `def test_evaluate_writes_report_file(self, mock_load_test, mock_resolv...`
> **Type:** Function definition

### Line 164
> **Code:** `"""evaluate should write report to LATEST_REPORT."""`
> **Type:** Logical operation

### Line 165
> **Code:** `features, labels = self._create_test_data(50)`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 167
> **Code:** `mock_resolve_model.return_value = self._create_mock_model()`
> **Type:** Assignment/comparison

### Line 168
> **Code:** ``
> **Type:** Empty line

### Line 169
> **Code:** `# Patch the report path`
> **Type:** Comment: Patch the report path

### Line 170
> **Code:** `with patch("src.models.evaluate.LATEST_REPORT", tmp_path / "latest_rep...`
> **Type:** Context manager

### Line 171
> **Code:** `with patch("src.models.evaluate.EVALUATION_DIR", tmp_path):`
> **Type:** Context manager

### Line 172
> **Code:** `report = evaluate()`
> **Type:** Assignment/comparison

### Line 173
> **Code:** ``
> **Type:** Empty line

### Line 174
> **Code:** `report_file = tmp_path / "latest_report.json"`
> **Type:** Assignment/comparison

### Line 175
> **Code:** `assert report_file.exists()`
> **Type:** Enforces a condition

### Line 176
> **Code:** ``
> **Type:** Empty line

### Line 177
> **Code:** `with report_file.open() as f:`
> **Type:** Context manager

### Line 178
> **Code:** `saved_report = json.load(f)`
> **Type:** Assignment/comparison

### Line 179
> **Code:** `assert saved_report["gates_passed"] == report["gates_passed"]`
> **Type:** Enforces a condition

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** `def test_load_test_set_prefers_reference_csv(self, tmp_path, monkeypat...`
> **Type:** Function definition

### Line 182
> **Code:** `"""_load_test_set should prefer reference.csv when available."""`
> **Type:** Code statement

### Line 183
> **Code:** `# Create reference.csv with test data`
> **Type:** Comment: Create reference.csv with test data

### Line 184
> **Code:** `reference_dir = tmp_path / "data" / "monitoring"`
> **Type:** Assignment/comparison

### Line 185
> **Code:** `reference_dir.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 186
> **Code:** ``
> **Type:** Empty line

### Line 187
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 188
> **Code:** `col: np.random.randn(50) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line 189
> **Code:** `})`
> **Type:** Code statement

### Line 190
> **Code:** `features["label"] = np.random.choice([0, 1], 50)`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `features["prediction"] = np.random.uniform(0, 1, 50)`
> **Type:** Assignment/comparison

### Line 192
> **Code:** ``
> **Type:** Empty line

### Line 193
> **Code:** `ref_path = reference_dir / "reference.csv"`
> **Type:** Assignment/comparison

### Line 194
> **Code:** `features.to_csv(ref_path, index=False)`
> **Type:** Assignment/comparison

### Line 195
> **Code:** ``
> **Type:** Empty line

### Line 196
> **Code:** `# Mock PROJECT_ROOT to point to tmp_path`
> **Type:** Comment: Mock PROJECT_ROOT to point to tmp_path

### Line 197
> **Code:** `with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):`
> **Type:** Context manager

### Line 198
> **Code:** `X_test, y_test = _load_test_set(tmp_path / "features.parquet")`
> **Type:** Assignment/comparison

### Line 199
> **Code:** ``
> **Type:** Empty line

### Line 200
> **Code:** `assert len(X_test) == 50`
> **Type:** Enforces a condition

### Line 201
> **Code:** `assert len(y_test) == 50`
> **Type:** Enforces a condition

### Line 202
> **Code:** `assert list(X_test.columns) == FEATURE_ORDER`
> **Type:** Enforces a condition

### Line 203
> **Code:** ``
> **Type:** Empty line

### Line 204
> **Code:** `def test_load_test_set_fallback_to_parquet(self, tmp_path):`
> **Type:** Function definition

### Line 205
> **Code:** `"""_load_test_set should fall back to parquet when no reference.csv.""...`
> **Type:** Code statement

### Line 206
> **Code:** `# Create parquet file`
> **Type:** Comment: Create parquet file

### Line 207
> **Code:** `features_dir = tmp_path / "data" / "features"`
> **Type:** Assignment/comparison

### Line 208
> **Code:** `features_dir.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 209
> **Code:** ``
> **Type:** Empty line

### Line 210
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 211
> **Code:** `col: np.random.randn(100) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line 212
> **Code:** `})`
> **Type:** Code statement

### Line 213
> **Code:** `features[TARGET_FEATURE] = np.random.choice([0, 1], 100)`
> **Type:** Assignment/comparison

### Line 214
> **Code:** ``
> **Type:** Empty line

### Line 215
> **Code:** `parquet_path = features_dir / "features.parquet"`
> **Type:** Assignment/comparison

### Line 216
> **Code:** `features.to_parquet(parquet_path, index=False)`
> **Type:** Assignment/comparison

### Line 217
> **Code:** ``
> **Type:** Empty line

### Line 218
> **Code:** `with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):`
> **Type:** Context manager

### Line 219
> **Code:** `with patch("src.models.evaluate.DEFAULT_DATA", parquet_path):`
> **Type:** Context manager

### Line 220
> **Code:** `X_test, y_test = _load_test_set(parquet_path)`
> **Type:** Assignment/comparison

### Line 221
> **Code:** ``
> **Type:** Empty line

### Line 222
> **Code:** `assert len(X_test) == 100`
> **Type:** Enforces a condition

### Line 223
> **Code:** `assert len(y_test) == 100`
> **Type:** Enforces a condition

### Line 224
> **Code:** ``
> **Type:** Empty line

### Line 225
> **Code:** `def test_load_test_set_samples_large_dataset(self, tmp_path):`
> **Type:** Function definition

### Line 226
> **Code:** `"""_load_test_set should sample large datasets to 5000 rows."""`
> **Type:** Code statement

### Line 227
> **Code:** `features_dir = tmp_path / "data" / "features"`
> **Type:** Assignment/comparison

### Line 228
> **Code:** `features_dir.mkdir(parents=True)`
> **Type:** Assignment/comparison

### Line 229
> **Code:** ``
> **Type:** Empty line

### Line 230
> **Code:** `features = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line 231
> **Code:** `col: np.random.randn(10000) for col in FEATURE_ORDER`
> **Type:** Logical operation

### Line 232
> **Code:** `})`
> **Type:** Code statement

### Line 233
> **Code:** `features[TARGET_FEATURE] = np.random.choice([0, 1], 10000)`
> **Type:** Assignment/comparison

### Line 234
> **Code:** ``
> **Type:** Empty line

### Line 235
> **Code:** `parquet_path = features_dir / "features.parquet"`
> **Type:** Assignment/comparison

### Line 236
> **Code:** `features.to_parquet(parquet_path, index=False)`
> **Type:** Assignment/comparison

### Line 237
> **Code:** ``
> **Type:** Empty line

### Line 238
> **Code:** `with patch("src.models.evaluate.PROJECT_ROOT", tmp_path):`
> **Type:** Context manager

### Line 239
> **Code:** `with patch("src.models.evaluate.DEFAULT_DATA", parquet_path):`
> **Type:** Context manager

### Line 240
> **Code:** `X_test, y_test = _load_test_set(parquet_path)`
> **Type:** Assignment/comparison

### Line 241
> **Code:** ``
> **Type:** Empty line

### Line 242
> **Code:** `assert len(X_test) == 5000`
> **Type:** Enforces a condition

### Line 243
> **Code:** `assert len(y_test) == 5000`
> **Type:** Enforces a condition

### Line 244
> **Code:** ``
> **Type:** Empty line

### Line 245
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 246
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 247
> **Code:** `def test_evaluate_model_with_perfect_predictions(self, mock_load_test,...`
> **Type:** Function definition

### Line 248
> **Code:** `"""evaluate_model should handle perfect predictions (f1=1.0)."""`
> **Type:** Assignment/comparison

### Line 249
> **Code:** `features, labels = self._create_test_data(50)`
> **Type:** Assignment/comparison

### Line 250
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 251
> **Code:** ``
> **Type:** Empty line

### Line 252
> **Code:** `# Perfect model - predicts exactly the labels`
> **Type:** Comment: Perfect model - predicts exactly the labels

### Line 253
> **Code:** `model = MagicMock()`
> **Type:** Assignment/comparison

### Line 254
> **Code:** `model.predict.return_value = labels.values`
> **Type:** Assignment/comparison

### Line 255
> **Code:** `model.predict_proba.return_value = np.column_stack([1 - labels.values,...`
> **Type:** Assignment/comparison

### Line 256
> **Code:** `mock_resolve_model.return_value = model`
> **Type:** Assignment/comparison

### Line 257
> **Code:** ``
> **Type:** Empty line

### Line 258
> **Code:** `metrics = evaluate_model(model, features, labels)`
> **Type:** Assignment/comparison

### Line 259
> **Code:** ``
> **Type:** Empty line

### Line 260
> **Code:** `assert metrics["f1"] == 1.0`
> **Type:** Enforces a condition

### Line 261
> **Code:** `assert metrics["accuracy"] == 1.0`
> **Type:** Enforces a condition

### Line 262
> **Code:** `assert metrics["precision"] == 1.0`
> **Type:** Enforces a condition

### Line 263
> **Code:** `assert metrics["recall"] == 1.0`
> **Type:** Enforces a condition

### Line 264
> **Code:** ``
> **Type:** Empty line

### Line 265
> **Code:** `@patch("src.models.evaluate._resolve_model")`
> **Type:** Function call

### Line 266
> **Code:** `@patch("src.models.evaluate._load_test_set")`
> **Type:** Function call

### Line 267
> **Code:** `def test_evaluate_model_with_worst_predictions(self, mock_load_test, m...`
> **Type:** Function definition

### Line 268
> **Code:** `"""evaluate_model should handle worst predictions (f1=0.0)."""`
> **Type:** Assignment/comparison

### Line 269
> **Code:** `features, labels = self._create_test_data(50)`
> **Type:** Assignment/comparison

### Line 270
> **Code:** `mock_load_test.return_value = (features, labels)`
> **Type:** Assignment/comparison

### Line 271
> **Code:** ``
> **Type:** Empty line

### Line 272
> **Code:** `# Worst model - predicts opposite of labels`
> **Type:** Comment: Worst model - predicts opposite of labels

### Line 273
> **Code:** `model = MagicMock()`
> **Type:** Assignment/comparison

### Line 274
> **Code:** `model.predict.return_value = 1 - labels.values`
> **Type:** Assignment/comparison

### Line 275
> **Code:** `model.predict_proba.return_value = np.column_stack([labels.values, 1 -...`
> **Type:** Assignment/comparison

### Line 276
> **Code:** `mock_resolve_model.return_value = model`
> **Type:** Assignment/comparison

### Line 277
> **Code:** ``
> **Type:** Empty line

### Line 278
> **Code:** `metrics = evaluate_model(model, features, labels)`
> **Type:** Assignment/comparison

### Line 279
> **Code:** ``
> **Type:** Empty line

### Line 280
> **Code:** `assert metrics["f1"] == 0.0`
> **Type:** Enforces a condition

### Line 281
> **Code:** `assert metrics["accuracy"] == 0.0`
> **Type:** Enforces a condition

### Line 282
> **Code:** ``
> **Type:** Empty line

### Line 283
> **Code:** ``
> **Type:** Empty line

### Line 284
> **Code:** `class TestEvaluateIntegration:`
> **Type:** Class definition

### Line 285
> **Code:** `"""Integration-style tests for evaluate.py with real models (skipped b...`
> **Type:** Arithmetic operation

### Line 286
> **Code:** ``
> **Type:** Empty line

### Line 287
> **Code:** `@pytest.mark.skip(reason="Requires trained model and full environment"...`
> **Type:** Assignment/comparison

### Line 288
> **Code:** `def test_evaluate_with_real_model(self):`
> **Type:** Function definition

### Line 289
> **Code:** `"""Test evaluate with a real trained model from MLflow."""`
> **Type:** Code statement

### Line 290
> **Code:** `pytest.skip("Integration test - requires MLflow server and trained mod...`
> **Type:** Arithmetic operation

### Line 291
> **Code:** ``
> **Type:** Empty line

### Line 292
> **Code:** ``
> **Type:** Empty line

### Line 293
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 294
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 294
- **Code lines:** 219
- **Comments:** 12
- **TODO items:** 3
- **Empty lines:** 60

---
*Documentation generated for: mlops-project-documentation*
*File: test_evaluate.py*
---

# mlops-project-documentation: test_api.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/unit/test_api.py`
- **Total lines:** 190
- **File size:** 6813 bytes

## Line Type Summary
- **Code:** 150
- **Comment:** 2
- **Empty:** 35
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for FastAPI inference API."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** `from unittest.mock import MagicMock, patch`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  12
> **Code:** `from fastapi.testclient import TestClient`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  16
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `from src.api.main import app`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from src.api.schemas import ChurnPredictionRequest, PredictionResponse`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `client = TestClient(app)`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `def _valid_payload() -> dict:`
> **Type:** Function definition

### Line  26
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  27
> **Code:** `"Gender": "Male",`
> **Type:** Code statement

### Line  28
> **Code:** `"SeniorCitizen": 0,`
> **Type:** Logical operation

### Line  29
> **Code:** `"Partner": "Yes",`
> **Type:** Code statement

### Line  30
> **Code:** `"Dependents": "No",`
> **Type:** Code statement

### Line  31
> **Code:** `"Tenure": 12,`
> **Type:** Code statement

### Line  32
> **Code:** `"PhoneService": "Yes",`
> **Type:** Code statement

### Line  33
> **Code:** `"MultipleLines": "No",`
> **Type:** Code statement

### Line  34
> **Code:** `"InternetService": "DSL",`
> **Type:** Code statement

### Line  35
> **Code:** `"OnlineSecurity": "Yes",`
> **Type:** Code statement

### Line  36
> **Code:** `"OnlineBackup": "No",`
> **Type:** Code statement

### Line  37
> **Code:** `"DeviceProtection": "No",`
> **Type:** Code statement

### Line  38
> **Code:** `"TechSupport": "Yes",`
> **Type:** Logical operation

### Line  39
> **Code:** `"StreamingTV": "No",`
> **Type:** Code statement

### Line  40
> **Code:** `"StreamingMovies": "No",`
> **Type:** Code statement

### Line  41
> **Code:** `"Contract": "Month-to-month",`
> **Type:** Arithmetic operation

### Line  42
> **Code:** `"PaperlessBilling": "No",`
> **Type:** Code statement

### Line  43
> **Code:** `"PaymentMethod": "Electronic check",`
> **Type:** Code statement

### Line  44
> **Code:** `"MonthlyCharges": 50.0,`
> **Type:** Code statement

### Line  45
> **Code:** `"TotalCharges": 600.0,`
> **Type:** Code statement

### Line  46
> **Code:** `}`
> **Type:** Code statement

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `class TestHealthEndpoint:`
> **Type:** Class definition

### Line  50
> **Code:** `"""Test /health endpoint."""`
> **Type:** Arithmetic operation

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def test_health_returns_200(self):`
> **Type:** Function definition

### Line  53
> **Code:** `"""GET /health should return 200 with status ok or degraded."""`
> **Type:** Arithmetic operation

### Line  54
> **Code:** `response = client.get("/health")`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line  56
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `assert "status" in data`
> **Type:** Enforces a condition

### Line  58
> **Code:** `assert data["status"] in ("ok", "degraded")`
> **Type:** Enforces a condition

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `class TestPredictEndpoint:`
> **Type:** Class definition

### Line  62
> **Code:** `"""Test /predict endpoint."""`
> **Type:** Arithmetic operation

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `@patch("src.api.main.loader.get_bundle")`
> **Type:** Function call

### Line  65
> **Code:** `def test_predict_valid_payload_returns_prediction_and_probability(self...`
> **Type:** Function definition

### Line  66
> **Code:** `"""POST /predict with valid payload returns prediction (0/1) and proba...`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `mock_bundle = MagicMock()`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `mock_bundle.model_name = "churn_model"`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `mock_bundle.version = "1"`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `mock_bundle.predict_proba.return_value = [[0.3, 0.7]]  # [prob_class_0...`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `mock_get_bundle.return_value = mock_bundle`
> **Type:** Assignment/comparison

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `response = client.post("/predict", json=_valid_payload())`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line  75
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `assert "prediction" in data`
> **Type:** Enforces a condition

### Line  77
> **Code:** `assert "probability" in data`
> **Type:** Enforces a condition

### Line  78
> **Code:** `assert data["prediction"] in (0, 1)`
> **Type:** Enforces a condition

### Line  79
> **Code:** `assert 0.0 <= data["probability"] <= 1.0`
> **Type:** Enforces a condition

### Line  80
> **Code:** `assert data["model_name"] == "churn_model"`
> **Type:** Enforces a condition

### Line  81
> **Code:** `assert data["model_version"] == "1"`
> **Type:** Enforces a condition

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `@patch("src.api.main.loader.get_bundle")`
> **Type:** Function call

### Line  84
> **Code:** `def test_predict_batch_returns_list(self, mock_get_bundle):`
> **Type:** Function definition

### Line  85
> **Code:** `"""POST /predict with list payload returns list of predictions."""`
> **Type:** Arithmetic operation

### Line  86
> **Code:** `mock_bundle = MagicMock()`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `mock_bundle.model_name = "churn_model"`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `mock_bundle.version = "1"`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `mock_bundle.predict_proba.return_value = [[0.3, 0.7], [0.8, 0.2]]`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `mock_get_bundle.return_value = mock_bundle`
> **Type:** Assignment/comparison

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `payload = [_valid_payload(), _valid_payload()]`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `response = client.post("/predict", json=payload)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line  95
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `assert isinstance(data, list)`
> **Type:** Enforces a condition

### Line  97
> **Code:** `assert len(data) == 2`
> **Type:** Enforces a condition

### Line  98
> **Code:** `for item in data:`
> **Type:** For loop

### Line  99
> **Code:** `assert "prediction" in item`
> **Type:** Enforces a condition

### Line 100
> **Code:** `assert "probability" in item`
> **Type:** Enforces a condition

### Line 101
> **Code:** `assert item["prediction"] in (0, 1)`
> **Type:** Enforces a condition

### Line 102
> **Code:** `assert 0.0 <= item["probability"] <= 1.0`
> **Type:** Enforces a condition

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `def test_predict_invalid_payload_returns_422(self):`
> **Type:** Function definition

### Line 105
> **Code:** `"""POST /predict with invalid payload returns 422."""`
> **Type:** Arithmetic operation

### Line 106
> **Code:** `invalid_payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `invalid_payload["Gender"] = "Invalid"  # not in Literal`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `response = client.post("/predict", json=invalid_payload)`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `assert response.status_code == 422`
> **Type:** Enforces a condition

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `def test_predict_empty_batch_returns_422(self):`
> **Type:** Function definition

### Line 112
> **Code:** `"""POST /predict with empty list returns 422."""`
> **Type:** Arithmetic operation

### Line 113
> **Code:** `response = client.post("/predict", json=[])`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `assert response.status_code == 422`
> **Type:** Enforces a condition

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `def test_predict_missing_fields_returns_422(self):`
> **Type:** Function definition

### Line 117
> **Code:** `"""POST /predict with missing required fields returns 422."""`
> **Type:** Arithmetic operation

### Line 118
> **Code:** `response = client.post("/predict", json={})`
> **Type:** Assignment/comparison

### Line 119
> **Code:** `assert response.status_code == 422`
> **Type:** Enforces a condition

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** ``
> **Type:** Empty line

### Line 122
> **Code:** `class TestMetricsEndpoint:`
> **Type:** Class definition

### Line 123
> **Code:** `"""Test /metrics endpoint."""`
> **Type:** Arithmetic operation

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `def test_metrics_exposes_prometheus_metrics(self):`
> **Type:** Function definition

### Line 126
> **Code:** `"""GET /metrics should return Prometheus metrics text."""`
> **Type:** Arithmetic operation

### Line 127
> **Code:** `response = client.get("/metrics")`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line 129
> **Code:** `content = response.text`
> **Type:** Assignment/comparison

### Line 130
> **Code:** `# Check for standard prometheus-fastapi-instrumentator metrics`
> **Type:** Comment: Check for standard prometheus-fastapi-instrumentator metrics

### Line 131
> **Code:** `assert "http_requests_total" in content or "http_request_duration_seco...`
> **Type:** Enforces a condition

### Line 132
> **Code:** `# Check for our custom metrics`
> **Type:** Comment: Check for our custom metrics

### Line 133
> **Code:** `assert "model_prediction_value" in content or "predictions_total" in c...`
> **Type:** Enforces a condition

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `class TestModelInfoEndpoint:`
> **Type:** Class definition

### Line 137
> **Code:** `"""Test /model-info endpoint."""`
> **Type:** Arithmetic operation

### Line 138
> **Code:** ``
> **Type:** Empty line

### Line 139
> **Code:** `@patch("src.api.main.loader.get_bundle")`
> **Type:** Function call

### Line 140
> **Code:** `def test_model_info_returns_metadata(self, mock_get_bundle):`
> **Type:** Function definition

### Line 141
> **Code:** `"""GET /model-info should return model metadata."""`
> **Type:** Arithmetic operation

### Line 142
> **Code:** `mock_bundle = MagicMock()`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `mock_bundle.model_name = "churn_model"`
> **Type:** Assignment/comparison

### Line 144
> **Code:** `mock_bundle.version = "3"`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `mock_bundle.run_id = "abc123"`
> **Type:** Assignment/comparison

### Line 146
> **Code:** `mock_get_bundle.return_value = mock_bundle`
> **Type:** Assignment/comparison

### Line 147
> **Code:** ``
> **Type:** Empty line

### Line 148
> **Code:** `response = client.get("/model-info")`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `assert response.status_code == 200`
> **Type:** Enforces a condition

### Line 150
> **Code:** `data = response.json()`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `assert data["model_name"] == "churn_model"`
> **Type:** Enforces a condition

### Line 152
> **Code:** `assert data["model_version"] == "3"`
> **Type:** Enforces a condition

### Line 153
> **Code:** `assert data["run_id"] == "abc123"`
> **Type:** Enforces a condition

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** `class TestSchemas:`
> **Type:** Class definition

### Line 157
> **Code:** `"""Test Pydantic request/response schemas."""`
> **Type:** Arithmetic operation

### Line 158
> **Code:** ``
> **Type:** Empty line

### Line 159
> **Code:** `def test_churn_prediction_request_valid(self):`
> **Type:** Function definition

### Line 160
> **Code:** `"""Valid payload should create ChurnPredictionRequest."""`
> **Type:** Code statement

### Line 161
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 162
> **Code:** `request = ChurnPredictionRequest(**payload)`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `df = request.to_dataframe()`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `assert len(df) == 1`
> **Type:** Enforces a condition

### Line 165
> **Code:** `assert list(df.columns) == list(payload.keys())`
> **Type:** Enforces a condition

### Line 166
> **Code:** ``
> **Type:** Empty line

### Line 167
> **Code:** `def test_churn_prediction_request_invalid_gender(self):`
> **Type:** Function definition

### Line 168
> **Code:** `"""Invalid gender should raise validation error."""`
> **Type:** Logical operation

### Line 169
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 170
> **Code:** `payload["Gender"] = "Invalid"`
> **Type:** Assignment/comparison

### Line 171
> **Code:** `with pytest.raises(Exception):`
> **Type:** Context manager

### Line 172
> **Code:** `ChurnPredictionRequest(**payload)`
> **Type:** Arithmetic operation

### Line 173
> **Code:** ``
> **Type:** Empty line

### Line 174
> **Code:** `def test_churn_prediction_request_invalid_tenure(self):`
> **Type:** Function definition

### Line 175
> **Code:** `"""Negative tenure should raise validation error."""`
> **Type:** Logical operation

### Line 176
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 177
> **Code:** `payload["Tenure"] = -5`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `with pytest.raises(Exception):`
> **Type:** Context manager

### Line 179
> **Code:** `ChurnPredictionRequest(**payload)`
> **Type:** Arithmetic operation

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** `def test_churn_prediction_request_invalid_monthly_charges(self):`
> **Type:** Function definition

### Line 182
> **Code:** `"""Negative monthly charges should raise validation error."""`
> **Type:** Logical operation

### Line 183
> **Code:** `payload = _valid_payload()`
> **Type:** Assignment/comparison

### Line 184
> **Code:** `payload["MonthlyCharges"] = -10.0`
> **Type:** Assignment/comparison

### Line 185
> **Code:** `with pytest.raises(Exception):`
> **Type:** Context manager

### Line 186
> **Code:** `ChurnPredictionRequest(**payload)`
> **Type:** Arithmetic operation

### Line 187
> **Code:** ``
> **Type:** Empty line

### Line 188
> **Code:** ``
> **Type:** Empty line

### Line 189
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 190
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 190
- **Code lines:** 150
- **Comments:** 2
- **TODO items:** 3
- **Empty lines:** 35

---
*Documentation generated for: mlops-project-documentation*
*File: test_api.py*
---

# mlops-project-documentation: test_data_quality.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/tests/data/test_data_quality.py`
- **Total lines:** 130
- **File size:** 5153 bytes

## Line Type Summary
- **Code:** 97
- **Comment:** 0
- **Empty:** 30
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Tests for data quality validation using Great Expectations."""`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `import json`
> **Type:** Imports a module

### Line   7
> **Code:** `import sys`
> **Type:** Imports a module

### Line   8
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  11
> **Code:** `import pytest`
> **Type:** Imports a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `DATA_PATH = PROJECT_ROOT / "data" / "raw" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `EXPECTATIONS_PATH = PROJECT_ROOT / "great_expectations" / "expectation...`
> **Type:** Assignment/comparison

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `class TestDataQuality:`
> **Type:** Class definition

### Line  22
> **Code:** `"""Validate the committed dataset against the Great Expectations suite...`
> **Type:** Code statement

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `@pytest.fixture(scope="class")`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `def dataset(self):`
> **Type:** Function definition

### Line  26
> **Code:** `"""Load the raw dataset."""`
> **Type:** Code statement

### Line  27
> **Code:** `if not DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  28
> **Code:** `pytest.skip(f"Dataset not found at {DATA_PATH}")`
> **Type:** Logical operation

### Line  29
> **Code:** `return pd.read_csv(DATA_PATH)`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `@pytest.fixture(scope="class")`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `def expectations(self):`
> **Type:** Function definition

### Line  33
> **Code:** `"""Load the expectation suite."""`
> **Type:** Code statement

### Line  34
> **Code:** `if not EXPECTATIONS_PATH.exists():`
> **Type:** Conditional statement

### Line  35
> **Code:** `pytest.skip(f"Expectations not found at {EXPECTATIONS_PATH}")`
> **Type:** Logical operation

### Line  36
> **Code:** `with EXPECTATIONS_PATH.open() as f:`
> **Type:** Context manager

### Line  37
> **Code:** `return json.load(f)`
> **Type:** Returns a value from a function

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def test_dataset_exists(self, dataset):`
> **Type:** Function definition

### Line  40
> **Code:** `"""Dataset file should exist and be readable."""`
> **Type:** Logical operation

### Line  41
> **Code:** `assert len(dataset) > 0`
> **Type:** Enforces a condition

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `def test_expectations_exist(self, expectations):`
> **Type:** Function definition

### Line  44
> **Code:** `"""Expectations suite should exist and be valid."""`
> **Type:** Logical operation

### Line  45
> **Code:** `assert "expectations" in expectations`
> **Type:** Enforces a condition

### Line  46
> **Code:** `assert len(expectations["expectations"]) > 0`
> **Type:** Enforces a condition

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def test_row_count_between(self, dataset):`
> **Type:** Function definition

### Line  49
> **Code:** `"""Row count should be between 1000 and 5M."""`
> **Type:** Logical operation

### Line  50
> **Code:** `min_val = 1000`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `max_val = 5_000_000`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `assert min_val <= len(dataset) <= max_val`
> **Type:** Enforces a condition

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `def test_critical_columns_not_null(self, dataset):`
> **Type:** Function definition

### Line  55
> **Code:** `"""Critical columns should have no null values."""`
> **Type:** Code statement

### Line  56
> **Code:** `for col in ["Tenure", "MonthlyCharges", "TotalCharges", "Churn"]:`
> **Type:** For loop

### Line  57
> **Code:** `assert col in dataset.columns, f"Missing column: {col}"`
> **Type:** Enforces a condition

### Line  58
> **Code:** `assert dataset[col].notna().all(), f"Column {col} has null values"`
> **Type:** Enforces a condition

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `def test_tenure_range(self, dataset):`
> **Type:** Function definition

### Line  61
> **Code:** `"""Tenure should be between 0 and 120."""`
> **Type:** Logical operation

### Line  62
> **Code:** `assert dataset["Tenure"].between(0, 120).all()`
> **Type:** Enforces a condition

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def test_monthly_charges_range(self, dataset):`
> **Type:** Function definition

### Line  65
> **Code:** `"""MonthlyCharges should be between 0 and 1000."""`
> **Type:** Logical operation

### Line  66
> **Code:** `assert dataset["MonthlyCharges"].between(0, 1000).all()`
> **Type:** Enforces a condition

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def test_total_charges_range(self, dataset):`
> **Type:** Function definition

### Line  69
> **Code:** `"""TotalCharges should be between 0 and 100000."""`
> **Type:** Logical operation

### Line  70
> **Code:** `assert dataset["TotalCharges"].between(0, 100_000).all()`
> **Type:** Enforces a condition

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `def test_gender_values(self, dataset):`
> **Type:** Function definition

### Line  73
> **Code:** `"""Gender should only contain Male or Female."""`
> **Type:** Logical operation

### Line  74
> **Code:** `assert set(dataset["Gender"].unique()).issubset({"Male", "Female"})`
> **Type:** Enforces a condition

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `def test_senior_citizen_values(self, dataset):`
> **Type:** Function definition

### Line  77
> **Code:** `"""SeniorCitizen should only be 0 or 1."""`
> **Type:** Logical operation

### Line  78
> **Code:** `assert set(dataset["SeniorCitizen"].unique()).issubset({0, 1})`
> **Type:** Enforces a condition

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def test_contract_values(self, dataset):`
> **Type:** Function definition

### Line  81
> **Code:** `"""Contract should only contain valid values."""`
> **Type:** Code statement

### Line  82
> **Code:** `valid = {"Month-to-month", "One year", "Two year"}`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `assert set(dataset["Contract"].unique()).issubset(valid)`
> **Type:** Enforces a condition

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def test_internet_service_values(self, dataset):`
> **Type:** Function definition

### Line  86
> **Code:** `"""InternetService should only contain valid values."""`
> **Type:** Code statement

### Line  87
> **Code:** `valid = {"DSL", "Fiber optic", "No"}`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `assert set(dataset["InternetService"].unique()).issubset(valid)`
> **Type:** Enforces a condition

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `def test_payment_method_values(self, dataset):`
> **Type:** Function definition

### Line  91
> **Code:** `"""PaymentMethod should only contain valid values."""`
> **Type:** Code statement

### Line  92
> **Code:** `valid = {"Electronic check", "Mailed check", "Bank transfer (automatic...`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `assert set(dataset["PaymentMethod"].unique()).issubset(valid)`
> **Type:** Enforces a condition

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `def test_churn_values(self, dataset):`
> **Type:** Function definition

### Line  96
> **Code:** `"""Churn should only contain Yes or No."""`
> **Type:** Logical operation

### Line  97
> **Code:** `assert set(dataset["Churn"].unique()).issubset({"Yes", "No"})`
> **Type:** Enforces a condition

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def test_tenure_type(self, dataset):`
> **Type:** Function definition

### Line 100
> **Code:** `"""Tenure should be integer type."""`
> **Type:** Code statement

### Line 101
> **Code:** `assert pd.api.types.is_integer_dtype(dataset["Tenure"])`
> **Type:** Enforces a condition

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `def test_monthly_charges_type(self, dataset):`
> **Type:** Function definition

### Line 104
> **Code:** `"""MonthlyCharges should be float type."""`
> **Type:** Code statement

### Line 105
> **Code:** `assert pd.api.types.is_float_dtype(dataset["MonthlyCharges"])`
> **Type:** Enforces a condition

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `def test_gender_no_digits(self, dataset):`
> **Type:** Function definition

### Line 108
> **Code:** `"""Gender column should not contain digits."""`
> **Type:** Logical operation

### Line 109
> **Code:** `assert not dataset["Gender"].astype(str).str.contains(r"[0-9]").any()`
> **Type:** Enforces a condition

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `@pytest.mark.skipif(`
> **Type:** Code statement

### Line 113
> **Code:** `True,  # Always skip the Great Expectations runtime validation - it's ...`
> **Type:** Arithmetic operation

### Line 114
> **Code:** `reason="Great Expectations runtime validation requires full GE install...`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `)`
> **Type:** Code statement

### Line 116
> **Code:** `class TestGreatExpectationsRuntime:`
> **Type:** Class definition

### Line 117
> **Code:** `"""Runtime validation using Great Expectations (requires GE installed)...`
> **Type:** Code statement

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** `def test_ge_runtime_validation(self, dataset, expectations):`
> **Type:** Function definition

### Line 120
> **Code:** `"""Run Great Expectations validation against the dataset."""`
> **Type:** Code statement

### Line 121
> **Code:** `pytest.importorskip("great_expectations")`
> **Type:** Logical operation

### Line 122
> **Code:** `from great_expectations.dataset import PandasDataset`
> **Type:** Imports specific names from a module

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `ge_dataset = PandasDataset(dataset)`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `results = ge_dataset.validate(expectations)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `assert results.success`
> **Type:** Enforces a condition

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 130
> **Code:** `pytest.main([__file__, "-v"])`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 130
- **Code lines:** 97
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 30

---
*Documentation generated for: mlops-project-documentation*
*File: test_data_quality.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/airflow/__init__.py`
- **Total lines:** 4
- **File size:** 208 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""airflow package: DAGs and operators for the churn MLOps pipeline.""...`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: training_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/airflow/dags/training_pipeline.py`
- **Total lines:** 108
- **File size:** 4047 bytes

## Line Type Summary
- **Code:** 80
- **Comment:** 0
- **Empty:** 25
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add data validation before training`
> **Type:** TODO: high - Add data validation before training

### Line   2
> **Code:** `# TODO: medium - Implement hyperparameter logging`
> **Type:** TODO: medium - Implement hyperparameter logging

### Line   3
> **Code:** `# TODO: low - Add model explainability integration`
> **Type:** TODO: low - Add model explainability integration

### Line   4
> **Code:** `"""DAG: full training pipeline.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Runs the complete model lifecycle on the current data snapshot:`
> **Type:** Code statement

### Line   7
> **Code:** `validate -> preprocess -> build_features -> train -> evaluate -> promo...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `The MLflow run_id produced by training is passed to the evaluation tas...`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import sys`
> **Type:** Imports a module

### Line  14
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from airflow.operators.python import PythonOperator`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from airflow.utils.dates import days_ago`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from airflow import DAG`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.data.preprocessing import preprocess  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from src.data.validation import validate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from src.features.build_features import build_features  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.models.evaluate import evaluate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** `from src.models.promote import promote_candidate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from src.models.train import train_model  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `from src.monitoring.alerting import send_alert  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `DAG_ID = "training_pipeline"`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `DEFAULT_ARGS = {`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `"owner": "mlops",`
> **Type:** Code statement

### Line  36
> **Code:** `"depends_on_past": False,`
> **Type:** Code statement

### Line  37
> **Code:** `"retries": 1,`
> **Type:** Code statement

### Line  38
> **Code:** `"retry_delay": timedelta(minutes=5),`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `"on_failure_callback": lambda context: send_alert(`
> **Type:** Code statement

### Line  40
> **Code:** `f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", se...`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `),`
> **Type:** Code statement

### Line  42
> **Code:** `}`
> **Type:** Code statement

### Line  43
> **Code:** `dag = DAG(`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `dag_id=DAG_ID,`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `default_args=DEFAULT_ARGS,`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `schedule_interval="@weekly",`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `start_date=days_ago(2),`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `catchup=False,`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `tags=["training", "mlflow"],`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `doc_md=(`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `"Validates data, rebuilds features, trains and registers a new churn m...`
> **Type:** Logical operation

### Line  52
> **Code:** `"then promotes it if it passes the gates."`
> **Type:** Code statement

### Line  53
> **Code:** `),`
> **Type:** Code statement

### Line  54
> **Code:** `)`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def _validate() -> str:`
> **Type:** Function definition

### Line  58
> **Code:** `summary = validate()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if summary["failed"]:`
> **Type:** Conditional statement

### Line  60
> **Code:** `raise RuntimeError(f"data validation failed: {summary['failed']} expec...`
> **Type:** Raises an exception

### Line  61
> **Code:** `return f"validation passed {summary['passed']}/{summary['total']}"`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def _preprocess() -> str:`
> **Type:** Function definition

### Line  65
> **Code:** `df = preprocess()`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `return f"preprocessed {len(df)} rows"`
> **Type:** Returns a value from a function

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def _build_features() -> str:`
> **Type:** Function definition

### Line  70
> **Code:** `features = build_features()`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `return f"built {features.shape[0]} rows x {features.shape[1]} features...`
> **Type:** Returns a value from a function

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `def _train(**context) -> str:`
> **Type:** Function definition

### Line  75
> **Code:** `result = train_model()`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `context["task_instance"].xcom_push(key="run_id", value=result["run_id"...`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `context["task_instance"].xcom_push(key="f1", value=result["metrics"]["...`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `return f"training completed run_id={result['run_id']} f1={result['metr...`
> **Type:** Returns a value from a function

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `def _evaluate(**context) -> str:`
> **Type:** Function definition

### Line  82
> **Code:** `run_id = context["task_instance"].xcom_pull(task_ids="train_model", ke...`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `report = evaluate(run_id=run_id)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `if not report["gates_passed"]:`
> **Type:** Conditional statement

### Line  85
> **Code:** `raise RuntimeError("evaluation gates not met; stopping before promotio...`
> **Type:** Raises an exception

### Line  86
> **Code:** `return f"evaluation passed f1={report['metrics']['f1']:.4f}"`
> **Type:** Returns a value from a function

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def _promote() -> str:`
> **Type:** Function definition

### Line  90
> **Code:** `production = promote_candidate()`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `return f"promoted version {production['version']} to production"`
> **Type:** Returns a value from a function

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `def _notify(**context) -> str:`
> **Type:** Function definition

### Line  95
> **Code:** `f1 = context["task_instance"].xcom_pull(task_ids="train_model", key="f...`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `send_alert(f"training_pipeline completed | f1={f1:.4f}", severity="inf...`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `return "notification sent"`
> **Type:** Returns a value from a function

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `validate_data = PythonOperator(task_id="validate_data", python_callabl...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `preprocess_data = PythonOperator(task_id="preprocess", python_callable...`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `build_features_task = PythonOperator(task_id="build_features", python_...`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `train_task = PythonOperator(task_id="train_model", python_callable=_tr...`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `evaluate_task = PythonOperator(task_id="evaluate_model", python_callab...`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `promote_task = PythonOperator(task_id="promote_model", python_callable...`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `notify_task = PythonOperator(task_id="notify_team", python_callable=_n...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `validate_data >> preprocess_data >> build_features_task >> train_task ...`
> **Type:** Comparison operation

## Summary
- **Total lines:** 108
- **Code lines:** 80
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 25

---
*Documentation generated for: mlops-project-documentation*
*File: training_pipeline.py*
---

# mlops-project-documentation: retraining_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/airflow/dags/retraining_pipeline.py`
- **Total lines:** 118
- **File size:** 4284 bytes

## Line Type Summary
- **Code:** 89
- **Comment:** 0
- **Empty:** 26
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add data validation before training`
> **Type:** TODO: high - Add data validation before training

### Line   2
> **Code:** `# TODO: medium - Implement hyperparameter logging`
> **Type:** TODO: medium - Implement hyperparameter logging

### Line   3
> **Code:** `# TODO: low - Add model explainability integration`
> **Type:** TODO: low - Add model explainability integration

### Line   4
> **Code:** `"""DAG: retraining triggered by drift detection.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Runs daily. The `check_drift` task short-circuits the pipeline: if no ...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `was detected by Evidently since the last run, nothing is retrained. On...`
> **Type:** Logical operation

### Line   8
> **Code:** `the full loop executes: preprocess -> features -> train -> evaluate ->`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `promote-if-better -> notify. Promotion only happens when the candidate...`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `the current production model on the same test set.`
> **Type:** Code statement

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import sys`
> **Type:** Imports a module

### Line  16
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `from airflow.operators.python import PythonOperator, ShortCircuitOpera...`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** `from airflow.utils.dates import days_ago`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `from airflow import DAG`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `from src.data.preprocessing import preprocess  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.features.build_features import build_features  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** `from src.models.evaluate import evaluate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from src.models.promote import promote_candidate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `from src.models.train import train_model  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** `from src.monitoring.alerting import send_alert  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  33
> **Code:** `from src.monitoring.drift_detection import detect_drift  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `DAG_ID = "retraining_pipeline"`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `DEFAULT_ARGS = {`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `"owner": "mlops",`
> **Type:** Code statement

### Line  38
> **Code:** `"depends_on_past": False,`
> **Type:** Code statement

### Line  39
> **Code:** `"retries": 1,`
> **Type:** Code statement

### Line  40
> **Code:** `"retry_delay": timedelta(minutes=5),`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `"on_failure_callback": lambda context: send_alert(`
> **Type:** Code statement

### Line  42
> **Code:** `f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", se...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `),`
> **Type:** Code statement

### Line  44
> **Code:** `}`
> **Type:** Code statement

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `dag = DAG(`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `dag_id=DAG_ID,`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `default_args=DEFAULT_ARGS,`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `schedule_interval="@daily",`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `start_date=days_ago(2),`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `catchup=False,`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `tags=["retraining", "drift"],`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `doc_md="Retrains the model when Evidently detects drift on the product...`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `)`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def _check_drift() -> bool:`
> **Type:** Function definition

### Line  58
> **Code:** `report = detect_drift()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if report["drift_detected"]:`
> **Type:** Conditional statement

### Line  60
> **Code:** `send_alert(`
> **Type:** Code statement

### Line  61
> **Code:** `"drift detected "`
> **Type:** Code statement

### Line  62
> **Code:** `f"(score={report['drift_score']:.3f}, threshold={report['threshold']})...`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `severity="warning",`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `dag=DAG_ID,`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `)`
> **Type:** Code statement

### Line  66
> **Code:** `return True`
> **Type:** Returns a value from a function

### Line  67
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `def _preprocess() -> str:`
> **Type:** Function definition

### Line  71
> **Code:** `df = preprocess()`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `return f"preprocessed {len(df)} rows"`
> **Type:** Returns a value from a function

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `def _build_features() -> str:`
> **Type:** Function definition

### Line  76
> **Code:** `features = build_features()`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `return f"built {features.shape[0]} rows x {features.shape[1]} features...`
> **Type:** Returns a value from a function

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def _train(**context) -> str:`
> **Type:** Function definition

### Line  81
> **Code:** `result = train_model()`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `context["task_instance"].xcom_push(key="run_id", value=result["run_id"...`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `return f"retraining completed run_id={result['run_id']} f1={result['me...`
> **Type:** Returns a value from a function

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def _evaluate(**context) -> str:`
> **Type:** Function definition

### Line  87
> **Code:** `run_id = context["task_instance"].xcom_pull(task_ids="train_model", ke...`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `report = evaluate(run_id=run_id)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `if not report["gates_passed"]:`
> **Type:** Conditional statement

### Line  90
> **Code:** `raise RuntimeError("evaluation gates not met; stopping before promotio...`
> **Type:** Raises an exception

### Line  91
> **Code:** `return f"evaluation passed f1={report['metrics']['f1']:.4f}"`
> **Type:** Returns a value from a function

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `def _promote() -> str:`
> **Type:** Function definition

### Line  95
> **Code:** `production = promote_candidate()`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `send_alert(`
> **Type:** Code statement

### Line  97
> **Code:** `f"retraining promoted model version {production['version']} to product...`
> **Type:** Data structure operation

### Line  98
> **Code:** `f"(f1={production['metrics']['f1']:.4f})",`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `severity="info",`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `dag=DAG_ID,`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `)`
> **Type:** Code statement

### Line 102
> **Code:** `return f"promoted version {production['version']}"`
> **Type:** Returns a value from a function

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `def _notify() -> str:`
> **Type:** Function definition

### Line 106
> **Code:** `send_alert("retraining_pipeline completed", severity="info", dag=DAG_I...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `return "notification sent"`
> **Type:** Returns a value from a function

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `check_drift = ShortCircuitOperator(task_id="check_drift", python_calla...`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `preprocess_task = PythonOperator(task_id="preprocess", python_callable...`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `build_features_task = PythonOperator(task_id="build_features", python_...`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `train_task = PythonOperator(task_id="train_model", python_callable=_tr...`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `evaluate_task = PythonOperator(task_id="evaluate_model", python_callab...`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `promote_task = PythonOperator(task_id="promote_model", python_callable...`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `notify_task = PythonOperator(task_id="notify_team", python_callable=_n...`
> **Type:** Assignment/comparison

### Line 117
> **Code:** ``
> **Type:** Empty line

### Line 118
> **Code:** `check_drift >> preprocess_task >> build_features_task >> train_task >>...`
> **Type:** Comparison operation

## Summary
- **Total lines:** 118
- **Code lines:** 89
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 26

---
*Documentation generated for: mlops-project-documentation*
*File: retraining_pipeline.py*
---

# mlops-project-documentation: data_ingestion_dag.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/airflow/dags/data_ingestion_dag.py`
- **Total lines:** 76
- **File size:** 2404 bytes

## Line Type Summary
- **Code:** 57
- **Comment:** 0
- **Empty:** 16
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add tag mapping version control`
> **Type:** TODO: high - Add tag mapping version control

### Line   2
> **Code:** `# TODO: medium - Implement store-and-forward buffer health checks`
> **Type:** TODO: medium - Implement store-and-forward buffer health checks

### Line   3
> **Code:** `# TODO: low - Add unmapped tag alerting`
> **Type:** TODO: low - Add unmapped tag alerting

### Line   4
> **Code:** `"""DAG: periodic data ingestion.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Scheduled every night: pulls the latest raw data, validates it with th...`
> **Type:** Code statement

### Line   7
> **Code:** `Great Expectations suite, then versions it with DVC and pushes it to t...`
> **Type:** Logical operation

### Line   8
> **Code:** `configured remote (MinIO). Failures raise an alert through the alertin...`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import sys`
> **Type:** Imports a module

### Line  14
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from airflow.operators.bash import BashOperator`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from airflow.operators.python import PythonOperator`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from airflow.utils.dates import days_ago`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `from airflow import DAG`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `from src.data.ingestion import ingest  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from src.data.validation import validate  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from src.monitoring.alerting import send_alert  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `DAG_ID = "data_ingestion_dag"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `DEFAULT_ARGS = {`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `"owner": "mlops",`
> **Type:** Code statement

### Line  33
> **Code:** `"depends_on_past": False,`
> **Type:** Code statement

### Line  34
> **Code:** `"retries": 2,`
> **Type:** Code statement

### Line  35
> **Code:** `"retry_delay": timedelta(minutes=5),`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `"on_failure_callback": lambda context: send_alert(`
> **Type:** Code statement

### Line  37
> **Code:** `f"DAG {DAG_ID} task {context.get('task_instance').task_id} failed", se...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `),`
> **Type:** Code statement

### Line  39
> **Code:** `}`
> **Type:** Code statement

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `dag = DAG(`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `dag_id=DAG_ID,`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `default_args=DEFAULT_ARGS,`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `schedule_interval="0 2 * * *",`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `start_date=days_ago(2),`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `catchup=False,`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `tags=["ingestion", "data"],`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `doc_md="Fetches, validates and DVC-versions the raw churn dataset ever...`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `)`
> **Type:** Code statement

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _ingest() -> str:`
> **Type:** Function definition

### Line  53
> **Code:** `df = ingest()`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `return f"ingested {len(df)} rows"`
> **Type:** Returns a value from a function

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def _validate() -> str:`
> **Type:** Function definition

### Line  58
> **Code:** `summary = validate()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if summary["failed"]:`
> **Type:** Conditional statement

### Line  60
> **Code:** `raise RuntimeError(f"data validation failed: {summary['failed']} expec...`
> **Type:** Raises an exception

### Line  61
> **Code:** `return f"validation passed {summary['passed']}/{summary['total']}"`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `ingest_data = PythonOperator(task_id="ingest_data", python_callable=_i...`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `validate_data = PythonOperator(task_id="validate_data", python_callabl...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `version_data = BashOperator(`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `task_id="version_data",`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `bash_command=(`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `"cd {{ dag_run.conf.get('project_root', '/opt/airflow') }} && "`
> **Type:** Arithmetic operation

### Line  70
> **Code:** `"dvc add data/raw/dataset.csv && dvc commit -f && "`
> **Type:** Arithmetic operation

### Line  71
> **Code:** `"(dvc remote list | grep -q . && dvc push || echo 'no dvc remote confi...`
> **Type:** Arithmetic operation

### Line  72
> **Code:** `),`
> **Type:** Code statement

### Line  73
> **Code:** `dag=dag,`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `)`
> **Type:** Code statement

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `ingest_data >> validate_data >> version_data`
> **Type:** Comparison operation

## Summary
- **Total lines:** 76
- **Code lines:** 57
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 16

---
*Documentation generated for: mlops-project-documentation*
*File: data_ingestion_dag.py*
---

# mlops-project-documentation: drift_sensor.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/airflow/plugins/drift_sensor.py`
- **Total lines:** 43
- **File size:** 1498 bytes

## Line Type Summary
- **Code:** 30
- **Comment:** 0
- **Empty:** 10
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Airflow plugin: drift sensor + shared DAG helpers.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** ``DriftDetectedSensor` polls the drift report produced by`
> **Type:** Logical operation

### Line   7
> **Code:** `src/monitoring/drift_detection.py and succeeds as soon as drift is det...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `which is how the retraining loop is triggered.`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import json`
> **Type:** Imports a module

### Line  14
> **Code:** `import os`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from airflow.plugins_manager import AirflowPlugin`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from airflow.sensors.base import BaseSensorOperator`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `class DriftDetectedSensor(BaseSensorOperator):`
> **Type:** Class definition

### Line  22
> **Code:** `template_fields = ("drift_report_path",)`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def __init__(self, drift_report_path: str | None = None, **kwargs):`
> **Type:** Function definition

### Line  25
> **Code:** `super().__init__(**kwargs)`
> **Type:** Arithmetic operation

### Line  26
> **Code:** `default = Path(os.environ.get("DRIFT_REPORT_PATH", "data/monitoring/dr...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `self.drift_report_path = drift_report_path or str(default)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def poke(self, context: dict) -> bool:`
> **Type:** Function definition

### Line  30
> **Code:** `report = Path(self.drift_report_path)`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `if not report.exists():`
> **Type:** Conditional statement

### Line  32
> **Code:** `self.log.info("drift report %s not found yet", report)`
> **Type:** Arithmetic operation

### Line  33
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  34
> **Code:** `with report.open() as fh:`
> **Type:** Context manager

### Line  35
> **Code:** `payload = json.load(fh)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `detected = bool(payload.get("drift_detected", False))`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `self.log.info("drift_detected=%s score=%s", detected, payload.get("dri...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `return detected`
> **Type:** Returns a value from a function

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `class DriftAlertPlugin(AirflowPlugin):`
> **Type:** Class definition

### Line  42
> **Code:** `name = "mlops_drift_plugin"`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `sensors = [DriftDetectedSensor]`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 43
- **Code lines:** 30
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 10

---
*Documentation generated for: mlops-project-documentation*
*File: drift_sensor.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/airflow/plugins/__init__.py`
- **Total lines:** 4
- **File size:** 195 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""airflow plugins package: custom hooks and operators."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/__init__.py`
- **Total lines:** 4
- **File size:** 201 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""src package: core source code for the churn MLOps project."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/models/__init__.py`
- **Total lines:** 4
- **File size:** 207 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""models package: training, evaluation, and MLflow registry logic."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: evaluate.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/models/evaluate.py`
- **Total lines:** 155
- **File size:** 5846 bytes

## Line Type Summary
- **Code:** 124
- **Comment:** 0
- **Empty:** 28
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add quality gate with thresholds`
> **Type:** TODO: high - Add quality gate with thresholds

### Line   2
> **Code:** `# TODO: medium - Implement comparison vs current production model`
> **Type:** TODO: medium - Implement comparison vs current production model

### Line   3
> **Code:** `# TODO: low - Add metrics export for Evidence Pack`
> **Type:** TODO: low - Add metrics export for Evidence Pack

### Line   4
> **Code:** `"""Model evaluation and validation gate.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Loads a candidate model (from an MLflow run or a local pickle), evalua...`
> **Type:** Logical operation

### Line   7
> **Code:** `on the held-out test features and compares it against configured quali...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `thresholds. Writes a JSON evaluation report; exits non-zero when the c...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `does not meet the gate so the pipeline stops before promotion.`
> **Type:** Logical operation

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `import os`
> **Type:** Imports a module

### Line  17
> **Code:** `import sys`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  22
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  25
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  26
> **Code:** `from sklearn.metrics import (`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `accuracy_score,`
> **Type:** Logical operation

### Line  28
> **Code:** `f1_score,`
> **Type:** Logical operation

### Line  29
> **Code:** `precision_score,`
> **Type:** Logical operation

### Line  30
> **Code:** `recall_score,`
> **Type:** Logical operation

### Line  31
> **Code:** `roc_auc_score,`
> **Type:** Logical operation

### Line  32
> **Code:** `)`
> **Type:** Code statement

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `from src.features.build_features import TARGET_FEATURE, FEATURE_ORDER`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config...`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `EVALUATION_DIR = PROJECT_ROOT / "models" / "evaluation"`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `LATEST_REPORT = EVALUATION_DIR / "latest_report.json"`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `DEFAULT_THRESHOLDS = {"min_f1": 0.35, "min_accuracy": 0.70, "min_roc_a...`
> **Type:** Assignment/comparison

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def _resolve_model(model_uri: str | None, run_id: str | None):`
> **Type:** Function definition

### Line  47
> **Code:** `if run_id:`
> **Type:** Conditional statement

### Line  48
> **Code:** `try:`
> **Type:** Code statement

### Line  49
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `return mlflow.sklearn.load_model(f"runs:/{run_id}/model")`
> **Type:** Returns a value from a function

### Line  52
> **Code:** `except Exception:  # nosec B110 - fallback to next source`
> **Type:** Arithmetic operation

### Line  53
> **Code:** `pass`
> **Type:** Code statement

### Line  54
> **Code:** `if model_uri:`
> **Type:** Conditional statement

### Line  55
> **Code:** `try:`
> **Type:** Code statement

### Line  56
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `return mlflow.sklearn.load_model(model_uri)`
> **Type:** Returns a value from a function

### Line  59
> **Code:** `except Exception:  # nosec B110 - fallback to local pickle`
> **Type:** Arithmetic operation

### Line  60
> **Code:** `pass`
> **Type:** Code statement

### Line  61
> **Code:** `if Path(DEFAULT_LOCAL_MODEL).exists():`
> **Type:** Conditional statement

### Line  62
> **Code:** `return joblib.load(DEFAULT_LOCAL_MODEL)`
> **Type:** Returns a value from a function

### Line  63
> **Code:** `raise FileNotFoundError("No candidate model found (run_id, model_uri o...`
> **Type:** Raises an exception

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `def _load_test_set(data_path: str | Path) -> tuple[pd.DataFrame, pd.Se...`
> **Type:** Function definition

### Line  67
> **Code:** `"""Prefer the held-out test set written by train.py (data/monitoring/r...`
> **Type:** Arithmetic operation

### Line  68
> **Code:** `fall back to the full feature dataset when it is not available."""`
> **Type:** Logical operation

### Line  69
> **Code:** `reference = PROJECT_ROOT / "data" / "monitoring" / "reference.csv"`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `if reference.exists():`
> **Type:** Conditional statement

### Line  71
> **Code:** `df = pd.read_csv(reference)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `return df[FEATURE_ORDER], df["label"].astype(int)`
> **Type:** Returns a value from a function

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `data_path = Path(data_path or DEFAULT_DATA)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `if not data_path.exists():`
> **Type:** Conditional statement

### Line  76
> **Code:** `raise FileNotFoundError(f"Feature dataset not found: {data_path}")`
> **Type:** Raises an exception

### Line  77
> **Code:** `features = pd.read_parquet(data_path)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `if len(features) > 5000:`
> **Type:** Conditional statement

### Line  79
> **Code:** `X_test = features.sample(n=5000, random_state=42)[FEATURE_ORDER]`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `y_test = features.loc[X_test.index, TARGET_FEATURE].astype(int)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `return X_test, y_test`
> **Type:** Returns a value from a function

### Line  82
> **Code:** `return features[FEATURE_ORDER], features[TARGET_FEATURE].astype(int)`
> **Type:** Returns a value from a function

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> ...`
> **Type:** Function definition

### Line  86
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `y_prob = model.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  89
> **Code:** `"f1": float(f1_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line  90
> **Code:** `"accuracy": float(accuracy_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line  91
> **Code:** `"precision": float(precision_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line  92
> **Code:** `"recall": float(recall_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line  93
> **Code:** `"roc_auc": float(roc_auc_score(y_test, y_prob)),`
> **Type:** Logical operation

### Line  94
> **Code:** `"n_samples": int(len(y_test)),`
> **Type:** Code statement

### Line  95
> **Code:** `}`
> **Type:** Code statement

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** `def evaluate(`
> **Type:** Function definition

### Line  99
> **Code:** `data_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `model_uri: str | None = None,`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `run_id: str | None = None,`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `thresholds: dict | None = None,`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line 104
> **Code:** `X_test, y_test = _load_test_set(data_path)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `model = _resolve_model(model_uri, run_id)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `metrics = evaluate_model(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** `thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `gates = {`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `"min_f1": {"metric": "f1", "value": thresholds["min_f1"]},`
> **Type:** Data structure operation

### Line 112
> **Code:** `"min_accuracy": {"metric": "accuracy", "value": thresholds["min_accura...`
> **Type:** Data structure operation

### Line 113
> **Code:** `"min_roc_auc": {"metric": "roc_auc", "value": thresholds["min_roc_auc"...`
> **Type:** Data structure operation

### Line 114
> **Code:** `}`
> **Type:** Code statement

### Line 115
> **Code:** `gates_passed = all(metrics[gate["metric"]] >= gate["value"] for gate i...`
> **Type:** Assignment/comparison

### Line 116
> **Code:** ``
> **Type:** Empty line

### Line 117
> **Code:** `report = {`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `"model_uri": model_uri or (f"runs:/{run_id}/model" if run_id else "loc...`
> **Type:** Arithmetic operation

### Line 119
> **Code:** `"run_id": run_id,`
> **Type:** Code statement

### Line 120
> **Code:** `"metrics": metrics,`
> **Type:** Code statement

### Line 121
> **Code:** `"thresholds": thresholds,`
> **Type:** Code statement

### Line 122
> **Code:** `"gates": gates,`
> **Type:** Code statement

### Line 123
> **Code:** `"gates_passed": gates_passed,`
> **Type:** Code statement

### Line 124
> **Code:** `}`
> **Type:** Code statement

### Line 125
> **Code:** `EVALUATION_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `with LATEST_REPORT.open("w") as fh:`
> **Type:** Context manager

### Line 127
> **Code:** `json.dump(report, fh, indent=2)`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `return report`
> **Type:** Returns a value from a function

### Line 129
> **Code:** ``
> **Type:** Empty line

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 132
> **Code:** `parser = argparse.ArgumentParser(description="Evaluate a candidate mod...`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `parser.add_argument("--data", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `parser.add_argument("--model-uri", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `parser.add_argument("--run-id", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `parser.add_argument("--min-f1", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `parser.add_argument("--min-accuracy", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 138
> **Code:** `parser.add_argument("--min-roc-auc", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 140
> **Code:** ``
> **Type:** Empty line

### Line 141
> **Code:** `thresholds = {}`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `for name, cli_arg in (("min_f1", args.min_f1), ("min_accuracy", args.m...`
> **Type:** For loop

### Line 143
> **Code:** `if cli_arg is not None:`
> **Type:** Conditional statement

### Line 144
> **Code:** `thresholds[name] = cli_arg`
> **Type:** Assignment/comparison

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** `report = evaluate(args.data, args.model_uri, args.run_id, thresholds)`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `print(f"evaluation: f1={report['metrics']['f1']:.4f} accuracy={report[...`
> **Type:** Prints output to console

### Line 148
> **Code:** `f"roc_auc={report['metrics']['roc_auc']:.4f} gates_passed={report['gat...`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `if not report["gates_passed"]:`
> **Type:** Conditional statement

### Line 150
> **Code:** `print(f"evaluation gates not met: {json.dumps(report['gates'])}", file...`
> **Type:** Prints output to console

### Line 151
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line 152
> **Code:** ``
> **Type:** Empty line

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 155
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 155
- **Code lines:** 124
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 28

---
*Documentation generated for: mlops-project-documentation*
*File: evaluate.py*
---

# mlops-project-documentation: train.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/models/train.py`
- **Total lines:** 197
- **File size:** 7934 bytes

## Line Type Summary
- **Code:** 163
- **Comment:** 0
- **Empty:** 31
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add data validation before training`
> **Type:** TODO: high - Add data validation before training

### Line   2
> **Code:** `# TODO: medium - Implement hyperparameter logging`
> **Type:** TODO: medium - Implement hyperparameter logging

### Line   3
> **Code:** `# TODO: low - Add model explainability integration`
> **Type:** TODO: low - Add model explainability integration

### Line   4
> **Code:** `"""Model training with MLflow tracking and registration.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Trains a RandomForest churn classifier on the feature store snapshot:`
> **Type:** Logical operation

### Line   7
> **Code:** `1. start an MLflow run and log hyperparameters`
> **Type:** Logical operation

### Line   8
> **Code:** `2. train + evaluate on a held-out test split`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `3. log metrics, confusion matrix, feature importances and the fitted`
> **Type:** Logical operation

### Line  10
> **Code:** `feature transformer config as artifacts`
> **Type:** Logical operation

### Line  11
> **Code:** `4. register the model in the MLflow Model Registry (stage: Staging)`
> **Type:** Function call

### Line  12
> **Code:** `5. persist a local model.pkl (DVC output) and metrics.json (DVC metric...`
> **Type:** Logical operation

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `import json`
> **Type:** Imports a module

### Line  19
> **Code:** `import os`
> **Type:** Imports a module

### Line  20
> **Code:** `import sys`
> **Type:** Imports a module

### Line  21
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  25
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  28
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `import matplotlib.pyplot as plt  # noqa: E402`
> **Type:** Imports a module

### Line  33
> **Code:** `import mlflow  # noqa: E402`
> **Type:** Imports a module

### Line  34
> **Code:** `import numpy as np  # noqa: E402`
> **Type:** Imports a module

### Line  35
> **Code:** `import pandas as pd  # noqa: E402`
> **Type:** Imports a module

### Line  36
> **Code:** `from sklearn.ensemble import RandomForestClassifier  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  37
> **Code:** `from sklearn.metrics import (  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  38
> **Code:** `ConfusionMatrixDisplay,`
> **Type:** Code statement

### Line  39
> **Code:** `accuracy_score,`
> **Type:** Logical operation

### Line  40
> **Code:** `f1_score,`
> **Type:** Logical operation

### Line  41
> **Code:** `precision_score,`
> **Type:** Logical operation

### Line  42
> **Code:** `recall_score,`
> **Type:** Logical operation

### Line  43
> **Code:** `roc_auc_score,`
> **Type:** Logical operation

### Line  44
> **Code:** `)`
> **Type:** Code statement

### Line  45
> **Code:** `from sklearn.model_selection import train_test_split  # noqa: E402`
> **Type:** Imports specific names from a module

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `from src.features.build_features import TARGET_FEATURE, FEATURE_ORDER ...`
> **Type:** Imports specific names from a module

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `DEFAULT_DATA = PROJECT_ROOT / "data" / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config...`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `DEFAULT_MODEL_OUTPUT = PROJECT_ROOT / "models" / "model.pkl"`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `DEFAULT_METRICS = PROJECT_ROOT / "metrics.json"`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference....`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "churn_model")`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `DEFAULT_PARAMS = {`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `"n_estimators": 300,`
> **Type:** Logical operation

### Line  57
> **Code:** `"max_depth": 15,`
> **Type:** Code statement

### Line  58
> **Code:** `"min_samples_leaf": 3,`
> **Type:** Code statement

### Line  59
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line  60
> **Code:** `"class_weight": "balanced",`
> **Type:** Code statement

### Line  61
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line  62
> **Code:** `}`
> **Type:** Code statement

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `def _save_confusion_matrix(y_true, y_pred, path: Path) -> None:`
> **Type:** Function definition

### Line  66
> **Code:** `fig, ax = plt.subplots(figsize=(6, 5))`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=ax, cmap="B...`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `fig.tight_layout()`
> **Type:** Function call

### Line  69
> **Code:** `fig.savefig(path, dpi=120)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def _save_feature_importances(model, feature_names: list[str], path: P...`
> **Type:** Function definition

### Line  74
> **Code:** `importances = model.feature_importances_`
> **Type:** Imports a module

### Line  75
> **Code:** `order = np.argsort(importances)[::-1]`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `fig, ax = plt.subplots(figsize=(9, 6))`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `ax.barh([feature_names[i] for i in order][:20], importances[order][:20...`
> **Type:** Logical operation

### Line  78
> **Code:** `ax.invert_yaxis()`
> **Type:** Function call

### Line  79
> **Code:** `ax.set_xlabel("feature importance")`
> **Type:** Logical operation

### Line  80
> **Code:** `fig.tight_layout()`
> **Type:** Function call

### Line  81
> **Code:** `fig.savefig(path, dpi=120)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def train_model(`
> **Type:** Function definition

### Line  86
> **Code:** `data_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `config_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `model_output: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `model_name: str = MODEL_NAME,`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `params: dict | None = None,`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  92
> **Code:** `data_path = Path(data_path or DEFAULT_DATA)`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `config_path = Path(config_path or DEFAULT_CONFIG)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `model_output = Path(model_output or DEFAULT_MODEL_OUTPUT)`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `params = {**DEFAULT_PARAMS, **(params or {})}`
> **Type:** Assignment/comparison

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `if not data_path.exists():`
> **Type:** Conditional statement

### Line  98
> **Code:** `raise FileNotFoundError(f"Feature dataset not found: {data_path}")`
> **Type:** Raises an exception

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `features = pd.read_parquet(data_path)`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `if TARGET_FEATURE not in features.columns:`
> **Type:** Conditional statement

### Line 102
> **Code:** `raise ValueError(f"Target column '{TARGET_FEATURE}' missing from featu...`
> **Type:** Raises an exception

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `X = features[FEATURE_ORDER]`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `y = features[TARGET_FEATURE].astype(int)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0....`
> **Type:** Assignment/comparison

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `model = RandomForestClassifier(**params)`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `model.fit(X_train, y_train)`
> **Type:** Function call

### Line 110
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `y_prob = model.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `"accuracy": float(accuracy_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line 115
> **Code:** `"f1": float(f1_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line 116
> **Code:** `"precision": float(precision_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line 117
> **Code:** `"recall": float(recall_score(y_test, y_pred)),`
> **Type:** Logical operation

### Line 118
> **Code:** `"roc_auc": float(roc_auc_score(y_test, y_prob)),`
> **Type:** Logical operation

### Line 119
> **Code:** `"train_size": int(len(X_train)),`
> **Type:** Code statement

### Line 120
> **Code:** `"test_size": int(len(X_test)),`
> **Type:** Code statement

### Line 121
> **Code:** `}`
> **Type:** Code statement

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** `run_id = None`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `try:`
> **Type:** Code statement

### Line 125
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:...`
> **Type:** Arithmetic operation

### Line 126
> **Code:** `with mlflow.start_run(run_name="churn-training") as run:`
> **Type:** Context manager

### Line 127
> **Code:** `run_id = run.info.run_id`
> **Type:** Assignment/comparison

### Line 128
> **Code:** `mlflow.set_tag("model_name", model_name)`
> **Type:** Function call

### Line 129
> **Code:** `mlflow.set_tag("git_commit", os.environ.get("GIT_COMMIT", "unknown"))`
> **Type:** Function call

### Line 130
> **Code:** `mlflow.set_tag("data_version", os.environ.get("DVC_DATA_VERSION", "unk...`
> **Type:** Function call

### Line 131
> **Code:** `mlflow.log_params(params)`
> **Type:** Function call

### Line 132
> **Code:** `mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, ...`
> **Type:** Logical operation

### Line 133
> **Code:** ``
> **Type:** Empty line

### Line 134
> **Code:** `confusion_path = PROJECT_ROOT / "models" / "artifacts" / "confusion_ma...`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `importance_path = PROJECT_ROOT / "models" / "artifacts" / "feature_imp...`
> **Type:** Imports a module

### Line 136
> **Code:** `confusion_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `_save_confusion_matrix(y_test, y_pred, confusion_path)`
> **Type:** Function call

### Line 138
> **Code:** `_save_feature_importances(model, list(X.columns), importance_path)`
> **Type:** Logical operation

### Line 139
> **Code:** `mlflow.log_artifact(str(confusion_path))`
> **Type:** Function call

### Line 140
> **Code:** `mlflow.log_artifact(str(importance_path))`
> **Type:** Logical operation

### Line 141
> **Code:** `mlflow.log_artifact(str(config_path))`
> **Type:** Function call

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** `mlflow.sklearn.log_model(`
> **Type:** Code statement

### Line 144
> **Code:** `model,`
> **Type:** Code statement

### Line 145
> **Code:** `artifact_path="model",`
> **Type:** Assignment/comparison

### Line 146
> **Code:** `registered_model_name=model_name,`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `input_example=X_test.iloc[[0]],`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `)`
> **Type:** Code statement

### Line 149
> **Code:** `try:`
> **Type:** Code statement

### Line 150
> **Code:** `client = mlflow.tracking.MlflowClient()`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `version = client.get_latest_versions(model_name, stages=["None"])[0].v...`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `client.transition_model_version_stage(model_name, version, stage="Stag...`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `mlflow.set_tag("registry_version", version)`
> **Type:** Function call

### Line 154
> **Code:** `print(f"registered {model_name} version {version} -> Staging")`
> **Type:** Prints output to console

### Line 155
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line 156
> **Code:** `print(f"warning: registry transition failed: {exc}")`
> **Type:** Prints output to console

### Line 157
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line 158
> **Code:** `print(f"warning: MLflow tracking failed (continuing offline): {exc}")`
> **Type:** Prints output to console

### Line 159
> **Code:** ``
> **Type:** Empty line

### Line 160
> **Code:** `model_output.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 161
> **Code:** `joblib.dump(model, model_output)`
> **Type:** Function call

### Line 162
> **Code:** `(PROJECT_ROOT / "metrics.json").write_text(json.dumps(metrics, indent=...`
> **Type:** Assignment/comparison

### Line 163
> **Code:** ``
> **Type:** Empty line

### Line 164
> **Code:** `reference = X_test.copy()`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `reference["prediction"] = y_prob`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `reference["label"] = y_test.values`
> **Type:** Assignment/comparison

### Line 167
> **Code:** `DEFAULT_REFERENCE.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 168
> **Code:** `reference.to_csv(DEFAULT_REFERENCE, index=False)`
> **Type:** Assignment/comparison

### Line 169
> **Code:** ``
> **Type:** Empty line

### Line 170
> **Code:** `return {"run_id": run_id, "model_name": model_name, "metrics": metrics...`
> **Type:** Returns a value from a function

### Line 171
> **Code:** ``
> **Type:** Empty line

### Line 172
> **Code:** ``
> **Type:** Empty line

### Line 173
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 174
> **Code:** `parser = argparse.ArgumentParser(description="Train and register the c...`
> **Type:** Assignment/comparison

### Line 175
> **Code:** `parser.add_argument("--data", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 176
> **Code:** `parser.add_argument("--config", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 177
> **Code:** `parser.add_argument("--model-output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `parser.add_argument("--model-name", type=str, default=MODEL_NAME)`
> **Type:** Assignment/comparison

### Line 179
> **Code:** `parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS...`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `parser.add_argument("--max-depth", type=int, default=DEFAULT_PARAMS["m...`
> **Type:** Assignment/comparison

### Line 181
> **Code:** `parser.add_argument("--min-samples-leaf", type=int, default=DEFAULT_PA...`
> **Type:** Assignment/comparison

### Line 182
> **Code:** `parser.add_argument("--seed", type=int, default=DEFAULT_PARAMS["random...`
> **Type:** Assignment/comparison

### Line 183
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 184
> **Code:** ``
> **Type:** Empty line

### Line 185
> **Code:** `params = {`
> **Type:** Assignment/comparison

### Line 186
> **Code:** `"n_estimators": args.n_estimators,`
> **Type:** Logical operation

### Line 187
> **Code:** `"max_depth": args.max_depth,`
> **Type:** Code statement

### Line 188
> **Code:** `"min_samples_leaf": args.min_samples_leaf,`
> **Type:** Code statement

### Line 189
> **Code:** `"class_weight": DEFAULT_PARAMS["class_weight"],`
> **Type:** Data structure operation

### Line 190
> **Code:** `"random_state": args.seed,`
> **Type:** Logical operation

### Line 191
> **Code:** `}`
> **Type:** Code statement

### Line 192
> **Code:** `result = train_model(args.data, args.config, args.model_output, args.m...`
> **Type:** Assignment/comparison

### Line 193
> **Code:** `print(f"run_id={result['run_id']} f1={result['metrics']['f1']:.4f} roc...`
> **Type:** Prints output to console

### Line 194
> **Code:** ``
> **Type:** Empty line

### Line 195
> **Code:** ``
> **Type:** Empty line

### Line 196
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 197
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 197
- **Code lines:** 163
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 31

---
*Documentation generated for: mlops-project-documentation*
*File: train.py*
---

# mlops-project-documentation: promote.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/models/promote.py`
- **Total lines:** 118
- **File size:** 4666 bytes

## Line Type Summary
- **Code:** 90
- **Comment:** 0
- **Empty:** 25
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add promotion gate with evidence pack requirement`
> **Type:** TODO: high - Add promotion gate with evidence pack requirement

### Line   2
> **Code:** `# TODO: medium - Implement human approval recording`
> **Type:** TODO: medium - Implement human approval recording

### Line   3
> **Code:** `# TODO: low - Add rollback capability documentation`
> **Type:** TODO: low - Add rollback capability documentation

### Line   4
> **Code:** `"""Promotion logic: Staging -> Production in the MLflow Model Registry...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `A candidate (the latest evaluation report) is promoted only if:`
> **Type:** Logical operation

### Line   7
> **Code:** `- it passed the evaluation gates (evaluate.py), and`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- it beats the currently deployed production model on the same test se...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `The previous production version is archived. The promotion is recorded...`
> **Type:** Logical operation

### Line  11
> **Code:** `models/evaluation/production_report.json so the API and dashboards can...`
> **Type:** Arithmetic operation

### Line  12
> **Code:** `which model is live and why.`
> **Type:** Logical operation

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `import json`
> **Type:** Imports a module

### Line  19
> **Code:** `import os`
> **Type:** Imports a module

### Line  20
> **Code:** `import sys`
> **Type:** Imports a module

### Line  21
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `LATEST_REPORT = PROJECT_ROOT / "models" / "evaluation" / "latest_repor...`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "producti...`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "churn_model")`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def _client():`
> **Type:** Function definition

### Line  31
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:...`
> **Type:** Arithmetic operation

### Line  34
> **Code:** `return mlflow.tracking.MlflowClient()`
> **Type:** Returns a value from a function

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `def current_production(model_name: str = MODEL_NAME) -> dict | None:`
> **Type:** Function definition

### Line  38
> **Code:** `try:`
> **Type:** Code statement

### Line  39
> **Code:** `client = _client()`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `versions = client.get_latest_versions(model_name, stages=["Production"...`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `if not versions:`
> **Type:** Conditional statement

### Line  42
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  43
> **Code:** `version = versions[0]`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `report = {}`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `if PRODUCTION_REPORT.exists():`
> **Type:** Conditional statement

### Line  46
> **Code:** `report = json.loads(PRODUCTION_REPORT.read_text())`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `return {"version": int(version.version), "run_id": version.run_id, "re...`
> **Type:** Returns a value from a function

### Line  48
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line  49
> **Code:** `print(f"warning: could not read production model from registry: {exc}"...`
> **Type:** Prints output to console

### Line  50
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def promote_candidate(model_name: str = MODEL_NAME, force: bool = Fals...`
> **Type:** Function definition

### Line  54
> **Code:** `if not LATEST_REPORT.exists():`
> **Type:** Conditional statement

### Line  55
> **Code:** `raise FileNotFoundError(f"No candidate report found at {LATEST_REPORT}...`
> **Type:** Raises an exception

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `candidate = json.loads(LATEST_REPORT.read_text())`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `if not candidate.get("gates_passed") and not force:`
> **Type:** Conditional statement

### Line  59
> **Code:** `raise RuntimeError("Candidate did not pass evaluation gates; refusing ...`
> **Type:** Raises an exception

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `client = _client()`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `versions = client.get_latest_versions(model_name, stages=["Staging"])`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `if not versions:`
> **Type:** Conditional statement

### Line  64
> **Code:** `raise RuntimeError(f"No Staging version found for model '{model_name}'...`
> **Type:** Raises an exception

### Line  65
> **Code:** `version = versions[0]`
> **Type:** Assignment/comparison

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** `production = current_production(model_name)`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `if production and not force:`
> **Type:** Conditional statement

### Line  69
> **Code:** `candidate_f1 = candidate["metrics"]["f1"]`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `production_f1 = production["report"].get("metrics", {}).get("f1")`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `if production_f1 is not None and candidate_f1 < production_f1:`
> **Type:** Conditional statement

### Line  72
> **Code:** `raise RuntimeError(`
> **Type:** Raises an exception

### Line  73
> **Code:** `f"Candidate f1={candidate_f1:.4f} < production f1={production_f1:.4f};...`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `"(use --force to override)."`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `)`
> **Type:** Code statement

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `for previous in client.search_model_versions(f"name='{model_name}'"):`
> **Type:** For loop

### Line  78
> **Code:** `if previous.current_stage == "Production":`
> **Type:** Conditional statement

### Line  79
> **Code:** `client.transition_model_version_stage(model_name, previous.version, st...`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `print(f"archived {model_name} version {previous.version}")`
> **Type:** Prints output to console

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `client.transition_model_version_stage(model_name, version.version, sta...`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `client.update_model_version(`
> **Type:** Code statement

### Line  84
> **Code:** `model_name,`
> **Type:** Code statement

### Line  85
> **Code:** `version.version,`
> **Type:** Code statement

### Line  86
> **Code:** `description=f"Promoted by promote.py | f1={candidate['metrics']['f1']:...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `)`
> **Type:** Code statement

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `production_report = {`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `"model_name": model_name,`
> **Type:** Code statement

### Line  91
> **Code:** `"version": int(version.version),`
> **Type:** Code statement

### Line  92
> **Code:** `"run_id": version.run_id or candidate.get("run_id"),`
> **Type:** Logical operation

### Line  93
> **Code:** `"promoted_at": None,`
> **Type:** Code statement

### Line  94
> **Code:** `"metrics": candidate["metrics"],`
> **Type:** Logical operation

### Line  95
> **Code:** `}`
> **Type:** Code statement

### Line  96
> **Code:** `PRODUCTION_REPORT.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `PRODUCTION_REPORT.write_text(json.dumps(production_report, indent=2))`
> **Type:** Assignment/comparison

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `print(f"promoted {model_name} version {version.version} -> Production"...`
> **Type:** Prints output to console

### Line 100
> **Code:** `return production_report`
> **Type:** Returns a value from a function

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 104
> **Code:** `parser = argparse.ArgumentParser(description="Promote the latest valid...`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `parser.add_argument("--model-name", type=str, default=MODEL_NAME)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `parser.add_argument("--force", action="store_true", help="Skip product...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** `try:`
> **Type:** Code statement

### Line 110
> **Code:** `report = promote_candidate(args.model_name, args.force)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `print(json.dumps(report, indent=2))`
> **Type:** Prints output to console

### Line 112
> **Code:** `except (RuntimeError, FileNotFoundError) as exc:`
> **Type:** Logical operation

### Line 113
> **Code:** `print(f"promotion failed: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line 114
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** ``
> **Type:** Empty line

### Line 117
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 118
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 118
- **Code lines:** 90
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 25

---
*Documentation generated for: mlops-project-documentation*
*File: promote.py*
---

# mlops-project-documentation: model_loader.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/api/model_loader.py`
- **Total lines:** 124
- **File size:** 4584 bytes

## Line Type Summary
- **Code:** 96
- **Comment:** 0
- **Empty:** 25
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Model loading for the inference API.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Loads the production model once at startup from the MLflow Model Regis...`
> **Type:** Code statement

### Line   7
> **Code:** `(`models:/<MODEL_NAME>/Production`) and applies the same fitted featur...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `transformer that was used at training time. Falls back to an explicit ...`
> **Type:** Logical operation

### Line   9
> **Code:** `URI or a local pickle when the registry is unreachable (local dev).`
> **Type:** Logical operation

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `A periodic reload can be enabled with RELOAD_INTERVAL (seconds) so reg...`
> **Type:** Code statement

### Line  12
> **Code:** `promotions are picked up without a full restart.`
> **Type:** Code statement

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import json`
> **Type:** Imports a module

### Line  18
> **Code:** `import os`
> **Type:** Imports a module

### Line  19
> **Code:** `import threading`
> **Type:** Imports a module

### Line  20
> **Code:** `import time`
> **Type:** Imports a module

### Line  21
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  24
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `from src.features.build_features import FeatureTransformer`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `DEFAULT_CONFIG_PATH = PROJECT_ROOT / "data" / "features" / "features_c...`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `DEFAULT_LOCAL_MODEL = PROJECT_ROOT / "models" / "model.pkl"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "churn_model")`
> **Type:** Assignment/comparison

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `class ModelBundle:`
> **Type:** Class definition

### Line  36
> **Code:** `def __init__(`
> **Type:** Function definition

### Line  37
> **Code:** `self,`
> **Type:** Code statement

### Line  38
> **Code:** `model,`
> **Type:** Code statement

### Line  39
> **Code:** `transformer: FeatureTransformer,`
> **Type:** Logical operation

### Line  40
> **Code:** `model_name: str,`
> **Type:** Code statement

### Line  41
> **Code:** `version: str,`
> **Type:** Code statement

### Line  42
> **Code:** `run_id: str | None = None,`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `):`
> **Type:** Code statement

### Line  44
> **Code:** `self.model = model`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `self.transformer = transformer`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `self.model_name = model_name`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `self.version = version`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `self.run_id = run_id`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  51
> **Code:** `features = self.transformer.transform(df)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `return self.model.predict_proba(features)`
> **Type:** Returns a value from a function

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `class ModelLoader:`
> **Type:** Class definition

### Line  56
> **Code:** `def __init__(self, model_name: str = MODEL_NAME, config_path: str | Pa...`
> **Type:** Function definition

### Line  57
> **Code:** `self.model_name = model_name`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `self.config_path = Path(config_path or os.environ.get("FEATURES_CONFIG...`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `self._bundle: ModelBundle | None = None`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `self._lock = threading.Lock()`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `self._loaded_at: float = 0.0`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `def load(self) -> ModelBundle:`
> **Type:** Function definition

### Line  64
> **Code:** `with self._lock:`
> **Type:** Context manager

### Line  65
> **Code:** `bundle, version, run_id = self._load_model()`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `self._bundle = bundle`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `self._bundle.version = version`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `self._bundle.run_id = run_id`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `self._loaded_at = time.time()`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `return self._bundle`
> **Type:** Returns a value from a function

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `def _load_model(self) -> tuple[ModelBundle, str, str | None]:`
> **Type:** Function definition

### Line  73
> **Code:** `if not self.config_path.exists():`
> **Type:** Conditional statement

### Line  74
> **Code:** `raise FileNotFoundError(f"Features config not found: {self.config_path...`
> **Type:** Raises an exception

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `config = json.loads(self.config_path.read_text())`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `transformer = FeatureTransformer.from_config(config)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `registry_uri = f"models:/{self.model_name}/Production"`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `explicit_uri = os.environ.get("MLFLOW_MODEL_URI")`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `if explicit_uri:`
> **Type:** Conditional statement

### Line  82
> **Code:** `try:`
> **Type:** Code statement

### Line  83
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:...`
> **Type:** Arithmetic operation

### Line  86
> **Code:** `model = mlflow.sklearn.load_model(explicit_uri)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `return ModelBundle(model, transformer, self.model_name, explicit_uri, ...`
> **Type:** Returns a value from a function

### Line  88
> **Code:** `except Exception:  # noqa: BLE001  # nosec B110 - fallback to registry...`
> **Type:** Arithmetic operation

### Line  89
> **Code:** `pass`
> **Type:** Code statement

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `try:`
> **Type:** Code statement

### Line  92
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:...`
> **Type:** Arithmetic operation

### Line  95
> **Code:** `client = mlflow.tracking.MlflowClient()`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `model = mlflow.sklearn.load_model(registry_uri)`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `version = client.get_latest_versions(self.model_name, stages=["Product...`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `return (`
> **Type:** Returns a value from a function

### Line  99
> **Code:** `ModelBundle(model, transformer, self.model_name, str(version.version),...`
> **Type:** Logical operation

### Line 100
> **Code:** `str(version.version),`
> **Type:** Code statement

### Line 101
> **Code:** `version.run_id,`
> **Type:** Code statement

### Line 102
> **Code:** `)`
> **Type:** Code statement

### Line 103
> **Code:** `except Exception:  # noqa: BLE001  # nosec B110 - fallback to local pi...`
> **Type:** Arithmetic operation

### Line 104
> **Code:** `pass`
> **Type:** Code statement

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `if DEFAULT_LOCAL_MODEL.exists():`
> **Type:** Conditional statement

### Line 107
> **Code:** `model = joblib.load(DEFAULT_LOCAL_MODEL)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `return ModelBundle(model, transformer, self.model_name, "local"), "loc...`
> **Type:** Returns a value from a function

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `raise RuntimeError(f"Model '{self.model_name}' unavailable: no registr...`
> **Type:** Raises an exception

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `def get_bundle(self) -> ModelBundle:`
> **Type:** Function definition

### Line 113
> **Code:** `if self._bundle is None:`
> **Type:** Conditional statement

### Line 114
> **Code:** `return self.load()`
> **Type:** Returns a value from a function

### Line 115
> **Code:** `interval = int(os.environ.get("RELOAD_INTERVAL", "0") or 0)`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `if interval > 0 and time.time() - self._loaded_at > interval:`
> **Type:** Conditional statement

### Line 117
> **Code:** `try:`
> **Type:** Code statement

### Line 118
> **Code:** `return self.load()`
> **Type:** Returns a value from a function

### Line 119
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line 120
> **Code:** `return self._bundle`
> **Type:** Returns a value from a function

### Line 121
> **Code:** `return self._bundle`
> **Type:** Returns a value from a function

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `loader = ModelLoader()`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 124
- **Code lines:** 96
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 25

---
*Documentation generated for: mlops-project-documentation*
*File: model_loader.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/api/__init__.py`
- **Total lines:** 4
- **File size:** 215 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""api package: FastAPI application exposing the churn prediction endp...`
> **Type:** Code statement

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: metrics.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/api/metrics.py`
- **Total lines:** 52
- **File size:** 1646 bytes

## Line Type Summary
- **Code:** 37
- **Comment:** 0
- **Empty:** 12
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Prometheus instrumentation for the FastAPI application.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Exposes:`
> **Type:** Code statement

### Line   7
> **Code:** `- request count / latency histograms per endpoint and status (instrume...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- prediction value histogram (feeds the model drift dashboards)`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `- live model version gauge`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from prometheus_client import Gauge, Histogram`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from prometheus_fastapi_instrumentator import Instrumentator`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `MODEL_PREDICTION_VALUE = Histogram(`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `"model_prediction_value",`
> **Type:** Code statement

### Line  19
> **Code:** `"Distribution of predicted churn probabilities",`
> **Type:** Code statement

### Line  20
> **Code:** `buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `)`
> **Type:** Code statement

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PREDICTIONS_TOTAL = Gauge(`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `"predictions_total",`
> **Type:** Code statement

### Line  25
> **Code:** `"Cumulative number of prediction requests",`
> **Type:** Code statement

### Line  26
> **Code:** `["model_version"],`
> **Type:** Data structure operation

### Line  27
> **Code:** `)`
> **Type:** Code statement

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `MODEL_VERSION = Gauge(`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `"mlops_model_version",`
> **Type:** Code statement

### Line  31
> **Code:** `"Version of the model currently served",`
> **Type:** Code statement

### Line  32
> **Code:** `["model_name"],`
> **Type:** Data structure operation

### Line  33
> **Code:** `)`
> **Type:** Code statement

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def setup_metrics(app) -> Instrumentator:`
> **Type:** Function definition

### Line  37
> **Code:** `instrumentator = Instrumentator(`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `should_group_status_codes=False,`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `should_group_untemplated=True,`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `should_respect_env_var=False,`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `)`
> **Type:** Code statement

### Line  42
> **Code:** `instrumentator.instrument(app).expose(app, endpoint="/metrics", includ...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `return instrumentator`
> **Type:** Returns a value from a function

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def record_prediction(probability: float, model_version: str) -> None:`
> **Type:** Function definition

### Line  47
> **Code:** `MODEL_PREDICTION_VALUE.observe(probability)`
> **Type:** Function call

### Line  48
> **Code:** `PREDICTIONS_TOTAL.labels(model_version=model_version).inc()`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `def set_model_version(model_name: str, model_version: str) -> None:`
> **Type:** Function definition

### Line  52
> **Code:** `MODEL_VERSION.labels(model_name=model_name).set(float(model_version) i...`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 52
- **Code lines:** 37
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 12

---
*Documentation generated for: mlops-project-documentation*
*File: metrics.py*
---

# mlops-project-documentation: schemas.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/api/schemas.py`
- **Total lines:** 74
- **File size:** 2850 bytes

## Line Type Summary
- **Code:** 53
- **Comment:** 0
- **Empty:** 18
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Pydantic request/response schemas for the inference API.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Field aliases match the training columns exactly so the feature transf...`
> **Type:** Logical operation

### Line   7
> **Code:** `can be applied without training/serving skew. Pydantic rejects malform...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `payloads with a 422 and a clear error message.`
> **Type:** Logical operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from typing import Literal`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from pydantic import BaseModel, Field`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `YesNo = Literal["Yes", "No"]`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `NoService = Literal["Yes", "No", "No phone service"]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `NoInternet = Literal["Yes", "No", "No internet service"]`
> **Type:** Assignment/comparison

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `class ChurnPredictionRequest(BaseModel):`
> **Type:** Class definition

### Line  23
> **Code:** `gender: Literal["Male", "Female"] = Field(alias="Gender")`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `senior_citizen: Literal[0, 1] = Field(alias="SeniorCitizen")`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `partner: YesNo = Field(alias="Partner")`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `dependents: YesNo = Field(alias="Dependents")`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `tenure: int = Field(alias="Tenure", ge=0, le=120)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `phone_service: YesNo = Field(alias="PhoneService")`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `multiple_lines: NoService = Field(alias="MultipleLines")`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `internet_service: Literal["DSL", "Fiber optic", "No"] = Field(alias="I...`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `online_security: NoInternet = Field(alias="OnlineSecurity")`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `online_backup: NoInternet = Field(alias="OnlineBackup")`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `device_protection: NoInternet = Field(alias="DeviceProtection")`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `tech_support: NoInternet = Field(alias="TechSupport")`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `streaming_tv: NoInternet = Field(alias="StreamingTV")`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `streaming_movies: NoInternet = Field(alias="StreamingMovies")`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `contract: Literal["Month-to-month", "One year", "Two year"] = Field(al...`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `paperless_billing: YesNo = Field(alias="PaperlessBilling")`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `payment_method: Literal[`
> **Type:** Code statement

### Line  40
> **Code:** `"Electronic check", "Mailed check", "Bank transfer (automatic)", "Cred...`
> **Type:** Code statement

### Line  41
> **Code:** `] = Field(alias="PaymentMethod")`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `monthly_charges: float = Field(alias="MonthlyCharges", ge=0, le=1000)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `total_charges: float = Field(alias="TotalCharges", ge=0, le=100000)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `model_config = {"populate_by_name": True}`
> **Type:** Assignment/comparison

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `def to_dataframe(self):`
> **Type:** Function definition

### Line  48
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `return pd.DataFrame([self.model_dump(by_alias=True)])`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `class PredictionResponse(BaseModel):`
> **Type:** Class definition

### Line  54
> **Code:** `prediction: int = Field(description="1 if the customer is predicted to...`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `probability: float = Field(ge=0.0, le=1.0, description="Predicted chur...`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `model_name: str`
> **Type:** Code statement

### Line  57
> **Code:** `model_version: str`
> **Type:** Code statement

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `PredictionRequest = ChurnPredictionRequest | list[ChurnPredictionReque...`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `PredictionResult = PredictionResponse | list[PredictionResponse]`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `class HealthResponse(BaseModel):`
> **Type:** Class definition

### Line  65
> **Code:** `status: str`
> **Type:** Code statement

### Line  66
> **Code:** `model_name: str | None = None`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `model_version: str | None = None`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `class ModelInfoResponse(BaseModel):`
> **Type:** Class definition

### Line  71
> **Code:** `model_name: str`
> **Type:** Code statement

### Line  72
> **Code:** `model_version: str`
> **Type:** Code statement

### Line  73
> **Code:** `run_id: str | None = None`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `production_metrics: dict | None = None`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 74
- **Code lines:** 53
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 18

---
*Documentation generated for: mlops-project-documentation*
*File: schemas.py*
---

# mlops-project-documentation: main.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/api/main.py`
- **Total lines:** 103
- **File size:** 3384 bytes

## Line Type Summary
- **Code:** 81
- **Comment:** 0
- **Empty:** 19
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add request validation and error handling`
> **Type:** TODO: high - Add request validation and error handling

### Line   2
> **Code:** `# TODO: medium - Implement request/response logging`
> **Type:** TODO: medium - Implement request/response logging

### Line   3
> **Code:** `# TODO: low - Add health check endpoint improvement`
> **Type:** TODO: low - Add health check endpoint improvement

### Line   4
> **Code:** `"""FastAPI inference service for the churn model.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Endpoints:`
> **Type:** Code statement

### Line   7
> **Code:** `- POST /predict        single or batch prediction`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- GET  /health         liveness/readiness probe for Kubernetes`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `- GET  /metrics        Prometheus metrics`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `- GET  /model-info     metadata of the loaded model`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `import logging`
> **Type:** Imports a module

### Line  17
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  20
> **Code:** `from fastapi import FastAPI, HTTPException`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `from src.api import metrics`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from src.api.model_loader import loader`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from src.api.schemas import (`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `ChurnPredictionRequest,`
> **Type:** Code statement

### Line  26
> **Code:** `HealthResponse,`
> **Type:** Code statement

### Line  27
> **Code:** `ModelInfoResponse,`
> **Type:** Code statement

### Line  28
> **Code:** `PredictionRequest,`
> **Type:** Code statement

### Line  29
> **Code:** `PredictionResponse,`
> **Type:** Code statement

### Line  30
> **Code:** `PredictionResult,`
> **Type:** Code statement

### Line  31
> **Code:** `)`
> **Type:** Code statement

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `logger = logging.getLogger("mlops-api")`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `PRODUCTION_REPORT = PROJECT_ROOT / "models" / "evaluation" / "producti...`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `app = FastAPI(`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `title="MLOps Churn Inference API",`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `description="Serves the production churn model from the MLflow Model R...`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `version="1.0.0",`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `)`
> **Type:** Code statement

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `@app.on_event("startup")`
> **Type:** Function call

### Line  45
> **Code:** `def _startup() -> None:`
> **Type:** Function definition

### Line  46
> **Code:** `try:`
> **Type:** Code statement

### Line  47
> **Code:** `bundle = loader.load()`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `metrics.set_model_version(bundle.model_name, bundle.version)`
> **Type:** Function call

### Line  49
> **Code:** `logger.info("model loaded: %s version %s", bundle.model_name, bundle.v...`
> **Type:** Arithmetic operation

### Line  50
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line  51
> **Code:** `logger.error("model loading failed: %s", exc)`
> **Type:** Arithmetic operation

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `@app.get("/health", response_model=HealthResponse, tags=["health"])`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `def health() -> HealthResponse:`
> **Type:** Function definition

### Line  56
> **Code:** `try:`
> **Type:** Code statement

### Line  57
> **Code:** `bundle = loader.get_bundle()`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `return HealthResponse(status="ok", model_name=bundle.model_name, model...`
> **Type:** Returns a value from a function

### Line  59
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line  60
> **Code:** `return HealthResponse(status="degraded")`
> **Type:** Returns a value from a function

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `@app.get("/model-info", response_model=ModelInfoResponse, tags=["healt...`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `def model_info() -> ModelInfoResponse:`
> **Type:** Function definition

### Line  65
> **Code:** `bundle = loader.get_bundle()`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `production_metrics = None`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `if PRODUCTION_REPORT.exists():`
> **Type:** Conditional statement

### Line  68
> **Code:** `production_metrics = json.loads(PRODUCTION_REPORT.read_text()).get("me...`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `return ModelInfoResponse(`
> **Type:** Returns a value from a function

### Line  70
> **Code:** `model_name=bundle.model_name,`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `model_version=bundle.version,`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `run_id=bundle.run_id,`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `production_metrics=production_metrics,`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `)`
> **Type:** Code statement

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `def _predict_one(request: ChurnPredictionRequest) -> PredictionRespons...`
> **Type:** Function definition

### Line  78
> **Code:** `bundle = loader.get_bundle()`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `df = request.to_dataframe()`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `try:`
> **Type:** Code statement

### Line  81
> **Code:** `probabilities = np.asarray(bundle.predict_proba(df))[:, 1]`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line  83
> **Code:** `raise HTTPException(status_code=500, detail=f"prediction failed: {exc}...`
> **Type:** Raises an exception

### Line  84
> **Code:** `probability = float(probabilities[0])`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `metrics.record_prediction(probability, bundle.version)`
> **Type:** Logical operation

### Line  86
> **Code:** `return PredictionResponse(`
> **Type:** Returns a value from a function

### Line  87
> **Code:** `prediction=int(probability >= 0.5),`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `probability=probability,`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `model_name=bundle.model_name,`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `model_version=bundle.version,`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `)`
> **Type:** Code statement

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `@app.post("/predict", response_model=PredictionResult, tags=["inferenc...`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `def predict(payload: PredictionRequest) -> PredictionResult:`
> **Type:** Function definition

### Line  96
> **Code:** `if isinstance(payload, list):`
> **Type:** Conditional statement

### Line  97
> **Code:** `if not payload:`
> **Type:** Conditional statement

### Line  98
> **Code:** `raise HTTPException(status_code=422, detail="empty prediction batch")`
> **Type:** Raises an exception

### Line  99
> **Code:** `return [_predict_one(request) for request in payload]`
> **Type:** Returns a value from a function

### Line 100
> **Code:** `return _predict_one(payload)`
> **Type:** Returns a value from a function

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `metrics.setup_metrics(app)`
> **Type:** Function call

## Summary
- **Total lines:** 103
- **Code lines:** 81
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 19

---
*Documentation generated for: mlops-project-documentation*
*File: main.py*
---

# mlops-project-documentation: alerting.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/monitoring/alerting.py`
- **Total lines:** 60
- **File size:** 1950 bytes

## Line Type Summary
- **Code:** 45
- **Comment:** 0
- **Empty:** 12
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""Alerting helpers used by the monitoring loop and the Airflow DAGs.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Channels (in order of preference):`
> **Type:** Logical operation

### Line   7
> **Code:** `1. Slack webhook (SLACK_WEBHOOK_URL)`
> **Type:** Function call

### Line   8
> **Code:** `2. Local alert log file (data/monitoring/alerts/alerts.jsonl) — always...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `No secrets are ever logged: only the webhook URL prefix is shown.`
> **Type:** Code statement

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `import os`
> **Type:** Imports a module

### Line  17
> **Code:** `import time`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from typing import Any`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import requests`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `ALERT_LOG = PROJECT_ROOT / "data" / "monitoring" / "alerts" / "alerts....`
> **Type:** Assignment/comparison

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `SEVERITY_LEVELS = {"debug": 10, "info": 20, "warning": 30, "critical":...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def send_slack(message: str, severity: str = "info", webhook_url: str ...`
> **Type:** Function definition

### Line  30
> **Code:** `webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `if not webhook_url:`
> **Type:** Conditional statement

### Line  32
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  33
> **Code:** `emoji = {`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `"debug": ":mag:",`
> **Type:** Code statement

### Line  35
> **Code:** `"info": ":information_source:",`
> **Type:** Logical operation

### Line  36
> **Code:** `"warning": ":warning:",`
> **Type:** Code statement

### Line  37
> **Code:** `"critical": ":red_circle:",`
> **Type:** Code statement

### Line  38
> **Code:** `}.get(severity, ":bell:")`
> **Type:** Function call

### Line  39
> **Code:** `try:`
> **Type:** Code statement

### Line  40
> **Code:** `response = requests.post(webhook_url, json={"text": f"{emoji} `[{sever...`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `return response.status_code == 200`
> **Type:** Returns a value from a function

### Line  42
> **Code:** `except requests.RequestException:`
> **Type:** Code statement

### Line  43
> **Code:** `return False`
> **Type:** Returns a value from a function

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def send_alert(message: str, severity: str = "info", **extra: Any) -> ...`
> **Type:** Function definition

### Line  47
> **Code:** `entry = {`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `"timestamp": time.time(),`
> **Type:** Code statement

### Line  49
> **Code:** `"severity": severity,`
> **Type:** Code statement

### Line  50
> **Code:** `"message": message,`
> **Type:** Code statement

### Line  51
> **Code:** `"extra": extra,`
> **Type:** Code statement

### Line  52
> **Code:** `}`
> **Type:** Code statement

### Line  53
> **Code:** `ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `with ALERT_LOG.open("a") as fh:`
> **Type:** Context manager

### Line  55
> **Code:** `fh.write(json.dumps(entry) + "\n")`
> **Type:** Arithmetic operation

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `delivered = send_slack(message, severity)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `entry["slack_delivered"] = delivered`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `print(f"[alert:{severity}] {message}" + (" (slack)" if delivered else ...`
> **Type:** Prints output to console

### Line  60
> **Code:** `return entry`
> **Type:** Returns a value from a function

## Summary
- **Total lines:** 60
- **Code lines:** 45
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 12

---
*Documentation generated for: mlops-project-documentation*
*File: alerting.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/monitoring/__init__.py`
- **Total lines:** 4
- **File size:** 229 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""monitoring package: drift detection and monitoring utilities."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: drift_detection.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/monitoring/drift_detection.py`
- **Total lines:** 228
- **File size:** 8680 bytes

## Line Type Summary
- **Code:** 187
- **Comment:** 0
- **Empty:** 38
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add alert rule for ingestion stalls`
> **Type:** TODO: high - Add alert rule for ingestion stalls

### Line   2
> **Code:** `# TODO: medium - Implement dashboard for drift detection`
> **Type:** TODO: medium - Implement dashboard for drift detection

### Line   3
> **Code:** `# TODO: low - Add prediction distribution monitoring`
> **Type:** TODO: low - Add prediction distribution monitoring

### Line   4
> **Code:** `"""Model and data drift detection with Evidently AI.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Compares the current production window (features + predictions logged ...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `API) against the training reference snapshot:`
> **Type:** Code statement

### Line   8
> **Code:** `- data drift per feature (Kolmogorov-Smirnov for numeric, chi-square /`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `Jensen-Shannon for categorical)`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `- prediction drift (distribution of predicted probabilities)`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `- global drift score = fraction of drifted features`
> **Type:** Assignment/comparison

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `If the score exceeds the configured threshold (DRIFT_THRESHOLD, defaul...`
> **Type:** Logical operation

### Line  14
> **Code:** ``drift_detected` is set to true — the signal that triggers the Airflow`
> **Type:** Code statement

### Line  15
> **Code:** ``retraining_pipeline`. When Evidently is not installed, a scipy-based`
> **Type:** Arithmetic operation

### Line  16
> **Code:** `Kolmogorov-Smirnov fallback is used so the check still runs.`
> **Type:** Arithmetic operation

### Line  17
> **Code:** `"""`
> **Type:** Code statement

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  22
> **Code:** `import json`
> **Type:** Imports a module

### Line  23
> **Code:** `import os`
> **Type:** Imports a module

### Line  24
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `DEFAULT_REFERENCE = PROJECT_ROOT / "data" / "monitoring" / "reference....`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `DEFAULT_CURRENT = PROJECT_ROOT / "data" / "monitoring" / "current.csv"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "monitoring"`
> **Type:** Assignment/comparison

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `NUMERIC_FEATURES = ["Tenure", "MonthlyCharges", "TotalCharges", "charg...`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `CATEGORICAL_FEATURES = [`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `"Gender",`
> **Type:** Code statement

### Line  36
> **Code:** `"SeniorCitizen",`
> **Type:** Logical operation

### Line  37
> **Code:** `"Partner",`
> **Type:** Code statement

### Line  38
> **Code:** `"Dependents",`
> **Type:** Code statement

### Line  39
> **Code:** `"PhoneService",`
> **Type:** Code statement

### Line  40
> **Code:** `"MultipleLines",`
> **Type:** Code statement

### Line  41
> **Code:** `"InternetService",`
> **Type:** Code statement

### Line  42
> **Code:** `"OnlineSecurity",`
> **Type:** Code statement

### Line  43
> **Code:** `"OnlineBackup",`
> **Type:** Code statement

### Line  44
> **Code:** `"DeviceProtection",`
> **Type:** Code statement

### Line  45
> **Code:** `"TechSupport",`
> **Type:** Logical operation

### Line  46
> **Code:** `"StreamingTV",`
> **Type:** Code statement

### Line  47
> **Code:** `"StreamingMovies",`
> **Type:** Code statement

### Line  48
> **Code:** `"Contract",`
> **Type:** Code statement

### Line  49
> **Code:** `"PaperlessBilling",`
> **Type:** Code statement

### Line  50
> **Code:** `"PaymentMethod",`
> **Type:** Code statement

### Line  51
> **Code:** `]`
> **Type:** Code statement

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `def _features_columns(df: pd.DataFrame) -> list[str]:`
> **Type:** Function definition

### Line  55
> **Code:** `return [c for c in NUMERIC_FEATURES + CATEGORICAL_FEATURES if c in df....`
> **Type:** Returns a value from a function

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `def _evidently_report(reference: pd.DataFrame, current: pd.DataFrame) ...`
> **Type:** Function definition

### Line  59
> **Code:** `from evidently import ColumnMapping`
> **Type:** Imports specific names from a module

### Line  60
> **Code:** `from evidently.metric_preset import DataDriftPreset`
> **Type:** Imports specific names from a module

### Line  61
> **Code:** `from evidently.metrics import ColumnDriftMetric`
> **Type:** Imports specific names from a module

### Line  62
> **Code:** `from evidently.report import Report`
> **Type:** Imports specific names from a module

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `features = _features_columns(reference)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `column_mapping = ColumnMapping(`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `prediction="prediction" if "prediction" in reference.columns else None...`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `target="label" if "label" in reference.columns else None,`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `numerical_features=[c for c in NUMERIC_FEATURES if c in features],`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `categorical_features=[c for c in CATEGORICAL_FEATURES if c in features...`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `metrics: list = [DataDriftPreset()]`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `if "prediction" in reference.columns:`
> **Type:** Conditional statement

### Line  74
> **Code:** `metrics.append(ColumnDriftMetric("prediction"))`
> **Type:** Function call

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `report = Report(metrics=metrics)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `report.run(reference_data=reference, current_data=current, column_mapp...`
> **Type:** Assignment/comparison

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `return report.as_dict()`
> **Type:** Returns a value from a function

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `def _extract_drift_score(payload: dict) -> tuple[float, dict]:`
> **Type:** Function definition

### Line  83
> **Code:** `drifted = 0`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `total = 0`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `per_column: dict[str, dict] = {}`
> **Type:** Assignment/comparison

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** `def walk(node: dict) -> None:`
> **Type:** Function definition

### Line  88
> **Code:** `nonlocal drifted, total`
> **Type:** Code statement

### Line  89
> **Code:** `result = node.get("result", {})`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `if isinstance(result, dict):`
> **Type:** Conditional statement

### Line  91
> **Code:** `by_column = result.get("drift_by_columns") or result.get("drift_by_col...`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `if isinstance(by_column, dict):`
> **Type:** Conditional statement

### Line  93
> **Code:** `for col, info in by_column.items():`
> **Type:** For loop

### Line  94
> **Code:** `detected = bool(info.get("drift_detected", False))`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `stats = info.get("drift_stat_test", {})`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `per_column[col] = {`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `"drift_detected": detected,`
> **Type:** Code statement

### Line  98
> **Code:** `"test": stats.get("drift_stat_test_name", stats.get("name", "unknown")...`
> **Type:** Code statement

### Line  99
> **Code:** `"score": stats.get("drift_score"),`
> **Type:** Logical operation

### Line 100
> **Code:** `}`
> **Type:** Code statement

### Line 101
> **Code:** `drifted += int(detected)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `total += 1`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `if "number_of_drifted_columns" in result and "number_of_columns" in re...`
> **Type:** Conditional statement

### Line 104
> **Code:** `drifted = int(result["number_of_drifted_columns"])`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `total = int(result["number_of_columns"])`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `for value in node.values():`
> **Type:** For loop

### Line 107
> **Code:** `if isinstance(value, dict):`
> **Type:** Conditional statement

### Line 108
> **Code:** `walk(value)`
> **Type:** Function call

### Line 109
> **Code:** `for value in node.values():`
> **Type:** For loop

### Line 110
> **Code:** `if isinstance(value, list):`
> **Type:** Conditional statement

### Line 111
> **Code:** `for item in value:`
> **Type:** For loop

### Line 112
> **Code:** `if isinstance(item, dict):`
> **Type:** Conditional statement

### Line 113
> **Code:** `walk(item)`
> **Type:** Function call

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `walk(payload)`
> **Type:** Function call

### Line 116
> **Code:** `score = drifted / total if total else 0.0`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `return score, per_column`
> **Type:** Returns a value from a function

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `def _ks_fallback(reference: pd.DataFrame, current: pd.DataFrame) -> tu...`
> **Type:** Function definition

### Line 121
> **Code:** `from scipy import stats`
> **Type:** Imports specific names from a module

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** `drifted = 0`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `total = 0`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `per_column: dict[str, dict] = {}`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `for col in _features_columns(reference):`
> **Type:** For loop

### Line 127
> **Code:** `if col not in current.columns:`
> **Type:** Conditional statement

### Line 128
> **Code:** `continue`
> **Type:** Code statement

### Line 129
> **Code:** `ref_vals = pd.to_numeric(reference[col], errors="coerce").dropna()`
> **Type:** Assignment/comparison

### Line 130
> **Code:** `cur_vals = pd.to_numeric(current[col], errors="coerce").dropna()`
> **Type:** Assignment/comparison

### Line 131
> **Code:** `if ref_vals.empty or cur_vals.empty:`
> **Type:** Conditional statement

### Line 132
> **Code:** `continue`
> **Type:** Code statement

### Line 133
> **Code:** `stat, p_value = stats.ks_2samp(ref_vals, cur_vals)`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `detected = bool(p_value < 0.05 and stat > 0.1)`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `per_column[col] = {"drift_detected": detected, "test": "ks_2samp", "sc...`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `drifted += int(detected)`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `total += 1`
> **Type:** Assignment/comparison

### Line 138
> **Code:** `return (drifted / total if total else 0.0), per_column`
> **Type:** Returns a value from a function

### Line 139
> **Code:** ``
> **Type:** Empty line

### Line 140
> **Code:** ``
> **Type:** Empty line

### Line 141
> **Code:** `def detect_drift(`
> **Type:** Function definition

### Line 142
> **Code:** `reference_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `current_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 144
> **Code:** `threshold: float | None = None,`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `output_dir: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 146
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line 147
> **Code:** `reference_path = Path(reference_path or os.environ.get("DRIFT_REFERENC...`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `current_path = Path(current_path or os.environ.get("DRIFT_CURRENT") or...`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `threshold = float(threshold if threshold is not None else os.environ.g...`
> **Type:** Assignment/comparison

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `if not reference_path.exists():`
> **Type:** Conditional statement

### Line 153
> **Code:** `raise FileNotFoundError(f"Reference dataset not found: {reference_path...`
> **Type:** Raises an exception

### Line 154
> **Code:** `if not current_path.exists():`
> **Type:** Conditional statement

### Line 155
> **Code:** `raise FileNotFoundError(f"Current production data not found: {current_...`
> **Type:** Raises an exception

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `reference = pd.read_csv(reference_path)`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `current = pd.read_csv(current_path)`
> **Type:** Assignment/comparison

### Line 159
> **Code:** ``
> **Type:** Empty line

### Line 160
> **Code:** `try:`
> **Type:** Code statement

### Line 161
> **Code:** `payload = _evidently_report(reference, current)`
> **Type:** Assignment/comparison

### Line 162
> **Code:** `engine = "evidently"`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line 164
> **Code:** `payload = {}`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `engine = "scipy-fallback"`
> **Type:** Assignment/comparison

### Line 166
> **Code:** ``
> **Type:** Empty line

### Line 167
> **Code:** `drift_score, per_column = _extract_drift_score(payload) if payload els...`
> **Type:** Assignment/comparison

### Line 168
> **Code:** `if not per_column and engine == "evidently":`
> **Type:** Conditional statement

### Line 169
> **Code:** `drift_score, per_column = _ks_fallback(reference, current)`
> **Type:** Assignment/comparison

### Line 170
> **Code:** `engine = "scipy-fallback"`
> **Type:** Assignment/comparison

### Line 171
> **Code:** ``
> **Type:** Empty line

### Line 172
> **Code:** `report = {`
> **Type:** Assignment/comparison

### Line 173
> **Code:** `"engine": engine,`
> **Type:** Code statement

### Line 174
> **Code:** `"drift_score": drift_score,`
> **Type:** Logical operation

### Line 175
> **Code:** `"threshold": threshold,`
> **Type:** Code statement

### Line 176
> **Code:** `"drift_detected": drift_score > threshold,`
> **Type:** Comparison operation

### Line 177
> **Code:** `"drifted_features": sorted(c for c, info in per_column.items() if info...`
> **Type:** Logical operation

### Line 178
> **Code:** `"per_column": per_column,`
> **Type:** Code statement

### Line 179
> **Code:** `"reference": str(reference_path),`
> **Type:** Code statement

### Line 180
> **Code:** `"current": str(current_path),`
> **Type:** Code statement

### Line 181
> **Code:** `"generated_at": None,`
> **Type:** Code statement

### Line 182
> **Code:** `}`
> **Type:** Code statement

### Line 183
> **Code:** ``
> **Type:** Empty line

### Line 184
> **Code:** `output_dir.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 185
> **Code:** `with (output_dir / "drift_report.json").open("w") as fh:`
> **Type:** Context manager

### Line 186
> **Code:** `json.dump(report, fh, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 187
> **Code:** ``
> **Type:** Empty line

### Line 188
> **Code:** `if engine == "evidently":`
> **Type:** Conditional statement

### Line 189
> **Code:** `try:`
> **Type:** Code statement

### Line 190
> **Code:** `from evidently import ColumnMapping`
> **Type:** Imports specific names from a module

### Line 191
> **Code:** `from evidently.metric_preset import DataDriftPreset`
> **Type:** Imports specific names from a module

### Line 192
> **Code:** `from evidently.report import Report`
> **Type:** Imports specific names from a module

### Line 193
> **Code:** ``
> **Type:** Empty line

### Line 194
> **Code:** `html_report = Report(metrics=[DataDriftPreset()])`
> **Type:** Assignment/comparison

### Line 195
> **Code:** `html_report.run(`
> **Type:** Logical operation

### Line 196
> **Code:** `reference_data=reference,`
> **Type:** Assignment/comparison

### Line 197
> **Code:** `current_data=current,`
> **Type:** Assignment/comparison

### Line 198
> **Code:** `column_mapping=ColumnMapping(`
> **Type:** Assignment/comparison

### Line 199
> **Code:** `prediction="prediction" if "prediction" in reference.columns else None...`
> **Type:** Assignment/comparison

### Line 200
> **Code:** `target="label" if "label" in reference.columns else None,`
> **Type:** Assignment/comparison

### Line 201
> **Code:** `),`
> **Type:** Code statement

### Line 202
> **Code:** `)`
> **Type:** Code statement

### Line 203
> **Code:** `html_report.save_html(str(output_dir / "drift_report.html"))`
> **Type:** Arithmetic operation

### Line 204
> **Code:** `except Exception:  # noqa: BLE001  # nosec B110 - html report is best ...`
> **Type:** Arithmetic operation

### Line 205
> **Code:** `pass`
> **Type:** Code statement

### Line 206
> **Code:** ``
> **Type:** Empty line

### Line 207
> **Code:** `return report`
> **Type:** Returns a value from a function

### Line 208
> **Code:** ``
> **Type:** Empty line

### Line 209
> **Code:** ``
> **Type:** Empty line

### Line 210
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 211
> **Code:** `parser = argparse.ArgumentParser(description="Detect drift between ref...`
> **Type:** Assignment/comparison

### Line 212
> **Code:** `parser.add_argument("--reference", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 213
> **Code:** `parser.add_argument("--current", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 214
> **Code:** `parser.add_argument("--threshold", type=float, default=None)`
> **Type:** Assignment/comparison

### Line 215
> **Code:** `parser.add_argument("--output-dir", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 216
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 217
> **Code:** ``
> **Type:** Empty line

### Line 218
> **Code:** `report = detect_drift(args.reference, args.current, args.threshold, ar...`
> **Type:** Assignment/comparison

### Line 219
> **Code:** `print(`
> **Type:** Prints output to console

### Line 220
> **Code:** `f"drift engine={report['engine']} score={report['drift_score']:.3f} th...`
> **Type:** Assignment/comparison

### Line 221
> **Code:** `f"drift_detected={report['drift_detected']}"`
> **Type:** Assignment/comparison

### Line 222
> **Code:** `)`
> **Type:** Code statement

### Line 223
> **Code:** `if report["drift_detected"]:`
> **Type:** Conditional statement

### Line 224
> **Code:** `print(f"drifted features: {report['drifted_features']}")`
> **Type:** Prints output to console

### Line 225
> **Code:** ``
> **Type:** Empty line

### Line 226
> **Code:** ``
> **Type:** Empty line

### Line 227
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 228
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 228
- **Code lines:** 187
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 38

---
*Documentation generated for: mlops-project-documentation*
*File: drift_detection.py*
---

# mlops-project-documentation: validation.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/data/validation.py`
- **Total lines:** 190
- **File size:** 7451 bytes

## Line Type Summary
- **Code:** 148
- **Comment:** 0
- **Empty:** 39
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Data validation with Great Expectations.`
> **Type:** Code statement

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Loads a declarative expectation suite (great_expectations/expectations...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `and validates a pandas DataFrame against it. Uses the Great Expectatio...`
> **Type:** Logical operation

### Line   8
> **Code:** `available, and falls back to a lightweight built-in evaluator for the ...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `expectation types so validation always runs in CI.`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `Exits non-zero if any expectation fails.`
> **Type:** Arithmetic operation

### Line  12
> **Code:** `"""`
> **Type:** Code statement

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  17
> **Code:** `import json`
> **Type:** Imports a module

### Line  18
> **Code:** `import sys`
> **Type:** Imports a module

### Line  19
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `DEFAULT_SUITE = PROJECT_ROOT / "great_expectations" / "expectations" /...`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `SUPPORTED_EXPECTATIONS = [`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `"expect_table_row_count_to_be_between",`
> **Type:** Code statement

### Line  29
> **Code:** `"expect_column_values_to_not_be_null",`
> **Type:** Logical operation

### Line  30
> **Code:** `"expect_column_values_to_be_between",`
> **Type:** Code statement

### Line  31
> **Code:** `"expect_column_values_to_be_in_set",`
> **Type:** Code statement

### Line  32
> **Code:** `"expect_column_values_to_be_of_type",`
> **Type:** Code statement

### Line  33
> **Code:** `"expect_column_values_to_not_match_regex",`
> **Type:** Logical operation

### Line  34
> **Code:** `]`
> **Type:** Code statement

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `class ValidationError(RuntimeError):`
> **Type:** Class definition

### Line  38
> **Code:** `pass`
> **Type:** Code statement

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `def load_suite(path: str | Path) -> dict:`
> **Type:** Function definition

### Line  42
> **Code:** `path = Path(path)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  44
> **Code:** `raise FileNotFoundError(f"Expectation suite not found: {path}")`
> **Type:** Raises an exception

### Line  45
> **Code:** `with path.open() as fh:`
> **Type:** Context manager

### Line  46
> **Code:** `return json.load(fh)`
> **Type:** Returns a value from a function

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def _check_expectation(df: pd.DataFrame, expectation: dict) -> tuple[b...`
> **Type:** Function definition

### Line  50
> **Code:** `kind = expectation["expectation_type"]`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `kwargs = expectation.get("kwargs", {})`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `column = kwargs.get("column")`
> **Type:** Assignment/comparison

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `if kind == "expect_table_row_count_to_be_between":`
> **Type:** Conditional statement

### Line  55
> **Code:** `return kwargs["min_value"] <= len(df) <= kwargs["max_value"], f"row co...`
> **Type:** Returns a value from a function

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `if column is None or column not in df.columns:`
> **Type:** Conditional statement

### Line  58
> **Code:** `return False, f"column '{column}' missing"`
> **Type:** Returns a value from a function

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `if kind == "expect_column_values_to_not_be_null":`
> **Type:** Conditional statement

### Line  61
> **Code:** `bad = int(df[column].isna().sum())`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `return bad == 0, f"{bad} null values in {column}"`
> **Type:** Returns a value from a function

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `if kind == "expect_column_values_to_be_between":`
> **Type:** Conditional statement

### Line  65
> **Code:** `if not pd.api.types.is_numeric_dtype(df[column]):`
> **Type:** Conditional statement

### Line  66
> **Code:** `return False, f"{column} not numeric"`
> **Type:** Returns a value from a function

### Line  67
> **Code:** `vals = df[column].dropna()`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `lo, hi = kwargs.get("min_value", -float("inf")), kwargs.get("max_value...`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `bad = int(((vals < lo) | (vals > hi)).sum())`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `return bad == 0, f"{bad} values outside [{lo}, {hi}] in {column}"`
> **Type:** Returns a value from a function

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `if kind == "expect_column_values_to_be_in_set":`
> **Type:** Conditional statement

### Line  73
> **Code:** `allowed = set(kwargs.get("value_set", []))`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `vals = df[column].dropna().astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `bad = int((~vals.isin(allowed)).sum())`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `return bad == 0, f"{bad} unexpected values in {column}"`
> **Type:** Returns a value from a function

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `if kind == "expect_column_values_to_be_of_type":`
> **Type:** Conditional statement

### Line  79
> **Code:** `actual = str(df[column].dtype)`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `expected = kwargs.get("type_")`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `return actual == expected, f"{column} dtype {actual} != {expected}"`
> **Type:** Returns a value from a function

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `if kind == "expect_column_values_to_not_match_regex":`
> **Type:** Conditional statement

### Line  84
> **Code:** `pattern = kwargs.get("regex")`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `matches = df[column].dropna().astype(str).str.contains(pattern, regex=...`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `bad = int(matches.sum())`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `return bad == 0, f"{bad} rows match forbidden regex in {column}"`
> **Type:** Returns a value from a function

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `return True, f"unsupported expectation {kind} ignored"`
> **Type:** Returns a value from a function

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `def validate_dataframe(df: pd.DataFrame, suite: dict) -> dict:`
> **Type:** Function definition

### Line  93
> **Code:** `results = []`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `failures = 0`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `for expectation in suite.get("expectations", []):`
> **Type:** For loop

### Line  96
> **Code:** `kind = expectation["expectation_type"]`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `if kind not in SUPPORTED_EXPECTATIONS:`
> **Type:** Conditional statement

### Line  98
> **Code:** `continue`
> **Type:** Code statement

### Line  99
> **Code:** `try:`
> **Type:** Code statement

### Line 100
> **Code:** `success, detail = _check_expectation(df, expectation)`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `except Exception as exc:  # noqa: BLE001`
> **Type:** Code statement

### Line 102
> **Code:** `success, detail = False, str(exc)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `results.append({"expectation_type": kind, "kwargs": expectation.get("k...`
> **Type:** Function call

### Line 104
> **Code:** `failures += 0 if success else 1`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `summary = {`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `"suite": suite.get("expectation_suite_name", "dataset_suite"),`
> **Type:** Code statement

### Line 108
> **Code:** `"total": len(results),`
> **Type:** Code statement

### Line 109
> **Code:** `"passed": len(results) - failures,`
> **Type:** Arithmetic operation

### Line 110
> **Code:** `"failed": failures,`
> **Type:** Code statement

### Line 111
> **Code:** `"results": results,`
> **Type:** Code statement

### Line 112
> **Code:** `}`
> **Type:** Code statement

### Line 113
> **Code:** `return summary`
> **Type:** Returns a value from a function

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `def _to_ge_suite(suite: dict):`
> **Type:** Function definition

### Line 117
> **Code:** `from great_expectations.core import ExpectationSuite`
> **Type:** Imports specific names from a module

### Line 118
> **Code:** `from great_expectations.expectations.expectation import ExpectationCon...`
> **Type:** Imports specific names from a module

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `ge_suite = ExpectationSuite(expectation_suite_name=suite.get("expectat...`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `for expectation in suite.get("expectations", []):`
> **Type:** For loop

### Line 122
> **Code:** `if expectation["expectation_type"] in SUPPORTED_EXPECTATIONS:`
> **Type:** Conditional statement

### Line 123
> **Code:** `ge_suite.add_expectation(`
> **Type:** Code statement

### Line 124
> **Code:** `ExpectationConfiguration(expectation_type=expectation["expectation_typ...`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `)`
> **Type:** Code statement

### Line 126
> **Code:** `return ge_suite`
> **Type:** Returns a value from a function

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `def validate_expectations_suite(df: pd.DataFrame, suite: dict) -> dict...`
> **Type:** Function definition

### Line 130
> **Code:** `try:`
> **Type:** Code statement

### Line 131
> **Code:** `from great_expectations import from_pandas  # type: ignore`
> **Type:** Imports specific names from a module

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `ge_result = from_pandas(df, expectation_suite=_to_ge_suite(suite)).val...`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `summary = {`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `"suite": suite.get("expectation_suite_name", "dataset_suite"),`
> **Type:** Code statement

### Line 136
> **Code:** `"total": int(ge_result.statistics["evaluated_expectations"]),`
> **Type:** Data structure operation

### Line 137
> **Code:** `"passed": int(ge_result.statistics["successful_expectations"]),`
> **Type:** Data structure operation

### Line 138
> **Code:** `"failed": int(ge_result.statistics["evaluated_expectations"] - ge_resu...`
> **Type:** Arithmetic operation

### Line 139
> **Code:** `"engine": "great_expectations",`
> **Type:** Code statement

### Line 140
> **Code:** `}`
> **Type:** Code statement

### Line 141
> **Code:** `if not ge_result.success:`
> **Type:** Conditional statement

### Line 142
> **Code:** `summary["failures"] = [`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `{"expectation_type": r.expectation_config.expectation_type, "detail": ...`
> **Type:** Logical operation

### Line 144
> **Code:** `for r in ge_result.results`
> **Type:** For loop

### Line 145
> **Code:** `if not r.success`
> **Type:** Conditional statement

### Line 146
> **Code:** `]`
> **Type:** Code statement

### Line 147
> **Code:** `return summary`
> **Type:** Returns a value from a function

### Line 148
> **Code:** `except Exception:  # noqa: BLE001`
> **Type:** Code statement

### Line 149
> **Code:** `return validate_dataframe(df, suite)`
> **Type:** Returns a value from a function

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `def validate(input_path: str | Path | None = None, suite_path: str | P...`
> **Type:** Function definition

### Line 153
> **Code:** `input_path = Path(input_path or DEFAULT_INPUT)`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `suite = load_suite(suite_path or DEFAULT_SUITE)`
> **Type:** Assignment/comparison

### Line 155
> **Code:** `if not input_path.exists():`
> **Type:** Conditional statement

### Line 156
> **Code:** `raise FileNotFoundError(f"Input dataset not found: {input_path}")`
> **Type:** Raises an exception

### Line 157
> **Code:** `df = pd.read_csv(input_path)`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `return validate_expectations_suite(df, suite)`
> **Type:** Returns a value from a function

### Line 159
> **Code:** ``
> **Type:** Empty line

### Line 160
> **Code:** ``
> **Type:** Empty line

### Line 161
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 162
> **Code:** `parser = argparse.ArgumentParser(description="Validate dataset against...`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `parser.add_argument("--input", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `parser.add_argument("--suite", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `parser.add_argument("--json-output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 166
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 167
> **Code:** ``
> **Type:** Empty line

### Line 168
> **Code:** `summary = validate(args.input, args.suite)`
> **Type:** Assignment/comparison

### Line 169
> **Code:** `print(f"suite={summary['suite']} passed={summary['passed']}/{summary['...`
> **Type:** Prints output to console

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `if args.json_output:`
> **Type:** Conditional statement

### Line 172
> **Code:** `Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 173
> **Code:** `with Path(args.json_output).open("w") as fh:`
> **Type:** Context manager

### Line 174
> **Code:** `json.dump(summary, fh, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 175
> **Code:** ``
> **Type:** Empty line

### Line 176
> **Code:** `if summary["failed"]:`
> **Type:** Conditional statement

### Line 177
> **Code:** `for failure in summary.get("failures", []):`
> **Type:** For loop

### Line 178
> **Code:** `print(f"  FAIL {failure.get('expectation_type')}: {failure.get('detail...`
> **Type:** Prints output to console

### Line 179
> **Code:** `raise ValidationError(f"Data validation failed: {summary['failed']} ex...`
> **Type:** Raises an exception

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** ``
> **Type:** Empty line

### Line 182
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 183
> **Code:** `try:`
> **Type:** Code statement

### Line 184
> **Code:** `main()`
> **Type:** Function call

### Line 185
> **Code:** `except ValidationError as exc:`
> **Type:** Logical operation

### Line 186
> **Code:** `print(f"validation error: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line 187
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line 188
> **Code:** `except (FileNotFoundError, OSError) as exc:`
> **Type:** Logical operation

### Line 189
> **Code:** `print(f"validation error: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line 190
> **Code:** `sys.exit(2)`
> **Type:** Function call

## Summary
- **Total lines:** 190
- **Code lines:** 148
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 39

---
*Documentation generated for: mlops-project-documentation*
*File: validation.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/data/__init__.py`
- **Total lines:** 4
- **File size:** 213 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""data package: data loading, preprocessing, and DVC-managed versioni...`
> **Type:** Arithmetic operation

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: ingestion.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/data/ingestion.py`
- **Total lines:** 102
- **File size:** 3618 bytes

## Line Type Summary
- **Code:** 79
- **Comment:** 0
- **Empty:** 20
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: high - Add tag mapping version control`
> **Type:** TODO: high - Add tag mapping version control

### Line   2
> **Code:** `# TODO: medium - Implement store-and-forward buffer health checks`
> **Type:** TODO: medium - Implement store-and-forward buffer health checks

### Line   3
> **Code:** `# TODO: low - Add unmapped tag alerting`
> **Type:** TODO: low - Add unmapped tag alerting

### Line   4
> **Code:** `"""Data ingestion: pull raw data from a source (CSV file or URL) into ...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Idempotent: re-running produces the same normalized raw dataset.`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `Source is resolved as: --source CLI arg > INGESTION_SOURCE env > defau...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  13
> **Code:** `import os`
> **Type:** Imports a module

### Line  14
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `DEFAULT_SOURCE = PROJECT_ROOT / "data" / "external" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `DEFAULT_DESTINATION = PROJECT_ROOT / "data" / "raw" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `RAW_COLUMN_TYPES: dict[str, str] = {`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `"CustomerID": "object",`
> **Type:** Code statement

### Line  24
> **Code:** `"Gender": "object",`
> **Type:** Code statement

### Line  25
> **Code:** `"SeniorCitizen": "int64",`
> **Type:** Logical operation

### Line  26
> **Code:** `"Partner": "object",`
> **Type:** Code statement

### Line  27
> **Code:** `"Dependents": "object",`
> **Type:** Code statement

### Line  28
> **Code:** `"Tenure": "int64",`
> **Type:** Code statement

### Line  29
> **Code:** `"PhoneService": "object",`
> **Type:** Code statement

### Line  30
> **Code:** `"MultipleLines": "object",`
> **Type:** Code statement

### Line  31
> **Code:** `"InternetService": "object",`
> **Type:** Code statement

### Line  32
> **Code:** `"OnlineSecurity": "object",`
> **Type:** Code statement

### Line  33
> **Code:** `"OnlineBackup": "object",`
> **Type:** Code statement

### Line  34
> **Code:** `"DeviceProtection": "object",`
> **Type:** Code statement

### Line  35
> **Code:** `"TechSupport": "object",`
> **Type:** Logical operation

### Line  36
> **Code:** `"StreamingTV": "object",`
> **Type:** Code statement

### Line  37
> **Code:** `"StreamingMovies": "object",`
> **Type:** Code statement

### Line  38
> **Code:** `"Contract": "object",`
> **Type:** Code statement

### Line  39
> **Code:** `"PaperlessBilling": "object",`
> **Type:** Code statement

### Line  40
> **Code:** `"PaymentMethod": "object",`
> **Type:** Code statement

### Line  41
> **Code:** `"MonthlyCharges": "float64",`
> **Type:** Code statement

### Line  42
> **Code:** `"TotalCharges": "float64",`
> **Type:** Code statement

### Line  43
> **Code:** `"Churn": "object",`
> **Type:** Code statement

### Line  44
> **Code:** `}`
> **Type:** Code statement

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `def _read_source(source: str | Path) -> pd.DataFrame:`
> **Type:** Function definition

### Line  48
> **Code:** `source = str(source)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `if source.startswith(("http://", "https://", "s3://")):`
> **Type:** Conditional statement

### Line  50
> **Code:** `return pd.read_csv(source)`
> **Type:** Returns a value from a function

### Line  51
> **Code:** `path = Path(source)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  53
> **Code:** `raise FileNotFoundError(f"Ingestion source not found: {source}")`
> **Type:** Raises an exception

### Line  54
> **Code:** `return pd.read_csv(path)`
> **Type:** Returns a value from a function

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def normalize(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  58
> **Code:** `df = df.copy()`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `df.columns = [c.strip() for c in df.columns]`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `for col in df.select_dtypes(include="object").columns:`
> **Type:** For loop

### Line  61
> **Code:** `df[col] = df[col].astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `for col, dtype in RAW_COLUMN_TYPES.items():`
> **Type:** For loop

### Line  63
> **Code:** `if col in df.columns:`
> **Type:** Conditional statement

### Line  64
> **Code:** `try:`
> **Type:** Code statement

### Line  65
> **Code:** `df[col] = df[col].astype(dtype)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `except (ValueError, TypeError):`
> **Type:** Logical operation

### Line  67
> **Code:** `df[col] = pd.to_numeric(df[col].str.replace(r"[$, ]", "", regex=True),...`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `def ingest(source: str | Path | None = None, destination: str | Path |...`
> **Type:** Function definition

### Line  72
> **Code:** `source = source or os.environ.get("INGESTION_SOURCE") or DEFAULT_SOURC...`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `destination = Path(destination or os.environ.get("INGESTION_DESTINATIO...`
> **Type:** Assignment/comparison

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `resolved = Path(source) if not str(source).startswith(("http", "s3")) ...`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `if isinstance(resolved, Path) and not resolved.exists():`
> **Type:** Conditional statement

### Line  77
> **Code:** `fallback = DEFAULT_DESTINATION if resolved != DEFAULT_DESTINATION else...`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `if fallback is not None and fallback.exists():`
> **Type:** Conditional statement

### Line  79
> **Code:** `resolved = fallback`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `else:`
> **Type:** Else block

### Line  81
> **Code:** `raise FileNotFoundError(f"Ingestion source not found: {source}")`
> **Type:** Raises an exception

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `df = _read_source(resolved)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `df = normalize(df)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `destination.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `df.to_csv(destination, index=False)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  92
> **Code:** `parser = argparse.ArgumentParser(description="Ingest raw churn data.")`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `parser.add_argument("--source", type=str, default=None, help="CSV path...`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `parser.add_argument("--destination", type=str, default=None, help="Out...`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `df = ingest(args.source, args.destination)`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `print(f"ingested {len(df)} rows x {len(df.columns)} columns -> data/ra...`
> **Type:** Prints output to console

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 102
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 102
- **Code lines:** 79
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 20

---
*Documentation generated for: mlops-project-documentation*
*File: ingestion.py*
---

# mlops-project-documentation: preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/data/preprocessing.py`
- **Total lines:** 87
- **File size:** 2611 bytes

## Line Type Summary
- **Code:** 64
- **Comment:** 0
- **Empty:** 20
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Data preprocessing: clean the raw dataset and produce a model-ready...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Operations (all idempotent):`
> **Type:** Code statement

### Line   7
> **Code:** `- Drop the identifier column (CustomerID).`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- Coerce numeric columns, drop rows with invalid numeric values.`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `- Ensure categorical columns contain no unexpected values.`
> **Type:** Arithmetic operation

### Line  10
> **Code:** `- Output: data/processed/dataset.csv`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `DROP_COLUMNS = ["CustomerID"]`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `NUMERIC_COLUMNS = ["Tenure", "MonthlyCharges", "TotalCharges"]`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `CATEGORICAL_COLUMNS = [`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `"Gender",`
> **Type:** Code statement

### Line  28
> **Code:** `"SeniorCitizen",`
> **Type:** Logical operation

### Line  29
> **Code:** `"Partner",`
> **Type:** Code statement

### Line  30
> **Code:** `"Dependents",`
> **Type:** Code statement

### Line  31
> **Code:** `"PhoneService",`
> **Type:** Code statement

### Line  32
> **Code:** `"MultipleLines",`
> **Type:** Code statement

### Line  33
> **Code:** `"InternetService",`
> **Type:** Code statement

### Line  34
> **Code:** `"OnlineSecurity",`
> **Type:** Code statement

### Line  35
> **Code:** `"OnlineBackup",`
> **Type:** Code statement

### Line  36
> **Code:** `"DeviceProtection",`
> **Type:** Code statement

### Line  37
> **Code:** `"TechSupport",`
> **Type:** Logical operation

### Line  38
> **Code:** `"StreamingTV",`
> **Type:** Code statement

### Line  39
> **Code:** `"StreamingMovies",`
> **Type:** Code statement

### Line  40
> **Code:** `"Contract",`
> **Type:** Code statement

### Line  41
> **Code:** `"PaperlessBilling",`
> **Type:** Code statement

### Line  42
> **Code:** `"PaymentMethod",`
> **Type:** Code statement

### Line  43
> **Code:** `]`
> **Type:** Code statement

### Line  44
> **Code:** `TARGET_COLUMN = "Churn"`
> **Type:** Assignment/comparison

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `def preprocess(input_path: str | Path | None = None, output_path: str ...`
> **Type:** Function definition

### Line  48
> **Code:** `input_path = Path(input_path or DEFAULT_INPUT)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `output_path = Path(output_path or DEFAULT_OUTPUT)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `if not input_path.exists():`
> **Type:** Conditional statement

### Line  52
> **Code:** `raise FileNotFoundError(f"Input dataset not found: {input_path}")`
> **Type:** Raises an exception

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `df = pd.read_csv(input_path)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `df = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])`
> **Type:** Assignment/comparison

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `for col in NUMERIC_COLUMNS:`
> **Type:** For loop

### Line  58
> **Code:** `if col in df.columns:`
> **Type:** Conditional statement

### Line  59
> **Code:** `df[col] = pd.to_numeric(df[col], errors="coerce")`
> **Type:** Assignment/comparison

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `df = df.dropna(subset=NUMERIC_COLUMNS).copy()`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `df = df[df["Tenure"] >= 0]`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `for col in CATEGORICAL_COLUMNS:`
> **Type:** For loop

### Line  65
> **Code:** `if col in df.columns:`
> **Type:** Conditional statement

### Line  66
> **Code:** `df[col] = df[col].astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `if TARGET_COLUMN in df.columns:`
> **Type:** Conditional statement

### Line  69
> **Code:** `df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(str).str.strip()`
> **Type:** Assignment/comparison

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `df.to_csv(output_path, index=False)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  77
> **Code:** `parser = argparse.ArgumentParser(description="Preprocess raw churn dat...`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `parser.add_argument("--input", type=str, default=None)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `parser.add_argument("--output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `df = preprocess(args.input, args.output)`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `print(f"preprocessed {len(df)} rows x {len(df.columns)} columns -> dat...`
> **Type:** Prints output to console

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  87
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 87
- **Code lines:** 64
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 20

---
*Documentation generated for: mlops-project-documentation*
*File: preprocessing.py*
---

# mlops-project-documentation: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/features/__init__.py`
- **Total lines:** 4
- **File size:** 190 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""features package: feature engineering pipeline."""`
> **Type:** Code statement

## Summary
- **Total lines:** 4
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 0

---
*Documentation generated for: mlops-project-documentation*
*File: __init__.py*
---

# mlops-project-documentation: build_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/features/build_features.py`
- **Total lines:** 157
- **File size:** 5789 bytes

## Line Type Summary
- **Code:** 125
- **Comment:** 0
- **Empty:** 29
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Feature engineering: transform processed data into model features.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Encapsulated in `FeatureTransformer` so the exact same transformations...`
> **Type:** Logical operation

### Line   7
> **Code:** `applied at training time and at inference time (no training/serving sk...`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `The fitted state (category mappings, numeric statistics, column order)...`
> **Type:** Logical operation

### Line   9
> **Code:** `persisted as a JSON config and shipped with the model as an MLflow art...`
> **Type:** Logical operation

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `Outputs:`
> **Type:** Code statement

### Line  12
> **Code:** `- data/features/features.parquet       (training features + target)`
> **Type:** Arithmetic operation

### Line  13
> **Code:** `- data/features/features_config.json   (fitted transformer state)`
> **Type:** Arithmetic operation

### Line  14
> **Code:** `"""`
> **Type:** Code statement

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  19
> **Code:** `import json`
> **Type:** Imports a module

### Line  20
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "features" / "features.parque...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `DEFAULT_CONFIG = PROJECT_ROOT / "data" / "features" / "features_config...`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `TARGET_COLUMN = "Churn"`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `TARGET_FEATURE = "churn_target"`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `NUMERIC_FEATURES = ["Tenure", "MonthlyCharges", "TotalCharges"]`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `CATEGORICAL_FEATURES = [`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `"Gender",`
> **Type:** Code statement

### Line  35
> **Code:** `"SeniorCitizen",`
> **Type:** Logical operation

### Line  36
> **Code:** `"Partner",`
> **Type:** Code statement

### Line  37
> **Code:** `"Dependents",`
> **Type:** Code statement

### Line  38
> **Code:** `"PhoneService",`
> **Type:** Code statement

### Line  39
> **Code:** `"MultipleLines",`
> **Type:** Code statement

### Line  40
> **Code:** `"InternetService",`
> **Type:** Code statement

### Line  41
> **Code:** `"OnlineSecurity",`
> **Type:** Code statement

### Line  42
> **Code:** `"OnlineBackup",`
> **Type:** Code statement

### Line  43
> **Code:** `"DeviceProtection",`
> **Type:** Code statement

### Line  44
> **Code:** `"TechSupport",`
> **Type:** Logical operation

### Line  45
> **Code:** `"StreamingTV",`
> **Type:** Code statement

### Line  46
> **Code:** `"StreamingMovies",`
> **Type:** Code statement

### Line  47
> **Code:** `"Contract",`
> **Type:** Code statement

### Line  48
> **Code:** `"PaperlessBilling",`
> **Type:** Code statement

### Line  49
> **Code:** `"PaymentMethod",`
> **Type:** Code statement

### Line  50
> **Code:** `]`
> **Type:** Code statement

### Line  51
> **Code:** `ENGINEERED_FEATURES = ["charges_per_tenure", "tenure_years", "num_serv...`
> **Type:** Assignment/comparison

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `SERVICE_COLUMNS = [`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `"OnlineSecurity",`
> **Type:** Code statement

### Line  55
> **Code:** `"OnlineBackup",`
> **Type:** Code statement

### Line  56
> **Code:** `"DeviceProtection",`
> **Type:** Code statement

### Line  57
> **Code:** `"TechSupport",`
> **Type:** Logical operation

### Line  58
> **Code:** `"StreamingTV",`
> **Type:** Code statement

### Line  59
> **Code:** `"StreamingMovies",`
> **Type:** Code statement

### Line  60
> **Code:** `]`
> **Type:** Code statement

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `FEATURE_ORDER = NUMERIC_FEATURES + ENGINEERED_FEATURES + CATEGORICAL_F...`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `def _engineer(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  66
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `out["charges_per_tenure"] = out["TotalCharges"] / (out["Tenure"] + 1)`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `out["tenure_years"] = out["Tenure"] / 12.0`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `out["num_services"] = sum((out[c].astype(str) == "Yes").astype(int) fo...`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `class FeatureTransformer:`
> **Type:** Class definition

### Line  74
> **Code:** `def __init__(self, numeric_features: list[str] | None = None, categori...`
> **Type:** Function definition

### Line  75
> **Code:** `self.numeric_features = numeric_features or NUMERIC_FEATURES`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `self.categorical_features = categorical_features or CATEGORICAL_FEATUR...`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `self.category_mappings: dict[str, dict[str, int]] = {}`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `self.numeric_stats: dict[str, dict[str, float]] = {}`
> **Type:** Assignment/comparison

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def fit(self, df: pd.DataFrame) -> FeatureTransformer:`
> **Type:** Function definition

### Line  81
> **Code:** `data = _engineer(df)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `for col in self.categorical_features:`
> **Type:** For loop

### Line  83
> **Code:** `categories = sorted(data[col].astype(str).unique())`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `self.category_mappings[col] = {cat: i for i, cat in enumerate(categori...`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `for col in self.numeric_features:`
> **Type:** For loop

### Line  86
> **Code:** `self.numeric_stats[col] = {"mean": float(data[col].mean()), "std": flo...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `return self`
> **Type:** Returns a value from a function

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def transform(self, df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  90
> **Code:** `data = _engineer(df).copy()`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `for col in self.categorical_features:`
> **Type:** For loop

### Line  92
> **Code:** `mapping = self.category_mappings.get(col, {})`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `data[col] = data[col].astype(str).map(mapping).fillna(-1).astype(int)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `for col in self.numeric_features:`
> **Type:** For loop

### Line  95
> **Code:** `data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0).asty...`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `for col in ENGINEERED_FEATURES:`
> **Type:** For loop

### Line  97
> **Code:** `data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0).asty...`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `return data[FEATURE_ORDER]`
> **Type:** Returns a value from a function

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line 101
> **Code:** `return self.fit(df).transform(df)`
> **Type:** Returns a value from a function

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `def to_config(self) -> dict:`
> **Type:** Function definition

### Line 104
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 105
> **Code:** `"numeric_features": self.numeric_features,`
> **Type:** Code statement

### Line 106
> **Code:** `"categorical_features": self.categorical_features,`
> **Type:** Logical operation

### Line 107
> **Code:** `"category_mappings": self.category_mappings,`
> **Type:** Logical operation

### Line 108
> **Code:** `"numeric_stats": self.numeric_stats,`
> **Type:** Code statement

### Line 109
> **Code:** `"feature_order": FEATURE_ORDER,`
> **Type:** Logical operation

### Line 110
> **Code:** `}`
> **Type:** Code statement

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `@classmethod`
> **Type:** Code statement

### Line 113
> **Code:** `def from_config(cls, config: dict) -> FeatureTransformer:`
> **Type:** Function definition

### Line 114
> **Code:** `transformer = cls(config["numeric_features"], config["categorical_feat...`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `transformer.category_mappings = config["category_mappings"]`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `transformer.numeric_stats = config["numeric_stats"]`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `return transformer`
> **Type:** Returns a value from a function

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `def build_features(`
> **Type:** Function definition

### Line 121
> **Code:** `input_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `output_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `config_path: str | Path | None = None,`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `) -> pd.DataFrame:`
> **Type:** Arithmetic operation

### Line 125
> **Code:** `input_path = Path(input_path or DEFAULT_INPUT)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `output_path = Path(output_path or DEFAULT_OUTPUT)`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `config_path = Path(config_path or DEFAULT_CONFIG)`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `if not input_path.exists():`
> **Type:** Conditional statement

### Line 130
> **Code:** `raise FileNotFoundError(f"Input dataset not found: {input_path}")`
> **Type:** Raises an exception

### Line 131
> **Code:** ``
> **Type:** Empty line

### Line 132
> **Code:** `df = pd.read_csv(input_path)`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `transformer = FeatureTransformer().fit(df)`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `features = transformer.fit_transform(df)`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `if TARGET_COLUMN in df.columns:`
> **Type:** Conditional statement

### Line 136
> **Code:** `features[TARGET_FEATURE] = (df[TARGET_COLUMN].astype(str).str.lower() ...`
> **Type:** Assignment/comparison

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `features.to_parquet(output_path, index=False)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `with config_path.open("w") as fh:`
> **Type:** Context manager

### Line 141
> **Code:** `json.dump(transformer.to_config(), fh, indent=2)`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `return features`
> **Type:** Returns a value from a function

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** ``
> **Type:** Empty line

### Line 145
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 146
> **Code:** `parser = argparse.ArgumentParser(description="Build features from proc...`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `parser.add_argument("--input", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `parser.add_argument("--output", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `parser.add_argument("--config", type=str, default=None)`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `features = build_features(args.input, args.output, args.config)`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `print(f"built {features.shape[0]} rows x {features.shape[1]} features ...`
> **Type:** Prints output to console

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 157
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 157
- **Code lines:** 125
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 29

---
*Documentation generated for: mlops-project-documentation*
*File: build_features.py*
---

# mlops-project-documentation: feature_store.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-project-documentation/.worktrees/proj4/src/features/feature_store.py`
- **Total lines:** 118
- **File size:** 5899 bytes

## Line Type Summary
- **Code:** 95
- **Comment:** 0
- **Empty:** 20
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `# TODO: medium - Add type hints where missing`
> **Type:** TODO: medium - Add type hints where missing

### Line   2
> **Code:** `# TODO: low - Add comprehensive docstring`
> **Type:** TODO: low - Add comprehensive docstring

### Line   3
> **Code:** `# TODO: low - Add error handling for edge cases`
> **Type:** TODO: low - Add error handling for edge cases

### Line   4
> **Code:** `"""Lightweight Parquet feature store, versioned by DVC.`
> **Type:** Logical operation

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `Each `put_features` writes data/features/features_v{N}.parquet togethe...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `documented schema (name, type, description, expected range). DVC versi...`
> **Type:** Code statement

### Line   8
> **Code:** `Parquet files; a Git commit pins the exact feature snapshot used for t...`
> **Type:** Logical operation

### Line   9
> **Code:** `so any production model can be traced back to its feature set.`
> **Type:** Code statement

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  15
> **Code:** `import json`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `DEFAULT_DIR = PROJECT_ROOT / "data" / "features"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `SCHEMA_FILE = "features_store_schema.json"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `FEATURE_SCHEMA = {`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `"Tenure": {"type": "float64", "description": "Months the customer has ...`
> **Type:** Data structure operation

### Line  26
> **Code:** `"MonthlyCharges": {"type": "float64", "description": "Monthly subscrip...`
> **Type:** Data structure operation

### Line  27
> **Code:** `"TotalCharges": {"type": "float64", "description": "Total charges paid...`
> **Type:** Data structure operation

### Line  28
> **Code:** `"charges_per_tenure": {`
> **Type:** Code statement

### Line  29
> **Code:** `"type": "float64",`
> **Type:** Code statement

### Line  30
> **Code:** `"description": "TotalCharges / (Tenure + 1)",`
> **Type:** Arithmetic operation

### Line  31
> **Code:** `"expected_range": [0, 1000],`
> **Type:** Data structure operation

### Line  32
> **Code:** `},`
> **Type:** Code statement

### Line  33
> **Code:** `"tenure_years": {"type": "float64", "description": "Tenure expressed i...`
> **Type:** Data structure operation

### Line  34
> **Code:** `"num_services": {"type": "int64", "description": "Number of subscribed...`
> **Type:** Data structure operation

### Line  35
> **Code:** `"Gender": {"type": "int64", "description": "Encoded gender (0/1)", "ex...`
> **Type:** Arithmetic operation

### Line  36
> **Code:** `"SeniorCitizen": {"type": "int64", "description": "1 if senior citizen...`
> **Type:** Logical operation

### Line  37
> **Code:** `"Partner": {"type": "int64", "description": "1 if has partner", "expec...`
> **Type:** Data structure operation

### Line  38
> **Code:** `"Dependents": {"type": "int64", "description": "1 if has dependents", ...`
> **Type:** Data structure operation

### Line  39
> **Code:** `"PhoneService": {"type": "int64", "description": "1 if has phone servi...`
> **Type:** Data structure operation

### Line  40
> **Code:** `"MultipleLines": {"type": "int64", "description": "Encoded multiple li...`
> **Type:** Arithmetic operation

### Line  41
> **Code:** `"InternetService": {"type": "int64", "description": "Encoded internet ...`
> **Type:** Arithmetic operation

### Line  42
> **Code:** `"OnlineSecurity": {"type": "int64", "description": "Encoded online sec...`
> **Type:** Arithmetic operation

### Line  43
> **Code:** `"OnlineBackup": {"type": "int64", "description": "Encoded online backu...`
> **Type:** Arithmetic operation

### Line  44
> **Code:** `"DeviceProtection": {"type": "int64", "description": "Encoded device p...`
> **Type:** Arithmetic operation

### Line  45
> **Code:** `"TechSupport": {"type": "int64", "description": "Encoded tech support"...`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `"StreamingTV": {"type": "int64", "description": "Encoded streaming TV"...`
> **Type:** Arithmetic operation

### Line  47
> **Code:** `"StreamingMovies": {"type": "int64", "description": "Encoded streaming...`
> **Type:** Arithmetic operation

### Line  48
> **Code:** `"Contract": {"type": "int64", "description": "Encoded contract type", ...`
> **Type:** Arithmetic operation

### Line  49
> **Code:** `"PaperlessBilling": {"type": "int64", "description": "1 if paperless b...`
> **Type:** Data structure operation

### Line  50
> **Code:** `"PaymentMethod": {"type": "int64", "description": "Encoded payment met...`
> **Type:** Arithmetic operation

### Line  51
> **Code:** `"churn_target": {"type": "int64", "description": "Target: 1 if custome...`
> **Type:** Data structure operation

### Line  52
> **Code:** `}`
> **Type:** Code statement

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `class FeatureStore:`
> **Type:** Class definition

### Line  56
> **Code:** `def __init__(self, base_dir: str | Path | None = None):`
> **Type:** Function definition

### Line  57
> **Code:** `self.base_dir = Path(base_dir or DEFAULT_DIR)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `self.base_dir.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `def _version_file(self, version: int) -> Path:`
> **Type:** Function definition

### Line  61
> **Code:** `return self.base_dir / f"features_v{version}.parquet"`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `def next_version(self) -> int:`
> **Type:** Function definition

### Line  64
> **Code:** `versions = [p.stem.split("_v")[-1] for p in self.base_dir.glob("featur...`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `return max((int(v) for v in versions), default=0) + 1`
> **Type:** Returns a value from a function

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** `def put_features(self, df: pd.DataFrame, version: int | None = None) -...`
> **Type:** Function definition

### Line  68
> **Code:** `version = version or self.next_version()`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `df.to_parquet(self._version_file(version), index=False)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `self.write_schema(df)`
> **Type:** Function call

### Line  71
> **Code:** `return version`
> **Type:** Returns a value from a function

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def get_features(self, version: int | None = None) -> pd.DataFrame:`
> **Type:** Function definition

### Line  74
> **Code:** `if version is None:`
> **Type:** Conditional statement

### Line  75
> **Code:** `version = max(1, self.next_version() - 1)`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `path = self._version_file(version)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  78
> **Code:** `raise FileNotFoundError(f"Feature version not found: {path}")`
> **Type:** Raises an exception

### Line  79
> **Code:** `return pd.read_parquet(path)`
> **Type:** Returns a value from a function

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `def list_versions(self) -> list[int]:`
> **Type:** Function definition

### Line  82
> **Code:** `return sorted(int(p.stem.split("_v")[-1]) for p in self.base_dir.glob(...`
> **Type:** Returns a value from a function

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `def write_schema(self, df: pd.DataFrame) -> None:`
> **Type:** Function definition

### Line  85
> **Code:** `schema = {"store": "lightweight-parquet", "versioned_by": "dvc", "feat...`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `for col in df.columns:`
> **Type:** For loop

### Line  87
> **Code:** `entry = dict(FEATURE_SCHEMA.get(col, {"type": str(df[col].dtype), "des...`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `entry["dtype"] = str(df[col].dtype)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `schema["features"][col] = entry`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `with (self.base_dir / SCHEMA_FILE).open("w") as fh:`
> **Type:** Context manager

### Line  91
> **Code:** `json.dump(schema, fh, indent=2)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `def schema(self) -> dict:`
> **Type:** Function definition

### Line  94
> **Code:** `path = self.base_dir / SCHEMA_FILE`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  96
> **Code:** `return {}`
> **Type:** Returns a value from a function

### Line  97
> **Code:** `with path.open() as fh:`
> **Type:** Context manager

### Line  98
> **Code:** `return json.load(fh)`
> **Type:** Returns a value from a function

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 102
> **Code:** `parser = argparse.ArgumentParser(description="Inspect the lightweight ...`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `parser.add_argument("--list-versions", action="store_true")`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `parser.add_argument("--schema", action="store_true")`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `parser.add_argument("--show", type=int, default=None, help="Show head ...`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `store = FeatureStore()`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `if args.list_versions:`
> **Type:** Conditional statement

### Line 110
> **Code:** `print(f"versions: {store.list_versions()}")`
> **Type:** Prints output to console

### Line 111
> **Code:** `if args.schema:`
> **Type:** Conditional statement

### Line 112
> **Code:** `print(json.dumps(store.schema(), indent=2))`
> **Type:** Prints output to console

### Line 113
> **Code:** `if args.show is not None:`
> **Type:** Conditional statement

### Line 114
> **Code:** `print(store.get_features(args.show).head(5).to_string())`
> **Type:** Prints output to console

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** ``
> **Type:** Empty line

### Line 117
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 118
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 118
- **Code lines:** 95
- **Comments:** 0
- **TODO items:** 3
- **Empty lines:** 20

---
*Documentation generated for: mlops-project-documentation*
*File: feature_store.py*
---

