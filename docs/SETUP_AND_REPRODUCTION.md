# KubeCostFinOps — Setup, Execution & Reproduction Guide

This guide provides end-to-end instructions for launching, testing, and reproducing the **Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms** on a local Windows machine.

---

## 1. Prerequisites & Environment Requirements

| Dependency | Minimum Version | Verified Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11 64-bit | Windows 11 Enterprise | Host operating system |
| **Python** | 3.10+ | 3.14.0 (Windows) | Backend API, FinOps Engine, Experiment Runner |
| **Docker Desktop** | 24.0+ | Docker Desktop v28+ | Local container runtime for Kind node |
| **Kind** (Kubernetes-in-Docker) | v0.20+ | v0.27.0 | Local multi-node / single-node cluster provisioner |
| **kubectl** | v1.28+ | v1.31.4 | Kubernetes CLI client |
| **Kubernetes Cluster** | v1.28+ | v1.37.0 (`kubecost-finops-local`) | Local evaluation target cluster |

> [!NOTE]
> All core backend and FinOps dependencies use Python standard libraries (`http.server`, `urllib.request`, `json`, `csv`, `math`, `unittest`, `subprocess`, `argparse`). No third-party pip packages or npm installs are required to run the backend or dashboard.

---

## 2. Cluster Topology & Verification

The project is designed to run against a local Kind cluster named `kubecost-finops-local`.

### 2.1 Verify Cluster Status
Open a Windows PowerShell terminal:

```powershell
# Verify cluster context
kubectl cluster-info --context kind-kubecost-finops-local

# Check cluster nodes
kubectl get nodes -o wide

# Verify core namespaces
kubectl get namespaces
```

Expected namespaces:
- `default`
- `kube-system`
- `monitoring` (Contains Kube-State-Metrics v2.12.0 and Metrics Server v0.7.1)
- `edusaas` (Contains the educational SaaS proxy workload)

### 2.2 Verify Metrics Server & Telemetry API
The experiment runner and telemetry pipeline consume live cgroup metrics via the Kubernetes Metrics API (`metrics.k8s.io`):

```powershell
# Verify Metrics Server pod
kubectl get pods -n monitoring -l k8s-app=metrics-server

# Verify live pod CPU/memory measurements
kubectl top pods -n edusaas
```

Expected output:
```
NAME                               READY   STATUS    RESTARTS   AGE
edusaas-backend-777bc59b8d-xxxxx   1/1     Running   0          ...
edusaas-backend-777bc59b8d-yyyyy   1/1     Running   0          ...
```

