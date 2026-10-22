# KubeCostFinOps — Comprehensive Forensic Code Audit

**Date:** 2026-10-16  
**Auditor:** Principal Cloud Architect, Kubernetes Systems Engineer, and QA Lead  
**Branch:** `develop` | **Git Commit:** `d18df0c`  
**Target Workload:** `edusaas-backend` (2 replicas, `hashicorp/http-echo:latest`)  
**Target Cluster:** `kubecost-finops-local` (Kind v0.27.0, Kubernetes v1.37.0 on Docker Desktop)

---

## 1. Executive Summary

A comprehensive, non-destructive static and dynamic code audit was performed across the entire repository. The audit encompassed Python FinOps logic, Prometheus/KSM ingestion parsers, REST routing, HTML5/CSS/JavaScript presentation, Kubernetes manifests, automated test suites, and empirical benchmark artifacts.

Key Audit Conclusions:
1. **Mathematical & Algorithmic Integrity:** The FinOps calculation engine accurately evaluates requested vCPUs and memory against the declared AWS US-East-1 on-demand reference rates ($0.031611/vCPU-hr, $0.004237/GB-hr, 730 hrs/month). Baseline requested monthly cost ($13.0845 -> $13.08) and proposed rightsized cost ($2.6942 -> $2.69) with $10.39 simulated savings (79.41% from unrounded totals / 79.4% stored in artifacts) were independently verified to 4 decimal places.
2. **Strict Dry-Run Enforcement:** Rightsizing recommendations were verified to be strictly advisory. Live cluster resource requests (`cpu: 250m`, `memory: 256Mi`) remained completely untouched during and after load testing.
3. **Security Hardening Applied:** Directory traversal vulnerabilities in the experiment ID lookup route were remediated with strict regex whitelisting and directory boundary assertions. DOM XSS risks in `app.js` were neutralized by introducing `escapeHtml` sanitization for all dynamic telemetry values.
4. **Endpoint Aliases & Contract Consistency:** REST route discrepancies between documentation and internal handler names were resolved by adding canonical route aliases for health, monthly costs, and forecasts.
5. **Zero External Dependency Verification:** The entire codebase operates using standard library modules, eliminating supply-chain vulnerabilities and installation overhead.

---

## 2. Forensic Findings & Action Matrix

| ID | Component | Severity | Description & Evidence | Action Taken | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | `src/backend/main.py` | **Medium** | Path traversal risk in `/api/v1/experiments/<run_id>`: `run_id` was concatenated to `os.path.join` without sanitization. | Added `re.match(r"^[a-zA-Z0-9_\-]+$", run_id)` check and verified `os.path.abspath(target_dir)` resides strictly within the experiments directory. | **FIXED** |
| **SEC-02** | `src/frontend/app.js` | **Low-Medium** | Potential DOM XSS: Dynamic JSON fields (`namespace`, `workload`, `deployment`, `evidence`) were interpolated directly into `innerHTML`. | Created `escapeHtml` function and applied sanitization to all dynamic string insertions in table rows, cards, and legend elements. | **FIXED** |
| **REL-01** | `src/backend/main.py` | **Medium** | Inconsistent endpoint naming: Root docs referenced `/api/v1/cost/monthly` and `/api/v1/forecast/demand`, while backend only listened on `/api/v1/costs/summary` and `/api/v1/forecast`. | Added transparent route aliasing in `do_GET` supporting both legacy and canonical REST paths without breaking existing clients. | **FIXED** |
| **REL-02** | `src/frontend/app.js` | **Low** | Hardcoded fallback metrics: If experiment financial summary was missing, frontend fell back to hardcoded numbers (`'13.08'`, `'2.69'`, `'10.39'`, `'15.2m'`). | Replaced hardcoded fallback strings with clean `'--'` placeholders to prevent displaying unverified data as measured telemetry. | **FIXED** |
| **REL-03** | `scripts/final_check.py` | **Medium** | Test loader module resolution: `scripts/final_check.py` failed with `ModuleNotFoundError: No module named 'src'` when invoked directly. | Added `PROJECT_ROOT` to `sys.path` and configured `top_level_dir=tests_dir` in `unittest.defaultTestLoader.discover`. | **FIXED** |
| **DOC-01** | `README.md` | **Low** | Trailing whitespaces identified by `git diff --check`. | Cleaned whitespace formatting across documentation files. | **FIXED** |

---

## 3. Detailed Component Audits

### 3.1 FinOps Engine (`src/finops_engine/`)

- **`cost_analyzer.py`**:
  - `DEFAULT_AWS_PRICING` accurately defines:
    - `cpu_hourly_per_core = 0.031611`
    - `ram_hourly_per_gb = 0.004237`
    - `hours_per_month = 730.0`
  - Unit Conversion: Divides memory bytes by `1024.0**3` (binary GiB), matching AWS EC2 memory quoting standards where 1 GB of instance RAM equals 1,073,741,824 bytes.
  - Namespace Aggregation: Correctly handles both OpenCost windowed dictionaries and direct flat records.
  - Zero-Resource & Exception Handling: Appropriately returns `0.0` or raises `ConnectionError`/`ValueError` on malformed inputs.

