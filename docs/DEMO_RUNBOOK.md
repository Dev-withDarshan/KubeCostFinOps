# KubeCostFinOps — Live Demonstration Runbook

This runbook provides a complete, step-by-step presentation script designed for a flawless **5-to-7 minute academic and technical demonstration** of the **Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence**.

---

## 1. Pre-Demo Verification Checklist (1 Minute Before Presentation)

Open Windows PowerShell in the project directory:
```powershell
cd C:\Users\gnavy\Downloads\KubeCostFinOps_Cloud_Project_2026
```

Execute the pre-flight integrity check:
```powershell
# 1. Quick release-readiness verification
python scripts/final_check.py

# 2. Verify Kubernetes cluster status
kubectl get nodes
kubectl get pods -n edusaas
```

**Expected Outcome:**
- `scripts/final_check.py` returns `OVERALL STATUS: RELEASE READY (27 passed, 0 failures)`.
- Node `kubecost-finops-local-control-plane` is `Ready`.
- 2 pods of `edusaas-backend` are `Running` (1/1 Ready, 0 restarts).

---

## 2. Terminal Commands to Launch the Demonstration

### Terminal 1: Run the Automated Test Suite
Show the examiner that the implementation is covered by automated unit and regression tests:
```powershell
python -m unittest discover -s tests -v
```
*Expected: 54 tests run in ~2.5 seconds with `OK` (100% passing).*

### Terminal 2: Start the Backend API & Dashboard Server
```powershell
python src/backend/main.py --host 127.0.0.1 --port 8000
```
*Expected output: `Serving HTTP on 127.0.0.1 port 8000 (http://127.0.0.1:8000/) ...`*

---

## 3. Five-to-Seven Minute Demonstration Script

### Step 1: Open the Interactive Web Dashboard (0:00 – 1:00)
- **URL to Open:** [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)
- **What to say:**
  > *"This is the KubeCostFinOps dashboard. It provides full cost observability and FinOps intelligence for an educational SaaS platform deployed on Kubernetes. Notice the green indicator in the top header: the web dashboard communicates in real time with our Python standard-library REST backend on port 8000."*
- **What to point out:**
  - Header: Connected API indicator with real-time round-trip latency (~2ms).
  - Cluster status badge: `kubecost-finops-local` (Kubernetes v1.37.0).

---

### Step 2: Overview & Workload Cost Allocation (1:00 – 2:30)
- **Scroll to Section 1 & Section 2:** *Overview KPIs* and *Modeled Cloud Cost Allocation*.
- **What to say:**
  > *"In an educational SaaS environment like an LMS or examination portal, traffic is highly volatile. Here, our data ingestion pipeline has scraped Kube-State-Metrics on port 8080. It parsed container specifications and computed request-based monthly costs using published AWS US-East-1 reference rates ($0.031611/vCPU-hour, $0.004237/GB-RAM-hour)."*
- **What to point out:**
  - **KPI Cards:** Total monthly cost, allocated vCPU cores, and allocated RAM.
  - **Namespace Breakdown Table:** Shows how costs are attributed between namespaces (`edusaas`, `monitoring`, `kube-system`).
  - **Provenance Tag:** Point to the badge that explicitly states `MODELED REQUEST ESTIMATE` — highlight that this is modeled against AWS reference rates, not a live cloud bill.

---

### Step 3: Controlled Benchmark Experiment & Rightsizing (2:30 – 4:30)
- **Scroll to Section 4:** *Controlled FinOps Benchmark Experiment*.
- **What to say:**
  > *"Here is the core empirical evidence of our project. We conducted a reproducible, controlled 4-phase benchmark against our live educational workload: Baseline Idle, Warmup Load at 10 RPS, Peak Exam Burst at 25 RPS, and Post-Load Cooldown. Telemetry was sampled directly from the Linux kernel cgroups via Kubelet /stats/summary and the Kubernetes Metrics Server."*
- **What to point out:**
  - **Card 1 (Configured Spec):** The deployment was statically allocated **250m CPU and 256Mi RAM per pod** across 2 replicas, totaling $13.08/month.
  - **Card 2 (Measured Peak Telemetry):** Even during the peak student exam rush at 24.2 RPS (683 requests with zero HTTP errors and a 4.61ms p50 latency), peak CPU usage only reached **15.16 millicores (6.06% of requested)**, and memory peaked at **6.45 MiB (2.52% of requested)**. This empirically proves >93.9% idle compute waste!
  - **Card 3 (FinOps Rightsizing Proposal):** Applying a conservative **+20% safety buffer** and high-availability safety floors (50m CPU, 64Mi RAM) while retaining 2 replicas, our engine proposes rightsizing to **50m CPU and 64Mi RAM**.
  - **Simulated Savings:** Reduces monthly modeled cost from **$13.08 to $2.69**, achieving a **79.41% cost reduction ($10.39/month)** (79.4% stored in artifact).

