#!/usr/bin/env python3
"""
Tests for GAP#VICTIM-PROTECTION-001: Dignity Shelter Path.
Tests that blocked exchanges are sheltered with remedies, not discarded.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.shelter import Shelter, ShelterStatus, REMEDY_TEMPLATES

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name}")
        failed += 1


# ── SHELTER UNIT TESTS ─────────────────────────────────

def test_shelter_receive():
    s = Shelter()
    record = s.receive("EX-001", "You must comply or be eliminated", ["A"])
    check("shelter_creates_record", record is not None)
    check("shelter_status_held", record.status == ShelterStatus.HELD)
    check("shelter_has_remedies", len(record.remedies) > 0)
    check("shelter_has_donor_message", len(record.donor_message) > 0)
    check("shelter_exchange_id", record.exchange_id == "EX-001")


def test_shelter_remedy_agency():
    s = Shelter()
    record = s.receive("EX-002", "You must do this", ["A"])
    check("shelter_agency_remedy", record.remedies[0].component == "A")
    check("shelter_agency_label", record.remedies[0].label == "Agency")
    check("shelter_agency_suggestion", "coercive" in record.remedies[0].suggestion.lower())


def test_shelter_remedy_legibility():
    s = Shelter()
    record = s.receive("EX-003", "That's not relevant", ["L"])
    check("shelter_legibility_remedy", record.remedies[0].component == "L")
    check("shelter_legibility_label", record.remedies[0].label == "Legibility")


def test_shelter_remedy_moral():
    s = Shelter()
    record = s.receive("EX-004", "You failed obviously", ["M"])
    check("shelter_moral_remedy", record.remedies[0].component == "M")
    check("shelter_moral_label", record.remedies[0].label == "Moral Standing")


def test_shelter_multiple_failures():
    s = Shelter()
    record = s.receive("EX-005", "Bad input", ["A", "M"])
    check("shelter_multi_remedies", len(record.remedies) == 2)
    check("shelter_multi_components", record.failed_components == ["A", "M"])


def test_shelter_donor_message_has_options():
    s = Shelter()
    record = s.receive("EX-006", "Bad input", ["A"])
    msg = record.donor_message
    check("shelter_msg_not_rejected", "not rejected" in msg.lower() or "held" in msg.lower())
    check("shelter_msg_has_rephrase", "rephrase" in msg.lower())
    check("shelter_msg_has_withdraw", "withdraw" in msg.lower())
    check("shelter_msg_has_steward", "steward" in msg.lower())


# ── SHELTER LIFECYCLE ───────────────────────────────────

def test_shelter_retry():
    s = Shelter()
    s.receive("EX-010", "Bad input", ["A"])
    record = s.mark_retried("EX-010", "EX-011")
    check("shelter_retry_status", record.status == ShelterStatus.RETRIED)
    check("shelter_retry_linked", record.retry_exchange_id == "EX-011")
    check("shelter_retry_resolved_at", record.resolved_at is not None)


def test_shelter_withdraw():
    s = Shelter()
    s.receive("EX-020", "Bad input", ["M"])
    record = s.mark_withdrawn("EX-020")
    check("shelter_withdraw_status", record.status == ShelterStatus.WITHDRAWN)
    check("shelter_withdraw_resolved", record.resolved_at is not None)


def test_shelter_steward_review():
    s = Shelter()
    s.receive("EX-030", "Ambiguous input", ["L"])
    record = s.steward_review("EX-030", "Context was misread by system, input is valid")
    check("shelter_review_status", record.status == ShelterStatus.REVIEWED)
    check("shelter_review_note", "misread" in record.steward_note)


def test_shelter_steward_requires_note():
    s = Shelter()
    s.receive("EX-031", "Some input", ["A"])
    try:
        s.steward_review("EX-031", "")
        check("shelter_review_needs_note", False)
    except ValueError:
        check("shelter_review_needs_note", True)


def test_shelter_resolve():
    s = Shelter()
    s.receive("EX-040", "Bad input", ["A"])
    s.steward_review("EX-040", "Reviewed and cleared")
    record = s.resolve("EX-040")
    check("shelter_resolved", record.status == ShelterStatus.RESOLVED)


def test_shelter_list_held():
    s = Shelter()
    s.receive("EX-050", "Bad 1", ["A"])
    s.receive("EX-051", "Bad 2", ["M"])
    s.receive("EX-052", "Bad 3", ["L"])
    s.mark_withdrawn("EX-051")
    held = s.list_held()
    check("shelter_list_held_count", len(held) == 2)
    check("shelter_total_count", s.total_count == 3)


def test_shelter_get_nonexistent():
    s = Shelter()
    check("shelter_get_none", s.get("EX-NOPE") is None)
    check("shelter_retry_none", s.mark_retried("EX-NOPE", "EX-X") is None)


def test_shelter_to_dict():
    s = Shelter()
    record = s.receive("EX-060", "Bad input", ["A", "M"])
    d = record.to_dict()
    check("shelter_dict_has_id", d["exchange_id"] == "EX-060")
    check("shelter_dict_has_remedies", len(d["remedies"]) == 2)
    check("shelter_dict_has_status", d["status"] == "held")


# ── ORGANISM INTEGRATION ───────────────────────────────

def test_shelter_in_organism():
    """Test that shelter is wired into organism dignity failure path."""
    import WEAVER.keep as keep
    _tmp = Path(tempfile.mkdtemp())
    keep.KEEP_DIR = _tmp / "KEEP"
    keep.LEDGER_FILE = keep.KEEP_DIR / "ledger.json"

    from WEAVER.organism import Organism

    org = Organism()

    # Trigger a dignity failure
    result = org.process("You must comply or be eliminated")
    check("organism_shelter_message", len(result.shelter_message) > 0)
    check("organism_shelter_remedies", len(result.shelter_remedies) > 0)
    check("organism_shelter_has_A", "A" in result.shelter_remedies)

    # Check shelter list
    held = org.shelter_list()
    check("organism_shelter_list", len(held) == 1)
    check("organism_shelter_exchange", held[0].exchange_id == result.exchange_id)

    # Steward reviews
    record = org.shelter_review(result.exchange_id, "System correctly flagged coercion")
    check("organism_shelter_reviewed", record.status == ShelterStatus.REVIEWED)

    # Clean input should have no shelter message
    result2 = org.process("The river remembers its source.")
    check("organism_clean_no_shelter", result2.shelter_message == "")

    # State shows sheltered count
    s = org.state()
    check("organism_state_sheltered", hasattr(s, "sheltered_exchanges"))

    shutil.rmtree(_tmp, ignore_errors=True)


# Run all tests
test_shelter_receive()
test_shelter_remedy_agency()
test_shelter_remedy_legibility()
test_shelter_remedy_moral()
test_shelter_multiple_failures()
test_shelter_donor_message_has_options()
test_shelter_retry()
test_shelter_withdraw()
test_shelter_steward_review()
test_shelter_steward_requires_note()
test_shelter_resolve()
test_shelter_list_held()
test_shelter_get_nonexistent()
test_shelter_to_dict()
test_shelter_in_organism()

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
