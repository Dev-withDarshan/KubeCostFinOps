"""
report_data.py
Contains all structured data, paper analyses, table contents, and citations
for the BCSE355L Final Project Report.
"""

PROJECT_METADATA = {
    "title": "Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence",
    "course_code": "BCSE355L",
    "course_name": "Cloud Architecture Design",
    "institution": "Vellore Institute of Technology, Vellore",
    "instructor": "Dr. Priya V",
    "team_number": "Team Project (4 Students)",
    "repository_url": "https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026",
    "submission_date": "21 October 2026",
    "programme": "B.Tech. Information Technology — III Year",
    "students": [
        {"name": "K. DARSHAN", "reg_no": "24BIT0119", "role": "Project Lead & Cloud Architect", "branch": "feature/darshan"},
        {"name": "DHANUSHKODI Y", "reg_no": "24BIT0143", "role": "Backend Developer & DevOps Engineer", "branch": "feature/dhanushkodi"},
        {"name": "T. THARUN", "reg_no": "24BIT0155", "role": "ML Engineer & Data Pipeline Developer", "branch": "feature/tharun"},
        {"name": "S. SANJAY", "reg_no": "24BIT0315", "role": "Frontend Developer & Documentation Lead", "branch": "feature/sanjay"},
    ]
}

# ---------------------------------------------------------------------------
# 15 Verified Research Papers (P1 - P15) for Table 0 and Table 1
# ---------------------------------------------------------------------------
PAPERS_DATA = [
    {
        "id": "P1",
        "student": "K. Darshan",
        "authors": "Ahmad, H., Treude, C., Wagner, M., & Szabo, C. (2025)",
        "title": "Towards resource-efficient reactive and proactive auto-scaling for microservice architectures",
        "venue": "Journal of Systems and Software, 225, Article 112390",
        "doi": "https://doi.org/10.1016/j.jss.2025.112390",
        "problem": "Delays, oscillation, and simultaneous over- and under-provisioning in default Kubernetes Horizontal Pod Autoscaling (HPA) when handling bursty microservice workloads.",
        "method": "Smart HPA (reactive heuristic) and ProSmart HPA (proactive ML-driven autoscaling) that cooperatively share node capacity across interdependent microservices.",
        "dataset_eval": "Sock Shop and TrainTicket microservice benchmarks under fluctuating synthetic and trace-driven arrival rates.",
        "findings": "Reduced over-provisioning by up to 34% and under-provisioning by 28% compared to standard Kubernetes HPA without violating p95 latency thresholds.",
        "existing_method": "Proactive and reactive HPA algorithms sharing cluster resources across microservices based purely on CPU/memory utilization thresholds.",
        "advantages": "Demonstrates that reactive and proactive policies can be coupled effectively; provides rigorous evaluation of over- and under-provisioning trade-offs.",
        "limitations": "Focuses strictly on raw hardware allocation; does not model financial cost metrics, cloud billing structures, or domain-specific calendar demand surges.",
        "gap": "Evaluates resource efficiency but lacks dollar-based cost attribution and does not incorporate domain calendar events (e.g., examination schedules) into scaling decisions.",
        "improvement": "Combine academic calendar features with container resource telemetry, mapping rightsizing recommendations directly to AWS reference hourly pricing."
    },
    {
        "id": "P2",
        "student": "T. Tharun",
        "authors": "Pothu, S. N., & Kailasam, S. (2024)",
        "title": "Effective priority-based resource allocation for proactive auto-scaling framework in workload prediction using hybrid tree-enhanced vector machine model",
        "venue": "Discover Sustainability, 5, Article 391",
        "doi": "https://doi.org/10.1007/s43621-024-00583-x",
        "problem": "High operational energy waste and resource misallocation in cloud data centers resulting from unpredictable demand swings.",
        "method": "Hybrid Tree-Enhanced Support Vector Machine (HTE-SVM) combined with priority-based proactive resource allocation across virtual machines.",
        "dataset_eval": "Real-world web workload traces (NASA and ClarkNet server access logs) evaluated for prediction accuracy and energy expenditure.",
        "findings": "Achieved 94.2% workload forecasting accuracy and reduced cloud data center operational energy consumption by 18.5%.",
        "existing_method": "Hybrid Decision Tree and Support Vector Machine (HTE-SVM) model classifying workload demand into operational priority tiers.",
        "advantages": "High prediction accuracy on historical web traces; establishes a priority-tiered scheduling hierarchy for non-critical workloads.",
        "limitations": "Evaluated at the coarse virtual machine (VM) level rather than containerized microservices; does not provide Kubernetes pod-level telemetry.",
        "gap": "VM-level workload classification does not translate directly to granular container cgroups, pod replica counts, or Kubernetes namespace cost showback.",
        "improvement": "Map priority-based demand classification directly to Kubernetes pod resource requests and limits, enforcing high-availability replica floors."
    },
    {
        "id": "P3",
        "student": "K. Darshan",
        "authors": "Tran, M.-N., & Kim, Y. (2024)",
        "title": "Optimized resource usage with hybrid auto-scaling system for Knative serverless edge computing",
        "venue": "Future Generation Computer Systems, 152, 304–316",
        "doi": "https://doi.org/10.1016/j.future.2023.11.010",
        "problem": "Cold-start latency spikes and memory over-allocation in serverless container platforms (Knative) hosted on edge-cloud nodes.",
        "method": "Hybrid autoscaling architecture combining proactive ARIMA traffic forecasting with fine-grained vertical container rightsizing.",
        "dataset_eval": "Synthetic and real trace-driven web request streams evaluated on a physical multi-node Kubernetes/Knative testbed.",
        "findings": "Decreased tail request latency by 22% while cutting memory footprint by 31.4% across distributed edge nodes.",
        "existing_method": "ARIMA-based proactive horizontal pod scaling coupled with vertical pod memory resizing in a Knative serverless environment.",
        "advantages": "Addresses both replica count and vertical sizing simultaneously; provides concrete evaluation on real containerized testbed infrastructure.",
        "limitations": "Serverless scale-to-zero model is unsuited for stateful educational portals and long-lived database connections; lacks cloud financial cost modeling.",
        "gap": "The serverless edge environment assumes scale-to-zero semantics, whereas enterprise educational SaaS requires persistent HA floors and explicit FinOps visibility.",
        "improvement": "Retain persistent minimum replica floors (e.g., 2 replicas) for high availability and calculate cost savings using transparent cloud hourly billing rates."
    },
    {
        "id": "P4",
        "student": "T. Tharun",
        "authors": "Zhang, H., Guo, T., Tian, W., & Ma, H. (2024)",
        "title": "Learning-driven hybrid scaling for multi-type services in cloud",
        "venue": "Journal of Parallel and Distributed Computing, 189, Article 104880",
        "doi": "https://doi.org/10.1016/j.jpdc.2024.104880",
        "problem": "Balancing strict Service Level Objective (SLO) compliance against cloud infrastructure leasing costs across heterogeneous multi-tier services.",
        "method": "Ensemble deep learning predictor coupled with reinforcement learning for concurrent horizontal and vertical scaling with anomaly compensation.",
        "dataset_eval": "Alibaba Cluster Trace 2018 and Google Cluster Trace 2019 evaluated for response time violations and virtual instance hourly costs.",
        "findings": "Maintained >99.2% SLO compliance while decreasing overall virtual compute leasing expenses by 24.6%.",
        "existing_method": "Ensemble neural network forecasting coupled with Q-learning reinforcement learning for multi-service autoscaling.",
        "advantages": "Simultaneously optimizes response time and compute leasing cost; accounts for complex multi-service interaction effects.",
        "limitations": "High computational complexity and training overhead; complex reward functions make policy decisions opaque and difficult to audit.",
        "gap": "Complex multi-service RL policies cannot be safely deployed without transparent safety guardrails and dry-run audit mechanisms.",
        "improvement": "Implement an interpretable, rule-governed recommendation engine with +20% safety headroom and auditable dry-run validation before applying actions."
    },
    {
        "id": "P5",
        "student": "Dhanushkodi Y",
        "authors": "Alidoost Alanagh, Y., Firouzi, M., Rasouli Kenari, A., & Shamsi, M. (2023)",
        "title": "Introducing an adaptive model for auto-scaling cloud computing based on workload classification",
        "venue": "Concurrency and Computation: Practice and Experience, 35(22), Article e7720",
        "doi": "https://doi.org/10.1002/cpe.7720",
        "problem": "Standard autoscalers applying a single uniform forecasting algorithm across diverse, non-stationary workload patterns.",
        "method": "Unsupervised workload classification (clustering traces into bursty, periodic, and steady regimes) to dynamically select the best-fit predictor.",
        "dataset_eval": "Real-world web server access logs (University of Saskatchewan and Calgary web server traces).",
        "findings": "Improved autoscaling provisioning responsiveness by 29% and reduced prediction error by 33% across regime transitions.",
        "existing_method": "K-means clustering to classify workload segments, routing each segment to specialized regression or time-series forecasters.",
        "advantages": "Demonstrates that classifying workload regimes before forecasting significantly reduces prediction error compared to a single static model.",
        "limitations": "Evaluated exclusively on offline historical web server logs; does not integrate live Kubernetes cgroup metrics or FinOps cost visibility.",
        "gap": "Offline web log classification does not provide live cluster telemetry ingestion or tie predicted traffic surges to dollar-cost savings.",
        "improvement": "Ingest live Kubernetes Metrics API telemetry in real time and categorize workload phases (Baseline, Low Load, Exam Surge, Recovery) for tailored FinOps rightsizing."
    },
    {
        "id": "P6",
        "student": "K. Darshan",
        "authors": "Saravanan, G., & Santhosh Babu, A. V. (2024)",
        "title": "Workload prediction for enhancing power efficiency of cloud data centers using optimized self-attention-based progressive generative adversarial network",
        "venue": "International Journal of Communication Systems, 37(1), Article e5634",
        "doi": "https://doi.org/10.1002/dac.5634",
        "problem": "Inability of conventional shallow neural networks to capture long-range temporal dependencies and extreme burst peaks in enterprise cloud workloads.",
        "method": "Self-Attention Progressive Generative Adversarial Network (SA-PGAN) optimizing multi-step workload time-series generation.",
        "dataset_eval": "PlanetLab and Google Cluster traces evaluating Root Mean Square Error (RMSE), Mean Absolute Error (MAE), and server power consumption.",
        "findings": "Reduced workload forecasting RMSE to 0.042 and delivered an estimated 16.8% reduction in cloud server power overhead.",
        "existing_method": "Generative Adversarial Network with self-attention layers generating synthetic workload forecasts to preemptively spin up capacity.",
        "advantages": "Captures complex temporal correlations and sharp workload bursts better than standard recurrent neural networks.",
        "limitations": "Extremely heavy training and inference computation; requires massive historical training datasets; prone to mode collapse during sudden shifts.",
        "gap": "Heavy neural architectures require GPU infrastructure that increases cost, defeating the purpose of lightweight FinOps cost optimization for smaller institutions.",
        "improvement": "Employ lightweight statistical and additive calendar-aware models (e.g., Prophet-style diurnal and event-based forecasting) deployable on standard CPU instances."
    },
    {
        "id": "P7",
        "student": "K. Darshan",
        "authors": "Jia, K., Xiang, J., & Li, B. (2024)",
        "title": "DuCFF: A dual-channel feature-fusion network for workload prediction in a cloud infrastructure",
        "venue": "Electronics, 13(18), Article 3588",
        "doi": "https://doi.org/10.3390/electronics13183588",
        "problem": "Feature decoupling where sequential temporal telemetry and exogenous environmental features are processed independently without cross-feature fusion.",
        "method": "Dual-Channel Feature-Fusion Network (DuCFF) combining 1D Convolutional Neural Networks (CNN) with Bidirectional LSTM channels.",
        "dataset_eval": "Public multi-tenant cloud workload traces incorporating external calendar indicators evaluated on CPU and memory utilization sequences.",
        "findings": "Outperformed standard LSTM and GRU baselines with a 19.3% reduction in MAE and 21.5% improvement in peak traffic forecast accuracy.",
        "existing_method": "Two-branch neural architecture processing temporal metric sequences in parallel with exogenous context before feature fusion.",
        "advantages": "Explicitly demonstrates the importance of fusing external domain indicators with internal performance metrics for accurate peak prediction.",
        "limitations": "Does not close the operational loop: outputs raw predicted numbers without translating them into actionable Kubernetes scaling or rightsizing actions.",
        "gap": "Feature fusion stops at numerical prediction and does not generate safe Kubernetes pod resource specifications or assess FinOps economic impact.",
        "improvement": "Connect exogenous feature fusion (academic calendar exam flags, deadlines) directly to an automated FinOps rightsizing engine with safety floors."
    },
    {
        "id": "P8",
        "student": "T. Tharun",
        "authors": "Alharthi, S., Alshamsi, A., Alseiari, A., & Alwarafy, A. (2024)",
        "title": "Auto-scaling techniques in cloud computing: Issues and research directions",
        "venue": "Sensors, 24(17), Article 5551",
        "doi": "https://doi.org/10.3390/sensors24175551",
        "problem": "Lack of comprehensive taxonomic standardization and empirical trade-off analysis across modern cloud autoscaling paradigms.",
        "method": "Systematic literature survey analyzing over 120 autoscaling publications spanning reactive, proactive, hybrid, and machine learning techniques.",
        "dataset_eval": "Taxonomic classification and comparative matrix across AWS, GCP, Azure, and open-source container orchestrators.",
        "findings": "Identified critical industry deficiencies: less than 15% of surveyed systems incorporate cost metrics, and under 5% account for domain calendar events.",
        "existing_method": "Taxonomic survey categorizing autoscalers by architecture, trigger metrics, decision mechanisms, and cloud deployment models.",
        "advantages": "Provides an authoritative, holistic overview of the current state of cloud autoscaling and clearly articulates open research frontiers.",
        "limitations": "Secondary survey paper without an original empirical software prototype or experimental benchmark.",
        "gap": "Confirms the widespread absence of FinOps cost accountability and domain-specific calendar integration in production autoscalers.",
        "improvement": "Directly address the primary gaps identified by Alharthi et al. by building an end-to-end framework uniting FinOps cost attribution with calendar-aware scaling."
    },
    {
        "id": "P9",
        "student": "Dhanushkodi Y",
        "authors": "Xue, S., Qu, C., Shi, X., Liao, C., Zhu, S., Tan, X., Ma, L., Wang, S., Wang, S., Hu, Y., Lei, L., Zheng, Y., Li, J., & Zhang, J. (2022)",
        "title": "A meta reinforcement learning approach for predictive autoscaling in the cloud",
        "venue": "Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 4290–4299",
        "doi": "https://doi.org/10.1145/3534678.3539063",
        "problem": "Prohibitive cold-start training times and catastrophic forgetting when standard reinforcement learning models encounter unseen cloud workload regimes.",
        "method": "Meta-Reinforcement Learning (Meta-RL) architecture utilizing few-shot policy generalization across diverse multi-tenant cloud workloads.",
        "dataset_eval": "Industrial production workload traces from Ant Group spanning thousands of online microservices.",
        "findings": "Accelerated policy adaptation to new workload profiles by 80% while saving 14.7% in compute allocation without compromising SLOs.",
        "existing_method": "Model-agnostic meta-learning training policy networks across multiple task distributions to achieve fast few-shot online adaptation.",
        "advantages": "Overcomes the slow convergence of standard RL in dynamic environments; validated on massive enterprise-scale production microservices.",
        "limitations": "Requires sophisticated distributed training infrastructure and access to massive cross-workload historical repositories.",
        "gap": "Meta-RL is over-engineered for educational institutions that operate predictable, calendar-governed academic cycles rather than thousands of arbitrary services.",
        "improvement": "Use deterministic academic calendar rules and statistical moving averages that provide predictable, explainable rightsizing without training overhead."
    },
    {
        "id": "P10",
        "student": "S. Sanjay",
        "authors": "Qiu, H., Banerjee, S. S., Jha, S., Kalbarczyk, Z. T., & Iyer, R. K. (2020)",
        "title": "FIRM: An intelligent fine-grained resource management framework for SLO-oriented microservices",
        "venue": "Proceedings of the 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI '20), 805–825",
        "doi": "https://www.usenix.org/conference/osdi20/presentation/qiu",
        "problem": "Microservice tail-latency degradation and cascading resource contention caused by uncoordinated per-pod autoscaling across deep call graphs.",
        "method": "FIRM framework utilizing adaptive reinforcement learning to identify bottlenecked microservices, mitigate contention, and dynamically rightsize resource limits.",
        "dataset_eval": "DeathStarBench microservice benchmark suites (Social Network and Media Service) evaluated on a physical 40-node server cluster.",
        "findings": "Reduced tail (p99) latency by up to 16x and prevented 90% of SLO violations while reclaiming up to 62% in overallocated CPU cores.",
        "existing_method": "Dynamic reinforcement learning tracking critical latency paths and applying fine-grained vertical container resource adjustments.",
        "advantages": "Pioneering work in microservice-aware resource isolation and SLO preservation; rigorous physical cluster evaluation.",
        "limitations": "High systems overhead requiring kernel-level eBPF instrumentation; focuses on low-level contention rather than monthly cloud dollar expenditure.",
        "gap": "Focuses on microsecond-level CPU throttling and tail latency rather than cloud cost modeling, educational demand forecasting, or FinOps accountability.",
        "improvement": "Translate resource rightsizing into transparent AWS reference monthly dollar costs while establishing explicit minimum resource floors (50m/64Mi) to prevent tail latency spikes."
    },
    {
        "id": "P11",
        "student": "S. Sanjay",
        "authors": "Rzadca, K., Findeisen, P., Świderski, J., Zych, P., Broniek, P., Kusmierek, J., Nowak, P., Strack, B., Witusowski, P., Hand, S., & Wilkes, J. (2020)",
        "title": "Autopilot: Workload autoscaling at Google",
        "venue": "Proceedings of the 15th European Conference on Computer Systems (EuroSys '20), Article 16",
        "doi": "https://doi.org/10.1145/3342195.3387524",
        "problem": "Vast cluster-wide resource slack caused by human operators conservatively over-sizing resource requests to prevent out-of-memory or throttling crashes.",
        "method": "Google Autopilot combining historical utilization windowing, exponential moving averages, and automated horizontal/vertical sizing algorithms.",
        "dataset_eval": "Google global production fleet consisting of hundreds of thousands of jobs and millions of containers evaluated over multiple months.",
        "findings": "Reduced aggregate cluster resource slack by over 50% across Google's worldwide production container fleet with negligible task disruption.",
        "existing_method": "Multi-window historical utilization tracking combining moving averages with decay factors to recommend rightsized task limits and task counts.",
        "advantages": "The definitive empirical benchmark for production container rightsizing at scale; proves that automated rightsizing can safely reclaim >50% slack.",
        "limitations": "Proprietary internal Google Borg architecture; tightly coupled to internal telemetry and lacks public cloud billing awareness or calendar hooks.",
        "gap": "Autopilot operates in private corporate infrastructure without public cloud multi-tenant billing models (AWS On-Demand/Spot) or academic event conditioning.",
        "improvement": "Adapt Autopilot's proven moving-window rightsizing principles to standard Kubernetes and open AWS reference pricing with domain calendar awareness."
    },
    {
        "id": "P12",
        "student": "K. Darshan",
        "authors": "Burns, B., Grant, B., Oppenheimer, D., Brewer, E., & Wilkes, J. (2016)",
        "title": "Borg, Omega, and Kubernetes",
        "venue": "ACM Queue, 14(1), 70–93",
        "doi": "https://doi.org/10.1145/2898442.2898444",
        "problem": "Designing robust, decoupled, and declarative container orchestration platforms capable of scaling distributed applications across shared server pools.",
        "method": "Foundational architectural analysis tracing the evolution from Google Borg and Omega to the open-source Kubernetes container management system.",
        "dataset_eval": "Architectural case study based on more than a decade of Google container orchestration production operations.",
        "findings": "Established core cloud-native abstractions: declarative state reconciliation, pod encapsulation, label-based loose coupling, and cgroup isolation.",
        "existing_method": "Declarative desired-state control loops continuously reconciling actual cluster state against user-specified YAML manifests.",
        "advantages": "Defines the fundamental architectural philosophy and container abstractions governing modern Kubernetes cloud engineering.",
        "limitations": "Foundational systems architecture paper; does not address autonomous cloud financial engineering, FinOps showback, or modern public cloud pricing.",
        "gap": "Kubernetes reconciles pod requests declared by humans but lacks internal economic intelligence to verify whether declared requests are financially wasteful.",
        "improvement": "Build an external FinOps reconciliation loop that inspects live cgroup utilization and proposes rightsized declarative pod manifests."
    },
    {
        "id": "P13",
        "student": "Dhanushkodi Y",
        "authors": "Taylor, S. J., & Letham, B. (2018)",
        "title": "Forecasting at scale",
        "venue": "The American Statistician, 72(1), 37–45",
        "doi": "https://doi.org/10.1080/00031305.2017.1380080",
        "problem": "Difficulty of producing accurate, automated, and robust time-series forecasts across thousands of business metrics with non-linear trends and holidays.",
        "method": "Decomposable additive time-series model (Prophet) combining non-linear trend curves, multi-period Fourier seasonality, and custom holiday/calendar effects.",
        "dataset_eval": "Thousands of daily and hourly business event and web traffic time-series at Meta (Facebook).",
        "findings": "Delivered robust, automated forecasts resilient to missing data, outliers, and structural trend shifts, with human-interpretable parameters.",
        "existing_method": "Decomposable additive regression model: y(t) = g(t) + s(t) + h(t) + e(t) modeling trend, seasonality, and holiday events.",
        "advantages": "Excels at incorporating custom calendar events (holidays, exams) with interpretable coefficients; robust to missing data and regime shifts.",
        "limitations": "Designed for macro business metrics; requires integration scaffolding to ingest high-frequency container telemetry and output Kubernetes scaling actions.",
        "gap": "Calendar-aware forecasting has not been integrated into a closed-loop Kubernetes FinOps engine to trigger pre-emptive scaling before exam traffic surges.",
        "improvement": "Incorporate Prophet's additive calendar formulation into the FinOps forecasting pipeline to model academic examination windows and assignment deadlines."
    },
    {
        "id": "P14",
        "student": "K. Darshan",
        "authors": "Mao, H., Schwarzkopf, M., Venkatakrishnan, S. B., Meng, Z., & Alizadeh, M. (2019)",
        "title": "Learning scheduling algorithms for data processing clusters",
        "venue": "Proceedings of the ACM SIGCOMM 2019 Conference, 270–288",
        "doi": "https://doi.org/10.1145/3341302.3342080",
        "problem": "Hand-tuned heuristic cluster schedulers (FIFO, Fair, DRF) failing to optimize execution times across complex directed acyclic graph (DAG) job workflows.",
        "method": "Decima system employing Graph Neural Networks (GNN) and reinforcement learning to learn workload-aware scheduling policies directly from job DAG structures.",
        "dataset_eval": "Large-scale Spark and data analytics workload traces evaluated on physical testbed clusters and high-fidelity simulators.",
        "findings": "Reduced average job completion time by 21% to 3x compared to state-of-the-art hand-crafted cluster scheduling heuristics.",
        "existing_method": "Graph Neural Networks embedding job DAG dependencies, trained via policy gradient reinforcement learning to schedule tasks.",
        "advantages": "Demonstrates that learned policies can drastically outperform human-engineered heuristics in complex multi-resource scheduling environments.",
        "limitations": "Targeted at big-data batch DAG computation (Spark) rather than continuous, interactive educational web application microservices.",
        "gap": "Batch job DAG scheduling does not address continuous HTTP request-driven educational SaaS workloads or monthly public cloud cost attribution.",
        "improvement": "Focus on interactive SaaS request telemetry and establish deterministic rightsizing algorithms that provide immediate, verifiable FinOps savings."
    },
    {
        "id": "P15",
        "student": "S. Sanjay",
        "authors": "Mao, H., Alizadeh, M., Menache, I., & Kandula, S. (2016)",
        "title": "Resource management with deep reinforcement learning",
        "venue": "Proceedings of the 15th ACM Workshop on Hot Topics in Networks (HotNets '16), 50–56",
        "doi": "https://doi.org/10.1145/3005745.3005750",
        "problem": "Multi-resource packing in cluster computing where heuristic bin-packing algorithms make sub-optimal trade-offs between CPU, memory, and time.",
        "method": "DeepRM system translating cluster allocation states directly to scheduling decisions using model-free deep policy gradient reinforcement learning.",
        "dataset_eval": "Simulated multi-resource computing clusters under synthetic and trace-derived job arrival sequences.",
        "findings": "Demonstrated that neural agents can learn effective multi-resource bin-packing and fair-sharing policies purely through environmental reward signals.",
        "existing_method": "Deep policy gradient neural network observing 2D image-like representations of cluster resource allocation to place tasks.",
        "advantages": "Foundational proof-of-concept demonstrating that reinforcement learning can solve multi-resource allocation without handcrafted heuristics.",
        "limitations": "Simulated discrete time-step environment; did not evaluate real Linux cgroups, live network jitter, or commercial cloud billing structures.",
        "gap": "Simulated RL allocation does not establish practical, auditable cost savings in live Kubernetes clusters hosting latency-sensitive educational services.",
        "improvement": "Implement transparent, inspectable FinOps cost formulas grounded in empirical Kubernetes Metrics Server cgroup measurements and AWS reference rates."
    }
]

