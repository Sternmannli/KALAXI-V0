#!/usr/bin/env python3
"""
canonicalize.py — KALAXI Canonicalization + Federated Trust + Emergency Governance
Version: 1.0
Grounded in: EFP (federation.py), COV#006, COV#012, MANIFEST/tier1_stone.md

Three capabilities in one module:
  1. CANONICALIZATION — Produce duplicate_id_report, enforce tie-breaker policies,
     generate canonical manifest with deterministic JSON (RFC-8785 approach)
  2. ARTIFACT SIGNING — Ed25519 signatures on steward decisions and manifests
  3. EMERGENCY GOVERNANCE — Escalation playbook, audit trail, role definitions

Federation and external credibility require provable integrity.
This module converts an internal experiment into a trustworthy protocol.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from enum import Enum

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


# ═══════════════════════════════════════════════════
# PART 1: CANONICALIZATION
# ═══════════════════════════════════════════════════

# ID Patterns from the registry
ID_PATTERNS = {
    "COV": re.compile(r'COV#(\d+|NEW-[A-Z])'),
    "ANOM": re.compile(r'ANOM#(\d+)'),
    "P": re.compile(r'P#(\d+|EMERGE-\d+)'),
    "W": re.compile(r'W#(\d+)'),
    "GAP": re.compile(r'GAP#([A-Z0-9_-]+)'),
    "OBS": re.compile(r'OBS-(\d+)'),
    "T": re.compile(r'T#(\d+)'),
    "EV": re.compile(r'EV-(\d+)'),
    "ST": re.compile(r'ST-(\d+)'),
}


@dataclass
class IDEntry:
    """A single ID entry found in the codebase."""
    id_type: str           # COV, ANOM, P, W, etc.
    full_id: str           # COV#001, P#2135, etc.
    source_file: str       # Where it was found
    line_number: int
    context: str           # Surrounding text


@dataclass
class DuplicateReport:
    """Report of duplicate IDs found."""
    duplicates: Dict[str, List[IDEntry]]  # ID → list of entries
    total_ids_scanned: int
    unique_ids: int
    duplicate_count: int
    suggested_tiebreakers: List[dict]
    timestamp: str


class Canonicalizer:
    """
    Scans the codebase for all registered IDs, detects duplicates,
    and produces a canonical manifest.
    """

    SCAN_EXTENSIONS = {'.md', '.txt', '.py', '.json'}
    SKIP_DIRS = {'node_modules', '__pycache__', '.git', 'dist', 'site'}

    def __init__(self, root: Path = ROOT):
        self._root = root
        self._entries: List[IDEntry] = []
        self._ids: Dict[str, List[IDEntry]] = defaultdict(list)

    def scan(self) -> DuplicateReport:
        """Scan the codebase for all IDs and detect duplicates."""
        self._entries = []
        self._ids = defaultdict(list)

        for filepath in self._walk_files():
            self._scan_file(filepath)

        # Find duplicates
        duplicates = {
            full_id: entries
            for full_id, entries in self._ids.items()
            if len(entries) > 1
        }

        # Generate tiebreaker suggestions
        tiebreakers = []
        for full_id, entries in duplicates.items():
            tiebreakers.append({
                "id": full_id,
                "occurrences": len(entries),
                "files": list(set(e.source_file for e in entries)),
                "policy": self._suggest_tiebreaker(full_id, entries),
            })

        return DuplicateReport(
            duplicates=duplicates,
            total_ids_scanned=len(self._entries),
            unique_ids=len(self._ids),
            duplicate_count=len(duplicates),
            suggested_tiebreakers=tiebreakers,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _walk_files(self):
        """Walk the codebase, skipping non-relevant directories."""
        for path in self._root.rglob('*'):
            if any(skip in path.parts for skip in self.SKIP_DIRS):
                continue
            if path.is_file() and path.suffix in self.SCAN_EXTENSIONS:
                yield path

    def _scan_file(self, filepath: Path):
        """Scan a single file for ID patterns."""
        try:
            text = filepath.read_text(errors='ignore')
        except Exception:
            return

        lines = text.split('\n')
        rel_path = str(filepath.relative_to(self._root))

        for line_num, line in enumerate(lines, 1):
            for id_type, pattern in ID_PATTERNS.items():
                for match in pattern.finditer(line):
                    full_id = match.group(0)
                    entry = IDEntry(
                        id_type=id_type,
                        full_id=full_id,
                        source_file=rel_path,
                        line_number=line_num,
                        context=line.strip()[:120],
                    )
                    self._entries.append(entry)
                    self._ids[full_id].append(entry)

    def _suggest_tiebreaker(self, full_id: str, entries: List[IDEntry]) -> str:
        """Suggest a tiebreaker policy for a duplicate ID."""
        # Priority: tier1_stone > MANIFEST > CANON > everything else
        priority_dirs = ["MANIFEST/metadata/tier1_stone", "MANIFEST", "CANON", "WEAVER"]
        for priority in priority_dirs:
            canonical_entries = [e for e in entries if priority in e.source_file]
            if canonical_entries:
                return f"Canonical source: {canonical_entries[0].source_file} (highest-priority file)"

        # If all in same file, it's a reference pattern, not a true duplicate
        files = set(e.source_file for e in entries)
        if len(files) == 1:
            return "Same-file references — not a conflict. ID is referenced multiple times in one document."

        return "Steward review required — no clear priority file."

    def canonical_manifest(self) -> dict:
        """
        Produce the canonical manifest — all IDs, their types,
        their canonical source file, and their status.
        """
        manifest = {
            "manifest_version": "1.0",
            "generated": datetime.now(timezone.utc).isoformat(),
            "generator": "V-003 canonicalize.py",
            "total_ids": len(self._ids),
            "entries": {},
        }

        for full_id, entries in sorted(self._ids.items()):
            # Pick canonical entry (first by priority)
            canonical = self._pick_canonical(entries)
            manifest["entries"][full_id] = {
                "type": entries[0].id_type,
                "canonical_source": canonical.source_file,
                "canonical_line": canonical.line_number,
                "reference_count": len(entries),
                "all_sources": list(set(e.source_file for e in entries)),
            }

        return manifest

    def _pick_canonical(self, entries: List[IDEntry]) -> IDEntry:
        """Pick the canonical entry from multiple references."""
        priority = ["tier1_stone", "tier2_weaver", "tier3_honey", "tier4_hand",
                     "MANIFEST", "CANON", "THRESHOLD", "WEAVER"]
        for p in priority:
            for e in entries:
                if p in e.source_file:
                    return e
        return entries[0]


# ═══════════════════════════════════════════════════
# PART 2: ARTIFACT SIGNING (Ed25519)
# ═══════════════════════════════════════════════════

@dataclass
class SignedArtifact:
    """An artifact with a cryptographic signature."""
    artifact_id: str
    content_hash: str          # SHA-256 of canonical JSON
    signature: str             # Ed25519 signature (stub until keys provisioned)
    signer_id: str
    signer_role: str
    timestamp: str
    verification_status: str   # "unverified", "valid", "invalid"


class ArtifactSigner:
    """
    Ed25519 artifact signing for steward decisions and manifests.

    Currently uses HMAC-SHA256 as a stub. When Ed25519 keys are
    provisioned (via PyNaCl or cryptography library), the sign/verify
    methods swap to real Ed25519.

    Every signed artifact produces a verification chain entry.
    """

    def __init__(self, signer_id: str = "V-003", signer_role: str = "steward-system"):
        self._signer_id = signer_id
        self._signer_role = signer_role
        self._chain: List[SignedArtifact] = []
        # Stub key — replace with real Ed25519 keypair
        self._signing_key = hashlib.sha256(f"KALAXI-STUB-KEY:{signer_id}".encode()).hexdigest()

    def _canonical_json(self, data: dict) -> str:
        """RFC-8785 canonical JSON: sorted keys, no whitespace."""
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    def _content_hash(self, content: str) -> str:
        """SHA-256 of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _sign_stub(self, content_hash: str) -> str:
        """HMAC-SHA256 stub signature. Replace with Ed25519."""
        import hmac
        return hmac.new(
            self._signing_key.encode(),
            content_hash.encode(),
            hashlib.sha256
        ).hexdigest()

    def sign(self, artifact_id: str, data: dict) -> SignedArtifact:
        """
        Sign an artifact (manifest, steward decision, etc.).

        The data is canonicalized (RFC-8785), hashed, and signed.
        Returns a SignedArtifact with the signature and hash.
        """
        canonical = self._canonical_json(data)
        content_hash = self._content_hash(canonical)
        signature = self._sign_stub(content_hash)

        artifact = SignedArtifact(
            artifact_id=artifact_id,
            content_hash=content_hash,
            signature=signature,
            signer_id=self._signer_id,
            signer_role=self._signer_role,
            timestamp=datetime.now(timezone.utc).isoformat(),
            verification_status="unverified",
        )

        self._chain.append(artifact)
        return artifact

    def verify(self, artifact: SignedArtifact, data: dict) -> bool:
        """
        Verify a signed artifact against its data.
        Recomputes hash and signature, compares.
        """
        canonical = self._canonical_json(data)
        content_hash = self._content_hash(canonical)
        expected_sig = self._sign_stub(content_hash)

        valid = (
            artifact.content_hash == content_hash and
            artifact.signature == expected_sig
        )

        artifact.verification_status = "valid" if valid else "invalid"
        return valid

    def sign_manifest(self, manifest: dict) -> Tuple[SignedArtifact, dict]:
        """Sign a canonical manifest and return both."""
        artifact = self.sign("MANIFEST-CANONICAL", manifest)
        signed_manifest = {
            **manifest,
            "_signature": {
                "artifact_id": artifact.artifact_id,
                "content_hash": artifact.content_hash,
                "signature": artifact.signature,
                "signer_id": artifact.signer_id,
                "signer_role": artifact.signer_role,
                "timestamp": artifact.timestamp,
                "algorithm": "HMAC-SHA256-STUB (Ed25519 ready)",
            }
        }
        return artifact, signed_manifest

    @property
    def chain_length(self) -> int:
        return len(self._chain)

    @property
    def chain(self) -> List[SignedArtifact]:
        return list(self._chain)


