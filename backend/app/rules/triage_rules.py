from __future__ import annotations

import re


RED_FLAG_GROUPS = [
    ("đau ngực", "khó thở"),
    ("đau ngực", "vã mồ hôi"),
    ("đau ngực dữ dội",),
    ("liệt",),
    ("yếu liệt",),
    ("méo miệng",),
    ("nói khó",),
    ("co giật",),
    ("bất tỉnh",),
    ("ngất",),
    ("chảy máu nhiều",),
    ("chảy máu không cầm",),
    ("đau đầu dữ dội", "cứng gáy"),
    ("đau đầu đột ngột",),
    ("khó thở nặng",),
    ("tím tái",),
]

URGENT_KEYWORDS = [
    "sốt cao",
    "sốt trên 39",
    "khó thở",
    "đau dữ dội",
    "kéo dài",
    "nặng lên",
    "nôn liên tục",
    "tiêu chảy nhiều",
]

HIGH_RISK_GROUPS = {"trẻ nhỏ", "phụ nữ mang thai", "người cao tuổi", "bệnh nền", "suy giảm miễn dịch"}


def phrase_present(text: str, phrase: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    for match in re.finditer(pattern, text.lower(), flags=re.UNICODE):
        prefix = text.lower()[max(0, match.start() - 18) : match.start()].strip()
        if re.search(r"(không|chưa|không kèm|không có)$", prefix, flags=re.UNICODE):
            continue
        return True
    return False


def has_red_flag(text: str, explicit_flags: list[str]) -> bool:
    combined = " ".join([text, " ".join(explicit_flags)])
    return any(all(phrase_present(combined, phrase) for phrase in group) for group in RED_FLAG_GROUPS)


def classify_triage(text: str, discomfort_level: int, age: int, risk_groups: list[str], explicit_flags: list[str]) -> tuple[str, str, str]:
    normalized_risk_groups = {group.strip().lower() for group in risk_groups}
    high_risk = bool(normalized_risk_groups.intersection(HIGH_RISK_GROUPS)) or age >= 70 or age <= 5

    if has_red_flag(text, explicit_flags) or (age <= 5 and any(phrase_present(text, keyword) for keyword in ("sốt cao", "co giật", "li bì"))):
        return (
            "EMERGENCY",
            "critical",
            "Triệu chứng có dấu hiệu nguy hiểm. Vui lòng gọi cấp cứu hoặc đến cơ sở y tế gần nhất ngay.",
        )
    if discomfort_level >= 8 or any(phrase_present(text, keyword) for keyword in URGENT_KEYWORDS):
        return (
            "URGENT_CARE",
            "high" if high_risk else "medium",
            "Nên đi khám sớm trong ngày hoặc liên hệ cơ sở y tế nếu triệu chứng tăng.",
        )
    if high_risk or discomfort_level >= 5:
        return (
            "BOOK_APPOINTMENT",
            "medium",
            "Nên đặt lịch khám để được bác sĩ đánh giá, nhất là khi triệu chứng kéo dài hoặc lặp lại.",
        )
    return (
        "SELF_CARE",
        "low",
        "Có thể theo dõi và chăm sóc tạm thời nếu triệu chứng nhẹ, không kéo dài hoặc không nặng lên.",
    )


def temporary_advice_for(triage_label: str) -> list[str]:
    if triage_label == "EMERGENCY":
        return [
            "Ngừng vận động mạnh và giữ tư thế dễ thở.",
            "Không tự lái xe nếu đang đau ngực, khó thở, chóng mặt hoặc yếu liệt.",
            "Gọi người thân hoặc cấp cứu hỗ trợ ngay.",
        ]
    if triage_label == "URGENT_CARE":
        return [
            "Theo dõi nhiệt độ, nhịp thở và mức độ đau.",
            "Uống đủ nước nếu không có chống chỉ định.",
            "Chuẩn bị thông tin triệu chứng, thời điểm bắt đầu và thuốc đang dùng trước khi đi khám.",
        ]
    if triage_label == "BOOK_APPOINTMENT":
        return [
            "Ghi lại triệu chứng chính, thời gian xuất hiện và yếu tố làm nặng hơn.",
            "Đặt lịch khám chuyên khoa phù hợp.",
            "Đi khám sớm hơn nếu triệu chứng tăng nhanh hoặc xuất hiện dấu hiệu nguy hiểm.",
        ]
    return [
        "Nghỉ ngơi và theo dõi triệu chứng.",
        "Uống đủ nước nếu phù hợp với tình trạng sức khỏe.",
        "Đi khám nếu triệu chứng kéo dài, tái phát hoặc nặng lên.",
    ]
