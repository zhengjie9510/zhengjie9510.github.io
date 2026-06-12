#!/usr/bin/env python3
"""
reader.py — Fetch and filter articles from RSS/Atom feeds, output concise summaries

Usage:
  python reader.py <URL> [URL2 ...] [options]

Filter options (defaults to latest 10 if none specified):
  --days  N       Articles from the last N days
  --hours N       Articles from the last N hours
  --top   N       Latest N articles (no time limit)

Other options:
  --sources FILE  Read URLs from a file (one per line, # for comments)
  --max N         Max items per feed (default: 20)
  --no-content    Output titles + links + dates only, no summary
  --json          Output JSON (for programmatic use)

Examples:
  python reader.py https://openai.com/blog/rss.xml --days 1
  python reader.py https://hnrss.org/frontpage --top 5
  python reader.py --sources feeds.txt --hours 12 --max 10
"""

import sys
import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

try:
    import feedparser
except ImportError:
    print("[Error] Missing feedparser dependency. Run: pip3 install feedparser", file=sys.stderr)
    sys.exit(1)


# ── Windows compat: force UTF-8 on stdout/stderr ────────────────────────────
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ── Arg parsing ──────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="RSS/Atom feed fetcher and filter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("urls", nargs="*", help="RSS/Atom feed URLs")
    p.add_argument("--sources", help="Read URLs from file (one per line, # for comments)")
    p.add_argument("--days", type=float, help="Articles from the last N days")
    p.add_argument("--hours", type=float, help="Articles from the last N hours")
    p.add_argument("--top", type=int, help="Latest N articles (no time limit)")
    p.add_argument("--max", type=int, default=20, help="Max items per feed (default: 20)")
    p.add_argument("--no-content", action="store_true", help="Titles + links + dates only")
    p.add_argument("--json", action="store_true", help="Output JSON")
    return p.parse_args()


# ── Fetching ─────────────────────────────────────────────────────────────────

def read_feed(url, timeout=15):
    """Fetch and parse an RSS/Atom feed. Returns (feed_title, items) or raises."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; RSSFetcher/2.0)",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()

    # Detect encoding
    encoding = "utf-8"
    content_type = resp.headers.get("Content-Type", "")
    import re
    m = re.search(r"charset=([^\s;]+)", content_type, re.IGNORECASE)
    if m:
        encoding = m.group(1).strip('"\'')
    xml_text = raw.decode(encoding, errors="replace")

    # Parse with feedparser
    feed = feedparser.parse(xml_text)

    if feed.bozo and not feed.entries:
        raise ValueError(f"Parse error: {feed.bozo_exception}")

    feed_title = feed.feed.get("title", "") or ""
    items = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()

        # Extract publish date
        pub = None
        for date_field in ("published_parsed", "updated_parsed"):
            parsed = entry.get(date_field)
            if parsed:
                try:
                    pub = datetime(*parsed[:6], tzinfo=timezone.utc)
                    break
                except (TypeError, ValueError):
                    pass

        # Extract summary
        content = ""
        if entry.get("summary"):
            content = entry.summary
        elif entry.get("content"):
            content = entry.content[0].get("value", "")
        # Strip HTML tags
        if content:
            content = re.sub(r"<[^>]+>", " ", content)
            content = re.sub(r"\s+", " ", content).strip()
            if len(content) > 200:
                content = content[:200] + "…"

        if title or link:
            items.append({
                "title": title or "Untitled",
                "link": link,
                "content": content,
                "date": pub,
            })

    return feed_title, items


# ── Filtering ────────────────────────────────────────────────────────────────

def filter_items(items, args):
    """Filter items by time and count."""
    now = datetime.now(timezone.utc)

    if args.days:
        cutoff = now - timedelta(days=args.days)
        items = [i for i in items if i["date"] and i["date"] >= cutoff]
    elif args.hours:
        cutoff = now - timedelta(hours=args.hours)
        items = [i for i in items if i["date"] and i["date"] >= cutoff]

    # Sort by date descending, undated items last
    items.sort(
        key=lambda i: i["date"] or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    limit = args.top if args.top else args.max
    return items[:limit]


# ── Output ───────────────────────────────────────────────────────────────────

def fmt_date(dt):
    if not dt:
        return "Unknown date"
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def render_markdown(feed_title, items, url, no_content):
    """Render items as Markdown."""
    lines = [f"## {feed_title or url}"]
    if not items:
        lines.append("(No articles in this time range)")
        return "\n".join(lines)
    for i, item in enumerate(items, 1):
        lines.append(f"\n{i}. **{item['title']}** · {fmt_date(item['date'])}")
        lines.append(f"   {item['link']}")
        if not no_content and item["content"]:
            lines.append(f"   {item['content']}")
    return "\n".join(lines)


def render_json(feed_title, items, url):
    """Render items as JSON."""
    data = {
        "feed": feed_title or url,
        "items": [
            {
                "title": item["title"],
                "link": item["link"],
                "date": fmt_date(item["date"]),
                "content": item["content"],
            }
            for item in items
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


# ── Main ─────────────────────────────────────────────────────────────────────

def load_urls(args):
    """Collect all URLs from args and sources file."""
    urls = list(args.urls)
    if args.sources:
        try:
            try:
                with open(args.sources, encoding="utf-8") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(args.sources, encoding="gbk", errors="replace") as f:
                    lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)
        except FileNotFoundError:
            print(f"[Error] File not found: {args.sources}", file=sys.stderr)
            sys.exit(1)
    return urls


def main():
    args = parse_args()
    urls = load_urls(args)

    if not urls:
        print("[Error] Provide at least one RSS/Atom URL, or use --sources FILE", file=sys.stderr)
        sys.exit(1)

    # Filter description
    if args.days:
        filter_desc = f"Last {args.days} day{'s' if args.days != 1 else ''}"
    elif args.hours:
        filter_desc = f"Last {args.hours} hour{'s' if args.hours != 1 else ''}"
    elif args.top:
        filter_desc = f"Latest {args.top}"
    else:
        filter_desc = f"Latest {args.max}"

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # JSON mode: collect all results, then output
    if args.json:
        all_results = []
        for url in urls:
            try:
                feed_title, items = read_feed(url)
                items = filter_items(items, args)
                all_results.append({
                    "feed": feed_title or url,
                    "url": url,
                    "items": [
                        {
                            "title": item["title"],
                            "link": item["link"],
                            "date": fmt_date(item["date"]),
                            "content": item["content"],
                        }
                        for item in items
                    ],
                })
            except Exception as e:
                all_results.append({
                    "feed": url,
                    "url": url,
                    "error": str(e),
                    "items": [],
                })
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
        return

    # Markdown mode
    print(f"# RSS Summary · {filter_desc} · {now_str}\n")

    for url in urls:
        try:
            feed_title, items = read_feed(url)
            items = filter_items(items, args)
            print(render_markdown(feed_title, items, url, args.no_content))
            print()
        except urllib.error.HTTPError as e:
            print(f"## {url}\n[Fetch failed] HTTP {e.code}: {e.reason}\n")
        except urllib.error.URLError as e:
            print(f"## {url}\n[Fetch failed] Connection error: {e.reason}\n")
        except Exception as e:
            print(f"## {url}\n[Fetch failed] {e}\n")


if __name__ == "__main__":
    main()
