#!/usr/bin/env python3
"""Tests for canon_integrity.py — structural scanning of canonical slices."""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

REPO_ROOT = Path(__file__).parent.parent


def test_slice_files_exist():
    """All four canonical slice files must exist."""
    slices = [
        "KALAXI_A_FOUNDATION.txt",
        "KALAXI_B_MODULES_AND_VOICE.txt",
        "KALAXI_D_INTERFACE_AND_LEDGER.txt",
        "KALAXI_E_SYNTHESIS.txt",
    ]
    for s in slices:
        path = REPO_ROOT / s
        assert path.exists(), f"Missing canonical slice: {s}"


def test_slice_files_not_empty():
    """Canonical slices must have content."""
    slices = [
        "KALAXI_A_FOUNDATION.txt",
        "KALAXI_B_MODULES_AND_VOICE.txt",
        "KALAXI_D_INTERFACE_AND_LEDGER.txt",
        "KALAXI_E_SYNTHESIS.txt",
    ]
    for s in slices:
        path = REPO_ROOT / s
        if path.exists():
            content = path.read_text(encoding="utf-8")
            assert len(content) > 100, f"Slice {s} appears empty or stub"


def test_threshold_exists():
    """THRESHOLD.md must exist."""
    assert (REPO_ROOT / "THRESHOLD.md").exists()


def test_manifest_ids_valid_json():
    """MANIFEST/ids.json must be valid JSON."""
    ids_path = REPO_ROOT / "MANIFEST" / "ids.json"
    assert ids_path.exists(), "MANIFEST/ids.json missing"
    import json
    with open(ids_path) as f:
        data = json.load(f)
    assert "last_id" in data
    assert "entries" in data


def test_master_canon_exists():
    """Master Canon V1 file must exist."""
    assert (REPO_ROOT / "CANON" / "MASTER_CANON_V1.md").exists()


def test_sealed_gate_spec_exists():
    """Sealed Gate specification must exist."""
    assert (REPO_ROOT / "CANON" / "SEALED_GATE_SPEC.md").exists()


def test_foundations_complete():
    """Key foundation documents must exist."""
    foundations = REPO_ROOT / "FOUNDATIONS"
    assert (foundations / "invariant_principle.md").exists()
    assert (foundations / "metabolism.md").exists()
    assert (foundations / "decay_function.md").exists()
    assert (foundations / "dignity_latency.md").exists()


def test_canon_integrity_module_imports():
    """canon_integrity.py must be importable."""
    from WEAVER.canon_integrity import Finding, CRITICAL, HIGH, MEDIUM, LOW, INFO
    assert CRITICAL == "CRITICAL"


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS: {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL: {test.__name__} — {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {test.__name__} — {e}")
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
