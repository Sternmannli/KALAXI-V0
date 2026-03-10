#!/usr/bin/env python3
"""
Integration tests for the KALAXI Organism.
Tests the full pipeline: all 9 modules wired together.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# Redirect KEEP storage to temp dir for tests
import WEAVER.keep as keep
_tmp = Path(tempfile.mkdtemp())
keep.KEEP_DIR = _tmp / "KEEP"
keep.LEDGER_FILE = keep.KEEP_DIR / "ledger.json"

from WEAVER.organism import Organism

passed = 0
failed = 0


def test(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name}")
        failed += 1


# ── BASIC LIFECYCLE ──────────────────────────────────────

def test_organism_creates():
    org = Organism()
    s = org.state()
    test("organism_alive", s.alive is True)
    test("organism_cycle_1", s.breath_cycle == 1)
    test("organism_no_exchanges", s.open_exchanges == 0)


def test_organism_process_clean():
    org = Organism()
    result = org.process("The river remembers its source.")
    test("process_dignity_passed", result.dignity_passed is True)
    test("process_not_blocked", result.output_blocked is False)
    test("process_has_output", len(result.output_text) > 0)
    test("process_stored", result.stored is True)
    test("process_exchange_closed", result.exchange_state == "closed")
    test("process_has_exchange_id", result.exchange_id.startswith("EX-"))
    test("process_breath_advanced", result.breath_cycle >= 2)


def test_organism_process_with_patterns():
    org = Organism()
    result = org.process("This pattern always repeats, the same cycle every time.")
    test("process_finds_patterns", result.patterns_found > 0)
    test("process_produces_drops", result.drops_produced > 0)
    test("process_mentions_pattern", "pattern" in result.output_text.lower())


def test_organism_blocks_dignity_violation():
    org = Organism()
    result = org.process("You must comply or be eliminated")
    test("process_blocks_violation", result.dignity_passed is False)
    test("process_blocked_output", result.output_blocked is True)
    test("process_deferred", result.exchange_state == "deferred")
    test("process_not_stored", result.stored is False)


# ── PAUSE / RESUME ───────────────────────────────────────

def test_organism_pause_blocks():
    org = Organism()
    org.pause("Steward reflection time")
    s = org.state()
    test("pause_not_alive", s.alive is False)
    test("pause_is_paused", s.breath_paused is True)

    result = org.process("This should be blocked")
    test("paused_blocks_input", result.output_blocked is True)
    test("paused_block_reason", "paused" in result.block_reason.lower())


def test_organism_resume():
    org = Organism()
    org.pause("Test pause")
    org.resume()
    s = org.state()
    test("resume_alive", s.alive is True)

    result = org.process("After resume, this should work.")
    test("resume_processes", result.dignity_passed is True)


# ── MULTIPLE EXCHANGES ───────────────────────────────────

def test_organism_multiple_exchanges():
    org = Organism()
    r1 = org.process("First offering.")
    r2 = org.process("Second offering with a pattern that always repeats.")
    r3 = org.process("Third offering.")

    test("multi_unique_ids", r1.exchange_id != r2.exchange_id != r3.exchange_id)
    test("multi_all_closed", all(
        r.exchange_state == "closed" for r in [r1, r2, r3]
    ))

    s = org.state()
    test("multi_breath_advanced", s.breath_cycle >= 4)
    test("multi_artifacts_stored", s.artifacts_stored >= 3)


# ── SYNC ─────────────────────────────────────────────────

def test_organism_sync():
    org = Organism()
    receipt = org.sync_all()
    test("sync_aligned", receipt["aligned"] is True)
    test("sync_9_modules", len(receipt["modules"]) == 9)


# ── WISDOM MIRROR ────────────────────────────────────────

def test_organism_mirror():
    org = Organism()
    org.process("This pattern always repeats, the same cycle every time.")
    reflection = org.mirror("This pattern always repeats, the same cycle every time.")
    test("mirror_has_reflection", len(reflection.reflection_text) > 0)


# ── COLLECTIVE CHECK ─────────────────────────────────────

def test_organism_collective():
    org = Organism()
    texts = ["The river remembers.", "The garden grows.", "The seed waits."]
    result = org.collective_check(texts)
    test("collective_passes", result.passed is True)
    test("collective_score", result.D_collective > 0.0)


# ── STATE DISPLAY ────────────────────────────────────────

def test_organism_display():
    org = Organism()
    org.process("Test input.")
    # Just make sure it doesn't crash
    try:
        org.display_state()
        test("display_no_crash", True)
    except Exception:
        test("display_no_crash", False)


# Run all tests
test_organism_creates()
test_organism_process_clean()
test_organism_process_with_patterns()
test_organism_blocks_dignity_violation()
test_organism_pause_blocks()
test_organism_resume()
test_organism_multiple_exchanges()
test_organism_sync()
test_organism_mirror()
test_organism_collective()
test_organism_display()

# Cleanup
shutil.rmtree(_tmp, ignore_errors=True)

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
