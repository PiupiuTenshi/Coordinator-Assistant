from __future__ import annotations

import argparse
from pathlib import Path

if __package__ is None or __package__ == "":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from training.config import ANNOTATED_DIR, DEFAULTS, MODEL_NAME, MODELS_DIR, TRIAGE_LABELS
from training.data import assert_trainable_split, read_triage_csv


def build_dataset(path: Path, label_to_id: dict[str, int]):
    from datasets import Dataset

    rows = read_triage_csv(path)
    return Dataset.from_list(
        [
            {
                "text": row["text"],
                "label": label_to_id[row["triage_label"]],
                "sentence_id": row.get("sentence_id", ""),
            }
            for row in rows
        ]
    )


def tokenize_text(tokenizer):
    def encode(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=DEFAULTS.max_length,
        )

    return encode


def run(validate_only: bool = False) -> None:
    train_rows = read_triage_csv(ANNOTATED_DIR / "triage_train.csv")
    valid_rows = read_triage_csv(ANNOTATED_DIR / "triage_valid.csv")
    print(f"Triage records: train={len(train_rows)}, valid={len(valid_rows)}")
    if validate_only:
        return
    assert_trainable_split("triage", len(train_rows), len(valid_rows))

    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        DataCollatorWithPadding,
        Trainer,
        TrainingArguments,
        set_seed,
    )
    from training.metrics import compute_triage_metrics

    label_to_id = {label: index for index, label in enumerate(TRIAGE_LABELS)}
    id_to_label = {index: label for label, index in label_to_id.items()}
    set_seed(DEFAULTS.seed)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(TRIAGE_LABELS),
        id2label=id_to_label,
        label2id=label_to_id,
    )

    train_dataset = build_dataset(ANNOTATED_DIR / "triage_train.csv", label_to_id)
    valid_dataset = build_dataset(ANNOTATED_DIR / "triage_valid.csv", label_to_id)
    train_dataset = train_dataset.map(tokenize_text(tokenizer), batched=True)
    valid_dataset = valid_dataset.map(tokenize_text(tokenizer), batched=True)

    output_dir = MODELS_DIR / "triage_classifier"
    args = TrainingArguments(
        output_dir=str(output_dir),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=DEFAULTS.learning_rate,
        per_device_train_batch_size=DEFAULTS.batch_size,
        per_device_eval_batch_size=DEFAULTS.batch_size,
        num_train_epochs=DEFAULTS.epochs,
        weight_decay=DEFAULTS.weight_decay,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        report_to="none",
        seed=DEFAULTS.seed,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_triage_metrics,
    )
    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    print(f"Saved triage model to {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune PhoBERT for triage classification.")
    parser.add_argument("--validate-only", action="store_true", help="Only check that triage data is readable.")
    args = parser.parse_args()
    run(validate_only=args.validate_only)


if __name__ == "__main__":
    main()
