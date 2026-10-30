# FINAL MASTER PROJECT HANDOFF & SUBMISSION AUDIT

**Project Title:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Course:** BCSE355L — Cloud Architecture Design  
**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Vellore  
**Project Lead:** K. Darshan (Reg No: 24BIT0119)  
**Team Members:** Dhanushkodi Y (24BIT0143), T. Tharun (24BIT0155), S. Sanjay (24BIT0315)  
**Repository:** [https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026](https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026)  
*(Canonical GitHub URL: [https://github.com/Dev-withDarshan/KubeCostFinOps](https://github.com/Dev-withDarshan/KubeCostFinOps))*  
**Active Branch:** `develop`  
**Verified Commit Hash:** `9bead7750c5d2447008c9d3170272fd9bdeb00a9`  
**Commit Message:** `feat(release): complete Phase-II & Phase-III release, 54 verified tests, 59-page report, and AWS deployment architecture`  
**Remote Push Status:** **PUSHED & UP-TO-DATE WITH ORIGIN/DEVELOP**  
**Final Status Category:** **CODE AND RELEASE READY — AWS DEPLOYMENT AWAITING COST APPROVAL**  

---

## 1. Executive Summary & Verification Verdict

All local implementation, forensic experiment validation, automated testing, academic report generation, release packaging, and remote GitHub publishing milestones are **100% complete and verified**:

1. **Automated Regression Suite:** 54 out of 54 unit and integration tests passing (`python -m unittest discover tests -v`) in 2.48s.
2. **Release Readiness Verification:** 28 out of 28 checks passing (`python scripts/final_check.py --run-tests`).
3. **Forensic Experiment Validation:** 10 out of 10 checks passing for both primary run (`exp-20261016-141448`) and adverse counter-evidence run (`exp-20261016-141118`).
4. **Academic Final Report:** 59-page comprehensive project report verified in Microsoft Word OpenXML (`.docx`) and Adobe PDF (`.pdf`), complete with 15 scholarly literature analyses, formal figures, tables, methodology, and empirical findings.
5. **Release Integrity:** Cryptographic SHA-256 release manifest (`release/BCSE355L_KubeCostFinOps_Final/SHA256SUMS.txt`) verified with **15/15 files matching 100%**.
6. **Remote Repository Synchronization:** Branch `develop` pushed to GitHub; remote confirmed at `9bead7750c5d2447008c9d3170272fd9bdeb00a9`.
7. **AWS Cloud Architecture:** Ultra-low-cost Zero-NAT Gateway EKS architecture fully designed with CloudFormation templates, Kubernetes manifests, deployment automation (`src/aws/scripts/deploy-aws.ps1`), teardown automation (`src/aws/scripts/teardown-aws.ps1`), and line-item cost modeling.
8. **AWS Cost Gate & Authentication:** AWS CLI currently has no configured credentials on the local host (`NoCredentials`). Cloud resources remain unprovisioned pending credential configuration and user cost authorization.

---

## 2. Independent Verification & Reproduction Commands

Every metric, test, and artifact is independently reproducible using standard Python and PowerShell tools:

```powershell
# ==============================================================================
# 1. RUN AUTOMATED TEST SUITE (54 Tests)
# ==============================================================================
python -m unittest discover tests -v

# ==============================================================================
# 2. RUN RELEASE READINESS CHECKER (28 Checks)
# ==============================================================================
python scripts/final_check.py --run-tests

# ==============================================================================
# 3. RUN FORENSIC EXPERIMENT VALIDATIONS (10 Checks Each)
# ==============================================================================
python scripts/validate_experiment.py --dir results/experiments/exp-20261016-141448
python scripts/validate_experiment.py --dir results/experiments/exp-20261016-141118

# ==============================================================================
# 4. VERIFY CRYPTOGRAPHIC SHA-256 RELEASE CHECKSUMS (15 Files)
# ==============================================================================
python -c "import hashlib, os; base = r'release\BCSE355L_KubeCostFinOps_Final'; all_ok = True
with open(os.path.join(base, 'SHA256SUMS.txt')) as f:
    for line in f:
        if line.strip():
            h_exp, rpath = line.split(maxsplit=1); fpath = os.path.join(base, rpath.strip().replace('/', os.sep))
            h = hashlib.sha256(open(fpath, 'rb').read()).hexdigest().lower()
            match = (h == h_exp.lower()); all_ok = all_ok and match
            print(f'[{'MATCH' if match else 'MISMATCH'}] {rpath.strip()}')
print('OVERALL STATUS:', 'PASS' if all_ok else 'FAIL')"

# ==============================================================================
# 5. LAUNCH INTERACTIVE FINOPS DASHBOARD
# ==============================================================================
python src/backend/main.py --host 127.0.0.1 --port 8000
# Dashboard UI: http://127.0.0.1:8000/
# API Health:   http://127.0.0.1:8000/api/v1/health
# Spend API:    http://127.0.0.1:8000/api/v1/cost/monthly
# Rightsizing:  http://127.0.0.1:8000/api/v1/recommendations
# Experiments:  http://127.0.0.1:8000/api/v1/experiments/latest
```

---

## 3. Authoritative Workspace Deliverable Inventory

| # | Deliverable Category | Workspace Path | Verification Status |
|---|---|---|---|
| 1 | **Final DOCX Report** | `1Submission/FINAL_VERIFIED/BCSE355L_Kubernetes_FinOps_Final_Report.docx` | Verified 59 pages via Word COM |
| 2 | **Final PDF Report** | `1Submission/FINAL_VERIFIED/BCSE355L_Kubernetes_FinOps_Final_Report.pdf` | Verified 59 pages |
| 3 | **Personalized Lead Report** | `release/BCSE355L_KubeCostFinOps_Final/BCSE355L_Final_Project_Report_K_Darshan.pdf` | Matches Lead submission |
| 4 | **Core FinOps Engine** | `src/finops_engine/` (`cost_analyzer.py`, `recommendation_engine.py`, `pipeline.py`, `experiment_runner.py`, `ml_forecast.py`) | All unit tests passing |
| 5 | **REST Backend Server** | `src/backend/main.py` | 10 API endpoints, XSS/path traversal protected |
| 6 | **Frontend Dashboard** | `src/frontend/` (`index.html`, `styles.css`, `app.js`) | Responsive, dark mode, sanitized DOM |
| 7 | **CloudFormation Template** | `src/aws/cloudformation/eks-infrastructure.yaml` | Zero-NAT Gateway architecture |
| 8 | **AWS K8s Manifests** | `src/aws/k8s/` (`namespace.yaml`, `edusaas-workload.yaml`, `finops-platform.yaml`, `hpa.yaml`, `ingress-alb.yaml`) | Production-ready EKS specs |
| 9 | **AWS Deployment Automation**| `src/aws/scripts/deploy-aws.ps1` | EKS, ECR push, rollout, verification |
| 10 | **AWS Teardown Automation** | `src/aws/scripts/teardown-aws.ps1` | Zero lingering billable resources |
| 11 | **AWS Cost Estimate** | `docs/AWS_COST_ESTIMATE_AND_INVENTORY.md` | Hourly, 3-hour, and monthly breakdown |
| 12 | **Release Package** | `release/BCSE355L_KubeCostFinOps_Final/` | SHA-256 verified, evidence bundled |
| 13 | **Project Documentation** | `docs/` (`ARCHITECTURE.md`, `EXPERIMENT_RESULTS.md`, `SETUP_AND_REPRODUCTION.md`, `DEMO_RUNBOOK.md`, `REVIEW_QA_PREPARATION.md`) | Fully cross-referenced |

---

## 4. Key Verified Research & Experimental Findings

- **Empirical Peak CPU Utilization:** 15.16 millicores (only 6.06% of the 250m requested spec).
- **Empirical Peak Memory Utilization:** 6.45 MiB (only 2.52% of the 256Mi requested spec).
- **Modeled Baseline Monthly Spend:** $13.0845 ($13.08) per workload.
- **Modeled Rightsized Monthly Spend:** $2.6942 ($2.69) with 50m CPU and 64Mi RAM safety floors, 2 replicas, and +20% buffer.
- **Modeled Monthly Savings:** $10.3903 ($10.39) per workload (79.41% unrounded / 79.4% stored reduction).
- **Adverse Workload Behavior (Run `exp-20261016-141118`):** At 30 RPS, client-side HTTP timeouts occurred while container CPU and memory remained non-saturated. This finding is transparently documented in the report, and application capacity limits are conservatively reported rather than inflated.
- **Dry-Run Safety:** Recommendations remain strictly advisory; running cluster specifications were not mutated.

---

## 5. AWS Production Deployment Architecture & Cost Gate

### 5.1 Architecture Design Principles
- **Zero-NAT Gateway:** Bypasses AWS NAT Gateway charges ($32.40/month per gateway + data transfer) by utilizing public subnets with tightly restricted AWS Security Groups.
- **Minimal Worker Node:** 1x `t3.medium` (2 vCPUs, 4 GiB RAM) managed by an EKS Node Group.
- **Single Ingress Point:** AWS Application Load Balancer (ALB) routes both dashboard static assets and API requests.
- **ECR Container Registry:** Versioned container image (`kubecost-finops-platform:v1.0.0`).

### 5.2 Estimated Cost Breakdown

| Resource | Spec / Quantity | Hourly Cost (USD) | 3-Hour Evaluation (USD) | Monthly Cost (730 hrs, USD) | Approx Monthly (INR @ ₹84/$) |
|---|---|---|---|---|---|
| **EKS Control Plane** | Kubernetes v1.30 Managed Cluster | $0.1000 | $0.300 | $73.00 | ~₹6,132 |
| **EC2 Worker Node** | 1x `t3.medium` (On-Demand) | $0.0416 | $0.125 | $30.37 | ~₹2,551 |
| **EBS Storage** | 20 GiB gp3 Root Volume | $0.0022 | $0.007 | $1.60 | ~₹134 |
| **Application Load Balancer** | 1x AWS ALB | $0.0225 | $0.068 | $16.43 | ~₹1,380 |
| **Public IPv4 Address** | Attached to ALB/EC2 | $0.0050 | $0.015 | $3.65 | ~₹307 |
| **Amazon ECR** | < 200 MB container image | $0.0001 | $0.000 | $0.02 | ~₹2 |
| **Data Transfer & Logs** | Basic egress (< 1 GB) | $0.0000 | $0.000 | $0.09 | ~₹8 |
| **TOTAL** | | **~$0.1714 / hr** | **~$0.51 USD** | **~$125.16 USD** | **~₹10,514 INR** |

*Note: The 3-hour evaluation cost is approximately **$0.51 USD (~₹43 INR)**. Immediate teardown using `src/aws/scripts/teardown-aws.ps1` returns ongoing hourly expenses to **$0.00 / hour**.*

### 5.3 AWS Deployment Prerequisites & Activation Steps
When the user chooses to deploy to AWS:
1. Configure credentials safely in terminal (without pasting into chat):
   ```powershell
   aws configure
   # Enter AWS Access Key ID, Secret Access Key, Default region: us-east-1
   ```
2. Verify caller identity:
   ```powershell
   aws sts get-caller-identity
   ```
3. Start Docker Desktop (required for building and pushing the container to ECR).
4. Run the automated deployment script:
   ```powershell
   .\src\aws\scripts\deploy-aws.ps1 -Region "us-east-1"
   ```
5. Run the teardown script when evaluation is complete:
   ```powershell
   .\src\aws\scripts\teardown-aws.ps1 -Region "us-east-1"
   ```

---

## 6. University Submission Package & Checklist

For the BCSE355L final course submission (VTOP / LMS / Course Instructor Portal):

### 6.1 Primary Deliverables to Upload
1. **Primary PDF Report:**
   `1Submission/FINAL_VERIFIED/BCSE355L_Kubernetes_FinOps_Final_Report.pdf`  
   *(or `release/BCSE355L_KubeCostFinOps_Final/BCSE355L_Kubernetes_FinOps_Final_Report.pdf`)*  
   - SHA-256: `638e78de5c4da931e834a6f2118044d2b5a01c44737a2e0695cff989e9997100`
   - Exact Length: 59 pages
2. **Editable Source Report (if requested):**
   `1Submission/FINAL_VERIFIED/BCSE355L_Kubernetes_FinOps_Final_Report.docx`  
   - SHA-256: `767c99035804c74edaf6bdd9b1d7f8e593966a26620a2f92125c56e4bc746894`
3. **GitHub Project Repository Link:**
   `https://github.com/Dev-withDarshan/KubeCostFinOps_Cloud_Project_2026`  
   `Commit Hash: 9bead7750c5d2447008c9d3170272fd9bdeb00a9` (Branch: `develop`)

### 6.2 Submission Quality Checklist
- [x] Title page correctly formatted with course title, code (BCSE355L), and faculty guide.
- [x] All 4 team members with registration numbers (24BIT0119, 24BIT0143, 24BIT0155, 24BIT0315) listed.
- [x] Abstract, Table of Contents, 14 Chapters, and Appendices A/B/C complete and verified.
- [x] 15 real scholarly references with verified DOIs included.
- [x] Local Kind empirical results clearly distinguished from proposed AWS deployment.
- [x] Modeled 79.4% rightsizing savings clearly labeled as estimates.
- [x] Repository push confirmed and verified on GitHub.
- [x] Cryptographic checksums verified across release deliverables.
