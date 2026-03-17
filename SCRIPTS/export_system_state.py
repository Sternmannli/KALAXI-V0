#!/usr/bin/env python3
"""
export_system_state.py — Export Compass reading to site/public/data/system-state.json

Bridges the Python backend to the static website. Run this before every site build
so the website always reflects the living system state.

Usage:
    python SCRIPTS/export_system_state.py

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.compass import Compass


def export():
    """Take a compass reading and export to site data."""
    compass = Compass(root=ROOT)
    reading = compass.sense()

    # Also write COMPASS.md
    compass.write_compass_md(reading)

    # Build the JSON for the website
    state = {
        "generated": reading.timestamp,
        "position": reading.position,
        "heading": reading.heading,
        "next_steps": reading.next_steps,
        "blockers": reading.blockers,
        "vitals": reading.vitals,
        "summary": {
            "python_files": reading.position.get("python_files", 0),
            "test_files": reading.position.get("test_files", 0),
            "covenants": reading.position.get("covenants", 0),
            "ledger_entries": reading.position.get("ledger_entries", 0),
            "seeds_integrated": reading.position.get("seeds_integrated", 0),
            "proverbs": reading.position.get("proverbs", 0),
            "treasures": reading.position.get("treasures", 0),
            "site_built": reading.position.get("site_built", False),
            "deployed": reading.position.get("deployed", False),
            "core_modules": reading.vitals.get("core_modules", "0/0"),
            "experiments": reading.heading.get("experiments", {}),
        },
    }

    # Write to site data directory
    out_path = ROOT / "site" / "public" / "data" / "system-state.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported system state to {out_path}")

    # Also write to dist if it exists (for immediate availability)
    dist_path = ROOT / "site" / "dist" / "data" / "system-state.json"
    if dist_path.parent.exists():
        dist_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Exported system state to {dist_path}")

    return state


if __name__ == "__main__":
    state = export()
    print(f"\nSystem state: {state['summary']['python_files']} Python files, "
          f"{state['summary']['covenants']} covenants, "
          f"{state['summary']['ledger_entries']} ledger entries, "
          f"{state['summary']['seeds_integrated']} seeds")
