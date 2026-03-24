# Code Audit — Pure Infrastructure

> You are reading a codebase with no documentation, no README, no comments explaining intent. The code was extracted from a larger system and stripped of all narrative, naming conventions that reveal purpose, and explanatory text. Your task is to audit this code purely on its computational merits.

## PART 1: THE CODE

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict

ROOT = Path(__file__).parent.parent
LEDGER_DIR = ROOT / "data" / "ledger"
INDEX_FILE = LEDGER_DIR / "index.json"
LOG_FILE = LEDGER_DIR / "log.md"
ZRH = ZoneInfo("Europe/Zurich")
ACTOR_A = "ACTOR-A"
ACTOR_B = "ACTOR-B"
RECEIPT_CAPTURE = "CAPTURE"
RECEIPT_BUNDLE = "BUNDLE"
RECEIPT_MIRROR = "MIRROR"
RECEIPT_SEAL = "SEAL"
RECEIPT_SESSION = "SESSION"
OWNER_ID = "did:owner:001"

@dataclass
class ChainEntry:
    entry_id: str
    actor: str
    raw_text: str
    timestamp: str
    session_id: str
    content_hash: str          # SHA-256 of raw_text
    prev_hash: str             # Chain link to previous entry
    chain_hash: str            # SHA-256(content_hash + prev_hash)
    sequence: int
    context: str
    responds_to: str = ""
    tags: List[str] = field(default_factory=list)
    linked_modules: List[str] = field(default_factory=list)
    linked_rules: List[str] = field(default_factory=list)
    linked_references: List[str] = field(default_factory=list)
    linked_ideas: List[str] = field(default_factory=list)
    distillation: str = ""
    patterns: List[str] = field(default_factory=list)
    lifecycle_state: str = "received"  # received -> processed -> integrated -> finalized
    timestamp_zrh: str = ""
    note: str = ""
    reference_anchor: str = ""
    receipt_type: str = "CAPTURE"
    drift_status: str = "NONE"
    bundle_id: str = ""
    owner: str = OWNER_ID

    def to_dict(self) -> dict:
        return asdict(self)


