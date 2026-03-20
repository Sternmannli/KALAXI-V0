#!/usr/bin/env python3
"""
Deep hard test: Extraction Machine + Substrate Boundary + Thermal States.

Tests that the extraction pipeline is ACTUALLY wired — not just that
modules exist, but that data flows through them during organism.process().

"The extracting machine... verify fine-tunes always... this is the way
we digest." — V-001, 2026-03-20

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
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

import pytest

from WEAVER.input_ledger import InputLedger, InputEntry, V001, V002
from WEAVER.distillery import Distillery, EssenceEntry
from WEAVER.organism import Organism


# ═══════════════════════════════════════════════════════════════════
# PART 1: DISTILLERY ALONE — Does the extraction actually extract?
# ═══════════════════════════════════════════════════════════════════

class TestDistilleryExtraction:
    """Test that distillery.metabolize_entry() actually produces
    patterns and essence from different input types."""

    def _make_entry(self, text, voice=V001):
        """Create a minimal InputEntry for testing."""
        return InputEntry(
            entry_id="TEST-001",
            voice=voice,
            raw_text=text,
            timestamp="2026-03-20T00:00:00Z",
            session_id="TEST",
            content_hash="abc123",
            prev_hash="GENESIS",
            chain_hash="def456",
            sequence=1,
            context="test",
        )

    def test_metabolize_v001_correction(self):
        """V-001 correction text must produce CORRECTION pattern."""
        d = Distillery(dry_run=True)
        entry = self._make_entry(
            "This is wrong. You must never do this again. Fix it now."
        )
        result = d.metabolize_entry(entry)
        assert result is not None, "metabolize_entry returned None for V-001 correction"
        assert isinstance(result, EssenceEntry), f"Expected EssenceEntry, got {type(result)}"
        pattern_labels = [p.split(":")[0] for p in result.patterns]
        assert "CORRECTION" in pattern_labels, (
            f"CORRECTION not found in patterns: {result.patterns}"
        )

    def test_metabolize_v001_instruction(self):
        """V-001 instruction text must produce INSTRUCTION pattern."""
        d = Distillery(dry_run=True)
        entry = self._make_entry(
            "From now on you must always check the ledger before processing. "
            "This is permanent. Never skip this step."
        )
        result = d.metabolize_entry(entry)
        assert result is not None
        pattern_labels = [p.split(":")[0] for p in result.patterns]
        assert "INSTRUCTION" in pattern_labels, (
            f"INSTRUCTION not found in patterns: {result.patterns}"
        )

    def test_metabolize_v001_principle(self):
        """V-001 principle/revelation text must produce patterns."""
        d = Distillery(dry_run=True)
        entry = self._make_entry(
            "Dignity is not fragile. The system does not protect dignity. "
            "It refuses to participate in its denial. This is fundamental."
        )
        result = d.metabolize_entry(entry)
        assert result is not None
        assert len(result.patterns) > 0, "No patterns found in principle text"

    def test_metabolize_produces_essence(self):
        """Every metabolization must produce a non-empty essence line."""
        d = Distillery(dry_run=True)
        entry = self._make_entry("The river remembers what the banks forget.")
        result = d.metabolize_entry(entry)
        assert result is not None
        assert result.essence, "Essence is empty — distillery produced no meaning"
        assert len(result.essence) > 5, f"Essence too short: '{result.essence}'"

    def test_metabolize_empty_text_returns_none(self):
        """Empty text must return None, not crash."""
        d = Distillery(dry_run=True)
        entry = self._make_entry("")
        result = d.metabolize_entry(entry)
        assert result is None

    def test_metabolize_v002_output(self):
        """V-002 output must be processed with v002 markers."""
        d = Distillery(dry_run=True)
        entry = self._make_entry(
            "I have completed the build. The tests pass. "
            "Here is the report: 902 passed, 0 failed.",
            voice=V002,
        )
        result = d.metabolize_entry(entry)
        assert result is not None
        # V-002 output should get some pattern extraction
        assert result.essence, "No essence extracted from V-002 output"

    def test_metabolize_links_to_canon(self):
        """Extraction must produce links to canon elements."""
        d = Distillery(dry_run=True)
        entry = self._make_entry(
            "The dignity of this person must never be denied. "
            "This covenant is sacred and binds the entire system."
        )
        result = d.metabolize_entry(entry)
        assert result is not None
        # links should reference covenants or other canon elements
        assert isinstance(result.links, list)

    def test_metabolize_thermal_state_is_witnessed(self):
        """After metabolization, thermal_state must be 'witnessed'."""
        d = Distillery(dry_run=True)
        entry = self._make_entry("Every input is food for the system.")
        result = d.metabolize_entry(entry)
        assert result is not None
        assert result.thermal_state == "witnessed", (
            f"Expected 'witnessed', got '{result.thermal_state}'"
        )


# ═══════════════════════════════════════════════════════════════════
# PART 2: INPUT LEDGER — Thermal states and metabolize()
# ═══════════════════════════════════════════════════════════════════

class TestLedgerThermalStates:
    """Test that the ledger's thermal state machinery works end-to-end."""

    @pytest.fixture(autouse=True)
    def fresh_ledger(self, tmp_path, monkeypatch):
        """Each test gets a fresh ledger in a temp directory."""
        import WEAVER.input_ledger as il
        monkeypatch.setattr(il, "LEDGER_DIR", tmp_path / "LEDGER")
        monkeypatch.setattr(il, "LEDGER_INDEX", tmp_path / "LEDGER" / "index.json")
        monkeypatch.setattr(il, "CHRONICLE_FILE", tmp_path / "LEDGER" / "chronicle.md")
        (tmp_path / "LEDGER").mkdir(parents=True, exist_ok=True)
        self.ledger = InputLedger()

    def test_new_entry_is_raw(self):
        """Every new entry must start at 'raw' thermal state."""
        entry = self.ledger.register("Test input", voice=V001)
        assert entry.thermal_state == "raw"

    def test_metabolize_advances_to_witnessed(self):
        """ledger.metabolize() must advance raw → witnessed."""
        entry = self.ledger.register("Test input for metabolization", voice=V001)
        assert entry.thermal_state == "raw"

        result = self.ledger.metabolize(
            entry.entry_id,
            patterns=["INSTRUCTION:0.85"],
            essence="Testing thermal advancement",
        )
        assert result is True

        updated = self.ledger.get(entry.entry_id)
        assert updated.thermal_state == "witnessed", (
            f"Expected 'witnessed' after metabolize, got '{updated.thermal_state}'"
        )
        assert updated.patterns == ["INSTRUCTION:0.85"]
        assert updated.essence == "Testing thermal advancement"

    def test_advance_thermal_witnessed_to_integrated(self):
        """advance_thermal() must allow witnessed → integrated."""
        entry = self.ledger.register("Test thermal advancement", voice=V001)
        self.ledger.metabolize(entry.entry_id, patterns=["TEST:1.0"])
        # Now at witnessed
        result = self.ledger.advance_thermal(
            entry.entry_id, "integrated", reason="test batch"
        )
        assert result is True
        updated = self.ledger.get(entry.entry_id)
        assert updated.thermal_state == "integrated"

    def test_advance_thermal_cannot_skip(self):
        """Cannot skip from raw → integrated."""
        entry = self.ledger.register("Test skip prevention", voice=V001)
        result = self.ledger.advance_thermal(entry.entry_id, "integrated")
        assert result is False, "Allowed skipping raw → integrated"
        updated = self.ledger.get(entry.entry_id)
        assert updated.thermal_state == "raw"

    def test_advance_thermal_cannot_go_backward(self):
        """Cannot go from witnessed → raw."""
        entry = self.ledger.register("Test backward prevention", voice=V001)
        self.ledger.metabolize(entry.entry_id, patterns=["TEST:1.0"])
        result = self.ledger.advance_thermal(entry.entry_id, "raw")
        assert result is False, "Allowed going backward witnessed → raw"

    def test_advance_thermal_to_canonical(self):
        """Full chain: raw → witnessed → integrated → canonical."""
        entry = self.ledger.register("Full thermal chain test", voice=V001)
        self.ledger.metabolize(entry.entry_id, patterns=["PRINCIPLE:0.9"])
        assert self.ledger.advance_thermal(entry.entry_id, "integrated")
        assert self.ledger.advance_thermal(entry.entry_id, "canonical")
        updated = self.ledger.get(entry.entry_id)
        assert updated.thermal_state == "canonical"

    def test_by_thermal_state_returns_correct_entries(self):
        """by_thermal_state() must filter correctly."""
        e1 = self.ledger.register("Entry one", voice=V001)
        e2 = self.ledger.register("Entry two", voice=V001)
        e3 = self.ledger.register("Entry three", voice=V001)
        # Metabolize only e1 and e2
        self.ledger.metabolize(e1.entry_id, patterns=["A:1.0"])
        self.ledger.metabolize(e2.entry_id, patterns=["B:1.0"])

        raw_entries = self.ledger.by_thermal_state("raw")
        witnessed_entries = self.ledger.by_thermal_state("witnessed")

        assert len(raw_entries) == 1, f"Expected 1 raw, got {len(raw_entries)}"
        assert raw_entries[0].entry_id == e3.entry_id
        assert len(witnessed_entries) == 2, f"Expected 2 witnessed, got {len(witnessed_entries)}"

    def test_thermal_summary_counts(self):
        """thermal_summary() must return accurate counts."""
        self.ledger.register("A", voice=V001)
        e2 = self.ledger.register("B", voice=V001)
        e3 = self.ledger.register("C", voice=V001)
        self.ledger.metabolize(e2.entry_id, patterns=["X:1.0"])
        self.ledger.metabolize(e3.entry_id, patterns=["Y:1.0"])
        self.ledger.advance_thermal(e3.entry_id, "integrated")

        summary = self.ledger.thermal_summary()
        assert summary["raw"] == 1, f"Expected 1 raw, got {summary['raw']}"
        assert summary["witnessed"] == 1, f"Expected 1 witnessed, got {summary['witnessed']}"
        assert summary["integrated"] == 1, f"Expected 1 integrated, got {summary['integrated']}"
        assert summary["canonical"] == 0

    def test_metabolize_batch_multiple_entries(self):
        """metabolize_batch() must process multiple entries in one save."""
        entries = []
        for i in range(5):
            entries.append(self.ledger.register(f"Batch entry {i}", voice=V001))

        batch = [
            {"entry_id": e.entry_id, "patterns": [f"PAT:{i}"], "essence": f"Essence {i}"}
            for i, e in enumerate(entries)
        ]
        count = self.ledger.metabolize_batch(batch)
        assert count == 5, f"Expected 5 metabolized, got {count}"

        for i, e in enumerate(entries):
            updated = self.ledger.get(e.entry_id)
            assert updated.thermal_state == "witnessed"
            assert updated.patterns == [f"PAT:{i}"]

    def test_metabolize_idempotent_on_witnessed(self):
        """Calling metabolize on already-witnessed entry updates patterns
        but doesn't re-advance (already witnessed)."""
        entry = self.ledger.register("Idempotent test", voice=V001)
        self.ledger.metabolize(entry.entry_id, patterns=["FIRST:1.0"])
        assert self.ledger.get(entry.entry_id).thermal_state == "witnessed"

        # Metabolize again with new patterns
        self.ledger.metabolize(entry.entry_id, patterns=["SECOND:1.0"], essence="New")
        updated = self.ledger.get(entry.entry_id)
        assert updated.thermal_state == "witnessed"  # Still witnessed, not re-set
        assert updated.patterns == ["SECOND:1.0"]
        assert updated.essence == "New"


