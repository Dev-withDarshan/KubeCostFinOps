# ⚙️ Backend — KubeCostFinOps API Server

Lightweight, production-grade REST API server powering the KubeCostFinOps intelligence platform.

Built with pure Python standard-library networking (`http.server`, `urllib`, `json`), requiring **zero extra package installations** and operating with a minimal memory footprint (< 25 MB RAM).

---

## 🚀 Quickstart

### Launch the API Server
```powershell
# From the repository root
C:\Python314\python.exe -m src.backend.main --port 8000 --host 127.0.0.1
```

### Run All Unit Tests
```powershell
C:\Python314\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📡 REST API Endpoints

All endpoints are strictly **read-only** and return standard `application/json` responses.

| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | Returns service status, version, timestamp, and snapshot availability. |
| `GET` | `/api/v1/metrics/live` | None | Returns the latest collected Kubernetes state snapshot and collection provenance. |
| `GET` | `/api/v1/costs/summary` | None | Returns modeled request-based hourly/monthly cost estimates and namespace breakdowns. |
| `GET` | `/api/v1/recommendations` | `type=all\|rightsizing\|hpa`, `buffer=0.20` | Returns rightsizing and autoscaling recommendations with evidence and limitations. |
| `GET` | `/api/v1/forecast` | `source=live\|synthetic`, `metric=cpu\|memory\|rpm`, `horizon=6` | Returns statistical resource demand forecasts with strict provenance disclosures. |

---

## 🔒 Security & Limitations
1. **Read-Only Operation:** This server never scales, mutates, or deletes Kubernetes cluster objects.
2. **Cost Estimation Disclosure:** Modeled costs are request-based estimates from AWS US-East-1 reference rate cards. They are not actual AWS cloud bills.
3. **Forecasting Provenance:** Synthetic demonstration forecasts are explicitly labeled `is_synthetic: true`. Live forecasts require at least 5 distinct historical snapshot files.
