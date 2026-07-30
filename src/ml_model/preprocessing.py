"""
preprocessing.py — Data Preprocessing for Demand Forecasting

Loads raw Prometheus / CloudWatch metrics, cleans missing values,
engineers time-based features (hour, day-of-week, exam-period flags),
and produces train/test splits ready for model training.

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import logging
from typing import Any, Dict, Tuple

import pandas as pd

logger = logging.getLogger(__name__)


def load_raw_metrics(filepath: str) -> pd.DataFrame:
    """Load raw metric data from a CSV or Parquet file.

    Args:
        filepath: Path to the raw metrics file.

    Returns:
        A pandas DataFrame with raw metric records.
    """
    # TODO: Support CSV and Parquet formats
    raise NotImplementedError


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values, remove duplicates, and fix data types.

    Args:
        df: Raw metrics DataFrame.

    Returns:
        Cleaned DataFrame.
    """
    # TODO: Implement data cleaning pipeline
    raise NotImplementedError


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based and domain-specific features.

    Features to generate:
        - hour_of_day, day_of_week, is_weekend
        - is_exam_period (based on academic calendar dates)
        - rolling averages of CPU / memory utilisation

    Args:
        df: Cleaned metrics DataFrame.

    Returns:
        DataFrame with additional feature columns.
    """
    # TODO: Implement feature engineering logic
    raise NotImplementedError


def split_data(
    df: pd.DataFrame,
    test_ratio: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataset into training and testing sets (time-aware split).

    Args:
        df: Feature-engineered DataFrame, sorted by timestamp.
        test_ratio: Fraction of data to reserve for testing (default: 20%).

    Returns:
        A tuple of (train_df, test_df).
    """
    # TODO: Implement chronological train/test split
    raise NotImplementedError
