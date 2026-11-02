# KubeCostFinOps — Comprehensive Evaluation Speaker Script
**Course:** BCSE355L — Cloud Architecture Design  
**Institution:** Vellore Institute of Technology (VIT), Vellore  
**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Team Lead & Presenter:** K. Darshan  
**Target Delivery Duration:** 10 to 12 Minutes (Plus 5–10 Minutes Faculty Q&A)

---

## Presentation Delivery Instructions & Strategy
1. **Pacing:** Speak at an even, confident pace (~130 words per minute).
2. **Academic Rigor:** Emphasize the mathematical foundations (cgroups accounting, reference pricing models, 20% safety headroom buffer, Holt's linear smoothing equations).
3. **Honesty & Transparency:** Explicitly state the distinction between measured container telemetry, modeled AWS reference prices, and realized cloud invoices. Never pretend offline simulations are newly created live AWS instances.
4. **Demonstration Alignment:** Refer directly to the live dashboard cockpit at `http://127.0.0.1:8000` and the genuine evidence screenshots.

---

## Slide-by-Slide Speaking Script

### Slide 1: Title & Team Members (0:00 – 0:45)
> **Slide Title:** *Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence*  
> **Key Focus:** Context, Team, Repository & Status

**Spoken Transcript:**
"Good morning, respected faculty members and evaluation committee. 

My name is K. Darshan, presenting our final project for BCSE355L Cloud Architecture Design: *Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence*.

In modern cloud-native academic ecosystems, containerized SaaS platforms—such as university learning management systems, digital exam portals, and automated code evaluation services—struggle with a fundamental cloud dilemma: how to guarantee zero-downtime availability during sudden student surges while eliminating the massive financial waste caused by idle container overprovisioning.

Today, we present an end-to-end, production-verified FinOps engineering solution. Our implementation has been rigorously developed on GitHub, verified with 57 automated unit and integration tests, passed through 28 comprehensive release checks, and empirically benchmarked on controlled workloads to achieve a modeled monthly cost reduction of 69% to 79.4%."

---

### Slide 2: Problem Statement (0:45 – 1:30)
> **Slide Title:** *Problem Statement: Cloud Resource & Budget Waste in Education*  
> **Key Focus:** Diurnal variance, static overprovisioning, HPA/VPA shortcomings

**Spoken Transcript:**
"Let us examine the core engineering problem. Educational workloads exhibit extreme diurnal and cyclical load volatility. During scheduled assignment deadlines or timed semester exams, request volume surges exponentially. Conversely, during late night hours, weekends, and academic vacations, traffic plummets into protracted idle troughs. The peak-to-trough ratio frequently exceeds 10 to 1.

Because an Out-Of-Memory kill or CPU throttling during an active exam is intolerable, cloud administrators routinely configure Kubernetes resource requests for peak anticipated load—for example, statically allocating 500 millicores of CPU and 512 Megabytes of RAM to microservices that consume less than 50 millicores 90% of the time.

In Kubernetes, resource *requests* represent guaranteed scheduling reservations. Even when a container sits idle, the Kubernetes scheduler locks that node CPU and memory, preventing other workloads from utilizing it. This leads to 60% to 80% permanent idle resource waste billed directly to the institution.

Existing Kubernetes autoscalers fail to solve this. The Horizontal Pod Autoscaler (HPA) scales out replica counts—meaning if a pod’s requests are oversized, HPA simply multiplies the financial waste across multiple nodes. Conversely, the native Vertical Pod Autoscaler (VPA) forcibly evicts and restarts running containers to change request specs, which terminates active student exam sessions. Proprietary SaaS tools like Kubecost and Cast.ai solve parts of this, but require expensive enterprise licensing, heavy agents, and external cloud dependencies. There is no open, non-disruptive, educational-aware FinOps engine available."

---

### Slide 3: Motivation (1:30 – 2:15)
> **Slide Title:** *Motivation: FinOps & Cloud Financial Accountability*  
> **Key Focus:** Institutional budget constraints, FinOps Inform-Optimize-Operate cycle

**Spoken Transcript:**
"Our motivation directly aligns with the FinOps cultural and operational movement: bringing financial accountability to the variable spending model of cloud computing.

Unlike commercial enterprises that pass cloud infrastructure costs onto customers, universities operate under fixed, inelastic departmental budgets and research grants. When unmonitored Kubernetes clusters generate 35% unallocated reservation waste, valuable institutional resources are lost.

Our framework implements the three pillars of the FinOps lifecycle:
1. **Inform:** Providing real-time, granular visibility into container-level expenditures by attributing costs down to dollars per vCPU-hour and dollars per GB-hour.
2. **Optimize:** Identifying reservation slack and computing data-driven rightsizing targets that incorporate safety headroom buffers.
3. **Operate:** Aligning continuous cluster capacity with the university's academic calendar through predictive time-series forecasting.

Architecturally, our system is strictly non-disruptive, completely self-hosted with zero external SaaS dependencies, and maintains mathematically verifiable provenance across all metrics."

---

### Slide 4: Project Objectives & Scope (2:15 – 3:00)
> **Slide Title:** *Project Objectives & Technical Scope*  
> **Key Focus:** 4 primary technical deliverables

**Spoken Transcript:**
"To resolve this challenge, we established four clear technical objectives:

First, **Continuous Telemetry Ingestion:** Building a non-intrusive scraping harness that samples container cgroups CPU and memory metrics every 15 seconds through Prometheus, Kube-State-Metrics, and OpenCost, maintaining seamless dual-mode operation between live cluster polling and offline forensic validation.

Second, **FinOps Cost Attribution:** Engineering a transparent pricing engine that maps Kubernetes resource vectors to standard AWS US-East-1 reference pricing cards—specifically $0.031611 per core-hour and $0.004237 per GB-hour across standard 730-hour monthly accounting periods.

Third, **Non-Disruptive Advisory Rightsizing:** Developing an intelligent rightsizing algorithm that computes optimal request targets based on peak historical utilization plus a 20% safety headroom buffer, while strictly enforcing architectural floors of 10 millicores CPU and 32 Megabytes RAM.

Fourth, **Operational Demand Forecasting & Cockpit:** Implementing a Double Exponential Smoothing (Holt's Linear Trend) forecasting baseline with 95% confidence intervals, exposed through a responsive, single-pane-of-glass executive dashboard."

---

### Slide 5: State of the Art & Research Gap (3:00 – 3:45)
> **Slide Title:** *State of the Art & Research Gap Analysis*  
> **Key Focus:** Comparative matrix against VPA, HPA, and Kubecost

**Spoken Transcript:**
"Slide 5 provides a comparative breakdown against current state-of-the-art approaches.

As shown in our evaluation matrix:
- Manual static sizing provides zero downtime, but at the cost of catastrophic overprovisioning and high financial waste.
- Kubernetes native VPA provides resource recommendations, but its active actuation mode forcibly evicts running pods, causing intolerable service interruptions.
- Commercial solutions like Kubecost and Cast.ai offer robust features, but are closed-source, require heavy in-cluster agents, and demand expensive recurring subscriptions that universities cannot justify.

Our framework uniquely bridges this gap. It operates in an **advisory declarative mode**, generating production-ready Kubernetes patch manifests that cloud administrators can review and apply during scheduled maintenance windows, guaranteeing zero downtime during classroom sessions. Furthermore, its cost attribution model is completely open, auditable, and requires zero external network calls."

---

### Slide 6: Proposed 3-Tier Architecture (3:45 – 4:30)
> **Slide Title:** *Proposed 3-Tier System Architecture*  
> **Key Focus:** Ingestion Tier, Analytical Engine Tier, Presentation Tier

**Spoken Transcript:**
"Our system architecture is structured into three clean, decoupled tiers:

**Tier 1 is the Telemetry & Ingestion Layer.** Workloads run inside Docker and Kubernetes containers on Kind or AWS EKS. At the node level, the Kubelet exposes container cgroups metrics via `/stats/summary`. Prometheus scrapes these metrics at 15-second intervals, while Kube-State-Metrics supplies declarative pod request and limit vectors. An ingestion adapter provides seamless dual-mode resilience, falling back to verified forensic datasets if cluster forwarders are unforwarded.

**Tier 2 is the FinOps Analytical Engine.** This layer houses our mathematical cost attribution module, the advisory rightsizing calculator with its 20% safety buffer, and the Holt's Linear Trend time-series forecasting model.

**Tier 3 is the Presentation & Management Cockpit.** It consists of a zero-dependency REST backend built on Python's standard library HTTP server, and an executive web dashboard developed in pure Vanilla HTML5, CSS3, and ES6 JavaScript. The entire architecture is lightweight, portable, and runs without heavy external application servers."

---

### Slide 7: Technology Stack & Cloud Infrastructure (4:30 – 5:15)
> **Slide Title:** *Technology Stack & Cloud Infrastructure*  
> **Key Focus:** EKS CloudFormation, Prometheus, Python backend, Vanilla JS frontend

**Spoken Transcript:**
"Examining the technical implementation specifications on Slide 7:

For cloud orchestration, we authored a production-ready AWS CloudFormation template defining 15 declarative infrastructure resources, including VPC, public subnets, security groups, an EKS cluster, IAM roles, and a managed node group utilizing cost-effective `t3.medium` EC2 instances. Crucially, we designed the architecture with a **Zero-NAT Gateway** layout, deploying nodes into public subnets with route table internet gateways. This intentional design choice eliminates the standard $0.045 per hour idle AWS NAT Gateway charge, saving approximately $32.40 per month during evaluation cycles.

For telemetry, we utilize Prometheus v2.45, Kube-State-Metrics, and OpenCost. 

Our backend is written in Python 3.14 using standard library components for the HTTP server, paired with NumPy, SciPy, and Pandas for rolling window statistics and time-series smoothing. Our frontend uses zero NPM build tooling or CDN scripts, allowing it to render instantly and function completely air-gapped."

---

### Slide 8: FinOps Engine & Cost Attribution (5:15 – 6:00)
> **Slide Title:** *FinOps Engine: Mathematical Cost Attribution Model*  
> **Key Focus:** Equations, AWS reference card, 730 hours/month standard

**Spoken Transcript:**
"Slide 8 details the mathematical core of our FinOps engine. 

The hourly cost of any container is computed as:
$$C_{\text{hourly}} = (R_{\text{CPU}} \times P_{\text{CPU}}) + (R_{\text{RAM}} \times P_{\text{RAM}})$$
Where $R_{\text{CPU}}$ is the allocated vCPU reservation in cores, and $R_{\text{RAM}}$ is the allocated memory in Gigabytes.

We ground our pricing in published AWS US-East-1 reference card rates for general-purpose compute:
- CPU unit price $P_{\text{CPU}}$ is $0.031611 per vCPU-hour.
- RAM unit price $P_{\text{RAM}}$ is $0.004237 per GB-hour.

To project monthly expenditure, we multiply hourly costs by 730 hours—the universally accepted FinOps accounting standard for monthly cloud operational hours.

Our engine attributes these costs hierarchically from container to pod, namespace, and total cluster spend. Crucially, we maintain absolute transparency: our dashboard explicitly isolates measured telemetry from reference price modeling, ensuring no opaque marketing claims or black-box estimates."

---

### Slide 9: Kubernetes Monitoring Architecture (6:00 – 6:45)
> **Slide Title:** *Kubernetes Monitoring & Telemetry Architecture*  
> **Key Focus:** Linux cgroups, Kubelet Summary API, Prometheus exposition, health matrix

**Spoken Transcript:**
"Slide 9 illustrates the observational plumbing. 

Telemetry begins in the Linux kernel through cgroups v1 and v2 accounting. CPU consumption is recorded via `cpu.stat`, tracking cumulative run time in microseconds. Memory usage is captured via `memory.current`, reflecting the container's active working set.

The node Kubelet harvests these metrics and exposes them at `/stats/summary`. Prometheus periodically scrapes the endpoint using standard exposition format, calculating rate derivatives like `rate(container_cpu_usage_seconds_total[1m])`. Concurrently, Kube-State-Metrics reads the Kubernetes etcd cluster state to provide the static requests and limits defined in the deployment YAML.

To ensure technical transparency, we implemented a dedicated component health API at `/api/v1/monitoring/status`. It actively probes Prometheus on port 9090, KSM on port 8080, and OpenCost on port 9003. When cloud port forwards are disconnected, the dashboard displays an honest 'Unavailable' indicator and gracefully activates our validated forensic benchmark datasets."

---

### Slide 10: Rightsizing Intelligence & Forecasting (6:45 – 7:30)
> **Slide Title:** *Rightsizing Intelligence & Demand Forecasting*  
> **Key Focus:** Peak + 20% safety buffer, floors (10m CPU, 32Mi RAM), Holt's smoothing

**Spoken Transcript:**
"Slide 10 presents our two analytical algorithms: advisory rightsizing and demand forecasting.

Our rightsizing algorithm computes optimal requests using the formula:
$$R_{\text{rec, CPU}} = \max\left(U_{\text{peak, CPU}} \times (1 + S_{\text{buffer}}),\ \text{Floor}_{\text{CPU}}\right)$$
$$R_{\text{rec, RAM}} = \max\left(U_{\text{peak, RAM}} \times (1 + S_{\text{buffer}}),\ \text{Floor}_{\text{RAM}}\right)$$

We calibrate the safety headroom buffer $S_{\text{buffer}}$ to 20% (a 1.20 multiplier) over peak observed load, while enforcing strict architectural minimum floors of 10 millicores CPU and 32 Megabytes RAM. This safety buffer is critical in educational systems: it absorbs sudden classroom micro-bursts, accommodates Java JVM JIT compilation spikes, and prevents fatal out-of-memory terminations.

For operational forecasting, we implemented Holt's Linear Trend model (Double Exponential Smoothing). By calibrating level smoothing factor alpha to 0.35 and trend factor beta to 0.15, the model separates baseline demand drift from short-term fluctuations, generating 95% confidence bounds ($\pm 1.96 \cdot \text{RMSE}$) so infrastructure teams can plan cluster capacity weeks ahead of exam cycles."

---

### Slide 11: Live Interactive Dashboard Demonstration (7:30 – 8:15)
> **Slide Title:** *Live Interactive Dashboard Demonstration*  
> **Key Focus:** Real UI walkthrough, executive KPI cards, comparison bar, inventory

**Spoken Transcript:**
"On Slide 11, we showcase our live dashboard cockpit, captured directly from our running environment.

As you can see:
- The top header provides instant cluster situational awareness with six executive KPI cards. It displays our baseline monthly spend of $24.15 alongside our rightsized spend of $7.48, highlighting an immediate 69.0% projected savings ($16.67/month).
- Directly beneath, a dynamic cost comparison bar visually contrasts baseline versus optimized spend.
- The cockpit features an active benchmark selector dropdown, allowing evaluators to inspect individual historical forensic runs like `exp-20261016-141448`.
- Further down, an active workload inventory details container-level requests, current utilization, and recommended patches.
- The UI polls asynchronously every 15 seconds with zero browser flicker and complete air-gapped independence."

---

### Slide 12: Experimental Methodology (8:15 – 9:00)
> **Slide Title:** *Experimental Methodology: 4-Phase Controlled Load Profile*  
> **Key Focus:** Benchmark profile, 70 seconds duration, 4 distinct phases

**Spoken Transcript:**
"Slide 12 outlines our rigorous experimental methodology. 

To scientifically validate our framework under realistic educational conditions, we executed a 70-second 4-phase controlled load profile against a containerized educational backend under experiment ID `exp-20261016-141448`:

- **Phase 1 (0 to 10 seconds): Baseline Idle at 0 RPS.** This phase measures the quiescent container state where CPU usage remains under 5 millicores, quantifying the massive initial overprovisioning gap.
- **Phase 2 (10 to 30 seconds): Moderate Load at 5 RPS.** Simulates regular classroom activities such as lecture quiz submissions, pushing CPU to 35 millicores.
- **Phase 3 (30 to 60 seconds): Stress Surge at 15 RPS.** Simulates a synchronized submission deadline rush. CPU utilization peaks at 82.3 millicores with a 95th percentile latency of 28.4 milliseconds and zero dropped requests.
- **Phase 4 (60 to 70 seconds): Recovery at 0 RPS.** Evaluates resource decay hysteresis and memory garbage collection as the container returns to quiescent baseline.

The entire dataset was verified against 10 out of 10 automated forensic integrity checks."

---

### Slide 13: Results & Empirical Cost Comparison (9:00 – 9:45)
> **Slide Title:** *Experimental Results & Empirical Cost Comparison*  
> **Key Focus:** 79.4% savings on benchmark workload, 0% error rate, sub-30ms latency

**Spoken Transcript:**
"Slide 13 presents our empirical experimental results.

Under the static baseline allocation, the container requested 500 millicores CPU and 512 Megabytes RAM, resulting in a modeled monthly expenditure of $13.08. 

Our FinOps engine analyzed the 4-phase benchmark, identified the peak utilization of 82.3 millicores, applied our 20% safety headroom buffer, and recommended a rightsized allocation of 98.8 millicores CPU and 128 Megabytes RAM.

This reduced monthly container expenditure from **$13.08 down to $2.69**—an empirical cost reduction of **79.4%**, saving $10.39 per container per month.

Crucially, this optimization was achieved with **zero performance degradation**: the request error rate remained 0.00% across all test phases, and the 95th percentile response latency rose by only 0.6 milliseconds (from 27.8ms to 28.4ms).

Furthermore, when subjected to an adverse stress test of 30 RPS on a single container replica, connection timeouts confirmed that vertical rightsizing must be complemented by horizontal autoscaling during severe traffic surges."

---

### Slide 14: Limitations & Future Scope (9:45 – 10:30)
> **Slide Title:** *Limitations & Future Engineering Roadmap*  
> **Key Focus:** Honest boundaries, GitOps PR generation, SageMaker ML, Karpenter

**Spoken Transcript:**
"In Slide 14, we present our technical limitations and future research scope with complete academic honesty.

**Our Current Limitations:**
1. Our engine operates strictly in **advisory mode**, generating declarative YAML patches rather than auto-mutating clusters, requiring administrator approval before rollout.
2. The empirical validation was conducted over a controlled 70-second burst profile. Multi-week telemetry ingestion is required to model semester-scale seasonal shifts.
3. Our pricing model utilizes standard AWS US-East-1 list rates; it does not model complex institutional enterprise agreements (EDP) or Spot instance discount curves.

**Our Future Roadmap:**
1. **GitOps Integration:** Automatically submitting rightsizing YAML patches as pull requests to ArgoCD or Flux repositories.
2. **Deep Learning Forecasting:** Migrating from statistical Holt-Winters to temporal transformer models such as DeepAR or Temporal Fusion Transformers (TFT) hosted on AWS SageMaker.
3. **Cluster Node Bin-Packing:** Integrating with Karpenter to physically consolidate pods and trigger EC2 node downscaling, converting container reservation savings into real cloud invoice reductions."

---

### Slide 15: Conclusion & Faculty Q&A (10:30 – 11:15)
> **Slide Title:** *Conclusion & Faculty Evaluation Q&A*  
> **Key Focus:** Verification summary, 57/57 tests passing, readiness for evaluation

**Spoken Transcript:**
"In conclusion, respected evaluators:

We have designed, implemented, and validated an enterprise-grade Kubernetes FinOps cost optimization framework tailored to SaaS-based educational platforms.

Our deliverables include:
- **57 passing automated unit and integration tests.**
- **28 passed release health checks with zero defects.**
- **10 out of 10 forensic verification passes** on controlled benchmark datasets.
- A demonstrated **69% to 79.4% modeled cloud cost reduction.**
- A reliable, non-disruptive advisory architecture with strict safety headroom.
- A fully reproducible one-command demonstration cockpit.

All code, manifests, and documentation are live on GitHub in the `develop` branch.

Thank you for your time, guidance, and evaluation. We now welcome your questions."

---

## Faculty Q&A Quick Reference Card
*(Keep this summary in front of you during questions)*

1. **Why 79.4% savings?**  
   Baseline static reservation (500m CPU, 512Mi RAM) = $13.08/mo. Rightsized allocation based on peak load 82.3m + 20% buffer (98.8m CPU, 128Mi RAM) = $2.69/mo. Difference is $10.39/mo or 79.4%.
2. **Why modeled and not actual AWS invoice?**  
   AWS bills for the underlying EC2 node instances (e.g., $0.0416/hr for `t3.medium`). Container savings are *allocatable headroom savings*. To realize cash savings on AWS invoices, rightsized pods must be packed together so Karpenter or Cluster Autoscaler can terminate unnecessary EC2 nodes.
3. **Why advisory instead of mutating?**  
   Mutating running pods requires Kubernetes to terminate and restart the pod (until in-place pod resizing becomes generally available). During university exams, pod restarts drop active HTTP sessions and destroy websocket states. Advisory mode provides safe declarative manifests for scheduled maintenance windows.
4. **Why did the 30 RPS test timeout?**  
   A single Python container backend replica has an internal single-threaded event loop concurrency ceiling. At 30 RPS, concurrent connections exhausted the HTTP socket backlog, proving that vertical rightsizing must be paired with horizontal pod autoscaling (HPA) for high-concurrency spikes.
5. **How does Holt's Linear Trend work?**  
   It uses double exponential smoothing: level equation ($L_t$) smooths baseline consumption with $\alpha=0.35$, trend equation ($T_t$) smooths growth slope with $\beta=0.15$. Future prediction is $L_t + h \cdot T_t$, bounded by $95\%$ confidence intervals ($1.96 \cdot \text{RMSE}$).

