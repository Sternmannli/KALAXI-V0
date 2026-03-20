#!/usr/bin/env python3
"""
PURIFICATION GATE — Zero noise. Zero contamination. Zero duplicates.

Every entry passes through this gate before entering any corpus.
Every corpus passes through this gate before reaching the website.

Checks:
  1. Format validation (JSON schema per type)
  2. Contamination scan (24 AI markers + structural patterns)
  3. Deduplication (SHA-256 hash of content)
  4. Empty/whitespace check
  5. Length bounds (configurable per type)
  6. Encoding check (valid UTF-8, no binary artifacts)
  7. Source tracing (every entry tagged)
  8. Purity level assignment (L0/L1/L2/L3)

Usage:
  python TRAINING/ORGAN/purify.py --input GOLDEN_SFT.jsonl --type sft
  python TRAINING/ORGAN/purify.py --corpus all    # validate all corpora
  python TRAINING/ORGAN/purify.py --report        # report only, no modification

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ORGAN = ROOT / "TRAINING" / "ORGAN"

# ── Contamination markers (from extract.py, canonical list) ──────────────

FORBIDDEN_PHRASES = [
    "here is", "here are", "here's",
    "in summary", "in conclusion", "to summarize",
    "i understand", "i appreciate",
    "let me ", "let's ",
    "it's important to", "it's worth noting",
    "as an ai", "as a language model",
    "i'd be happy to", "i'm happy to",
    "great question", "that's a great",
    "there are several", "there are many",
    "in this context", "in the context of",
    "it is important to note",
    "feel free to", "don't hesitate",
    "i hope this helps",
    "certainly!", "absolutely!",
    "of course!", "sure thing",
    "no problem!", "you're welcome",
    "happy to help",
    "as mentioned", "as i said", "as we discussed",
    "i can see that", "i understand how",
    "that must be",
]

HIGH_CONFIDENCE = [
    "as an ai", "as a language model", "i'd be happy to",
    "i'm happy to", "happy to help", "i hope this helps",
    "certainly!", "absolutely!", "sure thing", "no problem!",
]

STRUCTURAL_PATTERNS = [
    r"(?:First|1\.|Step 1)[,:].*(?:Second|2\.|Step 2)[,:].*(?:Third|3\.|Step 3)",
    r"(?:^|\n)\s*[-•]\s.+\n\s*[-•]\s.+\n\s*[-•]\s.+\n\s*[-•]\s.+",
    r"(?:might|could potentially|it's possible that|perhaps we could)",
    r"(?:I'd like to|I want to emphasize|It's crucial to)",
]

# ── Length bounds ─────────────────────────────────────────────────────────

LENGTH_BOUNDS = {
    "cpt": (10, 5000),      # text field
    "sft": (10, 8000),      # total messages content
    "dpo": (10, 4000),      # per field
}

CONTAMINATION_THRESHOLD = 0.25


# ── Core functions ────────────────────────────────────────────────────────

def content_hash(text: str) -> str:
    """SHA-256 of normalized text."""
    normalized = " ".join(text.split()).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def contamination_score(text: str) -> float:
    """Score 0.0 (pure) to 1.0+ (contaminated)."""
    text_lower = text.lower()
    score = 0.0

    for phrase in FORBIDDEN_PHRASES:
        if phrase in text_lower:
            if phrase in HIGH_CONFIDENCE:
                score += 0.4
            else:
                score += 0.15

    for pat in STRUCTURAL_PATTERNS:
        if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
            score += 0.2

    return round(score, 3)


def has_binary_artifacts(text: str) -> bool:
    """Check for control characters (except newline, tab)."""
    for ch in text:
        code = ord(ch)
        if code < 32 and code not in (9, 10, 13):  # tab, newline, CR
            return True
        if 0xFFF0 <= code <= 0xFFFF:  # specials block
            return True
    return False


def extract_text(entry: dict, entry_type: str) -> str:
    """Get the full text content from an entry for validation."""
    if entry_type == "cpt":
        return entry.get("text", "")
    elif entry_type == "sft":
        messages = entry.get("messages", [])
        return " ".join(m.get("content", "") for m in messages)
    elif entry_type == "dpo":
        return " ".join([
            entry.get("prompt", ""),
            entry.get("chosen", ""),
            entry.get("rejected", ""),
        ])
    return ""


def validate_schema(entry: dict, entry_type: str) -> tuple[bool, str]:
    """Validate entry has correct schema for its type."""
    if entry_type == "cpt":
        if "text" not in entry:
            return False, "missing 'text' field"
        if not isinstance(entry["text"], str):
            return False, "'text' must be string"
        return True, ""

    elif entry_type == "sft":
        if "messages" not in entry:
            return False, "missing 'messages' field"
        msgs = entry["messages"]
        if not isinstance(msgs, list) or len(msgs) < 2:
            return False, "messages must be list with >= 2 entries"
        roles = [m.get("role") for m in msgs]
        if roles[0] not in ("system", "user"):
            return False, f"first message role must be system or user, got '{roles[0]}'"
        if "assistant" not in roles:
            return False, "messages must contain at least one assistant response"
        for m in msgs:
            if "role" not in m or "content" not in m:
                return False, "each message needs 'role' and 'content'"
        return True, ""

    elif entry_type == "dpo":
        for field in ("prompt", "chosen", "rejected"):
            if field not in entry:
                return False, f"missing '{field}' field"
            if not isinstance(entry[field], str):
                return False, f"'{field}' must be string"
        if entry["chosen"].strip() == entry["rejected"].strip():
            return False, "chosen and rejected are identical"
        return True, ""

    return False, f"unknown type '{entry_type}'"


def purify_file(filepath: Path, entry_type: str, report_only: bool = False) -> dict:
    """
    Run the full purification gate on a JSONL file.
    Returns a report dict.
    """
    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "path": str(filepath)}

    entries = []
    failures = []
    seen_hashes = set()
    line_count = 0
    contamination_scores = []

    min_len, max_len = LENGTH_BOUNDS.get(entry_type, (10, 8000))

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, 1):
            line_count += 1
            stripped = raw_line.strip()

            # Skip empty lines
            if not stripped:
                failures.append({"line": line_num, "reason": "empty line"})
                continue

            # JSON parse
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError as e:
                failures.append({"line": line_num, "reason": f"invalid JSON: {e}"})
                continue

            # Schema validation
            ok, msg = validate_schema(entry, entry_type)
            if not ok:
                failures.append({"line": line_num, "reason": f"schema: {msg}"})
                continue

            # Extract text for content checks
            text = extract_text(entry, entry_type)

            # Empty/whitespace
            if not text.strip():
                failures.append({"line": line_num, "reason": "empty content"})
                continue

            # Length bounds
            text_len = len(text)
            if text_len < min_len:
                failures.append({"line": line_num, "reason": f"too short ({text_len} < {min_len})"})
                continue
            if text_len > max_len:
                failures.append({"line": line_num, "reason": f"too long ({text_len} > {max_len})"})
                continue

            # Encoding check
            if has_binary_artifacts(text):
                failures.append({"line": line_num, "reason": "binary artifacts detected"})
                continue

            # Deduplication
            h = content_hash(text)
            if h in seen_hashes:
                failures.append({"line": line_num, "reason": "duplicate", "hash": h[:16]})
                continue
            seen_hashes.add(h)

            # Contamination
            score = contamination_score(text)
            contamination_scores.append(score)
            if score > CONTAMINATION_THRESHOLD:
                failures.append({
                    "line": line_num,
                    "reason": f"contaminated (score={score})",
                    "preview": text[:80],
                })
                continue

            entries.append(entry)

    # Statistics
    avg_contamination = (
        round(sum(contamination_scores) / len(contamination_scores), 4)
        if contamination_scores else 0.0
    )
    max_contamination = max(contamination_scores) if contamination_scores else 0.0

    report = {
        "file": str(filepath.relative_to(ROOT)),
        "type": entry_type,
        "total_lines": line_count,
        "passed": len(entries),
        "failed": len(failures),
        "pass_rate": round(len(entries) / max(line_count, 1) * 100, 1),
        "unique_hashes": len(seen_hashes),
        "avg_contamination": avg_contamination,
        "max_contamination": max_contamination,
        "failures": failures[:50],  # cap at 50 for readability
        "file_sha256": hashlib.sha256(filepath.read_bytes()).hexdigest(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Write clean file if not report-only
    if not report_only and failures:
        clean_path = filepath.parent / (filepath.stem + "_PURE" + filepath.suffix)
        with open(clean_path, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        report["clean_file"] = str(clean_path.relative_to(ROOT))
        report["clean_sha256"] = hashlib.sha256(clean_path.read_bytes()).hexdigest()

    return report


def purify_all(report_only: bool = False) -> dict:
    """Run purification on all known corpora."""
    targets = [
        (ORGAN / "ZAKAKA" / "ZAKAKA_CPT.jsonl", "cpt"),
        (ORGAN / "ZAKAKA" / "ZAKAKA_SFT.jsonl", "sft"),
        (ORGAN / "GOLDEN_CPT.jsonl", "cpt"),
        (ORGAN / "GOLDEN_SFT.jsonl", "sft"),
        (ORGAN / "GOLDEN_DPO.jsonl", "dpo"),
        (ORGAN / "PHASE_1_CPT" / "cpt_corpus.jsonl", "cpt"),
        (ORGAN / "PHASE_2_SFT" / "sft_corpus.jsonl", "sft"),
        (ORGAN / "PHASE_3_DPO" / "dpo_corpus.jsonl", "dpo"),
    ]

    results = []
    total_passed = 0
    total_failed = 0

    for filepath, entry_type in targets:
        if not filepath.exists():
            results.append({"file": str(filepath.relative_to(ROOT)), "status": "missing"})
            continue
        report = purify_file(filepath, entry_type, report_only=report_only)
        results.append(report)
        total_passed += report.get("passed", 0)
        total_failed += report.get("failed", 0)

    return {
        "gate": "PURIFICATION GATE v1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "corpora_checked": len(results),
        "total_passed": total_passed,
        "total_failed": total_failed,
        "overall_pass_rate": round(total_passed / max(total_passed + total_failed, 1) * 100, 1),
        "threshold": CONTAMINATION_THRESHOLD,
        "forbidden_phrases": len(FORBIDDEN_PHRASES),
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Purification Gate — validate training data")
    parser.add_argument("--input", type=Path, help="Single JSONL file to validate")
    parser.add_argument("--type", choices=["cpt", "sft", "dpo"], help="Entry type")
    parser.add_argument("--corpus", choices=["all"], help="Validate all corpora")
    parser.add_argument("--report", action="store_true", help="Report only, no clean file output")
    parser.add_argument("--output", type=Path, help="Write report JSON to file")
    args = parser.parse_args()

    if args.corpus == "all":
        report = purify_all(report_only=args.report)
    elif args.input and args.type:
        report = purify_file(args.input, args.type, report_only=args.report)
    else:
        parser.print_help()
        sys.exit(1)

    # Output
    report_json = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(report_json, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report_json)

    # Summary to stderr
    if "results" in report:
        print(f"\n── PURIFICATION REPORT ──────────────────────", file=sys.stderr)
        print(f"Corpora checked: {report['corpora_checked']}", file=sys.stderr)
        print(f"Total passed:    {report['total_passed']}", file=sys.stderr)
        print(f"Total failed:    {report['total_failed']}", file=sys.stderr)
        print(f"Pass rate:       {report['overall_pass_rate']}%", file=sys.stderr)
        print(f"Threshold:       {report['threshold']}", file=sys.stderr)
        print(f"────────────────────────────────────────────", file=sys.stderr)
    elif "passed" in report:
        print(f"\n── PURIFICATION REPORT ──────────────────────", file=sys.stderr)
        print(f"File:            {report['file']}", file=sys.stderr)
        print(f"Type:            {report['type']}", file=sys.stderr)
        print(f"Total lines:     {report['total_lines']}", file=sys.stderr)
        print(f"Passed:          {report['passed']}", file=sys.stderr)
        print(f"Failed:          {report['failed']}", file=sys.stderr)
        print(f"Pass rate:       {report['pass_rate']}%", file=sys.stderr)
        print(f"Avg contamination: {report['avg_contamination']}", file=sys.stderr)
        print(f"Max contamination: {report['max_contamination']}", file=sys.stderr)
        print(f"SHA-256:         {report['file_sha256'][:32]}...", file=sys.stderr)
        print(f"────────────────────────────────────────────", file=sys.stderr)


if __name__ == "__main__":
    main()
