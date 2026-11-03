# KubeCostFinOps — Presentation Evidence Index

**Project Title:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Course:** BCSE355L – Cloud Architecture (VIT Vellore)  
**Academic Level:** B.Tech Information Technology (3rd Year)  
**Authors:** K. Darshan (24BIT0119), Dhanushkodi Y (24BIT0143), T. Tharun (24BIT0155), S. Sanjay (24BIT0315)  
**Verified Live Cloud Endpoint:** `http://16.16.185.117:8000`  
**Date of Audit & Compilation:** 3 November 2026  

---

## Purpose & Scientific Provenance Statement

This document serves as the **academic evidence index** for the BCSE355L project presentation. In strict accordance with engineering audit standards, **every factual claim, numerical metric, formula, and visual screenshot** displayed in `KubeCostFinOps_Professional_Project_Presentation.pptx` is cataloged below with its exact source file, line number, or command provenance.

---

## Slide-by-Slide Evidence Mapping

### Slide 1: Title Slide & Team Verification
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Project Title | Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence | `README.md`, `docs/Work_Distribution.md` |
| Course Code & Name | BCSE355L – Cloud Architecture | `docs/Work_Distribution.md`, line 4 |
| Student Team Members | K. Darshan (24BIT0119), Dhanushkodi Y (24BIT0143), T. Tharun (24BIT0155), S. Sanjay (24BIT0315) | `docs/FINAL_MASTER_HANDOFF.md`, lines 6–7 |
| Live AWS Public IP | `16.16.185.117:8000` (Region: `eu-north-1` Stockholm) | AWS CLI `describe-instances`, instance `i-0879db7d6fe817a84` |

---

### Slide 2: Project Overview & Executive Summary
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Ingestion Architecture | Non-intrusive scraping via KSM (`8080`), Prometheus (`9090`), OpenCost (`9003`) | `src/backend/main.py`, `scripts/run_port_forwards.sh` |
| Rightsizing Headroom Buffer | Default +20% (`0.20`) above observed peak | `src/finops_engine/recommendation_engine.py`, lines 26, 35 |
| Minimum Replica Floor | Minimum 2 replicas strictly preserved for high availability | `src/finops_engine/recommendation_engine.py`, `results/experiments/exp-20261016-141448/recommendations.json` |
| Workload Cost Optimization | 79.4% cost reduction in controlled benchmark; 68.3% cluster-wide | `results/experiments/exp-20261016-141448/evaluation.json` |

---

### Slide 3: The SaaS Educational Infrastructure Cost Problem
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Static Allocation Defaults | 250m CPU (`0.25` cores) and 256Mi RAM (`0.25` GiB) per replica | `src/k8s/deployment.yaml`, lines 25–35 |
| Measured Idle Capacity | 93.9% of requested CPU idle during deadline peak (15.16m used vs 250m requested) | `results/experiments/exp-20261016-141448/evaluation.json` |
| Scheduler Reservation Bias | Kubernetes schedules based on resource *requests*, not runtime usage | Kubernetes upstream scheduling specification (`Kube-Scheduler`) |

---

### Slide 4: Motivation & Need for FinOps
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| FinOps Framework Mapping | Inform, Normalize, Optimize, Operate | FinOps Foundation Open Standard |
| Workload Safety Classification | Workloads tiered into Actionable, Infrastructure, and Protected Control Plane | `src/backend/main.py`, `build_recommendations_response()` |
| Advisory Governance Policy | `NEVER_AUTO_APPLY — Advisory only. Manual FinOps review and GitOps PR required` | `src/finops_engine/recommendation_engine.py`, `tests/test_backend_api.py` |

---

### Slide 5: Project Objectives & Implementation Scope
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Verified Passing Test Suite | 57/57 Unit & Integration tests passing | `tests/test_backend_api.py`, `tests/test_finops_engine.py` |
| In-Cluster OpenCost Status | HTTP 200, online at `localhost:9003` | `evidence/final-presentation/live-deployment/06_opencost_allocation_records.png` |
| AWS Zero-Spend Guardrail | $5.00 USD monthly budget limit with 80% ($4.00) and 100% ($5.00) email alerts | AWS Budgets API `describe-budget` (Account: `388766927945`) |

