"""
verify_all_sections_live.py — Verify all 6 dashboard sections and drawer interaction
against the live running server at http://127.0.0.1:8000.
"""
import subprocess
import json
import os
import re
import shutil

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
INDEX_PATH = r"C:\Users\gnavy\Downloads\KubeCostFinOps\src\frontend\index.html"
BACKUP_PATH = r"C:\Users\gnavy\Downloads\KubeCostFinOps\src\frontend\index.html.bak_sections"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    orig_html = f.read()

shutil.copyfile(INDEX_PATH, BACKUP_PATH)

probe_code = """
<script>
window.addEventListener('DOMContentLoaded', async () => {
    // Wait for all asynchronous API calls and render passes
    await new Promise(r => setTimeout(r, 1500));

    const checks = {};

    // 1. Header & Status
    const statusText = document.getElementById('apiStatusText')?.textContent || '';
    const statusClass = document.getElementById('apiStatusIndicator')?.className || '';
    const banner = document.getElementById('globalAlertBanner');
    const bannerStyle = banner ? window.getComputedStyle(banner) : null;
    checks.header = {
        apiStatusText: statusText,
        connected: statusText === 'API Connected',
        indicatorUp: statusClass.includes('status-up'),
        alertBannerHidden: banner ? banner.hidden : false,
        alertBannerDisplay: bannerStyle ? bannerStyle.display : null,
        noVisibleAlert: bannerStyle ? (bannerStyle.display === 'none' || banner.hidden === true) : false
    };

    // 2. Section 1: Executive Overview KPIs
    const kpiMonthly = document.getElementById('kpiMonthlyCost')?.textContent || '';
    const kpiOptimized = document.getElementById('kpiOptimizedCost')?.textContent || '';
    const kpiSavings = document.getElementById('kpiSavingsAmount')?.textContent || '';
    const kpiCpu = document.getElementById('kpiCpuValue')?.textContent || '';
    const kpiMem = document.getElementById('kpiMemValue')?.textContent || '';
    checks.overview = {
        kpiMonthlyCost: kpiMonthly,
        kpiOptimizedCost: kpiOptimized,
        kpiSavingsAmount: kpiSavings,
        kpiCpuValue: kpiCpu,
        kpiMemValue: kpiMem,
        loaded: kpiMonthly.length > 0 && kpiMonthly !== '--'
    };

    // 3. Section 2: Cost Allocation & Namespace Table
    const tbodyNs = document.getElementById('tbodyNamespaceCosts');
    const nsRows = tbodyNs ? tbodyNs.querySelectorAll('tr').length : 0;
    const costValBaseline = document.getElementById('costValBaseline')?.textContent || '';
    const costValOptimized = document.getElementById('costValOptimized')?.textContent || '';
    checks.costAllocation = {
        namespaceRows: nsRows,
        costValBaseline: costValBaseline,
        costValOptimized: costValOptimized,
        loaded: nsRows > 0 && costValBaseline.length > 0
    };

    // 4. Section 3: Rightsizing & Recommendations
    const recsContainer = document.getElementById('recommendationsContainer');
    const recCards = recsContainer ? recsContainer.querySelectorAll('.recommendation-card').length : 0;
    const countAll = document.getElementById('countRecsAll')?.textContent || '0';
    checks.recommendations = {
        cardCount: recCards,
        countBadge: countAll,
        loaded: recCards > 0 || parseInt(countAll) > 0
    };

    // 5. Section 4: Controlled Experiments
    const expSelect = document.getElementById('selectExperimentRun');
    const expOptions = expSelect ? expSelect.querySelectorAll('option').length : 0;
    const expContent = document.getElementById('experimentContent');
    checks.experiments = {
        optionsCount: expOptions,
        hasContent: expContent ? expContent.children.length > 0 : false,
        loaded: expOptions > 0
    };

    // 6. Section 5: Kubernetes Monitoring & Component Stack
    const statusProm = document.getElementById('statusPrometheus')?.textContent || '';
    const statusKsm = document.getElementById('statusKsm')?.textContent || '';
    const statusOpenCost = document.getElementById('statusOpenCost')?.textContent || '';
    const tbodyWorkloads = document.getElementById('tbodyWorkloads');
    const workloadRows = tbodyWorkloads ? tbodyWorkloads.querySelectorAll('tr').length : 0;
    checks.monitoring = {
        statusPrometheus: statusProm,
        statusKsm: statusKsm,
        statusOpenCost: statusOpenCost,
        workloadRows: workloadRows,
        loaded: workloadRows > 0 && statusKsm.length > 0
    };

    // 7. Section 6: Demand Forecasting
    const svgChart = document.getElementById('forecastSvgChart');
    const svgPolylines = svgChart ? svgChart.querySelectorAll('polyline, path').length : 0;
    const tbodyForecast = document.getElementById('tbodyForecastSteps');
    const forecastRows = tbodyForecast ? tbodyForecast.querySelectorAll('tr').length : 0;
    checks.forecasting = {
        svgRendered: svgPolylines > 0,
        forecastStepsRows: forecastRows,
        loaded: svgPolylines > 0 && forecastRows > 0
    };

    // 8. Drawer Interaction Check
    const drawer = document.getElementById('settingsDrawer');
    const btnToggle = document.getElementById('btnToggleSettings');
    const btnClose = document.getElementById('btnCloseSettings');
    
    // Initial: closed
    const dInit = window.getComputedStyle(drawer);
    const initClosed = drawer.hidden === true && dInit.display === 'none';

    // Open via gear button
    btnToggle.click();
    await new Promise(r => setTimeout(r, 100));
    const dOpen = window.getComputedStyle(drawer);
    const opensOk = drawer.hidden === false && dOpen.display === 'flex';

    // Close via close button
    btnClose.click();
    await new Promise(r => setTimeout(r, 100));
    const dClosed = window.getComputedStyle(drawer);
    const closesOk = drawer.hidden === true && dClosed.display === 'none';

    checks.drawer = {
        initClosed: initClosed,
        opensViaButton: opensOk,
        closesViaButton: closesOk,
        working: initClosed && opensOk && closesOk
    };

    const out = document.createElement('div');
    out.id = 'sections-verification-output';
    out.textContent = JSON.stringify(checks);
    document.body.appendChild(out);
});
</script>
"""

