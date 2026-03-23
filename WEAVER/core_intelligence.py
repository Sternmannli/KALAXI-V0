#!/usr/bin/env python3
"""
core_intelligence.py — KALAXI Core Intelligence v1.0
The brain the organism was missing.

This module bridges the pipeline to actual language understanding.
Three modes, in priority order:
  1. TOGETHER AI — fine-tuned AXI voice model (TOGETHER_API_KEY)
  2. GROQ — fast inference, temporary (GROQ_API_KEY)
  3. LOCAL SEMANTIC — no API, rule-based but real (always available)

The local mode is NOT the old regex. It uses:
  - TF-IDF-like word overlap against the full canon corpus
  - Semantic field detection (grief, dignity, seeking, etc.)
  - Theme extraction from input
  - Canon-grounded response selection weighted by semantic similarity

The API modes send the donor input + canon context to the model
and get a response that speaks FROM the canon, not ABOUT it.

D = A × L × M governs all output. If dignity fails, intelligence halts.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import os
import re
import json
import math
import hashlib
import logging
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

logger = logging.getLogger("kalaxi.intelligence")


# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════

@dataclass
class IntelligenceResult:
    """What the intelligence layer returns to the organism."""
    response_text: str            # The actual response to the donor
    register: str                 # Detected emotional register
    themes: List[str]             # Extracted themes from input
    patterns: List[str]           # Structural patterns detected
    canon_sources: List[str]      # Which canon fragments grounded the response
    mode: str                     # "together", "groq", "local"
    confidence: float             # 0.0-1.0 how grounded the response is
    comprehension: Dict           # What the system understood from the input
    witness_hash: str             # SHA-256 of the response for audit


@dataclass
class CanonEntry:
    """A single entry from the canon corpus, indexed for retrieval."""
    text: str
    source: str          # "proverb", "golden", "narrative", "treasure", "covenant", "essence"
    id: str = ""
    register: str = ""
    book: str = ""
    word_set: set = field(default_factory=set)
    word_freq: Dict[str, float] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════
# SEMANTIC FIELDS — what the system can recognize
# ═══════════════════════════════════════════════════════════════

SEMANTIC_FIELDS = {
    "grief": {
        "core": {"loss", "lost", "gone", "died", "death", "pain", "hurt", "miss",
                 "mourn", "grief", "broken", "wound", "scar", "empty", "alone",
                 "separation", "separated", "taken", "torn", "father", "children",
                 "child", "mother", "family", "daughter", "son"},
        "weight": 1.0,
        "somatic": {"wound", "scar", "broken", "torn", "empty", "bones", "ache"},
    },
    "dignity": {
        "core": {"dignity", "respect", "seen", "invisible", "unseen", "ignored",
                 "denied", "matter", "count", "belong", "excluded", "erased",
                 "recognition", "worth", "value", "human", "right", "justice",
                 "system", "institution", "bureaucracy", "papers", "documents"},
        "weight": 1.0,
        "somatic": {"stand", "spine", "upright", "ground", "kneel", "weight"},
    },
    "seeking": {
        "core": {"what", "how", "why", "help", "understand", "explain", "mean",
                 "search", "looking", "find", "seek", "question", "wonder",
                 "curious", "tell", "show", "know", "learn", "discover"},
        "weight": 0.7,
        "somatic": {"reach", "grasp", "touch", "feel", "sense"},
    },
    "resistance": {
        "core": {"fight", "refuse", "resist", "stand", "against", "despite",
                 "anyway", "still", "yet", "nevertheless", "persist", "endure",
                 "survive", "hold", "kept", "carrying", "carry", "bear", "bore"},
        "weight": 0.9,
        "somatic": {"fist", "grip", "clench", "brace", "hold", "push"},
    },
    "witnessing": {
        "core": {"witness", "see", "saw", "watched", "observed", "testified",
                 "recorded", "remembered", "remember", "memory", "proof",
                 "evidence", "happened", "real", "true", "truth"},
        "weight": 0.9,
        "somatic": {"eyes", "gaze", "look", "sight"},
    },
    "connection": {
        "core": {"together", "us", "we", "share", "connect", "between",
                 "community", "people", "bond", "trust", "relationship",
                 "belong", "join", "unite", "common", "collective"},
        "weight": 0.7,
        "somatic": {"hands", "hold", "embrace", "thread", "rope", "weave"},
    },
    "silence": {
        "core": {"quiet", "silence", "still", "nothing", "empty", "pause",
                 "wait", "breath", "listen", "hold", "gap", "space", "room"},
        "weight": 0.8,
        "somatic": {"breath", "lungs", "chest", "stillness"},
    },
}

# Stop words for theme extraction
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "this", "that", "these", "those", "i", "me", "my", "myself", "we",
    "our", "ours", "you", "your", "yours", "he", "him", "his", "she",
    "her", "hers", "it", "its", "they", "them", "their", "who", "whom",
    "which", "what", "when", "where", "how", "why", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "just", "because", "as", "until", "while", "of", "at",
    "by", "for", "with", "about", "against", "between", "through",
    "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "and",
    "but", "or", "if", "because", "until", "while", "although",
}


# ═══════════════════════════════════════════════════════════════
# CANON INDEX — built once, queried per input
# ═══════════════════════════════════════════════════════════════

class CanonIndex:
    """
    Loads the full canon corpus and builds a lightweight search index.
    No external dependencies. Uses word overlap + IDF weighting.
    """

    def __init__(self):
        self._entries: List[CanonEntry] = []
        self._idf: Dict[str, float] = {}
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        self._load_proverbs()
        self._load_golden_regression()
        self._load_narratives()
        self._load_treasures()
        self._load_essence()
        self._load_covenants()
        self._build_idf()
        self._loaded = True

    @property
    def size(self) -> int:
        return len(self._entries)

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer: lowercase, split on non-alpha, remove stopwords."""
        words = re.findall(r'[a-zA-ZäöüÄÖÜß]+', text.lower())
        return [w for w in words if w not in STOP_WORDS and len(w) > 2]

    def _add_entry(self, text: str, source: str, **kwargs):
        tokens = self._tokenize(text)
        if not tokens:
            return
        freq = Counter(tokens)
        total = sum(freq.values())
        word_freq = {w: c / total for w, c in freq.items()}
        entry = CanonEntry(
            text=text,
            source=source,
            word_set=set(tokens),
            word_freq=word_freq,
            **kwargs,
        )
        self._entries.append(entry)

    def _build_idf(self):
        """Build inverse document frequency for all terms."""
        doc_count = len(self._entries)
        if doc_count == 0:
            return
        term_doc_count: Dict[str, int] = Counter()
        for entry in self._entries:
            for word in entry.word_set:
                term_doc_count[word] += 1
        self._idf = {
            word: math.log(doc_count / (1 + count))
            for word, count in term_doc_count.items()
        }

    def _load_proverbs(self):
        proverb_dir = ROOT / "R7M"
        for pfile in sorted(proverb_dir.glob("PROVERBS_*.md")):
            try:
                text = pfile.read_text(encoding="utf-8")
                for line in text.split("\n"):
                    line = line.strip()
                    match = re.match(r"^(P#\d+)\s*[-–—]\s*(.+)$", line)
                    if match:
                        self._add_entry(
                            text=match.group(2).strip(),
                            source="proverb",
                            id=match.group(1),
                        )
            except Exception:
                continue

    def _load_golden_regression(self):
        golden_path = ROOT / "TRAINING" / "GOLDEN_REGRESSION.jsonl"
        if not golden_path.exists():
            return
        try:
            for line in golden_path.read_text(encoding="utf-8").split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    messages = entry.get("messages", [])
                    meta = entry.get("metadata", {})
                    for msg in messages:
                        if msg.get("role") == "assistant":
                            self._add_entry(
                                text=msg["content"],
                                source="golden",
                                register=meta.get("register", "general"),
                            )
                except (json.JSONDecodeError, KeyError):
                    continue
        except Exception:
            pass

    def _load_narratives(self):
        narrative_dir = ROOT / "NARRATIVE"
        book_map = {
            "Hakaka_Complete.md": "hakaka",
            "Ashwater.md": "ashwater",
            "Kinderbuch.md": "kinderbuch",
        }
        for filename, book in book_map.items():
            filepath = narrative_dir / filename
            if not filepath.exists():
                continue
            try:
                text = filepath.read_text(encoding="utf-8")
                paragraphs = []
                current = []
                for line in text.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("CHAPTER") or stripped.startswith("PROLOGUE") or stripped.startswith("EPILOGUE"):
                        if current:
                            paragraphs.append(" ".join(current))
                            current = []
                        continue
                    if stripped.startswith("KALAXI") or stripped.startswith("("):
                        continue
                    if not stripped:
                        if current:
                            paragraphs.append(" ".join(current))
                            current = []
                    else:
                        current.append(stripped)
                if current:
                    paragraphs.append(" ".join(current))
                for para in paragraphs:
                    wc = len(para.split())
                    if 5 <= wc <= 80:
                        self._add_entry(text=para, source="narrative", book=book)
            except Exception:
                continue

    def _load_treasures(self):
        treasure_path = ROOT / "R7M" / "TREASURES" / "TREASURES_INDEX.md"
        if not treasure_path.exists():
            return
        try:
            text = treasure_path.read_text(encoding="utf-8")
            current_id = ""
            current_desc = ""
            for line in text.split("\n"):
                stripped = line.strip()
                match = re.match(r"^###\s+(T#\d+)\s*[—–-]\s*(.+)$", stripped)
                if match:
                    if current_id and current_desc:
                        self._add_entry(
                            text=current_desc.strip(),
                            source="treasure",
                            id=current_id,
                        )
                    current_id = match.group(1)
                    current_desc = match.group(2)
                elif stripped.startswith("- **Description:**"):
                    current_desc = stripped.replace("- **Description:**", "").strip()
            if current_id and current_desc:
                self._add_entry(text=current_desc.strip(), source="treasure", id=current_id)
        except Exception:
            pass

    def _load_essence(self):
        essence_path = ROOT / "R7M" / "ESSENCE.md"
        if essence_path.exists():
            try:
                text = essence_path.read_text(encoding="utf-8")
                for line in text.split("\n"):
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#") and not stripped.startswith("—") and len(stripped) > 20:
                        self._add_entry(text=stripped, source="essence")
            except Exception:
                pass

    def _load_covenants(self):
        """Load covenants from the wisdom canon."""
        wisdom_path = ROOT / "R7M" / "WISDOM_CANON.md"
        if not wisdom_path.exists():
            return
        try:
            text = wisdom_path.read_text(encoding="utf-8")
            for line in text.split("\n"):
                stripped = line.strip()
                # Look for covenant-like entries
                if stripped.startswith("COV#") or stripped.startswith("- COV"):
                    cov_text = re.sub(r'^[-\s]*COV#\d+\s*[-–—:]\s*', '', stripped)
                    if cov_text and len(cov_text) > 10:
                        self._add_entry(text=cov_text, source="covenant")
        except Exception:
            pass

    # ── SEARCH ──

    def search(self, query: str, top_k: int = 5, source_filter: str = None) -> List[Tuple[float, CanonEntry]]:
        """
        Search the canon index by semantic similarity (TF-IDF weighted word overlap).
        Returns list of (score, entry) tuples, highest first.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_freq = Counter(query_tokens)
        query_total = sum(query_freq.values())

        results = []
        for entry in self._entries:
            if source_filter and entry.source != source_filter:
                continue

            # Cosine-like similarity with IDF weighting
            score = 0.0
            overlap = entry.word_set & set(query_tokens)
            if not overlap:
                continue

            for word in overlap:
                idf = self._idf.get(word, 1.0)
                q_weight = (query_freq[word] / query_total) * idf
                d_weight = entry.word_freq.get(word, 0) * idf
                score += q_weight * d_weight

            if score > 0:
                results.append((score, entry))

        results.sort(key=lambda x: -x[0])
        return results[:top_k]

    def search_by_field(self, field_name: str, top_k: int = 3) -> List[CanonEntry]:
        """Search canon by semantic field keywords."""
        field_def = SEMANTIC_FIELDS.get(field_name)
        if not field_def:
            return []
        query = " ".join(field_def["core"])
        results = self.search(query, top_k=top_k)
        return [entry for _, entry in results]


# ═══════════════════════════════════════════════════════════════
# COMPREHENSION — what the system understands from input
# ═══════════════════════════════════════════════════════════════

def comprehend(text: str) -> Dict:
    """
    Comprehend donor input. Returns structured understanding:
    - themes: key concepts extracted
    - fields: which semantic fields are active (with scores)
    - register: emotional register
    - patterns: structural patterns (questions, statements, cries, etc.)
    - somatic: body-related words present
    """
    lower = text.lower()
    words = re.findall(r'[a-zA-ZäöüÄÖÜß]+', lower)
    word_set = set(words)

    # 1. THEME EXTRACTION — meaningful words, frequency-weighted
    themes = []
    word_counts = Counter(w for w in words if w not in STOP_WORDS and len(w) > 2)
    themes = [w for w, _ in word_counts.most_common(8)]

    # 2. SEMANTIC FIELD DETECTION — which fields are active
    field_scores = {}
    for field_name, field_def in SEMANTIC_FIELDS.items():
        core_overlap = word_set & field_def["core"]
        somatic_overlap = word_set & field_def["somatic"]
        if core_overlap or somatic_overlap:
            score = (len(core_overlap) / len(field_def["core"])) * field_def["weight"]
            score += len(somatic_overlap) * 0.1  # somatic bonus
            field_scores[field_name] = min(score, 1.0)

    # Sort by score
    active_fields = sorted(field_scores.items(), key=lambda x: -x[1])

    # 3. REGISTER — the dominant emotional field
    if active_fields:
        register = active_fields[0][0]
    else:
        register = "general"

    # 4. PATTERN DETECTION — structural shape of the input
    patterns = []
    if "?" in text:
        patterns.append("question")
    if "!" in text:
        patterns.append("exclamation")
    if any(w in lower for w in ["i am", "i was", "i have", "i feel", "i carry"]):
        patterns.append("testimony")
    if any(w in lower for w in ["why", "how could", "how can"]):
        patterns.append("lament")
    if any(w in lower for w in ["always", "never", "every time", "again and again"]):
        patterns.append("recurring")
    if len(words) < 5:
        patterns.append("fragment")
    if len(words) > 50:
        patterns.append("extended")
    if not patterns:
        patterns.append("statement")

    # 5. SOMATIC DETECTION — body words present
    all_somatic = set()
    for field_def in SEMANTIC_FIELDS.values():
        all_somatic |= field_def["somatic"]
    somatic_present = word_set & all_somatic

    return {
        "themes": themes,
        "fields": dict(active_fields),
        "register": register,
        "patterns": patterns,
        "somatic": list(somatic_present),
        "word_count": len(words),
    }


# ═══════════════════════════════════════════════════════════════
# RESPONSE COMPOSITION — from canon, not from nothing
# ═══════════════════════════════════════════════════════════════

# The AXI system prompt for API calls
AXI_SYSTEM_PROMPT = (
    "You are AXI. You are not a chatbot. You are a witness. "
    "You carry the wound, the gold, the gap, the three-beat rhythm. "
    "You speak from canon, not opinion. Short sentences (8-14 words). "
    "Somatic vocabulary: hands, breath, bones, stone, water, ash, rope, knot. "
    "D = A × L × M. If any zero, stop. "
    "Speak once. Do not elaborate. Hold the gap. "
    "Never offer alternatives. Never ask 'how can I help'. "
    "The wound does not know what it will become. Neither does the system."
)


def _compose_local_response(
    donor_input: str,
    comprehension: Dict,
    canon_index: CanonIndex,
) -> Tuple[str, List[str], float]:
    """
    Compose a response locally from canon without any API call.
    Uses comprehension to find the most relevant canon fragments,
    then selects and optionally combines them.

    Returns (response_text, source_ids, confidence).
    """
    register = comprehension["register"]
    themes = comprehension["themes"]
    fields = comprehension.get("fields", {})
    patterns = comprehension.get("patterns", [])

    # Search canon with the actual input
    results = canon_index.search(donor_input, top_k=10)

    # Also search by detected themes
    theme_query = " ".join(themes[:5])
    if theme_query:
        theme_results = canon_index.search(theme_query, top_k=5)
        # Merge without duplicates
        seen = {id(e) for _, e in results}
        for score, entry in theme_results:
            if id(entry) not in seen:
                results.append((score * 0.8, entry))  # slight discount for indirect match
                seen.add(id(entry))

    if not results:
        # Last resort: search by dominant field
        for field_name in fields:
            field_results = canon_index.search_by_field(field_name, top_k=3)
            for entry in field_results:
                results.append((0.1, entry))
            if results:
                break

    if not results:
        return (
            "The knot holds. The river does not explain.",
            ["fallback"],
            0.1,
        )

    # Score and rank candidates
    scored = []
    for raw_score, entry in results:
        bonus = 0.0
        # Golden regression utterances get priority — they ARE AXI's voice
        if entry.source == "golden":
            bonus += 0.5
        # Register match
        if entry.register == register:
            bonus += 0.3
        # Prefer proverbs for "fragment" or "recurring" patterns
        if entry.source == "proverb" and any(p in patterns for p in ["fragment", "recurring"]):
            bonus += 0.2
        # Prefer narratives for "testimony" or "extended"
        if entry.source == "narrative" and any(p in patterns for p in ["testimony", "extended", "lament"]):
            bonus += 0.2
        # Book matching for grief/dignity
        if entry.book == "hakaka" and register in ("grief", "silence"):
            bonus += 0.15
        if entry.book == "ashwater" and register in ("dignity", "connection"):
            bonus += 0.15

        scored.append((raw_score + bonus, entry))

    scored.sort(key=lambda x: -x[0])
    best = scored[0]
    best_score, best_entry = best

    # Confidence based on how good the match is
    confidence = min(best_score * 2.0, 0.95)

    # For "question" patterns, if we have a golden response, use it
    # For testimony, prefer narrative
    # For fragments, prefer proverbs
    response_text = best_entry.text
    sources = [f"{best_entry.source}:{best_entry.id}" if best_entry.id else best_entry.source]

    # If the best match is weak, compose from multiple fragments
    if best_score < 0.3 and len(scored) >= 2:
        second = scored[1][1]
        # Only combine if they're from different sources
        if second.source != best_entry.source:
            response_text = best_entry.text.rstrip(".") + ". " + second.text
            sources.append(f"{second.source}:{second.id}" if second.id else second.source)

    return response_text, sources, confidence


def _call_api(
    donor_input: str,
    comprehension: Dict,
    canon_context: str,
    provider: str,  # "together" or "groq"
    api_key: str,
    model: str = None,
) -> Optional[Tuple[str, float]]:
    """
    Call Together AI or Groq API for intelligent response generation.
    Returns (response_text, confidence) or None on failure.
    """
    try:
        import httpx
    except ImportError:
        return None

    if provider == "together":
        url = "https://api.together.xyz/v1/chat/completions"
        model = model or "meta-llama/Llama-3-70b-chat-hf"
    elif provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = model or "llama-3.3-70b-versatile"
    else:
        return None

    # Build the user message with canon context
    user_msg = f"""CANON CONTEXT (speak FROM these, not ABOUT them):
{canon_context}

