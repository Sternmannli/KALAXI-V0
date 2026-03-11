# KALAXI Staging Deploy Checklist

Minimum steps to deploy the intake door in a secure staging environment.

## Prerequisites

- [ ] Python 3.10+ installed
- [ ] `pip install fastapi uvicorn pydantic pynacl python-dotenv`
- [ ] Steward keypairs generated (see step 1)
- [ ] Staging host isolated behind VPN or IP allowlist (steward IPs only)

## Steps

### 1. Generate steward keys

```
python TOOLS/ed25519_sign.py gen --out-dir keys/steward1
python TOOLS/ed25519_sign.py gen --out-dir keys/steward2
python TOOLS/ed25519_sign.py gen --out-dir keys/steward3
```

SECURITY: Never commit `keys/` to git. Add to `.gitignore`. Distribute private keys via secure channel (Signal, in-person, HSM).

### 2. Configure environment

Create `.env` in deployment directory:
```
SIMULATION_ONLY=true
KEEP_STORE_PATH=/var/kalaxi/keep_store.jsonl
STEWARD_KEYS_DIR=/var/kalaxi/keys/
```

### 3. Start intake service (staging)

```
uvicorn WEAVER.intake:app --host 127.0.0.1 --port 8000
```

For production-like setup, front with NGINX reverse proxy enforcing TLS and IP allowlist.

### 4. Run canonicalization on existing manifests

```
python WEAVER/canonicalize.py
```

This scans the codebase, produces `MANIFEST/canonical_manifest.json` and `MANIFEST/duplicate_id_report.json`.

### 5. Sign the canonical manifest

```
python TOOLS/ed25519_sign.py sign \
  --key keys/steward1/private.hex \
  --in MANIFEST/canonical_manifest_bundle.json \
  --out MANIFEST/signed_s1.json

python TOOLS/ed25519_sign.py add \
  --key keys/steward2/private.hex \
  --in MANIFEST/signed_s1.json \
  --out MANIFEST/signed_2s.json

python TOOLS/ed25519_sign.py verify --in MANIFEST/signed_2s.json
```

### 6. Verify end-to-end

- [ ] Intake endpoint responds (POST /intake with 4-question ritual)
- [ ] KEEP store writes append-only JSONL
- [ ] Canonical manifest is signed and verifiable
- [ ] Early warning pipeline runs on synthetic data
- [ ] Emergency playbook distributed to steward emails

### 7. Invite test stewards

Invite 3 trusted stewards. Run end-to-end test cycle:
1. Submit test observations via intake
2. Run canonicalization
3. Sign manifest with multi-sig
4. Verify all signatures pass

## Security Notes

- SIMULATION_ONLY=true until legal sign-off for live donors
- KMS-backed key storage required for production (file-based keys for staging only)
- All KEEP writes must be append-only at application layer
- Privacy budget (epsilon) tracking must be active before any real donor data
- Legal counsel must review consent wording before inviting non-steward donors

## Going Live

When staging is validated and legal review complete:
1. Set SIMULATION_ONLY=false
2. Invite closed cohort (3-30 people, steward-vetted)
3. Monitor early-warning pipeline for false positive rate
4. Track cost-per-alert metric before expanding

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