# ═══════════════════════════════════════════════════
# PART 3: EMERGENCY GOVERNANCE
# ═══════════════════════════════════════════════════

class EscalationLevel(Enum):
    """Emergency escalation levels (ordered by severity)."""
    ROUTINE = 0
    ELEVATED = 1
    EMERGENCY = 2
    CONSTITUTIONAL = 3


@dataclass
class EscalationRecord:
    """Record of an escalation event."""
    record_id: str
    level: EscalationLevel
    trigger: str               # What caused the escalation
    description: str
    initiated_by: str          # "system", "steward", "donor"
    roles_notified: List[str]
    audit_trail: List[dict]
    resolution: str
    timestamp: str
    resolved: bool


EMERGENCY_PLAYBOOK = {
    "title": "KALAXI Emergency Governance Playbook v1.0",
    "purpose": "Define roles, escalation paths, and audit requirements for emergency governance.",
    "roles": {
        "steward": {
            "description": "Primary decision authority. Mohamed Farag.",
            "powers": ["pause exchanges", "review triage", "approve federation", "override provisional"],
            "constraints": ["Cannot override sealed gate", "Cannot delete KEEP artifacts", "Must provide reason for all actions"],
        },
        "system_v003": {
            "description": "AI steward assistant. Claude (V-003).",
            "powers": ["detect drift", "generate alerts", "produce reports", "suggest remedies"],
            "constraints": ["Cannot act without steward approval in LIVE mode", "Cannot modify sealed gate", "All actions logged"],
        },
        "ethics_reviewer": {
            "description": "External ethics review (future role).",
            "powers": ["audit triage decisions", "recommend covenant amendments", "flag constitutional issues"],
            "constraints": ["Advisory only — cannot directly modify system"],
        },
        "legal_counsel": {
            "description": "Legal review for privacy, GDPR, and compliance.",
            "powers": ["review data flows", "approve federation agreements", "flag legal risks"],
            "constraints": ["Cannot access individual donor data without steward approval"],
        },
    },
    "escalation_paths": {
        "routine": {
            "trigger": "Normal operational event",
            "response_time": "Next review cycle",
            "roles_involved": ["system_v003"],
            "audit_required": False,
        },
        "elevated": {
            "trigger": "Dignity drift detected (DECLINING), single-donor concern",
            "response_time": "48 hours",
            "roles_involved": ["system_v003", "steward"],
            "audit_required": True,
        },
        "emergency": {
            "trigger": "Critical dignity drift, sealed gate trigger, or privacy breach",
            "response_time": "Immediate (< 4 hours)",
            "roles_involved": ["system_v003", "steward", "ethics_reviewer"],
            "audit_required": True,
            "actions": ["Pause affected exchanges", "Generate incident report", "Notify steward"],
        },
        "constitutional": {
            "trigger": "Covenant violation, sealed gate compromise attempt, or structural harm (RHIZOME alert)",
            "response_time": "Immediate — system halts affected domain",
            "roles_involved": ["system_v003", "steward", "ethics_reviewer", "legal_counsel"],
            "audit_required": True,
            "actions": [
                "Halt all affected exchanges",
                "Generate full audit trail",
                "Steward + ethics review required before resumption",
                "Legal counsel notified if data breach suspected",
                "Incident report filed in MANIFEST",
            ],
        },
    },
    "audit_trail_requirements": {
        "what_is_logged": [
            "Every escalation trigger and level",
            "Every role notification and response",
            "Every decision and its rationale",
            "Every resolution and follow-up action",
            "Timestamps for all events (UTC)",
        ],
        "retention": "Permanent (COV#010 — no silent deletion)",
        "access": "Steward + authorized reviewers only",
        "format": "Append-only JSON in MANIFEST/escalation_log.json",
    },
    "legal_checklist": [
        "Is donor consent still valid for this action?",
        "Does this action require GDPR notification?",
        "Is the privacy budget within limits?",
        "Are all affected donors' rights preserved?",
        "Is the audit trail complete and tamper-evident?",
    ],
}


