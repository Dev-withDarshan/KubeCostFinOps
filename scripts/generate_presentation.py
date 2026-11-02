"""
generate_presentation.py - Generates the complete 15-slide PowerPoint deck,
embedded speaker notes, and companion PDF for BCSE355L university evaluation.
"""

import os
import sys
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "1Submission", "PRESENTATION")
EVIDENCE_DIR = os.path.join(WORKSPACE_ROOT, "evidence", "final-presentation")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color Palette
COLOR_BG_DARK = RGBColor(10, 25, 47)       # Navy
COLOR_BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
COLOR_PRIMARY = RGBColor(30, 58, 138)      # Blue 900
COLOR_ACCENT = RGBColor(2, 132, 199)       # Cyan 600
COLOR_SUCCESS = RGBColor(16, 185, 129)     # Emerald 500
COLOR_TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
COLOR_CARD_BG = RGBColor(255, 255, 255)
COLOR_CARD_BORDER = RGBColor(226, 232, 240)

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="BCSE355L CLOUD ARCHITECTURE DESIGN"):
    # Category / Breadcrumb
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.7))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

def add_card(slide, left, top, width, height, title="", border_color=COLOR_CARD_BORDER, bg_color=COLOR_CARD_BG):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    if title:
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.alignment = PP_ALIGN.LEFT
    return shape

