#!/bin/bash
set -e
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "=========================================================="
echo " Starting KubeCostFinOps Automated Cloud Setup on Ubuntu"
echo "=========================================================="

# 1. Update and install prerequisites
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y docker.io git curl python3 python3-pip

systemctl start docker
systemctl enable docker

# 2. Install kubectl
curl -LO "https://dl.k8s.io/release/v1.31.0/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin/

# 3. Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/

# 4. Clone repository
mkdir -p /opt
cd /opt
if [ -d "KubeCostFinOps" ]; then
    rm -rf KubeCostFinOps
fi
git clone https://github.com/Dev-withDarshan/KubeCostFinOps.git -b develop
cd /opt/KubeCostFinOps

# 5. Create Kind Cluster
kind create cluster --name kubecost-finops-local --image kindest/node:v1.31.0

# Wait for cluster node ready
kubectl wait --for=condition=Ready node -l node-role.kubernetes.io/control-plane --timeout=180s

# 6. Apply Workload & Monitoring Manifests
kubectl apply -f src/k8s/deployment.yaml
kubectl apply -f src/k8s/service.yaml
kubectl apply -f src/k8s/hpa.yaml
kubectl apply -f src/k8s/monitoring/prometheus.yaml
kubectl apply -f src/k8s/monitoring/kube-state-metrics.yaml
kubectl apply -f src/k8s/monitoring/opencost.yaml

# Wait for deployments to be available
kubectl wait --for=condition=Available deployment/edusaas-backend -n edusaas --timeout=180s || true
kubectl wait --for=condition=Available deployment/kube-state-metrics -n monitoring --timeout=180s || true
kubectl wait --for=condition=Available deployment/prometheus-server -n monitoring --timeout=180s || true
kubectl wait --for=condition=Available deployment/opencost -n monitoring --timeout=180s || true

# 7. Create Background Port-Forward Systemd Service
cat << 'EOF' > /etc/systemd/system/kubecost-portforwards.service
[Unit]
Description=Kubernetes Port Forwards for Monitoring Stack
After=network.target

[Service]
Type=simple
User=root
Restart=always
RestartSec=5
ExecStart=/bin/bash -c "kubectl -n monitoring port-forward svc/kube-state-metrics 8080:8080 --address 0.0.0.0 & kubectl -n monitoring port-forward svc/prometheus-server 9090:9090 --address 0.0.0.0 & kubectl -n monitoring port-forward svc/opencost 9003:9003 --address 0.0.0.0 & wait"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable kubecost-portforwards.service
systemctl start kubecost-portforwards.service

sleep 10

# 8. Ingest Initial Snapshot
python3 -m src.finops_engine.pipeline --endpoint http://127.0.0.1:8080/metrics --output-dir results || true

# 9. Create FinOps API Server Systemd Service
cat << 'EOF' > /etc/systemd/system/kubecost-finops.service
[Unit]
Description=KubeCostFinOps REST API Server & Live Dashboard
After=network.target kubecost-portforwards.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/KubeCostFinOps
ExecStart=/usr/bin/python3 -m src.backend.main --port 8000 --host 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable kubecost-finops.service
systemctl start kubecost-finops.service

# 10. Background Telemetry Collector Cron / Periodic Ingestion
cat << 'EOF' > /etc/systemd/system/kubecost-collector.service
[Unit]
Description=KubeCostFinOps Periodic Telemetry Collector

[Service]
Type=oneshot
User=root
WorkingDirectory=/opt/KubeCostFinOps
ExecStart=/usr/bin/python3 -m src.finops_engine.pipeline --endpoint http://127.0.0.1:8080/metrics --output-dir results
EOF

cat << 'EOF' > /etc/systemd/system/kubecost-collector.timer
[Unit]
Description=Run KubeCostFinOps collector every 60 seconds

[Timer]
OnBootSec=30sec
OnUnitActiveSec=60sec
Unit=kubecost-collector.service

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable kubecost-collector.timer
systemctl start kubecost-collector.timer

echo "=========================================================="
echo " KubeCostFinOps AWS Deployment Finished Successfully!"
echo " Server listening on port 8000"
echo "=========================================================="

