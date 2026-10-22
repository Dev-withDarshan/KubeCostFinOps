"""
ml_forecast.py — Baseline Resource & Demand Forecasting Engine

Provides deterministic, lightweight statistical forecasting baselines (Simple Exponential
Smoothing, Holt's Linear Trend) for Kubernetes resource demand and educational workload telemetry.

Key Architectural Principles:
1. Strict Provenance: Clearly separates live cluster state observations from synthetic demonstration data.
2. Explicit Disclaimers: KSM snapshots represent object specifications (requested capacity),
   NOT continuous CPU/memory utilization timeseries or live application traffic.
3. Insufficient Data Integrity: Never fabricates forecasts from inadequate history. Explicitly
   rejects datasets smaller than the required threshold.
4. Zero Heavy Dependencies: Standard Python math/statistics with deterministic random seeding.

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import datetime
import glob
import json
import logging
import math
import os
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

MINIMUM_HISTORY_OBSERVATIONS = 5
DEFAULT_FORECAST_HORIZON = 6
DEFAULT_ALPHA = 0.35  # Level smoothing parameter
DEFAULT_BETA = 0.15   # Trend smoothing parameter

FORECAST_DISCLAIMER = (
    "STATISTICAL BASELINE FORECAST: Generated using Holt's Linear Trend / Exponential "
    "Smoothing models. This is an exploratory capacity planning tool, not an SLA guarantee. "
    "KSM state metrics reflect requested pod allocations; they do not measure actual OS kernel "
    "CPU/RAM utilization or external user request volumes unless telemetry is explicitly paired."
)

SYNTHETIC_DISCLAIMER = (
    "SYNTHETIC DEMONSTRATION TELEMETRY: Generated via deterministic diurnal trigonometric "
    "simulation with pseudo-random Gaussian noise. NOT derived from real production monitoring. "
    "Designed exclusively for educational and architectural validation."
)


class InsufficientDataError(ValueError):
    """Raised when historical observations are fewer than the required threshold."""
    pass


def validate_and_sort_timeseries(
    data: List[Dict[str, Any]],
    time_key: str = "timestamp",
    val_key: str = "value",
) -> List[Tuple[datetime.datetime, float]]:
    """Validate and sort a list of timeseries observation dictionaries.

    Args:
        data: List of dicts containing a timestamp and a numeric value.
        time_key: Key name for the timestamp (ISO 8601 string or datetime).
        val_key: Key name for the observation value.

    Returns:
        List of (datetime, float) tuples sorted chronologically ascending.

    Raises:
        ValueError: If entries are missing keys, unparseable, or invalid.
    """
    if not isinstance(data, list):
        raise ValueError("Input timeseries must be a list of records.")

    cleaned: List[Tuple[datetime.datetime, float]] = []
    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError(f"Record at index {idx} must be a dictionary.")

        if time_key not in entry or val_key not in entry:
            raise ValueError(f"Record at index {idx} missing required keys '{time_key}' or '{val_key}'.")

        raw_ts = entry[time_key]
        raw_val = entry[val_key]

        # Parse timestamp
        if isinstance(raw_ts, datetime.datetime):
            dt = raw_ts
        elif isinstance(raw_ts, str):
            try:
                # Handle ISO format with Z or timezone offsets
                clean_ts = raw_ts.replace("Z", "+00:00")
                dt = datetime.datetime.fromisoformat(clean_ts)
            except ValueError as exc:
                raise ValueError(f"Unparseable ISO timestamp '{raw_ts}' at index {idx}: {exc}") from exc
        else:
            raise ValueError(f"Unsupported timestamp type '{type(raw_ts).__name__}' at index {idx}.")

        # Parse numeric value
        try:
            val = float(raw_val)
            if math.isnan(val) or math.isinf(val):
                raise ValueError(f"Value at index {idx} is NaN or Infinite.")
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid numeric value '{raw_val}' at index {idx}: {exc}") from exc

        cleaned.append((dt, val))

    # Sort strictly by timestamp ascending
    cleaned.sort(key=lambda x: x[0])
    return cleaned


def holt_linear_trend_forecast(
    values: List[float],
    horizon: int = DEFAULT_FORECAST_HORIZON,
    alpha: float = DEFAULT_ALPHA,
    beta: float = DEFAULT_BETA,
) -> Tuple[List[float], float, float]:
    """Compute point forecasts and error metrics using Holt's Linear Trend model.

    Formula:
      Level: L_t = alpha * Y_t + (1 - alpha) * (L_{t-1} + T_{t-1})
      Trend: T_t = beta * (L_t - L_{t-1}) + (1 - beta) * T_{t-1}
      Forecast: Y_hat_{t+h} = L_t + h * T_t

    Args:
        values: Chronological list of historical floating-point observations.
        horizon: Number of future periods to forecast.
        alpha: Smoothing factor for level (0 < alpha <= 1).
        beta: Smoothing factor for trend (0 < beta <= 1).

    Returns:
        Tuple of:
          - List of forecasted values of length `horizon`
          - Final smoothed level L_T
          - Final estimated trend T_T
    """
    n = len(values)
    if n < 2:
        raise ValueError(f"Holt's Linear Trend requires at least 2 points, got {n}.")

    # Initialize level and trend
    level = values[0]
    trend = values[1] - values[0]

    for t in range(1, n):
        y_t = values[t]
        last_level = level
        level = alpha * y_t + (1.0 - alpha) * (last_level + trend)
        trend = beta * (level - last_level) + (1.0 - beta) * trend

    forecasts: List[float] = []
    for h in range(1, horizon + 1):
        pred = level + (h * trend)
        # Capacity/demand cannot be negative
        forecasts.append(max(0.0, round(pred, 4)))

    return forecasts, round(level, 4), round(trend, 4)


def evaluate_forecast_holdout(
    values: List[float],
    test_size: int = 2,
    alpha: float = DEFAULT_ALPHA,
    beta: float = DEFAULT_BETA,
) -> Optional[Dict[str, float]]:
    """Compute MAE and RMSE on a hold-out test split of the historical sequence.

    Args:
        values: Historical values.
        test_size: Number of tail observations to hold out.
        alpha: Level smoothing factor.
        beta: Trend smoothing factor.

    Returns:
        Dict with 'mae', 'rmse', 'train_size', 'test_size' if computable, else None.
    """
    if len(values) < (test_size + 3):
        return None  # History too short to build a defensible holdout split

    train_data = values[:-test_size]
    test_data = values[-test_size:]

    try:
        preds, _, _ = holt_linear_trend_forecast(train_data, horizon=test_size, alpha=alpha, beta=beta)
    except Exception:
        return None

    errors = [actual - pred for actual, pred in zip(test_data, preds)]
    mae = sum(abs(e) for e in errors) / len(errors)
    rmse = math.sqrt(sum(e ** 2 for e in errors) / len(errors))

    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "train_points": len(train_data),
        "test_points": len(test_data),
    }


def generate_synthetic_edusaas_timeseries(
    num_hours: int = 48,
    start_time: Optional[datetime.datetime] = None,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Generate a realistic, synthetic EduSaaS API demand timeseries.

    Models diurnal university activity:
      - Low overnight base traffic (2 AM - 6 AM): ~15-30 requests/min
      - Peak lecture & assessment submissions (10 AM - 4 PM): ~180-240 requests/min
      - Evening study review burst (7 PM - 10 PM): ~120-160 requests/min
      - Pseudorandom variance with deterministic Gaussian noise

    Args:
        num_hours: Number of hourly observation points to generate.
        start_time: Starting timestamp. Defaults to 48 hours prior to UTC now.
        random_seed: Seed for deterministic reproducibility.

    Returns:
        Dictionary containing metadata, provenance disclosures, and observation list.
    """
    if start_time is None:
        now = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)
        start_time = now - datetime.timedelta(hours=num_hours)

    import random
    rng = random.Random(random_seed)

    observations: List[Dict[str, Any]] = []
    base_rpm = 25.0

    for i in range(num_hours):
        current_time = start_time + datetime.timedelta(hours=i)
        hour = current_time.hour
        weekday = current_time.weekday()

        # Academic Calendar Feature Engineering:
        # Exam periods: Tuesdays (1) & Thursdays (3) between 09:00 and 16:00
        # Assignment deadlines: Sunday (6) & Wednesday (2) nights 20:00-23:00
        is_exam = (weekday in (1, 3)) and (9 <= hour <= 16)
        is_deadline = (weekday in (2, 6)) and (20 <= hour <= 23)

        exam_multiplier = 1.35 if is_exam else 1.0
        deadline_boost = 60.0 if is_deadline else 0.0

        # Diurnal mathematical pattern
        # Peak around 14:00 (hour 14) and 20:00 (hour 20)
        daily_cycle = math.sin((hour - 6) / 24.0 * 2.0 * math.pi)
        day_factor = max(0.0, daily_cycle) * 160.0

        evening_burst = 50.0 if 19 <= hour <= 22 else 0.0
        noise = rng.gauss(0, 8.0)

        raw_rpm = max(10.0, base_rpm + day_factor + evening_burst + deadline_boost + noise)
        rpm = round(raw_rpm * exam_multiplier, 1)
        simulated_cpu_estimate = round(rpm * 0.0025, 4)  # ~0.25 to 0.6 cores

        # Educational SaaS workload domain telemetry fields
        active_students = int(round(rpm * 3.5 + (150 if is_exam else 0)))
        cpu_used_m = round(simulated_cpu_estimate * 1000.0, 1)
        mem_used_mb = round(48.0 + (active_students * 0.075) + abs(noise * 0.5), 1)
        resp_time_ms = round(4.5 + (rpm * 0.012) + (6.0 if is_exam else 0.0), 2)

        observations.append({
            "timestamp": current_time.isoformat(),
            "requests_per_minute": rpm,
            "simulated_cpu_demand_cores": simulated_cpu_estimate,
            "active_students": active_students,
            "is_exam_period": is_exam,
            "is_assignment_deadline": is_deadline,
            "cpu_used_m": cpu_used_m,
            "memory_used_mb": mem_used_mb,
            "response_time_ms": resp_time_ms,
        })

    return {
        "metadata": {
            "dataset_name": "EduSaaS_Simulated_LMS_Traffic",
            "data_type": "SYNTHETIC_DEMO",
            "generation_method": "diurnal_sine_wave_with_evening_burst_and_gaussian_noise",
            "random_seed": random_seed,
            "observations_count": len(observations),
            "interval": "1 hour",
            "disclaimer": SYNTHETIC_DISCLAIMER,
        },
        "observations": observations,
    }


