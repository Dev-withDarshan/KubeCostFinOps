"""
verify_browser_console.py - Checks for JavaScript console errors or uncaught exceptions
during live browser rendering of the FinOps dashboard.
"""

import subprocess
import re

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "http://127.0.0.1:8000"

def test_console():
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--enable-logging=stderr",
        "--v=1",
        "--virtual-time-budget=4000",
        URL
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    stderr = res.stderr
    print(f"[CONSOLE LOG LENGTH] {len(stderr)} characters")

    # Look for JS errors
    js_errors = re.findall(r"(?:Uncaught|ReferenceError|TypeError|SyntaxError|Unhandled).*$", stderr, re.MULTILINE)
    if js_errors:
        print("[FAIL] JavaScript errors found in console:")
        for err in js_errors:
            print(f"  - {err}")
        return False
    else:
        print("[PASS] ZERO Uncaught JavaScript errors detected in browser console!")
        return True

if __name__ == "__main__":
    if not test_console():
        exit(1)
