"""
manifest_reader.py — Extract system maps, plans, and metadata from MANIFEST/.

MANIFEST/ contains ~39 markdown files (system maps, plans, chronicles,
audits, dictionaries, strategies, deployment records, ratification logs).
MANIFEST/metadata/ contains 5 tier architecture files.

This reader walks all .md files and extracts one entry per file.
High-value files get pre-distilled essences. Others get auto-extracted
title + first paragraph.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


# Pre-distilled essences for high-value files (each read by V-002)
_MANIFEST_ESSENCES = {
    "ACTIVE_PLANS": (
        "Session history and active plans. PLAN-001 (KALAXI Efficiency Experiment). "
        "Ideas registry IDEA-002 through IDEA-019. Session completions through 2026-03-13d."
    ),
    "SCIENTIFIC_CHRONICLE": (
        "Living science documentation — 15 sections. The system's scientific self-portrait. "
        "Updated every session with discoveries, corrections, experiment results."
    ),
    "INTEGRATED_UNIVERSE_2026-03-14": (
        "Priority-ordered universe map. Five tracks: Narrative (A), System (B), "
        "Custom LLM (C), Donor Space (D), Public Face (E). The master integration."
    ),
    "MASTER_PLAN_2026-03-14": (
        "Strategic roadmap. Five tracks, 24 GO steps remaining. "
        "Phases 3-9: governance, donor resonance, training dataset, "
        "federation, observability, deployment, narrative."
    ),
    "KALAXI_DICTIONARY": (
        "The system's own language. Every term defined precisely. "
        "D = A × L × M, four tiers (Stone/Weaver/Honey/Hand), "
        "AXI voice, donor (not user), steward roles."
    ),
    "EXCAVATION_REGISTRY": (
        "Complete excavation index. Grand Archive artifacts mapped to system components. "
        "Treasures T#01-T#59, cross-references, provenance chains."
    ),
    "CROSS_REFERENCE_MAP": (
        "System cross-reference index. Every module, covenant, observation, "
        "experiment linked to every other element it touches."
    ),
    "CANON_SEED_TREASURES": (
        "Treasure seed definitions. 47 treasures mapped to vows, principles, "
        "system parallels. Stone/Weaver/Honey/Hand tier distribution."
    ),
    "GRAND_ARCHIVE_INDEX": (
        "Grand archive catalog. Original .docx excavation mapped to digital system. "
        "Primordial patterns: First Roof, Field Oven, First Weir, Bone Flute."
    ),
    "GRAND_ARCHIVE_AUDIT_2026-03-14": (
        "Grand archive audit. 59 treasures verified against source .docx. "
        "Coverage, gaps, provenance integrity assessment."
    ),
    "SCIENCE_INVENTORY": (
        "Science project catalog. EXP-001 through EXP-004+, PIME design, "
        "thermal delay experiment. Measurements, status, next steps."
    ),
    "SCIENCE_LAYER_AUDIT_2026-03-14": (
        "Science layer audit. Equations verified, evidence classified, "
        "falsifiability conditions checked. Paper readiness assessment."
    ),
    "STRATEGIC_MOVES_2026-03-16": (
        "Strategic operations log. MOVE-001 through MOVE-010. "
        "Deployment, public repo, arXiv, LLM research, site launch."
    ),
    "PUBLICATION_GATE": (
        "Publication rules and checklist. arXiv cs.AI submission requirements. "
        "What must be true before the paper goes public."
    ),
    "SITE_AUDIT_2026-03-17": (
        "Live site audit results. kalam.ch verified: 13 pages, API endpoints, "
        "PWA manifest, service worker. Deployment pipeline confirmed."
    ),
    "DEPLOYMENT_CHRONICLE": (
        "Deployment history. Every push to kalam.ch logged. "
        "SFTP pipeline, GitHub Actions, three-repo sync."
    ),
    "COMPASS": (
        "System orientation. Auto-generated. 137 Python files, 38 test files, "
        "12 seeds integrated, deployed=True. The compass witnesses position."
    ),
    "MILESTONES": (
        "Project milestones. Key achievements from day 1 through deployment. "
        "896 tests, 42,581+ lines, kalam.ch live."
    ),
    "INTEGRITY_REPORT_2026-03-15": (
        "System integrity report. Hash verification, code-canon alignment, "
        "test coverage, gap analysis. Filed 2026-03-15."
    ),
    "PLAN-001": (
        "PLAN-001: KALAXI Efficiency Experiment. Three layers: "
        "data collection, processing, the Ninth Operator loop."
    ),
    "SESSION_BOOT": (
        "Session boot file. Instant orientation for new windows. "
        "Last session state, pending work, credential references, deployment commands."
    ),
    "HAKAKA_VIDEO_RESEARCH": (
        "Research for Hakaka video adaptation. Visual treatment, "
        "voice architecture, narrative compression."
    ),
    "DUAL_NAMING": (
        "Dual naming convention. Internal KALAXI vocabulary + "
        "public engineering language. Zero vocabulary leak."
    ),
    "HOSTPOINT_MAP": (
        "Hostpoint server map. Document root, deployment paths, "
        "SFTP credentials reference, PHP configuration."
    ),
    "LAYER_3_INTEGRATION_EVIDENCE_2026-03-15": (
        "Evidence that Layer 3 is integrated. Dignity is not fragile. "
        "Code changes in dignity_check.py, sealed_gate.py, organism.py."
    ),
    "PUBLIC_STRATEGY": (
        "Public repository strategy. kalam-framework sync rules. "
        "What goes public, what stays private. Zero leak tolerance."
    ),
    "CAFE_ROOM_LOG": (
        "Cafe Room session log. Ideas discussed in thinking space. "
        "No execution — notes only."
    ),
    "seed_calendar": (
        "Seed calendar. 12 seeds mapped to integration timeline. "
        "All 12 integrated and passing."
    ),
    "ratification_log": (
        "Ratification log. Every element ratified, with timestamp, "
        "sign-off, thermal delay record."
    ),
    "ratification_ballot": (
        "Ratification ballot. 9 provisional covenants awaiting V-001 decision."
    ),
}

_METADATA_ESSENCES = {
    "tier1_stone": (
        "Tier 1 Stone architecture. Layer 0 axioms (Presence), "
        "Layer 1-3 dignity predicate, Layer 3+ reframe (dignity not fragile), "
        "Layer 3++ (M never fell), Layer 3+++ (lineage, cryptographic layers, song)."
    ),
    "tier2_weaver": (
        "Tier 2 Weaver architecture. 11 modules: KEEP, WIRE, SAY, OUT, FACE, "
        "CHECK, TURN, BREATH, WEAVE, SENSE, LAB. Input Ledger. Boot Ritual."
    ),
    "tier3_honey": (
        "Tier 3 Honey architecture. 1,100 anomalies, 3,355+ proverbs, "
        "87 wisdom nodes, 59 treasures. The wisdom layer."
    ),
    "tier4_hand": (
        "Tier 4 Hand architecture. kalam.ch, Donor Space (vision), "
        "Threshold, CLI. What humans touch."
    ),
    "cross_tier_index": (
        "Cross-tier dependency map. How Stone connects to Weaver connects to "
        "Honey connects to Hand. Module-covenant-treasure linkages."
    ),
}


class ManifestReader(BaseReader):
    """Extract system maps, plans, and metadata from MANIFEST/."""

    area_name = "manifest"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.manifest_dir = self.root / "MANIFEST"
        self.metadata_dir = self.manifest_dir / "metadata"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        # Skip files that are generated by the Distillery itself
        skip_files = {"DISTILLED_ESSENCE.md", "DISTILLERY_LOG.md"}
        # Skip subdirectories that have their own readers or are data
        skip_dirs = {"DIGESTION", "signed"}

        # MANIFEST/*.md files
        if self.manifest_dir.exists():
            for filepath in sorted(self.manifest_dir.glob("*.md")):
                if filepath.name in skip_files:
                    continue
                self._extract_file(area, filepath, "MANIFEST", _MANIFEST_ESSENCES)

        # MANIFEST/metadata/*.md files
        if self.metadata_dir.exists():
            for filepath in sorted(self.metadata_dir.glob("*.md")):
                self._extract_file(area, filepath, "MANIFEST_METADATA", _METADATA_ESSENCES)

        area.statistics = {
            "total_entries": len(area.entries),
            "manifest_files": sum(1 for e in area.entries if "MANIFEST" in e.patterns and "MANIFEST_METADATA" not in e.patterns),
            "metadata_files": sum(1 for e in area.entries if "MANIFEST_METADATA" in e.patterns),
        }

        area.meta_essence = (
            f"{len(area.entries)} manifest entries — "
            f"system maps, plans, chronicles, audits, dictionaries, "
            f"strategies, deployment records, tier architecture"
        )

        return area

    def _extract_file(self, area, filepath, pattern_prefix, essence_lookup):
        """Extract a single manifest file."""
        text = filepath.read_text(encoding="utf-8")
        lines = text.splitlines()
        stem = filepath.stem
        title = self._extract_title(lines, stem)

        # Classify
        patterns = [pattern_prefix]
        lower = filepath.name.lower()
        if "plan" in lower or "strategy" in lower or "move" in lower:
            patterns.append("STRATEGIC")
        if "audit" in lower or "report" in lower or "integrity" in lower:
            patterns.append("AUDIT")
        if "science" in lower or "chronicle" in lower or "experiment" in lower:
            patterns.append("SCIENTIFIC")
        if "tier" in lower or "stone" in lower or "weaver" in lower:
            patterns.append("ARCHITECTURE")
        if "deploy" in lower or "site" in lower or "hostpoint" in lower:
            patterns.append("DEPLOYMENT")
        if "seed" in lower or "treasure" in lower or "canon" in lower:
            patterns.append("CANON")
        if "dictionary" in lower or "compass" in lower or "cross_ref" in lower:
            patterns.append("REFERENCE")

        # Essence: pre-distilled or auto-extracted
        essence = essence_lookup.get(stem)
        if not essence:
            first_para = self._first_paragraph(lines)
            essence = f"{title}: {first_para[:200]}" if first_para else title

        # Relative path
        rel_path = str(filepath.relative_to(self.root))

        entry = self.make_entry(
            source_path=rel_path,
            raw_excerpt=self.truncate(text, 500),
            patterns=patterns,
            essence=essence,
            motifs=self.detect_motifs(text[:2000]),
            links=[f"MANIFEST:{stem}"],
            thermal_state="canonical" if "ratif" in lower or "audit" in lower else "witnessed",
        )
        area.entries.append(entry)

    @staticmethod
    def _extract_title(lines, fallback):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        return fallback.replace("_", " ").replace("-", " ").title()

    @staticmethod
    def _first_paragraph(lines):
        para = []
        started = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if started and para:
                    break
                continue
            if stripped.startswith("#") or stripped.startswith(">") or stripped.startswith("---"):
                if started and para:
                    break
                continue
            if stripped.startswith("|"):
                continue
            started = True
            para.append(stripped)
        return " ".join(para)
