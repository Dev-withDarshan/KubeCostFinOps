"""
test_drawer_real_http.py - Tests live interaction with the settings drawer over HTTP (http://127.0.0.1:8000)
using Chrome DevTools Protocol or an injected evaluation script.
"""

import subprocess
import json
import time
import os

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "http://127.0.0.1:8000"

# We write a standalone test HTML file inside src/frontend/ so all relative paths (styles.css, app.js) resolve naturally
TEST_HTML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "frontend", "drawer_test_runner.html")

def test_drawer_via_chrome():
    with open("src/frontend/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    test_script = """
    <script>
    (async function() {
        const results = [];
        function record(name, passed, detail) {
            results.push({ name, passed, detail });
            console.log(`[TEST-RESULT] ${passed ? 'PASS' : 'FAIL'}: ${name} (${detail})`);
        }

        // Wait for dashboard boot & data rendering
        await new Promise(r => setTimeout(r, 800));

        const drawer = document.getElementById('settingsDrawer');
        const btnToggle = document.getElementById('btnToggleSettings');
        const btnClose = document.getElementById('btnCloseSettings');
        const btnRefresh = document.getElementById('btnRefreshAll');

        // 1. Initial State: Must be completely closed, no backdrop overlay, no pointer-events
        const s1 = window.getComputedStyle(drawer);
        const test1 = drawer.hidden === true && !drawer.classList.contains('open') && s1.display === 'none';
        record('Initial State is Closed', test1, `hidden=${drawer.hidden}, open=${drawer.classList.contains('open')}, display=${s1.display}`);

        // 2. Center of page must NOT be blocked by overlay
        const centerEl = document.elementFromPoint(window.innerWidth / 2, 200);
        const test2 = centerEl && !drawer.contains(centerEl);
        record('Center Screen Not Obstructed by Overlay', test2, `Element at (W/2, 200): <${centerEl?.tagName.toLowerCase()} class="${centerEl?.className}">`);

        // 3. Open Drawer via Gear Button
        btnToggle.click();
        await new Promise(r => setTimeout(r, 200));
        const s2 = window.getComputedStyle(drawer);
        const test3 = drawer.hidden === false && drawer.classList.contains('open') && s2.display === 'flex';
        record('Drawer Opens via Toggle Button', test3, `hidden=${drawer.hidden}, open=${drawer.classList.contains('open')}, display=${s2.display}`);

        // 4. Close Drawer via Close (X) Button
        btnClose.click();
        await new Promise(r => setTimeout(r, 200));
        const s3 = window.getComputedStyle(drawer);
        const test4 = drawer.hidden === true && !drawer.classList.contains('open') && s3.display === 'none';
        record('Drawer Closes via X Button', test4, `hidden=${drawer.hidden}, open=${drawer.classList.contains('open')}, display=${s3.display}`);

        // 5. Normal Dashboard Interaction is 100% Restored
        const rRect = btnRefresh.getBoundingClientRect();
        const elAtRefresh = document.elementFromPoint(rRect.left + 5, rRect.top + 5);
        const test5 = elAtRefresh && (elAtRefresh === btnRefresh || btnRefresh.contains(elAtRefresh));
        record('Normal Dashboard Interaction Restored (Refresh Button Clickable)', test5, `Element at refresh: <${elAtRefresh?.tagName.toLowerCase()} id="${elAtRefresh?.id}">`);

        // 6. Test Escape Key Closes Drawer
        btnToggle.click();
        await new Promise(r => setTimeout(r, 200));
        window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', bubbles: true }));
        await new Promise(r => setTimeout(r, 200));
        const s4 = window.getComputedStyle(drawer);
        const test6 = drawer.hidden === true && !drawer.classList.contains('open') && s4.display === 'none';
        record('Drawer Closes via Escape Key', test6, `hidden=${drawer.hidden}, open=${drawer.classList.contains('open')}, display=${s4.display}`);

        // 7. Test Clicking Blurred Backdrop Closes Drawer
        btnToggle.click();
        await new Promise(r => setTimeout(r, 200));
        drawer.dispatchEvent(new MouseEvent('click', { bubbles: true, target: drawer }));
        await new Promise(r => setTimeout(r, 200));
        const s5 = window.getComputedStyle(drawer);
        const test7 = drawer.hidden === true && !drawer.classList.contains('open') && s5.display === 'none';
        record('Drawer Closes via Backdrop Click', test7, `hidden=${drawer.hidden}, open=${drawer.classList.contains('open')}, display=${s5.display}`);

        // 8. Publish results element
        const div = document.createElement('div');
        div.id = 'automated-drawer-test-results';
        div.textContent = JSON.stringify(results);
        document.body.appendChild(div);
    })();
    </script>
    """

    test_html = html.replace("</body>", f"{test_script}</body>")
    with open(TEST_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(test_html)

    # Now run Chrome headless to render drawer_test_runner.html
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=4000",
        "--dump-dom",
        f"file:///{TEST_HTML_PATH.replace(os.sep, '/')}"
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")

    # Clean up test runner file
    if os.path.exists(TEST_HTML_PATH):
        os.remove(TEST_HTML_PATH)

    import re
    match = re.search(r'<div id="automated-drawer-test-results">(.*?)</div>', res.stdout)
    if not match:
        print("[FAIL] Test output not captured in rendered DOM!")
        return False

    results = json.loads(match.group(1))
    print("\n=======================================================")
    print("  GOOGLE CHROME INTERACTION TEST RESULTS (REAL ENGINE)")
    print("=======================================================")
    all_passed = True
    for r in results:
        status = "[PASS]" if r["passed"] else "[FAIL]"
        print(f"{status} {r['name']}")
        print(f"       {r['detail']}")
        if not r["passed"]:
            all_passed = False
    print("=======================================================\n")
    return all_passed

if __name__ == "__main__":
    passed = test_drawer_via_chrome()
    if not passed:
        exit(1)
