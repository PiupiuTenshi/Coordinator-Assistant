from __future__ import annotations

import argparse
from pathlib import Path

from annotation.bio import build_bio_sentences, sentence_records_from_articles, write_bio_file
from annotation.split import group_by_split
from annotation.triage import build_triage_rows, write_triage_csv
from crawler.config import DATA_DIR


def require_input(path: Path) -> None:
    if not path.exists():
        raise SystemExit(
            f"Missing input file: {path}\n"
            "Run phase 1 first, for example:\n"
            "python phase1_pipeline.py --demo"
        )


def run_phase2(clean_articles_path: Path) -> None:
    require_input(clean_articles_path)

    annotated_dir = DATA_DIR / "annotated"
    sentence_rows = sentence_records_from_articles(clean_articles_path)
    bio_rows = build_bio_sentences(sentence_rows)
    triage_rows = build_triage_rows(sentence_rows)

    bio_splits = group_by_split(bio_rows)
    triage_splits = group_by_split(triage_rows)

    bio_counts = {
        split: write_bio_file(rows, annotated_dir / f"{split}.bio")
        for split, rows in bio_splits.items()
    }
    triage_counts = {
        split: write_triage_csv(rows, annotated_dir / f"triage_{split}.csv")
        for split, rows in triage_splits.items()
    }

    summary_path = annotated_dir / "phase2_summary.md"
    summary_path.write_text(
        build_summary(len(sentence_rows), bio_counts, triage_counts),
        encoding="utf-8",
    )

    print(f"Sentences loaded: {len(sentence_rows)}")
    print(f"BIO counts: {bio_counts}")
    print(f"Triage counts: {triage_counts}")
    print(f"Summary: {summary_path}")


def build_summary(total_sentences: int, bio_counts: dict[str, int], triage_counts: dict[str, int]) -> str:
    lines = [
        "# Phase 2 Annotation Dataset Summary",
        "",
        f"- Total candidate sentences from clean articles: {total_sentences}",
        f"- BIO train/valid/test: {bio_counts.get('train', 0)}/{bio_counts.get('valid', 0)}/{bio_counts.get('test', 0)}",
        f"- Triage train/valid/test: {triage_counts.get('train', 0)}/{triage_counts.get('valid', 0)}/{triage_counts.get('test', 0)}",
        "",
        "## Outputs",
        "",
        "- `data/annotated/train.bio`",
        "- `data/annotated/valid.bio`",
        "- `data/annotated/test.bio`",
        "- `data/annotated/triage_train.csv`",
        "- `data/annotated/triage_valid.csv`",
        "- `data/annotated/triage_test.csv`",
        "",
        "## Review Notes",
        "",
        "- Các nhãn được tạo tự động bằng từ điển/rule nên chỉ là gợi ý ban đầu.",
        "- Người gán nhãn cần sửa span triệu chứng, thêm duration/severity/body part nếu cần.",
        "- Nhãn `EMERGENCY` phải được review kỹ để tránh bỏ sót ca nguy hiểm.",
        "- Chia tập theo `article_id` để hạn chế rò rỉ cùng bài giữa train và test.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run phase 2: generate BIO and triage annotation seeds.")
    parser.add_argument("--input", type=Path, default=DATA_DIR / "clean" / "clean_articles.jsonl")
    args = parser.parse_args()
    run_phase2(args.input)


if __name__ == "__main__":
    main()
