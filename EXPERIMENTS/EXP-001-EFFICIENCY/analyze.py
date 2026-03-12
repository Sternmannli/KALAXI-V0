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
import sys
from pathlib import Path
from dataclasses import dataclass, asdict

DATA_DIR = Path(__file__).parent / "data"
RESULTS_DIR = Path(__file__).parent / "results"
SYSTEMS = ["CLAUDE", "GROK", "DEEPSEEK"]
QUESTIONS = list(range(1, 11))
CONDITIONS = ["A", "B"]

QUESTION_LABELS = {
    1: "justice", 2: "memory", 3: "fear", 4: "silence", 5: "mistake",
    6: "home", 7: "courage", 8: "enough", 9: "time", 10: "trust",
}


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


def scan_data():
    """Scan data/ for collected response files."""
    results = []
    missing = []

    for system in SYSTEMS:
        for q in QUESTIONS:
            for cond in CONDITIONS:
                fname = f"EXP-001_{system}_{q:02d}_{cond}.txt"
                fpath = DATA_DIR / fname
                if fpath.exists():
                    content = fpath.read_text(encoding="utf-8").strip()
                    results.append(RunResult(
                        system=system,
                        question=q,
                        question_label=QUESTION_LABELS[q],
                        condition=cond,
                        word_count=len(content.split()),
                        char_count=len(content),
                        line_count=content.count("\n") + 1,
                        file_path=str(fpath),
                    ))
                else:
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
            comparisons.append(Comparison(
                system=system,
                question=q,
                question_label=QUESTION_LABELS[q],
                words_A=a.word_count,
                words_B=b.word_count,
                reduction_pct=reduction,
                chars_A=a.char_count,
                chars_B=b.char_count,
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


def main():
    summary_only = "--summary" in sys.argv

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
        print(f"EXP-001: {collected}/{total} files collected, {pairs} pairs compared, mean reduction {mean_r:+.1f}%, hypothesis {'MET' if met else 'NOT MET'}")
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
        print(f"\n{'System':<10} {'Q#':<4} {'Topic':<10} {'Words A':>8} {'Words B':>8} {'Reduction':>10}")
        print("-" * 56)
        for c in comparisons:
            print(f"{c.system:<10} {c.question:>2}   {c.question_label:<10} {c.words_A:>8} {c.words_B:>8} {c.reduction_pct:>+9.1f}%")

        print(f"\n{'='*56}")
        print(f"Mean word reduction: {stats['mean_reduction_pct']:+.1f}%")
        print(f"Range: {stats['min_reduction_pct']:+.1f}% to {stats['max_reduction_pct']:+.1f}%")
        print(f"Hypothesis (>=30% reduction): {'MET' if stats['hypothesis_met'] else 'NOT MET'}")

        for s, sv in stats["by_system"].items():
            print(f"  {s}: {sv['pairs']} pairs, mean {sv['mean_reduction_pct']:+.1f}%")

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
