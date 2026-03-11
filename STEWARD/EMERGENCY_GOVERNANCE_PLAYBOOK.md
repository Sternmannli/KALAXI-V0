# KALAXI Emergency Governance Playbook v1.0

Purpose: immediate, operational steps for incidents involving dignity, privacy, or Mycelium critical alerts.

## Roles

### Steward Council (minimum 3 members)
- Approves emergency actions via 2-of-3 multi-sig (Ed25519)
- Cannot override sealed gate (COV#003)
- Cannot delete KEEP artifacts (COV#010)
- Must provide written rationale for all actions

### Incident Triage Lead
- Coordinates response, opens Incident Record
- First responder — assesses severity, assigns escalation level
- Reports to Steward Council within response window

### Legal Counsel
- Provides jurisdictional guidance (EU AI Act, Swiss FADP, GDPR)
- Reviews data flows, approves federation agreements
- Cannot access individual donor data without steward approval

### Audit Officer
- Independent post-incident reviewer
- Writes signed audit report (Ed25519)
- Advisory — cannot directly modify system

## Triggering Events

- Mycelium RHIZOME alert (critical multi-domain structural signal)
- Any Sealed Gate trigger (forced erasure, cognitive torture, depersonalization)
- Evidence of privacy-budget exhaustion or deanonymization attempt
- Covenant violation detected by CHECK module
- External legal action (subpoena, regulatory inquiry)

## Escalation Levels

### ROUTINE (Level 0)
- Trigger: Normal operational event
- Response: Next review cycle
- Roles: system_v003
- Audit: Not required

### ELEVATED (Level 1)
- Trigger: Dignity drift detected (DECLINING), single-domain concern
- Response: Within 48 hours
- Roles: system_v003, steward
- Audit: Required
- Actions: Monitor, document, assess trajectory

### EMERGENCY (Level 2)
- Trigger: Critical dignity drift, sealed gate proximity, privacy breach
- Response: Immediate (< 4 hours)
- Roles: system_v003, steward, ethics_reviewer
- Audit: Required
- Actions:
  - Pause affected exchanges
  - Generate incident report
  - Notify steward council
  - Switch system to SIMULATION_ONLY if live mode active

### CONSTITUTIONAL (Level 3)
- Trigger: Covenant violation, sealed gate compromise attempt, RHIZOME alert
- Response: Immediate — system halts affected domain
- Roles: system_v003, steward, ethics_reviewer, legal_counsel
- Audit: Required
- Actions:
  - Halt ALL affected exchanges
  - Generate full audit trail
  - Steward + ethics review required before resumption
  - Legal counsel notified if data breach suspected
  - Incident report filed in MANIFEST/escalation_log.json

## Immediate Actions (0-2 hours)

1. Triage lead opens Incident Record (append-only), records initial facts, timestamp, manifest hash
2. If automated federation outputs are enabled, switch to LOCK/Simulation-only mode immediately
3. Steward Council convenes (virtual) and applies 2-of-3 multi-sig to any emergency action
4. Legal Counsel assesses disclosure obligations
5. If donor safety risk exists, enact Shelter: isolate affected artifacts, assign human liaison

## Short-Term (2-72 hours)

- Collect all evidence, preserve logs, preserve privacy budget accounting
- Produce redacted initial report for stakeholders
- Continue triage with hourly updates during critical window

## Post-Incident (within 30 days)

- Audit Officer writes detailed signed report (Ed25519)
- Steward council publishes redacted summary
- Apply operational or covenant amendments as required
- For major amendments: follow centre-shift policy (3-year consensus + 1,000-day cooling)

## Multi-Sig Procedure

1. Generate steward keypairs: `python TOOLS/ed25519_sign.py gen --out-dir keys/stewardN`
2. Sign incident decision: `python TOOLS/ed25519_sign.py sign --key keys/steward1/private.hex --in decision.json --out signed.json`
3. Add second signature: `python TOOLS/ed25519_sign.py add --key keys/steward2/private.hex --in signed.json --out signed_2.json`
4. Verify threshold met: `python TOOLS/ed25519_sign.py multisig-check --in signed_2.json --threshold 2`

## Legal Checklist

- [ ] Is donor consent still valid for this action?
- [ ] Does this action require GDPR/FADP notification?
- [ ] Is the privacy budget (epsilon) within limits?
- [ ] Are all affected donors' rights preserved?
- [ ] Is the audit trail complete and tamper-evident?
- [ ] Has legal counsel reviewed any proposed disclosure?

## Reversal Protocol

If an emergency action was taken in error:
1. Document the error in the Incident Record
2. Steward Council signs a reversal decision (2-of-3)
3. Restore affected artifacts from KEEP (append-only — original data preserved)
4. Notify affected parties
5. File reversal report in MANIFEST

## Notes

- All incident artifacts, signatures, and decisions are appended to the audit manifest
- Retention: permanent (COV#010 — no silent deletion)
- Access: steward + authorized reviewers only
- Format: append-only JSON in MANIFEST/escalation_log.json
- This playbook is operational — legal counsel must provide jurisdictional appendices before non-steward donors are invited

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
