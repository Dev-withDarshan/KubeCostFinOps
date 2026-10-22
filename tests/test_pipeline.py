"""
test_pipeline.py — Comprehensive Unit Tests for the FinOps Data Ingestion Pipeline

Validates HTTP handling, exposition parsing, provenance schemas, atomic export,
error handling, and financial modeling disclaimers using deterministic mocked fixtures.

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import csv
import io
import json
import os
import tempfile
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

from src.finops_engine.pipeline import (
    DEFAULT_KSM_ENDPOINT,
    FINANCIAL_DISCLAIMER,
    SCHEMA_VERSION,
    KSMConnectionError,
    KSMDataError,
    build_k8s_state_snapshot,
    export_snapshot_csv,
    export_snapshot_json,
    fetch_ksm_exposition,
    generate_pipeline_snapshot,
    main,
    run_pipeline_once,
)

# Sample deterministic Prometheus exposition fixture matching actual KSM v2.12.0 output
SAMPLE_KSM_EXPOSITION = (
    "# HELP kube_pod_container_resource_requests The number of requested request resource by a container.\n"
    "# TYPE kube_pod_container_resource_requests gauge\n"
    'kube_pod_container_resource_requests{namespace="edusaas",pod="lms-api-7b8f-1",container="api",resource="cpu",unit="core"} 0.25\n'
    'kube_pod_container_resource_requests{namespace="edusaas",pod="lms-api-7b8f-1",container="api",resource="memory",unit="byte"} 268435456\n'
    'kube_pod_container_resource_requests{namespace="monitoring",pod="kube-state-metrics-abc",container="ksm",resource="cpu",unit="core"} 0.05\n'
    'kube_pod_container_resource_requests{namespace="monitoring",pod="kube-state-metrics-abc",container="ksm",resource="memory",unit="byte"} 67108864\n'
    "# HELP kube_pod_container_resource_limits The number of requested limit resource by a container.\n"
    "# TYPE kube_pod_container_resource_limits gauge\n"
    'kube_pod_container_resource_limits{namespace="edusaas",pod="lms-api-7b8f-1",container="api",resource="cpu",unit="core"} 0.5\n'
    'kube_pod_container_resource_limits{namespace="edusaas",pod="lms-api-7b8f-1",container="api",resource="memory",unit="byte"} 536870912\n'
    "# HELP kube_pod_info Information about pod.\n"
    "# TYPE kube_pod_info gauge\n"
    'kube_pod_info{namespace="edusaas",pod="lms-api-7b8f-1",uid="uuid-1",host_ip="172.18.0.2",pod_ip="10.244.0.10",node="worker-node-1"} 1\n'
    'kube_pod_info{namespace="monitoring",pod="kube-state-metrics-abc",uid="uuid-2",host_ip="172.18.0.2",pod_ip="10.244.0.5",node="worker-node-1"} 1\n'
    "# HELP kube_pod_status_phase The pods current phase.\n"
    "# TYPE kube_pod_status_phase gauge\n"
    'kube_pod_status_phase{namespace="edusaas",pod="lms-api-7b8f-1",phase="Running"} 1\n'
    "# HELP kube_deployment_status_replicas The number of replicas per deployment.\n"
    "# TYPE kube_deployment_status_replicas gauge\n"
    'kube_deployment_status_replicas{namespace="edusaas",deployment="lms-api"} 2\n'
    "# HELP kube_node_status_condition The condition of a cluster node.\n"
    "# TYPE kube_node_status_condition gauge\n"
    'kube_node_status_condition{node="worker-node-1",condition="Ready",status="true"} 1\n'
    'kube_node_status_condition{node="worker-node-1",condition="MemoryPressure",status="false"} 1\n'
)


class TestKSMDataPipeline(unittest.TestCase):
    """Unit test suite verifying all 12 required pipeline capabilities."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    # 1. Valid metrics response parsing
    def test_valid_metrics_response_parsing(self):
        """Pipeline must accurately parse valid KSM exposition metrics into structured state."""
        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION, source_endpoint="http://127.0.0.1:8080/metrics")
        observed = snapshot["observed_k8s_state"]

        self.assertEqual(observed["container_count"], 2)
        self.assertIn("edusaas", observed["namespaces"])
        self.assertIn("monitoring", observed["namespaces"])
        self.assertAlmostEqual(observed["total_requested_cpu_cores"], 0.30, places=2)
        # 268435456 + 67108864 = 335544320 bytes
        self.assertEqual(observed["total_requested_memory_bytes"], 335544320)
        self.assertEqual(observed["deployments"]["edusaas/lms-api"], 2)

    # 2. HTTP failure handling
    @patch("urllib.request.urlopen")
    def test_http_failure_handling(self, mock_urlopen):
        """Pipeline must raise KSMConnectionError on HTTP 404 or 500 errors."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://127.0.0.1:8080/metrics",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=io.BytesIO(b"Server error"),
        )
        with self.assertRaises(KSMConnectionError) as ctx:
            fetch_ksm_exposition("http://127.0.0.1:8080/metrics")
        self.assertIn("HTTP 500", str(ctx.exception))

    # 3. Timeout handling
    @patch("urllib.request.urlopen")
    def test_timeout_handling(self, mock_urlopen):
        """Pipeline must catch timeout errors and raise KSMConnectionError with duration."""
        mock_urlopen.side_effect = TimeoutError("Connection timed out")
        with self.assertRaises(KSMConnectionError) as ctx:
            fetch_ksm_exposition("http://127.0.0.1:8080/metrics", timeout=2.5)
        self.assertIn("timed out after 2.5 seconds", str(ctx.exception))

    # 4. Malformed exposition data
    @patch("urllib.request.urlopen")
    def test_malformed_exposition_data(self, mock_urlopen):
        """Pipeline must reject HTML error documents disguised as exposition text."""
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = b"<!DOCTYPE html><html><body>Error 404 Not Found</body></html>"
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        with self.assertRaises(KSMDataError) as ctx:
            fetch_ksm_exposition("http://127.0.0.1:8080/metrics")
        self.assertIn("HTML webpage instead of Prometheus exposition", str(ctx.exception))

    # 5. Empty but valid responses
    def test_empty_valid_response(self):
        """Pipeline must gracefully handle an empty metrics payload without crashing."""
        empty_metrics = "# No metrics exposed\n"
        snapshot = generate_pipeline_snapshot(empty_metrics, source_endpoint="http://127.0.0.1:8080/metrics")

        self.assertEqual(snapshot["metadata"]["collection_status"], "SUCCESS")
        self.assertEqual(snapshot["observed_k8s_state"]["container_count"], 0)
        self.assertEqual(snapshot["observed_k8s_state"]["total_requested_cpu_cores"], 0.0)
        self.assertEqual(snapshot["modeled_financial_estimates"]["total_monthly_cost_usd"], 0.0)

    # 6. Snapshot schema and provenance fields
    def test_snapshot_schema_and_provenance(self):
        """Snapshot must contain full provenance metadata and adhere to schema version 1.0.0."""
        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION, source_endpoint="http://127.0.0.1:8080/metrics")
        meta = snapshot["metadata"]

        self.assertEqual(meta["schema_version"], SCHEMA_VERSION)
        self.assertEqual(meta["source_endpoint"], "http://127.0.0.1:8080/metrics")
        self.assertEqual(meta["collection_status"], "SUCCESS")
        self.assertIn("T", meta["collection_timestamp_utc"])  # ISO 8601 UTC
        self.assertGreater(meta["payload_bytes"], 0)
        self.assertEqual(meta["observed_container_count"], 2)
        self.assertEqual(meta["financial_disclaimer"], FINANCIAL_DISCLAIMER)

    # 7. JSON export
    def test_json_export(self):
        """export_snapshot_json must write valid, parseable JSON to the specified destination."""
        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION)
        json_file = os.path.join(self.temp_dir.name, "snapshot.json")

        written_path = export_snapshot_json(snapshot, json_file)
        self.assertTrue(os.path.isfile(written_path))

        with open(written_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        self.assertEqual(loaded["metadata"]["schema_version"], SCHEMA_VERSION)
        self.assertEqual(loaded["observed_k8s_state"]["container_count"], 2)

    # 8. CSV export
    def test_csv_export(self):
        """export_snapshot_csv must write flattened container records with correct headers."""
        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION)
        csv_file = os.path.join(self.temp_dir.name, "snapshot.csv")

        written_path = export_snapshot_csv(snapshot, csv_file)
        self.assertTrue(os.path.isfile(written_path))

        with open(written_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))

        self.assertEqual(len(reader), 2)
        first_row = reader[0]
        self.assertIn("namespace", first_row)
        self.assertIn("pod", first_row)
        self.assertIn("container", first_row)
        self.assertIn("cpu_request_cores", first_row)
        self.assertIn("hourly_modeled_cost_usd", first_row)
        self.assertGreater(float(first_row["hourly_modeled_cost_usd"]), 0.0)
        self.assertEqual(first_row["cost_classification"], "MODELED_REQUEST_ESTIMATE")

    # 9. Output-directory creation
    def test_output_directory_creation(self):
        """Pipeline export must automatically create missing nested parent directories."""
        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION)
        nested_dir = os.path.join(self.temp_dir.name, "deeply", "nested", "finops", "snapshots")
        json_file = os.path.join(nested_dir, "test.json")

        self.assertFalse(os.path.exists(nested_dir))
        export_snapshot_json(snapshot, json_file)
        self.assertTrue(os.path.isdir(nested_dir))
        self.assertTrue(os.path.isfile(json_file))

    # 10. No accidental overwrite of unrelated files
    def test_no_accidental_overwrite(self):
        """Pipeline must preserve existing sibling files and not overwrite unrelated artifacts."""
        sibling_file = os.path.join(self.temp_dir.name, "unrelated_academic_report.docx")
        with open(sibling_file, "w", encoding="utf-8") as f:
            f.write("ORIGINAL_CONTENT")

        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION)
        snapshot_file = os.path.join(self.temp_dir.name, "ksm_snapshot_2026.json")
        export_snapshot_json(snapshot, snapshot_file)

        # Confirm sibling file is completely intact
        with open(sibling_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "ORIGINAL_CONTENT")

    # 11. Explicit failure behavior when live collection is unavailable
    @patch("urllib.request.urlopen")
    def test_explicit_failure_when_unavailable(self, mock_urlopen):
        """When connection is refused, pipeline must fail explicitly without substituting synthetic data."""
        mock_urlopen.side_effect = ConnectionRefusedError("[WinError 10061] No connection could be made")

        with self.assertRaises(KSMConnectionError) as ctx:
            run_pipeline_once(endpoint="http://127.0.0.1:8080/metrics", save_files=False)

        error_text = str(ctx.exception)
        self.assertIn("Connection refused", error_text)
        self.assertIn("kubectl port-forward -n monitoring svc/kube-state-metrics 8080:8080", error_text)

    # 12. Correct labeling of modeled costs versus measured observations
    def test_modeled_cost_labeling(self):
        """Pipeline must explicitly label costs as modeled estimates and include disclaimers."""
        snapshot = generate_pipeline_snapshot(SAMPLE_KSM_EXPOSITION)
        fin = snapshot["modeled_financial_estimates"]

        self.assertEqual(fin["financial_classification"], "MODELED_REQUEST_ESTIMATE")
        self.assertIn("Modeled request-based financial estimates", fin["disclaimer"])
        self.assertIn("AWS US-East-1", fin["pricing_reference"])

    # 13. CLI Exit codes
    def test_cli_exit_codes(self):
        """CLI must return exit code 2 on invalid arguments."""
        exit_code_invalid_timeout = main(["--timeout", "-5"])
        self.assertEqual(exit_code_invalid_timeout, 2)

        exit_code_invalid_poll = main(["--poll-interval", "-1"])
        self.assertEqual(exit_code_invalid_poll, 2)


if __name__ == "__main__":
    unittest.main()
