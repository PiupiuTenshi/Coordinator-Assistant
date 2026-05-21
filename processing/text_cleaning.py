from __future__ import annotations

import re
import unicodedata


SENTENCE_RE = re.compile(r"(?<=[.!?。！？])\s+")
NOISE_PHRASES = (
    "để đặt lịch khám",
    "tải ứng dụng",
    "quý khách vui lòng",
    "đăng ký nhận tư vấn",
)


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def clean_text(text: str) -> str:
    text = normalize_unicode(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = []
    for line in text.splitlines():
        stripped = re.sub(r"\s+", " ", line).strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if any(phrase in lowered for phrase in NOISE_PHRASES):
            continue
        if len(stripped) < 20:
            continue
        lines.append(stripped)
    return "\n".join(lines)


def split_sentences(text: str) -> list[str]:
    sentences: list[str] = []
    for paragraph in clean_text(text).splitlines():
        for sentence in SENTENCE_RE.split(paragraph):
            sentence = sentence.strip(" -•\t")
            if len(sentence) >= 20:
                sentences.append(sentence)
    return sentences


def content_fingerprint(text: str) -> str:
    lowered = clean_text(text).lower()
    return re.sub(r"\W+", "", lowered, flags=re.UNICODE)
