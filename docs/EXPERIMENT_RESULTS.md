# KubeCostFinOps — Controlled Experiment Results Report

**Experiment Run ID:** `exp-20261016-141448`  
**Execution Timestamp:** 2026-10-16T14:14:48Z  
**Duration:** 69.4 seconds  
**Target Cluster:** `kubecost-finops-local` (Kind v0.27.0, Kubernetes v1.37.0)  
**Target Namespace:** `edusaas`  
**Target Workload:** `edusaas-backend` (`hashicorp/http-echo:latest`, 2 Replicas)  
**Artifact Path:** `results/experiments/exp-20261016-141448/`

---

## 1. Executive Summary

A controlled, four-phase empirical benchmark was conducted against the `edusaas-backend` educational SaaS proxy service to evaluate the accuracy of the FinOps Intelligence pipeline in detecting over-provisioned infrastructure, calculating conservative rightsizing targets, and projecting cost savings under standard AWS reference pricing.

Key empirical findings:
1. **Severe Static Over-Provisioning Confirmed:** Under a peak student exam burst of **24.2 Requests Per Second (RPS)** across two replicas, the actual peak measured CPU consumption was **15.16 millicores (6.06% of the 250m configured request)**, and peak memory consumption was **6.45 MiB (2.52% of the 256 MiB configured request)**.
2. **Conservative Rightsizing with Production Safety Floors:** With a **+20% safety margin** above measured peak usage and mandatory safety floors (50m CPU, 64Mi RAM) to ensure high-availability stability, the FinOps engine proposed rightsized requests of **50m CPU** and **64Mi RAM** per replica.
3. **Significant Cost Reduction:** Baseline requested resources incurred a modeled cost of **$13.08/month** for the 2 replicas. The proposed dry-run rightsized configuration requires **$2.69/month**, achieving **$10.39/month in simulated savings (79.41% unrounded reduction / 79.4% stored)** while maintaining zero errors and sub-10ms response times.

---

## 2. Experimental Setup & Workload Specifications

### 2.1 Workload Details
- **Container Image:** `hashicorp/http-echo:latest` (lightweight HTTP microservice responding with configured JSON text, serving as a controlled proxy for educational portal requests).
- **Replica Count:** 2 replicas (`edusaas-backend-777bc59b8d-n755w`, `edusaas-backend-777bc59b8d-w2gvh`).
- **Configured Baseline Requests:**
  - CPU: `250m` (0.25 vCPU) per pod → `500m` total
  - Memory: `256Mi` (0.25 GiB) per pod → `512Mi` total
- **Configured Baseline Limits:**
  - CPU: `500m` (0.50 vCPU) per pod → `1000m` total
  - Memory: `512Mi` (0.50 GiB) per pod → `1024Mi` total

### 2.2 Telemetry Instrumentation
- **Telemetry Ingestion Source:** Kubernetes Metrics Server (`/apis/metrics.k8s.io/v1beta1/namespaces/edusaas/pods`) pulling raw Linux cgroup v2 accounting directly from Kubelet.
- **Sampling Frequency:** Polled at 2.0-second intervals for 36 sampling cycles (72 individual pod observations across the 2 running pods).
- **Load Generation Client:** Standard Python HTTP client utilizing socket connection reuse via `http.client.HTTPConnection` to target the `edusaas-backend-svc` cluster service via local port-forwarding.

---

## 3. Four-Phase Benchmark Performance & Telemetry

The experiment evaluated 4 operational phases representative of educational platform traffic patterns:

| Phase | Phase Name | Duration | Requests | Mean RPS | Error Rate | Latency p50 | Latency p95 | Peak Pod CPU | Peak Pod RAM |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase A** | Baseline Idle | 10.0 s | 0 | 0.0 RPS | 0.0% | — | — | 1.83 m | 5.86 Mi |
| **Phase B** | Warmup Load | 15.0 s | 145 | 9.7 RPS | 0.0% | 4.88 ms | 13.68 ms | 4.54 m | 6.07 Mi |
| **Phase C** | Peak Exam Burst | 25.0 s | 506 | 24.2 RPS | 0.0% | 4.55 ms | 10.74 ms | 15.16 m | 6.45 Mi |
| **Phase D** | Post-Load Cooldown | 15.0 s | 0 | 0.0 RPS | 0.0% | — | — | 2.05 m | 6.41 Mi |
| **Total** | **Full Benchmark** | **69.4 s** | **683** | **9.8 RPS** | **0.0%** | **4.61 ms** | **11.23 ms** | **15.16 m** | **6.45 Mi** |

