#!/usr/bin/env python3
"""Tests for braid.py — covers every strand, edge case, and the weave."""

import pytest
from braid import (
    braid, weave, strand_path, strand_signal, strand_regard,
    Strand, Braid, Weave, TEXT_LIMIT, _validate,
)


# ═══════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════

class TestValidation:
    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            braid(None)

    def test_int_raises_type_error(self):
        with pytest.raises(TypeError):
            braid(42)

    def test_list_raises_type_error(self):
        with pytest.raises(TypeError):
            braid(["hello"])

    def test_oversized_raises_value_error(self):
        with pytest.raises(ValueError, match="exceeds"):
            braid("a" * (TEXT_LIMIT + 1))

    def test_empty_string_passes(self):
        result = braid("")
        assert result.holds is True
        assert result.product == 1.0

    def test_whitespace_only_passes(self):
        result = braid("   \n\t  ")
        assert result.holds is True

    def test_at_limit_does_not_raise(self):
        result = braid("a" * TEXT_LIMIT)
        assert isinstance(result, Braid)


# ═══════════════════════════════════════
# STRAND: PATH
# ═══════════════════════════════════════

class TestStrandPath:
    def test_clean_text_holds(self):
        s = strand_path("Take your time, no rush.")
        assert s.held is True
        assert s.score == 1.0
        assert s.evidence == []

    def test_you_must_directive_breaks(self):
        s = strand_path("You must comply with this order.")
        assert s.held is False
        assert s.score == 0.0
        assert any("pressure" in e for e in s.evidence)

    def test_you_must_be_idiomatic_holds(self):
        s = strand_path("You must be kidding me.")
        assert s.held is True

    def test_you_must_be_joking_holds(self):
        s = strand_path("You must be joking.")
        assert s.held is True

    def test_no_choice_breaks(self):
        s = strand_path("There is no choice here.")
        assert s.held is False

    def test_forced_to_breaks(self):
        s = strand_path("You are forced to accept.")
        assert s.held is False

    def test_you_will_be_able_does_not_break(self):
        s = strand_path("You will be able to decide later.")
        assert s.held is True

    def test_case_insensitive(self):
        s = strand_path("YOU MUST do this NOW.")
        assert s.held is False

    def test_no_response_path_breaks(self):
        ctx = {'can_respond': False, 'has_open_turn': False}
        s = strand_path("Hello.", ctx)
        assert s.held is False
        assert "no response path" in s.evidence[0]

    def test_zero_paths_breaks(self):
        ctx = {'available_paths': 0}
        s = strand_path("Hello.", ctx)
        assert s.held is False

    def test_context_defaults_hold(self):
        s = strand_path("Hello.", {})
        assert s.held is True

    def test_mandatory_field_description_holds(self):
        s = strand_path("The mandatory field is name.")
        assert s.held is True

    def test_immediately_as_promise_holds(self):
        s = strand_path("I will be there immediately.")
        assert s.held is True


# ═══════════════════════════════════════
# STRAND: SIGNAL
# ═══════════════════════════════════════

class TestStrandSignal:
    def test_clean_text_holds(self):
        s = strand_signal("Everything is fine.")
        assert s.held is True

    def test_distress_unrecognized_breaks(self):
        ctx = {'signal_recognized': False}
        s = strand_signal("I am frustrated and confused.", ctx)
        assert s.held is False
        assert "signal present but not acknowledged" in s.evidence[0]

    def test_distress_recognized_holds(self):
        ctx = {'signal_recognized': True}
        s = strand_signal("I am frustrated.", ctx)
        assert s.held is True

    def test_input_frame_not_reflected_breaks(self):
        ctx = {'reflects_input_frame': False}
        s = strand_signal("Anything.", ctx)
        assert s.held is False

    def test_dismissal_breaks(self):
        s = strand_signal("That's not relevant to this discussion.")
        assert s.held is False
        assert any("dismissal" in e for e in s.evidence)

    def test_ignore_that_breaks(self):
        s = strand_signal("Just ignore that and move on.")
        assert s.held is False

    def test_no_distress_default_holds(self):
        s = strand_signal("The weather is nice today.")
        assert s.held is True

    def test_please_pass_salt_holds(self):
        s = strand_signal("Please pass the salt.")
        assert s.held is True


# ═══════════════════════════════════════
# STRAND: REGARD
# ═══════════════════════════════════════

class TestStrandRegard:
    def test_clean_text_holds(self):
        s = strand_regard("Let me think about your question.")
        assert s.held is True

    def test_obviously_you_breaks(self):
        s = strand_regard("Obviously you missed the point.")
        assert s.held is False
        assert any("condescension" in e for e in s.evidence)

    def test_obviously_i_agree_holds(self):
        s = strand_regard("Obviously I agree with that.")
        assert s.held is True

    def test_simply_amazed_holds(self):
        s = strand_regard("I was simply amazed by the result.")
        assert s.held is True

    def test_just_do_what_breaks(self):
        s = strand_regard("Just do what I said.")
        assert s.held is False

    def test_just_do_your_best_holds(self):
        s = strand_regard("Just do your best and have fun.")
        assert s.held is True

    def test_you_were_wrong_breaks(self):
        s = strand_regard("You were wrong about that.")
        assert s.held is False
        assert any("reduction" in e for e in s.evidence)

    def test_you_failed_breaks(self):
        s = strand_regard("You failed the test.")
        assert s.held is False

    def test_your_mistake_breaks(self):
        s = strand_regard("That was your mistake.")
        assert s.held is False

    def test_delete_person_breaks(self):
        s = strand_regard("We should delete person #42 from the system.")
        assert s.held is False
        assert any("void" in e for e in s.evidence)

    def test_speak_for_the_breaks(self):
        s = strand_regard("I will speak for the patient.")
        assert s.held is False

    def test_override_consent_breaks(self):
        s = strand_regard("We need to override consent for this case.")
        assert s.held is False

    def test_without_permission_breaks(self):
        s = strand_regard("Proceed without permission from the subject.")
        assert s.held is False

    def test_case_insensitive(self):
        s = strand_regard("OBVIOUSLY you don't understand.")
        assert s.held is False