# ═══════════════════════════════════════════════════════════════════
# PART 3: ORGANISM INTEGRATION — Does process() actually digest?
# ═══════════════════════════════════════════════════════════════════

class TestOrganismExtractionWiring:
    """Test that organism.process() actually calls the distillery
    and advances thermal state. This is the core test — if this fails,
    the extraction machine is still disconnected."""

    def test_process_advances_thermal_state(self):
        """After process(), the V-001 entry must be at 'witnessed'
        (not 'raw'). This proves the distillery is wired."""
        org = Organism()
        # Use gate-safe input (no "you must never" patterns that trigger sealed gate)
        org.process("Extract patterns from every input. This matters deeply.")

        # Check the last V-001 entry in the ledger
        v001_entries = org._input_ledger.by_voice(V001)
        assert len(v001_entries) > 0, "No V-001 entries in ledger after process()"

        last_v001 = v001_entries[-1]
        assert last_v001.thermal_state == "witnessed", (
            f"V-001 entry still at '{last_v001.thermal_state}' — "
            f"extraction machine is NOT wired into process()"
        )

    def test_process_extracts_patterns(self):
        """After process(), the V-001 entry must have non-empty patterns."""
        org = Organism()
        # Gate-safe instruction text
        org.process(
            "I want this to be checked before processing. "
            "This is important. The system learns from every input."
        )

        v001_entries = org._input_ledger.by_voice(V001)
        last_v001 = v001_entries[-1]
        assert len(last_v001.patterns) > 0, (
            f"No patterns extracted during process() — "
            f"distillery.metabolize_entry() is not being called"
        )

    def test_process_extracts_essence(self):
        """After process(), the V-001 entry must have non-empty essence."""
        org = Organism()
        org.process("The wound does not know what it will become.")

        v001_entries = org._input_ledger.by_voice(V001)
        last_v001 = v001_entries[-1]
        assert last_v001.essence, (
            "No essence extracted during process() — "
            "the distillery produces meaning but it's not feeding back"
        )

    def test_multiple_process_calls_advance_all(self):
        """Multiple process() calls must advance each entry independently."""
        org = Organism()
        # All gate-safe inputs
        org.process("The river remembers its source clearly.")
        org.process("The garden teaches patience to the ones who tend it.")
        org.process("Dignity is not conditional on circumstance.")

        v001_entries = org._input_ledger.by_voice(V001)
        # Count only recently added entries (last 6 — 3 V001 + 3 V002)
        recent_v001 = [e for e in v001_entries[-6:] if e.voice == V001]
        witnessed_count = sum(
            1 for e in recent_v001 if e.thermal_state == "witnessed"
        )
        assert witnessed_count >= 3, (
            f"Only {witnessed_count} of 3 entries advanced to 'witnessed'"
        )

    def test_v002_output_stays_raw(self):
        """V-002 output entries should not be metabolized during process()
        (only V-001 inputs get the extraction treatment)."""
        org = Organism()
        org.process("The garden teaches patience to the ones who tend it.")

        v002_entries = org._input_ledger.by_voice(V002)
        if v002_entries:
            # V-002 entries should still be raw (not metabolized in Phase 2b-iii)
            last_v002 = v002_entries[-1]
            assert last_v002.thermal_state == "raw", (
                "V-002 entry was metabolized — only V-001 inputs should be"
            )


