from __future__ import annotations

from collections import Counter

if __package__ is None or __package__ == "":
    from pathlib import Path
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from training.config import NER_LABELS, TRIAGE_LABELS
from training.data import dataset_stats, read_bio, read_triage_csv
from training.config import ANNOTATED_DIR


def main() -> None:
    stats = dataset_stats()
    print("Dataset stats:")
    print(stats)

    unknown_ner = Counter()
    for split in ("train", "valid", "test"):
        for row in read_bio(ANNOTATED_DIR / f"{split}.bio"):
            unknown_ner.update(label for label in row["ner_tags"] if label not in NER_LABELS)

    unknown_triage = Counter()
    triage_distribution = Counter()
    for split in ("train", "valid", "test"):
        for row in read_triage_csv(ANNOTATED_DIR / f"triage_{split}.csv"):
            label = row.get("triage_label", "")
            triage_distribution[label] += 1
            if label not in TRIAGE_LABELS:
                unknown_triage[label] += 1

    print(f"Unknown NER labels: {dict(unknown_ner)}")
    print(f"Unknown triage labels: {dict(unknown_triage)}")
    print(f"Triage distribution: {dict(triage_distribution)}")

    if unknown_ner or unknown_triage:
        raise SystemExit("Dataset contains unknown labels.")


if __name__ == "__main__":
    main()
