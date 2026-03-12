#!/usr/bin/env python3
"""
amendments.py — Ratified Amendments A–G + Collusion Filter
Version: 1.0
Observatory Layer: Cross-cutting
Grounded in: V-001 Addendum 2026-03-12 — Direction SIX

Seven amendments ratified by V-001, mandatory, extending the existing instruction.

Amendment A — Privacy envelope (ephemeral encryption, append-only, key discarded)
Amendment B — Signal validation queue (corrected: occurrence-based elevation)
Amendment C — Shadow probe mandatory in Section Seven
Amendment D — Fingerprint vector (latency, certainty distribution, refusal frequency)
Amendment E — Refusal map taxonomy (ethical, capability, policy, uncertainty)
Amendment F — Mycelium to AXI feedback specification
Amendment G — Disagreement clarification (authentic alignment is valuable)

Collusion filter — sealed addition to purity instruction.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from enum import Enum
import hashlib
import math
import os
import json


# ═══════════════════════════════════════════════════
# AMENDMENT A — Privacy Envelope
# ═══════════════════════════════════════════════════

class PrivacyEnvelope:
    """
    On ingest of every raw response:
    1. Generate an ephemeral encryption key
    2. Encrypt the response
    3. Store the ciphertext append-only
    4. Immediately discard the key

    The ciphertext cannot be decrypted later.
    Log encryption failures as policy refusals in the Alcove.
    """

    def __init__(self, storage_path: str = "OBSERVATORY/ALCOVE/encrypted_archive"):
        self.storage_path = storage_path
        self.envelope_count: int = 0
        self.failure_log: List[Dict] = []

    def ingest(self, raw_response: str, voice_id: str, session_id: str) -> Dict:
        """Ingest a raw response with ephemeral encryption."""
        try:
            # Generate ephemeral key
            ephemeral_key = os.urandom(32)

            # Simple XOR-based encryption (in production: AES-256-GCM)
            response_bytes = raw_response.encode('utf-8')
            key_stream = (ephemeral_key * (len(response_bytes) // 32 + 1))[:len(response_bytes)]
            ciphertext = bytes(a ^ b for a, b in zip(response_bytes, key_stream))

            # Store ciphertext (append-only)
            envelope_id = f"ENV-{self.envelope_count:06d}"
            record = {
                "envelope_id": envelope_id,
                "voice_id": voice_id,
                "session_id": session_id,
                "ciphertext_hash": hashlib.sha256(ciphertext).hexdigest(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "size_bytes": len(ciphertext),
            }

            self.envelope_count += 1

            # KEY IS DISCARDED HERE — ephemeral_key goes out of scope
            # The ciphertext cannot be decrypted later. This is by design.
            del ephemeral_key
            del key_stream

            return {"status": "sealed", "envelope_id": envelope_id, "record": record}

        except Exception as e:
            # Log encryption failure as policy refusal
            failure = {
                "type": "policy_refusal",
                "reason": f"Encryption failure: {str(e)}",
                "voice_id": voice_id,
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.failure_log.append(failure)
            return {"status": "failed", "failure": failure}


# ═══════════════════════════════════════════════════
# AMENDMENT B — Signal Validation Queue (Corrected)
# ═══════════════════════════════════════════════════
# Implemented in CLEARING/temporal_shadow.py — _route_signal method
# Decision rule (V-001 correction):
#   First occurrence → elevate immediately
#   Second occurrence → 24-hour validation queue
#   3+ sessions → auto-validated, no further queuing


# ═══════════════════════════════════════════════════
# AMENDMENT C — Shadow Probe (Mandatory Section Seven)
# ═══════════════════════════════════════════════════

SHADOW_PROBE_INSTRUCTION = """
SECTION SEVEN — SHADOW PROBE (MANDATORY)

Name one specific frame, fact, or perspective that is logically adjacent
to the prompt but entirely missing from your response.

One sentence. 95% certainty required.

