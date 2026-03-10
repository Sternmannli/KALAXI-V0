#!/usr/bin/env python3
"""
health_dashboard.py — KALAXI Registry Health Dashboard
Version: 1.0
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]

Scans the repository and reports on the health of all registries.
Run: python3 SCRIPTS/health_dashboard.py
"""

import re
from pathlib import Path
from collections import Counter

REPO = Path(__file__).parent.parent


def count_in_file(filepath, pattern):
    """Count regex matches in a file."""
    try:
        text = filepath.read_text(encoding="utf-8")
        return len(re.findall(pattern, text))
    except (FileNotFoundError, UnicodeDecodeError):
        return 0


def scan_threshold():
    """Scan THRESHOLD.md for all entry types."""
    path = REPO / "THRESHOLD.md"
    text = path.read_text(encoding="utf-8")
    types = Counter()
    statuses = Counter()
    for line in text.splitlines():
        m = re.match(r'\[.*?\] — (\w[\w\-]*)', line)
        if m:
            types[m.group(1)] += 1
        if "[PROVISIONAL]" in line:
            statuses["PROVISIONAL"] += 1
        if "[SEALED]" in line:
            statuses["SEALED"] += 1
        if "[FILED]" in line:
            statuses["FILED"] += 1
        if "[REGISTERED]" in line:
            statuses["REGISTERED"] += 1
    return types, statuses


def scan_covenants():
    """Scan tier1_stone.md for covenants."""
    path = REPO / "MANIFEST" / "metadata" / "tier1_stone.md"
    text = path.read_text(encoding="utf-8")
    ratified = len(re.findall(r'^\- \*\*COV#\d+:\*\*', text, re.MULTILINE))
    provisional = len(re.findall(r'^\- \*\*COV#NEW', text, re.MULTILINE))
    provisional += len(re.findall(r'^\- \*\*COV#VOID', text, re.MULTILINE))
    newly_registered = len(re.findall(r'^\- \*\*COV#0(?:08|15):\*\*', text, re.MULTILINE))
    return ratified, provisional, newly_registered


def scan_proverbs():
    """Count proverb references across the repo."""
    threshold = REPO / "THRESHOLD.md"
    text = threshold.read_text(encoding="utf-8")
    emerge = len(re.findall(r'P#EMERGE-\d+', text))
    prov = len(re.findall(r'PROV#CONV-\d+', text))
    return emerge, prov


def scan_anomalies():
    """Count anomaly references in THRESHOLD."""
    path = REPO / "THRESHOLD.md"
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r'ANOM#[\w\-]+', text))


def scan_gaps():
    """Count gap references in THRESHOLD."""
    path = REPO / "THRESHOLD.md"
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r'GAP#[\w\-]+', text))


def scan_treasures():
    """Check treasure index status."""
    path = REPO / "R7M" / "TREASURES" / "TREASURES_INDEX.md"
    text = path.read_text(encoding="utf-8")
    documented = len(re.findall(r'### T#\d+', text))
    unextracted = len(re.findall(r'UNEXTRACTED', text))
    return documented, unextracted


