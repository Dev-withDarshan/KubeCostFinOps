import unittest
from typing import Any, Dict

from src.finops_engine.cost_analyzer import (
    aggregate_costs_by_namespace,
    calculate_ksm_cluster_costs,
    calculate_savings_potential,
    fetch_kubecost_data,
    identify_idle_resources,
    parse_ksm_metrics,
)
from src.finops_engine.recommendation_engine import (
    apply_recommendations,
    generate_hpa_recommendations,
    generate_rightsizing_recommendations,
    suggest_spot_instance_placement,
)


class TestCostAnalyzer(unittest.TestCase):
    """Deterministic tests for the cost_analyzer module."""

    def test_aggregate_costs_by_namespace_returns_dict(self):
        """aggregate_costs_by_namespace should return a dict keyed by namespace with aggregated sums."""
        sample_cost_data = {
            "data": [
                {"namespace": "default", "totalCost": 12.50},
                {"namespace": "monitoring", "totalCost": 8.75},
                {"namespace": "default", "totalCost": 2.50},
            ]
        }
        result = aggregate_costs_by_namespace(sample_cost_data)
        self.assertIsInstance(result, dict)
        self.assertIn("default", result)
        self.assertIn("monitoring", result)
        self.assertAlmostEqual(result["default"], 15.00, places=2)
        self.assertAlmostEqual(result["monitoring"], 8.75, places=2)

    def test_aggregate_costs_windowed_format(self):
        """aggregate_costs_by_namespace should parse OpenCost windowed dictionaries."""
        windowed_data = {
            "data": [
                {
                    "edusaas": {"totalCost": 45.20},
                    "monitoring": {"totalCost": 12.30},
                }
            ]
        }
        result = aggregate_costs_by_namespace(windowed_data)
        self.assertAlmostEqual(result["edusaas"], 45.20, places=2)
        self.assertAlmostEqual(result["monitoring"], 12.30, places=2)

    def test_identify_idle_resources_respects_threshold(self):
        """identify_idle_resources should flag resources whose efficiency is below threshold."""
        sample_data = {
            "data": [
                {"name": "idle-worker-pod", "namespace": "edusaas", "efficiency": 0.04, "totalCost": 50.0},
                {"name": "active-api-pod", "namespace": "edusaas", "efficiency": 0.65, "totalCost": 80.0},
            ]
        }
        result = identify_idle_resources(sample_data, idle_threshold=0.10)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "idle-worker-pod")
        self.assertEqual(result[0]["status"], "IDLE")
        self.assertAlmostEqual(result[0]["wasted_cost"], 48.0, places=1)

    def test_calculate_savings_potential(self):
        """calculate_savings_potential should accurately compute per-category and total savings."""
        current = {"compute": 500.0, "storage": 100.0, "network": 50.0}
        recommended = {"compute": 350.0, "storage": 80.0, "network": 45.0}

        savings = calculate_savings_potential(current, recommended)
        self.assertAlmostEqual(savings["compute_savings"], 150.0, places=2)
        self.assertAlmostEqual(savings["compute_savings_pct"], 30.0, places=1)
        self.assertAlmostEqual(savings["storage_savings"], 20.0, places=2)
        self.assertAlmostEqual(savings["total_savings"], 175.0, places=2)
        self.assertAlmostEqual(savings["total_savings_pct"], 26.92, places=1)

    def test_fetch_kubecost_data_unreachable(self):
        """fetch_kubecost_data should raise ConnectionError when endpoint cannot be reached."""
        with self.assertRaises(ConnectionError):
            fetch_kubecost_data("http://127.0.0.1:59999/nonexistent")

    def test_parse_ksm_metrics_and_calculate_costs(self):
        """parse_ksm_metrics should parse raw Prometheus exposition text and calculate costs."""
        sample_metrics = (
            '# HELP kube_pod_container_resource_requests The number of requested request resource\n'
            'kube_pod_container_resource_requests{namespace="edusaas",pod="backend-1",container="api",resource="cpu",unit="core"} 0.5\n'
            'kube_pod_container_resource_requests{namespace="edusaas",pod="backend-1",container="api",resource="memory",unit="byte"} 1073741824\n'
            'kube_deployment_status_replicas{namespace="edusaas",deployment="backend"} 2\n'
        )
        parsed = parse_ksm_metrics(sample_metrics)
        self.assertIn(("edusaas", "backend-1", "api"), parsed["pod_requests"])
        reqs = parsed["pod_requests"][("edusaas", "backend-1", "api")]
        self.assertEqual(reqs["cpu"], 0.5)
        self.assertEqual(reqs["memory"], 1073741824.0)

        # Cost calculation
        costs = calculate_ksm_cluster_costs(parsed)
        self.assertIn("edusaas", costs["namespace_costs"])
        # 0.5 core * 0.031611 = 0.0158055; 1 GiB * 0.004237 = 0.004237; Total/hr = ~0.0200425
        self.assertGreater(costs["total_hourly_cost_usd"], 0.01)
        self.assertGreater(costs["total_monthly_cost_usd"], 10.0)


