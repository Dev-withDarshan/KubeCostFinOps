# 🖥️ Frontend — KubeCostFinOps Intelligence Dashboard

Production-grade, lightweight web dashboard delivering Kubernetes resource analytics, modeled cloud cost allocations, rightsizing simulations, and statistical demand forecasting.

Designed to run **out of the box with zero npm packages or complex build chains**, serving directly from the lightweight Python API server or any standard static file server.

---

## 🌟 Key Architecture & Capabilities

1. **Direct Backend API Integration:**
   Consumes live Python backend REST endpoints:
   - `GET /api/health` — Cluster connection health and snapshot freshness.
   - `GET /api/v1/metrics/live` — Live observed Kubernetes node and container specifications.
   - `GET /api/v1/costs/summary` — Modeled request-based financial allocations.
   - `GET /api/v1/recommendations` — Rightsizing and Horizontal Pod Autoscaling (HPA) recommendations with evidence and assumptions.
   - `GET /api/v1/forecast` — Dynamic forecasting supporting both live historical analysis and synthetic educational demonstrations.

2. **Clean Design System:**
   - Modern dark cloud FinOps palette with accessible contrast.
   - Custom SVG charts: namespace cost allocation tracks and forecasting line charts with shaded 95% confidence intervals and interactive hover tooltips.
   - Fully responsive grid layout adapting across desktop (1320px) down to mobile viewport widths.

3. **Engineering Transparency & Provenance:**
   - Unmistakably distinguishes between **Observed Kubernetes State** (KSM specifications), **Modeled Financial Estimates** (AWS US-East-1 on-demand baseline rates), and **Synthetic Demonstrations** (simulated 48-hour student LMS traffic).
   - Distinct, informative `INSUFFICIENT DATA` view when live cluster snapshot history is less than the required 5-observation threshold.

---

## 🚀 Quickstart & Launch

### Option 1: Unified Server (Recommended)
The backend API server automatically serves the frontend dashboard:
```powershell
# From repository root
C:\Python314\python.exe -m src.backend.main --port 8000 --host 127.0.0.1
```
Open your browser and navigate to:
**`http://127.0.0.1:8000/`** or **`http://127.0.0.1:8000/index.html`**

### Option 2: Standalone Static Server
```powershell
# Serve frontend on port 3000
cd src\frontend
C:\Python314\python.exe -m http.server 3000
```
Open **`http://127.0.0.1:3000/`**, click the **Settings (gear icon)** in the top right, and ensure the API Base URL is set to `http://127.0.0.1:8000`.

---

## 🧪 Testing & Validation

Run all 40 unit and integration tests (validating API endpoints, forecasting algorithms, data pipeline, and static frontend delivery):
```powershell
C:\Python314\python.exe -m unittest discover -s tests -p "test_*.py" -v
```