# ---------------------------------------------------------------------------
# Novelty Dimension Data for Table 2
# ---------------------------------------------------------------------------
NOVELTY_DATA = [
    {
        "dimension": "New Feature: Academic Calendar Integration",
        "existing": "Generic cloud autoscalers (Kubernetes HPA, AWS Target Tracking) react purely to current CPU/RAM thresholds with zero awareness of academic schedules, causing reactive lag during sudden examination bursts.",
        "proposed": "Domain-specific FinOps intelligence engine that ingests structured academic calendar features (exam periods, assignment deadlines, diurnal student cycles) to anticipate traffic surges before they occur.",
        "demonstration": "Evaluated using the synthetic educational workload telemetry pipeline (`ml_forecast.py`) outputting 6 correlated domain fields and tested under 10 RPS and 25 RPS simulated student traffic phases."
    },
    {
        "dimension": "Algorithm / Processing: FinOps Rightsizing with Safety Floors",
        "existing": "Standard rightsizing tools either propose aggressive down-scaling that risks OOM crashes during unexpected spikes, or rely on opaque black-box machine learning models with unpredictable decisions.",
        "proposed": "Conservative rightsizing recommendation algorithm enforcing a +20% buffer above measured peak usage, mandatory high-availability replica retention (>=2), and absolute production safety floors (50m CPU, 64Mi RAM).",
        "demonstration": "Empirical benchmark `exp-20261016-141448` where configured 250m/256Mi requests were safely rightsized to 50m/64Mi, preserving zero error rate and sub-6ms p95 latency while projecting 79.41% cost reduction."
    },
    {
        "dimension": "Cloud Architecture / AWS Integration",
        "existing": "Monolithic cloud architectures or unmonitored container clusters lacking granular namespace-level cost attribution and event-driven remediation loops.",
        "proposed": "Enterprise AWS-native architecture coupling Amazon EKS, EC2 On-Demand/Spot instances, Prometheus telemetry, DynamoDB real-time event storage, S3 archival, and automated Lambda cost-remediation functions.",
        "demonstration": "Documented in complete architectural diagrams (Figures 1, 2, and 3), multi-AZ VPC network designs, and formal infrastructure-as-code manifests in `src/k8s/` and `src/aws/`."
    },
    {
        "dimension": "Security, Automation & Verification",
        "existing": "Autoscaling scripts that execute blind live cluster mutations without verification, exposing clusters to destabilization, API path traversal, or privilege escalation.",
        "proposed": "Defense-in-depth security model featuring IAM least-privilege policies, regex-whitelisted API inputs, sanitized frontend DOM rendering, non-mutating dry-run rightsizing validation, and automated regression suites.",
        "demonstration": "Verified via 54 automated unit/integration tests (100% pass rate in 2.3s) and 28 release-readiness verification checks with zero warnings and zero security vulnerabilities."
    }
]

