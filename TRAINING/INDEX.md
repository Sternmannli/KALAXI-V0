# TRAINING — Brain

The voice factory. Where system knowledge becomes training data for AXI's own model.

## Two Layers

### Top Level — Legacy & Active Datasets
These files were created before ORGAN/ was structured. Some feed into ORGAN/, some are standalone.

| File | Purpose | Status |
|------|---------|--------|
| `axi_training.jsonl` | Full voice training corpus (640KB, 10K+ examples) | ACTIVE — primary dataset |
| `axi_eval.jsonl` | Evaluation dataset (49KB) | ACTIVE — used by evaluate.py |
| `GOLDEN_REGRESSION.jsonl` | 200 golden utterances across 9 registers | ACTIVE — regression testing |
| `CANON_SEED_V1.jsonl` | Canon seed v1 (51KB) | Feeds ORGAN/ |
| `CANON_SEED_V1_AUTOTRAIN.jsonl` | AutoTrain format (112KB) | AutoTrain variant |
| `REGISTER_GAP_FEAR_DIGNITY.jsonl` | Gap-filling for fear + dignity registers (7KB) | Supplement |
| `raw_essence.json` | Raw extracted essence (3.4MB) | Intermediate — feeds extract_essence.py |
| `eval_results.json` | Evaluation results | Output of evaluate.py |
| `train_config.json` | Training configuration | Together AI config |

### Top Level — Scripts
| Script | Purpose |
|--------|---------|
| `train.py` | Training script (Together AI) |
| `evaluate.py` | Evaluation against golden set |
| `extract_essence.py` | Essence extraction from system (39KB) |
| `format_data.py` | Data formatting utility |
| `AUTOTRAIN_GUIDE.md` | Hugging Face AutoTrain integration guide |

### ORGAN/ — The Structured Pipeline
This is the well-organized part. Three phases of training data preparation.

```
ORGAN/
├── PHASE_1_CPT/     # Causal Prediction Training — system learns the language
│   └── cpt_corpus.jsonl + meta
├── PHASE_2_SFT/     # Supervised Fine-Tuning — system learns to respond
│   └── sft_corpus.jsonl
├── PHASE_3_DPO/     # Direct Preference Optimization — system learns what is better
│   └── dpo_corpus.jsonl
├── GOLDEN_CPT.jsonl  # Gold standard CPT examples
├── GOLDEN_SFT.jsonl  # Gold standard SFT examples
├── GOLDEN_DPO.jsonl  # Gold standard DPO examples
├── ZAKAKA/           # Zakaka corpus builder
├── REFINERY/         # Rejected/filtered examples
├── build_corpus.py   # Corpus builder
├── extract.py        # Extraction utility
├── purify.py         # Data purification
├── EXTRACTION_RULES.md  # Rules for extraction
├── REGISTRY.md       # Phase registry
├── MANIFEST.json     # Organ phase manifest
└── SCAN_DIGEST_2026-03-18.md  # Scan results
```

## Data Flow

```
System knowledge (R7M/, CANON/, NARRATIVE/, VOICE/)
    → extract_essence.py → raw_essence.json
    → format_data.py → axi_training.jsonl + axi_eval.jsonl
    → ORGAN/build_corpus.py → CPT/SFT/DPO corpora
    → train.py → Together AI fine-tune
    → evaluate.py → eval_results.json (compared against GOLDEN_REGRESSION.jsonl)
```

## Connection to SCIENCE/

EXP-007 high-scoring responses (4-5) feed into `ORGAN/PHASE_3_DPO/` as "chosen" examples. Low-scoring responses (1-2) feed as "rejected." The Kimi encounter data is the first source of empirical DPO pairs for presence.

## What Needs Attention

1. **Top-level clutter:** 9 data files + 4 scripts + 1 guide at the top level. ORGAN/ is the structured home. Over time, the top-level files should be understood as either (a) inputs to ORGAN/, (b) active standalone datasets, or (c) historical. This brain clarifies which is which.
2. **Register gaps:** Fear register (10 examples) and dignity register (15 examples) are below the 25-example target. `REGISTER_GAP_FEAR_DIGNITY.jsonl` partially fills this.
3. **Training not yet run:** All data is ready. Together AI key is set. The fine-tune has not been triggered. This is Priority 2A in ACTIVE_PLANS.md.
