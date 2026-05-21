from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from crawler.config import DATA_DIR, PROJECT_ROOT


MODEL_NAME = "vinai/phobert-base"
ANNOTATED_DIR = DATA_DIR / "annotated"
MODELS_DIR = PROJECT_ROOT / "models"


NER_LABELS = [
    "O",
    "B-SYMPTOM",
    "I-SYMPTOM",
    "B-BODY_PART",
    "I-BODY_PART",
    "B-DURATION",
    "I-DURATION",
    "B-SEVERITY",
    "I-SEVERITY",
    "B-FREQUENCY",
    "I-FREQUENCY",
    "B-RISK_FACTOR",
    "I-RISK_FACTOR",
]

TRIAGE_LABELS = ["SELF_CARE", "BOOK_APPOINTMENT", "URGENT_CARE", "EMERGENCY"]


@dataclass(frozen=True)
class TrainDefaults:
    max_length: int = 256
    learning_rate: float = 2e-5
    epochs: int = 3
    batch_size: int = 8
    weight_decay: float = 0.01
    seed: int = 42


DEFAULTS = TrainDefaults()
