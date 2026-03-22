---
name: blog-post-formatter
description: "博客文章规范化工具：处理从外部复制进来的文章，包括文件名规范化、front matter生成、图片下载与重命名、封面设置、公众号引流插入"
---

# 博客文章规范化 Skill

## 适用场景
用户从外部（如微信公众号、CSDN、知乎等）复制文章到 _posts 目录，需要规范化处理。

## 执行流程

### 步骤 1：分析原文件
读取原文件，提取信息：
- 文章标题（如有）
- 文章日期（发布日期 or 今天）
- 文章中的图片 URL 列表
- 文章摘要/描述

### 步骤 2：生成规范文件名
格式：`YYYY-MM-DD-{slug}.md`

- **日期来源优先级**：
  1. 用户指定日期
  2. 原文件中的日期信息
  3. 当前日期
  
- **Slug 生成规则**：
  - 基于文章标题翻译或提取关键词
  - 小写英文字母
  - 空格和特殊字符替换为连字符 `-`
  - 示例：`别再复制粘贴提示词了` → `ai-agent-skill`

### 步骤 3：处理图片

#### 3.1 扫描文章中的图片
查找所有图片引用：
- Markdown 格式：`![alt](url)`
- HTML 格式：`<img src="url">`
- 本地图片路径

#### 3.2 下载外部图片
对于每个外部 URL 图片：
1. 下载到 `assets/img/posts/`
2. 生成英文文件名：`{slug}-{序号}.{扩展名}`
3. **压缩图片**：宽度调整为 1200px，等比例缩放
4. 更新文章中的图片引用路径

**图片压缩方法**：
```bash
# 使用 ImageMagick（如已安装）
convert input.png -resize 1200x output.png

# 或使用 macOS 自带的 sips
sips -Z 1200 input.png --out output.png
```

#### 3.3 重命名本地图片
如果已有本地图片但名称不规范：
- 重命名为：`{slug}-{描述}.{扩展名}`

#### 3.4 设置封面
- **第一张图片**作为封面
- 封面路径写入 front matter：`image: /assets/img/posts/{封面文件名}`

### 步骤 4：生成 Front Matter

```yaml
---
layout: post
title: "{文章标题}"
date: {YYYY-MM-DD HH:MM:SS +0800}
categories: [ 技术, {分类} ]
tags: [ {标签1}, {标签2}, {标签3} ]
description: "{100字以内的文章摘要}"
image: /assets/img/posts/{封面文件名}
---
```

**字段处理**：
- `title`：从原文提取或使用文件名，检查引号冲突（中文引号改为书名号『』）
- `date`：使用确定的发布日期
- `categories`：根据内容自动推断或询问用户 [技术, AI] 等
- `tags`：提取文章关键词作为标签
- `description`：提取文章前100字或生成摘要

### 步骤 5：插入公众号引流

在 front matter 之后、正文之前插入：

```html
<div align="center" style="margin: 20px 0;">
    <img src="/assets/img/wechat-qr-white.png" alt="AI在学公众号" style="max-width: 320px; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">
      🔍 微信扫码或搜索「AI在学」关注公众号
    </p>
</div>
```

### 步骤 6：清理与格式化

- 删除原文中已有的公众号推广信息（避免重复）
- 规范化 Markdown 格式
- 确保标题层级正确（从 ## 开始）

### 步骤 7：保存新文件

- 保存为规范文件名
- 删除原文件（如果名称不规范）

## 用户确认点

按照 git-safe-commit Skill 的规则，以下操作需要确认：

### 处理前确认（可选）
如果检测到多张图片或复杂情况，询问：
> 检测到文章包含 [N] 张外部图片，需要下载。
> 建议文件名：`2026-03-20-ai-economic-crisis.md`
> 
> 是否开始处理？
> - ✅ 是，开始处理
> - ✏️ 修改文件名
> - ❌ 取消

### 完成后确认
处理完成后，展示变更摘要：
> ✅ 文章规范化完成：
> - 新文件名：`2026-03-20-ai-economic-crisis.md`
> - 下载图片：[N] 张
> - 封面设置：`ai-economic-crisis-cover.png`
> 
> 是否提交更改？
> - ✅ 是，提交
> - ❌ 否，先不提交

## 示例

**输入**：新文件 `AI越成功，经济越危险？.md`

**自动处理**：
1. 提取标题
2. 生成文件名：`2026-03-20-ai-economic-crisis.md`
3. 发现 1 个外部图片 URL
4. 下载图片，重命名为 `ai-economic-crisis-cover.png`
5. 生成 front matter
6. 插入公众号引流
7. 删除原文推广信息

**输出**：规范化的博客文章，可直接发布。

## 高级处理（Python 脚本）

对于复杂处理（如批量图片处理、内容分析等），可在当前目录创建临时 Python 虚拟环境：

```bash
# 创建临时环境
python3 -m venv .temp_venv
source .temp_venv/bin/activate

# 安装依赖
pip install -q pillow requests

# 执行处理脚本
python process_images.py

# 完成后删除环境
deactivate
rm -rf .temp_venv
```

**注意**：任务完成后必须删除临时环境，保持项目整洁。

## 注意事项

- 图片下载失败时保留原 URL，并告知用户
- 标题中的引号统一改为书名号『』避免 YAML 解析错误
- 摘要超过 100 字时自动截断并加省略号
- 图片压缩优先使用系统自带工具（sips/convert），复杂场景才用 Python
