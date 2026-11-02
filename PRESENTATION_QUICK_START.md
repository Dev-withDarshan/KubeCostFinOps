# KubeCostFinOps — Presentation Quick Start Guide

**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Course:** BCSE355L Cloud Architecture & Computing  
**Institution:** Vellore Institute of Technology (VIT), Vellore  
**Team Lead:** K. Darshan  
**Evaluation Date:** Academic Year 2025–2026 (Final Project Evaluation)

---

## 1. Quick Startup (Zero-Friction Single Command)

To launch the complete FinOps platform and open the interactive dashboard in your browser, open PowerShell in the project directory (`C:\Users\gnavy\Downloads\KubeCostFinOps`) and run:

```powershell
.\START_PRESENTATION.ps1
```

### What this command does:
1. Validates project structure and core Python dependencies (`yaml`, `pandas`, `numpy`).
2. Cleans up any stale processes bound to port 8000.
3. Launches the lightweight Python REST backend server (`src/backend/main.py`) in the background.
4. Polls `/api/ready` to verify health.
5. Automatically opens the interactive dashboard at **`http://127.0.0.1:8000`** in your default web browser.

To stop the platform after the presentation:
```powershell
.\STOP_PRESENTATION.ps1
```

---

## 2. Demonstration Flow (10–12 Minute Faculty Presentation)

Follow this structured sequence during your faculty evaluation:

### Step 1: Problem Introduction (1 Minute)
* **What to say:** "Educational SaaS platforms (like Moodle, LMS, Canvas) face extreme workload variance: intense traffic spikes during 11:59 PM assignment deadlines and exam weeks, followed by long idle periods overnight. Standard static Kubernetes resource requests overprovision for the peak, leading to massive financial waste — up to 70–80% idle headroom."
* **What to show:** Open the dashboard at `http://127.0.0.1:8000`. Point to the header badge showing cluster telemetry provenance.

### Step 2: Executive FinOps Overview (2 Minutes)
* **What to show:** **Section 1: Executive FinOps Overview**
* **Key metrics to highlight:**
  * **Modeled Baseline Spend:** `$24.15/mo` ($0.0330/hr) based on static container requests across 8 containers.
  * **Rightsized Optimized Spend:** `$7.48/mo` ($0.0102/hr) achieved by downsizing requests to empirical utilization + 20% safety headroom.
  * **Projected Monthly Savings:** **`$16.67/mo` (69.0% cost reduction)**.
  * **CPU & RAM Capacity:** 1.000 Cores allocated vs. 15.2m observed peak (98.5% idle headroom).
* **Technical note:** Clarify that costs are calculated against public AWS US-East-1 reference cards ($0.031611/core-hr, $0.004237/GiB-hr), strictly distinguished from live AWS billing invoices.

### Step 3: Cost Intelligence & Breakdown (2 Minutes)
* **What to show:** **Section 2: Cost Intelligence & Allocation**
* **Key elements to highlight:**
  * **Baseline vs. Rightsized Comparison Bar:** Visual delta showing $24.15 dropping to $7.48.
  * **Namespace Breakdown:** `kube-system` ($22.80/mo, 94.4%) vs `monitoring` ($1.35/mo, 5.6%).
  * **Resource Cost Attribution:** CPU dominates cloud spend ($23.08/mo, 95.6%) compared to RAM ($1.07/mo, 4.4%), confirming that CPU rightsizing yields the greatest financial return.

### Step 4: Rightsizing & HPA Intelligence (2 Minutes)
* **What to show:** **Section 3: FinOps Optimization & Rightsizing**
* **Key elements to highlight:**
  * Click the filter tabs: **All Recommendations**, **Rightsizing**, **HPA Tuning**.
  * Highlight the safety headroom selector (10%, 20%, 30%). Show that the platform enforces an absolute minimum floor (0.01 cores, 0.032 GiB) to guarantee stability.
  * Explain the advisory dry-run model: recommendations are evaluated for capacity planning without executing unapproved mutating pod evictions.

