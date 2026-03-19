"""
anomaly_reader.py — Extract all anomalies from R7M/WISDOM_CANON.md.

Parses ##ANOM:XXXX blocks with fields: description, severity, status,
module, covenant_tags, proverb_links, felt_domain, remedy_status, note,
udhr_resonance. Handles both numbered (ANOM:0001) and named (ANOM:NEW-001).

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Dict

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


RE_ANOM_HEADER = re.compile(r'^##ANOM:(.+)$')


class AnomalyReader(BaseReader):
    """Extract all anomalies from R7M/WISDOM_CANON.md."""

    area_name = "anomalies"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.source_path = self.root / "R7M" / "WISDOM_CANON.md"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.source_path.exists():
            area.meta_essence = "WISDOM_CANON.md not found"
            return area

        text = self.source_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        anomalies = self._parse_anomalies(lines)

        severity_counts = {}
        domain_counts = {}

        for anom in anomalies:
            anom_id = anom["id"]
            desc = anom.get("description", "")
            severity = anom.get("severity", "unknown")
            module = anom.get("module", "unknown")
            felt_domain = anom.get("felt_domain", "unknown")
            covenants = anom.get("covenant_tags", [])
            proverbs = anom.get("proverb_links", [])
            note = anom.get("note", "")
            provisional = anom.get("provisional", False)

            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            domain_counts[felt_domain] = domain_counts.get(felt_domain, 0) + 1

            # Build pattern list
            patterns = [
                f"SEVERITY:{severity}",
                f"MODULE:{module}",
                f"DOMAIN:{felt_domain}",
            ]
            if provisional:
                patterns.append("PROVISIONAL")

            # Links: covenants + proverbs
            links = [f"ANOM#{anom_id}"] + covenants + proverbs

            # Essence: the description IS the essence for anomalies
            essence = desc
            if note:
                essence = f"{desc} — {note[:200]}"

            entry = self.make_entry(
                source_path=f"R7M/WISDOM_CANON.md::ANOM#{anom_id}",
                raw_excerpt=self._format_block(anom),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(desc),
                voice_markers=[],  # Anomalies are records, not voice
                links=links,
                thermal_state="witnessed" if not provisional else "raw",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_anomalies": len(anomalies),
            "severity_distribution": severity_counts,
            "domain_distribution": domain_counts,
            "provisional_count": sum(1 for a in anomalies if a.get("provisional")),
        }

        area.meta_patterns = [
            f"severity:{k}:{v}" for k, v in sorted(
                severity_counts.items(), key=lambda x: -x[1]
            )
        ]

        area.meta_essence = (
            f"{len(anomalies)} anomalies extracted — "
            f"the system's documented failures and gaps"
        )

        return area

    def _parse_anomalies(self, lines: List[str]) -> List[Dict]:
        """Parse all ##ANOM: blocks from the file lines."""
        anomalies = []
        i = 0

        while i < len(lines):
            match = RE_ANOM_HEADER.match(lines[i].strip())
            if match:
                anom_id = match.group(1).strip()
                fields = {"id": anom_id}

                # Parse fields until next section or empty block
                i += 1
                while i < len(lines):
                    line = lines[i].strip()
                    if not line:
                        i += 1
                        # Check if next non-empty line is a new section/anom
                        if i < len(lines) and (
                            lines[i].strip().startswith("##")
                            or lines[i].strip().startswith("---")
                        ):
                            break
                        continue
                    if line.startswith("##") or line.startswith("---"):
                        break

                    # Parse key: value
                    if ":" in line:
                        key, _, value = line.partition(":")
                        key = key.strip()
                        value = value.strip()

                        if key in ("covenant_tags", "proverb_links", "udhr_resonance"):
                            # Parse list: [COV#001, COV#002]
                            value = [
                                v.strip()
                                for v in value.strip("[]").split(",")
                                if v.strip()
                            ]
                        elif key == "provisional":
                            value = value.lower() == "true"

                        fields[key] = value
                    i += 1

                anomalies.append(fields)
            else:
                i += 1

        return anomalies

    @staticmethod
    def _format_block(anom: Dict) -> str:
        """Format anomaly as readable block for raw_excerpt."""
        parts = [f"ANOM#{anom['id']}: {anom.get('description', '')}"]
        if anom.get("severity"):
            parts.append(f"severity={anom['severity']}")
        if anom.get("module"):
            parts.append(f"module={anom['module']}")
        if anom.get("felt_domain"):
            parts.append(f"domain={anom['felt_domain']}")
        return " | ".join(parts)