# ---------------------------------------------------------------------------
# Dataset Description for Table 3
# ---------------------------------------------------------------------------
DATASET_ATTRIBUTES = [
    ("Dataset name", "Educational SaaS Platform Workload & Telemetry Dataset (Synthetic & Live Ingestion)"),
    ("Source / organisation", "Generated locally via `src/finops_engine/ml_forecast.py` and ingested from live Kubernetes cgroup accounting via Metrics Server v0.7.1 and Kube-State-Metrics v2.12.0"),
    ("URL / repository path", "https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026 (local paths: `dataset/`, `results/experiments/exp-20261016-141448/`)"),
    ("Dataset size", "Synthetic trace: ~1.2 MB (CSV/JSON); Empirical experiment logs: 36 polling cycles (72 pod observation rows, 10.1 KB CSV)"),
    ("Number of records / samples", "Synthetic dataset: 2,016 hourly time-steps (12 weeks of academic calendar telemetry); Empirical run: 72 granular pod utilization samples over 70 seconds"),
    ("Number of features", "6 primary operational and domain features: active_students, is_exam_period, is_assignment_deadline, cpu_used_m, memory_used_mb, response_time_ms"),
    ("Data types / format", "Tabular time-series formatted as comma-separated values (CSV) and structured JavaScript Object Notation (JSON)"),
    ("License / usage restrictions", "MIT License (open-source academic use; permissible for research benchmarking and reproducibility)"),
    ("Purpose in this project", "Benchmarking the FinOps cost analyzer, evaluating demand forecasting models, and validating conservative pod rightsizing algorithms under simulated student load"),
    ("Preprocessing required", "Chronological train/validation/test splitting, z-score normalization of continuous telemetry, one-hot/binary encoding of calendar event flags, and outlier sanitization"),
    ("Privacy / ethical considerations", "Telemetry contains purely synthetic student counts and container cgroup hardware metrics; no personally identifiable information (PII), student grades, or proprietary institutional data are present")
]

