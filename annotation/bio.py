from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from crawler.config import DATA_DIR
from crawler.io_utils import read_jsonl
from processing.symptoms import load_symptoms
from processing.text_cleaning import normalize_unicode


TOKEN_RE = re.compile(r"\w+|[^\w\s]", flags=re.UNICODE)


@dataclass(frozen=True)
class Token:
    text: str
    start: int
    end: int


def tokenize_with_offsets(text: str) -> list[Token]:
    return [Token(match.group(), match.start(), match.end()) for match in TOKEN_RE.finditer(text)]


def find_spans(text: str, phrases: list[str]) -> list[tuple[int, int, str]]:
    lowered = normalize_unicode(text.lower())
    spans: list[tuple[int, int, str]] = []
    for phrase in phrases:
        pattern = r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)"
        for match in re.finditer(pattern, lowered, flags=re.UNICODE):
            spans.append((match.start(), match.end(), phrase))
    spans.sort(key=lambda span: (span[0], -(span[1] - span[0])))

    selected: list[tuple[int, int, str]] = []
    occupied: set[int] = set()
    for start, end, phrase in spans:
        positions = set(range(start, end))
        if occupied.intersection(positions):
            continue
        selected.append((start, end, phrase))
        occupied.update(positions)
    return selected


def label_tokens(text: str, symptoms: list[str]) -> list[tuple[str, str]]:
    tokens = tokenize_with_offsets(text)
    spans = find_spans(text, symptoms)
    labels = ["O"] * len(tokens)

    for start, end, _phrase in spans:
        span_token_indexes = [
            index
            for index, token in enumerate(tokens)
            if token.start < end and token.end > start and re.search(r"\w", token.text, flags=re.UNICODE)
        ]
        for offset, token_index in enumerate(span_token_indexes):
            labels[token_index] = "B-SYMPTOM" if offset == 0 else "I-SYMPTOM"

    return [(token.text, labels[index]) for index, token in enumerate(tokens)]


def sentence_records_from_articles(clean_articles_path: Path) -> list[dict]:
    articles = read_jsonl(clean_articles_path)
    rows: list[dict] = []
    for article in articles:
        article_id = str(article.get("article_id", ""))
        for index, sentence in enumerate(article.get("sentences", [])):
            rows.append(
                {
                    "sentence_id": f"{article_id}-{index:04d}",
                    "article_id": article_id,
                    "url": article.get("url", ""),
                    "title": article.get("title", ""),
                    "specialty": article.get("specialty", ""),
                    "text": sentence,
                }
            )
    return rows


def build_bio_sentences(sentence_rows: list[dict]) -> list[dict]:
    symptoms = load_symptoms(DATA_DIR / "dictionaries" / "symptom_seed.txt")
    output: list[dict] = []
    for row in sentence_rows:
        token_labels = label_tokens(row["text"], symptoms)
        if any(label != "O" for _token, label in token_labels):
            output.append({**row, "token_labels": token_labels})
    return output


def write_bio_file(rows: list[dict], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    sentence_count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(f"# sentence_id={row['sentence_id']}\n")
            handle.write(f"# article_id={row['article_id']}\n")
            handle.write(f"# source_url={row.get('url', '')}\n")
            for token, label in row["token_labels"]:
                handle.write(f"{token}\t{label}\n")
            handle.write("\n")
            sentence_count += 1
    return sentence_count
