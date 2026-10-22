"""
pipeline.py — Live Kubernetes State Metrics Ingestion & FinOps Snapshot Pipeline

Ingests object-state telemetry from Kube-State-Metrics (KSM), normalizes
Kubernetes observations (pod requests, limits, phases, deployments, node conditions),
integrates with the FinOps cost modeling engine, and generates verifiable JSON and CSV snapshots.

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import argparse
import csv
import datetime
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from src.finops_engine.cost_analyzer import (
    DEFAULT_AWS_PRICING,
    calculate_ksm_cluster_costs,
    parse_ksm_metrics,
)
from src.finops_engine.recommendation_engine import (
    generate_rightsizing_recommendations,
)

logger = logging.getLogger(__name__)

# Constants and Defaults
DEFAULT_KSM_ENDPOINT = "http://127.0.0.1:8080/metrics"
DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_OUTPUT_DIR = "results"
DEFAULT_OUTPUT_PREFIX = "ksm_snapshot"
SCHEMA_VERSION = "1.0.0"
DATA_SOURCE_NAME = "Kube-State-Metrics (HTTP Prometheus Exposition)"

FINANCIAL_DISCLAIMER = (
    "Modeled request-based financial estimates calculated using public AWS US-East-1 "
    "on-demand reference rates (m5.large equivalent: $0.031611/vCPU-hr, $0.004237/GB-RAM-hr, "
    "730 operational hours/month). These do NOT represent actual cloud billing invoices, "
    "in-cluster OpenCost allocations, or measured real-time utilization."
)


class KSMConnectionError(ConnectionError):
    """Raised when Kube-State-Metrics endpoint cannot be reached or connected to."""
    pass


class KSMDataError(ValueError):
    """Raised when Kube-State-Metrics returns invalid, empty, or malformed exposition data."""
    pass


def fetch_ksm_exposition(
    endpoint: str = DEFAULT_KSM_ENDPOINT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> str:
    """Retrieve raw Prometheus exposition metrics text from Kube-State-Metrics.

    Args:
        endpoint: HTTP URL of the KSM /metrics endpoint.
        timeout: Network connect and read timeout in seconds.

    Returns:
        The raw text payload in Prometheus exposition format.

    Raises:
        KSMConnectionError: If connection is refused, times out, or host is unreachable.
        KSMDataError: If response is non-text, HTML error page, or malformed.
    """
    if not endpoint or not isinstance(endpoint, str):
        raise ValueError(f"Invalid endpoint specified: '{endpoint}'")

    parsed_url = urllib.parse.urlparse(endpoint)
    if parsed_url.scheme not in ("http", "https"):
        raise ValueError(
            f"Unsupported URL scheme '{parsed_url.scheme}' in endpoint '{endpoint}'. "
            "Must be 'http' or 'https'."
        )

    req = urllib.request.Request(
        endpoint,
        headers={
            "User-Agent": "KubeCostFinOps-Pipeline/1.0",
            "Accept": "text/plain; version=0.0.4, */*",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.status
            content_type = response.headers.get("Content-Type", "")
            raw_bytes = response.read()

    except urllib.error.HTTPError as exc:
        raise KSMConnectionError(
            f"Kube-State-Metrics HTTP error at '{endpoint}': HTTP {exc.code} {exc.reason}."
        ) from exc

    except (urllib.error.URLError, TimeoutError, ConnectionRefusedError, OSError) as exc:
        error_msg = str(exc)
        # Check for connection refused error (e.g. WinError 10061 or errno 111)
        if "10061" in error_msg or "refused" in error_msg.lower() or isinstance(exc, ConnectionRefusedError):
            raise KSMConnectionError(
                f"Failed to connect to Kube-State-Metrics at '{endpoint}': Connection refused.\n"
                "If running against a local Kind/Minikube cluster, ensure host port-forwarding is active:\n"
                "  kubectl port-forward -n monitoring svc/kube-state-metrics 8080:8080"
            ) from exc

        if "timed out" in error_msg.lower() or isinstance(exc, TimeoutError):
            raise KSMConnectionError(
                f"Connection to Kube-State-Metrics at '{endpoint}' timed out after {timeout} seconds."
            ) from exc

        raise KSMConnectionError(
            f"Failed to reach Kube-State-Metrics at '{endpoint}': {exc}"
        ) from exc

    if status_code != 200:
        raise KSMConnectionError(
            f"Kube-State-Metrics returned unexpected HTTP status {status_code} from '{endpoint}'."
        )

    # Decode payload
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise KSMDataError(
            f"Kube-State-Metrics returned binary/non-UTF-8 payload from '{endpoint}': {exc}"
        ) from exc

    # Sanity check: verify it is not an HTML error document
    stripped = text.strip()
    if stripped.startswith("<!DOCTYPE html") or stripped.startswith("<html"):
        raise KSMDataError(
            f"Kube-State-Metrics returned an HTML webpage instead of Prometheus exposition text from '{endpoint}'."
        )

    return text


def build_k8s_state_snapshot(ksm_data: Dict[str, Any]) -> Dict[str, Any]:
    """Structure parsed KSM observations into a normalized Kubernetes state document.

    Extracts nodes, namespaces, deployments, and container specifications
    strictly from observed metric families.
    """
    pod_requests = ksm_data.get("pod_requests", {})
    pod_limits = ksm_data.get("pod_limits", {})
    pod_info = ksm_data.get("pod_info", {})
    pod_phases = ksm_data.get("pod_phases", {})
    deployments = ksm_data.get("deployments", {})
    node_conditions = ksm_data.get("node_conditions", {})

    # Collect unique namespaces and nodes
    namespaces = set()
    nodes = set()
    container_records: List[Dict[str, Any]] = []

    total_cpu_requests_cores = 0.0
    total_memory_requests_bytes = 0.0

    # Build container inventory
    all_keys = set(pod_requests.keys()) | set(pod_limits.keys())
    for (ns, pod, container) in sorted(all_keys):
        namespaces.add(ns)
        reqs = pod_requests.get((ns, pod, container), {})
        limits = pod_limits.get((ns, pod, container), {})
        info = pod_info.get((ns, pod), {})
        phase = pod_phases.get((ns, pod), "Unknown")

        node = info.get("node", "unknown")
        if node and node != "unknown":
            nodes.add(node)

        cpu_req = reqs.get("cpu", 0.0)
        mem_req = reqs.get("memory", 0.0)
        cpu_lim = limits.get("cpu", 0.0)
        mem_lim = limits.get("memory", 0.0)

        total_cpu_requests_cores += cpu_req
        total_memory_requests_bytes += mem_req

        container_records.append({
            "namespace": ns,
            "pod": pod,
            "container": container,
            "node": node,
            "host_ip": info.get("host_ip", ""),
            "pod_ip": info.get("pod_ip", ""),
            "pod_phase": phase,
            "cpu_request_cores": round(cpu_req, 4),
            "memory_request_bytes": int(mem_req),
            "memory_request_gb": round(mem_req / (1024.0 ** 3), 4),
            "cpu_limit_cores": round(cpu_lim, 4),
            "memory_limit_bytes": int(mem_lim),
            "memory_limit_gb": round(mem_lim / (1024.0 ** 3), 4),
        })

    # Nodes with conditions
    node_list = []
    for node_name in sorted(nodes | set(node_conditions.keys())):
        node_list.append({
            "name": node_name,
            "conditions": node_conditions.get(node_name, {}),
        })

    return {
        "nodes": node_list,
        "namespaces": sorted(list(namespaces)),
        "deployments": deployments,
        "container_count": len(container_records),
        "total_requested_cpu_cores": round(total_cpu_requests_cores, 4),
        "total_requested_memory_bytes": int(total_memory_requests_bytes),
        "total_requested_memory_gb": round(total_memory_requests_bytes / (1024.0 ** 3), 4),
        "containers": container_records,
    }


def generate_pipeline_snapshot(
    metrics_text: str,
    source_endpoint: str = DEFAULT_KSM_ENDPOINT,
    pricing: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Parse raw KSM exposition and construct a complete FinOps snapshot.

    Clearly separates:
      1. Provenance metadata
      2. Measured Kubernetes state observations
      3. Modeled financial estimates (based on public rate cards)
      4. Simulated optimization recommendations

    Args:
        metrics_text: Raw Prometheus exposition string.
        source_endpoint: URL or file path where data was gathered.
        pricing: Optional pricing rate dictionary.

    Returns:
        Structured FinOps snapshot dictionary.
    """
    timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ksm_data = parse_ksm_metrics(metrics_text)
    observed_state = build_k8s_state_snapshot(ksm_data)
    cost_summary = calculate_ksm_cluster_costs(ksm_data, pricing=pricing)

    # Generate simulated rightsizing recommendations from requests
    usage_records = []
    for c in observed_state["containers"]:
        req_cpu = c["cpu_request_cores"]
        req_mem = c["memory_request_gb"]
        # In the absence of Prometheus/cAdvisor timeseries, evaluate against baseline profile
        peak_cpu = round(req_cpu * 0.25, 4)
        peak_mem = round(req_mem * 0.40, 4)
        usage_records.append({
            "workload": f"{c['pod']}/{c['container']}",
            "namespace": c["namespace"],
            "container": c["container"],
            "current_cpu_request": req_cpu,
            "peak_cpu_usage": peak_cpu,
            "current_memory_request_gb": req_mem,
            "peak_memory_usage_gb": peak_mem,
        })

    rightsizing_recs = generate_rightsizing_recommendations({"items": usage_records}, buffer_pct=0.20)
    simulated_savings = sum(r.get("projected_monthly_savings_usd", 0.0) for r in rightsizing_recs)

    snapshot = {
        "metadata": {
            "schema_version": SCHEMA_VERSION,
            "data_source": DATA_SOURCE_NAME,
            "collection_timestamp_utc": timestamp_utc,
            "source_endpoint": source_endpoint,
            "collection_status": "SUCCESS",
            "payload_bytes": len(metrics_text.encode("utf-8")),
            "observed_container_count": observed_state["container_count"],
            "financial_disclaimer": FINANCIAL_DISCLAIMER,
        },
        "observed_k8s_state": observed_state,
        "modeled_financial_estimates": {
            "pricing_reference": cost_summary.get("pricing_reference", "AWS US-East-1 Reference Rates"),
            "total_hourly_cost_usd": cost_summary.get("total_hourly_cost_usd", 0.0),
            "total_monthly_cost_usd": cost_summary.get("total_monthly_cost_usd", 0.0),
            "namespace_costs": cost_summary.get("namespace_costs", {}),
            "containers": cost_summary.get("containers", []),
            "financial_classification": "MODELED_REQUEST_ESTIMATE",
            "disclaimer": FINANCIAL_DISCLAIMER,
        },
        "simulated_rightsizing_estimates": {
            "total_recommendations": len(rightsizing_recs),
            "projected_monthly_savings_usd": round(simulated_savings, 2),
            "simulation_note": "Simulated request-downsizing with 20% safety buffer above peak; not realized billing savings.",
            "recommendations": rightsizing_recs,
        },
    }

    return snapshot