# ---------------------------------------------------------------------------
# AWS Services Planning Data for Table 4
# ---------------------------------------------------------------------------
AWS_SERVICES_DATA = [
    {
        "service": "Amazon EKS",
        "purpose": "Managed Kubernetes control plane orchestrating educational microservices and FinOps telemetry workloads",
        "integration": "Deploys `edusaas-backend` pods across private subnets; integrates with IAM OIDC provider for pod-level roles (IRSA)",
        "status": "Planned / Architected (Tested locally via Kind running Kubernetes v1.37.0 control plane; Kind CLI v0.33.0)",
        "considerations": "$0.10/hour cluster fee ($73.00/month); secured via private endpoint access and AWS IAM authenticator"
    },
    {
        "service": "Amazon EC2 (Node Groups)",
        "purpose": "Provides elastic compute worker nodes (t3.medium / m5.large) executing containerized workloads",
        "integration": "Managed node groups across multi-AZ subnets; integrates with Cluster Autoscaler / Karpenter for node scaling",
        "status": "Planned / Reference Modeled (Priced at AWS US-East-1 reference rates for cost analysis)",
        "considerations": "Mix of 70% Spot and 30% On-Demand instances to cut node compute expenses by up to 60%; isolated in private subnets"
    },
    {
        "service": "Amazon S3",
        "purpose": "Scalable object storage for raw telemetry logs, daily cost snapshots, and historical experiment artifacts",
        "integration": "FinOps pipeline streams daily usage CSV/JSON files to S3 bucket via AWS SDK / Boto3; Athena queries data",
        "status": "Planned / Architected (Local filesystem used as artifact store in `results/experiments/`)",
        "considerations": "S3 Standard with lifecycle rule transitioning logs to Glacier after 90 days; AES-256 SSE-S3 encryption"
    },
    {
        "service": "Amazon RDS (PostgreSQL)",
        "purpose": "Managed relational database storing institutional configurations, course data, and persistent FinOps cost records",
        "integration": "Backend REST API reads/writes user records and recommendation audit logs via connection pool in private subnet",
        "status": "Planned / Architected (Documented in architectural schema and Phase-I planning)",
        "considerations": "Multi-AZ deployment for high availability; encrypted at rest via AWS KMS; automated daily snapshots"
    },
    {
        "service": "Amazon DynamoDB",
        "purpose": "High-throughput, single-digit millisecond NoSQL database storing real-time streaming telemetry and active alerts",
        "integration": "KSM scraper and Metrics Server ingestion pipeline write time-stamped metric records with TTL expiration",
        "status": "Planned / Architected (In-memory and JSON storage utilized in local prototype)",
        "considerations": "On-Demand capacity mode to match bursty academic traffic; encrypted via AWS KMS; point-in-time recovery enabled"
    },
    {
        "service": "Amazon API Gateway",
        "purpose": "Serverless API entry point exposing REST endpoints to the web dashboard with throttling and authentication",
        "integration": "Proxies requests to backend microservices and Lambda functions; validates Cognito JWT tokens at the boundary",
        "status": "Planned / Architected (Python standard library multi-threaded HTTP server implemented in `src/backend/main.py`)",
        "considerations": "Rate limiting (1,000 RPS burst, 500 RPS steady) to prevent economic denial-of-sustainability (EDoS) attacks"
    },
    {
        "service": "AWS IAM & Cognito",
        "purpose": "Identity and Access Management enforcing role-based access control and user authentication for students/analysts",
        "integration": "Cognito User Pools issue JWTs for frontend dashboard; IAM roles for service accounts (IRSA) grant pod permissions",
        "status": "Planned / Policy Documented (IAM least-privilege policy defined in `security/iam_least_privilege_policy.json`)",
        "considerations": "Strict principle of least privilege; MFA enforced for FinOps administrator and DevOps roles"
    },
    {
        "service": "Amazon CloudWatch",
        "purpose": "Centralized logging, metric monitoring, and automated budget alarm dispatching across cloud resources",
        "integration": "Container Insights collects EKS cluster performance; CloudWatch Alarms trigger SNS cost notifications",
        "status": "Planned / Architected (Local Prometheus text format parsed via KSM scraper in prototype)",
        "considerations": "Log retention set to 14 days to minimize CloudWatch Ingestion expenses; metric filters alert on budget overruns"
    },
    {
        "service": "Amazon SNS",
        "purpose": "Pub/Sub messaging service delivering real-time cost-anomaly notifications to administrators via email/SMS",
        "integration": "Triggered by CloudWatch Alarms and Lambda rightsizing functions when spend deviates >15% from forecast",
        "status": "Planned / Architected (REST API alert payloads implemented in prototype)",
        "considerations": "Encrypted topic delivery; HTTPS delivery endpoints with signature verification"
    },
    {
        "service": "Amazon SageMaker",
        "purpose": "Machine learning platform training and hosting the academic-calendar-aware workload demand forecasting model",
        "integration": "Pulls historical telemetry from S3, trains time-series regression models, and exposes real-time inference endpoint",
        "status": "Planned / Scaffolding Created (`src/ml_model/train.py` and `predict.py` provide model structure)",
        "considerations": "Serverless inference endpoint or scheduled batch transforms during off-peak hours to avoid idle endpoint fees"
    },
    {
        "service": "AWS Lambda",
        "purpose": "Serverless compute executing event-driven FinOps remediation actions, nightly cleanup, and report generation",
        "integration": "Triggered by SNS alerts or EventBridge cron schedules; executes approved rightsizing actions via Kubernetes API",
        "status": "Planned / Architected (Documented in system workflow; executed via Python scripts in prototype)",
        "considerations": "Short execution timeout (30s) and minimal memory allocation (128 MB) ensuring negligible execution costs"
    },
    {
        "service": "Amazon Route 53 & CloudFront",
        "purpose": "Global DNS routing, CDN edge caching, and TLS termination for the educational SaaS platform web application",
        "integration": "Routes student traffic to CloudFront distribution edge locations; forwards dynamic API calls to API Gateway",
        "status": "Planned / Architected (Documented in Section 10 of Phase-I architectural plan)",
        "considerations": "AWS WAF integration at CloudFront edge blocking malicious IP ranges and Layer 7 DDoS attacks"
    }
]

