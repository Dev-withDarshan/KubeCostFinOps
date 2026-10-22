"""
test_backend_api.py — Comprehensive Unit & Integration Tests for Backend API & Forecasting

Tests:
1. API Health (snapshot available / missing)
2. Live Metrics retrieval & HTTP 503 on missing snapshot
3. Cost summary schema, namespace breakdowns, and explicit disclaimers
4. Rightsizing and HPA recommendations with evidence, assumptions, and confidence
5. Forecast endpoint with insufficient live data (explicit rejection)
6. Forecast endpoint with valid synthetic educational history
7. Invalid query parameters (HTTP 400)
8. Corrupt/malformed snapshot resilience (HTTP 500)
9. Unknown route 404 handling
10. Read-only mutation rejection (HTTP 405 for POST/PUT/DELETE)
11. Forecasting chronological sorting and input validation
12. Forecasting reproducibility and holdout metrics (MAE/RMSE)

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import datetime
import json
import os
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

from src.backend.main import (
    build_cost_summary_response,
    build_forecast_response,
    build_health_response,
    build_metrics_live_response,
    build_recommendations_response,
    build_experiments_latest_response,
    create_server,
)
from src.finops_engine.ml_forecast import (
    evaluate_forecast_holdout,
    generate_synthetic_edusaas_timeseries,
    holt_linear_trend_forecast,
    run_demand_forecast,
    validate_and_sort_timeseries,
)

SAMPLE_SNAPSHOT = {
    "metadata": {
        "schema_version": "1.0.0",
        "data_source": "Kube-State-Metrics (HTTP Prometheus Exposition)",
        "collection_timestamp_utc": "2026-10-16T06:45:30.958561+00:00",
        "source_endpoint": "http://127.0.0.1:8080/metrics",
        "collection_status": "SUCCESS",
        "payload_bytes": 123606,
        "observed_container_count": 2,
        "financial_disclaimer": "Modeled request-based financial estimates calculated using public AWS reference rates.",
    },
    "observed_k8s_state": {
        "nodes": [{"name": "node-1", "conditions": {"Ready": "true"}}],
        "namespaces": ["edusaas", "monitoring"],
        "deployments": {"edusaas/lms-api": 2},
        "container_count": 2,
        "total_requested_cpu_cores": 0.5,
        "total_requested_memory_bytes": 536870912,
        "total_requested_memory_gb": 0.5,
        "containers": [
            {
                "namespace": "edusaas",
                "pod": "lms-api-1",
                "container": "api",
                "node": "node-1",
                "cpu_request_cores": 0.25,
                "memory_request_bytes": 268435456,
                "memory_request_gb": 0.25,
            },
            {
                "namespace": "monitoring",
                "pod": "ksm-1",
                "container": "ksm",
                "node": "node-1",
                "cpu_request_cores": 0.25,
                "memory_request_bytes": 268435456,
                "memory_request_gb": 0.25,
            },
        ],
    },
    "modeled_financial_estimates": {
        "pricing_reference": "AWS US-East-1 on-demand baseline rates (m5.large equivalent)",
        "total_hourly_cost_usd": 0.0165,
        "total_monthly_cost_usd": 12.08,
        "namespace_costs": {
            "edusaas": {"hourly": 0.0082, "monthly": 6.04, "cpu_cores": 0.25, "memory_gb": 0.25},
            "monitoring": {"hourly": 0.0082, "monthly": 6.04, "cpu_cores": 0.25, "memory_gb": 0.25},
        },
        "financial_classification": "MODELED_REQUEST_ESTIMATE",
        "disclaimer": "Modeled request-based financial estimates calculated using public AWS reference rates.",
    },
    "simulated_rightsizing_estimates": {
        "total_recommendations": 2,
        "projected_monthly_savings_usd": 8.34,
        "simulation_note": "Simulated request-downsizing with 20% safety buffer above peak.",
    },
}


class TestBackendAPI(unittest.TestCase):
    """Unit and HTTP-level tests for the lightweight FinOps API server."""

    @classmethod
    def setUpClass(cls):
        # Set up a dedicated temporary directory with a valid snapshot
        cls.test_dir = tempfile.TemporaryDirectory()
        cls.results_dir = cls.test_dir.name

        cls.valid_snapshot_path = os.path.join(cls.results_dir, "ksm_snapshot_20261016_010000.json")
        with open(cls.valid_snapshot_path, "w", encoding="utf-8") as f:
            json.dump(SAMPLE_SNAPSHOT, f)

        # Bind server to port 0 (OS picks a free ephemeral port)
        cls.server = create_server(host="127.0.0.1", port=0, results_dir=cls.results_dir)
        cls.port = cls.server.server_port
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.test_dir.cleanup()

    def _http_get(self, path: str) -> Tuple[int, Dict[str, Any]]:
        """Helper to send a GET request and parse JSON."""
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "TestClient/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                code = resp.status
                body = resp.read().decode("utf-8")
                return code, json.loads(body)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8")
            return exc.code, json.loads(body)

    # 1. Health endpoint
    def test_health_endpoint_success(self):
        code, data = self._http_get("/api/health")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "UP")
        self.assertEqual(data["version"], "1.0.0")
        self.assertTrue(data["snapshot_status"]["available"])
        self.assertEqual(data["snapshot_status"]["latest_snapshot_file"], "ksm_snapshot_20261016_010000.json")

    # 2. Health endpoint when snapshot is missing
    def test_health_endpoint_no_snapshot(self):
        empty_dir = tempfile.TemporaryDirectory()
        try:
            health = build_health_response(results_dir=empty_dir.name)
            self.assertEqual(health["status"], "UP")
            self.assertFalse(health["snapshot_status"]["available"])
        finally:
            empty_dir.cleanup()

    # 3. Live metrics endpoint
    def test_metrics_live_endpoint_success(self):
        code, data = self._http_get("/api/v1/metrics/live")
        self.assertEqual(code, 200)
        self.assertIn("metadata", data)
        self.assertIn("observed_k8s_state", data)
        self.assertEqual(data["observed_k8s_state"]["container_count"], 2)

    # 4. Live metrics endpoint when missing (HTTP 503)
    def test_metrics_live_endpoint_missing(self):
        empty_dir = tempfile.TemporaryDirectory()
        try:
            status, data = build_metrics_live_response(results_dir=empty_dir.name)
            self.assertEqual(status, 503)
            self.assertEqual(data["error"], "Service Unavailable")
            self.assertIn("No Kubernetes state snapshot has been captured", data["message"])
        finally:
            empty_dir.cleanup()

    # 5. Cost summary endpoint
    def test_cost_summary_endpoint_success(self):
        code, data = self._http_get("/api/v1/costs/summary")
        self.assertEqual(code, 200)
        self.assertEqual(data["financial_classification"], "MODELED_REQUEST_ESTIMATE")
        self.assertEqual(data["total_monthly_modeled_cost_usd"], 12.08)
        self.assertIn("edusaas", data["namespace_breakdown"])
        self.assertIn("Modeled request-based", data["disclaimer"])

    # 6. Recommendations endpoint
    def test_recommendations_endpoint_all(self):
        code, data = self._http_get("/api/v1/recommendations")
        self.assertEqual(code, 200)
        self.assertIn("rightsizing_recommendations", data)
        self.assertIn("hpa_recommendations", data)
        self.assertGreater(data["total_rightsizing_recommendations"], 0)
        self.assertGreater(data["total_hpa_recommendations"], 0)

        # Check evidence and limitations
        first_rs = data["rightsizing_recommendations"][0]
        self.assertIn("evidence", first_rs)
        self.assertIn("confidence", first_rs)
        self.assertIn("limitations_notice", data)

    # 7. Recommendations filter & buffer
    def test_recommendations_filter_and_buffer(self):
        code, data = self._http_get("/api/v1/recommendations?type=rightsizing&buffer=0.15")
        self.assertEqual(code, 200)
        self.assertEqual(data["total_hpa_recommendations"], 0)
        self.assertGreater(data["total_rightsizing_recommendations"], 0)

    # 8. Forecast endpoint with insufficient live data
    def test_forecast_live_insufficient_data(self):
        # We only have 1 snapshot in results_dir, so history is < 5
        code, data = self._http_get("/api/v1/forecast?source=live")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "INSUFFICIENT_DATA")
        self.assertEqual(data["historical_observations_count"], 1)
        self.assertEqual(data["minimum_required_observations"], 5)
        self.assertIn("a minimum of 5 chronologically distinct points is strictly required", data["message"])

    # 9. Forecast endpoint with synthetic history
    def test_forecast_synthetic_success(self):
        code, data = self._http_get("/api/v1/forecast?source=synthetic&horizon=8")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "SUCCESS")
        self.assertTrue(data["is_synthetic"])
        self.assertEqual(data["data_provenance"], "SYNTHETIC_DEMO")
        self.assertEqual(data["forecast_horizon"], 8)
        self.assertEqual(len(data["forecast_points"]), 8)
        self.assertIn("SYNTHETIC DEMONSTRATION TELEMETRY", data["disclaimer"])

    # 10. Invalid parameters (HTTP 400)
    def test_invalid_parameters_400(self):
        code, data = self._http_get("/api/v1/forecast?source=invalid_source")
        self.assertEqual(code, 400)
        self.assertEqual(data["error"], "Bad Request")

        code2, data2 = self._http_get("/api/v1/forecast?horizon=-1")
        self.assertEqual(code2, 400)
        self.assertEqual(data2["error"], "Bad Request")

        code3, data3 = self._http_get("/api/v1/recommendations?buffer=not_a_number")
        self.assertEqual(code3, 400)
        self.assertEqual(data3["error"], "Bad Request")

    # 11. Malformed snapshot resilience (HTTP 500)
    def test_malformed_snapshot_handling(self):
        corrupt_dir = tempfile.TemporaryDirectory()
        try:
            bad_file = os.path.join(corrupt_dir.name, "ksm_bad.json")
            with open(bad_file, "w", encoding="utf-8") as f:
                f.write("{ INVALID JSON NOT COMPLETE ...")

            status, data = build_metrics_live_response(results_dir=corrupt_dir.name)
            self.assertEqual(status, 500)
            self.assertEqual(data["error"], "Internal Error")
        finally:
            corrupt_dir.cleanup()

    # 12. Unknown route 404
    def test_unknown_endpoint_404(self):
        code, data = self._http_get("/api/v1/nonexistent_path")
        self.assertEqual(code, 404)
        self.assertEqual(data["error"], "Not Found")
        self.assertIn("valid_endpoints", data)

    # 13. Read-only mutation rejection (HTTP 405)
    def test_read_only_mutation_rejection(self):
        req = urllib.request.Request(f"{self.base_url}/api/v1/metrics/live", method="POST", data=b'{"action":"scale"}')
        try:
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.fail(f"Expected HTTP 405, got {resp.status}")
        except urllib.error.HTTPError as exc:
            self.assertEqual(exc.code, 405)
            body = json.loads(exc.read().decode("utf-8"))
            self.assertEqual(body["error"], "Method Not Allowed")

    # 14. Static frontend asset serving
    def test_static_frontend_serving(self):
        """Server must serve dashboard index.html, styles.css, and app.js with correct MIME types."""
        # Index HTML
        req = urllib.request.Request(f"{self.base_url}/")
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/html", resp.headers.get("Content-Type", ""))
            content = resp.read().decode("utf-8")
            self.assertIn("KubeCostFinOps", content)

        # Stylesheet CSS
        req_css = urllib.request.Request(f"{self.base_url}/styles.css")
        with urllib.request.urlopen(req_css, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/css", resp.headers.get("Content-Type", ""))

        # Application JS
        req_js = urllib.request.Request(f"{self.base_url}/app.js")
        with urllib.request.urlopen(req_js, timeout=3.0) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("application/javascript", resp.headers.get("Content-Type", ""))

    # 15. Experiment latest endpoint when missing (404)
    def test_experiments_endpoint_missing_404(self):
        empty_dir = tempfile.TemporaryDirectory()
        try:
            status, data = build_experiments_latest_response(results_dir=empty_dir.name)
            self.assertEqual(status, 404)
            self.assertEqual(data["status"], "NOT_AVAILABLE")
            self.assertIn("No Kubernetes FinOps experiment run found", data["message"])
        finally:
            empty_dir.cleanup()

    # 16. Experiment latest endpoint with valid run (200)
    def test_experiments_endpoint_success(self):
        exp_dir = os.path.join(self.results_dir, "experiments", "exp-sample-01")
        os.makedirs(exp_dir, exist_ok=True)
        with open(os.path.join(exp_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump({"run_id": "exp-sample-01", "cluster": "test-cluster"}, f)
        with open(os.path.join(exp_dir, "evaluation.json"), "w", encoding="utf-8") as f:
            json.dump({"run_id": "exp-sample-01", "phases": {}}, f)
        with open(os.path.join(exp_dir, "recommendations.json"), "w", encoding="utf-8") as f:
            json.dump({"action": "DOWNSIZE_REQUESTS", "projected_monthly_savings_usd": 10.39}, f)

        code, data = self._http_get("/api/v1/experiments/latest")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "COMPLETED")
        self.assertEqual(data["run_id"], "exp-sample-01")
        self.assertEqual(data["recommendations"]["action"], "DOWNSIZE_REQUESTS")
        self.assertIn("metadata.json", data["artifacts_available"])

    # 17. Experiment listing endpoint
    def test_experiments_list_endpoint(self):
        code, data = self._http_get("/api/v1/experiments")
        self.assertEqual(code, 200)
        self.assertIn("experiments_count", data)
        self.assertGreaterEqual(data["experiments_count"], 1)
        self.assertTrue(any(r["run_id"] == "exp-sample-01" for r in data["runs"]))

    # 18. Specific experiment run lookup
    def test_experiments_specific_run_success(self):
        code, data = self._http_get("/api/v1/experiments/exp-sample-01")
        self.assertEqual(code, 200)
        self.assertEqual(data["run_id"], "exp-sample-01")
        self.assertEqual(data["status"], "COMPLETED")

    # 19. Specific experiment run not found (404)
    def test_experiments_specific_run_not_found(self):
        code, data = self._http_get("/api/v1/experiments/exp-nonexistent-999")
        self.assertEqual(code, 404)
        self.assertEqual(data["status"], "NOT_FOUND")

    # 20. Path traversal protection on experiment runs
    def test_experiment_path_traversal_protection(self):
        code, data = self._http_get("/api/v1/experiments/..%2F..%2Fetc")
        self.assertIn(code, (400, 404))

    # 21. Endpoint aliases (health, cost/monthly, forecast/demand)
    def test_endpoint_aliases(self):
        # Health alias
        code, data = self._http_get("/api/v1/health")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "UP")

        # Cost monthly alias
        code, data = self._http_get("/api/v1/cost/monthly")
        self.assertEqual(code, 200)
        self.assertEqual(data["financial_classification"], "MODELED_REQUEST_ESTIMATE")

        # Forecast demand alias
        code, data = self._http_get("/api/v1/forecast/demand?source=synthetic&horizon=4")
        self.assertEqual(code, 200)
        self.assertEqual(data["status"], "SUCCESS")


class TestForecastingModule(unittest.TestCase):
    """Unit tests for src/finops_engine/ml_forecast.py."""

    def test_validate_and_sort_chronological_ordering(self):
        """Timeseries validation must sort unordered observations and reject invalid entries."""
        unordered = [
            {"timestamp": "2026-10-16T12:00:00Z", "value": 30.0},
            {"timestamp": "2026-10-16T10:00:00Z", "value": 10.0},
            {"timestamp": "2026-10-16T11:00:00Z", "value": 20.0},
        ]
        cleaned = validate_and_sort_timeseries(unordered)
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(cleaned[0][1], 10.0)
        self.assertEqual(cleaned[1][1], 20.0)
        self.assertEqual(cleaned[2][1], 30.0)

        # Invalid entry check
        with self.assertRaises(ValueError):
            validate_and_sort_timeseries([{"timestamp": "invalid_date", "value": 10.0}])

        with self.assertRaises(ValueError):
            validate_and_sort_timeseries([{"timestamp": "2026-10-16T10:00:00Z", "value": "not_a_num"}])

    def test_forecast_reproducibility(self):
        """Forecasting algorithm must produce identical output for identical inputs."""
        history = [10.0, 12.0, 15.0, 18.0, 22.0, 25.0, 28.0]
        preds1, lvl1, trd1 = holt_linear_trend_forecast(history, horizon=4)
        preds2, lvl2, trd2 = holt_linear_trend_forecast(history, horizon=4)

        self.assertEqual(preds1, preds2)
        self.assertEqual(lvl1, lvl2)
        self.assertEqual(trd1, trd2)
        self.assertEqual(len(preds1), 4)

    def test_holdout_evaluation_metrics(self):
        """Holdout evaluation must compute valid MAE and RMSE."""
        history = [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
        metrics = evaluate_forecast_holdout(history, test_size=2)
        self.assertIsNotNone(metrics)
        self.assertIn("mae", metrics)
        self.assertIn("rmse", metrics)
        self.assertGreaterEqual(metrics["mae"], 0.0)
        self.assertGreaterEqual(metrics["rmse"], 0.0)

    def test_synthetic_edusaas_generator(self):
        """Synthetic generator must be deterministic and label provenance explicitly."""
        fixed_dt = datetime.datetime(2026, 10, 14, 0, 0, tzinfo=datetime.timezone.utc)
        bundle1 = generate_synthetic_edusaas_timeseries(num_hours=24, start_time=fixed_dt, random_seed=99)
        bundle2 = generate_synthetic_edusaas_timeseries(num_hours=24, start_time=fixed_dt, random_seed=99)

        self.assertEqual(bundle1, bundle2)
        meta = bundle1["metadata"]
        self.assertEqual(meta["data_type"], "SYNTHETIC_DEMO")
        self.assertEqual(meta["random_seed"], 99)
        self.assertEqual(len(bundle1["observations"]), 24)

        # Academic calendar feature verification
        first_obs = bundle1["observations"][0]
        self.assertIn("active_students", first_obs)
        self.assertIn("is_exam_period", first_obs)
        self.assertIn("is_assignment_deadline", first_obs)
        self.assertIn("cpu_used_m", first_obs)
        self.assertIn("memory_used_mb", first_obs)
        self.assertIn("response_time_ms", first_obs)
        self.assertIsInstance(first_obs["is_exam_period"], bool)
        self.assertIsInstance(first_obs["is_assignment_deadline"], bool)
        self.assertGreater(first_obs["active_students"], 0)
        self.assertGreater(first_obs["cpu_used_m"], 0.0)



if __name__ == "__main__":
    unittest.main()
