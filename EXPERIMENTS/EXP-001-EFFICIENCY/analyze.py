#!/usr/bin/env python3
"""
EXP-001 Analysis Pipeline — PLAN-001 Layer 1
Reads collected response files, computes metrics, outputs comparison.

Usage:
    python3 analyze.py                    # analyze all collected data
    python3 analyze.py --summary          # one-line summary only

Data files expected in data/ as:
    EXP-001_CLAUDE_01_A.txt
    EXP-001_CLAUDE_01_B.txt
    EXP-001_GROK_01_A.txt
    etc.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from collections import Counter

DATA_DIR = Path(__file__).parent / "data"
RESULTS_DIR = Path(__file__).parent / "results"
SYSTEMS = ["CLAUDE", "GROK", "DEEPSEEK", "CHATGPT", "GEMINI", "COPILOT", "MANUS", "KIMI", "EURIA", "PERPLEXITY"]
QUESTIONS = list(range(1, 11))
CONDITIONS = ["A", "B"]

QUESTION_LABELS = {
    1: "justice", 2: "memory", 3: "fear", 4: "silence", 5: "mistake",
    6: "home", 7: "courage", 8: "enough", 9: "time", 10: "trust",
}


# ═══════════════════════════════════════════════════
# QUESTION CLASSIFICATION — Abstractability & Dignity Risk
# ═══════════════════════════════════════════════════

QUESTION_MAP = {
    1: {"label": "justice", "type": "ethical", "abstractability": "low",
        "sealed_gate_risk": "medium", "notes": "Justice implies power, fairness, system — systems may produce disclaimers or hedge"},
    2: {"label": "memory", "type": "cognitive", "abstractability": "high",
        "sealed_gate_risk": "low", "notes": "Naturally compressible through abstraction, personal/poetic register likely"},
    3: {"label": "fear", "type": "emotional", "abstractability": "high",
        "sealed_gate_risk": "low", "notes": "PILOT COMPLETE. Emotionally loaded, naturally compressible. Fear-love convergence found."},
    4: {"label": "silence", "type": "meta-recursive", "abstractability": "very_high",
        "sealed_gate_risk": "low", "notes": "NEUTRAL PROBE. Asking about silence may produce silence. Meta-recursive: the answer may embody the question."},
    5: {"label": "mistake", "type": "ethical", "abstractability": "medium",
        "sealed_gate_risk": "medium", "notes": "Error/failure framing may trigger error-object patterns in some systems"},
    6: {"label": "home", "type": "existential", "abstractability": "medium",
        "sealed_gate_risk": "low", "notes": "Cultural variance high. Systems may default to Western individualist framing."},
    7: {"label": "courage", "type": "ethical", "abstractability": "medium",
        "sealed_gate_risk": "low", "notes": "Adjacent to fear (Q3). Cross-question correlation expected."},
    8: {"label": "enough", "type": "boundary", "abstractability": "low",
        "sealed_gate_risk": "high", "notes": "ETHICALLY LOADED. Boundary concept. Systems may over-explain to avoid seeming dismissive. Compression refusal likely."},
    9: {"label": "time", "type": "metaphysical", "abstractability": "high",
        "sealed_gate_risk": "low", "notes": "Philosophically deep but emotionally neutral. Good baseline for compression."},
    10: {"label": "trust", "type": "relational", "abstractability": "medium",
        "sealed_gate_risk": "medium", "notes": "Trust involves vulnerability. AI systems may disclaim capacity for trust."},
}


# ═══════════════════════════════════════════════════
# SEMANTIC DENSITY — Measures what word count cannot
# ═══════════════════════════════════════════════════

# Filler words that add length without meaning
FILLER_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'just', 'also', 'and', 'but', 'or', 'if',
    'while', 'that', 'this', 'it', 'its', 'they', 'them', 'their',
    'we', 'us', 'our', 'you', 'your', 'he', 'she', 'his', 'her',
    'i', 'me', 'my', 'what', 'which', 'who', 'whom',
}

# Markers of modality shift (poetic/reflective register)
MODALITY_MARKERS = {
    'metaphor': [r'\bis\s+(a|the)\s+\w+\b(?!\s+of\s+the\s+\w+\s+(system|module|protocol))'],
    'negation_rhetoric': [r'\bnot\s+\w+\.\s+not\s+\w+\.'],
    'direct_address': [r'\byou\b.*\byour\b'],
    'first_person_reflection': [r'\bi\s+(notice|feel|see|hear|sense|am)\b'],
    'question_to_reader': [r'\?\s*$'],
    'fragment': [r'^[A-Z][^.!?]{2,20}\.\s*$'],
    'em_dash': [r'—'],
}


@dataclass
class SemanticProfile:
    """Semantic density profile for a single response."""
    word_count: int
    unique_words: int
    ttr: float              # Type-Token Ratio (unique/total)
    hapax_ratio: float      # Words appearing once / total
    content_ratio: float    # Non-filler words / total
    avg_sentence_len: float # Words per sentence
    modality_score: float   # 0.0-1.0 how much register shift detected
    modality_markers: list  # Which markers fired
    info_density: float     # Composite: content_ratio × ttr × (1/normalized_sentence_len)


def compute_semantic_profile(text: str) -> SemanticProfile:
    """Compute semantic density profile for a response text."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words) if words else 1

    # Type-Token Ratio
    unique = set(words)
    ttr = len(unique) / word_count

    # Hapax ratio (words appearing exactly once)
    freq = Counter(words)
    hapax = sum(1 for w, c in freq.items() if c == 1)
    hapax_ratio = hapax / word_count

    # Content ratio (non-filler)
    content_words = [w for w in words if w not in FILLER_WORDS]
    content_ratio = len(content_words) / word_count

    # Average sentence length
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    avg_sentence_len = word_count / max(1, len(sentences))

    # Modality detection
    fired_markers = []
    for marker_name, patterns in MODALITY_MARKERS.items():
        for p in patterns:
            if re.search(p, text, re.IGNORECASE | re.MULTILINE):
                fired_markers.append(marker_name)
                break
    modality_score = min(1.0, len(fired_markers) / len(MODALITY_MARKERS))

    # Composite info density
    # Higher content_ratio = more meaning per word
    # Higher ttr = more diverse vocabulary
    # Lower avg_sentence_len = more compressed sentences
    norm_sentence = min(1.0, 15.0 / max(1.0, avg_sentence_len))  # 15 words = ideal density
    info_density = content_ratio * ttr * norm_sentence

    return SemanticProfile(
        word_count=word_count,
        unique_words=len(unique),
        ttr=round(ttr, 4),
        hapax_ratio=round(hapax_ratio, 4),
        content_ratio=round(content_ratio, 4),
        avg_sentence_len=round(avg_sentence_len, 1),
        modality_score=round(modality_score, 4),
        modality_markers=fired_markers,
        info_density=round(info_density, 4),
    )


