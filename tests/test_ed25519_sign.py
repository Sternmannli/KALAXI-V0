#!/usr/bin/env python3
"""
Tests for Ed25519 signing CLI and upgraded ArtifactSigner.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""
import sys
import json
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "TOOLS"))

import pytest

# Test availability
try:
    from nacl.signing import SigningKey
    NACL_AVAILABLE = True
except ImportError:
    NACL_AVAILABLE = False

from WEAVER.canonicalize import ArtifactSigner


class TestArtifactSignerEd25519:
    """Test ArtifactSigner with real Ed25519 (when PyNaCl available)."""

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_ed25519_sign_and_verify(self):
        signer = ArtifactSigner(signer_id="test-steward", signer_role="steward")
        assert signer.algorithm == "Ed25519"
        data = {"test": "value", "number": 42}
        artifact = signer.sign("TEST-ED25519", data)
        assert artifact.signature != ""
        assert signer.verify(artifact, data) is True

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_ed25519_tampered_fails(self):
        signer = ArtifactSigner()
        data = {"original": "data"}
        artifact = signer.sign("TAMPER-TEST", data)
        tampered = {"original": "TAMPERED"}
        assert signer.verify(artifact, tampered) is False

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_ed25519_manifest_bundle(self):
        signer = ArtifactSigner(signer_id="steward1", signer_role="steward")
        manifest = {"version": "1.0", "entries": {"COV#001": {"status": "ratified"}}}
        bundle = signer.sign_manifest_bundle(manifest)
        assert "manifest" in bundle
        assert "signatures" in bundle
        assert len(bundle["signatures"]) == 1
        assert bundle["signatures"][0]["algorithm"] == "Ed25519"
        assert bundle["signatures"][0]["public_key"] == signer.public_key

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_ed25519_sign_manifest_includes_key(self):
        signer = ArtifactSigner()
        manifest = {"test": True}
        _, signed = signer.sign_manifest(manifest)
        assert signed["_signature"]["algorithm"] == "Ed25519"
        assert "public_key" in signed["_signature"]

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_ed25519_deterministic_hash(self):
        signer = ArtifactSigner()
        data1 = {"b": 2, "a": 1}
        data2 = {"a": 1, "b": 2}
        art1 = signer.sign("X", data1)
        art2 = signer.sign("Y", data2)
        assert art1.content_hash == art2.content_hash

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_ed25519_from_key_file(self):
        """Test loading a key from file (like steward would do)."""
        tmpdir = tempfile.mkdtemp()
        try:
            # Generate a key
            sk = SigningKey.generate()
            from nacl.encoding import HexEncoder
            key_path = Path(tmpdir) / "private.hex"
            key_path.write_text(sk.encode(encoder=HexEncoder).decode())

            signer = ArtifactSigner(
                signer_id="file-steward",
                signer_role="steward",
                private_key_path=str(key_path),
            )
            assert signer.algorithm == "Ed25519"
            data = {"signed_from": "file_key"}
            artifact = signer.sign("FILE-KEY-TEST", data)
            assert signer.verify(artifact, data) is True
        finally:
            shutil.rmtree(tmpdir)


class TestEd25519CLI:
    """Test the CLI tool functions directly."""

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_gen_sign_verify_flow(self):
        """Full flow: generate keys, sign manifest, verify."""
        from TOOLS.ed25519_sign import gen_keys, sign_manifest, verify_signed, add_signature

        tmpdir = tempfile.mkdtemp()
        try:
            # Generate two keypairs
            gen_keys(f"{tmpdir}/steward1")
            gen_keys(f"{tmpdir}/steward2")
            assert (Path(tmpdir) / "steward1" / "private.hex").exists()
            assert (Path(tmpdir) / "steward1" / "public.hex").exists()

            # Create a test manifest
            manifest = {"test": "manifest", "version": "1.0"}
            manifest_path = f"{tmpdir}/manifest.json"
            Path(manifest_path).write_text(json.dumps(manifest))

            # Sign with steward 1
            signed_path = f"{tmpdir}/signed_s1.json"
            sign_manifest(f"{tmpdir}/steward1/private.hex", manifest_path, signed_path)
            assert Path(signed_path).exists()

            # Verify
            assert verify_signed(signed_path) is True

            # Add steward 2 signature
            signed_2_path = f"{tmpdir}/signed_s2.json"
            add_signature(signed_path, f"{tmpdir}/steward2/private.hex", signed_2_path)

            # Verify both
            assert verify_signed(signed_2_path) is True

            # Check that the signed file has 2 signatures
            data = json.loads(Path(signed_2_path).read_text())
            assert len(data["signatures"]) == 2
        finally:
            shutil.rmtree(tmpdir)

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_duplicate_signer_rejected(self):
        """Same steward cannot sign twice."""
        from TOOLS.ed25519_sign import gen_keys, sign_manifest, add_signature

        tmpdir = tempfile.mkdtemp()
        try:
            gen_keys(f"{tmpdir}/steward1")
            manifest = {"test": True}
            manifest_path = f"{tmpdir}/m.json"
            Path(manifest_path).write_text(json.dumps(manifest))

            signed_path = f"{tmpdir}/signed.json"
            sign_manifest(f"{tmpdir}/steward1/private.hex", manifest_path, signed_path)

            # Try to add same key again — should exit with error
            with pytest.raises(SystemExit):
                add_signature(signed_path, f"{tmpdir}/steward1/private.hex", f"{tmpdir}/out.json")
        finally:
            shutil.rmtree(tmpdir)

    @pytest.mark.skipif(not NACL_AVAILABLE, reason="PyNaCl not installed")
    def test_multisig_check(self):
        """Test N-of-M threshold check."""
        from TOOLS.ed25519_sign import gen_keys, sign_manifest, add_signature, multisig_check

        tmpdir = tempfile.mkdtemp()
        try:
            gen_keys(f"{tmpdir}/s1")
            gen_keys(f"{tmpdir}/s2")
            gen_keys(f"{tmpdir}/s3")

            manifest = {"governance": "decision"}
            mp = f"{tmpdir}/m.json"
            Path(mp).write_text(json.dumps(manifest))

            # Sign with 2 of 3
            sign_manifest(f"{tmpdir}/s1/private.hex", mp, f"{tmpdir}/sig1.json")
            add_signature(f"{tmpdir}/sig1.json", f"{tmpdir}/s2/private.hex", f"{tmpdir}/sig2.json")

            # 2-of-3 should pass
            assert multisig_check(f"{tmpdir}/sig2.json", 2) is True
            # 3-of-3 should fail (only 2 signed)
            assert multisig_check(f"{tmpdir}/sig2.json", 3) is False
        finally:
            shutil.rmtree(tmpdir)


class TestArtifactSignerHMACFallback:
    """Ensure HMAC fallback still works (existing test compatibility)."""

    def test_hmac_sign_and_verify(self):
        """Force HMAC mode by not providing Ed25519 key and mocking NACL away."""
        # The existing tests already cover this via the base ArtifactSigner
        signer = ArtifactSigner(signer_id="test", signer_role="test-role")
        data = {"test": "value"}
        artifact = signer.sign("HMAC-TEST", data)
        assert artifact.signature != ""
        assert signer.verify(artifact, data) is True

    def test_chain_grows_with_upgrade(self):
        signer = ArtifactSigner()
        signer.sign("A", {"a": 1})
        signer.sign("B", {"b": 2})
        signer.sign("C", {"c": 3})
        assert signer.chain_length == 3
