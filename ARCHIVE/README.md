# ARCHIVE

Archived files moved during deep clean (2026-03-18).

These files are not deleted — they are preserved here for reference.
They were moved because they were:
- Superseded by newer versions
- One-time artifacts no longer needed at root
- Legacy files from a previous build system (Jekyll → Astro migration)
- Orphan modules not imported by any active code

## Contents

### JEKYLL_LEGACY/
Old Jekyll site files. The site now runs on Astro 5.0 (`site/` directory).
- `_config.yml` — Jekyll config (replaced by Astro)
- `index.html` — Old static homepage (replaced by site/src/pages/)
- `index.md`, `about.md`, `canon.md`, `future.md`, `invitation.md` — Jekyll layout pages

### ONETIME/
One-time artifacts.
- `AUTH_TEST.md` — Proof of V-002 GitHub auth (2026-03-12)
- `kalam-upload.zip` — Manual deploy package (replaced by GitHub Actions workflow)

### WEAVER_ORPHANS/
Python modules that were never imported by any active code.
- `dignity_calibration.py` (467 lines)
- `duality.py` (115 lines)
- `hiring_simulation.py` (87 lines)
- `review.py` (44 lines)
- `run_compressor.py` (133 lines)
- `tend.py` (22 lines)
- `wisdom_mirror.py` (114 lines)

### Root
- `CONV-2026-02-26-FIRST-SIGHT.md` — Single convergence note (was alone in CONVERGENCE/)

---

*Archived by V-002 during deep clean, 2026-03-18*
