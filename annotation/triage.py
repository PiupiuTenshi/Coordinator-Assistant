from __future__ import annotations

import csv
import re
from pathlib import Path

from crawler.io_utils import ensure_parent
from processing.symptoms import find_symptoms, load_symptoms


EMERGENCY_PATTERNS = (
    ("đau ngực", "khó thở"),
    ("liệt",),
    ("méo miệng",),
    ("nói khó",),
    ("co giật",),
    ("ngất",),
    ("chảy máu",),
    ("cứng gáy",),
    ("vã mồ hôi", "đau ngực"),
)

URGENT_KEYWORDS = (
    "sốt cao",
    "khó thở",
    "đau dữ dội",
    "kéo dài",
    "nặng lên",
    "trẻ nhỏ",
    "phụ nữ mang thai",
    "người cao tuổi",
    "bệnh nền",
)

BOOK_KEYWORDS = (
    "đặt lịch",
    "đi khám",
    "khám chuyên khoa",
    "được đánh giá",
    "theo dõi",
)


def phrase_is_present(text: str, phrase: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    for match in re.finditer(pattern, text, flags=re.UNICODE):
        prefix = text[max(0, match.start() - 16) : match.start()].strip()
        if re.search(r"(không|chưa|không kèm|không có)$", prefix, flags=re.UNICODE):
            continue
        return True
    return False


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return all(phrase_is_present(lowered, phrase) for phrase in phrases)


def classify_sentence(text: str) -> tuple[str, str]:
    lowered = text.lower()
    if any(has_all(lowered, pattern) for pattern in EMERGENCY_PATTERNS):
        return "EMERGENCY", "Có dấu hiệu nguy hiểm theo rule seed, cần ưu tiên cấp cứu hoặc cơ sở y tế gần nhất."
    if any(phrase_is_present(lowered, keyword) for keyword in URGENT_KEYWORDS):
        return "URGENT_CARE", "Nên đi khám sớm trong ngày hoặc liên hệ cơ sở y tế nếu triệu chứng tăng."
    if any(phrase_is_present(lowered, keyword) for keyword in BOOK_KEYWORDS):
        return "BOOK_APPOINTMENT", "Nên đặt lịch khám để được bác sĩ đánh giá."
    return "SELF_CARE", "Có thể theo dõi và chăm sóc tạm thời nếu triệu chứng nhẹ, không kéo dài."


def build_triage_rows(sentence_rows: list[dict]) -> list[dict]:
    symptoms = load_symptoms()
    rows: list[dict] = []
    for row in sentence_rows:
        matched_symptoms = find_symptoms(row["text"], symptoms)
        if not matched_symptoms:
            continue
        label, action = classify_sentence(row["text"])
        rows.append(
            {
                "sentence_id": row["sentence_id"],
                "article_id": row["article_id"],
                "url": row.get("url", ""),
                "text": row["text"],
                "symptoms": "|".join(matched_symptoms),
                "triage_label": label,
                "suggested_action": action,
                "review_status": "auto_labeled_needs_review",
            }
        )
    return rows


def write_triage_csv(rows: list[dict], path: Path) -> int:
    ensure_parent(path)
    fieldnames = [
        "sentence_id",
        "article_id",
        "url",
        "text",
        "symptoms",
        "triage_label",
        "suggested_action",
        "review_status",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
