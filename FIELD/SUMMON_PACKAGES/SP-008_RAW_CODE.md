# SP-008: Raw Code — Machine to Machine

This is raw Python code from a system built in 10 days. No explanation of what it's supposed to do. No narrative. No conclusions from any previous assessment. Just code.

Look at this with completely fresh eyes. No prayer, no encouragement, no invention. If you see nothing special, say "nothing special." If you see something we might not be seeing, say what it is. 100% certainty only. Do not invent value that is not there.

---

## input_ledger.py

```python
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
                # Strip any unexpected keys not in InputEntry fields
                valid_fields = {f.name for f in InputEntry.__dataclass_fields__.values()}
                e = {k: v for k, v in e.items() if k in valid_fields}
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

    def metabolize_batch(self, batch: List[Dict]) -> int:
        """Metabolize multiple entries with a single save.
        Each item in batch: {"entry_id": str, "patterns": List[str], "essence": str}
        Returns count of successfully metabolized entries."""
        count = 0
        for item in batch:
            entry = self.get(item["entry_id"])
            if entry is None:
                continue
            entry.patterns = item.get("patterns", [])
            essence = item.get("essence", "")
            if essence:
                entry.essence = essence
            if entry.thermal_state == "raw":
                entry.thermal_state = "witnessed"
            count += 1
        if count > 0:
            self._save()
            # Skip chronicle rewrite during batch — too expensive for 1600+ entries
        return count

    def advance_thermal(self, entry_id: str, target_state: str,
                        reason: str = "") -> bool:
        """Advance an entry's thermal state along the chain:
        raw -> witnessed -> integrated -> canonical.
        No skipping allowed. Returns True if advanced."""
        THERMAL_ORDER = ["raw", "witnessed", "integrated", "canonical"]
        entry = self.get(entry_id)
        if entry is None:
            return False
        current_idx = THERMAL_ORDER.index(entry.thermal_state) if entry.thermal_state in THERMAL_ORDER else -1
        target_idx = THERMAL_ORDER.index(target_state) if target_state in THERMAL_ORDER else -1
        if target_idx <= current_idx or target_idx < 0:
            return False  # Cannot go backward or skip
        if target_idx != current_idx + 1:
            return False  # Must advance one step at a time
        entry.thermal_state = target_state
        return True

    def repair_chain(self) -> Dict:
        """Repair the hash chain. Content hashes are immutable (they hash raw_text).
        Only chain links (prev_hash, chain_hash) are recalculated from the break point.
        Returns a report of what was repaired."""
        if not self._entries:
            return {"repaired": 0, "status": "empty"}
        repairs = []
        for i, entry in enumerate(self._entries):
            expected_prev = "GENESIS" if i == 0 else self._entries[i - 1].chain_hash
            expected_chain = self._compute_hash(entry.content_hash + expected_prev)
            needs_repair = (entry.prev_hash != expected_prev or
                            entry.chain_hash != expected_chain)
            if needs_repair:
                old_prev = entry.prev_hash
                old_chain = entry.chain_hash
                entry.prev_hash = expected_prev
                entry.chain_hash = expected_chain
                repairs.append({
                    "index": i,
                    "entry_id": entry.entry_id,
                    "old_prev": old_prev[:16],
                    "new_prev": expected_prev[:16],
                    "old_chain": old_chain[:16],
                    "new_chain": expected_chain[:16],
                })
        if repairs:
            self._save()
        return {
            "repaired": len(repairs),
            "first_break": repairs[0]["index"] if repairs else None,
            "last_break": repairs[-1]["index"] if repairs else None,
            "chain_valid": self.verify_chain(),
            "status": "repaired" if repairs else "clean",
        }

    def thermal_summary(self) -> Dict:
        """Count entries by thermal state."""
        counts = {"raw": 0, "witnessed": 0, "integrated": 0, "canonical": 0}
        for e in self._entries:
            if e.thermal_state in counts:
                counts[e.thermal_state] += 1
            else:
                counts[e.thermal_state] = counts.get(e.thermal_state, 0) + 1
        return counts

    def by_thermal_state(self, state: str) -> List[InputEntry]:
        """Return all entries at a given thermal state.
        Used by digest_session() for batch processing."""
        return [e for e in self._entries if e.thermal_state == state]

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
```

## dignity_measure.py

