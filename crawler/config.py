from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


@dataclass(frozen=True)
class CrawlConfig:
    user_agent: str = "MedicalSymptomQRResearchBot/0.1 contact: your_email@example.com"
    request_timeout: int = 20
    delay_seconds: float = 3.0
    max_retries: int = 2
    cache_dir: Path = DATA_DIR / "cache" / "html"
    allowed_domains: tuple[str, ...] = ("vinmec.com", "www.vinmec.com")


DEFAULT_CONFIG = CrawlConfig()
