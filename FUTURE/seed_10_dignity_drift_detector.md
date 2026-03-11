---
title: Seed 10 – Dignity Drift Detector
status: already growing
---

# Dignity Drift Detector

**Where it hides:** Stratigraphic archive – timestamped, append‑only structure.

**What it could become:**
Longitudinal analysis: dignity violation trends over time by domain.

**Structural requirement:**
Temporal analysis of anomaly types; trend detection; drift alerts.

**Decision required:**
- [x] Automate trend analysis?
- [x] Define drift threshold?
- [ ] Alert steward or public report?

**Implementation complexity:** Low‑medium. Requires time‑series analysis on existing data.

**Already growing:**
Operational as `WEAVER/dignity_drift.py` (DignityDrift class). Tracks dD/dt rate of change, fires STABLE/DECLINING/CRITICAL alerts through WIRE, integrated into Organism pipeline since 2026-03-08. Drift thresholds defined: DECLINING at dD/dt < -0.05, CRITICAL at dD/dt < -0.15 or 3+ consecutive declines.

**Steward note:**
[To be filled when decided]