### Step 5: Controlled Empirical Benchmark (3 Minutes)
* **What to show:** **Section 4: Controlled Kubernetes FinOps Experiment**
* **Key elements to highlight:**
  * Show the **Benchmark Run Selector** dropdown.
  * Select **`exp-20261016-141448`** (Empirical 4-Phase Benchmark). Point out the green badge: **`VALIDATED (10/10 PASS)`**.
  * Explain the 4-phase workload cycle:
    1. `BASELINE`: 0 RPS idle state (7.82m CPU).
    2. `LOW_LOAD`: 5 RPS sustained (8.66m CPU, 4.55ms p50 latency, 0.0% error rate).
    3. `HIGHER_LOAD`: 15 RPS peak (15.16m CPU, 5.90ms p95 latency, 0.0% error rate).
    4. `RECOVERY`: Return to baseline (8.22m CPU).
  * Show the rightsizing result for this specific deployment (`edusaas-backend`):
    * Configured spec: 250m CPU, 256Mi RAM per replica ($13.08/mo).
    * Proposed rightsized spec: 50m CPU, 64Mi RAM per replica ($2.69/mo).
    * **Empirical savings: $10.39/mo (79.4% reduction)** with zero application errors.

### Step 6: Kubernetes Monitoring & Integration Disclosures (1 Minute)
* **What to show:** **Section 5: Kubernetes Cluster & Monitoring Telemetry**
* **Key elements to highlight:**
  * Component cards: Prometheus Server, Kube-State-Metrics, OpenCost, Cluster Nodes.
  * Explain that when running in offline demo mode, the dashboard honestly displays Prometheus port-forward as "Offline / Snapshots Active" and OpenCost as "Reference Model Active", demonstrating rigorous academic honesty.
  * Show the active container inventory table.

### Step 7: Demand Forecasting Engine (2 Minutes)
* **What to show:** **Section 6: Resource Demand & Workload Forecasting**
* **Key elements to highlight:**
  * Toggle between **Synthetic Demo** and **Live Cluster History**.
  * Explain the algorithm: **Holt's Linear Trend baseline (Double Exponential Smoothing)** with level smoothing ($\alpha=0.35$) and trend smoothing ($\beta=0.15$).
  * Show the interactive SVG chart: historical curve, forecasted trajectory, and shaded 95% Gaussian confidence intervals ($\pm 1.96 \cdot \text{RMSE}$). Hover over forecast points to reveal tooltips.
  * Point to the evaluation tags: MAE and RMSE metrics.

### Step 8: Conclusion & Viva Q&A (2 Minutes)
* Summarize: "The framework proves that combining Kubernetes state telemetry with FinOps cost intelligence achieves a 69–79% reduction in modeled cloud capacity costs while maintaining safety headroom and multi-replica high availability."

---

## 3. Key Endpoint Verification Table

| Endpoint | Method | Purpose |
|---|---|---|
| `http://127.0.0.1:8000/` | GET | Interactive FinOps Web Dashboard |
| `http://127.0.0.1:8000/api/health` | GET | Overall system health & snapshot metadata |
| `http://127.0.0.1:8000/api/ready` | GET | Readiness probe for automated startup |
| `http://127.0.0.1:8000/api/v1/monitoring/status` | GET | Integration stack health (Prometheus, KSM, OpenCost) |
| `http://127.0.0.1:8000/api/v1/costs/summary` | GET | Baseline vs. optimized costs and namespace breakdown |
| `http://127.0.0.1:8000/api/v1/recommendations` | GET | Rightsizing and HPA optimization advisories |
| `http://127.0.0.1:8000/api/v1/experiments` | GET | Catalog of empirical benchmark runs |
| `http://127.0.0.1:8000/api/v1/experiments/exp-20261016-141448` | GET | Detailed forensic artifacts for primary experiment |
| `http://127.0.0.1:8000/api/v1/forecast?source=synthetic` | GET | Holt's linear trend forecast points & confidence bounds |

---

## 4. Emergency Backup Procedure

If port 8000 is occupied by another local service on your machine:
```powershell
.\START_PRESENTATION.ps1 -Port 8080
```
Then navigate to `http://127.0.0.1:8080/`.

If you prefer to run the server in an open foreground console window to show logs to the evaluator:
```powershell
python -m src.backend.main --port 8000
```
Then open `http://127.0.0.1:8000/` in Chrome or Edge.

