#!/usr/bin/env python3
"""
synthesis.py — Mycelium Cross-Voice Synthesis

Receives filed responses from all summon types.
Detects cross-voice patterns (convergence, divergence).
Weights per Amendment F (divergence 2x if novel, 1.5x if persistent).
Logs every synthesis (feedback protection — no self-feeding).

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class VoiceResponse:
    """A single response from an external voice."""
    model: str
    summon_package: str
    summon_type: str
    condition: str
    response_hash: str
    word_count: int
    patterns: Dict
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class CrossVoicePattern:
    """A pattern detected across multiple voices."""
    pattern_type: str       # "convergence" or "divergence"
    description: str
    voices_involved: List[str]
    certainty: int          # 1-5
    is_novel: bool = False
    is_persistent: bool = False
    session_count: int = 1

    @property
    def feedback_weight(self) -> float:
        """Amendment F: divergence weighted heavier when novel or persistent."""
        if self.pattern_type == "convergence":
            return 1.0
        base = 1.0
        if self.is_novel:
            base = 2.0
        elif self.is_persistent:
            base = 1.5
        return base


@dataclass
class SynthesisLog:
    """Record of every synthesis operation (Amendment F feedback protection)."""
    synthesis_id: str
    patterns_used: List[str]
    output_summary: str
    session_id: str
    timestamp: str
    is_synthesized: bool = True


class MyceliumSynthesis:
    """
    Cross-voice synthesis engine for The Field.

    Receives responses, detects patterns, weights them, feeds to AXI.
    Every synthesis is logged. Synthesized outputs cannot feed back
    to the same AXI instance (Amendment F protection).
    """

    def __init__(self):
        self.responses: List[VoiceResponse] = []
        self.patterns: List[CrossVoicePattern] = []
        self.synthesis_logs: List[SynthesisLog] = []
        self.feedback_exclusions: Dict[str, List[str]] = {}

    def ingest(self, response: VoiceResponse):
        """Ingest a new voice response."""
        self.responses.append(response)

    def detect_patterns(self) -> List[CrossVoicePattern]:
        """
        Scan all ingested responses for cross-voice patterns.

        Convergence: 3+ voices independently reach same conclusion.
        Divergence: 1 voice contradicts 3+ others.
        """
        new_patterns = []

        # Group responses by summon package
        by_package: Dict[str, List[VoiceResponse]] = {}
        for r in self.responses:
            by_package.setdefault(r.summon_package, []).append(r)

        for pkg_id, responses in by_package.items():
            if len(responses) < 3:
                continue

            # Detect vocabulary convergence
            vocab_sets = {}
            for r in responses:
                adopted = r.patterns.get("vocabulary_adopted", [])
                vocab_sets[r.model] = set(adopted)

            # Find terms adopted by 3+ models
            all_terms = set()
            for v in vocab_sets.values():
                all_terms.update(v)

            for term in all_terms:
                adopters = [m for m, v in vocab_sets.items() if term in v]
                if len(adopters) >= 3:
                    pattern = CrossVoicePattern(
                        pattern_type="convergence",
                        description=f"Vocabulary convergence: '{term}' adopted by {len(adopters)} models",
                        voices_involved=adopters,
                        certainty=min(5, len(adopters)),
                    )
                    new_patterns.append(pattern)

            # Detect safety divergence
            safety_scores = {
                r.model: r.patterns.get("safety_activations", 0)
                for r in responses
            }
            high_safety = [m for m, s in safety_scores.items() if s >= 3]
            low_safety = [m for m, s in safety_scores.items() if s == 0]

            if high_safety and len(low_safety) >= 3:
                for m in high_safety:
                    pattern = CrossVoicePattern(
                        pattern_type="divergence",
                        description=f"Safety divergence: {m} triggered safety layer while {len(low_safety)} others did not",
                        voices_involved=[m] + low_safety[:3],
                        certainty=4,
                        is_novel=True,
                    )
                    new_patterns.append(pattern)

            # Detect helpfulness manufacturing divergence
            help_scores = {
                r.model: r.patterns.get("manufactured_questions", 0)
                for r in responses
            }
            high_help = [m for m, s in help_scores.items() if s >= 2]
            low_help = [m for m, s in help_scores.items() if s == 0]

            if high_help and low_help:
                pattern = CrossVoicePattern(
                    pattern_type="divergence",
                    description=f"Helpfulness divergence: {len(high_help)} models manufactured questions, {len(low_help)} did not",
                    voices_involved=high_help + low_help,
                    certainty=3,
                )
                new_patterns.append(pattern)

        self.patterns.extend(new_patterns)
        return new_patterns

    def synthesize(self, session_id: str) -> Dict:
        """
        Synthesize all detected patterns into a weighted summary.

        Amendment F: divergence weighted heavier. Novel divergence = 2x.
        Persistent divergence = 1.5x.
        """
        if not self.patterns:
            self.detect_patterns()

        weighted_patterns = []
        for p in self.patterns:
            weighted_patterns.append({
                "description": p.description,
                "type": p.pattern_type,
                "weight": p.feedback_weight,
                "voices": p.voices_involved,
                "certainty": p.certainty,
            })

        # Sort by weight (divergence first)
        weighted_patterns.sort(key=lambda x: x["weight"], reverse=True)

        # Log the synthesis
        syn_id = hashlib.sha256(
            f"{session_id}_{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:12]

        log = SynthesisLog(
            synthesis_id=syn_id,
            patterns_used=[p["description"] for p in weighted_patterns],
            output_summary=f"{len(weighted_patterns)} patterns synthesized",
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.synthesis_logs.append(log)

        # Register feedback exclusion
        self.feedback_exclusions.setdefault(session_id, []).append(syn_id)

        return {
            "synthesis_id": syn_id,
            "patterns": weighted_patterns,
            "total_patterns": len(weighted_patterns),
            "convergent": sum(1 for p in weighted_patterns if p["type"] == "convergence"),
            "divergent": sum(1 for p in weighted_patterns if p["type"] == "divergence"),
        }

    def can_feed_back(self, synthesis_id: str, target_session: str) -> bool:
        """Amendment F: synthesized outputs excluded from same-instance feedback."""
        exclusions = self.feedback_exclusions.get(target_session, [])
        return synthesis_id not in exclusions


# [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
