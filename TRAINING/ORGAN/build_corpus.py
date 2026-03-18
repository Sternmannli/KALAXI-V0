#!/usr/bin/env python3
"""
TRAINING ORGAN — Corpus Builder
Merges all phase data, validates, reports.
Produces the final GOLDEN_CORPUS files ready for Together.ai upload.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent
ORGAN = ROOT / "TRAINING" / "ORGAN"
PHASE_1 = ORGAN / "PHASE_1_CPT"
PHASE_2 = ORGAN / "PHASE_2_SFT"
PHASE_3 = ORGAN / "PHASE_3_DPO"


def validate_cpt_entry(entry: dict) -> tuple[bool, str]:
    """Validate a CPT entry."""
    if "text" not in entry:
        return False, "missing 'text' field"
    if not entry["text"].strip():
        return False, "empty text"
    if len(entry["text"]) < 5:
        return False, f"text too short ({len(entry['text'])} chars)"
    return True, ""


def validate_sft_entry(entry: dict) -> tuple[bool, str]:
    """Validate an SFT entry."""
    if "messages" not in entry:
        return False, "missing 'messages' field"
    msgs = entry["messages"]
    if len(msgs) != 3:
        return False, f"expected 3 messages, got {len(msgs)}"
    if msgs[0]["role"] != "system":
        return False, "first message must be system"
    if msgs[1]["role"] != "user":
        return False, "second message must be user"
    if msgs[2]["role"] != "assistant":
        return False, "third message must be assistant"
    if not msgs[2]["content"].strip():
        return False, "empty assistant response"
    return True, ""


def validate_dpo_entry(entry: dict) -> tuple[bool, str]:
    """Validate a DPO entry."""
    for field in ("prompt", "chosen", "rejected"):
        if field not in entry:
            return False, f"missing '{field}' field"
        if not entry[field].strip():
            return False, f"empty '{field}'"
    if entry["chosen"] == entry["rejected"]:
        return False, "chosen and rejected are identical"
    return True, ""


def load_and_validate(filepath: Path, validator) -> tuple[list, int, list]:
    """Load JSONL file, validate each entry, return (valid, invalid_count, errors)."""
    valid = []
    errors = []
    invalid = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: JSON parse error: {e}")
                invalid += 1
                continue

            ok, msg = validator(entry)
            if ok:
                valid.append(entry)
            else:
                errors.append(f"Line {i}: {msg}")
                invalid += 1

    return valid, invalid, errors


def build():
    """Build and validate the complete corpus."""
    print("=" * 60)
    print("TRAINING ORGAN — CORPUS BUILDER")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # ─── Phase 1: CPT ────────────────────────────────────────────────────
    print("\n--- Phase 1: CPT Validation ---")
    cpt_file = PHASE_1 / "cpt_corpus.jsonl"
    cpt_valid, cpt_invalid, cpt_errors = load_and_validate(cpt_file, validate_cpt_entry)
    print(f"  Valid: {len(cpt_valid)}, Invalid: {cpt_invalid}")
    for err in cpt_errors[:5]:
        print(f"  ERROR: {err}")

    # ─── Phase 2: SFT ────────────────────────────────────────────────────
    print("\n--- Phase 2: SFT Validation ---")
    sft_file = PHASE_2 / "sft_corpus.jsonl"
    sft_valid, sft_invalid, sft_errors = load_and_validate(sft_file, validate_sft_entry)
    print(f"  Valid: {len(sft_valid)}, Invalid: {sft_invalid}")
    for err in sft_errors[:5]:
        print(f"  ERROR: {err}")

    # ─── Phase 3: DPO ────────────────────────────────────────────────────
    print("\n--- Phase 3: DPO Validation ---")
    dpo_file = PHASE_3 / "dpo_corpus.jsonl"
    dpo_valid, dpo_invalid, dpo_errors = load_and_validate(dpo_file, validate_dpo_entry)
    print(f"  Valid: {len(dpo_valid)}, Invalid: {dpo_invalid}")
    for err in dpo_errors[:5]:
        print(f"  ERROR: {err}")

    # ─── Write final outputs ─────────────────────────────────────────────
    print("\n--- Writing Final Corpus Files ---")

    # Phase 1: CPT corpus (for continued pre-training)
    final_cpt = ORGAN / "GOLDEN_CPT.jsonl"
    with open(final_cpt, "w", encoding="utf-8") as f:
        for entry in cpt_valid:
            f.write(json.dumps({"text": entry["text"]}, ensure_ascii=False) + "\n")
    print(f"  GOLDEN_CPT.jsonl: {len(cpt_valid)} entries")

    # Phase 2: SFT corpus (for instruction fine-tuning)
    final_sft = ORGAN / "GOLDEN_SFT.jsonl"
    with open(final_sft, "w", encoding="utf-8") as f:
        for entry in sft_valid:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  GOLDEN_SFT.jsonl: {len(sft_valid)} entries")

    # Phase 3: DPO corpus (for preference optimization)
    final_dpo = ORGAN / "GOLDEN_DPO.jsonl"
    with open(final_dpo, "w", encoding="utf-8") as f:
        for entry in dpo_valid:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  GOLDEN_DPO.jsonl: {len(dpo_valid)} entries")

    # ─── Statistics ──────────────────────────────────────────────────────
    total = len(cpt_valid) + len(sft_valid) + len(dpo_valid)
    total_invalid = cpt_invalid + sft_invalid + dpo_invalid

    # Word counts
    cpt_words = sum(len(e["text"].split()) for e in cpt_valid)
    sft_words = sum(len(e["messages"][2]["content"].split()) for e in sft_valid)
    dpo_chosen_words = sum(len(e["chosen"].split()) for e in dpo_valid)
    dpo_rejected_words = sum(len(e["rejected"].split()) for e in dpo_valid)

    # File sizes
    cpt_size = final_cpt.stat().st_size
    sft_size = final_sft.stat().st_size
    dpo_size = final_dpo.stat().st_size

    print("\n" + "=" * 60)
    print("CORPUS BUILD COMPLETE")
    print("=" * 60)
    print(f"\n  Phase 1 (CPT):  {len(cpt_valid):>5} entries | {cpt_words:>6} words | {cpt_size:>8} bytes")
    print(f"  Phase 2 (SFT):  {len(sft_valid):>5} entries | {sft_words:>6} words | {sft_size:>8} bytes")
    print(f"  Phase 3 (DPO):  {len(dpo_valid):>5} entries | {dpo_chosen_words:>6} chosen words | {dpo_size:>8} bytes")
    print(f"                                    {dpo_rejected_words:>6} rejected words")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  TOTAL:          {total:>5} entries | {cpt_words + sft_words + dpo_chosen_words:>6} words (pure)")
    print(f"  Invalid:        {total_invalid:>5}")
    print(f"\n  Files:")
    print(f"    {final_cpt.relative_to(ROOT)}")
    print(f"    {final_sft.relative_to(ROOT)}")
    print(f"    {final_dpo.relative_to(ROOT)}")

    # ─── Manifest ────────────────────────────────────────────────────────
    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "pipeline": "CPT → SFT → DPO (three-phase)",
        "phases": {
            "cpt": {"entries": len(cpt_valid), "words": cpt_words, "bytes": cpt_size},
            "sft": {"entries": len(sft_valid), "words": sft_words, "bytes": sft_size},
            "dpo": {"entries": len(dpo_valid), "chosen_words": dpo_chosen_words, "rejected_words": dpo_rejected_words, "bytes": dpo_size},
        },
        "total_entries": total,
        "total_pure_words": cpt_words + sft_words + dpo_chosen_words,
        "invalid_entries": total_invalid,
        "contamination_threshold": 0.25,
        "files": [
            str(final_cpt.relative_to(ROOT)),
            str(final_sft.relative_to(ROOT)),
            str(final_dpo.relative_to(ROOT)),
        ],
    }
    (ORGAN / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n  Manifest: TRAINING/ORGAN/MANIFEST.json")
    print("=" * 60)


if __name__ == "__main__":
    build()
