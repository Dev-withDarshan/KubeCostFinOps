# Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Kubernetes-v1.37-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes" />
  <img src="https://img.shields.io/badge/Orchestrator-Kind-blue?style=for-the-badge" alt="Kind" />
  <img src="https://img.shields.io/badge/FinOps-Foundation-00D2B4?style=for-the-badge" alt="FinOps" />
  <img src="https://img.shields.io/badge/Tests-54%20Passing-success?style=for-the-badge" alt="54 Passing Tests" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

> **Course:** BCSE355L — Cloud Architecture
> **Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence
> **Branch:** `develop`
> **Status:** Release Engineering Complete & Verified (54/54 Passing Tests, Zero External Dependencies)

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [System Architecture](#system-architecture)
- [Implementation Status: Implemented vs. Simulated](#implementation-status-implemented-vs-simulated)
- [Repository Structure](#repository-structure)
- [Prerequisites & Environment](#prerequisites--environment)
- [Quickstart: Launching the System](#quickstart-launching-the-system)
- [Automated Test Suite (54 Tests Verified)](#automated-test-suite-54-tests-verified)
- [Backend REST API & Interactive Dashboard](#backend-rest-api--interactive-dashboard)
- [Controlled Benchmark Experiment Results](#controlled-benchmark-experiment-results)
- [Reproducing the Experiment](#reproducing-the-experiment)
- [Release Readiness & Forensic Validation Scripts](#release-readiness--forensic-validation-scripts)
- [Academic & Technical Honesty](#academic--technical-honesty)
- [Limitations & Future Work](#limitations--future-work)
- [Documentation Links](#documentation-links)
- [Team & Acknowledgments](#team--acknowledgments)
- [License](#license)

---

## Problem Statement

SaaS-based educational platforms (Learning Management Systems, online examination portals, student enrollment portals) experience **highly volatile, bursty workloads** characterized by prolonged idle capacity during nights and off-semesters, punctuated by massive traffic surges during exam windows, assignment submission deadlines, and result announcements.

When hosted on Kubernetes, these platforms suffer from four critical operational challenges:
1. **Severe Static Over-Provisioning:** Engineering teams provision pod resource requests and limits to withstand worst-case historical peaks. During normal hours, 60–80% of allocated vCPU and memory capacity remains unutilized, incurring unnecessary cloud spending.
2. **Reactive, Lagging Autoscaling:** Default Horizontal Pod Autoscalers (HPAs) rely on trailing metric windows (typically 15–60 seconds), scaling out only *after* end users experience latency degradation or HTTP timeouts.
3. **Absence of Workload Cost Attribution:** Standard cloud provider bills aggregate cluster costs at the EC2 instance or node level without namespace- or deployment-level attribution.
4. **Lack of Integrated FinOps Feedback Loops:** Most organizations lack automated pipelines that translate raw cgroup utilization telemetry into conservative, safety-checked rightsizing recommendations without risking high-availability SLAs.

This project delivers an end-to-end **Kubernetes FinOps Intelligence Framework** that continuously ingests telemetry, calculates AWS-modeled workload costs, produces conservative rightsizing recommendations with high-availability safety floors, forecasts traffic surges, and provides an interactive web dashboard for real-time visibility.

---

## Objectives

1. **Telemetry Ingestion:** Ingest raw Kubernetes resource requests, limits, and real-time cgroup utilization from Kube-State-Metrics (KSM) and the Kubernetes Metrics API (`metrics.k8s.io`).
2. **Deterministic FinOps Cost Modeling:** Model per-pod and per-workload hourly and monthly costs using standard AWS US-East-1 on-demand reference rates ($0.031611/vCPU-hr, $0.004237/GB-hr).
3. **Safe, Conservative Rightsizing:** Formulate rightsizing recommendations using peak-utilization heuristics, a +20% safety headroom factor, and strict production safety floors (50m CPU, 64Mi RAM), retaining multi-pod replica counts for High Availability.
4. **Statistical Demand Forecasting:** Provide predictive demand forecasting to anticipate educational calendar spikes before traffic arrives.
5. **Zero-Dependency Lightweight Architecture:** Implement the complete backend, ingestion pipeline, forecasting module, and test suite entirely in Python standard libraries with zero pip or npm installation requirements.
6. **Empirical Validation:** Execute a reproducible 4-phase benchmark experiment measuring HTTP latency, throughput, and actual cgroup telemetry under simulated exam load.

---

## System Architecture

The framework is organized into a four-layer architecture separating telemetry collection, algorithmic intelligence, container orchestration, and stakeholder visualization:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                            │
│  Interactive FinOps Dashboard (HTML5 / Vanilla CSS / ES6 JavaScript)     │
│  - Real-time Cost Breakdown  ·  Recommendations  ·  4-Phase Benchmark   │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │ JSON REST API (HTTP 8000)
┌────────────────────────────────────┴────────────────────────────────────┐
│                           INTELLIGENCE LAYER                            │
│  FinOps Engine & Statistical Predictor (Python Standard Library)        │
│  - Cost Analyzer (AWS m5.large Model: $0.031611/vCPU-hr, $0.004237/GB-h)│
│  - Rightsizing Engine (+20% Headroom, Safety Floors, HA Preservation)   │
│  - Statistical Demand Forecaster (EWMA / Moving Averages)               │
│  - Controlled Benchmark Experiment Runner (4-Phase Load & Cgroups)      │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │ Normalized Telemetry
┌────────────────────────────────────┴────────────────────────────────────┐
│                          DATA INGESTION LAYER                           │
│  Pipeline Collector (Python)                                            │
│  - Kube-State-Metrics (KSM) Prometheus Text Parser (Port 8080)          │
│  - Kubernetes Metrics API (Kubelet / Metrics Server cgroups)            │
│  - Unit Normalizer (Nanocores/Millicores → Cores, Bytes/MiB → GiB)     │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │ Telemetry Scraping
┌────────────────────────────────────┴────────────────────────────────────┐
│                          ORCHESTRATION LAYER                            │
│  Kubernetes Cluster (Local Kind Prototype: v1.37.0 on Docker Desktop)   │
│  - Workload: edusaas-backend (2 Replicas, ClusterIP Service)            │
│  - Monitoring: Kube-State-Metrics v2.12.0 & Metrics Server v0.7.1       │
│  - Autoscaling: HorizontalPodAutoscaler (CPU 70% Target)                │
└─────────────────────────────────────────────────────────────────────────┘
```

For complete architectural data-flow sequences, Mermaid diagrams, and component mappings, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Implementation Status: Implemented vs. Simulated

To uphold technical and academic honesty, all capabilities are classified into their exact operational state:

| Component | Status | Classification | Reality Details |
| :--- | :--- | :--- | :--- |
| **FinOps Cost Analyzer** | **Working** | Implemented | Computes hourly/monthly spend using AWS m5.large on-demand reference rates. Fully unit tested. |
| **Rightsizing Engine** | **Working** | Implemented | Applies peak + 20% margin with 50m/64Mi safety floors. Preserves replica count. |
| **KSM Data Ingestion** | **Working** | Implemented | Fetches & parses live Prometheus text format from KSM endpoint (HTTP 200). Generates JSON/CSV. |
| **REST API Server** | **Working** | Implemented | Python standard-library HTTP server with 6 JSON endpoints, CORS, query filters, and 404 handling. |
| **Interactive Dashboard**| **Working** | Implemented | Vanilla HTML5/CSS/JS interface displaying live API data, 3-card summary, and benchmark tables. |
| **Controlled Experiment**| **Working** | Implemented | Automated 4-phase benchmark script measuring HTTP latency & cgroup telemetry under load. |
| **Automated Tests** | **Working** | Implemented | **54 unit tests passing in 2.5s** across engine, pipeline, API, and experiment runner. |
| **Statistical Forecast** | **Working** | Implemented | Exponentially weighted moving average with simulated educational calendar spikes. |
| **Cluster Platform** | **Working** | Local Prototype | Kind v0.27.0 (v1.37.0) on Docker Desktop. AWS EKS is the future deployment target. |
| **Benchmark Workload** | **Working** | Proxy Service | `hashicorp/http-echo:latest` proxy microservice. Production LMS is future target. |
| **Cost Savings Action** | **Dry-Run** | Advisory Only | Recommendations are computed as advisory deltas; cluster manifests are NOT mutated in-flight. |
| **Cloud Billing Data** | **Simulated** | Modeled Reference | Uses published AWS reference rates. No live AWS account is billed. |
| **SageMaker / ML Train** | *Staged* | Phase-II Architecture | Architecture diagrams and scaffolding defined for future AWS SageMaker integration. |

---

## Repository Structure

```
KubeCostFinOps_Cloud_Project_2026/
├── README.md                          ← Project overview & verified results (this file)
├── LICENSE                            ← MIT License
│
├── docs/                              ← Comprehensive technical & academic documentation
│   ├── README.md                      ← Documentation index & deliverables checklist
│   ├── SETUP_AND_REPRODUCTION.md      ← Step-by-step setup, test, and reproduction guide
│   ├── EXPERIMENT_RESULTS.md          ← Detailed benchmark evaluation & honesty declaration
│   ├── ARCHITECTURE.md                ← Data flow, Kind vs. AWS matrix, component status
│   ├── FINAL_VERIFICATION.md          ← Regression test logs, API verification, cluster audit
│   ├── FINAL_CODE_AUDIT.md            ← Forensic code audit, finding matrix, & mitigations
│   ├── SECURITY_AND_RELIABILITY.md    ← Security review, path traversal fixes, & DOM XSS audit
│   ├── DEMO_RUNBOOK.md                ← 5-to-7 minute live presentation runbook & cheat sheet
│   ├── REVIEW_QA_PREPARATION.md       ← 20 challenging viva questions & authoritative answers
│   ├── PROJECT_HANDOVER.md            ← Executive handoff summary & shutdown instructions
│   ├── RELEASE_READINESS.md           ← Release certification across 10 quality gates
│   ├── Work_Distribution.md           ← Team member responsibilities
│   ├── Literature_Survey.md           ← Academic literature review
│   └── Research_Gap.md                ← Analysis of gaps in current FinOps tooling
│
├── scripts/                           ← Release verification & forensic scripts (Zero external deps)
│   ├── final_check.py                 ← Release readiness integrity & verification checker
│   └── validate_experiment.py         ← Forensic mathematical experiment validator
│
├── src/                               ← Core source code implementation
│   ├── backend/                       ← Lightweight Python REST API server
│   │   ├── main.py                    ← Multi-endpoint HTTP server with CORS & 404 handling
│   │   └── README.md
│   ├── finops_engine/                 ← FinOps Intelligence core
│   │   ├── cost_analyzer.py           ← AWS reference cost calculation module
│   │   ├── recommendation_engine.py   ← Conservative rightsizing & safety floors
│   │   ├── pipeline.py                ← Kube-State-Metrics Prometheus text parser
│   │   ├── ml_forecast.py             ← Statistical demand & resource forecaster
│   │   ├── experiment_runner.py       ← 4-phase controlled benchmark runner
│   │   └── kubecost_config.yaml       ← FinOps pricing & threshold configuration
│   ├── frontend/                      ← Vanilla web dashboard (Zero-dependency)
│   │   ├── index.html                 ← Semantic HTML5 layout with benchmark cards
│   │   ├── styles.css                 ← Responsive dark-mode styling with FinOps theme
│   │   ├── app.js                     ← Async API client with reactive DOM updates
│   │   └── README.md
│   └── k8s/                           ← Kubernetes manifests & monitoring configs
│       ├── namespace.yaml             ← edusaas namespace
│       ├── deployment.yaml            ← 2-replica educational proxy workload
│       ├── service.yaml               ← ClusterIP service (port 5678)
│       ├── hpa.yaml                   ← Horizontal Pod Autoscaler (70% CPU target)
│       ├── ingress.yaml               ← Ingress route specification
│       └── monitoring/                ← Kube-State-Metrics & Metrics Server manifests
│
├── tests/                             ← Automated regression test suite (54 tests)
│   ├── test_finops_engine.py          ← FinOps math & rightsizing tests (9 tests)
│   ├── test_pipeline.py               ← KSM ingestion & normalization tests (13 tests)
│   ├── test_backend_api.py            ← REST API & endpoint contract tests (25 tests)
│   └── test_experiment_runner.py      ← Benchmark metrics & aggregation tests (7 tests)
│
├── results/                           ← Benchmark snapshots & experiment artifacts
│   ├── README.md
│   └── experiments/                   ← Isolated experiment run records
│       └── exp-20261016-141448/       ← Latest verified 4-phase benchmark run
│           ├── metadata.json          ← Environment, node, image metadata
│           ├── observations.json      ← Time-series telemetry (74 observations)
│           ├── observations.csv       ← Tabular pod metrics for analysis
│           ├── recommendations.json   ← Rightsizing recommendation output
│           ├── evaluation.json        ← Comparative cost & savings analysis
│           └── README.md              ← Benchmark run summary
│
└── architecture/                      ← Architectural diagrams and schemas
    ├── README.md
    ├── AWS_Architecture.png
    ├── System_Architecture.png
    └── Workflow.png
```

---

## Prerequisites & Environment

| Dependency | Minimum Version | Verified Runtime | Purpose |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11 64-bit | Windows 11 Enterprise | Host OS |
| **Python** | 3.10+ | 3.14.0 | Backend API, FinOps Engine, Benchmark Runner |
| **Docker Desktop** | 24.0+ | Docker Desktop v28+ | Local container runtime for Kind |
| **Kind** | v0.20+ | v0.27.0 | Kubernetes-in-Docker cluster runner |
| **kubectl** | v1.28+ | v1.31.4 | Kubernetes management client |

> [!NOTE]
> No third-party pip packages (`requirements.txt`) or npm modules (`node_modules`) are needed. The system runs out-of-the-box using the Python standard library.

---

## Quickstart: Launching the System

### Step 1: Verify Kubernetes Cluster
Open Windows PowerShell:
```powershell
# Verify local Kind cluster is operational
kubectl get nodes
kubectl get pods -n edusaas
kubectl get pods -n monitoring
```

### Step 2: Start the Backend API & Web Dashboard
```powershell
# From the repository root:
python src/backend/main.py --host 127.0.0.1 --port 8000
```

### Step 3: Access the Dashboard & API
- Open your browser to: **`http://127.0.0.1:8000/`**
- Test the REST API:
  - Health check: `http://127.0.0.1:8000/api/v1/health`
  - Monthly costs: `http://127.0.0.1:8000/api/v1/cost/monthly`
  - Rightsizing recommendations: `http://127.0.0.1:8000/api/v1/recommendations`
  - Latest experiment benchmark: `http://127.0.0.1:8000/api/v1/experiments/latest`

---

## Automated Test Suite (54 Tests Verified)

The entire system is guarded by a comprehensive regression suite discoverable via standard Python unittest:

```powershell
python -m unittest discover -s tests -v
```

### Verified Test Run Output:
```
Ran 54 tests in 2.522s

OK
```

- `tests/test_finops_engine.py` (9 tests): Cost formula accuracy, zero-resource handling, safety floor enforcement, +20% headroom.
- `tests/test_pipeline.py` (13 tests): Prometheus text parsing, nanocore/byte unit conversion, snapshot generation, graceful error recovery.
- `tests/test_backend_api.py` (25 tests): REST route dispatch, query string filters, CORS preflights, static file serving, 404 error handling, `/api/v1/experiments/<run_id>` resolution, directory traversal protection (`..` rejection, regex whitelist), and route aliases (`/api/v1/health`, `/api/v1/cost/monthly`, `/api/v1/forecast/demand`).
- `tests/test_experiment_runner.py` (7 tests): Metric aggregation, quantile calculations, phase transitions, dry-run evaluation.

---

## Backend REST API & Interactive Dashboard

The backend API server (`src/backend/main.py`) provides clean, decoupled JSON endpoints that power the frontend dashboard:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/health` | `GET` | System uptime, target cluster status, and component health |
| `/api/v1/cost/monthly` | `GET` | Workload cost attribution based on AWS reference rates (supports `?namespace=` and `?workload=`) |
| `/api/v1/recommendations` | `GET` | Conservative rightsizing suggestions with safety floors and HA preservation |
| `/api/v1/forecast/demand` | `GET` | 14-day statistical traffic and resource forecast (supports `?days=`) |
| `/api/v1/experiments/latest` | `GET` | Most recent controlled benchmark experiment results |
| `/api/v1/experiments/<run_id>` | `GET` | Historical experiment results lookup by run ID (with 404 error handling) |

---

## Controlled Benchmark Experiment Results

**Latest Experiment Run:** [`exp-20261016-141448`](file:///C:/Users/gnavy/Downloads/KubeCostFinOps_Cloud_Project_2026/results/experiments/exp-20261016-141448)
**Execution Timestamp:** 2026-10-16T14:14:48Z
**Duration:** 69.4 seconds | **Total Observations:** 74 (36 samples across 2 pods)
**HTTP Requests:** 683 requests | **Failures:** 0 (100.0% success rate) | **p50 Latency:** 4.61 ms

### 1. Four-Phase Benchmark Performance

| Phase | Phase Name | Duration | Requests | Mean RPS | Error Rate | Latency p50 | Latency p95 | Peak Pod CPU | Peak Pod RAM |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase A** | Baseline Idle | 10.0 s | 0 | 0.0 RPS | 0.0% | — | — | 1.83 m | 5.86 Mi |
| **Phase B** | Warmup Load | 15.0 s | 145 | 9.7 RPS | 0.0% | 4.88 ms | 13.68 ms | 4.54 m | 6.07 Mi |
| **Phase C** | Peak Exam Burst | 25.0 s | 506 | 24.2 RPS | 0.0% | 4.55 ms | 10.74 ms | 15.16 m | 6.45 Mi |
| **Phase D** | Post-Load Cooldown | 15.0 s | 0 | 0.0 RPS | 0.0% | — | — | 2.05 m | 6.41 Mi |

### 2. Empirical FinOps Cost Optimization (2 Replicas)

| Dimension | Baseline Configured | Proposed Rightsized | Reduction | Provenance Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Per-Pod CPU Request** | 250 m (0.250 cores) | 50 m (0.050 cores) | **-80.0%** | Measured peak (15.16m) + 20% margin, clamped to 50m floor |
| **Per-Pod RAM Request** | 256 Mi (0.250 GiB) | 64 Mi (0.0625 GiB) | **-75.0%** | Measured peak (6.45Mi) + 20% margin, clamped to 64Mi floor |
| **Workload Replicas** | 2 | 2 | **0.0%** | Configured specification (Preserves High Availability) |
| **Monthly CPU Cost** | $11.54 / month | $2.31 / month | -$9.23 / month | Modeled AWS reference rate ($0.031611/vCPU-hr) |
| **Monthly RAM Cost** | $1.55 / month | $0.39 / month | -$1.16 / month | Modeled AWS reference rate ($0.004237/GB-hr) |
| **Total Monthly Spend** | **$13.08 / month** | **$2.69 / month** | **-$10.39 / month** | **Simulated Dry-Run Savings (-79.41% unrounded / -79.4% stored)** |

---

## Reproducing the Experiment

To reproduce the benchmark experiment against the live cluster:

```powershell
# Run the 70-second controlled benchmark
python src/finops_engine/experiment_runner.py --duration 70 --namespace edusaas --service edusaas-backend-svc --port 5678
```

The experiment runner will:
1. Automatically establish a background port-forward to the cluster service.
2. Cycle through the 4 workload phases (Idle → Warmup → Peak → Cooldown).
3. Sample live cgroup telemetry from Kubelet via Metrics Server every 2 seconds.
4. Synthesize rightsizing recommendations and cost comparisons.
5. Save the complete artifact bundle under `results/experiments/<new_run_id>/`.
6. Terminate port-forwards cleanly upon completion.

---

## Release Readiness & Forensic Validation Scripts

Two automated verification utilities are provided in `scripts/` using strictly standard Python libraries:

### 1. Forensic Experiment Validator
Validates mathematical consistency, artifact schemas, and unit conversions across experiment artifacts:
```powershell
python scripts/validate_experiment.py
```
*Executes 10 forensic checks: checks file existence, schema validity, observation count reconciliation against CSV, timestamp continuity, pod replica preservation, unit conversion fidelity, peak utilization calculation, percentile validity, AWS cost math, and dry-run safety distinction.*

### 2. Comprehensive Release-Readiness Checker
Validates repository integrity, essential configuration files, documentation completeness, and can execute the complete regression test suite:
```powershell
# Fast static integrity audit (28 checks)
python scripts/final_check.py

# Full release verification (Static integrity + full 54-test regression execution)
python scripts/final_check.py --run-tests
```

---

## Academic & Technical Honesty

In keeping with rigorous academic integrity standards:
- **Workload Proxy:** The evaluated workload is `hashicorp/http-echo`, not a full production LMS such as Moodle or Canvas.
- **Cluster Platform:** The prototype runs on a local Kind cluster on Windows Docker Desktop, not a multi-AZ AWS EKS deployment.
- **Billing Rates:** Cost estimates are modeled using published AWS on-demand reference rates, not real monthly AWS bills.
- **Dry-Run Enforcement:** Rightsizing recommendations are simulated; no running pods were terminated or manifests altered during testing.
- **Forecasting Model:** The demand forecasting model uses Exponential Moving Averages (EWMA) on synthetic calendar data to demonstrate predictive scaling principles; it is not an enterprise-trained deep learning model.

---

## Limitations & Future Work

1. **Short Observation Duration:** The benchmark ran for 70 seconds. Production FinOps analysis typically requires 7–14 days of telemetry to capture diurnal cycles and batch jobs.
2. **Workload Statefulness:** `http-echo` is stateless and memory-stable. Real enterprise LMS applications exhibit JVM heap fragmentation and dynamic memory caching requiring larger floors.
3. **Phase-II Cloud Integration:** Deploying on AWS EKS with Prometheus/OpenCost and integrating Karpenter for node-level spot autoscaling will be pursued in Phase-II.

---

## Documentation Links

### Core Technical Guides
- 📊 [Stage 06: Monitoring Infrastructure Setup](docs/stage_06_monitoring_setup.md)
- 📘 [Setup & Reproduction Guide](docs/SETUP_AND_REPRODUCTION.md)
- 📊 [Controlled Experiment Results](docs/EXPERIMENT_RESULTS.md)
- 🏗️ [System Architecture & Data Flow](docs/ARCHITECTURE.md)
- 🔍 [Final Engineering Verification Audit](docs/FINAL_VERIFICATION.md)

### Release Engineering & Auditing
- 🔬 [Final Code & Repository Audit](docs/FINAL_CODE_AUDIT.md)
- 🛡️ [Security & Reliability Review](docs/SECURITY_AND_RELIABILITY.md)
- ✅ [Release Readiness Certification](docs/RELEASE_READINESS.md)
- 📊 [Final Master Execution Report](docs/FINAL_EXECUTION_REPORT.md)

### Live Demonstration & Evaluation Prep
- 🚀 [Live Demonstration Runbook (5-7 Min Walkthrough)](docs/DEMO_RUNBOOK.md)
- 🎓 [Review & Viva Q&A Preparation (20 Questions & Answers)](docs/REVIEW_QA_PREPARATION.md)
- 📋 [Project Handover & Safe Shutdown](docs/PROJECT_HANDOVER.md)

### Academic Research Deliverables
- 📄 [Literature Survey](docs/Literature_Survey.md)
- 📄 [Research Gap Analysis](docs/Research_Gap.md)
- 👥 [Team Work Distribution](docs/Work_Distribution.md)

---

## Team & Acknowledgments

| Name & Registration No. | Role | Responsibilities |
| :--- | :--- | :--- |
| **K. DARSHAN** (24BIT0119) | Project Lead & Cloud Architect | Local Kind cluster, FinOps engine, rightsizing algorithms, test suite |
| **T. THARUN** (24BIT0155) | ML & Data Pipeline Engineer | Statistical demand forecasting, KSM ingestion pipeline |
| **DHANUSHKODI Y** (24BIT0143) | Backend & Systems Engineer | Lightweight REST API server, endpoint contract testing |
| **S. SANJAY** (24BIT0315) | Frontend & Documentation Lead | Vanilla web dashboard, benchmark visualization, technical documentation |

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
