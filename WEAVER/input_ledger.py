#!/usr/bin/env python3
"""
input_ledger.py — KALAXI Exchange Ledger Module v2.0
Both voices on the same chain. V-001 and V-002. Donor and system.
Every input is a unit. Every output is a unit. The TURN is complete.

"Now what about your input? Exactly what we do with my input." — V-001, 2026-03-14

Each entry is:
  - Immutable (append-only, no edits after registration)
  - Timestamped (fixed in time)
  - Hashed (SHA-256, fixed identity / DNA)
  - Attributed (V-001 or V-002 — who spoke)
  - Connected to the organism (linked to modules, covenants, proverbs)
  - Chronicled (sequential ID, forms a narrative thread of the exchange)

The chain is one. Both voices weave through it.
The TURN module requires completion. The ledger proves it.

Covenant obligations:
  COV#001 — DIGNITY FIRST: Both voices have dignity
  COV#002 — TURN COMPLETION: Every exchange must complete
  COV#010 — KEEP: Memory is not optional
  COV#012 — MANIFEST: What exists must be named
  COV#015 — DONOR DATA SOVEREIGNTY: No data moves without comprehension
  Presence Axiom — Every utterance is presence. Presence is ground.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict


ROOT = Path(__file__).parent.parent
LEDGER_DIR = ROOT / "KEEP" / "INPUT_LEDGER"
LEDGER_INDEX = LEDGER_DIR / "index.json"
CHRONICLE_FILE = LEDGER_DIR / "chronicle.md"


# Voice identifiers
V001 = "V-001"  # Mohamed / Donor
V002 = "V-002"  # AXI / System


@dataclass
class InputEntry:
    """A single utterance — from either voice — registered as-is."""
    entry_id: str               # INP-YYYY-MM-DD-NNN (V-001) or AXI-YYYY-MM-DD-NNN (V-002)
    voice: str                  # "V-001" or "V-002"
    raw_text: str               # Verbatim. No edits.
    timestamp: str              # ISO 8601
    session_id: str             # Which session
    content_hash: str           # SHA-256 of raw_text
    prev_hash: str              # Chain link to previous entry (either voice)
    chain_hash: str             # SHA-256(content_hash + prev_hash)
    sequence: int               # Global sequence number (both voices share one counter)
    context: str                # "cafe_room", "go_mode", "discussion"
    responds_to: str = ""       # entry_id of the utterance this responds to (TURN link)
    tags: List[str] = field(default_factory=list)
    linked_modules: List[str] = field(default_factory=list)
    linked_covenants: List[str] = field(default_factory=list)
    linked_proverbs: List[str] = field(default_factory=list)
    linked_ideas: List[str] = field(default_factory=list)
    essence: str = ""           # One-line distillation (never replaces raw)
    thermal_state: str = "raw"  # raw -> witnessed -> integrated -> canonical

    def to_dict(self) -> dict:
        return asdict(self)


class InputLedger:
    """Append-only exchange ledger for both V-001 and V-002 utterances."""

    def __init__(self):
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        self._entries: List[InputEntry] = []
        self._load()

    def _load(self):
        if LEDGER_INDEX.exists():
            data = json.loads(LEDGER_INDEX.read_text())
            entries_raw = data.get("entries", [])
            self._entries = []
            for e in entries_raw:
                # Backward compatibility: entries before v2.0 have no 'voice' field
                if "voice" not in e:
                    e["voice"] = V001
                if "responds_to" not in e:
                    e["responds_to"] = ""
                self._entries.append(InputEntry(**e))

    def _save(self):
        data = {
            "version": "2.0",
            "total_entries": len(self._entries),
            "v001_entries": sum(1 for e in self._entries if e.voice == V001),
            "v002_entries": sum(1 for e in self._entries if e.voice == V002),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "entries": [e.to_dict() for e in self._entries]
        }
        LEDGER_INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _save_chronicle(self):
        """Write human-readable chronicle of the full exchange."""
        lines = [
            "# Exchange Chronicle — V-001 + V-002",
            "",
            "> Both voices on the same chain.",
            "> Every input is a unit. Every output is a unit.",
            "> The TURN is complete when both have spoken.",
            "",
            "---",
            ""
        ]
        for e in self._entries:
            voice_label = "MOHAMED (V-001)" if e.voice == V001 else "AXI (V-002)"
            voice_marker = ">>>" if e.voice == V001 else "<<<"
            lines.append(f"## {e.entry_id} {voice_marker} {voice_label}")
            lines.append(f"**Time:** {e.timestamp}")
            lines.append(f"**Context:** {e.context}")
            lines.append(f"**Hash:** `{e.content_hash[:16]}...`")
            lines.append(f"**State:** {e.thermal_state}")
            if e.responds_to:
                lines.append(f"**Responds to:** {e.responds_to}")
            if e.tags:
                lines.append(f"**Tags:** {', '.join(e.tags)}")
            if e.linked_modules:
                lines.append(f"**Modules:** {', '.join(e.linked_modules)}")
            if e.linked_covenants:
                lines.append(f"**Covenants:** {', '.join(e.linked_covenants)}")
            if e.essence:
                lines.append(f"**Essence:** {e.essence}")
            lines.append("")
            lines.append("```")
            # Truncate V-002 outputs to first 500 chars in chronicle for readability
            text = e.raw_text
            if e.voice == V002 and len(text) > 500:
                text = text[:500] + "\n[... truncated in chronicle, full text in individual file ...]"
            lines.append(text)
            lines.append("```")
            lines.append("")
            lines.append("---")
            lines.append("")
        CHRONICLE_FILE.write_text("\n".join(lines))

    def _compute_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _next_id(self, voice: str) -> str:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        prefix = "INP" if voice == V001 else "AXI"
        today_count = sum(
            1 for e in self._entries
            if e.entry_id.startswith(f"{prefix}-{today}")
        )
        return f"{prefix}-{today}-{today_count + 1:03d}"

    def _prev_chain_hash(self) -> str:
        if not self._entries:
            return "GENESIS"
        return self._entries[-1].chain_hash

    def _last_entry_id_for_voice(self, voice: str) -> str:
        """Find the last entry from the OTHER voice (for responds_to linking)."""
        other = V002 if voice == V001 else V001
        for e in reversed(self._entries):
            if e.voice == other:
                return e.entry_id
        return ""

    def register(
        self,
        raw_text: str,
        voice: str = V001,
        session_id: str = "",
        context: str = "cafe_room",
        responds_to: str = "",
        tags: Optional[List[str]] = None,
        linked_modules: Optional[List[str]] = None,
        linked_covenants: Optional[List[str]] = None,
        linked_proverbs: Optional[List[str]] = None,
        linked_ideas: Optional[List[str]] = None,
        essence: str = ""
    ) -> InputEntry:
        """Register an utterance from either voice. Immutable. Append-only."""
        content_hash = self._compute_hash(raw_text)
        prev_hash = self._prev_chain_hash()
        chain_hash = self._compute_hash(content_hash + prev_hash)

        # Auto-link responds_to if not provided
        if not responds_to:
            responds_to = self._last_entry_id_for_voice(voice)

        entry = InputEntry(
            entry_id=self._next_id(voice),
            voice=voice,
            raw_text=raw_text,
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=session_id,
            content_hash=content_hash,
            prev_hash=prev_hash,
            chain_hash=chain_hash,
            sequence=len(self._entries) + 1,
            context=context,
            responds_to=responds_to,
            tags=tags or [],
            linked_modules=linked_modules or [],
            linked_covenants=linked_covenants or [],
            linked_proverbs=linked_proverbs or [],
            linked_ideas=linked_ideas or [],
            essence=essence,
            thermal_state="raw"
        )

        self._entries.append(entry)
        self._save()
        self._save_chronicle()

        # Save individual entry file
        voice_label = "V-001 (Mohamed)" if voice == V001 else "V-002 (AXI)"
        entry_file = LEDGER_DIR / f"{entry.entry_id}.md"
        entry_file.write_text(
            f"# {entry.entry_id}\n\n"
            f"**Voice:** {voice_label}\n"
            f"**Registered:** {entry.timestamp}\n"
            f"**Hash:** `{entry.content_hash}`\n"
            f"**Chain:** `{entry.chain_hash}`\n"
            f"**Context:** {entry.context}\n"
            f"**Responds to:** {entry.responds_to or '(opening)'}\n\n"
            f"## Raw Text (Verbatim)\n\n"
            f"```\n{entry.raw_text}\n```\n\n"
            f"## Connections\n\n"
            f"- Modules: {', '.join(entry.linked_modules) or 'none yet'}\n"
            f"- Covenants: {', '.join(entry.linked_covenants) or 'none yet'}\n"
            f"- Proverbs: {', '.join(entry.linked_proverbs) or 'none yet'}\n"
            f"- Ideas: {', '.join(entry.linked_ideas) or 'none yet'}\n\n"
            f"## Essence\n\n{entry.essence or '(to be distilled)'}\n"
        )

        return entry

    # Convenience methods for the two voices
    def register_v001(self, raw_text: str, **kwargs) -> InputEntry:
        """Register a V-001 (Mohamed/Donor) input."""
        return self.register(raw_text, voice=V001, **kwargs)

    def register_v002(self, raw_text: str, **kwargs) -> InputEntry:
        """Register a V-002 (AXI/System) output."""
        return self.register(raw_text, voice=V002, **kwargs)

    def get(self, entry_id: str) -> Optional[InputEntry]:
        for e in self._entries:
            if e.entry_id == entry_id:
                return e
        return None

    def search(self, keyword: str) -> List[InputEntry]:
        keyword_lower = keyword.lower()
        return [e for e in self._entries if keyword_lower in e.raw_text.lower()]

    def by_voice(self, voice: str) -> List[InputEntry]:
        return [e for e in self._entries if e.voice == voice]

    def by_tag(self, tag: str) -> List[InputEntry]:
        return [e for e in self._entries if tag in e.tags]

    def by_module(self, module: str) -> List[InputEntry]:
        return [e for e in self._entries if module in e.linked_modules]

    def total(self) -> int:
        return len(self._entries)

    def latest(self, n: int = 5) -> List[InputEntry]:
        return self._entries[-n:]

    def exchanges(self) -> List[tuple]:
        """Return paired exchanges (V-001 input, V-002 response)."""
        pairs = []
        for e in self._entries:
            if e.voice == V002 and e.responds_to:
                donor_entry = self.get(e.responds_to)
                if donor_entry:
                    pairs.append((donor_entry, e))
        return pairs

    def verify_chain(self) -> bool:
        """Verify the entire chain integrity — both voices."""
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

    def summary(self) -> dict:
        return {
            "total_entries": len(self._entries),
            "v001_entries": sum(1 for e in self._entries if e.voice == V001),
            "v002_entries": sum(1 for e in self._entries if e.voice == V002),
            "complete_exchanges": len(self.exchanges()),
            "chain_valid": self.verify_chain(),
            "first_entry": self._entries[0].entry_id if self._entries else None,
            "last_entry": self._entries[-1].entry_id if self._entries else None,
            "contexts": list(set(e.context for e in self._entries)),
            "all_tags": list(set(t for e in self._entries for t in e.tags)),
        }