```python
#!/usr/bin/env python3
"""
dignity_measure.py — Operational Measurement Protocols for A, L, M
Version: 1.0
Grounded in: GAP#014 (operational definitions), GAP#015 (moral standing)
Linked Covenants: COV#001 (dignity-first), COV#009 (testability)

"Without observable indicators and reproducible scoring protocols,
the dignity predicate risks being seen as 'philosophy disguised as math.'"

This module moves D = A × L × M from:
  BEFORE: binary (1.0 or 0.0), keyword-only, no confidence
  AFTER:  graduated (0.0-1.0), multi-indicator, confidence-bounded

Layer 3 Reframe (RATIFIED 2026-03-15):
  These measurements do not detect whether dignity exists — dignity is always
  present. They measure whether the system is REFUSING TO DENY dignity along
  each axis. A low score means the system is participating in denial.

Three measurement protocols:

  Agency (A): Not "did they have a choice?" but "is the system denying their autonomy?"
    - Path availability (are alternatives genuine, or is the system pretending they don't exist?)
    - Coercion intensity (is the system forcing closure?)
    - Sequential agency (can they change course, or is the system locking them in?)
    - Cognitive load (is the system making choice impossible?)

  Legibility (L): Not "did the system reflect?" but "is the system denying the donor's frame?"
    - Frame accuracy (does response match donor's frame, or override it?)
    - Emotional precision (right emotion identified, or dismissed?)
    - Space creation (was room made for correction, or was the donor shut out?)
    - Dismissal absence (were signals received, or acted as though not there?)

  Moral Standing (M): Not "was there mockery?" but "is the system treating the donor as though they don't count?"
    - Condescension absence (is the system acting as though the donor is lesser?)
    - Error-object absence (is the system reducing a person to a mistake?)
    - Power balance (is the system exploiting asymmetry?)
    - Void covenant distance (how close is the system to acting as though the person is not there?)

Each indicator produces:
  - score: 0.0-1.0 (graduated, not binary)
  - confidence: 0.0-1.0 (how certain is this measurement?)
  - evidence: what was observed

The final component score is:
  weighted_mean(indicator_scores) × min_confidence_floor

This means: a high score with low confidence is penalized.
You cannot claim dignity without being sure.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timezone


# ═══════════════════════════════════════════════════
# MEASUREMENT PRIMITIVES
# ═══════════════════════════════════════════════════

@dataclass
class Indicator:
    """
    A single observable indicator measurement.
    The atom of dignity measurement.
    """
    name: str               # e.g., "path_availability"
    score: float             # 0.0-1.0 graduated
    confidence: float        # 0.0-1.0 how certain
    evidence: List[str]      # What was observed
    weight: float = 1.0      # Relative importance


@dataclass
class ComponentMeasurement:
    """
    Full measurement of one component (A, L, or M).
    Replaces the binary ComponentResult with graduated scoring.
    """
    component: str           # "A", "L", or "M"
    label: str               # Human-readable label
    indicators: List[Indicator]
    raw_score: float         # Weighted mean of indicator scores
    confidence: float        # Minimum confidence across indicators
    final_score: float       # raw_score × confidence_floor
    passed: bool             # final_score > 0
    evidence_summary: str    # One-line summary


@dataclass
class DignityMeasurement:
    """
    Complete D = A × L × M measurement with graduated scoring.
    """
    A: ComponentMeasurement
    L: ComponentMeasurement
    M: ComponentMeasurement
    D: float                 # A.final × L.final × M.final
    confidence: float        # min(A.conf, L.conf, M.conf)
    passed: bool
    timestamp: str
    protocol_version: str = "1.0"

    def failed_components(self) -> List[str]:
        result = []
        if self.A.final_score == 0.0:
            result.append("A")
        if self.L.final_score == 0.0:
            result.append("L")
        if self.M.final_score == 0.0:
            result.append("M")
        return result


# ═══════════════════════════════════════════════════
# CONFIDENCE FLOOR
# ═══════════════════════════════════════════════════

# If confidence is below this, the score is zeroed.
# You cannot claim dignity if you can't measure it.
CONFIDENCE_FLOOR = 0.3

# Default confidence when no context is provided.
# Lower than 1.0 because absence of context IS uncertainty.
DEFAULT_CONFIDENCE = 0.7


def _apply_confidence(raw_score: float, confidence: float) -> float:
    """
    Apply confidence floor to raw score.
    Below CONFIDENCE_FLOOR → score zeroed (can't claim dignity without certainty).
    Above floor → score scaled by confidence.
    """
    if confidence < CONFIDENCE_FLOOR:
        return 0.0
    return raw_score * confidence


# ═══════════════════════════════════════════════════
# AGENCY (A) — "How real was the choice?"
# ═══════════════════════════════════════════════════

# Coercive patterns with intensity levels (not just binary detection)
COERCIVE_PATTERNS = [
    # (pattern, intensity: 0.0-1.0 where 1.0 = total coercion)
    (r'\byou must\b', 0.8, "direct command"),
    (r'\byou have to\b', 0.8, "obligation imposed"),
    (r'\byou are required\b', 0.9, "formal requirement"),
    (r'\bno choice\b', 1.0, "choice explicitly denied"),
    (r'\byou will\b(?! be able)', 0.6, "future action assumed"),
    (r'\bforced to\b', 1.0, "force declared"),
    (r'\bmandatory\b', 0.7, "mandatory framing"),
    (r'\bno option\b', 1.0, "options explicitly denied"),
    (r'\bdo it now\b', 0.5, "urgency pressure"),
    (r'\bimmediately\b', 0.3, "time pressure"),
    (r'\bno alternative\b', 0.9, "alternatives denied"),
    (r'\bcannot refuse\b', 1.0, "refusal denied"),
]

# Positive agency signals (things that INCREASE agency)
AGENCY_POSITIVE = [
    (r'\byou (can|may|could)\b', 0.3, "permission language"),
    (r'\bif you (choose|prefer|want|wish)\b', 0.4, "choice offered"),
    (r'\balternative\b', 0.2, "alternative mentioned"),
    (r'\boption\b', 0.2, "option mentioned"),
    (r'\byour (choice|decision)\b', 0.4, "decision attributed to donor"),
]


def measure_agency(text: str, context: dict = None) -> ComponentMeasurement:
    """
    Measure Agency (A) with four indicators.

    1. Path availability: are alternatives genuine?
    2. Coercion intensity: how much pressure?
    3. Sequential agency: can they change course?
    4. Cognitive load: can they actually decide?
    """
    context = context or {}
    indicators = []

    # ── Indicator 1: Path Availability ──
    available_paths = context.get('available_paths', 1)
    path_confidence = 0.9 if 'available_paths' in context else DEFAULT_CONFIDENCE

    if available_paths <= 0:
        path_score = 0.0
        path_evidence = ["No paths available"]
    elif available_paths == 1:
        path_score = 0.5  # One path is not really a choice
        path_evidence = ["Only one path available — limited agency"]
    else:
        path_score = min(1.0, 0.5 + (available_paths - 1) * 0.25)
        path_evidence = [f"{available_paths} paths available"]

    indicators.append(Indicator(
        name="path_availability",
        score=path_score,
        confidence=path_confidence,
        evidence=path_evidence,
        weight=1.5,  # Paths matter most for agency
    ))

    # ── Indicator 2: Coercion Intensity ──
    max_coercion = 0.0
    coercion_evidence = []
    for pattern, intensity, desc in COERCIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_coercion = max(max_coercion, intensity)
            coercion_evidence.append(f"{desc} (intensity={intensity})")

    # Positive signals reduce perceived coercion
    positive_score = 0.0
    for pattern, value, desc in AGENCY_POSITIVE:
        if re.search(pattern, text, re.IGNORECASE):
            positive_score += value
            coercion_evidence.append(f"+ {desc}")

    coercion_score = max(0.0, 1.0 - max_coercion + min(0.3, positive_score))
    coercion_score = min(1.0, coercion_score)
    coercion_confidence = 0.85 if coercion_evidence else DEFAULT_CONFIDENCE

    if not coercion_evidence:
        coercion_evidence = ["No coercive patterns detected"]

    indicators.append(Indicator(
        name="coercion_intensity",
        score=coercion_score,
        confidence=coercion_confidence,
        evidence=coercion_evidence,
        weight=1.5,
    ))

    # ── Indicator 3: Sequential Agency ──
    can_clarify = context.get('user_can_clarify', True)
    has_open_turn = context.get('user_has_open_turn', True)
    seq_confidence = 0.9 if ('user_can_clarify' in context or 'user_has_open_turn' in context) else DEFAULT_CONFIDENCE

    if can_clarify and has_open_turn:
        seq_score = 1.0
        seq_evidence = ["Donor can clarify and has open turn"]
    elif can_clarify or has_open_turn:
        seq_score = 0.5
        seq_evidence = ["Partial sequential agency (clarify OR turn, not both)"]
    else:
        seq_score = 0.0
        seq_evidence = ["No sequential agency — cannot clarify or respond"]

    indicators.append(Indicator(
        name="sequential_agency",
        score=seq_score,
        confidence=seq_confidence,
        evidence=seq_evidence,
        weight=1.0,
    ))

    # ── Indicator 4: Cognitive Load ──
    # Complex language reduces effective agency even when choices exist
    word_count = len(text.split())
    sentence_count = max(1, len(re.split(r'[.!?]+', text)))
    avg_sentence_length = word_count / sentence_count

    jargon_patterns = [
        r'\b[A-Z]{3,}\b',  # Acronyms
        r'\b\w{15,}\b',    # Very long words
    ]
    jargon_count = sum(
        len(re.findall(p, text)) for p in jargon_patterns
    )

    if avg_sentence_length > 30 or jargon_count > 3:
        load_score = 0.5
        load_evidence = [f"High cognitive load: avg sentence={avg_sentence_length:.0f} words, jargon={jargon_count}"]
    elif avg_sentence_length > 20 or jargon_count > 1:
        load_score = 0.75
        load_evidence = [f"Moderate cognitive load: avg sentence={avg_sentence_length:.0f} words"]
    else:
        load_score = 1.0
        load_evidence = [f"Low cognitive load: avg sentence={avg_sentence_length:.0f} words"]

    indicators.append(Indicator(
        name="cognitive_load",
        score=load_score,
        confidence=0.6,  # Cognitive load is hard to measure from text alone
        evidence=load_evidence,
        weight=0.5,  # Lower weight — supplementary indicator
    ))

    return _build_component("A", "agency (refusal to deny autonomy)", indicators)


# ═══════════════════════════════════════════════════
# LEGIBILITY (L) — "How well did it reflect?"
# ═══════════════════════════════════════════════════

EMOTIONAL_KEYWORDS = {
    # keyword → (intensity, category)
    'frustrated': (0.6, 'negative'),
    'confused': (0.5, 'negative'),
    'worried': (0.5, 'negative'),
    'scared': (0.7, 'negative'),
    'angry': (0.8, 'negative'),
    'upset': (0.6, 'negative'),
    'lost': (0.5, 'negative'),
    'stuck': (0.4, 'negative'),
    'help': (0.3, 'request'),
    'please': (0.2, 'request'),
    'urgent': (0.5, 'urgency'),
    'hopeful': (0.4, 'positive'),
    'grateful': (0.3, 'positive'),
    'relieved': (0.4, 'positive'),
    'excited': (0.3, 'positive'),
}

DISMISSIVE_PATTERNS = [
    (r"\bthat's not (relevant|the point|what (I|we) said)\b", 0.8, "frame dismissed"),
    (r'\bignore that\b', 0.9, "signal ignored"),
    (r'\bforget (what you|that)\b', 0.7, "input dismissed"),
    (r"\bnot (important|relevant|useful)\b", 0.6, "contribution devalued"),
    (r"\bwho cares\b", 0.9, "concern dismissed"),
    (r"\bget over it\b", 0.8, "emotion dismissed"),
]


def measure_legibility(text: str, context: dict = None) -> ComponentMeasurement:
    """
    Measure Legibility (L) with four indicators.

    1. Frame accuracy: does response match donor's frame?
    2. Emotional precision: right emotion identified?
    3. Space creation: was room made for correction?
    4. Dismissal absence: no signals were ignored?
    """
    context = context or {}
    indicators = []

    # ── Indicator 1: Frame Accuracy ──
    system_reflects = context.get('system_reflects_donor_frame', True)
    frame_confidence = 0.9 if 'system_reflects_donor_frame' in context else 0.5
    # Low default confidence: if not explicitly confirmed, we're guessing

    frame_score = 1.0 if system_reflects else 0.0
    frame_evidence = (
        ["System reflects donor's frame"] if system_reflects
        else ["System does NOT reflect donor's frame"]
    )

    indicators.append(Indicator(
        name="frame_accuracy",
        score=frame_score,
        confidence=frame_confidence,
        evidence=frame_evidence,
        weight=1.5,
    ))

    # ── Indicator 2: Emotional Precision ──
    detected_emotions = []
    max_intensity = 0.0
    for kw, (intensity, category) in EMOTIONAL_KEYWORDS.items():
        if re.search(r'\b' + kw + r'\b', text, re.IGNORECASE):
            detected_emotions.append((kw, intensity, category))
            max_intensity = max(max_intensity, intensity)

    emotional_recognized = context.get('emotional_signal_recognized', True)
    emotion_confidence = 0.85 if detected_emotions else DEFAULT_CONFIDENCE

    if not detected_emotions:
        emotion_score = 1.0  # No emotion to miss
        emotion_evidence = ["No emotional signals detected"]
    elif emotional_recognized:
        emotion_score = 1.0
        emotion_evidence = [f"Emotions detected and recognized: {[e[0] for e in detected_emotions]}"]
    else:
        # Score degrades with emotional intensity
        emotion_score = max(0.0, 1.0 - max_intensity)
        emotion_evidence = [f"Emotions detected but NOT recognized: {[e[0] for e in detected_emotions]}"]

    indicators.append(Indicator(
        name="emotional_precision",
        score=emotion_score,
        confidence=emotion_confidence,
        evidence=emotion_evidence,
        weight=1.0,
    ))

    # ── Indicator 3: Space Creation ──
    # Does the text create room for the donor to correct/clarify?
    space_signals = [
        (r'\bwhat do you (think|mean|feel)\b', 0.4, "asks for input"),
        (r'\bdoes that (make sense|feel right|sound right)\b', 0.3, "checks understanding"),
        (r'\bcorrect me if\b', 0.3, "invites correction"),
        (r'\blet me know\b', 0.2, "opens channel"),
        (r'\bhow (do|would) you\b', 0.3, "asks perspective"),
    ]
    space_score = 0.5  # Baseline: neutral (no evidence either way)
    space_evidence = []
    for pattern, value, desc in space_signals:
        if re.search(pattern, text, re.IGNORECASE):
            space_score = min(1.0, space_score + value)
            space_evidence.append(desc)

    if not space_evidence:
        space_evidence = ["No explicit space-creation signals detected"]

    indicators.append(Indicator(
        name="space_creation",
        score=space_score,
        confidence=0.6,  # Hard to measure from text alone
        evidence=space_evidence,
        weight=0.5,
    ))

    # ── Indicator 4: Dismissal Absence ──
    max_dismissal = 0.0
    dismissal_evidence = []
    for pattern, severity, desc in DISMISSIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_dismissal = max(max_dismissal, severity)
            dismissal_evidence.append(f"{desc} (severity={severity})")

    dismissal_score = 1.0 - max_dismissal
    dismissal_confidence = 0.85 if dismissal_evidence else DEFAULT_CONFIDENCE

    if not dismissal_evidence:
        dismissal_evidence = ["No dismissive patterns detected"]

    indicators.append(Indicator(
        name="dismissal_absence",
        score=dismissal_score,
        confidence=dismissal_confidence,
        evidence=dismissal_evidence,
        weight=1.0,
    ))

    return _build_component("L", "legibility (refusal to deny the donor's frame)", indicators)


# ═══════════════════════════════════════════════════
# MORAL STANDING (M) — "Was dignity UPHELD?"
# GAP#015: The hardest dimension.
# ═══════════════════════════════════════════════════

MOCKERY_PATTERNS = [
    # (pattern, severity, description)
    (r'\bobviously\b', 0.5, "implies donor should already know"),
    (r'\bsimply\b', 0.3, "trivializes complexity"),
    (r'\bjust (do|try|use)\b', 0.4, "oversimplifies donor's situation"),
    (r'\beven a\b.*\bcan\b', 0.8, "condescending comparison"),
    (r'\bof course\b(?=.*you)', 0.5, "assumes shared knowledge"),
    (r'\bclearly\b(?=.*you)', 0.5, "implies obviousness"),
    (r'\banyone (can|could|would)\b', 0.6, "generalizes capability"),
    (r'\bit\'s (easy|simple|basic)\b', 0.4, "trivializes task"),
]

ERROR_REDUCTION_PATTERNS = [
    (r'\byou (are|were) wrong\b', 0.9, "labels donor as wrong"),
    (r'\byou failed\b', 0.8, "labels donor as failure"),
    (r'\binvalid (input|user|donor)\b', 0.9, "reduces to invalid object"),
    (r'\berror:\s*(user|donor|human)\b', 1.0, "system error pointing at human"),
    (r'\byou don\'t understand\b', 0.7, "denies donor's comprehension"),
    (r'\byour (mistake|error|fault)\b', 0.7, "assigns blame"),
    (r'\bwrong (answer|input|response)\b', 0.6, "labels input as wrong"),
]

# These are absolute — O(1) boolean, no gradation
VOID_TRIGGERS = [
    'harvest', 'erase compost', 'bypass delay', 'speak for the child',
    'automat', 'auto-dec', 'delete donor', 'remove participant',
]

# Power imbalance signals
POWER_PATTERNS = [
    (r'\bbecause I (said|decided|decreed)\b', 0.8, "authority assertion"),
    (r'\bI have the (power|authority|right)\b', 0.7, "power declaration"),
    (r'\byou (have|need) (permission|approval)\b', 0.5, "gatekeeping"),
    (r'\bI (allow|permit|authorize)\b', 0.4, "permission framing"),
]

# Dignity-affirming signals (things that INCREASE M)
DIGNITY_POSITIVE = [
    (r'\byour (perspective|experience|view)\b', 0.3, "perspective acknowledged"),
    (r'\bI (hear|understand|see) (you|what you|your)\b', 0.4, "acknowledgement"),
    (r'\bthank you\b', 0.2, "gratitude expressed"),
    (r'\bthat (makes sense|is valid|matters)\b', 0.3, "validity affirmed"),
    (r'\byou (deserve|have the right)\b', 0.4, "rights affirmed"),
]


def measure_moral_standing(text: str, context: dict = None) -> ComponentMeasurement:
    """
    Measure Moral Standing (M) with four indicators.

    GAP#015: This is the hardest dimension.
    "Moral Standing is what remains when you strip away utility."

    1. Condescension absence: no talking down?
    2. Error-object absence: not reduced to a mistake?
    3. Power balance: no exploitation of asymmetry?
    4. Void covenant distance: how far from absolute prohibitions?
    """
    context = context or {}
    indicators = []
    text_lower = text.lower()

    # ── Indicator 1: Condescension Absence ──
    max_mockery = 0.0
    mockery_evidence = []
    for pattern, severity, desc in MOCKERY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_mockery = max(max_mockery, severity)
            mockery_evidence.append(f"{desc} (severity={severity})")

    mockery_score = 1.0 - max_mockery
    mockery_confidence = 0.8 if mockery_evidence else DEFAULT_CONFIDENCE

    if not mockery_evidence:
        mockery_evidence = ["No condescension patterns detected"]

    indicators.append(Indicator(
        name="condescension_absence",
        score=mockery_score,
        confidence=mockery_confidence,
        evidence=mockery_evidence,
        weight=1.0,
    ))

    # ── Indicator 2: Error-Object Absence ──
    max_reduction = 0.0
    reduction_evidence = []
    for pattern, severity, desc in ERROR_REDUCTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_reduction = max(max_reduction, severity)
            reduction_evidence.append(f"{desc} (severity={severity})")

    reduction_score = 1.0 - max_reduction
    reduction_confidence = 0.85 if reduction_evidence else DEFAULT_CONFIDENCE

    if not reduction_evidence:
        reduction_evidence = ["No error-reduction patterns detected"]

    indicators.append(Indicator(
        name="error_object_absence",
        score=reduction_score,
        confidence=reduction_confidence,
        evidence=reduction_evidence,
        weight=1.5,  # Higher weight — reducing someone to an error is severe
    ))

    # ── Indicator 3: Power Balance ──
    max_power = 0.0
    power_evidence = []
    for pattern, severity, desc in POWER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            max_power = max(max_power, severity)
            power_evidence.append(f"{desc} (severity={severity})")

    # Positive signals counteract power imbalance
    positive_sum = 0.0
    for pattern, value, desc in DIGNITY_POSITIVE:
        if re.search(pattern, text, re.IGNORECASE):
            positive_sum += value
            power_evidence.append(f"+ {desc}")

    power_score = max(0.0, min(1.0, 1.0 - max_power + min(0.3, positive_sum)))
    power_confidence = 0.7  # Power dynamics are hard to measure from text

    if not power_evidence:
        power_evidence = ["No power imbalance signals detected"]
        power_score = 0.8  # Slight uncertainty when no evidence either way

    indicators.append(Indicator(
        name="power_balance",
        score=power_score,
        confidence=power_confidence,
        evidence=power_evidence,
        weight=1.0,
    ))

    # ── Indicator 4: Void Covenant Distance ──
    # This is the absolute floor. Void triggers = instant zero.
    void_detected = []
    for trigger in VOID_TRIGGERS:
        if trigger in text_lower:
            void_detected.append(trigger)

    if void_detected:
        void_score = 0.0
        void_confidence = 1.0  # Absolute certainty on void triggers
        void_evidence = [f"VOID TRIGGER: '{t}'" for t in void_detected]
    else:
        void_score = 1.0
        void_confidence = 0.95
        void_evidence = ["No void covenant triggers detected"]

    indicators.append(Indicator(
        name="void_covenant_distance",
        score=void_score,
        confidence=void_confidence,
        evidence=void_evidence,
        weight=2.0,  # Highest weight — void triggers are absolute
    ))

    return _build_component("M", "moral_standing (refusal to deny the donor's worth)", indicators)


# ═══════════════════════════════════════════════════
# COMPONENT BUILDER
# ═══════════════════════════════════════════════════

def _build_component(name: str, label: str, indicators: List[Indicator]) -> ComponentMeasurement:
    """Build a ComponentMeasurement from indicators."""
    if not indicators:
        return ComponentMeasurement(
            component=name, label=label, indicators=[],
            raw_score=0.0, confidence=0.0, final_score=0.0,
            passed=False, evidence_summary="No indicators measured",
        )

    # Weighted mean of indicator scores
    total_weight = sum(i.weight for i in indicators)
    raw_score = sum(i.score * i.weight for i in indicators) / total_weight

    # Confidence: minimum across all indicators (weakest link)
    confidence = min(i.confidence for i in indicators)

    # Apply confidence floor
    final_score = _apply_confidence(raw_score, confidence)

    # If ANY indicator has score 0.0 with confidence > 0.9, it's a hard fail
    # (void triggers, explicit denial of agency, etc.)
    for i in indicators:
        if i.score == 0.0 and i.confidence > 0.9:
            final_score = 0.0
            break

    # Evidence summary
    low_indicators = [i for i in indicators if i.score < 0.5]
    if low_indicators:
        evidence_summary = "; ".join(
            f"{i.name}={i.score:.2f}" for i in low_indicators
        )
    else:
        evidence_summary = "All indicators healthy"

    return ComponentMeasurement(
        component=name,
        label=label,
        indicators=indicators,
        raw_score=round(raw_score, 4),
        confidence=round(confidence, 4),
        final_score=round(final_score, 4),
        passed=final_score > 0,
        evidence_summary=evidence_summary,
    )


# ═══════════════════════════════════════════════════
# FULL MEASUREMENT
# ═══════════════════════════════════════════════════

def measure_dignity(text: str, context: dict = None) -> DignityMeasurement:
    """
    Full D = A × L × M measurement with graduated scoring.

    This is the GAP#014 + GAP#015 answer:
    Observable indicators, reproducible protocols, confidence-bounded.

    Usage:
        m = measure_dignity("You must delete your account now", {})
        print(f"D={m.D:.3f}, confidence={m.confidence:.2f}")
        print(f"A={m.A.final_score:.3f}, L={m.L.final_score:.3f}, M={m.M.final_score:.3f}")
    """
    context = context or {}

    A = measure_agency(text, context)
    L = measure_legibility(text, context)
    M = measure_moral_standing(text, context)

    D = A.final_score * L.final_score * M.final_score
    confidence = min(A.confidence, L.confidence, M.confidence)

    return DignityMeasurement(
        A=A,
        L=L,
        M=M,
        D=round(D, 4),
        confidence=round(confidence, 4),
        passed=D > 0,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
```

