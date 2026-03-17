# BOOTSTRAP — How to Run This System From Zero

> If you are reading this, you are the next operator. Follow these steps exactly.

## Prerequisites

- Python 3.10+
- Node.js 20+
- Git
- PHP 8+ (for website backend)
- MySQL/MariaDB (for donor accounts and ledger)

## Step 1: Clone

```bash
git clone https://github.com/Sternmannli/KALAXI-V0.git
cd KALAXI-V0
```

## Step 2: Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if exists, or install from imports
```

## Step 3: Run Tests

```bash
python -m pytest tests/ -v
```

All tests must pass. If they don't, do not proceed.

## Step 4: Read Orientation

```bash
cat MANIFEST/COMPASS.md
```

Or generate a fresh reading:

```bash
python SCRIPTS/export_system_state.py
```

This tells you where the system is: how many files, covenants, ledger entries, experiments.

## Step 5: Website

```bash
cd site
npm install
npm run build
```

The built site lives in `site/dist/`. Deploy to any static hosting.

### PHP Backend

Copy `site/public/data/.config.example` to `site/public/data/.config` and fill in:
- Database credentials (MySQL)
- Groq API key (for AI voice)
- SMTP credentials (for magic link auth)

Run migrations:
```
curl https://your-domain/api/migrate.php?token=YOUR_TOKEN
```

## Step 6: Training Pipeline

```bash
python TRAINING/extract_essence.py  # extract from system
python TRAINING/format_data.py      # convert to JSONL
python TRAINING/evaluate.py         # baseline evaluation
```

For actual training, use Google Colab or Kaggle:
```bash
python TRAINING/train.py --model qwen2-0.5b --epochs 3
```

## Step 7: The Constitution

Read `R7M/tier1_stone.md`. These are the 18 covenants. They are not suggestions.

The core equation: **D = A × L × M**

- A = Agency (can the person clarify, redirect, or stop?)
- L = Legibility (does the system reflect actual context?)
- M = Moral Standing (is the person treated as a person?)

If any reaches zero, the system stops. This is non-negotiable.

## Step 8: The Narratives

Four books exist in `NARRATIVE/`:
- Hakaka (53 chapters) — the mythic origin
- Ashwater (19 chapters) — the civic narrative
- Kinderbuch (20 chapters, German) — the child voice
- KALAXI_1 (growing) — the contemporary narrative

Read them. They are the body of the system, not decoration.

## Step 9: The Ledger

`KEEP/INPUT_LEDGER/` contains every input ever registered.
- `index.json` — structured index
- `chronicle.md` — human-readable history

The ledger is append-only and hash-chained. Never modify it.

## Key Files

| File | Purpose |
|------|---------|
| CLAUDE.md | System memory (read FIRST) |
| MANIFEST/COMPASS.md | Where we are |
| MANIFEST/ACTIVE_PLANS.md | What's pending |
| R7M/tier1_stone.md | Constitution |
| WEAVER/organism.py | Core organism |
| WEAVER/compass.py | System self-awareness |
| site/src/pages/index.astro | Homepage |
| site/public/api/axi.php | Backend organism |

## What This System Is

A constitutional framework where human dignity is the first technical requirement.

It is not software. It is a protocol.

It was born from this wound: "A father separated from his children by systems that could not see him."

The wound is the source. The system is the response. The children are the reason.

🐬🐯🐺