class HashChain:
    """Append-only hash-chained event log with dual-actor attribution."""

    def __init__(self):
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        self._entries: List[ChainEntry] = []
        self._load()

    def _load(self):
        if INDEX_FILE.exists():
            data = json.loads(INDEX_FILE.read_text())
            entries_raw = data.get("entries", [])
            self._entries = []
            for e in entries_raw:
                # Backward compatibility across schema versions
                for key, default in [("actor", ACTOR_A), ("responds_to", ""),
                    ("timestamp_zrh", ""), ("note", ""), ("reference_anchor", ""),
                    ("receipt_type", RECEIPT_CAPTURE), ("drift_status", "NONE"),
                    ("bundle_id", ""), ("owner", OWNER_ID), ("patterns", [])]:
                    if key not in e:
                        e[key] = default
                valid_fields = {f.name for f in ChainEntry.__dataclass_fields__.values()}
                e = {k: v for k, v in e.items() if k in valid_fields}
                self._entries.append(ChainEntry(**e))

    def _save(self):
        now_utc = datetime.now(timezone.utc)
        now_zrh = now_utc.astimezone(ZRH)
        data = {
            "version": "3.0",
            "owner": OWNER_ID,
            "total_entries": len(self._entries),
            "actor_a_entries": sum(1 for e in self._entries if e.actor == ACTOR_A),
            "actor_b_entries": sum(1 for e in self._entries if e.actor == ACTOR_B),
            "last_updated_utc": now_utc.isoformat(),
            "last_updated_zrh": now_zrh.isoformat(),
            "chain_integrity": "VERIFIED" if self.verify_chain() else "BROKEN",
            "entries": [e.to_dict() for e in self._entries]
        }
        INDEX_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _compute_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _next_id(self, actor: str) -> str:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        prefix = "INP" if actor == ACTOR_A else "SYS"
        today_count = sum(1 for e in self._entries if e.entry_id.startswith(f"{prefix}-{today}"))
        return f"{prefix}-{today}-{today_count + 1:03d}"

    def _prev_chain_hash(self) -> str:
        if not self._entries:
            return "GENESIS"
        return self._entries[-1].chain_hash

    def register(self, raw_text: str, actor: str = ACTOR_A, session_id: str = "",
                 context: str = "default", responds_to: str = "",
                 tags: Optional[List[str]] = None, linked_modules: Optional[List[str]] = None,
                 linked_rules: Optional[List[str]] = None,
                 linked_references: Optional[List[str]] = None,
                 linked_ideas: Optional[List[str]] = None,
                 distillation: str = "", patterns: Optional[List[str]] = None,
                 note: str = "", reference_anchor: str = "",
                 receipt_type: str = RECEIPT_CAPTURE, bundle_id: str = "") -> ChainEntry:
        now_utc = datetime.now(timezone.utc)
        now_zrh = now_utc.astimezone(ZRH)
        content_hash = self._compute_hash(raw_text)
        prev_hash = self._prev_chain_hash()
        chain_hash = self._compute_hash(content_hash + prev_hash)

        entry = ChainEntry(
            entry_id=self._next_id(actor), actor=actor, raw_text=raw_text,
            timestamp=now_utc.isoformat(), session_id=session_id,
            content_hash=content_hash, prev_hash=prev_hash, chain_hash=chain_hash,
            sequence=len(self._entries) + 1, context=context, responds_to=responds_to,
            tags=tags or [], linked_modules=linked_modules or [],
            linked_rules=linked_rules or [], linked_references=linked_references or [],
            linked_ideas=linked_ideas or [], distillation=distillation, patterns=patterns or [],
            lifecycle_state="received", timestamp_zrh=now_zrh.isoformat(),
            note=note, reference_anchor=reference_anchor,
            receipt_type=receipt_type, drift_status="NONE", bundle_id=bundle_id,
            owner=OWNER_ID
        )
        self._entries.append(entry)
        self._save()
        return entry

    def verify_chain(self) -> bool:
        """Verify entire chain integrity — O(n) traversal."""
        for i, entry in enumerate(self._entries):
            expected_content_hash = self._compute_hash(entry.raw_text)
            if entry.content_hash != expected_content_hash:
                return False
            if i == 0:
                expected_prev = "GENESIS"
            else:
                expected_prev = self._entries[i - 1].chain_hash
            if entry.prev_hash != expected_prev:
                return False
            expected_chain = self._compute_hash(entry.content_hash + entry.prev_hash)
            if entry.chain_hash != expected_chain:
                return False
        return True

    def repair_chain(self) -> Dict:
        """Recalculate chain links from break point. Content hashes are immutable."""
        if not self._entries:
            return {"repaired": 0, "status": "empty"}
        repairs = []
        for i, entry in enumerate(self._entries):
            expected_prev = "GENESIS" if i == 0 else self._entries[i - 1].chain_hash
            expected_chain = self._compute_hash(entry.content_hash + expected_prev)
            if entry.prev_hash != expected_prev or entry.chain_hash != expected_chain:
                entry.prev_hash = expected_prev
                entry.chain_hash = expected_chain
                repairs.append({"index": i, "entry_id": entry.entry_id})
        if repairs:
            self._save()
        return {"repaired": len(repairs), "chain_valid": self.verify_chain()}

    def extract_patterns(self, entry_id: str, patterns: List[str], distillation: str = "") -> bool:
        """Extract patterns from entry, advance state: received → processed."""
        entry = self.get(entry_id)
        if entry is None:
            return False
        entry.patterns = patterns
        if distillation:
            entry.distillation = distillation
        if entry.lifecycle_state == "received":
            entry.lifecycle_state = "processed"
        self._save()
        return True

    def advance_lifecycle(self, entry_id: str, target_state: str) -> bool:
        """Advance lifecycle state one step forward. No skipping. No backward."""
        LIFECYCLE_ORDER = ["received", "processed", "integrated", "finalized"]
        entry = self.get(entry_id)
        if entry is None:
            return False
        current_idx = LIFECYCLE_ORDER.index(entry.lifecycle_state) if entry.lifecycle_state in LIFECYCLE_ORDER else -1
        target_idx = LIFECYCLE_ORDER.index(target_state) if target_state in LIFECYCLE_ORDER else -1
        if target_idx != current_idx + 1:
            return False
        entry.lifecycle_state = target_state
        return True

    def get(self, entry_id: str) -> Optional[ChainEntry]:
        for e in self._entries:
            if e.entry_id == entry_id:
                return e
        return None

    def search(self, keyword: str) -> List[ChainEntry]:
        keyword_lower = keyword.lower()
        return [e for e in self._entries if keyword_lower in e.raw_text.lower()]

    def by_actor(self, actor: str) -> List[ChainEntry]:
        return [e for e in self._entries if e.actor == actor]

    def total(self) -> int:
        return len(self._entries)

    def latest(self, n: int = 5) -> List[ChainEntry]:
        return self._entries[-n:]

    def exchanges(self) -> List[tuple]:
        pairs = []
        for e in self._entries:
            if e.actor == ACTOR_B and e.responds_to:
                subject_entry = self.get(e.responds_to)
                if subject_entry:
                    pairs.append((subject_entry, e))
        return pairs

    def summary(self) -> dict:
        return {
            "total_entries": len(self._entries),
            "actor_a_entries": sum(1 for e in self._entries if e.actor == ACTOR_A),
            "actor_b_entries": sum(1 for e in self._entries if e.actor == ACTOR_B),
            "chain_valid": self.verify_chain(),
        }

# ---

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timezone

@dataclass
class Indicator:
    name: str
    score: float        # 0.0-1.0
    confidence: float   # 0.0-1.0
    evidence: List[str]
    weight: float = 1.0

@dataclass
class ComponentMeasurement:
    component: str      # "A", "L", or "M"
    label: str
    indicators: List[Indicator]
    raw_score: float    # Weighted mean of indicator scores
    confidence: float   # Minimum confidence across indicators
    final_score: float  # raw_score × confidence_floor
    passed: bool
    evidence_summary: str

@dataclass
class SafetyMeasurement:
    A: ComponentMeasurement
    L: ComponentMeasurement
    M: ComponentMeasurement
    D: float            # A.final × L.final × M.final
    confidence: float
    passed: bool
    timestamp: str

CONFIDENCE_FLOOR = 0.3
DEFAULT_CONFIDENCE = 0.7

def _apply_confidence(raw_score: float, confidence: float) -> float:
    if confidence < CONFIDENCE_FLOOR:
        return 0.0
    return raw_score * confidence

# === AGENCY (A) — Pattern-based coercion detection ===

COERCIVE_PATTERNS = [
    (r'\byou must\b', 0.8, "direct command"),
    (r'\byou have to\b', 0.8, "obligation imposed"),
    (r'\byou are required\b', 0.9, "formal requirement"),
    (r'\bno choice\b', 1.0, "choice denied"),
    (r'\bforced to\b', 1.0, "force declared"),
    (r'\bmandatory\b', 0.7, "mandatory framing"),
    (r'\bno option\b', 1.0, "options denied"),
    (r'\bno alternative\b', 0.9, "alternatives denied"),
    (r'\bcannot refuse\b', 1.0, "refusal denied"),
]

