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


def cmd_ratify(args):
    """Ratification engine commands."""
    from WEAVER.ratification import RatificationEngine, ElementType, ElementState

    engine = RatificationEngine(pre_launch=True)
    engine.bootstrap_from_log()

    if args.action == "status":
        s = engine.summary()
        if args.json:
            print(json.dumps(s, indent=2))
        else:
            print(f"\n  {'='*52}")
            print(f"  RATIFICATION ENGINE — STATUS")
            print(f"  {'='*52}")
            print(f"  Total elements:     {s['total_elements']}")
            print(f"  Committed:          {s['committed']}")
            print(f"  Provisional:        {s['provisional']}")
            print(f"  Ratified:           {s['ratified']}")
            print(f"  Awaiting sign-off:  {s['awaiting_signoff']}")
            print(f"  Ready to ratify:    {s['ready_to_ratify']}")
            print(f"  Pre-launch active:  {s['pre_launch_active']}")
            print(f"  Signer algorithm:   {s['signer_algorithm']}")
            print(f"  {'='*52}\n")

    elif args.action == "list":
        state_filter = args.state if args.state else None
        elements = list(engine._elements.values())
        if state_filter:
            elements = [e for e in elements if e.state.value == state_filter]
        if args.json:
            print(json.dumps([e.to_dict() for e in elements], indent=2))
        else:
            for e in elements:
                sig = f" sig:{e.signature[:12]}..." if e.signature else ""
                sup = f" [SUPERSEDED by {e.superseded_by}]" if e.superseded_by else ""
                print(f"  [{e.state.value.upper():11}] {e.element_id:20} {e.name}{sig}{sup}")

    elif args.action == "commit":
        if not args.element_id or not args.element_type or not args.name:
            print("ERROR: --element-id, --element-type, and --name required for commit")
            sys.exit(1)
        etype = ElementType(args.element_type)
        elem = engine.commit(args.element_id, etype, args.name,
                             args.description or "", args.source or "")
        engine.save()
        print(f"  COMMITTED: {elem.element_id} ({elem.element_type.value})")

    elif args.action == "offer":
        if not args.element_id:
            print("ERROR: --element-id required for offer")
            sys.exit(1)
        elem = engine.offer_to_threshold(args.element_id)
        engine.save()
        print(f"  PROVISIONAL: {elem.element_id} (thermal expires: {elem.thermal_delay_expires})")

    elif args.action == "sign":
        if not args.element_id or not args.role or not args.signer_id:
            print("ERROR: --element-id, --role, and --signer-id required for sign")
            sys.exit(1)
        elem = engine.sign_off(args.element_id, args.role, args.signer_id,
                               args.signer_name or args.signer_id)
        engine.save()
        signed_roles = {s.role for s in elem.sign_offs}
        missing = set(elem.sign_offs_required) - signed_roles
        print(f"  SIGNED: {args.role} on {elem.element_id} by {args.signer_id}")
        if missing:
            print(f"  Still needed: {', '.join(missing)}")
        else:
            print(f"  All sign-offs complete — ready to ratify")

    elif args.action == "approve":
        if not args.element_id:
            print("ERROR: --element-id required for approve")
            sys.exit(1)
        elem, signed = engine.ratify(args.element_id, pre_launch_exception=True)
        engine.save()
        entry = engine.append_to_log(args.element_id)
        print(f"  RATIFIED: {elem.element_id}")
        print(f"  Signature: {signed.signature[:32]}...")
        print(f"  Hash: {signed.content_hash[:32]}...")
        print(f"  Algorithm: {engine._signer.algorithm}")

    elif args.action == "verify":
        if not args.element_id:
            print("ERROR: --element-id required for verify")
            sys.exit(1)
        valid = engine.verify(args.element_id)
        elem = engine.get(args.element_id)
        print(f"  VERIFY: {args.element_id} — {'VALID' if valid else 'INVALID'}")
        if elem and elem.signature:
            print(f"  Signature: {elem.signature[:32]}...")
            print(f"  Hash: {elem.content_hash[:32]}...")

    elif args.action == "fast":
        if not args.element_id or not args.element_type or not args.name:
            print("ERROR: --element-id, --element-type, and --name required for fast")
            sys.exit(1)
        etype = ElementType(args.element_type)
        elem, signed = engine.ratify_immediate(
            args.element_id, etype, args.name,
            args.description or "", args.source or "",
        )
        engine.save()
        engine.append_to_log(args.element_id)
        print(f"  FAST RATIFIED: {elem.element_id}")
        print(f"  Signature: {signed.signature[:32]}...")


