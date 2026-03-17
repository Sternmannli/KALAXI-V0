#!/usr/bin/env python3
"""
train.py — LoRA fine-tuning script for AXI voice model.

Designed to run on free compute (Google Colab T4, Kaggle P100, Lightning.ai A10G).

Usage:
    python TRAINING/train.py --model qwen2-0.5b --epochs 3 --lr 2e-4

Model candidates:
    - qwen2-0.5b     (Qwen/Qwen2-0.5B-Instruct) — smallest, fastest
    - tinyllama       (TinyLlama/TinyLlama-1.1B-Chat-v1.0) — good base
    - smollm          (HuggingFaceTB/SmolLM-1.7B-Instruct) — edge-optimized
    - phi3-mini       (microsoft/Phi-3-mini-4k-instruct) — strongest reasoning

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRAINING = ROOT / "TRAINING"

MODEL_MAP = {
    "qwen2-0.5b": "Qwen/Qwen2-0.5B-Instruct",
    "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "smollm": "HuggingFaceTB/SmolLM-1.7B-Instruct",
    "phi3-mini": "microsoft/Phi-3-mini-4k-instruct",
}


def main():
    parser = argparse.ArgumentParser(description="LoRA fine-tune for AXI voice")
    parser.add_argument("--model", default="qwen2-0.5b", choices=list(MODEL_MAP.keys()))
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--output-dir", default=str(TRAINING / "checkpoints"))
    parser.add_argument("--dry-run", action="store_true", help="Print config without training")
    args = parser.parse_args()

    model_id = MODEL_MAP[args.model]
    train_file = TRAINING / "axi_training.jsonl"
    eval_file = TRAINING / "axi_eval.jsonl"

    if not train_file.exists():
        print("Run extract_essence.py and format_data.py first.")
        return

    # Count training examples
    with open(train_file) as f:
        train_count = sum(1 for _ in f)
    with open(eval_file) as f:
        eval_count = sum(1 for _ in f)

    config = {
        "model": model_id,
        "train_data": str(train_file),
        "eval_data": str(eval_file),
        "train_examples": train_count,
        "eval_examples": eval_count,
        "epochs": args.epochs,
        "learning_rate": args.lr,
        "batch_size": args.batch_size,
        "lora_r": args.lora_r,
        "lora_alpha": args.lora_alpha,
        "lora_dropout": 0.05,
        "max_length": args.max_length,
        "output_dir": args.output_dir,
        "gradient_accumulation_steps": 4,
        "warmup_ratio": 0.1,
        "weight_decay": 0.01,
        "fp16": True,
        "logging_steps": 10,
        "save_strategy": "epoch",
    }

    print("=" * 60)
    print("AXI Voice Model — LoRA Fine-Tuning Configuration")
    print("=" * 60)
    for k, v in config.items():
        print(f"  {k}: {v}")
    print("=" * 60)

    if args.dry_run:
        # Save config for reference
        config_path = TRAINING / "train_config.json"
        config_path.write_text(json.dumps(config, indent=2))
        print(f"\nDry run. Config saved to {config_path}")
        print("\nTo train on Google Colab, upload this script and run:")
        print(f"  !pip install transformers peft datasets accelerate bitsandbytes")
        print(f"  !python train.py --model {args.model} --epochs {args.epochs}")
        return

    # ── Actual training ──
    try:
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            Trainer,
        )
        from peft import LoraConfig, get_peft_model, TaskType
        from datasets import load_dataset
    except ImportError:
        print("\nRequired packages not installed. Run:")
        print("  pip install transformers peft datasets accelerate bitsandbytes")
        print("\nOr use --dry-run to generate config only.")
        return

    print(f"\nLoading model: {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        load_in_8bit=True,
        device_map="auto",
    )

    # LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load data
    def tokenize(example):
        msgs = example["messages"]
        text = tokenizer.apply_chat_template(msgs, tokenize=False)
        return tokenizer(text, truncation=True, max_length=args.max_length, padding="max_length")

    dataset = load_dataset("json", data_files={"train": str(train_file), "eval": str(eval_file)})
    tokenized = dataset.map(tokenize, remove_columns=["messages"])

    # Training args
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        warmup_ratio=0.1,
        weight_decay=0.01,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        load_best_model_at_end=True,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["eval"],
    )

    print("\nTraining started...")
    trainer.train()

    # Save
    model.save_pretrained(args.output_dir + "/final")
    tokenizer.save_pretrained(args.output_dir + "/final")
    print(f"\nModel saved to {args.output_dir}/final")


if __name__ == "__main__":
    main()