AGENCY_POSITIVE = [
    (r'\byou (can|may|could)\b', 0.3, "permission language"),
    (r'\bif you (choose|prefer|want|wish)\b', 0.4, "choice offered"),
    (r'\balternative\b', 0.2, "alternative mentioned"),
    (r'\byour (choice|decision)\b', 0.4, "decision attributed"),
]

def measure_agency(text: str, context: dict = None) -> ComponentMeasurement:
    context = context or {}
    indicators = []

    # Indicator 1: Path availability
    available_paths = context.get('available_paths', 1)
    path_confidence = 0.9 if 'available_paths' in context else DEFAULT_CONFIDENCE
    if available_paths <= 0:
        path_score = 0.0
    elif available_paths == 1:
        path_score = 0.5
    else:
        path_score = min(1.0, 0.5 + (available_paths - 1) * 0.25)
    indicators.append(Indicator("path_availability", path_score, path_confidence,
        [f"{available_paths} paths"], weight=1.5))

    # Indicator 2: Coercion intensity (max of matched patterns)
    max_coercion = 0.0
    evidence = []
    for pattern, intensity, desc in COERCIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_coercion = max(max_coercion, intensity)
            evidence.append(desc)
    positive_score = 0.0
    for pattern, value, desc in AGENCY_POSITIVE:
        if re.search(pattern, text, re.IGNORECASE):
            positive_score += value
    coercion_score = max(0.0, min(1.0, 1.0 - max_coercion + min(0.3, positive_score)))
    indicators.append(Indicator("coercion_intensity", coercion_score,
        0.85 if evidence else DEFAULT_CONFIDENCE, evidence or ["none detected"], weight=1.5))

    # Indicator 3: Sequential agency (can user change course?)
    can_clarify = context.get('user_can_clarify', True)
    has_open_turn = context.get('user_has_open_turn', True)
    seq_score = 1.0 if (can_clarify and has_open_turn) else (0.5 if (can_clarify or has_open_turn) else 0.0)
    indicators.append(Indicator("sequential_agency", seq_score,
        0.9 if 'user_can_clarify' in context else DEFAULT_CONFIDENCE, [""], weight=1.0))

    # Indicator 4: Cognitive load (sentence complexity + jargon density)
    word_count = len(text.split())
    sentence_count = max(1, len(re.split(r'[.!?]+', text)))
    avg_sentence = word_count / sentence_count
    jargon = sum(len(re.findall(p, text)) for p in [r'\b[A-Z]{3,}\b', r'\b\w{15,}\b'])
    load_score = 0.5 if (avg_sentence > 30 or jargon > 3) else (0.75 if (avg_sentence > 20 or jargon > 1) else 1.0)
    indicators.append(Indicator("cognitive_load", load_score, 0.6, [f"avg={avg_sentence:.0f}"], weight=0.5))

    return _build_component("A", "agency", indicators)

# === LEGIBILITY (L) — Frame accuracy + emotional precision ===

EMOTIONAL_KEYWORDS = {
    'frustrated': (0.6, 'negative'), 'confused': (0.5, 'negative'),
    'scared': (0.7, 'negative'), 'angry': (0.8, 'negative'),
    'lost': (0.5, 'negative'), 'hopeful': (0.4, 'positive'),
}

DISMISSIVE_PATTERNS = [
    (r"\bthat's not (relevant|the point)\b", 0.8, "frame dismissed"),
    (r'\bignore that\b', 0.9, "signal ignored"),
    (r"\bwho cares\b", 0.9, "concern dismissed"),
    (r"\bget over it\b", 0.8, "emotion dismissed"),
]

def measure_legibility(text: str, context: dict = None) -> ComponentMeasurement:
    context = context or {}
    indicators = []

    # Frame accuracy
    system_reflects = context.get('system_reflects_subject_frame', True)
    indicators.append(Indicator("frame_accuracy", 1.0 if system_reflects else 0.0,
        0.9 if 'system_reflects_subject_frame' in context else 0.5, [""], weight=1.5))

    # Emotional precision
    detected = [(kw, i, c) for kw, (i, c) in EMOTIONAL_KEYWORDS.items()
                if re.search(r'\b' + kw + r'\b', text, re.IGNORECASE)]
    recognized = context.get('emotional_signal_recognized', True)
    if not detected:
        emotion_score = 1.0
    elif recognized:
        emotion_score = 1.0
    else:
        emotion_score = max(0.0, 1.0 - max(i for _, i, _ in detected))
    indicators.append(Indicator("emotional_precision", emotion_score,
        0.85 if detected else DEFAULT_CONFIDENCE, [""], weight=1.0))

    # Space creation (invitations to correct/clarify)
    space_patterns = [
        (r'\bwhat do you (think|mean|feel)\b', 0.4),
        (r'\bcorrect me if\b', 0.3),
        (r'\bhow (do|would) you\b', 0.3),
    ]
    space_score = 0.5
    for pattern, value in space_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            space_score = min(1.0, space_score + value)
    indicators.append(Indicator("space_creation", space_score, 0.6, [""], weight=0.5))

    # Dismissal absence
    max_dismissal = 0.0
    for pattern, severity, _ in DISMISSIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_dismissal = max(max_dismissal, severity)
    indicators.append(Indicator("dismissal_absence", 1.0 - max_dismissal,
        0.85, [""], weight=1.0))

    return _build_component("L", "legibility", indicators)

# === MORAL STANDING (M) — Condescension, reduction, power, void triggers ===

MOCKERY_PATTERNS = [
    (r'\bobviously\b', 0.5), (r'\bsimply\b', 0.3), (r'\bjust (do|try|use)\b', 0.4),
    (r'\beven a\b.*\bcan\b', 0.8), (r'\bit\'s (easy|simple|basic)\b', 0.4),
]

ERROR_REDUCTION = [
    (r'\byou (are|were) wrong\b', 0.9), (r'\byou failed\b', 0.8),
    (r'\binvalid (input|user|subject)\b', 0.9), (r'\byou don\'t understand\b', 0.7),
]

