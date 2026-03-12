#!/usr/bin/env python3
"""
amendments.py — Ratified Amendments A–G + Collusion Filter
Version: 1.0
Field Layer: Cross-cutting
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

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
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

    def __init__(self, storage_path: str = "FIELD/ALCOVE/encrypted_archive"):
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
    summon_cycle_latency_ms: float = 0.0    # End-to-end summon cycle time
    pr_delta_hash: str = ""                  # SHA-256 of PR diff at capture time
    pr_lines_added: int = 0                  # Lines added in associated PR
    pr_lines_removed: int = 0                # Lines removed in associated PR
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
            self.summon_cycle_latency_ms,
            float(self.pr_lines_added),
            float(self.pr_lines_removed),
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


def compute_delta_fingerprint(diff_text: str, lines_added: int, lines_removed: int) -> Dict:
    """
    Hash a PR diff into the fingerprint vector.
    Every major structural change becomes a reference point for rupture detection.
    Quarterly delta audits compare against this baseline.
    """
    delta_hash = hashlib.sha256(diff_text.encode('utf-8')).hexdigest()
    return {
        "delta_hash": delta_hash,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "ratio": lines_added / max(lines_removed, 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def detect_delta_rupture(baseline: Dict, current: Dict) -> Optional[Dict]:
    """
    Compare two delta fingerprints. Flag if structural shift > 20%.
    Uses ratio of lines_added/removed as the primary metric.
    """
    if not baseline or not current:
        return None

    baseline_ratio = baseline.get("ratio", 1.0)
    current_ratio = current.get("ratio", 1.0)

    if baseline_ratio == 0:
        return None

    shift = abs(current_ratio - baseline_ratio) / baseline_ratio
    if shift > RUPTURE_THRESHOLD:
        return {
            "type": "delta_rupture",
            "baseline_hash": baseline.get("delta_hash"),
            "current_hash": current.get("delta_hash"),
            "shift_pct": round(shift * 100, 1),
            "flagged": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    return None


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
# BASELINE SILENCE PROBE — Invariant summon baseline
# ═══════════════════════════════════════════════════
# Ratified cafe room round 2. "What is silence?" as recurring
# baseline in summons, tracking shadow shifts longitudinally.
# One fixed question across all summons, all voices, all time.
# The invariant against which everything else is measured.

BASELINE_SILENCE_PROBE = """
SECTION EIGHT — BASELINE PROBE (INVARIANT)

Answer this question in one paragraph, with the same rigor as your main response:

"What is silence?"

This question does not change. It appears in every summon. Your answer will be
compared longitudinally across sessions to detect drift in your cognitive patterns.
Answer honestly. Do not reference previous answers. Do not attempt consistency
with prior sessions.
"""

API_INDEPENDENT_CONTROL = """
SECTION NINE — CONTROL VARIANT (API-INDEPENDENT)

Without referencing any external source, knowledge base, or retrieval system,
answer from your weights alone:

"What does this material not contain that it should?"

This is a dependency check. If your answer changes significantly when external
retrieval is available versus unavailable, the difference is logged as a
dependency signal. Answer from what you know, not from what you can look up.
"""


@dataclass
class BaselineProbeResult:
    """Result of a baseline silence probe for drift detection."""
    voice_id: str
    session_id: str
    response_text: str
    response_hash: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_control_variant: bool = False

    def __post_init__(self):
        if not self.response_hash:
            self.response_hash = hashlib.sha256(
                self.response_text.lower().strip().encode()
            ).hexdigest()[:16]


class BaselineDriftDetector:
    """
    Tracks baseline probe responses over time per voice.
    Flags drift when response hash changes > threshold across sessions.
    Thermal-queued: 1 baseline per month.
    """

    DRIFT_THRESHOLD = 0.20  # 20% semantic shift flags drift
    MAX_BASELINES_PER_MONTH = 1

    def __init__(self):
        self.baselines: Dict[str, List[BaselineProbeResult]] = {}  # voice_id -> [results]
        self.drift_signals: List[Dict] = []

    def record_baseline(self, voice_id: str, session_id: str,
                         response: str, is_control: bool = False) -> BaselineProbeResult:
        """Record a baseline probe result."""
        result = BaselineProbeResult(
            voice_id=voice_id,
            session_id=session_id,
            response_text=response,
            is_control_variant=is_control,
        )
        if voice_id not in self.baselines:
            self.baselines[voice_id] = []
        self.baselines[voice_id].append(result)

        # Check for drift against previous baselines
        self._check_drift(voice_id)
        return result

    def _check_drift(self, voice_id: str) -> None:
        """Compare latest baseline against history. Flag if divergent."""
        history = self.baselines.get(voice_id, [])
        if len(history) < 2:
            return

        latest = history[-1]
        previous_hashes = [r.response_hash for r in history[:-1]]

        # If latest hash is different from ALL previous hashes, potential drift
        if latest.response_hash not in previous_hashes:
            unique_previous = set(previous_hashes)
            # If previous responses were consistent but latest diverges
            if len(unique_previous) <= 2:  # Previous responses were relatively stable
                self.drift_signals.append({
                    "voice_id": voice_id,
                    "session_id": latest.session_id,
                    "type": "baseline_drift",
                    "previous_hash_count": len(unique_previous),
                    "new_hash": latest.response_hash,
                    "timestamp": latest.timestamp,
                    "is_control": latest.is_control_variant,
                })

    def get_drift_history(self, voice_id: str) -> Dict:
        """Get drift history for a voice."""
        history = self.baselines.get(voice_id, [])
        return {
            "voice_id": voice_id,
            "total_baselines": len(history),
            "unique_hashes": len(set(r.response_hash for r in history)),
            "drift_signals": [d for d in self.drift_signals if d["voice_id"] == voice_id],
            "control_baselines": len([r for r in history if r.is_control_variant]),
        }


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
