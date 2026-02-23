import re
from pathlib import Path

THRESHOLD_FILE = Path("THRESHOLD.md")
SLICE_A = Path("KALAXI_A_FOUNDATION.txt")
SLICE_C = Path("KALAXI_C_WISDOM.txt")

seed_pattern = re.compile(
    r'^\[(?P<timestamp>[^\]]+)\] -- (?P<type>\w+) -- (?P<id>[^\s]+) .*'
)

def get_slice_file(seed_type):
    if seed_type == 'gap':
        return SLICE_A
    elif seed_type in ('proverb', 'anomaly', 'wisdom node'):
        return SLICE_C
    else:
        return None

def main():
    if not THRESHOLD_FILE.exists():
        return

    lines = THRESHOLD_FILE.read_text().splitlines()
    new_lines = []

    for line in lines:
        if not line.strip() or '[MOVED]' in line:
            new_lines.append(line)
            continue

        match = seed_pattern.match(line)
        if match:
            seed_type = match.group('type')
            target = get_slice_file(seed_type)
            if target:
                with open(target, 'a') as f:
                    f.write('\n' + line + '\n')
                new_lines.append(line + ' [MOVED]')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    THRESHOLD_FILE.write_text('\n'.join(new_lines))

if __name__ == '__main__':
    main()