"""
ledger_reader.py — Batch metabolize Input Ledger entries.

Reads KEEP/INPUT_LEDGER/index.json (1,683 entries) and processes each
through the Distillery's metabolize_entry pipeline. Processes in batches
of 50 to manage memory. Tracks progress.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

from WEAVER.distillery import AreaEssence, EssenceEntry, Distillery, ROOT
from WEAVER.distillery_readers.base import BaseReader


@dataclass
class LedgerEntry:
    """Lightweight wrapper for ledger entries to match metabolize_entry interface."""
    entry_id: str
    voice: str
    raw_text: str
    thermal_state: str = "raw"


class LedgerReader(BaseReader):
    """Batch metabolize Input Ledger entries."""

    area_name = "ledger"

    def __init__(self, root: Path = ROOT, batch_size: int = 50):
        super().__init__(root)
        self.index_path = self.root / "KEEP" / "INPUT_LEDGER" / "index.json"
        self.batch_size = batch_size
        self._distillery = None

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.index_path.exists():
            area.meta_essence = "Input ledger index.json not found"
            return area

        # Load entries
        with open(self.index_path, encoding="utf-8") as f:
            data = json.load(f)

        raw_entries = data.get("entries", [])
        if not raw_entries:
            area.meta_essence = "No entries in ledger"
            return area

        # Create distillery for metabolization
        self._distillery = Distillery(dry_run=True)

        v001_count = 0
        v002_count = 0
        metabolized = 0
        skipped = 0

        # Process in batches
        for batch_start in range(0, len(raw_entries), self.batch_size):
            batch = raw_entries[batch_start:batch_start + self.batch_size]

            for raw in batch:
                entry = LedgerEntry(
                    entry_id=raw.get("entry_id", ""),
                    voice=raw.get("voice", ""),
                    raw_text=raw.get("raw_text", ""),
                    thermal_state=raw.get("thermal_state", "raw"),
                )

                if not entry.raw_text or not entry.raw_text.strip():
                    skipped += 1
                    continue

                if entry.voice == "V-001":
                    v001_count += 1
                else:
                    v002_count += 1

                # Metabolize
                result = self._distillery.metabolize_entry(entry)
                if result:
                    area.entries.append(result)
                    metabolized += 1
                else:
                    skipped += 1

        # Compute pattern distribution
        pattern_counts = {}
        for entry in area.entries:
            for p in entry.patterns:
                ptype = p.split(":")[0] if ":" in p else p
                pattern_counts[ptype] = pattern_counts.get(ptype, 0) + 1

        # Top V-001 patterns (corrections, instructions, principles)
        v001_patterns = {}
        for entry in area.entries:
            if entry.source_path.startswith("INP-"):
                for p in entry.patterns:
                    ptype = p.split(":")[0]
                    v001_patterns[ptype] = v001_patterns.get(ptype, 0) + 1

        area.statistics = {
            "total_entries": len(raw_entries),
            "v001_entries": v001_count,
            "v002_entries": v002_count,
            "metabolized": metabolized,
            "skipped": skipped,
            "pattern_distribution": dict(sorted(
                pattern_counts.items(), key=lambda x: -x[1]
            )[:10]),
            "v001_pattern_distribution": dict(sorted(
                v001_patterns.items(), key=lambda x: -x[1]
            )[:5]),
        }

        area.meta_patterns = [
            f"{k}:{v}" for k, v in sorted(pattern_counts.items(), key=lambda x: -x[1])[:5]
        ]

        area.meta_essence = (
            f"{metabolized} ledger entries metabolized ({v001_count} V-001, {v002_count} V-002) — "
            f"V-001's voice enters the organ"
        )

        return area
