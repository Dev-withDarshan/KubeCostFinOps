#!/usr/bin/env bash
# scripts/setup_local_cluster.sh — KubeCostFinOps Local Cluster Setup Script for Linux/WSL
# Reproducible provisioning and deployment of local Kind cluster and monitoring stack.

set -euo pipefail

CLUSTER_NAME="${1:-kubecost-finops-local}"
CONFIG_FILE="${2:-kind-config.yaml}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "==========================================================================="
echo ">> 1. Inspecting Host Tooling and Prerequisites"
echo "==========================================================================="

command -v git >/dev/null 2>&1 && echo "[PASS] Git available: $(git --version)" || echo "[WARN] Git not found."
command -v python3 >/dev/null 2>&1 && echo "[PASS] Python available: $(python3 --version)" || echo "[WARN] Python3 not found."

if ! command -v docker >/dev/null 2>&1; then
    echo "[FAIL] Docker CLI not found. Please install Docker Engine or Docker Desktop."
    exit 1
fi
echo "[PASS] Docker CLI available."

if ! docker info >/dev/null 2>&1; then
    echo "[FAIL] Docker daemon is not running or current user lacks docker group permissions."
    echo "Remediation: start Docker daemon or execute: sudo systemctl start docker"
    exit 1
fi
echo "[PASS] Docker daemon is running."

if ! command -v kind >/dev/null 2>&1; then
    echo "[FAIL] Kind CLI not found. Please install Kind: https://kind.sigs.k8s.io/docs/user/quick-start/"
    exit 1
fi
echo "[PASS] Kind CLI available: $(kind version)"

if ! command -v kubectl >/dev/null 2>&1; then
    echo "[FAIL] kubectl CLI not found. Please install kubectl."
    exit 1
fi
echo "[PASS] kubectl CLI available."

echo "==========================================================================="
echo ">> 2. Verifying or Creating Kind Cluster: ${CLUSTER_NAME}"
echo "==========================================================================="

if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "[PASS] Kind cluster '${CLUSTER_NAME}' already exists. Preserving cluster."
else
    echo "Creating Kind cluster '${CLUSTER_NAME}' using '${CONFIG_FILE}'..."
    kind create cluster --name "${CLUSTER_NAME}" --config "${CONFIG_FILE}"
    echo "[PASS] Kind cluster '${CLUSTER_NAME}' created successfully."
fi

kubectl config use-context "kind-${CLUSTER_NAME}" >/dev/null
echo "[PASS] kubectl context set to: kind-${CLUSTER_NAME}"

echo "==========================================================================="
echo ">> 3. Applying Namespaces and Workload Quotas"
echo "==========================================================================="
kubectl apply -f src/k8s/namespace.yaml
echo "[PASS] Namespaces 'monitoring' and 'edusaas' applied."

echo "==========================================================================="
echo ">> 4. Deploying Kube-State-Metrics (KSM v2.12.0)"
echo "==========================================================================="
kubectl apply -f src/k8s/monitoring/ksm.yaml
kubectl rollout status deployment/kube-state-metrics -n monitoring --timeout=120s
echo "[PASS] Kube-state-metrics is Ready."

echo "==========================================================================="
echo ">> 5. Deploying Prometheus Server (v2.51.0)"
echo "==========================================================================="
kubectl apply -f src/k8s/monitoring/prometheus.yaml
kubectl rollout status deployment/prometheus-server -n monitoring --timeout=120s
echo "[PASS] Prometheus server is Ready."

echo "==========================================================================="
echo ">> 6. Deploying OpenCost Cost Allocation Engine (v1.108.1)"
echo "==========================================================================="
kubectl apply -f src/k8s/monitoring/opencost.yaml
kubectl rollout status deployment/opencost -n monitoring --timeout=180s
echo "[PASS] OpenCost allocation engine is Ready."

echo "==========================================================================="
echo ">> 7. Deploying EduSaaS Baseline Workload"
echo "==========================================================================="
kubectl apply -f src/k8s/deployment.yaml
kubectl apply -f src/k8s/service.yaml
kubectl apply -f src/k8s/hpa.yaml
kubectl rollout status deployment/edusaas-backend -n edusaas --timeout=120s || true
echo "[PASS] Workload manifests applied."

echo "==========================================================================="
echo ">> 8. Deployment Overview"
echo "==========================================================================="
kubectl get pods -n monitoring
echo ""
kubectl get pods -n edusaas
echo ""
kubectl get svc -n monitoring
echo ""
echo "[SUCCESS] Monitoring infrastructure setup complete."
