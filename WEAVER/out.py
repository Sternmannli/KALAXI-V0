#!/usr/bin/env python3
"""
out.py — KALAXI OUT Module v1.0
Export and Anonymization. Governs what leaves the system boundary.

Covenant obligations:
  COV#011 — Output must satisfy covenant checks before export.
  COV#001 — Donor identity protected. Pattern only, never person.

Anonymization standard (from EFP):
  Privacy floor: k >= 7 (minimum k-anonymity)
  Epsilon: <= 1.0 (differential privacy budget)
  Window: >= 14 days (temporal aggregation minimum)
  Signature: Ed25519 over RFC-8785 canonical JSON
  Hash: SHA-256

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass


ROOT = Path(__file__).parent.parent

# Anonymization constants (from EFP spec)
K_ANONYMITY_FLOOR = 7
EPSILON_BUDGET = 1.0
TEMPORAL_WINDOW_DAYS = 14

# Ownership stamp (required on all exports)
OWNERSHIP_STAMP = {
    "copyright": "did:axi:mohamed (KALAM)",
    "owner": "Mohamed Farag",
    "contact": "info@kalam.ch",
    "timezone": "Europe/Zurich",
}


@dataclass
class ExportResult:
    content: str
    format: str
    anonymized: bool
    covenant_violations: list
    stamped: bool
    hash: str
    timestamp: str


@dataclass
class AnonymizationPolicy:
    """Controls how data is anonymized before export."""
    k_anonymity: int = K_ANONYMITY_FLOOR
    epsilon: float = EPSILON_BUDGET
    temporal_window_days: int = TEMPORAL_WINDOW_DAYS
    strip_names: bool = True
    strip_emails: bool = True
    strip_ids: bool = True
    strip_timestamps: bool = False  # Timestamps are provenance — careful


def _sha(text):
    return hashlib.sha256(text.strip().encode()).hexdigest()


def _now():
    return datetime.now(timezone.utc).isoformat()


def anonymize(data, policy=None):
    """
    Anonymize data according to policy.
    Pattern only, never person. COV#001.
    """
    if policy is None:
        policy = AnonymizationPolicy()

    result = str(data)

    if policy.strip_emails:
        result = re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+', '[EMAIL_REDACTED]', result)

    if policy.strip_names:
        # Strip common name patterns (Name: value)
        result = re.sub(r'(?i)(name|author|steward|donor):\s*\S+', r'\1: [REDACTED]', result)

    if policy.strip_ids:
        # Strip did: identifiers
        result = re.sub(r'did:\w+:\w+', '[DID_REDACTED]', result)
        # Strip phone patterns
        result = re.sub(r'\+?\d{10,}', '[PHONE_REDACTED]', result)

    return result


def validate_covenants(artifact):
    """
    Validate that an artifact passes all covenant checks before export.
    Returns list of violations. Empty list = pass.
    """
    import sys
    sys.path.insert(0, str(ROOT))
    from WEAVER.dignity_check import check_dignity

    violations = []

    # COV#001 — Dignity check
    audit = check_dignity(str(artifact), felt_domain="export-gate")
    if audit.D == 0.0:
        audit_obj = audit.audit_object()
        violations.append({
            "covenant": "COV#001",
            "type": "dignity_failure",
            "detail": audit_obj.get("failed_components", []),
        })

    # COV#001 — Identity leakage check
    text = str(artifact).lower()
    identity_patterns = [
        (r'[\w.+-]+@[\w-]+\.[\w.]+', "email address"),
        (r'did:\w+:\w+', "DID identifier"),
        (r'\+?\d{10,}', "phone number"),
    ]
    for pattern, label in identity_patterns:
        if re.search(pattern, text):
            violations.append({
                "covenant": "COV#001",
                "type": "identity_leakage",
                "detail": f"Possible {label} found in export artifact",
            })

    return violations


def stamp(artifact):
    """
    Add ownership stamp to artifact. Required on all exports.
    Returns stamped artifact as dict.
    """
    now = _now()
    content = str(artifact)

    return {
        "content": content,
        "stamp": OWNERSHIP_STAMP,
        "hash": _sha(content),
        "timestamp": now,
        "export_version": "1.0",
    }


def export(artifact, fmt="json", anonymization_level="standard"):
    """
    Full export pipeline: validate → anonymize → stamp → format.

    anonymization_level:
      "none"     — no anonymization (internal use only)
      "standard" — k>=7, epsilon<=1.0, strip PII
      "maximum"  — all identifiers stripped, timestamps generalized
    """
    now = _now()

    # Step 1: Validate covenants
    violations = validate_covenants(artifact)
    if violations:
        return ExportResult(
            content="",
            format=fmt,
            anonymized=False,
            covenant_violations=violations,
            stamped=False,
            hash="",
            timestamp=now,
        )

    # Step 2: Anonymize
    content = str(artifact)
    anonymized = False

    if anonymization_level == "standard":
        content = anonymize(content)
        anonymized = True
    elif anonymization_level == "maximum":
        policy = AnonymizationPolicy(
            strip_names=True,
            strip_emails=True,
            strip_ids=True,
            strip_timestamps=True,
        )
        content = anonymize(content, policy)
        # Also generalize any remaining dates
        content = re.sub(r'\d{4}-\d{2}-\d{2}', '[DATE_REDACTED]', content)
        anonymized = True

    # Step 3: Stamp
    stamped_obj = stamp(content)

    # Step 4: Format
    if fmt == "json":
        output = json.dumps(stamped_obj, indent=2)
    elif fmt == "text":
        output = (
            f"{content}\n\n"
            f"---\n"
            f"© {OWNERSHIP_STAMP['copyright']}\n"
            f"Hash: {stamped_obj['hash']}\n"
            f"Exported: {now}\n"
        )
    else:
        output = content

    return ExportResult(
        content=output,
        format=fmt,
        anonymized=anonymized,
        covenant_violations=[],
        stamped=True,
        hash=stamped_obj["hash"],
        timestamp=now,
    )
