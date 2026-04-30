---
name: blog-post-processor
description: 格式转换工具：将来源清晰、内容规整的博客文章（微信公众号、CSDN、技术博客等）转换为 Jekyll 格式。包括内容提取、图片本地化、front matter 生成和排版规范化。不处理内容重写或低质量源修复。
---

# 博客文章处理器

将来源清晰、格式规整的博客文章转换为 Jekyll 兼容的 markdown 格式。

## 能力边界

| ✅ 适用 | ❌ 不适用 |
|--------|----------|
| 来源清晰、内容完整的文章（公众号、CSDN、技术博客）| 需要重写内容逻辑、补充背景知识的场景 |
| 格式转换、图片本地化、排版规范化 | OCR 错误、乱码、大量无关广告的源内容 |
| 轻度清理（移除推广 HTML、格式化代码块）| 从原始材料人工整理成文的场景 |

**核心定位**：搬运工，不是作者。负责把已成型的内容标准化，不负责创作或深度改写。

---

## 关键规则：必须处理所有图片

**文章中的每一张图片都必须下载并转换为本地引用。**

不许跳过任何图片，不许在最终的 markdown 中保留外部 URL。

---

## 输入类型

### 类型 A：URL 导入
用户提供一个 URL（微信公众号、CSDN、网页文章等）。

### 类型 B：本地文件处理
用户已经将文件保存到 `_posts/` 目录。

---

## 处理流程

### 步骤 1：获取内容

**如果是 URL：**
- 使用 FetchURL 工具获取文章内容
- 从 HTML/meta 标签提取元数据

**如果是本地文件：**
- 直接读取文件
- 提取已有元数据

### 步骤 2：提取所有图片（关键步骤）

**必须扫描内容中的所有图片：**

1. **Markdown 格式：** `![alt](url)`
2. **HTML 格式：** `<img src="url">`
3. **原始 URL：** 任何图片 URL 模式

**提取方法：**
- 在获取的 HTML/源码中搜索所有图片模式
- 列出找到的每个图片 URL
- 建立映射：原始 URL → 本地文件名

**图片命名规范：**
```
{slug}-{描述}.png
```

示例：
- 第一张/封面图：`{slug}-cover.png`
- 流程图：`{slug}-workflow.png`
- 训练曲线：`{slug}-training-curve.png`
- 图 1、2、3：`{slug}-figure-1.png` 等

### 步骤 3：下载所有图片（必须执行）

**下载每一张图片：**

```bash
# 对每个找到的 URL 执行：
curl -L -o "assets/img/posts/{slug}-{描述}.png" "{原始URL}"
```

**验证下载：**
```bash
ls -la assets/img/posts/{slug}-*
```

**如有需要压缩（特别是大于 500KB 的封面）：**
```bash
# 封面图：调整为 800px 宽度，80% 质量 JPEG
sips -Z 800 input.png --out output.jpg -s format jpeg -s formatOptions 80
```

### 步骤 4：提取并确认元数据

提取：
- **标题**：从 HTML `<title>`、h1 或文章元数据
- **日期**：如未明确指定，询问用户
- **描述**：生成 100 字以内的摘要

**向用户确认：**
> 检测到文章信息：
> - 标题：[提取的标题]
> - 图片数量：[N] 张
> - 建议日期：[YYYY-MM-DD]
> 
> 请确认或修改日期。

### 步骤 5：生成 Jekyll Front Matter

```yaml
---
layout: post
title: "文章标题"
date: YYYY-MM-DD HH:MM:SS +0800
categories: [ 技术, AI ]
tags: [ tag1, tag2, tag3 ]
description: "文章摘要"
image: /assets/img/posts/{slug}-cover.jpg  # 如果有封面
---
```

### 步骤 6：格式化内容并替换图片引用

**清理：**
- 移除微信/CSDN 推广 HTML
- 转换表情符号章节标记为 markdown 标题
- 格式化代码块，添加语言标签

**必须替换所有图片引用：**

替换前：
```markdown
![](https://external-url.com/image.png)
```

替换后：
```markdown
<div align="center">
  <img src="/assets/img/posts/{slug}-{描述}.png" alt="描述" style="max-width: 600px;">
  <p style="color: #888; font-size: 12px; margin-top: 8px;">图注</p>
</div>
```

**插入公众号二维码**（front matter 之后）：
```html
<div align="center" style="margin: 20px 0;">
    <img src="/assets/img/wechat-qr-white.png" alt="AI在学公众号" style="max-width: 320px; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">🔍 微信扫码或搜索「AI在学」关注公众号</p>
</div>
```

**标题层级：**
- 从 `##`（二级）开始，不要用 `#`（一级）

### 步骤 7：保存并验证

**生成文件名：**
```
_posts/YYYY-MM-DD-{slug}.md
```

**关键：最终验证清单**

在说完"完成"之前，验证：
- [ ] 所有图片已下载到 `assets/img/posts/`
- [ ] 所有外部图片 URL 已替换为本地路径
- [ ] markdown 中没有剩余的 `http://` 或 `https://` 图片链接
- [ ] 图片居中并带图注
- [ ] 文件已重命名为标准格式
- [ ] 原文件已删除（如适用）

**验证命令：**
```bash
# 检查是否还有外部 URL
grep -E "https?://.*\.(png|jpg|jpeg|gif|webp)" _posts/YYYY-MM-DD-{slug}.md
# 应该返回空
```

---

## 示例

**带多张图片的 URL 导入：**
```
用户："导入这篇文章：https://mp.weixin.qq.com/s/xxxxx"
→ 获取内容
→ 从文章中提取全部 4 张图片
→ 下载：article-cover.png, article-figure-1.png, article-figure-2.png, article-figure-3.png
→ 询问日期
→ 创建 2025-05-10-article-title.md，所有图片使用本地引用
→ 验证：grep 返回空
```

**要避免的错误：**
```
❌ 错误：只下载了 1 张封面图，剩下 3 张图表仍使用外部 URL
✅ 正确：下载了全部 4 张图片，替换了所有引用
```

---

## 常见错误

1. **以为 FetchURL 会自动提取图片** - 它只提取文本。必须手动扫描图片 URL。
2. **跳过"装饰性"图片** - 每张图片都重要，包括图表、流程图、截图。
3. **忘记替换 URL** - 仅下载不够，必须更新 markdown 中的引用。
4. **不进行验证** - 始终运行 grep 检查确保没有外部 URL 残留。
