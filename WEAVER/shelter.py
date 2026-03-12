#!/usr/bin/env python3
"""
shelter.py — GAP#VICTIM-PROTECTION-001: Dignity Shelter Path
Version: 1.0
Grounded in: COV#008 (shelter path), COV#002 (silence is not closure)

When dignity fails, the system must not just block — it must offer a way back.
The shelter is where blocked exchanges go to be held, not discarded.

Principles:
  - A blocked exchange is not a rejected person
  - Every dignity failure gets a remedy suggestion
  - The donor can always retry, rephrase, or withdraw
  - Nothing is silently dropped (COV#002)
  - The steward can review sheltered exchanges

Flow:
  1. Dignity check fails (D=0.0)
  2. Exchange is sheltered (not discarded)
  3. Remedy is generated based on which component(s) failed
  4. Donor receives: what happened, why, and what they can do
  5. Steward can review sheltered exchanges
  6. Donor can retry with rephrased input
  7. If retry passes, original shelter record is linked

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict
from enum import Enum


class ShelterStatus(Enum):
    """Status of a sheltered exchange."""
    HELD = "held"               # Waiting for donor action or steward review
    RETRIED = "retried"         # Donor retried with new input
    WITHDRAWN = "withdrawn"     # Donor chose to withdraw
    REVIEWED = "reviewed"       # Steward reviewed and made a decision
    RESOLVED = "resolved"       # Dignity restored through retry or steward action


@dataclass
class Remedy:
    """A suggested remedy for a dignity failure."""
    component: str              # Which component failed: A, L, or M
    label: str                  # Human-readable label
    suggestion: str             # What the donor can do
    example: str                # Example of a rephrased input


# Remedy templates based on which dignity component failed
REMEDY_TEMPLATES = {
    "A": Remedy(
        component="A",
        label="Agency",
        suggestion=(
            "The input contained coercive language that removes choice. "
            "Try rephrasing without commands or ultimatums. "
            "The system preserves the donor's right to choose."
        ),
        example=(
            "Instead of 'You must do X', try 'I would like to explore X' "
            "or 'Could we consider X?'"
        ),
    ),
    "L": Remedy(
        component="L",
        label="Legibility",
        suggestion=(
            "The input dismissed or ignored the donor's frame of reference. "
            "Try rephrasing to acknowledge what was said. "
            "The system reflects, it does not dismiss."
        ),
        example=(
            "Instead of 'That's not relevant', try 'I hear what you said, "
            "and I'd like to add...' or 'Building on that thought...'"
        ),
    ),
    "M": Remedy(
        component="M",
        label="Moral Standing",
        suggestion=(
            "The input contained language that reduces a person to an error "
            "or mocks their understanding. Try rephrasing with respect. "
            "Every donor is a person, not a problem to solve."
        ),
        example=(
            "Instead of 'You failed' or 'Obviously you should...', try "
            "'Let me help clarify...' or 'Here is another way to look at it...'"
        ),
    ),
}


@dataclass
class ShelterRecord:
    """A record of a sheltered (blocked) exchange."""
    exchange_id: str
    input_text: str             # Original input (truncated for privacy)
    failed_components: List[str]
    remedies: List[Remedy]
    donor_message: str          # What we tell the donor
    status: ShelterStatus
    sheltered_at: str
    retry_exchange_id: Optional[str] = None
    steward_note: Optional[str] = None
    resolved_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "exchange_id": self.exchange_id,
            "input_summary": self.input_text[:80],
            "failed_components": self.failed_components,
            "remedies": [
                {"component": r.component, "label": r.label, "suggestion": r.suggestion}
                for r in self.remedies
            ],
            "donor_message": self.donor_message,
            "status": self.status.value,
            "sheltered_at": self.sheltered_at,
            "retry_exchange_id": self.retry_exchange_id,
            "steward_note": self.steward_note,
            "resolved_at": self.resolved_at,
        }


class Shelter:
    """
    The Dignity Shelter. Holds blocked exchanges with care.

    Usage:
        shelter = Shelter()
        record = shelter.receive(exchange_id, input_text, failed_components)
        # record.donor_message tells the donor what happened and what to do
        # record.remedies gives specific suggestions

        # Later, donor retries:
        shelter.mark_retried(exchange_id, new_exchange_id)

        # Or steward reviews:
        shelter.steward_review(exchange_id, "Approved after context review")
    """

    def __init__(self):
        self._records: Dict[str, ShelterRecord] = {}

    def receive(self, exchange_id: str, input_text: str, failed_components: List[str]) -> ShelterRecord:
        """
        Shelter a blocked exchange. Generate remedies and donor message.

        Args:
            exchange_id: The exchange that was blocked
            input_text: The original donor input
            failed_components: List of failed component names ("A", "L", "M")

        Returns:
            ShelterRecord with remedies and donor-facing message
        """
        # Generate remedies for each failed component
        remedies = []
        for comp in failed_components:
            if comp in REMEDY_TEMPLATES:
                remedies.append(REMEDY_TEMPLATES[comp])

        # Build donor-facing message
        donor_message = self._build_donor_message(failed_components, remedies)

        record = ShelterRecord(
            exchange_id=exchange_id,
            input_text=input_text[:200],  # Truncate for privacy
            failed_components=failed_components,
            remedies=remedies,
            donor_message=donor_message,
            status=ShelterStatus.HELD,
            sheltered_at=datetime.now(timezone.utc).isoformat(),
        )

        self._records[exchange_id] = record
        return record

    def _build_donor_message(self, failed_components: List[str], remedies: List[Remedy]) -> str:
        """Build a respectful, clear message for the donor."""
        parts = [
            "Your exchange has been held — not rejected, held.",
            "The system detected a dignity concern and paused to protect everyone involved.",
        ]

        if len(failed_components) == 1:
            r = remedies[0] if remedies else None
            if r:
                parts.append(f"Specifically: {r.suggestion}")
                parts.append(f"Suggestion: {r.example}")
        else:
            parts.append("Multiple dignity components were affected:")
            for r in remedies:
                parts.append(f"  - {r.label}: {r.suggestion}")

        parts.append(
            "You can: (1) rephrase and try again, "
            "(2) withdraw this exchange, or "
            "(3) wait for steward review."
        )
        parts.append("Your voice matters. The system waits for you.")

        return " ".join(parts)

    def mark_retried(self, exchange_id: str, retry_exchange_id: str) -> Optional[ShelterRecord]:
        """Mark a sheltered exchange as retried with new input."""
        record = self._records.get(exchange_id)
        if record is None:
            return None
        record.status = ShelterStatus.RETRIED
        record.retry_exchange_id = retry_exchange_id
        record.resolved_at = datetime.now(timezone.utc).isoformat()
        return record

    def mark_withdrawn(self, exchange_id: str) -> Optional[ShelterRecord]:
        """Mark a sheltered exchange as withdrawn by the donor."""
        record = self._records.get(exchange_id)
        if record is None:
            return None
        record.status = ShelterStatus.WITHDRAWN
        record.resolved_at = datetime.now(timezone.utc).isoformat()
        return record

    def steward_review(self, exchange_id: str, note: str) -> Optional[ShelterRecord]:
        """Steward reviews a sheltered exchange."""
        if not note:
            raise ValueError("Steward review requires a note (COV#002: silence is not closure)")
        record = self._records.get(exchange_id)
        if record is None:
            return None
        record.status = ShelterStatus.REVIEWED
        record.steward_note = note
        record.resolved_at = datetime.now(timezone.utc).isoformat()
        return record

    def resolve(self, exchange_id: str) -> Optional[ShelterRecord]:
        """Mark a sheltered exchange as fully resolved."""
        record = self._records.get(exchange_id)
        if record is None:
            return None
        record.status = ShelterStatus.RESOLVED
        if not record.resolved_at:
            record.resolved_at = datetime.now(timezone.utc).isoformat()
        return record

    def get(self, exchange_id: str) -> Optional[ShelterRecord]:
        """Retrieve a shelter record."""
        return self._records.get(exchange_id)

    def list_held(self) -> List[ShelterRecord]:
        """List all exchanges currently held in shelter."""
        return [r for r in self._records.values() if r.status == ShelterStatus.HELD]

    def list_all(self) -> List[ShelterRecord]:
        """List all shelter records."""
        return list(self._records.values())

    @property
    def held_count(self) -> int:
        return len(self.list_held())

    @property
    def total_count(self) -> int:
        return len(self._records)
