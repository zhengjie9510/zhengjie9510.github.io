---
name: rss-fetch
description: >
  当用户说"获取 RSS"、"看最新资讯"、"读取订阅源"、"查看更新"、
  "获取最近 N 天/小时的文章"、"显示最新 N 条"，或任何从 RSS/Atom
  订阅源获取并汇总内容的请求时，使用此技能。
  技能通过运行 rss_fetch.py，按时间或数量过滤后再返回结果——
  不会将原始 feed XML 直接输出给模型。
metadata:
  version: "0.1.0"
---

# RSS Fetch 技能

运行此技能目录下的 `rss_fetch.py`，用于获取并过滤 RSS/Atom 订阅源。
脚本只输出符合条件的条目纯文本，可直接阅读和展示。

依赖：Python 3.7+，无需第三方包，支持 Windows / macOS / Linux。

## 脚本路径

```
skills/rss-fetch/rss_fetch.py
```

## 使用命令

### 按时间过滤

```bash
# 最近 1 天
uv run skills/rss-fetch/rss_fetch.py <URL> --days 1

# 最近 2 天
uv run skills/rss-fetch/rss_fetch.py <URL> --days 2

# 最近 12 小时
uv run skills/rss-fetch/rss_fetch.py <URL> --hours 12
```

### 按数量过滤

```bash
# 最新 5 条（不限时间）
uv run skills/rss-fetch/rss_fetch.py <URL> --top 5

# 最新 10 条（不传参数时的默认行为）
uv run skills/rss-fetch/rss_fetch.py <URL>
```

### 多个订阅源

```bash
uv run skills/rss-fetch/rss_fetch.py <URL1> <URL2> <URL3> --days 1
```

### 从源文件读取

```bash
uv run skills/rss-fetch/rss_fetch.py --sources feeds.txt --days 1
```

`feeds.txt` 格式——每行一个 URL，`#` 开头为注释：

```
# AI
https://openai.com/blog/rss.xml
https://www.anthropic.com/news/rss.xml

# 科技
https://hnrss.org/frontpage
```

### 只输出标题和链接（节省 token）

```bash
uv run skills/rss-fetch/rss_fetch.py <URL> --days 1 --no-content
```

### 限制每个源的最大条数

```bash
uv run skills/rss-fetch/rss_fetch.py --sources feeds.txt --days 2 --max 5
```

## 参数选择速查

| 用户说 | 使用参数 |
|---|---|
| 最近一天 / last 24 hours | `--hours 24` 或 `--days 1` |
| 最近两天 / last 2 days | `--days 2` |
| 最新 5 条 / latest 5 | `--top 5` |
| 最近一周 / last week | `--days 7` |

> **URL 决策优先级**
> 1. 用户直接给出 URL → 立即执行
> 2. 模型本身就知道该话题对应的 URL → 直接使用
> 3. 不确定 URL 或话题过于宽泛 → 查阅 `rss-sources.md` 推荐后由用户确认

## 输出格式

```
# RSS 摘要 · 最近 1 天 · 2026-06-08 10:00 UTC

## Feed 名称

1. **文章标题** · 2026-06-08 08:30 UTC
   https://example.com/article
   文章摘要内容……

2. ...
```

读取输出后直接展示给用户。除非用户明确要求阅读某篇文章，否则不要重新请求或打开任何 URL。
