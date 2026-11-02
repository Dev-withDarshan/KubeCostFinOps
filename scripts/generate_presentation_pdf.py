"""
generate_presentation_pdf.py - Generates the matching 15-page presentation PDF
using Chrome's headless print-to-pdf engine with pixel-perfect 16:9 layout.
"""

import os
import sys
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "1Submission", "PRESENTATION")
EVIDENCE_DIR = os.path.join(WORKSPACE_ROOT, "evidence", "final-presentation")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_presentation_html():
    dash_img_uri = os.path.join(EVIDENCE_DIR, "01_dashboard_executive_overview.png").replace("\\", "/")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>KubeCostFinOps - Final Project Presentation</title>
<style>
  @page {{
    size: 13.333in 7.5in;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }}
  body {{
    background-color: #f1f5f9;
    color: #0f172a;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 13.333in;
    height: 7.5in;
    page-break-after: always;
    padding: 0.6in 0.8in;
    position: relative;
    overflow: hidden;
    background: #f8fafc;
  }}
  .slide.dark {{
    background: #0a192f;
    color: #f8fafc;
  }}
  .category {{
    font-size: 11pt;
    font-weight: 700;
    color: #0284c7;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.1in;
  }}
  .title {{
    font-size: 24pt;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 0.4in;
    line-height: 1.2;
  }}
  .slide.dark .title {{
    color: #ffffff;
  }}
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4in;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.35in;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 0.25in;
  }}
  .card {{
    background: #ffffff;
    border: 1.5pt solid #e2e8f0;
    border-radius: 8pt;
    padding: 0.35in;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  }}
  .slide.dark .card {{
    background: #0f2140;
    border-color: #0284c7;
    color: #cbd5e1;
  }}
  .card-title {{
    font-size: 13pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 0.2in;
    border-bottom: 1.5pt solid #e2e8f0;
    padding-bottom: 0.1in;
  }}
  .slide.dark .card-title {{
    color: #38bdf8;
    border-color: #1e3a8a;
  }}
  .card-body p {{
    font-size: 11pt;
    line-height: 1.5;
    margin-bottom: 0.12in;
    color: #334155;
  }}
  .slide.dark .card-body p {{
    color: #cbd5e1;
  }}
  .table-custom {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.1in;
    font-size: 11pt;
  }}
  .table-custom th {{
    background: #1e3a8a;
    color: #ffffff;
    padding: 10pt;
    text-align: left;
  }}
  .table-custom td {{
    padding: 10pt;
    border-bottom: 1pt solid #e2e8f0;
    background: #ffffff;
  }}
  .table-custom tr:nth-child(even) td {{
    background: #f8fafc;
  }}
  .highlight-badge {{
    display: inline-block;
    padding: 4pt 8pt;
    border-radius: 4pt;
    font-weight: 700;
    background: #dcfce7;
    color: #15803d;
  }}
  .formula-box {{
    background: #f1f5f9;
    border-left: 4pt solid #0284c7;
    padding: 0.2in;
    font-family: monospace;
    font-size: 11pt;
    margin-bottom: 0.2in;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: TITLE -->
<div class="slide dark" style="display:flex; flex-direction:column; justify-content:center;">
  <div style="border-left: 6pt solid #0284c7; padding-left: 0.3in; margin-bottom: 0.5in;">
    <div class="category" style="color:#38bdf8; font-size:13pt;">BCSE355L — CLOUD ARCHITECTURE DESIGN | FINAL EVALUATION</div>
    <div class="title" style="font-size:32pt; margin-bottom:0.1in;">Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence</div>
    <div style="font-size:15pt; color:#94a3b8;">Automated Telemetry, Auditable Cost Attribution, Advisory Rightsizing & Demand Forecasting</div>
  </div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">INSTITUTION & PROGRAM</div>
      <div class="card-body">
        <p><strong>Institution:</strong> Vellore Institute of Technology (VIT), Vellore</p>
        <p><strong>Department:</strong> School of Computer Science and Engineering</p>
        <p><strong>Evaluation:</strong> Final Academic Project Review (November 2026)</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">DEVELOPMENT TEAM & STATUS</div>
      <div class="card-body">
        <p><strong>Team Lead:</strong> K. Darshan</p>
        <p><strong>Repository:</strong> github.com/Dev-withDarshan/KubeCostFinOps (develop)</p>
        <p><strong>Verification:</strong> 57/57 Automated Tests Passing | 28/28 Release Checks Verified</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 2: PROBLEM STATEMENT -->
<div class="slide">
  <div class="category">PROBLEM FORMULATION</div>
  <div class="title">Problem Statement: Cloud Resource & Budget Waste in Education</div>
  <div class="grid-3">
    <div class="card">
      <div class="card-title">1. Extreme Load Variance</div>
      <div class="card-body">
        <p>• Educational platforms (Moodle, Canvas, code evaluators) suffer extreme diurnal traffic fluctuations.</p>
        <p>• Huge traffic spikes during submission deadlines and timed exams.</p>
        <p>• Protracted idle troughs overnight and during semester breaks with >10:1 peak-to-trough ratios.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">2. Static Overprovisioning</div>
      <div class="card-body">
        <p>• Administrators set container requests to peak historical limits to prevent fatal OOMKills.</p>
        <p>• Standard 500m CPU / 512Mi RAM requests idle at under 50m CPU.</p>
        <p>• In Kubernetes, requests lock underlying node capacity 24/7, generating 60-80% idle waste.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">3. Tooling Deficiencies</div>
      <div class="card-body">
        <p>• Horizontal Pod Autoscaler (HPA) multiplies waste by spinning up oversized pod replicas.</p>
        <p>• Vertical Pod Autoscaler (VPA) evicts running pods, causing exam session dropouts.</p>
        <p>• Commercial SaaS tools (Kubecost, Cast.ai) impose high licensing costs and heavy agent overhead.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 3: MOTIVATION -->
<div class="slide">
  <div class="category">ECONOMIC CONTEXT</div>
  <div class="title">Motivation: FinOps & Cloud Financial Accountability</div>
  <div class="grid-2" style="margin-bottom:0.3in;">
    <div class="card">
      <div class="card-title">ACADEMIC BUDGET REALITIES</div>
      <div class="card-body">
        <p>• Universities operate under fixed, non-elastic infrastructure grants.</p>
        <p>• Unmonitored Kubernetes clusters waste over 35% of cloud expenditure on unallocated reservations.</p>
        <p>• Every dollar wasted on idle reservation is capital lost from educational computing grants.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">THE FINOPS LIFECYCLE PARADIGM</div>
      <div class="card-body">
        <p>• <strong>Inform:</strong> Real-time visibility into per-container cost attribution ($/vCPU-hr and $/GB-hr).</p>
        <p>• <strong>Optimize:</strong> Data-driven rightsizing with safety buffers to eliminate reservation slack.</p>
        <p>• <strong>Operate:</strong> Align cluster provisioning with pedagogical schedules via predictive forecasting.</p>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">ARCHITECTURAL DESIGN PRINCIPLES</div>
    <div class="card-body">
      <p>• <strong>Non-Disruptive:</strong> Advisory declarative YAML recommendations without pod evictions.</p>
      <p>• <strong>Strict Traceability:</strong> Mathematical separation of cgroups telemetry, reference rates, and billing invoices.</p>
      <p>• <strong>Self-Hosted:</strong> Zero external SaaS dependencies, ensuring compliance with institutional privacy policies.</p>
    </div>
  </div>
</div>

<!-- SLIDE 4: OBJECTIVES -->
<div class="slide">
  <div class="category">PROJECT GOALS</div>
  <div class="title">Project Objectives & Technical Scope</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">1. CONTINUOUS TELEMETRY INGESTION</div>
      <div class="card-body">
        <p>• Ingest cgroups CPU (`cpu.stat`) and memory (`memory.current`) at 15-second intervals.</p>
        <p>• Interface with Prometheus (9090), Kube-State-Metrics (8080), and OpenCost (9003).</p>
        <p>• Seamless dual-mode operation: live cluster polling with offline fallback to forensic datasets.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">2. FINOPS COST ATTRIBUTION</div>
      <div class="card-body">
        <p>• Map container allocations to dollar spend via AWS US-East-1 reference rates ($0.031611/core-hr, $0.004237/GB-hr).</p>
        <p>• Attribute expenditure to container, pod, and namespace tiers across 730 monthly hours.</p>
        <p>• Full mathematical transparency with auditable formula derivation.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">3. ADVISORY RIGHTSIZING</div>
      <div class="card-body">
        <p>• Derive optimized requests using peak utilization + 20% safety headroom buffer.</p>
        <p>• Enforce minimum architectural safety floors (10m CPU, 32Mi RAM).</p>
        <p>• Output declarative Kubernetes patch specifications without evicting live pods.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">4. OPERATIONAL FORECASTING & COCKPIT</div>
      <div class="card-body">
        <p>• Double Exponential Smoothing (Holt's Linear Trend) with 95% confidence intervals.</p>
        <p>• Executive single-pane cockpit with 6 real-time KPI cards and interactive cost comparison.</p>
        <p>• Production-hardened with 57 automated tests and clean release verification.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 5: STATE OF THE ART & RESEARCH GAP -->
<div class="slide">
  <div class="category">COMPARATIVE ANALYSIS</div>
  <div class="title">State of the Art & Research Gap Analysis</div>
  <table class="table-custom">
    <thead>
      <tr>
        <th>Evaluation Dimension</th>
        <th>Manual Static Sizing</th>
        <th>Kubernetes Native VPA</th>
        <th>Commercial Tools (Kubecost)</th>
        <th style="background:#0284c7;">Our FinOps Framework</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Intervention Mode</strong></td>
        <td>Manual human guesswork</td>
        <td>Forced in-place pod eviction</td>
        <td>Agent mutation / advice</td>
        <td><strong>Advisory Declarative Manifests</strong></td>
      </tr>
      <tr>
        <td><strong>Workload Downtime</strong></td>
        <td>Zero (but high waste)</td>
        <td>High (Drops student sessions)</td>
        <td>Low to Medium</td>
        <td><strong>Zero (Non-disruptive)</strong></td>
      </tr>
      <tr>
        <td><strong>Cost Attribution</strong></td>
        <td>None (Spreadsheets)</td>
        <td>None (Resource metrics only)</td>
        <td>Proprietary closed engine</td>
        <td><strong>Traceable Open AWS Price Card</strong></td>
      </tr>
      <tr>
        <td><strong>Academic Surge Focus</strong></td>
        <td>None</td>
        <td>None (Generic reactive)</td>
        <td>Enterprise SaaS focused</td>
        <td><strong>Tailored to Exam/Deadline Peaks</strong></td>
      </tr>
      <tr>
        <td><strong>Licensing & Overhead</strong></td>
        <td>Free</td>
        <td>Free (K8s SIG)</td>
        <td>Expensive Commercial Tier</td>
        <td><strong>Open Source & Zero External CDN</strong></td>
      </tr>
    </tbody>
  </table>
</div>

<!-- SLIDE 6: PROPOSED ARCHITECTURE -->
<div class="slide">
  <div class="category">SYSTEM DESIGN</div>
  <div class="title">Proposed 3-Tier System Architecture</div>
  <div class="grid-3">
    <div class="card">
      <div class="card-title">TIER 1: TELEMETRY & INGESTION</div>
      <div class="card-body">
        <p><strong>Kubernetes Cluster</strong><br>• Docker / Kind / AWS EKS Pods<br>• Linux cgroups kernel telemetry</p>
        <p><strong>Scraping Agents</strong><br>• Kubelet Summary API (/stats/summary)<br>• Kube-State-Metrics (Port 8080)<br>• Prometheus Server (Port 9090)<br>• OpenCost API (Port 9003)</p>
        <p><strong>Ingestion Gateway</strong><br>• 15s scrape interval<br>• Dual-mode fallback adapter</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">TIER 2: FINOPS ANALYTICAL ENGINE</div>
      <div class="card-body">
        <p><strong>Cost Attribution Engine</strong><br>• Reference card pricing matrix<br>• $0.031611/core-hr | $0.004237/GB-hr<br>• 730-hour monthly projections</p>
        <p><strong>Rightsizing Intelligence</strong><br>• Peak utilization + 20% headroom<br>• 10m CPU / 32Mi RAM safety floor</p>
        <p><strong>Forecasting Baseline</strong><br>• Holt's Linear Trend (alpha=0.35, beta=0.15)<br>• 95% Confidence Interval bounds</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">TIER 3: PRESENTATION & COCKPIT</div>
      <div class="card-body">
        <p><strong>REST Backend API</strong><br>• Python Standard Library Server<br>• /api/health & /api/ready<br>• /api/v1/costs/summary<br>• /api/v1/recommendations<br>• /api/v1/monitoring/status</p>
        <p><strong>Executive Web Cockpit</strong><br>• Vanilla ES6 + Responsive CSS3<br>• 6 Real-time KPI Cards<br>• Baseline vs Rightsized bar<br>• Benchmark run selector</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 7: TECH STACK -->
<div class="slide">
  <div class="category">IMPLEMENTATION SPECIFICATION</div>
  <div class="title">Technology Stack & Cloud Infrastructure</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">CONTAINER & CLOUD ORCHESTRATION</div>
      <div class="card-body">
        <p>• <strong>Kubernetes (Kind / AWS EKS):</strong> Multi-node workload deployment with resource request/limit specs.</p>
        <p>• <strong>AWS CloudFormation:</strong> 15 declarative infrastructure resources (VPC, public subnets, EKS Cluster, t3.medium Managed NodeGroup, IAM roles).</p>
        <p>• <strong>Zero-NAT Gateway Design:</strong> Eliminates $0.045/hr idle NAT fees during academic evaluation sessions.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">TELEMETRY & INGESTION HARNESS</div>
      <div class="card-body">
        <p>• <strong>Prometheus v2.45+:</strong> Scrapes container metrics every 15s via standard exposition format.</p>
        <p>• <strong>Kube-State-Metrics:</strong> Emits declarative container limits and requests.</p>
        <p>• <strong>OpenCost:</strong> Real-time allocation engine matching container usage vectors to cloud pricing cards.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">ANALYTICAL ENGINE & REST SERVER</div>
      <div class="card-body">
        <p>• <strong>Python 3.14 + Standard Library:</strong> Built-in lightweight HTTP service eliminating bloated runtime dependencies.</p>
        <p>• <strong>NumPy, SciPy, Pandas:</strong> Statistical rolling windows, Holt's linear smoothing, and RMSE calculations.</p>
        <p>• <strong>Automated Test Suite:</strong> 57 unit & integration tests passing with 100% code coverage.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">EXECUTIVE COCKPIT & UI</div>
      <div class="card-body">
        <p>• <strong>Vanilla HTML5, CSS3, ES6:</strong> Zero external CDN reliance, 100% self-hosted, air-gap safe.</p>
        <p>• <strong>Real-Time Dynamic Polling:</strong> Asynchronous parallel fetching with zero UI flicker.</p>
        <p>• <strong>Honest Provenance:</strong> Clear visual badges distinguishing live cluster metrics from historical benchmarks.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 8: FINOPS ENGINE & COST ATTRIBUTION -->
<div class="slide">
  <div class="category">FINANCIAL ENGINEERING</div>
  <div class="title">FinOps Engine: Mathematical Cost Attribution Model</div>
  <div class="formula-box">
    <strong>HOURLY CONTAINER COST FORMULA:</strong><br>
    C_hourly = ( R_cpu * P_cpu ) + ( R_ram * P_ram )<br>
    Where R_cpu = Allocated vCPU cores, R_ram = Allocated Memory in GB.<br><br>
    <strong>AWS US-EAST-1 REFERENCE PRICING MATRIX (t3.medium compute blend):</strong><br>
    P_cpu = $0.031611 per vCPU-hour  |  P_ram = $0.004237 per GB-hour<br><br>
    <strong>MONTHLY PROJECTION (Standard 730 accounting hours/month):</strong><br>
    C_monthly = C_hourly * 730 hours
  </div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">GRANULAR MULTI-TIER ATTRIBUTION</div>
      <div class="card-body">
        <p>• Hierarchical rollups: Container → Pod → Namespace → Cluster total.</p>
        <p>• Distinct attribution of compute-heavy vs memory-heavy workloads.</p>
        <p>• Explicit quantification of the 'reservation slack' (unused headroom paid to cloud providers).</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">AUDITABLE PROVENANCE GUARANTEE</div>
      <div class="card-body">
        <p>• Strict boundary between measured cgroups metrics, reference pricing cards, and actual cloud bills.</p>
        <p>• No black-box estimations: every value displayed in the UI is mathematically verifiable.</p>
        <p>• Verified in automated test suite (`test_cost_analyzer.py` passing 100%).</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 9: KUBERNETES MONITORING -->
<div class="slide">
  <div class="category">OBSERVABILITY INFRASTRUCTURE</div>
  <div class="title">Kubernetes Monitoring & Telemetry Architecture</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">TELEMETRY EXTRACTION WORKFLOW</div>
      <div class="card-body">
        <p>1. <strong>cgroups Kernel Accounting:</strong> CPU ticks via `cpu.stat`, active memory footprint via `memory.current`.</p>
        <p>2. <strong>Kubelet Summary API:</strong> Node agent aggregates container metrics at `/stats/summary`.</p>
        <p>3. <strong>Prometheus Scraping:</strong> Ingests `container_cpu_usage_seconds_total` and `container_memory_working_set_bytes` at 15s intervals.</p>
        <p>4. <strong>Kube-State-Metrics:</strong> Emits declarative container requests and limits from cluster etcd.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">COMPONENT HEALTH & RESILIENCE MATRIX</div>
      <div class="card-body">
        <p>• Dedicated endpoint (`/api/v1/monitoring/status`) performs automated HTTP health checks:</p>
        <p>&nbsp;&nbsp;• Prometheus (Port 9090) readiness probe.</p>
        <p>&nbsp;&nbsp;• Kube-State-Metrics (Port 8080) metrics availability.</p>
        <p>&nbsp;&nbsp;• OpenCost (Port 9003) allocation endpoint.</p>
        <p>&nbsp;&nbsp;• Kubernetes Node & Pod scheduling status.</p>
        <p>• Automatic, honest fallback to verified forensic benchmark data when live cloud forwarding is disconnected.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 10: RIGHTSIZING & FORECASTING -->
<div class="slide">
  <div class="category">ALGORITHMIC INTELLIGENCE</div>
  <div class="title">Rightsizing Intelligence & Demand Forecasting</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">ADVISORY RIGHTSIZING ALGORITHM</div>
      <div class="card-body">
        <p><strong>Mathematical Formulation:</strong></p>
        <p><code>R_rec_cpu = max( U_peak_cpu * (1 + S_buffer), Floor_cpu )</code></p>
        <p><code>R_rec_ram = max( U_peak_ram * (1 + S_buffer), Floor_ram )</code></p>
        <p><strong>Safety Parameters:</strong></p>
        <p>• Safety Headroom Buffer (S_buffer) = <strong>20% (1.20x multiplier)</strong></p>
        <p>• Architectural CPU Floor = <strong>10m (0.010 vCPU cores)</strong></p>
        <p>• Architectural RAM Floor = <strong>32Mi (33,554,432 bytes)</strong></p>
        <p><strong>Purpose:</strong> Absorbs classroom question surges, JVM compilation spikes, and prevents fatal OOMKills.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">HOLT'S LINEAR TREND FORECASTING</div>
      <div class="card-body">
        <p><strong>Double Exponential Smoothing Formulation:</strong></p>
        <p><code>Level:  L_t = alpha * Y_t + (1 - alpha) * (L_{{t-1}} + T_{{t-1}})</code></p>
        <p><code>Trend:  T_t = beta * (L_t - L_{{t-1}}) + (1 - beta) * T_{{t-1}}</code></p>
        <p><code>Forecast: Y_hat_{{t+h}} = L_t + h * T_t</code></p>
        <p><strong>Calibrated Hyperparameters:</strong></p>
        <p>• Level factor alpha = <strong>0.35</strong> | Trend factor beta = <strong>0.15</strong></p>
        <p>• 95% Confidence Bounds: <code>Y_hat_{{t+h}} ± 1.96 * RMSE</code></p>
        <p><strong>Value:</strong> Projects upcoming exam deadline surges across hourly horizons.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 11: DASHBOARD DEMONSTRATION -->
<div class="slide">
  <div class="category">OPERATIONAL VALIDATION</div>
  <div class="title">Live Interactive Dashboard Demonstration</div>
  <div style="display:flex; gap:0.4in; align-items:flex-start;">
    <div style="flex:1.8; border:2pt solid #0284c7; border-radius:8pt; overflow:hidden; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1);">
      <img src="{dash_img_uri}" style="width:100%; display:block;" alt="Dashboard Screenshot">
    </div>
    <div style="flex:1.2;">
      <div class="card">
        <div class="card-title">KEY DEMONSTRATION HIGHLIGHTS</div>
        <div class="card-body">
          <p>• <strong>6 Executive KPI Cards:</strong> Baseline ($24.15) vs Rightsized ($7.48), 69.0% immediate savings, active pods, and cluster resource utilization.</p>
          <p>• <strong>Real-Time Comparison Bar:</strong> Visual progress track highlighting realized savings gap.</p>
          <p>• <strong>Benchmark Run Selector:</strong> Dropdown to toggle forensic experiment runs (`exp-20261016-141448`).</p>
          <p>• <strong>Workload Inventory:</strong> Pod-by-pod container tracking showing current vs recommended allocations.</p>
          <p>• <strong>Zero-Flicker Polling:</strong> Asynchronous updates every 15s.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 12: EXPERIMENTAL METHODOLOGY -->
<div class="slide">
  <div class="category">EMPIRICAL BENCHMARKING</div>
  <div class="title">Experimental Methodology: 4-Phase Controlled Load Profile</div>
  <div class="formula-box" style="margin-bottom:0.25in;">
    <strong>CONTROLLED LOAD EXPERIMENT SPECIFICATION (EXPERIMENT ID: exp-20261016-141448)</strong><br>
    Benchmark Duration: 70 seconds across 4 distinct operational phases | 1-second telemetry sampling | Zero dropped requests
  </div>
  <div class="grid-4">
    <div class="card">
      <div class="card-title" style="font-size:11pt;">PHASE 1: IDLE</div>
      <div class="card-body">
        <p><strong>Load:</strong> 0 RPS (10s)</p>
        <p>Establishes quiescent baseline. CPU stays below 5m. Proves the existence of massive idle reservation slack.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title" style="font-size:11pt;">PHASE 2: MODERATE</div>
      <div class="card-body">
        <p><strong>Load:</strong> 5 RPS (20s)</p>
        <p>Simulates standard classroom quiz interactions. CPU reaches 35m. 100% availability maintained.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title" style="font-size:11pt;">PHASE 3: STRESS</div>
      <div class="card-body">
        <p><strong>Load:</strong> 15 RPS (30s)</p>
        <p>Simulates synchronized deadline submission rush. CPU peaks at 82.3m. P95 latency: 28.4ms. 0 errors.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title" style="font-size:11pt;">PHASE 4: RECOVERY</div>
      <div class="card-body">
        <p><strong>Load:</strong> 0 RPS (10s)</p>
        <p>Load removed. Observes container memory reclamation and CPU decay hysteresis back to baseline.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 13: RESULTS & EMPIRICAL COST COMPARISON -->
<div class="slide">
  <div class="category">QUANTITATIVE VALIDATION</div>
  <div class="title">Experimental Results & Empirical Cost Comparison</div>
  <div class="grid-2">
    <div>
      <table class="table-custom" style="margin-top:0;">
        <thead>
          <tr>
            <th>Metric / Dimension</th>
            <th>Static Baseline</th>
            <th>FinOps Rightsized</th>
            <th style="background:#0284c7;">Savings / Delta</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>CPU Request</strong></td>
            <td>500m (0.50 cores)</td>
            <td>98.8m (0.0988 cores)</td>
            <td><span class="highlight-badge">-80.2% Reduction</span></td>
          </tr>
          <tr>
            <td><strong>Memory Request</strong></td>
            <td>512 MiB</td>
            <td>128 MiB</td>
            <td><span class="highlight-badge">-75.0% Reduction</span></td>
          </tr>
          <tr>
            <td><strong>Monthly Spend</strong></td>
            <td>$13.08 / month</td>
            <td>$2.69 / month</td>
            <td><span class="highlight-badge">$10.39 / mo Saved</span></td>
          </tr>
          <tr>
            <td><strong>Modeled Savings</strong></td>
            <td>0.0% (Baseline)</td>
            <td><strong>79.4% SAVED</strong></td>
            <td><strong style="color:#15803d;">79.4% SAVINGS</strong></td>
          </tr>
          <tr>
            <td><strong>Error Rate</strong></td>
            <td>0.00%</td>
            <td>0.00%</td>
            <td><strong>Zero Degradation</strong></td>
          </tr>
          <tr>
            <td><strong>P95 Latency</strong></td>
            <td>27.8 ms</td>
            <td>28.4 ms</td>
            <td><strong>+0.6 ms (Negligible)</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="card">
      <div class="card-title">EMPIRICAL TAKEAWAYS</div>
      <div class="card-body">
        <p>• <strong>79.4% Proven Cost Reduction:</strong> Drops monthly spend from $13.08 to $2.69 per container.</p>
        <p>• <strong>Flawless Reliability:</strong> Zero request drops or HTTP timeouts across the entire 70-second test.</p>
        <p>• <strong>Adverse Concurrency Test (30 RPS):</strong> At 30 RPS on a single container, timeout latency confirmed that vertical rightsizing must be complemented by horizontal replica autoscaling during extreme surges.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 14: LIMITATIONS & FUTURE SCOPE -->
<div class="slide">
  <div class="category">CRITICAL ANALYSIS</div>
  <div class="title">Limitations & Future Engineering Roadmap</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">HONEST TECHNICAL LIMITATIONS</div>
      <div class="card-body">
        <p>1. <strong>Advisory Mode:</strong> Generates declarative YAML patches rather than auto-mutating clusters, requiring human administrative sign-off.</p>
        <p>2. <strong>Benchmark Duration:</strong> 70s controlled burst profile proves surge resilience, but multi-week telemetry is needed for seasonal academic calendars.</p>
        <p>3. <strong>Pricing Assumptions:</strong> Grounded in AWS US-East-1 list pricing; does not incorporate custom enterprise discount agreements (EDP) or Spot rates.</p>
        <p>4. <strong>Single-Pod Limit:</strong> Rightsizing individual containers cannot compensate for insufficient pod replicas at 30+ RPS.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">FUTURE RESEARCH ROADMAP</div>
      <div class="card-body">
        <p>1. <strong>GitOps Automation:</strong> Automatically generate Pull Requests with recommended patches to ArgoCD / Flux repositories.</p>
        <p>2. <strong>AWS SageMaker ML Forecasting:</strong> Upgrade from Holt's Linear Trend to Temporal Fusion Transformers (TFT) or DeepAR for seasonal demand modeling.</p>
        <p>3. <strong>Cluster Bin-Packing (Karpenter):</strong> Couple pod rightsizing with dynamic node consolidation to physically downscale EC2 instances and realize cash savings.</p>
        <p>4. <strong>Multi-Cloud Cost Modeling:</strong> Expand cost attribution to incorporate cross-AZ data transfer fees and EBS storage volumes.</p>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 15: CONCLUSION & QA -->
<div class="slide dark" style="display:flex; flex-direction:column; justify-content:center;">
  <div style="border-left: 6pt solid #0284c7; padding-left: 0.3in; margin-bottom: 0.4in;">
    <div class="category" style="color:#38bdf8; font-size:13pt;">EVALUATION SUMMARY & WRAP-UP</div>
    <div class="title" style="font-size:30pt; margin-bottom:0.1in;">Conclusion & Faculty Evaluation Q&A</div>
    <div style="font-size:14pt; color:#94a3b8;">BCSE355L Cloud Architecture Design | VIT Vellore</div>
  </div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">VERIFIED DELIVERABLE ACHIEVEMENTS</div>
      <div class="card-body">
        <p>• <strong>57/57 Automated Tests Passing:</strong> Comprehensive unit & integration coverage.</p>
        <p>• <strong>28/28 Release Checks Verified:</strong> 100% clean repository status.</p>
        <p>• <strong>10/10 Forensic Verification:</strong> Validated benchmark integrity on controlled experiments.</p>
        <p>• <strong>69.0% - 79.4% Cost Reduction:</strong> Modeled savings verified on containerized workloads.</p>
        <p>• <strong>Advisory Rightsizing with 20% Buffer:</strong> Zero-downtime, non-disruptive cloud optimization.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-title">EVALUATION & REPOSITORY COORDINATES</div>
      <div class="card-body">
        <p><strong>Team Lead:</strong> K. Darshan</p>
        <p><strong>GitHub:</strong> github.com/Dev-withDarshan/KubeCostFinOps (develop)</p>
        <p><strong>Demonstration Cockpit:</strong> http://127.0.0.1:8000</p>
        <br>
        <p style="font-size:13pt; color:#38bdf8; font-weight:700;">Thank you, respected faculty evaluators.<br>We invite your questions.</p>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""
    html_path = os.path.join(OUTPUT_DIR, "presentation_deck.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[HTML] Slide deck template written: {html_path}")
    return html_path

def convert_html_to_pdf(html_path):
    pdf_path = os.path.join(OUTPUT_DIR, "Final_Project_Presentation.pdf")
    print(f"[PDF] Printing slide deck to PDF via Google Chrome...")
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"[SUCCESS] PDF generated: {pdf_path} ({size_kb:.1f} KB)")
        return pdf_path
    else:
        print(f"[FAIL] Could not generate PDF: {res.stderr}")
        return None

def main():
    html_path = build_presentation_html()
    convert_html_to_pdf(html_path)

if __name__ == "__main__":
    main()
