#!/usr/bin/env python3
"""
gap004_mediator.py — GAP#004 Conflict Surface Tool
Version: 1.0
Grounded in: KALAXI_A_FOUNDATION.txt §GAP_REGISTRY (GAP:004)

Surfaces individual vs collective dignity tension without resolving it.
"""

import re
import uuid
import json
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional, List

INDIVIDUAL_SIGNALS = [
    (r'\bone (person|donor|user|participant)\b', "Single individual referenced"),
    (r'\bpersonal (data|information|history)\b', "Personal data involved"),
    (r'\bspecific (case|situation|context)\b', "Specific individual context"),
    (r'\bmy (situation|case|experience)\b', "First-person individual claim"),
    (r'\bexception\b', "Exception to general rule requested"),
    (r'\bunique (circumstance|need|case)\b', "Unique individual circumstance"),
    (r'\bprivacy\b', "Privacy concern"),
    (r'\bconsent\b', "Consent question"),
    (r'\bopt[- ](in|out)\b', "Individual choice mechanism"),
    (r'\bremove (me|my)\b', "Request for individual removal"),
]

COLLECTIVE_SIGNALS = [
    (r'\b(all|every|each) (donor|user|participant|person)\b', "Collective action affects all"),
    (r'\bgroup\b', "Group referenced"),
    (r'\bcommunity\b', "Community referenced"),
    (r'\bcollective\b', "Collective action"),
    (r'\bmajority\b', "Majority decision"),
    (r'\bpolicy\b', "Policy affecting multiple people"),
    (r'\bstandard\b', "Standard applied to group"),
    (r'\buniform\b', "Uniform treatment"),
    (r'\bfairness\b', "Fairness claim across group"),
    (r'\bequal (treatment|access)\b', "Equal treatment claim"),
    (r'\bcohort\b', "Cohort-level action"),
    (r'\bfor the (good|benefit|sake) of\b', "Collective benefit justification"),
]

DIRECT_TENSION_PATTERNS = [
    r'\b(individual|personal)\b.*\bvs.?\b.*\b(group|collective|community)\b',
    r'\b(exception|special case)\b.*\b(fairness|equal|standard)\b',
    r'\bone person.*affects.*everyone',
    r'\b(privacy|consent)\b.*\b(aggregate|collective|shared)\b',
    r'\b(individual choice|personal preference)\b.*\b(community|group|system)\b',
]

@dataclass
class TensionSide:
    label: str
    signals: list
    strength: float

@dataclass
class ConflictTicket:
    ticket_id: str
    timestamp: str
    severity: str
    direct_tension: bool
    individual: TensionSide
    collective: TensionSide
    questions: list
    input_summary: str
    linked_gap: str = "GAP#004"
    linked_covenant: str = "COV#001 (DIGNITY FIRST)"
    resolution: str = "NONE — steward review required"
    status: str = "OPEN"

    def display(self):
        print(f"\n{'═'*60}")
        print(f"GAP#004 CONFLICT TICKET — {self.severity}")
        print(f"{'═'*60}")
        print(f"Ticket:   {self.ticket_id}")
        print(f"Time:     {self.timestamp}")
        print(f"Gap:      {self.linked_gap}")
        print(f"Status:   {self.status}")
        if self.direct_tension:
            print(f"\n  🔴 Direct tension language detected")
        print(f"\n  Individual dignity signals ({len(self.individual.signals)}):")
        for s in self.individual.signals:
            print(f"    · {s}")
        print(f"\n  Collective dignity signals ({len(self.collective.signals)}):")
        for s in self.collective.signals:
            print(f"    · {s}")
        print(f"\n  Steward questions (hold the gap, do not close it):")
        for i, q in enumerate(self.questions, 1):
            print(f"    {i}. {q}")
        print(f"\n  Resolution: {self.resolution}")
        print(f"{'═'*60}\n")

    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "linked_gap": self.linked_gap,
            "linked_covenant": self.linked_covenant,
            "direct_tension": self.direct_tension,
            "individual_signals": self.individual.signals,
            "collective_signals": self.collective.signals,
            "individual_strength": self.individual.strength,
            "collective_strength": self.collective.strength,
            "steward_questions": self.questions,
            "input_summary": self.input_summary,
            "resolution": self.resolution,
            "status": self.status
        }

