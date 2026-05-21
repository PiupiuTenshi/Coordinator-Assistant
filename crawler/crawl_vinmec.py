from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

import requests

from crawler.config import DEFAULT_CONFIG, CrawlConfig, DATA_DIR
from crawler.io_utils import read_lines, write_jsonl
from crawler.parse_article import parse_article
from crawler.robots_check import check_robots


def cache_path_for(url: str, cache_dir: Path) -> Path:
    return cache_dir / f"{hashlib.sha1(url.encode('utf-8')).hexdigest()}.html"


def fetch_html(url: str, config: CrawlConfig = DEFAULT_CONFIG, use_cache: bool = True) -> str:
    config.cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_path_for(url, config.cache_dir)
    if use_cache and cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    last_error: Exception | None = None
    for attempt in range(config.max_retries + 1):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": config.user_agent},
                timeout=config.request_timeout,
            )
            response.raise_for_status()
            html = response.text
            cache_path.write_text(html, encoding="utf-8")
            time.sleep(config.delay_seconds)
            return html
        except requests.RequestException as exc:
            last_error = exc
            if attempt < config.max_retries:
                time.sleep(config.delay_seconds * (attempt + 1))
    raise RuntimeError(f"Could not fetch {url}: {last_error}")


def crawl_urls(urls: list[str], output_path: Path, skip_robots: bool = False) -> int:
    records = []
    for url in urls:
        if not skip_robots:
            robots = check_robots(url)
            if not robots.allowed:
                print(f"SKIP {url} - {robots.reason}")
                continue
        html = fetch_html(url)
        records.append(parse_article(url, html))
        print(f"OK {url}")
    return write_jsonl(records, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl public medical articles into raw_articles.jsonl.")
    parser.add_argument("--urls", type=Path, default=DATA_DIR / "input" / "sample_urls.txt")
    parser.add_argument("--output", type=Path, default=DATA_DIR / "raw" / "raw_articles.jsonl")
    parser.add_argument("--skip-robots", action="store_true", help="Only use for local cached/demo HTML.")
    args = parser.parse_args()

    urls = read_lines(args.urls)
    if not urls:
        raise SystemExit(f"No URLs found in {args.urls}")
    count = crawl_urls(urls, args.output, skip_robots=args.skip_robots)
    print(f"Wrote {count} records to {args.output}")


if __name__ == "__main__":
    main()
