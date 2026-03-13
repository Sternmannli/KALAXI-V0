"""
WEAVER — KALAXI Tier 2: Logic Layer
Nine modules wired into one living organism.
"""

import sys
from pathlib import Path

# Ensure the project root is importable
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
