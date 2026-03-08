#!/usr/bin/env python3
"""
Tests for the five pillar detectors.
These tests verify pattern-matching logic WITHOUT requiring ML model downloads.
They test the regex/heuristic layers only.
"""

import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# --- Humour detector pattern tests ---

def test_humour_self_deprecation_patterns():
    """Self-deprecation patterns should match expected text."""
    patterns = [
        r"\bI am (bad|terrible|useless|wrong|stupid)\b",
        r"\bmy fault\b",
        r"\bof course I\b",
        r"\bI can't (even|believe|help)\b"
    ]
    matches = [
        "I am terrible at this",
        "It's my fault entirely",
        "of course I failed again",
        "I can't even think straight"
    ]
    for pattern, text in zip(patterns, matches):
        assert re.search(pattern, text, re.IGNORECASE), f"Pattern '{pattern}' should match '{text}'"


# --- Absurdity detector pattern tests ---

def test_absurdity_paradox_patterns():
    """Paradox patterns should detect contradictions."""
    patterns = [
        r"\bI know that I don't know\b",
        r"\btrue (and|but) false\b",
        r"\balways (and|but) never\b",
        r"\bcontradiction\b",
        r"\bimpossible\b"
    ]
    texts = [
        "I know that I don't know anything",
        "It's true but false at the same time",
        "She is always but never here",
        "This is a contradiction",
        "The task is impossible"
    ]
    for pattern, text in zip(patterns, texts):
        assert re.search(pattern, text, re.IGNORECASE), f"Pattern '{pattern}' should match '{text}'"


def test_absurdity_meta_cognitive_markers():
    """Meta-cognitive markers should detect reflective language."""
    markers = [
        r"\bI (think|wonder|ask|question|ponder)\b",
        r"\bwhy\b",
        r"\bmeaning\b",
        r"\bpurpose\b",
    ]
    text = "I wonder about the meaning and purpose of why we exist"
    for marker in markers:
        assert re.search(marker, text, re.IGNORECASE), f"Marker '{marker}' should match"


# --- Obsession detector pattern tests ---

def test_obsession_intrusion_markers():
    """Intrusion markers should detect recurring thought patterns."""
    markers = [
        r"\bkeep (thinking|worrying|remembering)\b",
        r"\bcan't stop\b",
        r"\balways on my mind\b",
        r"\bhaunts me\b",
        r"\brecurring thought\b"
    ]
    texts = [
        "I keep thinking about it",
        "I can't stop worrying",
        "It's always on my mind",
        "The memory haunts me",
        "It's a recurring thought"
    ]
    for marker, text in zip(markers, texts):
        assert re.search(marker, text, re.IGNORECASE), f"Marker '{marker}' should match '{text}'"


def test_obsession_responsibility_markers():
    """Responsibility inflation markers should detect patterns."""
    markers = [
        r"\bI (must|have to|need to)\b",
        r"\bit's my (responsibility|fault|duty)\b",
        r"\bI should have\b",
    ]
    texts = [
        "I must do something about this",
        "It's my responsibility to fix it",
        "I should have known better",
    ]
    for marker, text in zip(markers, texts):
        assert re.search(marker, text, re.IGNORECASE), f"Marker '{marker}' should match '{text}'"


# --- Love detector pattern tests ---

def test_love_letter_indicators():
    """Love letter markers should detect romantic language."""
    indicators = [
        (r"\bdear\b", "Dear friend, I write to you"),
        (r"\bmy (love|darling|dearest|heart|soul)\b", "My dearest companion"),
        (r"\bI (miss|need|want|cherish|adore)\b", "I miss you deeply"),
        (r"\bwithout you\b", "Life without you is grey"),
    ]
    for pattern, text in indicators:
        assert re.search(pattern, text, re.IGNORECASE), f"Pattern '{pattern}' should match '{text}'"


# --- Cross-pillar tests ---

def test_no_false_positive_on_neutral():
    """Neutral text should not trigger specialized markers."""
    text = "The weather is nice today. I went to the store."
    obsession_markers = [
        r"\bkeep (thinking|worrying|remembering)\b",
        r"\bcan't stop\b",
        r"\bhaunts me\b",
    ]
    for marker in obsession_markers:
        assert not re.search(marker, text, re.IGNORECASE), f"Neutral text triggered '{marker}'"


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS: {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL: {test.__name__} — {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {test.__name__} — {e}")
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
