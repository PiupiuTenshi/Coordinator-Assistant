from __future__ import annotations

from pathlib import Path

from crawler.config import PROJECT_ROOT


class PhoBertModelAdapter:
    """Lazy placeholder for Phase 3 models.

    The backend works without trained models by using dictionary/rule fallback.
    When `models/symptom_ner` and `models/triage_classifier` contain real
    Hugging Face artifacts, this adapter can be extended to load them once.
    """

    def __init__(self) -> None:
        self.ner_model_dir = PROJECT_ROOT / "models" / "symptom_ner"
        self.triage_model_dir = PROJECT_ROOT / "models" / "triage_classifier"

    def model_available(self, model_dir: Path) -> bool:
        return (model_dir / "config.json").exists()

    def status(self) -> dict:
        return {
            "ner_available": self.model_available(self.ner_model_dir),
            "triage_available": self.model_available(self.triage_model_dir),
            "fallback": "dictionary_and_rules",
        }


model_adapter = PhoBertModelAdapter()
