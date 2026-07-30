# 🏗️ Architecture Diagrams

This folder contains the architecture and framework diagrams for the Kubernetes Cost Optimization Framework.

## Diagrams

| File | Description |
|------|-------------|
| `AWS_Architecture.png` | High-level AWS service topology showing EKS, SageMaker, RDS, S3, API Gateway, Cognito, and network layout |
| `System_Architecture.png` | End-to-end system architecture depicting the four-layer design: Data Ingestion → Intelligence → Orchestration → Presentation |
| `Workflow.png` | Decision workflow from metric collection → demand forecasting → FinOps recommendation → automated action |

## Architecture Overview

The system follows a **four-layer architecture**:

```
┌─────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                  │
│         React.js Dashboard  ·  Grafana Panels        │
├─────────────────────────────────────────────────────┤
│                ORCHESTRATION LAYER                   │
│    AWS EKS  ·  HPA  ·  Cluster Autoscaler  ·  Spot  │
├─────────────────────────────────────────────────────┤
│                 INTELLIGENCE LAYER                   │
│    SageMaker (Forecasting)  ·  FinOps Engine         │
├─────────────────────────────────────────────────────┤
│                DATA INGESTION LAYER                  │
│   Prometheus  ·  Kubecost/OpenCost  ·  CloudWatch    │
└─────────────────────────────────────────────────────┘
```

## Design Decisions

1. **AWS-native services** are preferred where possible (EKS, SageMaker, RDS) to minimize operational overhead.
2. **Prometheus + Kubecost** provide the cost data foundation without vendor lock-in (OpenCost is CNCF-backed).
3. **SageMaker** is chosen over self-hosted ML infrastructure for managed training and inference at scale.
4. **React.js** frontend is separate from Grafana dashboards — Grafana serves ops teams; React serves management/FinOps stakeholders.

> **Note:** Diagram image files are currently placeholders and will be replaced with actual architecture diagrams using draw.io / Lucidchart.