### 3.1 HTTP Latency and Throughput Analysis
Across all 683 HTTP transactions:
- **Total Requests:** 683
- **Failed Requests:** 0 (100.0% success rate)
- **Median Latency (p50):** 4.61 ms
- **95th Percentile Latency (p95):** 11.23 ms
- **99th Percentile Latency (p99):** 28.45 ms
- Even at peak throughput (24.2 RPS), latency remained strictly bounded (p50: 4.55 ms, p95: 10.74 ms), proving that the service suffered no cgroup throttling or queue contention.

### 3.2 Telemetry Summary
- **Pod Replicas Monitored:** 2 pods
- **Total Time-Series Samples:** 36 time steps × 2 pods = 72 pod metric observations (+2 aggregate summary observations = 74 observations).
- **Observed Pod CPU Mean:** 4.12 m
- **Observed Pod CPU 95th Percentile:** 11.84 m
- **Observed Pod CPU Max Peak:** 15.16 m (6.06% of requested 250m)
- **Observed Pod RAM Mean:** 6.18 MiB
- **Observed Pod RAM Max Peak:** 6.45 MiB (2.52% of requested 256Mi)

---

## 4. FinOps Rightsizing Logic & Mathematical Formulations

### 4.1 Recommendation Formula
To safeguard against latency spikes, CPU throttling, and OOM-kills, the recommendation engine calculates the proposed request using a headroom multiplier and minimum production floors:

$$\text{Proposed CPU} = \max\left(\text{CPU Floor},\; \text{Peak Observed CPU} \times (1 + \text{Headroom})\right)$$

$$\text{Proposed RAM} = \max\left(\text{RAM Floor},\; \text{Peak Observed RAM} \times (1 + \text{Headroom})\right)$$

Where:
- $\text{Headroom} = 0.20$ (+20% safety margin)
- $\text{CPU Floor} = 0.050\text{ cores}$ ($50\text{ millicores}$)
- $\text{RAM Floor} = 0.0625\text{ GiB}$ ($64\text{ MiB}$)
- Replicas retained = $2$ (ensures multi-pod high availability)

### 4.2 Application to Measured Peaks
1. **CPU Calculation:**
   $$\text{Raw Target} = 15.16\text{ m} \times 1.20 = 18.19\text{ m}$$
   $$\text{Proposed CPU} = \max(50\text{ m},\; 18.19\text{ m}) = \mathbf{50\text{ m}}\; (0.050\text{ cores})$$
2. **RAM Calculation:**
   $$\text{Raw Target} = 6.45\text{ Mi} \times 1.20 = 7.74\text{ Mi}$$
   $$\text{Proposed RAM} = \max(64\text{ Mi},\; 7.74\text{ Mi}) = \mathbf{64\text{ Mi}}\; (0.0625\text{ GiB})$$

The engine appropriately clamped both metrics to their safety floors, ensuring workloads are never starved below Kubernetes scheduling minimums.

---

## 5. Cost Model Assumptions & Projected Savings

### 5.1 Pricing Model
Costs are modeled using published **AWS US-East-1 on-demand reference rates** based on the General Purpose compute standard ($m5.large$ baseline: 2 vCPU, 8 GiB RAM at $0.096/hour):
- **CPU Reference Rate:** $\$0.031611\text{ per vCPU-hour}$
- **RAM Reference Rate:** $\$0.004237\text{ per GB-hour}$
- **Monthly Hours Baseline:** $730\text{ hours/month}$