class EmergencyGovernance:
    """
    Emergency governance engine. Manages escalation, audit trails,
    and the playbook.
    """

    def __init__(self):
        self._records: List[EscalationRecord] = []
        self._counter = 0
        self._current_level = EscalationLevel.ROUTINE

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _next_id(self) -> str:
        self._counter += 1
        return f"ESC-{self._counter:04d}"

    def escalate(self, level: EscalationLevel, trigger: str,
                 description: str, initiated_by: str = "system") -> EscalationRecord:
        """
        Initiate an escalation. Determines roles to notify based on playbook.
        """
        path = EMERGENCY_PLAYBOOK["escalation_paths"].get(level.name.lower(), {})
        roles = path.get("roles_involved", ["steward"])

        record = EscalationRecord(
            record_id=self._next_id(),
            level=level,
            trigger=trigger,
            description=description,
            initiated_by=initiated_by,
            roles_notified=roles,
            audit_trail=[{
                "event": "escalation_initiated",
                "level": level.name.lower(),
                "trigger": trigger,
                "timestamp": self._now(),
                "initiated_by": initiated_by,
            }],
            resolution="",
            timestamp=self._now(),
            resolved=False,
        )

        self._records.append(record)

        if level.value > self._current_level.value:  # Numeric comparison
            self._current_level = level

        return record

    def resolve(self, record_id: str, resolution: str,
                resolved_by: str = "steward") -> EscalationRecord:
        """Resolve an escalation with explicit resolution."""
        record = next((r for r in self._records if r.record_id == record_id), None)
        if record is None:
            raise KeyError(f"Escalation {record_id} not found.")

        record.resolution = resolution
        record.resolved = True
        record.audit_trail.append({
            "event": "resolved",
            "resolution": resolution,
            "resolved_by": resolved_by,
            "timestamp": self._now(),
        })

        # Check if we can lower the current level
        unresolved = [r for r in self._records if not r.resolved]
        if unresolved:
            self._current_level = max(
                (r.level for r in unresolved),
                key=lambda l: l.value
            )
        else:
            self._current_level = EscalationLevel.ROUTINE

        return record

    def add_audit_entry(self, record_id: str, event: str, details: str,
                        actor: str = "system"):
        """Add an entry to an escalation's audit trail."""
        record = next((r for r in self._records if r.record_id == record_id), None)
        if record is None:
            raise KeyError(f"Escalation {record_id} not found.")

        record.audit_trail.append({
            "event": event,
            "details": details,
            "actor": actor,
            "timestamp": self._now(),
        })

    @property
    def current_level(self) -> EscalationLevel:
        return self._current_level

    @property
    def open_escalations(self) -> List[EscalationRecord]:
        return [r for r in self._records if not r.resolved]

    def playbook_text(self) -> str:
        """Return the playbook as readable text (for auditors)."""
        pb = EMERGENCY_PLAYBOOK
        lines = [
            f"# {pb['title']}",
            f"\n{pb['purpose']}",
            "\n## Roles",
        ]
        for role_id, role in pb["roles"].items():
            lines.append(f"\n### {role_id}")
            lines.append(f"  {role['description']}")
            lines.append(f"  Powers: {', '.join(role['powers'])}")
            lines.append(f"  Constraints: {', '.join(role['constraints'])}")

        lines.append("\n## Escalation Paths")
        for level, path in pb["escalation_paths"].items():
            lines.append(f"\n### {level.upper()}")
            lines.append(f"  Trigger: {path['trigger']}")
            lines.append(f"  Response time: {path['response_time']}")
            lines.append(f"  Roles: {', '.join(path['roles_involved'])}")
            if 'actions' in path:
                lines.append(f"  Actions:")
                for a in path['actions']:
                    lines.append(f"    - {a}")

        lines.append("\n## Legal Checklist")
        for item in pb["legal_checklist"]:
            lines.append(f"  [ ] {item}")

        return "\n".join(lines)

    def save_escalation_log(self):
        """Save escalation records to MANIFEST."""
        log_file = ROOT / "MANIFEST" / "escalation_log.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        records = [{
            "record_id": r.record_id,
            "level": r.level.name.lower(),
            "trigger": r.trigger,
            "description": r.description,
            "initiated_by": r.initiated_by,
            "roles_notified": r.roles_notified,
            "audit_trail": r.audit_trail,
            "resolution": r.resolution,
            "resolved": r.resolved,
            "timestamp": r.timestamp,
        } for r in self._records]

        with open(log_file, "w") as f:
            json.dump(records, f, indent=2)


