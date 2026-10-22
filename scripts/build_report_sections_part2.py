"""
build_report_sections_part2.py
Contains builder functions for Chapters 6 through 10:
Architecture, Dataset, AWS Services Planning, Methodology, and Implementation.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_data import (
    DATASET_ATTRIBUTES,
    AWS_SERVICES_DATA,
    TOOLS_DATA,
    MODULES_DATA
)

from build_report_sections import (
    set_cell_shading,
    set_cell_margins,
    set_table_borders,
    style_header_cell,
    style_body_cell,
    setup_table_behavior,
    add_p,
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_callout_box,
    add_image_with_caption
)

# ---------------------------------------------------------------------------
# Chapter 6: Proposed System and Architecture
# ---------------------------------------------------------------------------
def build_chapter_6(doc):
    add_heading_1(doc, "6. Proposed System and Architecture")
    
    add_heading_2(doc, "6.1 System Overview")
    add_p(doc, (
        "The proposed Kubernetes Cost Optimization Framework operates as a decoupled, multi-tier architectural loop spanning five "
        "interconnected operational planes: (1) Workload & Ingestion Plane, (2) Storage & Telemetry Lake Plane, (3) FinOps Analytics & ML Engine Plane, "
        "(4) API & Visualization Plane, and (5) Execution & Governance Plane. Student and faculty users interact with containerized educational "
        "applications hosted across private worker nodes. The system continuously extracts container cgroup resource utilization, normalizes telemetry, "
        "projects near-term demand based on academic calendar schedules, computes hourly/monthly cloud costs against AWS reference rates, "
        "and generates conservative rightsizing recommendations governed by high-availability safety floors."
    ))
    
    add_heading_2(doc, "6.2 Diagram 1 — AWS Cloud Architecture (Mandatory)")
    add_p(doc, (
        "Figure 1 illustrates the comprehensive AWS Cloud Architecture designed for enterprise-grade SaaS educational hosting. "
        "The architecture is anchored within a multi-Availability Zone (AZ) Virtual Private Cloud (VPC) adhering to AWS Well-Architected Framework best practices."
    ))
    
    # Figure 1: AWS Architecture
    add_image_with_caption(
        doc,
        "architecture/AWS_Architecture.png",
        "Figure 1. Proposed AWS Cloud Architecture. Dashed elements represent target production extensions; solid elements reflect local prototype foundations.",
        width=Inches(5.6)
    )
    
    add_p(doc, (
        "Detailed Component & Dataflow Analysis for Figure 1:\n"
        "• Edge & Perimeter Security Layer: Incoming student and faculty web traffic resolves via Amazon Route 53 with latency-based routing. "
        "Amazon CloudFront provides global CDN caching for static assets, while AWS WAF inspects traffic at the edge, blocking SQL injection, "
        "cross-site scripting, and Layer 7 denial-of-service attempts. TLS 1.3 termination occurs at the edge, forwarding dynamic requests to Amazon API Gateway.\n"
        "• Network Isolation (VPC): The network architecture spans two Availability Zones (AZ-a and AZ-b) partitioned into Public and Private Subnets. "
        "Public subnets host Internet Gateways, NAT Gateways, and Application Load Balancers (ALB). Private subnets host compute nodes and databases, "
        "ensuring zero direct public ingress to container hosts.\n"
        "• Container Orchestration (Amazon EKS): Amazon EKS coordinates microservices across managed EC2 node groups. The worker fleet utilizes a "
        "cost-optimized blend of 30% On-Demand instances (for stateful components) and 70% Spot instances (for stateless microservices), managed via Karpenter.\n"
        "• Persistence & Telemetry Lake: Relational data (courses, enrollments, users) resides in Amazon RDS PostgreSQL configured for Multi-AZ standby replication. "
        "High-frequency operational metrics stream to Amazon DynamoDB for real-time dashboard queries, while raw historical metric logs are archived to "
        "Amazon S3 buckets with S3 Glacier lifecycle transitions after 90 days.\n"
        "• FinOps & Machine Learning Intelligence: Amazon SageMaker ingests historical utilization and academic calendar data from S3 to train demand "
        "forecasting models. AWS Lambda executes automated, event-driven FinOps remediation tasks (e.g., dispatching rightsizing requests, scaling worker pools), "
        "notifying administrators via Amazon SNS."
    ))
    
    add_heading_2(doc, "6.3 Diagram 2 — Complete System Architecture (Mandatory)")
    add_p(doc, (
        "Figure 2 illustrates the Complete System Architecture, detailing the end-to-end data processing workflow from container cgroup telemetry "
        "to the presentation layer and governance controls."
    ))
    
    # Figure 2: Complete System Architecture
    add_image_with_caption(
        doc,
        "architecture/System_Architecture.png",
        "Figure 2. Complete System Architecture. Highlights data ingestion, FinOps analytical processing, storage, dashboard binding, and safety controls.",
        width=Inches(5.6)
    )
    
    add_p(doc, (
        "Detailed Pipeline Workflow Analysis for Figure 2:\n"
        "1. Telemetry Ingestion Layer: Linux kernel cgroup v2 accounting data is gathered by the Kubelet on each node. The Kubernetes Metrics Server "
        "polls these cgroups, exposing CPU millicores and memory bytes via `/apis/metrics.k8s.io/v1beta1`. In parallel, Kube-State-Metrics (KSM) "
        "generates structured object metadata detailing deployment replicas, pod phase statuses, configured resource requests, and limits.\n"
        "2. FinOps Processing Engine: The Python ingestion pipeline (`pipeline.py`) scrapes these metric streams, standardizes units (nanocores to millicores, "
        "bytes to binary MiB/GiB), and feeds them to the Cost Analyzer (`cost_analyzer.py`). The Cost Analyzer models spend using AWS US-East-1 reference "
        "pricing. Simultaneously, the ML Demand Forecaster (`ml_forecast.py`) models diurnal and academic calendar event cycles.\n"
        "3. Recommendation & Safety Layer: The Recommendation Engine (`recommendation_engine.py`) takes measured peak usage, applies a +20% safety margin, "
        "and enforces production safety floors (50m CPU, 64Mi RAM) and high-availability replica counts (>=2). Recommendations are packaged as non-mutating "
        "dry-run JSON specifications.\n"
        "4. API & Visualization Layer: A lightweight multi-threaded HTTP server (`backend/main.py`) exposes REST endpoints. The responsive web dashboard "
        "(`frontend/`) queries the API to render dynamic cost metrics, rightsizing summaries, and benchmark charts with strict DOM sanitization."
    ))
    
    add_heading_2(doc, "6.4 Workflow / Use Cases")
    add_p(doc, (
        "Figure 3 depicts the operational workflow lifecycle governing the FinOps framework across four iterative phases: Monitor, Analyze, Forecast, and Optimize."
    ))
    
    # Figure 3: Workflow Diagram
    add_image_with_caption(
        doc,
        "architecture/Workflow.png",
        "Figure 3. Operational Workflow Lifecycle: Closed-loop FinOps stages from continuous cluster monitoring to human-approved optimization.",
        width=Inches(5.6)
    )
    
    add_p(doc, (
        "Step-by-Step Workflow Walkthrough:\n"
        "• Phase 1 (Continuous Monitoring): Metrics Server and KSM poll active pods at 2-second intervals, aggregating cgroup CPU and memory telemetry.\n"
        "• Phase 2 (Cost & Telemetry Analysis): The Cost Analyzer matches live requests against AWS reference rates, calculating exact baseline spend.\n"
        "• Phase 3 (Demand Forecasting): The forecaster evaluates current calendar status (e.g., active examination window) to determine near-term traffic trends.\n"
        "• Phase 4 (Rightsizing & Governance): The recommendation engine generates safety-clamped configurations, presenting them in the dashboard for analyst review. "
        "Upon approval, declarative manifest updates are pushed through GitOps pipelines."
    ))
    
    add_heading_2(doc, "6.5 Security, Availability and Scalability Design")
    add_p(doc, (
        "The architecture enforces rigorous security, availability, and scalability standards:\n"
        "• Principle of Least Privilege (IAM): Pods utilize IAM Roles for Service Accounts (IRSA), eliminating long-lived credentials inside containers. "
        "Management roles possess scoped permissions restricted to specific namespaces (documented in `security/iam_least_privilege_policy.json`).\n"
        "• Data Encryption: Data in transit is enforced via TLS 1.3 across all communication channels. Data at rest (RDS, DynamoDB, S3) is encrypted "
        "using AWS KMS customer-managed keys (CMK) with automated annual rotation.\n"
        "• Non-Mutating Dry-Run Safety: The local engine operates in strictly non-mutating dry-run mode. Recommendations do not alter live pod specifications "
        "without explicit human authorization, preventing unintended workload disruptions.\n"
        "• High Availability (HA) & Redundancy: Workloads maintain a minimum of 2 replicas spread across multi-AZ subnets, backed by pod anti-affinity rules."
    ))

# ---------------------------------------------------------------------------
# Chapter 7: Dataset Description
# ---------------------------------------------------------------------------
def build_chapter_7(doc):
    add_heading_1(doc, "7. Dataset Description")
    add_p(doc, (
        "To evaluate the FinOps framework under realistic conditions, this project utilizes a dual-component dataset: live empirical container "
        "telemetry harvested from the local Kubernetes testbed, paired with a statistically grounded synthetic educational workload time-series generator "
        "(`ml_forecast.py`) that models 12 weeks of academic calendar activity. Table 3 documents all 11 required dataset attributes."
    ))
    
    # Table 3: Dataset Attribute Table
    add_p(doc, "Table 3. Educational SaaS Workload Dataset Specifications.", bold=True, space_before=6, space_after=2)
    tbl_ds = doc.add_table(rows=len(DATASET_ATTRIBUTES)+1, cols=2)
    tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ds, color="CBD5E1", sz="4")
    
    headers_ds = ["Dataset Attribute", "Verified Specification & Technical Details"]
    ds_widths = [Inches(2.4), Inches(4.2)]
    for c_idx, h_text in enumerate(headers_ds):
        style_header_cell(tbl_ds.rows[0].cells[c_idx], h_text, width=ds_widths[c_idx])
        
    for r_idx, (attr, det) in enumerate(DATASET_ATTRIBUTES):
        row = tbl_ds.rows[r_idx+1]
        style_body_cell(row.cells[0], attr, bold=True, width=ds_widths[0], bg_color="F8FAFC")
        style_body_cell(row.cells[1], det, width=ds_widths[1])
        
    setup_table_behavior(tbl_ds)
    
    add_heading_2(doc, "7.1 Data Preparation Plan and Leakage Control")
    add_p(doc, (
        "Data preparation and machine learning evaluation adhere to strict methodological safeguards:\n"
        "• Chronological Holdout Splitting: Time-series data is partitioned chronologically (70% training, 15% validation, 15% testing) rather than "
        "shuffled randomly. This prevents future temporal information from leaking into past model states.\n"
        "• Normalization & Scaling: Continuous features (active students, CPU millicores, RAM MiB) are standardized via z-score normalization computed "
        "strictly on training splits.\n"
        "• Calendar Indicator Encoding: Temporal indicators (`is_exam_period`, `is_assignment_deadline`) are encoded as binary flags (0 or 1), "
        "enabling both regression forecasters and rule-based scalers to condition resource sizing on institutional events.\n"
        "• Privacy Protection: Telemetry contains exclusively aggregated system metrics and synthetic student concurrency numbers. No personally "
        "identifiable information (PII), student grades, or institutional credentials exist in the dataset or codebase."
    ))

# ---------------------------------------------------------------------------
# Chapter 8: AWS Services Planning
# ---------------------------------------------------------------------------
def build_chapter_8(doc):
    add_heading_1(doc, "8. AWS Services Planning")
    add_p(doc, (
        "The project architecture incorporates 12 specialized AWS services selected to deliver scalable, secure, and cost-efficient cloud hosting. "
        "Table 4 provides the comprehensive planning matrix, documenting each service's purpose, integration dataflow, verification status, "
        "and security/cost considerations."
    ))
    
    # Table 4: AWS Services Planning Matrix
    add_p(doc, "Table 4. AWS Services Planning Matrix and Implementation Status.", bold=True, space_before=6, space_after=2)
    tbl_aws = doc.add_table(rows=len(AWS_SERVICES_DATA)+1, cols=5)
    tbl_aws.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_aws, color="CBD5E1", sz="4")
    
    headers_aws = ["AWS Service", "Purpose in Project", "Input / Output Integration", "Status", "Security & Cost Notes"]
    aws_widths = [Inches(1.2), Inches(1.5), Inches(1.4), Inches(1.2), Inches(1.3)]
    for c_idx, h_text in enumerate(headers_aws):
        style_header_cell(tbl_aws.rows[0].cells[c_idx], h_text, width=aws_widths[c_idx])
        
    for r_idx, s_info in enumerate(AWS_SERVICES_DATA):
        row = tbl_aws.rows[r_idx+1]
        style_body_cell(row.cells[0], s_info["service"], bold=True, width=aws_widths[0])
        style_body_cell(row.cells[1], s_info["purpose"], width=aws_widths[1])
        style_body_cell(row.cells[2], s_info["integration"], width=aws_widths[2])
        style_body_cell(row.cells[3], s_info["status"], width=aws_widths[3])
        style_body_cell(row.cells[4], s_info["considerations"], width=aws_widths[4])
        
    setup_table_behavior(tbl_aws)
    
    add_heading_2(doc, "8.1 AWS Deployment and Network Design")
    add_p(doc, (
        "The production deployment plan specifies a multi-AZ Virtual Private Cloud (VPC) spanning two Availability Zones within the `us-east-1` region. "
        "The CIDR block is allocated as `10.0.0.0/16`, partitioned into:\n"
        "• Public Subnets (`10.0.1.0/24`, `10.0.2.0/24`): Hosting NAT Gateways, Internet Gateways, and Application Load Balancers.\n"
        "• Private Application Subnets (`10.0.10.0/24`, `10.0.20.0/24`): Dedicated to Amazon EKS managed worker nodes with private endpoints only.\n"
        "• Private Database Subnets (`10.0.100.0/24`, `10.0.200.0/24`): Isolated data tier hosting Amazon RDS PostgreSQL and VPC endpoints.\n"
        "Security groups enforce strict ingress boundaries: ALB accepts HTTPS (port 443) from Route 53; EKS worker nodes accept traffic exclusively "
        "from the ALB security group on NodePort ranges; RDS accepts connections solely from worker node security groups on port 5432."
    ))
    
    add_heading_2(doc, "8.2 Cost Estimation Breakdown")
    add_p(doc, (
        "To model financial savings accurately without incurring premature cloud billing during prototyping, the Cost Analyzer applies standard "
        "published AWS US-East-1 on-demand reference pricing rates: $0.031611 per vCPU-hour and $0.004237 per GiB-hour (derived from standard general-purpose "
        "compute instance benchmarks), calculated over an academic month of 730 operational hours. Binary conversions are enforced strictly "
        "(1 vCPU = 1,000 millicores; 1 GiB = 1,024 MiB = $1024^3$ bytes).\n\n"
        "Cost Calculation Walkthrough for 2-Replica Workload:\n"
        "1. Baseline Configured Cost (250m CPU, 256Mi RAM per pod; 500m CPU, 512Mi RAM total across 2 replicas):\n"
        "   • CPU Component: 0.50 vCPU × $0.031611/vCPU-hr × 730 hrs = $11.538015 / month\n"
        "   • Memory Component: 0.50 GiB × $0.004237/GiB-hr × 730 hrs = $1.546505 / month\n"
        "   • Total Baseline Cost: $11.538015 + $1.546505 = $13.084520 / month (Formatted display: $13.08 / month)\n\n"
        "2. Proposed Rightsized Cost (50m CPU, 64Mi RAM per pod safety floor; 100m CPU, 128Mi RAM total across 2 replicas):\n"
        "   • CPU Component: 0.10 vCPU × $0.031611/vCPU-hr × 730 hrs = $2.307603 / month\n"
        "   • Memory Component: 0.125 GiB × $0.004237/GiB-hr × 730 hrs = $0.386626 / month\n"
        "   • Total Rightsized Cost: $2.307603 + $0.386626 = $2.694229 / month (Formatted display: $2.69 / month)\n\n"
        "3. Projected Monthly Savings:\n"
        "   • Absolute Monthly Savings: $13.084520 - $2.694229 = $10.390291 / month (Formatted display: $10.39 / month)\n"
        "   • Percentage Reduction (Unrounded): ($10.390291 / $13.084520) × 100% = 79.4090% (Stored: 79.41%)\n"
        "   • Note on Percentage from Rounded Totals: ($10.39 / $13.08) × 100% = 79.434% (Reported in audit notes to prevent confusion).\n"
        "These figures represent modeled resource request expenses; they are not an active AWS bill or invoice."
    ))

# ---------------------------------------------------------------------------
# Chapter 9: Methodology and Implementation Plan
# ---------------------------------------------------------------------------
def build_chapter_9(doc):
    add_heading_1(doc, "9. Methodology and Implementation Plan")
    
    add_heading_2(doc, "9.1 Overall Methodology")
    add_p(doc, (
        "The project methodology follows an iterative, six-stage engineering lifecycle:\n"
        "1. Requirements Analysis & Domain Modeling: Formulating academic traffic patterns, identifying exam surge dynamics, and defining FinOps objectives.\n"
        "2. Architectural & Security Design: Specifying multi-AZ AWS Cloud Architecture, Complete System Architecture, IAM policies, and safety constraints.\n"
        "3. Local Cluster Prototyping: Deploying Kind Kubernetes cluster with Metrics Server, Kube-State-Metrics, and the educational proxy workload.\n"
        "4. Engine & Dashboard Development: Implementing telemetry scraping, cost calculation math, calendar forecasting, REST APIs, and UI dashboard.\n"
        "5. Controlled Benchmarking & Forensic Verification: Conducting multi-phase load tests, verifying math accuracy, and auditing security.\n"
        "6. AWS Production Roadmap: Documenting infrastructure-as-code manifests and operational runbooks for cloud deployment."
    ))
    
    add_heading_2(doc, "9.2 Tools and Technologies")
    add_p(doc, (
        "Table 5 details the software tools, runtime environments, and architectural technologies utilized throughout the project."
    ))
    
    # Table 5: Tools and Technologies Table
    add_p(doc, "Table 5. Software Tools, Libraries, and Technology Stack.", bold=True, space_before=6, space_after=2)
    tbl_tools = doc.add_table(rows=len(TOOLS_DATA)+1, cols=3)
    tbl_tools.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tools, color="CBD5E1", sz="4")
    
    headers_tools = ["Tool / Technology", "Purpose in Project", "Version / Configuration / Technical Role"]
    tools_widths = [Inches(1.8), Inches(2.6), Inches(2.2)]
    for c_idx, h_text in enumerate(headers_tools):
        style_header_cell(tbl_tools.rows[0].cells[c_idx], h_text, width=tools_widths[c_idx])
        
    for r_idx, t_info in enumerate(TOOLS_DATA):
        row = tbl_tools.rows[r_idx+1]
        style_body_cell(row.cells[0], t_info["tool"], bold=True, width=tools_widths[0])
        style_body_cell(row.cells[1], t_info["purpose"], width=tools_widths[1])
        style_body_cell(row.cells[2], t_info["version"], width=tools_widths[2])
        
    setup_table_behavior(tbl_tools)
    
    add_heading_2(doc, "9.3 Step-by-Step Implementation Plan")
    add_p(doc, (
        "Implementation proceeded across seven discrete developmental milestones:\n"
        "• Step 1 — Cluster Environment: Provisioned Kind cluster (`kubecost-finops-local`) running Kubernetes v1.37.0 on Docker Desktop (Kind CLI v0.33.0); deployed Metrics Server and KSM.\n"
        "• Step 2 — Workload Manifests: Deployed `edusaas-backend` (`hashicorp/http-echo`) 2-replica deployment, cluster service, and HPA configs in `edusaas` namespace.\n"
        "• Step 3 — Telemetry Ingestion Pipeline: Authored `pipeline.py` to poll Metrics Server API and parse KSM Prometheus text metrics.\n"
        "• Step 4 — FinOps Engine & Forecaster: Developed `cost_analyzer.py`, `recommendation_engine.py`, and `ml_forecast.py` in standard Python.\n"
        "• Step 5 — REST API & Dashboard: Implemented `backend/main.py` dispatching 10 routes, and built the glassmorphic dark-mode dashboard (`frontend/`).\n"
        "• Step 6 — Security Remediation: Mitigated path traversal in `/api/v1/experiments/<run_id>` via regex whitelisting and eliminated DOM XSS vulnerabilities.\n"
        "• Step 7 — Controlled Benchmarking & Audit: Executed 4-phase benchmark (`exp-20261016-141448`), ran 54 regression tests, and performed forensic validation."
    ))
    
    add_heading_2(doc, "9.4 Evaluation Metrics")
    add_p(doc, (
        "System performance and optimization efficacy are evaluated using seven quantitative metrics:\n"
        "1. Request Throughput (RPS): Completed successful HTTP requests divided by elapsed phase duration: $RPS = N_{success} / \\Delta t$.\n"
        "2. Response Latency Percentiles (p50, p95 ms): The 50th and 95th percentile request round-trip latencies recorded during benchmark phases.\n"
        "3. CPU Utilization (millicores): Active cgroup kernel CPU consumption polled from Metrics Server, where 1,000 millicores equals 1 full vCPU.\n"
        "4. Memory Utilization (MiB): Active cgroup resident set size (RSS) and working set memory, where 1 MiB equals $1024^2$ bytes.\n"
        "5. Request Error Rate (%): $(N_{failed} / N_{total}) \\times 100\\%$. The target threshold is strictly 0.0% under normal operating conditions.\n"
        "6. Modeled Monthly Cost ($/month): Total projected cloud expense applying AWS reference pricing over 730 operational hours.\n"
        "7. Safety Margin Compliance: Verification that proposed rightsizing maintains a +20% buffer above observed peak usage and does not violate 50m/64Mi floors."
    ))

# ---------------------------------------------------------------------------
# Chapter 10: Implementation / Development
# ---------------------------------------------------------------------------
def build_chapter_10(doc):
    add_heading_1(doc, "10. Implementation / Development")
    
    add_heading_2(doc, "10.1 Implemented Modules")
    add_p(doc, (
        "The project codebase is organized into modular Python standard library packages, Kubernetes manifests, and web frontend components. "
        "Table 6 lists all implemented modules, technical implementation details, associated tools, verified evidence paths, and status."
    ))
    
    # Table 6: Implemented Modules Table
    add_p(doc, "Table 6. Implemented Code Modules and Verification Status.", bold=True, space_before=6, space_after=2)
    tbl_mod = doc.add_table(rows=len(MODULES_DATA)+1, cols=5)
    tbl_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_mod, color="CBD5E1", sz="4")
    
    headers_mod = ["Module", "Implementation Details", "AWS / Tools", "Evidence (Artifact / Commit)", "Status"]
    mod_widths = [Inches(1.3), Inches(1.8), Inches(1.1), Inches(1.3), Inches(1.1)]
    for c_idx, h_text in enumerate(headers_mod):
        style_header_cell(tbl_mod.rows[0].cells[c_idx], h_text, width=mod_widths[c_idx])
        
    for r_idx, m_info in enumerate(MODULES_DATA):
        row = tbl_mod.rows[r_idx+1]
        style_body_cell(row.cells[0], m_info["module"], bold=True, width=mod_widths[0])
        style_body_cell(row.cells[1], m_info["details"], width=mod_widths[1])
        style_body_cell(row.cells[2], m_info["tools"], width=mod_widths[2])
        style_body_cell(row.cells[3], m_info["evidence"], width=mod_widths[3])
        style_body_cell(row.cells[4], m_info["status"], width=mod_widths[4])
        
    setup_table_behavior(tbl_mod)
    
    add_heading_2(doc, "10.2 Configuration Evidence and Terminal Verifications")
    add_p(doc, (
        "Cluster and code health were verified through direct terminal inspections in the local workspace. A full inspection across all cluster "
        "namespaces confirmed zero crashing pods, zero restarts, and zero OOMKilled events:\n"
        "• Pod Status (`kubectl get pods -n edusaas`): Two replicas (`edusaas-backend-7485d55c8f-kq86l` and `edusaas-backend-7485d55c8f-wxtv5`) "
        "running continuously in the `edusaas` namespace with status `Running` and 0 restarts.\n"
        "• Monitoring Infrastructure: Metrics Server v0.7.1 and Kube-State-Metrics v2.12.0 verified healthy in the `kube-system` namespace, "
        "serving metrics via port 8080.\n"
        "• Automated Test Discovery: Executing `python -m unittest discover tests` executed 54 unit and integration tests in 2.319 seconds with "
        "100% pass rate (zero failures, zero errors).\n"
        "• Release Readiness Checker: Executing `python scripts/final_check.py --run-tests` returned a perfect score of 28/28 checks passed with zero warnings.\n"
        "• Forensic Experiment Checker: Executing `python scripts/validate_experiment.py --dir results/experiments/exp-20261016-141448` returned 10/10 checks passed."
    ))
    
    add_heading_2(doc, "10.3 GitHub Repository Structure")
    add_p(doc, (
        "The project repository follows the standard course naming convention (`ProjectName_Cloud_Project_2026`) and is hosted publicly at: "
        "`https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026`. The repository structure is organized cleanly as follows:\n\n"
        "```\n"
        "KubeCostFinOps_Cloud_Project_2026/\n"
        "├── README.md                          # Comprehensive project overview and quickstart guide\n"
        "├── LICENSE                            # MIT open-source academic license\n"
        "├── kind-config.yaml                   # Kind cluster configuration file\n"
        "├── requirements.txt                   # Optional dependencies (Python standard library core)\n"
        "├── architecture/                      # Architectural diagrams (AWS, System, Workflow PNGs)\n"
        "├── docs/                              # Planning, audit, verification, and demo runbooks\n"
        "├── dataset/                           # Raw telemetry schemas and synthetic dataset traces\n"
        "├── monitoring/                        # Prometheus and Grafana configuration manifests\n"
        "├── security/                          # IAM least-privilege policies and KMS encryption notes\n"
        "├── src/                               # Core software source code\n"
        "│   ├── aws/                           # IAM policies and serverless Lambda functions\n"
        "│   ├── backend/                       # Multi-threaded Python REST API server (main.py)\n"
        "│   ├── finops_engine/                 # Cost analyzer, forecaster, pipeline, and recommendation engine\n"
        "│   ├── frontend/                      # Web dashboard interface (index.html, app.js, styles.css)\n"
        "│   ├── k8s/                           # Kubernetes deployments, services, HPA, and ingress\n"
        "│   └── ml_model/                      # Machine learning training and prediction scaffolding\n"
        "├── results/                           # Experiment artifacts (exp-20261016-141448) and validation logs\n"
        "├── scripts/                           # Release checkers, test runners, and docx report generators\n"
        "└── tests/                             # Automated regression test suite (54 test cases)\n"
        "```"
    ))

print("build_report_sections_part2.py loaded Chapters 6 to 10.")
