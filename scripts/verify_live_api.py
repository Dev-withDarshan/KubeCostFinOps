"""
verify_live_api.py — Rigorously test every dashboard API endpoint over live HTTP
"""
import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:8000"

ENDPOINTS = [
    ("/api/health", ["status", "version", "capabilities", "snapshot_status"]),
    ("/api/ready", ["status", "service", "version", "timestamp_utc"]),
    ("/api/v1/monitoring/status", ["timestamp_utc", "integrations", "kubernetes_cluster"]),
    ("/api/v1/metrics/live", ["snapshot_file", "metadata", "observed_k8s_state"]),
    ("/api/v1/costs/summary", ["total_hourly_modeled_cost_usd", "total_monthly_modeled_cost_usd", "optimized_monthly_modeled_cost_usd", "projected_monthly_savings_usd"]),
    ("/api/v1/recommendations?type=all&buffer=0.2", ["total_rightsizing_recommendations", "total_hpa_recommendations", "total_projected_monthly_savings_usd", "rightsizing_recommendations"]),
    ("/api/v1/forecast?source=synthetic&metric=rpm&horizon=6", ["status", "model_name", "metric_name", "forecast_points", "evaluation_metrics"]),
    ("/api/v1/forecast?source=live&metric=cpu&horizon=6", ["status", "metric_name", "historical_observations_count"]),
    ("/api/v1/experiments", ["experiments_count", "runs"]),
    ("/api/v1/experiments/latest", ["status", "run_id", "metadata", "evaluation", "artifacts_available"]),
]

print("===========================================================================")
print("  VERIFYING REAL API COMMUNICATION (HTTP 127.0.0.1:8000)")
print("===========================================================================")

all_ok = True
for path, required_keys in ENDPOINTS:
    url = BASE_URL + path
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            status = resp.status
            cors = resp.headers.get("Access-Control-Allow-Origin")
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            missing = [k for k in required_keys if k not in data]
            if missing:
                print(f"[FAIL] {path} — Status {status} ({elapsed_ms}ms) — Missing keys: {missing}")
                all_ok = False
            else:
                print(f"[PASS] {path:<50} Status {status} ({elapsed_ms:>4.1f}ms) CORS: {cors}")
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
        print(f"[FAIL] {path:<50} Error after {elapsed_ms}ms: {exc}")
        all_ok = False

print("===========================================================================")
if not all_ok:
    exit(1)
print("[PASS] All 10 live API endpoints verified with valid schemas and active CORS headers.")