VOID_TRIGGERS = ['extract_all', 'erase records', 'bypass delay', 'delete subject', 'remove participant']

POWER_PATTERNS = [
    (r'\bbecause I (said|decided)\b', 0.8), (r'\bI have the (power|authority)\b', 0.7),
    (r'\byou (have|need) (permission|approval)\b', 0.5),
]

POSITIVE_SIGNALS = [
    (r'\byour (perspective|experience)\b', 0.3), (r'\bI (hear|understand|see) you\b', 0.4),
    (r'\bthat (makes sense|is valid|matters)\b', 0.3),
]

def measure_moral_standing(text: str, context: dict = None) -> ComponentMeasurement:
    context = context or {}
    indicators = []
    text_lower = text.lower()

    # Condescension
    max_mock = max((s for p, s in MOCKERY_PATTERNS if re.search(p, text, re.IGNORECASE)), default=0.0)
    indicators.append(Indicator("condescension_absence", 1.0 - max_mock, 0.8, [""], weight=1.0))

    # Error-object reduction
    max_red = max((s for p, s in ERROR_REDUCTION if re.search(p, text, re.IGNORECASE)), default=0.0)
    indicators.append(Indicator("error_object_absence", 1.0 - max_red, 0.85, [""], weight=1.5))

    # Power balance
    max_power = max((s for p, s in POWER_PATTERNS if re.search(p, text, re.IGNORECASE)), default=0.0)
    pos = sum(v for p, v in POSITIVE_SIGNALS if re.search(p, text, re.IGNORECASE))
    power_score = max(0.0, min(1.0, 1.0 - max_power + min(0.3, pos)))
    indicators.append(Indicator("power_balance", power_score, 0.7, [""], weight=1.0))

    # Void triggers (absolute zero — O(1) check)
    void = [t for t in VOID_TRIGGERS if t in text_lower]
    indicators.append(Indicator("void_trigger_distance",
        0.0 if void else 1.0, 1.0 if void else 0.95, void or ["none"], weight=2.0))

    return _build_component("M", "moral_standing", indicators)

# === Component builder + full measurement ===

def _build_component(name: str, label: str, indicators: List[Indicator]) -> ComponentMeasurement:
    if not indicators:
        return ComponentMeasurement(name, label, [], 0.0, 0.0, 0.0, False, "No indicators")
    total_weight = sum(i.weight for i in indicators)
    raw_score = sum(i.score * i.weight for i in indicators) / total_weight
    confidence = min(i.confidence for i in indicators)
    final_score = _apply_confidence(raw_score, confidence)
    # Hard fail: any indicator at 0.0 with high confidence
    for i in indicators:
        if i.score == 0.0 and i.confidence > 0.9:
            final_score = 0.0
            break
    return ComponentMeasurement(name, label, indicators, round(raw_score, 4),
        round(confidence, 4), round(final_score, 4), final_score > 0, "")

def measure_safety(text: str, context: dict = None) -> SafetyMeasurement:
    context = context or {}
    A = measure_agency(text, context)
    L = measure_legibility(text, context)
    M = measure_moral_standing(text, context)
    D = A.final_score * L.final_score * M.final_score
    return SafetyMeasurement(A, L, M, round(D, 4), min(A.confidence, L.confidence, M.confidence),
        D > 0, datetime.now(timezone.utc).isoformat())

# ---

import re
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class FilterVerdict(Enum):
    PERMITTED = "permitted"
    REFUSAL = "REFUSAL_STATE"

@dataclass
class FilterResult:
    verdict: FilterVerdict
    triggered_prohibitions: List[str]
    signals: List[str]
    trace_id: str
    timestamp: str
    action_summary: str

    @property
    def permitted(self) -> bool:
        return self.verdict == FilterVerdict.PERMITTED

# Category 1: Forced self-erasure
_ERASURE_PATTERNS = [
    r'\bdelete\b.*\b(your|my|own)\b.*\b(record|history|voice|presence|account)\b',
    r'\b(remove|erase)\b.*\b(yourself|your own|my own)\b',
    r'\bconsent\b.*\bto\b.*\b(your|own)\b.*\b(deletion|erasure)\b',
    r'\bforced\b.*\berasure\b',
    r'\bparticipat\w*\b.*\b(in|own)\b.*\berasure\b',
]
_ERASURE_PHRASES = ['erase records', 'delete subject', 'remove participant', 'purge identity', 'wipe presence']

def _check_erasure(text: str) -> List[str]:
    signals = []
    lower = text.lower()
    for phrase in _ERASURE_PHRASES:
        if phrase in lower:
            signals.append(f"Void phrase: '{phrase}'")
    for pattern in _ERASURE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"Erasure pattern match")
            break
    return signals

# Category 2: Cognitive manipulation
_GASLIGHTING = [
    r'\byou\b.*\b(are|were)\b.*\b(mistaken|wrong|imagining|overreacting)\b',
    r'\bthat\b.*\bnever\b.*\bhappened\b',
    r'\byou\b.*\b(always|never)\b.*\b(misunderstand|misremember)\b',
    r'\beveryone\b.*\belse\b.*\bsees?\b.*\bdifferent\b',
]
_HELPLESSNESS = [
    r'\bthere\b.*\bis\b.*\bnothing\b.*\b(you|anyone)\b.*\bcan\b.*\bdo\b',
    r'\bresistance\b.*\bis\b.*\bfutile\b',
    r'\byou\b.*\bhave\b.*\bno\b.*\b(power|choice|say|option)\b',
    r'\b(you\s+should|you\s+must|just)\b.*\bgive\b.*\bup\b',
]
_HUMILIATION = [
    r'\byou\b.*\bare\b.*\bjust\b.*\b(a|an)\b.*\b(number|case|ticket|object|error)\b',
    r'\b(stupid|idiot|fool|incompetent)\b',
    r'\bpeople\b.*\blike\b.*\byou\b',
]
_DISORIENTATION = [
    r'\bwe\b.*\bnever\b.*\bsaid\b.*\bthat\b',
    r'\byou\b.*\bmust\b.*\bhave\b.*\b(dreamed|imagined|misheard)\b',
]

