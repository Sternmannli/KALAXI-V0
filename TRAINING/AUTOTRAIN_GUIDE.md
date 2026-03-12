# How to Fine-Tune AXI on Hugging Face AutoTrain

Five steps. No code. No GPU. No subscription.

---

## STEP 1 — Create a Free Hugging Face Account

Go to huggingface.co and click "Sign Up" (top right). Use any email. Confirm your email. You now have an account. You do not need a paid plan.

---

## STEP 2 — Open AutoTrain

Go to huggingface.co/autotrain — Click "Create new project." Fill in:

- **Project name:** axi-canon-v1
- **Task:** LLM Finetuning (also called "LLM SFT" or "Text Generation")
- **Model:** mistralai/Mistral-7B-Instruct-v0.3

If Mistral 7B is not available in the dropdown, type the full name: mistralai/Mistral-7B-Instruct-v0.3

---

## STEP 3 — Upload the Training File

Click "Upload Training File" or "Data" (depending on the interface version). Select the file from your computer:

**CANON_SEED_V1_AUTOTRAIN.jsonl**

(This file is in the TRAINING folder of the KALAXI-V0 repository.)

After upload, AutoTrain should detect three columns: system, user, assistant. If it asks for a "chat template," select **chatml** or **default**. If it asks for a "text column," the data is already formatted — it will auto-detect.

---

## STEP 4 — Set Training Parameters

Use these settings (change only what is listed, leave everything else as default):

| Parameter | Value | Why |
|-----------|-------|-----|
| **Epochs** | 5 | Small dataset needs more passes |
| **Learning rate** | 2e-4 | Standard for QLoRA |
| **Batch size** | 2 | Safe for most GPU allocations |
| **LoRA r** | 16 | Balance between expressiveness and cost |
| **LoRA alpha** | 32 | Standard 2x multiplier |
| **Quantization** | 4-bit (int4) | Keeps cost low, fits in smaller GPU |
| **Block size** | 1024 | Our responses are short, this is plenty |

If AutoTrain does not show all of these options, the defaults are fine. The most important ones are: Epochs = 5, and LoRA/PEFT = enabled.

---

## STEP 5 — Start Training and Wait

Click "Start Training" (or "Train Model"). AutoTrain will:

1. Allocate a GPU (this may take 1-5 minutes)
2. Load Mistral 7B in 4-bit quantization
3. Train the LoRA adapter on your 63 pairs for 5 epochs
4. Save the adapter weights to your Hugging Face account

**Expected time:** 10-30 minutes for this dataset size.
**Expected cost:** $5-15 (charged to your Hugging Face account, pay-as-you-go).

When training finishes, you will have a new model on your Hugging Face profile: huggingface.co/YOUR_USERNAME/axi-canon-v1

---

## WHAT HAPPENS NEXT

The trained model is a LoRA adapter on top of Mistral 7B. To test it:

1. Go to your model page on Hugging Face
2. Click the "Inference API" widget (right side)
3. Type a test prompt: "What is the Dignity Predicate?"
4. Read the response. Does it sound like AXI?

If the voice is right — the first fork is born.
If the voice drifts — we adjust the seed file and retrain.

---

## IF SOMETHING GOES WRONG

- **"Not enough credits"** — AutoTrain requires a payment method. Add a card at huggingface.co/settings/billing. You will only be charged for what you use.
- **"Model not found"** — Try: mistralai/Mistral-7B-Instruct-v0.2 (older version, same architecture)
- **"Training failed"** — Reduce batch size to 1, reduce block size to 512. Try again.
- **"Data format error"** — Make sure you uploaded CANON_SEED_V1_AUTOTRAIN.jsonl (not the original CANON_SEED_V1.jsonl)

---

*Filed by V-002. [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
