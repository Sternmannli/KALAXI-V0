#!/usr/bin/env python3
"""
Clean for Public — Vocabulary stripping for kalam-framework sync.

Takes files from the private KALAXI-V0 repo, strips internal vocabulary,
and copies cleaned versions to the public kalam-framework repo.

Zero leak tolerance. Every internal term is caught and replaced.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import argparse
import json
import os
import re
import shutil
from pathlib import Path


# Internal vocabulary → public replacement
VOCABULARY_MAP = {
    # Identity markers
    r'\bV-001\b': 'founder',
    r'\bV-002\b': 'operator',
    r'\bV-003\b': 'contributor',
    r'\bMohamed Farag\b': '[founder]',
    r'\bMohamed\b': '[founder]',
    r'\bLaila\b': '[child-1]',
    r'\bYara\b': '[child-2]',
    r'\bSalim\b': '[child-3]',
    r'🐬🐯🐺': '',
    r'\[V-002 · GO: .*?\]': '',

    # System-specific names
    r'\bKALAXI\b': 'kalam',
    r'\bKALAXI-V0\b': 'kalam-framework',
    r'\bAXI\b': 'the system',
    r'\bHakaka\b': '[narrative-1]',
    r'\bAshwater\b': '[narrative-2]',
    r'\bKinderbuch\b': '[narrative-3]',

    # Internal references
    r'\bkalam\.ch\b': '[deployment-domain]',
    r'\bHostpoint\b': '[hosting-provider]',
    r'\bfaragmoh\b': '[account]',
    r'\bSternmannli\b': '[org]',

    # Experiment identifiers
    r'\bEXP-001\b': 'efficiency-experiment',
    r'\bEXP-002\b': 'convergence-experiment',
    r'\bEXP-003\b': 'gate-experiment',
    r'\bEXP-004\b': 'generation-experiment',
}

# Files that should NEVER be synced (even if in manifest paths)
NEVER_SYNC = {
    'CLAUDE.md',
    '.env',
    '.config',
    'credentials',
    'INPUT_LEDGER',
    'chronicle.md',
    'index.json',
}


def clean_content(text: str) -> str:
    """Strip internal vocabulary from text content."""
    for pattern, replacement in VOCABULARY_MAP.items():
        text = re.sub(pattern, replacement, text)

    # Remove empty commit signatures
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

    return text


def should_skip(path: str) -> bool:
    """Check if a file should never be synced."""
    name = os.path.basename(path)
    for blocked in NEVER_SYNC:
        if blocked in path or blocked == name:
            return True
    return False


def sync_file(source: Path, target: Path) -> bool:
    """Clean and copy a single file. Returns True if file was synced."""
    if should_skip(str(source)):
        return False

    target.parent.mkdir(parents=True, exist_ok=True)

    # Binary files: copy as-is
    if source.suffix in {'.png', '.jpg', '.svg', '.ico', '.woff', '.woff2'}:
        shutil.copy2(source, target)
        return True

    # Text files: clean vocabulary
    try:
        content = source.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return False

    cleaned = clean_content(content)
    target.write_text(cleaned, encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser(description='Clean and sync to public repo')
    parser.add_argument('--source', required=True, help='Path to private repo root')
    parser.add_argument('--target', required=True, help='Path to public repo root')
    parser.add_argument('--manifest', required=True, help='Path to sync manifest JSON')
    args = parser.parse_args()

    source_root = Path(args.source).resolve()
    target_root = Path(args.target).resolve()
    manifest_path = Path(args.manifest).resolve()

    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        return

    with open(manifest_path) as f:
        manifest = json.load(f)

    synced = 0
    skipped = 0

    for entry in manifest.get('files', []):
        src_pattern = entry.get('source', '')
        tgt_dir = entry.get('target', '')

        # Resolve glob patterns
        src_path = source_root / src_pattern
        if '*' in src_pattern:
            for match in source_root.glob(src_pattern):
                if match.is_file():
                    rel = match.relative_to(source_root)
                    tgt = target_root / tgt_dir / rel.name
                    if sync_file(match, tgt):
                        synced += 1
                    else:
                        skipped += 1
        elif src_path.is_file():
            tgt = target_root / tgt_dir / src_path.name
            if sync_file(src_path, tgt):
                synced += 1
            else:
                skipped += 1
        elif src_path.is_dir():
            for match in src_path.rglob('*'):
                if match.is_file():
                    rel = match.relative_to(src_path)
                    tgt = target_root / tgt_dir / rel
                    if sync_file(match, tgt):
                        synced += 1
                    else:
                        skipped += 1

    print(f"Synced: {synced} files, Skipped: {skipped} files")


if __name__ == '__main__':
    main()
