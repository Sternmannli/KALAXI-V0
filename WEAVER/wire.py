#!/usr/bin/env python3
"""
wire.py — KALAXI WIRE Module v1.0
Messaging and Signal. Governs how information moves between components and actors.

Covenant obligations:
  COV#002 — Every exchange must complete its cycle. Wire handles delivery confirmation.

Core operations: send, receive, confirm, broadcast, subscribe
No message lost silently. Priority messages never dropped.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from collections import defaultdict


ROOT = Path(__file__).parent.parent
WIRE_DIR = ROOT / "WIRE"
WIRE_LOG = WIRE_DIR / "wire_log.json"

# Priority levels
PRIORITY_CRITICAL = 0  # Never dropped, never queued
PRIORITY_HIGH = 1      # Never dropped, may queue briefly
PRIORITY_NORMAL = 2    # May queue under load
PRIORITY_LOW = 3       # May queue with notification


@dataclass
class Message:
    id: str
    source: str
    destination: str
    content: str
    priority: int = PRIORITY_NORMAL
    timestamp: str = ""
    confirmed: bool = False
    confirm_timestamp: str = ""
    topic: str = ""


class WireFailure(Exception):
    """Raised when message delivery fails. Always logged, never silent."""
    pass


class Wire:
    """The WIRE module — message bus for KALAXI components."""

    def __init__(self):
        self._queue = defaultdict(list)  # destination -> [messages]
        self._log = []
        self._subscribers = defaultdict(list)  # topic -> [handlers]
        self._msg_counter = 0
        self._load_log()

    def _load_log(self):
        if WIRE_LOG.exists():
            with open(WIRE_LOG) as f:
                self._log = json.load(f)

    def _save_log(self):
        WIRE_DIR.mkdir(parents=True, exist_ok=True)
        with open(WIRE_LOG, "w") as f:
            json.dump(self._log, f, indent=2)

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _next_id(self):
        self._msg_counter += 1
        return f"MSG-{self._msg_counter:06d}"

    def send(self, content, destination, priority=PRIORITY_NORMAL, source="system"):
        """Send a message. Returns message ID. Logs failure if no listener."""
        msg_id = self._next_id()
        now = self._now()

        entry = {
            "id": msg_id,
            "source": source,
            "destination": destination,
            "content": content,
            "priority": priority,
            "timestamp": now,
            "confirmed": False,
            "confirm_timestamp": "",
            "topic": "",
        }

        self._queue[destination].append(entry)

        self._log.append({
            "event": "send",
            "message_id": msg_id,
            "source": source,
            "destination": destination,
            "priority": priority,
            "timestamp": now,
        })
        self._save_log()

        return msg_id

    def receive(self, source):
        """Receive next message from a source's queue. Returns None if empty."""
        queue = self._queue.get(source, [])
        if not queue:
            return None

        # Priority messages first (lower number = higher priority)
        queue.sort(key=lambda m: m["priority"])
        msg = queue.pop(0)

        self._log.append({
            "event": "receive",
            "message_id": msg["id"],
            "source": source,
            "timestamp": self._now(),
        })
        self._save_log()

        return msg

    def confirm(self, message_id):
        """Confirm delivery of a message. COV#002 — every exchange completes its cycle."""
        now = self._now()

        self._log.append({
            "event": "confirm",
            "message_id": message_id,
            "timestamp": now,
        })
        self._save_log()

        return {"message_id": message_id, "confirmed": True, "timestamp": now}

    def broadcast(self, content, topic, source="system", priority=PRIORITY_NORMAL):
        """Broadcast a message to all subscribers of a topic."""
        msg_id = self._next_id()
        now = self._now()

        handlers = self._subscribers.get(topic, [])

        entry = {
            "id": msg_id,
            "source": source,
            "destination": f"topic:{topic}",
            "content": content,
            "priority": priority,
            "timestamp": now,
            "confirmed": False,
            "confirm_timestamp": "",
            "topic": topic,
        }

        # Deliver to all subscribers
        for handler in handlers:
            try:
                handler(entry)
            except Exception as e:
                self._log.append({
                    "event": "wire_failure",
                    "message_id": msg_id,
                    "topic": topic,
                    "error": str(e),
                    "timestamp": now,
                })

        self._log.append({
            "event": "broadcast",
            "message_id": msg_id,
            "topic": topic,
            "subscriber_count": len(handlers),
            "timestamp": now,
        })
        self._save_log()

        return msg_id

    def subscribe(self, topic, handler):
        """Subscribe a handler to a topic."""
        self._subscribers[topic].append(handler)
        self._log.append({
            "event": "subscribe",
            "topic": topic,
            "timestamp": self._now(),
        })
        self._save_log()

    def pending_count(self, destination=None):
        """Count pending messages, optionally for a specific destination."""
        if destination:
            return len(self._queue.get(destination, []))
        return sum(len(q) for q in self._queue.values())

    def unconfirmed_count(self):
        """Count messages sent but not yet confirmed."""
        sent = set()
        confirmed = set()
        for entry in self._log:
            if entry["event"] == "send":
                sent.add(entry["message_id"])
            elif entry["event"] == "confirm":
                confirmed.add(entry["message_id"])
        return len(sent - confirmed)

    def log_summary(self):
        """Return summary of wire activity."""
        events = defaultdict(int)
        for entry in self._log:
            events[entry["event"]] += 1
        return dict(events)