---

### Slide 6: Proposed System & End-to-End Workflow
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Multi-Step Dataflow | Pods → KSM/Prometheus → Ingestion Normalizer → Cost Analyzer → Sizing → Web UI | `src/finops_engine/pipeline.py`, `src/backend/main.py` |
| Sub-15ms Response Time | Actual observed API round-trip latency: 10ms – 12ms | `evidence/final-presentation/live-deployment/01_dashboard_executive_overview.png` |

---

### Slide 7: Technology Stack
| Technology | Exact Version / Artifact | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Python Core Backend | Python 3.12 (Standard Library `http.server`) | `src/backend/main.py` |
| Kubernetes Virtualization | Kind v0.24 running Kubernetes v1.31.0 on Docker 26.1 | Host terminal `kind --version`, `kubectl version` |
| Kube-State-Metrics | v2.13.0 (`registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.13.0`) | `src/k8s/monitoring/ksm.yaml` |
| Prometheus TSDB | v2.54.1 (`prom/prometheus:v2.54.1`) | `src/k8s/monitoring/prometheus.yaml` |
| Metrics Server | v0.7.2 (`registry.k8s.io/metrics-server/metrics-server:v0.7.2`) | `src/k8s/monitoring/metrics-server.yaml` |
| OpenCost Engine | v1.121.3 (`ghcr.io/opencost/opencost:latest`) | `src/k8s/monitoring/opencost.yaml` |
| Operating System & Host | Canonical Ubuntu 24.04 LTS (Kernel 7.0.0-1014-aws) on AWS EC2 `t3.small` | AWS EC2 `describe-instances` |

---

### Slide 8: System Architecture
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Layered Architecture Diagram | Vector-rendered 300 DPI diagram | `presentation/presentation_assets/architecture_diagram.png` |
| Namespaces Deployed | `edusaas`, `monitoring`, `kube-system`, `local-path-storage` | `src/k8s/namespace.yaml` |

---

### Slide 9: Monitoring & Telemetry Pipeline
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| KSM Exposition Endpoint | `http://127.0.0.1:8080/metrics` (183,233 bytes payload) | `src/finops_engine/pipeline.py`, `evidence/.../ksm_metrics_sample.txt` |
| Prometheus Active Targets | 6/6 scrape targets UP (kube-state-metrics, prometheus, kubernetes-nodes, apiserver) | `evidence/final-presentation/live-deployment/04_prometheus_targets_all_up.png` |
| Kernel Telemetry | Linux CFS quota (`cpu.cfs_quota_us`) and memory page counters via cAdvisor | Linux kernel cgroups v2 specification |

---

### Slide 10: FinOps Cost Analysis Engine & Modeling Formulas
| Mathematical Parameter | Verified Constant / Value | Primary Source File / Provenance |
| :--- | :--- | :--- |
| CPU Hourly Baseline Rate ($R_{\text{CPU}}$) | `$0.031611` per vCPU-hour (~$23.08 / month) | `src/finops_engine/cost_analyzer.py`, line 22 |
| RAM Hourly Baseline Rate ($R_{\text{RAM}}$) | `$0.004237` per GiB-hour (~$3.09 / month) | `src/finops_engine/cost_analyzer.py`, line 23 |
| Monthly Operational Hours ($T$) | `730.0` hours (365 days × 24 hrs / 12 months) | `src/finops_engine/cost_analyzer.py`, line 25 |
| Monthly Spend Equation | $\text{Monthly} = \left(\text{CPU}_{\text{cores}} \times 0.031611 + \text{RAM}_{\text{GiB}} \times 0.004237\right) \times 730$ | `src/finops_engine/cost_analyzer.py`, lines 180–195 |

---