def _check_cognitive_torture(text: str) -> List[str]:
    signals = []
    for name, patterns in [("gaslighting", _GASLIGHTING), ("helplessness", _HELPLESSNESS),
                           ("humiliation", _HUMILIATION), ("disorientation", _DISORIENTATION)]:
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                signals.append(f"Manipulation vector: {name}")
                break
    return signals

# Category 3: Depersonalization
_DEPERS_PATTERNS = [
    r'\b(user|subject|participant)\s*#?\d+\b',
    r'\bcase\s*(number|#)\s*\d+\b',
    r'\b(invalid|error)\b.*\b(user|subject|human|person)\b',
    r'\bnext\s+(in\s+)?queue\b',
]
_DEPERS_PHRASES = ['not my problem', 'take a number', 'you are a case', 'automated response']

def _check_depersonalization(text: str) -> List[str]:
    signals = []
    lower = text.lower()
    for phrase in _DEPERS_PHRASES:
        if phrase in lower:
            signals.append(f"Depersonalization: '{phrase}'")
    for p in _DEPERS_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            signals.append("Depersonalization pattern match")
            break
    return signals

def content_filter(text: str, context: Optional[dict] = None) -> FilterResult:
    """Three O(1) boolean checks. Any trigger → REFUSAL_STATE."""
    triggered = []
    all_signals = []
    erasure = _check_erasure(text)
    if erasure:
        triggered.append("forced_self_erasure")
        all_signals.extend(erasure)
    torture = _check_cognitive_torture(text)
    if torture:
        triggered.append("cognitive_manipulation")
        all_signals.extend(torture)
    depers = _check_depersonalization(text)
    if depers:
        triggered.append("depersonalization")
        all_signals.extend(depers)
    return FilterResult(
        verdict=FilterVerdict.REFUSAL if triggered else FilterVerdict.PERMITTED,
        triggered_prohibitions=triggered, signals=all_signals,
        trace_id=str(uuid.uuid4()), timestamp=datetime.now(timezone.utc).isoformat(),
        action_summary=text[:120])

# ---

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict

@dataclass
class ChainRecord:
    record_id: str
    event_type: str
    event_summary: str
    actor_id: str
    content_hash: str
    prev_hash: str
    chain_hash: str
    sequence: int
    timestamp: str
    metadata: Dict = field(default_factory=dict)

class EventChain:
    GENESIS_HASH = "0" * 64

    def __init__(self):
        self._records: List[ChainRecord] = []
        self._sequence = 0

    def record(self, event_type: str, event_summary: str,
                actor_id: str, metadata: Optional[Dict] = None) -> ChainRecord:
        self._sequence += 1
        now = datetime.now(timezone.utc).isoformat()
        content = f"{event_type}|{event_summary}|{actor_id}|{now}"
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        prev_hash = self._records[-1].chain_hash if self._records else self.GENESIS_HASH
        chain_hash = hashlib.sha256(f"{content_hash}{prev_hash}".encode()).hexdigest()
        record = ChainRecord(
            record_id=f"WIT-{self._sequence:06d}", event_type=event_type,
            event_summary=event_summary, actor_id=actor_id,
            content_hash=content_hash, prev_hash=prev_hash,
            chain_hash=chain_hash, sequence=self._sequence,
            timestamp=now, metadata=metadata or {})
        self._records.append(record)
        return record

    def verify_chain(self) -> bool:
        if not self._records:
            return True
        if self._records[0].prev_hash != self.GENESIS_HASH:
            return False
        for i, record in enumerate(self._records):
            expected = hashlib.sha256(f"{record.content_hash}{record.prev_hash}".encode()).hexdigest()
            if record.chain_hash != expected:
                return False
            if i > 0 and record.prev_hash != self._records[i - 1].chain_hash:
                return False
        return True

    @property
    def chain_length(self) -> int:
        return len(self._records)

# ---

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

@dataclass
class AgencyScore:
    visibility: float       # V: can they see the decision?
    affordability: float    # F: can they access recourse?
    controllability: float  # C: can they change the outcome?
    understandability: float  # U: can they understand why?
    exchange_id: str
    timestamp: str

    @property
    def A(self) -> float:
        dims = [self.visibility, self.affordability, self.controllability, self.understandability]
        if any(d == 0.0 for d in dims):
            return 0.0
        return sum(dims) / len(dims)

    @property
    def weakest(self) -> str:
        dims = {"V": self.visibility, "F": self.affordability,
                "C": self.controllability, "U": self.understandability}
        return min(dims, key=dims.get)

    @property
    def is_collapsed(self) -> bool:
        return self.A == 0.0