$$\text{Monthly Cost} = \left(\text{vCPU Cores} \times \$0.031611 + \text{RAM GiB} \times \$0.004237\right) \times 730$$

### 5.2 Comparative Cost Breakdown (2 Replicas)

| Dimension | Baseline Configured (Requested) | Proposed Rightsized (Dry-Run) | Absolute Delta | Percentage Reduction | Provenance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CPU Request (per pod)** | 250 m (0.250 cores) | 50 m (0.050 cores) | -200 m | -80.0% | Measured + Safety Floor |
| **RAM Request (per pod)** | 256 Mi (0.250 GiB) | 64 Mi (0.0625 GiB) | -192 Mi | -75.0% | Measured + Safety Floor |
| **Replicas** | 2 | 2 | 0 | 0.0% | Preserved HA |
| **Total vCPU Allocated** | 0.500 vCPU | 0.100 vCPU | -0.400 vCPU | -80.0% | Computed Specification |
| **Total RAM Allocated** | 0.500 GiB | 0.125 GiB | -0.375 GiB | -75.0% | Computed Specification |
| **Monthly CPU Cost** | $11.54 / mo | $2.31 / mo | -$9.23 / mo | -80.0% | Modeled AWS Rate |
| **Monthly RAM Cost** | $1.55 / mo | $0.39 / mo | -$1.16 / mo | -75.0% | Modeled AWS Rate |
| **Total Monthly Cost** | **$13.08 / mo** | **$2.69 / mo** | **-$10.39 / mo** | **-79.41%** | **Simulated Dry-Run Savings (-79.4% stored)** |

---

## 6. Academic & Technical Honesty: What Was Measured vs. Simulated

To preserve rigorous academic integrity, the project explicitly differentiates between empirical telemetry and simulated models:

| Component | Status | Classification | Explanation |
| :--- | :--- | :--- | :--- |
| **Pod CPU Usage** | **Measured** | Empirical Telemetry | Measured via Metrics Server / Linux cgroups during load burst (peak: 15.16m). |
| **Pod RAM Usage** | **Measured** | Empirical Telemetry | Measured via Metrics Server / Linux cgroups (peak: 6.45Mi). |
| **HTTP RPS & Latency** | **Measured** | Empirical Telemetry | Measured directly by Python benchmark client across 683 requests. |
| **Baseline Resource Request** | **Configured** | Specification | Declared in `src/k8s/deployment.yaml` (250m CPU, 256Mi RAM). |
| **Cloud Billing Rates** | **Modeled** | Published Reference Model | AWS US-East-1 on-demand reference rates ($0.031611/vCPU-hr, $0.004237/GB-hr). No real AWS account was billed. |
| **Cost Savings ($10.39/mo)** | **Simulated** | Dry-Run Simulation | Mathematically computed delta based on proposed resource reduction; cluster was NOT mutated. |
| **Traffic Workload** | **Proxy** | Synthetic Workload | `hashicorp/http-echo` was used as a lightweight proxy service rather than a full monolithic LMS. |

---

## 7. Threats to Validity & Limitations

1. **Synthetic Workload Complexity:** `hashicorp/http-echo` responds instantly in memory and does not execute database queries, session deserialization, or heavy business logic typical of production Canvas or Moodle deployments. A real LMS would exhibit higher baseline memory footprints (typically 256Mi–1GiB) and occasional GC pauses.
2. **Local Kind Node vs. AWS EKS Bare Metal:** The test executed on Kind on Docker Desktop on Windows. Cgroup measurements reflect the virtualized container environment rather than an AWS Nitro EC2 hypervisor.
3. **Short Observation Window (70 seconds):** While adequate for demonstrating responsiveness to burst traffic, a production FinOps recommendation engine requires 7 to 14 days of historical telemetry to capture weekly diurnal patterns and scheduled batch jobs.
4. **Dry-Run Enforcement:** In strict compliance with safe engineering rules, the recommendation was NOT auto-applied to the running cluster during the experiment. Long-term post-rightsizing stability under real multi-hour exam workloads remains a subject for Phase-II production trials.