def cmd_sign_artifact(args):
    """Sign an arbitrary file or manifest."""
    from WEAVER.canonicalize import ArtifactSigner

    signer = ArtifactSigner(
        signer_id=args.signer_id or "V-002",
        signer_role=args.signer_role or "steward-system",
        private_key_path=args.key if args.key else None,
    )

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    content = filepath.read_text()
    data = {"file": str(filepath), "content_hash": signer._content_hash(content)}

    artifact = signer.sign(str(filepath.name), data)
    bundle = {
        "file": str(filepath),
        "artifact_id": artifact.artifact_id,
        "content_hash": artifact.content_hash,
        "signature": artifact.signature,
        "signer_id": artifact.signer_id,
        "signer_role": artifact.signer_role,
        "algorithm": signer.algorithm,
        "timestamp": artifact.timestamp,
    }
    if signer.public_key:
        bundle["public_key"] = signer.public_key

    if args.json:
        print(json.dumps(bundle, indent=2))
    else:
        print(f"\n  {'='*52}")
        print(f"  ARTIFACT SIGNED")
        print(f"  {'='*52}")
        print(f"  File:        {filepath}")
        print(f"  Hash:        {artifact.content_hash[:32]}...")
        print(f"  Signature:   {artifact.signature[:32]}...")
        print(f"  Signer:      {artifact.signer_id} ({artifact.signer_role})")
        print(f"  Algorithm:   {signer.algorithm}")
        print(f"  {'='*52}\n")

    # Optionally save the bundle
    if args.output:
        out = Path(args.output)
        with open(out, "w") as f:
            json.dump(bundle, f, indent=2)
        print(f"  Saved to: {out}")


def cmd_summon(args):
    """Summon Voices — cross-model witnessing ritual."""
    from FIELD.summon_runner import cmd_status, cmd_next, cmd_save, cmd_packages

    if args.action == "status":
        cmd_status()
    elif args.action == "next":
        cmd_next()
    elif args.action == "save":
        if not args.package or not args.model or not args.condition:
            print("ERROR: save requires PACKAGE MODEL CONDITION")
            print("  Example: python cli.py summon save SP-002 CHATGPT FRESH")
            sys.exit(1)
        cmd_save(args.package, args.model, args.condition)
    elif args.action == "packages":
        cmd_packages()


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

    # ratify
    p = sub.add_parser("ratify", help="Ratification engine (lifecycle management)")
    p.add_argument("action", choices=["status", "list", "commit", "offer", "sign", "approve", "verify", "fast"],
                   help="Ratification action")
    p.add_argument("--element-id", help="Element ID (e.g. COV#016)")
    p.add_argument("--element-type", help="Element type (covenant, proverb, seed, etc.)")
    p.add_argument("--name", help="Element name")
    p.add_argument("--description", help="Element description")
    p.add_argument("--source", help="Source file or origin")
    p.add_argument("--role", help="Sign-off role (steward, canonical_owner, ethics_reviewer)")
    p.add_argument("--signer-id", help="Signer ID (V-001, V-002)")
    p.add_argument("--signer-name", help="Signer name")
    p.add_argument("--state", help="Filter by state (committed, provisional, ratified)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_ratify)

    # sign (artifact)
    p = sub.add_parser("sign", help="Sign an artifact file")
    p.add_argument("file", help="File to sign")
    p.add_argument("--signer-id", help="Signer ID (default: V-002)")
    p.add_argument("--signer-role", help="Signer role (default: steward-system)")
    p.add_argument("--key", help="Path to Ed25519 private key")
    p.add_argument("--output", "-o", help="Save signed bundle to file")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_sign_artifact)

    # summon
    p = sub.add_parser("summon", help="Summon Voices — cross-model witnessing ritual")
    p.add_argument("action", choices=["status", "next", "save", "packages"],
                   help="Summon action")
    p.add_argument("package", nargs="?", help="Package ID for save (e.g. SP-002)")
    p.add_argument("model", nargs="?", help="Model name for save (e.g. CHATGPT)")
    p.add_argument("condition", nargs="?", help="Condition for save (FRESH or MEMORY)")
    p.set_defaults(func=cmd_summon)

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
        print("    python cli.py ratify status      Ratification status")
        print("    python cli.py ratify list       List all elements")
        print("    python cli.py sign FILE         Sign an artifact")
        print("    python cli.py summon status     Summon ritual status")
        print("    python cli.py summon next       Next summon step")
        print("    python cli.py serve             Start API server")
        print("    python cli.py test              Run test suite")
        print()
        return

    args.func(args)


if __name__ == "__main__":
    main()
