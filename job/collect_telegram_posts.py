#!/usr/bin/env python3
"""Fetch t.me/s/* channel previews and RSS feeds; emit JSON lines with concrete post URLs + text snippets."""
from __future__ import annotations

import html as html_lib
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

UA = "Mozilla/5.0 (compatible; vacancy-collector/1.0; +https://dzmitrykashlach.github.io)"


def fetch(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


class MessageExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_text = False
        self._text_depth = 0
        self._pending_post: str | None = None
        self._buf: list[str] = []
        self.messages: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: v for k, v in attrs if v is not None}
        cls = ad.get("class", "") or ""
        classes = cls.split()
        if tag == "div" and "tgme_widget_message" in classes and "tgme_widget_message_text" not in cls:
            dp = ad.get("data-post")
            if dp:
                self._pending_post = dp
        if (
            self._pending_post
            and tag == "div"
            and "tgme_widget_message_text" in classes
            and not self._in_text
        ):
            self._in_text = True
            self._text_depth = 1
            self._buf = []
        elif self._in_text and tag == "div":
            self._text_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._in_text:
            if tag == "div":
                self._text_depth -= 1
                if self._text_depth <= 0:
                    raw = "".join(self._buf)
                    raw = re.sub(r"\s+", " ", raw).strip()
                    post = self._pending_post
                    if post and raw:
                        chan, pid = post.split("/", 1)
                        url = f"https://t.me/{chan}/{pid}"
                        self.messages.append((url, html_lib.unescape(raw)[:900]))
                    self._in_text = False
                    self._pending_post = None
                    self._buf = []

    def handle_data(self, data: str) -> None:
        if self._in_text:
            self._buf.append(data)


def extract_tme_posts(page_url: str) -> list[tuple[str, str]]:
    html = fetch(page_url)
    p = MessageExtractor()
    p.feed(html)
    # Newest-first in page: reverse to ascending id for checkpoint friendliness — keep as returned (usually newest first)
    return p.messages


def rss_items(rss_url: str) -> list[tuple[str, str]]:
    xml = fetch(rss_url)
    root = ET.fromstring(xml)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items: list[tuple[str, str]] = []
    for ch in root.findall(".//item"):
        title_el = ch.find("title")
        link_el = ch.find("link")
        title = (title_el.text or "").strip() if title_el is not None else ""
        link = (link_el.text or "").strip() if link_el is not None else ""
        if link:
            items.append((link, title[:500]))
    if not items:
        for ent in root.findall(".//atom:entry", ns):
            link_el = ent.find("atom:link", ns)
            title_el = ent.find("atom:title", ns)
            title = (title_el.text or "").strip() if title_el is not None else ""
            href = link_el.get("href", "") if link_el is not None else ""
            if href:
                items.append((href, title[:500]))
    return items


def parse_channel_urls(body: str) -> list[str]:
    """Extract channel page URLs from job-channels.md (table or list). One URL per line."""
    urls: list[str] = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("```"):
            continue
        if s.startswith("|"):
            parts = [p.strip() for p in s.split("|")]
            parts = [p for p in parts if p]
            if not parts:
                continue
            sep = parts[0]
            if sep and set(sep) <= {":", "-"}:
                continue
            header = parts[0].lower()
            if header in ("url", "channel", "channel url", "links"):
                continue
            cell = parts[0]
            if cell.startswith("http"):
                urls.append(cell.split()[0])
        elif s.startswith("- ") and "http" in s:
            m = re.search(r"https://[^\s)|>`]+", s)
            if m:
                urls.append(m.group(0).rstrip(").,"))
        elif s.startswith("http"):
            urls.append(s.split()[0])

    seen: set[str] = set()
    out: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def jvm_backend_hint(text: str) -> bool:
    t = text.lower()
    signals = (
        "java",
        "kotlin",
        "jvm",
        "spring",
        "micronaut",
        "ktor",
        "hibernate",
        "graalvm",
    )
    if not any(s in t for s in signals):
        return False
    anti = (
        "frontend only",
        "only react",
        "vue.js developer",
        "flutter",
        "ios developer",
        "android developer",
        "1c разработ",
    )
    if any(a in t for a in anti) and "java" not in t and "kotlin" not in t:
        return False
    return True


def main() -> None:
    channels_path = sys.argv[1] if len(sys.argv) > 1 else "job-channels.md"
    with open(channels_path, encoding="utf-8") as f:
        body = f.read()
    urls = parse_channel_urls(body)

    out: list[dict] = []
    for u in urls:
        if "/t.me/s/" in u or u.startswith("https://t.me/s/"):
            try:
                posts = extract_tme_posts(u)
                for link, snippet in posts:
                    out.append(
                        {
                            "channel_page": u,
                            "post_url": link,
                            "snippet": snippet,
                            "jvm_hint": jvm_backend_hint(snippet),
                        }
                    )
            except Exception as e:
                out.append({"channel_page": u, "error": str(e)})
        elif "tg.i-c-a.su/rss" in u:
            try:
                for link, title in rss_items(u):
                    text = title
                    out.append(
                        {
                            "channel_page": u,
                            "post_url": link,
                            "snippet": text,
                            "jvm_hint": jvm_backend_hint(text),
                        }
                    )
            except Exception as e:
                out.append({"channel_page": u, "error": str(e)})
        else:
            out.append({"channel_page": u, "skip": True})

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
