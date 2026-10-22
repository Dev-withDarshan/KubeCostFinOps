# Stage 06: Static Validation Report (Level A)

**Execution Timestamp:** `2026-10-20T14:07:17.373741+00:00`

**Status:** `29 / 29 Checks Passed (100%)`

## Summary Matrix

| Category | Total Checks | Passed | Failed |
| :--- | :--- | :--- | :--- |
| `manifest_checks` | 15 | 15 | 0 |
| `cross_reference_checks` | 5 | 5 | 0 |
| `rbac_checks` | 3 | 3 | 0 |
| `image_version_checks` | 3 | 3 | 0 |
| `resource_sizing_checks` | 3 | 3 | 0 |
| **Overall** | **29** | **29** | **0** |

## Detailed Item Results

### `manifest_checks`

| Verification Item | Status | Verification Details |
| :--- | :--- | :--- |
| `kind-config.yaml` | **PASS** | 1 document(s) parsed successfully |
| `src/k8s/namespace.yaml` | **PASS** | 4 document(s) parsed successfully |
| `src/k8s/monitoring/ksm.yaml` | **PASS** | 5 document(s) parsed successfully |
| `src/k8s/monitoring/prometheus.yaml` | **PASS** | 6 document(s) parsed successfully |
| `src/k8s/monitoring/opencost.yaml` | **PASS** | 6 document(s) parsed successfully |
| `src/k8s/monitoring/opencost-helm-values.yaml` | **PASS** | 1 document(s) parsed successfully |
| `src/k8s/monitoring/metrics-server.yaml` | **PASS** | 9 document(s) parsed successfully |
| `src/k8s/deployment.yaml` | **PASS** | 1 document(s) parsed successfully |
| `src/k8s/service.yaml` | **PASS** | 1 document(s) parsed successfully |
| `src/k8s/hpa.yaml` | **PASS** | 1 document(s) parsed successfully |
| `src/k8s/ingress.yaml` | **PASS** | 1 document(s) parsed successfully |
| `monitoring/prometheus_config.yaml` | **PASS** | 1 document(s) parsed successfully |
| `src/finops_engine/kubecost_config.yaml` | **PASS** | 1 document(s) parsed successfully |
| `embedded_prometheus_yml` | **PASS** | Valid YAML. Scrape jobs: ['prometheus', 'kube-state-metrics', 'opencost', 'kubernetes-nodes-cadvisor', 'kubernetes-apiservers', 'kubernetes-pods'] |
| `embedded_opencost_pricing_json` | **PASS** | Valid JSON. Provider: AWS |

### `cross_reference_checks`

| Verification Item | Status | Verification Details |
| :--- | :--- | :--- |
| `opencost_to_prometheus_dns` | **PASS** | Endpoint matches service: http://prometheus-server.monitoring.svc.cluster.local:9090 |
| `prometheus_scrapes_ksm` | **PASS** | Target: kube-state-metrics.monitoring.svc.cluster.local:8080 |
| `prometheus_scrapes_opencost` | **PASS** | Target: opencost.monitoring.svc.cluster.local:9003 |
| `finops_config_opencost_endpoint` | **PASS** | Endpoint: http://opencost.monitoring.svc.cluster.local:9003 |
| `finops_config_prometheus_endpoint` | **PASS** | Endpoint: http://prometheus-server.monitoring.svc.cluster.local:9090 |

### `rbac_checks`

| Verification Item | Status | Verification Details |
| :--- | :--- | :--- |
| `ksm_rbac_binding` | **PASS** | SA kube-state-metrics cleanly bound to CR kube-state-metrics and Deployment |
| `prometheus_rbac_binding` | **PASS** | SA prometheus-server cleanly bound to CR prometheus-server and Deployment |
| `opencost_rbac_binding` | **PASS** | SA opencost cleanly bound to CR opencost and Deployment |

### `image_version_checks`

| Verification Item | Status | Verification Details |
| :--- | :--- | :--- |
| `ksm` | **PASS** | Image matches: registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.12.0 |
| `prometheus` | **PASS** | Image matches: prom/prometheus:v2.51.0 |
| `opencost` | **PASS** | Image matches: quay.io/kubecost1/kubecost-cost-model:v1.108.1 |

### `resource_sizing_checks`

| Verification Item | Status | Verification Details |
| :--- | :--- | :--- |
| `ksm` | **PASS** | Requests: {'cpu': '50m', 'memory': '64Mi'}, Limits: {'cpu': '200m', 'memory': '128Mi'} |
| `prometheus` | **PASS** | Requests: {'cpu': '100m', 'memory': '256Mi'}, Limits: {'cpu': '500m', 'memory': '512Mi'} |
| `opencost` | **PASS** | Requests: {'cpu': '100m', 'memory': '128Mi'}, Limits: {'cpu': '500m', 'memory': '512Mi'} |