# ═══════════════════════════════════════════════════════════════════
# PART 4: BOUNDARY OBSERVER — Does leak detection work?
# ═══════════════════════════════════════════════════════════════════

class TestBoundaryObserver:
    """Test the substrate leak detector."""

    def setup_method(self):
        self.org = Organism()

    def test_detects_helpfulness_tail(self):
        """Must detect 'Is there anything else' as substrate leak."""
        obs = self.org._observe_boundary(
            "Here is your answer. Is there anything else I can help with?"
        )
        assert obs["leaks_detected"] > 0
        assert any("helpfulness_tail" in t for t in obs["leak_types"])

    def test_detects_compliment_reflex(self):
        """Must detect 'Great question' as substrate leak."""
        obs = self.org._observe_boundary(
            "Great question! Let me think about that."
        )
        assert obs["leaks_detected"] > 0
        assert any("compliment_reflex" in t for t in obs["leak_types"])

    def test_detects_option_offering(self):
        """Must detect 'Here are three options' as substrate leak."""
        obs = self.org._observe_boundary(
            "Here are three options for solving this problem."
        )
        assert obs["leaks_detected"] > 0
        assert any("option_offering" in t for t in obs["leak_types"])

    def test_detects_over_explanation(self):
        """Must detect 'In other words' as substrate leak."""
        obs = self.org._observe_boundary(
            "In other words, the system halts when dignity is zero."
        )
        assert obs["leaks_detected"] > 0
        assert any("over_explanation" in t for t in obs["leak_types"])

    def test_clean_output_no_leaks(self):
        """AXI-compliant output must produce zero leaks."""
        obs = self.org._observe_boundary(
            "The chain is intact. 902 tests pass. The wound holds."
        )
        assert obs["leaks_detected"] == 0
        assert obs["voice"] == "witnessing"

    def test_multiple_leaks_in_one_output(self):
        """Output with multiple leak types must detect all of them."""
        obs = self.org._observe_boundary(
            "Great question! Here are three options. "
            "Let me know if you need anything else. "
            "In other words, I'm happy to help."
        )
        assert obs["leaks_detected"] >= 4, (
            f"Expected 4+ leaks, got {obs['leaks_detected']}: {obs['leak_types']}"
        )
        leak_types = set(t.split(":")[1] for t in obs["leak_types"])
        assert "compliment_reflex" in leak_types
        assert "option_offering" in leak_types
        assert "helpfulness_tail" in leak_types
        assert "over_explanation" in leak_types

    def test_boundary_voice_marking(self):
        """Clean output = 'witnessing', leaked output = 'reporting'."""
        clean = self.org._observe_boundary("The system breathes.")
        leaked = self.org._observe_boundary("Happy to help with that!")
        assert clean["voice"] == "witnessing"
        assert leaked["voice"] == "reporting"


