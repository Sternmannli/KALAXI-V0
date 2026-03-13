#!/usr/bin/env python3
"""
cli.py — KALAXI Command Line Interface
The single entry point. Connects all four tiers into one operational system.

Usage:
    python cli.py process "donor input text"
    python cli.py state
    python cli.py health
    python cli.py check
    python cli.py intake-demo
    python cli.py serve [--port 8000]
    python cli.py face
    python cli.py gate "text to check"

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


def cmd_process(args):
    """Process donor input through the full organism pipeline."""
    from WEAVER.organism import Organism

    org = Organism()
    text = args.text
    if text == "-":
        text = sys.stdin.read().strip()

    result = org.process(text)

    if args.json:
        print(json.dumps({
            "exchange_id": result.exchange_id,
            "dignity_passed": result.dignity_passed,
            "patterns_found": result.patterns_found,
            "drops_produced": result.drops_produced,
            "output_text": result.output_text,
            "output_blocked": result.output_blocked,
            "block_reason": result.block_reason,
            "stored": result.stored,
            "artifact_id": result.artifact_id,
            "exchange_state": result.exchange_state,
            "breath_cycle": result.breath_cycle,
            "drift_level": result.drift_level,
            "complexity": result.complexity,
            "agency_A": result.agency_A,
            "warnings": result.warnings,
        }, indent=2))
    else:
        status = "PASS" if result.dignity_passed else "BLOCKED"
        print(f"\n  {'='*52}")
        print(f"  KALAXI PROCESS — {status}")
        print(f"  {'='*52}")
        print(f"  Exchange:     {result.exchange_id}")
        print(f"  Dignity:      {'PASSED' if result.dignity_passed else 'FAILED'}")
        print(f"  Patterns:     {result.patterns_found}")
        print(f"  Drops:        {result.drops_produced}")
        print(f"  Complexity:   {result.complexity}")
        print(f"  Agency A:     {result.agency_A:.3f} (weakest: {result.agency_weakest})")
        print(f"  Drift:        {result.drift_level} (dD/dt={result.drift_rate:.4f})")
        if result.output_text:
            print(f"\n  Output:")
            print(f"    {result.output_text}")
        if result.output_blocked:
            print(f"\n  BLOCKED: {result.block_reason}")
        if result.warnings:
            print(f"\n  Warnings:")
            for w in result.warnings:
                print(f"    - {w}")
        print(f"  {'='*52}\n")


def cmd_state(args):
    """Show full organism state."""
    from WEAVER.organism import Organism

    org = Organism()
    if args.json:
        import dataclasses
        s = org.state()
        print(json.dumps(dataclasses.asdict(s), indent=2, default=str))
    else:
        org.display_state()


def cmd_health(args):
    """Run health dashboard."""
    from SCRIPTS.health_dashboard import main as health_main
    health_main()


def cmd_check(args):
    """Run full system verification."""
    from SCRIPTS.run_full_check import main as check_main
    check_main()


def cmd_face(args):
    """Show steward dashboard."""
    from FACE.face import main as face_main
    face_main()


def cmd_gate(args):
    """Check text against the Sealed Gate."""
    from WEAVER.sealed_gate import sealed_gate

    text = args.text
    if text == "-":
        text = sys.stdin.read().strip()

    result = sealed_gate(text)

    if args.json:
        print(json.dumps(result.audit_object(), indent=2))
    else:
        icon = "PERMITTED" if result.permitted else "REFUSAL_STATE"
        print(f"\n  {'='*52}")
        print(f"  SEALED GATE — {icon}")
        print(f"  {'='*52}")
        if result.triggered_prohibitions:
            for p in result.triggered_prohibitions:
                print(f"    TRIGGERED: {p}")
        if result.signals:
            for s in result.signals:
                print(f"    Signal: {s}")
        receipt = result.refusal_receipt()
        if receipt:
            print(f"    Receipt: {receipt}")
            print(f"    Axi: {result.axi_voice()}")
        if result.permitted:
            print(f"    All three prohibitions clear.")
        print(f"  {'='*52}\n")


def cmd_intake_demo(args):
    """Run the donor intake demo."""
    from WEAVER.intake import demo
    demo()


def cmd_report(args):
    """Generate full system report."""
    from WEAVER.organism import Organism

    org = Organism()
    report = org.full_report()
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print(f"\n  {'='*52}")
        print(f"  KALAXI FULL SYSTEM REPORT")
        print(f"  {'='*52}")
        print(f"  Organism:          {report['organism']}")
        print(f"  Breath cycle:      {report['breath_cycle']}")
        print(f"  Exchanges:         {report['exchanges_processed']}")
        print(f"  Dignity drift:     {report['dignity_drift']}")
        print(f"  Oracle:            {report['oracle']}")
        print(f"  Prevention:        {report['prevention']}")
        print(f"  Mycelium:          {report['mycelium']}")
        print(f"  Emergency:         {report['emergency']}")
        ninth = report['ninth_operator']
        print(f"  Ninth Operator:    {ninth['words_received']} received, {ninth['loop_completions']} loops")
        ew = report['early_warning']
        print(f"  Early warning:     EWMA={'ALERT' if ew['ewma_breached'] else 'ok'}, CUSUM={'ALARM' if ew['cusum_alarm'] else 'ok'}")
        f = report['field']
        print(f"  FIELD:             {f['voices']} voices, {f['donors']} donors, {f['audits']} audits")
        print(f"  {'='*52}\n")


def cmd_serve(args):
    """Start the API server."""
    try:
        import uvicorn
    except ImportError:
        print("ERROR: uvicorn not installed. Run: pip install uvicorn fastapi")
        sys.exit(1)

    print(f"\n  KALAXI API Server starting on port {args.port}...")
    print(f"  Docs at: http://localhost:{args.port}/docs")
    print(f"  Intake at: http://localhost:{args.port}/intake/begin\n")

    uvicorn.run(
        "WEAVER.intake:app",
        host="0.0.0.0",
        port=args.port,
        reload=False,
    )


def cmd_test(args):
    """Run the test suite."""
    import subprocess
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    if args.quick:
        cmd = [sys.executable, "-m", "pytest", "tests/", "-q"]
    result = subprocess.run(cmd, cwd=str(ROOT))
    sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        prog="kalaxi",
        description="KALAXI — Dignity-first constitutional framework",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # process
    p = sub.add_parser("process", help="Process donor input through the organism")
    p.add_argument("text", help="Input text (use '-' for stdin)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_process)

    # state
    p = sub.add_parser("state", help="Show full organism state")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_state)

    # health
    p = sub.add_parser("health", help="Run health dashboard")
    p.set_defaults(func=cmd_health)

    # check
    p = sub.add_parser("check", help="Run full system verification")
    p.set_defaults(func=cmd_check)

    # face
    p = sub.add_parser("face", help="Show steward dashboard")
    p.set_defaults(func=cmd_face)

    # gate
    p = sub.add_parser("gate", help="Check text against Sealed Gate")
    p.add_argument("text", help="Text to check (use '-' for stdin)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_gate)

    # intake-demo
    p = sub.add_parser("intake-demo", help="Run donor intake demo")
    p.set_defaults(func=cmd_intake_demo)

    # report
    p = sub.add_parser("report", help="Generate full system report")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_report)

    # serve
    p = sub.add_parser("serve", help="Start the API server")
    p.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    p.set_defaults(func=cmd_serve)

    # test
    p = sub.add_parser("test", help="Run the test suite")
    p.add_argument("--quick", "-q", action="store_true", help="Quick mode")
    p.set_defaults(func=cmd_test)

    args = parser.parse_args()

    if args.command is None:
        # No command given — show state overview
        print("\n  KALAXI v1.0.0 — Dignity-first constitutional framework")
        print("  ─────────────────────────────────────────────────────")
        print("  Commands:")
        print("    python cli.py process \"text\"    Process donor input")
        print("    python cli.py state             Show organism state")
        print("    python cli.py report            Full system report")
        print("    python cli.py health            Health dashboard")
        print("    python cli.py check             System verification")
        print("    python cli.py face              Steward dashboard")
        print("    python cli.py gate \"text\"        Sealed Gate check")
        print("    python cli.py intake-demo       Donor intake demo")
        print("    python cli.py serve             Start API server")
        print("    python cli.py test              Run test suite")
        print()
        return

    args.func(args)


if __name__ == "__main__":
    main()