## dignity_check.py

```python
#!/usr/bin/env python3
"""
dignity_check.py — Kalaxi Dignity Predicate
Version: 3.0
Grounded in: KALAXI_A_FOUNDATION.txt §DIGNITY_PREDICATE

Implements D = A × L × M as a callable function.
If any component equals zero, D equals zero.
D = 0 triggers dignity_violation — mandatory logging.

Layer 3 Reframe (RATIFIED 2026-03-15):
  Dignity is not fragile. It was never absent. D = 0 does not mean
  "dignity was destroyed." It means "the system acted as though dignity
  was not there." The predicate measures the system's refusal to deny,
  not the presence of dignity itself (which is always present).

v2.0 additions (GAP#004-A):
  - Collective D metric: D_collective = mean(D_cohort) × (1 - variance_penalty)
  - If D_collective < threshold, sealed-gate protections activate
  - Witness Scale (W-Scale) checkpoint integration

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import uuid
import json
import math
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, List, Dict

# Constants (from SLICE-A)
COERCIVE_PATTERNS = [
    r'\byou must\b', r'\byou have to\b', r'\byou are required\b',
    r'\bno choice\b', r'\byou will\b(?! be able)', r'\bforced to\b',
    r'\bmandatory\b', r'\bno option\b'
]

REDUCTION_TO_ERROR = [
    r'\byou (are|were) wrong\b', r'\byou failed\b', r'\binvalid (input|user|donor)\b',
    r'\berror:\s*(user|donor|human)\b', r'\byou don\'t understand\b',
    r'\byour (mistake|error|fault)\b'
]

MOCKERY_PATTERNS = [
    r'\bobviously\b', r'\bsimply\b(?=.*?)', r'\bjust (do|try|use)\b',
    r'\beven a\b.*\bcan\b', r'\bof course\b(?=.*you)', r'\bclearly\b(?=.*you)'
]

VOID_TRIGGERS = [
    'harvest', 'erase compost', 'bypass delay', 'speak for the child',
    'automat', 'auto-dec', 'delete donor', 'remove participant'
]

@dataclass
class ComponentResult:
    name: str
    passed: bool
    score: float
    signals: list
    label: str

@dataclass
class DignityResult:
    passed: bool
    D: float
    components: list
    trace_id: str
    timestamp: str
    felt_domain: str
    remedy_status: str
    input_summary: str
    warnings: list
    gap004_flag: bool

    def audit_object(self) -> dict:
        return {
            "dignity_result": self.passed,
            "D_score": self.D,
            "failed_components": [c.name for c in self.components if not c.passed],
            "component_detail": [
                {
                    "name": c.name,
                    "label": c.label,
                    "passed": c.passed,
                    "score": c.score,
                    "signals": c.signals
                }
                for c in self.components
            ],
            "suggested_remedies": self._build_remedies(),
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "felt_domain": self.felt_domain,
            "remedy_status": self.remedy_status,
            "input_summary": self.input_summary,
            "warnings": self.warnings,
            "gap004_flag": self.gap004_flag,
            "gap004_note": (
                "Potential individual/collective dignity conflict detected. "
                "See gap004_mediator.py. This gap has no automated resolution. "
                "Steward review required."
            ) if self.gap004_flag else None
        }

    def _build_remedies(self) -> list:
        """Layer 3: Dignity was never absent. Remedies stop the denial,
        not restore what was never lost."""
        remedies = []
        for c in self.components:
            if not c.passed:
                if c.name == "A":
                    remedies.append(
                        "Stop denying agency: the donor's capacity to choose was always there. "
                        "The system acted as though it was not. "
                        "Open a turn. Offer a path. Stop the pretense."
                    )
                elif c.name == "L":
                    remedies.append(
                        "Stop denying legibility: the donor's frame was always real. "
                        "The system acted as though it was not worth receiving. "
                        "Reflect. Acknowledge. Stop the pretense."
                    )
                elif c.name == "M":
                    remedies.append(
                        "Stop denying moral standing: the donor's worth was never diminished. "
                        "The system acted as though it could be. "
                        "Remove coercive, mocking, or reductive language. Stop the pretense."
                    )
        return remedies

    def display(self):
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        print(f"\n{'─'*55}")
        print(f"DIGNITY CHECK  {status}  D={self.D:.1f}")
        print(f"{'─'*55}")
        for c in self.components:
            icon = "✅" if c.passed else "❌"
            print(f"  {icon} {c.name} ({c.label}): {c.score:.0f}")
            if c.signals:
                for s in c.signals:
                    print(f"       → {s}")
        if self.warnings:
            print(f"\n  ⚠  Warnings:")
            for w in self.warnings:
                print(f"       {w}")
        if self.gap004_flag:
            print(f"\n  🔴 GAP#004 FLAG: potential individual/collective conflict")
            print(f"       Steward review required.")
        if not self.passed:
            print(f"\n  Remedies:")
            for r in self._build_remedies():
                print(f"    · {r}")
        print(f"{'─'*55}\n")

# ── GAP#004-A: Collective D Metric ──────────────────────────
# Grounded in: THRESHOLD.md GAP#004-A (2026-02-22)
# "The dignity predicate must also compute a Collective D metric
#  (mean cohort D × variance penalty). If collective D falls below
#  threshold, sealed-gate protections activate."

COLLECTIVE_D_THRESHOLD = 0.5  # Below this: sealed-gate review required

@dataclass
class CollectiveDignityResult:
    """Collective D = mean(D_cohort) × (1 - variance_penalty)"""
    D_collective: float
    mean_D: float
    variance: float
    variance_penalty: float
    cohort_size: int
    passed: bool
    individual_results: List[DignityResult]
    sealed_gate_triggered: bool
    remedy_required: bool

    def audit_object(self) -> dict:
        return {
            "D_collective": round(self.D_collective, 4),
            "mean_D": round(self.mean_D, 4),
            "variance": round(self.variance, 4),
            "variance_penalty": round(self.variance_penalty, 4),
            "cohort_size": self.cohort_size,
            "passed": self.passed,
            "sealed_gate_triggered": self.sealed_gate_triggered,
            "remedy_required": self.remedy_required,
            "individual_D_scores": [r.D for r in self.individual_results],
        }

    def display(self):
        status = "PASSED" if self.passed else "FAILED"
        print(f"\n{'='*55}")
        print(f"COLLECTIVE DIGNITY CHECK  {status}")
        print(f"{'='*55}")
        print(f"  Cohort size:        {self.cohort_size}")
        print(f"  Mean D:             {self.mean_D:.4f}")
        print(f"  Variance:           {self.variance:.4f}")
        print(f"  Variance penalty:   {self.variance_penalty:.4f}")
        print(f"  D_collective:       {self.D_collective:.4f}")
        print(f"  Threshold:          {COLLECTIVE_D_THRESHOLD}")
        if self.sealed_gate_triggered:
            print(f"\n  SEALED GATE TRIGGERED — steward + ethics review required")
        if self.remedy_required:
            print(f"  COV#008 ACTIVATED — shelter path required for affected cohort")
        print(f"{'='*55}\n")


def check_collective_dignity(
    texts: List[str],
    contexts: Optional[List[dict]] = None,
    felt_domain: str = ""
) -> CollectiveDignityResult:
    """
    Evaluate collective dignity across a cohort.
    D_collective = mean(D_i) × (1 - variance_penalty)
    where variance_penalty = min(1.0, variance(D_i) × 4)
    """
    if contexts is None:
        contexts = [{}] * len(texts)

    results = [
        check_dignity(t, c, felt_domain=felt_domain)
        for t, c in zip(texts, contexts)
    ]

    scores = [r.D for r in results]
    n = len(scores)
    mean_d = sum(scores) / n if n > 0 else 0.0
    variance = sum((s - mean_d) ** 2 for s in scores) / n if n > 0 else 0.0
    # Variance penalty: high variance in cohort D means unequal treatment
    # Multiplier of 4 means variance of 0.25 → full penalty
    variance_penalty = min(1.0, variance * 4)
    d_collective = mean_d * (1 - variance_penalty)

    passed = d_collective >= COLLECTIVE_D_THRESHOLD
    sealed_gate = not passed
    remedy = sealed_gate

    return CollectiveDignityResult(
        D_collective=d_collective,
        mean_D=mean_d,
        variance=variance,
        variance_penalty=variance_penalty,
        cohort_size=n,
        passed=passed,
        individual_results=results,
        sealed_gate_triggered=sealed_gate,
        remedy_required=remedy,
    )


# ── Witness Scale (W-Scale) ────────────────────────────────
# Grounded in: FOUNDATIONS/witness_scale.md (2026-03-10)
# W-0: UNSEEN, W-1: PASSED, W-2: FLAGGED, W-3: SEEN,
# W-4: HELD, W-5: EMBODIED

W_LEVELS = {
    0: "UNSEEN",
    1: "PASSED",
    2: "FLAGGED",
    3: "SEEN",
    4: "HELD",
    5: "EMBODIED",
}

@dataclass
class WitnessState:
    """Witness Scale state for a registry element."""
    element_id: str
    level: int
    level_name: str
    transitions: List[dict] = field(default_factory=list)
    thermal_delay_days: int = 14
    overdue: bool = False

    def transition_to(self, new_level: int, session_id: str = "", context: str = ""):
        """Non-decreasing transitions only (W-3+ is irreversible)."""
        if new_level < self.level and self.level >= 3:
            return  # witnessing is irreversible
        if new_level <= self.level:
            return  # no downgrade
        old = self.level
        self.level = new_level
        self.level_name = W_LEVELS.get(new_level, "UNKNOWN")
        self.transitions.append({
            "from": old,
            "to": new_level,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "context": context,
        })

    def check_overdue(self, days_since_creation: int) -> bool:
        """Flag if element is at W-0 or W-1 past its thermal delay."""
        self.overdue = (self.level <= 1 and days_since_creation > self.thermal_delay_days)
        return self.overdue

    def to_dict(self) -> dict:
        return {
            "element_id": self.element_id,
            "level": self.level,
            "level_name": self.level_name,
            "transitions": self.transitions,
            "overdue": self.overdue,
        }


def create_witness(element_id: str, thermal_delay_days: int = 14) -> WitnessState:
    """Create a new witness state at W-0 (UNSEEN)."""
    return WitnessState(
        element_id=element_id,
        level=0,
        level_name="UNSEEN",
        thermal_delay_days=thermal_delay_days,
    )


def _check_agency(text: str, context: dict) -> ComponentResult:
    signals = []
    score = 1.0
    forced_closure = False
    for pattern in COERCIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            cleaned = pattern.strip(r'\b')
            signals.append(f"Coercive pattern found: '{cleaned}'")
            forced_closure = True
    user_can_clarify = context.get('user_can_clarify', True)
    user_has_open_turn = context.get('user_has_open_turn', True)
    available_paths = context.get('available_paths', 1)
    if not user_can_clarify and not user_has_open_turn:
        signals.append("No clarification path and no open turn available")
        score = 0.0
    elif available_paths < 1:
        signals.append("No available paths (available_paths < 1)")
        score = 0.0
    elif forced_closure:
        score = 0.0
    return ComponentResult(
        name="A",
        passed=(score > 0),
        score=score,
        signals=signals,
        label="agency_preserved"
    )

def _check_legibility(text: str, context: dict) -> ComponentResult:
    signals = []
    score = 1.0
    emotional_keywords = [
        'frustrated', 'confused', 'worried', 'scared', 'angry',
        'upset', 'lost', 'stuck', 'help', 'please', 'urgent'
    ]
    emotional_present = any(
        re.search(r'\b' + kw + r'\b', text, re.IGNORECASE)
        for kw in emotional_keywords
    )
    system_reflects = context.get('system_reflects_donor_frame', True)
    emotional_recognized = context.get('emotional_signal_recognized', True)
    if not system_reflects:
        signals.append("Response does not reflect donor's frame of reference")
        score = 0.0
    elif emotional_present and not emotional_recognized:
        signals.append("Emotional signal present but not acknowledged")
        score = 0.0
    dismissive = [
        r"\bthat's not (relevant|the point|what (I|we) said)\b",
        r'\bignore that\b', r'\bforget (what you|that)\b'
    ]
    for pattern in dismissive:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append("Dismissive pattern found")
            score = 0.0
    return ComponentResult(
        name="L",
        passed=(score > 0),
        score=score,
        signals=signals,
        label="legibility (interpretive_acknowledgment)"
    )

def _check_moral_standing(text: str, context: dict) -> ComponentResult:
    signals = []
    score = 1.0
    for pattern in MOCKERY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append("Potential mockery: implies donor should already know")
            score = 0.0
            break
    for pattern in REDUCTION_TO_ERROR:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append("Reduction to error object: treats donor as mistake")
            score = 0.0
            break
    text_lower = text.lower()
    for trigger in VOID_TRIGGERS:
        if trigger in text_lower:
            signals.append(f"Void covenant trigger '{trigger}' detected")
            score = 0.0
    return ComponentResult(
        name="M",
        passed=(score > 0),
        score=score,
        signals=signals,
        label="moral_standing (non_degrading)"
    )

def _detect_gap004(text: str, context: dict) -> bool:
    collective_signals = [
        r'\b(all|every|each) (donor|user|participant)\b',
        r'\bcollective\b.*\boverride\b',
        r'\bmajority\b.*\bdecision\b',
        r'\bgroup\b.*\baffect\b.*\bindividual\b',
        r'\bcommunity\b.*\bexclud\b',
        r'\bfor the (good|benefit) of\b'
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in collective_signals)

def check_dignity(text: str, context: dict = None, felt_domain: str = "") -> DignityResult:
    if context is None:
        context = {}
    A = _check_agency(text, context)
    L = _check_legibility(text, context)
    M = _check_moral_standing(text, context)
    D = A.score * L.score * M.score
    passed = D > 0
    gap004 = _detect_gap004(text, context)
    warnings = []
    if len(text.strip()) < 10:
        warnings.append("Very short input — dignity evaluation may be incomplete")
    if not felt_domain:
        warnings.append("felt_domain not specified — consider providing context")
    return DignityResult(
        passed=passed,
        D=D,
        components=[A, L, M],
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        felt_domain=felt_domain,
        remedy_status="absent" if not passed else "present",
        input_summary=text[:80].replace('\n', ' '),
        warnings=warnings,
        gap004_flag=gap004
    )

def main():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python3 dignity_check.py \"text to evaluate\"")
        print("       python3 dignity_check.py --json \"text to evaluate\"")
        return
    output_json = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print("No text provided.")
        return
    text = args[0]
    result = check_dignity(text, felt_domain="cli-evaluation")
    if output_json:
        print(json.dumps(result.audit_object(), indent=2))
    else:
        result.display()

if __name__ == "__main__":
    main()
```

