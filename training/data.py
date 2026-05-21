from __future__ import annotations

import csv
from pathlib import Path


def read_bio(path: Path) -> list[dict]:
    if not path.exists():
        return []

    rows: list[dict] = []
    metadata: dict[str, str] = {}
    tokens: list[str] = []
    labels: list[str] = []

    def flush() -> None:
        nonlocal metadata, tokens, labels
        if tokens:
            rows.append({"tokens": tokens, "ner_tags": labels, **metadata})
        metadata = {}
        tokens = []
        labels = []

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                flush()
                continue
            if line.startswith("#"):
                if "=" in line:
                    key, value = line[1:].strip().split("=", 1)
                    metadata[key.strip()] = value.strip()
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            token = " ".join(parts[:-1])
            label = parts[-1]
            tokens.append(token)
            labels.append(label)
    flush()
    return rows


def read_triage_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def dataset_stats() -> dict:
    from training.config import ANNOTATED_DIR

    stats = {
        "bio": {
            "train": len(read_bio(ANNOTATED_DIR / "train.bio")),
            "valid": len(read_bio(ANNOTATED_DIR / "valid.bio")),
            "test": len(read_bio(ANNOTATED_DIR / "test.bio")),
        },
        "triage": {
            "train": len(read_triage_csv(ANNOTATED_DIR / "triage_train.csv")),
            "valid": len(read_triage_csv(ANNOTATED_DIR / "triage_valid.csv")),
            "test": len(read_triage_csv(ANNOTATED_DIR / "triage_test.csv")),
        },
    }
    return stats


def assert_trainable_split(task: str, train_count: int, valid_count: int) -> None:
    if train_count == 0:
        raise SystemExit(f"No {task} training records found. Run phase2_pipeline.py first.")
    if valid_count == 0:
        raise SystemExit(
            f"No {task} validation records found. Add more articles or manually create a valid split before training. "
            "You can still run with --validate-only to inspect the dataset."
        )
