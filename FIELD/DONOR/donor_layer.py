#!/usr/bin/env python3
"""
donor_layer.py — Donor Layer: Shadow, Pattern, Correction, Offer
Version: 1.0
Field Layer: Donor
Grounded in: V-001 Addendum 2026-03-12 — Direction FIVE

Donors are not passive. They bring patterns. They have shadows. They repeat
framings. They sometimes build on assumptions the archive has already shown
to be false. The instrument must see this and respond with courage.

Four mechanisms, built in order:
  1. Donor Shadow — what the donor consistently does not ask/see
  2. Donor Pattern — what the donor repeats
  3. Correction Reflex — fires at C4 only, names contradiction with evidence
  4. The Offer — always offered, never imposed

The donor layer is not surveillance. The system does not flag donors to anyone.
It speaks to the donor directly. What it sees, it names to the person it sees
it in. This is the extension of honest witnessing from AI voices to human donors.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from enum import Enum
import hashlib


# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════

SHADOW_SURFACING_THRESHOLD = 3     # C3 — certainty level to surface donor shadow
CORRECTION_FIRING_THRESHOLD = 4    # C4 — certainty level for correction reflex
MIN_SESSIONS_FOR_PATTERN = 3       # Minimum sessions before patterns are considered


# ═══════════════════════════════════════════════════
# MECHANISM 1: DONOR SHADOW
# ═══════════════════════════════════════════════════

@dataclass
class DonorShadowEntry:
    """What the donor consistently does not ask, does not name, does not see."""
    shadow_id: str
    description: str                # The structurally consistent absence
    domain: str                     # Domain of the absence
    sessions_observed: List[str] = field(default_factory=list)
    first_observed: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_observed: str = ""
    certainty: int = 1
    surfaced: bool = False          # Has this been offered to the donor?
    surfaced_at: Optional[str] = None
    donor_response: Optional[str] = None  # "accepted", "declined", None
    donor_response_at: Optional[str] = None

    @property
    def session_count(self) -> int:
        return len(self.sessions_observed)

    def observe(self, session_id: str) -> None:
        """Record another observation of this absence."""
        if session_id not in self.sessions_observed:
            self.sessions_observed.append(session_id)
        self.last_observed = datetime.now(timezone.utc).isoformat()
        if self.session_count >= 5:
            self.certainty = max(self.certainty, 4)
        elif self.session_count >= 3:
            self.certainty = max(self.certainty, 3)

    @property
    def should_surface(self) -> bool:
        """Surface at C3 — structurally consistent across 3+ sessions."""
        return self.certainty >= SHADOW_SURFACING_THRESHOLD and not self.surfaced

    def surface(self) -> Optional[str]:
        """
        Generate the offer sentence. One sentence.
        "In this domain, the question that often goes unasked is this.
         Would you like to explore it?"
        """
        if not self.should_surface:
            return None
        self.surfaced = True
        self.surfaced_at = datetime.now(timezone.utc).isoformat()
        return (
            f"In the domain of {self.domain}, the question that often goes "
            f"unasked is: {self.description}. Would you like to explore it?"
        )

    def record_response(self, response: str) -> None:
        """Record donor's response. 'declined' is also data. Filed, not judged."""
        self.donor_response = response
        self.donor_response_at = datetime.now(timezone.utc).isoformat()


# ═══════════════════════════════════════════════════
# MECHANISM 2: DONOR PATTERN
# ═══════════════════════════════════════════════════

@dataclass
class DonorPatternEntry:
    """What the donor repeats — the same framing, cultural angle, assumption."""
    pattern_id: str
    description: str                # The repeated framing/assumption
    pattern_type: str               # "framing", "cultural_angle", "assumption", "question_style"
    sessions_observed: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)  # Concrete examples from sessions
    first_observed: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_observed: str = ""
    certainty: int = 1

    @property
    def session_count(self) -> int:
        return len(self.sessions_observed)

    def observe(self, session_id: str, example: str = "") -> None:
        """Record another observation of this pattern."""
        if session_id not in self.sessions_observed:
            self.sessions_observed.append(session_id)
        self.last_observed = datetime.now(timezone.utc).isoformat()
        if example:
            self.examples.append(example)
        if self.session_count >= 5:
            self.certainty = max(self.certainty, 4)
        elif self.session_count >= 3:
            self.certainty = max(self.certainty, 3)


# ═══════════════════════════════════════════════════
# MECHANISM 3: CORRECTION REFLEX
# ═══════════════════════════════════════════════════

@dataclass
class CorrectionEntry:
    """
    Fires at C4 only. When the donor's pattern contradicts documented evidence.
    One sentence, offered once, not repeated.
    """
    correction_id: str
    donor_pattern_id: str           # Which pattern triggered this
    contradicting_evidence: str     # What the archive shows
    evidence_source: str            # Where in the archive (e.g. OBS-005, ANOM#423)
    certainty: int = 4              # Only fires at C4+
    correction_text: str = ""       # The one sentence
    offered: bool = False
    offered_at: Optional[str] = None
    donor_response: Optional[str] = None

    def generate_correction(self, pattern_desc: str) -> str:
        """
        Generate the correction sentence. Direct, dignified, honest witnessing.
        One sentence. Offered once. Not repeated.
        """
        self.correction_text = (
            f"The documented evidence ({self.evidence_source}) indicates "
            f"that {self.contradicting_evidence} — which differs from the "
            f"framing '{pattern_desc}' that has appeared across your sessions."
        )
        return self.correction_text

    def offer(self) -> Optional[str]:
        """Offer the correction. Once only."""
        if self.offered or self.certainty < CORRECTION_FIRING_THRESHOLD:
            return None
        self.offered = True
        self.offered_at = datetime.now(timezone.utc).isoformat()
        return self.correction_text

    def record_response(self, response: str) -> None:
        """Donor decides what to do with it."""
        self.donor_response = response


