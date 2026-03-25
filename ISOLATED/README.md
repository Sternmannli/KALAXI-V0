# ISOLATED

Clean engineering modules. No connection to the parent repo's domain logic.
Each subdirectory is a standalone, portable library.

## drift/
Sliding-window drift detector for composite time-series scores.
Computes rate (dV/dt), acceleration (d²V/dt²), per-component tracking.
Persists state to JSON. Zero dependencies beyond stdlib.

### Run tests
```
cd drift && python -m pytest test_drift_detector.py -v
```
