# Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence

<p align="center">
  <img src="https://img.shields.io/badge/Cloud-AWS-FF9900?style=for-the-badge&logo=amazonaws" alt="AWS" />
  <img src="https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?style=for-the-badge&logo=kubernetes" alt="Kubernetes" />
  <img src="https://img.shields.io/badge/ML-SageMaker-232F3E?style=for-the-badge&logo=amazonsagemaker" alt="SageMaker" />
  <img src="https://img.shields.io/badge/Monitoring-Prometheus-E6522C?style=for-the-badge&logo=prometheus" alt="Prometheus" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

> **Course:** BCSE355L — Cloud Architecture  
> **Phase:** Phase-I (Repository Scaffold & Project Planning)  
> **Due Date:** 30 July 2026

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Proposed Architecture / Framework](#proposed-architecture--framework)
- [Technology Stack](#technology-stack)
- [AWS Services](#aws-services)
- [Dataset Details](#dataset-details)
- [Repository Structure](#repository-structure)
- [Team Members](#team-members)
- [Work Distribution](#work-distribution)
- [Literature Survey & Research Gap](#literature-survey--research-gap)
- [Installation](#installation)
- [Deployment](#deployment)
- [Results](#results)
- [Future Scope](#future-scope)
- [License](#license)

---

## Problem Statement

SaaS-based educational platforms (LMS, online examination portals, virtual labs) experience **highly variable workloads** — idle capacity during off-hours and sudden traffic surges during exam weeks, result announcements, and enrollment windows. When deployed on Kubernetes (e.g., AWS EKS), these platforms frequently suffer from:

1. **Over-provisioned clusters** — static resource requests and limits lead to 40–60 % compute waste during non-peak periods.
2. **Reactive scaling** — default Horizontal Pod Autoscalers respond *after* latency spikes have already degraded user experience.
3. **Lack of cost visibility** — engineering teams have no namespace-level or workload-level cost attribution, making it impossible to identify the most expensive services.
4. **Under-utilization of spot instances** — fear of interruptions prevents adoption of spot/preemptible nodes even for fault-tolerant batch workloads (grading pipelines, report generation).

There is currently **no open-source, end-to-end framework** that combines real-time Kubernetes cost observability (Kubecost/OpenCost + Prometheus), **ML-driven demand forecasting** (to predict exam-period traffic spikes days in advance), and **automated FinOps recommendations** (rightsizing, HPA tuning, spot-instance placement) in a single, cohesive system tailored for educational SaaS workloads.

This project addresses that gap by building a **Kubernetes Cost Optimization Framework** powered by FinOps Intelligence, specifically designed for the unique traffic patterns of educational platforms.

---

## Objectives

1. **Design and deploy** a Kubernetes-based infrastructure on **AWS EKS** tailored for educational SaaS workloads with proper namespace isolation.
2. **Implement real-time cost monitoring** using **Prometheus** and **Kubecost / OpenCost** with per-namespace and per-workload cost breakdowns.
3. **Build an ML-driven demand forecasting model** using **Amazon SageMaker** to predict traffic spikes during exam periods, enrollment windows, and result days.
4. **Develop a FinOps recommendation engine** that generates actionable suggestions for Kubernetes rightsizing, HPA tuning, and spot-instance placement.
5. **Automate cost-saving actions** through a feedback loop that applies approved recommendations to Kubernetes manifests and scaling policies.
6. **Achieve measurable cost savings** (target: 25–40 % reduction in monthly cloud spend) while maintaining SLA-compliant performance (p99 latency < 500 ms).
7. **Visualize insights** via Grafana dashboards that display cost trends, forecasting accuracy, and optimization impact in real time.

---

## Proposed Architecture / Framework

The system follows a **four-layer architecture**:

| Layer | Components | Purpose |
|-------|-----------|---------|
| **Data Ingestion** | Prometheus, Kubecost/OpenCost, CloudWatch | Collect resource usage, cost metrics, and application telemetry |
| **Intelligence** | Amazon SageMaker, FinOps Engine | ML-driven demand forecasting and cost optimization recommendations |
| **Orchestration** | AWS EKS, HPA, Cluster Autoscaler | Kubernetes workload scheduling, scaling, and spot-instance management |
| **Presentation** | Grafana, React.js Dashboard | Real-time cost dashboards, alerts, and recommendation approvals |

### Architecture Diagrams

| Diagram | Description |
|---------|-------------|
| ![AWS Architecture](architecture/AWS_Architecture.png) | High-level AWS service topology showing EKS, SageMaker, RDS, S3, and network layout |
| ![System Architecture](architecture/System_Architecture.png) | End-to-end system architecture depicting data flow across all four layers |
| ![Workflow](architecture/Workflow.png) | Decision workflow from metric collection → forecasting → recommendation → action |

> **Note:** Architecture diagrams are located in the [`architecture/`](architecture/) folder. See [`architecture/README.md`](architecture/README.md) for detailed descriptions.

---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Cloud Provider** | Amazon Web Services (AWS) |
| **Container Orchestration** | Kubernetes (AWS EKS) |
| **Monitoring & Observability** | Prometheus, Grafana, Kubecost / OpenCost |
| **Machine Learning** | Amazon SageMaker, Python (scikit-learn, pandas, numpy, Prophet) |
| **Backend API** | Python (Flask/FastAPI — FinOps Engine), Node.js (Application Backend) |
| **Frontend** | React.js (Cost Dashboard & Recommendation UI) |
| **Databases** | PostgreSQL (Amazon RDS), Amazon DynamoDB |
| **Storage** | Amazon S3 (datasets, model artifacts, logs) |
| **Auth & API Gateway** | Amazon Cognito, Amazon API Gateway |
| **Serverless** | AWS Lambda (event-driven automation) |
| **Infrastructure as Code** | Kubernetes YAML manifests, Helm Charts |
| **CI/CD** | GitHub Actions |
| **Security** | AWS IAM (least-privilege), KMS (encryption at rest) |

---

## AWS Services

| Service | Role in This Project |
|---------|---------------------|
| **Amazon EKS** | Managed Kubernetes control plane and worker nodes hosting educational SaaS services |
| **Amazon SageMaker** | ML model training, hosting, and real-time inference for demand forecasting |
| **Amazon RDS (PostgreSQL)** | Relational storage for application data, cost records, and recommendation history |
| **Amazon DynamoDB** | NoSQL store for high-throughput metrics ingestion and real-time state |
| **Amazon S3** | Object storage for raw/processed datasets, model artifacts, and cost reports |
| **AWS Lambda** | Serverless functions for event-driven automation (e.g., triggering scaling on forecast alerts) |
| **Amazon API Gateway** | RESTful API management for frontend-to-backend communication |
| **Amazon Cognito** | User authentication and role-based access control |
| **AWS IAM & KMS** | Least-privilege access policies and encryption key management |
| **Amazon CloudWatch** | Supplementary logging and alarms for infrastructure-level events |

---

## Dataset Details

This project uses **Kubernetes cluster resource metrics** and **application-level traffic data**. The datasets are organized under the [`dataset/`](dataset/) directory.

| Dataset | Source | Format | Description |
|---------|--------|--------|-------------|
| **Kubernetes Resource Metrics** | Prometheus (live cluster) / [Kaggle K8s datasets](https://www.kaggle.com/) | CSV / JSON | CPU utilization, memory usage, pod counts, and network I/O per namespace and workload, sampled at 1-minute intervals |
| **Historical Cost Data** | Kubecost / OpenCost API exports | CSV | Per-namespace and per-deployment cost breakdowns including compute, storage, and network costs |
| **Application Traffic Logs** | ALB access logs, CloudWatch | CSV / Parquet | HTTP request counts, response times, error rates, and user session data for the educational platform |
| **Academic Calendar Events** | Manually curated | CSV | Exam schedules, enrollment windows, result dates — used as exogenous features for the forecasting model |

> **Data Volume:** Estimated 500K–1M metric data points per week from a 3-node EKS cluster running representative workloads.  
> **Privacy:** All datasets are infrastructure-level metrics; no student PII is collected or processed.  
> See [`dataset/README.md`](dataset/README.md) for data schema details and preprocessing instructions.

---

## Repository Structure

```
KubeCostFinOps_Cloud_Project_2026/
├── README.md                          ← Project overview (this file)
├── LICENSE                            ← MIT License
├── .gitignore                         ← Git ignore rules
│
├── docs/                              ← Project documentation
│   ├── README.md                      ← Documentation index
│   ├── Work_Distribution.md           ← Team work allocation & responsibilities
│   ├── Literature_Survey.md           ← Literature survey document
│   ├── Research_Gap.md                ← Research gap analysis
│   ├── Project_Report.docx            ← Phase-I project report
│   ├── Objectives.docx                ← Detailed project objectives
│   └── Novelty.docx                   ← Novelty of proposed approach
│
├── architecture/                      ← Architecture & framework diagrams
│   ├── README.md                      ← Diagram descriptions & design rationale
│   ├── AWS_Architecture.png           ← AWS service topology diagram
│   ├── System_Architecture.png        ← End-to-end system architecture
│   └── Workflow.png                   ← Data & decision workflow diagram
│
├── dataset/                           ← Datasets for ML model training
│   ├── README.md                      ← Dataset schema & preprocessing guide
│   ├── raw/                           ← Raw, unprocessed data files
│   │   └── README.md
│   ├── processed/                     ← Cleaned & feature-engineered data
│   │   └── README.md
│   └── dataset_description.pdf        ← Dataset description document
│
├── src/                               ← Source code (all implementation)
│   ├── frontend/                      ← React.js cost dashboard UI
│   │   └── README.md
│   ├── backend/                       ← Node.js application backend
│   │   └── README.md
│   ├── finops_engine/                 ← Python FinOps recommendation engine
│   │   ├── cost_analyzer.py
│   │   ├── recommendation_engine.py
│   │   └── kubecost_config.yaml
│   ├── ml_model/                      ← SageMaker ML model code
│   │   ├── preprocessing.py
│   │   ├── train.py
│   │   └── predict.py
│   ├── aws/                           ← AWS-specific configurations
│   │   ├── lambda_functions/          ← Lambda function code
│   │   │   └── README.md
│   │   └── iam_policies/             ← IAM policy documents
│   │       └── README.md
│   └── k8s/                           ← Kubernetes manifests
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── hpa.yaml
│       └── ingress.yaml
│
├── monitoring/                        ← Observability configurations
│   ├── prometheus_config.yaml
│   └── grafana_dashboard.json
│
├── security/                          ← Security policies & configs
│   ├── iam_least_privilege_policy.json
│   └── kms_key_policy_notes.md
│
├── tests/                             ← Unit & integration tests
│   └── test_finops_engine.py
│
├── results/                           ← Experiment results & benchmarks
│   └── README.md
│
└── presentation/                      ← Project presentation materials
    └── README.md
```

---

## Team Members

| # | Name | Registration No. | Role | GitHub |
|---|------|------------------|------|--------|
| 1 | **Darshan** | — | Project Lead & Cloud Architect | [@Dev-withDarshan](https://github.com/Dev-withDarshan) |
| 2 | **Tharun** | — | ML Engineer & Data Pipeline Developer | — |
| 3 | **Dhanushkodi** | — | Backend Developer & DevOps Engineer | — |
| 4 | **Sanjay** | — | Frontend Developer & Documentation Lead | — |

> **Note:** Registration numbers and GitHub profile links will be updated by each team member on their respective feature branches.

---

## Work Distribution

A detailed work distribution document is available at **[`docs/Work_Distribution.md`](docs/Work_Distribution.md)**.

### Summary

| Team Member | Primary Responsibilities | Deliverables |
|------------|------------------------|-------------|
| **Darshan** | AWS EKS cluster setup, FinOps engine development, Kubecost/OpenCost integration, overall architecture design | `src/finops_engine/`, `src/k8s/`, `architecture/`, `security/` |
| **Tharun** | ML demand forecasting model (SageMaker), data preprocessing, model training & evaluation | `src/ml_model/`, `dataset/`, `monitoring/` |
| **Dhanushkodi** | Backend API development (Node.js), Lambda functions, database schema design, CI/CD pipeline | `src/backend/`, `src/aws/`, `tests/` |
| **Sanjay** | React.js cost dashboard UI, Grafana dashboard configuration, literature survey, documentation & presentation | `src/frontend/`, `docs/`, `presentation/`, `results/` |

---

## Literature Survey & Research Gap

Detailed documents are available in the [`docs/`](docs/) folder:

- 📄 **[Literature Survey](docs/Literature_Survey.md)** — Comprehensive review of existing Kubernetes cost optimization tools, FinOps frameworks, and ML-based autoscaling research.
- 📄 **[Research Gap](docs/Research_Gap.md)** — Identified gaps in current approaches and how this project addresses them.
- 📄 **[Novelty](docs/Novelty.docx)** — Unique contributions of the proposed framework.

---

## Installation

> **Placeholder — Phase-II.** Installation instructions (Python dependencies, Node packages, AWS CLI configuration, kubectl setup) will be added once development begins.

---

## Deployment

> **Placeholder — Phase-II.** Deployment steps (EKS cluster provisioning, Helm chart installation for Prometheus/Kubecost, SageMaker endpoint creation, application deployment) will be documented here.

---

## Results

> **Placeholder — Phase-II.** Experimental results, cost-saving metrics, forecasting accuracy, and performance benchmarks will be presented in the [`results/`](results/) folder after implementation and testing.

---

## Future Scope

- **Multi-cloud support** — Extend the framework to GKE (Google Cloud) and AKS (Azure) for vendor-agnostic cost optimization.
- **Reinforcement Learning** — Replace rule-based recommendations with an RL agent that learns optimal scaling policies over time.
- **Real-time anomaly detection** — Integrate anomaly detection on cost and resource usage streams for proactive alerting.
- **Granular chargeback** — Implement namespace- and team-level cost allocation for multi-tenant educational platforms.
- **Custom Kubernetes Operator** — Build a CRD-based operator that applies FinOps recommendations as native Kubernetes resources.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