### 2.3 Verify Workload Manifests (Dry-Run Safety)
The baseline educational workload manifests are located in `src/k8s/`:
- [`deployment.yaml`](file:///C:/Users/gnavy/Downloads/KubeCostFinOps_Cloud_Project_2026/src/k8s/deployment.yaml): Deploys 2 replicas of `hashicorp/http-echo:latest` configured with static baseline requests (`cpu: 250m`, `memory: 256Mi`) and limits (`cpu: 500m`, `memory: 512Mi`).
- [`service.yaml`](file:///C:/Users/gnavy/Downloads/KubeCostFinOps_Cloud_Project_2026/src/k8s/service.yaml): Exposes port 5678 via ClusterIP `edusaas-backend-svc`.
- [`hpa.yaml`](file:///C:/Users/gnavy/Downloads/KubeCostFinOps_Cloud_Project_2026/src/k8s/hpa.yaml): Target 70% CPU utilization (2–5 replicas).

---

## 3. Running the Test Suite

The comprehensive regression suite covers unit testing of the FinOps calculation algorithms, Prometheus/KSM ingestion parser, lightweight REST API, and experiment runner.

### 3.1 Execute Full Test Suite
From the repository root (`C:\Users\gnavy\Downloads\KubeCostFinOps_Cloud_Project_2026`):

```powershell
python -m unittest discover -s tests -v
```

### 3.2 Expected Test Coverage
Verified benchmark: **52 tests passing**, 0 failures, 0 errors in ~2.5 seconds:
- `tests/test_finops_engine.py` (9 tests): Cost calculation, rightsizing, safety floors, AWS reference rate accuracy.
- `tests/test_pipeline.py` (13 tests): Prometheus text exposition parser, unit normalization, cost aggregation.
- `tests/test_backend_api.py` (23 tests): REST handlers, query filtering, CORS headers, error handling, latest and specific run lookups (`/api/v1/experiments/<run_id>`).
- `tests/test_experiment_runner.py` (7 tests): Metric aggregation, quantile calculation, dry-run rightsizing synthesis.

---

## 4. Launching the Backend API & Interactive Dashboard

The backend API server serves both RESTful JSON endpoints and the dashboard frontend on a single port via a standard-library HTTP server.

### 4.1 Start the Server
```powershell
python src/backend/main.py --host 127.0.0.1 --port 8000
```

### 4.2 Available Endpoints & Dashboard Access
Open a web browser to:
- **Interactive FinOps Dashboard**: `http://127.0.0.1:8000/` (or `http://127.0.0.1:8000/index.html`)

Test the REST API endpoints in a separate PowerShell window or browser:
```powershell
# 1. Health & Cluster Status
curl.exe -s http://127.0.0.1:8000/api/v1/health

# 2. Monthly Cost Breakdown (Modeled AWS reference rates)
curl.exe -s http://127.0.0.1:8000/api/v1/cost/monthly

# 3. FinOps Rightsizing Recommendations
curl.exe -s http://127.0.0.1:8000/api/v1/recommendations

# 4. Demand & Resource Forecast
curl.exe -s http://127.0.0.1:8000/api/v1/forecast/demand

# 5. Latest Controlled Experiment Benchmark
curl.exe -s http://127.0.0.1:8000/api/v1/experiments/latest

# 6. Specific Experiment Run Retrieval
curl.exe -s http://127.0.0.1:8000/api/v1/experiments/exp-20261016-141448
```

---

## 5. Running the Controlled FinOps Experiment

The experiment runner executes a controlled 4-phase benchmark against the live cluster:
1. **Phase A (Baseline Idle)**: 10s idle observation of baseline cgroup usage.
2. **Phase B (Warmup Load)**: 15s bounded traffic (~10 RPS) simulating standard student portal browsing.
3. **Phase C (Peak Exam Load)**: 25s concurrent traffic (~25 RPS) simulating simultaneous exam submissions.
4. **Phase D (Post-Load Cooldown)**: 15s post-burst idle observation to measure resource decay.

### 5.1 Run Command
```powershell
python src/finops_engine/experiment_runner.py --duration 70 --namespace edusaas --service edusaas-backend-svc --port 5678
```

### 5.2 Artifact Outputs
Each run creates an isolated directory under `results/experiments/<run_id>/` containing:
- `metadata.json`: Run timestamps, node specs, container images, parameter values.
- `observations.json`: Time-series telemetry samples (cgroup CPU/memory per pod, load client RPS and latency).
- `observations.csv`: Tabular observations suitable for data analysis and visualization.
- `recommendations.json`: Conservative FinOps rightsizing recommendation with safety margin.
- `evaluation.json`: Comparative cost analysis between baseline request and simulated rightsized request.
- `README.md`: Human-readable summary of the experiment run.

---

## 6. Safe Cleanup Instructions

> [!CAUTION]
> In accordance with safety rules, never run destructive cleanup commands against shared environments. Only terminate processes and temporary resources created specifically for this project.

```powershell
# 1. Terminate any background Python server processes
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*main.py*" } | Stop-Process

# 2. Terminate any lingering port-forward processes
Get-Process kubectl -ErrorAction SilentlyContinue | Stop-Process -Confirm:$false

# 3. Verify edusaas workload is undisturbed
kubectl get pods -n edusaas
```
