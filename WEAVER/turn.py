#!/usr/bin/env python3
"""
turn.py — KALAXI TURN Module v1.0
Exchange Cycle Management. Every exchange has an open and a closed state.
Silence is not closure.

Covenant obligations:
  COV#002 — Every exchange must complete its cycle.

Core operations: open, close, defer, status, list_open
A donor always has at least one open path forward (agency_preserved).

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum


ROOT = Path(__file__).parent.parent
TURN_DIR = ROOT / "TURN"
TURN_LOG = TURN_DIR / "exchanges.json"


class ExchangeState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    DEFERRED = "deferred"


@dataclass
class TurnToken:
    exchange_id: str
    state: ExchangeState
    opened: str
    closed: str
    resolution: str
    defer_reason: str
    available_paths: list


class SilentClosureError(Exception):
    """Raised when an exchange is closed without explicit resolution.
    Silence is not closure. COV#002."""
    pass


class AgencyViolationError(Exception):
    """Raised when closing would leave donor with zero paths forward."""
    pass


class Turn:
    """The TURN module — manages exchange cycles."""

    def __init__(self):
        self._exchanges = {}
        self._log = []
        self._counter = 0

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def open(self, exchange_id=None, available_paths=None):
        """
        Open a new exchange. Returns a turn token.
        available_paths: what the donor can do next (at least 1 required).
        """
        if available_paths is None:
            available_paths = ["respond", "defer", "withdraw"]

        if not available_paths:
            raise AgencyViolationError(
                "Cannot open an exchange with zero paths. "
                "agency_preserved requires available_paths >= 1. (COV#002)"
            )

        if exchange_id is None:
            self._counter += 1
            exchange_id = f"EX-{self._counter:06d}"

        now = self._now()

        token = TurnToken(
            exchange_id=exchange_id,
            state=ExchangeState.OPEN,
            opened=now,
            closed="",
            resolution="",
            defer_reason="",
            available_paths=list(available_paths),
        )

        self._exchanges[exchange_id] = token

        self._log.append({
            "event": "open",
            "exchange_id": exchange_id,
            "paths": available_paths,
            "timestamp": now,
        })

        return token

    def close(self, exchange_id, resolution):
        """
        Close an exchange with explicit resolution.
        Silent closure is forbidden — resolution MUST be provided. COV#002.
        """
        if not resolution or not resolution.strip():
            raise SilentClosureError(
                "An exchange may not be silently closed. "
                "Close requires explicit resolution or explicit deferral. (COV#002)"
            )

        token = self._exchanges.get(exchange_id)
        if token is None:
            raise KeyError(f"Exchange {exchange_id} not found.")

        if token.state == ExchangeState.CLOSED:
            raise ValueError(f"Exchange {exchange_id} is already closed.")

        now = self._now()
        token.state = ExchangeState.CLOSED
        token.closed = now
        token.resolution = resolution

        self._log.append({
            "event": "close",
            "exchange_id": exchange_id,
            "resolution": resolution,
            "timestamp": now,
        })

        return token

    def defer(self, exchange_id, reason):
        """
        Defer an exchange — marks as deferred, not closed.
        Deferred exchanges appear in the manifest.
        """
        if not reason or not reason.strip():
            raise SilentClosureError(
                "Deferral requires explicit reason. (COV#002)"
            )

        token = self._exchanges.get(exchange_id)
        if token is None:
            raise KeyError(f"Exchange {exchange_id} not found.")

        if token.state == ExchangeState.CLOSED:
            raise ValueError(f"Exchange {exchange_id} is already closed. Cannot defer.")

        now = self._now()
        token.state = ExchangeState.DEFERRED
        token.defer_reason = reason

        self._log.append({
            "event": "defer",
            "exchange_id": exchange_id,
            "reason": reason,
            "timestamp": now,
        })

        return token

    def status(self, exchange_id):
        """Get current state of an exchange."""
        token = self._exchanges.get(exchange_id)
        if token is None:
            return None
        return token.state

    def list_open(self):
        """List all open exchanges. COV#002 — nothing left unresolved silently."""
        return [
            token for token in self._exchanges.values()
            if token.state == ExchangeState.OPEN
        ]

    def list_deferred(self):
        """List all deferred exchanges."""
        return [
            token for token in self._exchanges.values()
            if token.state == ExchangeState.DEFERRED
        ]

    def count_by_state(self):
        """Count exchanges by state."""
        counts = {s: 0 for s in ExchangeState}
        for token in self._exchanges.values():
            counts[token.state] += 1
        return {s.value: c for s, c in counts.items()}

    def reopen(self, exchange_id, reason):
        """Reopen a deferred exchange."""
        token = self._exchanges.get(exchange_id)
        if token is None:
            raise KeyError(f"Exchange {exchange_id} not found.")
        if token.state == ExchangeState.CLOSED:
            raise ValueError(f"Exchange {exchange_id} is closed. Cannot reopen.")

        now = self._now()
        token.state = ExchangeState.OPEN
        token.defer_reason = ""

        self._log.append({
            "event": "reopen",
            "exchange_id": exchange_id,
            "reason": reason,
            "timestamp": now,
        })

        return token