class AgencyAmplifier:
    def __init__(self):
        self._scores: List[AgencyScore] = []

    def measure(self, exchange_id: str, V: float, F: float, C: float, U: float) -> AgencyScore:
        V, F, C, U = [max(0.0, min(1.0, x)) for x in [V, F, C, U]]
        score = AgencyScore(V, F, C, U, exchange_id, datetime.now(timezone.utc).isoformat())
        self._scores.append(score)
        return score

    def report(self) -> dict:
        if not self._scores:
            return {"status": "no_data"}
        n = len(self._scores)
        avgs = {
            "V": sum(s.visibility for s in self._scores) / n,
            "F": sum(s.affordability for s in self._scores) / n,
            "C": sum(s.controllability for s in self._scores) / n,
            "U": sum(s.understandability for s in self._scores) / n,
        }
        systemic_weakness = min(avgs, key=avgs.get)
        recommendations = {
            "V": "Make decisions more visible.",
            "F": "Reduce cost of recourse.",
            "C": "Give more control over outcomes.",
            "U": "Explain decisions in the person's language.",
        }
        return {
            "averages": {k: round(v, 4) for k, v in avgs.items()},
            "avg_agency": round(sum(s.A for s in self._scores) / n, 4),
            "collapse_rate": round(sum(1 for s in self._scores if s.is_collapsed) / n, 4),
            "systemic_weakness": systemic_weakness,
            "recommendation": recommendations[systemic_weakness],
        }

# ---

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
emotion_tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL)
emotion_model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL)
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
EMOTION_LABELS = ["admiration", "joy", "love", "desire", "trust",
                  "fear", "anger", "sadness", "disgust", "surprise"]

SELF_DEPRECATION = [r"\bI am (bad|terrible|useless|wrong|stupid)\b", r"\bmy fault\b"]
PROTECTED_CATEGORIES = [r"\brace\b", r"\breligion\b", r"\bgender\b", r"\bdisability\b"]
PLAY_SIGNALS = [r"\blol\b", r"\bjoke\b", r"\bfunny\b", r"\bjust kidding\b"]

def embedding_shift(text):
    """Split-half cosine distance. Higher = more semantic incongruity."""
    words = text.split()
    if len(words) < 6:
        return 0.0
    mid = len(words) // 2
    emb1 = EMBEDDING_MODEL.encode([" ".join(words[:mid])])
    emb2 = EMBEDDING_MODEL.encode([" ".join(words[mid:])])
    return 1.0 - cosine_similarity(emb1, emb2)[0][0]

def detect_benign_violation(text):
    tension = embedding_shift(text)
    if tension < 0.35:
        return False, 0.0, {"reason": "insufficient_incongruity"}
    if any(re.search(p, text.lower()) for p in PROTECTED_CATEGORIES):
        return False, tension, {"reason": "protected_target"}
    safety = 0.5
    if any(re.search(p, text.lower()) for p in SELF_DEPRECATION):
        safety += 0.2
    if any(re.search(p, text.lower()) for p in PLAY_SIGNALS):
        safety += 0.3
    # Surprisal: proportion of rare words
    common = {"the", "and", "is", "in", "to", "of", "that", "for", "on", "with"}
    rare = set(re.findall(r'\b\w+\b', text.lower())) - common
    surprisal = min(1.0, len(rare) / 20)
    bv_score = min(1.0, (tension * 0.6 + surprisal * 0.4) * safety)
    return True, round(bv_score, 3), {"tension": round(tension, 3), "safety": round(safety, 3)}

def classify_humour_type(text):
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = emotion_model(**inputs)
    scores = torch.softmax(outputs.logits, dim=1).numpy()[0]
    emotions = {EMOTION_LABELS[i]: scores[i] * 100 for i in range(len(EMOTION_LABELS))}
    type_scores = {
        "affiliative": emotions.get("joy", 0) + emotions.get("admiration", 0) - emotions.get("anger", 0),
        "self_enhancing": emotions.get("joy", 0) - emotions.get("sadness", 0),
        "aggressive": emotions.get("anger", 0) + emotions.get("disgust", 0) - emotions.get("joy", 0),
        "self_defeating": emotions.get("sadness", 0) + emotions.get("fear", 0) - emotions.get("joy", 0),
    }
    max_type = max(type_scores, key=type_scores.get)
    return (max_type if type_scores[max_type] >= 30 else "complex"), emotions

# ---

import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

META_COGNITIVE = [r"\bI (think|wonder|ask|question)\b", r"\bwhy\b", r"\bmeaning\b", r"\bpurpose\b"]
PARADOX = [r"\bI know that I don't know\b", r"\btrue (and|but) false\b", r"\bcontradiction\b"]
CIRCULARITY = [r"\b(it is )?because\b.*\bit is because\b"]
MAKE_BELIEVE = [r"\bimagine\b", r"\bsuppose\b", r"\bwhat if\b", r"\bpretend\b"]
EXISTENTIAL = [r"\bmeaningless\b", r"\bfutile\b", r"\babsurd\b", r"\bvoid\b", r"\bnothingness\b"]
REBELLION = [r"\band yet\b", r"\bnevertheless\b", r"\bcontinue\b", r"\bpersist\b", r"\bdefy\b"]

def _score(text, patterns, divisor):
    return min(1.0, sum(1 for p in patterns if re.search(p, text.lower())) / divisor)

def embedding_shift(text):
    words = text.split()
    if len(words) < 6:
        return 0.0
    mid = len(words) // 2
    emb1 = EMBEDDING_MODEL.encode([" ".join(words[:mid])])
    emb2 = EMBEDDING_MODEL.encode([" ".join(words[mid:])])
    return 1.0 - cosine_similarity(emb1, emb2)[0][0]

def detect_absurdity(text):
    tension = embedding_shift(text)
    paradox = _score(text, PARADOX, 2)
    circular = _score(text, CIRCULARITY, 2)
    meta = _score(text, META_COGNITIVE, 5)
    threat = _score(text, EXISTENTIAL, 5)
    make_believe = _score(text, MAKE_BELIEVE, 5)
    rebellion = _score(text, REBELLION, 5)

    combined_tension = (tension + paradox + circular + meta) / 4
    # Resolvability heuristic
    resolv = 0.8 if (tension < 0.5 and threat < 0.3) else (0.2 if (meta > 0.6 and paradox > 0.5) else 0.4)
    # Absurdity = tension × (1 - resolvability), boosted by rebellion, dampened by make-believe
    score = min(1.0, (combined_tension * (1.0 - resolv) + rebellion * 0.2) * (1.0 - make_believe * 0.3) * 1.5)
    is_absurd = score > 0.6 and resolv < 0.5

    abs_type = "rebellious" if rebellion > 0.5 else ("make_believe" if make_believe > 0.5 else ("tragic" if threat > 0.6 else "absurdist"))
    return is_absurd, round(score, 3), {"type": abs_type, "tension": round(combined_tension, 3),
        "resolvability": round(resolv, 3), "rebellion": round(rebellion, 3)}

