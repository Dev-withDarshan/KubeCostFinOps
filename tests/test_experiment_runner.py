"""
test_experiment_runner.py — Unit Tests for FinOps Experiment Runner

Validates:
  - Percentile calculations (p50, p95, p99) under edge and standard distributions.
  - FinOps rightsizing analysis formulation with safety margins and floor constraints.
  - Rejection of insufficient or invalid telemetry observations.
  - Modeled AWS on-demand cost calculations and savings projections.
  - Complete versioned artifact export (JSON, CSV, README.md).

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from src.finops_engine.experiment_runner import (
    calculate_percentile,
    compute_finops_analysis,
    export_experiment_results,
    generate_experiment_markdown_report,
    KubeletTelemetryCollector,
    LoadGenerator,
)


class TestPercentileCalculation(unittest.TestCase):
    """Test percentile helper function."""

    def test_empty_list_returns_zero(self):
        self.assertEqual(calculate_percentile([], 50.0), 0.0)

    def test_single_value(self):
        self.assertEqual(calculate_percentile([42.5], 50.0), 42.5)
        self.assertEqual(calculate_percentile([42.5], 95.0), 42.5)

    def test_known_distribution(self):
        # 1 to 100
        data = [float(i) for i in range(1, 101)]
        p50 = calculate_percentile(data, 50.0)
        p95 = calculate_percentile(data, 95.0)
        self.assertAlmostEqual(p50, 50.5, delta=0.5)
        self.assertAlmostEqual(p95, 95.0, delta=1.0)


class TestFinOpsAnalysis(unittest.TestCase):
    """Test recommendation and modeled cost calculation logic."""

    def test_insufficient_evidence_when_empty(self):
        res = compute_finops_analysis("edusaas-backend", "edusaas", [])
        self.assertEqual(res["status"], "INSUFFICIENT_EVIDENCE")

    def test_insufficient_evidence_when_zero_metrics(self):
        zero_obs = [{"pods": [{"observed_cpu_millicores": 0.0, "observed_memory_working_set_mib": 0.0}]}]
        res = compute_finops_analysis("edusaas-backend", "edusaas", zero_obs)
        self.assertEqual(res["status"], "INSUFFICIENT_EVIDENCE")

    def test_valid_observations_produce_downsizing_recommendation(self):
        # Peak pod CPU = 20m, peak RAM = 5Mi
        obs = [
            {
                "pods": [
                    {
                        "pod_name": "edusaas-backend-1",
                        "observed_cpu_millicores": 15.0,
                        "observed_memory_working_set_mib": 4.5,
                    },
                    {
                        "pod_name": "edusaas-backend-2",
                        "observed_cpu_millicores": 20.0,
                        "observed_memory_working_set_mib": 5.0,
                    },
                ]
            }
        ]
        res = compute_finops_analysis(
            workload="edusaas-backend",
            namespace="edusaas",
            observations=obs,
            replicas=2,
            buffer_pct=0.20,
        )

        self.assertEqual(res["status"], "RECOMMENDED")
        self.assertEqual(res["action"], "DOWNSIZE_REQUESTS")
        self.assertEqual(res["replicas"], 2)

        # Check evidence metrics
        evid = res["empirical_telemetry_evidence"]
        self.assertEqual(evid["peak_observed_cpu_millicores"], 20.0)
        self.assertEqual(evid["peak_observed_memory_mib"], 5.0)

        # 20m is 0.020 cores. 0.020 * 1.20 = 0.024 cores.
        # But minimum safety floor is 0.050 cores!
        logic = res["recommendation_logic"]
        self.assertEqual(logic["proposed_cpu_request_cores_per_replica"], 0.050)
        self.assertEqual(logic["proposed_memory_request_gib_per_replica"], 0.0625)

        # Modeled financial impact
        fin = res["modeled_financial_impact"]
        self.assertGreater(fin["current_modeled_monthly_cost_usd"], fin["proposed_modeled_monthly_cost_usd"])
        self.assertGreater(fin["projected_monthly_savings_usd"], 0.0)
        self.assertGreater(fin["savings_percentage"], 50.0)
        self.assertIn("Modeled estimate", fin["disclaimer"])


class TestArtifactExport(unittest.TestCase):
    """Test exporting all required experiment artifacts."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_all_artifacts(self):
        metadata = {
            "run_id": "exp-test-001",
            "timestamp_utc": "2026-10-16T14:00:00Z",
            "cluster": "test-cluster",
            "kubernetes_version": "v1.37.0",
            "namespace": "edusaas",
            "deployment": "edusaas-backend",
            "replicas": 2,
            "telemetry_source": "test-source",
        }
        observations = [
            {
                "timestamp_utc": "2026-10-16T14:00:02Z",
                "phase": "BASELINE",
                "elapsed_seconds": 2.0,
                "target_rps": 0,
                "concurrency": 0,
                "pods": [
                    {
                        "pod_name": "edusaas-backend-abc",
                        "observed_cpu_millicores": 10.0,
                        "observed_memory_working_set_mib": 3.5,
                        "requested_cpu_millicores": 250.0,
                        "requested_memory_mib": 256.0,
                        "cpu_utilization_pct": 4.0,
                        "memory_utilization_pct": 1.4,
                    }
                ],
                "phase_latency_p50_ms": 0.0,
                "phase_latency_p95_ms": 0.0,
                "phase_error_rate_pct": 0.0,
                "phase_throughput_rps": 0.0,
            }
        ]
        recommendations = {
            "status": "RECOMMENDED",
            "action": "DOWNSIZE_REQUESTS",
            "modeled_financial_impact": {
                "current_modeled_monthly_cost_usd": 13.09,
                "proposed_modeled_monthly_cost_usd": 2.70,
                "projected_monthly_savings_usd": 10.39,
                "savings_percentage": 79.4,
                "disclaimer": "Modeled estimate",
            },
            "empirical_telemetry_evidence": {
                "peak_observed_cpu_millicores": 10.0,
                "peak_observed_memory_mib": 3.5,
                "peak_observed_cpu_utilization_pct": 4.0,
                "peak_observed_memory_utilization_pct": 1.4,
            },
            "recommendation_logic": {
                "proposed_cpu_request_cores_per_replica": 0.050,
                "proposed_memory_request_gib_per_replica": 0.0625,
            },
        }
        evaluation = {
            "run_id": "exp-test-001",
            "phases": {
                "BASELINE": {
                    "target_rps": 0,
                    "requests_completed": 0,
                    "throughput_rps": 0.0,
                    "latency_ms_p50": 0.0,
                    "latency_ms_p95": 0.0,
                    "error_rate_pct": 0.0,
                    "avg_pod_cpu_millicores": 10.0,
                    "avg_pod_memory_mib": 3.5,
                }
            },
        }

        run_dir = export_experiment_results(
            run_id="exp-test-001",
            output_base_dir=self.test_dir,
            metadata=metadata,
            observations=observations,
            recommendations=recommendations,
            evaluation=evaluation,
        )

        expected_files = [
            "metadata.json",
            "observations.json",
            "observations.csv",
            "recommendations.json",
            "evaluation.json",
            "README.md",
        ]
        for fname in expected_files:
            fpath = os.path.join(run_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing expected file: {fname}")
            self.assertGreater(os.path.getsize(fpath), 0, f"File is empty: {fname}")

        # Check README content
        with open(os.path.join(run_dir, "README.md"), "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Experiment Evaluation Report", content)
            self.assertIn("DOWNSIZE_REQUESTS", content)
            self.assertIn("10.39", content)


if __name__ == "__main__":
    unittest.main()
