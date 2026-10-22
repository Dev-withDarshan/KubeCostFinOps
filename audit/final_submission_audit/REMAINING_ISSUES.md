# Remaining Issues, Technical Hygiene, and Viva Defense Runbook

**Project:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Course:** BCSE355L — Cloud Architecture Design (VIT B.Tech)  
**Audit Standard:** Pre-Submission Risk Assessment & Final Defense Preparation  

---

## 1. Actionable Priority Checklist

| Priority | Category | Issue Description | Impact | Recommended Action |
| :---: | :--- | :--- | :--- | :--- |
| **P1** | **Git / Repository Hygiene** | **Phase-II/III Code and Reports Reside Only Locally.** All newly implemented modules (`src/backend/main.py`, `src/finops_engine/experiment_runner.py`, `ml_forecast.py`, `pipeline.py`, `src/frontend/`, `tests/`, `1Submission/`) are currently untracked or uncommitted in the local working copy. Remote GitHub repository only has Phase-I commits. | Evaluator checking GitHub will only see Phase-I planning documents unless code is committed and pushed. | **Immediate Action Required:** User must explicitly review, stage, commit, and push these files to GitHub. *(See Section 2 for exact commands).* |
| **P2** | **Git Branch Synchronization** | **Feature Branches Out of Sync.** Remote feature branches (`origin/feature/darshan`, `origin/feature/dhanushkodi`, `origin/feature/sanjay`, `origin/feature/tharun`) point to initial scaffold commit `a678739`. | If instructor inspects individual student branches on GitHub, they will appear empty. | Merge or rebase the finalized `develop` branch into the individual feature branches and push to origin. |
| **P3** | **Academic Defense** | **Oral Viva Defense Preparation.** Student team must be thoroughly prepared to articulate the distinction between local Kind simulation, advisory dry-run recommendations, and live AWS deployments. | Potential loss of marks during viva if students claim live AWS EKS deployment occurred when evidence shows local Kind testing. | Review Viva Defense Cheat Sheet in Section 3. |
| **P4** | **Repository Artifact Archiving** | **Audit Records Preservation.** Ensure that this forensic audit directory (`audit/final_submission_audit/`) is committed as a permanent QA artifact in the repository. | Demonstrates professional rigor and software quality auditing to evaluators. | Include `audit/` in Git commit. |

---

## 2. Git Hygiene & Push Authorization Runbook

> [!WARNING]
> **Strict Policy Reminder:**
> Under non-negotiable rule #10, the AI auditor does NOT automatically run `git commit` or `git push`. The commands below are provided for the student project lead to execute once authorized.

### 2.1 Git Status Analysis
Running `git status` reveals:
- **Modified Tracked Files (13 files):**
  - `README.md`, `docs/README.md`, `monitoring/prometheus_config.yaml`
  - `src/backend/README.md`, `src/finops_engine/cost_analyzer.py`, `kubecost_config.yaml`, `recommendation_engine.py`
  - `src/frontend/README.md`, `src/k8s/deployment.yaml`, `hpa.yaml`, `ingress.yaml`, `service.yaml`
  - `tests/test_finops_engine.py`
- **Untracked Deliverables & Modules (25+ items):**
  - `1Submission/` (Contains authoritative `.docx` and `.pdf` final reports)
  - `BCSE355L_Kubernetes_FinOps_Final_Report.docx` and `.pdf` (Root copies)
  - `src/backend/main.py`, `src/finops_engine/pipeline.py`, `experiment_runner.py`, `ml_forecast.py`
  - `src/frontend/index.html`, `styles.css`, `app.js`
  - `tests/test_backend_api.py`, `test_pipeline.py`, `test_experiment_runner.py`
  - `scripts/` (Validation and generation scripts)
  - `results/experiments/` (Empirical and adverse experiment artifacts)
  - `docs/` (Technical documentation guides)
  - `audit/final_submission_audit/` (This audit suite)

### 2.2 Recommended Command Sequence for Project Lead
To synchronize the local working tree with GitHub `origin/develop`:

```bash
# 1. Inspect status to confirm all files
git status

# 2. Stage all implementation files, tests, scripts, and reports
git add src/ tests/ scripts/ results/ docs/ audit/ 1Submission/ README.md kind-config.yaml requirements.txt monitoring/

# 3. Create a comprehensive Phase-II / Phase-III completion commit
git commit -m "feat(finops): complete Phase-II & Phase-III implementation, tests, experiments, and final submission report"

# 4. Push to remote develop branch
git push origin develop

# 5. (Optional) Fast-forward main and feature branches if required by course rubric
git checkout main
git merge develop
git push origin main
git checkout develop
```

---

## 3. Oral Viva Defense Preparation: Evaluator Q&A Cheat Sheet

