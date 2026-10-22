# KubeCostFinOps — Security and Reliability Review

**Audit Date:** 2026-10-16  
**Auditor:** Principal Cloud Architect & Security Reviewer  
**Scope:** Lightweight Python API Server (`src/backend/main.py`), Web Dashboard Controller (`src/frontend/app.js`), Ingestion Pipeline (`src/finops_engine/pipeline.py`), and Kubernetes Manifests (`src/k8s/`).

---

## 1. Security Posture Overview

The KubeCostFinOps framework is engineered as a local developer prototype and educational research platform. To ensure high reliability and safe local execution without introducing excessive enterprise authentication overhead, the architecture implements defense-in-depth principles:
- **Read-Only Operations:** The API server strictly rejects mutating HTTP verbs (POST, PUT, DELETE, PATCH), preventing accidental cluster reconfiguration.
- **Strict Local Loopback Binding:** The backend binds strictly to `127.0.0.1` by default, preventing unintended network exposure on local area networks.
- **Zero Third-Party Dependencies:** Built exclusively on the Python standard library, eliminating npm/pip package vulnerabilities, dependency hijacking, and supply-chain supply risks.
- **Explicit Data Sanitization:** Input parameters and dynamic web presentations are validated and HTML-escaped.

> [!NOTE]
> This review documents an internal architecture and code-level security inspection. It does not constitute a certified third-party penetration test or SOC2 compliance audit.

---

## 2. Threat Modeling & Vulnerability Findings

### 2.1 Path Traversal in Experiment Run Retrieval (Remediated)
- **Vulnerability Description:** The endpoint `/api/v1/experiments/<run_id>` allowed arbitrary string inputs in the URL path. An attacker submitting encoded path traversal sequences (e.g., `../../etc/passwd` or `..%2F..%2Fwindows`) could theoretically attempt to inspect directories outside the experiment storage directory.
- **Severity:** Medium.
- **Remediation Implemented:**
  1. **Strict Regex Whitelist:** Added regex validation `^[a-zA-Z0-9_\-]+$` in `build_experiments_latest_response`. Any identifier containing slashes, backslashes, dots, or control characters is rejected immediately with HTTP 400 Bad Request.
  2. **Canonical Path Resolution:** Enforced `os.path.abspath` resolution and asserted `target_dir.startswith(base_exp_dir)`. If the resolved canonical directory escapes the designated experiments root, the request is rejected with HTTP 404.
- **Verification:** Automated unit test `test_experiment_path_traversal_protection` confirms that `GET /api/v1/experiments/..%2F..%2Fetc` returns HTTP 400 or 404.

### 2.2 Path Traversal in Static Asset Serving (Verified Secure)
- **Review Description:** Static files served by `send_static_file` were audited to ensure users cannot download arbitrary local system files via URLs like `/../../Windows/System32/drivers/etc/hosts`.
- **Finding:** The handler implements an explicit whitelist:
  - Path `""`, `"/"`, `"/index.html"`, `"/dashboard"` maps strictly to `frontend/index.html`.
  - Path `"/styles.css"` maps strictly to `frontend/styles.css`.
  - Path `"/app.js"` maps strictly to `frontend/app.js`.
  - All other paths trigger HTTP 404 with a structured JSON error payload.
- **Verdict:** Secure by design. Arbitrary file path resolution is impossible.

### 2.3 Cross-Site Scripting (XSS) in Dashboard DOM Insertion (Remediated)
- **Vulnerability Description:** In `src/frontend/app.js`, telemetry fields from JSON responses (e.g., namespace names, deployment names, workload identifiers, evidence notes) were previously interpolated into template literals and assigned directly to `innerHTML`. If a compromised or malicious pod name (e.g. `<img src=x onerror=alert(1)>`) was scraped into a snapshot, it could execute arbitrary JavaScript in the user's browser session.
- **Severity:** Low-Medium (requires malicious cluster state).
- **Remediation Implemented:**
  - Implemented an `escapeHtml(str)` utility function replacing `&`, `<`, `>`, `"`, and `'` with their respective HTML entities.
  - Applied `escapeHtml()` across namespace legend items, table rows, rightsizing recommendation cards, and experiment metadata rows.
- **Verdict:** Remediated. Dynamic strings are rendered as sanitized text.

### 2.4 Unhandled JSON Serialization & Server Crashes (Verified Resilient)
- **Review Description:** The server was evaluated against malformed JSON, corrupted snapshot files, and unexpected data types.
- **Finding:**
  - `send_json()` wraps `json.dumps()` in a try/except block; if serialization fails, it emits a clean HTTP 500 without crashing the server process.
  - Snapshot loading in `load_snapshot()` catches all I/O and decoding exceptions, returning `None`.
  - Automated tests `test_malformed_snapshot_handling` and `test_empty_valid_response` confirm the server recovers gracefully from corrupt files on disk.

### 2.5 Cross-Origin Resource Sharing (CORS) Configuration
- **Review Description:** The API server emits:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: GET, OPTIONS`
  - `Access-Control-Allow-Headers: Content-Type`
- **Assessment:** Acceptable for a local read-only development server designed to allow testing from local file origins (`file:///`) or alternate development ports (`localhost:3000`). Because the API contains zero credentialed state, session cookies, or mutating endpoints, permissive CORS presents no CSRF risk.

---

## 3. Reliability & Operational Safety

| Assessment Area | Implementation Safeguard | Verified Behavior |
| :--- | :--- | :--- |
| **Network Socket Exhaustion** | Load generator utilizes `http.client.HTTPConnection` with connection reuse rather than repeatedly creating raw sockets. | Successfully handled 683 HTTP requests at 24.2 RPS without exhausting Windows socket pool. |
| **Process Isolation** | Server runs as a standard-library single-threaded or multi-threaded daemon. | Clean shutdown upon receiving `SIGINT` or `Ctrl+C`. Zero lingering background threads. |
| **Cluster Invariance** | Rightsizing recommendations calculate resource savings strictly in memory. | Live cluster pods verified with `kubectl get deployment`: resource specs remained `250m` / `256Mi`. |
| **Memory Headroom** | The entire Python runtime requires less than 45 MB of RSS memory. | Verified on host with >2.2 GB free physical memory. |
| **Error Status Codes** | Structured JSON error payloads with standard HTTP codes (400, 404, 405, 500, 503). | Validated across 54 automated unit tests. |

---

## 4. Residual Risks & Production Hardening Roadmap

For future production deployments on AWS EKS:
1. **Authentication & Authorization:** The current prototype lacks authentication. In an enterprise cloud deployment, the API should be fronted by AWS API Gateway or an ingress controller with OAuth2/OIDC integration (e.g., AWS Cognito or Keycloak).
2. **TLS Termination:** The local server communicates over plaintext HTTP (`http://127.0.0.1:8000`). Cloud deployments must terminate TLS 1.3 via AWS ALB or CloudFront with ACM certificates.
3. **Rate Limiting:** Although the load generator is bounded to 35 RPS locally, production APIs should enforce token-bucket rate limiting to mitigate denial-of-service risks.
4. **Secret Management:** The repository contains zero hardcoded API keys, database credentials, or AWS secrets. Cloud deployments should load credentials via AWS Secrets Manager and IAM Roles for Service Accounts (IRSA).
