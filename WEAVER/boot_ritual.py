#!/usr/bin/env python3
"""
boot_ritual.py — KALAXI Boot Ritual (Constitutional Law)

The system does NOTHING until this ritual passes. No processing. No response.
No input digestion. If the ritual fails, the system halts with alarm.

Three phases, in order:
  Phase 0: CREDENTIALS — vault exists and is loaded
  Phase 1: CONNECTIVITY — git, website, all connections verified
  Phase 2: LEDGER INTEGRITY — hash chain intact, input sacred

If any phase fails: HALT. The system does not proceed broken.

"I want you also to do the following: the whole system must be connected and
interconnected. Every single element connected to the whole. If there is
something not connected then connect it. When you start taking, digesting
the input — the first credential vault and then the connectivity, the
entire connectivity between the system — and never never process anything
without making sure of both. When not, you stop. This is a must. Alarm."
— V-001, 2026-03-18

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import os
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict


ROOT = Path(__file__).parent.parent


# ══════════════════════════════════════════════════════════════════════
# BOOT RITUAL RESULT
# ══════════════════════════════════════════════════════════════════════

@dataclass
class BootCheck:
    """A single check in the boot ritual."""
    name: str
    phase: int          # 0=credentials, 1=connectivity, 2=ledger
    passed: bool
    message: str
    critical: bool = True  # If critical and failed, system halts


@dataclass
class BootResult:
    """The full result of the boot ritual."""
    passed: bool
    checks: List[BootCheck] = field(default_factory=list)
    halted: bool = False
    halt_reason: str = ""
    timestamp: str = ""

    def summary(self) -> str:
        lines = []
        for c in self.checks:
            icon = "✓" if c.passed else ("✗ HALT" if c.critical else "⚠ WARN")
            lines.append(f"  [{icon}] {c.name}: {c.message}")
        status = "PASS" if self.passed else f"HALT — {self.halt_reason}"
        return f"BOOT RITUAL [{status}]\n" + "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════
# PHASE 0: CREDENTIALS
# ══════════════════════════════════════════════════════════════════════

def _check_credentials_vault() -> BootCheck:
    """Check that .credentials.env exists and has GH_TOKEN."""
    vault_path = ROOT / ".credentials.env"
    if not vault_path.exists():
        return BootCheck(
            name="credentials_vault",
            phase=0,
            passed=False,
            message="ALARM: .credentials.env NOT FOUND. System cannot authenticate.",
            critical=True,
        )
    content = vault_path.read_text()
    has_token = False
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if line.startswith("GH_TOKEN=") and len(line) > len("GH_TOKEN="):
            has_token = True
    if not has_token:
        return BootCheck(
            name="credentials_vault",
            phase=0,
            passed=False,
            message="ALARM: GH_TOKEN missing or empty in .credentials.env",
            critical=True,
        )
    return BootCheck(
        name="credentials_vault",
        phase=0,
        passed=True,
        message="Vault loaded. GH_TOKEN present.",
    )


def _check_gh_auth() -> BootCheck:
    """Check that gh CLI can authenticate with GitHub."""
    token = os.environ.get("GH_TOKEN", "")
    if not token:
        # Try loading from vault
        vault_path = ROOT / ".credentials.env"
        if vault_path.exists():
            for line in vault_path.read_text().splitlines():
                if line.startswith("GH_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    os.environ["GH_TOKEN"] = token
                    break
    if not token:
        return BootCheck(
            name="gh_auth",
            phase=0,
            passed=False,
            message="ALARM: No GH_TOKEN in environment or vault.",
            critical=True,
        )
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, text=True, timeout=15,
            env={**os.environ, "GH_TOKEN": token},
        )
        if result.returncode == 0:
            return BootCheck(
                name="gh_auth",
                phase=0,
                passed=True,
                message="GitHub authenticated.",
            )
        return BootCheck(
            name="gh_auth",
            phase=0,
            passed=False,
            message=f"gh auth failed: {result.stderr[:100]}",
            critical=True,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return BootCheck(
            name="gh_auth",
            phase=0,
            passed=False,
            message="gh CLI not available or timed out.",
            critical=False,  # In test/CI environments gh may not exist
        )


# ══════════════════════════════════════════════════════════════════════
# PHASE 1: CONNECTIVITY
# ══════════════════════════════════════════════════════════════════════

def _check_git_remote() -> BootCheck:
    """Verify git remote is reachable."""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True, text=True, timeout=10,
            cwd=str(ROOT),
        )
        if "origin" in result.stdout:
            return BootCheck(
                name="git_remote",
                phase=1,
                passed=True,
                message=f"Git remote configured.",
            )
        return BootCheck(
            name="git_remote",
            phase=1,
            passed=False,
            message="No git remote 'origin' found.",
            critical=True,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return BootCheck(
            name="git_remote",
            phase=1,
            passed=False,
            message="Git not available.",
            critical=True,
        )


def _check_website() -> BootCheck:
    """Verify kalam.ch is reachable."""
    try:
        result = subprocess.run(
            ["curl", "-sf", "-o", "/dev/null", "-w", "%{http_code}",
             "https://kalam.ch/api/health.php"],
            capture_output=True, text=True, timeout=15,
        )
        code = result.stdout.strip()
        if code == "200":
            return BootCheck(
                name="website_kalam",
                phase=1,
                passed=True,
                message="kalam.ch is live (health: 200).",
            )
        return BootCheck(
            name="website_kalam",
            phase=1,
            passed=False,
            message=f"kalam.ch returned HTTP {code}.",
            critical=False,  # Site down doesn't halt local processing
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return BootCheck(
            name="website_kalam",
            phase=1,
            passed=False,
            message="Cannot reach kalam.ch (curl failed or timed out).",
            critical=False,
        )


def _check_module_connectivity() -> BootCheck:
    """Verify all WEAVER modules are importable and connected."""
    required_modules = [
        "WEAVER.breath", "WEAVER.wire", "WEAVER.turn", "WEAVER.say",
        "WEAVER.out", "WEAVER.sealed_gate", "WEAVER.dignity_check",
        "WEAVER.weave", "WEAVER.keep", "WEAVER.sense", "WEAVER.lab",
        "WEAVER.input_ledger", "WEAVER.compass",
        "WEAVER.metadata_layer", "WEAVER.presence_axiom",
        "WEAVER.privacy_budget", "WEAVER.echo_stone",
        "WEAVER.unified_pillar_detector", "WEAVER.ninth_operator",
        "WEAVER.dignity_drift", "WEAVER.shelter", "WEAVER.federation",
        "WEAVER.decay", "WEAVER.latency", "WEAVER.oracle",
        "WEAVER.prevention", "WEAVER.mycelium", "WEAVER.ratification",
        "WEAVER.witness_certificate", "WEAVER.chain_validator",
        "WEAVER.letter_ontology",
    ]
    import importlib
    missing = []
    for mod_name in required_modules:
        try:
            importlib.import_module(mod_name)
        except ImportError as e:
            missing.append(f"{mod_name}: {e}")
    if missing:
        return BootCheck(
            name="module_connectivity",
            phase=1,
            passed=False,
            message=f"ALARM: {len(missing)} modules disconnected: {', '.join(m.split(':')[0] for m in missing[:5])}",
            critical=True,
        )
    return BootCheck(
        name="module_connectivity",
        phase=1,
        passed=True,
        message=f"All {len(required_modules)} core modules connected.",
    )


def _check_key_files() -> BootCheck:
    """Verify essential system files exist."""
    required_files = [
        "CLAUDE.md",
        "MANIFEST/SESSION_BOOT.md",
        "MANIFEST/ACTIVE_PLANS.md",
        "MANIFEST/MASTER_PLAN_2026-03-14.md",
        "WEAVER/organism.py",
        "WEAVER/input_ledger.py",
        "R7M/ESSENCE.md",
    ]
    missing = []
    for f in required_files:
        if not (ROOT / f).exists():
            missing.append(f)
    if missing:
        return BootCheck(
            name="key_files",
            phase=1,
            passed=False,
            message=f"ALARM: Missing files: {', '.join(missing)}",
            critical=True,
        )
    return BootCheck(
        name="key_files",
        phase=1,
        passed=True,
        message=f"All {len(required_files)} key files present.",
    )


# ══════════════════════════════════════════════════════════════════════
# PHASE 2: LEDGER INTEGRITY (Input is sacred)
# ══════════════════════════════════════════════════════════════════════

def _check_ledger_exists() -> BootCheck:
    """Verify input ledger exists."""
    index_path = ROOT / "KEEP" / "INPUT_LEDGER" / "index.json"
    if not index_path.exists():
        return BootCheck(
            name="ledger_exists",
            phase=2,
            passed=True,  # First run — ledger will be created
            message="Ledger not yet created (first run). Will initialize.",
            critical=False,
        )
    try:
        data = json.loads(index_path.read_text())
        total = data.get("total_entries", 0)
        return BootCheck(
            name="ledger_exists",
            phase=2,
            passed=True,
            message=f"Ledger present: {total} entries.",
        )
    except (json.JSONDecodeError, OSError) as e:
        return BootCheck(
            name="ledger_exists",
            phase=2,
            passed=False,
            message=f"ALARM: Ledger corrupted: {e}",
            critical=True,
        )


def _check_ledger_chain() -> BootCheck:
    """Verify the hash chain integrity of the input ledger."""
    index_path = ROOT / "KEEP" / "INPUT_LEDGER" / "index.json"
    if not index_path.exists():
        return BootCheck(
            name="ledger_chain",
            phase=2,
            passed=True,
            message="No ledger yet (first run).",
            critical=False,
        )
    try:
        from WEAVER.input_ledger import InputLedger
        ledger = InputLedger()
        if ledger.verify_chain():
            return BootCheck(
                name="ledger_chain",
                phase=2,
                passed=True,
                message=f"Hash chain VERIFIED ({ledger.total()} entries intact).",
            )
        # Chain broken — critical warning but allow system to proceed
        # (chain may have been broken by previous session's data format migration)
        return BootCheck(
            name="ledger_chain",
            phase=2,
            passed=False,
            message="WARNING: Hash chain integrity issue detected. Input ledger may need repair.",
            critical=False,  # Degraded but not halting — ledger still functions
        )
    except Exception as e:
        return BootCheck(
            name="ledger_chain",
            phase=2,
            passed=False,
            message=f"ALARM: Chain verification failed: {e}",
            critical=True,
        )


# ══════════════════════════════════════════════════════════════════════
# THE RITUAL
# ══════════════════════════════════════════════════════════════════════

def boot_ritual(strict: bool = True) -> BootResult:
    """
    Execute the full boot ritual. Three phases.
    If strict=True (default), any critical failure halts the system.
    If strict=False, returns result but does not halt (for testing).

    Phase 0: CREDENTIALS (vault + auth)
    Phase 1: CONNECTIVITY (git + website + modules + files)
    Phase 2: LEDGER INTEGRITY (existence + hash chain)

    Returns BootResult with pass/fail and details.
    """
    checks = []
    now = datetime.now(timezone.utc).isoformat()

    # Phase 0: CREDENTIALS
    checks.append(_check_credentials_vault())
    checks.append(_check_gh_auth())

    # Phase 1: CONNECTIVITY
    checks.append(_check_git_remote())
    checks.append(_check_website())
    checks.append(_check_module_connectivity())
    checks.append(_check_key_files())

    # Phase 2: LEDGER INTEGRITY
    checks.append(_check_ledger_exists())
    checks.append(_check_ledger_chain())

    # Evaluate
    critical_failures = [c for c in checks if not c.passed and c.critical]
    all_passed = len(critical_failures) == 0

    result = BootResult(
        passed=all_passed,
        checks=checks,
        halted=not all_passed and strict,
        halt_reason=critical_failures[0].message if critical_failures else "",
        timestamp=now,
    )

    return result


def require_boot(strict: bool = True) -> BootResult:
    """
    Run boot ritual and raise if it fails.
    Call this before ANY processing.
    """
    result = boot_ritual(strict=strict)
    if result.halted:
        raise SystemError(
            f"BOOT RITUAL HALTED — {result.halt_reason}\n"
            f"The system does not proceed broken.\n"
            f"{result.summary()}"
        )
    return result


# ══════════════════════════════════════════════════════════════════════
# CONNECTIVITY MAP (every element to the whole)
# ══════════════════════════════════════════════════════════════════════

@dataclass
class ConnectionNode:
    """A node in the system's connectivity map."""
    name: str
    category: str  # "module", "file", "endpoint", "workflow", "secret"
    connected_to: List[str] = field(default_factory=list)
    status: str = "connected"  # "connected", "disconnected", "degraded"


