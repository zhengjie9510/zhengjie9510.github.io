# RSS Sources Reference

Curated feeds by category. Use when the user asks for a topic but hasn't provided a URL.

## AI & Machine Learning

| Name | URL |
|------|-----|
| Google DeepMind | `https://deepmind.google/blog/rss.xml` |
| Hugging Face Blog | `https://huggingface.co/blog/feed.xml` |
| arXiv cs.AI | `https://rss.arxiv.org/rss/cs.AI` |
| arXiv cs.LG | `https://rss.arxiv.org/rss/cs.LG` |
| MIT Technology Review | `https://www.technologyreview.com/feed/` |

## Programming & Engineering

| Name | URL |
|------|-----|
| GitHub Blog | `https://github.blog/feed/` |
| Hacker News | `https://hnrss.org/frontpage` |
| CSS-Tricks | `https://css-tricks.com/feed/` |
| The Changelog | `https://changelog.com/feed` |
| Julia Evans | `https://jvns.ca/atom.xml` |
| Stack Overflow Blog | `https://stackoverflow.blog/feed/` |

## Security

| Name | URL |
|------|-----|
| Krebs on Security | `https://krebsonsecurity.com/feed/` |
| Schneier on Security | `https://www.schneier.com/feed/atom/` |

## Chinese Tech & Media

| Name | URL |
|------|-----|
| 少数派 | `https://sspai.com/feed` |
| 知乎日报 | `https://plink.anyfeeder.com/zhihu/daily` |
| 潮流周刊 | `https://weekly.tw93.fun/rss.xml` |

## 新闻与媒体

| 名称 | URL |
|------|-----|
| 半岛电视台 | `https://www.aljazeera.com/xml/rss/all.xml` |
| Ars Technica 科技 | `https://feeds.arstechnica.com/arstechnica/index` |
| 美联社 | `https://rsshub.app/apnews/topics/apf-topnews` |
| BBC 新闻 | `http://feeds.bbci.co.uk/news/rss.xml` |
| 美国国家公共广播 | `https://feeds.npr.org/1001/rss.xml` |
| 路透社 | `https://www.reutersagency.com/feed/` |
| TechCrunch 科技创投 | `https://techcrunch.com/feed/` |
| 卫报 | `https://www.theguardian.com/world/rss` |

## Design & Product

| Name | URL |
|------|-----|
| Smashing Magazine | `https://www.smashingmagazine.com/feed` |

## Thought & Essays

| Name | URL |
|------|-----|
| Wait But Why | `https://waitbutwhy.com/feed` |

## RSSHub 动态生成模式

RSSHub 可为没有原生 RSS 的网站生成订阅源：

```
# GitHub releases
https://rsshub.app/github/releases/<owner>/<repo>

# Telegram 频道
https://rsshub.app/telegram/channel/<channel_name>

# B 站 UP 主
https://rsshub.app/bilibili/user/video/<uid>

# 微博用户
https://rsshub.app/weibo/user/<uid>
```

完整路由列表：https://docs.rsshub.app/routes/
