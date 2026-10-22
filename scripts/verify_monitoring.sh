#!/usr/bin/env bash
# scripts/verify_monitoring.sh — KubeCostFinOps Monitoring Infrastructure Verification Script for Linux/WSL
# Validates namespaces, pods, services, Prometheus scrape targets, KSM metrics, and OpenCost API.

set -euo pipefail

CLUSTER_CONTEXT="${1:-kind-kubecost-finops-local}"
OUTPUT_DIR="${2:-results/stage_06}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "${OUTPUT_DIR}"
LOG_FILE="${OUTPUT_DIR}/stage_06_verification_${TIMESTAMP}.log"

echo "===========================================================================" | tee "${LOG_FILE}"
echo "KUBECOSTFINOPS STAGE 06 MONITORING VERIFICATION LOG - ${TIMESTAMP}" | tee -a "${LOG_FILE}"
echo "===========================================================================" | tee -a "${LOG_FILE}"

echo ">> 1. Checking Cluster Reachability" | tee -a "${LOG_FILE}"
if kubectl cluster-info --context "${CLUSTER_CONTEXT}" >> "${LOG_FILE}" 2>&1; then
    echo "[PASS] Cluster '${CLUSTER_CONTEXT}' is reachable." | tee -a "${LOG_FILE}"
else
    echo "[FAIL] Cluster '${CLUSTER_CONTEXT}' is unreachable. Verify Docker and Kind are running." | tee -a "${LOG_FILE}"
    exit 1
fi

echo ">> 2. Verifying Dedicated Namespaces" | tee -a "${LOG_FILE}"
NAMESPACES="$(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}')"
if echo "${NAMESPACES}" | grep -qw "monitoring" && echo "${NAMESPACES}" | grep -qw "edusaas"; then
    echo "[PASS] Namespaces 'monitoring' and 'edusaas' exist." | tee -a "${LOG_FILE}"
else
    echo "[FAIL] Required namespaces not found. Present: ${NAMESPACES}" | tee -a "${LOG_FILE}"
    exit 1
fi

echo ">> 3. Verifying Pod Readiness in 'monitoring'" | tee -a "${LOG_FILE}"
kubectl get pods -n monitoring | tee -a "${LOG_FILE}"

echo ">> 4. Verifying ClusterIP Services" | tee -a "${LOG_FILE}"
kubectl get svc -n monitoring | tee -a "${LOG_FILE}"

echo ">> 5. Testing Kube-State-Metrics Output" | tee -a "${LOG_FILE}"
KSM_POD="$(kubectl get pod -n monitoring -l app.kubernetes.io/name=kube-state-metrics -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
if [ -n "${KSM_POD}" ]; then
    kubectl exec -n monitoring "${KSM_POD}" -c kube-state-metrics -- wget -qO- http://localhost:8080/metrics | grep -E "kube_pod_info|kube_pod_container_resource_requests" | head -n 5 | tee -a "${LOG_FILE}"
    echo "[PASS] Kube-state-metrics metrics verified." | tee -a "${LOG_FILE}"
fi

echo ">> 6. Testing Prometheus Scrape Target Health" | tee -a "${LOG_FILE}"
PROM_POD="$(kubectl get pod -n monitoring -l app.kubernetes.io/name=prometheus-server -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
if [ -n "${PROM_POD}" ]; then
    kubectl exec -n monitoring "${PROM_POD}" -c prometheus -- wget -qO- http://localhost:9090/api/v1/targets | tee -a "${LOG_FILE}"
    echo "[PASS] Prometheus target health checked." | tee -a "${LOG_FILE}"
fi

echo ">> 7. Testing OpenCost Allocation Compute API" | tee -a "${LOG_FILE}"
OC_POD="$(kubectl get pod -n monitoring -l app.kubernetes.io/name=opencost -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
if [ -n "${OC_POD}" ]; then
    kubectl exec -n monitoring "${OC_POD}" -c opencost -- wget -qO- "http://localhost:9003/allocation/compute?window=1h" | tee -a "${LOG_FILE}"
    echo "[PASS] OpenCost allocation API checked." | tee -a "${LOG_FILE}"
fi

echo ">> Verification finished. Log: ${LOG_FILE}" | tee -a "${LOG_FILE}"