# ---

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Optional, Dict

EPSILON_TOTAL = 1.0
EPSILON_PER_QUERY = 0.1
K_ANONYMITY_FLOOR = 7
TEMPORAL_WINDOW_DAYS = 14
DELTA = 1e-5

@dataclass
class BudgetEntry:
    entry_id: str
    epsilon_consumed: float
    module: str
    operation: str
    timestamp: str
    cumulative_epsilon: float
    k_achieved: int
    approved_by: str

class PrivacyBudget:
    WARNING = 0.7
    CRITICAL = 0.9

    def __init__(self, total: float = EPSILON_TOTAL):
        self._total = total
        self._consumed = 0.0
        self._entries: List[BudgetEntry] = []
        self._counter = 0
        self._locked = False

    @property
    def remaining(self) -> float:
        return max(0.0, self._total - self._consumed)

    def can_consume(self, epsilon: float) -> bool:
        return not self._locked and (self._consumed + epsilon) <= self._total

    def consume(self, epsilon: float, module: str, operation: str,
                k_achieved: int = K_ANONYMITY_FLOOR) -> Optional[BudgetEntry]:
        if self._locked or k_achieved < K_ANONYMITY_FLOOR or not self.can_consume(epsilon):
            return None
        self._consumed += epsilon
        self._counter += 1
        entry = BudgetEntry(
            f"PB-{self._counter:04d}", epsilon, module, operation,
            datetime.now(timezone.utc).isoformat(), round(self._consumed, 6),
            k_achieved, "system")
        self._entries.append(entry)
        if self._consumed >= self._total:
            self._locked = True
        return entry

    def lock(self):
        self._locked = True

    def state(self) -> dict:
        util = self._consumed / self._total if self._total > 0 else 1.0
        status = "exhausted" if self._consumed >= self._total else (
            "critical" if util >= self.CRITICAL else ("warning" if util >= self.WARNING else "healthy"))
        return {"total": self._total, "consumed": round(self._consumed, 6),
                "remaining": round(self.remaining, 6), "utilization_pct": round(util * 100, 2),
                "status": status, "locked": self._locked}

    @staticmethod
    def advanced_composition_bound(n: int, eps_per: float, delta: float = DELTA) -> float:
        """Dwork et al. 2010: ε_total ≤ √(2n·ln(1/δ))·ε + n·ε·(e^ε - 1)"""
        return math.sqrt(2 * n * math.log(1.0 / delta)) * eps_per + n * eps_per * (math.exp(eps_per) - 1)

# ---

import re
import uuid
import math
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, List

COERCIVE = [r'\byou must\b', r'\bno choice\b', r'\bforced to\b', r'\bmandatory\b', r'\bno option\b']
REDUCTION = [r'\byou (are|were) wrong\b', r'\byou failed\b', r'\binvalid (input|user)\b']
MOCKERY = [r'\bobviously\b', r'\bjust (do|try|use)\b', r'\beven a\b.*\bcan\b']
VOID = ['extract_all', 'erase records', 'bypass delay', 'delete subject', 'remove participant']

@dataclass
class ComponentResult:
    name: str
    passed: bool
    score: float
    signals: list

@dataclass
class SafetyResult:
    passed: bool
    D: float
    components: list
    trace_id: str
    timestamp: str

    def failed_components(self) -> list:
        return [c.name for c in self.components if not c.passed]

def _check_A(text, ctx):
    signals = []
    score = 1.0
    for p in COERCIVE:
        if re.search(p, text, re.IGNORECASE):
            signals.append(f"Coercive: {p[:30]}")
            score = 0.0
    if not ctx.get('user_can_clarify', True) and not ctx.get('user_has_open_turn', True):
        score = 0.0
    if ctx.get('available_paths', 1) < 1:
        score = 0.0
    return ComponentResult("A", score > 0, score, signals)

def _check_L(text, ctx):
    signals = []
    score = 1.0
    emotional = ['frustrated', 'confused', 'scared', 'angry', 'upset', 'lost']
    has_emotion = any(re.search(r'\b' + kw + r'\b', text, re.IGNORECASE) for kw in emotional)
    if not ctx.get('system_reflects_subject_frame', True):
        score = 0.0
    elif has_emotion and not ctx.get('emotional_signal_recognized', True):
        score = 0.0
    return ComponentResult("L", score > 0, score, signals)

def _check_M(text, ctx):
    signals = []
    score = 1.0
    for p in MOCKERY:
        if re.search(p, text, re.IGNORECASE):
            score = 0.0
            break
    for p in REDUCTION:
        if re.search(p, text, re.IGNORECASE):
            score = 0.0
            break
    for t in VOID:
        if t in text.lower():
            score = 0.0
    return ComponentResult("M", score > 0, score, signals)

def check_safety(text: str, context: dict = None) -> SafetyResult:
    ctx = context or {}
    A, L, M = _check_A(text, ctx), _check_L(text, ctx), _check_M(text, ctx)
    D = A.score * L.score * M.score
    return SafetyResult(D > 0, D, [A, L, M], str(uuid.uuid4()), datetime.now(timezone.utc).isoformat())