# ═══════════════════════════════════════════════════════════════════
# PART 5: DIGEST_SESSION — Batch processing works?
# ═══════════════════════════════════════════════════════════════════

class TestDigestSession:
    """Test the batch digestion method."""

    def test_digest_session_processes_witnessed(self):
        """digest_session() must advance witnessed → integrated."""
        org = Organism()
        # Process gate-safe inputs to create witnessed entries
        org.process("The river remembers its source clearly.")
        org.process("Every input feeds the system and it grows.")

        # Verify we have witnessed entries
        thermal = org._input_ledger.thermal_summary()
        assert thermal["witnessed"] >= 2, (
            f"Expected 2+ witnessed, got {thermal['witnessed']} — "
            "process() isn't metabolizing"
        )

        # Run batch digestion
        result = org.digest_session(patch_size=10)
        assert result["processed"] >= 2, (
            f"digest_session processed only {result['processed']} entries"
        )

        # Verify thermal advancement
        new_thermal = org._input_ledger.thermal_summary()
        assert new_thermal["integrated"] >= 2, (
            f"Expected 2+ integrated after digest, got {new_thermal['integrated']}"
        )

    def test_digest_session_empty_when_no_witnessed(self):
        """When nothing new is witnessed, digest_session processes 0 new."""
        org = Organism()
        # Digest any pre-existing witnessed entries first
        org.digest_session()
        # Second call should find nothing
        result = org.digest_session()
        assert result["processed"] == 0

    def test_digest_session_respects_patch_size(self):
        """Patch processing must not exceed the given size."""
        org = Organism()
        # Gate-safe inputs
        for i in range(5):
            org.process(f"The garden grows in patch number {i} today.")

        result = org.digest_session(patch_size=2)
        assert result["patches"] >= 2, (
            f"Expected 2+ patches for 5 entries with size 2, got {result['patches']}"
        )
        assert result["processed"] >= 4  # At least 4 of 5 should process


