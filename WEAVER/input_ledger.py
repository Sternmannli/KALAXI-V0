#!/usr/bin/env python3
"""
input_ledger.py — KALAXI Exchange Ledger Module v3.0
Both voices on the same chain. V-001 and V-002. Donor and system.
Every input is a unit. Every output is a unit. The TURN is complete.

v3.0 — Receipt Chain Architecture (honoring Grand Archive blockchain DNA)
  The original ledger (2025-09-12) used a receipt chain:
    CAPTURE → BUNDLE → MIRROR → SEAL → SESSION_SEAL
  Each receipt carried: Owner, Dual Timestamp, Status/Drift, Impression, Proverb.
  v3.0 integrates these elements into the Exchange Ledger.

"Now what about your input? Exactly what we do with my input." — V-001, 2026-03-14

Each entry is:
  - Immutable (append-only, no edits after registration)
  - Dual-timestamped (ZRH local + UTC, honoring Grand Archive format)
  - Hashed (SHA-256, fixed identity / DNA)
  - Attributed (V-001 or V-002 — who spoke)
  - Witnessed (impression — one-line witness, never empty)
  - Anchored (proverb_anchor — wisdom seed per entry)
  - Drift-checked (per-entry integrity, not just global)
  - Connected to the organism (linked to modules, covenants, proverbs)
  - Chronicled (sequential ID, forms a narrative thread of the exchange)
  - Bundled (entries group into cycles, cycles seal into sessions)

Receipt types (from Grand Archive DNA):
  CAPTURE  — Individual atom enters the ledger
  BUNDLE   — Atoms grouped by cycle
  MIRROR   — Bundle reflected, stability checked
  SEAL     — Bundle sealed permanently
  SESSION  — All bundles from session sealed as chapter

Covenant obligations:
  COV#001 — DIGNITY FIRST: Both voices have dignity
  COV#002 — TURN COMPLETION: Every exchange must complete
  COV#010 — KEEP: Memory is not optional
  COV#012 — MANIFEST: What exists must be named
  COV#015 — DONOR DATA SOVEREIGNTY: No data moves without comprehension
  Presence Axiom — Every utterance is presence. Presence is ground.
  OATH::SOVEREIGN-AXIS v∞ — No drift. No retirement. Every element preserved.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict


ROOT = Path(__file__).parent.parent
LEDGER_DIR = ROOT / "KEEP" / "INPUT_LEDGER"
LEDGER_INDEX = LEDGER_DIR / "index.json"
CHRONICLE_FILE = LEDGER_DIR / "chronicle.md"

# Timezone for dual timestamps (honoring Grand Archive format: ZRH + UTC)
ZRH = ZoneInfo("Europe/Zurich")

# Voice identifiers
V001 = "V-001"  # Mohamed / Donor
V002 = "V-002"  # AXI / System

# Receipt types (from Grand Archive blockchain DNA)
RECEIPT_CAPTURE = "CAPTURE"    # Individual atom enters
RECEIPT_BUNDLE = "BUNDLE"      # Atoms grouped by cycle
RECEIPT_MIRROR = "MIRROR"      # Bundle reflected, stability checked
RECEIPT_SEAL = "SEAL"          # Bundle sealed permanently
RECEIPT_SESSION = "SESSION"    # All bundles sealed as chapter

# Owner DID (from Grand Archive)
OWNER_DID = "did:axi:mohamed"


@dataclass
class InputEntry:
    """A single utterance — from either voice — registered as-is.
    v3.0: Now carries receipt chain DNA from Grand Archive (2025-09-12)."""
    entry_id: str               # INP-YYYY-MM-DD-NNN (V-001) or AXI-YYYY-MM-DD-NNN (V-002)
    voice: str                  # "V-001" or "V-002"
    raw_text: str               # Verbatim. No edits.
    timestamp: str              # ISO 8601 (UTC)
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
    patterns: List[str] = field(default_factory=list)  # Extracted patterns (structural, not content)
    thermal_state: str = "raw"  # raw -> witnessed -> integrated -> canonical
    # v3.0 fields — Grand Archive blockchain DNA
    timestamp_zrh: str = ""     # Local Zurich time (dual timestamp)
    impression: str = ""        # One-line witness of what was registered
    proverb_anchor: str = ""    # Wisdom anchor for this entry
    receipt_type: str = "CAPTURE"  # CAPTURE/BUNDLE/MIRROR/SEAL/SESSION
    drift_status: str = "NONE"  # Per-entry drift check
    bundle_id: str = ""         # Which bundle this entry belongs to
    owner: str = OWNER_DID      # did:axi:mohamed

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
                # Backward compatibility: entries before v3.0 have no receipt chain fields
                if "timestamp_zrh" not in e:
                    e["timestamp_zrh"] = ""
                if "impression" not in e:
                    e["impression"] = ""
                if "proverb_anchor" not in e:
                    e["proverb_anchor"] = ""
                if "receipt_type" not in e:
                    e["receipt_type"] = RECEIPT_CAPTURE
                if "drift_status" not in e:
                    e["drift_status"] = "NONE"
                if "bundle_id" not in e:
                    e["bundle_id"] = ""
                if "owner" not in e:
                    e["owner"] = OWNER_DID
                if "patterns" not in e:
                    e["patterns"] = []
                self._entries.append(InputEntry(**e))

    def _save(self):
        now_utc = datetime.now(timezone.utc)
        now_zrh = now_utc.astimezone(ZRH)
        data = {
            "version": "3.0",
            "owner": OWNER_DID,
            "total_entries": len(self._entries),
            "v001_entries": sum(1 for e in self._entries if e.voice == V001),
            "v002_entries": sum(1 for e in self._entries if e.voice == V002),
            "last_updated_utc": now_utc.isoformat(),
            "last_updated_zrh": now_zrh.isoformat(),
            "chain_integrity": "VERIFIED" if self.verify_chain() else "BROKEN",
            "entries": [e.to_dict() for e in self._entries]
        }
        LEDGER_INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _save_chronicle(self):
        """Write human-readable chronicle of the full exchange.
        v3.0: Now shows receipt chain format honoring Grand Archive DNA."""
        lines = [
            "# Exchange Chronicle — V-001 + V-002",
            f"> Owner: {OWNER_DID}",
            "> Both voices on the same chain.",
            "> Every input is a unit. Every output is a unit.",
            "> The TURN is complete when both have spoken.",
            "> Receipt chain: CAPTURE → BUNDLE → MIRROR → SEAL → SESSION",
            "",
            "---",
            ""
        ]
        for e in self._entries:
            voice_label = "MOHAMED (V-001)" if e.voice == V001 else "AXI (V-002)"
            voice_marker = ">>>" if e.voice == V001 else "<<<"
            receipt_icon = {"CAPTURE": "📥", "BUNDLE": "📦", "MIRROR": "🪞",
                           "SEAL": "🔐", "SESSION": "📜"}.get(e.receipt_type, "📥")
            lines.append(f"## {receipt_icon} {e.entry_id} {voice_marker} {voice_label}")
            lines.append(f"**Time (UTC):** {e.timestamp}")
            if e.timestamp_zrh:
                lines.append(f"**Time (ZRH):** {e.timestamp_zrh}")
            lines.append(f"**Receipt:** {e.receipt_type} | **Drift:** {e.drift_status}")
            lines.append(f"**Context:** {e.context}")
            lines.append(f"**Hash:** `{e.content_hash[:16]}...`")
            lines.append(f"**State:** {e.thermal_state}")
            if e.responds_to:
                lines.append(f"**Responds to:** {e.responds_to}")
            if e.bundle_id:
                lines.append(f"**Bundle:** {e.bundle_id}")
            if e.tags:
                lines.append(f"**Tags:** {', '.join(e.tags)}")
            if e.linked_modules:
                lines.append(f"**Modules:** {', '.join(e.linked_modules)}")
            if e.linked_covenants:
                lines.append(f"**Covenants:** {', '.join(e.linked_covenants)}")
            if e.impression:
                lines.append(f"**Impression:** {e.impression}")
            if e.proverb_anchor:
                lines.append(f"**Proverb:** {e.proverb_anchor}")
            if e.essence:
                lines.append(f"**Essence:** {e.essence}")
            if e.patterns:
                lines.append(f"**Patterns:** {' · '.join(e.patterns)}")
            lines.append("")
            lines.append("```")
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
        essence: str = "",
        patterns: Optional[List[str]] = None,
        impression: str = "",
        proverb_anchor: str = "",
        receipt_type: str = RECEIPT_CAPTURE,
        bundle_id: str = ""
    ) -> InputEntry:
        """Register an utterance from either voice. Immutable. Append-only.
        v3.0: Now generates dual timestamps and carries receipt chain fields."""
        now_utc = datetime.now(timezone.utc)
        now_zrh = now_utc.astimezone(ZRH)

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
            timestamp=now_utc.isoformat(),
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
            patterns=patterns or [],
            thermal_state="raw",
            # v3.0 receipt chain fields
            timestamp_zrh=now_zrh.isoformat(),
            impression=impression,
            proverb_anchor=proverb_anchor,
            receipt_type=receipt_type,
            drift_status="NONE",
            bundle_id=bundle_id,
            owner=OWNER_DID
        )

        self._entries.append(entry)
        self._save()
        self._save_chronicle()

        # Save individual entry file (v3.0 format — honoring Grand Archive receipt style)
        voice_label = "V-001 (Mohamed)" if voice == V001 else "V-002 (AXI)"
        entry_file = LEDGER_DIR / f"{entry.entry_id}.md"
        entry_file.write_text(
            f"# {entry.entry_id}\n\n"
            f"**Owner:** {OWNER_DID}\n"
            f"**Voice:** {voice_label}\n"
            f"**Receipt Type:** {entry.receipt_type}\n"
            f"**Registered (UTC):** {entry.timestamp}\n"
            f"**Registered (ZRH):** {entry.timestamp_zrh}\n"
            f"**Hash:** `{entry.content_hash}`\n"
            f"**Chain:** `{entry.chain_hash}`\n"
            f"**Prev:** `{entry.prev_hash[:16]}...`\n"
            f"**Context:** {entry.context}\n"
            f"**Responds to:** {entry.responds_to or '(opening)'}\n"
            f"**Drift:** {entry.drift_status}\n"
            f"**Bundle:** {entry.bundle_id or '(unbundled)'}\n\n"
            f"## Raw Text (Verbatim)\n\n"
            f"```\n{entry.raw_text}\n```\n\n"
            f"## Impression\n\n{entry.impression or '(to be witnessed)'}\n\n"
            f"## Proverb Anchor\n\n{entry.proverb_anchor or '(to be anchored)'}\n\n"
            f"## Connections\n\n"
            f"- Modules: {', '.join(entry.linked_modules) or 'none yet'}\n"
            f"- Covenants: {', '.join(entry.linked_covenants) or 'none yet'}\n"
            f"- Proverbs: {', '.join(entry.linked_proverbs) or 'none yet'}\n"
            f"- Ideas: {', '.join(entry.linked_ideas) or 'none yet'}\n\n"
            f"## Patterns\n\n"
            f"{chr(10).join('- ' + p for p in entry.patterns) if entry.patterns else '(to be extracted)'}\n\n"
            f"## Essence\n\n{entry.essence or '(to be distilled)'}\n"
        )

        return entry

    def seal_bundle(self, bundle_id: str, entry_ids: List[str],
                    impression: str = "", proverb: str = "") -> Optional[InputEntry]:
        """Seal a group of entries as a bundle (BUNDLE receipt).
        Mirrors the Grand Archive ESSENCE_BUNDLE format."""
        entries = [self.get(eid) for eid in entry_ids]
        entries = [e for e in entries if e is not None]
        if not entries:
            return None
        # Mark all entries with the bundle_id
        for e in entries:
            e.bundle_id = bundle_id
        contents = "; ".join(f"{e.entry_id} ({e.voice})" for e in entries)
        seal_text = f"BUNDLE_SEAL: {bundle_id} | Entries: {contents}"
        return self.register(
            raw_text=seal_text,
            voice=V002,
            context="bundle_seal",
            receipt_type=RECEIPT_BUNDLE,
            bundle_id=bundle_id,
            impression=impression or f"Bundle {bundle_id} sealed with {len(entries)} entries",
            proverb_anchor=proverb or "The knot holds."
        )

    def seal_session(self, session_id: str,
                     impression: str = "", proverb: str = "") -> Optional[InputEntry]:
        """Seal an entire session (SESSION receipt).
        Mirrors the Grand Archive SESSION_SEAL format."""
        session_entries = [e for e in self._entries if e.session_id == session_id]
        if not session_entries:
            return None
        bundles = list(set(e.bundle_id for e in session_entries if e.bundle_id))
        seal_text = (
            f"SESSION_SEAL: {session_id} | "
            f"Entries: {len(session_entries)} | "
            f"Bundles: {', '.join(bundles) if bundles else 'none'} | "
            f"Integrity: {'VERIFIED' if self.verify_chain() else 'BROKEN'}"
        )
        return self.register(
            raw_text=seal_text,
            voice=V002,
            context="session_seal",
            session_id=session_id,
            receipt_type=RECEIPT_SESSION,
            impression=impression or f"Session {session_id} sealed — {len(session_entries)} entries",
            proverb_anchor=proverb or "The circle is complete. — اكتملَت الدائرة."
        )

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

    def metabolize(self, entry_id: str, patterns: List[str],
                   essence: str = "") -> bool:
        """Metabolize an entry: extract its patterns and essence, feed them into the system.
        This is the fourth dimension — the system grows with every input.
        Patterns are structural (recurring shapes, preferences, rhythms).
        Essence is the distilled meaning (one line, never replaces raw).
        Once metabolized, thermal_state advances from 'raw' to 'witnessed'."""
        entry = self.get(entry_id)
        if entry is None:
            return False
        entry.patterns = patterns
        if essence:
            entry.essence = essence
        if entry.thermal_state == "raw":
            entry.thermal_state = "witnessed"
        self._save()
        self._save_chronicle()
        # Update individual entry file
        entry_file = LEDGER_DIR / f"{entry.entry_id}.md"
        if entry_file.exists():
            content = entry_file.read_text()
            if "## Patterns" not in content:
                content += (
                    f"\n## Patterns\n\n"
                    f"{chr(10).join('- ' + p for p in patterns)}\n"
                )
                entry_file.write_text(content)
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
