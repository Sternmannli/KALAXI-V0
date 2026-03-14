#!/usr/bin/env python3
"""
sync_public.py — System → Public Surface Sync

Reads internal system metrics, sanitizes them through the Publication Gate,
and outputs a clean pulse.json for the public GitHub Pages site.

Run after every system change to keep the public face in sync:
    python3 SCRIPTS/sync_public.py

Output: docs/pulse.json (in the public repo clone)
        FACE/KALAM_CH/pulse.json (local copy for FACE module)

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent

# ---------- SOURCES ----------

def count_patterns(root: Path) -> dict:
    """Count publishable patterns from system data."""
    patterns_file = root / "MANIFEST" / "patterns.json"
    if patterns_file.exists():
        data = json.loads(patterns_file.read_text())
        return {
            "total_patterns": sum(p.get("count", 0) for p in data),
            "unique_sources": sum(p.get("sources", 0) for p in data),
            "pattern_categories": len(data),
        }
    return {"total_patterns": 0, "unique_sources": 0, "pattern_categories": 0}


def count_tools(root: Path) -> int:
    """Count published tools in public repo."""
    public_tools = root / "MANIFEST" / "PUBLICATION_GATE.md"
    if not public_tools.exists():
        return 0
    text = public_tools.read_text()
    return text.count("PUBLISHED")


def count_experiments(root: Path) -> int:
    """Count experiment protocols."""
    exp_dir = root / "EXPERIMENTS"
    if not exp_dir.exists():
        return 0
    return len(list(exp_dir.glob("*.md"))) + len(list(exp_dir.glob("*.py")))


def count_observations(root: Path) -> int:
    """Count observations at C3+ confidence."""
    obs_dir = root / "R7M" / "OBSERVATIONS"
    if not obs_dir.exists():
        return 0
    count = 0
    for f in obs_dir.rglob("*.md"):
        text = f.read_text()
        # Count C3+ observations
        count += len(re.findall(r'C[345]', text))
    return count


def count_detectors(root: Path) -> int:
    """Count active detectors."""
    det_dir = root / "TOOLS"
    if not det_dir.exists():
        return 0
    return len([f for f in det_dir.glob("*.py") if f.name != "__init__.py"])


def system_health(root: Path) -> str:
    """Overall system health indicator."""
    threshold = root / "THRESHOLD.md"
    if not threshold.exists():
        return "growing"

    lines = [l for l in threshold.read_text().splitlines()
             if l.strip().startswith("[20")]
    if len(lines) > 20:
        return "thriving"
    elif len(lines) > 5:
        return "growing"
    return "seeding"


# ---------- PUBLICATION GATE ----------

FORBIDDEN = re.compile(
    r'V-001|V-002|V-003|Mohamed|AXI|Hakaka|KALAXI|mycelium|'
    r'steward|donor|covenant|COV#|ANOM#|P#\d|T#\d|sealed.gate|'
    r'red.feather|cafe.room|thermal.delay|mirror.ritual|'
    r'witness.ceremony|Laila|Yara|Salim',
    re.IGNORECASE
)


def is_clean(text: str) -> bool:
    """Check text passes Publication Gate vocabulary filter."""
    return not FORBIDDEN.search(text)


# ---------- BUILD PULSE ----------

def build_pulse(root: Path) -> dict:
    """Build the public pulse data."""
    patterns = count_patterns(root)

    pulse = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "health": system_health(root),
        "metrics": {
            "patterns_collected": patterns["total_patterns"],
            "unique_contributors": patterns["unique_sources"],
            "pattern_categories": patterns["pattern_categories"],
            "tools_published": count_tools(root),
            "experiments_active": count_experiments(root),
            "observations_validated": count_observations(root),
            "detectors_active": count_detectors(root),
        },
        "framework": {
            "gate_function": "D = A × L × M",
            "gate_description": "Non-compensatory: any zero collapses the score",
            "dimensions": ["Agency", "Legibility", "Moral Standing"],
            "confidence_scale": "C1 (anecdotal) → C5 (adversarially tested)",
        },
        "privacy": {
            "personal_data_collected": False,
            "tracking": False,
            "cookies": False,
            "data_model": "patterns only, never persons",
        }
    }

    # Final safety check
    pulse_text = json.dumps(pulse)
    if not is_clean(pulse_text):
        print("ERROR: Pulse contains forbidden terms. Aborting.", file=sys.stderr)
        sys.exit(1)

    return pulse


def main():
    pulse = build_pulse(ROOT)

    # Write to FACE module (local)
    face_dir = ROOT / "FACE" / "KALAM_CH"
    face_dir.mkdir(parents=True, exist_ok=True)
    (face_dir / "pulse.json").write_text(json.dumps(pulse, indent=2) + "\n")

    # Write to docs staging (for public repo)
    docs_dir = ROOT / "DOCS" / "public-site"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "pulse.json").write_text(json.dumps(pulse, indent=2) + "\n")

    # If public repo clone exists, write there too
    public_clone = Path("/tmp/kalam-framework/docs")
    if public_clone.exists():
        (public_clone / "pulse.json").write_text(json.dumps(pulse, indent=2) + "\n")
        print(f"Synced to public repo: {public_clone / 'pulse.json'}")

    print(f"Pulse generated: {pulse['metrics']}")
    print(f"Health: {pulse['health']}")


if __name__ == "__main__":
    main()
