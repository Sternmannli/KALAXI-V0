#!/usr/bin/env python3
"""
voice_regression.py — AXI Voice Regression Test Runner

Reads GOLDEN_REGRESSION.jsonl, runs each reference response through
voice_lint, and produces a regression score. Used to detect voice drift
when training new models or updating the voice canon.

Usage:
    python TOOLS/voice_regression.py                     # full run
    python TOOLS/voice_regression.py --register grief    # single register
    python TOOLS/voice_regression.py --json              # JSON output
    python TOOLS/voice_regression.py --strict            # strict mode

Exits 0 if >=90% pass, 1 otherwise.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "TOOLS"))

from voice_lint import lint  # noqa: E402


def run_regression(corpus_path: Path, strict: bool = False,
                   register_filter: str = None) -> dict:
    """Run voice lint on every golden regression entry."""
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "pass_rate": 0.0,
        "by_register": defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0}),
        "failures": [],
    }

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            metadata = entry.get("metadata", {})
            register = metadata.get("register", "unknown")

            if register_filter and register != register_filter:
                continue

            messages = entry.get("messages", [])
            response = ""
            prompt = ""
            for msg in messages:
                if msg["role"] == "assistant":
                    response = msg["content"]
                elif msg["role"] == "user":
                    prompt = msg["content"]

            if not response:
                continue

            results["total"] += 1
            results["by_register"][register]["total"] += 1

            passed, reason, details = lint(response, strict=strict)

            if passed:
                results["passed"] += 1
                results["by_register"][register]["passed"] += 1
            else:
                results["failed"] += 1
                results["by_register"][register]["failed"] += 1
                results["failures"].append({
                    "register": register,
                    "prompt": prompt[:80],
                    "response": response[:120],
                    "reason": reason,
                    "voice_score": metadata.get("voice_score", 0),
                })

    if results["total"] > 0:
        results["pass_rate"] = round(results["passed"] / results["total"] * 100, 1)

    # Convert defaultdict to regular dict for JSON
    results["by_register"] = dict(results["by_register"])

    return results


def main():
    corpus_path = ROOT / "TRAINING" / "GOLDEN_REGRESSION.jsonl"
    if not corpus_path.exists():
        print(f"Golden regression corpus not found: {corpus_path}")
        print("Run: python SCRIPTS/build_golden_regression.py")
        sys.exit(1)

    output_json = "--json" in sys.argv
    strict = "--strict" in sys.argv
    register_filter = None

    for i, arg in enumerate(sys.argv):
        if arg == "--register" and i + 1 < len(sys.argv):
            register_filter = sys.argv[i + 1]

    results = run_regression(corpus_path, strict=strict,
                             register_filter=register_filter)

    if output_json:
        # Truncate failures for cleaner JSON
        for f in results["failures"]:
            f["response"] = f["response"][:80]
        print(json.dumps(results, indent=2))
    else:
        print(f"AXI Voice Regression — {'STRICT' if strict else 'STANDARD'} mode")
        print(f"{'=' * 55}")
        print(f"Total:  {results['total']}")
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")
        print(f"Rate:   {results['pass_rate']}%")
        print()
        print("By register:")
        for reg, data in sorted(results["by_register"].items()):
            rate = round(data["passed"] / data["total"] * 100, 1) if data["total"] > 0 else 0
            bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
            print(f"  {reg:12s} {bar} {rate:5.1f}% ({data['passed']}/{data['total']})")

        if results["failures"]:
            print(f"\nFirst 5 failures:")
            for f in results["failures"][:5]:
                print(f"  [{f['register']}] {f['reason']}")
                print(f"    \"{f['response'][:80]}...\"")

    threshold = 90.0
    if results["pass_rate"] >= threshold:
        if not output_json:
            print(f"\nVERDICT: PASS (>= {threshold}%)")
        sys.exit(0)
    else:
        if not output_json:
            print(f"\nVERDICT: FAIL (< {threshold}%)")
        sys.exit(1)


if __name__ == "__main__":
    main()
