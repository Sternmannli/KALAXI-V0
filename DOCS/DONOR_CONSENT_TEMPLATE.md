# KALAXI Donor Consent Template — DRAFT

**STATUS: DRAFT — Requires legal counsel review before use with non-steward donors.**
**Jurisdiction: Switzerland (Swiss Federal Act on Data Protection / FADP). EU GDPR compliance required for EU-resident donors.**

---

## Informed Consent for Participation in KALAXI

### What is KALAXI?
KALAXI is a dignity-measurement research system that collects observations about human experiences to detect patterns of dignity gain or loss. It is operated by Mohamed Farag (Steward) from Switzerland.

### What we collect
We ask you four questions per exchange:
1. Did dignity increase?
2. Did dignity decrease?
3. What happened?
4. What should be kept?

Your answers are stored as observations. We do not collect your name, email, phone number, or any identifying information unless you voluntarily provide it.

### How your data is used
- Your observations are anonymized before any analysis
- Patterns are detected only when 7 or more donors show the same signal (k-anonymity ≥ 7)
- A mathematical privacy budget (ε ≤ 1.0) limits how much any analysis can reveal
- No individual observation is ever shared outside the system without your explicit consent
- Your data is never sold, rented, or used for advertising

### Your rights
- **Access:** You may request a copy of your observations at any time
- **Withdrawal:** You may withdraw your consent at any time. Your future data will not be collected. Previously anonymized patterns cannot be un-anonymized.
- **Correction:** You may correct any observation you have made
- **Deletion:** You may request deletion of your raw observations. Anonymized aggregate patterns that have already been computed cannot be individually reversed.
- **Explanation:** You may ask for an explanation of any pattern detected from your observations

### Data protection
- All data is stored in append-only encrypted storage
- Steward access requires Ed25519 key authentication
- Three absolute prohibitions are enforced by the system (Sealed Gate): forced erasure of identity, cognitive torture, and depersonalization. If any of these are detected, the system halts.
- Privacy budget consumption is logged and auditable

### Retention
- Raw observations are retained for the duration of your participation plus 90 days after withdrawal
- Anonymized patterns are retained permanently as part of the wisdom registry
- Audit logs are retained permanently (COV#010 — no silent deletion)

### Contact
- Steward: Mohamed Farag
- Email: info@kalam.ch
- Location: Switzerland

### Legal basis
- Consent (this document)
- Swiss FADP Art. 6 (lawfulness), Art. 7 (purpose limitation)
- GDPR Art. 6(1)(a) (consent) for EU-resident donors

---

**By participating, you confirm that:**
- [ ] You have read and understood this consent document
- [ ] You voluntarily agree to share observations
- [ ] You understand you may withdraw at any time
- [ ] You understand that anonymized aggregate patterns cannot be reversed after computation

**Signature:** _________________________ **Date:** _____________

---

**IMPORTANT: This template is a DRAFT. Legal counsel must review and approve before any non-steward donor is invited. Particular attention needed for: (1) FADP compliance details, (2) cross-border data transfer provisions if EU donors participate, (3) minor donor protections if applicable.**

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