class TestRecommendationEngine(unittest.TestCase):
    """Deterministic tests for the recommendation_engine module."""

    def test_generate_rightsizing_recommendations_non_empty(self):
        """Rightsizing recommendations should flag over-provisioned pods and compute savings."""
        sample_metrics = {
            "data": [
                {
                    "name": "edusaas-backend-heavy",
                    "namespace": "edusaas",
                    "container": "backend",
                    "current_cpu_request": 1.0,
                    "peak_cpu_usage": 0.20,
                    "current_memory_request_gb": 2.0,
                    "peak_memory_usage_gb": 0.50,
                }
            ]
        }
        # 20% safety buffer over 0.20 CPU -> proposed 0.24 CPU. Savings = 0.76 CPU.
        recommendations = generate_rightsizing_recommendations(sample_metrics, buffer_pct=0.2)
        self.assertEqual(len(recommendations), 1)
        rec = recommendations[0]
        self.assertEqual(rec["action"], "DOWNSIZE_REQUESTS")
        self.assertAlmostEqual(rec["proposed_cpu_request"], 0.24, places=2)
        self.assertAlmostEqual(rec["cpu_savings_cores"], 0.76, places=2)
        self.assertGreater(rec["projected_monthly_savings_usd"], 15.0)

    def test_generate_hpa_recommendations(self):
        """generate_hpa_recommendations should detect high burstiness and lower target threshold."""
        profiles = [
            {
                "deployment": "edusaas-exam-portal",
                "namespace": "edusaas",
                "avg_cpu_utilization": 25.0,
                "peak_cpu_utilization": 90.0,
                "current_min_replicas": 2,
                "current_max_replicas": 10,
                "current_target_cpu": 60,
            }
        ]
        recs = generate_hpa_recommendations(profiles)
        self.assertEqual(len(recs), 1)
        rec = recs[0]
        self.assertGreater(rec["burst_ratio"], 3.0)
        self.assertEqual(rec["proposed_target_cpu_pct"], 50)
        self.assertGreaterEqual(rec["proposed_max_replicas"], 10)

    def suggest_spot_instance_placement(self):
        """suggest_spot_instance_placement should recommend spot instances for stateless workloads."""
        node_pools = [
            {
                "name": "worker-pool-1",
                "instance_type": "m5.large",
                "lifecycle": "on-demand",
                "hourly_cost": 0.096,
                "workloads": [
                    {"name": "autograder-worker", "labels": {"tier": "batch", "workload_type": "stateless"}},
                    {"name": "database-stateful", "labels": {"tier": "storage"}},
                ],
            }
        ]
        suggestions = suggest_spot_instance_placement(node_pools)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]["workload"], "autograder-worker")
        self.assertEqual(suggestions[0]["recommended_spot_instance"], "m5.large-spot")
        self.assertEqual(suggestions[0]["discount_pct"], 70)
        self.assertGreater(suggestions[0]["projected_monthly_savings_usd"], 30.0)

    def test_apply_recommendations_dry_run(self):
        """apply_recommendations should simulate actions and calculate total projected savings."""
        sample_recs = [
            {"workload": "api-1", "namespace": "edusaas", "action": "DOWNSIZE_REQUESTS", "projected_monthly_savings_usd": 25.50},
            {"workload": "worker-1", "namespace": "edusaas", "action": "SPOT_MIGRATION", "projected_monthly_savings_usd": 42.00},
        ]
        result = apply_recommendations(sample_recs, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["total_actions"], 2)
        self.assertEqual(result["status"], "DRY_RUN_COMPLETE")
        self.assertAlmostEqual(result["projected_monthly_savings_usd"], 67.50, places=2)


if __name__ == "__main__":
    unittest.main()
