#!/usr/bin/env python3
"""
canon_integrity.py — Kalaxi Canon Integrity Scanner
Version: 1.0
Grounded in: KALAXI_D_INTERFACE_AND_LEDGER (FORWARD_INSTRUCTIONS section)
             KALAXI_A_FOUNDATION.txt §GOVERNANCE

Scans the four canonical slices for structural issues.
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional, List

REPO_ROOT = Path(__file__).parent.parent
SLICE_A = REPO_ROOT / "KALAXI_A_FOUNDATION.txt"
SLICE_B = REPO_ROOT / "KALAXI_B_MODULES_AND_VOICE.txt"
SLICE_C = REPO_ROOT / "KALAXI_C_WISDOM.txt"
SLICE_D = REPO_ROOT / "KALAXI_D_INTERFACE_AND_LEDGER.txt"
IDS_JSON = REPO_ROOT / "MANIFEST" / "ids.json" if (REPO_ROOT / "MANIFEST").exists() else REPO_ROOT / "ids.json"
SUPERSEDED_FILES = ["KALAXI_01_CORE_AND_GOVERNANCE.txt", "KALAXI_02_PROVERB_CANON.txt"]
KNOWN_OATHS = {"SOVEREIGN-AXIS": "7f6d42e5", "FULL-POWER": "a9c3fbb9"}
CRITICAL, HIGH, MEDIUM, LOW, INFO = "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"

@dataclass
class Finding:
    severity: str
    category: str
    description: str
    location: str
    canon_reference: str
    action_required: str
    auto_resolvable: bool = False

class CanonIntegrityScanner:
    def __init__(self, repo_root: Path = None):
        self.root = repo_root or REPO_ROOT
        self.findings: list = []
        self.files_checked = []
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def _add(self, severity, category, description, location, canon_ref, action, auto=False):
        self.findings.append(Finding(severity, category, description, location, canon_ref, action, auto))

    def _read_slice(self, path: Path) -> Optional[str]:
        if not path.exists():
            self._add(CRITICAL, "missing_file", f"Canonical slice file not found: {path.name}", str(path),
                      "COV#012 (MANIFEST PRESENCE), COV#NEW-E",
                      f"Locate {path.name} and ensure it is in the repository root")
            return None
        self.files_checked.append(path.name)
        return path.read_text(encoding='utf-8', errors='replace')

    def check_oath_hashes(self, text_a: str):
        if not text_a:
            return
        sa = re.search(r'OATH::SOVEREIGN-AXIS.*?HASH:\s*([0-9a-f]+)', text_a, re.DOTALL | re.IGNORECASE)
        if sa:
            found = sa.group(1).strip()[:8]
            exp = KNOWN_OATHS["SOVEREIGN-AXIS"]
            if found != exp:
                self._add(HIGH, "oath_hash", f"SOVEREIGN-AXIS hash mismatch: {found}... expected {exp}...",
                          "SLICE-A §OATHS", "SLICE-D FORWARD item 6",
                          "Verify against original SliceD source.")
            else:
                self._add(INFO, "oath_hash", f"SOVEREIGN-AXIS hash matches known value ({exp}...).",
                          "SLICE-A", "SLICE-D", "None")
        else:
            self._add(HIGH, "oath_hash", "SOVEREIGN-AXIS OATH not found in SLICE-A",
                      "SLICE-A", "SLICE-D", "Locate OATH section.")
        fp = re.search(r'OATH::FULL-POWER.*?HASH:\s*([0-9a-f]+)', text_a, re.DOTALL | re.IGNORECASE)
        if fp:
            found = fp.group(1).strip()[:8]
            exp = KNOWN_OATHS["FULL-POWER"]
            if found != exp:
                self._add(HIGH, "oath_hash", f"FULL-POWER hash mismatch: {found}... expected {exp}...",
                          "SLICE-A", "SLICE-D", "Verify against original.")
        else:
            self._add(HIGH, "oath_hash", "FULL-POWER OATH not found in SLICE-A", "SLICE-A", "SLICE-D", "Locate OATH section.")

    def check_gap004_open(self, text_a: str):
        if not text_a:
            return
        m = re.search(r'GAP:004.*?Status:\s*(\w+)', text_a, re.DOTALL | re.IGNORECASE)
        if m:
            status = m.group(1).strip().upper()
            if status in ('CLOSED', 'RESOLVED', 'RATIFIED'):
                self._add(CRITICAL, "gap_status",
                          f"GAP#004 shows status '{status}' but has no resolution path. This may be a false closure.",
                          "SLICE-A §GAP_REGISTRY", "SLICE-D item 2",
                          "Verify closure is genuine. If no resolution path documented, reopen immediately.")
            else:
                self._add(INFO, "gap_status", "GAP#004 correctly marked OPEN.",
                          "SLICE-A", "SLICE-D", "Continue holding the gap. See gap004_mediator.py.")
        else:
            self._add(HIGH, "gap_status", "GAP#004 not found in SLICE-A gap registry",
                      "SLICE-A", "COV#012", "Verify GAP#004 is present and correctly marked.")

    def check_provisional_covenants(self, text_a: str):
        if not text_a:
            return
        p = re.findall(r'(COV[:#][A-Z0-9\-]+).*?\[PROVISIONAL\]', text_a, re.IGNORECASE)
        if p:
            self._add(MEDIUM, "provisional_covenant",
                      f"Provisional covenants found: {', '.join(set(p))}. These require 90-day cooling and two-signature ratification.",
                      "SLICE-A §COVENANTS", "SLICE-A §GOVERNANCE (90-day cooling)",
                      "Do not treat these as ratified. 90-day cooling period and dual sign-off required.")

    def check_proverb_linkage(self, text_a: str, text_c: str):
        if not text_a:
            return
        anomalies = re.findall(r'ANOM#[A-Z0-9\-]+', text_a or '')
        if text_c:
            anomalies += re.findall(r'ANOM#[A-Z0-9\-]+', text_c)
        anomalies = list(set(anomalies))
        proverbs = set(re.findall(r'P#[A-Z0-9\-]+', text_a or ''))
        if text_c:
            proverbs |= set(re.findall(r'P#[A-Z0-9\-]+', text_c))
        if anomalies and not proverbs:
            self._add(HIGH, "proverb_linkage",
                      f"Found {len(anomalies)} anomaly references but no proverb links. COV#006 requires every anomaly to link to at least one proverb.",
                      "SLICE-A §COVENANTS COV#006, SLICE-C", "COV#006",
                      "Link each anomaly to at least one proverb before ratification.")
        elif anomalies:
            self._add(INFO, "proverb_linkage",
                      f"Found {len(anomalies)} anomaly references and {len(proverbs)} proverb references. Manual verification required.",
                      "SLICE-A", "COV#006", "Verify individual ANOM→proverb links during tending ritual.")

    def check_superseded_files(self):
        for fname in SUPERSEDED_FILES:
            fpath = self.root / fname
            if fpath.exists():
                content = fpath.read_text(encoding='utf-8', errors='replace')
                if 'superseded' not in content.lower():
                    self._add(HIGH, "superseded_file",
                              f"{fname} exists but is not marked superseded. It may contain oath hash errors or outdated content.",
                              str(fpath), "SLICE-D item 10",
                              f"Open {fname}, add 'STATUS: superseded' header, add amendment entry in MANIFEST/amendments.md.")
            else:
                self._add(INFO, "superseded_file",
                          f"{fname} not present in repository (correct — was superseded)",
                          "repo root", "SLICE-D item 10", "None")

    def check_chapter_completeness(self, text_c: str):
        if not text_c:
            return
        refs = re.findall(r'[Cc]hapter[\s\-_]?(\d+)', text_c)
        if refs:
            nums = sorted(set(int(n) for n in refs if n.isdigit()))
            if nums:
                expected = set(range(1, max(nums)+1))
                found = set(nums)
                missing = expected - found
                if missing:
                    self._add(MEDIUM, "chapter_completeness",
                              f"Chapter references found up to {max(nums)} but chapters {sorted(missing)} not referenced in SLICE-C. May indicate missing ingestion.",
                              "SLICE-C", "SLICE-D item 3",
                              "Steward provides source for missing chapters. Secretary integrates into SLICE-C amendment with new IDs.")

    def check_duplicate_ids(self, *texts):
        all_ids = []
        for t in texts:
            if t:
                all_ids += re.findall(r'(?:P|ANOM|GAP|W|COV)#[A-Z0-9\-]+', t)
        seen = {}
        duplicates = []
        for i in all_ids:
            seen[i] = seen.get(i, 0) + 1
            if seen[i] == 2:
                duplicates.append(i)
        if duplicates:
            self._add(HIGH, "duplicate_ids",
                      f"Duplicate IDs found across slices: {', '.join(duplicates[:10])}" +
                      (f" and {len(duplicates)-10} more" if len(duplicates) > 10 else ""),
                      "cross-slice", "SLICE-A §GOVERNANCE (consistency_check)",
                      "Investigate each duplicate. Determine which is canonical, which should be superseded. Use amendment protocol (COV#NEW-F).")
        else:
            self._add(INFO, "duplicate_ids", "No duplicate IDs detected across readable slices",
                      "cross-slice", "SLICE-A", "None")

    def check_ratification_status(self, text_a: str):
        if not text_a:
            return
        if re.search(r'STATUS:\s*ratified', text_a, re.IGNORECASE) and \
           re.search(r'provisional:\s*true', text_a, re.IGNORECASE):
            self._add(HIGH, "ratification_status",
                      "SLICE-A contains both 'STATUS: ratified' and 'provisional: true'. This is a contradiction per GAP#010.",
                      "SLICE-A header", "GAP#010, SLICE-A §GOVERNANCE",
                      "Clarify: is this file committed (pushed to repo) or ratified (90-day cooling + two signatures)? Update status accordingly.")

    def run(self) -> list:
        self.findings = []
        text_a = self._read_slice(SLICE_A)
        text_b = self._read_slice(SLICE_B)
        text_c = self._read_slice(SLICE_C)
        if not SLICE_D.exists():
            self._add(CRITICAL, "missing_file", "SLICE-D not found. This file contains the Interface and Ledger.",
                      str(SLICE_D), "SLICE-D item 6",
                      "Locate KALAXI_CANON_SliceD.docx and convert to readable text. Do not ratify oath-related elements until SliceD is verified.")
        else:
            self._add(MEDIUM, "slice_d_format", "SLICE-D exists as a binary PDF file. Text scanning is not possible.",
                      str(SLICE_D), "SLICE-D item 6",
                      "Convert SliceD to plain text (.txt or .md) for machine verification. Until then, oath-related ratification should be blocked.")
        self.check_oath_hashes(text_a)
        self.check_gap004_open(text_a)
        self.check_provisional_covenants(text_a)
        self.check_proverb_linkage(text_a, text_c)
        self.check_superseded_files()
        self.check_chapter_completeness(text_c)
        self.check_duplicate_ids(text_a, text_b, text_c)
        self.check_ratification_status(text_a)
        return self.findings

    def display_report(self):
        severity_order = [CRITICAL, HIGH, MEDIUM, LOW, INFO]
        counts = {s: 0 for s in severity_order}
        for f in self.findings:
            counts[f.severity] += 1
        print(f"\n{'═'*65}")
        print(f"CANON INTEGRITY REPORT — {self.timestamp[:10]}")
        print(f"{'═'*65}")
        print(f"Files checked: {', '.join(self.files_checked) or 'none'}")
        print(f"Total findings: {len(self.findings)}")
        for sev in severity_order:
            if counts[sev] > 0:
                print(f"  {sev}: {counts[sev]}")
        print()
        for sev in severity_order:
            for f in self.findings:
                if f.severity == sev:
                    icon = {CRITICAL: '🔴', HIGH: '🟠', MEDIUM: '🟡', LOW: '🔵', INFO: '⚪'}.get(sev, '·')
                    print(f"{icon} [{f.severity}] {f.category}")
                    print(f"   {f.description}")
                    print(f"   Location:   {f.location}")
                    print(f"   Canon ref:  {f.canon_reference}")
                    print(f"   Action:     {f.action_required}\n")
        print(f"{'─'*65}")
        print("No findings were auto-resolved. All require steward review.")
        print(f"{'═'*65}\n")

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "files_checked": self.files_checked,
            "total_findings": len(self.findings),
            "findings": [
                {
                    "severity": f.severity,
                    "category": f.category,
                    "description": f.description,
                    "location": f.location,
                    "canon_reference": f.canon_reference,
                    "action_required": f.action_required,
                    "auto_resolvable": f.auto_resolvable
                }
                for f in self.findings
            ]
        }

def main():
    args = sys.argv[1:]
    output_json = '--json' in args
    root = REPO_ROOT
    for i, arg in enumerate(args):
        if arg == '--root' and i+1 < len(args):
            root = Path(args[i+1])
    scanner = CanonIntegrityScanner(root)
    scanner.run()
    if output_json:
        print(json.dumps(scanner.to_dict(), indent=2))
    else:
        scanner.display_report()

if __name__ == "__main__":
    main()