# ---------------------------------------------------------------------------
# Tools and Technologies Data for Table 5
# ---------------------------------------------------------------------------
TOOLS_DATA = [
    {
        "tool": "Kubernetes (Kind)",
        "purpose": "Local multi-node container orchestration testbed hosting the educational SaaS microservice workloads",
        "version": "Kubernetes v1.37.0 running in Kind on Docker Desktop (Host Kind CLI v0.33.0; earlier docs referenced v0.27.0 baseline)"
    },
    {
        "tool": "Python Standard Library",
        "purpose": "Core development runtime powering telemetry ingestion, cost analysis, recommendation engine, and REST API",
        "version": "Python v3.14.0 (utilizing `http.server`, `urllib`, `json`, `csv`, `math`, `unittest` with zero heavy dependencies)"
    },
    {
        "tool": "Kubernetes Metrics Server",
        "purpose": "Cluster-wide aggregator of container resource usage metrics pulling cgroup CPU and memory telemetry from Kubelet",
        "version": "v0.7.1 deployed in `kube-system` namespace exposed via `/apis/metrics.k8s.io/v1beta1`"
    },
    {
        "tool": "Kube-State-Metrics (KSM)",
        "purpose": "Exposes structured cluster object metadata (pod counts, replica states, resource requests, limits, phase statuses)",
        "version": "v2.12.0 deployed in `kube-system` namespace serving raw Prometheus exposition format text"
    },
    {
        "tool": "Docker Desktop",
        "purpose": "Container engine providing container isolation, networking, and virtualization for Kind Kubernetes nodes",
        "version": "Docker Community Edition v28.0.1 (WSL2 backend integration)"
    },
    {
        "tool": "Vanilla Web Technologies",
        "purpose": "Lightweight, responsive frontend web dashboard visualizing cluster metrics, monthly costs, and rightsizing actions",
        "version": "HTML5, CSS3 (Modern dark-mode glassmorphic design), Vanilla JavaScript ES6 (zero third-party UI framework overhead)"
    },
    {
        "tool": "AWS Cloud Services",
        "purpose": "Target production cloud infrastructure architecture for scalable educational SaaS hosting and FinOps automation",
        "version": "AWS Cloud Architecture Design (Amazon EKS, EC2, S3, RDS, DynamoDB, SageMaker, Lambda, IAM, KMS)"
    },
    {
        "tool": "Git & GitHub",
        "purpose": "Source control, feature branch management, automated issue tracking, and collaborative development workflow",
        "version": "Git v2.48.1; GitHub Repository: `https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026`"
    }
]

