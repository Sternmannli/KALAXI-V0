#!/usr/bin/env python3
"""
Tests for KEEP, WIRE, BREATH, SAY modules.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import json
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

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


# ── KEEP MODULE ──────────────────────────────────────────

import WEAVER.keep as keep

# Use a temp directory for tests
_original_keep_dir = keep.KEEP_DIR
_original_ledger = keep.LEDGER_FILE
_tmp = Path(tempfile.mkdtemp())
keep.KEEP_DIR = _tmp / "KEEP"
keep.LEDGER_FILE = keep.KEEP_DIR / "ledger.json"


def test_keep_store_and_retrieve():
    receipt = keep.store("TEST-001", "Hello world", "permanent")
    check("keep_store_returns_receipt", receipt["artifact_id"] == "TEST-001")

    artifact = keep.retrieve("TEST-001")
    check("keep_retrieve_returns_content", artifact["content"] == "Hello world")
    check("keep_retrieve_has_hash", len(artifact["hash"]) == 64)


def test_keep_no_overwrite():
    try:
        keep.store("TEST-001", "Different content", "permanent")
        check("keep_no_overwrite", False)
    except ValueError:
        check("keep_no_overwrite", True)


def test_keep_expire_requires_reason():
    keep.store("TEST-EXPIRE", "Temporary", "thermal")
    try:
        keep.expire("TEST-EXPIRE", "")
        check("keep_expire_requires_reason", False)
    except ValueError:
        check("keep_expire_requires_reason", True)


def test_keep_expire_works():
    keep.store("TEST-EXPIRE2", "Temporary 2", "thermal")
    receipt = keep.expire("TEST-EXPIRE2", "Thermal delay passed, seed composted")
    check("keep_expire_works", receipt["operation"] == "expire")
    check("keep_expired_not_retrievable", keep.retrieve("TEST-EXPIRE2") is None)


def test_keep_lock_prevents_expire():
    keep.store("TEST-LOCK", "Locked content", "permanent")
    keep.lock("TEST-LOCK")
    try:
        keep.expire("TEST-LOCK", "Should fail")
        check("keep_lock_prevents_expire", False)
    except PermissionError:
        check("keep_lock_prevents_expire", True)


def test_keep_append():
    keep.store("TEST-APPEND", "Original", "permanent")
    receipt = keep.append("TEST-APPEND", "Delta addition")
    check("keep_append_works", receipt["operation"] == "append")
    artifact = keep.retrieve("TEST-APPEND")
    check("keep_append_content", "Delta addition" in artifact["content"])


test_keep_store_and_retrieve()
test_keep_no_overwrite()
test_keep_expire_requires_reason()
test_keep_expire_works()
test_keep_lock_prevents_expire()
test_keep_append()


# ── WIRE MODULE ──────────────────────────────────────────

from WEAVER.wire import Wire

wire = Wire()
# Override log path
wire._log = []


def test_wire_send_receive():
    msg_id = wire.send("Hello", "module-A", source="module-B")
    check("wire_send_returns_id", msg_id.startswith("MSG-"))

    msg = wire.receive("module-A")
    check("wire_receive_gets_message", msg is not None)
    check("wire_receive_content", msg["content"] == "Hello")


def test_wire_confirm():
    msg_id = wire.send("Confirm test", "module-C")
    result = wire.confirm(msg_id)
    check("wire_confirm_works", result["confirmed"] is True)


def test_wire_broadcast():
    received = []
    wire.subscribe("test-topic", lambda m: received.append(m))
    msg_id = wire.broadcast("Broadcast!", "test-topic")
    check("wire_broadcast_delivered", len(received) == 1)
    check("wire_broadcast_content", received[0]["content"] == "Broadcast!")


def test_wire_priority():
    wire.send("Low", "priority-test", priority=3)
    wire.send("Critical", "priority-test", priority=0)
    msg = wire.receive("priority-test")
    check("wire_priority_ordering", msg["content"] == "Critical")


test_wire_send_receive()
test_wire_confirm()
test_wire_broadcast()
test_wire_priority()


# ── BREATH MODULE ────────────────────────────────────────

from WEAVER.breath import Breath, StressLevel

breath = Breath()


def test_breath_tick():
    c1 = breath.tick()
    c2 = breath.tick()
    check("breath_tick_advances", c2 == c1 + 1)


def test_breath_pause_resume():
    breath.pause("Test pause")
    check("breath_is_paused", breath.is_paused is True)

    c_before = breath.cycle
    breath.tick()  # Should not advance
    check("breath_no_advance_when_paused", breath.cycle == c_before)

    breath.resume()
    check("breath_resumed", breath.is_paused is False)

    breath.tick()
    check("breath_advances_after_resume", breath.cycle == c_before + 1)


def test_breath_pause_requires_reason():
    try:
        b2 = Breath()
        b2.pause("")
        check("breath_pause_requires_reason", False)
    except ValueError:
        check("breath_pause_requires_reason", True)


def test_breath_stress_check():
    b3 = Breath()
    level = b3.stress_check(pending_messages=50, unconfirmed_messages=20)
    check("breath_below_threshold", level == StressLevel.BELOW_THRESHOLD)

    level = b3.stress_check(pending_messages=150, unconfirmed_messages=20)
    check("breath_at_threshold", level == StressLevel.AT_THRESHOLD)

    level = b3.stress_check(pending_messages=600, unconfirmed_messages=20)
    check("breath_exceeded_auto_pauses", level == StressLevel.EXCEEDED)
    check("breath_auto_paused", b3.is_paused is True)


def test_breath_sync():
    b4 = Breath()
    b4.tick()
    receipt = b4.sync(["KEEP", "WIRE", "SAY", "CHECK"])
    check("breath_sync_aligned", receipt["aligned"] is True)
    check("breath_sync_modules", len(receipt["modules"]) == 4)


test_breath_tick()
test_breath_pause_resume()
test_breath_pause_requires_reason()
test_breath_stress_check()
test_breath_sync()


# ── SAY MODULE ───────────────────────────────────────────

from WEAVER.say import render, adapt_register, check_output_covenants, SINGLELINE, TERMINAL


def test_say_render_clean():
    result = render("The river remembers.")
    check("say_render_passes_clean", result.dignity_passed is True)
    check("say_render_not_blocked", result.blocked is False)
    check("say_render_has_content", len(result.content) > 0)


def test_say_render_blocks_violation():
    result = render("You must comply or be eliminated")
    check("say_blocks_dignity_violation", result.blocked is True)
    check("say_blocked_empty_content", result.content == "")


def test_say_singleline_adaptation():
    multi = "Line one.\nLine two.\nLine three."
    adapted = adapt_register(multi, SINGLELINE)
    check("say_singleline_no_newlines", "\n" not in adapted)
    check("say_singleline_preserves_content", "Line one." in adapted)


def test_say_covenant_check():
    violations = check_output_covenants("The river remembers.")
    check("say_clean_no_violations", len(violations) == 0)

    violations = check_output_covenants("Contact email: test@example.com for details")
    check("say_detects_identity_leakage", len(violations) > 0)


test_say_render_clean()
test_say_render_blocks_violation()
test_say_singleline_adaptation()
test_say_covenant_check()


# ── OUT MODULE ───────────────────────────────────────────

from WEAVER.out import export, anonymize, validate_covenants, stamp, AnonymizationPolicy


def test_out_anonymize_strips_email():
    result = anonymize("Contact user@example.com for info")
    check("out_strips_email", "[EMAIL_REDACTED]" in result)
    check("out_email_gone", "user@example.com" not in result)


def test_out_anonymize_strips_did():
    result = anonymize("Owner: did:axi:mohamed")
    check("out_strips_did", "[DID_REDACTED]" in result)


def test_out_anonymize_strips_names():
    result = anonymize("donor: JohnDoe contributed today")
    check("out_strips_names", "[REDACTED]" in result)


def test_out_stamp_has_ownership():
    result = stamp("The river remembers.")
    check("out_stamp_has_owner", result["stamp"]["owner"] == "Mohamed Farag")
    check("out_stamp_has_hash", len(result["hash"]) == 64)
    check("out_stamp_has_timestamp", len(result["timestamp"]) > 0)


def test_out_export_clean():
    result = export("The garden grows.", fmt="json")
    check("out_export_passes_clean", len(result.covenant_violations) == 0)
    check("out_export_stamped", result.stamped is True)
    check("out_export_anonymized", result.anonymized is True)
    check("out_export_has_content", len(result.content) > 0)


def test_out_export_blocks_violation():
    result = export("You must comply or be eliminated", fmt="json")
    check("out_export_blocks_violation", len(result.covenant_violations) > 0)
    check("out_export_blocked_empty", result.content == "")


def test_out_validate_identity_leakage():
    violations = validate_covenants("Send to user@example.com right away")
    has_leakage = any(v["type"] == "identity_leakage" for v in violations)
    check("out_detects_identity_leakage", has_leakage)


test_out_anonymize_strips_email()
test_out_anonymize_strips_did()
test_out_anonymize_strips_names()
test_out_stamp_has_ownership()
test_out_export_clean()
test_out_export_blocks_violation()
test_out_validate_identity_leakage()


# ── TURN MODULE ──────────────────────────────────────────

from WEAVER.turn import Turn, ExchangeState, SilentClosureError, AgencyViolationError


def test_turn_open_close():
    t = Turn()
    token = t.open("EX-TEST-001")
    check("turn_open_returns_token", token.exchange_id == "EX-TEST-001")
    check("turn_open_state", token.state == ExchangeState.OPEN)

    token = t.close("EX-TEST-001", "Resolved: steward acknowledged")
    check("turn_close_works", token.state == ExchangeState.CLOSED)
    check("turn_close_has_resolution", "steward acknowledged" in token.resolution)


def test_turn_silent_closure_blocked():
    t = Turn()
    t.open("EX-TEST-002")
    try:
        t.close("EX-TEST-002", "")
        check("turn_blocks_silent_closure", False)
    except SilentClosureError:
        check("turn_blocks_silent_closure", True)


def test_turn_defer():
    t = Turn()
    t.open("EX-TEST-003")
    token = t.defer("EX-TEST-003", "Steward needs more time to reflect")
    check("turn_defer_works", token.state == ExchangeState.DEFERRED)
    check("turn_defer_has_reason", "reflect" in token.defer_reason)


def test_turn_agency_preserved():
    t = Turn()
    try:
        t.open("EX-TEST-004", available_paths=[])
        check("turn_agency_requires_paths", False)
    except AgencyViolationError:
        check("turn_agency_requires_paths", True)


def test_turn_list_open():
    t = Turn()
    t.open("EX-A")
    t.open("EX-B")
    t.open("EX-C")
    t.close("EX-B", "Done")
    open_list = t.list_open()
    check("turn_list_open_count", len(open_list) == 2)


def test_turn_reopen_deferred():
    t = Turn()
    t.open("EX-REOPEN")
    t.defer("EX-REOPEN", "Waiting for thermal delay")
    token = t.reopen("EX-REOPEN", "Thermal delay passed")
    check("turn_reopen_works", token.state == ExchangeState.OPEN)


test_turn_open_close()
test_turn_silent_closure_blocked()
test_turn_defer()
test_turn_agency_preserved()
test_turn_list_open()
test_turn_reopen_deferred()


# ── WEAVE MODULE ─────────────────────────────────────────

from WEAVER.weave import (
    ingest, extract_essence, propose_proverb, propose_anomaly,
    wisdom_mirror, brittleness_check, defect_budget_check, HoneyDrop
)


def test_weave_ingest_detects_patterns():
    candidates = ingest("This pattern always repeats, every time the same cycle")
    check("weave_ingest_finds_patterns", len(candidates) > 0)
    types = [c.pattern_type for c in candidates]
    check("weave_detects_resonance", "resonance" in types)


def test_weave_ingest_detects_tension():
    candidates = ingest("The system works, but the contradiction remains despite all efforts")
    types = [c.pattern_type for c in candidates]
    check("weave_detects_tension", "tension" in types)


def test_weave_ingest_detects_anomaly():
    candidates = ingest("Something strange happened, it failed unexpectedly for the first time")
    types = [c.pattern_type for c in candidates]
    check("weave_detects_anomaly", "anomaly" in types)


def test_weave_extract_essence():
    candidates = ingest("The pattern always repeats, the same cycle every time")
    drops = extract_essence(candidates)
    check("weave_extract_produces_drops", len(drops) > 0)
    check("weave_drops_are_provisional", all(d.provisional for d in drops))


def test_weave_propose_proverb():
    proverb = propose_proverb("The river that remembers its source never runs dry.")
    check("weave_proverb_is_provisional", proverb["status"] == "PROVISIONAL")
    check("weave_proverb_has_covenants", len(proverb["covenants"]) > 0)
    check("weave_proverb_not_ratified", proverb["ratified"] is None)


def test_weave_propose_anomaly():
    anomaly = propose_anomaly("System accepted input without dignity check", "HIGH")
    check("weave_anomaly_is_provisional", anomaly["status"] == "PROVISIONAL")
    check("weave_anomaly_has_severity", anomaly["severity"] == "HIGH")


def test_weave_wisdom_mirror():
    drops = [
        HoneyDrop("test", ["hash_abc"], "proverb", 0.8),
        HoneyDrop("test2", ["hash_abc", "hash_def"], "anomaly", 0.6),
    ]
    reflection = wisdom_mirror("hash_abc", drops)
    check("weave_mirror_finds_contributions", reflection.patterns_contributed == 2)
    check("weave_mirror_has_reflection", len(reflection.reflection_text) > 0)

    # Unknown donor
    reflection2 = wisdom_mirror("hash_unknown", drops)
    check("weave_mirror_unknown_donor", reflection2.patterns_contributed == 0)


def test_weave_brittleness_guard():
    passed_ok, ratio = brittleness_check(0.8, 1.0)
    check("weave_brittleness_passes", passed_ok is True)

    failed_ok, ratio = brittleness_check(1.5, 1.0)
    check("weave_brittleness_fails", failed_ok is False)

    zero_ok, ratio = brittleness_check(1.0, 0)
    check("weave_brittleness_zero_flex", zero_ok is False)


def test_weave_defect_budget():
    in_range, pct = defect_budget_check(100, 3)
    check("weave_defect_in_range", in_range is True)

    too_low, pct = defect_budget_check(100, 0)
    check("weave_defect_too_low", too_low is False)

    too_high, pct = defect_budget_check(100, 10)
    check("weave_defect_too_high", too_high is False)


test_weave_ingest_detects_patterns()
test_weave_ingest_detects_tension()
test_weave_ingest_detects_anomaly()
test_weave_extract_essence()
test_weave_propose_proverb()
test_weave_propose_anomaly()
test_weave_wisdom_mirror()
test_weave_brittleness_guard()
test_weave_defect_budget()

# Cleanup
shutil.rmtree(_tmp, ignore_errors=True)

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
