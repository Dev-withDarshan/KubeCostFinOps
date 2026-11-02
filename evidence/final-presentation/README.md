# KubeCostFinOps -- Final Presentation Evidence Suite
**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Institution:** Vellore Institute of Technology (VIT), Vellore  
**Course:** BCSE355L - Cloud Architecture Design  
**Team Lead:** K. Darshan  
**Generated Date:** November 2026  
**Backend Port:** `http://127.0.0.1:8000` (PID Managed)

---

## 1. Evidence Artifact Index

This directory contains genuine, un-fabricated visual captures of the running KubeCostFinOps cockpit, FinOps mathematical engines, and REST endpoints taken via headless Google Chrome (`1920x1080` and `1920x2400`).

| Screenshot File | Resolution | Target Component | Demonstrated Technical Value |
|---|---|---|---|
| `01_dashboard_executive_overview.png` | 1920 x 1200 | Executive Header & KPI Cockpit | Shows 6 real-time metrics cards, Baseline vs. Rightsized Cost comparison bar ($24.15 vs. $7.48, 69.0% savings), and Benchmark run dropdown selector (`exp-20261016-141448`). |
| `02_cost_comparison_and_breakdown.png` | 1600 x 1000 | FinOps Cost Attribution Section | Displays monthly cost comparison, projected annual savings ($200.04/yr), CPU core cost allocation ($0.031611/core-hr), and RAM GB cost allocation ($0.004237/GB-hr). |
| `03_dashboard_full_cockpit.png` | 1920 x 2400 | Full UI Scroll Panorama | Complete single-pane-of-glass overview covering Executive KPIs, Cost Comparison, Rightsizing Recommendations Table, 4-Phase Controlled Experiment Analysis, Demand Forecasting Model, and Monitoring Stack Matrix. |
| `04_api_health_endpoint.png` | 1200 x 800 | REST `/api/health` | HTTP 200 payload with system status, UTC timestamp, memory usage, and operational uptime. |
| `05_api_monitoring_status.png` | 1200 x 800 | REST `/api/v1/monitoring/status` | Complete component availability matrix (Prometheus port 9090, Kube-State-Metrics port 8080, OpenCost port 9003, and cluster node availability). |
| `06_api_cost_summary.png` | 1200 x 800 | REST `/api/v1/costs/summary` | Real-time calculation verifying dynamic rightsizing totals ($24.15 baseline down to $7.48 rightsized). |
| `07_api_forecast_model.png` | 1200 x 800 | REST `/api/v1/forecast` | Statistical demand forecasting payload implementing Holt's Linear Trend baseline with 95% confidence intervals. |

---

## 2. Integrity Verification
- **Zero Fabrication:** Captured directly from live browser sessions running against `src.backend.main`.
- **Honest Provenance:** Clear labeling between historical benchmark runs (`exp-20261016-141448`), modeled AWS pricing card parameters ($0.031611/core-hr), and current cluster readiness.

