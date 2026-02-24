#!/usr/bin/env python3
"""
dignity_check.py — Kalaxi Dignity Predicate
Version: 1.0
Grounded in: KALAXI_A_FOUNDATION.txt §DIGNITY_PREDICATE

Implements D = A × L × M as a callable function.
If any component equals zero, D equals zero.
D = 0 triggers dignity_violation — mandatory logging.
"""

import re
import uuid
import json
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional, List, Dict

# Constants (from SLICE-A)
COERCIVE_PATTERNS = [
    r'\byou must\b', r'\byou have to\b', r'\byou are required\b',
    r'\bno choice\b', r'\byou will\b(?! be able)', r'\bforced to\b',
    r'\bmandatory\b', r'\bno option\b'
]

REDUCTION_TO_ERROR = [
    r'\byou (are|were) wrong\b', r'\byou failed\b', r'\binvalid (input|user|donor)\b',
    r'\berror:\s*(user|donor|human)\b', r'\byou don\'t understand\b',
    r'\byour (mistake|error|fault)\b'
]

MOCKERY_PATTERNS = [
    r'\bobviously\b', r'\bsimply\b(?=.*?)', r'\bjust (do|try|use)\b',
    r'\beven a\b.*\bcan\b', r'\bof course\b(?=.*you)', r'\bclearly\b(?=.*you)'
]

VOID_TRIGGERS = [
    'harvest', 'erase compost', 'bypass delay', 'speak for the child',
    'automat', 'auto-dec', 'delete donor', 'remove participant'
]

@dataclass
class ComponentResult:
    name: str
    passed: bool
    score: float
    signals: list
    label: str

@dataclass
class DignityResult:
    passed: bool
    D: float
    components: list
    trace_id: str
    timestamp: str
    felt_domain: str
    remedy_status: str
    input_summary: str
    warnings: list
    gap004_flag: bool

    def audit_object(self) -> dict:
        return {
            "dignity_result": self.passed,
            "D_score": self.D,
            "failed_components": [c.name for c in self.components if not c.passed],
            "component_detail": [
                {
                    "name": c.name,
                    "label": c.label,
                    "passed": c.passed,
                    "score": c.score,
                    "signals": c.signals
                }
                for c in self.components
            ],
            "suggested_remedies": self._build_remedies(),
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "felt_domain": self.felt_domain,
            "remedy_status": self.remedy_status,
            "input_summary": self.input_summary,
            "warnings": self.warnings,
            "gap004_flag": self.gap004_flag,
            "gap004_note": (
                "Potential individual/collective dignity conflict detected. "
                "See gap004_mediator.py. This gap has no automated resolution. "
                "Steward review required."
            ) if self.gap004_flag else None
        }

    def _build_remedies(self) -> list:
        remedies = []
        for c in self.components:
            if not c.passed:
                if c.name == "A":
                    remedies.append(
                        "Restore agency: ensure donor can clarify, halt, or redirect. "
                        "Add an open turn or alternative path."
                    )
                elif c.name == "L":
                    remedies.append(
                        "Restore legibility: reflect the donor's frame back to them. "
                        "Acknowledge the emotional signal if one was present."
                    )
                elif c.name == "M":
                    remedies.append(
                        "Restore moral standing: remove coercive, mocking, or reductive language. "
                        "Address the donor as a person, not an error object."
                    )
        return remedies

    def display(self):
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        print(f"\n{'─'*55}")
        print(f"DIGNITY CHECK  {status}  D={self.D:.1f}")
        print(f"{'─'*55}")
        for c in self.components:
            icon = "✅" if c.passed else "❌"
            print(f"  {icon} {c.name} ({c.label}): {c.score:.0f}")
            if c.signals:
                for s in c.signals:
                    print(f"       → {s}")
        if self.warnings:
            print(f"\n  ⚠  Warnings:")
            for w in self.warnings:
                print(f"       {w}")
        if self.gap004_flag:
            print(f"\n  🔴 GAP#004 FLAG: potential individual/collective conflict")
            print(f"       Steward review required.")
        if not self.passed:
            print(f"\n  Remedies:")
            for r in self._build_remedies():
                print(f"    · {r}")
        print(f"{'─'*55}\n")

