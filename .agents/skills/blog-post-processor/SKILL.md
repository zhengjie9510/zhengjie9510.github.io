---
name: blog-post-processor
description: Process blog posts from URLs or local files for Jekyll blogs. Use when user provides a URL to import, or has new/raw blog files needing formatting. Handles content extraction, image downloading, front matter generation, and Jekyll formatting.
---

# Blog Post Processor

Process blog posts from URLs or local files, converting them to Jekyll-compatible markdown format.

## Input Types

### Type A: URL Import
User provides a URL (WeChat, CSDN, web article).

### Type B: Local File Processing
User has already copied/saved a file to `_posts/` directory.

---

## Workflow

### Step 1: Get Content

**If URL provided:**
- Use FetchURL tool to retrieve article content
- Extract metadata from HTML/meta tags

**If local file provided:**
- Read the file directly
- Extract existing metadata if any

### Step 2: Extract & Confirm Metadata

Extract:
- **Title**: From HTML `<title>`, h1, or article metadata
- **Date**: 
  - Ask user if not clearly specified
  - Check for dates in URL or article header
- **Description**: Generate 100-character summary

**Confirm with user:**
> 检测到文章信息：
> - 标题：[提取的标题]
> - 建议日期：[YYYY-MM-DD]
> 
> 请确认或修改日期。

### Step 3: Download & Process Images

**Scan for images:**
- Markdown: `![alt](url)`
- HTML: `<img src="url">`

**Download external images:**
```bash
# Download to assets/img/posts/
curl -L -o "assets/img/posts/{slug}-{desc}.png" "{url}"
```

**Image naming:**
- Format: `{slug}-{description}.{ext}`
- Cover: `{slug}-cover.{ext}` (first image or user-specified)

**Compress images if needed:**
```bash
# Cover images: 1200px width, 80% quality
sips -Z 1200 input.png --out output.jpg -s format jpeg -s formatOptions 80
```

### Step 4: Generate Jekyll Front Matter

```yaml
---
layout: post
title: "文章标题"
date: YYYY-MM-DD HH:MM:SS +0800
categories: [ 技术, AI ]
tags: [ tag1, tag2, tag3 ]
description: "文章摘要"
image: /assets/img/posts/{slug}-cover.jpg  # Optional
---
```

**Title handling:**
- Replace quotes with book title marks 『』 to avoid YAML parsing issues

### Step 5: Format Content

**Clean up:**
- Remove WeChat/CSDN promotional HTML
- Convert emoji section markers to markdown headers
- Format code blocks with language tags

**Insert WeChat QR code** (after front matter):
```html
<div align="center" style="margin: 20px 0;">
    <img src="/assets/img/wechat-qr-white.png" alt="AI在学公众号" style="max-width: 320px; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">
      🔍 微信扫码或搜索「AI在学」关注公众号
    </p>
</div>
```

**Heading levels:**
- Start from `##` (h2), not `#` (h1)
- h1 is auto-generated from front matter title

**Image alignment:**
```markdown
<div align="center">
  <img src="/assets/img/posts/{image}" alt="描述" style="max-width: 600px;">
  <p style="color: #888; font-size: 12px; margin-top: 8px;">图注</p>
</div>
```

### Step 6: Save & Cleanup

**Generate filename:**
```
_posts/YYYY-MM-DD-{slug}.md
```

**After saving:**
- Delete original file (if name was non-standard)
- List all changes

---

## Output Checklist

Final post must have:
- [ ] Correct filename: `YYYY-MM-DD-slug.md`
- [ ] Valid Jekyll front matter
- [ ] Local image references only
- [ ] WeChat QR code inserted
- [ ] No promotional/external HTML
- [ ] Proper heading hierarchy (start from ##)

---

## Examples

**URL import:**
```
User: "Import this: https://mp.weixin.qq.com/s/xxxxx"
→ Fetch content
→ Ask for date
→ Download images  
→ Create 2025-05-10-article-title.md
```

**Local file processing:**
```
User: "处理这个新文件: 深度学习基础.md"
→ Read file
→ Extract title
→ Ask for date
→ Download images
→ Rename to 2025-12-01-batch-norm-layer-norm.md
→ Delete original
```
