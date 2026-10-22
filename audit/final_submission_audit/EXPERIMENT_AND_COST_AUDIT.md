# Experiment and FinOps Cost Calculation Audit

**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Course:** BCSE355L — Cloud Architecture Design  
**Audit Standard:** Forensic Data Integrity, Telemetry Provenance, and Mathematical Verification  
**Evaluation Scope:** All artifact directories under `results/experiments/` and FinOps Engine Pricing Formulas  

---

## 1. Inventory & Classification of Experiment Directories

The workspace contains three experiment directories under `results/experiments/`. Each directory was forensically analyzed for artifact completeness, schema validity, and telemetry authenticity:

| Directory Name | Classification | Primary Workload | Duration | Cycles / Samples | Authenticity & Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `exp-20261016-141448` | **EMPIRICAL BENCHMARK (Primary)** | `edusaas/edusaas-backend` (2 pods) | 69.4 seconds | 36 cycles (72 pod observations) | **Authentic Execution Evidence.** Executed against local multi-node Kind cluster `kubecost-finops-local` (Kubernetes v1.37.0). Controlled workload of 10 RPS and 25 RPS with 0.0% error rate. |
| `exp-20261016-141118` | **ADVERSE STRESS TEST (Adverse Run)** | `edusaas/edusaas-backend` (2 pods) | ~72 seconds | 38 cycles (76 pod observations) | **Authentic Execution Evidence (Counter-Evidence).** Executed at 30 RPS. Documented client connection timeouts (100.0% failure in Phase 3) while pod CPU/RAM remained non-saturated. The failure mechanism remains inconclusive (not proven socket exhaustion). |
| `exp-sample-01` | **SYNTHETIC TEST FIXTURE (Offline Mock)** | `edusaas/edusaas-backend` (2 pods) | N/A (Frozen snapshot) | 36 cycles (72 pod observations) | **Synthetic Test Fixture.** Explicitly copied from `exp-20261016-141448` to support unit tests, API route resolution, 404 validation, and offline dashboard rendering. Disclosed with prominent warning banners. |

---

## 2. Forensic Audit of Primary Empirical Run: `exp-20261016-141448`

### 2.1 Artifact Inventory & Structural Integrity
All six mandatory experiment artifacts are present, valid, and non-empty:
- `metadata.json` (1.13 KB): Execution environment, timestamp (UTC: `2026-10-16T14:14:48.454350+00:00`), cluster name (`kubecost-finops-local`), Kubernetes version (`v1.37.0`), target deployment (`edusaas/edusaas-backend`), and benchmark parameters.
- `observations.json` (78.99 KB): 36 cycle snapshots across 4 distinct phases (`BASELINE`, `LOW_LOAD`, `HIGHER_LOAD`, `RECOVERY`).
- `observations.csv` (10.10 KB): Exactly 72 pod-level observation records (36 cycles × 2 container replicas), perfectly matching `observations.json`.
- `recommendations.json` (2.56 KB): Advisory rightsizing recommendations with explicit safety floor clamping.
- `evaluation.json` (2.65 KB): Quantitative summary of peak telemetry, throughput, latency percentiles, and cost delta.
- `README.md` (2.50 KB): Human-readable markdown executive summary.

### 2.2 Workload Progression, Throughput, and Error Rates