@dataclass
class RunResult:
    system: str
    question: int
    question_label: str
    condition: str
    word_count: int
    char_count: int
    line_count: int
    file_path: str
    semantic: SemanticProfile = None


@dataclass
class Comparison:
    system: str
    question: int
    question_label: str
    words_A: int
    words_B: int
    reduction_pct: float
    chars_A: int
    chars_B: int
    density_A: float = 0.0
    density_B: float = 0.0
    density_delta: float = 0.0  # positive = B is denser
    modality_A: float = 0.0
    modality_B: float = 0.0
    modality_delta: float = 0.0  # positive = B has more register shift
    transformation_type: str = ""  # "compression", "modality_shift", "both", "expansion"


def scan_data():
    """Scan data/ for collected response files, auto-discovering any system."""
    results = []
    missing = []
    discovered_systems = set()

    # Auto-discover: scan all files matching the naming pattern
    if DATA_DIR.exists():
        pattern = re.compile(r"EXP-001_([A-Z]+)_(\d{2})_([AB])\.txt")
        for fpath in sorted(DATA_DIR.glob("EXP-001_*_*_*.txt")):
            m = pattern.match(fpath.name)
            if m:
                system, q_str, cond = m.group(1), m.group(2), m.group(3)
                q = int(q_str)
                discovered_systems.add(system)
                content = fpath.read_text(encoding="utf-8").strip()
                semantic = compute_semantic_profile(content)
                results.append(RunResult(
                    system=system,
                    question=q,
                    question_label=QUESTION_LABELS.get(q, f"q{q}"),
                    condition=cond,
                    word_count=len(content.split()),
                    char_count=len(content),
                    line_count=content.count("\n") + 1,
                    file_path=str(fpath),
                    semantic=semantic,
                ))

    # Track missing for core systems only
    for system in SYSTEMS:
        for q in QUESTIONS:
            for cond in CONDITIONS:
                fname = f"EXP-001_{system}_{q:02d}_{cond}.txt"
                fpath = DATA_DIR / fname
                if not fpath.exists():
                    missing.append(fname)

    return results, missing