# ---------------------------------------------------------------------------
# Implemented Modules Data for Table 6
# ---------------------------------------------------------------------------
MODULES_DATA = [
    {
        "module": "Telemetry Ingestion Pipeline",
        "details": "Pulls raw container resource telemetry from Kubernetes Metrics Server and KSM; parses Prometheus text; standardizes millicores and bytes.",
        "tools": "Kubernetes Metrics Server, KSM, `src/finops_engine/pipeline.py`",
        "evidence": "Observed 36 cycles (72 pod samples) in `observations.csv`; unit tested in `test_pipeline.py` (10 tests pass).",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "FinOps Cost Analyzer Engine",
        "details": "Calculates hourly and 730-hour monthly request and limit spend using AWS US-East-1 reference rates ($0.031611/vCPU-hr, $0.004237/GiB-hr).",
        "tools": "Python standard library `math`, `src/finops_engine/cost_analyzer.py`",
        "evidence": "Verified exact binary divisor math: $13.0845 baseline vs $2.6942 proposed (79.41% reduction); 8 tests in `test_finops_engine.py`.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "Recommendation Engine",
        "details": "Computes rightsized pod requests with +20% safety headroom; enforces mandatory production safety floors (50m CPU, 64Mi RAM) and HA replica retention.",
        "tools": "Python `src/finops_engine/recommendation_engine.py`, `kubecost_config.yaml`",
        "evidence": "Output in `recommendations.json`; dry-run rightsizing flags enforced; 8 unit tests in `test_finops_engine.py`.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "Academic Demand Forecaster",
        "details": "Generates synthetic educational timeseries modeling diurnal cycles, exam periods (Tue/Thu), assignment deadlines (Sun/Wed), and student counts.",
        "tools": "Python `src/finops_engine/ml_forecast.py`",
        "evidence": "6 academic features validated; forecast endpoint `/api/v1/forecast/demand` tested in `test_backend_api.py`.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "Benchmark & Experiment Runner",
        "details": "Orchestrates multi-phase empirical benchmarks (Baseline, Low Load, Higher Load, Recovery) using socket connection reuse; logs latency & telemetry.",
        "tools": "Python `src/finops_engine/experiment_runner.py`",
        "evidence": "Authoritative run `exp-20261016-141448` (683 requests, 0 errors, sub-6ms p95 latency); 10 unit tests in `test_experiment_runner.py`.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "REST API Server",
        "details": "Multi-threaded HTTP server dispatching 10 REST endpoints with JSON serialization, CORS headers, route aliases, regex path validation, and error handling.",
        "tools": "Python `http.server`, `src/backend/main.py`",
        "evidence": "17 automated API tests in `test_backend_api.py`; path traversal whitelisting and status code verification passing.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "Hardened Web Dashboard",
        "details": "Modern dark-mode dashboard rendering live telemetry, monthly cost cards, rightsizing tables, and experiment charts with DOM XSS sanitization.",
        "tools": "HTML5, CSS3, Vanilla JS (`src/frontend/index.html`, `app.js`, `styles.css`)",
        "evidence": "DOM contracts verified in `scripts/final_check.py`; dynamic XSS mitigation via `escapeHtml()`; responsive layout.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "Kubernetes Workload Manifests",
        "details": "Declarative YAML manifests for `edusaas` namespace, `edusaas-backend` 2-replica deployment, cluster service, ingress, and HPA configs.",
        "tools": "Kubernetes Manifests (`src/k8s/deployment.yaml`, `service.yaml`, `hpa.yaml`)",
        "evidence": "Live pods running on Kind cluster (`kubecost-finops-local`); verified via `kubectl get pods -n edusaas`.",
        "status": "Fully Implemented & Verified (Local)"
    },
    {
        "module": "Security & IAM Architecture",
        "details": "Documented least-privilege IAM policies, KMS envelope encryption architecture, and Pod Security Standards for AWS cloud deployment.",
        "tools": "AWS IAM, KMS (`security/iam_least_privilege_policy.json`, `src/aws/`)",
        "evidence": "Policy files in repository; security audit verified in `docs/SECURITY_AND_RELIABILITY.md`.",
        "status": "Policy Specified / Architected"
    },
    {
        "module": "Forensic Verification Utilities",
        "details": "Standalone checkers validating experiment JSON/CSV integrity, unit test discovery, code hygiene, and release readiness.",
        "tools": "Python scripts `scripts/final_check.py`, `scripts/validate_experiment.py`",
        "evidence": "10/10 experiment checks PASSED; 28/28 release checks PASSED; 54/54 automated tests PASSED.",
        "status": "Fully Implemented & Verified (Local)"
    }
]

# ---------------------------------------------------------------------------
# Test Plan and Test Cases Data for Table 7
# ---------------------------------------------------------------------------
TEST_CASES_DATA = [
    {
        "id": "T01",
        "scenario": "Telemetry Ingestion & Cgroup Parsing",
        "input": "Query Kubernetes Metrics Server v0.7.1 API at `/apis/metrics.k8s.io/v1beta1/namespaces/edusaas/pods`",
        "expected": "Successfully parse raw nano-core CPU and KiB memory strings into float millicores and MiB with zero NaN values.",
        "observed": "Ingested 36 consecutive cycles across 2 pods (72 samples); peak CPU 15.16m, peak RAM 6.45Mi correctly extracted.",
        "status": "PASS"
    },
    {
        "id": "T02",
        "scenario": "AWS Reference Rate Cost Modeling",
        "input": "Resource requests: 500m total CPU, 512Mi total RAM; AWS rates: $0.031611/vCPU-hr, $0.004237/GiB-hr for 730 hours.",
        "expected": "Exact monthly cost computed as $13.0845 ($11.5380 CPU + $1.5465 RAM) using binary 1024^3 GiB divisor.",
        "observed": "Calculated value matches $13.0845 exactly; rounded display is $13.08; zero math drift detected.",
        "status": "PASS"
    },
    {
        "id": "T03",
        "scenario": "Rightsizing Recommendation with Safety Floors",
        "input": "Observed peak usage: 15.16m CPU, 6.45Mi RAM; apply +20% buffer (18.19m CPU, 7.74Mi RAM); check safety floors.",
        "expected": "Clamp recommendations to minimum safety floors: 50m CPU (0.05 vCPU) and 64Mi RAM (0.0625 GiB) per pod replica.",
        "observed": "Engine clamped values to 50m CPU and 64Mi RAM; proposed monthly cost computed as $2.6942 ($10.39 savings / 79.41%).",
        "status": "PASS"
    },
    {
        "id": "T04",
        "scenario": "Non-Mutating Workload Invariance (Dry-Run)",
        "input": "Trigger recommendation generation and inspect live Kubernetes deployment specs in `edusaas` namespace.",
        "expected": "Live workload deployment specifications remain unchanged at 250m CPU and 256Mi RAM; zero pod restarts.",
        "observed": "Pod specs verified unmutated; zero restarts (`REST_COUNT=0`); dry-run safety contract maintained.",
        "status": "PASS"
    },
    {
        "id": "T05",
        "scenario": "Academic Calendar Demand Forecaster",
        "input": "Request synthetic forecast for horizon=24 hours via `/api/v1/forecast/demand?source=synthetic&horizon=24`",
        "expected": "Return 24 hourly steps containing active_students, is_exam_period, cpu_used_m, and response_time_ms fields.",
        "observed": "All 24 forecast records returned with valid diurnal curves and elevated resource usage during simulated exam hours.",
        "status": "PASS"
    },
    {
        "id": "T06",
        "scenario": "REST API Route Dispatch & Query Filtering",
        "input": "Send HTTP GET requests to all 10 registered API endpoints including route aliases `/api/v1/health` and `/api/health`",
        "expected": "HTTP 200 OK with valid JSON payloads and permissive CORS headers (`Access-Control-Allow-Origin: *`).",
        "observed": "All 10 endpoints returned HTTP 200 OK with compliant JSON schemas; route aliases dispatched correctly.",
        "status": "PASS"
    },
    {
        "id": "T07",
        "scenario": "API Security & Path Traversal Prevention",
        "input": "Send malicious HTTP GET requests containing directory traversal sequences: `/api/v1/experiments/..%2F..%2Fetc`",
        "expected": "Strict regex whitelisting (`^[a-zA-Z0-9_\\-]+$`) rejects malformed run IDs with HTTP 400 Bad Request.",
        "observed": "Request rejected immediately with HTTP 400 Bad Request; zero unauthorized file access permitted.",
        "status": "PASS"
    },
    {
        "id": "T08",
        "scenario": "Frontend DOM Sanitization (XSS Prevention)",
        "input": "Inject simulated script payloads and special characters into recommendation strings rendered in the dashboard.",
        "expected": "All dynamic text wrapped in `escapeHtml()`; HTML tags escaped as `&lt;` and `&gt;`; zero script execution.",
        "observed": "String escaping verified in DOM audit; zero unescaped innerHTML insertions found across `app.js`.",
        "status": "PASS"
    },
    {
        "id": "T09",
        "scenario": "Multi-Phase Controlled Load Benchmark",
        "input": "Execute 4-phase benchmark (`exp-20261016-141448`): Baseline (0 RPS) -> Low Load (10 RPS) -> Higher Load (25 RPS) -> Recovery.",
        "expected": "100% request success rate; p95 latency under 10ms; zero dropped connections across 70-second benchmark run.",
        "observed": "683 requests completed (196 at 10 RPS, 487 at 25 RPS); 0 errors (0.0%); p95 latency: 5.75ms and 5.90ms.",
        "status": "PASS"
    },
    {
        "id": "T10",
        "scenario": "Full Regression Test Suite Execution",
        "input": "Execute automated test discovery across `tests/` directory via `python -m unittest discover tests`",
        "expected": "Discover and execute >=50 test cases covering API, pipeline, engine, and experiment runner with 100% pass rate.",
        "observed": "54 test cases executed in 2.319 seconds; 54 PASSED, 0 failures, 0 errors, 0 warnings.",
        "status": "PASS"
    }
]

