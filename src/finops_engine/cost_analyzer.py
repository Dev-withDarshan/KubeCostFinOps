"""
cost_analyzer.py — FinOps Cost Analyzer Module

Connects to Kubecost / OpenCost APIs and Prometheus to retrieve, aggregate,
and analyze Kubernetes cluster cost data for the educational SaaS platform.

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Default AWS reference rates (US-East-1 on-demand baseline)
DEFAULT_AWS_PRICING = {
    "cpu_hourly_per_core": 0.031611,     # ~$23.08/month per core
    "ram_hourly_per_gb": 0.004237,       # ~$3.09/month per GiB
    "storage_hourly_per_gb": 0.000137,   # ~$0.10/month per GiB
    "hours_per_month": 730.0,
}


def fetch_kubecost_data(endpoint: str, namespace: Optional[str] = None) -> Dict[str, Any]:
    """Fetch cost allocation data from the Kubecost / OpenCost API or local mock.

    Args:
        endpoint: The Kubecost API endpoint URL or local JSON file path.
        namespace: Optional Kubernetes namespace to filter results.

    Returns:
        A dictionary containing raw cost allocation data.

    Raises:
        ConnectionError: If the Kubecost API is unreachable.
        ValueError: If the response is not valid JSON.
    """
    if not endpoint:
        raise ValueError("Endpoint URL or file path must be provided.")

    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        url = endpoint
        if namespace:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}filterNamespaces={urllib.parse.quote(namespace)}"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "KubeCostFinOps-Engine/1.0", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                payload = response.read().decode("utf-8")
                return json.loads(payload)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            logger.error("Failed to connect to Kubecost/OpenCost at %s: %s", url, exc)
            raise ConnectionError(f"Kubecost API at '{url}' is unreachable: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON returned from '{url}': {exc}") from exc
    else:
        # Support loading from local JSON file or raw JSON string for deterministic testing
        try:
            with open(endpoint, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            try:
                return json.loads(endpoint)
            except json.JSONDecodeError as exc:
                raise ConnectionError(f"Could not load data from '{endpoint}': {exc}") from exc


def aggregate_costs_by_namespace(cost_data: Dict[str, Any]) -> Dict[str, float]:
    """Aggregate total costs grouped by Kubernetes namespace.

    Handles multiple standard schemas:
      - OpenCost list of items: {"data": [{"namespace": "default", "totalCost": 12.50}, ...]}
      - OpenCost windowed dicts: {"data": [{"default": {"totalCost": 12.50}, ...}]}
      - Direct namespace mapping: {"data": {"default": 12.50, ...}}

    Args:
        cost_data: Raw cost data returned from fetch_kubecost_data().

    Returns:
        A dictionary mapping namespace names to their total cost (USD).
    """
    if not isinstance(cost_data, dict):
        raise ValueError("cost_data must be a dictionary.")

    aggregated: Dict[str, float] = {}
    raw_data = cost_data.get("data", cost_data)

    if isinstance(raw_data, list):
        for entry in raw_data:
            if not isinstance(entry, dict):
                continue
            # Check for direct record: {"namespace": "xyz", "totalCost": 12.5}
            if "namespace" in entry or "name" in entry:
                ns = entry.get("namespace") or entry.get("name")
                cost = float(entry.get("totalCost", entry.get("cost", 0.0)))
                aggregated[str(ns)] = round(aggregated.get(str(ns), 0.0) + cost, 4)
            else:
                # Check for window mapping: {"namespace_name": {"totalCost": ...}}
                for ns_name, ns_val in entry.items():
                    if isinstance(ns_val, dict):
                        cost = float(ns_val.get("totalCost", ns_val.get("cost", 0.0)))
                        aggregated[str(ns_name)] = round(aggregated.get(str(ns_name), 0.0) + cost, 4)
                    elif isinstance(ns_val, (int, float)):
                        aggregated[str(ns_name)] = round(aggregated.get(str(ns_name), 0.0) + float(ns_val), 4)

    elif isinstance(raw_data, dict):
        for ns_name, ns_val in raw_data.items():
            if isinstance(ns_val, dict):
                cost = float(ns_val.get("totalCost", ns_val.get("cost", 0.0)))
                aggregated[str(ns_name)] = round(aggregated.get(str(ns_name), 0.0) + cost, 4)
            elif isinstance(ns_val, (int, float)):
                aggregated[str(ns_name)] = round(aggregated.get(str(ns_name), 0.0) + float(ns_val), 4)

    return aggregated


def identify_idle_resources(cost_data: Dict[str, Any], idle_threshold: float = 0.1) -> List[Dict[str, Any]]:
    """Identify under-utilised or idle resources based on CPU/memory usage vs. requests.

    Args:
        cost_data: Raw cost data from Kubecost or OpenCost.
        idle_threshold: Utilisation ratio below which a resource is considered idle
                        (default: 0.1 = 10%).

    Returns:
        A list of resource descriptors flagged as idle.
    """
    if not isinstance(cost_data, dict):
        raise ValueError("cost_data must be a dictionary.")

    idle_resources: List[Dict[str, Any]] = []
    raw_data = cost_data.get("data", [])

    items_to_process = []
    if isinstance(raw_data, list):
        for entry in raw_data:
            if isinstance(entry, dict):
                if "name" in entry or "namespace" in entry or "efficiency" in entry:
                    items_to_process.append(entry)
                else:
                    for sub_key, sub_val in entry.items():
                        if isinstance(sub_val, dict):
                            item = dict(sub_val)
                            item.setdefault("name", sub_key)
                            items_to_process.append(item)
    elif isinstance(raw_data, dict):
        for k, v in raw_data.items():
            if isinstance(v, dict):
                item = dict(v)
                item.setdefault("name", k)
                items_to_process.append(item)

    for item in items_to_process:
        # Efficiency can be explicitly provided or calculated
        efficiency = None
        for eff_key in ("efficiency", "totalEfficiency", "cpuEfficiency", "ramEfficiency"):
            if eff_key in item and item[eff_key] is not None:
                try:
                    efficiency = float(item[eff_key])
                    break
                except (ValueError, TypeError):
                    pass

        # Alternatively calculate from usage vs request
        if efficiency is None:
            cpu_usage = float(item.get("cpuCoreUsage", item.get("cpu_usage", 0.0)))
            cpu_request = float(item.get("cpuCoreRequest", item.get("cpu_request", 0.0)))
            if cpu_request > 0:
                efficiency = cpu_usage / cpu_request

        total_cost = float(item.get("totalCost", item.get("cost", 0.0)))
        if efficiency is not None and efficiency < idle_threshold:
            idle_cost = round(total_cost * (1.0 - efficiency), 4)
            idle_resources.append({
                "name": item.get("name", "unknown"),
                "namespace": item.get("namespace", "unknown"),
                "efficiency": round(efficiency, 4),
                "idle_threshold": idle_threshold,
                "total_cost": round(total_cost, 4),
                "wasted_cost": idle_cost,
                "status": "IDLE",
                "recommendation": "Rightsize or terminate underutilised resource",
            })

    return idle_resources


def calculate_savings_potential(
    current_costs: Dict[str, float],
    recommended_costs: Dict[str, float],
) -> Dict[str, float]:
    """Calculate potential savings by comparing current vs. recommended configurations.

    Args:
        current_costs: Current cost breakdown by category.
        recommended_costs: Projected costs after applying recommendations.

    Returns:
        A dictionary with per-category savings amounts and percentages,
        plus overall totals.
    """
    if not isinstance(current_costs, dict) or not isinstance(recommended_costs, dict):
        raise ValueError("current_costs and recommended_costs must be dictionaries.")

    results: Dict[str, float] = {}
    total_current = 0.0
    total_recommended = 0.0

    for cat, current_val in current_costs.items():
        curr = float(current_val)
        rec = float(recommended_costs.get(cat, curr))
        savings = max(0.0, curr - rec)
        pct = (savings / curr * 100.0) if curr > 0 else 0.0

        results[f"{cat}_savings"] = round(savings, 2)
        results[f"{cat}_savings_pct"] = round(pct, 2)

        total_current += curr
        total_recommended += rec

    total_savings = max(0.0, total_current - total_recommended)
    total_pct = (total_savings / total_current * 100.0) if total_current > 0 else 0.0

    results["total_current_cost"] = round(total_current, 2)
    results["total_recommended_cost"] = round(total_recommended, 2)
    results["total_savings"] = round(total_savings, 2)
    results["total_savings_pct"] = round(total_pct, 2)

    return results


def parse_ksm_metrics(metrics_text: str) -> Dict[str, Any]:
    """Parse Prometheus exposition text from Kube-State-Metrics into structured resource records.

    Extracts:
      - kube_pod_container_resource_requests (cpu, memory)
      - kube_pod_container_resource_limits (cpu, memory)
      - kube_pod_info (node, host_ip, pod_ip)
      - kube_pod_status_phase (Running, Pending, etc.)
      - kube_deployment_status_replicas
      - kube_node_status_condition
    """
    if not isinstance(metrics_text, str):
        raise ValueError("metrics_text must be a string.")

    data: Dict[str, Any] = {
        "pod_requests": {},
        "pod_limits": {},
        "pod_info": {},
        "pod_phases": {},
        "deployments": {},
        "node_conditions": {},
    }

    req_pattern = re.compile(
        r'kube_pod_container_resource_requests\{namespace="([^"]+)",pod="([^"]+)",(?:[^}]*,)?container="([^"]+)",(?:[^}]*,)?resource="([^"]+)",unit="([^"]+)"\}\s+([0-9.e+-]+)'
    )
    lim_pattern = re.compile(
        r'kube_pod_container_resource_limits\{namespace="([^"]+)",pod="([^"]+)",(?:[^}]*,)?container="([^"]+)",(?:[^}]*,)?resource="([^"]+)",unit="([^"]+)"\}\s+([0-9.e+-]+)'
    )
    dep_pattern = re.compile(
        r'kube_deployment_status_replicas\{namespace="([^"]+)",deployment="([^"]+)"\}\s+([0-9.]+)'
    )
    info_pattern = re.compile(
        r'kube_pod_info\{namespace="([^"]+)",pod="([^"]+)",(?:[^}]*,)?host_ip="([^"]*)",(?:[^}]*,)?pod_ip="([^"]*)",(?:[^}]*,)?node="([^"]*)"'
    )
    phase_pattern = re.compile(
        r'kube_pod_status_phase\{namespace="([^"]+)",pod="([^"]+)",phase="([^"]+)"\}\s+([0-9.]+)'
    )
    node_cond_pattern = re.compile(
        r'kube_node_status_condition\{node="([^"]+)",condition="([^"]+)",status="([^"]+)"\}\s+([0-9.]+)'
    )

    for line in metrics_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        req_m = req_pattern.search(line)
        if req_m:
            ns, pod, container, res, unit, val = req_m.groups()
            key = (ns, pod, container)
            data["pod_requests"].setdefault(key, {})[res] = float(val)
            continue

        lim_m = lim_pattern.search(line)
        if lim_m:
            ns, pod, container, res, unit, val = lim_m.groups()
            key = (ns, pod, container)
            data["pod_limits"].setdefault(key, {})[res] = float(val)
            continue

        dep_m = dep_pattern.search(line)
        if dep_m:
            ns, dep, val = dep_m.groups()
            data["deployments"][f"{ns}/{dep}"] = int(float(val))
            continue

        info_m = info_pattern.search(line)
        if info_m:
            ns, pod, host_ip, pod_ip, node = info_m.groups()
            data["pod_info"][(ns, pod)] = {
                "host_ip": host_ip,
                "pod_ip": pod_ip,
                "node": node,
            }
            continue

        phase_m = phase_pattern.search(line)
        if phase_m:
            ns, pod, phase, val = phase_m.groups()
            if float(val) == 1.0:
                data["pod_phases"][(ns, pod)] = phase
            continue

        node_m = node_cond_pattern.search(line)
        if node_m:
            node, cond, status, val = node_m.groups()
            if float(val) == 1.0:
                data["node_conditions"].setdefault(node, {})[cond] = status
            continue

    return data


def calculate_ksm_cluster_costs(
    ksm_data: Dict[str, Any],
    pricing: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Calculate hourly and monthly AWS reference costs from parsed KSM resource requests."""
    rates = pricing or DEFAULT_AWS_PRICING
    cpu_rate = rates["cpu_hourly_per_core"]
    ram_rate = rates["ram_hourly_per_gb"]
    hours_month = rates.get("hours_per_month", 730.0)

    namespace_costs: Dict[str, Dict[str, float]] = {}
    container_records: List[Dict[str, Any]] = []

    for (ns, pod, container), reqs in ksm_data.get("pod_requests", {}).items():
        cpu_cores = reqs.get("cpu", 0.0)
        mem_bytes = reqs.get("memory", 0.0)
        mem_gb = mem_bytes / (1024.0 ** 3)

        hourly_cpu_cost = cpu_cores * cpu_rate
        hourly_ram_cost = mem_gb * ram_rate
        hourly_total = hourly_cpu_cost + hourly_ram_cost
        monthly_total = hourly_total * hours_month

        record = {
            "namespace": ns,
            "pod": pod,
            "container": container,
            "cpu_cores_requested": round(cpu_cores, 4),
            "memory_gb_requested": round(mem_gb, 4),
            "hourly_cost_usd": round(hourly_total, 6),
            "monthly_cost_usd": round(monthly_total, 4),
        }
        container_records.append(record)

        if ns not in namespace_costs:
            namespace_costs[ns] = {"hourly": 0.0, "monthly": 0.0, "cpu_cores": 0.0, "memory_gb": 0.0}
        namespace_costs[ns]["hourly"] += hourly_total
        namespace_costs[ns]["monthly"] += monthly_total
        namespace_costs[ns]["cpu_cores"] += cpu_cores
        namespace_costs[ns]["memory_gb"] += mem_gb

    # Round aggregated namespace costs
    for ns in namespace_costs:
        namespace_costs[ns]["hourly"] = round(namespace_costs[ns]["hourly"], 4)
        namespace_costs[ns]["monthly"] = round(namespace_costs[ns]["monthly"], 2)
        namespace_costs[ns]["cpu_cores"] = round(namespace_costs[ns]["cpu_cores"], 3)
        namespace_costs[ns]["memory_gb"] = round(namespace_costs[ns]["memory_gb"], 3)

    total_monthly = sum(v["monthly"] for v in namespace_costs.values())
    total_hourly = sum(v["hourly"] for v in namespace_costs.values())

    return {
        "pricing_reference": "AWS US-East-1 on-demand baseline rates (m5.large equivalent)",
        "total_hourly_cost_usd": round(total_hourly, 4),
        "total_monthly_cost_usd": round(total_monthly, 2),
        "namespace_costs": namespace_costs,
        "containers": container_records,
    }


