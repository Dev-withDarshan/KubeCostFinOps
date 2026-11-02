"""
test_survival_after_closure.py — Verifies that running START_PRESENTATION.ps1
in a dedicated PowerShell process leaves the Python backend daemon running
even after the PowerShell process terminates.
"""
import subprocess
import time
import urllib.request
import json
import os

print("--- 1. Launching START_PRESENTATION.ps1 in a separate PowerShell session ---")
cmd = [
    "powershell",
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", "START_PRESENTATION.ps1",
    "-NoBrowser"
]

# Run PowerShell to completion and wait for it to exit
proc = subprocess.run(cmd, capture_output=True, text=True)
print(f"PowerShell Process exited with return code: {proc.returncode}")
print("STDOUT tail:")
for line in proc.stdout.strip().splitlines()[-6:]:
    print("  ", line)

# Wait 2 seconds to ensure any cleanup would have occurred
time.sleep(2)

print("\n--- 2. Verifying Backend Process and Endpoints after PowerShell exit ---")
if os.path.exists(".backend.pid"):
    with open(".backend.pid", "r") as f:
        saved_pid = f.read().strip()
    print(f"Recorded Backend PID: {saved_pid}")
else:
    print("No .backend.pid file found")

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=3) as resp:
        data = json.loads(resp.read().decode())
        print(f"[PASS] /api/health HTTP {resp.status} OK — status: {data.get('status')}")
        print(f"[PASS] Service: {data.get('service')} v{data.get('version')}")
except Exception as exc:
    print(f"[FAIL] Backend unreachable: {exc}")
    exit(1)

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/ready", timeout=3) as resp:
        data = json.loads(resp.read().decode())
        print(f"[PASS] /api/ready HTTP {resp.status} OK — status: {data.get('status')}")
except Exception as exc:
    print(f"[FAIL] /api/ready unreachable: {exc}")
    exit(1)

print("\n[SUCCESS] The Python backend daemon successfully survives PowerShell window closure.")
