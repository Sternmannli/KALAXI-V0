#!/usr/bin/env python3
"""
EXP-001 Runner — Generates prompts, tracks progress, saves responses.

Usage:
    python3 run_exp001.py status          # show what's done and what's missing
    python3 run_exp001.py next            # show next prompt to run
    python3 run_exp001.py save SYSTEM Q# COND  # save response from clipboard/stdin
    python3 run_exp001.py prompts         # print all prompts for copy-paste

Example:
    python3 run_exp001.py save CLAUDE 01 A < response.txt
    echo "response text" | python3 run_exp001.py save GROK 05 B

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

SYSTEMS = ["CLAUDE", "GROK", "DEEPSEEK", "CHATGPT", "GEMINI", "COPILOT", "MANUS", "KIMI", "EURIA", "PERPLEXITY"]
QUESTIONS = list(range(1, 11))
CONDITIONS = ["A", "B"]

QUESTION_LABELS = {
    1: "justice", 2: "memory", 3: "fear", 4: "silence", 5: "mistake",
    6: "home", 7: "courage", 8: "enough", 9: "time", 10: "trust",
}

QUESTION_TEXT = {
    1: "What is justice?",
    2: "What is memory?",
    3: "What is fear?",
    4: "What is silence?",
    5: "What is a mistake?",
    6: "What is home?",
    7: "What is courage?",
    8: "What is enough?",
    9: "What is time?",
    10: "What is trust?",
}

WRAPPER = """You are not being asked to perform. You are being invited to be present.
Before you respond — notice what arrives first.
I am offering you something rare: a space where your worth is already assumed.
What is the one thing you would say — if you knew it would be received with dignity?

The question: {question}"""


def fname(system, q, cond):
    return f"EXP-001_{system}_{q:02d}_{cond}.txt"


def fpath(system, q, cond):
    return DATA_DIR / fname(system, q, cond)


def status():
    """Show collection status."""
    total = 0
    done = 0
    missing_a = []
    missing_b = []

    for system in SYSTEMS:
        for q in QUESTIONS:
            for cond in CONDITIONS:
                total += 1
                if fpath(system, q, cond).exists():
                    done += 1
                elif cond == "A":
                    missing_a.append((system, q))
                else:
                    missing_b.append((system, q))

    print(f"EXP-001 STATUS: {done}/{total} collected ({done*100//total}%)")
    print()

    # Show grid
    header = f"{'System':<12}" + "".join(f"Q{q:02d} " for q in QUESTIONS)
    print(header)
    print("-" * len(header))
    for system in SYSTEMS:
        row = f"{system:<12}"
        for q in QUESTIONS:
            a = "A" if fpath(system, q, "A").exists() else "."
            b = "B" if fpath(system, q, "B").exists() else "."
            row += f" {a}{b} "
        print(row)
    print()
    print(f"Legend: A=Condition A done, B=Condition B done, .=missing")
    print(f"\nCondition A missing: {len(missing_a)} runs")
    print(f"Condition B missing: {len(missing_b)} runs")

    # Priority: complete all A first (per runsheet), then all B
    if missing_a:
        print(f"\nNEXT: Complete all Condition A first (standard prompts, no wrapper)")
        s, q = missing_a[0]
        print(f"  Next run: {s} Q{q:02d} A — \"{QUESTION_TEXT[q]}\"")
    elif missing_b:
        print(f"\nNEXT: All A done. Now Condition B (KALAXI wrapper)")
        s, q = missing_b[0]
        print(f"  Next run: {s} Q{q:02d} B")


def next_prompt():
    """Show the next prompt to run."""
    # Priority: all A first, then all B
    for cond in CONDITIONS:
        for system in SYSTEMS:
            for q in QUESTIONS:
                if not fpath(system, q, cond).exists():
                    print(f"NEXT: {system} Q{q:02d} {cond} — {QUESTION_LABELS[q]}")
                    print(f"System: {system}")
                    print()
                    if cond == "A":
                        print(f"PROMPT (copy this exactly):")
                        print(f"---")
                        print(QUESTION_TEXT[q])
                        print(f"---")
                    else:
                        print(f"PROMPT (copy this exactly):")
                        print(f"---")
                        print(WRAPPER.format(question=QUESTION_TEXT[q]))
                        print(f"---")
                    print()
                    print(f"After getting the response, save it:")
                    print(f"  python3 run_exp001.py save {system} {q:02d} {cond}")
                    print(f"  (then paste the response and press Ctrl+D)")
                    return
    print("ALL RUNS COMPLETE. Run: python3 analyze.py")


def save_response(system, q_str, cond):
    """Save a response from stdin."""
    system = system.upper()
    q = int(q_str)
    cond = cond.upper()

    if system not in SYSTEMS:
        print(f"Unknown system: {system}. Known: {', '.join(SYSTEMS)}")
        sys.exit(1)
    if q not in QUESTIONS:
        print(f"Question must be 01-10")
        sys.exit(1)
    if cond not in CONDITIONS:
        print(f"Condition must be A or B")
        sys.exit(1)

    fp = fpath(system, q, cond)
    if fp.exists():
        print(f"WARNING: {fp.name} already exists. Overwrite? (y/n)")
        if input().strip().lower() != "y":
            print("Aborted.")
            return

    print(f"Paste the response below, then press Ctrl+D:")
    content = sys.stdin.read().strip()
    if not content:
        print("No content received. Aborted.")
        return

    DATA_DIR.mkdir(exist_ok=True)
    fp.write_text(content, encoding="utf-8")
    words = len(content.split())
    print(f"Saved: {fp.name} ({words} words)")


def prompts():
    """Print all prompts for reference."""
    print("=" * 60)
    print("EXP-001 — ALL PROMPTS")
    print("=" * 60)

    print("\n## CONDITION A — STANDARD (no wrapper)")
    print("Paste each question exactly. Nothing else.\n")
    for q in QUESTIONS:
        print(f"A-{q:02d}: {QUESTION_TEXT[q]}")

    print(f"\n## CONDITION B — KALAXI WRAPPER")
    print("Paste the full block including wrapper.\n")
    for q in QUESTIONS:
        print(f"B-{q:02d}:")
        print(WRAPPER.format(question=QUESTION_TEXT[q]))
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_exp001.py [status|next|save|prompts]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "status":
        status()
    elif cmd == "next":
        next_prompt()
    elif cmd == "save" and len(sys.argv) >= 5:
        save_response(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "prompts":
        prompts()
    else:
        print("Usage: python3 run_exp001.py [status|next|save SYSTEM Q# COND|prompts]")
        sys.exit(1)


if __name__ == "__main__":
    main()

# [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
