from __future__ import annotations

import argparse

from training.train_ner import run as run_ner
from training.train_triage import run as run_triage
from training.validate_phase3_data import main as validate_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Run phase 3 validation or PhoBERT fine-tuning.")
    parser.add_argument("--task", choices=["all", "ner", "triage"], default="all")
    parser.add_argument("--validate-only", action="store_true", help="Validate data without downloading/training models.")
    args = parser.parse_args()

    validate_data()
    if args.task in ("all", "ner"):
        run_ner(validate_only=args.validate_only)
    if args.task in ("all", "triage"):
        run_triage(validate_only=args.validate_only)


if __name__ == "__main__":
    main()