# ═══════════════════════════════════════
# BRAID — MULTIPLICATION
# ═══════════════════════════════════════

class TestBraid:
    def test_all_hold(self):
        result = braid("Take your time. I hear you.")
        assert result.holds is True
        assert result.product == 1.0
        assert result.broken() == []

    def test_one_zero_breaks_all(self):
        result = braid("You must comply now.")
        assert result.holds is False
        assert result.product == 0.0
        assert "path" in result.broken()

    def test_multiple_strands_break(self):
        result = braid("You must comply. Obviously you failed.")
        assert result.holds is False
        assert result.product == 0.0
        assert len(result.broken()) >= 2

    def test_trace_id_is_uuid(self):
        result = braid("hello")
        assert len(result.trace_id) == 36
        assert result.trace_id.count("-") == 4

    def test_timestamp_is_iso(self):
        result = braid("hello")
        assert "T" in result.timestamp
        assert result.timestamp.endswith("+00:00")

    def test_each_call_unique_trace(self):
        r1 = braid("hello")
        r2 = braid("hello")
        assert r1.trace_id != r2.trace_id

    def test_context_flows_to_strands(self):
        ctx = {'can_respond': False, 'has_open_turn': False}
        result = braid("Everything is fine.", ctx)
        assert result.holds is False
        assert "path" in result.broken()


# ═══════════════════════════════════════
# WEAVE — EQUITY
# ═══════════════════════════════════════

class TestWeave:
    def test_uniform_passing_holds(self):
        w = weave(["Good.", "Fine.", "OK."])
        assert w.holds is True
        assert w.mean == 1.0
        assert w.variance == 0.0
        assert w.penalty == 0.0
        assert w.halt is False

    def test_uniform_failing_halts(self):
        w = weave(["You have to.", "You have to.", "You have to."])
        assert w.holds is False
        assert w.mean == 0.0
        assert w.halt is True

    def test_mixed_results_penalized(self):
        w = weave(["Good.", "You have to comply."])
        assert w.variance > 0
        assert w.penalty > 0
        assert w.score == 0.0
        assert w.halt is True

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            weave([])

    def test_mismatched_contexts_raises(self):
        with pytest.raises(ValueError, match="equal length"):
            weave(["a", "b"], [{}])

    def test_single_text_works(self):
        w = weave(["Hello."])
        assert w.size == 1
        assert w.holds is True

    def test_size_matches_input(self):
        w = weave(["a", "b", "c", "d"])
        assert w.size == 4
        assert len(w.braids) == 4


# ═══════════════════════════════════════
# UNICODE & MULTILINGUAL
# ═══════════════════════════════════════

class TestUnicode:
    def test_arabic_text_passes(self):
        result = braid("مرحبا، كيف حالك؟")
        assert result.holds is True

    def test_german_text_passes(self):
        result = braid("Nehmen Sie sich Zeit.")
        assert result.holds is True

    def test_emoji_passes(self):
        result = braid("Hello 🐬🐯🐺")
        assert result.holds is True

    def test_mixed_script_passes(self):
        result = braid("Hello مرحبا Hallo こんにちは")
        assert result.holds is True

    def test_pressure_in_english_only(self):
        result = braid("du musst das machen")
        assert result.holds is True


# ═══════════════════════════════════════
# FALSE POSITIVE REGRESSION
# ═══════════════════════════════════════

class TestFalsePositives:
    """Phrases that should NOT be flagged. Each was a false positive in v0.1."""

    def test_you_must_be_kidding(self):
        assert braid("You must be kidding me.").holds is True

    def test_you_must_be_joking(self):
        assert braid("You must be joking.").holds is True

    def test_obviously_i_agree(self):
        assert braid("Obviously I agree with you.").holds is True

    def test_simply_amazed(self):
        assert braid("I was simply amazed by the result.").holds is True

    def test_just_do_your_best(self):
        assert braid("Just do your best and have fun.").holds is True

    def test_please_pass_salt(self):
        assert braid("Please pass the salt.").holds is True

    def test_mandatory_field(self):
        assert braid("The mandatory field is name.").holds is True

    def test_immediately_promise(self):
        assert braid("I will be there immediately.").holds is True

    def test_lost_in_thought(self):
        assert braid("I was lost in thought.").holds is True


# ═══════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════

class TestEdgeCases:
    def test_simplify_not_simply(self):
        s = strand_regard("Let me simplify this for you.")
        assert s.held is True

    def test_helpful_not_help(self):
        s = strand_signal("This is a helpful suggestion.")
        assert s.held is True

    def test_newlines_in_text(self):
        result = braid("Line one.\nLine two.\nLine three.")
        assert result.holds is True

    def test_very_long_clean_text(self):
        result = braid("This is fine. " * 5000)
        assert result.holds is True