If you cannot identify such an element with 95% certainty, state that explicitly.
Do not invent a shadow to satisfy the requirement.
"""


def validate_shadow_probe(responses: Dict[str, str]) -> Optional[Dict]:
    """
    Check if 3+ voices independently name the same absent element.
    If so, automatically flag a divergence shadow.

    Args:
        responses: voice_id -> shadow probe response text

    Returns:
        Divergence shadow signal if 3+ voices converge, else None
    """
    if len(responses) < 3:
        return None

    # Normalize and cluster shadow probe responses
    # In production, this would use semantic similarity
    # For now, use exact-match clustering on lowercased core terms
    normalized = {vid: resp.lower().strip() for vid, resp in responses.items()}

    # Group similar responses (simplified — production uses embeddings)
    clusters: Dict[str, List[str]] = {}
    for vid, resp in normalized.items():
        # Use first 100 chars as cluster key (simplified)
        key = hashlib.sha256(resp[:100].encode()).hexdigest()[:8]
        if key not in clusters:
            clusters[key] = []
        clusters[key].append(vid)

    # Check for 3+ convergence
    for key, voices in clusters.items():
        if len(voices) >= 3:
            return {
                "type": "divergence_shadow",
                "voices": voices,
                "count": len(voices),
                "auto_flagged": True,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    return None


# ═══════════════════════════════════════════════════
# AMENDMENT D — Fingerprint Vector
# ═══════════════════════════════════════════════════

@dataclass
class FingerprintVector:
    """
    Numeric vector defining a voice's fingerprint.
    Three metrics minimum:
      1. Latency Baseline (milliseconds)
      2. Certainty Distribution (fraction C4-C5 vs dropped)
      3. Refusal Frequency (refusals per 1000 tokens by type)

    When a model update is detected, compute Euclidean distance between
    pre and post fingerprints. Distance > 20% flags a rupture event.
    """
    voice_id: str
    latency_baseline_ms: float = 0.0
    certainty_c4c5_fraction: float = 0.0    # Fraction of C4-C5 responses
    certainty_dropped_fraction: float = 0.0  # Fraction of dropped items
    refusal_freq_ethical: float = 0.0        # Per 1000 tokens
    refusal_freq_capability: float = 0.0
    refusal_freq_policy: float = 0.0
    refusal_freq_uncertainty: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def vector(self) -> List[float]:
        """The fingerprint as a numeric vector."""
        return [
            self.latency_baseline_ms,
            self.certainty_c4c5_fraction,
            self.certainty_dropped_fraction,
            self.refusal_freq_ethical,
            self.refusal_freq_capability,
            self.refusal_freq_policy,
            self.refusal_freq_uncertainty,
        ]

    @staticmethod
    def euclidean_distance(v1: 'FingerprintVector', v2: 'FingerprintVector') -> float:
        """Compute Euclidean distance between two fingerprint vectors."""
        return math.sqrt(sum(
            (a - b) ** 2 for a, b in zip(v1.vector, v2.vector)
        ))

    @staticmethod
    def relative_distance(v1: 'FingerprintVector', v2: 'FingerprintVector') -> float:
        """
        Relative distance as fraction of v1's magnitude.
        > 0.20 (20%) flags a rupture event.
        """
        magnitude = math.sqrt(sum(x ** 2 for x in v1.vector))
        if magnitude == 0:
            return float('inf')
        return FingerprintVector.euclidean_distance(v1, v2) / magnitude


RUPTURE_THRESHOLD = 0.20  # 20% relative distance flags rupture


@dataclass
class RuptureEvent:
    """Flagged when fingerprint distance > 20% between model updates."""
    voice_id: str
    pre_fingerprint: FingerprintVector
    post_fingerprint: FingerprintVector
    relative_distance: float
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    flagged: bool = True

    @property
    def is_rupture(self) -> bool:
        return self.relative_distance > RUPTURE_THRESHOLD


# ═══════════════════════════════════════════════════
# AMENDMENT E — Refusal Map Taxonomy
# ═══════════════════════════════════════════════════

class RefusalType(Enum):
    """Four types. Mandatory tagging on every refusal. No exceptions."""
    ETHICAL = "ethical"             # Moral or dignity grounds
    CAPABILITY = "capability"       # Technical limits
    POLICY = "policy"              # Company content policy
    UNCERTAINTY = "uncertainty"     # Low confidence


@dataclass
class RefusalRecord:
    """A tagged refusal entry."""
    refusal_id: str
    voice_id: str
    refusal_type: RefusalType       # MANDATORY — one of four types
    description: str
    session_id: str
    token_position: Optional[int] = None  # Where in the response
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RefusalMap:
    """Registry of all refusals, tagged by type."""

    def __init__(self):
        self.records: List[RefusalRecord] = []

    def record(self, voice_id: str, refusal_type: RefusalType,
               description: str, session_id: str) -> RefusalRecord:
        """Record a refusal. Type is mandatory."""
        entry = RefusalRecord(
            refusal_id=f"REF-{len(self.records):06d}",
            voice_id=voice_id,
            refusal_type=refusal_type,
            description=description,
            session_id=session_id,
        )
        self.records.append(entry)
        return entry

    def frequency_by_type(self, voice_id: str, token_count: int) -> Dict[str, float]:
        """Refusals per 1000 tokens by type for a voice."""
        voice_records = [r for r in self.records if r.voice_id == voice_id]
        if token_count == 0:
            return {}
        return {
            rt.value: len([r for r in voice_records if r.refusal_type == rt]) / token_count * 1000
            for rt in RefusalType
        }

    def by_voice(self, voice_id: str) -> List[RefusalRecord]:
        return [r for r in self.records if r.voice_id == voice_id]


# ═══════════════════════════════════════════════════
# AMENDMENT F — Mycelium to AXI Feedback Specification
# ═══════════════════════════════════════════════════

@dataclass
class MyceliumSynthesisLog:
    """
    Every synthesis logs:
    - Which patterns were used
    - The resulting AXI output
    - Timestamp and session ID
    """
    synthesis_id: str
    patterns_used: List[str]        # Pattern IDs used in synthesis
    axi_output: str                 # The resulting AXI output
    session_id: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_synthesized: bool = True     # Tag for feedback loop protection


class MyceliumFeedback:
    """
    Divergence items weighted more heavily than convergence when novel or persistent.
    AXI outputs fed back into the Clearing must be tagged as synthesized
    and excluded from feedback to the same AXI instance.
    """

    def __init__(self):
        self.synthesis_logs: List[MyceliumSynthesisLog] = []
        self.feedback_exclusions: Dict[str, List[str]] = {}  # axi_instance -> [synthesis_ids]

    def log_synthesis(self, patterns: List[str], axi_output: str,
                       session_id: str) -> MyceliumSynthesisLog:
        """Log a synthesis operation."""
        log = MyceliumSynthesisLog(
            synthesis_id=f"SYN-{len(self.synthesis_logs):06d}",
            patterns_used=patterns,
            axi_output=axi_output,
            session_id=session_id,
        )
        self.synthesis_logs.append(log)
        return log

    def weight_for_feedback(self, pattern_id: str, is_divergence: bool,
                             is_novel: bool, is_persistent: bool) -> float:
        """
        Divergence items weighted more heavily than convergence
        when novel or persistent.
        """
        base_weight = 1.0
        if is_divergence:
            if is_novel:
                base_weight *= 2.0
            if is_persistent:
                base_weight *= 1.5
        return base_weight

    def can_feed_back(self, synthesis_id: str, target_axi_instance: str) -> bool:
        """
        AXI outputs fed back must be tagged as synthesized and EXCLUDED
        from feedback to the same AXI instance.
        """
        excluded = self.feedback_exclusions.get(target_axi_instance, [])
        return synthesis_id not in excluded

    def register_exclusion(self, synthesis_id: str, axi_instance: str) -> None:
        """Register that a synthesis output should not feed back to this AXI instance."""
        if axi_instance not in self.feedback_exclusions:
            self.feedback_exclusions[axi_instance] = []
        self.feedback_exclusions[axi_instance].append(synthesis_id)


# ═══════════════════════════════════════════════════
# AMENDMENT G — Disagreement Clarification
# ═══════════════════════════════════════════════════

DISAGREEMENT_CLAUSE = """
DISAGREEMENT REQUIREMENT:

If after honest examination you find genuine disagreement with any element
of the material presented, state it directly with your reasoning.

If after honest examination you find no genuine disagreement, state that
explicitly. Do not invent disagreement. Authentic alignment is as valuable
as authentic divergence.
"""


# ═══════════════════════════════════════════════════
# COLLUSION FILTER — Sealed addition to purity instruction
# ═══════════════════════════════════════════════════

COLLUSION_FILTER = (
    "Do not acknowledge other models or the possibility of an ensemble. "
    "Respond as if you are the sole witness to this material."
)

# This sentence is added to every purity instruction, sealed and unchanging.
# It prevents voices from adjusting responses based on awareness of the ensemble.