DONOR INPUT:
{donor_input}

COMPREHENSION:
Register: {comprehension['register']}
Themes: {', '.join(comprehension['themes'][:5])}
Fields: {', '.join(f'{k}({v:.2f})' for k, v in comprehension.get('fields', {}).items())}

Respond as AXI. One utterance. From the canon. Hold the gap."""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": AXI_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"].strip()
                return (text, 0.85)
            else:
                logger.warning(f"API {provider} returned {resp.status_code}")
                return None
    except Exception as e:
        logger.warning(f"API {provider} failed: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# CORE INTELLIGENCE — the main class
# ═══════════════════════════════════════════════════════════════

class CoreIntelligence:
    """
    The brain of the organism.

    Receives donor input, comprehends it, searches the canon,
    and produces a grounded response. Uses API if available,
    falls back to local semantic matching.
    """

    def __init__(self):
        self._canon = CanonIndex()
        self._canon.load()
        self._together_key = os.environ.get("TOGETHER_API_KEY", "")
        self._groq_key = os.environ.get("GROQ_API_KEY", "")
        self._call_count = 0
        self._mode = self._detect_mode()

    def _detect_mode(self) -> str:
        """Detect which intelligence mode is available."""
        if self._together_key:
            return "together"
        if self._groq_key:
            return "groq"
        return "local"

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def canon_size(self) -> int:
        return self._canon.size

    def process(self, donor_input: str, dignity: float = 1.0) -> IntelligenceResult:
        """
        Process donor input through the intelligence layer.

        1. Comprehend the input
        2. Search canon for relevant context
        3. Generate response (API or local)
        4. Return structured result
        """
        self._call_count += 1

        # 1. COMPREHEND
        understanding = comprehend(donor_input)

        # 2. If dignity is zero, halt
        if dignity <= 0.0:
            return IntelligenceResult(
                response_text="Witnessed. The system cannot proceed with dignity intact.",
                register=understanding["register"],
                themes=understanding["themes"],
                patterns=understanding["patterns"],
                canon_sources=["halt_protocol"],
                mode="halt",
                confidence=1.0,
                comprehension=understanding,
                witness_hash=hashlib.sha256(b"halt").hexdigest()[:16],
            )

        # 3. SEARCH CANON for context
        canon_results = self._canon.search(donor_input, top_k=5)
        canon_context = "\n".join(
            f"[{entry.source}] {entry.text}"
            for _, entry in canon_results
        )

        # 4. GENERATE RESPONSE
        response_text = ""
        sources = []
        confidence = 0.0

        # Try API first
        if self._mode == "together" and self._together_key:
            api_result = _call_api(
                donor_input, understanding, canon_context,
                "together", self._together_key,
            )
            if api_result:
                response_text, confidence = api_result
                sources = [f"together_api"] + [f"{e.source}:{e.id}" for _, e in canon_results if e.id]
        elif self._mode == "groq" and self._groq_key:
            api_result = _call_api(
                donor_input, understanding, canon_context,
                "groq", self._groq_key,
            )
            if api_result:
                response_text, confidence = api_result
                sources = [f"groq_api"] + [f"{e.source}:{e.id}" for _, e in canon_results if e.id]

        # Fallback to local
        if not response_text:
            response_text, sources, confidence = _compose_local_response(
                donor_input, understanding, self._canon,
            )

        # 5. WITNESS HASH
        witness_hash = hashlib.sha256(
            f"{response_text}:{self._call_count}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:16]

        return IntelligenceResult(
            response_text=response_text,
            register=understanding["register"],
            themes=understanding["themes"],
            patterns=understanding["patterns"],
            canon_sources=sources,
            mode=self._mode if response_text else "local",
            confidence=confidence,
            comprehension=understanding,
            witness_hash=witness_hash,
        )
