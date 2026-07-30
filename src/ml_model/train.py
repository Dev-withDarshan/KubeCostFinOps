"""
train.py — Model Training for Demand Forecasting

Trains an ML model (e.g., XGBoost, LSTM, or Prophet) on preprocessed
Kubernetes usage metrics to forecast upcoming demand spikes
(exam-period traffic patterns).

Designed to run locally or on Amazon SageMaker.

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import logging
from typing import Any, Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def build_model(model_type: str = "xgboost", hyperparams: Optional[Dict[str, Any]] = None) -> Any:
    """Instantiate and return an untrained forecasting model.

    Args:
        model_type: One of 'xgboost', 'lstm', or 'prophet'.
        hyperparams: Optional dictionary of model hyperparameters.

    Returns:
        An untrained model object.
    """
    # TODO: Instantiate the selected model with hyperparams
    raise NotImplementedError


def train_model(model: Any, train_df: pd.DataFrame, target_col: str = "cpu_utilisation") -> Any:
    """Train the model on the provided training data.

    Args:
        model: An untrained model object from build_model().
        train_df: Training DataFrame (features + target).
        target_col: Name of the target column.

    Returns:
        The trained model.
    """
    # TODO: Fit model on train_df
    raise NotImplementedError


def evaluate_model(model: Any, test_df: pd.DataFrame, target_col: str = "cpu_utilisation") -> Dict[str, float]:
    """Evaluate model performance on the test set.

    Args:
        model: A trained model.
        test_df: Test DataFrame.
        target_col: Name of the target column.

    Returns:
        A dictionary of evaluation metrics (e.g., MAE, RMSE, MAPE).
    """
    # TODO: Generate predictions and compute metrics
    raise NotImplementedError


def save_model(model: Any, output_path: str) -> str:
    """Serialize and save the trained model to disk or S3.

    Args:
        model: A trained model object.
        output_path: Local or S3 path for the saved model artifact.

    Returns:
        The path where the model was saved.
    """
    # TODO: Save model artifact (joblib / pickle / SageMaker format)
    raise NotImplementedError
