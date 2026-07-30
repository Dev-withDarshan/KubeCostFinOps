# Raw Data

This folder contains **raw, unprocessed data files** collected from various sources.

## Expected Contents (Phase-II)

- `k8s_metrics_raw.csv` — Raw Kubernetes resource metrics exported from Prometheus
- `cost_data_raw.csv` — Raw cost data from Kubecost/OpenCost API
- `traffic_logs_raw.csv` — Raw ALB access logs from CloudWatch
- `academic_calendar.csv` — Academic event schedule with expected traffic multipliers

## Data Collection Process

1. **Prometheus metrics** are scraped at 1-minute intervals from the EKS cluster.
2. **Cost data** is exported daily via Kubecost API.
3. **Traffic logs** are aggregated hourly from AWS ALB access logs.
4. **Academic calendar** is manually maintained by the project team.

> **Note:** Raw data files will be added during Phase-II after the EKS cluster is provisioned and data collection begins.
