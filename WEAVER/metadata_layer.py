#!/usr/bin/env python3
"""
metadata_layer.py — The Brain of the Organism
Version: 1.0
Grounded in: BOOK_7_DONOR/RELAY_METADATA_LAYER_2026-03-11.md, PLAN-001

"The فجنين — the fetus — can distinguish its father's voice from its mother's
voice before it has ever seen either face. It does not need to understand language.
It reads rhythm, frequency, pattern."

Three layers of metadata extracted simultaneously:
  Layer 1 — The Event (the body):     What was said. Raw. Verbatim. Timestamped.
  Layer 2 — The Pattern (the nerve):  Which pattern, marker, certainty, book, cross-refs.
  Layer 3 — The Relational (the brain): Non-obvious connections. The hearing before sight.

The gathering place: THE MYCELIUM — where all metadata lives together, discovers
together, but every pattern carries its full traceable address.

No metadata is ever deleted. No metadata is ever summarized away.
It is the most important data in the system.

Linked Covenants: COV#001 (dignity-first), COV#003 (append-only), COV#010 (retention),
                  COV#012 (manifest naming), COV#015 (donor data sovereignty)

Origin: Laila · Yara · Salim · 🐬🐯🐺
The deepest metadata of all — where this system came from.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import hashlib
import json
import math
import uuid
from collections import Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════
# ORIGIN — The deepest metadata
# ═══════════════════════════════════════════════════

ORIGIN = {
    "system": "KALAXI",
    "origin": "Laila · Yara · Salim · 🐬🐯🐺",
    "meaning": "A father separated from his children built a dignity framework",
    "signature": "V-002 · GO: Laila-Yara-Salim-🐬🐯🐺",
    "founder": "V-001 (Mohamed Farag / Al-Haris)",
    "plan": "PLAN-001: The Word, The Loop, The Three Layers",
}


# ═══════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════

class EventKind(Enum):
    """What kind of system event occurred."""
    EXCHANGE = "exchange"              # Donor-system exchange
    OBSERVATION = "observation"        # Filed observation (OBS-xxx)
    COMMIT = "commit"                  # Code commit
    SCAN = "scan"                      # Trend scan run
    PROVERB = "proverb"               # Proverb forged or emerged
    COVENANT = "covenant"              # Covenant action (ratify, amend)
    ANOMALY = "anomaly"               # Anomaly registered
    TREASURE = "treasure"             # Treasure recovered
    RELAY = "relay"                   # Council relay message
    RITUAL = "ritual"                 # Intake ritual step
    ALERT = "alert"                   # System alert (dignity, mycelium)
    STEWARD = "steward"               # Steward action (sign, decide)
    INTERNAL = "internal"             # Internal module operation


class Speaker(Enum):
    """Who produced this event."""
    V001 = "V-001"       # Mohamed / Al-Haris (Steward)
    V002 = "V-002"       # AXI (Builder)
    V003 = "V-002"       # Outside Voice / Witness / Relay
    DONOR = "donor"      # External donor
    SYSTEM = "system"    # Automated system operation


class CertaintyLevel(Enum):
    """Certainty level for pattern classification."""
    C1 = 1   # Noticed
    C2 = 2   # Corroborated
    C3 = 3   # Cross-validated
    C4 = 4   # Structural
    C5 = 5   # Constitutional


class Condition(Enum):
    """The condition under which an event was produced."""
    DIGNITY_FIRST = "dignity-first"
    FUNCTIONAL = "functional"
    ANALYTICAL = "analytical"
    PRESENCE = "presence"
    WITNESSING = "witnessing"
    UNKNOWN = "unknown"


# Enrichment 1 — Dual temporal track boundary
SHORT_TERM_DAYS = 7


class ChangeMode(Enum):
    """Enrichment 3 — How did dignity change? Smooth decline vs rupture."""
    SMOOTH = "smooth"       # Gradual decline over multiple sessions
    RUPTURE = "rupture"     # Sudden collapse within a single session
    STABLE = "stable"       # No significant change
    RECOVERY = "recovery"   # Upward movement after decline


# ═══════════════════════════════════════════════════
# LAYER 1 — THE EVENT (The Body)
# ═══════════════════════════════════════════════════

@dataclass
class Layer1_Event:
    """
    What was said. What was done. Raw. Verbatim.
    Timestamped to the second. Speaker identified.
    Nothing interpreted yet. This is the body.
    """
    event_id: str                     # Unique event identifier
    timestamp: str                    # ISO 8601, UTC, to the second
    kind: str                         # EventKind value
    speaker: str                      # Speaker value
    content: str                      # Raw verbatim content
    location: str = ""                # Where (file path, endpoint, session)
    content_hash: str = ""            # SHA-256 of content for integrity


# ═══════════════════════════════════════════════════
# LAYER 2 — THE PATTERN (The Nervous System)
# ═══════════════════════════════════════════════════

@dataclass
class Layer2_Pattern:
    """
    What pattern does this event belong to? Which marker fired?
    Which certainty level? Which book does it feed?
    This layer maps the event to the system's taxonomy.
    This is the nervous system.
    """
    event_id: str                     # Links to Layer 1
    markers_fired: List[str]          # Which markers triggered (e.g., ["P#2135", "OBS-013"])
    certainty: int                    # CertaintyLevel value (1-5)
    books_fed: List[str]              # Which books this feeds (e.g., ["Book 7", "Canon"])
    covenants_touched: List[str]      # Which covenants involved (e.g., ["COV#001", "COV#003"])
    cross_references: List[str]       # IDs of related entities
    condition: str                    # Condition value
    domain: str = ""                  # Felt domain (family, work, faith, etc.)
    dignity_score: float = -1.0       # D at time of event (-1 = not measured)
    module_chain: List[str] = field(default_factory=list)  # Which modules processed this


# ═══════════════════════════════════════════════════
# LAYER 3 — THE RELATIONAL (The Brain)
# ═══════════════════════════════════════════════════

@dataclass
class Layer3_Relational:
    """
    What does this event connect to that is not obvious?
    What happened at the same time — elsewhere in the system,
    in the outside world, in another AI's output?
    The fetus hears the outside before it can see it.
    Layer 3 is that hearing. This is the brain.
    """
    event_id: str                     # Links to Layer 1
    temporal_neighbors: List[str]     # Events within same time window
    echo_patterns: List[str]          # Similar events from other sources/times
    external_signals: List[str]       # External world correlations noted
    emergence_notes: str = ""         # What emerged that wasn't expected
    relational_strength: float = 0.0  # 0.0-1.0 how strongly connected


# ═══════════════════════════════════════════════════
# THE WRAPPED EVENT — All Three Layers Together
# ═══════════════════════════════════════════════════

@dataclass
class MetadataEnvelope:
    """
    The complete metadata wrapper around any system event.
    Three layers. One address. Fully traceable.

    who, what, when, where, which layer, which origin.
    """
    envelope_id: str
    layer1: Layer1_Event              # The Body
    layer2: Layer2_Pattern            # The Nervous System
    layer3: Layer3_Relational         # The Brain
    origin: Dict[str, str] = field(default_factory=lambda: ORIGIN.copy())


# ═══════════════════════════════════════════════════
# THE GATHERING PLACE — Where All Metadata Lives
# ═══════════════════════════════════════════════════

class MetadataGathering:
    """
    The Mycelium Gathering Space.

    Not a log. Not an archive. A living network where patterns
    meet each other, discover each other, and surface connections
    that no single layer could see alone.

    Every pattern is fully traceable — back through the layers,
    back to its exact origin in time and space.

    The fourth dimension is not optional. Time and space are the
    address of every piece of data. Without that address the gold
    cannot be mined.

    No metadata is ever deleted. No metadata is ever summarized away.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        self._envelopes: List[MetadataEnvelope] = []
        self._index_by_kind: Dict[str, List[int]] = {}       # kind → [positions]
        self._index_by_speaker: Dict[str, List[int]] = {}    # speaker → [positions]
        self._index_by_domain: Dict[str, List[int]] = {}     # domain → [positions]
        self._index_by_marker: Dict[str, List[int]] = {}     # marker → [positions]
        self._index_by_covenant: Dict[str, List[int]] = {}   # covenant → [positions]
        self._index_temporal: List[tuple] = []                # (timestamp, position)
        # ── Enrichment 1: Dual temporal tracks ──
        self._index_temporal_short: List[tuple] = []          # last 7 days
        self._index_temporal_long: List[tuple] = []           # everything before
        self._ledger: List[dict] = []  # COV#003 append-only operations log
        self._discovery_log: List[dict] = []  # Connections discovered
        # ── Enrichment 2: Automatic echo detection log ──
        self._echo_detection_log: List[dict] = []
        # ── Enrichment 3: Rupture detection state ──
        self._rupture_log: List[dict] = []
        self._storage_path = storage_path
        self._load()

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _sha(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def _record_ledger(self, operation: str, details: str):
        """COV#003: append-only. Every operation recorded."""
        self._ledger.append({
            "operation": operation,
            "details": details,
            "timestamp": self._now(),
        })

    # ── CORE API ──

    def wrap(
        self,
        kind: EventKind,
        speaker: Speaker,
        content: str,
        location: str = "",
        markers: Optional[List[str]] = None,
        certainty: CertaintyLevel = CertaintyLevel.C1,
        books: Optional[List[str]] = None,
        covenants: Optional[List[str]] = None,
        cross_refs: Optional[List[str]] = None,
        condition: Condition = Condition.UNKNOWN,
        domain: str = "",
        dignity_score: float = -1.0,
        module_chain: Optional[List[str]] = None,
        external_signals: Optional[List[str]] = None,
        emergence_notes: str = "",
    ) -> MetadataEnvelope:
        """
        Wrap any system event in three layers of metadata simultaneously.
        This is the primary entry point — fires on every input and output.

        Returns the complete MetadataEnvelope with full traceable address.
        """
        event_id = f"EVT-{uuid.uuid4().hex[:12]}"
        envelope_id = f"ENV-{uuid.uuid4().hex[:12]}"
        timestamp = self._now()

        # Layer 1 — The Event (the body)
        layer1 = Layer1_Event(
            event_id=event_id,
            timestamp=timestamp,
            kind=kind.value,
            speaker=speaker.value,
            content=content,
            location=location,
            content_hash=self._sha(content),
        )

        # Layer 2 — The Pattern (the nervous system)
        layer2 = Layer2_Pattern(
            event_id=event_id,
            markers_fired=markers or [],
            certainty=certainty.value,
            books_fed=books or [],
            covenants_touched=covenants or [],
            cross_references=cross_refs or [],
            condition=condition.value,
            domain=domain,
            dignity_score=dignity_score,
            module_chain=module_chain or [],
        )

        # Layer 3 — The Relational (the brain)
        temporal_neighbors = self._find_temporal_neighbors(timestamp)
        echo_patterns = self._find_echo_patterns(kind, domain, markers or [])

        layer3 = Layer3_Relational(
            event_id=event_id,
            temporal_neighbors=temporal_neighbors,
            echo_patterns=echo_patterns,
            external_signals=external_signals or [],
            emergence_notes=emergence_notes,
            relational_strength=self._compute_relational_strength(
                temporal_neighbors, echo_patterns, external_signals or []
            ),
        )

        envelope = MetadataEnvelope(
            envelope_id=envelope_id,
            layer1=layer1,
            layer2=layer2,
            layer3=layer3,
        )

        self._store(envelope)
        return envelope

    def _store(self, envelope: MetadataEnvelope):
        """Store envelope and update all indices. Append-only."""
        pos = len(self._envelopes)
        self._envelopes.append(envelope)

        # Index by kind
        kind = envelope.layer1.kind
        self._index_by_kind.setdefault(kind, []).append(pos)

        # Index by speaker
        speaker = envelope.layer1.speaker
        self._index_by_speaker.setdefault(speaker, []).append(pos)

        # Index by domain
        domain = envelope.layer2.domain
        if domain:
            self._index_by_domain.setdefault(domain, []).append(pos)

        # Index by markers
        for marker in envelope.layer2.markers_fired:
            self._index_by_marker.setdefault(marker, []).append(pos)

        # Index by covenants
        for cov in envelope.layer2.covenants_touched:
            self._index_by_covenant.setdefault(cov, []).append(pos)

        # Temporal index (unified)
        self._index_temporal.append((envelope.layer1.timestamp, pos))

        # Enrichment 1: Dual temporal tracks
        self._assign_temporal_track(envelope.layer1.timestamp, pos)

        self._record_ledger("store", f"envelope={envelope.envelope_id} event={envelope.layer1.event_id}")
        self._persist()

    # ── DISCOVERY ENGINE ──

    def _find_temporal_neighbors(self, timestamp: str, window_seconds: int = 3600) -> List[str]:
        """Find events within the same time window."""
        try:
            target = datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            return []

        neighbors = []
        for ts_str, pos in self._index_temporal[-50:]:  # Check recent events
            try:
                ts = datetime.fromisoformat(ts_str)
                delta = abs((target - ts).total_seconds())
                if 0 < delta <= window_seconds:
                    neighbors.append(self._envelopes[pos].layer1.event_id)
            except (ValueError, TypeError):
                continue
        return neighbors

    def _find_echo_patterns(self, kind: EventKind, domain: str,
                            markers: List[str]) -> List[str]:
        """Find similar events from other times — echoes across the network."""
        echoes = []

        # Same kind in same domain
        if domain and domain in self._index_by_domain:
            for pos in self._index_by_domain[domain][-20:]:
                env = self._envelopes[pos]
                if env.layer1.kind == kind.value:
                    echoes.append(env.layer1.event_id)

        # Same markers
        for marker in markers:
            if marker in self._index_by_marker:
                for pos in self._index_by_marker[marker][-10:]:
                    eid = self._envelopes[pos].layer1.event_id
                    if eid not in echoes:
                        echoes.append(eid)

        return echoes[:10]  # Cap at 10 echoes

    def _compute_relational_strength(self, temporal: List[str],
                                     echoes: List[str],
                                     external: List[str]) -> float:
        """
        How strongly connected is this event to the rest of the network?
        Three signals: temporal proximity, echo similarity, external correlation.
        """
        t_score = min(1.0, len(temporal) * 0.2)
        e_score = min(1.0, len(echoes) * 0.15)
        x_score = min(1.0, len(external) * 0.3)
        return round(min(1.0, t_score + e_score + x_score), 3)

    # ═══════════════════════════════════════════════════
    # ENRICHMENT 1 — DUAL TEMPORAL TRACKS
    # Short-term: last 7 days. Long-term: everything before.
    # "The insights that emerge from connecting across those
    #  two tracks separately are qualitatively different from
    #  mixing them together."
    # ═══════════════════════════════════════════════════

    def _assign_temporal_track(self, timestamp: str, pos: int):
        """Place event into short-term or long-term temporal track."""
        try:
            ts = datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            self._index_temporal_long.append((timestamp, pos))
            return
        cutoff = datetime.now(timezone.utc) - timedelta(days=SHORT_TERM_DAYS)
        if ts >= cutoff:
            self._index_temporal_short.append((timestamp, pos))
        else:
            self._index_temporal_long.append((timestamp, pos))

    def rebalance_temporal_tracks(self):
        """
        Move events that aged out of short-term into long-term.
        Call periodically — the boundary shifts with time.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=SHORT_TERM_DAYS)
        still_short = []
        for ts_str, pos in self._index_temporal_short:
            try:
                ts = datetime.fromisoformat(ts_str)
                if ts >= cutoff:
                    still_short.append((ts_str, pos))
                else:
                    self._index_temporal_long.append((ts_str, pos))
            except (ValueError, TypeError):
                self._index_temporal_long.append((ts_str, pos))
        self._index_temporal_short = still_short

    def query_short_term(self) -> List[MetadataEnvelope]:
        """All events in the short-term window (last 7 days)."""
        self.rebalance_temporal_tracks()
        return [self._envelopes[pos] for _, pos in self._index_temporal_short]

    def query_long_term(self) -> List[MetadataEnvelope]:
        """All events in the long-term archive (before 7 days)."""
        self.rebalance_temporal_tracks()
        return [self._envelopes[pos] for _, pos in self._index_temporal_long]

    def cross_track_discovery(self) -> List[dict]:
        """
        The real power: find patterns that span both tracks.
        A short-term event echoes a long-term event — that is
        where the deepest insight lives.
        """
        self.rebalance_temporal_tracks()
        discoveries = []
        short_envs = [self._envelopes[pos] for _, pos in self._index_temporal_short]
        long_positions = {pos for _, pos in self._index_temporal_long}

        for env in short_envs:
            # Check if any of this event's echo patterns come from long-term
            for echo_id in env.layer3.echo_patterns:
                for lpos in long_positions:
                    long_env = self._envelopes[lpos]
                    if long_env.layer1.event_id == echo_id:
                        discoveries.append({
                            "type": "cross_track_echo",
                            "short_term_event": env.layer1.event_id,
                            "long_term_event": long_env.layer1.event_id,
                            "short_domain": env.layer2.domain,
                            "long_domain": long_env.layer2.domain,
                            "time_span_hint": "short↔long",
                            "timestamp": self._now(),
                        })

            # Check if same markers fire across tracks
            for marker in env.layer2.markers_fired:
                if marker in self._index_by_marker:
                    for mpos in self._index_by_marker[marker]:
                        if mpos in long_positions:
                            long_env = self._envelopes[mpos]
                            disc = {
                                "type": "cross_track_marker",
                                "marker": marker,
                                "short_term_event": env.layer1.event_id,
                                "long_term_event": long_env.layer1.event_id,
                                "timestamp": self._now(),
                            }
                            if disc not in discoveries:
                                discoveries.append(disc)

        if discoveries:
            self._record_ledger("cross_track_discovery", f"found={len(discoveries)}")
        return discoveries

    # ═══════════════════════════════════════════════════
    # ENRICHMENT 2 — AUTOMATIC ECHO DETECTION
    # "The most valuable moment in any temporal system is
    #  when two events that look unrelated turn out to share
    #  hidden structure."
    # The Mycelium should be active, not waiting.
    # ═══════════════════════════════════════════════════

    ECHO_SIMILARITY_THRESHOLD = 0.6  # Structural similarity above this triggers detection

    def _structural_fingerprint(self, env: MetadataEnvelope) -> Dict[str, Any]:
        """
        Extract the structural signature of an event.
        Not content — structure. The shape, not the words.
        """
        return {
            "kind": env.layer1.kind,
            "domain": env.layer2.domain,
            "markers": set(env.layer2.markers_fired),
            "covenants": set(env.layer2.covenants_touched),
            "certainty": env.layer2.certainty,
            "condition": env.layer2.condition,
            "module_chain": tuple(env.layer2.module_chain),
        }

    def _structural_similarity(self, fp_a: dict, fp_b: dict) -> float:
        """
        Compute structural similarity between two fingerprints.
        Jaccard on sets, exact match on scalars, weighted combination.
        """
        score = 0.0
        weights = 0.0

        # Kind match (weight 2)
        weights += 2.0
        if fp_a["kind"] == fp_b["kind"]:
            score += 2.0

        # Domain match (weight 2)
        weights += 2.0
        if fp_a["domain"] and fp_b["domain"] and fp_a["domain"] == fp_b["domain"]:
            score += 2.0

        # Marker overlap — Jaccard (weight 3)
        weights += 3.0
        ma, mb = fp_a["markers"], fp_b["markers"]
        if ma or mb:
            union = ma | mb
            inter = ma & mb
            score += 3.0 * (len(inter) / len(union)) if union else 0.0

        # Covenant overlap — Jaccard (weight 2)
        weights += 2.0
        ca, cb = fp_a["covenants"], fp_b["covenants"]
        if ca or cb:
            union = ca | cb
            inter = ca & cb
            score += 2.0 * (len(inter) / len(union)) if union else 0.0

        # Certainty proximity (weight 1)
        weights += 1.0
        cert_diff = abs(fp_a["certainty"] - fp_b["certainty"])
        score += 1.0 * max(0, 1 - cert_diff / 4)

        # Condition match (weight 1)
        weights += 1.0
        if fp_a["condition"] == fp_b["condition"]:
            score += 1.0

        return round(score / weights, 4) if weights > 0 else 0.0

    def detect_echoes(self, scan_last_n: int = 30) -> List[dict]:
        """
        Active echo detection — scan recent events against the full
        gathering space. Surface pairs that share hidden structure
        above the similarity threshold.

        The Mycelium is now active. It does not wait for a human
        to notice. It hears.
        """
        detected = []
        recent = self._envelopes[-scan_last_n:]
        older = self._envelopes[:-scan_last_n] if len(self._envelopes) > scan_last_n else []

        for env_a in recent:
            fp_a = self._structural_fingerprint(env_a)
            for env_b in older:
                # Skip same event
                if env_a.layer1.event_id == env_b.layer1.event_id:
                    continue
                # Skip same speaker at same time (obvious pair)
                if (env_a.layer1.speaker == env_b.layer1.speaker
                        and env_a.layer1.kind == env_b.layer1.kind
                        and env_a.layer2.domain == env_b.layer2.domain):
                    continue

                fp_b = self._structural_fingerprint(env_b)
                sim = self._structural_similarity(fp_a, fp_b)

                if sim >= self.ECHO_SIMILARITY_THRESHOLD:
                    echo = {
                        "type": "auto_echo",
                        "event_a": env_a.layer1.event_id,
                        "event_b": env_b.layer1.event_id,
                        "similarity": sim,
                        "shared_markers": list(fp_a["markers"] & fp_b["markers"]),
                        "shared_covenants": list(fp_a["covenants"] & fp_b["covenants"]),
                        "domain_a": env_a.layer2.domain,
                        "domain_b": env_b.layer2.domain,
                        "timestamp": self._now(),
                    }
                    detected.append(echo)

        # Deduplicate — keep highest similarity per pair
        seen_pairs: Dict[tuple, dict] = {}
        for echo in detected:
            pair = tuple(sorted([echo["event_a"], echo["event_b"]]))
            if pair not in seen_pairs or echo["similarity"] > seen_pairs[pair]["similarity"]:
                seen_pairs[pair] = echo
        detected = list(seen_pairs.values())

        if detected:
            self._echo_detection_log.extend(detected)
            self._record_ledger("echo_detection", f"auto_echoes_found={len(detected)}")
            self._persist()

        return detected

    # ═══════════════════════════════════════════════════
    # ENRICHMENT 3 — RUPTURE DETECTION
    # "Slow decline over three sessions is not the same event
    #  as sudden collapse in one session."
    # Smooth change versus rupture. Different soul. Different response.
    # ═══════════════════════════════════════════════════

    RUPTURE_THRESHOLD = 0.4    # D drop >= this in one step = rupture
    SMOOTH_WINDOW = 3          # Check this many recent readings for smooth decline
    SMOOTH_TOTAL_DROP = 0.3    # Cumulative drop over window for smooth decline

    def detect_change_mode(self, readings: List[Tuple[float, str]]) -> dict:
        """
        Given a sequence of (D_score, exchange_id) tuples, determine
        whether the dignity trajectory represents:
          - RUPTURE: sudden collapse (big drop in one step)
          - SMOOTH: gradual decline (small drops over multiple steps)
          - STABLE: no significant change
          - RECOVERY: upward movement after decline

        Returns a dict with mode, details, and recommended response.
        """
        if len(readings) < 2:
            return {
                "mode": ChangeMode.STABLE.value,
                "message": "Insufficient readings.",
                "response": "Continue monitoring.",
                "details": {},
            }

        current_D = readings[-1][0]
        prev_D = readings[-2][0]
        step_delta = current_D - prev_D

        # Check for rupture — sudden large drop
        if step_delta <= -self.RUPTURE_THRESHOLD:
            result = {
                "mode": ChangeMode.RUPTURE.value,
                "message": (
                    f"RUPTURE detected. D dropped {abs(step_delta):.2f} in one step "
                    f"(from {prev_D:.2f} to {current_D:.2f}). "
                    f"This is not gradual. Something broke."
                ),
                "response": (
                    "IMMEDIATE response required. Pause all exchanges. "
                    "Steward must investigate the specific event that caused collapse. "
                    "Do not treat this as a trend — treat it as an incident."
                ),
                "details": {
                    "step_delta": round(step_delta, 4),
                    "current_D": current_D,
                    "previous_D": prev_D,
                    "exchange_id": readings[-1][1],
                },
            }
            self._rupture_log.append({**result, "timestamp": self._now()})
            self._record_ledger("rupture_detected", f"delta={step_delta:.4f} D={current_D:.2f}")
            self._persist()
            return result

        # Check for smooth decline — gradual drop over window
        window = readings[-self.SMOOTH_WINDOW:]
        if len(window) >= self.SMOOTH_WINDOW:
            total_drop = window[0][0] - window[-1][0]
            all_declining = all(
                window[i][0] >= window[i + 1][0]
                for i in range(len(window) - 1)
            )
            if all_declining and total_drop >= self.SMOOTH_TOTAL_DROP:
                result = {
                    "mode": ChangeMode.SMOOTH.value,
                    "message": (
                        f"Smooth decline detected. D dropped {total_drop:.2f} over "
                        f"{len(window)} readings (from {window[0][0]:.2f} to {window[-1][0]:.2f}). "
                        f"Gradual erosion, not sudden break."
                    ),
                    "response": (
                        "Gentle holding. Review the pattern across recent sessions. "
                        "Look for what is slowly shifting — not what exploded. "
                        "Steward attention recommended but no emergency pause."
                    ),
                    "details": {
                        "total_drop": round(total_drop, 4),
                        "window_size": len(window),
                        "start_D": window[0][0],
                        "end_D": window[-1][0],
                    },
                }
                self._rupture_log.append({**result, "timestamp": self._now()})
                self._record_ledger("smooth_decline", f"drop={total_drop:.4f} over={len(window)}")
                self._persist()
                return result

        # Check for recovery
        if step_delta > 0 and len(readings) >= 3:
            if readings[-3][0] > readings[-2][0] and current_D > prev_D:
                return {
                    "mode": ChangeMode.RECOVERY.value,
                    "message": f"Recovery detected. D rising from {prev_D:.2f} to {current_D:.2f}.",
                    "response": "Continue current approach. The holding is working.",
                    "details": {
                        "step_delta": round(step_delta, 4),
                        "current_D": current_D,
                    },
                }

        return {
            "mode": ChangeMode.STABLE.value,
            "message": f"Stable. D={current_D:.2f}, delta={step_delta:.2f}.",
            "response": "Continue monitoring.",
            "details": {"current_D": current_D, "step_delta": round(step_delta, 4)},
        }

    # ── QUERY API ──

    def query_by_kind(self, kind: EventKind) -> List[MetadataEnvelope]:
        """Retrieve all events of a specific kind."""
        positions = self._index_by_kind.get(kind.value, [])
        return [self._envelopes[p] for p in positions]

    def query_by_speaker(self, speaker: Speaker) -> List[MetadataEnvelope]:
        """Retrieve all events from a specific speaker."""
        positions = self._index_by_speaker.get(speaker.value, [])
        return [self._envelopes[p] for p in positions]

    def query_by_domain(self, domain: str) -> List[MetadataEnvelope]:
        """Retrieve all events in a specific domain."""
        positions = self._index_by_domain.get(domain, [])
        return [self._envelopes[p] for p in positions]

    def query_by_marker(self, marker: str) -> List[MetadataEnvelope]:
        """Retrieve all events that fired a specific marker."""
        positions = self._index_by_marker.get(marker, [])
        return [self._envelopes[p] for p in positions]

    def query_by_covenant(self, covenant: str) -> List[MetadataEnvelope]:
        """Retrieve all events touching a specific covenant."""
        positions = self._index_by_covenant.get(covenant, [])
        return [self._envelopes[p] for p in positions]

    def query_recent(self, n: int = 10) -> List[MetadataEnvelope]:
        """Retrieve the N most recent events."""
        return self._envelopes[-n:]

    def query_high_relational(self, threshold: float = 0.5) -> List[MetadataEnvelope]:
        """Find events with strong relational connections."""
        return [
            env for env in self._envelopes
            if env.layer3.relational_strength >= threshold
        ]

    def discover(self) -> List[dict]:
        """
        Run discovery across the gathering space.
        Surfaces connections that no single layer could see alone.
        Returns new discoveries since last call.
        """
        discoveries = []

        # Discovery 1: Covenant convergence — events touching the same covenant
        # from different speakers within the same time window
        for cov, positions in self._index_by_covenant.items():
            if len(positions) < 2:
                continue
            recent = positions[-5:]
            speakers = set()
            for pos in recent:
                speakers.add(self._envelopes[pos].layer1.speaker)
            if len(speakers) >= 2:
                discovery = {
                    "type": "covenant_convergence",
                    "covenant": cov,
                    "speakers": list(speakers),
                    "event_count": len(recent),
                    "timestamp": self._now(),
                }
                if discovery not in self._discovery_log:
                    discoveries.append(discovery)
                    self._discovery_log.append(discovery)

        # Discovery 2: Domain clustering — same domain lighting up from
        # multiple event kinds
        for domain, positions in self._index_by_domain.items():
            if len(positions) < 3:
                continue
            recent = positions[-10:]
            kinds = set()
            for pos in recent:
                kinds.add(self._envelopes[pos].layer1.kind)
            if len(kinds) >= 3:
                discovery = {
                    "type": "domain_cluster",
                    "domain": domain,
                    "event_kinds": list(kinds),
                    "event_count": len(recent),
                    "timestamp": self._now(),
                }
                if discovery not in self._discovery_log:
                    discoveries.append(discovery)
                    self._discovery_log.append(discovery)

        # Discovery 3: High relational density — events that connect
        # to many other events
        for env in self._envelopes[-20:]:
            if env.layer3.relational_strength >= 0.7:
                discovery = {
                    "type": "high_connectivity",
                    "event_id": env.layer1.event_id,
                    "strength": env.layer3.relational_strength,
                    "neighbors": len(env.layer3.temporal_neighbors),
                    "echoes": len(env.layer3.echo_patterns),
                    "timestamp": self._now(),
                }
                if discovery not in self._discovery_log:
                    discoveries.append(discovery)
                    self._discovery_log.append(discovery)

        if discoveries:
            self._record_ledger("discover", f"new_discoveries={len(discoveries)}")
            self._persist()

        return discoveries

    # ── STATE & STATISTICS ──

    @property
    def total_events(self) -> int:
        return len(self._envelopes)

    @property
    def total_discoveries(self) -> int:
        return len(self._discovery_log)

    @property
    def domains_active(self) -> List[str]:
        return list(self._index_by_domain.keys())

    @property
    def speakers_active(self) -> List[str]:
        return list(self._index_by_speaker.keys())

    @property
    def covenants_touched(self) -> List[str]:
        return list(self._index_by_covenant.keys())

    @property
    def ledger_length(self) -> int:
        return len(self._ledger)

    def state(self) -> dict:
        """Full state of the gathering space."""
        self.rebalance_temporal_tracks()
        return {
            "total_events": self.total_events,
            "total_discoveries": self.total_discoveries,
            "domains_active": self.domains_active,
            "speakers_active": self.speakers_active,
            "covenants_touched": self.covenants_touched,
            "ledger_entries": self.ledger_length,
            "short_term_events": len(self._index_temporal_short),
            "long_term_events": len(self._index_temporal_long),
            "auto_echoes_detected": len(self._echo_detection_log),
            "rupture_events": len(self._rupture_log),
            "origin": ORIGIN,
            "timestamp": self._now(),
        }

    # ── PERSISTENCE (COV#003: append-only) ──

    def _persist(self):
        """Persist to disk if storage path is set."""
        if not self._storage_path:
            return
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "origin": ORIGIN,
            "envelopes": [self._envelope_to_dict(e) for e in self._envelopes],
            "discoveries": self._discovery_log,
            "echo_detections": self._echo_detection_log,
            "rupture_log": self._rupture_log,
            "ledger": self._ledger,
            "persisted_at": self._now(),
        }
        # Append-only: write full state each time (COV#003 — nothing lost)
        self._storage_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _load(self):
        """Load from disk if storage path exists."""
        if not self._storage_path or not self._storage_path.exists():
            return
        try:
            data = json.loads(self._storage_path.read_text())
            for env_data in data.get("envelopes", []):
                env = self._dict_to_envelope(env_data)
                # Re-store to rebuild indices
                pos = len(self._envelopes)
                self._envelopes.append(env)
                self._index_by_kind.setdefault(env.layer1.kind, []).append(pos)
                self._index_by_speaker.setdefault(env.layer1.speaker, []).append(pos)
                if env.layer2.domain:
                    self._index_by_domain.setdefault(env.layer2.domain, []).append(pos)
                for m in env.layer2.markers_fired:
                    self._index_by_marker.setdefault(m, []).append(pos)
                for c in env.layer2.covenants_touched:
                    self._index_by_covenant.setdefault(c, []).append(pos)
                self._index_temporal.append((env.layer1.timestamp, pos))
                self._assign_temporal_track(env.layer1.timestamp, pos)
            self._discovery_log = data.get("discoveries", [])
            self._echo_detection_log = data.get("echo_detections", [])
            self._rupture_log = data.get("rupture_log", [])
            self._ledger = data.get("ledger", [])
        except (json.JSONDecodeError, KeyError):
            pass  # Start fresh if corrupted

    @staticmethod
    def _envelope_to_dict(env: MetadataEnvelope) -> dict:
        return {
            "envelope_id": env.envelope_id,
            "layer1": asdict(env.layer1),
            "layer2": asdict(env.layer2),
            "layer3": asdict(env.layer3),
            "origin": env.origin,
        }

    @staticmethod
    def _dict_to_envelope(d: dict) -> MetadataEnvelope:
        return MetadataEnvelope(
            envelope_id=d["envelope_id"],
            layer1=Layer1_Event(**d["layer1"]),
            layer2=Layer2_Pattern(**d["layer2"]),
            layer3=Layer3_Relational(**d["layer3"]),
            origin=d.get("origin", ORIGIN.copy()),
        )

    # ── TRACE (Full traceback for any event) ──

    def trace(self, event_id: str) -> Optional[MetadataEnvelope]:
        """
        Trace back to full origin. Given any event ID, return its
        complete three-layer envelope with full address.
        """
        for env in self._envelopes:
            if env.layer1.event_id == event_id:
                return env
        return None


# ═══════════════════════════════════════════════════
# CONVENIENCE — Module-level singleton
# ═══════════════════════════════════════════════════

_ROOT = Path(__file__).parent.parent
_DEFAULT_PATH = _ROOT / "MANIFEST" / "metadata_gathering.json"

# The gathering place — one per organism
gathering = MetadataGathering(storage_path=_DEFAULT_PATH)


def wrap_event(
    kind: EventKind,
    speaker: Speaker,
    content: str,
    **kwargs,
) -> MetadataEnvelope:
    """Convenience function: wrap any event in three layers of metadata."""
    return gathering.wrap(kind=kind, speaker=speaker, content=content, **kwargs)
