# TODO: medium - Add type hints where missing
# TODO: low - Add comprehensive docstring
# TODO: low - Add error handling for edge cases
"""Data validation with Great Expectations.

Loads a declarative expectation suite (great_expectations/expectations/dataset_suite.json)
and validates a pandas DataFrame against it. Uses the Great Expectations API when
available, and falls back to a lightweight built-in evaluator for the same
expectation types so validation always runs in CI.

Exits non-zero if any expectation fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SUITE = PROJECT_ROOT / "great_expectations" / "expectations" / "dataset_suite.json"
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "demand_data.csv"

SUPPORTED_EXPECTATIONS = [
    "expect_table_row_count_to_be_between",
    "expect_column_values_to_not_be_null",
    "expect_column_values_to_be_between",
    "expect_column_values_to_be_in_set",
    "expect_column_values_to_be_of_type",
    "expect_column_values_to_not_match_regex",
]


class ValidationError(RuntimeError):
    pass


def load_suite(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Expectation suite not found: {path}")
    with path.open() as fh:
        return json.load(fh)


def _check_expectation(df: pd.DataFrame, expectation: dict) -> tuple[bool, str]:
    kind = expectation["expectation_type"]
    kwargs = expectation.get("kwargs", {})
    column = kwargs.get("column")

    if kind == "expect_table_row_count_to_be_between":
        return kwargs["min_value"] <= len(df) <= kwargs["max_value"], f"row count {len(df)}"

    if column is None or column not in df.columns:
        return False, f"column '{column}' missing"

    if kind == "expect_column_values_to_not_be_null":
        bad = int(df[column].isna().sum())
        return bad == 0, f"{bad} null values in {column}"

    if kind == "expect_column_values_to_be_between":
        if not pd.api.types.is_numeric_dtype(df[column]):
            return False, f"{column} not numeric"
        vals = df[column].dropna()
        lo, hi = kwargs.get("min_value", -float("inf")), kwargs.get("max_value", float("inf"))
        bad = int(((vals < lo) | (vals > hi)).sum())
        return bad == 0, f"{bad} values outside [{lo}, {hi}] in {column}"

    if kind == "expect_column_values_to_be_in_set":
        allowed = set(kwargs.get("value_set", []))
        vals = df[column].dropna().astype(str).str.strip()
        bad = int((~vals.isin(allowed)).sum())
        return bad == 0, f"{bad} unexpected values in {column}"

    if kind == "expect_column_values_to_be_of_type":
        actual = str(df[column].dtype)
        expected = kwargs.get("type_")
        return actual == expected, f"{column} dtype {actual} != {expected}"

    if kind == "expect_column_values_to_not_match_regex":
        pattern = kwargs.get("regex")
        matches = df[column].dropna().astype(str).str.contains(pattern, regex=True)
        bad = int(matches.sum())
        return bad == 0, f"{bad} rows match forbidden regex in {column}"

    return True, f"unsupported expectation {kind} ignored"


def validate_dataframe(df: pd.DataFrame, suite: dict) -> dict:
    results = []
    failures = 0
    for expectation in suite.get("expectations", []):
        kind = expectation["expectation_type"]
        if kind not in SUPPORTED_EXPECTATIONS:
            continue
        try:
            success, detail = _check_expectation(df, expectation)
        except Exception as exc:  # noqa: BLE001
            success, detail = False, str(exc)
        results.append({"expectation_type": kind, "kwargs": expectation.get("kwargs", {}), "success": success, "detail": detail})
        failures += 0 if success else 1

    summary = {
        "suite": suite.get("expectation_suite_name", "dataset_suite"),
        "total": len(results),
        "passed": len(results) - failures,
        "failed": failures,
        "results": results,
    }
    return summary


def _to_ge_suite(suite: dict):
    from great_expectations.core import ExpectationSuite
    from great_expectations.expectations.expectation import ExpectationConfiguration

    ge_suite = ExpectationSuite(expectation_suite_name=suite.get("expectation_suite_name", "dataset_suite"))
    for expectation in suite.get("expectations", []):
        if expectation["expectation_type"] in SUPPORTED_EXPECTATIONS:
            ge_suite.add_expectation(
                ExpectationConfiguration(expectation_type=expectation["expectation_type"], kwargs=expectation.get("kwargs", {}))
            )
    return ge_suite


def validate_expectations_suite(df: pd.DataFrame, suite: dict) -> dict:
    try:
        from great_expectations import from_pandas  # type: ignore

        ge_result = from_pandas(df, expectation_suite=_to_ge_suite(suite)).validate()
        summary = {
            "suite": suite.get("expectation_suite_name", "dataset_suite"),
            "total": int(ge_result.statistics["evaluated_expectations"]),
            "passed": int(ge_result.statistics["successful_expectations"]),
            "failed": int(ge_result.statistics["evaluated_expectations"] - ge_result.statistics["successful_expectations"]),
            "engine": "great_expectations",
        }
        if not ge_result.success:
            summary["failures"] = [
                {"expectation_type": r.expectation_config.expectation_type, "detail": r.exception_message or "failed"}
                for r in ge_result.results
                if not r.success
            ]
        return summary
    except Exception:  # noqa: BLE001
        return validate_dataframe(df, suite)


def validate(input_path: str | Path | None = None, suite_path: str | Path | None = None) -> dict:
    input_path = Path(input_path or DEFAULT_INPUT)
    suite = load_suite(suite_path or DEFAULT_SUITE)
    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")
    df = pd.read_csv(input_path)
    return validate_expectations_suite(df, suite)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate dataset against Great Expectations suite.")
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--suite", type=str, default=None)
    parser.add_argument("--json-output", type=str, default=None)
    args = parser.parse_args()

    summary = validate(args.input, args.suite)
    print(f"suite={summary['suite']} passed={summary['passed']}/{summary['total']} failed={summary['failed']}")

    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        with Path(args.json_output).open("w") as fh:
            json.dump(summary, fh, indent=2, default=str)

    if summary["failed"]:
        for failure in summary.get("failures", []):
            print(f"  FAIL {failure.get('expectation_type')}: {failure.get('detail')}")
        raise ValidationError(f"Data validation failed: {summary['failed']} expectation(s) not met")


if __name__ == "__main__":
    try:
        main()
    except ValidationError as exc:
        print(f"validation error: {exc}", file=sys.stderr)
        sys.exit(1)
    except (FileNotFoundError, OSError) as exc:
        print(f"validation error: {exc}", file=sys.stderr)
        sys.exit(2)
