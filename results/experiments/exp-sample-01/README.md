# Experiment Evaluation Report — exp-sample-01 (SYNTHETIC TEST FIXTURE)

> [!WARNING]
> **SYNTHETIC TEST FIXTURE ONLY — NOT AN EMPIRICAL BENCHMARK**
> This directory is a synthetic test fixture copied from `exp-20261016-141448` exclusively to test API route resolution, 404 handling, and offline dashboard rendering.
> It must **NOT** be cited, evaluated, or presented as an independent or empirical benchmark run. The authoritative empirical benchmark run is [`exp-20261016-141448`](../exp-20261016-141448/).

**Date (UTC):** 2026-10-16T14:14:48.454350+00:00  
**Cluster:** `kubecost-finops-local` (v1.37.0)  
**Target Workload:** `edusaas/edusaas-backend` (2 replicas)  
**Telemetry Provenance:** Mock fixture derived from Kubelet Summary API & Metrics API  

---

## 1. Executive Summary

- **Fixture Status:** `SYNTHETIC_TEST_FIXTURE`
- **FinOps Recommendation Outcome:** `DOWNSIZE_REQUESTS` (SIMULATED)
- **Baseline Modeled Cost:** $13.08 / month
- **Proposed Rightsized Cost:** $2.69 / month
- **Projected Monthly Savings:** **$10.39 / month (79.41%)**

---

## 2. Load Profile & Metrics (Fixture Reference)

| Phase | Target RPS | Completed Reqs | Throughput (RPS) | Latency p50 (ms) | Latency p95 (ms) | Error Rate (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BASELINE` | 0.0 | 0 | 0.0 | 0.00 | 0.00 | 0.0% |
| `LOW_LOAD` | 10.0 | 196 | 9.7 | 4.66 | 5.75 | 0.0% |
| `HIGHER_LOAD` | 25.0 | 487 | 24.2 | 4.55 | 5.89 | 0.0% |
| `RECOVERY` | 0.0 | 0 | 0.0 | 0.00 | 0.00 | 0.0% |

---
*Reference synthetic test fixture for KubeCostFinOps API verification.*