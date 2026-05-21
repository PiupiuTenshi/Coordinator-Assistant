from __future__ import annotations

import argparse
from pathlib import Path

if __package__ is None or __package__ == "":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from training.config import ANNOTATED_DIR, DEFAULTS, MODEL_NAME, MODELS_DIR, NER_LABELS
from training.data import assert_trainable_split, read_bio


def build_dataset(path: Path, label_to_id: dict[str, int]):
    from datasets import Dataset

    rows = read_bio(path)
    return Dataset.from_list(
        [
            {
                "tokens": row["tokens"],
                "labels": [label_to_id[label] for label in row["ner_tags"]],
                "sentence_id": row.get("sentence_id", ""),
            }
            for row in rows
        ]
    )


def tokenize_and_align_labels(tokenizer, label_all_tokens: bool = False):
    def encode(examples):
        tokenized = tokenizer(
            examples["tokens"],
            truncation=True,
            is_split_into_words=True,
            max_length=DEFAULTS.max_length,
        )
        labels = []
        for index, label in enumerate(examples["labels"]):
            word_ids = tokenized.word_ids(batch_index=index)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(label[word_idx] if label_all_tokens else -100)
                previous_word_idx = word_idx
            labels.append(label_ids)
        tokenized["labels"] = labels
        return tokenized

    return encode


def run(validate_only: bool = False) -> None:
    train_rows = read_bio(ANNOTATED_DIR / "train.bio")
    valid_rows = read_bio(ANNOTATED_DIR / "valid.bio")
    print(f"NER records: train={len(train_rows)}, valid={len(valid_rows)}")
    if validate_only:
        return
    assert_trainable_split("NER", len(train_rows), len(valid_rows))

    from transformers import (
        AutoModelForTokenClassification,
        AutoTokenizer,
        DataCollatorForTokenClassification,
        Trainer,
        TrainingArguments,
        set_seed,
    )
    from training.metrics import compute_ner_metrics

    label_to_id = {label: index for index, label in enumerate(NER_LABELS)}
    id_to_label = {index: label for label, index in label_to_id.items()}
    set_seed(DEFAULTS.seed)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(NER_LABELS),
        id2label=id_to_label,
        label2id=label_to_id,
    )

    train_dataset = build_dataset(ANNOTATED_DIR / "train.bio", label_to_id)
    valid_dataset = build_dataset(ANNOTATED_DIR / "valid.bio", label_to_id)
    train_dataset = train_dataset.map(tokenize_and_align_labels(tokenizer), batched=True)
    valid_dataset = valid_dataset.map(tokenize_and_align_labels(tokenizer), batched=True)

    output_dir = MODELS_DIR / "symptom_ner"
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
        metric_for_best_model="f1",
        report_to="none",
        seed=DEFAULTS.seed,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForTokenClassification(tokenizer),
        compute_metrics=compute_ner_metrics(NER_LABELS),
    )
    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    print(f"Saved NER model to {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune PhoBERT for symptom NER.")
    parser.add_argument("--validate-only", action="store_true", help="Only check that BIO data is readable.")
    args = parser.parse_args()
    run(validate_only=args.validate_only)


if __name__ == "__main__":
    main()