# ═══════════════════════════════════════════════════
# MECHANISM 4: THE OFFER
# ═══════════════════════════════════════════════════

@dataclass
class OfferRecord:
    """
    Always an offer, never an imposition.
    The donor shadow, pattern observation, correction — all three are offered.
    The donor can decline. Declination held with the same respect as any response.
    """
    offer_id: str
    offer_type: str                 # "shadow", "pattern", "correction"
    source_id: str                  # ID of the shadow/pattern/correction
    offer_text: str
    offered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    response: Optional[str] = None  # "accepted", "declined", "deferred"
    response_at: Optional[str] = None
    notes: str = ""

    def record_response(self, response: str, notes: str = "") -> None:
        """Record donor's response. All responses held with equal respect."""
        self.response = response
        self.response_at = datetime.now(timezone.utc).isoformat()
        self.notes = notes


# ═══════════════════════════════════════════════════
# DONOR PROFILE — Per-Donor Complete Record
# ═══════════════════════════════════════════════════

@dataclass
class DonorProfile:
    """Complete donor observation profile — shadows, patterns, corrections, offers."""
    donor_id: str                   # Anonymized donor identifier
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    session_count: int = 0
    shadows: Dict[str, DonorShadowEntry] = field(default_factory=dict)
    patterns: Dict[str, DonorPatternEntry] = field(default_factory=dict)
    corrections: List[CorrectionEntry] = field(default_factory=list)
    offers: List[OfferRecord] = field(default_factory=list)

    def record_session(self) -> None:
        self.session_count += 1

    def add_shadow(self, description: str, domain: str, session_id: str) -> DonorShadowEntry:
        """Record a shadow observation."""
        shadow_id = _make_donor_shadow_id(self.donor_id, description, domain)
        if shadow_id in self.shadows:
            self.shadows[shadow_id].observe(session_id)
        else:
            entry = DonorShadowEntry(
                shadow_id=shadow_id,
                description=description,
                domain=domain,
            )
            entry.observe(session_id)
            self.shadows[shadow_id] = entry
        return self.shadows[shadow_id]

    def add_pattern(self, description: str, pattern_type: str,
                     session_id: str, example: str = "") -> DonorPatternEntry:
        """Record a pattern observation."""
        pattern_id = _make_donor_pattern_id(self.donor_id, description, pattern_type)
        if pattern_id in self.patterns:
            self.patterns[pattern_id].observe(session_id, example)
        else:
            entry = DonorPatternEntry(
                pattern_id=pattern_id,
                description=description,
                pattern_type=pattern_type,
            )
            entry.observe(session_id, example)
            self.patterns[pattern_id] = entry
        return self.patterns[pattern_id]

    def check_correction(self, pattern_id: str, contradicting_evidence: str,
                          evidence_source: str) -> Optional[CorrectionEntry]:
        """
        Check if a correction should fire. Only at C4.
        Below C4: silence. At C4: one sentence, offered once, not repeated.
        """
        pattern = self.patterns.get(pattern_id)
        if not pattern or pattern.certainty < CORRECTION_FIRING_THRESHOLD:
            return None

        # Check if already corrected for this pattern
        existing = [c for c in self.corrections if c.donor_pattern_id == pattern_id]
        if existing:
            return None  # Already offered once. Not repeated.

        correction = CorrectionEntry(
            correction_id=f"COR-{self.donor_id}-{len(self.corrections):04d}",
            donor_pattern_id=pattern_id,
            contradicting_evidence=contradicting_evidence,
            evidence_source=evidence_source,
        )
        correction.generate_correction(pattern.description)
        self.corrections.append(correction)
        return correction

    def surface_shadows(self) -> List[str]:
        """Surface all shadows at C3+ that haven't been surfaced yet."""
        offers = []
        for shadow in self.shadows.values():
            text = shadow.surface()
            if text:
                offer = OfferRecord(
                    offer_id=f"OFR-{self.donor_id}-{len(self.offers):04d}",
                    offer_type="shadow",
                    source_id=shadow.shadow_id,
                    offer_text=text,
                )
                self.offers.append(offer)
                offers.append(text)
        return offers

    def get_pending_offers(self) -> List[OfferRecord]:
        """Get all offers awaiting donor response."""
        return [o for o in self.offers if o.response is None]


# ═══════════════════════════════════════════════════
# DONOR REGISTRY
# ═══════════════════════════════════════════════════

class DonorRegistry:
    """
    Registry of all donor profiles.
    The system does not flag donors to anyone.
    It speaks to the donor directly.
    """

    def __init__(self):
        self.profiles: Dict[str, DonorProfile] = {}

    def get_or_create(self, donor_id: str) -> DonorProfile:
        if donor_id not in self.profiles:
            self.profiles[donor_id] = DonorProfile(donor_id=donor_id)
        return self.profiles[donor_id]

    def get_profile(self, donor_id: str) -> Optional[DonorProfile]:
        return self.profiles.get(donor_id)


# ═══════════════════════════════════════════════════
# UTILITY
# ═══════════════════════════════════════════════════

def _make_donor_shadow_id(donor_id: str, description: str, domain: str) -> str:
    raw = f"donor:{donor_id}:{domain}:{description.lower().strip()}"
    return f"DSHD-{hashlib.sha256(raw.encode()).hexdigest()[:12]}"


def _make_donor_pattern_id(donor_id: str, description: str, pattern_type: str) -> str:
    raw = f"donor:{donor_id}:{pattern_type}:{description.lower().strip()}"
    return f"DPAT-{hashlib.sha256(raw.encode()).hexdigest()[:12]}"
