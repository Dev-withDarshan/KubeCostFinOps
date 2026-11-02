"""
debug_live_dashboard.py — Test real HTTP http://127.0.0.1:8000 in Chrome
"""
import subprocess
import json
import os
import re
import time
import shutil

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
INDEX_PATH = r"C:\Users\gnavy\Downloads\KubeCostFinOps\src\frontend\index.html"
BACKUP_PATH = r"C:\Users\gnavy\Downloads\KubeCostFinOps\src\frontend\index.html.bak"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    orig_html = f.read()

# Backup index.html
shutil.copyfile(INDEX_PATH, BACKUP_PATH)

probe_code = """
<script>
window.addEventListener('DOMContentLoaded', async () => {
    // Wait for all initial async fetch and renders to complete
    await new Promise(r => setTimeout(r, 1200));
    
    const banner = document.getElementById('globalAlertBanner');
    const bStyle = banner ? window.getComputedStyle(banner) : null;
    const bannerTitle = document.getElementById('alertBannerTitle')?.textContent || '';
    const bannerMsg = document.getElementById('alertBannerMsg')?.textContent || '';
    
    const statusText = document.getElementById('apiStatusText')?.textContent || '';
    const indicatorClass = document.getElementById('apiStatusIndicator')?.className || '';
    
    const kpiCost = document.getElementById('kpiMonthlyCost')?.textContent || '';
    const kpiSavings = document.getElementById('kpiSavingsAmount')?.textContent || '';
    const lsBaseUrl = localStorage.getItem('kubecost_api_base_url');
    
    const probeData = {
        bannerHiddenAttr: banner ? banner.hidden : null,
        bannerComputedDisplay: bStyle ? bStyle.display : null,
        bannerVisibleOnScreen: bStyle ? (bStyle.display !== 'none' && bStyle.visibility !== 'hidden') : null,
        bannerTitle: bannerTitle,
        bannerMsg: bannerMsg,
        apiStatusText: statusText,
        indicatorClass: indicatorClass,
        kpiMonthlyCost: kpiCost,
        kpiSavingsAmount: kpiSavings,
        localStorageApiBaseUrl: lsBaseUrl
    };
    
    const out = document.createElement('div');
    out.id = 'debug-probe-output';
    out.textContent = JSON.stringify(probeData);
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
        "--virtual-time-budget=4000",
        "--dump-dom",
        "http://127.0.0.1:8000/"
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", timeout=15)
    
    match = re.search(r'<div id="debug-probe-output">(.*?)</div>', res.stdout)
    if match:
        data = json.loads(match.group(1))
        print("PROBE_SUCCESS")
        print(json.dumps(data, indent=2))
    else:
        print("PROBE_FAILED_TO_FIND_OUTPUT")
        print("STDOUT sample:", res.stdout[:500])
        print("STDERR sample:", res.stderr[:500])
finally:
    # Always restore original index.html
    if os.path.exists(BACKUP_PATH):
        shutil.copyfile(BACKUP_PATH, INDEX_PATH)
        os.remove(BACKUP_PATH)
