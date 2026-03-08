# weaver/dignity_filter.py
# Thin wrapper — delegates to the full dignity_check.py implementation.
# Kept for backwards compatibility so imports from either path work.
#
# The full D = A x L x M implementation lives in dignity_check.py.

import sys
from pathlib import Path

_weaver_dir = Path(__file__).parent
if str(_weaver_dir.parent) not in sys.path:
    sys.path.insert(0, str(_weaver_dir.parent))

from WEAVER.dignity_check import check_dignity, DignityResult, ComponentResult  # noqa: F401

__all__ = ['check_dignity', 'DignityResult', 'ComponentResult']