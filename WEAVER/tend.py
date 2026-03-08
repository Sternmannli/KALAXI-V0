#!/usr/bin/env python3
"""
tend.py — Thin wrapper for WEAVER/ path compatibility.
The full Kalaxi Tending Engine v2.2 lives at .github/scripts/tend.py.
This wrapper imports from there so both paths work.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from tend import *  # noqa: F401,F403

if __name__ == "__main__":
    import tend as _tend_engine
    if hasattr(_tend_engine, 'main'):
        _tend_engine.main()
    else:
        import importlib
        importlib.reload(_tend_engine)