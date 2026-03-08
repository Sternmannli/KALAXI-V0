#!/usr/bin/env python3
"""
run_full_check.py — Kalaxi Integrated Check Pipeline
Runs all verification steps in sequence:
1. Canon integrity scan
2. Dignity predicate validation (sample texts)
3. MANIFEST heartbeat verification
4. Test suite execution

Usage: python3 SCRIPTS/run_full_check.py
"""

import sys
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WEAVER = REPO_ROOT / "WEAVER"
TESTS = REPO_ROOT / "tests"

def header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def run_canon_integrity():
    header("STEP 1: Canon Integrity Scan")
    result = subprocess.run(
        [sys.executable, str(WEAVER / "canon_integrity.py")],
        capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"STDERR: {result.stderr}")
    return result.returncode == 0


def run_dignity_check():
    header("STEP 2: Dignity Predicate Validation")
    sys.path.insert(0, str(REPO_ROOT))
    from WEAVER.dignity_check import check_dignity

    test_cases = [
        ("Clean text", "Thank you for sharing your story.", True),
        ("Coercive", "You must comply immediately.", False),
        ("Void trigger", "We need to harvest the data.", False),
        ("Emotional", "I am frustrated with this process.", True),
    ]

    all_pass = True
    for label, text, expected in test_cases:
        result = check_dignity(text)
        status = "PASS" if result.passed == expected else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  [{status}] {label}: D={result.D:.1f} (expected {'pass' if expected else 'fail'})")

    return all_pass


def run_manifest_check():
    header("STEP 3: MANIFEST Heartbeat Verification")
    heartbeat = REPO_ROOT / "MANIFEST" / "heartbeat.md"
    if not heartbeat.exists():
        print("  FAIL: MANIFEST/heartbeat.md not found")
        return False

    content = heartbeat.read_text()
    if "Open gaps: ?" in content or "[YYYY-MM-DD]" in content:
        print("  FAIL: heartbeat.md still has template placeholders")
        return False

    print("  PASS: heartbeat.md is populated")

    ids_json = REPO_ROOT / "MANIFEST" / "ids.json"
    if not ids_json.exists():
        print("  FAIL: MANIFEST/ids.json not found")
        return False
    print("  PASS: ids.json exists")

    metadata_dir = REPO_ROOT / "MANIFEST" / "metadata"
    expected = ["tier1_stone.md", "tier2_weaver.md", "tier3_honey.md", "tier4_hand.md", "cross_tier_index.md"]
    for f in expected:
        if not (metadata_dir / f).exists():
            print(f"  FAIL: metadata/{f} not found")
            return False
    print(f"  PASS: All {len(expected)} metadata archive files present")
    return True


def run_tests():
    header("STEP 4: Test Suite")
    test_files = [
        "test_dignity.py",
        "test_canon_integrity.py",
        "test_detectors.py",
    ]
    all_pass = True
    for tf in test_files:
        path = TESTS / tf
        if not path.exists():
            print(f"  SKIP: {tf} not found")
            continue
        result = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True, text=True, cwd=str(REPO_ROOT)
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            summary = lines[-1] if lines else "no output"
            print(f"  PASS: {tf} — {summary}")
        else:
            print(f"  FAIL: {tf}")
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            all_pass = False
    return all_pass


def main():
    print("\nKALAXI FULL CHECK PIPELINE")
    print("=" * 60)

    results = []
    results.append(("Canon Integrity", run_canon_integrity()))
    results.append(("Dignity Predicate", run_dignity_check()))
    results.append(("MANIFEST Check", run_manifest_check()))
    results.append(("Test Suite", run_tests()))

    header("SUMMARY")
    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {name}")

    if all_pass:
        print("\nAll checks passed. The canon is healthy.")
    else:
        print("\nSome checks failed. Review the output above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
