#!/usr/bin/env python3
"""
Runner script for proverb_compressor.py
Parses anomalies from KALAXI_C_WISDOM.txt and feeds them to the compressor.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import sys
import os
import json
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(__file__))
from proverb_compressor import cluster_anomalies, generate_proverb_from_cluster, compress_all

WISDOM_FILE = os.path.join(os.path.dirname(__file__), '..', 'KALAXI_C_WISDOM.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'MANIFEST', 'PROVERB_APPROVAL_QUEUE.md')

def parse_anomalies(filepath):
    """Parse anomaly entries from KALAXI_C_WISDOM.txt"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Split on ##ANOM: markers
    blocks = re.split(r'##ANOM:', content)
    anomalies = []

    for block in blocks[1:]:  # skip preamble
        lines = block.strip().split('\n')
        if not lines:
            continue

        # Parse ID from first line
        anom_id = lines[0].strip().split()[0] if lines[0].strip() else 'unknown'
        anom_id = f"ANOM#{anom_id}"

        entry = {'id': anom_id, 'text': '', 'felt_domain': 'general'}

        for line in lines[1:]:
            line = line.strip()
            if line.startswith('---'):
                break
            if line.startswith('description:'):
                entry['text'] = line.replace('description:', '').strip()
            elif line.startswith('felt_domain:'):
                entry['felt_domain'] = line.replace('felt_domain:', '').strip()
            elif line.startswith('severity:'):
                entry['severity'] = line.replace('severity:', '').strip()
            elif line.startswith('module:'):
                entry['module'] = line.replace('module:', '').strip()

        if entry['text']:
            anomalies.append(entry)

    return anomalies


def write_results(candidates, output_path):
    """Append proverb candidates to the approval queue."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    header = f"\n\n---\n\n## Compressor Run — {timestamp}\n\n"
    header += f"**Anomalies processed:** fed from KALAXI_C_WISDOM.txt\n"
    header += f"**Candidates generated:** {len(candidates)}\n\n"

    entries = []
    for i, c in enumerate(candidates, 1):
        entry = f"### Candidate #{i}\n"
        entry += f"- **Text:** {c['text']}\n"
        entry += f"- **Source anomalies:** {', '.join(c['source_anomalies'])}\n"
        entry += f"- **Felt domains:** {', '.join(c['felt_domains'])}\n"
        entry += f"- **Status:** PROVISIONAL — awaiting V-001 review\n"
        entries.append(entry)

    with open(output_path, 'a') as f:
        f.write(header)
        if entries:
            f.write('\n'.join(entries))
        else:
            f.write("No candidates passed the lock test in this run.\n")
        f.write(f"\n\n_[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]_\n")

    return len(candidates)


if __name__ == '__main__':
    print("=== KALAXI Cross-Anomaly Proverb Compressor ===")
    print(f"Loading anomalies from {WISDOM_FILE}...")

    anomalies = parse_anomalies(WISDOM_FILE)
    print(f"Parsed {len(anomalies)} anomalies")

    for a in anomalies:
        print(f"  {a['id']}: {a['text'][:60]}... [{a['felt_domain']}]")

    # Also cluster by felt_domain for domain-aware compression
    domain_groups = {}
    for a in anomalies:
        domain_groups.setdefault(a['felt_domain'], []).append(a)

    print(f"\nDomain groups: {', '.join(f'{k}({len(v)})' for k,v in domain_groups.items())}")

    print("\nRunning clustering and compression (eps=0.8 for TF-IDF sparse space)...")
    candidates = compress_all(anomalies)

    # Also try domain-based clustering to catch groups TF-IDF missed
    existing_sources = set()
    for c in candidates:
        existing_sources.update(c['source_anomalies'])

    print("Also trying domain-based grouping for uncovered anomalies...")
    for domain, group in domain_groups.items():
        uncovered = [a for a in group if a['id'] not in existing_sources]
        if len(uncovered) >= 2:
            prov = generate_proverb_from_cluster(uncovered)
            if prov:
                candidates.append(prov)
        elif len(group) >= 2 and domain not in [c['felt_domains'][0] for c in candidates if c['felt_domains']]:
            prov = generate_proverb_from_cluster(group)
            if prov:
                candidates.append(prov)

    print(f"\nGenerated {len(candidates)} proverb candidates:")
    for c in candidates:
        print(f"  → \"{c['text']}\"")
        print(f"    from: {c['source_anomalies']}")

    count = write_results(candidates, OUTPUT_FILE)
    print(f"\nResults written to {OUTPUT_FILE}")
    print(f"Total candidates: {count}")
    print("Done. [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]")
