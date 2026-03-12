#!/usr/bin/env python3
"""
batch_sign.py — Sign all critical KALAXI artifacts with V-001 + V-002 keys.

Reads each artifact file, wraps it in a JSON manifest with metadata,
signs with V-002 first, then V-001 co-signs. Outputs signed bundles
to MANIFEST/signed/.

Usage:
  python TOOLS/batch_sign.py --v001-key keys/V-001/private.hex --v003-key keys/V-002/private.hex

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "TOOLS"))

from ed25519_sign import _canonical_json

try:
    from nacl.signing import SigningKey
    from nacl.encoding import HexEncoder
except ImportError:
    print("ERROR: pip install pynacl", file=sys.stderr)
    sys.exit(1)


# Critical artifacts to sign (path relative to ROOT, tier, description)
CRITICAL_ARTIFACTS = [
    ("CANON/MASTER_CANON_V1.md", "CONSTITUTIONAL", "Supreme constitution v1.0.0"),
    ("CANON/SEALED_GATE_SPEC.md", "CONSTITUTIONAL", "Three irreducible prohibitions"),
    ("MANIFEST/metadata/tier1_stone.md", "CONSTITUTIONAL", "Tier 1 foundation — covenants, governance rules"),
    ("MANIFEST/metadata/tier2_weaver.md", "OPERATIONAL", "Tier 2 — 9 modules, protocols, sealed gate"),
    ("MANIFEST/ratification_log.md", "GOVERNANCE", "Append-only ratification record"),
    ("MANIFEST/ids.json", "GOVERNANCE", "Master ID registry"),
    ("MANIFEST/escalation_log.json", "GOVERNANCE", "Incident and escalation log"),
    ("STEWARD/EMERGENCY_GOVERNANCE_PLAYBOOK.md", "GOVERNANCE", "Emergency governance protocol"),
    ("MANIFEST/metadata/tier3_honey.md", "REGISTRY", "Tier 3 — wisdom, anomalies, proverbs"),
    ("MANIFEST/metadata/tier4_hand.md", "REGISTRY", "Tier 4 — interface, ledger, receipts"),
]


def file_hash(path: Path) -> str:
    """SHA-256 of file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(rel_path: str, tier: str, description: str) -> dict:
    """Build a signable manifest for a file."""
    full_path = ROOT / rel_path
    if not full_path.exists():
        return None

    content_hash = file_hash(full_path)
    return {
        "artifact_id": rel_path,
        "tier": tier,
        "description": description,
        "content_hash_sha256": content_hash,
        "file_size_bytes": full_path.stat().st_size,
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "system": "KALAXI-V0",
        "protocol": "EFP-Ed25519",
    }


def sign_with_key(manifest: dict, sk: SigningKey) -> dict:
    """Sign a manifest and return signature entry."""
    manifest_bytes = _canonical_json(manifest)
    sig = sk.sign(manifest_bytes).signature.hex()
    pub = sk.verify_key.encode(encoder=HexEncoder).decode()
    return {
        "public_key": pub,
        "signature": sig,
        "algorithm": "Ed25519",
    }


def main():
    parser = argparse.ArgumentParser(description="Batch-sign critical KALAXI artifacts")
    parser.add_argument("--v001-key", required=True, help="Path to V-001 private.hex")
    parser.add_argument("--v003-key", required=True, help="Path to V-002 private.hex")
    args = parser.parse_args()

    sk_v001 = SigningKey(Path(args.v001_key).read_text().strip(), encoder=HexEncoder)
    sk_v003 = SigningKey(Path(args.v003_key).read_text().strip(), encoder=HexEncoder)

    pub_v001 = sk_v001.verify_key.encode(encoder=HexEncoder).decode()
    pub_v003 = sk_v003.verify_key.encode(encoder=HexEncoder).decode()

    out_dir = ROOT / "MANIFEST" / "signed"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Also build a registry of public keys
    key_registry = {
        "V-001": {"public_key": pub_v001, "role": "steward-owner", "name": "Mohamed Farag"},
        "V-002": {"public_key": pub_v003, "role": "steward-system", "name": "Claude (V-002)"},
    }
    (out_dir / "steward_keys.json").write_text(json.dumps(key_registry, indent=2))

    results = []
    for rel_path, tier, desc in CRITICAL_ARTIFACTS:
        manifest = build_manifest(rel_path, tier, desc)
        if manifest is None:
            print(f"  SKIP (not found): {rel_path}")
            continue

        # Sign with both keys
        sig_v003 = sign_with_key(manifest, sk_v003)
        sig_v003["signer_id"] = "V-002"
        sig_v003["signer_role"] = "steward-system"

        sig_v001 = sign_with_key(manifest, sk_v001)
        sig_v001["signer_id"] = "V-001"
        sig_v001["signer_role"] = "steward-owner"

        bundle = {
            "manifest": manifest,
            "signatures": [sig_v001, sig_v003],
        }

        # Write signed bundle
        safe_name = rel_path.replace("/", "_").replace(".", "_") + ".signed.json"
        bundle_path = out_dir / safe_name
        bundle_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False))

        results.append({
            "artifact": rel_path,
            "tier": tier,
            "content_hash": manifest["content_hash_sha256"][:16] + "...",
            "signers": ["V-001", "V-002"],
            "bundle": str(bundle_path.relative_to(ROOT)),
        })

        print(f"  SIGNED: {rel_path} [{tier}] => {safe_name}")

    # Write summary
    summary = {
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "total_artifacts": len(results),
        "signers": key_registry,
        "artifacts": results,
    }
    summary_path = out_dir / "SIGNING_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n  Summary: {summary_path}")
    print(f"  Total signed: {len(results)} artifacts")
    print(f"  V-001 public key: {pub_v001}")
    print(f"  V-002 public key: {pub_v003}")


if __name__ == "__main__":
    main()
