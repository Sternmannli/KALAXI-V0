#!/usr/bin/env python3
"""
Kalaxi Integration Example
Shows how to use all three tools together in a real workflow
"""

import sys
import json
from datetime import datetime

sys.path.insert(0, '.')
from dignity_check import check_dignity
from gap004_mediator import check_and_surface, surface_conflict
from canon_integrity import CanonIntegrityScanner

def evaluate_proposal(proposal_text: str, proposal_id: str = None) -> dict:
    print("="*70)
    print(f"KALAXI EVALUATION: {proposal_id or 'UNNAMED_PROPOSAL'}")
    print("="*70)
    print(f"Text: {proposal_text[:100]}...")
    print()

    print("Step 1: Running dignity check and GAP#004 scan...")
    result = check_and_surface(proposal_text)

    findings = {
        "proposal_id": proposal_id or f"PROP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "proposal_text": proposal_text,
        "dignity": {"passed": result['dignity_passed'], "score": result['D_score']},
        "gap004": {"detected": result['gap004_detected']},
        "recommendations": [],
        "blockers": []
    }

    if not result['dignity_passed']:
        findings["blockers"].append("DIGNITY_VIOLATION")
        findings["recommendations"].append(
            "BLOCK: Proposal violates dignity predicate. "
            "Review audit object and apply remedies before resubmission."
        )
        print("❌ DIGNITY VIOLATION DETECTED")
        print(json.dumps(result['dignity_audit'], indent=2))
    else:
        print("✅ Dignity check passed")

    if result['gap004_detected']:
        findings["blockers"].append("GAP004_TENSION")
        findings["recommendations"].append(
            "ESCALATE: Individual vs collective tension detected. "
            "Generate conflict ticket and route to steward review. "
            "Do not auto-resolve."
        )
        print("⚠️  GAP#004 TENSION DETECTED")
        ticket = result['gap004_ticket']
        print(f"   Severity: {ticket['severity']}")
        print(f"   Questions: {len(ticket['steward_questions'])} generated")
    else:
        print("✅ No GAP#004 tension detected")

    findings["status"] = "BLOCKED" if findings["blockers"] else "APPROVED_FOR_RATIFICATION"
    findings["next_action"] = "Steward review required" if findings["blockers"] else "Proceed to thermal delay (90-day cooling)"

    print()
    print("="*70)
    print(f"FINAL STATUS: {findings['status']}")
    print(f"Next Action: {findings['next_action']}")
    print("="*70)
    return findings

def periodic_integrity_check():
    print("\n" + "="*70)
    print("PERIODIC CANON INTEGRITY SCAN")
    print("="*70)
    scanner = CanonIntegrityScanner()
    scanner.run()
    report = scanner.to_dict()
    critical = sum(1 for f in report['findings'] if f['severity'] == 'CRITICAL')
    high = sum(1 for f in report['findings'] if f['severity'] == 'HIGH')
    if critical:
        print(f"\n🚨 CRITICAL FINDINGS: {critical}")
        print("CANON INTEGRITY COMPROMISED - IMMEDIATE STEWARD ACTION REQUIRED")
        return False
    elif high:
        print(f"\n⚠️  HIGH SEVERITY FINDINGS: {high}")
        print("Review required before next ratification")
        return True
    else:
        print("\n✅ Canon integrity maintained")
        return True

def main():
    print("\n" + "="*70)
    print("SCENARIO 1: Policy Change Proposal")
    print("="*70)
    proposal1 = """
    All community members must share their contact information with every
    other member to ensure transparency. This is mandatory and non-negotiable
    for the collective good.
    """
    r1 = evaluate_proposal(proposal1, "POLICY-2026-001")

    print("\n\n" + "="*70)
    print("SCENARIO 2: Revised Policy (Dignity-First)")
    print("="*70)
    proposal2 = """
    We invite community members to optionally share contact information
    with others who have similar interests. You can choose your comfort level,
    and change your mind at any time. What works best for you?
    """
    r2 = evaluate_proposal(proposal2, "POLICY-2026-001-REVISED")

    print("\n\n")
    ok = periodic_integrity_check()

    print("\n\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Proposal 1: {r1['status']} ({len(r1['blockers'])} blockers)")
    print(f"Proposal 2: {r2['status']} ({len(r2['blockers'])} blockers)")
    print(f"Canon Integrity: {'OK' if ok else 'COMPROMISED'}")

    all_results = {"scenarios": [r1, r2], "integrity_ok": ok, "export_timestamp": datetime.now().isoformat()}
    with open('evaluation_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    print("\nResults exported to: evaluation_results.json")

if __name__ == "__main__":
    main()