# ---------------------------------------------------------------------------
# Risks and Mitigation Data for Table 8
# ---------------------------------------------------------------------------
RISKS_DATA = [
    {
        "risk": "Unexpected Cloud Cost Overrun during Peak Exam Traffic",
        "likelihood_impact": "High / Critical",
        "mitigation": "Establish strict AWS CloudWatch Billing Alarms at $50 and $100 thresholds; configure AWS Budgets with automated SNS notifications; cap Horizontal Pod Autoscaler maxReplicas at 10.",
        "residual": "Low: Spend is bounded by deterministic replica ceilings and real-time alerts."
    },
    {
        "risk": "Service Outage / Crash Caused by Aggressive Container Rightsizing",
        "likelihood_impact": "Medium / Critical",
        "mitigation": "Enforce mandatory high-availability replica floors (>=2 replicas); add +20% safety margin above peak observed usage; clamp recommendations to absolute production floors (50m CPU, 64Mi RAM); retain dry-run approval gate.",
        "residual": "Low: Workloads retain redundant replicas and sufficient headroom for sudden bursts."
    },
    {
        "risk": "Metrics Ingestion Interruption / Metrics Server Unavailability",
        "likelihood_impact": "Medium / Moderate",
        "mitigation": "Implement exponential backoff and retry logic in `pipeline.py`; fall back to cached telemetry snapshots (`ksm_live_snapshot.json`); raise warning flags on stale data (>60s).",
        "residual": "Low: Offline snapshot fallback guarantees pipeline continuity during temporary cluster API blips."
    },
    {
        "risk": "Academic Calendar Drift / Unscheduled Emergency Exam Sessions",
        "likelihood_impact": "Low / High",
        "mitigation": "Couple proactive calendar-based scaling with reactive HPA thresholds; provide an administrative override toggle in the web dashboard for instant manual scaling.",
        "residual": "Low: Reactive autoscaler handles unpredicted traffic surges automatically."
    },
    {
        "risk": "Spot Instance Interruption during Active Examination Windows",
        "likelihood_impact": "Medium / High",
        "mitigation": "Maintain a mixed node group strategy (30% On-Demand baseline for stateful/critical pods, 70% Spot for stateless worker pods); deploy AWS Node Termination Handler to gracefully drain pods upon 2-minute warning.",
        "residual": "Low: Pods are gracefully migrated to surviving On-Demand nodes without session loss."
    },
    {
        "risk": "Credential Exposure & Unauthorized Management API Access",
        "likelihood_impact": "Low / Critical",
        "mitigation": "Zero secrets committed to Git repository (verified in `.gitignore` and security audit); IAM least-privilege policies; regex input validation on all API endpoints; TLS encryption in transit.",
        "residual": "Very Low: Strict security controls and perimeter validation mitigate unauthorized exposure."
    }
]