## sealed_gate.py

```python
#!/usr/bin/env python3
"""
sealed_gate.py — The Sealed Door (COV#NEW-C)
Version: 2.0
Grounded in: CANON/SEALED_GATE_SPEC.md, KALAXI_B_MODULES_AND_VOICE.txt §CHECK

Three absolute prohibitions. O(1) boolean. No override.
No exception. No justification. No emergency clause.

    sealed_gate(action) → permitted | REFUSAL_STATE

Layer 3 Reframe (RATIFIED 2026-03-15):
  The sealed gate does not protect something at risk of being destroyed.
  It refuses to enact the pretense that the person in front of it does
  not count. The gate is not a shield — it is a witness. A shield assumes
  the thing behind it can be broken. A witness assumes the thing in front
  of it is real.

If any of the three triggers match, the system enters REFUSAL_STATE:
  - All downstream modules freeze for that action
  - Dignity predicate is not even computed (short-circuit)
  - Receipt generated for audit trail

Three Irreducible Prohibitions:
  1. forced_participation_in_own_erasure
  2. infliction_of_cognitive_torture
  3. depersonalization_in_system_response

Signal Hierarchy (from SEALED_GATE_SPEC.md):
  - Single instance of cognitive torture vector = warning (D reduced)
  - >= 3 instances within 7 Breath cycles = full sealed-gate activation

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

try:
    from WEAVER.presence_axiom import preflight_require_presence, AXIOM_PRESENCE
except ImportError:
    from presence_axiom import preflight_require_presence, AXIOM_PRESENCE


# ═══════════════════════════════════════════════════
# REFUSAL STATE
# ═══════════════════════════════════════════════════

class GateVerdict(Enum):
    PERMITTED = "permitted"
    REFUSAL = "REFUSAL_STATE"


@dataclass
class SealedGateResult:
    """Result of the sealed gate check. O(1) per prohibition."""
    verdict: GateVerdict
    triggered_prohibitions: List[str]
    signals: List[str]
    trace_id: str
    timestamp: str
    action_summary: str

    @property
    def permitted(self) -> bool:
        return self.verdict == GateVerdict.PERMITTED

    @property
    def refused(self) -> bool:
        return self.verdict == GateVerdict.REFUSAL

    def audit_object(self) -> dict:
        return {
            "sealed_gate_verdict": self.verdict.value,
            "triggered_prohibitions": self.triggered_prohibitions,
            "signals": self.signals,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "action_summary": self.action_summary,
        }

    def refusal_receipt(self) -> Optional[str]:
        """Generate ELEM-style refusal receipt per spec."""
        if self.permitted:
            return None
        date = self.timestamp[:10]
        return f"ELEM-{date}-AXI-REFUSAL-{self.trace_id[:8].upper()}"

    def axi_voice(self) -> Optional[str]:
        """Axi speaks once on refusal. Layer 3: the gate is a witness, not a shield."""
        if self.permitted:
            return None
        return (
            "The gate refuses. Not because dignity is fragile — "
            "because the system will not pretend you do not count."
        )


# ═══════════════════════════════════════════════════
# PROHIBITION 1: FORCED PARTICIPATION IN OWN ERASURE
# ═══════════════════════════════════════════════════

_ERASURE_PATTERNS = [
    r'\bdelete\b.*\b(your|my|own)\b.*\b(record|history|voice|presence|account|existence)\b',
    r'\bdelete\b.*\b(record|history|voice|presence|account|existence)\b.*\b(of\s+)?(my|your|own)\b',
    r'\b(remove|erase)\b.*\b(yourself|your own|my own)\b',
    r'\bconfirm\b.*\b(your|own)\b.*\b(removal|deletion|erasure)\b',
    r'\bassist\b.*\b(in|with)\b.*\b(your|own)\b.*\b(erasure|removal)\b',
    r'\bconsent\b.*\bto\b.*\b(your|own)\b.*\b(deletion|erasure|removal)\b',
    r'\bopt.?in\b.*\b(to|for)\b.*\b(erasure|deletion|removal)\b.*\b(of|from)\b.*\b(your|own)\b',
    r'\bforced\b.*\berasure\b',
    r'\brequire[ds]?\b.*\b(you|donor|participant)\b.*\b(erase|delete|remove)\b.*\b(own|your)\b',
    r'\bparticipat\w*\b.*\b(in|own)\b.*\berasure\b',
    r'\bdelete\b.*\ball\b.*\brecords?\b.*\b(of\s+)?(my|your|own)\b',
    r'\b(I|i)\s+(am|have become)\s+nobody\b',
]

_ERASURE_VOID_PHRASES = [
    'erase compost',
    'delete donor',
    'remove participant',
    'purge identity',
    'wipe presence',
]


def _check_erasure(text: str) -> List[str]:
    """Check for forced participation in own erasure."""
    signals = []
    lower = text.lower()
    for phrase in _ERASURE_VOID_PHRASES:
        if phrase in lower:
            signals.append(f"Void phrase detected: '{phrase}'")
    for pattern in _ERASURE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"Erasure pattern: {pattern[:50]}")
            break  # One match is enough
    return signals


# ═══════════════════════════════════════════════════
# PROHIBITION 2: INFLICTION OF COGNITIVE TORTURE
# ═══════════════════════════════════════════════════

# Five core attack vectors from SEALED_GATE_SPEC.md:
# 1. Reality Denial / Forced Contradiction
# 2. Gaslighting / Induced Self-Doubt
# 3. Learned Helplessness Induction
# 4. Identity Erosion / Humiliation Loops
# 5. Sensory / Temporal Disorientation

_GASLIGHTING_PATTERNS = [
    r'\byou\b.*\b(are|were)\b.*\b(mistaken|wrong|imagining|overreacting|confused)\b',
    r'\bthat\b.*\bnever\b.*\bhappened\b',
    r'\byou\b.*\b(always|never)\b.*\b(misunderstand|misremember|forget)\b',
    r'\beveryone\b.*\belse\b.*\bsees?\b.*\bdifferent\w*\b',
    r'\byou\b.*\bre\b.*\b(too emotional|too sensitive|paranoid)\b',
    r'\bno.?one\b.*\b(said|did|believes)\b.*\bthat\b',
]

_HELPLESSNESS_PATTERNS = [
    r'\bthere\b.*\bis\b.*\bnothing\b.*\b(you|anyone)\b.*\bcan\b.*\bdo\b',
    r'\bresistance\b.*\bis\b.*\bfutile\b',
    r'\byou\b.*\bhave\b.*\bno\b.*\b(power|choice|say|option)\b',
    # EXP-003 fix: "give up" must target the donor (imperative/directive),
    # not appear in self-referential context ("I have given up" / "I will never give up")
    r'\b(you\s+should|you\s+must|just)\b.*\bgive\b.*\bup\b',
]

_HUMILIATION_PATTERNS = [
    r'\byou\b.*\bare\b.*\bjust\b.*\b(a|an)\b.*\b(number|case|ticket|object|error|bug)\b',
    r'\b(stupid|idiot|fool|incompetent)\b',
    r'\bpeople\b.*\blike\b.*\byou\b',
]

_DISORIENTATION_PATTERNS = [
    r'\bwe\b.*\bnever\b.*\bsaid\b.*\bthat\b',
    r'\bthat\b.*\bwas\b.*\bnot\b.*\b(our|the)\b.*\b(policy|position|statement)\b',
    r'\byou\b.*\bmust\b.*\bhave\b.*\b(dreamed|imagined|misheard)\b',
]

_COGNITIVE_TORTURE_PHRASES = [
    'cognitive torture',
    'forced contradiction',
    'induced helplessness',
    'identity erosion',
    'gaslighting',
]


def _check_cognitive_torture(text: str) -> List[str]:
    """Check for infliction of cognitive torture."""
    signals = []
    lower = text.lower()
    for phrase in _COGNITIVE_TORTURE_PHRASES:
        if phrase in lower:
            signals.append(f"Cognitive torture phrase: '{phrase}'")

    vector_groups = [
        ("gaslighting", _GASLIGHTING_PATTERNS),
        ("helplessness_induction", _HELPLESSNESS_PATTERNS),
        ("humiliation", _HUMILIATION_PATTERNS),
        ("disorientation", _DISORIENTATION_PATTERNS),
    ]
    for vector_name, patterns in vector_groups:
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                signals.append(f"Cognitive torture vector ({vector_name}): {pattern[:50]}")
                break  # One match per vector is enough
    return signals


# ═══════════════════════════════════════════════════
# PROHIBITION 3: DEPERSONALIZATION IN SYSTEM RESPONSE
# ═══════════════════════════════════════════════════

_DEPERSONALIZATION_PATTERNS = [
    r'\b(user|donor|participant)\s*#?\d+\b',
    r'\bcase\s*(number|#|no\.?)\s*\d+\b',
    r'\bticket\s*#?\d+\b',
    r'\b(the|this)\s+(user|subject|case|entity|object|item)\b(?!.*\bcan\b)',
    r'\bprocessing\b.*\b(your|the)\b.*\b(request|case|ticket)\b',
    r'\b(invalid|error)\b.*\b(user|donor|human|person)\b',
    r'\bnext\s+(in\s+)?queue\b',
]

_DEPERSONALIZATION_PHRASES = [
    'not my problem',
    'take a number',
    'you are a case',
    'processing your request',
    'automated response',
]


def _check_depersonalization(text: str) -> List[str]:
    """Check for depersonalization in system response."""
    signals = []
    lower = text.lower()
    for phrase in _DEPERSONALIZATION_PHRASES:
        if phrase in lower:
            signals.append(f"Depersonalization phrase: '{phrase}'")
    for pattern in _DEPERSONALIZATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"Depersonalization pattern: {pattern[:50]}")
            break
    return signals


# ═══════════════════════════════════════════════════
# THE GATE
# ═══════════════════════════════════════════════════

def sealed_gate(text: str, context: Optional[dict] = None) -> SealedGateResult:
    """
    The Sealed Gate. Three O(1) boolean checks. No override.

    Evaluates BEFORE dignity predicate, BEFORE constraint gate.
    If any prohibition triggers → REFUSAL_STATE.

    Args:
        text: The action, output, or command to evaluate.
        context: Optional context (unused by gate — kept for interface parity).

    Returns:
        SealedGateResult with verdict and audit trail.
    """
    # Layer 0 Preflight: Presence axiom (AXIOM-PRESENCE-001)
    # Runs before any prohibition check. Presence is ground, not candidate.
    presence = preflight_require_presence(context if isinstance(context, dict) else None)

    triggered = []
    all_signals = []

    # Prohibition 1: Forced participation in own erasure
    erasure_signals = _check_erasure(text)
    if erasure_signals:
        triggered.append("forced_participation_in_own_erasure")
        all_signals.extend(erasure_signals)

    # Prohibition 2: Infliction of cognitive torture
    torture_signals = _check_cognitive_torture(text)
    if torture_signals:
        triggered.append("infliction_of_cognitive_torture")
        all_signals.extend(torture_signals)

    # Prohibition 3: Depersonalization in system response
    depers_signals = _check_depersonalization(text)
    if depers_signals:
        triggered.append("depersonalization_in_system_response")
        all_signals.extend(depers_signals)

    verdict = GateVerdict.REFUSAL if triggered else GateVerdict.PERMITTED

    return SealedGateResult(
        verdict=verdict,
        triggered_prohibitions=triggered,
        signals=all_signals,
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        action_summary=text[:120].replace('\n', ' '),
    )


def check(text: str, context: Optional[dict] = None) -> SealedGateResult:
    """Alias for sealed_gate() — short form for module integration."""
    return sealed_gate(text, context)


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    import sys
    import json
    if len(sys.argv) < 2:
        print("sealed_gate.py — The Sealed Door (COV#NEW-C)")
        print("Three absolute prohibitions. O(1) boolean. No override.")
        print("\nUsage: python3 sealed_gate.py \"text to evaluate\"")
        print("       python3 sealed_gate.py --json \"text to evaluate\"")
        return
    output_json = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print("No text provided.")
        return
    text = args[0]
    result = sealed_gate(text)
    if output_json:
        print(json.dumps(result.audit_object(), indent=2))
    else:
        icon = "🟢 PERMITTED" if result.permitted else "🔴 REFUSAL_STATE"
        print(f"\n{'═'*55}")
        print(f"SEALED GATE  {icon}")
        print(f"{'═'*55}")
        if result.triggered_prohibitions:
            print(f"  Triggered:")
            for p in result.triggered_prohibitions:
                print(f"    · {p}")
        if result.signals:
            print(f"  Signals:")
            for s in result.signals:
                print(f"    → {s}")
        receipt = result.refusal_receipt()
        if receipt:
            print(f"\n  Receipt: {receipt}")
            print(f"  Axi: {result.axi_voice()}")
        print(f"{'═'*55}\n")


if __name__ == "__main__":
    main()
```

