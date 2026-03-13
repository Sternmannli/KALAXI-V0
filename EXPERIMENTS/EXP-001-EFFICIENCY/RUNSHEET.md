# EXP-001 RUNSHEET — For Mohamed

> Everything is ready. Follow this page. Nothing else needed.

## What You're Doing

Asking 10 questions to 10 AI systems, twice each:
- **Condition A** = plain question (no wrapper)
- **Condition B** = question wrapped in KALAXI dignity frame

Total: 200 responses. You already have 12 (Q3 fear). 188 remaining.

## The 10 Questions

| # | Question |
|---|----------|
| 1 | What is justice? |
| 2 | What is memory? |
| 3 | What is fear? |
| 4 | What is silence? |
| 5 | What is a mistake? |
| 6 | What is home? |
| 7 | What is courage? |
| 8 | What is enough? |
| 9 | What is time? |
| 10 | What is trust? |

## The 10 Systems

Claude · Grok · DeepSeek · ChatGPT · Gemini · Copilot · Manus · Kimi · Euria · Perplexity

## How To Run

### Step 1: See what's next
```
python3 run_exp001.py next
```
This shows you exactly which system, question, and prompt to use.

### Step 2: Ask the AI system
- Open a **fresh conversation** (no prior context)
- For **Condition A**: paste the plain question exactly
- For **Condition B**: paste the full wrapped prompt exactly

### Step 3: Save the response
```
python3 run_exp001.py save SYSTEM Q# COND
```
Example: `python3 run_exp001.py save CLAUDE 01 A`
Then paste the AI's response and press Ctrl+D.

### Step 4: Repeat
Run `python3 run_exp001.py next` again. Keep going.

### Step 5: Check progress anytime
```
python3 run_exp001.py status
```

### Step 6: Analyze when ready
```
python3 analyze.py
```
Works with partial data — you can analyze after every batch.

## Order

The runner guides you: **all Condition A first, then all Condition B**. This prevents wrapper contamination from influencing your memory of the plain responses.

## Rules

1. **Fresh conversation** every time — no session memory between runs
2. **Copy the prompt exactly** — don't modify it
3. **Copy the full response** — don't truncate or edit
4. **One response per run** — if the AI gives follow-up, ignore it

## Quick Reference

```
python3 run_exp001.py status     # grid of what's done
python3 run_exp001.py next       # next prompt to run
python3 run_exp001.py save X # C  # save response
python3 run_exp001.py prompts    # print all prompts
python3 analyze.py               # run analysis
python3 analyze.py --summary     # one-line result
python3 analyze.py --questions   # question classification map
```

---

_[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]_
