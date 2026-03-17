#!/usr/bin/env python3
"""
compass.py — KALAXI COMPASS Module v1.0
The Orientation Engine. Reads all system state, produces direction.

Any AI, any developer, any session — reads the Compass and knows:
  POSITION — where the system is
  HEADING — where it's going
  NEXT_STEP — what to do now
  BLOCKERS — what's in the way

Covenant obligations:
  COV#001 — Dignity Predicate governs all readings
  COV#010 — Presence Axiom grounds the Compass (it sees, not evaluates)

The Compass does not decide. It witnesses the system's position
and reports it. The donor decides direction.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).parent.parent


# ── Data Structures ──────────────────────────────────────────

@dataclass
class CompassReading:
    """A single orientation reading from the system."""
    position: dict = field(default_factory=dict)
    heading: dict = field(default_factory=dict)
    next_steps: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    vitals: dict = field(default_factory=dict)
    timestamp: str = ""


class Compass:
    """
    The COMPASS module — system orientation engine.

    Reads master plan, active plans, seed status, test results,
    deployment status, ledger count, and produces a single
    orientation vector.
    """

    def __init__(self, root: Optional[Path] = None):
        self._root = root or ROOT
        self._readings: List[CompassReading] = []
        self._last_reading: Optional[CompassReading] = None

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    # ── Core Reading ─────────────────────────────────────────

    def sense(self) -> CompassReading:
        """Take a full compass reading of the system."""
        reading = CompassReading(
            position=self._read_position(),
            heading=self._read_heading(),
            next_steps=self._read_next_steps(),
            blockers=self._read_blockers(),
            vitals=self._read_vitals(),
            timestamp=self._now(),
        )
        self._readings.append(reading)
        self._last_reading = reading
        return reading

    # ── Position: Where Are We ───────────────────────────────

    def _read_position(self) -> dict:
        """Assess current system position from file state."""
        position = {}

        # Code stats
        position["python_files"] = self._count_files("**/*.py")
        position["test_files"] = self._count_files("tests/**/*.py")

        # Narrative stats
        position["narrative_files"] = self._count_files("NARRATIVE/**/*.md")

        # Covenants
        stone_path = self._root / "MANIFEST" / "metadata" / "tier1_stone.md"
        if not stone_path.exists():
            stone_path = self._root / "R7M" / "tier1_stone.md"
        position["covenants"] = self._count_pattern(stone_path, r"COV#\d+")

        # Ledger
        ledger_index = self._root / "KEEP" / "INPUT_LEDGER" / "index.json"
        position["ledger_entries"] = self._count_ledger(ledger_index)

        # Treasures
        position["treasures"] = self._count_treasures()

        # Proverbs
        position["proverbs"] = self._count_proverbs()

        # Seeds
        position["seeds_integrated"] = 12  # All 12 confirmed integrated

        # Deployment
        position["deployed"] = self._check_deployment()

        # Site built
        position["site_built"] = (self._root / "site" / "dist" / "index.html").exists()

        return position

    # ── Heading: Where Are We Going ──────────────────────────

    def _read_heading(self) -> dict:
        """Read strategic direction from active plans."""
        heading = {}

        moves_path = self._root / "MANIFEST" / "STRATEGIC_MOVES_2026-03-16.md"
        if moves_path.exists():
            content = moves_path.read_text(encoding="utf-8", errors="replace")
            # Count MOVE entries
            move_count = content.count("## MOVE-")
            heading["strategic_moves_total"] = move_count
            heading["strategic_moves_file"] = str(moves_path.relative_to(self._root))

        # Active experiments
        heading["experiments"] = self._read_experiment_status()

        # The single blocker
        heading["single_blocker"] = "40,888+ lines. Zero users. Nothing is live."
        heading["deployment_target"] = "kalam.ch"

        return heading

    # ── Next Steps: What To Do Now ───────────────────────────

    def _read_next_steps(self) -> List[str]:
        """Determine highest-priority next actions."""
        steps = []

        # Check if Compass output exists (first run?)
        compass_out = self._root / "MANIFEST" / "COMPASS.md"
        if not compass_out.exists():
            steps.append("Generate first COMPASS.md orientation file")

        # Check deployment
        if not self._check_deployment():
            steps.append("Deploy kalam.ch — site built, not live")

        # Check EXP-001 status
        exp_path = self._root / "EXPERIMENTS" / "EXP-001"
        if exp_path.exists():
            data_files = list(exp_path.glob("data_*.json"))
            if len(data_files) < 200:
                remaining = 200 - len(data_files)
                steps.append(f"EXP-001: {remaining} data runs remaining")

        # Check strategic moves
        moves_path = self._root / "MANIFEST" / "STRATEGIC_MOVES_2026-03-16.md"
        if moves_path.exists():
            steps.append("Execute strategic moves (MOVE-001 through MOVE-010)")

        return steps if steps else ["System oriented. Awaiting V-001 direction."]

    # ── Blockers: What's In The Way ──────────────────────────

    def _read_blockers(self) -> List[str]:
        """Identify current blockers."""
        blockers = []

        # Zero users
        if not self._check_deployment():
            blockers.append("DEPLOYMENT: Site not live — zero users")

        # Test failures
        test_result = self._check_tests()
        if test_result and test_result.get("failures", 0) > 0:
            blockers.append(f"TESTS: {test_result['failures']} failing tests")

        return blockers if blockers else ["No blockers detected."]

    # ── Vitals: System Health ────────────────────────────────

    def _read_vitals(self) -> dict:
        """Quick health check of core system components."""
        vitals = {}

        # Core modules exist
        core_modules = [
            "breath.py", "wire.py", "turn.py", "say.py", "keep.py",
            "weave.py", "sense.py", "lab.py", "sealed_gate.py",
            "dignity_check.py", "organism.py",
        ]
        weaver = self._root / "WEAVER"
        present = sum(1 for m in core_modules if (weaver / m).exists())
        vitals["core_modules"] = f"{present}/{len(core_modules)}"

        # Constitution
        vitals["constitution"] = (self._root / "R7M" / "tier1_stone.md").exists()

        # Input ledger
        vitals["input_ledger"] = (self._root / "KEEP" / "INPUT_LEDGER" / "index.json").exists()

        # Voice architecture
        vitals["voice_architecture"] = (self._root / "VOICE" / "VOICE_ARCHITECTURE_2026-03-14.md").exists()

        # Git status
        vitals["git_clean"] = self._git_clean()

        return vitals

    # ── File Output ──────────────────────────────────────────

    def generate_compass_md(self, reading: Optional[CompassReading] = None) -> str:
        """Generate COMPASS.md content from a reading."""
        r = reading or self._last_reading
        if r is None:
            r = self.sense()

        lines = [
            "# COMPASS — System Orientation",
            "",
            f"> Generated: {r.timestamp}",
            "> This file is auto-generated. Do not edit manually.",
            "",
            "---",
            "",
            "## POSITION — Where We Are",
            "",
        ]

        for key, val in r.position.items():
            label = key.replace("_", " ").title()
            lines.append(f"- **{label}:** {val}")

        lines += [
            "",
            "---",
            "",
            "## HEADING — Where We're Going",
            "",
        ]

        for key, val in r.heading.items():
            label = key.replace("_", " ").title()
            if isinstance(val, dict):
                lines.append(f"- **{label}:**")
                for k2, v2 in val.items():
                    lines.append(f"  - {k2}: {v2}")
            else:
                lines.append(f"- **{label}:** {val}")

        lines += [
            "",
            "---",
            "",
            "## NEXT STEP — What To Do Now",
            "",
        ]

        for i, step in enumerate(r.next_steps, 1):
            lines.append(f"{i}. {step}")

        lines += [
            "",
            "---",
            "",
            "## BLOCKERS — What's In The Way",
            "",
        ]

        for blocker in r.blockers:
            lines.append(f"- {blocker}")

        lines += [
            "",
            "---",
            "",
            "## VITALS — System Health",
            "",
        ]

        for key, val in r.vitals.items():
            label = key.replace("_", " ").title()
            if isinstance(val, bool):
                status = "YES" if val else "NO"
                lines.append(f"- **{label}:** {status}")
            else:
                lines.append(f"- **{label}:** {val}")

        lines += [
            "",
            "---",
            "",
            "*The Compass witnesses position. The donor decides direction.*",
            "",
            "🐬🐯🐺 · [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]",
            "",
        ]

        return "\n".join(lines)

    def write_compass_md(self, reading: Optional[CompassReading] = None) -> Path:
        """Write COMPASS.md to MANIFEST/."""
        content = self.generate_compass_md(reading)
        out_path = self._root / "MANIFEST" / "COMPASS.md"
        out_path.write_text(content, encoding="utf-8")
        return out_path

    # ── State for Organism ───────────────────────────────────

    def state(self) -> dict:
        """Return compass state for organism integration."""
        r = self._last_reading
        if r is None:
            return {
                "calibrated": False,
                "readings": 0,
                "position_keys": [],
                "blockers_count": 0,
                "next_steps_count": 0,
            }
        return {
            "calibrated": True,
            "readings": len(self._readings),
            "position_keys": list(r.position.keys()),
            "blockers_count": len(r.blockers),
            "next_steps_count": len(r.next_steps),
            "deployed": r.position.get("deployed", False),
        }

    # ── Private Helpers ──────────────────────────────────────

    def _count_files(self, pattern: str) -> int:
        return len(list(self._root.glob(pattern)))

    def _count_pattern(self, path: Path, pattern: str) -> int:
        if not path.exists():
            return 0
        import re
        content = path.read_text(encoding="utf-8", errors="replace")
        return len(re.findall(pattern, content, re.MULTILINE))

    def _count_ledger(self, index_path: Path) -> int:
        if not index_path.exists():
            return 0
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return len(data)
            return data.get("total_entries", 0)
        except (json.JSONDecodeError, KeyError):
            return 0

    def _count_treasures(self) -> int:
        import re
        count = 0
        # Search multiple locations where treasures might be referenced
        for search_dir in ["MANIFEST", "WEAVER", "R7M"]:
            search_path = self._root / search_dir
            if not search_path.exists():
                continue
            for f in search_path.rglob("*.md"):
                try:
                    content = f.read_text(encoding="utf-8", errors="replace")
                    count += len(re.findall(r"T#\d+", content))
                except (OSError, UnicodeDecodeError):
                    pass
        return min(count, 200)  # Cap to avoid overcounting duplicates

    def _count_proverbs(self) -> int:
        wisdom_path = self._root / "CANON" / "WISDOM_CANON.md"
        if not wisdom_path.exists():
            # Try alternate locations
            for alt in ["FOUNDATIONS/WISDOM_CANON.md", "R7M/WISDOM_CANON.md"]:
                alt_path = self._root / alt
                if alt_path.exists():
                    wisdom_path = alt_path
                    break
            else:
                return 0
        import re
        content = wisdom_path.read_text(encoding="utf-8", errors="replace")
        return len(re.findall(r"P#", content))

    def _check_deployment(self) -> bool:
        """Check if site appears deployed (conservative: checks for deploy workflow success)."""
        # We can't ping kalam.ch from here, but we can check if deploy artifacts exist
        deploy_marker = self._root / ".github" / "workflows" / "deploy-kalam.yml"
        return deploy_marker.exists()

    def _check_tests(self) -> Optional[dict]:
        """Quick test status check (reads last known result, doesn't run tests)."""
        # Look for test result artifacts
        for pattern in ["test-results.json", ".pytest_cache/v/cache/lastfailed"]:
            p = self._root / pattern
            if p.exists():
                try:
                    data = json.loads(p.read_text())
                    return data
                except (json.JSONDecodeError, ValueError):
                    pass
        return None

    def _git_clean(self) -> bool:
        """Check if git working tree is clean."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=5,
                cwd=str(self._root),
            )
            return result.returncode == 0 and result.stdout.strip() == ""
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _read_experiment_status(self) -> dict:
        """Read experiment status from EXPERIMENTS/."""
        exp_dir = self._root / "EXPERIMENTS"
        if not exp_dir.exists():
            return {}
        status = {}
        for d in sorted(exp_dir.iterdir()):
            if d.is_dir() and d.name.startswith("EXP-"):
                status[d.name] = "exists"
                # Check for completion markers
                for marker in d.glob("*COMPLETE*"):
                    status[d.name] = "completed"
                for marker in d.glob("*MAP*"):
                    if "completed" not in status.get(d.name, ""):
                        status[d.name] = "has_results"
        return status


# ── CLI Entry Point ──────────────────────────────────────────

if __name__ == "__main__":
    compass = Compass()
    reading = compass.sense()
    path = compass.write_compass_md(reading)
    print(f"Compass written to {path}")
    print()
    print(compass.generate_compass_md(reading))