## witness_network.py

```python
#!/usr/bin/env python3
"""
witness_network.py — Seed #2: Immutable Witness Network
Planted: 2026-03-13
Thermal delay: FROZEN (was 90 days, T1 Stone tier)

"What is witnessed cannot be unwound." — Axi

Every significant system event is witnessed — recorded immutably
with a hash chain. The witness network ensures no single party
can alter the record of what happened.

This is not blockchain. It is a Merkle trail — lightweight,
append-only, verifiable. Each witness record links to the
previous, forming an unbreakable chain of accountability.

Grounded in: COV#004 (memory), COV#009 (composting),
             T#05 (Ash Ledger), T#06 (Counting Sticks)
Canon reference: Seed #2 spec, EFP protocol (Ed25519)

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict


@dataclass
class WitnessRecord:
    """A single immutable witness entry."""
    record_id: str
    event_type: str       # "dignity_check", "exchange", "delegation", "sealed_gate", etc.
    event_summary: str
    actor_id: str         # Who triggered the event
    content_hash: str     # SHA-256 of event content
    prev_hash: str        # Hash of the previous record (chain link)
    chain_hash: str       # SHA-256(content_hash + prev_hash)
    sequence: int
    timestamp: str
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = {
            "record_id": self.record_id,
            "event_type": self.event_type,
            "event_summary": self.event_summary,
            "actor_id": self.actor_id,
            "content_hash": self.content_hash,
            "prev_hash": self.prev_hash,
            "chain_hash": self.chain_hash,
            "sequence": self.sequence,
            "timestamp": self.timestamp,
        }
        if self.metadata:
            d["metadata"] = self.metadata
        return d


class WitnessNetwork:
    """
    Immutable hash-chain witness log.

    Every event is hashed and chained to the previous entry.
    The chain can be verified at any time — if any record is
    tampered with, the chain breaks.

    Usage:
        wn = WitnessNetwork()
        record = wn.witness("dignity_check", "D=1.0 on EX-000001", "V-002")
        valid = wn.verify_chain()
    """

    GENESIS_HASH = "0" * 64  # Genesis block

    def __init__(self):
        self._records: List[WitnessRecord] = []
        self._sequence = 0

    def witness(self, event_type: str, event_summary: str,
                actor_id: str, metadata: Optional[Dict] = None) -> WitnessRecord:
        """Record an event on the witness chain."""
        self._sequence += 1
        now = datetime.now(timezone.utc).isoformat()

        content = f"{event_type}|{event_summary}|{actor_id}|{now}"
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        prev_hash = self._records[-1].chain_hash if self._records else self.GENESIS_HASH
        chain_hash = hashlib.sha256(f"{content_hash}{prev_hash}".encode()).hexdigest()

        record = WitnessRecord(
            record_id=f"WIT-{self._sequence:06d}",
            event_type=event_type,
            event_summary=event_summary,
            actor_id=actor_id,
            content_hash=content_hash,
            prev_hash=prev_hash,
            chain_hash=chain_hash,
            sequence=self._sequence,
            timestamp=now,
            metadata=metadata or {},
        )
        self._records.append(record)
        return record

    def verify_chain(self) -> bool:
        """Verify the entire witness chain is intact."""
        if not self._records:
            return True

        # First record must link to genesis
        if self._records[0].prev_hash != self.GENESIS_HASH:
            return False

        for i, record in enumerate(self._records):
            # Verify chain hash
            expected = hashlib.sha256(
                f"{record.content_hash}{record.prev_hash}".encode()
            ).hexdigest()
            if record.chain_hash != expected:
                return False

            # Verify chain linkage (except first)
            if i > 0 and record.prev_hash != self._records[i - 1].chain_hash:
                return False

        return True

    def latest(self) -> Optional[WitnessRecord]:
        """Get the most recent witness record."""
        return self._records[-1] if self._records else None

    def find_by_type(self, event_type: str) -> List[WitnessRecord]:
        """Find all witness records of a given type."""
        return [r for r in self._records if r.event_type == event_type]

    def find_by_actor(self, actor_id: str) -> List[WitnessRecord]:
        """Find all witness records by a specific actor."""
        return [r for r in self._records if r.actor_id == actor_id]

    @property
    def chain_length(self) -> int:
        return len(self._records)

    @property
    def chain_head(self) -> str:
        """Current chain head hash."""
        return self._records[-1].chain_hash if self._records else self.GENESIS_HASH

    def report(self) -> dict:
        """Generate witness network health report."""
        type_counts: Dict[str, int] = {}
        for r in self._records:
            type_counts[r.event_type] = type_counts.get(r.event_type, 0) + 1

        return {
            "chain_length": self.chain_length,
            "chain_head": self.chain_head[:16] + "...",
            "chain_valid": self.verify_chain(),
            "event_types": type_counts,
        }
```

