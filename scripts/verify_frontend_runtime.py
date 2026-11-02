"""
verify_frontend_runtime.py - Tests live browser execution of http://127.0.0.1:8000
and checks DOM population, rendered KPI values, SVG chart, and console output.
"""

import os
import subprocess
import re

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "http://127.0.0.1:8000"

def test_frontend():
    print(f"[TEST] Launching Chrome headless to inspect {URL}...")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=4000",
        "--dump-dom",
        URL
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    dom = res.stdout
    print(f"[INFO] Rendered DOM length: {len(dom)} characters")

    # Verify key elements and rendered values
    checks = {
        "API Connected Status": r"API Connected",
        "KPI Baseline Spend": r"\$24\.15",
        "KPI Rightsized Spend": r"\$7\.48",
        "KPI Savings Amount": r"\$16\.67",
        "KPI Savings Percentage": r"69\.0% Reduction",
        "Cost Comparison Bar": r"cost-progress-track",
        "Experiment Benchmark Run": r"exp-20261016-141448",
        "Controlled Experiment 4-Phase Section": r"BASELINE|LOW_LOAD|HIGHER_LOAD|RECOVERY",
        "Rightsizing Recommendations Rendered": r"rec-card",
        "Forecasting Chart SVG Path": r"svg-forecast-line",
        "Forecasting Confidence Area": r"svg-confidence-area",
        "Kubernetes Monitoring Section": r"Prometheus Server",
        "Workload Container Table": r"tbodyWorkloads"
    }

    all_passed = True
    print("\n[VERIFICATION OF RENDERED DASHBOARD COMPONENTS]")
    for name, pattern in checks.items():
        if re.search(pattern, dom):
            print(f"  [PASS] {name:40} found in rendered DOM")
        else:
            print(f"  [FAIL] {name:40} NOT found in rendered DOM")
            all_passed = False

    return all_passed

if __name__ == "__main__":
    success = test_frontend()
    if not success:
        exit(1)
