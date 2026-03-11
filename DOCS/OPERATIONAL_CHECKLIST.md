# KALAXI Operational Checklist — What to Run First

Exact order of operations to convert design into trustworthy institution.

## Phase 1: Cryptographic Foundation (do first)

1. Generate steward keypairs (one per steward, minimum 3):
   ```
   python TOOLS/ed25519_sign.py gen --out-dir keys/steward1
   python TOOLS/ed25519_sign.py gen --out-dir keys/steward2
   python TOOLS/ed25519_sign.py gen --out-dir keys/steward3
   ```

2. Securely distribute private keys (HSM, Signal, or in-person). Never email. Never commit to git.

3. Record public keys in MANIFEST/steward_keys.json (public keys only).

## Phase 2: Canonicalize + Sign (establishes trust baseline)

4. Run canonicalization scan:
   ```
   python WEAVER/canonicalize.py
   ```
   Inspect MANIFEST/canonical_manifest.json and MANIFEST/duplicate_id_report.json.

5. Steward 1 signs:
   ```
   python TOOLS/ed25519_sign.py sign \
     --key keys/steward1/private.hex \
     --in MANIFEST/canonical_manifest_bundle.json \
     --out MANIFEST/signed_s1.json
   ```

6. Steward 2 co-signs:
   ```
   python TOOLS/ed25519_sign.py add \
     --key keys/steward2/private.hex \
     --in MANIFEST/signed_s1.json \
     --out MANIFEST/signed_2s.json
   ```

7. Verify multi-sig:
   ```
   python TOOLS/ed25519_sign.py verify --in MANIFEST/signed_2s.json
   python TOOLS/ed25519_sign.py multisig-check --in MANIFEST/signed_2s.json --threshold 2
   ```

8. Archive signed manifest in canonical store. Publish manifest hash to status page.

## Phase 3: Staging Intake (opens the small door)

9. Deploy intake in simulation mode (see DOCS/STAGING_DEPLOY_CHECKLIST.md).

10. Run 3 steward test ingests — verify observations flow through SAY, KEEP, dignity_check.

11. Run early-warning pipeline on synthetic data:
    ```
    python WEAVER/early_warning.py
    ```
    Confirm EWMA/CUSUM detectors fire on simulated decline trajectories.

## Phase 4: Calibrate Detectors

12. Optional parameter sweep for EWMA alpha/threshold choices:
    - Adjust alpha (0.1-0.3) and threshold (1.5-3.0) based on false positive rate
    - Target: actionable-alert rate > 80%, false positive rate < 20%

13. Review alert economics: estimate cost-per-alert (human triage hours per alert).

## Phase 5: Legal + Governance

14. Distribute Emergency Governance Playbook to all stewards (STEWARD/EMERGENCY_GOVERNANCE_PLAYBOOK.md).

15. Legal counsel reviews:
    - Donor consent wording
    - Privacy budget (epsilon) accounting
    - GDPR/FADP compliance for Swiss jurisdiction
    - Data retention and deletion policies

16. Legal counsel provides jurisdictional appendices for the playbook.

## Phase 6: Open the Door

17. When legal sign-off received, set SIMULATION_ONLY=false.

18. Invite first closed cohort (3-30 people, steward-vetted). Co-design the intake UX.

19. Monitor continuously:
    - Intake funnel: invites -> consented -> processed -> triaged
    - Privacy budget ledger: epsilon consumed per query/day
    - Alert economics: alerts/day, triage hours/alert
    - WVPS/GDI per module per cycle

20. First canonical manifest with real donor data: require fresh 2-of-3 multi-sig.

## Decision Points

- Do NOT proceed to Phase 6 without legal sign-off
- Do NOT disable SIMULATION_ONLY without steward council 2-of-3 approval
- Do NOT invite non-steward donors without consent wording approved by legal counsel

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