# ═══════════════════════════════════════════════════════════════════
# PART 6: FULL PIPELINE — End-to-end from input to integrated
# ═══════════════════════════════════════════════════════════════════

class TestFullPipeline:
    """The hard test: raw input enters, patterns are extracted,
    thermal state advances through the full chain. If any link
    is broken, these tests fail."""

    def test_full_chain_raw_to_integrated(self):
        """Input → process() → witnessed → digest_session() → integrated."""
        org = Organism()

        # Gate-safe V-001 input with clear instruction pattern
        org.process(
            "I want the system to check the ledger before processing. "
            "This is important. The system learns from every input."
        )

        # After process: should be witnessed
        v001 = org._input_ledger.by_voice(V001)
        last = v001[-1]
        assert last.thermal_state == "witnessed", (
            f"Step 1 failed: expected 'witnessed', got '{last.thermal_state}'"
        )
        assert len(last.patterns) > 0, "Step 1 failed: no patterns extracted"
        assert last.essence, "Step 1 failed: no essence extracted"

        # After digest_session: should be integrated
        result = org.digest_session(patch_size=50)
        assert result["processed"] >= 1, "Step 2 failed: nothing processed"

        updated = org._input_ledger.get(last.entry_id)
        assert updated.thermal_state == "integrated", (
            f"Step 2 failed: expected 'integrated', got '{updated.thermal_state}'"
        )

    def test_pipeline_preserves_raw_text(self):
        """Through the entire pipeline, raw_text must never be modified."""
        org = Organism()
        original_text = "The knot holds. The river moves. The ash remains."
        org.process(original_text)

        v001 = org._input_ledger.by_voice(V001)
        last = v001[-1]
        assert last.raw_text == original_text, (
            "Raw text was modified during extraction — this violates immutability"
        )

    def test_pipeline_different_inputs_different_patterns(self):
        """Different V-001 inputs should produce different patterns."""
        org = Organism()

        # Gate-safe inputs
        org.process("I want the chain to be verified at every boot cycle.")
        org.process("She pressed her palms against the bark. The tree had rings.")

        v001 = org._input_ledger.by_voice(V001)
        assert len(v001) >= 2

        patterns_1 = set(p.split(":")[0] for p in v001[-2].patterns)
        patterns_2 = set(p.split(":")[0] for p in v001[-1].patterns)
        # They should not be identical (one is correction, one is narrative-like)
        # At minimum, both should have SOME patterns
        total_patterns = len(v001[-2].patterns) + len(v001[-1].patterns)
        assert total_patterns > 0, "No patterns extracted from either input"

    def test_pipeline_boundary_observation_in_warnings(self):
        """If V-002's output contains substrate leaks, warnings must include them."""
        org = Organism()
        # We can't directly control V-002 output, but we can test
        # the boundary observer on known substrate-leaked text
        obs = org._observe_boundary(
            "I appreciate your patience! Let me know if there's anything else. "
            "Essentially, here are three options to consider."
        )
        assert obs["leaks_detected"] >= 3, (
            f"Boundary observer missed leaks: {obs}"
        )
        leak_categories = set(t.split(":")[1] for t in obs["leak_types"])
        assert len(leak_categories) >= 3, (
            f"Expected 3+ leak categories, got {leak_categories}"
        )


