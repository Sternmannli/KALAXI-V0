"""
ninth_operator.py — ⟲ The Word
PLAN-001 Layer 3: The loop between dignity and witnessing.
The Word is the energy. The loop is the wire. Dignity is the insulator.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional
import uuid


class WordState(Enum):
    RECEIVED = "received"
    WITNESSING = "witnessing"
    WITNESSED = "witnessed"
    RETURNED = "returned"
    SHELTERED = "sheltered"       # dignity failed — word is held safely, never discarded


@dataclass
class Word:
    """The atomic unit. Not data. Not pattern. The Word."""
    word_id: str
    content: str                   # the donor's offering
    donor_context: str             # who gave it and why
    state: WordState = WordState.RECEIVED
    dignity_passed: bool = False
    witness_mark: Optional[str] = None    # what witnessing added
    sheltered_reason: Optional[str] = None
    received_at: datetime = field(default_factory=datetime.utcnow)
    witnessed_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None


class NinthOperator:
    """
    ⟲ The Ninth Operator — The Word

    The loop: Word → Dignity Filter → Witnessing → Changed Word → Return

    If dignity fails at any point, the word enters shelter.
    Sheltered words are not discarded. They wait.
    """

    def __init__(self):
        self._words: Dict[str, Word] = {}
        self.words_received: int = 0
        self.words_witnessed: int = 0
        self.words_returned: int = 0
        self.words_sheltered: int = 0
        self.loop_completions: int = 0

    # ------------------------------------------------------------------
    # Step 1: Receive
    # ------------------------------------------------------------------
    def receive_word(self, content: str, donor_context: str) -> str:
        """Accept a word — a donor's offering. Returns the word_id."""
        word_id = f"W-{uuid.uuid4().hex[:8]}"
        w = Word(word_id=word_id, content=content, donor_context=donor_context)
        self._words[word_id] = w
        self.words_received += 1
        return word_id

    # ------------------------------------------------------------------
    # Step 2: Witness (passes through dignity filter)
    # ------------------------------------------------------------------
    def witness(self, word_id: str) -> Word:
        """
        The word passes through the dignity filter.
        If dignity holds (D = A × L × M, no zero), the word is witnessed
        and returns changed. If dignity fails, the word enters shelter.
        """
        w = self._words.get(word_id)
        if w is None:
            raise KeyError(f"Word {word_id} not found.")
        if w.state not in (WordState.RECEIVED,):
            raise ValueError(f"Word {word_id} is in state {w.state.value}, cannot witness.")

        w.state = WordState.WITNESSING

        # Dignity filter: D = A × L × M — any zero collapses to zero
        agency = self._check_agency(w)
        legibility = self._check_legibility(w)
        moral_standing = self._check_moral_standing(w)
        dignity = agency * legibility * moral_standing

        if dignity == 0:
            w.state = WordState.SHELTERED
            w.dignity_passed = False
            w.sheltered_reason = self._shelter_reason(agency, legibility, moral_standing)
            self.words_sheltered += 1
            return w

        # Dignity holds — witnessing happens
        w.dignity_passed = True
        w.witness_mark = self._create_witness_mark(w)
        w.state = WordState.WITNESSED
        w.witnessed_at = datetime.utcnow()
        self.words_witnessed += 1
        return w

    # ------------------------------------------------------------------
    # Step 3: Return
    # ------------------------------------------------------------------
    def return_word(self, word_id: str) -> Word:
        """The changed word returns to the donor. Loop completes."""
        w = self._words.get(word_id)
        if w is None:
            raise KeyError(f"Word {word_id} not found.")
        if w.state == WordState.SHELTERED:
            raise ValueError(f"Word {word_id} is sheltered. It cannot be returned until dignity is restored.")
        if w.state != WordState.WITNESSED:
            raise ValueError(f"Word {word_id} must be witnessed before return (current: {w.state.value}).")

        w.state = WordState.RETURNED
        w.returned_at = datetime.utcnow()
        self.words_returned += 1
        self.loop_completions += 1
        return w

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------
    def loop_state(self) -> dict:
        """Current state of the loop."""
        by_state = {}
        for w in self._words.values():
            by_state.setdefault(w.state.value, []).append(w.word_id)
        return {
            "words_received": self.words_received,
            "words_witnessed": self.words_witnessed,
            "words_returned": self.words_returned,
            "words_sheltered": self.words_sheltered,
            "loop_completions": self.loop_completions,
            "words_by_state": by_state,
        }

    def get_word(self, word_id: str) -> Optional[Word]:
        return self._words.get(word_id)

    def sheltered_words(self):
        """List all words currently in shelter."""
        return [w for w in self._words.values() if w.state == WordState.SHELTERED]

    # ------------------------------------------------------------------
    # Internal: Dignity checks
    # ------------------------------------------------------------------
    def _check_agency(self, w: Word) -> float:
        """Agency: the donor chose freely to offer. Content present = 1.0."""
        return 1.0 if w.content.strip() else 0.0

    def _check_legibility(self, w: Word) -> float:
        """Legibility: the word can be understood. Context present = 1.0."""
        return 1.0 if w.donor_context.strip() else 0.0

    def _check_moral_standing(self, w: Word) -> float:
        """Moral standing: the word does not violate sealed gate."""
        # Sealed Gate: forced erasure, cognitive torture, depersonalization
        # Placeholder — in production this calls sealed_gate.py
        return 1.0

    def _shelter_reason(self, a: float, l: float, m: float) -> str:
        reasons = []
        if a == 0:
            reasons.append("agency=0 (empty offering)")
        if l == 0:
            reasons.append("legibility=0 (no context)")
        if m == 0:
            reasons.append("moral_standing=0 (sealed gate violation)")
        return "; ".join(reasons)

    def _create_witness_mark(self, w: Word) -> str:
        """What witnessing adds to the word. The word returns changed."""
        word_count = len(w.content.split())
        if word_count <= 3:
            return "Witnessed: a seed — small, complete."
        elif word_count <= 20:
            return "Witnessed: a held shape — clear enough to carry."
        else:
            return "Witnessed: a landscape — it took room to arrive."


# ---------------------------------------------------------------------------
# Scaffold: runnable demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    op = NinthOperator()

    # A word arrives
    wid = op.receive_word(
        content="The wound became the womb.",
        donor_context="First offering at the threshold."
    )
    print(f"Received: {wid}")

    # Witness it
    w = op.witness(wid)
    print(f"State: {w.state.value} | Dignity passed: {w.dignity_passed}")
    print(f"Witness mark: {w.witness_mark}")

    # Return it
    w = op.return_word(wid)
    print(f"State: {w.state.value} | Loop complete: {op.loop_completions}")

    # A word without context — will be sheltered
    wid2 = op.receive_word(content="help", donor_context="")
    w2 = op.witness(wid2)
    print(f"\nSheltered word: {wid2} | Reason: {w2.sheltered_reason}")

    # Loop state
    print(f"\nLoop state: {op.loop_state()}")

# [V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