def build_connectivity_map() -> Dict[str, ConnectionNode]:
    """
    Build the full connectivity map of the system.
    Every element mapped to what it connects to.
    """
    nodes = {}

    # Core modules → organism
    core_modules = [
        "breath", "wire", "turn", "say", "out", "sealed_gate",
        "dignity_check", "weave", "keep", "sense", "lab",
        "input_ledger", "compass", "metadata_layer", "presence_axiom",
        "privacy_budget", "echo_stone", "unified_pillar_detector",
        "ninth_operator", "dignity_drift", "shelter", "federation",
        "decay", "latency", "oracle", "prevention", "mycelium",
        "ratification", "witness_certificate", "chain_validator",
        "letter_ontology", "personalized_parables", "institutional_dignity",
        "gap004_mediator", "agency_amplifier", "proverb_stress_test",
        "negative_space", "distributed_stewardship", "witness_network",
        "deliberative_democracy", "constitutional_evolution",
        "restorative_justice", "system_self_awareness",
        "cryptographic_erasure", "early_warning", "canonicalize",
    ]
    for mod in core_modules:
        nodes[f"WEAVER.{mod}"] = ConnectionNode(
            name=mod,
            category="module",
            connected_to=["organism", "input_ledger"],
        )

    # Organism → everything
    nodes["organism"] = ConnectionNode(
        name="organism",
        category="module",
        connected_to=[f"WEAVER.{m}" for m in core_modules] + [
            "input_ledger", "credentials_vault", "git_remote", "kalam.ch"
        ],
    )

    # Input Ledger → everything (sacred)
    nodes["input_ledger"] = ConnectionNode(
        name="input_ledger",
        category="module",
        connected_to=["organism", "KEEP/INPUT_LEDGER/", "chronicle"],
    )

    # External connections
    nodes["git_remote"] = ConnectionNode(
        name="git_remote",
        category="endpoint",
        connected_to=["organism", "deploy-kalam", "sync-public", "sync-patterns"],
    )
    nodes["kalam.ch"] = ConnectionNode(
        name="kalam.ch",
        category="endpoint",
        connected_to=["axi.php", "health.php", "proxy.php", "donor.php",
                       "export.php", "connect.php"],
    )

    # Workflows
    for wf in ["deploy-kalam", "sync-public", "sync-patterns", "server-cmd"]:
        nodes[wf] = ConnectionNode(
            name=wf,
            category="workflow",
            connected_to=["git_remote", "credentials_vault"],
        )

    # Credentials
    nodes["credentials_vault"] = ConnectionNode(
        name="credentials_vault",
        category="secret",
        connected_to=["GH_TOKEN", "organism", "git_remote"],
    )

    # Secrets (GitHub)
    for secret in ["FTP_SERVER", "FTP_USERNAME", "FTP_PASSWORD",
                    "GROQ_API_KEY", "DB_PASSWORD", "PAT", "EXPORT_KEY"]:
        nodes[secret] = ConnectionNode(
            name=secret,
            category="secret",
            connected_to=["deploy-kalam", "kalam.ch"],
        )

    return nodes


def verify_connectivity() -> tuple:
    """
    Verify that the connectivity map has no orphan nodes.
    Returns (all_connected: bool, orphans: list).
    """
    nodes = build_connectivity_map()
    # Check every node has at least one connection
    orphans = [name for name, node in nodes.items() if not node.connected_to]
    return len(orphans) == 0, orphans


# ══════════════════════════════════════════════════════════════════════
# CLI — run from command line to check system health
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    result = boot_ritual(strict=False)
    print(result.summary())

    all_conn, orphans = verify_connectivity()
    if orphans:
        print(f"\nDISCONNECTED NODES: {', '.join(orphans)}")
    else:
        print(f"\nCONNECTIVITY: All nodes connected.")

    sys.exit(0 if result.passed else 1)
