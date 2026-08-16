"""Tests for src.data.preprocessing module."""

import pandas as pd
import pytest

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocessing import preprocess, DROP_COLUMNS, NUMERIC_COLUMNS, CATEGORICAL_COLUMNS, TARGET_COLUMN


class TestPreprocessing:
    """Test preprocessing correctness."""

    def _run(self, df, tmp_path):
        """Write df to a CSV and run preprocess with file paths."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"
        df.to_csv(input_file, index=False)
        return preprocess(input_file, output_file)

    def test_drop_customer_id(self, tmp_path):
        """CustomerID column should be dropped."""
        df = pd.DataFrame({
            "CustomerID": ["123", "456"],
            "Gender": ["Male", "Female"],
            "SeniorCitizen": [0, 1],
            "Partner": ["Yes", "No"],
            "Dependents": ["No", "Yes"],
            "Tenure": [12, 24],
            "PhoneService": ["Yes", "Yes"],
            "MultipleLines": ["No", "Yes"],
            "InternetService": ["DSL", "Fiber optic"],
            "OnlineSecurity": ["Yes", "No"],
            "OnlineBackup": ["No", "Yes"],
            "DeviceProtection": ["No", "No"],
            "TechSupport": ["Yes", "No"],
            "StreamingTV": ["No", "No"],
            "StreamingMovies": ["No", "No"],
            "Contract": ["Month-to-month", "One year"],
            "PaperlessBilling": ["No", "Yes"],
            "PaymentMethod": ["Electronic check", "Mailed check"],
            "MonthlyCharges": [50.0, 70.0],
            "TotalCharges": [600.0, 1680.0],
            "Churn": ["No", "Yes"],
        })
        result = self._run(df, tmp_path)
        assert "CustomerID" not in result.columns

    def test_numeric_columns_coerced(self, tmp_path):
        """Numeric columns should be coerced, invalid rows dropped."""
        df = pd.DataFrame({
            "CustomerID": ["1", "2", "3"],
            "Gender": ["Male", "Female", "Male"],
            "SeniorCitizen": [0, 1, 0],
            "Partner": ["Yes", "No", "Yes"],
            "Dependents": ["No", "Yes", "No"],
            "Tenure": [12, "invalid", 24],
            "PhoneService": ["Yes", "Yes", "Yes"],
            "MultipleLines": ["No", "Yes", "No"],
            "InternetService": ["DSL", "Fiber optic", "DSL"],
            "OnlineSecurity": ["Yes", "No", "Yes"],
            "OnlineBackup": ["No", "Yes", "No"],
            "DeviceProtection": ["No", "No", "Yes"],
            "TechSupport": ["Yes", "No", "Yes"],
            "StreamingTV": ["No", "No", "No"],
            "StreamingMovies": ["No", "No", "No"],
            "Contract": ["Month-to-month", "One year", "Two year"],
            "PaperlessBilling": ["No", "Yes", "No"],
            "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)"],
            "MonthlyCharges": [50.0, 70.0, 90.0],
            "TotalCharges": [600.0, "bad", 2160.0],
            "Churn": ["No", "Yes", "No"],
        })
        result = self._run(df, tmp_path)
        assert len(result) == 2
        assert result["Tenure"].dtype in ("int64", "float64")
        assert result["TotalCharges"].dtype in ("int64", "float64")
        assert result["MonthlyCharges"].dtype in ("int64", "float64")

    def test_negative_tenure_dropped(self, tmp_path):
        """Rows with negative Tenure should be dropped."""
        df = pd.DataFrame({
            "CustomerID": ["1", "2"],
            "Gender": ["Male", "Female"],
            "SeniorCitizen": [0, 1],
            "Partner": ["Yes", "No"],
            "Dependents": ["No", "Yes"],
            "Tenure": [-5, 10],
            "PhoneService": ["Yes", "Yes"],
            "MultipleLines": ["No", "Yes"],
            "InternetService": ["DSL", "Fiber optic"],
            "OnlineSecurity": ["Yes", "No"],
            "OnlineBackup": ["No", "Yes"],
            "DeviceProtection": ["No", "No"],
            "TechSupport": ["Yes", "No"],
            "StreamingTV": ["No", "No"],
            "StreamingMovies": ["No", "No"],
            "Contract": ["Month-to-month", "One year"],
            "PaperlessBilling": ["No", "Yes"],
            "PaymentMethod": ["Electronic check", "Mailed check"],
            "MonthlyCharges": [50.0, 70.0],
            "TotalCharges": [600.0, 700.0],
            "Churn": ["No", "Yes"],
        })
        result = self._run(df, tmp_path)
        assert len(result) == 1
        assert result["Tenure"].iloc[0] == 10

    def test_categorical_stripped(self, tmp_path):
        """Categorical columns should be stripped of whitespace."""
        df = pd.DataFrame({
            "CustomerID": ["1"],
            "Gender": [" Male "],
            "SeniorCitizen": [0],
            "Partner": [" Yes "],
            "Dependents": ["No "],
            "Tenure": [12],
            "PhoneService": ["Yes"],
            "MultipleLines": ["No"],
            "InternetService": [" DSL "],
            "OnlineSecurity": ["Yes"],
            "OnlineBackup": ["No"],
            "DeviceProtection": ["No"],
            "TechSupport": ["Yes"],
            "StreamingTV": ["No"],
            "StreamingMovies": ["No"],
            "Contract": ["Month-to-month"],
            "PaperlessBilling": ["No"],
            "PaymentMethod": ["Electronic check"],
            "MonthlyCharges": [50.0],
            "TotalCharges": [600.0],
            "Churn": [" No "],
        })
        result = self._run(df, tmp_path)
        assert result["Gender"].iloc[0] == "Male"
        assert result["Partner"].iloc[0] == "Yes"
        assert result["InternetService"].iloc[0] == "DSL"
        assert result["Churn"].iloc[0] == "No"

    def test_target_column_preserved(self, tmp_path):
        """Target column (Churn) should be preserved and stripped."""
        df = pd.DataFrame({
            "CustomerID": ["1"],
            "Gender": ["Male"],
            "SeniorCitizen": [0],
            "Partner": ["Yes"],
            "Dependents": ["No"],
            "Tenure": [12],
            "PhoneService": ["Yes"],
            "MultipleLines": ["No"],
            "InternetService": ["DSL"],
            "OnlineSecurity": ["Yes"],
            "OnlineBackup": ["No"],
            "DeviceProtection": ["No"],
            "TechSupport": ["Yes"],
            "StreamingTV": ["No"],
            "StreamingMovies": ["No"],
            "Contract": ["Month-to-month"],
            "PaperlessBilling": ["No"],
            "PaymentMethod": ["Electronic check"],
            "MonthlyCharges": [50.0],
            "TotalCharges": [600.0],
            "Churn": [" Yes "],
        })
        result = self._run(df, tmp_path)
        assert TARGET_COLUMN in result.columns
        assert result[TARGET_COLUMN].iloc[0] == "Yes"

    def test_output_columns_match_expected(self, tmp_path):
        """Output should have all expected columns except CustomerID."""
        df = pd.DataFrame({
            "CustomerID": ["1"],
            "Gender": ["Male"],
            "SeniorCitizen": [0],
            "Partner": ["Yes"],
            "Dependents": ["No"],
            "Tenure": [12],
            "PhoneService": ["Yes"],
            "MultipleLines": ["No"],
            "InternetService": ["DSL"],
            "OnlineSecurity": ["Yes"],
            "OnlineBackup": ["No"],
            "DeviceProtection": ["No"],
            "TechSupport": ["Yes"],
            "StreamingTV": ["No"],
            "StreamingMovies": ["No"],
            "Contract": ["Month-to-month"],
            "PaperlessBilling": ["No"],
            "PaymentMethod": ["Electronic check"],
            "MonthlyCharges": [50.0],
            "TotalCharges": [600.0],
            "Churn": ["No"],
        })
        result = self._run(df, tmp_path)
        expected_cols = set(NUMERIC_COLUMNS + CATEGORICAL_COLUMNS + [TARGET_COLUMN])
        assert set(result.columns) == expected_cols

    def test_preprocess_with_file_paths(self, tmp_path):
        """Test preprocess with file input/output paths."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"
        
        df = pd.DataFrame({
            "CustomerID": ["1"],
            "Gender": ["Male"],
            "SeniorCitizen": [0],
            "Partner": ["Yes"],
            "Dependents": ["No"],
            "Tenure": [12],
            "PhoneService": ["Yes"],
            "MultipleLines": ["No"],
            "InternetService": ["DSL"],
            "OnlineSecurity": ["Yes"],
            "OnlineBackup": ["No"],
            "DeviceProtection": ["No"],
            "TechSupport": ["Yes"],
            "StreamingTV": ["No"],
            "StreamingMovies": ["No"],
            "Contract": ["Month-to-month"],
            "PaperlessBilling": ["No"],
            "PaymentMethod": ["Electronic check"],
            "MonthlyCharges": [50.0],
            "TotalCharges": [600.0],
            "Churn": ["No"],
        })
        df.to_csv(input_file, index=False)
        
        result = preprocess(input_file, output_file)
        
        assert output_file.exists()
        assert len(result) == 1
        assert "CustomerID" not in result.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])