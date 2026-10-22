# BCSE355L Final Project Release Deliverable Package
**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Course:** BCSE355L — Cloud Architecture Design  
**Institution:** Vellore Institute of Technology, Vellore  
**Release Tag:** submission-final-release-2026  
**Generated:** 2026-10-22T05:03:55.455212+00:00  

---

## 1. Release Manifest & Authoritative Files
This directory (`release/BCSE355L_KubeCostFinOps_Final/`) contains the authoritative submission package for final grading and academic evaluation:

1. `BCSE355L_Kubernetes_FinOps_Final_Report.pdf` — Primary authoritative 59-page final project report with formal figures, tables, 15 scholarly literature analyses, methodology, and experiment results.
2. `BCSE355L_Kubernetes_FinOps_Final_Report.docx` — OpenXML source format matching the VIT Final Project Report Template.
3. `BCSE355L_Final_Project_Report_K_Darshan.pdf / .docx` — Personalized student submission copies for Project Lead K. Darshan (24BIT0119).
4. `evidence/` — Direct empirical benchmark artifacts (`exp-20261016-141448`), adverse stress test artifacts (`exp-20261016-141118`), and cluster telemetry state snapshot.
5. `SHA256SUMS.txt` — Cryptographic checksum verification file.
6. `VALIDATION_MANIFEST.json` — Machine-readable validation audit record.

---

## 2. Student Team
- **K. DARSHAN** (24BIT0119) — Project Lead & Cloud Architect
- **DHANUSHKODI Y** (24BIT0143) — Backend Developer & DevOps Engineer
- **T. THARUN** (24BIT0155) — ML Engineer & Data Pipeline Developer
- **S. SANJAY** (24BIT0315) — Frontend Developer & Documentation Lead

---

## 3. Independent Verification & Reproduction Instructions
To independently verify the test suite, release checks, and forensic experiment math from the workspace root:

```powershell
# 1. Run all 54 unit tests:
python -m unittest discover tests -v

# 2. Run all 28 release readiness verification checks:
python scripts/final_check.py --run-tests

# 3. Mathematically verify primary empirical run:
python scripts/validate_experiment.py --dir results/experiments/exp-20261016-141448

# 4. Mathematically verify adverse counter-evidence run:
python scripts/validate_experiment.py --dir results/experiments/exp-20261016-141118

# 5. Launch the live interactive FinOps Web Dashboard:
python src/backend/main.py --port 8000
# Open browser at: http://localhost:8000
```

---

## 4. Key Verified Results
- **Empirical Peak CPU Utilization:** 15.16 millicores (6.06% of requested spec).
- **Empirical Peak Memory Utilization:** 6.45 MiB (2.52% of requested spec).
- **Modeled Baseline Monthly Cost:** $13.0845 ($13.08)
- **Modeled Rightsized Monthly Cost:** $2.6942 ($2.69)
- **Modeled Monthly Savings:** $10.3903 ($10.39) -> 79.4% reduction (79.41% unrounded).
- **Adverse Run Transparency:** At 30 RPS (run `exp-20261016-141118`), client timeouts occurred while container CPU/RAM remained non-saturated. The precise failure mechanism remains inconclusive, and application capacity limits are conservatively documented.