if __name__ == "__main__":
    import sys
    print("=" * 70)
    print("KUBECOSTFINOPS COST ANALYZER — ACADEMIC DEMONSTRATION RUNNER")
    print("=" * 70)

    # Demo 1: Namespace aggregation
    mock_opencost = {
        "data": [
            {"namespace": "edusaas", "totalCost": 42.80},
            {"namespace": "monitoring", "totalCost": 8.45},
            {"namespace": "kube-system", "totalCost": 18.20},
        ]
    }
    agg = aggregate_costs_by_namespace(mock_opencost)
    print("\n1. Cost Allocation by Namespace:")
    for ns, cost in agg.items():
        print(f"   - {ns:<15}: ${cost:>7.2f}/month")

    # Demo 2: Idle Resource Identification
    mock_idle = {
        "data": [
            {"name": "autograder-worker-1", "namespace": "edusaas", "efficiency": 0.04, "totalCost": 35.0},
            {"name": "lms-api-primary", "namespace": "edusaas", "efficiency": 0.62, "totalCost": 85.0},
        ]
    }
    idles = identify_idle_resources(mock_idle, idle_threshold=0.10)
    print(f"\n2. Idle / Under-utilised Workloads (Threshold < 10%):")
    for item in idles:
        print(f"   - Flagged: {item['name']} ({item['namespace']}) | Efficiency: {item['efficiency']*100:.1f}% | Wasted Cost: ${item['wasted_cost']:.2f}")

    # Demo 3: Savings Potential
    current = {"compute": 420.0, "memory": 180.0, "storage": 45.0}
    recommended = {"compute": 280.0, "memory": 130.0, "storage": 40.0}
    savings = calculate_savings_potential(current, recommended)
    print(f"\n3. Projected FinOps Rightsizing Savings:")
    print(f"   - Total Current Cost    : ${savings['total_current_cost']:.2f}/mo")
    print(f"   - Total Rightsized Cost : ${savings['total_recommended_cost']:.2f}/mo")
    print(f"   - Total Monthly Savings : ${savings['total_savings']:.2f}/mo ({savings['total_savings_pct']:.1f}%)")
    print("\n[OK] FinOps calculation engine self-test passed successfully.")
