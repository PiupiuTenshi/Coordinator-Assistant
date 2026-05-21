from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from crawler.config import DATA_DIR
from crawler.io_utils import read_lines, write_csv
from processing.text_cleaning import normalize_unicode


def load_symptoms(path: Path = DATA_DIR / "dictionaries" / "symptom_seed.txt") -> list[str]:
    symptoms = [normalize_unicode(line.lower()) for line in read_lines(path)]
    return sorted(set(symptoms), key=lambda item: (-len(item), item))


def find_symptoms(text: str, symptoms: list[str]) -> list[str]:
    lowered = normalize_unicode(text.lower())
    found: list[str] = []
    for symptom in symptoms:
        pattern = r"(?<!\w)" + re.escape(symptom) + r"(?!\w)"
        if re.search(pattern, lowered, flags=re.UNICODE):
            found.append(symptom)
    return found


def build_dictionary_rows(records: list[dict], symptoms: list[str]) -> list[dict]:
    counts: Counter[str] = Counter()
    examples: dict[str, str] = {}
    for record in records:
        text = "\n".join([record.get("title", ""), record.get("content_clean", "")])
        for symptom in find_symptoms(text, symptoms):
            counts[symptom] += 1
            examples.setdefault(symptom, record.get("title") or record.get("url", ""))

    rows = []
    for symptom in symptoms:
        rows.append(
            {
                "symptom": symptom,
                "normalized": symptom.replace(" ", "_"),
                "source": "seed_dictionary",
                "match_count": counts[symptom],
                "example": examples.get(symptom, ""),
            }
        )
    return rows


def write_symptom_dictionary(records: list[dict], output_path: Path) -> int:
    symptoms = load_symptoms()
    rows = build_dictionary_rows(records, symptoms)
    return write_csv(rows, output_path, ["symptom", "normalized", "source", "match_count", "example"])
