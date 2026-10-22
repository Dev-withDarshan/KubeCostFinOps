"""
build_report_sections.py
Contains builder functions for Chapters 1 through 5, including Front Matter, Table 0, Table 1, and Table 2.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_data import (
    PROJECT_METADATA,
    PAPERS_DATA,
    NOVELTY_DATA,
    DATASET_ATTRIBUTES,
    AWS_SERVICES_DATA,
    TOOLS_DATA,
    MODULES_DATA,
    TEST_CASES_DATA,
    RISKS_DATA,
    TEAM_CONTRIBUTION_DATA,
    TIMELINE_DATA,
    CHECKLIST_ITEMS
)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), val)
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    tblPr.append(tblBorders)

def style_header_cell(cell, text, width=None):
    set_cell_shading(cell, "1F4E79")
    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    if width:
        cell.width = width

def style_body_cell(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, width=None, bg_color=None):
    if bg_color:
        set_cell_shading(cell, bg_color)
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.0)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor(30, 41, 59)
    if width:
        cell.width = width

def setup_table_behavior(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in table.rows:
        trPr = r._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
    if len(table.rows) > 0:
        table.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))

def add_p(doc, text="", style="Normal", space_before=0, space_after=6, line_spacing=1.5, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph(style="Heading 2")
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(46, 64, 83)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph(style="Heading 3")
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout_box(doc, title, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_shading(c, "F8FAFC")
    set_cell_margins(c, top=100, bottom=100, left=160, right=160)
    tcPr = c._tc.get_or_add_tcPr()
    tblBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24')
    left.set(qn('w:color'), '1F4E79')
    tblBorders.append(left)
    for b in ['top', 'bottom', 'right']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'none')
        tblBorders.append(node)
    tcPr.append(tblBorders)
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(title + "\n")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(10)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(31, 78, 121)
    
    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(51, 65, 85)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def add_image_with_caption(doc, image_path, caption_text, width=Inches(5.8)):
    if not os.path.exists(image_path):
        add_p(doc, f"[Image placeholder: {os.path.basename(image_path)} not found]", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(image_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.font.italic = True
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(71, 85, 105)

# ---------------------------------------------------------------------------
# Section 0: Cover Page, Abstract & TOC
# ---------------------------------------------------------------------------
def build_front_matter(doc):
    # Title / Metadata Page
    add_p(doc, "PROJECT REPORT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=4)
    add_p(doc, "CLOUD ARCHITECTURE DESIGN – AWS CLOUD PROJECT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24)
    
    add_p(doc, "PROJECT TITLE", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=4)
    p_title = add_p(doc, PROJECT_METADATA["title"], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=32)
    p_title.runs[0].font.size = Pt(18)
    p_title.runs[0].font.color.rgb = RGBColor(31, 78, 121)
    
    # Metadata Table
    tbl = doc.add_table(rows=8, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="CBD5E1", sz="4")
    
    meta_rows = [
        ("Submitted by:", "K. DARSHAN (24BIT0119)\nDHANUSHKODI Y (24BIT0143)\nT. THARUN (24BIT0155)\nS. SANJAY (24BIT0315)"),
        ("Programme / Branch / Year:", PROJECT_METADATA["programme"]),
        ("Course Code and Name:", f"{PROJECT_METADATA['course_code']} – {PROJECT_METADATA['course_name']}"),
        ("Institution:", PROJECT_METADATA["institution"]),
        ("Course Instructor / Guide:", PROJECT_METADATA["instructor"]),
        ("Team Number:", PROJECT_METADATA["team_number"]),
        ("GitHub Repository:", PROJECT_METADATA["repository_url"]),
        ("Date of Submission:", PROJECT_METADATA["submission_date"])
    ]
    
    col_widths = [Inches(2.2), Inches(4.3)]
    for idx, (label, val) in enumerate(meta_rows):
        row = tbl.rows[idx]
        style_body_cell(row.cells[0], label, bold=True, width=col_widths[0], bg_color="F1F5F9")
        style_body_cell(row.cells[1], val, bold=False, width=col_widths[1])
    
    setup_table_behavior(tbl)
    doc.add_page_break()
    
    # Abstract
    add_heading_1(doc, "Abstract")
    abstract_text = (
        "Educational software-as-a-service (SaaS) platforms—such as learning management systems, online evaluation portals, "
        "and virtual assessment services—exhibit extreme, calendar-governed traffic fluctuations. Concurrent student requests "
        "surge by one to two orders of magnitude during scheduled examinations and assignment deadlines, while cluster capacity "
        "remains largely idle during off-peak and recess periods. Default Kubernetes cluster configurations rely on static, "
        "conservative resource allocations to avoid out-of-memory crashes or CPU throttling, leading to pervasive cluster "
        "over-provisioning and substantial cloud financial waste. This project develops and evaluates an end-to-end FinOps-informed "
        "Kubernetes cost optimization framework tailored for educational workloads. The framework integrates live container "
        "telemetry ingestion from the Kubernetes Metrics Server and Kube-State-Metrics, a multi-resource cost analyzer modeled "
        "on AWS US-East-1 reference pricing ($0.031611/vCPU-hr, $0.004237/GiB-hr), a domain-specific demand forecasting pipeline "
        "incorporating diurnal and academic calendar event indicators, and a conservative recommendation engine that enforces "
        "high-availability replica retention and strict safety floors (50m CPU, 64Mi RAM). The architecture is designed around "
        "enterprise AWS services, featuring Amazon EKS, EC2 On-Demand/Spot node groups, DynamoDB, RDS PostgreSQL, S3, and event-driven "
        "Lambda functions, secured via IAM least privilege and KMS envelope encryption. In local Kind cluster benchmarking across "
        "683 HTTP requests with zero errors, configured baseline requests (250m CPU, 256Mi RAM per pod) were safely rightsized to "
        "production floors, demonstrating an empirical peak utilization of 15.16 millicores CPU and 6.45 MiB RAM, projecting a "
        "modeled monthly cost reduction from $13.08 to $2.69 (79.41% unrounded savings). Completed local evaluations are formally "
        "distinguished from target AWS production deployments."
    )
    add_p(doc, abstract_text)
    
    add_heading_2(doc, "Keywords")
    add_p(doc, "Kubernetes; FinOps Intelligence; Cloud Cost Optimization; Workload Rightsizing; Demand Forecasting; Educational SaaS Architecture; AWS EKS.")
    
    doc.add_page_break()
    
    # Table of Contents
    add_heading_1(doc, "Table of Contents")
    toc_items = [
        ("1. Introduction", "1.1 Background; 1.2 Problem Statement; 1.3 Motivation & Significance; 1.4 Scope; 1.5 Organisation", "4"),
        ("2. Literature Survey / Related Work", "2.1 Survey of 15 Papers (Table 0); 2.2 Synthesis; 2.3 Individual Research Gaps (Table 1)", "6"),
        ("3. Research Gap Analysis", "3.1 Domain-Specific Gaps; 3.2 Methodological Deficiencies in Existing Autoscaling", "18"),
        ("4. Project Objectives", "4.1 SMART Objectives (1-5); 4.2 Expected Deliverables and Assessment Criteria", "19"),
        ("5. Novelty Summary", "5.1 Central Novelty Statement; 5.2 Novelty Dimension Comparison Matrix (Table 2)", "21"),
        ("6. Proposed System and Architecture", "6.1 Overview; 6.2 AWS Architecture (Fig 1); 6.3 System Architecture (Fig 2); 6.4 Workflow (Fig 3); 6.5 Security", "22"),
        ("7. Dataset Description", "7.1 Academic Workload Telemetry (Table 3); 7.2 Data Preparation & Leakage Control", "28"),
        ("8. AWS Services Planning", "8.1 AWS Services Matrix (Table 4); 8.2 Deployment Design; 8.3 Cost Estimation Breakdown", "29"),
        ("9. Methodology and Implementation Plan", "9.1 Overall Methodology; 9.2 Tools (Table 5); 9.3 Implementation Steps; 9.4 Evaluation Metrics", "33"),
        ("10. Implementation / Development", "10.1 Implemented Modules (Table 6); 10.2 Configuration Evidence; 10.3 GitHub Repository", "36"),
        ("11. Testing, Results and Observations", "11.1 Test Plan (Table 7); 11.2 Controlled Benchmark (Figs 4, 5, 6); 11.3 Adverse Trial; 11.4 Results Summary", "41"),
        ("12. Discussion, Limitations and Risk Analysis", "12.1 Findings Discussion; 12.2 Limitations; 12.3 Risks and Mitigation (Table 8)", "48"),
        ("13. Team Contribution and GitHub Management", "13.1 Team Contribution Matrix (Table 9); 13.2 Git Branch Workflow; 13.3 Contribution Evidence", "50"),
        ("14. Conclusion and Future Enhancements", "14.1 Concluding Verdict; 14.2 Planned AWS Production Enhancements", "52"),
        ("References", "Complete APA Citations for Research Papers (P1-P15), Cloud Documentation & Tooling", "53"),
        ("Appendix A – Project Timeline", "Phase-Wise Execution Milestone Tracking (Table 10)", "57"),
        ("Appendix B – Review Checklist", "Instructor Review Checklist Compliance Verification", "57"),
        ("Appendix C – Reproducibility Notes", "CLI Reproduction Commands & Artifact Inventory", "58")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_items)+1, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc, color="E2E8F0", sz="4")
    
    headers_toc = ["Chapter / Section", "Core Topics Covered", "Page"]
    toc_widths = [Inches(2.5), Inches(3.5), Inches(0.6)]
    for c_idx, h_text in enumerate(headers_toc):
        style_header_cell(tbl_toc.rows[0].cells[c_idx], h_text, width=toc_widths[c_idx])
    
    for r_idx, (ch_title, ch_desc, ch_page) in enumerate(toc_items):
        row = tbl_toc.rows[r_idx+1]
        style_body_cell(row.cells[0], ch_title, bold=True, width=toc_widths[0])
        style_body_cell(row.cells[1], ch_desc, bold=False, width=toc_widths[1])
        style_body_cell(row.cells[2], ch_page, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, width=toc_widths[2])
    
    setup_table_behavior(tbl_toc)
    doc.add_page_break()

# ---------------------------------------------------------------------------
# Chapter 1: Introduction
# ---------------------------------------------------------------------------
def build_chapter_1(doc):
    add_heading_1(doc, "1. Introduction")
    
    add_heading_2(doc, "1.1 Background")
    add_p(doc, (
        "Modern higher educational institutions and commercial educational technology (EdTech) providers rely increasingly "
        "on software-as-a-service (SaaS) architectures to deliver mission-critical learning management systems (LMS), online "
        "examination portals, coding sandbox environments, and distributed digital classrooms. To guarantee elasticity and service "
        "isolation, these platforms are deployed predominantly as containerized microservices orchestrated by Kubernetes (Burns et al., 2016). "
        "In Kubernetes, container resource allocation is governed by declarative 'requests' (which dictate scheduler reservation and node placement) "
        "and 'limits' (which cap kernel cgroup runtime consumption to prevent noisy-neighbor starvation). While these primitives provide "
        "robust operational stability, they fail to bridge the divide between infrastructure reservations and financial economics. "
        "A container resource request guarantees compute headroom on an underlying virtual host, incurring cloud leasing costs regardless "
        "of whether the allocated CPU cycles and memory pages are actively utilized. Consequently, cloud financial operations (FinOps) has "
        "emerged as an essential engineering discipline uniting technology, finance, and operations to establish continuous cost visibility, "
        "accountable attribution, and automated workload rightsizing (FinOps Foundation, 2024)."
    ))
    
    add_heading_2(doc, "1.2 Problem Statement")
    add_p(doc, (
        "Educational SaaS platforms operate under an acute operational contradiction: extreme, time-delimited demand volatility coupled with "
        "a zero-tolerance threshold for service disruption. Workload arrivals are tightly synchronized with the academic calendar; normal instructional "
        "hours produce moderate, predictable API traffic, whereas scheduled mid-semester examinations, finals, and assignment submission deadlines "
        "trigger demand spikes that rise by one to two orders of magnitude within minutes. To prevent catastrophic container out-of-memory (OOM) "
        "terminations or CPU-throttled request timeouts during exams, DevOps engineers systematically configure resource requests at peak-concurrency "
        "ceilings. Because these peak events occupy less than 5% of the operational academic calendar, educational clusters remain severely "
        "over-provisioned for the remaining 95% of the year. Industry studies and empirical research indicate that average enterprise container "
        "utilization rarely exceeds 10–15% of configured requests, resulting in substantial financial waste. Conversely, naive reactive autoscaling "
        "(such as standard Kubernetes HPA) exhibits latency lag during sudden examination bursts, risking severe student disruption. "
        "Therefore, educational institutions require a domain-aware FinOps framework that anticipates calendar events, models AWS cloud costs, "
        "and executes conservative rightsizing with strict safety floors."
    ))
    
    add_heading_2(doc, "1.3 Motivation and Significance")
    add_p(doc, (
        "Public and private educational institutions operate under stringent annual operational budgets, where cloud infrastructure overspending "
        "directly detracts from academic research, faculty hiring, and student scholarship funds. Commercial Kubernetes cost monitoring platforms "
        "(such as proprietary enterprise offerings) are often prohibitively expensive to license and operate as opaque black boxes that hide their "
        "underlying pricing equations. Furthermore, generic cloud autoscalers possess zero contextual awareness of academic calendar schedules, treating "
        "an examination morning identically to an ordinary weekend recess. Developing an open, transparent, and auditable FinOps framework "
        "grounded in Kubernetes telemetry and domain forecasting enables institutions to achieve substantial cloud savings (typically 20% to 40% "
        "across production fleets) while maintaining deterministic performance guarantees and high-availability safety guardrails during critical assessments."
    ))
    
    add_heading_2(doc, "1.4 Scope and Operational Boundaries")
    add_p(doc, (
        "To maintain academic and scientific integrity, this project establishes a clear, auditable distinction between the empirical work "
        "completed within the local Kind testbed prototype and the target architectural design planned for enterprise AWS production deployment."
    ))
    
    # Scope Table
    tbl_scope = doc.add_table(rows=7, cols=3)
    tbl_scope.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_scope, color="CBD5E1", sz="4")
    
    headers_scope = ["Architectural Dimension", "Completed Local Evaluation Scope (Evidenced)", "Planned AWS Production Scope (Architected)"]
    scope_widths = [Inches(1.8), Inches(2.4), Inches(2.4)]
    for c_idx, h_text in enumerate(headers_scope):
        style_header_cell(tbl_scope.rows[0].cells[c_idx], h_text, width=scope_widths[c_idx])
        
    scope_data = [
        ("Container Orchestration", "Local Kind cluster (`kubecost-finops-local`, K8s v1.37.0) on Docker Desktop with 2 workload replicas (`edusaas-backend`).", "Multi-AZ Amazon EKS cluster with managed On-Demand and Spot EC2 worker node groups across private subnets."),
        ("Telemetry Ingestion", "Kubernetes Metrics Server v0.7.1 and Kube-State-Metrics v2.12.0 scraping live Linux cgroups and object states.", "Amazon Managed Service for Prometheus pulling container metrics integrated with OpenCost Helm charts."),
        ("FinOps Engine & Pricing", "Python standard library multi-resource cost analyzer applying AWS US-East-1 reference pricing ($0.031611/vCPU-hr, $0.004237/GiB-hr).", "Real-time AWS Cost Explorer API integration, Cost and Usage Reports (CUR), and multi-tenant department showback."),
        ("Workload Forecasting", "Synthetic educational time-series generator (`ml_forecast.py`) outputting diurnal and exam features across 6 domain fields.", "Production Amazon SageMaker endpoint hosting distributed Prophet/LSTM forecasters retrained on historical LMS data."),
        ("Rightsizing Action Mode", "Non-mutating dry-run rightsizing recommendations with +20% safety buffer and 50m/64Mi safety floors.", "Automated GitOps / ArgoCD deployment reconciliation and event-driven AWS Lambda rightsizing with approval gates."),
        ("Verification & Testing", "54 passing regression unit tests, 10 experiment forensic checks, and 28 release readiness verifications.", "Enterprise chaos engineering (AWS Fault Injection Simulator) and multi-region disaster recovery failover.")
    ]
    for r_idx, (dim, comp, plan) in enumerate(scope_data):
        row = tbl_scope.rows[r_idx+1]
        style_body_cell(row.cells[0], dim, bold=True, width=scope_widths[0])
        style_body_cell(row.cells[1], comp, width=scope_widths[1])
        style_body_cell(row.cells[2], plan, width=scope_widths[2])
    
    setup_table_behavior(tbl_scope)
    
    add_heading_2(doc, "1.5 Report Organisation")
    add_p(doc, (
        "This report is structured into 14 comprehensive chapters following the instructor's submission requirements: "
        "Chapter 2 presents an in-depth literature survey of 15 peer-reviewed papers (P1–P15), comparative synthesis, and individual research gaps. "
        "Chapter 3 consolidates the core research gaps. Chapter 4 establishes specific project objectives and expected outcomes. "
        "Chapter 5 details the novelty claim and multi-dimensional comparison. Chapter 6 illustrates the proposed AWS and Complete System "
        "Architectures, complete with workflow diagrams and security specifications. Chapter 7 describes the workload dataset. "
        "Chapter 8 provides detailed AWS service planning and cost calculations. Chapter 9 outlines the methodology, tools, and evaluation metrics. "
        "Chapter 10 documents the implemented software modules, configuration evidence, and GitHub repository structure. "
        "Chapter 11 details empirical test cases, the authoritative controlled benchmark run, adverse counter-evidence, and results summary. "
        "Chapter 12 provides a critical discussion of limitations and risks. Chapter 13 presents the team contribution matrix and Git workflow. "
        "Chapter 14 concludes the report and identifies future AWS production enhancements, followed by APA References and Appendices A, B, and C."
    ))

# ---------------------------------------------------------------------------
# Chapter 2: Literature Survey / Related Work
# ---------------------------------------------------------------------------
def build_chapter_2(doc):
    add_heading_1(doc, "2. Literature Survey / Related Work")
    add_p(doc, (
        "A rigorous, systematic literature review was conducted covering 15 peer-reviewed research publications published predominantly between "
        "2023 and 2026 across leading venues (IEEE Transactions, ACM SIGCOMM/KDD, Springer, Elsevier, USENIX OSDI, and Scopus-indexed journals), "
        "supplemented by foundational systems papers establishing core Kubernetes and cloud time-series principles. "
        "Table 0 summarizes the 15 surveyed papers, documenting their full citations, problems addressed, methodology, evaluation datasets, and key findings."
    ))
    
    # Table 0: Literature Survey Summary
    add_p(doc, "Table 0. Literature Survey Summary (15 Research Papers Evaluated).", bold=True, space_before=6, space_after=2)
    tbl_lit = doc.add_table(rows=len(PAPERS_DATA)+1, cols=6)
    tbl_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lit, color="CBD5E1", sz="4")
    
    headers_lit = ["ID", "Full Citation & DOI", "Problem Addressed", "Method / Architecture", "Dataset / Evaluation", "Key Findings"]
    lit_widths = [Inches(0.5), Inches(1.8), Inches(1.3), Inches(1.2), Inches(1.0), Inches(1.2)]
    for c_idx, h_text in enumerate(headers_lit):
        style_header_cell(tbl_lit.rows[0].cells[c_idx], h_text, width=lit_widths[c_idx])
        
    for r_idx, p_info in enumerate(PAPERS_DATA):
        row = tbl_lit.rows[r_idx+1]
        style_body_cell(row.cells[0], p_info["id"], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, width=lit_widths[0])
        cit_text = f"{p_info['authors']}. \"{p_info['title']}\". {p_info['venue']}. DOI: {p_info['doi']}"
        style_body_cell(row.cells[1], cit_text, width=lit_widths[1])
        style_body_cell(row.cells[2], p_info["problem"], width=lit_widths[2])
        style_body_cell(row.cells[3], p_info["method"], width=lit_widths[3])
        style_body_cell(row.cells[4], p_info["dataset_eval"], width=lit_widths[4])
        style_body_cell(row.cells[5], p_info["findings"], width=lit_widths[5])
        
    setup_table_behavior(tbl_lit)
    
    add_heading_2(doc, "2.1 Synthesis and Comparison")
    add_p(doc, (
        "Cross-analysis of the surveyed literature reveals distinct research methodologies, architectural assumptions, and trade-offs. "
        "The papers can be synthesized into four primary technological categories:\n\n"
        "1. Reactive vs. Proactive Autoscaling (P1, P2, P3, P8): Standard reactive mechanisms (such as default Kubernetes HPA) scale solely in response "
        "to threshold breaches. As established by Ahmad et al. (P1) and Tran & Kim (P3), reactive scaling introduces unavoidable cold-start latency and "
        "frequently triggers over-compensating oscillations. Proactive mechanisms mitigate these delays by projecting near-term traffic. However, existing "
        "proactive schedulers rely almost exclusively on past hardware metrics rather than external business or institutional context.\n\n"
        "2. Machine Learning and Workload Forecasting (P4, P5, P6, P7, P13): Advanced forecasters employ diverse algorithms, ranging from additive regression "
        "(Prophet in P13) to hybrid SVMs (P2), dual-channel CNN-BiLSTMs (P7), and generative adversarial networks (P6). While deep learning models achieve "
        "impressive error reductions on benchmark traces (e.g., PlanetLab, Alibaba), they introduce prohibitive training overheads and require massive historical "
        "datasets that educational institutions rarely possess. Conversely, lightweight statistical models (P13) provide interpretable, event-conditioned "
        "extrapolations suitable for edge deployment.\n\n"
        "3. Reinforcement Learning for Cluster Scheduling (P9, P10, P14, P15): Seminal works by Mao et al. (P14, P15) and Xue et al. (P9) demonstrate that "
        "neural agents can learn complex job packing and multi-resource allocation directly from experience. Furthermore, FIRM (P10) highlights the importance "
        "of microservice SLO-preservation. However, online RL poses significant operational risks: exploration phases can cause sudden service crashes during "
        "high-stakes examinations, making unconstrained RL unacceptable in production educational environments without hard safety floors.\n\n"
        "4. Container Orchestration & Systems Realities (P11, P12): Google Autopilot (P11) and Borg/Kubernetes systems papers (P12) provide the empirical "
        "bedrock of modern container rightsizing. Autopilot proves that multi-window utilization tracking can safely reclaim over 50% of cluster slack. "
        "However, as Alharthi et al. (P8) observe in their comprehensive survey, less than 15% of existing autoscalers integrate explicit cloud monetary "
        "cost models, and fewer than 5% incorporate academic calendar features."
    ))
    
    add_heading_2(doc, "2.2 Individual Research Gap Analysis")
    add_p(doc, (
        "In accordance with course guidelines, each student team member independently analyzed their assigned research papers to evaluate "
        "existing methods, identify technical advantages and limitations, formulate research gaps in their own words, and propose actionable improvements. "
        "Table 1 presents this comprehensive individual analysis across all four students."
    ))
    
    # Table 1: Individual Research Gap Analysis
    add_p(doc, "Table 1. Individual Research Gap Analysis and Proposed Improvements.", bold=True, space_before=6, space_after=2)
    tbl_gap = doc.add_table(rows=len(PAPERS_DATA)+1, cols=6)
    tbl_gap.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_gap, color="CBD5E1", sz="4")
    
    headers_gap = ["Paper & Student", "Existing Method", "Advantages", "Limitations", "Research Gap Identified by Student", "Possible Improvement"]
    gap_widths = [Inches(1.2), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.3)]
    for c_idx, h_text in enumerate(headers_gap):
        style_header_cell(tbl_gap.rows[0].cells[c_idx], h_text, width=gap_widths[c_idx])
        
    for r_idx, p_info in enumerate(PAPERS_DATA):
        row = tbl_gap.rows[r_idx+1]
        id_stud = f"{p_info['id']} ({p_info['authors'].split(',')[0]})\n[{p_info['student']}]"
        style_body_cell(row.cells[0], id_stud, bold=True, width=gap_widths[0])
        style_body_cell(row.cells[1], p_info["existing_method"], width=gap_widths[1])
        style_body_cell(row.cells[2], p_info["advantages"], width=gap_widths[2])
        style_body_cell(row.cells[3], p_info["limitations"], width=gap_widths[3])
        style_body_cell(row.cells[4], p_info["gap"], width=gap_widths[4])
        style_body_cell(row.cells[5], p_info["improvement"], width=gap_widths[5])
        
    setup_table_behavior(tbl_gap)
    
    add_heading_2(doc, "2.3 Consolidated Research Gap")
    add_p(doc, (
        "Synthesizing the individual gaps across all 15 evaluated papers establishes a singular, consolidated research deficit: "
        "Existing cloud and container management research remains bifurcated between low-level reactive scheduling heuristics (which ignore "
        "cloud financial billing structures) and academic machine-learning algorithms (which optimize synthetic benchmark traces in simulation "
        "without integrating live container telemetry or enforcing high-availability production safety floors). Specifically, no existing open-source "
        "framework bridges the operational gap between Kubernetes Linux cgroup metrics, transparent public cloud pricing models (e.g., AWS EC2 On-Demand/Spot "
        "hourly rates), and domain-specific calendar exogenous factors (e.g., exam periods, assignment deadlines). This project directly addresses "
        "this consolidated gap by building a verifiable, end-to-end FinOps intelligence pipeline that converts real-time cluster telemetry into "
        "financially quantified, safety-clamped rightsizing recommendations tailored for educational SaaS platforms."
    ))

# ---------------------------------------------------------------------------
# Chapter 3: Research Gap Analysis
# ---------------------------------------------------------------------------
def build_chapter_3(doc):
    add_heading_1(doc, "3. Research Gap Analysis")
    add_p(doc, (
        "Building upon the literature survey, this chapter formalizes the four critical technical gaps that hinder effective cloud cost optimization "
        "in educational Kubernetes environments:"
    ))
    
    add_heading_2(doc, "3.1 Gap 1: Inadequate Handling of Cyclical and Bursty Academic Calendars")
    add_p(doc, (
        "Commercial and open-source autoscalers (such as Kubernetes HPA and AWS Auto Scaling) treat incoming traffic as an arbitrary stochastic process. "
        "They compute moving averages or threshold percentages over recent 1- to 5-minute metric windows. In an educational platform, traffic surges "
        "are not random anomalies; they are deterministic, synchronized events dictated by institutional course schedules, exam timetables, and submission "
        "deadlines. Because reactive autoscalers remain unaware of the academic calendar, they begin spinning up additional pod replicas only after latency "
        "has already spiked and students experience timeouts. Conversely, heavy deep learning predictors (such as LSTM or GAN networks in P6 and P7) "
        "fail to adapt quickly when exam schedules shift, requiring expensive model retraining."
    ))
    
    add_heading_2(doc, "3.2 Gap 2: Disconnection between Container Request Schedulers and Cloud Invoices")
    add_p(doc, (
        "Kubernetes schedules workloads based on user-declared 'requests', but cloud providers invoice customers based on provisioned virtual machine instances "
        "(e.g., AWS EC2 hourly rates). Traditional Kubernetes dashboards display CPU millicores and memory megabytes, leaving engineering teams blind "
        "to the dollar consequences of over-provisioning. Existing commercial tools that offer cost allocation (such as Kubecost) frequently require "
        "complex proprietary agents and do not provide an inspectable, deterministic pricing engine that can be audited and verified offline. "
        "There is an acute need for a lightweight, transparent FinOps engine that directly translates container cgroup reservations into exact AWS dollar "
        "line items using verifiable unit formulas."
    ))
    
    add_heading_2(doc, "3.3 Gap 3: Absence of Deterministic High-Availability Safety Floors in Rightsizing")
    add_p(doc, (
        "Existing algorithmic rightsizing solutions (including Google Autopilot in P11 and RL-based scalers in P4 and P10) aim to minimize aggregate "
        "resource slack by aggressively scaling down pod requests to match recent average usage. In an educational SaaS application, over-aggressive "
        "downscaling during off-peak periods can reduce pod allocations to extreme minimums (e.g., 5m CPU, 10Mi RAM). When hundreds of students suddenly "
        "log in simultaneously to access an online exam, these constricted pods experience immediate CPU throttling, socket starvation, or OOM terminations "
        "before horizontal scaling can take effect. Existing frameworks lack mandatory, immutable safety floors that preserve high-availability redundancy "
        "regardless of how low recent utilization drops."
    ))
    
    add_heading_2(doc, "3.4 Gap 4: Lack of Lightweight, Non-Mutating, and Auditable FinOps Pipelines")
    add_p(doc, (
        "Many advanced autoscaling frameworks proposed in academia operate either in pure software simulators (P15) or execute live cluster mutations "
        "without human oversight (P4, P9). In mission-critical higher education IT, un-audited automated mutations are strictly prohibited by governance "
        "policies. Current platforms lack a transparent dry-run recommendation architecture where suggested rightsizing configurations can be "
        "forensically inspected, modeled for savings, and evaluated against safety constraints in an offline dashboard before applying declarative mutations."
    ))

# ---------------------------------------------------------------------------
# Chapter 4: Project Objectives
# ---------------------------------------------------------------------------
def build_chapter_4(doc):
    add_heading_1(doc, "4. Project Objectives")
    add_p(doc, (
        "To systematically address the research gaps identified above, this project defines five specific, measurable, achievable, realistic, "
        "and time-bound (SMART) objectives:"
    ))
    
    objectives_list = [
        ("Objective 1: Telemetry Ingestion Pipeline", 
         "Design and deploy an automated telemetry ingestion pipeline capable of polling Kubernetes Metrics Server and Kube-State-Metrics APIs at 2-second intervals, extracting container cgroup CPU and memory telemetry, and parsing object metadata without third-party agent overhead. Success Criterion: Achieve 100% data ingestion continuity across 30+ consecutive sampling cycles with zero NaN values or unparsed metric strings."),
        ("Objective 2: FinOps Multi-Resource Cost Modeling Engine",
         "Develop an auditable FinOps cost analyzer that translates raw container resource requests and limits into hourly and 730-hour monthly dollar costs using published AWS US-East-1 reference pricing ($0.031611/vCPU-hr, $0.004237/GiB-hr) with exact binary GiB conversions. Success Criterion: Eliminate mathematical rounding drift, ensuring zero discrepancy between component sums and stored totals across all cost allocations."),
        ("Objective 3: Academic Calendar Demand Forecaster",
         "Implement a lightweight demand forecasting pipeline incorporating diurnal circadian curves, examination period flags (Tuesday/Thursday peaks), assignment submission deadlines (Sunday/Wednesday surges), and active student counts across 6 domain fields. Success Criterion: Expose standard REST forecast endpoints responding within <50 ms and demonstrating elevated resource projections during simulated academic exam windows."),
        ("Objective 4: Recommendation Engine with Production Safety Floors",
         "Construct a rule-governed rightsizing recommendation engine that calculates optimized pod configurations with a +20% safety headroom above measured peak usage, enforces mandatory high-availability replica preservation (>=2 replicas), and clamps requests to immutable production safety floors (50m CPU, 64Mi RAM). Success Criterion: Ensure recommendations operate in non-mutating dry-run mode, preserving live cluster workload stability."),
        ("Objective 5: Multi-Phase Controlled Benchmarking & Audit Suite",
         "Execute controlled empirical load benchmarks across distinct operational phases (Baseline, Low Load, Higher Load, Recovery), measuring request throughput, p50/p95 response latencies, and container resource utilization, supported by an automated regression test suite. Success Criterion: Achieve >99.9% request success under normal load, maintain p95 latency <10 ms, and attain a 100% pass rate across >=50 unit test cases.")
    ]
    
    for title, desc in objectives_list:
        add_p(doc, f"• {title}: ", bold=True, space_before=4, space_after=2)
        add_p(doc, desc, space_before=0, space_after=6)
        
    add_heading_2(doc, "4.1 Expected Outcomes and Assessment Criteria")
    add_p(doc, (
        "Table 3.1 outlines the core deliverable outcomes mapped directly to the project objectives, along with their verifiable assessment criteria."
    ))
    
    tbl_out = doc.add_table(rows=6, cols=4)
    tbl_out.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_out, color="CBD5E1", sz="4")
    
    headers_out = ["Objective ID", "Target Deliverable", "Success Metric / Threshold", "Evaluation Method"]
    out_widths = [Inches(1.0), Inches(2.2), Inches(2.0), Inches(1.4)]
    for c_idx, h_text in enumerate(headers_out):
        style_header_cell(tbl_out.rows[0].cells[c_idx], h_text, width=out_widths[c_idx])
        
    out_data = [
        ("OBJ-1", "Telemetry Ingestion Pipeline (`pipeline.py`)", ">=30 polling cycles; 100% parsing success; zero missing samples", "Unit test suite (`test_pipeline.py`) & live Kind cgroup scraping"),
        ("OBJ-2", "FinOps Cost Analyzer (`cost_analyzer.py`)", "Mathematical precision; exact binary GiB divisor ($1024^3$); zero drift", "Unit test suite (`test_finops_engine.py`) & forensic calculation audit"),
        ("OBJ-3", "Academic Forecaster (`ml_forecast.py`)", "6 academic features; horizon forecasting; API response <50 ms", "API integration tests (`test_backend_api.py`) & synthetic trace replay"),
        ("OBJ-4", "Recommendation Engine (`recommendation_engine.py`)", "Safety floors clamped (50m/64Mi); HA replicas preserved; dry-run mode", "Engine unit tests & JSON contract schema validation"),
        ("OBJ-5", "Benchmark Suite & Test Suite (`tests/`, `scripts/`)", ">=50 passing tests (54 achieved); 0 failures; 100% passing checks", "Automated regression runner (`unittest`) & `final_check.py`")
    ]
    for r_idx, (oid, deliv, met, evm) in enumerate(out_data):
        row = tbl_out.rows[r_idx+1]
        style_body_cell(row.cells[0], oid, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, width=out_widths[0])
        style_body_cell(row.cells[1], deliv, width=out_widths[1])
        style_body_cell(row.cells[2], met, width=out_widths[2])
        style_body_cell(row.cells[3], evm, width=out_widths[3])
        
    setup_table_behavior(tbl_out)

# ---------------------------------------------------------------------------
# Chapter 5: Novelty Summary
# ---------------------------------------------------------------------------
def build_chapter_5(doc):
    add_heading_1(doc, "5. Novelty Summary")
    
    add_p(doc, (
        "The central novelty of this project lies in the formulation of a domain-specific, closed-loop FinOps intelligence framework "
        "that bridges the gap between academic calendar temporal structures, Kubernetes cgroup telemetry, and public cloud financial billing models. "
        "Unlike generic autoscalers that react blindly to immediate metric thresholds, the proposed architecture incorporates structured academic event "
        "indicators (examination schedules, deadline surges, student concurrency) to anticipate demand while enforcing immutable production safety floors "
        "(50m CPU, 64Mi RAM) and high-availability replica redundancy. Furthermore, the framework provides an open, fully inspectable cost-modeling engine "
        "that maps container requests directly to AWS reference rates without proprietary agent licensing fees, validating recommendations through "
        "a non-mutating dry-run governance loop. Table 2 details the multi-dimensional comparison between existing approaches and the proposed framework."
    ))
    
    # Table 2: Novelty Dimension Comparison Matrix
    add_p(doc, "Table 2. Novelty Dimension Comparison Matrix.", bold=True, space_before=6, space_after=2)
    tbl_nov = doc.add_table(rows=len(NOVELTY_DATA)+1, cols=4)
    tbl_nov.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_nov, color="CBD5E1", sz="4")
    
    headers_nov = ["Novelty Dimension", "Existing Approach / Limitation", "Proposed Difference", "How Demonstrated / Evidenced"]
    nov_widths = [Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.5)]
    for c_idx, h_text in enumerate(headers_nov):
        style_header_cell(tbl_nov.rows[0].cells[c_idx], h_text, width=nov_widths[c_idx])
        
    for r_idx, n_item in enumerate(NOVELTY_DATA):
        row = tbl_nov.rows[r_idx+1]
        style_body_cell(row.cells[0], n_item["dimension"], bold=True, width=nov_widths[0])
        style_body_cell(row.cells[1], n_item["existing"], width=nov_widths[1])
        style_body_cell(row.cells[2], n_item["proposed"], width=nov_widths[2])
        style_body_cell(row.cells[3], n_item["demonstration"], width=nov_widths[3])
        
    setup_table_behavior(tbl_nov)

print("build_report_sections.py loaded Chapters 1 to 5.")
