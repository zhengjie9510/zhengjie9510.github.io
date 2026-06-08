#!/usr/bin/env python3
"""
rss_fetch.py — 抓取 RSS/Atom 源并过滤，输出精简文本供 AI 使用
支持 Windows / macOS / Linux，纯标准库，无需安装依赖

用法:
  python rss_fetch.py <URL> [URL2 ...] [选项]

过滤选项（不传则返回最近 10 条）:
  --days  N       返回最近 N 天内的条目
  --hours N       返回最近 N 小时内的条目
  --top   N       返回最新的 N 条（不限时间）

其他选项:
  --sources FILE  从文件读取 URL 列表（每行一个，# 开头为注释）
  --max N         每个源最多输出 N 条（默认 20，防止超长）
  --no-content    只输出标题+链接+时间，不含正文摘要

示例:
  python rss_fetch.py https://openai.com/blog/rss.xml --days 1
  python rss_fetch.py https://hnrss.org/frontpage --top 5
  python rss_fetch.py --sources feeds.txt --hours 12 --max 10
  python rss_fetch.py https://sspai.com/feed --days 2 --no-content
"""

import sys
import argparse
import urllib.request
import urllib.error
import re
import html
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime


# ── Windows 兼容：强制 stdout/stderr 使用 UTF-8 ───────────────────────────────
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ── 参数解析 ──────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="RSS 抓取过滤工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    p.add_argument("urls", nargs="*", help="RSS/Atom URL")
    p.add_argument("--sources", help="从文件读取 URL 列表（每行一个）")
    p.add_argument("--days",  type=float, help="最近 N 天")
    p.add_argument("--hours", type=float, help="最近 N 小时")
    p.add_argument("--top",   type=int,   help="最新 N 条（不限时间）")
    p.add_argument("--max",   type=int, default=20, help="每源最多条数（默认 20）")
    p.add_argument("--no-content", action="store_true", help="只输出标题+链接+时间")
    return p.parse_args()


# ── 抓取 ──────────────────────────────────────────────────────────────────────

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; RSSFetcher/1.0)",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            # 尝试从 HTTP 头或 XML 声明检测编码
            content_type = r.headers.get("Content-Type", "")
            encoding = "utf-8"
            m = re.search(r"charset=([^\s;]+)", content_type, re.IGNORECASE)
            if m:
                encoding = m.group(1).strip('"\'')
            else:
                # 从 XML 声明检测：<?xml version="1.0" encoding="..."?>
                head = raw[:200]
                mx = re.search(rb'encoding=["\']([^"\']+)["\']', head)
                if mx:
                    encoding = mx.group(1).decode("ascii", errors="ignore")
            return raw.decode(encoding, errors="replace")
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"连接失败: {e.reason}"
    except Exception as e:
        return None, f"错误: {e}"


# ── XML 解析（纯正则，无第三方依赖）─────────────────────────────────────────

def tag(text, name):
    """提取第一个 <name ...>...</name> 的内容，支持 CDATA"""
    m = re.search(
        rf"<{re.escape(name)}(?:\s[^>]*)?>(<!\[CDATA\[)?(.*?)(\]\]>)?</{re.escape(name)}>",
        text, re.DOTALL | re.IGNORECASE
    )
    if not m:
        return ""
    content = m.group(2) or ""
    return content.strip()

def attr(text, name, attribute):
    """提取 <name ... attribute="value"> 的属性值"""
    m = re.search(
        rf'<{re.escape(name)}(?:\s[^>]*?\s|\s){re.escape(attribute)}=["\']([^"\']*)["\']',
        text, re.IGNORECASE
    )
    return m.group(1).strip() if m else ""

def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def truncate(s, n=200):
    return s[:n] + "…" if len(s) > n else s

def parse_date(s):
    """解析 RFC 2822 或 ISO 8601，返回 UTC datetime 或 None"""
    if not s:
        return None
    s = s.strip()
    # RFC 2822（RSS 2.0 pubDate）
    try:
        return parsedate_to_datetime(s).astimezone(timezone.utc)
    except Exception:
        pass
    # ISO 8601（Atom updated/published）
    s2 = s
    if s2.endswith("Z"):
        s2 = s2[:-1] + "+00:00"
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s2, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            pass
    return None