def load_live_snapshot_history(
    results_dir: str = "results",
    metric_key: str = "total_requested_cpu_cores",
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Scan the results directory for historical KSM snapshot files.

    Args:
        results_dir: Directory containing JSON snapshot files.
        metric_key: State metric to extract ('total_requested_cpu_cores',
                    'total_requested_memory_gb', or 'container_count').

    Returns:
        Tuple of (list of {timestamp, value} records, provenance_info_dict).
    """
    pattern = os.path.join(results_dir, "ksm_*.json")
    snapshot_files = sorted(glob.glob(pattern))

    records: List[Dict[str, Any]] = []
    skipped_files: List[str] = []

    for file_path in snapshot_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            ts = data.get("metadata", {}).get("collection_timestamp_utc")
            state = data.get("observed_k8s_state", {})

            if not ts or not isinstance(state, dict):
                skipped_files.append(os.path.basename(file_path))
                continue

            val = state.get(metric_key)
            if val is not None:
                records.append({
                    "timestamp": ts,
                    "value": float(val),
                    "source_file": os.path.basename(file_path),
                })
        except Exception as exc:
            logger.warning("Failed to parse snapshot file %s: %s", file_path, exc)
            skipped_files.append(os.path.basename(file_path))

    provenance = {
        "snapshots_scanned": len(snapshot_files),
        "valid_records_extracted": len(records),
        "skipped_files": skipped_files,
        "results_dir": os.path.abspath(results_dir),
    }

    return records, provenance


def run_demand_forecast(
    observations: List[Dict[str, Any]],
    time_key: str = "timestamp",
    val_key: str = "value",
    horizon: int = DEFAULT_FORECAST_HORIZON,
    metric_name: str = "resource_demand",
    data_provenance: str = "LIVE_SNAPSHOT_HISTORY",
    min_history: int = MINIMUM_HISTORY_OBSERVATIONS,
) -> Dict[str, Any]:
    """Execute end-to-end forecasting pipeline with strict data integrity validation.

    Args:
        observations: Input list of observation dictionaries.
        time_key: Key for timestamp field.
        val_key: Key for observation numeric value.
        horizon: Number of periods to forecast into the future.
        metric_name: Description of the metric being forecast.
        data_provenance: Tag indicating source ("LIVE_SNAPSHOT_HISTORY" or "SYNTHETIC_DEMO").
        min_history: Minimum required distinct historical observations.

    Returns:
        Comprehensive forecast response dictionary matching FinOps API schema.
    """
    timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if not observations:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": (
                f"No historical records provided for metric '{metric_name}'. "
                f"At least {min_history} distinct observations are required to compute a forecast."
            ),
            "historical_observations_count": 0,
            "minimum_required_observations": min_history,
            "metric_name": metric_name,
            "data_provenance": data_provenance,
            "timestamp_utc": timestamp_utc,
            "disclaimer": FORECAST_DISCLAIMER,
        }

    # Validate and sort
    try:
        cleaned_series = validate_and_sort_timeseries(observations, time_key=time_key, val_key=val_key)
    except ValueError as exc:
        return {
            "status": "ERROR",
            "message": f"Timeseries validation error: {exc}",
            "metric_name": metric_name,
            "data_provenance": data_provenance,
            "timestamp_utc": timestamp_utc,
        }

    count = len(cleaned_series)
    if count < min_history:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": (
                f"Historical timeseries for '{metric_name}' contains {count} observation(s); "
                f"a minimum of {min_history} chronologically distinct points is strictly required."
            ),
            "historical_observations_count": count,
            "minimum_required_observations": min_history,
            "metric_name": metric_name,
            "data_provenance": data_provenance,
            "timestamp_utc": timestamp_utc,
            "disclaimer": FORECAST_DISCLAIMER,
        }

    # Extract values and determine time interval
    values = [val for _, val in cleaned_series]
    timestamps = [dt for dt, _ in cleaned_series]

    # Calculate median time step between observations
    time_deltas = [(timestamps[i] - timestamps[i - 1]).total_seconds() for i in range(1, len(timestamps))]
    median_delta_sec = sorted(time_deltas)[len(time_deltas) // 2] if time_deltas else 3600.0
    step_delta = datetime.timedelta(seconds=max(60.0, median_delta_sec))

    # Run Holt's model
    forecast_values, final_level, final_trend = holt_linear_trend_forecast(values, horizon=horizon)

    # Evaluate on holdout split if enough data
    eval_metrics = evaluate_forecast_holdout(values, test_size=min(3, max(1, count // 4)))

    # Compute prediction bounds using holdout RMSE or heuristic residual scale
    residual_scale = (eval_metrics["rmse"] if eval_metrics and eval_metrics.get("rmse") else (final_level * 0.10))
    residual_scale = max(0.01, residual_scale)

    # Build forecast points
    last_dt = timestamps[-1]
    forecast_points: List[Dict[str, Any]] = []

    for step_idx, pred_val in enumerate(forecast_values, start=1):
        step_dt = last_dt + (step_delta * step_idx)
        # 95% approximate confidence interval: +/- 1.96 * sqrt(step) * residual_scale
        margin = round(1.96 * math.sqrt(step_idx) * residual_scale, 4)
        lower_bound = max(0.0, round(pred_val - margin, 4))
        upper_bound = round(pred_val + margin, 4)

        forecast_points.append({
            "step": step_idx,
            "forecast_timestamp_utc": step_dt.isoformat(),
            "predicted_value": pred_val,
            "lower_bound_95": lower_bound,
            "upper_bound_95": upper_bound,
        })

    is_synthetic = (data_provenance == "SYNTHETIC_DEMO")

    return {
        "status": "SUCCESS",
        "model_name": "HoltLinearTrend_Baseline",
        "metric_name": metric_name,
        "data_provenance": data_provenance,
        "is_synthetic": is_synthetic,
        "timestamp_utc": timestamp_utc,
        "history_summary": {
            "points_count": count,
            "first_observation_utc": timestamps[0].isoformat(),
            "latest_observation_utc": timestamps[-1].isoformat(),
            "latest_observed_value": round(values[-1], 4),
            "smoothed_level": final_level,
            "smoothed_trend_per_step": final_trend,
        },
        "forecast_horizon": horizon,
        "forecast_step_seconds": int(step_delta.total_seconds()),
        "evaluation_metrics": eval_metrics,
        "forecast_points": forecast_points,
        "disclaimer": SYNTHETIC_DISCLAIMER if is_synthetic else FORECAST_DISCLAIMER,
    }
