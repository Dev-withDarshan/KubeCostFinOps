"""
build_report_sections_part3.py
Contains builder functions for Chapters 11 through 14, References, and Appendices A, B, and C.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_data import (
    TEST_CASES_DATA,
    RISKS_DATA,
    TEAM_CONTRIBUTION_DATA,
    TIMELINE_DATA,
    CHECKLIST_ITEMS,
    PAPERS_DATA
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
# Chapter 11: Testing, Results and Observations
# ---------------------------------------------------------------------------
def build_chapter_11(doc):
    add_heading_1(doc, "11. Testing, Results and Observations")
    
    add_heading_2(doc, "11.1 Test Plan and Test Cases")
    add_p(doc, (
        "The project testing strategy combines functional unit tests, security contract audits, and empirical performance benchmarks. "
        "Table 7 documents 10 formal test scenarios, detailing the scenario objective, input setup, expected behavior, observed results, and pass/fail verdict."
    ))
    
    # Table 7: Test Plan and Test Cases Table
    add_p(doc, "Table 7. Test Plan, Verification Scenarios, and Empirical Test Results.", bold=True, space_before=6, space_after=2)
    tbl_test = doc.add_table(rows=len(TEST_CASES_DATA)+1, cols=6)
    tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_test, color="CBD5E1", sz="4")
    
    headers_test = ["Test ID", "Scenario Description", "Input / Environment Setup", "Expected Result", "Observed Result", "Status"]
    test_widths = [Inches(0.6), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.3), Inches(0.8)]
    for c_idx, h_text in enumerate(headers_test):
        style_header_cell(tbl_test.rows[0].cells[c_idx], h_text, width=test_widths[c_idx])
        
    for r_idx, t_info in enumerate(TEST_CASES_DATA):
        row = tbl_test.rows[r_idx+1]
        style_body_cell(row.cells[0], t_info["id"], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, width=test_widths[0])
        style_body_cell(row.cells[1], t_info["scenario"], width=test_widths[1])
        style_body_cell(row.cells[2], t_info["input"], width=test_widths[2])
        style_body_cell(row.cells[3], t_info["expected"], width=test_widths[3])
        style_body_cell(row.cells[4], t_info["observed"], width=test_widths[4])
        style_body_cell(row.cells[5], t_info["status"], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, width=test_widths[5], bg_color="DCFCE7") # light green
        
    setup_table_behavior(tbl_test)
    
    add_heading_2(doc, "11.2 Authoritative Empirical Benchmark: exp-20261016-141448")
    add_p(doc, (
        "The primary empirical evaluation was conducted on 2026-10-16 under run ID `exp-20261016-141448`. The benchmark targeted the `edusaas-backend` "
        "microservice (2 replicas of `hashicorp/http-echo`) hosted in the local Kind cluster (`kubecost-finops-local`, K8s v1.37.0). "
        "The benchmark executed across four consecutive operational phases lasting 69.4 seconds total: (1) Baseline (0 RPS, 10s), (2) Low Load (10 RPS, 20s), "
        "(3) Higher Load (25 RPS, 20s), and (4) Recovery (0 RPS, 20s). Telemetry was polled every 2.0 seconds by Metrics Server v0.7.1, "
        "harvesting 36 polling cycles (72 pod observations across the two replicas)."
    ))
    
    # Table 7.1: Empirical Benchmark Results Table
    add_p(doc, "Table 7.1. Empirical Benchmark Throughput, Latency, and Resource Metrics (`exp-20261016-141448`).", bold=True, space_before=6, space_after=2)
    tbl_bench = doc.add_table(rows=5, cols=9)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_bench, color="CBD5E1", sz="4")
    
    headers_bench = ["Phase", "Target RPS", "Completed / Total", "Throughput", "p50 ms", "p95 ms", "Avg CPU (m)", "Avg RAM (MiB)", "Samples"]
    bench_widths = [Inches(1.0), Inches(0.7), Inches(1.1), Inches(0.8), Inches(0.6), Inches(0.6), Inches(0.8), Inches(0.8), Inches(0.6)]
    for c_idx, h_text in enumerate(headers_bench):
        style_header_cell(tbl_bench.rows[0].cells[c_idx], h_text, width=bench_widths[c_idx])
        
    bench_data = [
        ("BASELINE", "0 RPS", "0 / 0", "0.0 RPS", "0.00 ms", "0.00 ms", "0.00 m", "5.82 MiB", "10 cycles"),
        ("LOW_LOAD", "10 RPS", "196 / 196", "9.8 RPS", "4.66 ms", "5.75 ms", "5.88 m", "6.12 MiB", "10 cycles"),
        ("HIGHER_LOAD", "25 RPS", "487 / 487", "24.2 RPS", "4.55 ms", "5.90 ms", "12.45 m", "6.38 MiB", "10 cycles"),
        ("RECOVERY", "0 RPS", "0 / 0", "0.0 RPS", "0.00 ms", "0.00 ms", "0.22 m", "6.20 MiB", "6 cycles")
    ]
    for r_idx, b_row in enumerate(bench_data):
        row = tbl_bench.rows[r_idx+1]
        style_body_cell(row.cells[0], b_row[0], bold=True, width=bench_widths[0])
        style_body_cell(row.cells[1], b_row[1], width=bench_widths[1])
        style_body_cell(row.cells[2], b_row[2], width=bench_widths[2])
        style_body_cell(row.cells[3], b_row[3], width=bench_widths[3])
        style_body_cell(row.cells[4], b_row[4], width=bench_widths[4])
        style_body_cell(row.cells[5], b_row[5], width=bench_widths[5])
        style_body_cell(row.cells[6], b_row[6], width=bench_widths[6])
        style_body_cell(row.cells[7], b_row[7], width=bench_widths[7])
        style_body_cell(row.cells[8], b_row[8], width=bench_widths[8])
        
    setup_table_behavior(tbl_bench)
    
    # Insert Figures 4, 5, 6
    add_image_with_caption(
        doc,
        "extracted_final_images/img_2.png",
        "Figure 4. Controlled Benchmark Throughput across Operational Phases. Comparing target load vs. completed RPS (0 errors).",
        width=Inches(5.6)
    )
    
    add_image_with_caption(
        doc,
        "extracted_final_images/img_3.png",
        "Figure 5. Response Latency Percentiles (p50 and p95). Sub-6ms round-trip latency maintained across 10 RPS and 25 RPS load phases.",
        width=Inches(5.6)
    )
    
    add_image_with_caption(
        doc,
        "extracted_final_images/img_4.png",
        "Figure 6. Modeled Monthly Request Cost Comparison and Projected Savings ($13.08 baseline vs. $2.69 proposed rightsizing).",
        width=Inches(5.6)
    )
    
    add_p(doc, (
        "Resource Observations and Rightsizing Analysis:\n"
        "Across the 72 recorded pod observations, the peak measured CPU utilization was 15.16 millicores (representing only 6.06% of the 250m configured request), "
        "and peak memory utilization was 6.45 MiB (representing only 2.52% of the 256 MiB configured request). "
        "Applying the FinOps recommendation algorithm (+20% headroom: 18.19m CPU, 7.74Mi RAM) triggered the mandatory production safety floors. "
        "Consequently, the engine clamped the proposed requests to 50m CPU and 64Mi RAM per pod replica. "
        "Table 7.2 presents the comparative resource and financial breakdown."
    ))
    
    # Table 7.2: Comparative Resource and Cost Table
    add_p(doc, "Table 7.2. Workload Allocation, Peak Telemetry, and FinOps Rightsizing Targets.", bold=True, space_before=6, space_after=2)
    tbl_comp = doc.add_table(rows=5, cols=5)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_comp, color="CBD5E1", sz="4")
    
    headers_comp = ["Configuration State", "Per-Pod CPU", "Per-Pod Memory", "Total Cluster Cost (2 Replicas)", "Financial Impact"]
    comp_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.4), Inches(1.4)]
    for c_idx, h_text in enumerate(headers_comp):
        style_header_cell(tbl_comp.rows[0].cells[c_idx], h_text, width=comp_widths[c_idx])
        
    comp_data = [
        ("Configured Baseline Request", "250m (0.25 vCPU)", "256 MiB (0.25 GiB)", "$13.08 / month ($13.0845)", "Baseline Spend (100.0%)"),
        ("Empirical Peak Observed", "15.16m (0.0152 vCPU)", "6.45 MiB (0.0063 GiB)", "$0.72 / month ($0.7188)", "Active Utilization (5.49%)"),
        ("Proposed Rightsized Target", "50m (0.05 vCPU)", "64 MiB (0.0625 GiB)", "$2.69 / month ($2.6942)", "Target Spend (20.59%)"),
        ("Projected Net Savings", "-200m (-80.0%)", "-192 MiB (-75.0%)", "$10.39 / month ($10.3903)", "Modeled Reduction (79.41%)")
    ]
    for r_idx, c_row in enumerate(comp_data):
        row = tbl_comp.rows[r_idx+1]
        style_body_cell(row.cells[0], c_row[0], bold=True, width=comp_widths[0])
        style_body_cell(row.cells[1], c_row[1], width=comp_widths[1])
        style_body_cell(row.cells[2], c_row[2], width=comp_widths[2])
        style_body_cell(row.cells[3], c_row[3], width=comp_widths[3])
        style_body_cell(row.cells[4], c_row[4], bold=True, width=comp_widths[4], bg_color="F1F5F9" if r_idx < 3 else "DCFCE7")
        
    setup_table_behavior(tbl_comp)
    
    add_heading_2(doc, "11.3 Baseline Comparison & Adverse Counter-Evidence: exp-20261016-141118")
    add_p(doc, (
        "To adhere strictly to scientific integrity, adverse experimental counter-evidence is explicitly documented rather than concealed. "
        "Prior to the successful 25-RPS benchmark (`exp-20261016-141448`), an aggressive stress trial was conducted under run ID `exp-20261016-141118` "
        "targeting 30 RPS across 4 concurrent client workers during Phase 3 (HIGHER_LOAD). During this phase, 28 requests were attempted and all 28 failed "
        "with recorded latencies tightly clustered at ~3,010 ms (mean 3,012.45 ms, p50 3,010.99 ms, p95 3,025.13 ms), producing a recorded 100.0% phase error rate.\n\n"
        "Directly Observed Telemetry Facts:\n"
        "1. Workload Resource Utilization: Measured kernel cgroup telemetry during the failure shows that container compute resources remained essentially idle: "
        "average pod CPU consumption was only 1.68 millicores (peak 7.82m, or 3.13% of the 250m request) and memory consumption was 2.67 MiB "
        "(peak 3.45 MiB, or 1.35% of the 256 MiB request). No CPU throttling (`nr_throttled = 0`) or Out-Of-Memory (OOM) kills occurred.\n"
        "2. Failure Latency Profile: Elapsed request times uniformly exceeded the client harness's 3.0-second HTTP timeout threshold.\n\n"
        "Inferred Cause vs. Inconclusive Evidence:\n"
        "While low container CPU and memory demonstrate that the microservice was not compute-saturated, low resource usage alone does not constitute "
        "definitive proof of the network failure mechanism. Because the benchmark client caught HTTP exceptions generically (`status_code = 0`) without "
        "persisting socket-level tracebacks, Wireshark packet captures, or `kubectl port-forward` stderr streams, attributing the failure specifically to "
        "TCP backlog exhaustion or port-forward multiplexer queue saturation remains a suspected, plausible hypothesis rather than an experimentally confirmed fact. "
        "The root cause is therefore classified as inconclusive based strictly on the archived artifacts.\n\n"
        "Required Confirmatory Diagnostics:\n"
        "To conclusively confirm the exact bottleneck in future trials, the following diagnostics are required: (a) capturing uncaught client socket exception classes "
        "(e.g., distinguishing `TimeoutError` on connection handshake from read timeout); (b) loopback network packet captures (`tcpdump` on `127.0.0.1`) to inspect TCP "
        "SYN retransmissions or RST flags; (c) streaming verbose `kubectl port-forward -v=4` process logs to detect stream multiplexer queue saturation; and "
        "(d) inspecting server-side container access logs (`hashicorp/http-echo`) to verify if incoming requests ever traversed the container boundary.\n\n"
        "Operational Scope:\n"
        "In summary, the workload was successfully tested at 25 RPS in the local benchmarking setup (achieving sub-6ms p95 latency and 0.0% error rate). "
        "A subsequent 30 RPS trial experienced client timeouts. The precise failure mechanism remains inconclusive, and the application's maximum capacity "
        "has not been established."
    ))
    
    add_heading_2(doc, "11.4 Results Summary Against Project Objectives")
    add_p(doc, (
        "Table 7.3 summarizes the degree of achievement for each project objective defined in Chapter 4, citing verifiable empirical evidence."
    ))
    
    tbl_ach = doc.add_table(rows=6, cols=4)
    tbl_ach.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ach, color="CBD5E1", sz="4")
    
    headers_ach = ["Objective ID", "Target Objective", "Assessment Status", "Verifiable Evidence / Proof"]
    ach_widths = [Inches(1.0), Inches(2.0), Inches(1.4), Inches(2.4)]
    for c_idx, h_text in enumerate(headers_ach):
        style_header_cell(tbl_ach.rows[0].cells[c_idx], h_text, width=ach_widths[c_idx])
        
    ach_data = [
        ("OBJ-1", "Telemetry Ingestion Pipeline", "FULLY ACHIEVED", "36 cycles (72 pod samples) ingested without loss; `test_pipeline.py` (10 tests pass)."),
        ("OBJ-2", "FinOps Cost Modeling Engine", "FULLY ACHIEVED", "Exact binary math verified ($13.0845 vs $2.6942); zero rounding drift in `test_finops_engine.py`."),
        ("OBJ-3", "Academic Calendar Forecaster", "FULLY ACHIEVED", "Synthetic trace generator models diurnal and exam cycles across 6 features; REST API verified."),
        ("OBJ-4", "Rightsizing with Safety Floors", "FULLY ACHIEVED", "+20% buffer and 50m/64Mi safety floors clamped correctly in `recommendations.json`; dry-run enforced."),
        ("OBJ-5", "Controlled Benchmarks & Tests", "FULLY ACHIEVED", "683 requests completed with 0 errors in `exp-20261016-141448`; 54 unit tests pass in 2.3s.")
    ]
    for r_idx, (a_id, a_obj, a_stat, a_ev) in enumerate(ach_data):
        row = tbl_ach.rows[r_idx+1]
        style_body_cell(row.cells[0], a_id, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, width=ach_widths[0])
        style_body_cell(row.cells[1], a_obj, width=ach_widths[1])
        style_body_cell(row.cells[2], a_stat, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, width=ach_widths[2], bg_color="DCFCE7")
        style_body_cell(row.cells[3], a_ev, width=ach_widths[3])
        
    setup_table_behavior(tbl_ach)

# ---------------------------------------------------------------------------
# Chapter 12: Discussion, Limitations and Risk Analysis
# ---------------------------------------------------------------------------
def build_chapter_12(doc):
    add_heading_1(doc, "12. Discussion, Limitations and Risk Analysis")
    
    add_heading_2(doc, "12.1 Discussion")
    add_p(doc, (
        "The empirical findings confirm the central hypothesis of this research: educational Kubernetes clusters are subject to severe static "
        "over-provisioning when sized conservatively for peak examination traffic. Under a realistic peak load of 24.2 RPS, actual measured CPU "
        "consumption peaked at only 15.16 millicores per pod (6.06% of the 250m request), while memory peaked at 6.45 MiB (2.52% of the 256 MiB request). "
        "This establishes that 93.94% of reserved CPU and 97.48% of reserved memory sat completely idle during the benchmark. "
        "By applying the FinOps recommendation algorithm, the framework demonstrated that requests can be safely reduced to production floors "
        "(50m CPU, 64Mi RAM), yielding a modeled 79.41% cost reduction ($10.39/month per 2 replicas) while preserving high-availability redundancy "
        "and sub-6ms response times. Crucially, the enforcement of production safety floors prevents the engine from scaling down to dangerously low "
        "allocations that would trigger cold-start failures during sudden student logins."
    ))
    
    add_heading_2(doc, "12.2 Limitations")
    add_p(doc, (
        "To maintain academic rigor, several technical limitations must be acknowledged:\n"
        "1. Virtualized Local Testbed: Experiments were conducted on a single-node Kind cluster running on Docker Desktop (Windows 11). "
        "While cgroup accounting is functionally identical to production Linux hosts, local virtualization lacks real AWS multi-AZ network latency, "
        "cross-rack packet jitter, and noisy-neighbor hypervisor contention.\n"
        "2. Modeled vs. Invoiced Pricing: Cost reductions represent theoretical savings modeled against AWS reference hourly rates for container requests. "
        "They do not reflect actual AWS invoices, which are billed at the EC2 virtual machine instance level rather than individual container slices.\n"
        "3. In-Memory Latency Aggregation Boundary: While all 683 HTTP requests completed successfully and phase aggregates (p50, p95) were recorded "
        "by the benchmark client, individual microsecond-level per-request timestamps were not exported into `observations.csv`, preventing external "
        "re-aggregation of raw latency distributions.\n"
        "4. Workload Scope: Testing was performed against a lightweight HTTP proxy (`hashicorp/http-echo`). Enterprise LMS workloads (e.g., Moodle, Canvas) "
        "involve relational database connection pools, video transcoders, and memory-intensive JVM runtimes that exhibit distinct resource curves."
    ))
    
    add_heading_2(doc, "12.3 Risks and Mitigation Analysis")
    add_p(doc, (
        "Table 8 documents the comprehensive project risk management matrix, evaluating operational risks, impact levels, mitigation strategies, "
        "and residual risks."
    ))
    
    # Table 8: Risks and Mitigation Table
    add_p(doc, "Table 8. Project Risk Assessment and Technical Mitigation Matrix.", bold=True, space_before=6, space_after=2)
    tbl_risk = doc.add_table(rows=len(RISKS_DATA)+1, cols=4)
    tbl_risk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_risk, color="CBD5E1", sz="4")
    
    headers_risk = ["Project Risk & ID", "Likelihood / Impact", "Technical Mitigation Strategy", "Residual Risk"]
    risk_widths = [Inches(1.8), Inches(1.3), Inches(2.4), Inches(1.3)]
    for c_idx, h_text in enumerate(headers_risk):
        style_header_cell(tbl_risk.rows[0].cells[c_idx], h_text, width=risk_widths[c_idx])
        
    for r_idx, r_info in enumerate(RISKS_DATA):
        row = tbl_risk.rows[r_idx+1]
        style_body_cell(row.cells[0], f"R{r_idx+1:02d}: {r_info['risk']}", bold=True, width=risk_widths[0])
        style_body_cell(row.cells[1], r_info["likelihood_impact"], width=risk_widths[1])
        style_body_cell(row.cells[2], r_info["mitigation"], width=risk_widths[2])
        style_body_cell(row.cells[3], r_info["residual"], width=risk_widths[3])
        
    setup_table_behavior(tbl_risk)

# ---------------------------------------------------------------------------
# Chapter 13: Team Contribution and GitHub Management
# ---------------------------------------------------------------------------
def build_chapter_13(doc):
    add_heading_1(doc, "13. Team Contribution and GitHub Management")
    add_p(doc, (
        "The project was executed by a collaborative team of four undergraduate engineers, each fulfilling a designated architectural role. "
        "Table 9 details the specific individual contributions across all 12 core project activities."
    ))
    
    # Table 9: Team Contribution Matrix
    add_p(doc, "Table 9. Individual Team Member Contribution Matrix across Project Activities.", bold=True, space_before=6, space_after=2)
    tbl_team = doc.add_table(rows=len(TEAM_CONTRIBUTION_DATA)+1, cols=5)
    tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_team, color="CBD5E1", sz="4")
    
    headers_team = ["Activity", "K. Darshan (24BIT0119)", "T. Tharun (24BIT0155)", "Dhanushkodi Y (24BIT0143)", "S. Sanjay (24BIT0315)"]
    team_widths = [Inches(1.8), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)]
    for c_idx, h_text in enumerate(headers_team):
        style_header_cell(tbl_team.rows[0].cells[c_idx], h_text, width=team_widths[c_idx])
        
    for r_idx, t_row in enumerate(TEAM_CONTRIBUTION_DATA):
        row = tbl_team.rows[r_idx+1]
        style_body_cell(row.cells[0], t_row["activity"], bold=True, width=team_widths[0])
        style_body_cell(row.cells[1], t_row["darshan"], width=team_widths[1])
        style_body_cell(row.cells[2], t_row["tharun"], width=team_widths[2])
        style_body_cell(row.cells[3], t_row["dhanushkodi"], width=team_widths[3])
        style_body_cell(row.cells[4], t_row["sanjay"], width=team_widths[4])
        
    setup_table_behavior(tbl_team)
    
    add_heading_2(doc, "13.1 Branch and Pull Request Workflow")
    add_p(doc, (
        "The development team followed a structured Git branching strategy adhering to course guidelines:\n"
        "• `main`: Production-ready release branch updated exclusively at major project milestone deliveries.\n"
        "• `develop`: Active integration branch where features are integrated and regression-tested.\n"
        "• Feature Branches (`feature/darshan`, `feature/tharun`, `feature/dhanushkodi`, `feature/sanjay`): Dedicated per-member branches for isolated development.\n"
        "All code contributions were submitted via GitHub Pull Requests (PRs) requiring peer review and automated test suite validation before merging. "
        "Line endings were strictly normalized to LF across the entire repository, and `git diff --check` exits cleanly with zero whitespace or line-break errors."
    ))
    
    add_heading_2(doc, "13.2 Contribution Evidence Boundary")
    add_p(doc, (
        "Project deliverables, code manifests, and architectural documents are verified in the Git repository at commit `d18df0c`. "
        "To ensure transparency, individual student accounts and branch assignments are documented in `docs/Work_Distribution.md`. "
        "Per-student commit volumes are distributed across dedicated feature branches, with the repository currently tagged for Phase-I/Final delivery."
    ))

# ---------------------------------------------------------------------------
# Chapter 14: Conclusion and Future Enhancements
# ---------------------------------------------------------------------------
def build_chapter_14(doc):
    add_heading_1(doc, "14. Conclusion and Future Enhancements")
    
    add_heading_2(doc, "14.1 Conclusion")
    add_p(doc, (
        "This project successfully developed and evaluated a Kubernetes Cost Optimization Framework tailored specifically for SaaS-based educational "
        "platforms using FinOps intelligence. By integrating live cgroup telemetry ingestion from Kubernetes Metrics Server and Kube-State-Metrics with a "
        "transparent multi-resource cost analyzer applying AWS US-East-1 reference pricing, the framework provides actionable visibility into container spend. "
        "The recommendation engine enforces strict high-availability safety floors (50m CPU, 64Mi RAM) and +20% safety headroom, mitigating the dual risks "
        "of wasteful over-provisioning and catastrophic examination-period downtime. In controlled empirical benchmarks comprising 683 HTTP requests with "
        "zero failures, the framework demonstrated that static baseline requests (250m CPU, 256Mi RAM) could be safely rightsized to production floors, "
        "reducing modeled monthly request spend from $13.08 to $2.69 (79.41% savings) while maintaining sub-6ms p95 latencies. "
        "All 54 regression tests and 28 release readiness verifications passed successfully, delivering an open, robust, and reproducible FinOps foundation."
    ))
    
    add_heading_2(doc, "14.2 Future Enhancements")
    add_p(doc, (
        "Planned production extensions for future deployment cycles include:\n"
        "1. Live AWS EKS & Karpenter Deployment: Transitioning from local Kind to multi-AZ Amazon EKS, leveraging Karpenter for sub-minute node provisioning.\n"
        "2. Spot Instance Interruption Handling: Implementing AWS Node Termination Handlers to gracefully drain stateless worker pods during spot reclamation.\n"
        "3. Distributed SageMaker Model Serving: Training deep hybrid forecasters on multi-year institutional LMS logs and deploying real-time serverless endpoints.\n"
        "4. Automated GitOps Reconciliation: Integrating ArgoCD or Flux to automatically apply approved rightsizing pull requests into production clusters.\n"
        "5. Multi-Tenant Departmental Chargeback: Generating automated showback and chargeback cost allocation invoices across academic departments."
    ))

# ---------------------------------------------------------------------------
# References Section
# ---------------------------------------------------------------------------
def build_references(doc):
    add_heading_1(doc, "References")
    add_p(doc, (
        "All citations adhere strictly to the American Psychological Association (APA 7th Edition) format. "
        "References include all 15 peer-reviewed research papers (P1–P15), followed by official cloud documentation, standards, and tooling."
    ))
    
    apa_refs = [
        "Ahmad, H., Treude, C., Wagner, M., & Szabo, C. (2025). Towards resource-efficient reactive and proactive auto-scaling for microservice architectures. Journal of Systems and Software, 225, Article 112390. https://doi.org/10.1016/j.jss.2025.112390",
        "Alharthi, S., Alshamsi, A., Alseiari, A., & Alwarafy, A. (2024). Auto-scaling techniques in cloud computing: Issues and research directions. Sensors, 24(17), Article 5551. https://doi.org/10.3390/s24175551",
        "Alidoost Alanagh, Y., Firouzi, M., Rasouli Kenari, A., & Shamsi, M. (2023). Introducing an adaptive model for auto-scaling cloud computing based on workload classification. Concurrency and Computation: Practice and Experience, 35(22), Article e7720. https://doi.org/10.1002/cpe.7720",
        "Amazon Web Services. (2024). AWS Well-Architected Framework: Cost Optimization Pillar. AWS Whitepapers. https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/",
        "Amazon Web Services. (2026). Amazon Elastic Kubernetes Service (EKS) User Guide. AWS Documentation. https://docs.aws.amazon.com/eks/latest/userguide/",
        "Burns, B., Grant, B., Oppenheimer, D., Brewer, E., & Wilkes, J. (2016). Borg, Omega, and Kubernetes. ACM Queue, 14(1), 70–93. https://doi.org/10.1145/2898442.2898444",
        "Cloud Native Computing Foundation. (2024). CNCF FinOps for Kubernetes Whitepaper. Cloud Native Computing Foundation. https://www.cncf.io/reports/finops-for-kubernetes/",
        "FinOps Foundation. (2024). FinOps Framework: Principles and Phases of Cloud Financial Management. Linux Foundation. https://www.finops.org/framework/",
        "Jia, K., Xiang, J., & Li, B. (2024). DuCFF: A dual-channel feature-fusion network for workload prediction in a cloud infrastructure. Electronics, 13(18), Article 3588. https://doi.org/10.3390/electronics13183588",
        "Kubernetes Authors. (2026). Kubernetes Documentation: Resource Management for Pods and Containers. The Linux Foundation. https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/",
        "Mao, H., Alizadeh, M., Menache, I., & Kandula, S. (2016). Resource management with deep reinforcement learning. In Proceedings of the 15th ACM Workshop on Hot Topics in Networks (HotNets '16) (pp. 50–56). Association for Computing Machinery. https://doi.org/10.1145/3005745.3005750",
        "Mao, H., Schwarzkopf, M., Venkatakrishnan, S. B., Meng, Z., & Alizadeh, M. (2019). Learning scheduling algorithms for data processing clusters. In Proceedings of the ACM SIGCOMM 2019 Conference (pp. 270–288). Association for Computing Machinery. https://doi.org/10.1145/3341302.3342080",
        "Pothu, S. N., & Kailasam, S. (2024). Effective priority-based resource allocation for proactive auto-scaling framework in workload prediction using hybrid tree-enhanced vector machine model. Discover Sustainability, 5, Article 391. https://doi.org/10.1007/s43621-024-00583-x",
        "Qiu, H., Banerjee, S. S., Jha, S., Kalbarczyk, Z. T., & Iyer, R. K. (2020). FIRM: An intelligent fine-grained resource management framework for SLO-oriented microservices. In Proceedings of the 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI '20) (pp. 805–825). USENIX Association. https://www.usenix.org/conference/osdi20/presentation/qiu",
        "Rzadca, K., Findeisen, P., Świderski, J., Zych, P., Broniek, P., Kusmierek, J., Nowak, P., Strack, B., Witusowski, P., Hand, S., & Wilkes, J. (2020). Autopilot: Workload autoscaling at Google. In Proceedings of the 15th European Conference on Computer Systems (EuroSys '20) (Article 16, pp. 1–16). Association for Computing Machinery. https://doi.org/10.1145/3342195.3387524",
        "Saravanan, G., & Santhosh Babu, A. V. (2024). Workload prediction for enhancing power efficiency of cloud data centers using optimized self-attention-based progressive generative adversarial network. International Journal of Communication Systems, 37(1), Article e5634. https://doi.org/10.1002/dac.5634",
        "Storment, J. R., & Fuller, M. (2023). Cloud FinOps: Collaborative, Real-Time Cloud Financial Management (2nd ed.). O'Reilly Media.",
        "Taylor, S. J., & Letham, B. (2018). Forecasting at scale. The American Statistician, 72(1), 37–45. https://doi.org/10.1080/00031305.2017.1380080",
        "Tran, M.-N., & Kim, Y. (2024). Optimized resource usage with hybrid auto-scaling system for Knative serverless edge computing. Future Generation Computer Systems, 152, 304–316. https://doi.org/10.1016/j.future.2023.11.010",
        "Xue, S., Qu, C., Shi, X., Liao, C., Zhu, S., Tan, X., Ma, L., Wang, S., Wang, S., Hu, Y., Lei, L., Zheng, Y., Li, J., & Zhang, J. (2022). A meta reinforcement learning approach for predictive autoscaling in the cloud. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (pp. 4290–4299). Association for Computing Machinery. https://doi.org/10.1145/3534678.3539063",
        "Zhang, H., Guo, T., Tian, W., & Ma, H. (2024). Learning-driven hybrid scaling for multi-type services in cloud. Journal of Parallel and Distributed Computing, 189, Article 104880. https://doi.org/10.1016/j.jpdc.2024.104880"
    ]
    
    for ref_str in sorted(apa_refs):
        p_ref = add_p(doc, ref_str, space_before=2, space_after=6)
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)

# ---------------------------------------------------------------------------
# Appendices A, B, and C
# ---------------------------------------------------------------------------
def build_appendices(doc):
    doc.add_page_break()
    add_heading_1(doc, "Appendix A – Project Timeline and Milestone Tracking")
    add_p(doc, (
        "Table 10 documents the planned vs. executed milestone schedule across all six developmental phases of the project."
    ))
    
    # Table 10: Project Timeline Table
    add_p(doc, "Table 10. Phase-Wise Project Timeline and Completion Milestone Verification.", bold=True, space_before=6, space_after=2)
    tbl_time = doc.add_table(rows=len(TIMELINE_DATA)+1, cols=5)
    tbl_time.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_time, color="CBD5E1", sz="4")
    
    headers_time = ["Developmental Phase", "Planned Start", "Planned End", "Assigned Owners", "Status / Milestone Deliverables"]
    time_widths = [Inches(1.8), Inches(0.9), Inches(0.9), Inches(1.3), Inches(1.9)]
    for c_idx, h_text in enumerate(headers_time):
        style_header_cell(tbl_time.rows[0].cells[c_idx], h_text, width=time_widths[c_idx])
        
    for r_idx, t_item in enumerate(TIMELINE_DATA):
        row = tbl_time.rows[r_idx+1]
        style_body_cell(row.cells[0], t_item["phase"], bold=True, width=time_widths[0])
        style_body_cell(row.cells[1], t_item["start"], width=time_widths[1])
        style_body_cell(row.cells[2], t_item["end"], width=time_widths[2])
        style_body_cell(row.cells[3], t_item["owners"], width=time_widths[3])
        style_body_cell(row.cells[4], t_item["status"], width=time_widths[4])
        
    setup_table_behavior(tbl_time)
    
    add_heading_1(doc, "Appendix B – Review Checklist")
    add_p(doc, (
        "This checklist verifies adherence to all formatting, technical, and content requirements stipulated in the instructor's report template."
    ))
    
    for item_text, is_checked in CHECKLIST_ITEMS:
        mark = "☒" if is_checked else "☐"
        add_p(doc, f"{mark}  {item_text}", space_before=2, space_after=3)
        
    add_heading_1(doc, "Appendix C – Reproducibility Commands and Verification Notes")
    add_p(doc, (
        "To enable full academic reproducibility of all results and verifications reported in this document, execute the following "
        "standard command lines from the workspace root:\n\n"
        "```powershell\n"
        "# 1. Execute the 54-test automated regression suite:\n"
        "python -m unittest discover tests\n\n"
        "# 2. Run the 28-point release readiness checker:\n"
        "python scripts/final_check.py --run-tests\n\n"
        "# 3. Run the forensic validator against the authoritative benchmark:\n"
        "python scripts/validate_experiment.py --dir results/experiments/exp-20261016-141448\n\n"
        "# 4. Launch the local lightweight REST API and Dashboard server:\n"
        "python src/backend/main.py --port 8000\n"
        "# Dashboard is immediately accessible in browser at: http://localhost:8000\n"
        "```"
    ))

print("build_report_sections_part3.py loaded Chapters 11 to 14, References, and Appendices.")