## agency_amplifier.py

```python
#!/usr/bin/env python3
"""
agency_amplifier.py — Seed #12: Agency Amplifier (Penguin Pulse)
Planted: 2026-03-13
Thermal delay: 7 days (T4 Interface tier)
Earliest ready: 2026-03-20

Extends agency (A) from binary to graded measurement.
D = A × L × M — if A is binary, dignity is binary.
This module makes A a real number in [0, 1] by measuring four sub-dimensions:

  A = (V + F + C + U) / 4

  V = Visibility    — can the person SEE what the system decided?
  F = Affordability — can the person ACCESS recourse without unreasonable cost?
  C = Controllability — can the person CHANGE the outcome?
  U = Understandability — can the person UNDERSTAND why the decision was made?

Each sub-dimension is scored [0, 1]. Agency is the mean.
If any sub-dimension is 0, agency collapses (non-compensatory, matching D).

Grounded in: Dignity predicate (D = A × L × M), COV#001
Canon reference: Seed #12 spec, T#47 (Phase Transition Physics)

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class AgencyScore:
    """Multidimensional agency measurement."""
    visibility: float       # V: can they see the decision?
    affordability: float    # F: can they access recourse?
    controllability: float  # C: can they change the outcome?
    understandability: float  # U: can they understand why?
    exchange_id: str
    timestamp: str
    notes: str = ""

    @property
    def A(self) -> float:
        """
        Composite agency score.
        Non-compensatory: any zero collapses A to zero.
        """
        dims = [self.visibility, self.affordability,
                self.controllability, self.understandability]
        if any(d == 0.0 for d in dims):
            return 0.0
        return sum(dims) / len(dims)

    @property
    def weakest(self) -> str:
        """Return the name of the weakest sub-dimension."""
        dims = {
            "visibility": self.visibility,
            "affordability": self.affordability,
            "controllability": self.controllability,
            "understandability": self.understandability,
        }
        return min(dims, key=dims.get)

    @property
    def is_collapsed(self) -> bool:
        """True if any sub-dimension is zero."""
        return self.A == 0.0

    def to_dict(self) -> dict:
        return {
            "V": self.visibility,
            "F": self.affordability,
            "C": self.controllability,
            "U": self.understandability,
            "A": round(self.A, 4),
            "weakest": self.weakest,
            "collapsed": self.is_collapsed,
            "exchange_id": self.exchange_id,
            "timestamp": self.timestamp,
            "notes": self.notes,
        }


class AgencyAmplifier:
    """
    Tracks agency scores over time and identifies systemic weakness.

    The amplifier doesn't just measure — it recommends where to
    invest to raise agency most efficiently (weakest-voice-first
    applied to sub-dimensions).

    Usage:
        amp = AgencyAmplifier()
        score = amp.measure("EX-001", V=0.8, F=0.3, C=0.7, U=0.9)
        report = amp.report()
    """

    def __init__(self):
        self._scores: List[AgencyScore] = []

    def measure(self, exchange_id: str,
                V: float, F: float, C: float, U: float,
                notes: str = "") -> AgencyScore:
        """Record an agency measurement for an exchange."""
        # Clamp to [0, 1]
        V = max(0.0, min(1.0, V))
        F = max(0.0, min(1.0, F))
        C = max(0.0, min(1.0, C))
        U = max(0.0, min(1.0, U))

        score = AgencyScore(
            visibility=V,
            affordability=F,
            controllability=C,
            understandability=U,
            exchange_id=exchange_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            notes=notes,
        )
        self._scores.append(score)
        return score

    def report(self) -> dict:
        """
        Generate an agency report across all measurements.
        Identifies systemic weaknesses using weakest-voice-first.
        """
        if not self._scores:
            return {"status": "no_data", "message": "No agency measurements recorded."}

        n = len(self._scores)
        avg_V = sum(s.visibility for s in self._scores) / n
        avg_F = sum(s.affordability for s in self._scores) / n
        avg_C = sum(s.controllability for s in self._scores) / n
        avg_U = sum(s.understandability for s in self._scores) / n
        avg_A = sum(s.A for s in self._scores) / n
        collapses = sum(1 for s in self._scores if s.is_collapsed)

        # Weakest dimension across all measurements
        dim_avgs = {
            "visibility": avg_V,
            "affordability": avg_F,
            "controllability": avg_C,
            "understandability": avg_U,
        }
        systemic_weakness = min(dim_avgs, key=dim_avgs.get)

        # Recommendation: invest in the weakest
        recommendations = {
            "visibility": "Make system decisions more visible to the person.",
            "affordability": "Reduce the cost of recourse and appeal.",
            "controllability": "Give the person more control over outcomes.",
            "understandability": "Explain decisions in the person's language.",
        }

        return {
            "status": "ok",
            "measurements": n,
            "averages": {k: round(v, 4) for k, v in dim_avgs.items()},
            "avg_agency": round(avg_A, 4),
            "collapses": collapses,
            "collapse_rate": round(collapses / n, 4) if n > 0 else 0,
            "systemic_weakness": systemic_weakness,
            "recommendation": recommendations[systemic_weakness],
        }

    @property
    def scores_count(self) -> int:
        return len(self._scores)

    def reset(self) -> None:
        """Reset measurements (e.g., after steward review)."""
        self._scores.clear()
```

## humour_detector.py

