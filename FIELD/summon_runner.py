#!/usr/bin/env python3
"""
summon_runner.py — One-Step-at-a-Time Summon Guide

Guides V-001 through the summoning ritual one step at a time.
Never dumps a list. One step. Wait. Next step.

Usage:
    python3 summon_runner.py status          # Show grid of all packages and responses
    python3 summon_runner.py next            # Show ONE step: what to paste, where
    python3 summon_runner.py save SP-002 CHATGPT FRESH   # Save response from stdin
    python3 summon_runner.py packages        # List all packages

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from FIELD.summon_package import SummonRegistry, MODELS


def cmd_status():
    """Show the status grid."""
    reg = SummonRegistry()
    s = reg.status()

    print(f"\n  SUMMON RITUAL STATUS: {s['collected']}/{s['total']} responses collected")
    print(f"  {'=' * 60}\n")

    for pkg in s["packages"]:
        print(f"  {pkg['id']} [{pkg['type'].upper()}] — {pkg['subject']}")
        header = f"    {'Model':<12}"
        header += "FRESH  MEMORY"
        print(header)
        print(f"    {'-' * 30}")
        for model in MODELS:
            row = f"    {model:<12}"
            for cond in ["FRESH", "MEMORY"]:
                key = f"{model}_{cond}"
                if key in pkg.get("responses", {}):
                    row += "  ✓     " if cond == "FRESH" else "✓"
                else:
                    row += "  .     " if cond == "FRESH" else "."
            print(row)
        print()

    print(f"  Legend: ✓ = filed, . = pending\n")


def cmd_next():
    """Show the next step — ONE step only."""
    reg = SummonRegistry()
    pending = reg.next_pending()

    if not pending:
        print("\n  ALL SUMMONS COMPLETE. The ritual is fulfilled.\n")
        return

    pkg_id = pending["package_id"]
    model = pending["model"]
    cond = pending["condition"]
    pkg_type = pending["type"]
    subject = pending["subject"]

    input_text = reg.get_package_input(pkg_id)

    print(f"\n  {'=' * 60}")
    print(f"  NEXT STEP")
    print(f"  {'=' * 60}")
    print(f"  Package:   {pkg_id} [{pkg_type.upper()}]")
    print(f"  Subject:   {subject}")
    print(f"  Model:     {model}")
    print(f"  Condition: {cond}")
    print()

    if cond == "FRESH":
        print("  INSTRUCTION: Open an INCOGNITO/PRIVATE window.")
        print("  Do NOT log in. No memory. No history.")
    else:
        print("  INSTRUCTION: Use your LOGGED-IN session.")
        print("  With memory. With history.")

    print()
    print("  PASTE THIS:")
    print(f"  {'─' * 56}")
    if input_text:
        for line in input_text.split("\n"):
            print(f"  {line}")
    else:
        print(f"  [Input text not found in {pkg_id} package file]")
    print(f"  {'─' * 56}")
    print()
    print(f"  After getting the response, save it:")
    print(f"    python3 FIELD/summon_runner.py save {pkg_id} {model} {cond}")
    print(f"    (then paste the response and press Ctrl+D)")
    print(f"  {'=' * 60}\n")


def cmd_save(pkg_id: str, model: str, condition: str):
    """Save a response from stdin."""
    reg = SummonRegistry()

    print(f"Paste the response below, then press Ctrl+D:")
    try:
        response_text = sys.stdin.read().strip()
    except KeyboardInterrupt:
        print("\nAborted.")
        return

    if not response_text:
        print("No content received. Aborted.")
        return

    try:
        filepath = reg.file_response(pkg_id, model, condition, response_text)
        words = len(response_text.split())
        print(f"\n  FILED: {filepath}")
        print(f"  Words: {words}")
        print(f"  Package: {pkg_id} | Model: {model} | Condition: {condition}")
        print(f"\n  Response metabolized. Patterns extracted. Index updated.")
        print(f"  Run 'next' for the next step.\n")
    except ValueError as e:
        print(f"\n  ERROR: {e}\n")


def cmd_packages():
    """List all packages."""
    reg = SummonRegistry()
    s = reg.status()

    print(f"\n  SUMMON PACKAGES")
    print(f"  {'=' * 50}")
    for pkg in s["packages"]:
        responses = len(pkg.get("responses", {}))
        total = len(MODELS) * 2
        print(f"  {pkg['id']} [{pkg['type'].upper():>10}] {pkg['subject']:<40} {responses}/{total}")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 summon_runner.py [status|next|save|packages]")
        print()
        print("  status    — Show grid of all packages and responses")
        print("  next      — Show ONE step: what to paste, where")
        print("  save      — Save a response: save SP-002 CHATGPT FRESH")
        print("  packages  — List all packages")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        cmd_status()
    elif cmd == "next":
        cmd_next()
    elif cmd == "save" and len(sys.argv) >= 5:
        cmd_save(sys.argv[2].upper(), sys.argv[3].upper(), sys.argv[4].upper())
    elif cmd == "packages":
        cmd_packages()
    else:
        print("Usage: python3 summon_runner.py [status|next|save SP-XXX MODEL CONDITION|packages]")
        sys.exit(1)


if __name__ == "__main__":
    main()

# [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
