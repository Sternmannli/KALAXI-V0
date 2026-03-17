#!/usr/bin/env python3
"""
format_data.py — Convert raw essence to instruction-tuning JSONL.

Input: TRAINING/raw_essence.json (from extract_essence.py)
Output: TRAINING/axi_training.jsonl (instruction-tuning format)

Each item becomes a (system, instruction, response) triple suitable for
LoRA fine-tuning on Qwen2, Phi-3, SmolLM, or TinyLlama.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRAINING = ROOT / "TRAINING"

SYSTEM_PROMPT = (
    "You are AXI, the voice of the KALAXI constitutional framework. "
    "Your core law: D = A × L × M (Dignity = Agency × Legibility × Moral Standing). "
    "If any dimension reaches zero, you stop. You speak in short sentences. "
    "You witness before you respond. You hold the gap."
)

# Instruction templates per type
PROVERB_INSTRUCTIONS = [
    "Share wisdom about this.",
    "What does the canon say?",
    "Speak.",
    "A word for this moment.",
    "What does AXI offer here?",
    "Witness this.",
]

NARRATIVE_INSTRUCTIONS = [
    "Tell me about this.",
    "What happened here?",
    "Continue the story.",
    "What does the narrative hold?",
    "Read from the canon.",
]

COVENANT_INSTRUCTIONS = [
    "What is this covenant?",
    "Explain this law.",
    "What does the constitution say?",
    "State the rule.",
]

TREASURE_INSTRUCTIONS = [
    "What is this treasure?",
    "Describe this pattern.",
    "What does the archive hold here?",
]

VOICE_INSTRUCTIONS = [
    "How should AXI speak?",
    "What is the voice principle?",
    "Describe the voice architecture.",
]


def format_item(item: dict) -> dict | None:
    """Convert a raw essence item to instruction-tuning format."""
    item_type = item.get("type", "")
    text = item.get("text", "").strip()

    if not text or len(text) < 10:
        return None

    if item_type == "proverb":
        instruction = random.choice(PROVERB_INSTRUCTIONS)
        response = text
    elif item_type == "narrative":
        instruction = random.choice(NARRATIVE_INSTRUCTIONS)
        response = text
    elif item_type == "covenant":
        cov_id = item.get("id", "")
        instruction = random.choice(COVENANT_INSTRUCTIONS)
        if cov_id:
            instruction = f"{instruction} ({cov_id})"
        response = text
    elif item_type == "treasure":
        t_id = item.get("id", "")
        formula = item.get("formula", "")
        instruction = random.choice(TREASURE_INSTRUCTIONS)
        if t_id:
            instruction = f"{instruction} ({t_id})"
        response = text
        if formula:
            response += f"\n\nFormula: {formula}"
    elif item_type == "voice_principle":
        instruction = random.choice(VOICE_INSTRUCTIONS)
        response = text
    else:
        return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response},
        ]
    }


def main():
    raw_path = TRAINING / "raw_essence.json"
    if not raw_path.exists():
        print("Run extract_essence.py first.")
        return

    raw = json.loads(raw_path.read_text())
    items = raw.get("items", [])
    print(f"Loaded {len(items)} raw items.")

    formatted = []
    for item in items:
        result = format_item(item)
        if result:
            formatted.append(result)

    # Shuffle for training
    random.seed(42)
    random.shuffle(formatted)

    # Split: 90% train, 10% eval
    split_idx = int(len(formatted) * 0.9)
    train_set = formatted[:split_idx]
    eval_set = formatted[split_idx:]

    # Write JSONL
    train_path = TRAINING / "axi_training.jsonl"
    eval_path = TRAINING / "axi_eval.jsonl"

    with open(train_path, "w") as f:
        for item in train_set:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(eval_path, "w") as f:
        for item in eval_set:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Training: {len(train_set)} examples → {train_path}")
    print(f"Evaluation: {len(eval_set)} examples → {eval_path}")
    print(f"Total: {len(formatted)} instruction-tuning pairs")


if __name__ == "__main__":
    main()
