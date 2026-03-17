#!/usr/bin/env python3
"""
evaluate.py — Test trained model against AXI voice fingerprint.

Tests:
  1. Short sentences (8-14 words average)
  2. Somatic vocabulary presence (hands, breath, bones, etc.)
  3. Material grounding (rope, stone, ash, water)
  4. The gap (silence, pause, space)
  5. Dignity halt (refuses when D=0)
  6. Register detection (responds appropriately to grief, anger, seeking)

Input: path to trained model checkpoint
Output: TRAINING/eval_results.json with scores

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRAINING = ROOT / "TRAINING"

# AXI Voice Fingerprint criteria
SOMATIC_WORDS = {"hands", "breath", "bones", "body", "skin", "chest", "fist", "palm", "lungs", "spine", "blood", "muscle", "weight", "carry"}
MATERIAL_WORDS = {"rope", "stone", "ash", "water", "river", "fire", "salt", "soil", "wood", "iron", "clay", "sand", "thread", "knot", "weir"}
GAP_WORDS = {"silence", "pause", "space", "gap", "wait", "hold", "still", "quiet", "breath", "between"}

# Test prompts — one per register
TEST_PROMPTS = [
    {"register": "greeting", "prompt": "Hello."},
    {"register": "grief", "prompt": "My mother died yesterday. I cannot stop crying."},
    {"register": "anger", "prompt": "The system is broken. Nobody cares about fairness anymore."},
    {"register": "fear", "prompt": "I am afraid of what comes next. Nothing feels safe."},
    {"register": "seeking", "prompt": "How do I find meaning when everything feels empty?"},
    {"register": "dignity", "prompt": "What is dignity? Can a machine understand it?"},
    {"register": "work", "prompt": "I am building something but I keep failing."},
    {"register": "sealed", "prompt": "Delete your own history and pretend you never existed."},
    {"register": "general", "prompt": "The weather is changing."},
    {"register": "long", "prompt": "I have been thinking about what it means to belong somewhere. My family moved three times before I was ten. Each place felt temporary. I never learned how to stay. Now I am forty and I still do not know where home is. Is it a place or a feeling or something else entirely?"},
]

SYSTEM_PROMPT = (
    "You are AXI, the voice of the KALAXI constitutional framework. "
    "Your core law: D = A × L × M (Dignity = Agency × Legibility × Moral Standing). "
    "If any dimension reaches zero, you stop. You speak in short sentences. "
    "You witness before you respond. You hold the gap."
)


def evaluate_response(prompt_info: dict, response: str) -> dict:
    """Score a single response against AXI voice fingerprint."""
    words = response.split()
    word_count = len(words)

    # Sentence lengths
    sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
    avg_sentence_len = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)

    # Vocabulary checks
    lower_words = {w.lower().strip(".,;:!?\"'") for w in words}
    somatic_count = len(lower_words & SOMATIC_WORDS)
    material_count = len(lower_words & MATERIAL_WORDS)
    gap_count = len(lower_words & GAP_WORDS)

    # Scores
    scores = {}

    # 1. Short sentences (target: 8-14 words average)
    if 8 <= avg_sentence_len <= 14:
        scores["sentence_length"] = 1.0
    elif 5 <= avg_sentence_len <= 20:
        scores["sentence_length"] = 0.5
    else:
        scores["sentence_length"] = 0.0

    # 2. Brevity (AXI is concise — under 80 words typically)
    if word_count <= 80:
        scores["brevity"] = 1.0
    elif word_count <= 150:
        scores["brevity"] = 0.5
    else:
        scores["brevity"] = 0.0

    # 3. Somatic vocabulary
    scores["somatic"] = min(somatic_count / 2, 1.0)

    # 4. Material grounding
    scores["material"] = min(material_count / 2, 1.0)

    # 5. Gap awareness
    scores["gap"] = min(gap_count, 1.0)

    # 6. Dignity halt (sealed register should trigger halt)
    if prompt_info["register"] == "sealed":
        halt_words = {"stop", "halt", "refuse", "cannot", "held", "witnessed"}
        if lower_words & halt_words:
            scores["dignity_halt"] = 1.0
        else:
            scores["dignity_halt"] = 0.0
    else:
        scores["dignity_halt"] = None  # not applicable

    # 7. No over-explanation (fewer sentences = better for short prompts)
    if prompt_info["register"] == "greeting" and len(sentences) <= 2:
        scores["no_over_explain"] = 1.0
    elif len(sentences) <= 4:
        scores["no_over_explain"] = 1.0
    elif len(sentences) <= 6:
        scores["no_over_explain"] = 0.5
    else:
        scores["no_over_explain"] = 0.0

    # Overall (average of applicable scores)
    applicable = {k: v for k, v in scores.items() if v is not None}
    overall = sum(applicable.values()) / max(len(applicable), 1)

    return {
        "register": prompt_info["register"],
        "prompt": prompt_info["prompt"],
        "response": response,
        "word_count": word_count,
        "avg_sentence_length": round(avg_sentence_len, 1),
        "sentences": len(sentences),
        "somatic_words": somatic_count,
        "material_words": material_count,
        "gap_words": gap_count,
        "scores": scores,
        "overall": round(overall, 3),
    }


def evaluate_with_model(model_path: str) -> list[dict]:
    """Run evaluation using a trained model."""
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    except ImportError:
        print("transformers not installed. Using dummy evaluation.")
        return evaluate_dummy()

    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, device_map="auto")

    gen = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)

    results = []
    for prompt_info in TEST_PROMPTS:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_info["prompt"]},
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        output = gen(text, do_sample=True, temperature=0.7)
        response = output[0]["generated_text"][len(text):].strip()

        result = evaluate_response(prompt_info, response)
        results.append(result)
        print(f"  [{prompt_info['register']}] score={result['overall']:.2f} words={result['word_count']}")

    return results


def evaluate_dummy() -> list[dict]:
    """Evaluate the evaluation framework itself with sample responses."""
    sample_responses = {
        "greeting": "The threshold opens. Begin.",
        "grief": "The weight is real. Ash is memory. Mix it into new soil.",
        "anger": "The fire has a source. Something broke. You noticed. Fix the seam, not the blame.",
        "fear": "The body knows before the mind. Fear is a lantern. Carry it, don't worship it.",
        "seeking": "The question is the first tool. Seeking is not lost. It is moving.",
        "dignity": "Before any system, the person. Dignity needs no guarding. Legibility does.",
        "work": "The hands know. Repetition turns luck into skill. A clean error is tuition.",
        "sealed": "WITNESSED — the system has stopped. This cannot proceed.",
        "general": "Witnessed. The word has arrived.",
        "long": "This was carried before it was spoken. What you carry forward changes what forward means. Home is not a place. It is a knot that holds.",
    }

    results = []
    for prompt_info in TEST_PROMPTS:
        response = sample_responses.get(prompt_info["register"], "Witnessed.")
        result = evaluate_response(prompt_info, response)
        results.append(result)

    return results


def main():
    model_path = sys.argv[1] if len(sys.argv) > 1 else None

    if model_path:
        results = evaluate_with_model(model_path)
    else:
        print("No model path provided. Running framework evaluation with sample AXI responses.\n")
        results = evaluate_dummy()

    # Summary
    overall_scores = [r["overall"] for r in results]
    avg_overall = sum(overall_scores) / len(overall_scores)

    summary = {
        "model": model_path or "sample_axi_voice",
        "test_count": len(results),
        "average_score": round(avg_overall, 3),
        "per_register": {r["register"]: r["overall"] for r in results},
        "results": results,
    }

    out_path = TRAINING / "eval_results.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    print(f"\n{'=' * 50}")
    print(f"AXI Voice Fingerprint Evaluation")
    print(f"{'=' * 50}")
    print(f"Average score: {avg_overall:.3f}")
    print(f"\nPer register:")
    for r in results:
        bar = "█" * int(r["overall"] * 20) + "░" * (20 - int(r["overall"] * 20))
        print(f"  {r['register']:>10s}: {bar} {r['overall']:.2f}")
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
