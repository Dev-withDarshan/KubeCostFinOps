"""
preprocessing.py — Data Preprocessing Interface for Demand Forecasting

Architectural Scope Notice:
  This module defines the planned interface for enterprise AWS data pipelines.
  In the current verified local prototype, operational timeseries validation,
  chronological sorting, diurnal feature engineering, and holdout splitting are
  actively implemented, tested, and served via `src/finops_engine/ml_forecast.py`.

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
