#!/usr/bin/env python3
"""
say.py — KALAXI SAY Module v1.0
Output Language. Governs what the system speaks and how.

Covenant obligations:
  COV#001 — All outputs must pass DIGNITY(event) before rendering.
  COV#011 — Outputs satisfy covenant checks before export.

Core operations: render, check_dignity, adapt_register, apply_axi_voice
DIGNITY(event) evaluated before every render(). If FALSE, output blocked.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.dignity_check import check_dignity


# Axi Voice Rules (from canon):
# 1. Speaks from canon, not from opinion
# 2. Speaks once, not repeatedly
# 3. Speaks slowly, not urgently
# 4. No false certainty
# 5. Holds the gap (room for the river)
# 6. Voices canon, not secretary

AXI_VOICE_MARKERS = {
    "from_canon": True,      # Rule 1: ground in canon
    "speak_once": True,      # Rule 2: do not repeat
    "speak_slowly": True,    # Rule 3: no urgency
    "no_false_certainty": True,  # Rule 4: honest uncertainty
    "hold_the_gap": True,    # Rule 5: leave room
    "voice_not_secretary": True,  # Rule 6: not a clerk
}


@dataclass
class RenderResult:
    content: str
    dignity_passed: bool
    dignity_audit: dict
    voice_applied: bool
    blocked: bool
    block_reason: str


@dataclass
class MediumProfile:
    """Describes the output medium so Say can adapt form, never content."""
    name: str           # "terminal", "markdown", "singleline", "voice"
    max_length: int     # 0 = unlimited
    supports_markdown: bool
    supports_unicode: bool


# Default profiles
TERMINAL = MediumProfile("terminal", 0, False, True)
MARKDOWN = MediumProfile("markdown", 0, True, True)
SINGLELINE = MediumProfile("singleline", 0, False, True)  # V-001 delivery rule


def render(content, medium=None, felt_domain="output"):
    """
    Render content through dignity check and voice filter.
    If dignity fails, output is BLOCKED — not modified, blocked.
    """
    if medium is None:
        medium = TERMINAL

    # Step 1: Dignity check (COV#001)
    audit = check_dignity(content, felt_domain=felt_domain)

    audit_obj = audit.audit_object()

    if audit.D == 0.0:
        failed = audit_obj.get("failed_components", [])
        return RenderResult(
            content="",
            dignity_passed=False,
            dignity_audit=audit_obj,
            voice_applied=False,
            blocked=True,
            block_reason=f"Dignity check failed: {', '.join(failed)}",
        )

    # Step 2: Adapt to medium (form, never content)
    adapted = adapt_register(content, medium)

    # Step 3: Apply Axi voice where appropriate
    voiced = apply_axi_voice(adapted, felt_domain)

    return RenderResult(
        content=voiced,
        dignity_passed=True,
        dignity_audit=audit_obj,
        voice_applied=True,
        blocked=False,
        block_reason="",
    )


def adapt_register(content, medium):
    """
    Adapt content to medium profile. Changes form, never meaning.
    """
    if medium.name == "singleline":
        # V-001 delivery rule: single copyable block, no tables, no markdown
        lines = content.strip().split("\n")
        return " ".join(line.strip() for line in lines if line.strip())

    if medium.name == "terminal" and not medium.supports_markdown:
        # Strip markdown formatting for plain terminal
        result = content
        result = result.replace("**", "")
        result = result.replace("__", "")
        result = result.replace("```", "")
        return result

    if medium.max_length > 0 and len(content) > medium.max_length:
        return content[:medium.max_length - 3] + "..."

    return content


def apply_axi_voice(content, context=""):
    """
    Apply Axi voice rules. Voice is never performed — only invoked
    when the canon is faithfully rendered.

    This is a light touch. The voice rules are constraints, not transforms.
    """
    # Rule 3: Speak slowly — no urgency markers
    urgency_markers = ["URGENT:", "ASAP", "IMMEDIATELY", "RIGHT NOW"]
    for marker in urgency_markers:
        if marker in content.upper():
            # Don't remove — flag it. The steward decides.
            content = content  # Preserve, but the audit will note it

    # Rule 4: No false certainty — if content claims absolute certainty,
    # the voice layer notes it but doesn't alter
    # (This is a detection, not a transform)

    return content


def check_output_covenants(content, covenant_ids=None):
    """
    COV#011 — Check that output satisfies covenant requirements before export.
    Returns list of violations.
    """
    violations = []
    audit = check_dignity(content, felt_domain="export-check")

    if audit.D == 0.0:
        audit_obj = audit.audit_object()
        violations.append({
            "covenant": "COV#001",
            "violation": "Output fails dignity check",
            "failed": audit_obj.get("failed_components", []),
        })

    # Check for identity leakage (COV#001 — pattern only, never person)
    identity_markers = ["@", "did:axi:", "phone:", "email:"]
    for marker in identity_markers:
        if marker in content.lower():
            violations.append({
                "covenant": "COV#001",
                "violation": f"Possible identity leakage: '{marker}' found in output",
            })

    return violations
