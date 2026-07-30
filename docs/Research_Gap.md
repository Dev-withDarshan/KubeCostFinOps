# Research Gap Analysis

> **Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
> **Course:** BCSE355L — Cloud Architecture  
> **Date:** 30 July 2026

---

## 1. Introduction

Based on the literature survey, this document identifies the **research gaps** in the current body of work on Kubernetes cost optimization, FinOps, and ML-driven autoscaling. It then outlines how the proposed framework addresses each gap.

---

## 2. Identified Research Gaps

### Gap 1: Disconnect Between Cost Monitoring and Autoscaling

**Current State:** Existing Kubernetes autoscaling mechanisms (HPA, VPA, Cluster Autoscaler) operate solely on resource utilization metrics (CPU, memory) without any awareness of the *cost implications* of their scaling decisions. Conversely, cost monitoring tools like Kubecost and OpenCost provide cost visibility but do not feed that information back into autoscaling policies.

**Impact:** Organizations scale reactively based on utilization thresholds, often leading to over-provisioning during anticipation of spikes or under-provisioning during unexpected surges — both resulting in either wasted spend or degraded performance.

**How We Address It:** Our framework creates a **closed-loop feedback system** where cost data from Kubecost/OpenCost is fed into the FinOps recommendation engine, which in turn adjusts HPA parameters and resource requests/limits to minimize cost while meeting SLA targets.

---

### Gap 2: Absence of Predictive (Proactive) Scaling in Cost Optimization Frameworks

**Current State:** All major open-source Kubernetes cost optimization tools (Kubecost, OpenCost, KubeSurvivor, Goldilocks) rely on **historical or current** metrics to generate recommendations. None incorporate predictive models that forecast future demand and proactively adjust resources *before* traffic spikes occur.

**Impact:** For workloads with predictable seasonality (such as educational platforms with exam-period traffic), reactive approaches miss the opportunity to pre-scale infrastructure, resulting in both SLA violations during ramp-up and cost waste during over-cautious pre-provisioning.

**How We Address It:** We integrate an **ML-driven demand forecasting model** (using Prophet / LSTM on Amazon SageMaker) that predicts traffic patterns based on historical metrics and academic calendar events, enabling proactive scaling 24–48 hours ahead of anticipated demand surges.

---

### Gap 3: No Domain-Specific Cost Optimization for Educational Platforms

**Current State:** Existing FinOps frameworks and Kubernetes cost tools are designed for **generic cloud workloads**. They do not account for the unique characteristics of educational platforms:
- Highly seasonal traffic (exam periods, enrollment windows, result days)
- Distinct workload types (interactive web services vs. batch grading vs. report generation)
- Strict SLA requirements during critical academic events
- Multi-tenant architectures serving different departments/courses

**Impact:** Generic recommendations (e.g., "reduce CPU requests by 20 %") may be appropriate during off-peak hours but dangerous during exam week, when any resource reduction could cause cascading failures.

**How We Address It:** Our framework incorporates **academic calendar events as exogenous features** in the forecasting model, enabling context-aware recommendations that differentiate between off-peak optimization opportunities and peak-period protection requirements.

---

### Gap 4: Limited Integration of Spot Instances with Workload Classification

**Current State:** While tools like Karpenter support automatic spot instance provisioning, they lack workload classification intelligence. Current approaches treat spot placement as a cluster-level decision rather than a workload-specific one.

**Impact:** Critical services (e.g., live exam portals) may inadvertently be placed on spot instances, risking interruption during exams. Meanwhile, fault-tolerant batch workloads (grading, analytics) that could safely run on spot instances remain on expensive on-demand nodes.

**How We Address It:** Our FinOps engine classifies workloads into **criticality tiers** (Critical, Standard, Batch) and maps each tier to an appropriate instance strategy — on-demand for critical, mixed for standard, and spot-preferred for batch — with automatic failover policies.

---

### Gap 5: Lack of End-to-End FinOps Automation in Open-Source Ecosystems

**Current State:** The FinOps lifecycle (Inform → Optimize → Operate) is well-defined in theory but existing open-source tools only cover the **Inform** phase (cost visibility). The Optimize and Operate phases — generating recommendations and automatically applying them — require manual intervention or expensive commercial tools (CloudHealth, Apptio).

**Impact:** Organizations have cost visibility but lack the automation to act on insights, resulting in a "dashboard fatigue" where cost reports are generated but rarely lead to actionable changes.

**How We Address It:** Our framework automates the full FinOps lifecycle:
1. **Inform** — Kubecost/OpenCost + Prometheus for real-time cost data
2. **Optimize** — FinOps engine generates rightsizing, HPA tuning, and spot-placement recommendations
3. **Operate** — Approved recommendations are automatically applied via Kubernetes API updates and Lambda-triggered scaling actions

---

## 3. Research Gap Summary Table

| # | Research Gap | Existing Approach | Our Contribution |
|---|------------|-------------------|-----------------|
| 1 | Cost-agnostic autoscaling | HPA/VPA scale on utilization only | Closed-loop cost-aware scaling |
| 2 | No predictive cost optimization | Reactive recommendations from historical data | ML forecasting with SageMaker (Prophet/LSTM) |
| 3 | Generic (non-domain) frameworks | One-size-fits-all Kubernetes cost tools | Educational platform-specific calendar-aware optimization |
| 4 | Naive spot instance placement | Cluster-level spot decisions | Workload-classified, tier-based spot strategy |
| 5 | Manual FinOps lifecycle | Inform-only tools; Optimize/Operate are manual | End-to-end automated Inform → Optimize → Operate |

---

## 4. Novelty of the Proposed Approach

The novelty lies in the **convergence** of four elements that have not been combined in prior work:

1. **Real-time cost observability** (Kubecost + Prometheus) providing the "truth" layer
2. **ML demand forecasting** (SageMaker) enabling proactive rather than reactive optimization
3. **Domain-specific intelligence** (academic calendar awareness) for educational SaaS platforms
4. **Automated FinOps lifecycle** closing the loop from insight to action

This creates a **FinOps Intelligence** system that is predictive, domain-aware, and fully automated — addressing the critical gap between cost visibility and cost action in Kubernetes environments.

---

## 5. References

See [Literature Survey](Literature_Survey.md) for the complete list of referenced works.

---

*Last updated: 30 July 2026*