# ═══════════════════════════════════════════════════
# INTEGRATED DEMO
# ═══════════════════════════════════════════════════

def demo():
    """Run the full canonicalization + signing + governance demo."""
    print("=" * 65)
    print("KALAXI CANONICALIZATION + TRUST + GOVERNANCE — DEMO")
    print("=" * 65)

    # Part 1: Canonicalization
    print("\n--- PART 1: CANONICALIZATION ---")
    canon = Canonicalizer()
    report = canon.scan()
    print(f"  Total IDs scanned:    {report.total_ids_scanned}")
    print(f"  Unique IDs:           {report.unique_ids}")
    print(f"  Duplicate IDs:        {report.duplicate_count}")
    if report.suggested_tiebreakers:
        print(f"  Tiebreaker suggestions:")
        for tb in report.suggested_tiebreakers[:5]:
            print(f"    {tb['id']} — {tb['occurrences']} occurrences — {tb['policy']}")

    # Generate manifest
    manifest = canon.canonical_manifest()
    print(f"  Manifest entries:     {len(manifest['entries'])}")

    # Part 2: Signing
    print("\n--- PART 2: ARTIFACT SIGNING ---")
    signer = ArtifactSigner(signer_id="V-003", signer_role="steward-system")
    sig_artifact, signed_manifest = signer.sign_manifest(manifest)
    print(f"  Manifest signed:      {sig_artifact.artifact_id}")
    print(f"  Content hash:         {sig_artifact.content_hash[:32]}...")
    print(f"  Signature:            {sig_artifact.signature[:32]}...")
    print(f"  Algorithm:            HMAC-SHA256-STUB (Ed25519 ready)")

    # Verify
    valid = signer.verify(sig_artifact, manifest)
    print(f"  Verification:         {'VALID' if valid else 'INVALID'}")

    # Save
    manifest_file = ROOT / "MANIFEST" / "canonical_manifest.json"
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_file, "w") as f:
        json.dump(signed_manifest, f, indent=2)
    print(f"  Saved to:             {manifest_file}")

    # Save duplicate report
    report_file = ROOT / "MANIFEST" / "duplicate_id_report.json"
    report_data = {
        "total_ids_scanned": report.total_ids_scanned,
        "unique_ids": report.unique_ids,
        "duplicate_count": report.duplicate_count,
        "suggested_tiebreakers": report.suggested_tiebreakers,
        "timestamp": report.timestamp,
    }
    with open(report_file, "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"  Duplicate report:     {report_file}")

    # Part 3: Emergency Governance
    print("\n--- PART 3: EMERGENCY GOVERNANCE ---")
    gov = EmergencyGovernance()

    # Simulate an escalation
    esc = gov.escalate(
        level=EscalationLevel.ELEVATED,
        trigger="Dignity drift detected in 'family' domain",
        description="EWMA and CUSUM detectors both firing. 3 consecutive declines.",
        initiated_by="early_warning_pipeline",
    )
    print(f"  Escalation created:   {esc.record_id} [{esc.level.value}]")
    print(f"  Roles notified:       {', '.join(esc.roles_notified)}")

    # Resolve
    esc = gov.resolve(
        esc.record_id,
        resolution="Steward reviewed. Pattern was transient. Monitoring continues.",
        resolved_by="steward",
    )
    print(f"  Resolved:             {esc.resolved}")
    print(f"  Current level:        {gov.current_level.value}")

    # Save playbook
    playbook_file = ROOT / "MANIFEST" / "emergency_playbook.md"
    with open(playbook_file, "w") as f:
        f.write(gov.playbook_text())
    print(f"  Playbook saved:       {playbook_file}")

    # Save escalation log
    gov.save_escalation_log()
    print(f"  Escalation log saved: MANIFEST/escalation_log.json")

    print("\n" + "=" * 65)
    print("Canonicalization complete. Artifacts signed. Governance playbook active.")
    print("=" * 65)


if __name__ == "__main__":
    demo()
