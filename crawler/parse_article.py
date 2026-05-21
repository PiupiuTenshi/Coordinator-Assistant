from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from bs4 import BeautifulSoup


NOISE_SELECTORS = [
    "script",
    "style",
    "noscript",
    "header",
    "footer",
    "nav",
    "aside",
    "form",
    ".breadcrumb",
    ".breadcrumbs",
    ".related",
    ".advertisement",
    ".ads",
]


def article_id_for(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_meta(soup: BeautifulSoup, *names: str) -> str:
    for name in names:
        node = soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"property": name})
        if node and node.get("content"):
            return normalize_space(str(node["content"]))
    return ""


def parse_article(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    for selector in NOISE_SELECTORS:
        for node in soup.select(selector):
            node.decompose()

    title_node = soup.find("h1")
    title = normalize_space(title_node.get_text(" ", strip=True)) if title_node else ""
    if not title:
        title = extract_meta(soup, "og:title", "twitter:title", "title")

    article_node = soup.find("article") or soup.find("main") or soup.body or soup
    paragraphs = []
    for node in article_node.find_all(["p", "li", "h2", "h3"]):
        text = normalize_space(node.get_text(" ", strip=True))
        if len(text) >= 30:
            paragraphs.append(text)

    content_raw = "\n".join(dict.fromkeys(paragraphs))
    parsed = urlparse(url)
    return {
        "article_id": article_id_for(url),
        "source": "vinmec" if "vinmec" in parsed.netloc else parsed.netloc,
        "url": url,
        "title": title,
        "category": extract_meta(soup, "article:section", "category"),
        "specialty": "",
        "published_date": extract_meta(soup, "article:published_time", "datePublished"),
        "updated_date": extract_meta(soup, "article:modified_time", "dateModified"),
        "content_raw": content_raw,
        "crawled_at": datetime.now(timezone.utc).isoformat(),
    }