def split_blocks(xml, tag_name):
    """将 XML 按 <tag_name> 分割成块列表"""
    pattern = rf"<{re.escape(tag_name)}[\s>]"
    parts = re.split(pattern, xml, flags=re.IGNORECASE)
    return parts[1:]  # 第一段是 header，跳过

def parse_feed(xml):
    """解析 RSS 2.0 / Atom，返回 (feed_title, [item_dict])"""
    is_atom = bool(re.search(r"<feed[\s>]", xml[:600], re.IGNORECASE))

    feed_title = strip_html(tag(xml, "title"))

    if is_atom:
        blocks = split_blocks(xml, "entry")
        def get_link(block):
            # Atom <link href="..."> 或 <link>...</link>
            return attr(block, "link", "href") or strip_html(tag(block, "link"))
        date_tags = ["updated", "published"]
        content_tags = ["content", "summary"]
    else:
        blocks = split_blocks(xml, "item")
        def get_link(block):
            return strip_html(tag(block, "link"))
        date_tags = ["pubDate", "dc:date", "published"]
        content_tags = ["content:encoded", "description", "summary"]

    items = []
    for block in blocks:
        title = strip_html(tag(block, "title"))
        link  = get_link(block)

        content = ""
        for ctag in content_tags:
            raw = tag(block, ctag)
            if raw:
                content = truncate(strip_html(raw), 200)
                break

        pub = None
        for dtag in date_tags:
            raw_date = tag(block, dtag)
            if raw_date:
                pub = parse_date(raw_date)
                if pub:
                    break

        if title or link:
            items.append({"title": title, "link": link, "content": content, "date": pub})

    return feed_title, items


# ── 过滤 ──────────────────────────────────────────────────────────────────────

def filter_items(items, args):
    now = datetime.now(timezone.utc)

    if args.days:
        cutoff = now - timedelta(days=args.days)
        items = [i for i in items if i["date"] and i["date"] >= cutoff]
    elif args.hours:
        cutoff = now - timedelta(hours=args.hours)
        items = [i for i in items if i["date"] and i["date"] >= cutoff]

    # 有日期的排前面，按时间降序
    items.sort(
        key=lambda i: i["date"] or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True
    )

    if args.top:
        items = items[:args.top]
    else:
        items = items[:args.max]

    return items


# ── 输出 ──────────────────────────────────────────────────────────────────────

def fmt_date(dt):
    if not dt:
        return "未知时间"
    return dt.strftime("%Y-%m-%d %H:%M UTC")

def render(feed_title, items, url, no_content):
    lines = [f"## {feed_title or url}"]
    if not items:
        lines.append("（该时间段内无条目）")
        return "\n".join(lines)
    for i, item in enumerate(items, 1):
        lines.append(f"\n{i}. **{item['title'] or '无标题'}** · {fmt_date(item['date'])}")
        lines.append(f"   {item['link']}")
        if not no_content and item["content"]:
            lines.append(f"   {item['content']}")
    return "\n".join(lines)


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # 收集 URL
    urls = list(args.urls)
    if args.sources:
        try:
            # Windows 可能是 GBK 编码的文件，优先 UTF-8 再回退
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
            print(f"[错误] 找不到文件: {args.sources}", file=sys.stderr)
            sys.exit(1)

    if not urls:
        print("[错误] 请提供至少一个 RSS URL，或用 --sources 指定文件", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # 过滤描述
    if args.days:
        filter_desc = f"最近 {args.days} 天"
    elif args.hours:
        filter_desc = f"最近 {args.hours} 小时"
    elif args.top:
        filter_desc = f"最新 {args.top} 条"
    else:
        filter_desc = f"最新 {args.max} 条"

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"# RSS 摘要 · {filter_desc} · {now_str}\n")

    for url in urls:
        result = fetch(url)

        if isinstance(result, tuple):
            # (None, errMsg)
            print(f"## {url}\n[抓取失败] {result[1]}\n")
            continue

        try:
            feed_title, items = parse_feed(result)
            items = filter_items(items, args)
            print(render(feed_title, items, url, args.no_content))
            print()
        except Exception as e:
            print(f"## {url}\n[解析失败] {e}\n")


if __name__ == "__main__":
    main()