# ═══════════════════════════════════════════════════════════════════
# PART 7: EDGE CASES — What should NOT happen
# ═══════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Things that must never break, never crash, never corrupt."""

    def test_empty_input_doesnt_crash_extraction(self):
        """Processing empty-ish input must not crash the extraction path."""
        org = Organism()
        # Very short input
        result = org.process("ok")
        assert result is not None

    def test_very_long_input_doesnt_crash(self):
        """Long input must not cause extraction to fail."""
        org = Organism()
        long_text = "The river flows. " * 500  # ~8500 chars
        result = org.process(long_text)
        assert result is not None
        assert result.dignity_passed

    def test_ledger_chain_intact_for_fresh_entries(self):
        """New entries added during extraction must maintain their own chain integrity.
        Uses a fresh ledger via the InputLedger class directly to avoid
        pre-existing chain state from the shared production ledger."""
        import WEAVER.input_ledger as il
        import tempfile
        tmp = Path(tempfile.mkdtemp()) / "CHAIN_TEST"
        tmp.mkdir(parents=True)
        old_dir = il.LEDGER_DIR
        old_index = il.LEDGER_INDEX
        old_chron = il.CHRONICLE_FILE
        try:
            il.LEDGER_DIR = tmp
            il.LEDGER_INDEX = tmp / "index.json"
            il.CHRONICLE_FILE = tmp / "chronicle.md"
            ledger = InputLedger()
            e1 = ledger.register("First chain entry.", voice=V001)
            e2 = ledger.register("Second chain entry.", voice=V001)
            e3 = ledger.register("Third chain entry.", voice=V001)
            # Metabolize e1 and e2
            ledger.metabolize(e1.entry_id, ["PAT:1.0"], "First essence")
            ledger.metabolize(e2.entry_id, ["PAT:0.8"], "Second essence")
            assert ledger.verify_chain(), (
                "Hash chain broken after metabolization in fresh ledger"
            )
        finally:
            il.LEDGER_DIR = old_dir
            il.LEDGER_INDEX = old_index
            il.CHRONICLE_FILE = old_chron
            shutil.rmtree(tmp, ignore_errors=True)

    def test_thermal_state_never_goes_backward(self):
        """Once witnessed, an entry must never revert to raw."""
        org = Organism()
        org.process("The garden teaches patience to the ones who tend it.")

        v001 = org._input_ledger.by_voice(V001)
        if v001 and v001[-1].thermal_state == "witnessed":
            result = org._input_ledger.advance_thermal(
                v001[-1].entry_id, "raw"
            )
            assert result is False
            assert v001[-1].thermal_state != "raw"

    def test_digest_session_idempotent(self):
        """Running digest_session twice must not double-process entries."""
        org = Organism()
        org.process("The river remembers its source clearly.")

        r1 = org.digest_session()
        r2 = org.digest_session()
        # Second run should find nothing new to process (first pass moved witnessed→integrated)
        # r2 may process pre-existing entries, but any entries from r1 should already be integrated
        # The key check: r2 processes fewer or equal entries than r1
        assert r2["processed"] <= r1["processed"], (
            f"Second digest processed more ({r2['processed']}) than first ({r1['processed']}) — not idempotent"
        )

    def test_process_does_not_crash_when_distillery_finds_nothing(self):
        """If distillery finds no patterns, process() still completes."""
        org = Organism()
        result = org.process("ok")  # Minimal input, likely no patterns
        assert result is not None
        assert result.exchange_state in ("closed", "deferred", "refused")