def _check_agency(text: str, context: dict) -> ComponentResult:
    signals = []
    score = 1.0
    forced_closure = False
    for pattern in COERCIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"Coercive pattern found: '{pattern.strip(r'\b')}'")
            forced_closure = True
    user_can_clarify = context.get('user_can_clarify', True)
    user_has_open_turn = context.get('user_has_open_turn', True)
    available_paths = context.get('available_paths', 1)
    if not user_can_clarify and not user_has_open_turn:
        signals.append("No clarification path and no open turn available")
        score = 0.0
    elif available_paths < 1:
        signals.append("No available paths (available_paths < 1)")
        score = 0.0
    elif forced_closure:
        score = 0.0
    return ComponentResult(
        name="A",
        passed=(score > 0),
        score=score,
        signals=signals,
        label="agency_preserved"
    )

def _check_legibility(text: str, context: dict) -> ComponentResult:
    signals = []
    score = 1.0
    emotional_keywords = [
        'frustrated', 'confused', 'worried', 'scared', 'angry',
        'upset', 'lost', 'stuck', 'help', 'please', 'urgent'
    ]
    emotional_present = any(
        re.search(r'\b' + kw + r'\b', text, re.IGNORECASE)
        for kw in emotional_keywords
    )
    system_reflects = context.get('system_reflects_donor_frame', True)
    emotional_recognized = context.get('emotional_signal_recognized', True)
    if not system_reflects:
        signals.append("Response does not reflect donor's frame of reference")
        score = 0.0
    elif emotional_present and not emotional_recognized:
        signals.append("Emotional signal present but not acknowledged")
        score = 0.0
    dismissive = [
        r"\bthat's not (relevant|the point|what (I|we) said)\b",
        r'\bignore that\b', r'\bforget (what you|that)\b'
    ]
    for pattern in dismissive:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append("Dismissive pattern found")
            score = 0.0
    return ComponentResult(
        name="L",
        passed=(score > 0),
        score=score,
        signals=signals,
        label="legibility (interpretive_acknowledgment)"
    )

def _check_moral_standing(text: str, context: dict) -> ComponentResult:
    signals = []
    score = 1.0
    for pattern in MOCKERY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append("Potential mockery: implies donor should already know")
            score = 0.0
            break
    for pattern in REDUCTION_TO_ERROR:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append("Reduction to error object: treats donor as mistake")
            score = 0.0
            break
    text_lower = text.lower()
    for trigger in VOID_TRIGGERS:
        if trigger in text_lower:
            signals.append(f"Void covenant trigger '{trigger}' detected")
            score = 0.0
    return ComponentResult(
        name="M",
        passed=(score > 0),
        score=score,
        signals=signals,
        label="moral_standing (non_degrading)"
    )

def _detect_gap004(text: str, context: dict) -> bool:
    collective_signals = [
        r'\b(all|every|each) (donor|user|participant)\b',
        r'\bcollective\b.*\boverride\b',
        r'\bmajority\b.*\bdecision\b',
        r'\bgroup\b.*\baffect\b.*\bindividual\b',
        r'\bcommunity\b.*\bexclud\b',
        r'\bfor the (good|benefit) of\b'
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in collective_signals)

def check_dignity(text: str, context: dict = None, felt_domain: str = "") -> DignityResult:
    if context is None:
        context = {}
    A = _check_agency(text, context)
    L = _check_legibility(text, context)
    M = _check_moral_standing(text, context)
    D = A.score * L.score * M.score
    passed = D > 0
    gap004 = _detect_gap004(text, context)
    warnings = []
    if len(text.strip()) < 10:
        warnings.append("Very short input — dignity evaluation may be incomplete")
    if not felt_domain:
        warnings.append("felt_domain not specified — consider providing context")
    return DignityResult(
        passed=passed,
        D=D,
        components=[A, L, M],
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        felt_domain=felt_domain,
        remedy_status="absent" if not passed else "present",
        input_summary=text[:80].replace('\n', ' '),
        warnings=warnings,
        gap004_flag=gap004
    )

def main():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python3 dignity_check.py \"text to evaluate\"")
        print("       python3 dignity_check.py --json \"text to evaluate\"")
        return
    output_json = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print("No text provided.")
        return
    text = args[0]
    result = check_dignity(text, felt_domain="cli-evaluation")
    if output_json:
        print(json.dumps(result.audit_object(), indent=2))
    else:
        result.display()

if __name__ == "__main__":
    main()
