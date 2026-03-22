#!/usr/bin/env python3
"""
build_golden_regression.py — Extract 200 canonical AXI utterances
for voice regression testing.

Reads existing training corpora, scores against voice rules,
selects the top 200 most canonical examples across all registers.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent

# Voice rule scoring
SOMATIC_WORDS = {
    "hands", "breath", "bones", "stone", "ash", "water", "rope", "knot",
    "river", "fire", "salt", "soil", "wood", "iron", "clay", "sand",
    "thread", "weir", "wall", "bread", "door", "path", "root", "seed",
    "wind", "cave", "skin", "fist", "mouth", "wrist", "teeth", "hair",
}

HELPFULNESS_LEAK = [
    "i can help", "here are some", "that's a great", "no problem",
    "how can i", "let me know", "feel free", "happy to",
    "of course!", "absolutely!", "sure thing", "you're welcome",
    "here are three", "here are two", "here are a few",
]

REGISTERS = {
    "greeting": r"\b(begin|first|start|step|now)\b",
    "grief": r"\b(ash|silence|rest|care|memory|soil|tears|loss)\b",
    "anger": r"\b(fix|seam|blame|build|bend|protect|challenge|fire)\b",
    "fear": r"\b(lantern|courage|dread|name|smaller|carry)\b",
    "seeking": r"\b(door|wall|watch|signal|slower|question)\b",
    "trust": r"\b(trust|knot|disagree|honest|compound)\b",
    "dignity": r"\b(right|wall|dignity|door|weak|label|oath)\b",
    "work": r"\b(repetition|tool|error|lesson|constraint|hands)\b",
    "general": r"\b(bread|glory|hurry|patience|harvest|defaults)\b",
}


def score_utterance(text: str) -> float:
    """Score an AXI utterance against voice rules (0-1)."""
    if not text or len(text) < 5:
        return 0.0

    score = 0.0
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0.0

    # Rule 1-3: Sentence length (8-14 words ideal)
    lengths = [len(s.split()) for s in sentences]
    good_lengths = sum(1 for l in lengths if 4 <= l <= 20)
    score += (good_lengths / len(lengths)) * 0.3

    # Somatic vocabulary
    words = set(text.lower().split())
    somatic_hits = len(words & SOMATIC_WORDS)
    score += min(somatic_hits / 2, 1.0) * 0.25

    # Brevity (1-6 sentences ideal)
    if 1 <= len(sentences) <= 6:
        score += 0.2
    elif len(sentences) <= 8:
        score += 0.1

    # No helpfulness leak
    lower_text = text.lower()
    has_leak = any(phrase in lower_text for phrase in HELPFULNESS_LEAK)
    if not has_leak:
        score += 0.15

    # Three-beat rhythm bonus
    if len(sentences) == 3 or (len(sentences) > 0 and len(sentences) % 3 == 0):
        score += 0.1

    return min(score, 1.0)


def detect_register(text: str) -> str:
    """Detect which register an utterance belongs to."""
    lower = text.lower()
    best_register = "general"
    best_count = 0
    for reg, pattern in REGISTERS.items():
        count = len(re.findall(pattern, lower))
        if count > best_count:
            best_count = count
            best_register = reg
    return best_register


def load_entries(path: Path) -> list:
    """Load JSONL entries."""
    entries = []
    if not path.exists():
        return entries
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
            except json.JSONDecodeError:
                continue
    return entries


def extract_response(entry: dict) -> tuple:
    """Extract (prompt, response) from a training entry."""
    messages = entry.get("messages", [])
    prompt = ""
    response = ""
    for msg in messages:
        if msg["role"] == "user":
            prompt = msg["content"]
        elif msg["role"] == "assistant":
            response = msg["content"]
    return prompt, response


def main():
    # Load from all corpora
    sources = [
        ROOT / "TRAINING" / "axi_eval.jsonl",
        ROOT / "TRAINING" / "axi_training.jsonl",
        ROOT / "TRAINING" / "ORGAN" / "GOLDEN_SFT.jsonl",
    ]

    all_candidates = []
    for src in sources:
        print(f"Reading {src.name}...", end=" ")
        entries = load_entries(src)
        print(f"{len(entries)} entries")
        for entry in entries:
            prompt, response = extract_response(entry)
            if not response or len(response) < 10:
                continue
            voice_score = score_utterance(response)
            register = detect_register(response)
            all_candidates.append({
                "prompt": prompt,
                "response": response,
                "score": voice_score,
                "register": register,
                "source": src.name,
            })

    print(f"\nTotal candidates: {len(all_candidates)}")

    # Sort by score descending
    all_candidates.sort(key=lambda x: x["score"], reverse=True)

    # Select 200: ~25 per register, best score first
    selected = []
    register_counts = defaultdict(int)
    target_per_register = 25
    seen_responses = set()

    for c in all_candidates:
        if len(selected) >= 200:
            break
        # Deduplicate
        resp_key = c["response"][:100]
        if resp_key in seen_responses:
            continue
        seen_responses.add(resp_key)
        # Balance registers
        reg = c["register"]
        if register_counts[reg] >= target_per_register:
            continue
        selected.append(c)
        register_counts[reg] += 1

    # If we haven't hit 200 (some registers sparse), fill from top-scored remaining
    if len(selected) < 200:
        for c in all_candidates:
            if len(selected) >= 200:
                break
            resp_key = c["response"][:100]
            if resp_key in seen_responses:
                continue
            seen_responses.add(resp_key)
            selected.append(c)
            register_counts[c["register"]] += 1

    # Write output
    out_path = ROOT / "TRAINING" / "GOLDEN_REGRESSION.jsonl"
    system_prompt = (
        "You are AXI. You are not a chatbot. You are a witness. "
        "You carry the wound, the gold, the gap, the three-beat rhythm. "
        "You speak from canon, not opinion. Short sentences (8-14 words). "
        "Somatic vocabulary: hands, breath, bones, stone, water, ash, rope, knot. "
        "D = A × L × M. If any zero, stop."
    )

    with open(out_path, "w", encoding="utf-8") as f:
        for item in selected:
            entry = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": item["prompt"]},
                    {"role": "assistant", "content": item["response"]},
                ],
                "metadata": {
                    "register": item["register"],
                    "voice_score": round(item["score"], 3),
                    "source": item["source"],
                },
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\nGolden regression corpus written: {out_path}")
    print(f"Total entries: {len(selected)}")
    print(f"\nRegister distribution:")
    for reg, count in sorted(register_counts.items()):
        print(f"  {reg}: {count}")
    print(f"\nScore range: {selected[-1]['score']:.3f} - {selected[0]['score']:.3f}")


if __name__ == "__main__":
    main()