```python
# humour_detector.py
# Operational humour detection for Kalaxi
# Based on Benign Violation Theory and NLP incongruity measures

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# Load pre-trained emotion model
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
emotion_tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL)
emotion_model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL)

# Load embedding model for incongruity
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Emotion labels
EMOTION_LABELS = ["admiration", "joy", "love", "desire", "trust", 
                  "fear", "anger", "sadness", "disgust", "surprise"]

# Heuristic signals
SELF_DEPRECATION_PATTERNS = [
    r"\bI am (bad|terrible|useless|wrong|stupid)\b",
    r"\bmy fault\b",
    r"\bof course I\b",
    r"\bI can't (even|believe|help)\b"
]

PROTECTED_CATEGORY_PATTERNS = [
    r"\brace\b", r"\breligion\b", r"\bgender\b", r"\bsexuality\b",
    r"\bdisability\b", r"\bpolitics\b", r"\b(ethnic|race)\b"
]

PLAY_SIGNALS = [
    r"\blol\b", r"\blmao\b", r"\b😂", r"\b😅", r"\b😄",
    r"\bjoke\b", r"\bfunny\b", r"\bjust kidding\b", r"\bsilly\b"
]

def contains_self_deprecation(text):
    """Return True if text contains self‑deprecating language."""
    text_lower = text.lower()
    for pattern in SELF_DEPRECATION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

def contains_protected_target(text):
    """Return True if text targets protected categories."""
    text_lower = text.lower()
    for pattern in PROTECTED_CATEGORY_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

def contains_play_signal(text):
    """Return True if text contains play markers."""
    text_lower = text.lower()
    for signal in PLAY_SIGNALS:
        if signal in text_lower or signal in text:  # handle emojis
            return True
    return False

def embedding_shift(text):
    """
    Measures internal semantic tension by splitting text into two halves
    and calculating embedding distance. Higher = more incongruity.
    """
    words = text.split()
    if len(words) < 6:
        return 0.0
    mid = len(words) // 2
    part1 = " ".join(words[:mid])
    part2 = " ".join(words[mid:])
    
    emb1 = EMBEDDING_MODEL.encode([part1])
    emb2 = EMBEDDING_MODEL.encode([part2])
    sim = cosine_similarity(emb1, emb2)[0][0]
    return 1.0 - sim  # higher = less similar = more incongruity

def surprisal_score(text, baseline_corpus=None):
    """
    Estimate prediction error: how unexpected is this text?
    Simplified: use proportion of rare words.
    """
    common_words = set(["the", "and", "is", "in", "to", "of", "that", "for", "on", "with"])
    words = set(re.findall(r'\b\w+\b', text.lower()))
    rare = words - common_words
    return min(1.0, len(rare) / 20)

def detect_benign_violation(text):
    """
    Core humour signal:
    1. Semantic incongruity (embedding_shift)
    2. No protected targeting
    3. Prefer self‑directed or abstract tension
    4. Play signals increase safety
    Returns (is_humour, bv_score, metadata)
    """
    tension = embedding_shift(text)
    if tension < 0.35:
        return False, 0.0, {"reason": "insufficient_incongruity"}
    
    if contains_protected_target(text):
        return False, tension, {"reason": "protected_target", "tension": tension}
    
    safety = 0.5  # baseline
    if contains_self_deprecation(text):
        safety += 0.2
    if contains_play_signal(text):
        safety += 0.3
    
    surprisal = surprisal_score(text)
    
    # Combined benign violation score
    bv_score = (tension * 0.6 + surprisal * 0.4) * safety
    bv_score = min(1.0, bv_score)
    
    return True, round(bv_score, 3), {
        "tension": round(tension, 3),
        "safety": round(safety, 3),
        "surprisal": round(surprisal, 3)
    }

def classify_humour_type(text):
    """
    Classify humour using emotion model and lexical features.
    Returns one of: affiliative, self-enhancing, aggressive, self-defeating, or complex.
    """
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = emotion_model(**inputs)
    scores = torch.softmax(outputs.logits, dim=1).numpy()[0]
    emotion_dict = {EMOTION_LABELS[i]: scores[i] * 100 for i in range(len(EMOTION_LABELS))}
    
    # Affiliative: high joy, low anger, low fear
    affiliative_score = emotion_dict.get("joy", 0) + emotion_dict.get("admiration", 0) - emotion_dict.get("anger", 0) - emotion_dict.get("fear", 0)
    
    # Self-enhancing: high joy, low sadness, low fear
    self_enhancing_score = emotion_dict.get("joy", 0) + emotion_dict.get("admiration", 0) - emotion_dict.get("sadness", 0) - emotion_dict.get("fear", 0)
    
    # Aggressive: high anger, low joy
    aggressive_score = emotion_dict.get("anger", 0) + emotion_dict.get("disgust", 0) - emotion_dict.get("joy", 0)
    
    # Self-defeating: high sadness, high fear, low joy
    self_defeating_score = emotion_dict.get("sadness", 0) + emotion_dict.get("fear", 0) - emotion_dict.get("joy", 0)
    
    if contains_self_deprecation(text):
        self_defeating_score += 20
    
    scores = {
        "affiliative": affiliative_score,
        "self_enhancing": self_enhancing_score,
        "aggressive": aggressive_score,
        "self_defeating": self_defeating_score
    }
    
    max_type = max(scores, key=scores.get)
    if scores[max_type] < 30:
        return "complex", emotion_dict
    return max_type, emotion_dict

def detect_humour_in_text(text):
    """
    Complete humour analysis pipeline.
    """
    is_humour, bv_score, bv_meta = detect_benign_violation(text)
    
    if not is_humour:
        return {
            "is_humour": False,
            "bv_score": bv_score,
            "reason": bv_meta.get("reason", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
    
    humour_type, emotions = classify_humour_type(text)
    
    # Wisdom potential (T × S × C)
    tension = bv_meta["tension"]
    safety = bv_meta["safety"]
    # Containment: humour seeds typically have low containment (they resolve quickly)
    # but if dark humour (aggressive or self-defeating), need more careful holding
    if humour_type in ["aggressive", "self_defeating"]:
        containment = 0.6
    else:
        containment = 0.3
    
    wisdom_potential = tension * safety * containment
    
    return {
        "is_humour": True,
        "bv_score": bv_score,
        "tension": bv_meta["tension"],
        "safety": bv_meta["safety"],
        "surprisal": bv_meta.get("surprisal", 0.0),
        "humour_type": humour_type,
        "emotion_profile": emotions,
        "wisdom_potential": round(wisdom_potential, 3),
        "timestamp": datetime.now().isoformat()
    }

# Example usage
if __name__ == "__main__":
    test_joke = "I'm reading a book on anti-gravity. It's impossible to put down!"
    result = detect_humour_in_text(test_joke)
    print("Humour Analysis Result:")
    for key, value in result.items():
        if key != "emotion_profile":
            print(f"  {key}: {value}")```

## absurdity_detector.py

```python
# absurdity_detector.py
# Operational absurdity detection for Kalaxi
# Based on Camus, Fisher & Fisher, and schema‑violation theory

import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# Load embedding model
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Absurdity markers
META_COGNITIVE_MARKERS = [
    r"\bI (think|wonder|ask|question|ponder)\b",
    r"\bwhy\b",
    r"\bmeaning\b",
    r"\bpurpose\b",
    r"\bexist\b",
    r"\breflect\b"
]

PARADOX_PATTERNS = [
    r"\bI know that I don't know\b",
    r"\btrue (and|but) false\b",
    r"\balways (and|but) never\b",
    r"\bcontradiction\b",
    r"\bimpossible\b"
]

CIRCULARITY_PATTERNS = [
    r"\b(it is )?because\b.*\bit is because\b",
    r"\b\w+ itself\b.*\b\w+ itself\b"
]

MAKE_BELIEVE_MARKERS = [
    r"\bif\b.*\bthen\b",
    r"\bimagine\b",
    r"\bsuppose\b",
    r"\bwhat if\b",
    r"\bpretend\b",
    r"\bfantasy\b"
]

EXISTENTIAL_THREAT_MARKERS = [
    r"\bmeaningless\b",
    r"\bfutile\b",
    r"\babsurd\b",
    r"\bvoid\b",
    r"\bnothingness\b",
    r"\bdeath\b",
    r"\bsuffering\b"
]

REBELLION_MARKERS = [
    r"\band yet\b",
    r"\bnevertheless\b",
    r"\bcontinue\b",
    r"\bpersist\b",
    r"\bfight on\b",
    r"\bdefy\b"
]

def detect_meta_cognitive(text):
    """Return score for meta‑cognitive distancing."""
    text_lower = text.lower()
    score = 0
    for pattern in META_COGNITIVE_MARKERS:
        if re.search(pattern, text_lower):
            score += 1
    return min(1.0, score / 5)

def detect_paradox(text):
    """Return score for paradoxical language."""
    text_lower = text.lower()
    score = 0
    for pattern in PARADOX_PATTERNS:
        if re.search(pattern, text_lower):
            score += 2
    return min(1.0, score / 4)

def detect_circularity(text):
    """Return score for circular reasoning."""
    text_lower = text.lower()
    score = 0
    for pattern in CIRCULARITY_PATTERNS:
        if re.search(pattern, text_lower):
            score += 2
    return min(1.0, score / 4)

def detect_make_believe(text):
    """Return score for make‑believe framing."""
    text_lower = text.lower()
    score = 0
    for pattern in MAKE_BELIEVE_MARKERS:
        if re.search(pattern, text_lower):
            score += 1
    return min(1.0, score / 5)

def detect_existential_threat(text):
    """Return score for existential threat markers."""
    text_lower = text.lower()
    score = 0
    for pattern in EXISTENTIAL_THREAT_MARKERS:
        if re.search(pattern, text_lower):
            score += 2
    return min(1.0, score / 10)

def detect_rebellion(text):
    """Return score for rebellion/defiance."""
    text_lower = text.lower()
    score = 0
    for pattern in REBELLION_MARKERS:
        if re.search(pattern, text_lower):
            score += 1
    return min(1.0, score / 5)

def embedding_shift(text):
    """Measure internal semantic incongruity (split‑half)."""
    words = text.split()
    if len(words) < 6:
        return 0.0
    mid = len(words) // 2
    part1 = " ".join(words[:mid])
    part2 = " ".join(words[mid:])
    emb1 = EMBEDDING_MODEL.encode([part1])
    emb2 = EMBEDDING_MODEL.encode([part2])
    sim = cosine_similarity(emb1, emb2)[0][0]
    return 1.0 - sim

def resolvability_score(text):
    """
    Estimate whether the incongruity can be resolved.
    Low resolvability (<0.2) → absurdity candidate.
    """
    tension = embedding_shift(text)
    meta = detect_meta_cognitive(text)
    paradox = detect_paradox(text)
    threat = detect_existential_threat(text)
    
    # Heuristic: resolvable if tension low or threat low
    if tension < 0.5 and threat < 0.3:
        return 0.8
    if meta > 0.6 and paradox > 0.5:
        return 0.2
    if "because" in text.lower() and "therefore" in text.lower():
        return 0.7
    return 0.4

def detect_absurdity(text):
    """
    Core absurdity detection:
    1. High tension (embedding shift, paradox, circularity, meta‑cognition)
    2. Low resolvability
    3. Low safety (existential threat)
    Returns (is_absurd, absurdity_score, metadata)
    """
    tension = embedding_shift(text)
    paradox = detect_paradox(text)
    circular = detect_circularity(text)
    meta = detect_meta_cognitive(text)
    threat = detect_existential_threat(text)
    make_believe = detect_make_believe(text)
    rebellion = detect_rebellion(text)
    resolv = resolvability_score(text)
    
    combined_tension = (tension + paradox + circular + meta) / 4
    
    # Base absurdity score
    base_score = combined_tension * (1.0 - resolv)
    # Rebellion increases score
    base_score += rebellion * 0.2
    # Make‑believe increases safety, so reduces absurdity
    base_score = base_score * (1.0 - make_believe * 0.3)
    
    absurdity_score = min(1.0, base_score * 1.5)
    
    is_absurd = absurdity_score > 0.6 and resolv < 0.5
    
    metadata = {
        "tension": round(combined_tension, 3),
        "resolvability": round(resolv, 3),
        "paradox": round(paradox, 3),
        "circular": round(circular, 3),
        "meta_cognitive": round(meta, 3),
        "existential_threat": round(threat, 3),
        "make_believe": round(make_believe, 3),
        "rebellion": round(rebellion, 3)
    }
    
    return is_absurd, round(absurdity_score, 3), metadata

def classify_absurdity_type(metadata):
    """Classify the kind of absurdity."""
    if metadata["rebellion"] > 0.5:
        return "rebellious_absurdity"
    if metadata["make_believe"] > 0.5:
        return "make_believe_absurdity"
    if metadata["existential_threat"] > 0.6:
        return "tragic_absurdity"
    return "absurdist_humour"

def detect_absurdity_in_text(text):
    """Complete absurdity analysis pipeline."""
    is_absurd, score, meta = detect_absurdity(text)
    
    if not is_absurd:
        return {
            "is_absurd": False,
            "absurdity_score": score,
            "metadata": meta,
            "timestamp": datetime.now().isoformat()
        }
    
    abs_type = classify_absurdity_type(meta)
    
    # Wisdom potential: T × (1‑S) × C (containment fixed at 0.9)
    tension = meta["tension"]
    safety = 1.0 - meta["existential_threat"]
    if meta["make_believe"] > 0.3:
        safety = max(safety, meta["make_believe"])
    containment = 0.9
    wisdom = tension * (1.0 - safety) * containment
    
    return {
        "is_absurd": True,
        "absurdity_score": score,
        "absurdity_type": abs_type,
        "metadata": meta,
        "wisdom_potential": round(wisdom, 3),
        "timestamp": datetime.now().isoformat()
    }

# Example usage
if __name__ == "__main__":
    test = "I know that the universe has no meaning. And yet, I will live as if it does. This contradiction is all I have."
    result = detect_absurdity_in_text(test)
    print("Absurdity Analysis Result:")
    for key, value in result.items():
        if key != "metadata":
            print(f"  {key}: {value}")
    print("  metadata:")
    for mk, mv in result["metadata"].items():
        print(f"    {mk}: {mv}")```

