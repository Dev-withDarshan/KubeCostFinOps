# KubeCostFinOps — Live Deployment Evidence Package
**Course:** BCSE355L — Cloud Architecture Design  
**Institution:** Vellore Institute of Technology (VIT), Vellore  
**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Team Lead:** K. Darshan  
**Capture Timestamp (UTC):** 2026-11-02T20:55:44.511585+00:00  
**Cluster:** kind-kubecost-finops-local (Kubernetes v1.37.0)  
**Status:** **100% LIVE, EMPIRICAL & FULLY OPERATIONAL**

---

## 1. Verified Evidence Artifacts

| Filename | Type | Size | SHA-256 Checksum | Description |
|---|---|---|---|---|
| [00_dashboard_full_cockpit.png](00_dashboard_full_cockpit.png) | PNG Screenshot | 1265.3 KB | e8eb564ed3d258d6... | Full-page uncropped dashboard cockpit view (1920x5400) |
| [01_dashboard_executive_overview.png](01_dashboard_executive_overview.png) | PNG Screenshot | 253.4 KB | 506707b6b733cb38... | Executive Overview KPIs (.35 spend, .29 savings, API Connected) |
| [02_cost_allocation_and_breakdown.png](02_cost_allocation_and_breakdown.png) | PNG Screenshot | 258.8 KB | 7d06e708f4fa02db... | Cost Allocation and Namespace Breakdown Table |
| [03_rightsizing_recommendations.png](03_rightsizing_recommendations.png) | PNG Screenshot | 266.6 KB | e18cd65a84ba86d9... | Rightsizing Recommendations (20 cards with 20% headroom buffer) |
| [04_prometheus_targets_all_up.png](04_prometheus_targets_all_up.png) | PNG Screenshot | 18.9 KB | 2c11f309009d0e45... | Prometheus Web UI Targets (All 6 scrape targets in UP state) |
| [05_ksm_metrics_endpoint.png](05_ksm_metrics_endpoint.png) | PNG Screenshot | 150.8 KB | ad0b5f7c72b42b8d... | Kube-State-Metrics /metrics raw exposition data (1,094 series) |
| [06_opencost_allocation_records.png](06_opencost_allocation_records.png) | PNG Screenshot | 130.0 KB | c24481dca17d7c67... | OpenCost compute allocations per namespace |
| [07_kubernetes_nodes_and_pods.png](07_kubernetes_nodes_and_pods.png) | PNG Screenshot | 90.3 KB | e8b35e5c941f808c... | Live Kubernetes node and all namespace pods (15/15 Running) |
| [08_forecasting_dashboard.png](08_forecasting_dashboard.png) | PNG Screenshot | 218.1 KB | 519ba1ba45b0f6e1... | Holt Linear Trend baseline demand forecast SVG and steps |
| [09_experiment_results.png](09_experiment_results.png) | PNG Screenshot | 283.9 KB | 0a63420f9f9db092... | Controlled FinOps experiment benchmark (10/10 verified) |
| [10_component_monitoring_topology.png](10_component_monitoring_topology.png) | PNG Screenshot | 268.0 KB | 6feaee93bdde05ad... | Component Monitoring Topology (Prometheus, KSM, OpenCost all ONLINE) |
| [api_costs_summary.json](api_costs_summary.json) | JSON Telemetry | 4.8 KB | 5a26ffe879cbca1c... | Raw JSON output from /api/v1/costs/summary |
| [api_health.json](api_health.json) | JSON Telemetry | 0.7 KB | abadd0364a20dbaa... | Raw JSON output from /api/health |
| [k8s_cluster_state.txt](k8s_cluster_state.txt) | Raw Output | 3.7 KB | 564c5aef2f7c1d9a... | Raw terminal output of kubectl nodes and all pods |
| [ksm_metrics_sample.txt](ksm_metrics_sample.txt) | Raw Output | 180.9 KB | 093918ca74530861... | Raw Prometheus metrics exposition text from KSM :8080 |
| [monitoring_status.json](monitoring_status.json) | JSON Telemetry | 1.3 KB | 855d1757f8e54bb2... | Raw JSON output from FinOps Backend /api/v1/monitoring/status |
| [opencost_allocation.json](opencost_allocation.json) | JSON Telemetry | 10.4 KB | e1388adbc9b9fe3b... | Raw JSON output from OpenCost /allocation/compute |
| [prometheus_targets.json](prometheus_targets.json) | JSON Telemetry | 125.1 KB | 96bad9aff1ee90c3... | Raw JSON output from Prometheus /api/v1/targets |

---

## 2. Collection Commands Executed

`powershell
# 1. Prometheus Targets Verification
Invoke-RestMethod -Uri 'http://127.0.0.1:9090/api/v1/targets' | ConvertTo-Json -Depth 6 > prometheus_targets.json

# 2. OpenCost Compute Allocation
Invoke-RestMethod -Uri 'http://127.0.0.1:9003/allocation/compute?window=10m&aggregate=namespace' | ConvertTo-Json -Depth 6 > opencost_allocation.json

# 3. FinOps Backend Monitoring Matrix
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/monitoring/status' | ConvertTo-Json -Depth 6 > monitoring_status.json

# 4. KSM Raw Metrics
Invoke-RestMethod -Uri 'http://127.0.0.1:8080/metrics' > ksm_metrics_sample.txt

# 5. Live Kubernetes Cluster & Workloads
kubectl cluster-info; kubectl get nodes -o wide; kubectl get pods -A -o wide > k8s_cluster_state.txt

# 6. Unedited Chrome Headless Screenshot Suite
chrome.exe --headless=new --hide-scrollbars --window-size=1920,1080 --screenshot=<dest> <url>
`
