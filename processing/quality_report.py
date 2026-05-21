from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

from crawler.config import DATA_DIR
from crawler.io_utils import read_jsonl


def build_quality_report(records: list[dict]) -> str:
    total_articles = len(records)
    total_sentences = sum(int(record.get("sentence_count", 0)) for record in records)
    total_words = sum(int(record.get("word_count", 0)) for record in records)
    symptom_counter: Counter[str] = Counter()
    source_counter: Counter[str] = Counter()

    for record in records:
        source_counter[record.get("source", "unknown")] += 1
        symptom_counter.update(record.get("symptom_candidates", []))

    avg_words = round(total_words / total_articles, 1) if total_articles else 0
    avg_sentences = round(total_sentences / total_articles, 1) if total_articles else 0
    top_symptoms = symptom_counter.most_common(20)

    lines = [
        "# Báo cáo chất lượng dữ liệu giai đoạn 1",
        "",
        f"- Thời điểm tạo: {datetime.now().isoformat(timespec='seconds')}",
        f"- Số bài viết sạch: {total_articles}",
        f"- Tổng số câu: {total_sentences}",
        f"- Tổng số từ: {total_words}",
        f"- Trung bình câu/bài: {avg_sentences}",
        f"- Trung bình từ/bài: {avg_words}",
        "",
        "## Phân bố nguồn",
        "",
    ]

    if source_counter:
        for source, count in source_counter.most_common():
            lines.append(f"- {source}: {count}")
    else:
        lines.append("- Chưa có dữ liệu.")

    lines.extend(["", "## Triệu chứng khớp từ điển nhiều nhất", ""])
    if top_symptoms:
        for symptom, count in top_symptoms:
            lines.append(f"- {symptom}: {count}")
    else:
        lines.append("- Chưa phát hiện triệu chứng từ từ điển.")

    lines.extend(
        [
            "",
            "## Checklist cần review thủ công",
            "",
            "- Kiểm tra lại quyền sử dụng dữ liệu và robots.txt cho từng nguồn.",
            "- Đọc mẫu 10-20 bài để loại bỏ đoạn quảng cáo hoặc nội dung lặp.",
            "- Kiểm tra triệu chứng bị match sai ngữ cảnh.",
            "- Bổ sung triệu chứng còn thiếu vào `data/dictionaries/symptom_seed.txt`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate phase 1 data quality report.")
    parser.add_argument("--input", type=Path, default=DATA_DIR / "clean" / "clean_articles.jsonl")
    parser.add_argument("--output", type=Path, default=DATA_DIR / "reports" / "phase1_quality_report.md")
    args = parser.parse_args()

    records = read_jsonl(args.input)
    report = build_quality_report(records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote report to {args.output}")


if __name__ == "__main__":
    main()
