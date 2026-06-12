---
name: rss-reader
description: >
  Use this skill to read RSS/Atom feeds and get a summary of recent articles.
  Trigger when the user wants to check, fetch, or see recent/new/latest content
  from a source — a feed URL, a website name, a blog, or a feeds.txt file.
  Common patterns: "what's new on X", "get today's papers from arXiv",
  "check HN front page", "recent posts from this blog",
  "last N days/hours of updates", "latest N articles", "read my feeds.txt".
  Covers: time-based filtering (today, last N days/hours), quantity filtering
  (latest N), reading feed lists from files, multi-source aggregation.
  中文触发词：获取 RSS、看最新资讯、读取订阅源、查看更新、
  获取最近 N 天/小时的文章、显示最新 N 条。
  Do NOT use for: general web scraping, creating/generating RSS feeds,
  OPML import/export, or subscription management.
metadata:
  version: "1.0.0"
---

# RSS Reader Skill

Fetch articles from RSS/Atom feeds, filter by time or count, and output a concise summary.

Requires: Python 3.7+, feedparser.

## Script Path

```
skills/rss-reader/reader.py
```

## First-Time Setup

If `feedparser` is not installed:

```bash
pip3 install feedparser
```

> Use `pip3` on macOS/Linux, `pip` on Windows. If neither is found, try `python3 -m pip install feedparser`.

## Usage

Replace `python3` with `python` on Windows.

### Filter by Time

```bash
# Last 24 hours
python3 skills/rss-reader/reader.py <URL> --days 1

# Last 12 hours
python3 skills/rss-reader/reader.py <URL> --hours 12
```

### Filter by Count

```bash
# Latest 5 articles (no time limit)
python3 skills/rss-reader/reader.py <URL> --top 5

# Default: latest 10 articles
python3 skills/rss-reader/reader.py <URL>
```

### Multiple Feeds

```bash
python3 skills/rss-reader/reader.py <URL1> <URL2> <URL3> --days 1
```

### Read from a Sources File

```bash
python3 skills/rss-reader/reader.py --sources feeds.txt --days 1
```

`feeds.txt` format — one URL per line, `#` for comments:

```
# AI
https://openai.com/blog/rss.xml
https://www.anthropic.com/news/rss.xml

# Tech
https://hnrss.org/frontpage
```

### Titles and Links Only (saves tokens)

```bash
python3 skills/rss-reader/reader.py <URL> --days 1 --no-content
```

### Limit Max Items per Feed

```bash
python3 skills/rss-reader/reader.py --sources feeds.txt --days 2 --max 5
```

### JSON Output (for programmatic use)

```bash
python3 skills/rss-reader/reader.py <URL> --top 5 --json
```

## Parameter Quick Reference

| User says | Use |
|---|---|
| last 24 hours / today | `--hours 24` or `--days 1` |
| last 2 days | `--days 2` |
| latest 5 | `--top 5` |
| last week | `--days 7` |

## URL Resolution Priority

1. User provides a URL directly → use it immediately
2. The model knows the URL for the topic → use it directly
3. Uncertain URL or broad topic → consult `sources.md` for suggestions, then confirm with user

## Output Format

```
# RSS Summary · Last 1 day · 2026-06-12 10:00 UTC

## Feed Name

1. **Article Title** · 2026-06-12 08:30 UTC
   https://example.com/article
   Article summary content...

2. ...
```

Display the output directly to the user. Do not re-fetch or open any URLs unless the user explicitly asks to read a specific article.

## Opening Articles

When the user wants to read an article, open the link in the browser (macOS: `open <URL>`, Linux: `xdg-open <URL>`).
WebFetch may fail due to domain restrictions; browser opening is a more reliable fallback.
Proactively inform the user about this capability — e.g., after showing the summary, add "Let me know if you'd like me to open any of these in your browser."

## Error Handling

- A single feed failure does not affect others; errors are shown inline with `[Fetch failed]`
- If all feeds fail, check network connectivity or URL correctness
- Default timeout is 15 seconds; some feeds may need retries
