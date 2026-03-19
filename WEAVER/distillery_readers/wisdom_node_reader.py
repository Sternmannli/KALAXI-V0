"""
wisdom_node_reader.py — Extract wisdom nodes from R7M/WISDOM_CANON.md.

Wisdom nodes are provisional validation plans that link anomalies to proverbs
with measurable metrics.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Dict

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


RE_NODE_HEADER = re.compile(r'^W#(\d+)$')


class WisdomNodeReader(BaseReader):
    """Extract wisdom nodes from R7M/WISDOM_CANON.md."""

    area_name = "wisdom_nodes"

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

        # Find WISDOM_NODES section
        start = None
        for i, line in enumerate(lines):
            if line.strip() == "##SECTION:WISDOM_NODES":
                start = i
                break

        if start is None:
            area.meta_essence = "WISDOM_NODES section not found"
            return area

        nodes = self._parse_nodes(lines, start)

        for node in nodes:
            node_id = node["id"]
            anomaly = node.get("source_anomaly", "")
            proverb = node.get("source_proverb", "")
            metrics = node.get("metrics", [])
            plan = node.get("validation_plan", "")
            status = node.get("validation_status", "pending")

            links = [f"W#{node_id}"]
            if anomaly:
                links.append(anomaly)
            if proverb:
                links.append(proverb)

            essence = (
                f"Wisdom node linking {anomaly} to {proverb} — "
                f"measuring {', '.join(metrics)} — {status}"
            )

            entry = self.make_entry(
                source_path=f"R7M/WISDOM_CANON.md::W#{node_id}",
                raw_excerpt=plan,
                patterns=[f"STATUS:{status}", f"METRICS:{','.join(metrics)}"],
                essence=essence,
                links=links,
                thermal_state="raw" if status == "pending" else "witnessed",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_nodes": len(nodes),
            "pending": sum(1 for n in nodes if n.get("validation_status") == "pending"),
        }

        area.meta_essence = (
            f"{len(nodes)} wisdom nodes — provisional validation plans "
            f"linking anomalies to proverbs with measurable metrics"
        )

        return area

    def _parse_nodes(self, lines: List[str], start: int) -> List[Dict]:
        """Parse W# blocks from the WISDOM_NODES section."""
        nodes = []
        i = start + 1

        while i < len(lines):
            line = lines[i].strip()

            # Stop at next section
            if line.startswith("##") and not RE_NODE_HEADER.match(line):
                break
            if line.startswith("---"):
                break

            match = RE_NODE_HEADER.match(line)
            if match:
                node_id = match.group(1)
                fields = {"id": node_id}

                i += 1
                while i < len(lines):
                    fline = lines[i].strip()
                    if not fline:
                        i += 1
                        if i < len(lines) and (
                            RE_NODE_HEADER.match(lines[i].strip())
                            or lines[i].strip().startswith("##")
                            or lines[i].strip().startswith("---")
                        ):
                            break
                        continue
                    if RE_NODE_HEADER.match(fline) or fline.startswith("##") or fline.startswith("---"):
                        break

                    if ":" in fline:
                        key, _, value = fline.partition(":")
                        key = key.strip()
                        value = value.strip()
                        if key == "metrics":
                            value = [v.strip() for v in value.strip("[]").split(",") if v.strip()]
                        elif key == "provisional":
                            value = value.lower() == "true"
                        fields[key] = value
                    i += 1

                nodes.append(fields)
            else:
                i += 1

        return nodes
