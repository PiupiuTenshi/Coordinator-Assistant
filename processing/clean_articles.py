from __future__ import annotations

import argparse
from pathlib import Path

from crawler.config import DATA_DIR
from crawler.io_utils import read_jsonl, write_jsonl
from processing.symptoms import find_symptoms, load_symptoms, write_symptom_dictionary
from processing.text_cleaning import clean_text, content_fingerprint, split_sentences


def clean_articles(records: list[dict]) -> list[dict]:
    symptoms = load_symptoms()
    seen: set[str] = set()
    cleaned_records: list[dict] = []

    for record in records:
        content_clean = clean_text(record.get("content_raw", ""))
        fingerprint = content_fingerprint(content_clean)
        if not content_clean or fingerprint in seen:
            continue
        seen.add(fingerprint)

        sentences = split_sentences(content_clean)
        symptom_candidates = sorted(set(find_symptoms("\n".join([record.get("title", ""), content_clean]), symptoms)))
        cleaned = {
            **record,
            "content_clean": content_clean,
            "sentences": sentences,
            "sentence_count": len(sentences),
            "word_count": len(content_clean.split()),
            "symptom_candidates": symptom_candidates,
        }
        cleaned_records.append(cleaned)
    return cleaned_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean raw medical articles and build symptom dictionary.")
    parser.add_argument("--input", type=Path, default=DATA_DIR / "raw" / "raw_articles.jsonl")
    parser.add_argument("--output", type=Path, default=DATA_DIR / "clean" / "clean_articles.jsonl")
    parser.add_argument("--dictionary-output", type=Path, default=DATA_DIR / "dictionaries" / "symptom_dictionary.csv")
    args = parser.parse_args()

    raw_records = read_jsonl(args.input)
    cleaned_records = clean_articles(raw_records)
    article_count = write_jsonl(cleaned_records, args.output)
    symptom_count = write_symptom_dictionary(cleaned_records, args.dictionary_output)
    print(f"Wrote {article_count} clean records to {args.output}")
    print(f"Wrote {symptom_count} symptom rows to {args.dictionary_output}")


if __name__ == "__main__":
    main()
