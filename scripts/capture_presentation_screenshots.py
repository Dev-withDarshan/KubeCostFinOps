"""
capture_presentation_screenshots.py - Captures genuine high-resolution screenshots
of the KubeCostFinOps cockpit and API endpoints for university presentation evidence.
"""

import os
import sys
import time
import subprocess
import json
import urllib.request

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_DIR = os.path.join(WORKSPACE_ROOT, "evidence", "final-presentation")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_URL = "http://127.0.0.1:8000"

def ensure_evidence_dir():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

def verify_backend():
    url = f"{BASE_URL}/api/ready"
    try:
        req = urllib.request.urlopen(url, timeout=3)
        if req.status == 200:
            data = json.loads(req.read().decode('utf-8'))
            print(f"[PASS] Backend ready: {data.get('service')} v{data.get('version')}")
            return True
    except Exception as e:
        print(f"[FAIL] Backend not accessible: {e}")
        return False
    return False

def capture_screenshot(target_file, url, window_size="1920,1080", wait_sec=2):
    dest_path = os.path.join(EVIDENCE_DIR, target_file)
    print(f"[CAPTURE] Grabbing {target_file} from {url}...")
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={window_size}",
        f"--screenshot={dest_path}",
        url
    ]
    
    # Run chrome
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(wait_sec)
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        size_kb = os.path.getsize(dest_path) / 1024
        print(f"  --> Saved: {dest_path} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"  --> Failed to capture: {res.stderr}")
        return False

def main():
    ensure_evidence_dir()
    if not verify_backend():
        sys.exit(1)
        
    print(f"\n[INFO] Starting screenshot captures using Google Chrome...")
    
    # 1. Executive Overview & Full Dashboard
    capture_screenshot("01_dashboard_executive_overview.png", BASE_URL, window_size="1920,1200")
    
    # 2. Cost Intelligence Focus (scrolled / zoomed or slightly taller window)
    capture_screenshot("02_cost_comparison_and_breakdown.png", BASE_URL, window_size="1600,1000")
    
    # 3. Full page scroll view
    capture_screenshot("03_dashboard_full_cockpit.png", BASE_URL, window_size="1920,2400")
    
    # 4. API Endpoints Raw Evidence (Rendered via JSON view or direct endpoint)
    capture_screenshot("04_api_health_endpoint.png", f"{BASE_URL}/api/health", window_size="1200,800")
    capture_screenshot("05_api_monitoring_status.png", f"{BASE_URL}/api/v1/monitoring/status", window_size="1200,800")
    capture_screenshot("06_api_cost_summary.png", f"{BASE_URL}/api/v1/costs/summary", window_size="1200,800")
    capture_screenshot("07_api_forecast_model.png", f"{BASE_URL}/api/v1/forecast?source=synthetic", window_size="1200,800")
    
    print("\n[SUCCESS] Presentation screenshot suite captured in evidence/final-presentation/")

if __name__ == "__main__":
    main()

