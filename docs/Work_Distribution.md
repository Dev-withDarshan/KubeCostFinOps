# Work Distribution

> **Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
> **Course:** BCSE355L — Cloud Architecture  
> **Date:** 30 July 2026

---

## Team Members & Roles

| # | Name | Role | Branch |
|---|------|------|--------|
| 1 | **Darshan** | Project Lead & Cloud Architect | `feature/darshan` |
| 2 | **Tharun** | ML Engineer & Data Pipeline Developer | `feature/tharun` |
| 3 | **Dhanushkodi** | Backend Developer & DevOps Engineer | `feature/dhanushkodi` |
| 4 | **Sanjay** | Frontend Developer & Documentation Lead | `feature/sanjay` |

---

## Detailed Responsibility Matrix

### 1. Darshan — Project Lead & Cloud Architect

| # | Task | Deliverables | Phase |
|---|------|-------------|-------|
| 1.1 | AWS EKS cluster provisioning and configuration | EKS cluster with managed node groups, VPC, subnets | Phase-II |
| 1.2 | FinOps recommendation engine development | `src/finops_engine/cost_analyzer.py`, `recommendation_engine.py` | Phase-II |
| 1.3 | Kubecost / OpenCost integration with Prometheus | Helm chart configs, cost allocation setup | Phase-II |
| 1.4 | System architecture design & diagrams | `architecture/` folder — AWS, System, and Workflow diagrams | Phase-I |
| 1.5 | Security policies — IAM least privilege, KMS encryption | `security/iam_least_privilege_policy.json`, `kms_key_policy_notes.md` | Phase-I & II |
| 1.6 | Kubernetes manifests (Deployments, Services, HPA, Ingress) | `src/k8s/` — all YAML manifests | Phase-II |
| 1.7 | Overall project coordination and Git workflow management | Branch strategy, PR reviews, milestone tracking | All Phases |
| 1.8 | Spot-instance placement strategy | Node affinity rules, interruption handlers | Phase-II |

### 2. Tharun — ML Engineer & Data Pipeline Developer

| # | Task | Deliverables | Phase |
|---|------|-------------|-------|
| 2.1 | Data collection — Prometheus metrics export, CloudWatch logs | Raw CSV/JSON files in `dataset/raw/` | Phase-II |
| 2.2 | Data preprocessing and feature engineering | `src/ml_model/preprocessing.py`, cleaned data in `dataset/processed/` | Phase-II |
| 2.3 | ML model development — demand forecasting (Prophet / LSTM) | `src/ml_model/train.py` | Phase-II |
| 2.4 | Model inference endpoint on Amazon SageMaker | `src/ml_model/predict.py`, SageMaker endpoint config | Phase-II |
| 2.5 | Prometheus monitoring configuration | `monitoring/prometheus_config.yaml` | Phase-I & II |
| 2.6 | Model evaluation and accuracy benchmarking | Results in `results/` — RMSE, MAE, MAPE metrics | Phase-II |
| 2.7 | Dataset documentation | `dataset/README.md`, `dataset/dataset_description.pdf` | Phase-I |
| 2.8 | Academic calendar event data curation | Exam schedules, enrollment windows as exogenous features | Phase-II |

### 3. Dhanushkodi — Backend Developer & DevOps Engineer

| # | Task | Deliverables | Phase |
|---|------|-------------|-------|
| 3.1 | Node.js backend API development | `src/backend/` — REST API for dashboard data | Phase-II |
| 3.2 | Database schema design (PostgreSQL on RDS) | Schema migration scripts, ER diagrams | Phase-II |
| 3.3 | DynamoDB table design for real-time metrics | Table schemas, access patterns documentation | Phase-II |
| 3.4 | AWS Lambda functions for event-driven automation | `src/aws/lambda_functions/` | Phase-II |
| 3.5 | IAM policy authoring for Lambda and API Gateway | `src/aws/iam_policies/` | Phase-II |
| 3.6 | CI/CD pipeline setup (GitHub Actions) | `.github/workflows/` — build, test, deploy pipelines | Phase-II |
| 3.7 | Unit and integration test development | `tests/test_finops_engine.py`, additional test files | Phase-II |
| 3.8 | API Gateway and Cognito configuration | Auth flow setup, endpoint routing | Phase-II |

### 4. Sanjay — Frontend Developer & Documentation Lead

| # | Task | Deliverables | Phase |
|---|------|-------------|-------|
| 4.1 | React.js cost dashboard UI development | `src/frontend/` — interactive cost visualization dashboard | Phase-II |
| 4.2 | Grafana dashboard design and configuration | `monitoring/grafana_dashboard.json` | Phase-I & II |
| 4.3 | Literature survey research and documentation | `docs/Literature_Survey.md` | Phase-I |
| 4.4 | Research gap analysis | `docs/Research_Gap.md` | Phase-I |
| 4.5 | Project report compilation | `docs/Project_Report.docx` | Phase-I & II |
| 4.6 | Final presentation preparation | `presentation/` — slides and demo materials | Phase-II |
| 4.7 | Results compilation and visualization | `results/` — charts, tables, cost-saving analysis | Phase-II |
| 4.8 | README and documentation maintenance | `README.md`, `docs/README.md` | All Phases |

---

## Phase-Wise Timeline

| Phase | Timeline | Key Milestones | Status |
|-------|----------|---------------|--------|
| **Phase-I** | July 2026 | Repository scaffold, README, architecture diagrams, literature survey, research gap, work distribution | ✅ Complete |
| **Phase-II** | Aug–Sep 2026 | EKS cluster setup, backend/frontend development, ML model training, FinOps engine integration | 🔲 Upcoming |
| **Phase-III** | Oct 2026 | System integration, end-to-end testing, performance benchmarking, cost-saving validation | 🔲 Upcoming |
| **Phase-IV** | Nov 2026 | Final report, results documentation, presentation, demonstration | 🔲 Upcoming |

---

## Git Workflow

Each team member works on their **dedicated feature branch** and raises Pull Requests to the `develop` branch for review:

```
main (production-ready)
 └── develop (integration branch)
      ├── feature/darshan
      ├── feature/tharun
      ├── feature/dhanushkodi
      └── feature/sanjay
```

- All PRs require at least **one peer review** before merging.
- The `main` branch is updated only at the end of each phase.

---

## Communication & Collaboration

| Tool | Purpose |
|------|---------|
| **GitHub Issues** | Task tracking and bug reporting |
| **GitHub Projects** | Kanban board for sprint planning |
| **Pull Requests** | Code review and feature integration |

---

*Last updated: 30 July 2026*
