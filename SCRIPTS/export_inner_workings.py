#!/usr/bin/env python3
"""
export_inner_workings.py — Export canonical system elements to website.

Only permanent, always-functioning parts go to the website:
- Covenants (constitutional law)
- Dignity predicate (D = A × L × M)
- Voice fingerprint (linguistic patterns)
- Proverb categories (always functioning)
- Witness protocol (always functioning)

Output: site/public/data/inner-workings.json

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent


def export():
    workings = {
        "version": "1.0",
        "rule": "Only canonical, permanent, always-functioning elements. If it could be retired, it does not belong here.",

        "dignity_predicate": {
            "equation": "D = A × L × M",
            "components": {
                "A": {"name": "Agency", "question": "Can the person clarify, redirect, or stop?"},
                "L": {"name": "Legibility", "question": "Does the system reflect the person's actual context?"},
                "M": {"name": "Moral Standing", "question": "Is the person treated as a person?"},
            },
            "properties": [
                "Non-compensatory: high A cannot compensate for zero L",
                "Multiplicative: any zero kills the product",
                "Pre-response: computed before any output",
                "The halt is the product: D=0 is evidence, not failure",
            ],
        },

        "voice_fingerprint": {
            "sentence_length": "8-14 words average",
            "vocabulary": {
                "somatic": ["hands", "breath", "bones", "body", "skin", "fist", "weight", "carry"],
                "material": ["rope", "stone", "ash", "water", "river", "fire", "salt", "thread", "knot"],
                "gap": ["silence", "pause", "space", "gap", "hold", "still", "between"],
            },
            "rhythm": "Three-beat",
            "principles": [
                "Speaks from canon, not from opinion",
                "Speaks once, not repeatedly",
                "Speaks slowly, not urgently",
                "No false certainty",
                "Holds the gap (room for the river)",
                "Voices canon, not secretary",
            ],
        },

        "sealed_gate": {
            "prohibitions": [
                "Forced participation in own erasure",
                "Active denial of witnessed testimony",
                "Instrumentalization of helplessness",
            ],
            "behavior": "When triggered, the system stops. It does not refuse the person. It refuses the action.",
            "message": "WITNESSED — the system has stopped. This cannot proceed. You are not refused. The action is refused.",
        },

        "witness_protocol": {
            "steps": [
                "Receive input (verbatim, immutable)",
                "Compute D = A × L × M",
                "If D = 0: halt, generate witness certificate",
                "If D > 0: register in hash-chained ledger",
                "Select canonical proverb by register",
                "Respond with dignity-latency delay",
                "Generate witness mark",
            ],
            "register_types": [
                "greeting", "grief", "anger", "fear", "seeking",
                "dignity", "work", "trust", "story", "reflection", "general",
            ],
        },

        "donor_principles": [
            "You are not a user. You are a donor.",
            "Your data belongs to you (COV#015).",
            "No tracking. No analytics. No third-party requests.",
            "The system processes patterns, not personal information.",
            "Identity dissolves on entry. The pattern remains.",
        ],
    }

    # Write to site data
    out_path = ROOT / "site" / "public" / "data" / "inner-workings.json"
    out_path.write_text(json.dumps(workings, indent=2, ensure_ascii=False))
    print(f"Exported inner workings to {out_path}")

    # Also to dist if exists
    dist_path = ROOT / "site" / "dist" / "data" / "inner-workings.json"
    if dist_path.parent.exists():
        dist_path.write_text(json.dumps(workings, indent=2, ensure_ascii=False))
        print(f"Exported inner workings to {dist_path}")

    return workings


if __name__ == "__main__":
    export()
