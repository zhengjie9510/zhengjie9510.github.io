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
| 少数派 (sspai) | `https://sspai.com/feed` |
| 知乎日报 (Zhihu Daily) | `https://plink.anyfeeder.com/zhihu/daily` |
| 潮流周刊 (Tw93 Weekly) | `https://weekly.tw93.fun/rss.xml` |

## News & Media

| Name | URL |
|------|-----|
| Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/index` |
| Associated Press | `https://rsshub.app/apnews/topics/apf-topnews` |
| BBC News | `http://feeds.bbci.co.uk/news/rss.xml` |
| NPR | `https://feeds.npr.org/1001/rss.xml` |
| Reuters | `https://www.reutersagency.com/feed/` |
| TechCrunch | `https://techcrunch.com/feed/` |
| The Guardian | `https://www.theguardian.com/world/rss` |

## Design & Product

| Name | URL |
|------|-----|
| Smashing Magazine | `https://www.smashingmagazine.com/feed` |

## Thought & Essays

| Name | URL |
|------|-----|
| Wait But Why | `https://waitbutwhy.com/feed` |

## RSSHub Dynamic Routes

RSSHub can generate feeds for sites without native RSS:

```
# GitHub releases
https://rsshub.app/github/releases/<owner>/<repo>

# Telegram channel
https://rsshub.app/telegram/channel/<channel_name>

# Bilibili user videos
https://rsshub.app/bilibili/user/video/<uid>

# Weibo user
https://rsshub.app/weibo/user/<uid>
```

Full route list: https://docs.rsshub.app/routes/
