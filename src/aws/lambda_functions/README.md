# ⚡ AWS Lambda Functions

This folder will contain **serverless Lambda function code** for event-driven automation tasks.

## Planned Functions

| Function | Trigger | Purpose |
|----------|---------|---------|
| `forecast_trigger` | CloudWatch Scheduled Event | Invokes SageMaker inference endpoint on a schedule |
| `scaling_action` | SNS Notification | Applies approved scaling recommendations to EKS via Kubernetes API |
| `cost_report_generator` | CloudWatch Scheduled Event | Generates daily/weekly cost summary reports and stores in S3 |
| `alert_handler` | Prometheus Alertmanager webhook | Processes cost anomaly alerts and triggers notifications |

## Owner

**Dhanushkodi** — Backend Developer & DevOps Engineer (`feature/dhanushkodi` branch)

> **Note:** Implementation will begin in Phase-II.