### Slide 11: Intelligent Recommendation & Rightsizing Engine
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Safety Floor (CPU) | `0.010` CPU cores (10 millicores) | `src/finops_engine/recommendation_engine.py`, line 79 |
| Safety Floor (RAM) | `0.032` GiB (32 MiB) | `src/finops_engine/recommendation_engine.py`, line 80 |
| Over-Provisioning Threshold | $\Delta\text{CPU} > 0.02\text{ cores}$ OR $\Delta\text{RAM} > 0.05\text{ GiB}$ | `src/finops_engine/recommendation_engine.py`, line 87 |
| Protected Control Plane | Static pods in `kube-system` labeled `PROTECTED CONTROL PLANE (NEVER MUTATE)` | `src/backend/main.py`, lines 410–445 |
| Total Cluster Rightsizing Opps | 13 workloads flagged; simulated savings: $30.29/month | Live API `GET /api/v1/recommendations`, snapshot `20261103_062823` |

---

### Slide 12: Resource Capacity Forecasting Module
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Model Algorithm | Holt's Linear Trend / Double Exponential Smoothing | `src/finops_engine/ml_forecast.py`, lines 140–210 |
| Smoothing Parameters | Level smoothing $\alpha = 0.35$ | Trend smoothing $\beta = 0.15$ | `src/finops_engine/ml_forecast.py`, lines 30–31 |
| Minimum Observations Guardrail | Exactly 5 distinct chronological observations required | `src/finops_engine/ml_forecast.py`, line 28 |
| Mean Absolute Error (MAE) | `0.1713` CPU cores (evaluating 8 train, 2 test points) | Live API `GET /api/v1/forecast?source=live` |
| Root Mean Squared Error (RMSE) | `0.1750` CPU cores | Live API `GET /api/v1/forecast?source=live` |

---

### Slide 13: Controlled Experimental Methodology
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Experiment Run Identifier | `exp-20261016-141448` | `results/experiments/exp-20261016-141448/metadata.json` |
| Total Experiment Duration | `73.57` seconds | `results/experiments/exp-20261016-141448/evaluation.json`, line 4 |
| Phase 1: BASELINE | 15.01s duration, 0 target RPS, concurrency 0, 0 requests | `results/experiments/exp-20261016-141448/evaluation.json`, lines 6–23 |
| Phase 2: LOW LOAD | 20.19s duration, 10 target RPS, concurrency 2, 196 requests | `results/experiments/exp-20261016-141448/evaluation.json`, lines 24–41 |
| Phase 3: HIGHER LOAD | 20.16s duration, 25 target RPS, concurrency 4, 487 requests | `results/experiments/exp-20261016-141448/evaluation.json`, lines 42–59 |
| Phase 4: RECOVERY | 15.01s duration, 0 target RPS, concurrency 0, 0 requests | `results/experiments/exp-20261016-141448/evaluation.json`, lines 60–77 |
| Total Requests & Error Rate | 683 completed requests, exactly 0 failed requests (0.0% errors) | `results/experiments/exp-20261016-141448/evaluation.json`, lines 29–32, 47–50 |

---

### Slide 14: Empirical Results & Performance Analysis
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Workload Baseline Modeled Cost | `$13.08` / month (2 replicas × 0.25 CPU, 0.25 GiB) | `results/.../exp-20261016-141448/recommendations.json`, line 44 |
| Workload Proposed Modeled Cost | `$2.69` / month (2 replicas × 0.05 CPU, 0.0625 GiB) | `results/.../exp-20261016-141448/recommendations.json`, line 45 |
| Projected Workload Savings | `$10.39` / month (**79.4% cost reduction**) | `results/.../exp-20261016-141448/recommendations.json`, lines 46–47 |
| Annualized Workload Savings | `$124.68` / year | `results/.../exp-20261016-141448/recommendations.json`, line 48 |
| Cluster Baseline Spend (Live) | `$44.35` / month (13 observed workload specifications) | Live API `GET /api/v1/costs/summary`, snapshot `20261103_062823` |
| Cluster Optimized Spend (Live) | `$14.06` / month | Live API `GET /api/v1/costs/summary`, snapshot `20261103_062823` |
| Cluster-Wide Projected Savings | `$30.29` / month (**68.3% cost reduction**) | Live API `GET /api/v1/costs/summary`, snapshot `20261103_062823` |
| Workload Peak Latency | Mean: 4.82 ms | p95: 5.895 ms | p99: 9.923 ms | `results/.../exp-20261016-141448/evaluation.json`, lines 52–55 |

---

