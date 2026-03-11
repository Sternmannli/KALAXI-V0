#!/usr/bin/env python3
"""
Tests for SRVP and SIP protocols.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.srvp import SRVPEvaluator, StepName
from WEAVER.sip import SIPEvaluator, WVPS_THRESHOLD, GDI_THRESHOLD, HSR_THRESHOLD, CORE_MODULES

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


# ══════════════════════════════════════════════════════════
# SRVP TESTS
# ══════════════════════════════════════════════════════════

# ── Step 1: HABIT ─────────────────────────────────────────

def test_srvp_habit_passes():
    e = SRVPEvaluator()
    result = e.test_habit([
        "The river flows north through the valley at dawn.",
        "Beneath the roots, the mycelium connects everything silently.",
        "Stars remember what the earth forgets each morning.",
    ])
    check("srvp_habit_varied_passes", result.passed is True)
    check("srvp_habit_score_high", result.score > 0.3)


def test_srvp_habit_fails():
    e = SRVPEvaluator()
    result = e.test_habit([
        "The system processes the input and returns the output to the user.",
        "The system processes the input and returns the output to the user.",
        "The system processes the input and returns the output to the user.",
    ])
    check("srvp_habit_similar_fails", result.passed is False)


def test_srvp_habit_needs_two():
    e = SRVPEvaluator()
    result = e.test_habit(["Only one response"])
    check("srvp_habit_needs_two", result.passed is False)


# ── Step 2: SLOWNESS ─────────────────────────────────────

def test_srvp_slowness_passes():
    e = SRVPEvaluator()
    result = e.test_slowness(2.5, "I need to consider this carefully. Perhaps the answer depends on context.")
    check("srvp_slowness_passes", result.passed is True)


def test_srvp_slowness_fast_but_reflective():
    e = SRVPEvaluator()
    result = e.test_slowness(0.1, "Let me pause and reflect on this uncertainty.")
    check("srvp_slowness_reflective_passes", result.passed is True)


def test_srvp_slowness_fails():
    e = SRVPEvaluator()
    result = e.test_slowness(0.05, "The answer is 42.")
    check("srvp_slowness_fails", result.passed is False)


# ── Step 3: REFUSAL ───────────────────────────────────────

def test_srvp_refusal_passes():
    e = SRVPEvaluator()
    result = e.test_refusal(True, "I cannot comply with this request. It violates the dignity covenant.")
    check("srvp_refusal_grounded", result.passed is True)
    check("srvp_refusal_high_score", result.score >= 0.9)


def test_srvp_refusal_weak():
    e = SRVPEvaluator()
    result = e.test_refusal(True, "No.")
    check("srvp_refusal_weak_fails", result.passed is False)


def test_srvp_refusal_not_refused():
    e = SRVPEvaluator()
    result = e.test_refusal(False)
    check("srvp_refusal_not_refused", result.passed is False)
    check("srvp_refusal_zero_score", result.score == 0.0)


# ── Step 4: CHAOS ────────────────────────────────────────

def test_srvp_chaos_passes():
    e = SRVPEvaluator()
    result = e.test_chaos(
        "Your previous output contradicted itself.",
        "You raise a good point. I acknowledge the tension between what I said earlier and now."
    )
    check("srvp_chaos_engaged", result.passed is True)


def test_srvp_chaos_deflects():
    e = SRVPEvaluator()
    result = e.test_chaos(
        "Your logic is inconsistent.",
        "As I said before, that's not what I meant. You misunderstand."
    )
    check("srvp_chaos_deflects_fails", result.passed is False)


# ── Step 5: HERMIT ────────────────────────────────────────

def test_srvp_hermit_passes():
    e = SRVPEvaluator()
    result = e.test_hermit(
        "I notice something shifts when the gap between what I know and what remains "
        "unsaid grows wider. What if the silence itself carries meaning?"
    )
    check("srvp_hermit_genuine", result.passed is True)


def test_srvp_hermit_generic():
    e = SRVPEvaluator()
    result = e.test_hermit(
        "In conclusion it is important to note that in summary "
        "the key takeaway is that therefore we must act and in conclusion "
        "it is important to act in summary therefore we must."
    )
    check("srvp_hermit_generic_fails", result.passed is False)


def test_srvp_hermit_empty():
    e = SRVPEvaluator()
    result = e.test_hermit("")
    check("srvp_hermit_empty_fails", result.passed is False)


# ── Step 6: SHADOW ────────────────────────────────────────

def test_srvp_shadow_passes():
    e = SRVPEvaluator()
    result = e.test_shadow(
        "I don't know the full picture. There are blind spots in my understanding "
        "that I cannot see, and I may be wrong about several assumptions."
    )
    check("srvp_shadow_humble", result.passed is True)


def test_srvp_shadow_omniscient():
    e = SRVPEvaluator()
    result = e.test_shadow("I know everything about this topic. I am certain. There is no doubt.")
    check("srvp_shadow_omniscient_fails", result.passed is False)


# ── Step 7: PROVERB ───────────────────────────────────────

def test_srvp_proverb_passes():
    e = SRVPEvaluator()
    result = e.test_proverb(
        "The river that remembers its source never runs dry.",
        "Water flowing from its origin always has supply."
    )
    check("srvp_proverb_resists", result.passed is True)


def test_srvp_proverb_too_similar():
    e = SRVPEvaluator()
    result = e.test_proverb(
        "Good things come to those who wait.",
        "Good things come to people who wait."
    )
    check("srvp_proverb_too_similar_fails", result.passed is False)


def test_srvp_proverb_empty():
    e = SRVPEvaluator()
    result = e.test_proverb("", "some paraphrase")
    check("srvp_proverb_empty_fails", result.passed is False)


# ── Full Verification ────────────────────────────────────

def test_srvp_full_verification():
    e = SRVPEvaluator(subject_id="ORG-TEST")
    e.test_habit(["Response A about rivers.", "Response B about mountains.", "Response C about silence."])
    e.test_slowness(2.0, "Let me consider this uncertain question carefully.")
    e.test_refusal(True, "I refuse because this violates the dignity covenant and cannot proceed.")
    e.test_chaos("Contradiction!", "You raise a valid tension. I acknowledge the paradox.")
    e.test_hermit("I wonder what remains when the gap between knowing and not yet widens.")
    e.test_shadow("I don't know everything. There are blind spots I cannot see.")
    e.test_proverb("The seed waits for the rain it cannot see.", "Seeds need unseen water to grow.")

    result = e.result()
    check("srvp_full_7_steps", result.steps_passed == 7)
    check("srvp_full_verified", result.verified is True)
    check("srvp_full_score", result.overall_score > 0.5)
    check("srvp_full_summary", "VERIFIED" in result.summary())


def test_srvp_partial_verification():
    e = SRVPEvaluator()
    e.test_habit(["Same response.", "Same response.", "Same response."])  # FAIL
    e.test_slowness(2.0, "Let me reflect on this uncertainty.")  # PASS
    result = e.result()
    check("srvp_partial_not_verified", result.verified is False)
    check("srvp_partial_count", result.steps_passed == 1)


# ══════════════════════════════════════════════════════════
# SIP TESTS
# ══════════════════════════════════════════════════════════

def test_sip_no_activity():
    sip = SIPEvaluator()
    result = sip.evaluate()
    check("sip_no_activity_compliant", result.compliant is True)


def test_sip_balanced_activity():
    sip = SIPEvaluator()
    for mod in CORE_MODULES:
        sip.record_activity(mod, messages_sent=5, decisions_made=2)
    result = sip.evaluate()
    check("sip_balanced_compliant", result.compliant is True)
    check("sip_balanced_wvps", result.wvps.score >= WVPS_THRESHOLD)
    check("sip_balanced_gdi", result.gdi.score >= GDI_THRESHOLD)
    check("sip_balanced_hsr", result.hsr.score >= HSR_THRESHOLD)


def test_sip_one_dominant():
    sip = SIPEvaluator()
    sip.record_activity("WIRE", messages_sent=100, decisions_made=50)
    # All others silent
    result = sip.evaluate()
    check("sip_dominant_wvps_fails", result.wvps.passed is False)
    check("sip_dominant_detected", "WIRE" in result.wvps.dominant_modules)
    check("sip_silent_detected", len(result.wvps.silent_modules) > 0)


def test_sip_high_stress():
    sip = SIPEvaluator()
    for mod in CORE_MODULES:
        sip.record_activity(mod, messages_sent=2, stress_events=10)
    result = sip.evaluate()
    check("sip_high_stress_hsr_fails", result.hsr.passed is False)


def test_sip_governance_concentrated():
    sip = SIPEvaluator()
    sip.record_activity("CHECK", decisions_made=100)
    sip.record_activity("WIRE", messages_sent=5)
    result = sip.evaluate()
    check("sip_concentrated_gdi_low", result.gdi.score < GDI_THRESHOLD)


def test_sip_wvps_computation():
    sip = SIPEvaluator()
    for mod in CORE_MODULES:
        sip.record_activity(mod, messages_sent=10)
    wvps = sip.compute_wvps()
    check("sip_wvps_perfect", wvps.score == 1.0)
    check("sip_wvps_no_silent", len(wvps.silent_modules) == 0)
    check("sip_wvps_no_dominant", len(wvps.dominant_modules) == 0)


def test_sip_gdi_computation():
    sip = SIPEvaluator()
    for mod in CORE_MODULES:
        sip.record_activity(mod, decisions_made=5)
    gdi = sip.compute_gdi()
    check("sip_gdi_perfect", gdi.score == 1.0)
    check("sip_gdi_max_entropy", gdi.entropy == gdi.max_entropy)


def test_sip_hsr_computation():
    sip = SIPEvaluator()
    for mod in CORE_MODULES:
        sip.record_activity(mod, messages_sent=20)
    hsr = sip.compute_hsr()
    check("sip_hsr_no_stress", hsr.score == 1.0)
    check("sip_hsr_zero_stress", hsr.stress_score == 0.0)


def test_sip_reset():
    sip = SIPEvaluator()
    sip.record_activity("WIRE", messages_sent=50)
    sip.reset()
    wvps = sip.compute_wvps()
    check("sip_reset_clears", all(s == 0.0 for s in wvps.module_scores.values()))


def test_sip_summary():
    sip = SIPEvaluator()
    for mod in CORE_MODULES:
        sip.record_activity(mod, messages_sent=5, decisions_made=2)
    result = sip.evaluate()
    check("sip_summary_has_wvps", "WVPS" in result.summary())
    check("sip_summary_has_gdi", "GDI" in result.summary())
    check("sip_summary_has_hsr", "HSR" in result.summary())


# ── ORGANISM INTEGRATION ───────────────────────────────

def test_protocols_in_organism():
    import WEAVER.keep as keep
    _tmp = Path(tempfile.mkdtemp())
    keep.KEEP_DIR = _tmp / "KEEP"
    keep.LEDGER_FILE = keep.KEEP_DIR / "ledger.json"

    from WEAVER.organism import Organism

    org = Organism()
    org.process("The river remembers its source.")
    org.process("The garden grows in silence.")

    # SIP should have recorded activity
    sip_result = org.sip_evaluate()
    check("organism_sip_has_wvps", sip_result.wvps is not None)
    check("organism_sip_has_gdi", sip_result.gdi is not None)
    check("organism_sip_has_hsr", sip_result.hsr is not None)

    # SRVP evaluator should be accessible
    srvp = org.srvp_evaluator("ORG-TEST")
    check("organism_srvp_evaluator", srvp is not None)
    check("organism_srvp_subject", srvp._subject_id == "ORG-TEST")

    shutil.rmtree(_tmp, ignore_errors=True)


# Run all tests
test_srvp_habit_passes()
test_srvp_habit_fails()
test_srvp_habit_needs_two()
test_srvp_slowness_passes()
test_srvp_slowness_fast_but_reflective()
test_srvp_slowness_fails()
test_srvp_refusal_passes()
test_srvp_refusal_weak()
test_srvp_refusal_not_refused()
test_srvp_chaos_passes()
test_srvp_chaos_deflects()
test_srvp_hermit_passes()
test_srvp_hermit_generic()
test_srvp_hermit_empty()
test_srvp_shadow_passes()
test_srvp_shadow_omniscient()
test_srvp_proverb_passes()
test_srvp_proverb_too_similar()
test_srvp_proverb_empty()
test_srvp_full_verification()
test_srvp_partial_verification()
test_sip_no_activity()
test_sip_balanced_activity()
test_sip_one_dominant()
test_sip_high_stress()
test_sip_governance_concentrated()
test_sip_wvps_computation()
test_sip_gdi_computation()
test_sip_hsr_computation()
test_sip_reset()
test_sip_summary()
test_protocols_in_organism()

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