| Phase Name | Duration (s) | Target RPS | Completed Requests | Achieved Throughput (RPS) | Error Count | Error Rate (%) | Latency p50 (ms) | Latency p95 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BASELINE` | ~15 s | 0.0 | 0 | 0.0 | 0 | 0.0% | 0.00 | 0.00 |
| `LOW_LOAD` | ~20 s | 10.0 | 196 | 9.7 | 0 | 0.0% | 4.66 | 5.75 |
| `HIGHER_LOAD` | ~20 s | 25.0 | 487 | 24.2 | 0 | 0.0% | 4.55 | 5.89 |
| `RECOVERY` | ~15 s | 0.0 | 0 | 0.0 | 0 | 0.0% | 0.00 | 0.00 |
| **Total / Overall** | **69.4 s** | — | **683** | — | **0** | **0.0%** | — | — |

### 2.3 Telemetry Provenance and Utilization Extraction
- **Monitored Workload:** Deployment `edusaas/edusaas-backend` consisting of 2 pods:
  1. `edusaas-backend-7485d55c8f-wxtv5`
  2. `edusaas-backend-7485d55c8f-kq86l`
- **Configured Allocation (Spec):**
  - CPU Request: `250m` (0.250 cores) per replica -> `500m` (0.500 cores) total.
  - Memory Request: `256Mi` (0.250 GiB) per replica -> `512Mi` (0.500 GiB) total.
- **Measured Empirical Utilization:**
  - Raw Baseline CPU: `0.40m` (0.16% of requested spec).
  - Raw Baseline Memory: `2.10 MiB` (0.82% of requested spec).
  - Raw Peak Load CPU: `15.16m` (0.01516 cores, representing **6.06% of requested CPU**).
  - Raw Peak Load Memory: `6.45 MiB` (0.00630 GiB, representing **2.52% of requested RAM**).
  - Both peak utilization figures in `evaluation.json` match the maximum values across all 72 raw pod observations in `observations.csv` down to the micro-unit.

### 2.4 Critical Telemetry Finding: Latency Percentile Aggregation
> [!NOTE]
> **Audit Finding on Latency Metrics:**
> The latency percentiles reported in `evaluation.json` (`p50 = 4.66 ms / 4.55 ms`, `p95 = 5.75 ms / 5.89 ms`) were calculated **in-memory** by the benchmark client during request execution. The raw individual request timestamps and round-trip durations (microsecond samples) were not exported to disk; only cycle-level averages and summary metrics were stored in `observations.csv`. Consequently, request-level latency distributions cannot be recomputed post-hoc from the CSV alone. This is an expected lightweight design choice for local testing, but is explicitly disclosed here for complete academic transparency.

---

## 3. Adverse Experiment Audit: `exp-20261016-141118`

An outstanding strength of this project is the inclusion of authentic adverse experiment records rather than cherry-picked successes:

- **What Happened:** In run `exp-20261016-141118`, the benchmark client attempted to push **30.0 RPS** continuously against the local port-forwarded Kubernetes service.
- **Observed Result:**
  - `BASELINE`: 0 requests, 0 errors.
  - `LOW_LOAD` (10 RPS): 137 completed requests, 6.4 RPS throughput, 4 errors (2.8% error rate), p50 = 15.76 ms, p95 = 30.71 ms.
  - `HIGHER_LOAD` (30 RPS): 0 completed requests, **100.0% error rate**, p50 = 3010.99 ms, p95 = 3025.13 ms.
- **Analysis & Status of Root Cause:**
  1. *Observed Telemetry:* Pod CPU remained low (average 1.68m, peak 7.82m, 3.13% utilization) and memory remained low (average 2.67 MiB, peak 3.45 MiB, 1.35% utilization), demonstrating that the container was not compute-saturated. All requests failed with timeouts at ~3,010 ms against a 3,000 ms threshold.
  2. *Status of Network Mechanism:* Inconclusive. Attributing the timeouts specifically to TCP socket backlog exhaustion or `kubectl port-forward` stream multiplexer queue saturation is a plausible hypothesis, but is not confirmed by direct packet traces or socket error logs in the archive.
  3. *Operational Finding:* The workload was successfully tested at 25 RPS in the local benchmarking setup. A subsequent 30 RPS trial experienced client timeouts. The precise failure mechanism remains inconclusive, and the application's maximum capacity has not been established.

---

## 4. Rigorous FinOps Cost Calculation Recomputation

### 4.1 Pricing Reference Parameters
- **Cloud Provider Reference:** Amazon Web Services (AWS) Commercial Cloud
- **Reference Region:** `us-east-1` (US East, N. Virginia)
- **Billing Model:** General Purpose On-Demand Compute Instances (`m5.large` / `c5.large` baseline equivalent)
- **Documented Unit Rates:**
  - vCPU Rate ($R_{cpu}$): **$0.031611 per vCPU-hour**
  - Memory Rate ($R_{mem}$): **$0.004237 per GiB-hour**
- **Billing Duration:** Standard FinOps accounting month = **730 hours**

### 4.2 Independent Recomputation of Baseline Cost

The target workload operates 2 replicas with static configured requests:
- Total CPU: $2 \times 250\text{ m} = 500\text{ m} = 0.500\text{ vCPU}$
- Total Memory: $2 \times 256\text{ MiB} = 512\text{ MiB} = \frac{512}{1024}\text{ GiB} = 0.500\text{ GiB}$

$$\text{Monthly CPU Cost} = 0.500\text{ vCPU} \times \$0.031611/\text{vCPU-hr} \times 730\text{ hrs} = \$11.538015$$

$$\text{Monthly Memory Cost} = 0.500\text{ GiB} \times \$0.004237/\text{GiB-hr} \times 730\text{ hrs} = \$1.546505$$

$$\text{Total Baseline Monthly Cost} = \$11.538015 + \$1.546505 = \mathbf{\$13.084520}$$

- **System Display Value:** **$13.08 / month**
- **Discrepancy:** None. Exactly matches rounded down to 2 decimal places.

### 4.3 Independent Recomputation of Rightsized Cost

The recommendation engine calculates rightsized requests based on peak observed usage plus a 20% safety margin, clamped to conservative production safety floors:
- Measured Peak CPU: $15.16\text{ m}$. With +20% buffer: $15.16 \times 1.20 = 18.192\text{ m}$.
  - Clamped to Production Safety Floor: **$50\text{ m}$ (0.050 vCPU)** per replica.
- Measured Peak Memory: $6.45\text{ MiB}$. With +20% buffer: $6.45 \times 1.20 = 7.74\text{ MiB}$.
  - Clamped to Production Safety Floor: **$64\text{ MiB}$ (0.0625 GiB)** per replica.
- Replicas preserved: **2** (maintains High Availability).

Total Rightsized Resources:
- Total Rightsized CPU: $2 \times 50\text{ m} = 100\text{ m} = 0.100\text{ vCPU}$
- Total Rightsized Memory: $2 \times 64\text{ MiB} = 128\text{ MiB} = \frac{128}{1024}\text{ GiB} = 0.125\text{ GiB}$

$$\text{Rightsized Monthly CPU Cost} = 0.100\text{ vCPU} \times \$0.031611/\text{vCPU-hr} \times 730\text{ hrs} = \$2.307603$$

$$\text{Rightsized Monthly Memory Cost} = 0.125\text{ GiB} \times \$0.004237/\text{GiB-hr} \times 730\text{ hrs} = \$0.38662625$$

$$\text{Total Rightsized Monthly Cost} = \$2.307603 + \$0.38662625 = \mathbf{\$2.69422925}$$

- **System Display Value:** **$2.69 / month**
- **Discrepancy:** None. Exactly matches rounded down to 2 decimal places.

### 4.4 Independent Recomputation of Projected Savings & Percentage

$$\text{Monthly Projected Dollar Savings} = \$13.084520 - \$2.69422925 = \mathbf{\$10.39029075}$$

- **System Display Value:** **$10.39 / month**

Now let us examine the savings percentage across three distinct mathematical formulations:
1. **Unrounded Floating Point Calculation:**
   $$\frac{\$10.39029075}{\$13.084520} = 0.7940903328 \implies \mathbf{79.41\%}$$
2. **Stored Value in JSON Artifacts (`evaluation.json` / `recommendations.json`):**
   $$\text{savings\_percent} = \mathbf{79.4\%} \quad (\text{rounded to 1 decimal place})$$
3. **Derived from Rounded Display Values ($10.39 / $13.08):**
   $$\frac{\$10.39}{\$13.08} = 0.7943425076 \implies \mathbf{79.43\%}$$

> [!TIP]
> **Mathematical Verification Summary:**
> There is **no mathematical error or fabrication**. The variation between 79.4%, 79.41%, and 79.43% across different sections of the documentation stems solely from intermediate display rounding (1 decimal place vs 2 decimal places vs rounded totals). The underlying double-precision arithmetic is 100% consistent across all engine files.

---

## 5. Scope Boundaries & Excluded Billing Charges

For strict academic and engineering accuracy, the following cost factors are explicitly excluded from the workload-level FinOps model:

| Cost Component | Actual AWS Charge | Treatment in KubeCostFinOps | Engineering Justification |
| :--- | :--- | :--- | :--- |
| **EKS Control Plane** | $0.10 / cluster-hour ($73.00 / month) | **Excluded** | Fixed cluster-level overhead; invariant to pod rightsizing or container capacity reductions. |
| **EC2 Node-Level Packing** | Full instance price (e.g. $69.35/mo for `m5.large`) | **Modeled as Fractional Request** | Workload-level FinOps models container request attribution. Realized savings require node bin-packing via Cluster Autoscaler or Karpenter. |
| **EBS Persistent Volumes** | ~$0.08 / GB-month (gp3) | **Excluded** | The target EduSaaS microservice is a stateless API backend utilizing in-memory compute. |
| **NAT Gateway & Data Egress** | $0.045 / hour + $0.09 / GB egress | **Excluded** | Local Kind network traffic is internal virtual bridge networking; no public NAT egress incurred. |
| **CloudWatch / OpenSearch Logs**| $0.50 / GB ingested | **Excluded** | Telemetry scraped directly via Prometheus exposition format without external SaaS logging ingestion. |
| **Taxes & Enterprise Discounts** | Variable (EDP / Savings Plans) | **Excluded** | Modeled against public on-demand list prices. |

---

## 6. Causation vs. Correlation & Dry-Run Boundaries

1. **Non-Mutating Dry-Run Mode:**
   - The recommendation engine operates in **pure advisory mode**.
   - Running `python -m src.finops_engine.pipeline` or `experiment_runner.py` **did not mutate** the running Kubernetes deployment spec (`kubectl apply` was not executed).
   - The running pods remained at `250m` CPU and `256Mi` RAM. The 79.4% savings represents a **simulated projection**, not an active cluster mutation.
2. **Causation vs. Correlation:**
   - The experiment proves that the workload *can survive* 25 RPS with low latency while utilizing less than 20m CPU.
   - However, because the rightsized configuration (`50m` / `64Mi`) was not actively applied to the cluster during the benchmark, the data demonstrates that the workload was over-provisioned; it does not directly measure application performance *under* the constrained 50m limit. That would require an active Phase-IV mutated benchmark.
