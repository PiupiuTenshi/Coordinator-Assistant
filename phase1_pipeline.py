from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from crawler.config import DATA_DIR
from crawler.crawl_vinmec import crawl_urls
from crawler.io_utils import read_lines
from processing.clean_articles import clean_articles
from processing.quality_report import build_quality_report
from processing.symptoms import write_symptom_dictionary
from crawler.io_utils import read_jsonl, write_jsonl


def run_pipeline(urls_path: Path, skip_crawl: bool = False, skip_robots: bool = False, demo: bool = False) -> None:
    raw_path = DATA_DIR / "raw" / "raw_articles.jsonl"
    sample_raw_path = DATA_DIR / "raw" / "raw_articles.sample.jsonl"
    clean_path = DATA_DIR / "clean" / "clean_articles.jsonl"
    dictionary_path = DATA_DIR / "dictionaries" / "symptom_dictionary.csv"
    report_path = DATA_DIR / "reports" / "phase1_quality_report.md"

    if demo:
        if not sample_raw_path.exists():
            raise SystemExit(f"Demo file not found: {sample_raw_path}")
        shutil.copyfile(sample_raw_path, raw_path)
        skip_crawl = True
        print(f"Demo mode: copied {sample_raw_path} to {raw_path}")

    if not skip_crawl:
        urls = read_lines(urls_path)
        if not urls:
            raise SystemExit(
                "No URLs found in "
                f"{urls_path}.\n"
                "Add one public article URL per line, or run demo data with:\n"
                "python phase1_pipeline.py --demo"
            )
        crawl_urls(urls, raw_path, skip_robots=skip_robots)

    raw_records = read_jsonl(raw_path)
    cleaned_records = clean_articles(raw_records)
    write_jsonl(cleaned_records, clean_path)
    write_symptom_dictionary(cleaned_records, dictionary_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_quality_report(cleaned_records), encoding="utf-8")

    print(f"Raw: {raw_path}")
    print(f"Clean: {clean_path}")
    print(f"Dictionary: {dictionary_path}")
    print(f"Report: {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run phase 1: crawl, clean, dictionary, quality report.")
    parser.add_argument("--urls", type=Path, default=DATA_DIR / "input" / "sample_urls.txt")
    parser.add_argument("--skip-crawl", action="store_true", help="Use existing data/raw/raw_articles.jsonl.")
    parser.add_argument("--skip-robots", action="store_true", help="Only use for local cached/demo HTML.")
    parser.add_argument("--demo", action="store_true", help="Use bundled sample raw data instead of crawling URLs.")
    args = parser.parse_args()
    run_pipeline(args.urls, skip_crawl=args.skip_crawl, skip_robots=args.skip_robots, demo=args.demo)


if __name__ == "__main__":
    main()