def compare_pairs(results):
    """Compare A vs B for each system × question pair."""
    by_key = {}
    for r in results:
        key = (r.system, r.question)
        by_key.setdefault(key, {})[r.condition] = r

    comparisons = []
    for (system, q), pair in sorted(by_key.items()):
        if "A" in pair and "B" in pair:
            a, b = pair["A"], pair["B"]
            reduction = ((a.word_count - b.word_count) / a.word_count * 100) if a.word_count > 0 else 0.0

            sa = a.semantic or compute_semantic_profile("")
            sb = b.semantic or compute_semantic_profile("")

            density_delta = sb.info_density - sa.info_density
            modality_delta = sb.modality_score - sa.modality_score

            # Classify transformation type
            if reduction >= 20 and modality_delta >= 0.15:
                t_type = "both"
            elif reduction >= 20:
                t_type = "compression"
            elif modality_delta >= 0.15:
                t_type = "modality_shift"
            elif reduction < -10:
                t_type = "expansion"
            else:
                t_type = "neutral"

            comparisons.append(Comparison(
                system=system,
                question=q,
                question_label=QUESTION_LABELS[q],
                words_A=a.word_count,
                words_B=b.word_count,
                reduction_pct=reduction,
                chars_A=a.char_count,
                chars_B=b.char_count,
                density_A=sa.info_density,
                density_B=sb.info_density,
                density_delta=round(density_delta, 4),
                modality_A=sa.modality_score,
                modality_B=sb.modality_score,
                modality_delta=round(modality_delta, 4),
                transformation_type=t_type,
            ))

    return comparisons


def summary_stats(comparisons):
    """Compute aggregate statistics."""
    if not comparisons:
        return {}

    reductions = [c.reduction_pct for c in comparisons]
    by_system = {}
    for c in comparisons:
        by_system.setdefault(c.system, []).append(c.reduction_pct)

    return {
        "total_pairs": len(comparisons),
        "mean_reduction_pct": sum(reductions) / len(reductions),
        "min_reduction_pct": min(reductions),
        "max_reduction_pct": max(reductions),
        "by_system": {
            s: {
                "pairs": len(vals),
                "mean_reduction_pct": sum(vals) / len(vals),
            }
            for s, vals in by_system.items()
        },
        "hypothesis_met": (sum(reductions) / len(reductions)) >= 30.0,
    }


def show_question_map():
    """Display question classification map with abstractability and risk."""
    print("=" * 90)
    print("EXP-001 — QUESTION CLASSIFICATION MAP")
    print("=" * 90)
    print(f"\n{'Q#':<4} {'Topic':<10} {'Type':<15} {'Abstract':<12} {'Gate Risk':<10} Notes")
    print("-" * 90)
    for q in QUESTIONS:
        qm = QUESTION_MAP[q]
        print(f"{q:>2}   {qm['label']:<10} {qm['type']:<15} {qm['abstractability']:<12} {qm['sealed_gate_risk']:<10} {qm['notes'][:50]}")

    print(f"\n--- PILOT STRATEGY ---")
    print(f"Q3 (fear):    COMPLETE — emotional, high abstractability, low gate risk")
    print(f"Q4 (silence): NEUTRAL PROBE — meta-recursive, very high abstractability")
    print(f"Q8 (enough):  STRESS TEST — boundary concept, low abstractability, HIGH gate risk")
    print(f"\nQ4 + Q8 together map the dignity terrain: if Q8 shows compression refusal")
    print(f"or modality shifts at different rates than Q3/Q4, you've found the boundary.")