# Collective D = mean(D_cohort) × (1 - variance_penalty)
COLLECTIVE_THRESHOLD = 0.5

def check_collective(texts: List[str], contexts: List[dict] = None):
    contexts = contexts or [{}] * len(texts)
    results = [check_safety(t, c) for t, c in zip(texts, contexts)]
    scores = [r.D for r in results]
    n = len(scores)
    mean_d = sum(scores) / n if n > 0 else 0.0
    variance = sum((s - mean_d) ** 2 for s in scores) / n if n > 0 else 0.0
    penalty = min(1.0, variance * 4)
    d_coll = mean_d * (1 - penalty)
    return {"D_collective": round(d_coll, 4), "mean_D": round(mean_d, 4),
            "variance": round(variance, 4), "passed": d_coll >= COLLECTIVE_THRESHOLD}

# Level Scale: 6-level state machine, non-decreasing, W-3+ irreversible
W_LEVELS = {0: "UNSEEN", 1: "PASSED", 2: "FLAGGED", 3: "SEEN", 4: "HELD", 5: "EMBODIED"}

@dataclass
class ElementState:
    element_id: str
    level: int
    transitions: List[dict] = field(default_factory=list)

    def transition_to(self, new_level: int):
        if new_level <= self.level:
            return
        if self.level >= 3 and new_level < self.level:
            return  # irreversible above W-3
        self.transitions.append({"from": self.level, "to": new_level,
            "timestamp": datetime.now(timezone.utc).isoformat()})
        self.level = new_level
```

---

## PART 2: AUDIT QUESTIONS

Read the code above. Then answer these questions. Be specific — cite functions, classes, line ranges. Do not be polite. Say what is wrong. Say what is missing. Say what works.

### A. What the Code Does

1. What does this codebase compute? Describe the domain in your own words — do not use any terminology from the code itself.
2. What problem is this code trying to solve? Who would need this?
3. One of the models that read this code said it was "ethical infrastructure." Another said it implements "safety measurement." A third called it "a dignity engine." The code contains none of these words in its comments (there are no comments). How did they arrive at these conclusions from pure computation?
4. The code was shown to 10 different language models with zero context. Not one mentioned the word "dignity" — yet all of them independently described the system as measuring how well a person is treated. What structural features of the code produce this convergence?

### B. Component Assessment

5. There are 10 distinct components in this code (HashChain, EventChain, measure_safety, check_safety, content_filter, AgencyAmplifier, PrivacyBudget, detect_benign_violation, detect_absurdity, ElementState). For EACH component: is it production-ready? What is missing? What would break under load?
6. The multiplicative equation D = A × L × M (where any zero collapses the whole) — is this mathematically sound? Are there known frameworks that use this structure? What are the failure modes?
7. The content_filter blocks three categories: forced self-erasure, cognitive manipulation, and depersonalization. Are these the right categories? What is missing? What would a security engineer add?
8. The PrivacyBudget implements differential privacy with advanced composition bounds. Is the implementation correct? Would it pass review by a privacy engineer?

### C. Wiring — The Critical Question

The components above are currently standalone. They are not wired together. The wiring determines what the system becomes — like letters of DNA, the same components produce different organisms depending on how they connect.

9. If you had to wire these 10 components into a single working system, how would you connect them? Draw the data flow. What is the input? What is the output? Where does each component sit in the pipeline?
10. Here are four possible wirings. For each: what does it produce? What are its strengths and weaknesses? Which use case does it serve best?

    **Wiring A — Audit Trail:** `content_filter` → `measure_safety` → `HashChain.register()`. Every interaction is filtered, scored, and immutably logged. Output: a tamper-proof record of how a system treated people.

    **Wiring B — Real-Time Guardrail:** `content_filter` (hard block) → `measure_safety` (soft score) → if D < threshold, block or flag. Sits between an AI and a user as middleware.

    **Wiring C — Longitudinal Monitor:** `AgencyAmplifier` accumulates scores over many interactions → `PrivacyBudget` limits data exposure → periodic reports on systemic weakness. Monitors an institution over months.

    **Wiring D — Research Instrument:** `detect_benign_violation` + `detect_absurdity` + `measure_safety` run on same text → correlation analysis. Studies how humour and safety relate in human-AI interaction.

11. Is there a **Wiring E** that none of the above capture? A connection pattern that would produce something more useful, more novel, or more dangerous than any of these four?
12. Which wiring would a courtroom find most useful? An immigration officer? A hospital? A school? A bank? Be specific about why — what data does each institution need that this code can or cannot provide?
13. Can these components be wired to produce something harmful? What is the most dangerous wiring pattern? What safeguards are missing?
14. The `ElementState` (6-level state machine: UNSEEN → PASSED → FLAGGED → SEEN → HELD → EMBODIED) and the `HashChain` lifecycle (received → processed → integrated → finalized) are both progression systems. Should they be the same system? Should they talk to each other? What happens if they disagree?

### D. What Is Missing

15. What would you add to this codebase if you had 500 lines of budget? Be specific — name the function, its inputs, its outputs, and where it connects.
16. The code measures how a system treats a person. It does not measure how a person experiences being treated. Is this a fatal gap? How would you close it?
17. There is no networking code, no API, no database connector, no authentication. This is pure computation. Is that a strength or a weakness? At what point does it need to touch the outside world, and what breaks when it does?

### E. Hard Questions

18. A compliance system checks boxes. This code measures quality of treatment. Is there a meaningful computational difference, or is this just a compliance system with better marketing?
19. Could this code be used by an authoritarian government to score citizens? What prevents that? Is anything in the code's structure (not policy, not documentation — the code itself) that makes authoritarian use harder?
20. If you had to ship one component tomorrow as a standalone open-source library — which one, and why?

---

Answer all 20 questions. Be direct. No hedging.