### Slide 15: Dashboard Demonstration
| Screenshot Asset | Provenance & Verified Features | Primary File Path |
| :--- | :--- | :--- |
| Executive Overview | Live cluster health, API Connected (10ms), $44.35/mo baseline, $14.06/mo rightsized | `presentation/presentation_assets/01_dashboard_executive_overview.png` |
| Cost Allocation Breakdown | Namespace breakdown (kube-system 51.4%, edusaas 29.5%, monitoring 19.1%) | `presentation/presentation_assets/02_cost_allocation_and_breakdown.png` |
| Rightsizing Advisory Cards | Workload category badges (Application vs Infrastructure vs Protected Control Plane) | `presentation/presentation_assets/03_rightsizing_recommendations.png` |
| Capacity Forecasting Cockpit | Holt's linear trend projections, confidence bounds, and error evaluations | `presentation/presentation_assets/08_forecasting_dashboard.png` |

---

### Slide 16: AWS Cloud Deployment Architecture
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| AWS Region & Host Type | AWS EC2 `t3.small` (2 vCPU, 2 GiB RAM) in `eu-north-1` (Stockholm) | AWS CLI `describe-instances`, instance `i-0879db7d6fe817a84` |
| Host Operating System | Ubuntu 24.04 LTS (Kernel `7.0.0-1014-aws`) | SSH `uname -a` |
| Systemd Service: API | `kubecost-finops.service` (Active, supervising port 8000) | `scripts/kubecost-finops.service`, host `systemctl status` |
| Systemd Service: Port-Forwards | `kubecost-portforwards.service` (Active, forwarding 8080, 9090, 9003) | `scripts/kubecost-portforwards.service`, host `systemctl status` |
| Systemd Timer: Telemetry | `kubecost-collector.timer` (Active, executing pipeline every 60s) | `scripts/kubecost-collector.timer`, host `systemctl status` |
| AWS Budget Name & Limit | `KubeCostFinOps-ZeroCharge-Guard` ($5.00 limit, notifications to `darshanedu2256@gmail.com`) | `scripts/aws_budget.json`, `scripts/aws_budget_notifications.json` |
| Verified Accrued Spend | `$0.00 USD` (100% absorbed by promotional credits) | AWS Budgets API `describe-budget` |

---

### Slide 17: Security, Reliability, & Technical Limitations
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Port-Forward Bridge Stability | SPDY stream timeouts noted on idle `kubectl port-forward` bridges | Host journalctl `kubecost-collector.service` |
| Host Memory Utilization | 1272 MiB used out of 1905 MiB (633 MiB / 33.2% available headroom, 0 swap) | SSH `free -m` |
| Kubernetes Node Pressure | `MemoryPressure=False`, `DiskPressure=False`, `PIDPressure=False` | SSH `kubectl describe nodes` |
| Security Group Review | Ports 8000, 9090, 9003, 22 authorized to `0.0.0.0/0`; SSH tunneling recommended for prod | AWS CLI `describe-security-groups`, `sg-09406a8739b62cf5f` |

---

### Slide 18: Future Scope & Production Roadmap
| Roadmap Pillar | Target Cloud Architecture Technology | Technical Reference |
| :--- | :--- | :--- |
| Managed Kubernetes | Amazon EKS with multi-AZ managed node groups | AWS EKS Architecture Best Practices |
| Dynamic Node Auto-Scaling | Karpenter controller with Graviton (ARM64) spot-instance node pools | Karpenter Open Source Node Autoscaler |
| Billing Reconciliation | AWS Cost Explorer API and AWS Cost & Usage Reports (CUR) queried via Athena | AWS Billing and Cost Management Documentation |
| Closed-Loop Governance | ArgoCD / Flux GitOps controllers generating automated rightsizing Pull Requests | CNCF GitOps Standard |

---

### Slide 19: Conclusion & Academic Defense
| Technical Claim / Artifact | Verified Value / Identity | Primary Source File / Provenance |
| :--- | :--- | :--- |
| Primary Scientific Deliverable | End-to-end FinOps intelligence engine bridging object-state telemetry and cloud economics | Repository root, `src/finops_engine/` |
| Operational Cloud Verification | Working live deployment on public AWS EC2 host with zero-spend protection | Verified live endpoint: `http://16.16.185.117:8000` |