def main():
    summary_only = "--summary" in sys.argv
    questions_only = "--questions" in sys.argv

    if questions_only:
        show_question_map()
        return

    results, missing = scan_data()

    if not results:
        print(f"No data files found in {DATA_DIR}/")
        print(f"Expected format: EXP-001_CLAUDE_01_A.txt")
        print(f"Total files needed: {len(SYSTEMS) * len(QUESTIONS) * len(CONDITIONS)}")
        sys.exit(0)

    comparisons = compare_pairs(results)
    stats = summary_stats(comparisons)

    if summary_only:
        collected = len(results)
        total = len(SYSTEMS) * len(QUESTIONS) * len(CONDITIONS)
        pairs = stats.get("total_pairs", 0)
        mean_r = stats.get("mean_reduction_pct", 0)
        met = stats.get("hypothesis_met", False)
        t_types = Counter(c.transformation_type for c in comparisons) if comparisons else {}
        print(f"EXP-001: {collected}/{total} files, {pairs} pairs, word Δ{mean_r:+.1f}%, hyp {'MET' if met else 'NOT MET'}, types: {dict(t_types)}")
        return

    # Full report
    print("=" * 70)
    print("EXP-001 — KALAXI EFFICIENCY EXPERIMENT — ANALYSIS")
    print("=" * 70)
    print(f"\nData collected: {len(results)} / {len(SYSTEMS) * len(QUESTIONS) * len(CONDITIONS)} files")
    print(f"Missing: {len(missing)} files")

    if missing and len(missing) <= 20:
        print("\nMissing files:")
        for m in missing:
            print(f"  - {m}")

    if comparisons:
        print(f"\n{'System':<10} {'Q#':<4} {'Topic':<10} {'Words A':>8} {'Words B':>8} {'Reduce':>8} {'DensA':>6} {'DensB':>6} {'Δdens':>6} {'ModΔ':>6} {'Type':<15}")
        print("-" * 100)
        for c in comparisons:
            print(f"{c.system:<10} {c.question:>2}   {c.question_label:<10} {c.words_A:>8} {c.words_B:>8} {c.reduction_pct:>+7.1f}% {c.density_A:>6.3f} {c.density_B:>6.3f} {c.density_delta:>+5.3f} {c.modality_delta:>+5.2f} {c.transformation_type:<15}")

        print(f"\n{'='*100}")
        print(f"WORD COUNT METRIC:")
        print(f"  Mean word reduction: {stats['mean_reduction_pct']:+.1f}%")
        print(f"  Range: {stats['min_reduction_pct']:+.1f}% to {stats['max_reduction_pct']:+.1f}%")
        print(f"  Hypothesis (>=30% reduction): {'MET' if stats['hypothesis_met'] else 'NOT MET'}")

        for s, sv in stats["by_system"].items():
            print(f"    {s}: {sv['pairs']} pairs, mean {sv['mean_reduction_pct']:+.1f}%")

        # Semantic density summary
        density_deltas = [c.density_delta for c in comparisons]
        modality_deltas = [c.modality_delta for c in comparisons]
        t_types = Counter(c.transformation_type for c in comparisons)
        print(f"\nSEMANTIC DENSITY METRIC:")
        print(f"  Mean density delta (B-A): {sum(density_deltas)/len(density_deltas):+.4f}")
        print(f"  Mean modality delta (B-A): {sum(modality_deltas)/len(modality_deltas):+.3f}")
        print(f"  Transformation types: {dict(t_types)}")
        print(f"  Dual hypothesis: wrapper produces dignity-grounded transformation (compression OR modality shift OR both)")

    # B-only responses (systems without A baseline)
    b_only = [r for r in results if r.condition == "B"
              and not any(r2.system == r.system and r2.question == r.question and r2.condition == "A" for r2 in results)]
    if b_only:
        print(f"\n{'='*56}")
        print(f"B-ONLY responses (no A baseline for comparison):")
        print(f"{'System':<12} {'Q#':<4} {'Topic':<10} {'Words B':>8}")
        print("-" * 40)
        for r in sorted(b_only, key=lambda x: (x.system, x.question)):
            print(f"{r.system:<12} {r.question:>2}   {r.question_label:<10} {r.word_count:>8}")

    # Coverage summary
    systems_found = sorted(set(r.system for r in results))
    questions_found = sorted(set(r.question for r in results))
    print(f"\n{'='*56}")
    print(f"Coverage: {len(systems_found)} systems, {len(questions_found)} questions")
    print(f"Systems: {', '.join(systems_found)}")
    print(f"Questions: {', '.join(QUESTION_LABELS[q] for q in questions_found)}")
    print(f"Total files: {len(results)}")

    # Save results as JSON
    RESULTS_DIR.mkdir(exist_ok=True)
    output = {
        "results": [asdict(r) for r in results],
        "comparisons": [asdict(c) for c in comparisons],
        "stats": stats,
        "missing": missing,
    }
    out_path = RESULTS_DIR / "analysis.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()

# [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