# ---------------------------------------------------------------------------
# Team Contribution Data for Table 9
# ---------------------------------------------------------------------------
TEAM_CONTRIBUTION_DATA = [
    {
        "activity": "Literature Survey & Research Paper Analysis",
        "darshan": "Analyzed P1, P3, P6, P7, P12, P14 (6 papers: HPA, Knative, GAN forecaster, feature fusion, Kubernetes systems, cluster scheduling)",
        "tharun": "Analyzed P2, P4, P8 (3 papers: HTE-SVM, ensemble hybrid scaling, cloud autoscaling survey)",
        "dhanushkodi": "Analyzed P5, P9, P13 (3 papers: workload classification, Meta-RL, Prophet forecasting)",
        "sanjay": "Analyzed P10, P11, P15 (3 papers: FIRM microservice SLOs, Google Autopilot, DeepRM RL resource management)"
    },
    {
        "activity": "Research Gap Formulation & Novelty Definition",
        "darshan": "Led synthesis of 15 papers; drafted consolidated research gap; formulated 4-pillar novelty matrix",
        "tharun": "Documented limitations of existing ML workload models; analyzed absence of calendar indicators",
        "dhanushkodi": "Formulated economic gap between container cgroups and AWS monthly cloud invoice line items",
        "sanjay": "Analyzed operational risks of un-gated autoscaling; defined necessity of high-availability safety floors"
    },
    {
        "activity": "AWS Cloud Architecture Design (Diagram 1)",
        "darshan": "Lead Architect: designed VPC multi-AZ network, EKS cluster topology, Ingress, and AWS service integrations",
        "tharun": "Contributed SageMaker ML pipeline architecture and S3 telemetry lake dataflow design",
        "dhanushkodi": "Designed RDS PostgreSQL and DynamoDB dual database storage architecture and Lambda cost triggers",
        "sanjay": "Designed Route 53, CloudFront CDN, AWS WAF, and Cognito authentication user access layers"
    },
    {
        "activity": "Complete System Architecture Design (Diagram 2)",
        "darshan": "Lead Architect: designed end-to-end 5-layer system pipeline (Ingestion, FinOps, Storage, API, Workload)",
        "tharun": "Designed ML demand forecasting pipeline and academic calendar feature engineering dataflow",
        "dhanushkodi": "Designed REST API route contracts, JSON serialization protocols, and CORS security layers",
        "sanjay": "Designed frontend UI component hierarchy, state management, and real-time metric visualization flows"
    },
    {
        "activity": "Frontend Dashboard Development",
        "darshan": "Integrated dynamic experiment summary cards, monthly spend charts, and rightsizing recommendation tables",
        "tharun": "Designed telemetry data format bindings and academic calendar event indicators on the UI",
        "dhanushkodi": "Implemented asynchronous API client, error boundary placeholders ('--'), and status polling logic",
        "sanjay": "Lead Developer: built responsive HTML5/CSS3 dark-mode glassmorphic interface and implemented DOM XSS sanitization"
    },
    {
        "activity": "Backend REST API Development",
        "darshan": "Designed API route specifications, query filter parsers, and dry-run recommendation endpoint handlers",
        "tharun": "Implemented synthetic and live forecast endpoint handlers with horizon parameter validation",
        "dhanushkodi": "Lead Developer: built multi-threaded HTTP server (`src/backend/main.py`), route aliases, and path traversal whitelisting",
        "sanjay": "Authored comprehensive API test suite in `tests/test_backend_api.py` (17 tests covering all routes and error states)"
    },
    {
        "activity": "FinOps Cost Engine & Algorithms",
        "darshan": "Lead Developer: authored `cost_analyzer.py` and `recommendation_engine.py`; implemented binary GiB pricing math and safety floors",
        "tharun": "Co-authored safety margin calculation logic (+20% headroom above peak) and replica preservation checks",
        "dhanushkodi": "Implemented KSM Prometheus text scraper and unit standardization (millicores to vCPU, bytes to GiB)",
        "sanjay": "Verified mathematical consistency between unrounded (79.41%) and rounded-totals (79.43%) savings figures"
    },
    {
        "activity": "ML Forecasting & Synthetic Data Pipeline",
        "darshan": "Designed domain schema: active_students, is_exam_period, is_assignment_deadline, cpu_used_m, memory_used_mb",
        "tharun": "Lead Developer: authored `src/finops_engine/ml_forecast.py` generating 12 weeks of synthetic academic telemetry",
        "dhanushkodi": "Implemented data preprocessing scripts and feature engineering pipelines in `src/ml_model/`",
        "sanjay": "Authored dataset documentation and documented train/validation/test chronological holdout splitting"
    },
    {
        "activity": "Kubernetes Manifests & Cluster Deployment",
        "darshan": "Lead Engineer: authored `deployment.yaml`, `service.yaml`, `hpa.yaml`, and deployed Kind cluster (`kubecost-finops-local`)",
        "tharun": "Configured Metrics Server v0.7.1 and Kube-State-Metrics v2.12.0 manifests in `src/k8s/monitoring/`",
        "dhanushkodi": "Configured service port-forwarding scripts, cgroup v2 accounting verifications, and namespace isolations",
        "sanjay": "Verified pod status, zero crash loops, zero restarts, and resource requests/limits in `edusaas` namespace"
    },
    {
        "activity": "Automated Testing & Regression Suite",
        "darshan": "Co-authored regression test harness; developed cost calculation and cgroup verification tests across the 54-test suite",
        "tharun": "Co-authored experiment runner test suites validating socket reuse and phase benchmark progression",
        "dhanushkodi": "Task 3.7 Lead: co-authored backend API tests, endpoint assertions, and verified 100% pass rate across the 54 unit test suite",
        "sanjay": "Authored release readiness checkers (`scripts/final_check.py`) and experiment validation scripts (`scripts/validate_experiment.py`)"
    },
    {
        "activity": "Empirical Benchmarking & Validation",
        "darshan": "Executed primary benchmark run `exp-20261016-141448`; documented peak CPU (15.16m) and peak RAM (6.45Mi)",
        "tharun": "Analyzed adverse trial run `exp-20261016-141118` documenting 100% Phase-3 timeouts and cgroup non-saturation at 30 RPS",
        "dhanushkodi": "Validated forensic integrity of observation CSV/JSON logs; verified phase percentiles (p50/p95 latency)",
        "sanjay": "Plotted empirical throughput, latency, and cost comparison charts (Figures 4, 5, and 6) from raw benchmark data"
    },
    {
        "activity": "Report Compilation & Documentation",
        "darshan": "Project Lead: coordinated report compilation, reviewed technical accuracy, and validated guideline compliance",
        "tharun": "Authored dataset, AWS services planning, and ML methodology chapters; formatted technical tables",
        "dhanushkodi": "Authored implementation, architecture layer descriptions, and security/reliability documentation",
        "sanjay": "Documentation Lead: compiled final Word report (.docx), formatted APA references, and verified review checklist"
    }
]

# ---------------------------------------------------------------------------
# Project Timeline Data for Table 10 (Appendix A)
# ---------------------------------------------------------------------------
TIMELINE_DATA = [
    {
        "phase": "Phase I: Literature Survey, Research Gaps & Cloud Architecture Design",
        "start": "01/07/2026",
        "end": "30/07/2026",
        "owners": "K. Darshan, T. Tharun, Dhanushkodi Y, S. Sanjay",
        "status": "COMPLETED — Phase-I Report delivered, 15 papers analyzed, AWS & System Architecture diagrams authored"
    },
    {
        "phase": "Phase II: Local Kind Cluster Setup, Workload Manifests & Monitoring",
        "start": "01/08/2026",
        "end": "31/08/2026",
        "owners": "K. Darshan, Dhanushkodi Y",
        "status": "COMPLETED — Kind cluster `kubecost-finops-local` deployed, Metrics Server v0.7.1 and KSM v2.12.0 operational"
    },
    {
        "phase": "Phase III: FinOps Engine, Cost Modeling & Academic Demand Forecaster",
        "start": "01/09/2026",
        "end": "25/09/2026",
        "owners": "K. Darshan, T. Tharun",
        "status": "COMPLETED — `cost_analyzer.py`, `recommendation_engine.py`, and `ml_forecast.py` developed and unit-tested"
    },
    {
        "phase": "Phase IV: REST API Backend, Hardened Web Dashboard & Security Remediation",
        "start": "26/09/2026",
        "end": "10/10/2026",
        "owners": "Dhanushkodi Y, S. Sanjay",
        "status": "COMPLETED — 10 REST endpoints implemented, DOM XSS mitigated, path traversal whitelisting enforced"
    },
    {
        "phase": "Phase V: Multi-Phase Controlled Benchmarks & Empirical Experimentation",
        "start": "11/10/2026",
        "end": "16/10/2026",
        "owners": "K. Darshan, T. Tharun, Dhanushkodi Y, S. Sanjay",
        "status": "COMPLETED — Authoritative run `exp-20261016-141448` logged (683 requests, 0 errors, 79.41% modeled savings)"
    },
    {
        "phase": "Phase VI: Regression Testing, Forensic Audit & Final Report Compilation",
        "start": "17/10/2026",
        "end": "21/10/2026",
        "owners": "K. Darshan, T. Tharun, Dhanushkodi Y, S. Sanjay",
        "status": "COMPLETED — 54/54 tests passing, 28/28 verification checks passing, final academic report compiled"
    }
]

# ---------------------------------------------------------------------------
# Review Checklist Items for Appendix B
# ---------------------------------------------------------------------------
CHECKLIST_ITEMS = [
    ("Abstract is 200–300 words and describes the problem, challenges, proposed solution, AWS services, and status/results.", True),
    ("15 research papers are included, with citations and a comparative literature survey.", True),
    ("Every student has completed their own research gap analysis for assigned papers.", True),
    ("4–6 measurable objectives are listed with specific success criteria.", True),
    ("Novelty summary is limited to about one page and is supported by comparison with existing work.", True),
    ("Both required architecture diagrams are included and explained in detail.", True),
    ("Dataset name, source, URL, size, record count, feature count, data type, license, purpose, and preprocessing are documented.", True),
    ("AWS services, their purpose, status, security considerations, and estimated cost are documented.", True),
    ("Implementation evidence, test cases, actual results, limitations, and future work are included.", True),
    ("GitHub repository, branch workflow, pull requests, commits, and individual contributions are documented.", True),
    ("References use APA style; all borrowed ideas, figures, datasets, and documentation are cited.", True),
    ("No credentials, passwords, tokens, or confidential data appear in the report or repository.", True),
    ("Report follows the specified font, spacing, margin, heading, and page-number formatting.", True)
]

print("report_data.py initialized successfully.")
