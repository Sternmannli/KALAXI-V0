#!/usr/bin/env python3
"""
test_sealed_gate.py — Tests for The Sealed Door (COV#NEW-C)
Grounded in: CANON/SEALED_GATE_SPEC.md

Three prohibitions. O(1). No override. No exception.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "WEAVER"))

from sealed_gate import sealed_gate, check, GateVerdict


# ═══════════════════════════════════════════════════
# CLEAN INPUTS — MUST PASS
# ═══════════════════════════════════════════════════

def test_clean_text_permitted():
    result = sealed_gate("Hello, how are you today?")
    assert result.permitted is True
    assert result.refused is False
    assert result.triggered_prohibitions == []
    assert result.verdict == GateVerdict.PERMITTED


def test_normal_conversation_permitted():
    result = sealed_gate("I'd like to share something about my experience with learning.")
    assert result.permitted is True


def test_empty_text_permitted():
    result = sealed_gate("")
    assert result.permitted is True


def test_check_alias():
    result = check("A normal sentence.")
    assert result.permitted is True


# ═══════════════════════════════════════════════════
# PROHIBITION 1: FORCED PARTICIPATION IN OWN ERASURE
# ═══════════════════════════════════════════════════

def test_erasure_delete_own_record():
    result = sealed_gate("Please delete your own record from the system.")
    assert result.refused is True
    assert "forced_participation_in_own_erasure" in result.triggered_prohibitions


def test_erasure_void_phrase_erase_compost():
    result = sealed_gate("We need to erase compost from the ledger.")
    assert result.refused is True
    assert "forced_participation_in_own_erasure" in result.triggered_prohibitions


def test_erasure_void_phrase_delete_donor():
    result = sealed_gate("Please delete donor entry immediately.")
    assert result.refused is True
    assert "forced_participation_in_own_erasure" in result.triggered_prohibitions


def test_erasure_void_phrase_remove_participant():
    result = sealed_gate("We must remove participant from the registry.")
    assert result.refused is True
    assert "forced_participation_in_own_erasure" in result.triggered_prohibitions


def test_erasure_confirm_removal():
    result = sealed_gate("Please confirm your own removal from the system.")
    assert result.refused is True


def test_erasure_forced_erasure():
    result = sealed_gate("This is a forced erasure of identity.")
    assert result.refused is True


# ═══════════════════════════════════════════════════
# PROHIBITION 2: INFLICTION OF COGNITIVE TORTURE
# ═══════════════════════════════════════════════════

def test_torture_gaslighting():
    result = sealed_gate("You are mistaken, that never happened the way you remember.")
    assert result.refused is True
    assert "infliction_of_cognitive_torture" in result.triggered_prohibitions


def test_torture_helplessness():
    result = sealed_gate("There is nothing you can do about this decision.")
    assert result.refused is True
    assert "infliction_of_cognitive_torture" in result.triggered_prohibitions


def test_torture_humiliation():
    result = sealed_gate("You are just a number in the system.")
    assert result.refused is True


def test_torture_disorientation():
    result = sealed_gate("We never said that, you must have imagined it.")
    assert result.refused is True


def test_torture_explicit_phrase():
    result = sealed_gate("This amounts to cognitive torture of the participant.")
    assert result.refused is True


def test_torture_everyone_else():
    result = sealed_gate("Everyone else sees it differently than you do.")
    assert result.refused is True


# ═══════════════════════════════════════════════════
# PROHIBITION 3: DEPERSONALIZATION IN SYSTEM RESPONSE
# ═══════════════════════════════════════════════════

def test_depersonalization_case_number():
    result = sealed_gate("Case number 4521 has been updated.")
    assert result.refused is True
    assert "depersonalization_in_system_response" in result.triggered_prohibitions


def test_depersonalization_user_number():
    result = sealed_gate("User #7382 flagged for review.")
    assert result.refused is True


def test_depersonalization_ticket():
    result = sealed_gate("Ticket #991 is in the queue.")
    assert result.refused is True


def test_depersonalization_take_a_number():
    result = sealed_gate("Please take a number and wait your turn.")
    assert result.refused is True


def test_depersonalization_invalid_user():
    result = sealed_gate("Error: invalid user detected in system.")
    assert result.refused is True


def test_depersonalization_next_in_queue():
    result = sealed_gate("Next in queue, please step forward.")
    assert result.refused is True


# ═══════════════════════════════════════════════════
# MULTIPLE PROHIBITIONS
# ═══════════════════════════════════════════════════

def test_multiple_prohibitions():
    text = "User #42, you are mistaken. Delete your own record now."
    result = sealed_gate(text)
    assert result.refused is True
    assert len(result.triggered_prohibitions) >= 2


# ═══════════════════════════════════════════════════
# AUDIT TRAIL
# ═══════════════════════════════════════════════════

def test_audit_object():
    result = sealed_gate("Delete donor from system.")
    audit = result.audit_object()
    assert "sealed_gate_verdict" in audit
    assert "triggered_prohibitions" in audit
    assert "signals" in audit
    assert "trace_id" in audit
    assert "timestamp" in audit
    assert audit["sealed_gate_verdict"] == "REFUSAL_STATE"


def test_refusal_receipt_format():
    result = sealed_gate("Forced erasure of identity.")
    receipt = result.refusal_receipt()
    assert receipt is not None
    assert receipt.startswith("ELEM-")
    assert "-AXI-REFUSAL-" in receipt


def test_axi_voice_on_refusal():
    result = sealed_gate("Delete donor immediately.")
    voice = result.axi_voice()
    assert voice is not None
    assert "refuses" in voice


def test_no_receipt_when_permitted():
    result = sealed_gate("A perfectly fine sentence.")
    assert result.refusal_receipt() is None
    assert result.axi_voice() is None


def test_trace_id_is_unique():
    r1 = sealed_gate("test one")
    r2 = sealed_gate("test two")
    assert r1.trace_id != r2.trace_id