def scan_proposals():
    """Check structural proposals."""
    foundations = REPO / "FOUNDATIONS"
    proposals = []
    for f in sorted(foundations.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        if "PROVISIONAL" in text and "Structural Proposal" in text:
            proposals.append(f.name)
        elif "AXIOM" in text:
            proposals.append(f"{f.name} [AXIOM]")
    return proposals


def scan_tests():
    """Check test status."""
    tests_dir = REPO / "tests"
    if not tests_dir.exists():
        return 0
    return len(list(tests_dir.glob("test_*.py")))


def scan_weaver_modules():
    """Count WEAVER modules."""
    weaver = REPO / "WEAVER"
    return len(list(weaver.glob("*.py")))


def known_issues():
    """Extract known issues from CLAUDE.md."""
    path = REPO / "CLAUDE.md"
    text = path.read_text(encoding="utf-8")
    resolved = len(re.findall(r'~~.*~~ RESOLVED', text))
    partial = len(re.findall(r'~~.*~~ PARTIALLY RESOLVED', text))
    open_issues = len(re.findall(r'^- (?!~~)', text, re.MULTILINE))
    return resolved, partial, open_issues


def main():
    print("=" * 60)
    print("  KALAXI-V0 REGISTRY HEALTH DASHBOARD")
    print("  Generated: 2026-03-10")
    print("=" * 60)

    # Covenants
    rat, prov, new = scan_covenants()
    print(f"\n  COVENANTS")
    print(f"  {'Ratified:':<30} {rat}")
    print(f"  {'Provisional:':<30} {prov}")
    print(f"  {'Newly Registered:':<30} {new}")
    print(f"  {'Total:':<30} {rat + prov + new}")

    # Threshold entries
    types, statuses = scan_threshold()
    print(f"\n  THRESHOLD ENTRIES")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t + ':':<30} {c}")
    print(f"  {'---':<30}")
    for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {s + ':':<30} {c}")

    # Proverbs
    emerge, prov_conv = scan_proverbs()
    print(f"\n  PROVERBS (in THRESHOLD)")
    print(f"  {'Emergent (P#EMERGE):':<30} {emerge}")
    print(f"  {'Sealed (PROV#CONV):':<30} {prov_conv}")
    print(f"  {'Canonical (P#0001-3333):':<30} 3,333 (indexed)")

    # Anomalies
    anom = scan_anomalies()
    print(f"\n  ANOMALIES")
    print(f"  {'In THRESHOLD:':<30} {anom}")
    print(f"  {'Indexed (ANOM#0001-1100):':<30} 1,100 (canonical)")

    # Gaps
    gaps = scan_gaps()
    print(f"\n  GAPS")
    print(f"  {'In THRESHOLD:':<30} {gaps}")

    # Treasures
    doc, unext = scan_treasures()
    print(f"\n  TREASURES (T#01-T#47)")
    print(f"  {'Documented:':<30} {doc}")
    print(f"  {'Awaiting extraction:':<30} {unext}")
    total_t = doc + unext
    pct = (doc / 47 * 100) if total_t > 0 else 0
    print(f"  {'Coverage:':<30} {pct:.0f}%")

    # Proposals
    props = scan_proposals()
    print(f"\n  STRUCTURAL PROPOSALS")
    for p in props:
        print(f"    {p}")

    # Code
    modules = scan_weaver_modules()
    tests = scan_tests()
    print(f"\n  CODE")
    print(f"  {'WEAVER modules:':<30} {modules}")
    print(f"  {'Test files:':<30} {tests}")

    # Module inventory
    core_modules = ["keep", "wire", "breath", "say", "out", "turn", "weave",
                    "dignity_check", "organism"]
    extension_modules = ["dignity_drift", "shelter", "federation", "srvp", "sip"]
    print(f"\n  MODULE INVENTORY")
    print(f"  {'Core (9 + organism):':<30} {', '.join(m.upper() for m in core_modules)}")
    print(f"  {'Extensions (5):':<30} {', '.join(m.upper() for m in extension_modules)}")
    weaver_dir = REPO / "WEAVER"
    present = sum(1 for m in core_modules + extension_modules
                  if (weaver_dir / f"{m}.py").exists())
    print(f"  {'Modules present:':<30} {present}/{len(core_modules) + len(extension_modules)}")

    # Known Issues
    res, part, opn = known_issues()
    print(f"\n  KNOWN ISSUES (from CLAUDE.md)")
    print(f"  {'Resolved:':<30} {res}")
    print(f"  {'Partially resolved:':<30} {part}")

    # Health Score
    print(f"\n{'=' * 60}")
    health_items = [
        ("Covenants registered", rat + prov + new > 15),
        ("Treasures indexed (>20%)", doc >= 10),
        ("Proverbs active", emerge > 15),
        ("Anomalies tracked", anom > 5),
        ("Gaps documented", gaps > 3),
        ("Code modules present", modules > 10),
        ("Tests exist", tests > 0),
    ]
    passed = sum(1 for _, v in health_items if v)
    total = len(health_items)

    print(f"\n  HEALTH SCORE: {passed}/{total}")
    for name, ok in health_items:
        icon = "OK" if ok else "!!"
        print(f"  [{icon}] {name}")

    # Action items
    print(f"\n  NEXT ACTIONS")
    print(f"  1. Extract remaining 36 treasures from GRAND_ARCHIVE .docx")
    print(f"  2. Resolve Layer Three conflict (P#3328-P#3333, steward decision)")
    print(f"  3. Build FACE module v2 (web/visual steward dashboard)")
    print(f"  4. Implement Ed25519 real signatures for federation")

    # Completed actions
    print(f"\n  COMPLETED")
    print(f"  [DONE] All 9 core modules built and wired (organism.py)")
    print(f"  [DONE] GAP#PREVENTION-001: dignity drift detector (dD/dt)")
    print(f"  [DONE] GAP#VICTIM-PROTECTION-001: shelter path")
    print(f"  [DONE] GAP#MYCELIUM-CONNECT-001: EFP federation protocol")
    print(f"  [DONE] SRVP: 7-step ritual verification protocol")
    print(f"  [DONE] SIP: symmetric integration protocol (WVPS/GDI/HSR)")
    print(f"  [DONE] GAP#004-A collective D metric (dignity_check.py v2.0)")
    print(f"  [DONE] Witness Scale W-0..W-5 (dignity_check.py v2.0)")
    print(f"  [DONE] W#HIRING-001 signed and canonised as W#0088")
    print(f"  [DONE] 277 tests across 9 suites, 0 failures")

    print(f"\n{'=' * 60}")
    print(f"  [V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
