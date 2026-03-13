#!/usr/bin/env python3
"""
ratification.py — KALAXI Ratification Engine
Version: 1.0
Grounded in: tier1_stone.md (Element Lifecycle), COV#NEW-E (Canon Integrity),
             COV#NEW-F (Amendment Protocol), ratification_log.md

Three-state lifecycle: COMMITTED → PROVISIONAL → RATIFIED
Integrated with ArtifactSigner for cryptographic signing at ratification.

The ratification engine enforces:
  - Thermal delays (7 days seeds, 90 days covenants, 1000 days centre-shift)
  - Required sign-offs (steward, ethics reviewer)
  - Append-only ratification log
  - Cryptographic signatures on ratified elements
  - Pre-Launch Exception (no thermal delay before first donor)

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from enum import Enum

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.canonicalize import ArtifactSigner, SignedArtifact


# ═══════════════════════════════════════════════════
# ELEMENT LIFECYCLE
# ═══════════════════════════════════════════════════

class ElementState(Enum):
    """Three states. No element may carry two states simultaneously."""
    COMMITTED = "committed"
    PROVISIONAL = "provisional"
    RATIFIED = "ratified"


class ElementType(Enum):
    """Element types with their thermal delay and sign-off requirements."""
    COVENANT = "covenant"
    STRUCTURAL = "structural"
    PROVERB = "proverb"
    ANOMALY = "anomaly"
    SEED = "seed"
    AXIOM = "axiom"
    TREASURE = "treasure"
    DEFINITION = "definition"
    OATH = "oath"
    GO_SIGNAL = "go_signal"
    PATCH = "patch"
    CENTRE_SHIFT = "centre_shift"


# Thermal delay requirements (days) per element type
THERMAL_DELAYS = {
    ElementType.COVENANT: 90,
    ElementType.STRUCTURAL: 90,
    ElementType.PROVERB: 7,
    ElementType.ANOMALY: 7,
    ElementType.SEED: 7,
    ElementType.AXIOM: 90,
    ElementType.TREASURE: 7,
    ElementType.DEFINITION: 7,
    ElementType.OATH: 90,
    ElementType.GO_SIGNAL: 0,
    ElementType.PATCH: 0,
    ElementType.CENTRE_SHIFT: 1000,
}

# Sign-off requirements per element type
SIGNOFF_REQUIREMENTS = {
    ElementType.COVENANT: ["canonical_owner", "ethics_reviewer"],
    ElementType.STRUCTURAL: ["canonical_owner", "ethics_reviewer"],
    ElementType.PROVERB: ["steward"],
    ElementType.ANOMALY: ["steward"],
    ElementType.SEED: ["steward"],
    ElementType.AXIOM: ["canonical_owner", "ethics_reviewer"],
    ElementType.TREASURE: ["steward"],
    ElementType.DEFINITION: ["steward"],
    ElementType.OATH: ["canonical_owner", "ethics_reviewer"],
    ElementType.GO_SIGNAL: ["steward"],
    ElementType.PATCH: ["steward"],
    ElementType.CENTRE_SHIFT: ["canonical_owner", "ethics_reviewer", "senior_moderator_1", "senior_moderator_2"],
}


@dataclass
class SignOff:
    """A single sign-off on an element."""
    role: str               # "steward", "canonical_owner", "ethics_reviewer", etc.
    signer_id: str          # "V-001", "V-002"
    signer_name: str        # "Mohamed Farag", "Claude"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""


@dataclass
class RatificationElement:
    """A canonical element tracked through the lifecycle."""
    element_id: str                     # COV#001, P#2135, etc.
    element_type: ElementType
    name: str                           # Human-readable name
    description: str                    # What this element is
    state: ElementState = ElementState.COMMITTED
    source: str = ""                    # Source file or origin
    committed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provisional_at: Optional[str] = None
    ratified_at: Optional[str] = None
    thermal_delay_days: int = 0         # Computed from element type
    thermal_delay_expires: Optional[str] = None
    sign_offs: List[SignOff] = field(default_factory=list)
    sign_offs_required: List[str] = field(default_factory=list)
    signature: Optional[str] = None     # Cryptographic signature at ratification
    content_hash: Optional[str] = None  # SHA-256 of element content at ratification
    superseded_by: Optional[str] = None # If superseded (COV#NEW-F)
    pre_launch_exception: bool = False  # Ratified under pre-launch exception
    conditions: str = ""                # Any conditions on ratification
    changelog: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "element_id": self.element_id,
            "element_type": self.element_type.value,
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "source": self.source,
            "committed_at": self.committed_at,
            "provisional_at": self.provisional_at,
            "ratified_at": self.ratified_at,
            "thermal_delay_days": self.thermal_delay_days,
            "thermal_delay_expires": self.thermal_delay_expires,
            "sign_offs": [
                {"role": s.role, "signer_id": s.signer_id,
                 "signer_name": s.signer_name, "timestamp": s.timestamp, "notes": s.notes}
                for s in self.sign_offs
            ],
            "sign_offs_required": self.sign_offs_required,
            "signature": self.signature,
            "content_hash": self.content_hash,
            "superseded_by": self.superseded_by,
            "pre_launch_exception": self.pre_launch_exception,
            "conditions": self.conditions,
            "changelog": self.changelog,
        }


# ═══════════════════════════════════════════════════
# RATIFICATION ENGINE
# ═══════════════════════════════════════════════════

class RatificationError(Exception):
    """Raised when a ratification operation violates protocol."""
    pass


class RatificationEngine:
    """
    Manages the full element lifecycle: COMMITTED → PROVISIONAL → RATIFIED.

    Enforces:
      - Thermal delays per element type
      - Required sign-offs
      - No simultaneous states
      - Append-only changelog
      - Cryptographic signing at ratification
      - Pre-Launch Exception bypass

    Usage:
        engine = RatificationEngine()
        elem = engine.commit("COV#016", ElementType.COVENANT, "NEW COVENANT", "Description")
        engine.offer_to_threshold(elem.element_id)
        engine.sign_off(elem.element_id, "canonical_owner", "V-001", "Mohamed Farag")
        engine.sign_off(elem.element_id, "ethics_reviewer", "V-002", "Claude")
        result = engine.ratify(elem.element_id)
    """

    def __init__(self, signer: Optional[ArtifactSigner] = None,
                 pre_launch: bool = True, persist_path: Optional[Path] = None):
        self._elements: Dict[str, RatificationElement] = {}
        self._signer = signer or ArtifactSigner(signer_id="V-002", signer_role="steward-system")
        self._pre_launch = pre_launch  # Pre-launch exception active
        self._persist_path = persist_path or (ROOT / "MANIFEST" / "ratification_registry.json")
        self._log_path = ROOT / "MANIFEST" / "ratification_log.md"
        self._changelog: List[dict] = []

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    # ─── COMMIT ───

    def commit(self, element_id: str, element_type: ElementType,
               name: str, description: str, source: str = "") -> RatificationElement:
        """
        Register a new element as COMMITTED.
        Committed = technically present, not yet offered to Threshold.
        """
        if element_id in self._elements:
            raise RatificationError(f"{element_id} already registered.")

        thermal_days = THERMAL_DELAYS[element_type]
        required_signoffs = list(SIGNOFF_REQUIREMENTS[element_type])

        elem = RatificationElement(
            element_id=element_id,
            element_type=element_type,
            name=name,
            description=description,
            state=ElementState.COMMITTED,
            source=source,
            thermal_delay_days=thermal_days,
            sign_offs_required=required_signoffs,
        )
        elem.changelog.append(f"{self._now()} COMMITTED by V-002")

        self._elements[element_id] = elem
        self._log_change("commit", element_id, f"Registered as COMMITTED ({element_type.value})")
        return elem

    # ─── OFFER TO THRESHOLD (COMMITTED → PROVISIONAL) ───

    def offer_to_threshold(self, element_id: str) -> RatificationElement:
        """
        Move element from COMMITTED to PROVISIONAL.
        Starts the thermal delay clock.
        """
        elem = self._get(element_id)

        if elem.state != ElementState.COMMITTED:
            raise RatificationError(
                f"{element_id} is {elem.state.value}, not COMMITTED. "
                f"Only COMMITTED elements can be offered to Threshold."
            )

        elem.state = ElementState.PROVISIONAL
        elem.provisional_at = self._now()

        # Compute thermal delay expiry
        if self._pre_launch or elem.thermal_delay_days == 0:
            elem.thermal_delay_expires = elem.provisional_at  # Immediate
        else:
            offered = datetime.fromisoformat(elem.provisional_at)
            expires = offered + timedelta(days=elem.thermal_delay_days)
            elem.thermal_delay_expires = expires.isoformat()

        elem.changelog.append(
            f"{self._now()} PROVISIONAL — offered to Threshold"
            f" (thermal delay: {'waived (pre-launch)' if self._pre_launch else f'{elem.thermal_delay_days} days'})"
        )

        self._log_change("offer", element_id, f"COMMITTED → PROVISIONAL")
        return elem

    # ─── SIGN-OFF ───

    def sign_off(self, element_id: str, role: str, signer_id: str,
                 signer_name: str, notes: str = "") -> RatificationElement:
        """
        Record a sign-off on a PROVISIONAL element.
        Only required roles are accepted.
        """
        elem = self._get(element_id)

        if elem.state != ElementState.PROVISIONAL:
            raise RatificationError(
                f"{element_id} is {elem.state.value}. Sign-offs only accepted on PROVISIONAL elements."
            )

        if role not in elem.sign_offs_required:
            raise RatificationError(
                f"Role '{role}' is not required for {element_id}. "
                f"Required: {elem.sign_offs_required}"
            )

        # Check for duplicate sign-off
        existing = [s for s in elem.sign_offs if s.role == role]
        if existing:
            raise RatificationError(
                f"Role '{role}' already signed off on {element_id} "
                f"by {existing[0].signer_id} at {existing[0].timestamp}."
            )

        sign_off = SignOff(
            role=role,
            signer_id=signer_id,
            signer_name=signer_name,
            notes=notes,
        )
        elem.sign_offs.append(sign_off)
        elem.changelog.append(f"{self._now()} SIGN-OFF: {role} by {signer_id} ({signer_name})")

        self._log_change("sign_off", element_id, f"{role} signed by {signer_id}")
        return elem

    # ─── RATIFY (PROVISIONAL → RATIFIED) ───

    def ratify(self, element_id: str, pre_launch_exception: bool = False,
               conditions: str = "") -> Tuple[RatificationElement, SignedArtifact]:
        """
        Ratify a PROVISIONAL element. Checks:
          1. Element is PROVISIONAL
          2. Thermal delay has expired (or pre-launch exception)
          3. All required sign-offs present
          4. Signs the element cryptographically

        Returns the element and its cryptographic signature.
        """
        elem = self._get(element_id)

        if elem.state != ElementState.PROVISIONAL:
            raise RatificationError(
                f"{element_id} is {elem.state.value}, not PROVISIONAL."
            )

        # Check thermal delay
        use_exception = pre_launch_exception or self._pre_launch
        if not use_exception:
            now = datetime.now(timezone.utc)
            expires = datetime.fromisoformat(elem.thermal_delay_expires)
            if now < expires:
                remaining = (expires - now).days
                raise RatificationError(
                    f"{element_id} thermal delay not expired. "
                    f"{remaining} days remaining (expires {elem.thermal_delay_expires[:10]})."
                )

        # Check sign-offs
        signed_roles = {s.role for s in elem.sign_offs}
        missing = set(elem.sign_offs_required) - signed_roles
        if missing:
            raise RatificationError(
                f"{element_id} missing sign-offs: {', '.join(missing)}"
            )

        # Ratify
        elem.state = ElementState.RATIFIED
        elem.ratified_at = self._now()
        elem.pre_launch_exception = use_exception
        elem.conditions = conditions

        # Cryptographic signature
        artifact_data = {
            "element_id": elem.element_id,
            "element_type": elem.element_type.value,
            "name": elem.name,
            "ratified_at": elem.ratified_at,
            "sign_offs": [
                {"role": s.role, "signer_id": s.signer_id, "timestamp": s.timestamp}
                for s in elem.sign_offs
            ],
        }
        signed = self._signer.sign(f"RATIFY-{element_id}", artifact_data)
        elem.signature = signed.signature
        elem.content_hash = signed.content_hash

        elem.changelog.append(
            f"{self._now()} RATIFIED"
            f" {'(Pre-Launch Exception)' if use_exception else ''}"
            f" — signature: {signed.signature[:16]}..."
        )

        self._log_change("ratify", element_id,
                         f"PROVISIONAL → RATIFIED (sig: {signed.signature[:16]}...)")
        return elem, signed

    # ─── SUPERSEDE (COV#NEW-F) ───

    def supersede(self, old_id: str, new_id: str) -> RatificationElement:
        """
        Supersede an element. No deletion — only supersession via new ID.
        The old element is marked superseded but never removed.
        """
        old = self._get(old_id)
        if old_id == new_id:
            raise RatificationError("Cannot supersede an element with itself.")
        if new_id not in self._elements:
            raise RatificationError(f"{new_id} not registered. Register it first.")

        old.superseded_by = new_id
        old.changelog.append(f"{self._now()} SUPERSEDED by {new_id}")

        self._log_change("supersede", old_id, f"Superseded by {new_id}")
        return old

    # ─── QUERIES ───

    def get(self, element_id: str) -> Optional[RatificationElement]:
        return self._elements.get(element_id)

    def _get(self, element_id: str) -> RatificationElement:
        elem = self._elements.get(element_id)
        if elem is None:
            raise RatificationError(f"{element_id} not found in registry.")
        return elem

    def committed(self) -> List[RatificationElement]:
        return [e for e in self._elements.values() if e.state == ElementState.COMMITTED]

    def provisional(self) -> List[RatificationElement]:
        return [e for e in self._elements.values() if e.state == ElementState.PROVISIONAL]

    def ratified(self) -> List[RatificationElement]:
        return [e for e in self._elements.values() if e.state == ElementState.RATIFIED]

    def awaiting_signoff(self) -> List[RatificationElement]:
        """Elements that are provisional and missing sign-offs."""
        result = []
        for elem in self.provisional():
            signed_roles = {s.role for s in elem.sign_offs}
            missing = set(elem.sign_offs_required) - signed_roles
            if missing:
                result.append(elem)
        return result

    def thermal_delay_expired(self) -> List[RatificationElement]:
        """Provisional elements whose thermal delay has passed."""
        now = datetime.now(timezone.utc)
        result = []
        for elem in self.provisional():
            if elem.thermal_delay_expires:
                expires = datetime.fromisoformat(elem.thermal_delay_expires)
                if now >= expires:
                    result.append(elem)
        return result

    def ready_to_ratify(self) -> List[RatificationElement]:
        """Elements that have all sign-offs AND thermal delay expired."""
        now = datetime.now(timezone.utc)
        result = []
        for elem in self.provisional():
            # Check sign-offs
            signed_roles = {s.role for s in elem.sign_offs}
            missing = set(elem.sign_offs_required) - signed_roles
            if missing:
                continue
            # Check thermal delay
            if self._pre_launch or not elem.thermal_delay_expires:
                result.append(elem)
            else:
                expires = datetime.fromisoformat(elem.thermal_delay_expires)
                if now >= expires:
                    result.append(elem)
        return result

    def verify(self, element_id: str) -> bool:
        """Verify the cryptographic signature on a ratified element."""
        elem = self._get(element_id)
        if elem.state != ElementState.RATIFIED or not elem.signature:
            return False

        artifact_data = {
            "element_id": elem.element_id,
            "element_type": elem.element_type.value,
            "name": elem.name,
            "ratified_at": elem.ratified_at,
            "sign_offs": [
                {"role": s.role, "signer_id": s.signer_id, "timestamp": s.timestamp}
                for s in elem.sign_offs
            ],
        }
        signed = SignedArtifact(
            artifact_id=f"RATIFY-{element_id}",
            content_hash=elem.content_hash,
            signature=elem.signature,
            signer_id=self._signer._signer_id,
            signer_role=self._signer._signer_role,
            timestamp=elem.ratified_at,
            verification_status="unverified",
        )
        return self._signer.verify(signed, artifact_data)

    # ─── FAST PATH: commit + offer + sign + ratify in one call ───

    def ratify_immediate(self, element_id: str, element_type: ElementType,
                         name: str, description: str, source: str = "",
                         signer_id: str = "V-001", signer_name: str = "Mohamed Farag",
                         conditions: str = "") -> Tuple[RatificationElement, SignedArtifact]:
        """
        Fast path for pre-launch: commit, offer, sign, ratify in one call.
        Only valid when pre_launch=True.
        """
        if not self._pre_launch:
            raise RatificationError("ratify_immediate only valid during pre-launch phase.")

        elem = self.commit(element_id, element_type, name, description, source)
        self.offer_to_threshold(element_id)

        # Sign off all required roles
        for role in elem.sign_offs_required:
            if role in ("canonical_owner", "steward"):
                self.sign_off(element_id, role, signer_id, signer_name)
            elif role == "ethics_reviewer":
                self.sign_off(element_id, role, "V-002", "Claude (Pre-Launch Exception)")
            else:
                self.sign_off(element_id, role, signer_id, signer_name)

        return self.ratify(element_id, pre_launch_exception=True, conditions=conditions)

    # ─── SUMMARY ───

    def summary(self) -> dict:
        """Summary of the ratification registry."""
        return {
            "total_elements": len(self._elements),
            "committed": len(self.committed()),
            "provisional": len(self.provisional()),
            "ratified": len(self.ratified()),
            "awaiting_signoff": len(self.awaiting_signoff()),
            "ready_to_ratify": len(self.ready_to_ratify()),
            "pre_launch_active": self._pre_launch,
            "signer_algorithm": self._signer.algorithm,
        }

    # ─── PERSISTENCE ───

    def save(self) -> Path:
        """Save the registry to disk."""
        self._persist_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "generated": self._now(),
            "pre_launch": self._pre_launch,
            "elements": {eid: e.to_dict() for eid, e in self._elements.items()},
            "changelog": self._changelog,
        }
        with open(self._persist_path, "w") as f:
            json.dump(data, f, indent=2)
        return self._persist_path

    def load(self) -> int:
        """Load the registry from disk. Returns number of elements loaded."""
        if not self._persist_path.exists():
            return 0

        with open(self._persist_path) as f:
            data = json.load(f)

        self._pre_launch = data.get("pre_launch", True)
        self._changelog = data.get("changelog", [])

        for eid, edata in data.get("elements", {}).items():
            elem = RatificationElement(
                element_id=edata["element_id"],
                element_type=ElementType(edata["element_type"]),
                name=edata["name"],
                description=edata["description"],
                state=ElementState(edata["state"]),
                source=edata.get("source", ""),
                committed_at=edata.get("committed_at", ""),
                provisional_at=edata.get("provisional_at"),
                ratified_at=edata.get("ratified_at"),
                thermal_delay_days=edata.get("thermal_delay_days", 0),
                thermal_delay_expires=edata.get("thermal_delay_expires"),
                sign_offs=[
                    SignOff(role=s["role"], signer_id=s["signer_id"],
                            signer_name=s["signer_name"], timestamp=s["timestamp"],
                            notes=s.get("notes", ""))
                    for s in edata.get("sign_offs", [])
                ],
                sign_offs_required=edata.get("sign_offs_required", []),
                signature=edata.get("signature"),
                content_hash=edata.get("content_hash"),
                superseded_by=edata.get("superseded_by"),
                pre_launch_exception=edata.get("pre_launch_exception", False),
                conditions=edata.get("conditions", ""),
                changelog=edata.get("changelog", []),
            )
            self._elements[eid] = elem

        return len(self._elements)

    # ─── INTERNAL ───

    def _log_change(self, action: str, element_id: str, detail: str):
        self._changelog.append({
            "action": action,
            "element_id": element_id,
            "detail": detail,
            "timestamp": self._now(),
        })

    # ─── APPEND TO RATIFICATION LOG (MARKDOWN) ───

    def append_to_log(self, element_id: str) -> str:
        """
        Append a ratification entry to MANIFEST/ratification_log.md.
        Only works for RATIFIED elements. Returns the entry text.
        """
        elem = self._get(element_id)
        if elem.state != ElementState.RATIFIED:
            raise RatificationError(f"{element_id} is not ratified.")

        sign_off_text = ", ".join(
            f"{s.signer_id} ({s.signer_name})" for s in elem.sign_offs
        )
        thermal_text = (
            "Pre-Launch Exception" if elem.pre_launch_exception
            else f"{elem.thermal_delay_days} days"
        )

        entry = (
            f"| {elem.element_id} | {elem.name} | {elem.ratified_at[:10]} "
            f"| {thermal_text} | {sign_off_text} | {elem.source} |"
        )

        # Append to the log file
        if self._log_path.exists():
            content = self._log_path.read_text()
            # Find the right section to append to based on element type
            section_map = {
                ElementType.COVENANT: "### Covenants",
                ElementType.PROVERB: "### Proverbs",
                ElementType.STRUCTURAL: "### Structural Proposals",
                ElementType.AXIOM: "### Axioms",
                ElementType.TREASURE: "### Treasures",
                ElementType.DEFINITION: "### Definitions",
                ElementType.GO_SIGNAL: "### GO Signals",
                ElementType.OATH: "### Oaths",
            }
            section = section_map.get(elem.element_type, "### Other")

            # Append entry before "## Provisional Elements" section
            marker = "## Provisional Elements"
            if marker in content:
                content = content.replace(
                    marker,
                    f"{entry}\n\n{marker}",
                )
            else:
                content += f"\n{entry}\n"

            self._log_path.write_text(content)

        return entry

    # ─── BOOTSTRAP: Load existing ratifications from log ───

    def bootstrap_from_log(self) -> int:
        """
        Bootstrap the engine by registering all elements already in
        ratification_log.md as RATIFIED. Returns count of elements loaded.
        """
        if not self._log_path.exists():
            return 0

        content = self._log_path.read_text()
        count = 0

        # Parse table rows: | ID | Name | Date | Delay | SignOff | Source |
        import re
        row_pattern = re.compile(
            r'\|\s*(COV#[^\|]+|P#[^\|]+|DEF#[^\|]+|STRUCT#[^\|]+|'
            r'AXIOM#[^\|]+|T#[^\|]+|GO#[^\|]+|OATH::[^\|]+)\s*\|'
            r'\s*([^\|]*)\s*\|'
            r'\s*([^\|]*)\s*\|'
            r'\s*([^\|]*)\s*\|'
            r'\s*([^\|]*)\s*\|'
            r'\s*([^\|]*)\s*\|'
        )

        for match in row_pattern.finditer(content):
            eid = match.group(1).strip()
            name = match.group(2).strip()
            date = match.group(3).strip()
            delay = match.group(4).strip()
            signoff = match.group(5).strip()
            source = match.group(6).strip()

            if eid in self._elements:
                continue

            # Determine element type from ID prefix
            etype = self._type_from_id(eid)

            elem = RatificationElement(
                element_id=eid,
                element_type=etype,
                name=name,
                description=source,
                state=ElementState.RATIFIED,
                source=source,
                committed_at=date,
                provisional_at=date,
                ratified_at=date,
                thermal_delay_days=THERMAL_DELAYS.get(etype, 0),
                sign_offs_required=SIGNOFF_REQUIREMENTS.get(etype, ["steward"]),
                pre_launch_exception="Pre-Launch" in delay or "Pre-constitutional" in delay,
            )

            # Parse sign-off
            if "V-001" in signoff:
                elem.sign_offs.append(SignOff(
                    role="canonical_owner",
                    signer_id="V-001",
                    signer_name="Mohamed Farag",
                    timestamp=date,
                ))

            self._elements[eid] = elem
            count += 1

        return count

    @staticmethod
    def _type_from_id(element_id: str) -> ElementType:
        """Infer element type from its ID prefix."""
        eid = element_id.strip()
        if eid.startswith("COV#"):
            return ElementType.COVENANT
        elif eid.startswith("P#"):
            return ElementType.PROVERB
        elif eid.startswith("STRUCT#"):
            return ElementType.STRUCTURAL
        elif eid.startswith("AXIOM#"):
            return ElementType.AXIOM
        elif eid.startswith("T#"):
            return ElementType.TREASURE
        elif eid.startswith("DEF#"):
            return ElementType.DEFINITION
        elif eid.startswith("GO#"):
            return ElementType.GO_SIGNAL
        elif eid.startswith("OATH"):
            return ElementType.OATH
        else:
            return ElementType.SEED


# ═══════════════════════════════════════════════════
# MODULE API (for Organism integration)
# ═══════════════════════════════════════════════════

_ENGINE: Optional[RatificationEngine] = None

def get_engine(pre_launch: bool = True) -> RatificationEngine:
    """Get or create the singleton ratification engine."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = RatificationEngine(pre_launch=pre_launch)
    return _ENGINE

def ratification_summary() -> dict:
    """Quick summary for health dashboards."""
    return get_engine().summary()

def ratification_commit(element_id: str, element_type: str, name: str,
                        description: str, source: str = "") -> dict:
    """Commit a new element. Returns element dict."""
    etype = ElementType(element_type)
    elem = get_engine().commit(element_id, etype, name, description, source)
    return elem.to_dict()

def ratification_offer(element_id: str) -> dict:
    """Offer element to Threshold."""
    return get_engine().offer_to_threshold(element_id).to_dict()

def ratification_signoff(element_id: str, role: str, signer_id: str,
                         signer_name: str) -> dict:
    """Record a sign-off."""
    return get_engine().sign_off(element_id, role, signer_id, signer_name).to_dict()

def ratification_ratify(element_id: str) -> dict:
    """Ratify an element. Returns element dict."""
    elem, signed = get_engine().ratify(element_id, pre_launch_exception=True)
    return elem.to_dict()

def ratification_verify(element_id: str) -> bool:
    """Verify signature on a ratified element."""
    return get_engine().verify(element_id)