def export_snapshot_json(snapshot: Dict[str, Any], output_path: str) -> str:
    """Atomically write snapshot document to a JSON file.

    Args:
        snapshot: Snapshot dictionary.
        output_path: Destination JSON file path.

    Returns:
        The canonical path to the written file.
    """
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    tmp_path = f"{output_path}.tmp.{os.getpid()}"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    os.replace(tmp_path, output_path)
    return os.path.abspath(output_path)


def export_snapshot_csv(snapshot: Dict[str, Any], output_path: str) -> str:
    """Atomically write container-level state and modeled cost records to a CSV file.

    Args:
        snapshot: Snapshot dictionary containing observed_k8s_state.
        output_path: Destination CSV file path.

    Returns:
        The canonical path to the written file.
    """
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    timestamp = snapshot.get("metadata", {}).get("collection_timestamp_utc", "")
    pricing_ref = snapshot.get("modeled_financial_estimates", {}).get("pricing_reference", "")
    containers = snapshot.get("observed_k8s_state", {}).get("containers", [])

    # Map container costs from modeled_financial_estimates if present
    cost_map: Dict[Tuple[str, str, str], Dict[str, float]] = {}
    for c in snapshot.get("modeled_financial_estimates", {}).get("containers", []):
        key = (c.get("namespace", ""), c.get("pod", ""), c.get("container", ""))
        cost_map[key] = {
            "hourly_cost_usd": c.get("hourly_cost_usd", 0.0),
            "monthly_cost_usd": c.get("monthly_cost_usd", 0.0),
        }

    fieldnames = [
        "collection_timestamp_utc",
        "namespace",
        "pod",
        "container",
        "node",
        "pod_phase",
        "cpu_request_cores",
        "memory_request_bytes",
        "memory_request_gb",
        "cpu_limit_cores",
        "memory_limit_bytes",
        "memory_limit_gb",
        "hourly_modeled_cost_usd",
        "monthly_modeled_cost_usd",
        "cost_classification",
        "pricing_reference",
    ]

    tmp_path = f"{output_path}.tmp.{os.getpid()}"
    with open(tmp_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for c in containers:
            key = (c.get("namespace", ""), c.get("pod", ""), c.get("container", ""))
            cost_info = cost_map.get(key, {})

            writer.writerow({
                "collection_timestamp_utc": timestamp,
                "namespace": c.get("namespace", ""),
                "pod": c.get("pod", ""),
                "container": c.get("container", ""),
                "node": c.get("node", ""),
                "pod_phase": c.get("pod_phase", ""),
                "cpu_request_cores": c.get("cpu_request_cores", 0.0),
                "memory_request_bytes": c.get("memory_request_bytes", 0),
                "memory_request_gb": c.get("memory_request_gb", 0.0),
                "cpu_limit_cores": c.get("cpu_limit_cores", 0.0),
                "memory_limit_bytes": c.get("memory_limit_bytes", 0),
                "memory_limit_gb": c.get("memory_limit_gb", 0.0),
                "hourly_modeled_cost_usd": cost_info.get("hourly_cost_usd", 0.0),
                "monthly_modeled_cost_usd": cost_info.get("monthly_cost_usd", 0.0),
                "cost_classification": "MODELED_REQUEST_ESTIMATE",
                "pricing_reference": pricing_ref,
            })

    os.replace(tmp_path, output_path)
    return os.path.abspath(output_path)


def run_pipeline_once(
    endpoint: str = DEFAULT_KSM_ENDPOINT,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    output_prefix: str = DEFAULT_OUTPUT_PREFIX,
    pricing: Optional[Dict[str, float]] = None,
    save_files: bool = True,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Tuple[Dict[str, Any], Optional[str], Optional[str]]:
    """Execute one complete ingestion, modeling, and snapshot generation cycle.

    Args:
        endpoint: KSM metrics URL.
        output_dir: Directory where JSON/CSV will be stored.
        output_prefix: Prefix for snapshot files.
        pricing: Optional pricing rates.
        save_files: Whether to write JSON/CSV files to disk.
        timeout: Network timeout in seconds.

    Returns:
        Tuple of (snapshot_dict, json_path_or_none, csv_path_or_none).
    """
    logger.info("Fetching KSM metrics from %s (timeout=%ss)...", endpoint, timeout)
    metrics_text = fetch_ksm_exposition(endpoint=endpoint, timeout=timeout)

    snapshot = generate_pipeline_snapshot(
        metrics_text=metrics_text,
        source_endpoint=endpoint,
        pricing=pricing,
    )

    json_path = None
    csv_path = None

    if save_files:
        timestamp_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        json_filename = f"{output_prefix}_{timestamp_str}.json"
        csv_filename = f"{output_prefix}_{timestamp_str}.csv"

        json_dest = os.path.join(output_dir, json_filename)
        csv_dest = os.path.join(output_dir, csv_filename)

        json_path = export_snapshot_json(snapshot, json_dest)
        csv_path = export_snapshot_csv(snapshot, csv_dest)
        logger.info("Snapshot saved: JSON -> %s, CSV -> %s", json_path, csv_path)

    return snapshot, json_path, csv_path


def build_cli_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser with comprehensive option descriptions."""
    parser = argparse.ArgumentParser(
        prog="python -m src.finops_engine.pipeline",
        description=(
            "KubeCostFinOps Live Telemetry Ingestion & Cost Snapshot Pipeline.\n"
            "Queries Kube-State-Metrics (KSM) over HTTP, extracts container requests/limits,\n"
            "applies public cloud reference pricing models, and exports verifiable snapshots."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--endpoint", "-e",
        default=DEFAULT_KSM_ENDPOINT,
        help=f"Kube-State-Metrics HTTP exposition URL (default: {DEFAULT_KSM_ENDPOINT})",
    )
    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"HTTP connection and read timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to store output snapshots (default: '{DEFAULT_OUTPUT_DIR}')",
    )
    parser.add_argument(
        "--output-prefix", "-p",
        default=DEFAULT_OUTPUT_PREFIX,
        help=f"Filename prefix for generated snapshots (default: '{DEFAULT_OUTPUT_PREFIX}')",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Execute pipeline and output summary without writing files to disk",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=0,
        help="Polling interval in seconds for continuous monitoring. Default: 0 (one-shot mode).",
    )
    parser.add_argument(
        "--pricing-config",
        type=str,
        default=None,
        help="Optional path to custom JSON/YAML rate card configuration file.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint returning standard exit codes (0=success, 1=collection error, 2=config error)."""
    parser = build_cli_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code != 0 else 0

    if args.timeout <= 0:
        sys.stderr.write("Error: --timeout must be greater than zero.\n")
        return 2

    if args.poll_interval < 0:
        sys.stderr.write("Error: --poll-interval must be non-negative.\n")
        return 2

    # Load optional custom pricing
    pricing = None
    if args.pricing_config:
        if not os.path.isfile(args.pricing_config):
            sys.stderr.write(f"Error: Specified pricing config file not found: '{args.pricing_config}'\n")
            return 2
        try:
            with open(args.pricing_config, "r", encoding="utf-8") as f:
                pricing = json.load(f)
        except Exception as exc:
            sys.stderr.write(f"Error: Failed to parse pricing config '{args.pricing_config}': {exc}\n")
            return 2

    save_files = not args.no_save

    print("=" * 75)
    print("KUBECOSTFINOPS LIVE TELEMETRY INGESTION PIPELINE")
    print("=" * 75)
    print(f"Target Endpoint  : {args.endpoint}")
    print(f"Network Timeout  : {args.timeout}s")
    print(f"Save Snapshots   : {save_files} (Directory: {args.output_dir})")
    print(f"Execution Mode   : {'Continuous Polling (' + str(args.poll_interval) + 's)' if args.poll_interval > 0 else 'One-Shot Collection'}")
    print("=" * 75)

    try:
        iteration = 0
        while True:
            iteration += 1
            if args.poll_interval > 0:
                print(f"\n--- [Iteration {iteration} @ {datetime.datetime.now(datetime.timezone.utc).isoformat()}] ---")

            try:
                snapshot, json_p, csv_p = run_pipeline_once(
                    endpoint=args.endpoint,
                    output_dir=args.output_dir,
                    output_prefix=args.output_prefix,
                    pricing=pricing,
                    save_files=save_files,
                    timeout=args.timeout,
                )
            except KSMConnectionError as exc:
                sys.stderr.write(f"\n[COLLECTION FAILED] Network/Connection Error:\n{exc}\n")
                return 1
            except KSMDataError as exc:
                sys.stderr.write(f"\n[COLLECTION FAILED] Data Parsing Error:\n{exc}\n")
                return 1

            meta = snapshot["metadata"]
            state = snapshot["observed_k8s_state"]
            fin = snapshot["modeled_financial_estimates"]
            recs = snapshot["simulated_rightsizing_estimates"]

            print(f"[OK] Ingestion Status : {meta['collection_status']} ({meta['payload_bytes']} bytes received)")
            print(f"[OK] Observed Nodes   : {len(state['nodes'])} node(s)")
            print(f"[OK] Containers Found : {state['container_count']} active container request spec(s)")
            print(f"[OK] Total CPU Cores  : {state['total_requested_cpu_cores']:.3f} cores requested")
            print(f"[OK] Total Memory RAM : {state['total_requested_memory_gb']:.3f} GiB requested")
            print(f"[OK] Modeled Cost/mo  : ${fin['total_monthly_cost_usd']:.2f}/mo (AWS reference rate: m5.large baseline)")
            print(f"[OK] Rightsizing Opps : {recs['total_recommendations']} workload(s), simulated savings: ${recs['projected_monthly_savings_usd']:.2f}/mo")

            if json_p and csv_p:
                print(f"[OK] Exported JSON    : {json_p}")
                print(f"[OK] Exported CSV     : {csv_p}")

            if args.poll_interval <= 0:
                break

            time.sleep(args.poll_interval)

    except KeyboardInterrupt:
        print("\nPipeline execution stopped by user (SIGINT). Exiting cleanly.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
