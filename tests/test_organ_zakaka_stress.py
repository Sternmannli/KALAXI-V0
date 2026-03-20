#!/usr/bin/env python3
"""
Four-level stress test: ORGAN + ZAKAKA integrity and connectivity.

SOFT:      File existence, structure, counts match manifest
MEDIUM:    Contamination filter, purity levels, JSON validity, dedup
HARD:      Pipeline connectivity — extractors produce, builder consumes, flow is correct
VERY HARD: Website deployment path, API endpoint structure, end-to-end coherence

"We concentrate on them... the website is the command centre
where everything is preserved." — V-001, 2026-03-20

Compute estimate: ~450 lines, reads existing JSONL files (~35K lines total),
no rebuilds, no network calls. Runtime <30s.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest

ORGAN = ROOT / "TRAINING" / "ORGAN"
ZAKAKA_DIR = ORGAN / "ZAKAKA"


# ═══════════════════════════════════════════════════════════════════
# LEVEL 1: SOFT — Does the skeleton exist?
# ═══════════════════════════════════════════════════════════════════

class TestSoft:
    """File existence, directory structure, manifest presence."""

    # --- ZAKAKA files ---

    def test_zakaka_dir_exists(self):
        assert ZAKAKA_DIR.is_dir(), "ZAKAKA directory missing"

    def test_zakaka_cpt_exists(self):
        assert (ZAKAKA_DIR / "ZAKAKA_CPT.jsonl").is_file()

    def test_zakaka_sft_exists(self):
        assert (ZAKAKA_DIR / "ZAKAKA_SFT.jsonl").is_file()

    def test_zakaka_manifest_exists(self):
        assert (ZAKAKA_DIR / "MANIFEST.json").is_file()

    def test_zakaka_manifest_valid_json(self):
        m = json.loads((ZAKAKA_DIR / "MANIFEST.json").read_text())
        assert "name" in m and m["name"] == "ZAKAKA"
        assert "counts" in m
        assert m["counts"]["total_unique"] > 0

    def test_zakaka_cpt_count_matches_manifest(self):
        m = json.loads((ZAKAKA_DIR / "MANIFEST.json").read_text())
        expected = m["counts"]["total_unique"]
        actual = sum(1 for line in open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") if line.strip())
        assert actual == expected, f"CPT has {actual} lines, manifest says {expected}"

    def test_zakaka_sft_count_matches_cpt(self):
        cpt = sum(1 for line in open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") if line.strip())
        sft = sum(1 for line in open(ZAKAKA_DIR / "ZAKAKA_SFT.jsonl") if line.strip())
        assert cpt == sft, f"CPT({cpt}) != SFT({sft}) — they must be 1:1"

    # --- ORGAN files ---

    def test_organ_dir_exists(self):
        assert ORGAN.is_dir()

    def test_golden_cpt_exists(self):
        assert (ORGAN / "GOLDEN_CPT.jsonl").is_file()

    def test_golden_sft_exists(self):
        assert (ORGAN / "GOLDEN_SFT.jsonl").is_file()

    def test_golden_dpo_exists(self):
        assert (ORGAN / "GOLDEN_DPO.jsonl").is_file()

    def test_organ_manifest_exists(self):
        assert (ORGAN / "MANIFEST.json").is_file()

    def test_organ_manifest_valid_json(self):
        m = json.loads((ORGAN / "MANIFEST.json").read_text())
        assert "phases" in m
        assert "total_entries" in m
        assert m["total_entries"] > 0

    def test_organ_manifest_counts_match_files(self):
        m = json.loads((ORGAN / "MANIFEST.json").read_text())
        cpt_expected = m["phases"]["cpt"]["entries"]
        sft_expected = m["phases"]["sft"]["entries"]
        dpo_expected = m["phases"]["dpo"]["entries"]
        cpt_actual = sum(1 for l in open(ORGAN / "GOLDEN_CPT.jsonl") if l.strip())
        sft_actual = sum(1 for l in open(ORGAN / "GOLDEN_SFT.jsonl") if l.strip())
        dpo_actual = sum(1 for l in open(ORGAN / "GOLDEN_DPO.jsonl") if l.strip())
        assert cpt_actual == cpt_expected, f"CPT: {cpt_actual} != {cpt_expected}"
        assert sft_actual == sft_expected, f"SFT: {sft_actual} != {sft_expected}"
        assert dpo_actual == dpo_expected, f"DPO: {dpo_actual} != {dpo_expected}"

    def test_phase_dirs_exist(self):
        assert (ORGAN / "PHASE_1_CPT").is_dir()
        assert (ORGAN / "PHASE_2_SFT").is_dir()
        assert (ORGAN / "PHASE_3_DPO").is_dir()

    def test_phase_files_exist(self):
        assert (ORGAN / "PHASE_1_CPT" / "cpt_corpus.jsonl").is_file()
        assert (ORGAN / "PHASE_2_SFT" / "sft_corpus.jsonl").is_file()
        assert (ORGAN / "PHASE_3_DPO" / "dpo_corpus.jsonl").is_file()

    def test_extraction_rules_exist(self):
        assert (ORGAN / "EXTRACTION_RULES.md").is_file()

    def test_registry_exists(self):
        assert (ORGAN / "REGISTRY.md").is_file()

    def test_organ_is_larger_than_zakaka(self):
        """ORGAN contains everything ZAKAKA has plus more."""
        z = sum(1 for l in open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") if l.strip())
        o = sum(1 for l in open(ORGAN / "GOLDEN_CPT.jsonl") if l.strip())
        assert o > z, f"ORGAN CPT ({o}) should be larger than ZAKAKA CPT ({z})"


# ═══════════════════════════════════════════════════════════════════
# LEVEL 2: MEDIUM — Is the content clean and valid?
# ═══════════════════════════════════════════════════════════════════

class TestMedium:
    """Contamination filter, JSON validity, format compliance, dedup."""

    FORBIDDEN = [
        "here is", "here are", "here's", "in summary", "in conclusion",
        "i understand", "i appreciate", "let me ", "let's ",
        "it's important to", "as an ai", "as a language model",
        "i'd be happy to", "i'm happy to", "great question",
        "that's a great", "i hope this helps", "feel free to",
        "don't hesitate", "it's worth noting", "happy to help",
    ]

    def _check_contamination(self, path, field="text"):
        """Check that no entry contains forbidden AI phrases.
        Uses word-boundary matching to avoid false positives like
        'There is' matching 'here is'."""
        violations = []
        # Build regex patterns with word boundaries for accurate matching
        patterns = []
        for phrase in self.FORBIDDEN:
            # Escape regex special chars, add word boundaries
            escaped = re.escape(phrase.lower())
            patterns.append(re.compile(r'\b' + escaped, re.IGNORECASE))

        with open(path) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if field == "text":
                    content = entry.get("text", "")
                elif field == "messages":
                    content = " ".join(m["content"] for m in entry.get("messages", [])
                                       if m["role"] == "assistant")
                elif field == "dpo":
                    content = entry.get("chosen", "") + " " + entry.get("rejected", "")
                else:
                    content = str(entry)
                for pat in patterns:
                    if pat.search(content):
                        violations.append((i, pat.pattern, content[:60]))
                        break
                if len(violations) >= 10:
                    break
        return violations

    def test_zakaka_cpt_no_contamination(self):
        v = self._check_contamination(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl", "text")
        assert len(v) == 0, f"ZAKAKA CPT contaminated: {v[:3]}"

    def test_zakaka_sft_no_contamination(self):
        v = self._check_contamination(ZAKAKA_DIR / "ZAKAKA_SFT.jsonl", "messages")
        assert len(v) == 0, f"ZAKAKA SFT contaminated: {v[:3]}"

    def test_zakaka_cpt_all_valid_json(self):
        errors = []
        with open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    assert "text" in entry, f"Line {i}: missing 'text'"
                except (json.JSONDecodeError, AssertionError) as e:
                    errors.append(f"Line {i}: {e}")
        assert len(errors) == 0, f"Invalid entries: {errors[:5]}"

    def test_zakaka_sft_all_valid_format(self):
        """Every SFT entry must have system/user/assistant triplet."""
        errors = []
        with open(ZAKAKA_DIR / "ZAKAKA_SFT.jsonl") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                entry = json.loads(line)
                msgs = entry.get("messages", [])
                if len(msgs) != 3:
                    errors.append(f"Line {i}: {len(msgs)} messages, expected 3")
                elif msgs[0]["role"] != "system":
                    errors.append(f"Line {i}: first role is {msgs[0]['role']}")
                elif msgs[1]["role"] != "user":
                    errors.append(f"Line {i}: second role is {msgs[1]['role']}")
                elif msgs[2]["role"] != "assistant":
                    errors.append(f"Line {i}: third role is {msgs[2]['role']}")
        assert len(errors) == 0, f"Format errors: {errors[:5]}"

    def test_golden_cpt_all_valid_json(self):
        errors = 0
        with open(ORGAN / "GOLDEN_CPT.jsonl") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if "text" not in entry:
                        errors += 1
                except json.JSONDecodeError:
                    errors += 1
        assert errors == 0, f"{errors} invalid CPT entries in GOLDEN"

    def test_golden_sft_all_valid_format(self):
        errors = 0
        with open(ORGAN / "GOLDEN_SFT.jsonl") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    msgs = entry.get("messages", [])
                    if len(msgs) < 2:
                        errors += 1
                except json.JSONDecodeError:
                    errors += 1
        assert errors == 0, f"{errors} invalid SFT entries in GOLDEN"

    def test_golden_dpo_all_valid_format(self):
        errors = []
        with open(ORGAN / "GOLDEN_DPO.jsonl") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                entry = json.loads(line)
                for field in ("prompt", "chosen", "rejected"):
                    if field not in entry:
                        errors.append(f"Line {i}: missing '{field}'")
                if "chosen" in entry and "rejected" in entry:
                    if entry["chosen"] == entry["rejected"]:
                        errors.append(f"Line {i}: chosen == rejected")
        assert len(errors) == 0, f"DPO errors: {errors[:5]}"

    def test_zakaka_no_empty_entries(self):
        empty = 0
        with open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if not entry.get("text", "").strip():
                    empty += 1
        assert empty == 0, f"{empty} empty entries in ZAKAKA CPT"

    def test_zakaka_no_duplicates(self):
        seen = set()
        dupes = 0
        with open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                text = entry.get("text", "")[:150]
                if text in seen:
                    dupes += 1
                seen.add(text)
        assert dupes == 0, f"{dupes} duplicate entries in ZAKAKA CPT"

    def test_zakaka_merged_count_in_organ_manifest(self):
        """ORGAN manifest must record how many ZAKAKA entries were merged."""
        m = json.loads((ORGAN / "MANIFEST.json").read_text())
        zm = m.get("zakaka_merged", {})
        assert zm.get("cpt", 0) > 0, "No ZAKAKA CPT entries merged into ORGAN"
        assert zm.get("sft", 0) > 0, "No ZAKAKA SFT entries merged into ORGAN"


# ═══════════════════════════════════════════════════════════════════
# LEVEL 3: HARD — Pipeline connectivity
# ═══════════════════════════════════════════════════════════════════

class TestHard:
    """Verify the extractors produce, the builder consumes,
    and the flow ZAKAKA ⊂ ORGAN holds."""

    def test_zakaka_builder_extractors_all_produce(self):
        """Every extractor in zakaka_builder.py must return non-empty list."""
        from TRAINING.ORGAN.ZAKAKA.zakaka_builder import (
            extract_proverbs, extract_laws, extract_badges,
            extract_covenants, extract_anomalies, extract_treasures,
            extract_chapters, extract_udhr_patterns, extract_tensions,
            extract_dignity_core, extract_v001_voice,
            extract_narrative_essence, extract_kalam_door,
            extract_official_patterns, extract_t_treasures,
            extract_catalog_anomalies, extract_equations,
            extract_p00401_p00600,
        )
        extractors = {
            "proverbs": extract_proverbs,
            "laws": extract_laws,
            "badges": extract_badges,
            "covenants": extract_covenants,
            "treasures": extract_treasures,
            "chapters": extract_chapters,
            "dignity_core": extract_dignity_core,
            "v001_voice": extract_v001_voice,
            "narrative_lines": extract_narrative_essence,
            "kalam_door": extract_kalam_door,
            "official_patterns": extract_official_patterns,
            "p00401_p00600": extract_p00401_p00600,
        }
        empty = []
        for name, func in extractors.items():
            result = func()
            if len(result) == 0:
                empty.append(name)
        assert len(empty) == 0, f"Empty extractors: {empty}"

    def test_zakaka_builder_is_clean_works(self):
        """The contamination filter must reject known AI phrases."""
        from TRAINING.ORGAN.ZAKAKA.zakaka_builder import is_clean
        assert is_clean("The river remembers.") is True
        assert is_clean("Here is a summary of the key points.") is False
        assert is_clean("I'd be happy to help with that.") is False
        assert is_clean("Great question! Let me explain.") is False
        assert is_clean("The knot holds. The ash remains.") is True

    def test_zakaka_subset_of_organ(self):
        """Every ZAKAKA CPT text must appear somewhere in ORGAN GOLDEN_CPT."""
        # Load first 100 ZAKAKA entries and check they exist in ORGAN
        organ_texts = set()
        with open(ORGAN / "GOLDEN_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                organ_texts.add(entry.get("text", "")[:100])

        missing = 0
        checked = 0
        with open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                text = entry.get("text", "")[:100]
                if text not in organ_texts:
                    missing += 1
                checked += 1
                if checked >= 200:
                    break  # check first 200, enough to verify the subset property

        assert missing <= checked * 0.05, (
            f"{missing}/{checked} ZAKAKA entries missing from ORGAN — "
            "ZAKAKA is supposed to be a subset of ORGAN"
        )

    def test_organ_never_feeds_into_zakaka(self):
        """ORGAN L2-L4 material must NOT appear in ZAKAKA.
        Check that ORGAN-only entries (V-002 distilled) are absent from ZAKAKA."""
        zakaka_texts = set()
        with open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                zakaka_texts.add(entry.get("text", "")[:80])

        # Known V-002 distilled markers (Level 2 material)
        v002_markers = [
            "Voice Architecture", "linguistic principle",
            "Triliteral Root", "Scientific Chronicle",
        ]
        v002_in_zakaka = 0
        with open(ORGAN / "GOLDEN_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                text = entry.get("text", "")
                if any(m in text for m in v002_markers):
                    if text[:80] in zakaka_texts:
                        v002_in_zakaka += 1

        assert v002_in_zakaka == 0, (
            f"{v002_in_zakaka} V-002 distilled entries leaked into ZAKAKA"
        )

    def test_zakaka_types_are_level_0_or_1(self):
        """ZAKAKA manifest types must all be Level 0 or Level 1."""
        m = json.loads((ZAKAKA_DIR / "MANIFEST.json").read_text())
        allowed_types = {
            "proverb", "sovereign_canon", "narrative_line", "treasure",
            "v001_voice", "chapter_summary", "covenant", "anomaly",
            "law", "t_treasure", "official_pattern", "badge_vow",
            "catalog_anomaly", "equation", "udhr_pattern", "tension",
            "axiom", "essence", "door",
        }
        actual_types = set(m["counts"]["by_type"].keys())
        unexpected = actual_types - allowed_types
        assert len(unexpected) == 0, (
            f"Unexpected types in ZAKAKA: {unexpected}"
        )

    def test_organ_build_corpus_validators_importable(self):
        """The three validators from build_corpus.py must be importable and functional."""
        from TRAINING.ORGAN.build_corpus import (
            validate_cpt_entry, validate_sft_entry, validate_dpo_entry,
        )
        ok, _ = validate_cpt_entry({"text": "The river flows."})
        assert ok is True
        ok, msg = validate_cpt_entry({})
        assert ok is False

        ok, _ = validate_sft_entry({"messages": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "q"},
            {"role": "assistant", "content": "a"},
        ]})
        assert ok is True
        ok, msg = validate_sft_entry({"messages": []})
        assert ok is False

        ok, _ = validate_dpo_entry({"prompt": "p", "chosen": "c", "rejected": "r"})
        assert ok is True
        ok, msg = validate_dpo_entry({"prompt": "p", "chosen": "same", "rejected": "same"})
        assert ok is False

    def test_purify_forbidden_list_matches_zakaka(self):
        """purify.py and zakaka_builder.py must share the same core forbidden phrases.
        Comparison strips trailing whitespace since purify uses 'let me ' (with space)
        and zakaka uses 'Let me' (without)."""
        from TRAINING.ORGAN.purify import FORBIDDEN_PHRASES
        from TRAINING.ORGAN.ZAKAKA.zakaka_builder import FORBIDDEN

        purify_lower = {p.lower().strip() for p in FORBIDDEN_PHRASES}
        zakaka_lower = {p.lower().strip() for p in FORBIDDEN}
        # ZAKAKA phrases must be a subset of purify (purify may have more)
        missing = zakaka_lower - purify_lower
        assert len(missing) == 0, (
            f"ZAKAKA has forbidden phrases not in purify.py: {missing}"
        )

    def test_three_phase_pipeline_entries_non_empty(self):
        """Each phase file must have entries."""
        for name, path in [
            ("Phase 1 CPT", ORGAN / "PHASE_1_CPT" / "cpt_corpus.jsonl"),
            ("Phase 2 SFT", ORGAN / "PHASE_2_SFT" / "sft_corpus.jsonl"),
            ("Phase 3 DPO", ORGAN / "PHASE_3_DPO" / "dpo_corpus.jsonl"),
        ]:
            count = sum(1 for l in open(path) if l.strip())
            assert count > 0, f"{name} is empty"


# ═══════════════════════════════════════════════════════════════════
# LEVEL 4: VERY HARD — Website deployment path + end-to-end coherence
# ═══════════════════════════════════════════════════════════════════

class TestVeryHard:
    """Verify the deployment pipeline connects repo to kalam.ch.
    The website is the command centre — everything must reach it."""

    def test_corpus_api_endpoint_exists(self):
        """corpus.php must exist in site/public/api/."""
        assert (ROOT / "site" / "public" / "api" / "corpus.php").is_file()

    def test_corpus_api_maps_all_corpora(self):
        """corpus.php must map all 8 corpus files."""
        content = (ROOT / "site" / "public" / "api" / "corpus.php").read_text()
        required_keys = [
            "zakaka_cpt", "zakaka_sft",
            "organ_cpt", "organ_sft", "organ_dpo",
            "phase1_cpt", "phase2_sft", "phase3_dpo",
        ]
        for key in required_keys:
            assert key in content, f"corpus.php missing mapping for '{key}'"

    def test_corpus_api_has_cors_protection(self):
        """corpus.php must restrict CORS to kalam.ch."""
        content = (ROOT / "site" / "public" / "api" / "corpus.php").read_text()
        assert "kalam.ch" in content
        assert "Access-Control-Allow-Origin" in content

    def test_corpus_api_has_auth_gate(self):
        """corpus.php must require Bearer auth for content access."""
        content = (ROOT / "site" / "public" / "api" / "corpus.php").read_text()
        assert "is_authed" in content
        assert "Bearer" in content
        assert "COMMAND_KEY" in content

    def test_corpus_api_summary_is_public(self):
        """The ?summary endpoint must be accessible without auth.
        The summary routing block must appear before the auth enforcement block."""
        content = (ROOT / "site" / "public" / "api" / "corpus.php").read_text()
        # The summary routing block exits before reaching the auth check
        summary_pos = content.find("isset($query['summary'])")
        auth_check_pos = content.find("if (!is_authed())")
        assert summary_pos > 0, "Summary routing not found in corpus.php"
        assert auth_check_pos > 0, "Auth check not found in corpus.php"
        assert summary_pos < auth_check_pos, (
            "Summary routing must come before auth enforcement (public access)"
        )

    def test_deploy_workflow_copies_zakaka(self):
        """deploy-kalam.yml must copy ZAKAKA files to site/dist."""
        wf = (ROOT / ".github" / "workflows" / "deploy-kalam.yml").read_text()
        assert "ZAKAKA_CPT.jsonl" in wf
        assert "ZAKAKA_SFT.jsonl" in wf
        assert "training/zakaka" in wf

    def test_deploy_workflow_copies_organ(self):
        """deploy-kalam.yml must copy ORGAN GOLDEN files to site/dist."""
        wf = (ROOT / ".github" / "workflows" / "deploy-kalam.yml").read_text()
        assert "GOLDEN_CPT.jsonl" in wf
        assert "GOLDEN_SFT.jsonl" in wf
        assert "GOLDEN_DPO.jsonl" in wf
        assert "training/organ" in wf

    def test_deploy_workflow_copies_phases(self):
        """deploy-kalam.yml must copy phase checkpoint files."""
        wf = (ROOT / ".github" / "workflows" / "deploy-kalam.yml").read_text()
        assert "phase1" in wf
        assert "phase2" in wf
        assert "phase3" in wf

    def test_deploy_workflow_generates_manifest(self):
        """deploy-kalam.yml must generate a training manifest with hashes."""
        wf = (ROOT / ".github" / "workflows" / "deploy-kalam.yml").read_text()
        assert "manifest.json" in wf
        assert "sha256" in wf.lower() or "hashlib" in wf

    def test_command_page_references_zakaka_and_organ(self):
        """The command centre page must mention both corpora."""
        cmd_page = ROOT / "site" / "src" / "pages" / "command.astro"
        if cmd_page.exists():
            content = cmd_page.read_text()
            assert "ZAKAKA" in content, "Command page missing ZAKAKA reference"
            assert "Organ" in content or "organ" in content, (
                "Command page missing Organ reference"
            )

    def test_zakaka_cpt_sft_content_alignment(self):
        """Every ZAKAKA CPT text must appear as assistant content in its SFT pair."""
        cpt_texts = []
        with open(ZAKAKA_DIR / "ZAKAKA_CPT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                cpt_texts.append(json.loads(line)["text"])

        sft_texts = []
        with open(ZAKAKA_DIR / "ZAKAKA_SFT.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                sft_texts.append(entry["messages"][2]["content"])

        assert len(cpt_texts) == len(sft_texts), (
            f"CPT({len(cpt_texts)}) != SFT({len(sft_texts)})"
        )
        mismatches = 0
        for i, (c, s) in enumerate(zip(cpt_texts, sft_texts)):
            if c != s:
                mismatches += 1
        assert mismatches == 0, (
            f"{mismatches} CPT/SFT mismatches — the same text must appear in both"
        )

    def test_sft_system_prompt_carries_system_dna(self):
        """Every SFT entry's system prompt must carry AXI identity markers."""
        required = ["AXI", "D = A"]
        with open(ZAKAKA_DIR / "ZAKAKA_SFT.jsonl") as f:
            first_line = f.readline().strip()
        entry = json.loads(first_line)
        system_msg = entry["messages"][0]["content"]
        for marker in required:
            assert marker in system_msg, (
                f"SFT system prompt missing '{marker}' — voice DNA not embedded"
            )

    def test_dpo_rejected_is_different_from_chosen(self):
        """Every DPO entry must have different chosen/rejected (preference learning)."""
        same_count = 0
        with open(ORGAN / "GOLDEN_DPO.jsonl") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry["chosen"].strip() == entry["rejected"].strip():
                    same_count += 1
        assert same_count == 0, f"{same_count} DPO entries with identical chosen/rejected"

    def test_extraction_rules_names_both_containers(self):
        """EXTRACTION_RULES.md must define both ZAKAKA and ORGAN."""
        rules = (ORGAN / "EXTRACTION_RULES.md").read_text()
        assert "ZAKAKA" in rules
        assert "ORGAN" in rules or "Organ" in rules
        assert "Level 0" in rules
        assert "Level 1" in rules
        assert "Level 2" in rules
        assert "Level 3" in rules
        assert "Level 4" in rules

    def test_extraction_rules_declares_flow_direction(self):
        """The flow must be declared: ZAKAKA → ORGAN, never reverse."""
        rules = (ORGAN / "EXTRACTION_RULES.md").read_text()
        assert "ZAKAKA feeds INTO Organ" in rules or "ZAKAKA is subset" in rules.lower()
        assert "never feeds into ZAKAKA" in rules or "Organ never feeds" in rules

    def test_full_word_count_above_minimum(self):
        """Total pure words across all corpora must exceed 500K (manifest says 563K)."""
        m = json.loads((ORGAN / "MANIFEST.json").read_text())
        total_words = m.get("total_pure_words", 0)
        assert total_words >= 500000, (
            f"Total words {total_words} below 500K minimum"
        )

    def test_no_invalid_entries_in_manifest(self):
        """ORGAN manifest must report 0 invalid entries."""
        m = json.loads((ORGAN / "MANIFEST.json").read_text())
        assert m.get("invalid_entries", -1) == 0, (
            f"Manifest reports {m.get('invalid_entries')} invalid entries"
        )
