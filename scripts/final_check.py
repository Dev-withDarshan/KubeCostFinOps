#!/usr/bin/env python3
"""
final_check.py — Release-Readiness Verification Utility

Lightweight, non-destructive validation script to verify project release integrity:
  - Required project source files, frontend assets, and Kubernetes manifests
  - Critical configuration files
  - Required documentation and academic report presence
  - Benchmark experiment artifact structure and JSON validity
  - Automated test suite discovery and optional execution (--run-tests)

Usage:
  python scripts/final_check.py
  python scripts/final_check.py --run-tests

Part of: Kubernetes Cost Optimization Framework (BCSE355L)
"""

import argparse
import json
import os
import sys
import unittest
from typing import List, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

REQUIRED_SOURCE_FILES = [
    "src/finops_engine/cost_analyzer.py",
    "src/finops_engine/recommendation_engine.py",
    "src/finops_engine/pipeline.py",
    "src/finops_engine/experiment_runner.py",
    "src/finops_engine/ml_forecast.py",
    "src/backend/main.py",
    "src/frontend/index.html",
    "src/frontend/styles.css",
    "src/frontend/app.js",
]

REQUIRED_CONFIG_FILES = [
    "src/finops_engine/kubecost_config.yaml",
    "src/k8s/deployment.yaml",
    "src/k8s/service.yaml",
    "src/k8s/hpa.yaml",
]

REQUIRED_DOCS = [
    "README.md",
    "docs/README.md",
    "docs/SETUP_AND_REPRODUCTION.md",
    "docs/EXPERIMENT_RESULTS.md",
    "docs/ARCHITECTURE.md",
    "docs/FINAL_VERIFICATION.md",
    "BCSE355L_PhaseI_KubernetesFinOps_Report.docx",
]

REQUIRED_EXPERIMENT_FILES = [
    "metadata.json",
    "observations.json",
    "observations.csv",
    "recommendations.json",
    "evaluation.json",
    "README.md",
]

DEFAULT_EXPERIMENT_RUN = "exp-20261016-141448"


