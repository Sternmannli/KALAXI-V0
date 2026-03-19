"""
distillery_readers — Source-level readers for the KALAXI Distillery.

Each reader extracts essence from a specific content area in the repository,
reading the raw source files directly (not site JSON).

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from WEAVER.distillery_readers.base import BaseReader

__all__ = ["BaseReader"]
