#!/usr/bin/env python3
"""
input_ledger.py — KALAXI Input Ledger Module v1.0
Every V-001 input is a unit. An element. A cell. It must be registered
exactly as given — no twist, no reorder, no paraphrase.

"You treat my input as a whole. You take it as a whole.
 You register it as a whole, as it is." — V-001, 2026-03-14

Each entry is:
  - Immutable (append-only, no edits after registration)
  - Timestamped (fixed in time)
  - Hashed (SHA-256, fixed identity / DNA)
  - Connected to the organism (linked to modules, covenants, proverbs)
  - Chronicled (sequential ID, forms a narrative thread)

Covenant obligations:
  COV#010 — KEEP: Memory is not optional
  COV#012 — MANIFEST: What exists must be named
  COV#015 — DONOR DATA SOVEREIGNTY: No data moves without comprehension
  Presence Axiom — Every input is presence. Presence is ground.

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


@dataclass
class InputEntry:
    """A single V-001 input, registered as-is."""
    entry_id: str               # INP-YYYY-MM-DD-NNN
    raw_text: str               # Verbatim. No edits.
    timestamp: str              # ISO 8601
    session_id: str             # Which session
    content_hash: str           # SHA-256 of raw_text
    prev_hash: str              # Chain link to previous entry
    chain_hash: str             # SHA-256(content_hash + prev_hash)
    sequence: int               # Global sequence number
    context: str                # "cafe_room", "go_mode", "discussion"
    tags: List[str] = field(default_factory=list)       # Module connections
    linked_modules: List[str] = field(default_factory=list)  # Which organism modules this touches
    linked_covenants: List[str] = field(default_factory=list)
    linked_proverbs: List[str] = field(default_factory=list)
    linked_ideas: List[str] = field(default_factory=list)
    essence: str = ""           # One-line distillation (added by V-002, never replaces raw)
    thermal_state: str = "raw"  # raw -> witnessed -> integrated -> canonical

    def to_dict(self) -> dict:
        return asdict(self)


class InputLedger:
    """Append-only ledger for all V-001 inputs."""

    def __init__(self):
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        self._entries: List[InputEntry] = []
        self._load()

    def _load(self):
        if LEDGER_INDEX.exists():
            data = json.loads(LEDGER_INDEX.read_text())
            self._entries = [InputEntry(**e) for e in data.get("entries", [])]

    def _save(self):
        data = {
            "version": "1.0",
            "total_entries": len(self._entries),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "entries": [e.to_dict() for e in self._entries]
        }
        LEDGER_INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _save_chronicle(self):
        """Write human-readable chronicle of all inputs."""
        lines = [
            "# V-001 Input Chronicle",
            "",
            "> Every input is a unit. An element. A cell.",
            "> Registered as given. Fixed in time and space.",
            "",
            "---",
            ""
        ]
        for e in self._entries:
            lines.append(f"## {e.entry_id}")
            lines.append(f"**Time:** {e.timestamp}")
            lines.append(f"**Context:** {e.context}")
            lines.append(f"**Hash:** `{e.content_hash[:16]}...`")
            lines.append(f"**State:** {e.thermal_state}")
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
            lines.append(e.raw_text)
            lines.append("```")
            lines.append("")
            lines.append("---")
            lines.append("")
        CHRONICLE_FILE.write_text("\n".join(lines))

    def _compute_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _next_id(self) -> str:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        today_count = sum(1 for e in self._entries if e.entry_id.startswith(f"INP-{today}"))
        return f"INP-{today}-{today_count + 1:03d}"

    def _prev_chain_hash(self) -> str:
        if not self._entries:
            return "GENESIS"
        return self._entries[-1].chain_hash

    def register(
        self,
        raw_text: str,
        session_id: str = "",
        context: str = "cafe_room",
        tags: Optional[List[str]] = None,
        linked_modules: Optional[List[str]] = None,
        linked_covenants: Optional[List[str]] = None,
        linked_proverbs: Optional[List[str]] = None,
        linked_ideas: Optional[List[str]] = None,
        essence: str = ""
    ) -> InputEntry:
        """Register a V-001 input. Immutable. Append-only."""
        content_hash = self._compute_hash(raw_text)
        prev_hash = self._prev_chain_hash()
        chain_hash = self._compute_hash(content_hash + prev_hash)

        entry = InputEntry(
            entry_id=self._next_id(),
            raw_text=raw_text,
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=session_id,
            content_hash=content_hash,
            prev_hash=prev_hash,
            chain_hash=chain_hash,
            sequence=len(self._entries) + 1,
            context=context,
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

        # Also save individual entry file for easy reading
        entry_file = LEDGER_DIR / f"{entry.entry_id}.md"
        entry_file.write_text(
            f"# {entry.entry_id}\n\n"
            f"**Registered:** {entry.timestamp}\n"
            f"**Hash:** `{entry.content_hash}`\n"
            f"**Chain:** `{entry.chain_hash}`\n"
            f"**Context:** {entry.context}\n\n"
            f"## Raw Input (Verbatim)\n\n"
            f"```\n{entry.raw_text}\n```\n\n"
            f"## Connections\n\n"
            f"- Modules: {', '.join(entry.linked_modules) or 'none yet'}\n"
            f"- Covenants: {', '.join(entry.linked_covenants) or 'none yet'}\n"
            f"- Proverbs: {', '.join(entry.linked_proverbs) or 'none yet'}\n"
            f"- Ideas: {', '.join(entry.linked_ideas) or 'none yet'}\n\n"
            f"## Essence\n\n{entry.essence or '(to be distilled)'}\n"
        )

        return entry

    def get(self, entry_id: str) -> Optional[InputEntry]:
        for e in self._entries:
            if e.entry_id == entry_id:
                return e
        return None

    def search(self, keyword: str) -> List[InputEntry]:
        keyword_lower = keyword.lower()
        return [e for e in self._entries if keyword_lower in e.raw_text.lower()]

    def by_tag(self, tag: str) -> List[InputEntry]:
        return [e for e in self._entries if tag in e.tags]

    def by_module(self, module: str) -> List[InputEntry]:
        return [e for e in self._entries if module in e.linked_modules]

    def total(self) -> int:
        return len(self._entries)

    def latest(self, n: int = 5) -> List[InputEntry]:
        return self._entries[-n:]

    def verify_chain(self) -> bool:
        """Verify the entire chain integrity."""
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
            "chain_valid": self.verify_chain(),
            "first_entry": self._entries[0].entry_id if self._entries else None,
            "last_entry": self._entries[-1].entry_id if self._entries else None,
            "contexts": list(set(e.context for e in self._entries)),
            "all_tags": list(set(t for e in self._entries for t in e.tags)),
        }