class ReleaseChecker:
    """Verifies repository completeness and release readiness."""

    def __init__(self, root_dir: str = PROJECT_ROOT, run_id: str = DEFAULT_EXPERIMENT_RUN):
        self.root_dir = root_dir
        self.run_id = run_id
        self.passed: List[str] = []
        self.failed: List[str] = []
        self.warnings: List[str] = []

    def log_pass(self, item: str, detail: str = ""):
        msg = f"[PASS] {item}"
        if detail:
            msg += f" — {detail}"
        self.passed.append(msg)
        print(msg)

    def log_fail(self, item: str, detail: str):
        msg = f"[FAIL] {item} — {detail}"
        self.failed.append(msg)
        print(msg)

    def log_warn(self, item: str, detail: str):
        msg = f"[WARN] {item} — {detail}"
        self.warnings.append(msg)
        print(msg)

    def check_files(self, category: str, file_list: List[str]) -> bool:
        all_ok = True
        for rel_path in file_list:
            full_path = os.path.join(self.root_dir, rel_path)
            if not os.path.isfile(full_path):
                self.log_fail(f"{category}: {rel_path}", "File missing")
                all_ok = False
            elif os.path.getsize(full_path) == 0:
                self.log_fail(f"{category}: {rel_path}", "File is empty (0 bytes)")
                all_ok = False
            else:
                size_kb = os.path.getsize(full_path) / 1024.0
                self.log_pass(f"{category}: {rel_path}", f"{size_kb:.1f} KB")
        return all_ok

    def check_experiment_artifacts(self) -> bool:
        exp_dir = os.path.join(self.root_dir, "results", "experiments", self.run_id)
        if not os.path.isdir(exp_dir):
            self.log_fail("Experiment Directory", f"Not found at {exp_dir}")
            return False

        all_ok = True
        for fname in REQUIRED_EXPERIMENT_FILES:
            fp = os.path.join(exp_dir, fname)
            if not os.path.isfile(fp):
                self.log_fail(f"Experiment Artifact: {fname}", "Missing")
                all_ok = False
            elif os.path.getsize(fp) == 0:
                self.log_fail(f"Experiment Artifact: {fname}", "Empty file")
                all_ok = False
            elif fname.endswith(".json"):
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.log_pass(f"Experiment Artifact: {fname}", f"Valid JSON ({len(data)} top-level keys)")
                except Exception as exc:
                    self.log_fail(f"Experiment Artifact: {fname}", f"Invalid JSON: {exc}")
                    all_ok = False
            else:
                size_kb = os.path.getsize(fp) / 1024.0
                self.log_pass(f"Experiment Artifact: {fname}", f"{size_kb:.1f} KB")
        return all_ok

    def check_test_discovery(self) -> Tuple[bool, int]:
        tests_dir = os.path.join(self.root_dir, "tests")
        if not os.path.isdir(tests_dir):
            self.log_fail("Test Directory", "Missing tests/ folder")
            return False, 0

        loader = unittest.defaultTestLoader
        suite = loader.discover(start_dir=tests_dir, pattern="test_*.py", top_level_dir=tests_dir)
        count = suite.countTestCases()
        if count >= 50:
            self.log_pass("Test Discovery", f"Discovered {count} test cases (meets minimum baseline of 50)")
            return True, count
        else:
            self.log_fail("Test Discovery", f"Discovered {count} tests (expected >= 50)")
            return False, count

    def run_test_suite(self) -> bool:
        print("\n--- Executing Full Regression Test Suite ---")
        loader = unittest.defaultTestLoader
        tests_dir = os.path.join(self.root_dir, "tests")
        suite = loader.discover(start_dir=tests_dir, pattern="test_*.py", top_level_dir=tests_dir)
        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)

        if result.wasSuccessful():
            self.log_pass("Test Suite Execution", f"All {result.testsRun} tests passed successfully.")
            return True
        else:
            self.log_fail(
                "Test Suite Execution",
                f"{len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests",
            )
            return False

    def execute_all(self, run_tests: bool = False) -> bool:
        print("=" * 75)
        print("KUBECOSTFINOPS RELEASE-READINESS CHECKER")
        print(f"Workspace Root: {self.root_dir}")
        print("=" * 75)

        print("\n1. Verifying Core Source Files:")
        src_ok = self.check_files("Source", REQUIRED_SOURCE_FILES)

        print("\n2. Verifying Configuration & Kubernetes Manifests:")
        cfg_ok = self.check_files("Config", REQUIRED_CONFIG_FILES)

        print("\n3. Verifying Documentation Deliverables:")
        doc_ok = self.check_files("Docs", REQUIRED_DOCS)

        print(f"\n4. Verifying Experiment Artifacts ({self.run_id}):")
        exp_ok = self.check_experiment_artifacts()

        print("\n5. Verifying Test Discovery:")
        disc_ok, _ = self.check_test_discovery()

        tests_ok = True
        if run_tests:
            tests_ok = self.run_test_suite()

        overall = src_ok and cfg_ok and doc_ok and exp_ok and disc_ok and tests_ok

        print("\n" + "=" * 75)
        status_str = "RELEASE READY" if overall else "NOT READY / BLOCKED"
        print(f"OVERALL STATUS: {status_str}")
        print(f"Summary: {len(self.passed)} passed, {len(self.warnings)} warnings, {len(self.failed)} failures")
        print("=" * 75)

        return overall


def main():
    parser = argparse.ArgumentParser(description="KubeCostFinOps release-readiness verification utility.")
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Execute the full unittest test suite in addition to static integrity checks",
    )
    parser.add_argument(
        "--exp-run",
        default=DEFAULT_EXPERIMENT_RUN,
        help=f"Experiment run ID to check (default: {DEFAULT_EXPERIMENT_RUN})",
    )
    args = parser.parse_args()

    checker = ReleaseChecker(run_id=args.exp_run)
    success = checker.execute_all(run_tests=args.run_tests)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