---

### Step 4: Proving Dry-Run Safety & Experiment Reproducibility (4:30 – 5:30)
- **Switch to PowerShell Terminal:**
- **Run the forensic validator:**
  ```powershell
  python scripts/validate_experiment.py
  ```
- **What to say:**
  > *"To ensure technical and academic integrity, we built an independent forensic validator script. As you can see, all 10 checks pass: raw observation values match the evaluation report, observation counts in JSON match the CSV, and the cost formulas mathematically match the declared AWS reference rates."*
- **Verify Dry-Run Invariance:**
  ```powershell
  kubectl get deployment edusaas-backend -n edusaas -o jsonpath="{.spec.template.spec.containers[0].resources}"
  ```
- **What to say:**
  > *"Crucially, in adherence to strict FinOps audit guidelines, our engine operates in advisory dry-run mode. Notice that the live deployment in the cluster still has requests of 250m and 256Mi. We do NOT mutate running cluster workloads without explicit administrator approval."*

---

### Step 5: Demand Forecasting Module (5:30 – 6:30)
- **Scroll to Section 5 on Dashboard:** *Statistical Demand Forecasting*.
- **What to say:**
  > *"Educational platforms have predictable academic calendars (midterms, finals, enrollment). Our forecasting engine uses Exponentially Weighted Moving Averages (EWMA) to model traffic surges days in advance, allowing proactive scaling rather than reactive HPA thrashing."*
- **What to point out:**
  - SVG interactive chart showing historical data points and predicted surge window.
  - Evaluation tags: Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) computed on holdout data.
  - Clear provenance tag: Discloses whether the model is running on `LIVE_SNAPSHOT_HISTORY` or `SYNTHETIC_DEMO`.

---

## 4. Key Endpoints for Live Inspection

If the reviewer asks to inspect raw JSON endpoints, open:
- Health Check: [`http://127.0.0.1:8000/api/v1/health`](http://127.0.0.1:8000/api/v1/health)
- Modeled Cost Allocation: [`http://127.0.0.1:8000/api/v1/cost/monthly`](http://127.0.0.1:8000/api/v1/cost/monthly)
- Rightsizing Recommendations: [`http://127.0.0.1:8000/api/v1/recommendations`](http://127.0.0.1:8000/api/v1/recommendations)
- Latest Experiment Benchmark: [`http://127.0.0.1:8000/api/v1/experiments/latest`](http://127.0.0.1:8000/api/v1/experiments/latest)

---

## 5. Troubleshooting & Fast Recovery

| Issue | Cause | Instant Fix |
| :--- | :--- | :--- |
| **API Status shows "API Offline"** | Python server is not running on port 8000. | Run `python src/backend/main.py --host 127.0.0.1 --port 8000` in PowerShell. |
| **Port 8000 is already in use** | A previous Python server instance is still bound. | Run: `Get-Process python \| Where-Object { $_.MainWindowTitle -like "*main.py*" } \| Stop-Process` |
| **kubectl commands fail** | Kind cluster context is not selected. | Run `kubectl config use-context kind-kubecost-finops-local`. |
| **Metrics Server shows no metrics** | Container metrics scrape interval is syncing. | Wait 15 seconds; Metrics Server polls every 15s. |

---

## 6. What NOT to Claim (Academic Honesty Guardrails)

During the viva/presentation, **NEVER** claim:
1. Do **NOT** claim that this was deployed on Amazon AWS EKS. It runs on a local Kind Kubernetes v1.37.0 cluster on Docker Desktop.
2. Do **NOT** claim that `$10.39/month` was saved on an actual AWS bill. It is a **request-based modeled cost saving** calculated against published AWS reference rates.
3. Do **NOT** claim that the workload is a complete LMS with databases and grading scripts. It is `hashicorp/http-echo`, serving as a controlled, lightweight proxy microservice.
4. Do **NOT** claim that the rightsizing recommendation was auto-applied to the cluster. Emphasize that it is an **advisory dry-run recommendation** to preserve system stability.
5. Do **NOT** claim that the demand forecast is an enterprise deep learning model trained on SageMaker. It is an **EWMA statistical time-series model** with synthetic academic calendar spikes.

---

## 7. Shutdown Procedure (After Presentation)

```powershell
# 1. Stop the Python server: Press Ctrl+C in the server terminal window
# 2. Terminate any background port-forwarding:
Get-Process kubectl -ErrorAction SilentlyContinue | Stop-Process -Confirm:$false
```
