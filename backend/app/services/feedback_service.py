from __future__ import annotations

import json
from datetime import datetime, timezone

from crawler.config import DATA_DIR
from crawler.io_utils import ensure_parent
from backend.app.models.schemas import FeedbackRequest


def save_feedback(payload: FeedbackRequest) -> None:
    path = DATA_DIR / "feedback" / "feedback.jsonl"
    ensure_parent(path)
    record = {
        "session_id": payload.session_id,
        "rating": payload.rating,
        "comment": payload.comment,
        "triage_label": payload.triage_label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
