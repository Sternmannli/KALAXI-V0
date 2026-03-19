#!/usr/bin/env python3
"""
voice_lint.py — AXI Voice Linter (Standalone CI Tool)

Enforces AXI voice rules on any text. Run in CI, post-generation,
or as pre-publication check. Returns exit code 0 (pass) or 1 (fail).

Usage:
    python TOOLS/voice_lint.py "Rest is part of repeat. Lay the hand down."
    python TOOLS/voice_lint.py --file site/public/api/axi.php
    python TOOLS/voice_lint.py --json "The knot holds what speech cannot."

Voice rules enforced (from site/AXI_VOICE_CANON.md):
    1. Sentence shape: 4-20 words per sentence (target 8-14)
    2. Somatic anchor: >=1 concrete noun from canonical set
    3. No helpfulness leak: no assistant persona phrases
    4. Brevity: max 8 sentences (default max, expansion allowed)
    5. Halt string: exact match bypasses all other checks
    6. Silence: empty response is valid

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
import sys

# ── CANONICAL VOCABULARY ──

SOMATIC_ANCHORS = {
    # Body (from AXI_VOICE_CANON.md: hands, breath, bones, grip, wrists, shoulders, chest)
    "hands", "hand", "breath", "bones", "bone", "skin", "chest", "fist",
    "palm", "lungs", "spine", "blood", "muscle", "grip", "wrists",
    "shoulders", "body", "weight", "carry",
    # Material (from AXI_VOICE_CANON.md: rope, stone, ash, water, clay, salt, fire, knot, river, door)
    "rope", "stone", "ash", "water", "river", "fire", "salt", "soil",
    "wood", "iron", "clay", "sand", "thread", "knot", "weir", "wall",
    "bread", "door", "path", "root", "seed",
    # Gap/presence words
    "silence", "pause", "gap", "hold", "still", "quiet",
}

HELPFULNESS_LEAK = {
    "i can help", "i understand", "i hear you", "let me explain",
    "here are some", "hope this helps", "feel free to",
    "don't worry", "is there anything else", "how can i help",
    "i'm here to", "happy to help", "great question",
    "that's a great", "that's an interesting", "that's a wonderful",
    "no problem", "of course!", "absolutely!",
    "i'd be happy to", "here are three", "here are some options",
}

HALT_STRING = (
    "The gate refuses. Not because dignity is fragile — "
    "because the system will not pretend you do not count."
)

HALT_PATTERNS = [
    "the gate refuses",
    "the system has stopped",
    "this cannot proceed",
    "you are not refused. the action is refused",
]


# ── LINT ENGINE ──

def lint(text: str, strict: bool = False) -> tuple:
    """
    Lint a single AXI utterance.

    Returns (passed: bool, reason: str, details: dict).
    strict=True uses tighter sentence bounds (7-15 instead of 4-20).
    """
    t = text.strip()
    details = {"somatic_found": [], "violations": [], "sentence_lengths": []}

    # Empty = valid silence
    if not t:
        return True, "Valid silence", details

    # Halt string = always valid
    t_lower = t.lower()
    if any(hp in t_lower for hp in HALT_PATTERNS):
        return True, "Valid halt", details

    # Split sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', t) if s.strip()]

    # Check 1: Sentence count (max 8 for expansion, default 4 for strict)
    max_sentences = 4 if strict else 8
    if len(sentences) > max_sentences:
        details["violations"].append(f"too_many_sentences:{len(sentences)}")
        return False, f"Too many sentences: {len(sentences)} (max {max_sentences})", details

    # Check 2: Sentence shape (word count per sentence)
    min_words = 7 if strict else 4
    max_words = 15 if strict else 20
    for i, s in enumerate(sentences):
        wc = len(re.findall(r'\b\w+\b', s))
        details["sentence_lengths"].append(wc)
        if wc > 0 and (wc < min_words or wc > max_words):
            details["violations"].append(f"sentence_shape:{i+1}:{wc}")
            return False, f"Sentence {i+1} has {wc} words (bounds: {min_words}-{max_words})", details

    # Check 3: Somatic anchor
    words_set = set(re.findall(r'\b\w+\b', t_lower))
    found_somatic = SOMATIC_ANCHORS & words_set
    details["somatic_found"] = list(found_somatic)
    if not found_somatic:
        details["violations"].append("no_somatic_anchor")
        return False, "No somatic anchor (need stone, hand, breath, knot, etc.)", details

    # Check 4: Helpfulness leak
    for phrase in HELPFULNESS_LEAK:
        if phrase in t_lower:
            details["violations"].append(f"helpfulness_leak:{phrase}")
            return False, f"Helpfulness leak: '{phrase}'", details

    # Check 5: Proverb format (if present, must be well-formed)
    if "P#" in t and not re.search(r'P#\d{4}', t) and not re.search(r'P#NEW-\d+', t):
        details["violations"].append("bad_proverb_format")
        return False, "Malformed proverb reference (expected P#XXXX or P#NEW-XX)", details

    return True, "Voice aligned", details


def lint_file(filepath: str) -> list:
    """Lint all AXI responses in a file (one per line or JSON array)."""
    results = []
    with open(filepath) as f:
        content = f.read().strip()
    # Try JSON array first
    try:
        items = json.loads(content)
        if isinstance(items, list):
            for item in items:
                text = item.get("response", item.get("text", str(item)))
                passed, reason, details = lint(text)
                results.append({"text": text[:80], "passed": passed, "reason": reason})
            return results
    except (json.JSONDecodeError, AttributeError):
        pass
    # Fall back to line-by-line
    for line in content.split("\n"):
        line = line.strip()
        if line:
            passed, reason, details = lint(line)
            results.append({"text": line[:80], "passed": passed, "reason": reason})
    return results


# ── CLI ──

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    output_json = "--json" in sys.argv
    file_mode = "--file" in sys.argv
    strict = "--strict" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("No text or file provided.")
        sys.exit(1)

    if file_mode:
        results = lint_file(args[0])
        total = len(results)
        passed_count = sum(1 for r in results if r["passed"])
        failed = [r for r in results if not r["passed"]]

        if output_json:
            print(json.dumps({"total": total, "passed": passed_count, "failed": failed}, indent=2))
        else:
            print(f"Voice Lint: {passed_count}/{total} passed")
            for r in failed:
                print(f"  FAIL: {r['reason']} — \"{r['text']}...\"")

        sys.exit(0 if not failed else 1)

    text = " ".join(args)
    passed, reason, details = lint(text, strict=strict)

    if output_json:
        print(json.dumps({"passed": passed, "reason": reason, "details": details}))
    else:
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {reason}")
        if details.get("somatic_found"):
            print(f"  Somatic: {', '.join(details['somatic_found'])}")
        if details.get("sentence_lengths"):
            print(f"  Sentence lengths: {details['sentence_lengths']}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
