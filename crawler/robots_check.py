from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

from crawler.config import DEFAULT_CONFIG, CrawlConfig


@dataclass
class RobotsResult:
    url: str
    robots_url: str
    allowed: bool
    checked: bool
    reason: str


def robots_url_for(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def is_allowed_by_domain(url: str, config: CrawlConfig = DEFAULT_CONFIG) -> bool:
    hostname = (urlparse(url).hostname or "").lower()
    return hostname in config.allowed_domains


def check_robots(url: str, config: CrawlConfig = DEFAULT_CONFIG) -> RobotsResult:
    robots_url = robots_url_for(url)
    if not is_allowed_by_domain(url, config):
        return RobotsResult(url, robots_url, False, False, "Domain is not in the allowlist.")

    parser = RobotFileParser()
    parser.set_url(robots_url)
    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": config.user_agent},
            timeout=config.request_timeout,
        )
        if response.status_code >= 400:
            return RobotsResult(url, robots_url, False, True, f"robots.txt returned {response.status_code}.")
        parser.parse(response.text.splitlines())
    except requests.RequestException as exc:
        return RobotsResult(url, robots_url, False, False, f"Could not fetch robots.txt: {exc}")

    allowed = parser.can_fetch(config.user_agent, url)
    reason = "Allowed by robots.txt." if allowed else "Blocked by robots.txt."
    return RobotsResult(url, robots_url, allowed, True, reason)
