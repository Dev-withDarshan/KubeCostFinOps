# 📊 Dataset

This folder contains all datasets used for training the ML demand forecasting model and evaluating the FinOps recommendation engine.

## Directory Structure

```
dataset/
├── README.md                   ← This file
├── dataset_description.pdf     ← Formal dataset description document
├── raw/                        ← Raw, unprocessed data files
│   └── README.md
└── processed/                  ← Cleaned, feature-engineered data
    └── README.md
```

## Dataset Overview

| Dataset | Format | Source | Approximate Size |
|---------|--------|--------|-----------------|
| Kubernetes Resource Metrics | CSV / JSON | Prometheus (live cluster) | 500K–1M rows/week |
| Historical Cost Data | CSV | Kubecost / OpenCost API exports | ~10K rows/month |
| Application Traffic Logs | CSV / Parquet | ALB access logs, CloudWatch | ~200K rows/week |
| Academic Calendar Events | CSV | Manually curated | ~50 rows |

## Data Schema (Expected)

### Kubernetes Resource Metrics
| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Metric collection time (UTC) |
| `namespace` | string | Kubernetes namespace |
| `deployment` | string | Deployment name |
| `cpu_usage_cores` | float | CPU usage in cores |
| `cpu_request_cores` | float | CPU request in cores |
| `memory_usage_bytes` | int | Memory usage in bytes |
| `memory_request_bytes` | int | Memory request in bytes |
| `pod_count` | int | Number of running pods |

### Academic Calendar Events
| Column | Type | Description |
|--------|------|-------------|
| `event_date` | date | Date of the academic event |
| `event_type` | string | Type: exam, enrollment, result, assignment_deadline |
| `expected_multiplier` | float | Expected traffic multiplier (e.g., 3.5x) |
| `duration_hours` | int | Expected duration of the traffic spike |

## Privacy & Ethics

- All datasets consist of **infrastructure-level metrics** only.
- **No student PII** (Personally Identifiable Information) is collected, stored, or processed.
- Traffic logs are aggregated at the endpoint level; no individual user data is retained.