During the final technical defense, evaluators may probe technical boundaries. Use these concrete, evidence-backed responses:

### Question 1: "Why did you run this on Kind Kubernetes on Docker Desktop instead of a live AWS EKS cluster?"
> **Authoritative Response:**
> *"The approved project scope for BCSE355L was to design the cloud architecture and validate the FinOps algorithms. Deploying an idle AWS EKS cluster costs $0.10/hour ($73.00/month) just for the Kubernetes control plane, plus NAT Gateways and worker EC2 instances (~$140/month total), which is fiscally prohibitive for an undergraduate academic evaluation. Kind (Kubernetes-in-Docker) runs certified upstream Kubernetes v1.37.0 and exposes identical cgroup metrics (`usageNanoCores`, `workingSetBytes`) via the Kubelet Summary API. Our architecture is designed for AWS EKS as the proposed target cloud environment: the core Kubernetes manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`) adhere to standard Kubernetes v1 APIs; transition to production AWS EKS is documented as requiring AWS ALB Ingress annotations, Amazon ECR image registry hosting, and IAM Roles for Service Accounts (IRSA)."*

---

### Question 2: "Is your 79.4% cost savings an actual reduction on an AWS bill?"
> **Authoritative Response:**
> *"No, sir. We explicitly disclose that this is a modeled financial projection based on workload-level resource requests, evaluated against public AWS US-East-1 on-demand reference rates ($0.031611/vCPU-hr, $0.004237/GiB-hr). Our recommendation engine operates in advisory dry-run mode to ensure zero downtime. To translate this into realized cloud billing reductions, the Kubernetes cluster must run a cluster autoscaler (such as Karpenter) to pack the rightsized pods onto fewer EC2 worker nodes."*

---

### Question 3: "Why did your benchmark run only for 70 seconds? Can 70 seconds prove rightsizing for an LMS?"
> **Authoritative Response:**
> *"The 70-second controlled benchmark was designed as a rapid verification harness to prove the functionality of our telemetry extraction, buffer scaling (+20%), and safety floor clamping (50m CPU, 64Mi RAM) under controlled 10 RPS and 25 RPS load. For long-term diurnal university traffic patterns (exam periods, assignment deadlines), our framework includes a demand forecasting engine (`src/finops_engine/ml_forecast.py`) and a synthetic 48-hour LMS traffic dataset that models diurnal activity."*

---

### Question 4: "Why did run exp-20261016-141118 fail with a 100% error rate at 30 RPS?"
> **Authoritative Response:**
> *"That run represents our adverse stress-testing counter-evidence. The workload was successfully tested at 25 RPS in the local benchmarking setup (achieving sub-6ms p95 latency and 0.0% error rate). A subsequent 30 RPS trial (run `exp-20261016-141118`) experienced client timeouts (~3,010 ms). Measured kernel cgroup telemetry showed the pods were not compute-saturated (CPU peaked at only 7.82m and RAM at 3.45 MiB). However, because our test client caught exceptions generically without packet-level traces, the precise failure mechanism remains inconclusive, and the application's maximum capacity has not been established. We deliberately preserved this adverse trial to maintain academic integrity rather than claiming uninterrupted perfection."*

---

### Question 5: "Why do some tables say 79.4% while others say 79.41% or 79.43%?"
> **Authoritative Response:**
> *"The double-precision math is identical across all components: baseline is $13.0845/mo and proposed is $2.6942/mo, yielding $10.3903/mo in savings. When unrounded, the percentage is exactly 79.409% -> 79.41%. In the automated JSON files (`evaluation.json`), the system rounds to one decimal place (79.4%). If an evaluator calculates savings from the rounded currency totals ($10.39 / $13.08), it yields 79.43%. All three figures represent the exact same underlying calculation."*

---

## 4. Final Submission Checklist for Students

- [x] Complete Word report generated: `1Submission/BCSE355L_Kubernetes_FinOps_Final_Report.docx`
- [x] Complete PDF report compiled: `1Submission/BCSE355L_Kubernetes_FinOps_Final_Report.pdf`
- [x] Personalized team lead copy saved: `1Submission/BCSE355L_Final_Project_Report_K_Darshan.docx/pdf`
- [x] Full regression test suite passing: 54/54 tests (100%)
- [x] Release readiness checker passing: 28/28 checks (100%)
- [x] Experiment artifacts forensic validation passing: 10/10 checks (100%)
- [x] Security checks verified: Zero path traversal, zero XSS, zero leaked secrets
- [ ] **Pending Student Action:** Review, stage, commit, and push untracked files to GitHub `origin/develop`
- [ ] **Pending Student Action:** Upload `1Submission/BCSE355L_Kubernetes_FinOps_Final_Report.pdf` to the university LMS portal