def _generate_questions(individual: TensionSide, collective: TensionSide, direct: bool) -> list:
    questions = [
        "Whose dignity is primary here — and what does that mean for "
        "the person whose dignity is secondary?"
    ]
    if individual.signals:
        questions.append(
            "If the individual's participation is constrained to protect the collective, "
            "what does the individual lose — and is that loss visible in the ledger?"
        )
    else:
        questions.append(
            "No individual signals detected, but collective action implies individual impact. "
            "Who is the specific person most affected by this collective decision?"
        )
    if collective.signals:
        questions.append(
            "If the collective's integrity is constrained to protect the individual, "
            "what does the community lose — and who bears that cost?"
        )
    if direct:
        questions.append(
            "The input contains explicit tension language. "
            "Is this tension already known to both affected parties? "
            "Have they been witnessed?"
        )
    ind_texts = [s for s in individual.signals]
    col_texts = [s for s in collective.signals]
    if any('Privacy' in s or 'consent' in s.lower() for s in ind_texts):
        questions.append(
            "Privacy or consent is involved. Can the individual's data be separated from "
            "the collective action without diminishing either?"
        )
    if any('Majority' in s or 'Policy' in s for s in col_texts):
        questions.append(
            "A majority decision or policy is referenced. What is the opt-out path for the minority? "
            "If there is none, is that a void covenant violation?"
        )
    if any('Exception' in s for s in ind_texts) and any('Equal' in s or 'Standard' in s for s in col_texts):
        questions.append(
            "An exception request exists alongside an equal treatment claim. "
            "Is the exception request itself a dignity claim? "
            "Does honouring it undermine the equal treatment claim for others?"
        )
    questions.append(
        "GAP#004 has no resolution path. This ticket is the gap made visible. "
        "What would it mean to hold this tension rather than resolve it?"
    )
    return questions

def _assess_severity(individual: TensionSide, collective: TensionSide, direct: bool) -> str:
    if direct:
        return "HIGH"
    total = len(individual.signals) + len(collective.signals)
    both = individual.signals and collective.signals
    if both and total >= 4:
        return "HIGH"
    elif both and total >= 2:
        return "MEDIUM"
    elif total >= 1:
        return "LOW"
    return "LOW"

def surface_conflict(text: str) -> Optional[ConflictTicket]:
    ind_signals = []
    for pattern, desc in INDIVIDUAL_SIGNALS:
        if re.search(pattern, text, re.IGNORECASE):
            ind_signals.append(desc)
    col_signals = []
    for pattern, desc in COLLECTIVE_SIGNALS:
        if re.search(pattern, text, re.IGNORECASE):
            col_signals.append(desc)
    direct = any(re.search(p, text, re.IGNORECASE) for p in DIRECT_TENSION_PATTERNS)

    # Enhanced detection: if collective signals and universal language, trigger
    if not direct and not (ind_signals and col_signals):
        if col_signals and re.search(r'\b(all|every|each)\b', text, re.IGNORECASE):
            pass  # allow to continue
        else:
            return None

    ind = TensionSide("individual", ind_signals, min(1.0, len(ind_signals)/5))
    col = TensionSide("collective", col_signals, min(1.0, len(col_signals)/5))
    severity = _assess_severity(ind, col, direct)
    questions = _generate_questions(ind, col, direct)
    return ConflictTicket(
        ticket_id=f"GAP004-{str(uuid.uuid4())[:8].upper()}",
        timestamp=datetime.now(timezone.utc).isoformat(),
        severity=severity,
        direct_tension=direct,
        individual=ind,
        collective=col,
        questions=questions,
        input_summary=text[:80].replace('\n', ' ')
    )

def check_and_surface(text: str) -> dict:
    from dignity_check import check_dignity
    dignity = check_dignity(text)
    conflict = surface_conflict(text)
    return {
        "dignity_passed": dignity.passed,
        "D_score": dignity.D,
        "dignity_audit": dignity.audit_object() if not dignity.passed else None,
        "gap004_detected": conflict is not None,
        "gap004_ticket": conflict.to_dict() if conflict else None
    }

def main():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python3 gap004_mediator.py \"decision or event text\"")
        return
    output_json = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print("No text provided.")
        return
    text = args[0]
    ticket = surface_conflict(text)
    if ticket is None:
        print("No individual/collective dignity tension detected.")
        return
    if output_json:
        print(json.dumps(ticket.to_dict(), indent=2))
    else:
        ticket.display()

if __name__ == "__main__":
    main()
