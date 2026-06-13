---
name: rss-reader
description: >
  Use this skill to read RSS/Atom feeds and get a summary of recent articles.
  Trigger when the user wants to check, fetch, or see recent/new/latest content
  from a source — a feed URL, a website name, or a blog.
  Common patterns: "what's new on X", "get today's papers from arXiv",
  "check HN front page", "recent posts from this blog",
  "last N days/hours of updates", "latest N articles".
  Covers: time-based filtering (today, last N days/hours), quantity filtering
  (latest N), multi-source aggregation.
  中文触发词：获取 RSS、看最新资讯、读取订阅源、查看更新、
  获取最近 N 天/小时的文章、显示最新 N 条。
  Do NOT use for: general web scraping, creating/generating RSS feeds,
  OPML import/export.
metadata:
  version: "1.1.0"
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
pip install feedparser
```

## Usage

### Filter by Time

```bash
# Last 24 hours
python skills/rss-reader/reader.py <URL> --days 1

# Last 12 hours
python skills/rss-reader/reader.py <URL> --hours 12
```

### Filter by Count

```bash
# Latest 5 articles (no time limit)
python skills/rss-reader/reader.py <URL> --top 5

# Default: latest 10 articles
python skills/rss-reader/reader.py <URL>
```

### Multiple Feeds

```bash
python skills/rss-reader/reader.py <URL1> <URL2> <URL3> --days 1
```

### Titles and Links Only (saves tokens)

```bash
python skills/rss-reader/reader.py <URL> --days 1 --no-content
```

### JSON Output (for programmatic use)

```bash
python skills/rss-reader/reader.py <URL> --top 5 --json
```

## Parameter Quick Reference

| User says | Use |
|---|---|
| last 24 hours / today | `--hours 24` or `--days 1` |
| last 2 days | `--days 2` |
| latest 5 | `--top 5` |
| last week | `--days 7` |

## URL Resolution

The script requires explicit URLs — it does not read from files. When the user asks about a topic:

1. **Known URL** → use it directly
2. **Unknown URL** → consult `sources.md` for suggestions, confirm with user, then pass the URL to the script
3. **User says "my feeds"** → read `sources.md`, extract the URLs, and pass them as arguments

`sources.md` is a reference file for the model, not input for the script.

## Managing Sources (sources.md)

When the user wants to add or remove RSS feeds, manage `skills/rss-reader/sources.md`.

**Add a feed** — verify the URL first:

```bash
python skills/rss-reader/reader.py <URL> --top 1
```

- Returns articles → append to `sources.md` under the appropriate category. Create the category if it doesn't exist.
- Fails → tell the user the URL isn't a valid RSS/Atom feed.

**Never add a feed without testing it first.**

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
