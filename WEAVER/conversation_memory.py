#!/usr/bin/env python3
"""
conversation_memory.py — Short-term pattern tracking across turns.

The system must know what the donor keeps returning to.
Not storage (that is InputLedger). Not state (that is Turn).
This is awareness — the conversation's shape as it unfolds.

After 5 turns about a separated father: dominant_register=grief,
recurring_themes=[children], confidence_trend=stable.

The organism reads this before responding. Each response is
contextual, not random.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import Counter
from datetime import datetime, timezone


@dataclass
class TurnSnapshot:
    """What the system understood from one turn."""
    exchange_id: str
    register: str              # grief, dignity, greeting, crisis, general
    themes: List[str]          # [children, separation, institutions, ...]
    confidence: float          # 0.0-1.0 — how confident the detection was
    dignity_score: float       # D from dignity check
    canon_sources: List[str]   # which canon fragments were used in response
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class ConversationSnapshot:
    """The shape of the conversation so far."""
    dominant_register: str = "general"
    recurring_themes: List[str] = field(default_factory=list)
    confidence_trend: str = "stable"  # rising, stable, falling
    turn_count: int = 0
    dignity_trend: str = "stable"     # rising, stable, falling

    def to_dict(self) -> dict:
        return {
            "dominant_register": self.dominant_register,
            "recurring_themes": self.recurring_themes,
            "confidence_trend": self.confidence_trend,
            "turn_count": self.turn_count,
            "dignity_trend": self.dignity_trend,
        }


class ConversationMemory:
    """
    Tracks patterns across turns within a conversation.

    Not a database. Not a ledger. A living awareness of
    what the donor keeps returning to, what register
    dominates, and how confidence moves.
    """

    def __init__(self, max_turns: int = 50):
        self._turns: List[TurnSnapshot] = []
        self._max_turns = max_turns

    def record_turn(self, snapshot: TurnSnapshot) -> None:
        """Record one turn's understanding."""
        self._turns.append(snapshot)
        # Keep only the most recent turns
        if len(self._turns) > self._max_turns:
            self._turns = self._turns[-self._max_turns:]

    @property
    def turn_count(self) -> int:
        return len(self._turns)

    @property
    def dominant_register(self) -> str:
        """The most frequent register across all turns."""
        if not self._turns:
            return "general"
        counts = Counter(t.register for t in self._turns)
        return counts.most_common(1)[0][0]

    @property
    def recurring_themes(self) -> List[str]:
        """Themes that appear in more than one turn."""
        if not self._turns:
            return []
        theme_counts: Counter = Counter()
        for t in self._turns:
            theme_counts.update(t.themes)
        return [theme for theme, count in theme_counts.most_common()
                if count > 1]

    @property
    def confidence_trend(self) -> str:
        """Rising, stable, or falling confidence over recent turns."""
        return self._compute_trend([t.confidence for t in self._turns])

    @property
    def dignity_trend(self) -> str:
        """Rising, stable, or falling dignity over recent turns."""
        return self._compute_trend([t.dignity_score for t in self._turns])

    def snapshot(self) -> ConversationSnapshot:
        """Current conversation shape — pass this to witness records."""
        return ConversationSnapshot(
            dominant_register=self.dominant_register,
            recurring_themes=self.recurring_themes,
            confidence_trend=self.confidence_trend,
            turn_count=self.turn_count,
            dignity_trend=self.dignity_trend,
        )

    def to_dict(self) -> dict:
        """Full serialization for persistence."""
        return {
            "turns": [
                {
                    "exchange_id": t.exchange_id,
                    "register": t.register,
                    "themes": t.themes,
                    "confidence": t.confidence,
                    "dignity_score": t.dignity_score,
                    "canon_sources": t.canon_sources,
                    "timestamp": t.timestamp,
                }
                for t in self._turns
            ],
            "snapshot": self.snapshot().to_dict(),
        }

    @staticmethod
    def _compute_trend(values: List[float]) -> str:
        """Compute trend from a list of values."""
        if len(values) < 2:
            return "stable"
        # Look at the last 5 values
        recent = values[-5:]
        if len(recent) < 2:
            return "stable"
        # Simple: compare average of first half to second half
        mid = len(recent) // 2
        first_half = sum(recent[:mid]) / max(mid, 1)
        second_half = sum(recent[mid:]) / max(len(recent) - mid, 1)
        diff = second_half - first_half
        if diff > 0.05:
            return "rising"
        elif diff < -0.05:
            return "falling"
        return "stable"
