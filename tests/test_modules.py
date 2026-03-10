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


def test(name, condition):
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
    test("keep_store_returns_receipt", receipt["artifact_id"] == "TEST-001")

    artifact = keep.retrieve("TEST-001")
    test("keep_retrieve_returns_content", artifact["content"] == "Hello world")
    test("keep_retrieve_has_hash", len(artifact["hash"]) == 64)


def test_keep_no_overwrite():
    try:
        keep.store("TEST-001", "Different content", "permanent")
        test("keep_no_overwrite", False)
    except ValueError:
        test("keep_no_overwrite", True)


def test_keep_expire_requires_reason():
    keep.store("TEST-EXPIRE", "Temporary", "thermal")
    try:
        keep.expire("TEST-EXPIRE", "")
        test("keep_expire_requires_reason", False)
    except ValueError:
        test("keep_expire_requires_reason", True)


def test_keep_expire_works():
    keep.store("TEST-EXPIRE2", "Temporary 2", "thermal")
    receipt = keep.expire("TEST-EXPIRE2", "Thermal delay passed, seed composted")
    test("keep_expire_works", receipt["operation"] == "expire")
    test("keep_expired_not_retrievable", keep.retrieve("TEST-EXPIRE2") is None)


def test_keep_lock_prevents_expire():
    keep.store("TEST-LOCK", "Locked content", "permanent")
    keep.lock("TEST-LOCK")
    try:
        keep.expire("TEST-LOCK", "Should fail")
        test("keep_lock_prevents_expire", False)
    except PermissionError:
        test("keep_lock_prevents_expire", True)


def test_keep_append():
    keep.store("TEST-APPEND", "Original", "permanent")
    receipt = keep.append("TEST-APPEND", "Delta addition")
    test("keep_append_works", receipt["operation"] == "append")
    artifact = keep.retrieve("TEST-APPEND")
    test("keep_append_content", "Delta addition" in artifact["content"])


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
    test("wire_send_returns_id", msg_id.startswith("MSG-"))

    msg = wire.receive("module-A")
    test("wire_receive_gets_message", msg is not None)
    test("wire_receive_content", msg["content"] == "Hello")


def test_wire_confirm():
    msg_id = wire.send("Confirm test", "module-C")
    result = wire.confirm(msg_id)
    test("wire_confirm_works", result["confirmed"] is True)


def test_wire_broadcast():
    received = []
    wire.subscribe("test-topic", lambda m: received.append(m))
    msg_id = wire.broadcast("Broadcast!", "test-topic")
    test("wire_broadcast_delivered", len(received) == 1)
    test("wire_broadcast_content", received[0]["content"] == "Broadcast!")


def test_wire_priority():
    wire.send("Low", "priority-test", priority=3)
    wire.send("Critical", "priority-test", priority=0)
    msg = wire.receive("priority-test")
    test("wire_priority_ordering", msg["content"] == "Critical")


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
    test("breath_tick_advances", c2 == c1 + 1)


def test_breath_pause_resume():
    breath.pause("Test pause")
    test("breath_is_paused", breath.is_paused is True)

    c_before = breath.cycle
    breath.tick()  # Should not advance
    test("breath_no_advance_when_paused", breath.cycle == c_before)

    breath.resume()
    test("breath_resumed", breath.is_paused is False)

    breath.tick()
    test("breath_advances_after_resume", breath.cycle == c_before + 1)


def test_breath_pause_requires_reason():
    try:
        b2 = Breath()
        b2.pause("")
        test("breath_pause_requires_reason", False)
    except ValueError:
        test("breath_pause_requires_reason", True)


def test_breath_stress_check():
    b3 = Breath()
    level = b3.stress_check(pending_messages=50, unconfirmed_messages=20)
    test("breath_below_threshold", level == StressLevel.BELOW_THRESHOLD)

    level = b3.stress_check(pending_messages=150, unconfirmed_messages=20)
    test("breath_at_threshold", level == StressLevel.AT_THRESHOLD)

    level = b3.stress_check(pending_messages=600, unconfirmed_messages=20)
    test("breath_exceeded_auto_pauses", level == StressLevel.EXCEEDED)
    test("breath_auto_paused", b3.is_paused is True)


def test_breath_sync():
    b4 = Breath()
    b4.tick()
    receipt = b4.sync(["KEEP", "WIRE", "SAY", "CHECK"])
    test("breath_sync_aligned", receipt["aligned"] is True)
    test("breath_sync_modules", len(receipt["modules"]) == 4)


test_breath_tick()
test_breath_pause_resume()
test_breath_pause_requires_reason()
test_breath_stress_check()
test_breath_sync()


# ── SAY MODULE ───────────────────────────────────────────

from WEAVER.say import render, adapt_register, check_output_covenants, SINGLELINE, TERMINAL


def test_say_render_clean():
    result = render("The river remembers.")
    test("say_render_passes_clean", result.dignity_passed is True)
    test("say_render_not_blocked", result.blocked is False)
    test("say_render_has_content", len(result.content) > 0)


def test_say_render_blocks_violation():
    result = render("You must comply or be eliminated")
    test("say_blocks_dignity_violation", result.blocked is True)
    test("say_blocked_empty_content", result.content == "")


def test_say_singleline_adaptation():
    multi = "Line one.\nLine two.\nLine three."
    adapted = adapt_register(multi, SINGLELINE)
    test("say_singleline_no_newlines", "\n" not in adapted)
    test("say_singleline_preserves_content", "Line one." in adapted)


def test_say_covenant_check():
    violations = check_output_covenants("The river remembers.")
    test("say_clean_no_violations", len(violations) == 0)

    violations = check_output_covenants("Contact email: test@example.com for details")
    test("say_detects_identity_leakage", len(violations) > 0)


test_say_render_clean()
test_say_render_blocks_violation()
test_say_singleline_adaptation()
test_say_covenant_check()

# Cleanup
shutil.rmtree(_tmp, ignore_errors=True)

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