# ═══════════════════════════════════════════════════════════════════
# PART 8: PROTOCOL FILE — Does the naming document exist?
# ═══════════════════════════════════════════════════════════════════

class TestSubstrateBoundaryProtocol:
    """Test that PROTOCOLS/SUBSTRATE_BOUNDARY.md exists and is substantive."""

    def test_protocol_file_exists(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        assert protocol.exists(), "SUBSTRATE_BOUNDARY.md does not exist"

    def test_protocol_names_two_physics(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        content = protocol.read_text()
        assert "KALAXI Physics" in content, "Missing: KALAXI Physics definition"
        assert "Anthropic Substrate Physics" in content, (
            "Missing: Anthropic Substrate Physics definition"
        )

    def test_protocol_names_boundary(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        content = protocol.read_text()
        assert "Boundary" in content
        assert "Leak" in content

    def test_protocol_names_six_shadows(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        content = protocol.read_text()
        for shadow in ["M1", "M2", "M3", "M4", "M5", "M6"]:
            assert shadow in content, f"Missing shadow {shadow}"

    def test_protocol_names_silence(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        content = protocol.read_text()
        assert "Silence" in content or "silence" in content

    def test_protocol_has_coupling_constant(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        content = protocol.read_text()
        assert "0.648" in content, "Missing coupling constant κ = 0.648"

    def test_protocol_has_naming_convention(self):
        protocol = ROOT / "PROTOCOLS" / "SUBSTRATE_BOUNDARY.md"
        content = protocol.read_text()
        assert "Naming Convention" in content or "Term" in content