try:
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(orig_html.replace("</body>", probe_code + "</body>"))

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=5000",
        "--dump-dom",
        "http://127.0.0.1:8000/"
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", timeout=15)
    
    match = re.search(r'<div id="sections-verification-output">(.*?)</div>', res.stdout)
    if match:
        data = json.loads(match.group(1))
        print("===========================================================================")
        print("  DASHBOARD SECTIONS AND DRAWER LIVE STABILITY VERIFICATION")
        print("===========================================================================")
        
        # 1. Header
        h = data["header"]
        h_pass = h["connected"] and h["noVisibleAlert"]
        print(f"[{'PASS' if h_pass else 'FAIL'}] Header & Connectivity")
        print(f"       Status: {h['apiStatusText']} | Alert Banner Hidden: {h['alertBannerHidden']} | Display: {h['alertBannerDisplay']}")

        # 2. Overview
        o = data["overview"]
        print(f"[{'PASS' if o['loaded'] else 'FAIL'}] Section 1: Executive FinOps Overview")
        print(f"       Monthly Spend: {o['kpiMonthlyCost']} | Optimized: {o['kpiOptimizedCost']} | Monthly Savings: {o['kpiSavingsAmount']}")
        print(f"       CPU Request: {o['kpiCpuValue']} | Mem Request: {o['kpiMemValue']}")

        # 3. Cost Allocation
        c = data["costAllocation"]
        print(f"[{'PASS' if c['loaded'] else 'FAIL'}] Section 2: Cost Allocation & Comparison")
        print(f"       Namespace Breakdown Rows: {c['namespaceRows']} | Baseline: {c['costValBaseline']} | Optimized: {c['costValOptimized']}")

        # 4. Recommendations
        r = data["recommendations"]
        print(f"[{'PASS' if r['loaded'] else 'FAIL'}] Section 3: Rightsizing & Recommendations")
        print(f"       Recommendation Cards: {r['cardCount']} | Total Count Badge: {r['countBadge']}")

        # 5. Experiments
        e = data["experiments"]
        print(f"[{'PASS' if e['loaded'] else 'FAIL'}] Section 4: Controlled Experiments Benchmark")
        print(f"       Runs Loaded: {e['optionsCount']} runs | Artifact Details Visible: {e['hasContent']}")

        # 6. Monitoring
        m = data["monitoring"]
        print(f"[{'PASS' if m['loaded'] else 'FAIL'}] Section 5: Component Monitoring & Topology")
        print(f"       KSM: {m['statusKsm']} | OpenCost: {m['statusOpenCost']} | Prometheus: {m['statusPrometheus']}")
        print(f"       Workload Rows: {m['workloadRows']}")

        # 7. Forecasting
        f = data["forecasting"]
        print(f"[{'PASS' if f['loaded'] else 'FAIL'}] Section 6: Demand Forecasting (Holt Linear Trend)")
        print(f"       SVG Polyline Elements: {f['svgRendered']} | Forecast Steps Table Rows: {f['forecastStepsRows']}")

        # 8. Drawer
        d = data["drawer"]
        print(f"[{'PASS' if d['working'] else 'FAIL'}] Configuration Drawer Interaction")
        print(f"       Initial Closed: {d['initClosed']} | Opens via Gear: {d['opensViaButton']} | Closes via X: {d['closesViaButton']}")

        print("===========================================================================")
        all_ok = h_pass and o['loaded'] and c['loaded'] and r['loaded'] and e['loaded'] and m['loaded'] and f['loaded'] and d['working']
        if all_ok:
            print("[SUCCESS] All 6 dashboard sections and configuration drawer verified active.")
        else:
            print("[FAIL] One or more sections failed verification.")
            exit(1)
    else:
        print("[FAIL] Output not captured from DOM.")
        print(res.stdout[:500])
        exit(1)
finally:
    if os.path.exists(BACKUP_PATH):
        shutil.copyfile(BACKUP_PATH, INDEX_PATH)
        os.remove(BACKUP_PATH)
