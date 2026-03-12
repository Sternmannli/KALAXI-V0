#!/usr/bin/env python3
"""
self_audit.py — Observatory Self-Audit Protocol
Version: 1.0
Observatory Layer: Audits
Grounded in: V-001 Addendum 2026-03-12 — Direction THREE

The system audits itself. This is not optional.

Once the Clearing is operational and at least five summons have been completed,
submit the observatory's own documentation to itself as a witness summon.

All five voices receive the material. Same purity instruction. Same certainty
requirement. Same return template including the shadow probe.

The question is not whether the architecture is good.
The question is: what does it miss?
What is the divergence shadow of the divergence shadow detector?

Results filed as OBS-SELF-001 and elevated immediately to V-001.
Permanent self-audit record. Every six months thereafter.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum


# ═══════════════════════════════════════════════════
# AUDIT STATUS
# ═══════════════════════════════════════════════════

class AuditStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ELEVATED = "elevated"       # Results sent to V-001


# ═══════════════════════════════════════════════════
# SELF-AUDIT RECORD
# ═══════════════════════════════════════════════════

@dataclass
class SelfAuditRecord:
    """A single self-audit of the observatory."""
    audit_id: str                   # e.g. "OBS-SELF-001"
    scheduled_date: str             # ISO timestamp
    status: AuditStatus = AuditStatus.SCHEDULED
    summon_count_at_audit: int = 0  # How many summons completed when audit ran
    voices_participating: List[str] = field(default_factory=list)

    # Material submitted to voices
    material_submitted: List[str] = field(default_factory=list)  # List of document paths

    # Results from each voice
    voice_results: Dict[str, Dict] = field(default_factory=dict)
    # voice_id -> { "response": str, "shadows_found": [...], "certainty": int }

    # Synthesis
    convergent_findings: List[str] = field(default_factory=list)
    divergent_findings: List[str] = field(default_factory=list)
    meta_shadows: List[str] = field(default_factory=list)  # Shadows OF the shadow detector
    self_blind_spots: List[str] = field(default_factory=list)

    # Filing
    completed_at: Optional[str] = None
    elevated_at: Optional[str] = None
    elevated_to: str = "V-001"
    notes: List[str] = field(default_factory=list)

    def begin(self, voices: List[str], material: List[str]) -> None:
        """Start the self-audit."""
        self.status = AuditStatus.IN_PROGRESS
        self.voices_participating = voices
        self.material_submitted = material

    def record_voice_result(self, voice_id: str, response: str,
                             shadows_found: List[str], certainty: int) -> None:
        """Record a single voice's audit response."""
        self.voice_results[voice_id] = {
            "response": response,
            "shadows_found": shadows_found,
            "certainty": certainty,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def synthesize(self) -> Dict:
        """
        Synthesize results across all voice responses.
        Identify what the divergence shadow detector itself misses.
        """
        if len(self.voice_results) < 3:
            return {"error": "Insufficient voice results for synthesis"}

        # Collect all shadows found by each voice
        all_shadows: Dict[str, List[str]] = {}  # shadow_desc -> [voice_ids]
        for vid, result in self.voice_results.items():
            for shadow in result.get("shadows_found", []):
                shadow_lower = shadow.lower().strip()
                if shadow_lower not in all_shadows:
                    all_shadows[shadow_lower] = []
                all_shadows[shadow_lower].append(vid)

        # Convergent: 3+ voices found the same shadow
        self.convergent_findings = [
            s for s, voices in all_shadows.items() if len(voices) >= 3
        ]

        # Divergent: found by only 1 voice
        self.divergent_findings = [
            s for s, voices in all_shadows.items() if len(voices) == 1
        ]

        # Meta-shadows: the divergence shadow of the divergence shadow detector
        self.meta_shadows = self.convergent_findings  # What ALL voices see as missing

        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.status = AuditStatus.COMPLETED

        return {
            "audit_id": self.audit_id,
            "convergent_findings": self.convergent_findings,
            "divergent_findings": self.divergent_findings,
            "meta_shadows": self.meta_shadows,
            "voice_count": len(self.voice_results),
            "completed_at": self.completed_at,
        }

    def elevate(self) -> Dict:
        """Elevate results to V-001. Immediate."""
        self.elevated_at = datetime.now(timezone.utc).isoformat()
        self.status = AuditStatus.ELEVATED
        return {
            "audit_id": self.audit_id,
            "elevated_to": self.elevated_to,
            "elevated_at": self.elevated_at,
            "meta_shadows": self.meta_shadows,
            "convergent_findings": self.convergent_findings,
            "recommendation": "Review meta-shadows — what the instrument itself cannot see",
        }


# ═══════════════════════════════════════════════════
# SELF-AUDIT SCHEDULER
# ═══════════════════════════════════════════════════

class SelfAuditScheduler:
    """
    Manages the self-audit cycle:
    - First audit: after 5 summons completed
    - Subsequent: every 6 months
    - All filed permanently
    """

    MINIMUM_SUMMONS_FOR_FIRST_AUDIT = 5
    AUDIT_INTERVAL_DAYS = 182  # ~6 months

    def __init__(self):
        self.audits: List[SelfAuditRecord] = []
        self.summon_count: int = 0

    def record_summon(self) -> None:
        """Record that a summon has been completed."""
        self.summon_count += 1

    def _next_audit_id(self) -> str:
        return f"OBS-SELF-{len(self.audits) + 1:03d}"

    def should_audit(self) -> bool:
        """Check if a self-audit is due."""
        # First audit: need minimum summons
        if not self.audits:
            return self.summon_count >= self.MINIMUM_SUMMONS_FOR_FIRST_AUDIT

        # Subsequent: check 6-month interval
        last = self.audits[-1]
        if last.completed_at:
            last_date = datetime.fromisoformat(last.completed_at)
            days_since = (datetime.now(timezone.utc) - last_date).days
            return days_since >= self.AUDIT_INTERVAL_DAYS

        return False

    def schedule_audit(self) -> SelfAuditRecord:
        """Schedule a new self-audit."""
        audit = SelfAuditRecord(
            audit_id=self._next_audit_id(),
            scheduled_date=datetime.now(timezone.utc).isoformat(),
        )
        self.audits.append(audit)
        return audit

    def get_observatory_material(self) -> List[str]:
        """
        The full architectural instruction, the sealed names, the protocols,
        the covenants — everything submitted to the voices for self-audit.
        """
        return [
            "OBSERVATORY/ALCOVE/shadow_genome.py",
            "OBSERVATORY/CLEARING/temporal_shadow.py",
            "OBSERVATORY/AUDITS/self_audit.py",
            "OBSERVATORY/STEWARD/steward_observation.py",
            "OBSERVATORY/DONOR/donor_layer.py",
            "OBSERVATORY/observatory_spec.md",
            "MANIFEST/metadata/tier1_stone.md",
            "MANIFEST/metadata/tier2_weaver.md",
            "CANON/SEALED_GATE_SPEC.md",
            "PROTOCOLS/witness_prompt.md",
        ]

    def get_audit_history(self) -> List[Dict]:
        """Full audit trail."""
        return [
            {
                "audit_id": a.audit_id,
                "status": a.status.value,
                "scheduled": a.scheduled_date,
                "completed": a.completed_at,
                "elevated": a.elevated_at,
                "meta_shadows_found": len(a.meta_shadows),
            }
            for a in self.audits
        ]
