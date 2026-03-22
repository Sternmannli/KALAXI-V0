"""
test_voice_regression.py — Verify voice regression runner and golden corpus.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "TOOLS"))

from voice_lint import lint


GOLDEN_PATH = ROOT / "TRAINING" / "GOLDEN_REGRESSION.jsonl"


def test_golden_corpus_exists():
    """Golden regression corpus file must exist."""
    assert GOLDEN_PATH.exists(), "GOLDEN_REGRESSION.jsonl missing — run build_golden_regression.py"


def test_golden_corpus_has_200_entries():
    """Golden corpus must have exactly 200 entries."""
    if not GOLDEN_PATH.exists():
        return
    with open(GOLDEN_PATH) as f:
        count = sum(1 for line in f if line.strip())
    assert count == 200, f"Expected 200 entries, got {count}"


def test_golden_corpus_all_pass_lint():
    """Every entry in golden corpus must pass standard voice lint."""
    if not GOLDEN_PATH.exists():
        return
    failures = []
    with open(GOLDEN_PATH) as f:
        for i, line in enumerate(f):
            entry = json.loads(line)
            for msg in entry.get("messages", []):
                if msg["role"] == "assistant":
                    passed, reason, _ = lint(msg["content"])
                    if not passed:
                        failures.append(f"Entry {i}: {reason}")
    assert not failures, f"{len(failures)} entries fail lint:\n" + "\n".join(failures[:5])


def test_golden_corpus_covers_all_registers():
    """Golden corpus must cover at least 7 distinct registers."""
    if not GOLDEN_PATH.exists():
        return
    registers = set()
    with open(GOLDEN_PATH) as f:
        for line in f:
            entry = json.loads(line)
            reg = entry.get("metadata", {}).get("register", "unknown")
            registers.add(reg)
    assert len(registers) >= 7, f"Only {len(registers)} registers: {registers}"


def test_golden_corpus_format():
    """Each entry must have messages array with system, user, assistant roles."""
    if not GOLDEN_PATH.exists():
        return
    with open(GOLDEN_PATH) as f:
        for i, line in enumerate(f):
            entry = json.loads(line)
            messages = entry.get("messages", [])
            roles = [m["role"] for m in messages]
            assert "system" in roles, f"Entry {i}: missing system message"
            assert "user" in roles, f"Entry {i}: missing user message"
            assert "assistant" in roles, f"Entry {i}: missing assistant message"