def add_speaker_note(slide, note_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = note_text

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title & Team Members
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_BG_DARK)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(4.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_ACCENT
    bar.line.fill.background()

    # Title block
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.text = "BCSE355L -- Cloud Architecture Design | Final University Evaluation"
    p2.font.size = Pt(15)
    p2.font.bold = False
    p2.font.color.rgb = COLOR_ACCENT

    # Details Cards
    c1 = add_card(s1, Inches(1.2), Inches(3.6), Inches(5.2), Inches(2.2), "ACADEMIC INSTITUTION", COLOR_ACCENT, RGBColor(15, 33, 64))
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.add_paragraph()
    p.text = "Vellore Institute of Technology (VIT), Vellore\nSchool of Computer Science and Engineering\nAcademic Year 2026 | Faculty Evaluation Committee"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    c2 = add_card(s1, Inches(6.8), Inches(3.6), Inches(5.4), Inches(2.2), "DEVELOPMENT TEAM & STACK", COLOR_ACCENT, RGBColor(15, 33, 64))
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.add_paragraph()
    p.text = "Team Lead: K. Darshan\nRepository: github.com/Dev-withDarshan/KubeCostFinOps\nStack: Kubernetes, Prometheus, OpenCost, Python FinOps Engine\nStatus: 57/57 Automated Tests Passing | 28/28 Release Checks"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    add_speaker_note(s1, 
        "Good morning respected evaluators and faculty members. Welcome to the final project presentation for BCSE355L Cloud Architecture Design. "
        "Our project is titled 'Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence', led by K. Darshan. "
        "Today, we present an end-to-end, production-verified FinOps engineering solution that directly addresses the persistent cloud resource overprovisioning "
        "and financial waste endemic to educational cloud workloads. The system has been fully implemented, rigorously tested with 57 automated unit and integration tests, "
        "and empirically benchmarked to demonstrate a modeled cost reduction of 69% to 79.4%."
    )

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_BG_LIGHT)
    add_header(s2, "Problem Statement: Cloud Waste in Educational SaaS")

    card_w = Inches(3.6)
    card_h = Inches(5.0)

    p_c1 = add_card(s2, Inches(0.8), Inches(1.5), card_w, card_h, "1. Extreme Load Variance")
    tf = p_c1.text_frame
    tf.word_wrap = True
    bullets1 = [
        "\n• Educational SaaS platforms (Moodle, Canvas, automated code graders) experience extreme diurnal traffic swings.",
        "• Sudden traffic surges occur during assignment submission deadlines and timed semester examinations.",
        "• Prolonged quiescent lulls persist overnight, on weekends, and during academic vacations.",
        "• Ratio between peak burst load and baseline idle traffic often exceeds 10:1."
    ]
    for b in bullets1:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    p_c2 = add_card(s2, Inches(4.8), Inches(1.5), card_w, card_h, "2. Static Overprovisioning")
    tf = p_c2.text_frame
    tf.word_wrap = True
    bullets2 = [
        "\n• DevOps engineers routinely configure Kubernetes resource requests for peak anticipated load to prevent OOMKills.",
        "• In a typical deployment, 500m CPU and 512Mi RAM are statically reserved for containers using under 50m CPU at idle.",
        "• In multi-tenant clusters, requests reserve node capacity that cannot be scheduled by other pods.",
        "• Results in 60% to 80% permanent idle capacity waste charged directly to institutional cloud budgets."
    ]
    for b in bullets2:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    p_c3 = add_card(s2, Inches(8.8), Inches(1.5), card_w, card_h, "3. Traditional Tool Limitations")
    tf = p_c3.text_frame
    tf.word_wrap = True
    bullets3 = [
        "\n• Horizontal Pod Autoscaler (HPA): Scales replica count out, but if individual pod requests are oversized, it multiplies financial waste.",
        "• Vertical Pod Autoscaler (VPA): Evicts and restarts pods to adjust requests, causing disruption and exam session dropouts.",
        "• Commercial SaaS Tools (Kubecost, Cast.ai): Impose heavy agent overhead, closed proprietary licensing, and prohibitive costs.",
        "• Lack of an open, non-disruptive, educational-aware FinOps engine."
    ]
    for b in bullets3:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s2,
        "Slide 2 outlines the foundational problem motivating this project. In educational institutions like VIT, SaaS platforms such as learning management "
        "systems, digital test portals, and automated programming evaluation engines experience extreme load variance. During submission deadlines and exams, "
        "traffic spikes dramatically, followed by prolonged idle troughs overnight. Because downtime during an exam is catastrophic, cloud administrators statically "
        "overprovision Kubernetes container requests to peak numbers. However, Kubernetes requests guarantee scheduling reservations on the underlying VM nodes. "
        "This means universities pay for idle vCPUs and RAM 24/7. Standard autoscalers like HPA multiply this waste by scaling bloated pods, while VPA evicts and restarts "
        "running containers, dropping live student sessions. There is an urgent need for an automated, non-disruptive rightsizing framework."
    )

    # =========================================================================
    # SLIDE 3: Motivation
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_BG_LIGHT)
    add_header(s3, "Motivation: FinOps & Economic Cloud Accountability")

    m1 = add_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.4), "FINANCIAL REALITIES OF ACADEMIC IT")
    tf = m1.text_frame
    tf.word_wrap = True
    for text in [
        "\n• University IT departments operate under fixed, non-elastic annual infrastructure grants.",
        "• Cloud bills (AWS EKS, GCP GKE, Azure AKS) frequently experience unbudgeted overruns due to idle container reservations.",
        "• The FinOps Foundation reports that over 32% of enterprise cloud spend is pure waste, rising to 45% in unmonitored academic clusters."
    ]:
        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    m2 = add_card(s3, Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.4), "THE FINOPS LIFECYCLE PARADIGM")
    tf = m2.text_frame
    tf.word_wrap = True
    for text in [
        "\n• Inform: Provide complete, real-time visibility into container-level resource costs ($/vCPU-hr and $/GB-hr).",
        "• Optimize: Identify idle headroom, rightsize container requests with safety buffers, and project dollar savings.",
        "• Operate: Continuously align infrastructure capacity with pedagogical demand through statistical forecasting."
    ]:
        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    m3 = add_card(s3, Inches(0.8), Inches(4.1), Inches(11.6), Inches(2.4), "ACADEMIC & ARCHITECTURAL CONTRIBUTIONS")
    tf = m3.text_frame
    tf.word_wrap = True
    for text in [
        "\n• Non-Intrusive Telemetry: Scrapes Linux cgroups utilization via Prometheus without requiring proprietary in-container sidecars.",
        "• Mathematically Verifiable Cost Attribution: Grounded in public cloud pricing cards with explicit separation of telemetry vs. billing invoices.",
        "• Non-Disruptive Advisory Mode: Produces production-ready declarative YAML patches without evicting live pods during classroom hours.",
        "• Zero-Dependency Lightweight Control Plane: Lightweight Python core runnable in self-hosted air-gapped university environments."
    ]:
        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s3,
        "Moving to Slide 3, our motivation is rooted in the FinOps movement—bringing financial accountability to the variable spend model of cloud computing. "
        "Academic institutions operate on strict, grant-driven budgets. When cloud invoices arrive with 30-40% unallocated container waste, valuable educational "
        "funding is lost. By implementing the FinOps lifecycle—Inform, Optimize, and Operate—our framework provides container-level visibility, calculates "
        "exact rightsizing targets with a safety buffer, and projects institutional savings. Crucially, our architecture prioritizes non-disruptive advisory "
        "recommendations, meaning it never arbitrarily evicts running student pods."
    )

    # =========================================================================
    # SLIDE 4: Project Objectives
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, COLOR_BG_LIGHT)
    add_header(s4, "Project Objectives & Scope")

    obj_w = Inches(5.6)
    obj_h = Inches(2.4)

    o1 = add_card(s4, Inches(0.8), Inches(1.5), obj_w, obj_h, "1. TELEMETRY & INGESTION")
    tf = o1.text_frame
    tf.word_wrap = True
    for t in [
        "\n• Scrape container CPU (`cpu.stat`) and memory (`memory.current`) cgroups metrics at 15-second intervals.",
        "• Integrate with Prometheus, Kube-State-Metrics, and OpenCost APIs.",
        "• Maintain robust dual-mode operation: live cluster scraping with offline fallback to validated forensic benchmarks."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    o2 = add_card(s4, Inches(6.8), Inches(1.5), obj_w, obj_h, "2. FINOPS COST ENGINE")
    tf = o2.text_frame
    tf.word_wrap = True
    for t in [
        "\n• Model hourly and monthly expenditure using AWS US-East-1 reference pricing ($0.031611/vCPU-hr, $0.004237/GB-hr).",
        "• Attribute costs down to namespace, pod, and container granularities.",
        "• Guarantee strict mathematical traceability without inflated marketing figures."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    o3 = add_card(s4, Inches(0.8), Inches(4.1), obj_w, obj_h, "3. ADVISORY RIGHTSIZING")
    tf = o3.text_frame
    tf.word_wrap = True
    for t in [
        "\n• Compute optimized container requests using peak utilization plus a 20% safety headroom buffer.",
        "• Enforce architectural safety floors (10m CPU, 32Mi RAM) to prevent container starvation.",
        "• Provide zero-downtime declarative recommendation manifests."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    o4 = add_card(s4, Inches(6.8), Inches(4.1), obj_w, obj_h, "4. DEMAND FORECASTING & COCKPIT")
    tf = o4.text_frame
    tf.word_wrap = True
    for t in [
        "\n• Implement Holt's Linear Trend time-series forecasting baseline with 95% confidence intervals.",
        "• Build a responsive, single-pane-of-glass executive cockpit with real-time KPI cards and cost comparison bars.",
        "• Achieve 100% automated test coverage and release compliance."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s4,
        "Slide 4 defines our four primary engineering objectives. Objective 1 was to build a non-intrusive telemetry pipeline interfacing with Prometheus, "
        "KSM, and OpenCost. Objective 2 was to implement an auditable FinOps cost attribution engine based on standard cloud reference rates. Objective 3 "
        "was to construct the rightsizing algorithm, integrating a 20% safety buffer over peak usage and strict safety floors. Finally, Objective 4 was to "
        "implement statistical demand forecasting and deliver a responsive, zero-dependency executive dashboard. All four objectives have been fully implemented "
        "and verified in this release."
    )

    # =========================================================================
    # SLIDE 5: Existing Approaches & Research Gap
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, COLOR_BG_LIGHT)
    add_header(s5, "State of the Art & Research Gap Analysis")

    # Table comparison
    table_shape = s5.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(11.6), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(2.3)
    table.columns[3].width = Inches(2.4)
    table.columns[4].width = Inches(2.4)

    headers = ["Feature / Dimension", "Manual Provisioning", "Kubernetes VPA", "Commercial Tools (Kubecost)", "Our FinOps Framework"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ["Intervention Mode", "Static manual guesses", "Automatic In-Place Eviction", "Agent mutation / advice", "Advisory Declarative YAML"],
        ["Workload Downtime", "Zero (but high waste)", "High (Restarts active pods)", "Low to Medium", "Zero (Completely non-disruptive)"],
        ["Cost Attribution", "None / Spreadsheet estimates", "None (Resource-only focus)", "Proprietary pricing engine", "Open, traceable AWS pricing model"],
        ["Educational Focus", "None", "None (Generic)", "Enterprise commercial tier", "Tailored to academic surge cycles"]
    ]

    for row_idx, row_data in enumerate(data):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if (row_idx % 2 == 0) else COLOR_BG_LIGHT
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_DARK
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = COLOR_PRIMARY

    add_speaker_note(s5,
        "On Slide 5, we compare our work against the state of the art across four dimensions. Manual provisioning prevents crashes but locks in massive financial "
        "waste. Kubernetes native VPA provides resource recommendations, but its active actuation mode forcibly evicts running pods, causing catastrophic downtime "
        "during active university examinations. Enterprise commercial tools like Kubecost and Cast.ai offer robust capabilities but require expensive licenses, "
        "heavy agent installations, and external SaaS connectivity. Our framework fills this research gap: an open, non-disruptive, zero-dependency advisory engine "
        "specifically modeled for the surge-and-trough dynamics of educational computing."
    )

    # =========================================================================
    # SLIDE 6: Proposed Architecture
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, COLOR_BG_LIGHT)
    add_header(s6, "Proposed 3-Tier System Architecture")

    # 3 Architecture Tier Cards
    t_w = Inches(3.6)
    t_h = Inches(5.0)

    t1 = add_card(s6, Inches(0.8), Inches(1.5), t_w, t_h, "TIER 1: TELEMETRY & INGESTION")
    tf = t1.text_frame; tf.word_wrap = True
    for item in [
        "\n[Kubernetes Cluster / Kind / EKS]",
        "  • Pods running educational microservices",
        "  • cgroups Linux kernel accounting",
        "\n[Telemetry Agents]",
        "  • Kubelet Summary API (/stats/summary)",
        "  • Kube-State-Metrics (KSM, port 8080)",
        "  • Prometheus Server (port 9090)",
        "  • OpenCost allocation engine (port 9003)",
        "\n[Ingestion Gateway]",
        "  • 15s scrape interval",
        "  • Dual-mode fallback adapter"
    ]:
        p = tf.add_paragraph(); p.text = item; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    t2 = add_card(s6, Inches(4.8), Inches(1.5), t_w, t_h, "TIER 2: FINOPS ANALYTICAL ENGINE")
    tf = t2.text_frame; tf.word_wrap = True
    for item in [
        "\n[Cost Attribution Module]",
        "  • Reference card pricing matrix",
        "  • $0.031611/vCPU-hr | $0.004237/GB-hr",
        "  • Monthly projections (730 hrs)",
        "\n[Advisory Rightsizer]",
        "  • Peak utilization extraction",
        "  • 20% safety headroom buffer",
        "  • Safety floors (10m CPU, 32Mi RAM)",
        "\n[Forecasting Engine]",
        "  • Holt's Linear Trend model",
        "  • 95% Confidence Intervals",
        "  • Extensible SageMaker ML schema"
    ]:
        p = tf.add_paragraph(); p.text = item; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    t3 = add_card(s6, Inches(8.8), Inches(1.5), t_w, t_h, "TIER 3: PRESENTATION & COCKPIT")
    tf = t3.text_frame; tf.word_wrap = True
    for item in [
        "\n[REST API Service]",
        "  • Python Standard Library Server",
        "  • /api/health & /api/ready",
        "  • /api/v1/costs/summary",
        "  • /api/v1/recommendations",
        "  • /api/v1/monitoring/status",
        "\n[Executive Web Dashboard]",
        "  • Vanilla ES6 + Responsive CSS3",
        "  • 6 Real-time KPI Cards",
        "  • Baseline vs Rightsized bar",
        "  • Benchmark run selector",
        "  • Zero external CDN dependencies"
    ]:
        p = tf.add_paragraph(); p.text = item; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s6,
        "Slide 6 illustrates our 3-Tier System Architecture. Tier 1 handles Telemetry Ingestion. At the cluster level, Prometheus and Kube-State-Metrics collect "
        "raw kernel cgroups metrics without requiring invasive code changes inside application containers. Tier 2 is the core FinOps Analytical Engine, "
        "containing our cost attribution calculator, advisory rightsizing engine, and Holt's Linear Trend forecasting module. Tier 3 is the Presentation Cockpit, "
        "consisting of a zero-dependency Python REST backend and a responsive Vanilla JavaScript dashboard. The entire pipeline operates decoupled, ensuring "
        "high availability even when cloud connectivity fluctuates."
    )

    # =========================================================================
    # SLIDE 7: Technology Stack
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, COLOR_BG_LIGHT)
    add_header(s7, "Technology Stack & Infrastructure Specifications")

    col_w = Inches(5.6)
    col_h = Inches(2.4)

    c1 = add_card(s7, Inches(0.8), Inches(1.5), col_w, col_h, "CONTAINER & CLOUD ORCHESTRATION")
    tf = c1.text_frame; tf.word_wrap = True
    for t in [
        "\n• Kubernetes (v1.28+ / Kind / AWS EKS): Container runtime and workload management.",
        "• AWS CloudFormation: Production infrastructure template defining 15 declarative resources (VPC, subnets, EKS cluster, managed node group, IAM roles).",
        "• Cost-Optimized Network: Zero-NAT Gateway design using public subnets to eliminate unnecessary $0.045/hr AWS NAT charges during evaluations."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    c2 = add_card(s7, Inches(6.8), Inches(1.5), col_w, col_h, "TELEMETRY & MONITORING STACK")
    tf = c2.text_frame; tf.word_wrap = True
    for t in [
        "\n• Prometheus: Time-series database scraping cgroups metrics every 15s via exposition format.",
        "• Kube-State-Metrics (KSM): Emits declarative state metrics (pod limits, requests, status).",
        "• OpenCost: Cloud-native pricing engine mapping Kubernetes allocation vectors to hourly costs.",
        "• Health Matrix: Automated HTTP probing across ports 9090, 8080, and 9003."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    c3 = add_card(s7, Inches(0.8), Inches(4.1), col_w, col_h, "ANALYTICAL ENGINE & BACKEND")
    tf = c3.text_frame; tf.word_wrap = True
    for t in [
        "\n• Python 3.14 + Standard Library: Built-in `http.server` eliminating heavyweight external runtime dependencies like Gunicorn/FastAPI for maximum portability.",
        "• Numerical Computing: NumPy, SciPy, and Pandas for statistical rolling windows and trend decomposition.",
        "• Automated Test Harness: `unittest` suite with 57 automated tests and full HTTP lifecycle mocking."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    c4 = add_card(s7, Inches(6.8), Inches(4.1), col_w, col_h, "EXECUTIVE COCKPIT & FRONTEND")
    tf = c4.text_frame; tf.word_wrap = True
    for t in [
        "\n• Vanilla HTML5, Modern CSS3, ES6 JavaScript: Zero CDN dependencies, 100% air-gapped and responsive.",
        "• Client-side State: Asynchronous REST polling, dynamic metric computation, and SVG chart rendering.",
        "• Operational Transparency: Explicit badges distinguishing live telemetry from historical forensic benchmark runs."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s7,
        "Slide 7 details our technical stack. For cloud infrastructure, we engineered an AWS CloudFormation template with 15 declarative resources, featuring "
        "a zero-NAT gateway design to eliminate idle AWS network fees during evaluation. For telemetry, we leverage industry-standard Prometheus, Kube-State-Metrics, "
        "and OpenCost. Our backend is engineered in Python 3 using clean standard library HTTP architecture, ensuring that it runs reliably anywhere without complex "
        "binary compilation. The frontend is built with pure ES6 JavaScript and CSS, requiring no external CDN access and rendering the full dashboard in under 1 second."
    )

    # =========================================================================
    # SLIDE 8: FinOps Engine & Cost Attribution
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, COLOR_BG_LIGHT)
    add_header(s8, "FinOps Engine: Mathematical Cost Attribution Model")

    # Formula Card
    f_card = add_card(s8, Inches(0.8), Inches(1.5), Inches(11.6), Inches(2.2), "MATHEMATICAL FORMULATION & AWS REFERENCE PRICING")
    tf = f_card.text_frame; tf.word_wrap = True
    formulas = [
        "\n• Hourly Container Cost Formulation:",
        "    C_hourly = ( R_cpu * P_cpu ) + ( R_ram * P_ram )",
        "  Where R_cpu = Allocated vCPU cores, R_ram = Allocated Memory in GB.",
        "• AWS US-East-1 Reference Price Card (t3.medium compute blend):",
        "    P_cpu = $0.031611 per vCPU-hour  |  P_ram = $0.004237 per GB-hour",
        "• Monthly Expenditure Projection (FinOps standard 730 accounting hours/month):",
        "    C_monthly = C_hourly * 730 hours"
    ]
    for text in formulas:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    # Attribution Breakdown Cards
    b1 = add_card(s8, Inches(0.8), Inches(3.9), Inches(5.6), Inches(2.6), "GRANULAR COST ATTRIBUTION")
    tf = b1.text_frame; tf.word_wrap = True
    for text in [
        "\n• Multi-Level Allocation: Aggregates spend across container -> pod -> namespace -> cluster.",
        "• Resource Weighting: Distinguishes between compute-intensive workloads (high CPU cost) and caching microservices (high RAM cost).",
        "• Idle Capacity Visibility: Accurately identifies unallocated reservation gap (the 'slack') as chargeable institutional waste."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    b2 = add_card(s8, Inches(6.8), Inches(3.9), Inches(5.6), Inches(2.6), "AUDITABLE PROVENANCE & TRANSPARENCY")
    tf = b2.text_frame; tf.word_wrap = True
    for text in [
        "\n• Strict Separation of Concerns: Clear boundary between measured telemetry (vCPU/RAM), reference pricing models, and actual AWS billing invoices.",
        "• No Black-Box Calculations: All dollar projections shown in the dashboard trace directly to auditable equations and recorded benchmark metrics.",
        "• Verified in Automated Test Suite (`test_cost_analyzer.py` passing 100%)."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s8,
        "Slide 8 presents the mathematical foundation of our FinOps engine. The hourly cost of any container is the sum of its allocated CPU requests multiplied "
        "by the CPU reference price, plus its RAM requests multiplied by the RAM reference price. Based on AWS US-East-1 t3.medium pricing, CPU is attributed at "
        "$0.031611 per core-hour and memory at $0.004237 per GB-hour. Monthly costs are projected across the standard FinOps metric of 730 hours per month. "
        "Critically, our engine maintains complete mathematical provenance: we clearly distinguish between measured cgroups metrics, reference pricing models, "
        "and actual cloud bills, ensuring evaluators can verify every single calculation."
    )

    # =========================================================================
    # SLIDE 9: Kubernetes Monitoring Architecture
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, COLOR_BG_LIGHT)
    add_header(s9, "Kubernetes Monitoring & Telemetry Architecture")

    k1 = add_card(s9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.0), "TELEMETRY HARVESTING PIPELINE")
    tf = k1.text_frame; tf.word_wrap = True
    for text in [
        "\n1. Linux cgroups Kernel Accounting:",
        "   • CPU: Measured via `cpu.stat` (microsecond resolution).",
        "   • Memory: Working set measured via `memory.current`.",
        "\n2. Kubelet Summary API (/stats/summary):",
        "   • Node-level agent collects container metrics natively.",
        "\n3. Prometheus Time-Series Scrapes:",
        "   • Scrapes `container_cpu_usage_seconds_total` and `container_memory_working_set_bytes` every 15s.",
        "   • Window rate evaluation: `rate(container_cpu_usage_seconds_total[1m])`.",
        "\n4. Kube-State-Metrics (KSM):",
        "   • Supplies declarative specifications: `kube_pod_container_resource_requests`."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    k2 = add_card(s9, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.0), "COMPONENT HEALTH & RESILIENCE")
    tf = k2.text_frame; tf.word_wrap = True
    for text in [
        "\n• Dedicated Monitoring Status API (`/api/v1/monitoring/status`):",
        "   • Probes Prometheus (Port 9090) readiness.",
        "   • Probes Kube-State-Metrics (Port 8080) metrics availability.",
        "   • Probes OpenCost (Port 9003) allocation endpoint.",
        "   • Queries live Kubernetes cluster nodes and active pods.",
        "\n• Graceful Resilience & Transparency:",
        "   • If an integration is offline (e.g. port forwarding unforwarded), the cockpit displays an honest 'Unavailable (Port 9090)' badge.",
        "   • Automatically activates verified forensic benchmark data for continuous evaluation without mock fabrications."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s9,
        "Slide 9 explains our Kubernetes telemetry architecture. Container metrics originate directly from Linux cgroups at the kernel level. The node Kubelet "
        "exposes these via `/stats/summary`, and Prometheus scrapes rate-calculated vectors every 15 seconds. Simultaneously, Kube-State-Metrics provides "
        "the declarative requests and limits set in the deployment manifests. In our backend, we implemented a dedicated component health matrix that actively "
        "monitors Prometheus, KSM, and OpenCost. If a cloud port forward is disconnected, the system reports an honest offline status and transitions to our "
        "forensically validated experiment datasets."
    )

    # =========================================================================
    # SLIDE 10: Rightsizing & Forecasting
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, COLOR_BG_LIGHT)
    add_header(s10, "Rightsizing Intelligence & Demand Forecasting")

    r1 = add_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.0), "ADVISORY RIGHTSIZING ALGORITHM")
    tf = r1.text_frame; tf.word_wrap = True
    for text in [
        "\n• Mathematical Formulation:",
        "    R_rec_cpu = max( U_peak_cpu * (1 + S_buffer), Floor_cpu )",
        "    R_rec_ram = max( U_peak_ram * (1 + S_buffer), Floor_ram )",
        "\n• Safety Parameters:",
        "    • Safety Headroom Buffer (S_buffer) = 20% (1.20 multiplier)",
        "    • Architectural CPU Floor = 10m (0.010 vCPU cores)",
        "    • Architectural Memory Floor = 32Mi (33,554,432 bytes)",
        "\n• Why Safety Headroom Matters:",
        "    • Absorbs micro-bursts during classroom question rounds.",
        "    • Prevents CPU throttling during JIT compilation / JVM startup.",
        "    • Prevents fatal OOMKills from temporary memory allocations.",
        "\n• Non-Disruptive Advisory Manifests:",
        "    • Generates production Kubernetes patch specs without restarting live pods."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    r2 = add_card(s10, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.0), "HOLT'S LINEAR TREND FORECASTING")
    tf = r2.text_frame; tf.word_wrap = True
    for text in [
        "\n• Double Exponential Smoothing Equations:",
        "    Level:   L_t = alpha * Y_t + (1 - alpha) * (L_{t-1} + T_{t-1})",
        "    Trend:   T_t = beta * (L_t - L_{t-1}) + (1 - beta) * T_{t-1}",
        "    Forecast: Y_hat_{t+h} = L_t + h * T_t",
        "\n• Optimized Model Hyperparameters:",
        "    • Level smoothing factor (alpha) = 0.35",
        "    • Trend smoothing factor (beta) = 0.15",
        "\n• 95% Confidence Interval Bands:",
        "    Interval = Y_hat_{t+h} +/- (1.96 * RMSE)",
        "\n• Pedagogical Value:",
        "    • Anticipates upcoming exam week demand surges.",
        "    • Distinguishes baseline organic growth from transient spikes."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s10,
        "Slide 10 details our rightsizing algorithm and forecasting model. To compute safe rightsizing, we extract peak utilization and apply a 20% safety headroom buffer, "
        "enforcing architectural minimum floors of 10 millicores CPU and 32 Megabytes of RAM. This safety buffer ensures that containers never experience CPU throttling "
        "or out-of-memory crashes during microbursts. For forecasting, we implemented Holt's Linear Trend model with level smoothing alpha of 0.35 and trend smoothing "
        "beta of 0.15. The model projects future workload demand with 95% statistical confidence bounds, enabling university administrators to anticipate exam-period "
        "capacity needs well in advance."
    )

    # =========================================================================
    # SLIDE 11: Dashboard Demonstration & Screenshot Evidence
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, COLOR_BG_LIGHT)
    add_header(s11, "Live Interactive Dashboard Cockpit")

    # Add dashboard screenshot
    dash_img_path = os.path.join(EVIDENCE_DIR, "01_dashboard_executive_overview.png")
    if os.path.exists(dash_img_path):
        s11.shapes.add_picture(dash_img_path, Inches(0.8), Inches(1.5), width=Inches(7.2))

    # Feature Highlights Card
    f_card = add_card(s11, Inches(8.3), Inches(1.5), Inches(4.2), Inches(5.2), "COCKPIT CAPABILITIES")
    tf = f_card.text_frame; tf.word_wrap = True
    for item in [
        "\n1. Executive KPI Cards:",
        "   • Baseline Spend: $24.15/month",
        "   • Rightsized Spend: $7.48/month",
        "   • Projected Savings: 69.0% ($16.67/mo)",
        "\n2. Real-Time Comparison Bar:",
        "   • Visual progress track contrasting baseline versus optimized spend.",
        "\n3. Forensic Run Selector:",
        "   • Dropdown selector enabling live review of validated benchmark runs.",
        "\n4. Workload Inventory:",
        "   • Pod-by-pod container tracking with current vs recommended allocations.",
        "\n5. Zero-Flicker Polling:",
        "   • Real-time updates every 15s."
    ]:
        p = tf.add_paragraph(); p.text = item; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s11,
        "On Slide 11, we showcase our live interactive dashboard cockpit. This genuine screenshot was captured from our running backend. At the top, six executive "
        "KPI cards highlight monthly baseline spend ($24.15) versus rightsized spend ($7.48), yielding an immediate 69% cost reduction. Below, an intuitive comparison "
        "bar visually depicts the savings. The cockpit includes an active benchmark selector to inspect forensic experiment runs, an active container workload inventory, "
        "and a real-time monitoring health status panel. The dashboard is 100% responsive, renders with zero external CDN dependencies, and refreshes asynchronously."
    )

    # =========================================================================
    # SLIDE 12: Experimental Methodology
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, COLOR_BG_LIGHT)
    add_header(s12, "Experimental Methodology: 4-Phase Benchmark Load Profile")

    m_card = add_card(s12, Inches(0.8), Inches(1.5), Inches(11.6), Inches(2.2), "CONTROLLED LOAD PROFILE DESIGN (EXPERIMENT ID: exp-20261016-141448)")
    tf = m_card.text_frame; tf.word_wrap = True
    for text in [
        "\n• Controlled Benchmark Duration: 70 seconds across 4 distinct operational phases.",
        "• Workload Under Test: Containerized educational API backend running under Kubernetes resource constraints.",
        "• Automated Load Generation: Synchronized HTTP client issuing timed requests with millisecond latency logging.",
        "• Telemetry Sampling: Continuous 1-second resolution cgroups CPU/memory recording alongside Prometheus scraping."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT_DARK

    # 4 Phase Cards
    p_w = Inches(2.7)
    p_h = Inches(3.0)
    phases = [
        ("PHASE 1: IDLE", "0 RPS (10s)", "Establishes quiescent baseline consumption. CPU usage stays below 5m. Proves overprovisioning gap."),
        ("PHASE 2: MODERATE", "5 RPS (20s)", "Simulates standard classroom quiz interactions. CPU climbs to 35m. System maintains 100% availability."),
        ("PHASE 3: STRESS", "15 RPS (30s)", "Simulates peak exam submission rush. CPU peaks at 82.3m. P95 latency: 28.4ms. Zero dropped requests."),
        ("PHASE 4: RECOVERY", "0 RPS (10s)", "Load removed. Measures container memory reclamation and CPU decay hysteresis back to baseline.")
    ]
    for idx, (p_title, p_load, p_desc) in enumerate(phases):
        card = add_card(s12, Inches(0.8 + idx * 2.95), Inches(3.9), p_w, p_h, p_title)
        tf = card.text_frame; tf.word_wrap = True
        p = tf.add_paragraph()
        p.text = f"\nLoad: {p_load}\n\n{p_desc}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s12,
        "Slide 12 presents our experimental methodology. To rigorously evaluate the framework, we executed a 70-second 4-phase controlled load profile "
        "under experiment ID exp-20261016-141448. Phase 1 establishes the baseline idle consumption at 0 RPS for 10 seconds. Phase 2 introduces moderate load "
        "at 5 RPS for 20 seconds, representing regular classroom activity. Phase 3 injects a heavy 15 RPS surge for 30 seconds to simulate a synchronized "
        "exam submission deadline. Finally, Phase 4 enters a 10-second cool-down recovery to observe resource decay hysteresis. This entire run was verified "
        "by our automated forensic test harness, passing 10 out of 10 data integrity checks."
    )

    # =========================================================================
    # SLIDE 13: Results & Empirical Cost Comparison
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, COLOR_BG_LIGHT)
    add_header(s13, "Experimental Results & Empirical Cost Comparison")

    # Table with benchmark results
    t_shape = s13.shapes.add_table(5, 4, Inches(0.8), Inches(1.5), Inches(7.2), Inches(5.0))
    table = t_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(1.6)
    table.columns[3].width = Inches(1.8)

    r_headers = ["Metric / Parameter", "Baseline (Static)", "Rightsized (FinOps)", "Variance / Delta"]
    for col_idx, h_text in enumerate(r_headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = RGBColor(255, 255, 255)

    r_rows = [
        ["CPU Request", "500m (0.5 cores)", "98.8m (0.0988 cores)", "-80.2% Reduction"],
        ["Memory Request", "512 MiB", "128 MiB", "-75.0% Reduction"],
        ["Monthly Cost (USD)", "$13.08 / month", "$2.69 / month", "$10.39 / mo Saved"],
        ["Savings Percentage", "0.0% (Baseline)", "79.4% SAVINGS", "79.4% REDUCTION"]
    ]
    for row_idx, row in enumerate(r_rows):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if row_idx % 2 == 0 else COLOR_BG_LIGHT
            p = cell.text_frame.paragraphs[0]
            p.text = val; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_SUCCESS if "Reduction" in val or "SAVINGS" in val else COLOR_PRIMARY

    # Validation Highlights Card
    v_card = add_card(s13, Inches(8.3), Inches(1.5), Inches(4.2), Inches(5.0), "EMPIRICAL FINDINGS")
    tf = v_card.text_frame; tf.word_wrap = True
    for item in [
        "\n• 79.4% Workload Cost Reduction:",
        "  Baseline monthly cost dropped from $13.08 to $2.69 on the benchmarked container.",
        "\n• Zero Performance Degradation:",
        "  0.00% request failure rate across all 70 seconds of testing.",
        "\n• P95 Latency Maintained:",
        "  95th percentile latency remained under 28.4ms during the 15 RPS stress phase.",
        "\n• Adverse Test Insight (30 RPS):",
        "  When tested beyond single-pod concurrency at 30 RPS, timeouts confirmed the need for horizontal replica scaling alongside vertical rightsizing."
    ]:
        p = tf.add_paragraph(); p.text = item; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s13,
        "Slide 13 reveals our empirical experimental results. Under the static baseline allocation, the container requested 500m CPU and 512Mi RAM, resulting in "
        "a modeled monthly cost of $13.08. Our FinOps rightsizing engine calculated that peak demand during the 15 RPS surge was only 82.3m CPU. Adding our 20% "
        "safety headroom yielded a rightsized request of 98.8m CPU and 128Mi RAM, bringing monthly spend down to $2.69. This achieves an empirical cost reduction "
        "of 79.4%, with zero dropped requests and sub-30ms latency. Furthermore, our adverse 30 RPS test provided valuable forensic insight, demonstrating the "
        "boundary where horizontal autoscaling must complement vertical rightsizing."
    )

    # =========================================================================
    # SLIDE 14: Limitations & Future Scope
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, COLOR_BG_LIGHT)
    add_header(s14, "Limitations & Future Roadmap")

    l1 = add_card(s14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.0), "HONEST TECHNICAL LIMITATIONS")
    tf = l1.text_frame; tf.word_wrap = True
    for text in [
        "\n1. Advisory (Non-Mutating) Mode:",
        "   • Recommendations generate declarative YAML patches rather than auto-mutating live clusters. Requires administrator review before applying.",
        "\n2. Duration of Benchmark Data:",
        "   • Experimental validation was conducted over a controlled 70s profile; capturing semester-long seasonal variations requires multi-week telemetry ingestion.",
        "\n3. Pricing Model Assumptions:",
        "   • Uses AWS US-East-1 list rates; does not model complex institutional Enterprise Discount Programs (EDP) or Spot instance interruption discounts.",
        "\n4. Single-Pod Concurrency Ceiling:",
        "   • Rightsizing individual pods cannot compensate for insufficient replica count under extreme 30+ RPS loads."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    l2 = add_card(s14, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.0), "FUTURE RESEARCH ROADMAP")
    tf = l2.text_frame; tf.word_wrap = True
    for text in [
        "\n1. GitOps Automated PR Generation:",
        "   • Automatically submit rightsizing YAML patches as Git pull requests to ArgoCD / Flux repositories.",
        "\n2. Deep Learning Forecasting (SageMaker):",
        "   • Transition from statistical Holt-Winters to temporal transformer models (DeepAR / TFT) for complex academic calendar forecasting.",
        "\n3. Cluster Node Bin-Packing (Karpenter):",
        "   • Couple container rightsizing with dynamic Karpenter node provisioning to physically consolidate nodes and realize immediate EC2 invoice savings.",
        "\n4. Multi-Cloud Ingress Cost Modeling:",
        "   • Expand cost attribution to incorporate cross-AZ data transfer and storage volumes."
    ]:
        p = tf.add_paragraph(); p.text = text; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT_DARK

    add_speaker_note(s14,
        "Slide 14 addresses our technical limitations and future roadmap with academic honesty. First, our engine operates in advisory mode: it generates declarative "
        "patch manifests rather than mutating live production pods without human review. Second, while our 70-second load profile thoroughly validated surge dynamics, "
        "multi-week logging is required for semester-scale seasonal models. Third, our pricing engine uses public reference cards rather than custom enterprise discount "
        "structures. For our future roadmap, we plan to integrate automated GitOps pull requests via ArgoCD, integrate AWS SageMaker for deep learning time-series "
        "forecasting, and couple container rightsizing with Karpenter to physically terminate unneeded EC2 nodes."
    )

    # =========================================================================
    # SLIDE 15: Conclusion & Q&A
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, COLOR_BG_DARK)

    # Header in dark theme
    t_box = s15.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.6), Inches(1.2))
    tf = t_box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Conclusion & Faculty Evaluation Q&A"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = RGBColor(255, 255, 255)
    p2 = tf.add_paragraph()
    p2.text = "BCSE355L Cloud Architecture Design | Final Deliverable Verification"
    p2.font.size = Pt(14); p2.font.color.rgb = COLOR_ACCENT

    # Summary Card 1
    c1 = add_card(s15, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5), "PROJECT DELIVERABLE SUMMARY", COLOR_ACCENT, RGBColor(15, 33, 64))
    tf = c1.text_frame; tf.word_wrap = True
    for t in [
        "\n• 57/57 Automated Tests Passing (Unit & Integration).",
        "• 28/28 Release Health Checks Passed (100% clean).",
        "• 10/10 Forensic Verification on Experimental Benchmarks.",
        "• 69.0% - 79.4% Modeled Cost Reduction Demonstrated.",
        "• Non-Disruptive Advisory Rightsizing with 20% Safety Floor.",
        "• Zero-Dependency Local and Presentation Startup Scripts.",
        "• Fully Auditable Codebase & Academic Documentation."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = RGBColor(226, 232, 240)

    # Summary Card 2
    c2 = add_card(s15, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5), "EVALUATION & REPOSITORY ACCESS", COLOR_ACCENT, RGBColor(15, 33, 64))
    tf = c2.text_frame; tf.word_wrap = True
    for t in [
        "\n• Team Lead: K. Darshan",
        "• Course: BCSE355L - Cloud Architecture Design",
        "• Institution: Vellore Institute of Technology (VIT), Vellore",
        "• Repository: github.com/Dev-withDarshan/KubeCostFinOps",
        "• Branch: develop (Clean, Verified, Production Ready)",
        "\nThank you to our faculty evaluators.",
        "We are now ready for your questions."
    ]:
        p = tf.add_paragraph(); p.text = t; p.font.size = Pt(11); p.font.color.rgb = RGBColor(226, 232, 240)

    add_speaker_note(s15,
        "In conclusion, Slide 15 summarizes our project deliverables. We have engineered, stabilized, and validated an enterprise-grade Kubernetes FinOps "
        "cost optimization framework specifically tailored to educational SaaS workloads. With 57 passing automated tests, 28 passed release checks, "
        "10 out of 10 forensic verification passes, and a proven 69% to 79.4% modeled cost reduction, this project provides a rigorous, demonstrable, and "
        "academically sound solution. We thank the faculty evaluation committee for their time and guidance, and we are now delighted to answer your questions."
    )

    # Save Presentation PPTX
    pptx_path = os.path.join(OUTPUT_DIR, "Final_Project_Presentation.pptx")
    prs.save(pptx_path)
    print(f"[SUCCESS] PowerPoint deck created: {pptx_path} (15 slides)")
    return pptx_path

if __name__ == "__main__":
    build_presentation()