- **`recommendation_engine.py`**:
  - Rightsizing Formula: Applies a configurable safety buffer (default: `+20%`) over peak observed utilization.
  - Safety Floors: Implements strict hard floors (`50m CPU` / `0.050 cores` and `64Mi RAM` / `0.0625 GiB`).
  - High Availability Preservation: Does NOT downscale pod counts; explicitly retains a minimum of 2 replicas.
  - Output Structure: Generates separate fields for current specification, measured telemetry, and proposed rightsizing.

- **`pipeline.py`**:
  - Live Ingestion: Scrapes KSM Prometheus text exposition on port 8080.
  - Regex Parser: Robustly extracts `kube_pod_container_resource_requests`, `kube_pod_container_resource_limits`, and `kube_deployment_status_replicas`.
  - Snapshot Generation: Writes timestamped JSON and flattened CSV files under `results/`.
  - Resiliency: Gracefully handles malformed exposition data and network connection drops with informative exit codes.

- **`experiment_runner.py`**:
  - Multi-Phase Load Generator: Threaded HTTP client using `http.client.HTTPConnection` with connection reuse to prevent socket exhaustion under Windows port-forwarding.
  - Telemetry Collection: Polls Kubelet `/stats/summary` directly with automatic fallback to `metrics.k8s.io`.
  - Artifact Generation: Produces versioned directories under `results/experiments/<run_id>/` with 6 standard files.

- **`ml_forecast.py`**:
  - Algorithm: Exponentially Weighted Moving Average (EWMA) and Holt Linear Trend with parameter bounds.
  - Evaluation: Computes Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) against holdout sets.
  - Transparency: Distinguishes `LIVE_SNAPSHOT_HISTORY` from `SYNTHETIC_DEMO` datasets with mandatory disclaimers.

### 3.2 Backend REST API Server (`src/backend/main.py`)

- **Server Architecture**: Single-threaded `http.server.HTTPServer` with custom request handler `FinOpsAPIHandler`.
- **Port Binding**: Defaults strictly to loopback `127.0.0.1:8000` to prevent unintended network exposure.
- **CORS Handling**: `do_OPTIONS` returns HTTP 204 with `Access-Control-Allow-Origin: *` and `Access-Control-Allow-Methods: GET, OPTIONS`.
- **Input Sanitization**:
  - Query parameters (`buffer`, `horizon`, `source`, `metric`) parsed with type validation and range checking.
  - Experiment IDs validated using `^[a-zA-Z0-9_\-]+$` regex to prevent directory traversal.
- **Static File Whitelist**: Restricts file serving strictly to `index.html`, `styles.css`, and `app.js` located in `src/frontend/`.

### 3.3 Frontend Dashboard (`src/frontend/`)

- **Aesthetics & Technology**: Vanilla HTML5, CSS custom properties (dark-mode palette with FinOps branding), and modular JavaScript.
- **Zero Build Step**: Runs directly in modern browsers without requiring Webpack, Vite, or npm installs.
- **XSS Mitigation**: Implements `escapeHtml()` sanitizing all dynamic text extracted from API payloads.
- **Graceful Degradation**: When API server is unreachable, displays a clear connection alert banner with retry buttons rather than unhandled JavaScript exceptions.

### 3.4 Kubernetes Manifests (`src/k8s/`)

- **`deployment.yaml`**:
  - Deployment `edusaas-backend` in namespace `edusaas`.
  - Workload: `hashicorp/http-echo:latest` with arguments `-text='{"service":"edusaas-api","status":"ok"}'`.
  - 2 Replicas for high availability.
  - Resources configured: Requests `cpu: 250m`, `memory: 256Mi`; Limits `cpu: 500m`, `memory: 512Mi`.
- **`service.yaml`**: Exposes port 5678 via ClusterIP `edusaas-backend-svc`.
- **`hpa.yaml`**: Horizontal Pod Autoscaler targeting 70% CPU utilization (min: 2, max: 5 replicas).
- **`monitoring/`**: Complete Kube-State-Metrics (v2.12.0) and Metrics Server (v0.7.1) configurations.

---

## 4. Test Suite Audit & Discovery

- **Test Discovery Command**: `python -m unittest discover -s tests -v`
- **Total Tests Discovered**: 54 test cases across 4 test modules:
  - `tests/test_finops_engine.py`: 9 passing tests
  - `tests/test_pipeline.py`: 13 passing tests
  - `tests/test_backend_api.py`: 25 passing tests (including new path-traversal and route-alias tests)
  - `tests/test_experiment_runner.py`: 7 passing tests
- **Execution Performance**: 54 tests run in **2.52 seconds** with 0 failures and 0 errors.

---

## 5. Residual Risks & Unresolved Limitations

1. **Synthetic Educational Proxy:** The target container is `hashicorp/http-echo`, not an enterprise multi-tier LMS application. While ideal for measuring cgroup scaling under synthetic traffic, real JVM/Python LMS workloads exhibit higher baseline memory footprints and garbage collection pauses.
2. **Local Kind Virtualization:** Telemetry reflects Linux cgroup v2 accounting inside Docker Desktop for Windows. While structurally identical to AWS EKS cgroups, physical hypervisor nuances (Nitro vCPU stealing, EBS latency) are not simulated.
3. **Single-Node Kind Cluster:** The Kind cluster runs as a single multi-role control-plane node. Multi-AZ node draining, inter-zone networking costs, and spot instance terminations require a full cloud deployment.
4. **Advisory Rightsizing:** Rightsizing recommendations were deliberately NOT mutated into running cluster manifests. Post-downsizing behavior under sustained multi-hour exam workloads remains a Phase-II research objective.
