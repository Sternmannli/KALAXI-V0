# weaver/pattern_detector_v1.py
# Simple keyword pattern detector – scans THRESHOLD.md only

import re
from pathlib import Path
from collections import Counter

# Paths
ROOT = Path(__file__).parent.parent
THRESHOLD = ROOT / "THRESHOLD.md"
PATTERNS_FILE = ROOT / "MANIFEST" / "patterns.json"

def scan_patterns():
    """Scan THRESHOLD.md for recurring keywords."""
    if not THRESHOLD.exists():
        print("THRESHOLD.md not found")
        return []
    
    text = THRESHOLD.read_text()
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Simple stop words
    stop_words = {'seed', 'seeds', 'threshold', 'proverb', 'anomaly', 'gap', 
                  'wisdom', 'covenant', 'signed', 'moved', 'provisional', 'source'}
    
    words = [w for w in words if w not in stop_words]
    counter = Counter(words)
    
    # Find words that appear at least 3 times
    patterns = []
    for word, count in counter.most_common(20):
        if count >= 3:
            patterns.append({
                "keyword": word,
                "count": count,
                "confidence": round(count / 10, 2),  # simple confidence
                "source": "THRESHOLD.md"
            })
    
    return patterns

if __name__ == "__main__":
    patterns = scan_patterns()
    print(f"Found {len(patterns)} patterns")
    for p in patterns:
        print(f"  {p['keyword']}: {p['count']} times")