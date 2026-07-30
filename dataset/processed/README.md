# Processed Data

This folder contains **cleaned and feature-engineered data** ready for ML model training and evaluation.

## Expected Contents (Phase-II)

- `features_train.csv` — Training feature set with time-series features and academic calendar indicators
- `features_test.csv` — Test feature set for model evaluation
- `labels_train.csv` — Training labels (target variable: resource demand)
- `labels_test.csv` — Test labels for accuracy measurement

## Preprocessing Pipeline

Data processing is handled by `src/ml_model/preprocessing.py` and includes:

1. **Missing value imputation** — Forward-fill for time-series gaps
2. **Resampling** — Aggregation to 15-minute intervals for model training
3. **Feature engineering** — Lag features, rolling averages, day-of-week indicators, exam-period flags
4. **Normalization** — Min-max scaling for numerical features
5. **Train/test split** — Chronological split (80/20) to prevent data leakage

> **Note:** Processed data files will be generated during Phase-II after raw data collection and preprocessing.
