from __future__ import annotations

import hashlib
from collections import defaultdict


SplitName = str


def split_for_article(article_id: str) -> SplitName:
    bucket = int(hashlib.sha1(article_id.encode("utf-8")).hexdigest(), 16) % 100
    if bucket < 70:
        return "train"
    if bucket < 85:
        return "valid"
    return "test"


def group_by_split(items: list[dict]) -> dict[SplitName, list[dict]]:
    grouped: dict[SplitName, list[dict]] = defaultdict(list)
    for item in items:
        article_id = str(item.get("article_id") or item.get("source_id") or "")
        grouped[split_for_article(article_id)].append(item)
    return {split: grouped.get(split, []) for split in ("train", "valid", "test")}