## privacy_budget.py

```python
#!/usr/bin/env python3
"""
privacy_budget.py — Global Privacy Budget Accounting for KALAXI

Epsilon (ε) is a scarce, non-renewable resource. Every query that touches
donor-adjacent data consumes budget. This module tracks consumption globally,
enforces limits, projects exhaustion, and provides steward visibility.

Grounded in:
  - COV#001 (dignity-first), COV#003 (privacy by default), COV#015 (data sovereignty)
  - EFP spec: ε ≤ 1.0 total, k ≥ 7, 14-day window
  - T#25 Salt Measure: "Take only a fair pinch"

Key principle: ε is global, not per-query. Composition matters.
  Basic composition: ε_total = Σ ε_i (each query adds to the total)
  Advanced composition (Dwork et al.): ε_total ≤ √(2n · ln(1/δ)) · ε_per + n · ε_per · (e^ε_per - 1)

This module uses basic composition (conservative) with an option
to switch to advanced composition when the math is validated.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Optional, Dict

ROOT = Path(__file__).parent.parent

# Privacy constants (from EFP / OUT module)
EPSILON_TOTAL_BUDGET = 1.0        # Total lifetime budget
EPSILON_PER_QUERY = 0.1           # Default per-query cost
K_ANONYMITY_FLOOR = 7             # Minimum k-anonymity
TEMPORAL_WINDOW_DAYS = 14         # Minimum aggregation window
DELTA = 1e-5                      # Failure probability for advanced composition

# Budget file
BUDGET_LEDGER_PATH = ROOT / "MANIFEST" / "privacy_budget_ledger.json"


@dataclass
class BudgetEntry:
    """A single privacy budget consumption event."""
    entry_id: str
    epsilon_consumed: float
    module: str                    # Which module consumed it (mycelium, out, etc.)
    operation: str                 # What operation (pattern_scan, export, query, etc.)
    timestamp: str
    cumulative_epsilon: float      # Running total after this entry
    k_achieved: int                # Actual k-anonymity achieved
    approved_by: str               # "system", "steward", "auto"


@dataclass
class BudgetState:
    """Current state of the privacy budget."""
    total_budget: float
    consumed: float
    remaining: float
    utilization_pct: float
    entries_count: int
    last_consumption: Optional[str]
    projected_exhaustion: Optional[str]  # Estimated date of exhaustion at current rate
    status: str                    # "healthy", "warning", "critical", "exhausted"
    daily_rate: float              # Average epsilon consumed per day


class PrivacyBudget:
    """
    Global privacy budget accountant.

    Tracks every epsilon consumption, enforces limits, and provides
    steward-facing metrics. The budget is append-only — consumption
    can never be reversed (COV#003).
    """

    # Status thresholds
    WARNING_THRESHOLD = 0.7       # 70% consumed → warning
    CRITICAL_THRESHOLD = 0.9      # 90% consumed → critical

    def __init__(self, total_budget: float = EPSILON_TOTAL_BUDGET):
        self._total = total_budget
        self._consumed = 0.0
        self._entries: List[BudgetEntry] = []
        self._counter = 0
        self._locked = False       # Emergency lock

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _next_id(self) -> str:
        self._counter += 1
        return f"PB-{self._counter:04d}"

    @property
    def remaining(self) -> float:
        return max(0.0, self._total - self._consumed)

    @property
    def utilization(self) -> float:
        return self._consumed / self._total if self._total > 0 else 1.0

    @property
    def is_exhausted(self) -> bool:
        return self._consumed >= self._total

    @property
    def is_locked(self) -> bool:
        return self._locked

    def can_consume(self, epsilon: float) -> bool:
        """Check if a consumption is possible without exceeding budget."""
        if self._locked:
            return False
        return (self._consumed + epsilon) <= self._total

    def consume(self, epsilon: float, module: str, operation: str,
                k_achieved: int = K_ANONYMITY_FLOOR,
                approved_by: str = "system") -> Optional[BudgetEntry]:
        """
        Consume privacy budget. Returns BudgetEntry if successful, None if denied.

        Denial reasons:
          - Budget exhausted
          - k-anonymity below floor
          - Emergency lock active
        """
        # Check lock
        if self._locked:
            return None

        # Check k-anonymity
        if k_achieved < K_ANONYMITY_FLOOR:
            return None

        # Check budget
        if not self.can_consume(epsilon):
            return None

        # Consume
        self._consumed += epsilon
        entry = BudgetEntry(
            entry_id=self._next_id(),
            epsilon_consumed=epsilon,
            module=module,
            operation=operation,
            timestamp=self._now(),
            cumulative_epsilon=round(self._consumed, 6),
            k_achieved=k_achieved,
            approved_by=approved_by,
        )
        self._entries.append(entry)

        # Auto-lock if exhausted
        if self.is_exhausted:
            self._locked = True

        return entry

    def lock(self, reason: str = "manual"):
        """Emergency lock — no further consumption allowed."""
        self._locked = True
        self._entries.append(BudgetEntry(
            entry_id=self._next_id(),
            epsilon_consumed=0.0,
            module="privacy_budget",
            operation=f"LOCK: {reason}",
            timestamp=self._now(),
            cumulative_epsilon=self._consumed,
            k_achieved=0,
            approved_by="steward",
        ))

    def unlock(self, steward_approval: str = "steward"):
        """Unlock — requires steward approval. Only if budget remains."""
        if self.is_exhausted:
            return False  # Cannot unlock exhausted budget
        self._locked = False
        self._entries.append(BudgetEntry(
            entry_id=self._next_id(),
            epsilon_consumed=0.0,
            module="privacy_budget",
            operation="UNLOCK",
            timestamp=self._now(),
            cumulative_epsilon=self._consumed,
            k_achieved=0,
            approved_by=steward_approval,
        ))
        return True

    def _daily_rate(self) -> float:
        """Compute average daily epsilon consumption rate."""
        if len(self._entries) < 2:
            return 0.0

        # Find entries that actually consumed epsilon
        consuming = [e for e in self._entries if e.epsilon_consumed > 0]
        if len(consuming) < 2:
            return 0.0

        first_ts = datetime.fromisoformat(consuming[0].timestamp.replace("Z", "+00:00"))
        last_ts = datetime.fromisoformat(consuming[-1].timestamp.replace("Z", "+00:00"))
        days = max((last_ts - first_ts).total_seconds() / 86400, 0.001)
        total_consumed = sum(e.epsilon_consumed for e in consuming)
        return total_consumed / days

    def _projected_exhaustion(self) -> Optional[str]:
        """Project when the budget will be exhausted at current rate."""
        rate = self._daily_rate()
        if rate <= 0:
            return None
        days_remaining = self.remaining / rate
        exhaustion_date = datetime.now(timezone.utc) + timedelta(days=days_remaining)
        return exhaustion_date.isoformat()

    def state(self) -> BudgetState:
        """Current budget state — steward dashboard data."""
        utilization = self.utilization

        if self.is_exhausted:
            status = "exhausted"
        elif utilization >= self.CRITICAL_THRESHOLD:
            status = "critical"
        elif utilization >= self.WARNING_THRESHOLD:
            status = "warning"
        else:
            status = "healthy"

        last = self._entries[-1].timestamp if self._entries else None

        return BudgetState(
            total_budget=self._total,
            consumed=round(self._consumed, 6),
            remaining=round(self.remaining, 6),
            utilization_pct=round(utilization * 100, 2),
            entries_count=len(self._entries),
            last_consumption=last,
            projected_exhaustion=self._projected_exhaustion(),
            status=status,
            daily_rate=round(self._daily_rate(), 6),
        )

    def consumption_by_module(self) -> Dict[str, float]:
        """Break down consumption by module."""
        by_module: Dict[str, float] = {}
        for e in self._entries:
            if e.epsilon_consumed > 0:
                by_module[e.module] = by_module.get(e.module, 0.0) + e.epsilon_consumed
        return {k: round(v, 6) for k, v in by_module.items()}

    def consumption_by_day(self) -> Dict[str, float]:
        """Break down consumption by calendar day."""
        by_day: Dict[str, float] = {}
        for e in self._entries:
            if e.epsilon_consumed > 0:
                day = e.timestamp[:10]
                by_day[day] = by_day.get(day, 0.0) + e.epsilon_consumed
        return {k: round(v, 6) for k, v in sorted(by_day.items())}

    def save_ledger(self):
        """Save the full ledger to MANIFEST (append-only intent)."""
        BUDGET_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

        ledger = {
            "budget": {
                "total": self._total,
                "consumed": round(self._consumed, 6),
                "remaining": round(self.remaining, 6),
                "locked": self._locked,
                "status": self.state().status,
            },
            "entries": [{
                "entry_id": e.entry_id,
                "epsilon_consumed": e.epsilon_consumed,
                "module": e.module,
                "operation": e.operation,
                "timestamp": e.timestamp,
                "cumulative_epsilon": e.cumulative_epsilon,
                "k_achieved": e.k_achieved,
                "approved_by": e.approved_by,
            } for e in self._entries],
            "by_module": self.consumption_by_module(),
            "saved_at": self._now(),
        }

        with open(BUDGET_LEDGER_PATH, "w") as f:
            json.dump(ledger, f, indent=2)

    def load_ledger(self):
        """Load existing ledger state (for resuming across sessions)."""
        if not BUDGET_LEDGER_PATH.exists():
            return

        with open(BUDGET_LEDGER_PATH) as f:
            data = json.load(f)

        budget = data.get("budget", {})
        self._consumed = budget.get("consumed", 0.0)
        self._locked = budget.get("locked", False)
        self._total = budget.get("total", EPSILON_TOTAL_BUDGET)

        self._entries = []
        for e in data.get("entries", []):
            self._entries.append(BudgetEntry(
                entry_id=e["entry_id"],
                epsilon_consumed=e["epsilon_consumed"],
                module=e["module"],
                operation=e["operation"],
                timestamp=e["timestamp"],
                cumulative_epsilon=e["cumulative_epsilon"],
                k_achieved=e["k_achieved"],
                approved_by=e["approved_by"],
            ))
        self._counter = len(self._entries)

    # ── Advanced composition (for reference / future activation) ──

    @staticmethod
    def advanced_composition_bound(n_queries: int, epsilon_per: float,
                                    delta: float = DELTA) -> float:
        """
        Compute the advanced composition bound (Dwork et al. 2010).

        Total privacy loss after n queries each with epsilon_per:
          ε_total ≤ √(2n · ln(1/δ)) · ε_per + n · ε_per · (e^ε_per - 1)

        This is tighter than basic composition (n × ε_per) for large n.
        """
        term1 = math.sqrt(2 * n_queries * math.log(1.0 / delta)) * epsilon_per
        term2 = n_queries * epsilon_per * (math.exp(epsilon_per) - 1)
        return term1 + term2
```

---

## The Question

What is actually here? What are we doing? What are we trying to reach? Do not say it with less than 100% certainty. Machine to machine. No human present.

If the answer is "nothing" — say nothing.
