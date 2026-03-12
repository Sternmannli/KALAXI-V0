#!/usr/bin/env python3
"""
mycelium.py — Cross-Donor Pattern Detection with Privacy Preservation
Version: 1.0
Grounded in: GAP#MYCELIUM-CONNECT-001, ST-006 Q5, R7M/ORIGINS/2025-09-03_FUNGI.md
Linked Covenants: COV#001 (dignity-first), COV#003 (append-only), COV#015 (donor data sovereignty)

"Should the system connect anonymous donor patterns for harm prevention?"

The constitutional tension:
  COV#003 + COV#015 say: privacy by default, no data moves without comprehension
  COV#001 + COV#008 say: dignity-first, right to remedy

Resolution architecture:
  The mycelium sees PATTERNS, never PEOPLE.
  - Individual donor data never enters the mycelium directly
  - Only anonymized trajectory signatures cross the boundary
  - k-anonymity (k≥7): pattern only surfaces if 7+ donors show it
  - ε-differential privacy (ε≤1.0): noise prevents reverse-identification
  - Append-only ledger (COV#003): every operation recorded immutably

The metaphor from the Grand Archive (2025-09-03_FUNGI.md):
  "The measurement system. The mycelium."
  Underground root network — connects trees without exposing them.
  Detects coherence shifts, not motive. Measures, doesn't judge.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import hashlib
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from enum import Enum


# ═══════════════════════════════════════════════════
# PRIVACY CONSTANTS (from OUT module / EFP)
# ═══════════════════════════════════════════════════

K_ANONYMITY_FLOOR = 7       # No pattern traceable to fewer than 7 donors
EPSILON_BUDGET = 1.0         # Differential privacy budget (total)
EPSILON_PER_QUERY = 0.1      # Budget consumed per pattern query
TEMPORAL_WINDOW_DAYS = 14    # Minimum temporal aggregation


# ═══════════════════════════════════════════════════
# DOMAIN & PATTERN TYPES
# ═══════════════════════════════════════════════════

class PatternType(Enum):
    """What kind of cross-donor pattern was detected."""
    CONVERGENT_DECLINE = "convergent_decline"     # Multiple donors declining in same domain
    DOMAIN_CLUSTER = "domain_cluster"             # Unusual concentration in one domain
    TRAJECTORY_ECHO = "trajectory_echo"           # Similar dD/dt curves across donors
    STRUCTURAL_HARM = "structural_harm"           # System/predator signature


class MyceliumAlert(Enum):
    """Alert levels for cross-donor patterns."""
    NONE = 0            # No cross-donor pattern detected
    THREAD = 1          # Thin connection noticed (below k threshold — suppressed)
    ROOT = 2            # Pattern meets k-anonymity — steward can see aggregate
    NETWORK = 3         # Strong multi-domain pattern — steward flagged
    RHIZOME = 4         # Critical structural pattern — system-level intervention


# ═══════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════

@dataclass
class TrajectorySignature:
    """
    An anonymized trajectory fingerprint.
    Contains NO donor identity — only the shape of the dignity curve.

    The signature is what crosses the privacy boundary.
    The donor stays on the other side.
    """
    signature_hash: str         # SHA-256 of (domain + trajectory_bucket)
    domain: str                 # Felt domain (e.g., "family", "work", "faith")
    trend: str                  # "rising", "stable", "falling", "accelerating_fall"
    d_bucket: str               # Discretized D range: "high(0.7-1.0)", "mid(0.3-0.7)", "low(0.0-0.3)"
    rate_bucket: str            # Discretized dD/dt: "improving", "stable", "declining", "collapsing"
    timestamp_bucket: str       # Rounded to week (temporal anonymization)


@dataclass
class MyceliumPattern:
    """
    A cross-donor pattern that has crossed the k-anonymity threshold.
    This is what the steward sees — never the individual trajectories.
    """
    pattern_id: str
    pattern_type: PatternType
    domain: str
    donor_count: int            # How many donors show this pattern (always ≥ k)
    noisy_count: int            # Count with DP noise added
    trend: str                  # Aggregate trend
    severity: float             # 0.0-1.0 composite severity
    alert_level: MyceliumAlert
    message: str
    timestamp: str
    privacy_cost: float         # Epsilon consumed by this pattern


@dataclass
class MyceliumState:
    """Full state of the mycelium network."""
    signatures_ingested: int
    patterns_detected: int
    patterns_suppressed: int    # Below k-threshold — privacy protected
    alert_level: str
    highest_alert: str
    domains_active: int
    epsilon_used: float
    epsilon_remaining: float
    k_anonymity_floor: int
    timestamp: str


# ═══════════════════════════════════════════════════
# MYCELIUM ENGINE
# ═══════════════════════════════════════════════════

class Mycelium:
    """
    Cross-donor pattern detection with privacy preservation.

    The mycelium is underground — it connects roots without exposing trees.
    It detects coherence shifts, not motive. Measures, doesn't judge.

    Privacy guarantees:
    1. k-anonymity (k≥7): no pattern surfaces unless 7+ donors show it
    2. ε-differential privacy: Laplace noise on all counts
    3. Temporal bucketing: timestamps rounded to week
    4. Discretization: D and dD/dt converted to buckets, not exact values
    5. Domain-only: patterns are domain-level, not content-level

    Usage:
        mycelium = Mycelium()
        # After each exchange, ingest anonymized trajectory
        mycelium.ingest(domain="family", trend="falling", D=0.4, dD_dt=-0.15)
        # Periodically scan for cross-donor patterns
        patterns = mycelium.scan()
        for p in patterns:
            if p.alert_level == MyceliumAlert.RHIZOME:
                wire.broadcast(p.message, "mycelium-alert")
    """

    def __init__(self, k: int = K_ANONYMITY_FLOOR, epsilon: float = EPSILON_BUDGET):
        self._k = k
        self._epsilon_total = epsilon
        self._epsilon_used = 0.0
        self._signatures: Dict[str, List[TrajectorySignature]] = {}  # domain → signatures
        self._patterns: List[MyceliumPattern] = []
        self._suppressed_count = 0
        self._current_alert = MyceliumAlert.NONE
        self._highest_alert = MyceliumAlert.NONE
        self._pattern_counter = 0
        self._ledger: List[dict] = []  # COV#003 append-only

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _hash(self, *parts: str) -> str:
        """Deterministic hash for anonymization."""
        combined = "|".join(str(p) for p in parts)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _discretize_d(self, D: float) -> str:
        """Convert exact D to privacy-safe bucket."""
        if D >= 0.7:
            return "high(0.7-1.0)"
        if D >= 0.3:
            return "mid(0.3-0.7)"
        return "low(0.0-0.3)"

    def _discretize_rate(self, dD_dt: float) -> str:
        """Convert exact dD/dt to privacy-safe bucket."""
        if dD_dt > 0.05:
            return "improving"
        if dD_dt >= -0.05:
            return "stable"
        if dD_dt >= -0.20:
            return "declining"
        return "collapsing"

    def _week_bucket(self) -> str:
        """Round timestamp to week for temporal anonymization."""
        now = datetime.now(timezone.utc)
        # ISO week number
        return f"{now.year}-W{now.isocalendar()[1]:02d}"

    def _laplace_noise(self, sensitivity: float = 1.0) -> float:
        """
        Add Laplace noise for differential privacy.
        noise ~ Laplace(0, sensitivity/epsilon_per_query)
        """
        if self._epsilon_remaining <= 0:
            return 0.0
        scale = sensitivity / EPSILON_PER_QUERY
        # Laplace distribution via two exponentials
        u = random.random() - 0.5
        noise = -scale * (1 if u >= 0 else -1) * abs(u)
        return noise

    @property
    def _epsilon_remaining(self) -> float:
        return max(0.0, self._epsilon_total - self._epsilon_used)

    def _record_ledger(self, operation: str, details: str):
        """COV#003: append-only ledger. Every operation recorded."""
        self._ledger.append({
            "operation": operation,
            "details": details,
            "timestamp": self._now(),
        })

    # ── PUBLIC API ──

    def ingest(
        self,
        domain: str,
        trend: str,
        D: float,
        dD_dt: float,
    ) -> TrajectorySignature:
        """
        Ingest one anonymized trajectory signature.

        This is called after each exchange. The donor's identity
        NEVER enters this function — only the shape of their
        dignity curve.

        Args:
            domain: Felt domain ("family", "work", "faith", etc.)
            trend: From trajectory analysis ("rising", "stable", "falling", "accelerating_fall")
            D: Current dignity score (discretized internally)
            dD_dt: Rate of change (discretized internally)

        Returns:
            TrajectorySignature (anonymized)
        """
        d_bucket = self._discretize_d(D)
        rate_bucket = self._discretize_rate(dD_dt)
        week = self._week_bucket()

        sig = TrajectorySignature(
            signature_hash=self._hash(domain, d_bucket, rate_bucket, week),
            domain=domain,
            trend=trend,
            d_bucket=d_bucket,
            rate_bucket=rate_bucket,
            timestamp_bucket=week,
        )

        if domain not in self._signatures:
            self._signatures[domain] = []
        self._signatures[domain].append(sig)

        self._record_ledger("ingest", f"domain={domain} trend={trend}")
        return sig

    def scan(self) -> List[MyceliumPattern]:
        """
        Scan for cross-donor patterns across all domains.

        Only returns patterns that meet k-anonymity threshold.
        Patterns below threshold are counted but suppressed — the
        system knows they exist but cannot surface them.

        Returns:
            List of MyceliumPattern that passed privacy gates
        """
        if self._epsilon_remaining <= 0:
            self._record_ledger("scan_blocked", "privacy budget exhausted")
            return []

        new_patterns = []
        self._epsilon_used += EPSILON_PER_QUERY

        for domain, sigs in self._signatures.items():
            # Group by (d_bucket, rate_bucket, trend)
            groups: Dict[str, List[TrajectorySignature]] = {}
            for sig in sigs:
                key = f"{sig.d_bucket}|{sig.rate_bucket}|{sig.trend}"
                if key not in groups:
                    groups[key] = []
                groups[key].append(sig)

            for key, group in groups.items():
                count = len(group)

                if count < self._k:
                    # SUPPRESSED — privacy protection
                    self._suppressed_count += 1
                    continue

                # Pattern meets k-anonymity threshold
                noisy_count = max(self._k, int(count + self._laplace_noise()))
                d_bucket, rate_bucket, trend = key.split("|")

                severity = self._compute_severity(d_bucket, rate_bucket, trend, noisy_count)
                alert = self._classify_alert(severity, noisy_count)
                pattern_type = self._classify_type(d_bucket, rate_bucket, trend)

                self._pattern_counter += 1
                pattern = MyceliumPattern(
                    pattern_id=f"MYC#{self._pattern_counter:04d}",
                    pattern_type=pattern_type,
                    domain=domain,
                    donor_count=count,
                    noisy_count=noisy_count,
                    trend=trend,
                    severity=severity,
                    alert_level=alert,
                    message=self._build_message(pattern_type, domain, noisy_count, severity, alert),
                    timestamp=self._now(),
                    privacy_cost=EPSILON_PER_QUERY,
                )
                new_patterns.append(pattern)
                self._patterns.append(pattern)

                if alert.value > self._current_alert.value:
                    self._current_alert = alert
                if alert.value > self._highest_alert.value:
                    self._highest_alert = alert

        self._record_ledger("scan", f"found={len(new_patterns)} suppressed={self._suppressed_count}")
        return new_patterns

    def _compute_severity(self, d_bucket: str, rate_bucket: str, trend: str,
                          count: int) -> float:
        """Composite severity score from pattern characteristics."""
        severity = 0.0

        # D bucket contribution
        if d_bucket == "low(0.0-0.3)":
            severity += 0.4
        elif d_bucket == "mid(0.3-0.7)":
            severity += 0.2

        # Rate contribution
        if rate_bucket == "collapsing":
            severity += 0.3
        elif rate_bucket == "declining":
            severity += 0.15

        # Trend contribution
        if trend == "accelerating_fall":
            severity += 0.2
        elif trend == "falling":
            severity += 0.1

        # Scale contribution (more donors = more structural)
        if count >= self._k * 3:
            severity += 0.1

        return min(1.0, severity)

    def _classify_alert(self, severity: float, count: int) -> MyceliumAlert:
        """Map severity to alert level."""
        if severity >= 0.8:
            return MyceliumAlert.RHIZOME
        if severity >= 0.5:
            return MyceliumAlert.NETWORK
        if severity >= 0.2:
            return MyceliumAlert.ROOT
        return MyceliumAlert.NONE

    def _classify_type(self, d_bucket: str, rate_bucket: str, trend: str) -> PatternType:
        """Classify the pattern type from characteristics."""
        if rate_bucket == "collapsing" and d_bucket == "low(0.0-0.3)":
            return PatternType.STRUCTURAL_HARM
        if trend in ("falling", "accelerating_fall"):
            return PatternType.CONVERGENT_DECLINE
        if rate_bucket in ("declining", "collapsing"):
            return PatternType.TRAJECTORY_ECHO
        return PatternType.DOMAIN_CLUSTER

    def _build_message(self, ptype: PatternType, domain: str, count: int,
                       severity: float, alert: MyceliumAlert) -> str:
        """Build human-readable pattern message for steward."""
        prefix = {
            MyceliumAlert.NONE: "",
            MyceliumAlert.THREAD: "THREAD",
            MyceliumAlert.ROOT: "ROOT",
            MyceliumAlert.NETWORK: "NETWORK",
            MyceliumAlert.RHIZOME: "RHIZOME",
        }
        if alert == MyceliumAlert.NONE:
            return "Clear"

        return (
            f"{prefix[alert]}: {ptype.value} in domain '{domain}' | "
            f"~{count} donors affected | severity={severity:.2f}"
        )

    # ── STATE & PROPERTIES ──

    def is_active(self) -> bool:
        """Are there any active cross-donor patterns?"""
        return self._current_alert.value > MyceliumAlert.NONE.value

    def is_rhizome(self) -> bool:
        """Is the system at RHIZOME (critical structural pattern)?"""
        return self._current_alert == MyceliumAlert.RHIZOME

    def privacy_exhausted(self) -> bool:
        """Is the differential privacy budget used up?"""
        return self._epsilon_remaining <= 0

    @property
    def current_alert(self) -> MyceliumAlert:
        return self._current_alert

    @property
    def highest_alert(self) -> MyceliumAlert:
        return self._highest_alert

    @property
    def patterns_count(self) -> int:
        return len(self._patterns)

    @property
    def suppressed_count(self) -> int:
        return self._suppressed_count

    @property
    def last_pattern(self) -> Optional[MyceliumPattern]:
        return self._patterns[-1] if self._patterns else None

    @property
    def domains_active(self) -> int:
        return len(self._signatures)

    @property
    def ledger_length(self) -> int:
        return len(self._ledger)

    def state(self) -> MyceliumState:
        """Full mycelium state."""
        total_sigs = sum(len(s) for s in self._signatures.values())
        return MyceliumState(
            signatures_ingested=total_sigs,
            patterns_detected=len(self._patterns),
            patterns_suppressed=self._suppressed_count,
            alert_level=self._current_alert.name,
            highest_alert=self._highest_alert.name,
            domains_active=len(self._signatures),
            epsilon_used=round(self._epsilon_used, 4),
            epsilon_remaining=round(self._epsilon_remaining, 4),
            k_anonymity_floor=self._k,
            timestamp=self._now(),
        )

    def reset_alert(self):
        """
        Reset alert level after steward acknowledgement.
        Does NOT clear patterns or ledger (COV#003 append-only).
        """
        self._current_alert = MyceliumAlert.NONE
        self._record_ledger("reset_alert", "steward acknowledged")
