---
layout: post
title: "让 AI 真正帮你干活：借 Claude Desktop 的壳，给 DeepSeek 装上手脚"
date: 2026-06-30
categories: [ AI 应用 ]
tags: [Claude Desktop, DeepSeek, Windows, 教程]
description: "大模型本身只有脑子没有手脚，Claude Desktop 补齐了这双手脚——配上 DeepSeek 当大脑，AI 能直接操作你的文件，不用再复制粘贴。"
image: /assets/img/posts/claude-desktop-cover.png
---

桌面上有个文件夹，躺着几张一直没空整理的数据表。我把它扔给 Claude Desktop，只说了一句话：

> 帮我分析一下这个文档里面的数据，并帮我绘制统计分析图。

然后就没我什么事了。它自己翻开文件、跑统计、画图——描述性统计、趋势分析、相关性检验一口气做完，柱状图、折线图、热力图接连冒在对话框里。

整个过程我没打开过 Excel，没写一行公式，连图表样式都没碰过。

<p align="center">
  <img src="/assets/img/posts/claude-desktop-data-analysis.png" alt="Claude Desktop 数据分析实战截图" style="max-width: 640px;">
</p>

一份数据分析报告，就这么被一句话打发了。

---

这就是 Claude Desktop 配上 DeepSeek 之后的样子——大模型不再困在浏览器的聊天框里出不来，而是能伸手在你的电脑上干活：做 PPT、写报告、整表格、理文件、画图表。类似的思路，Open Claw（小龙虾）、腾讯 WorkBuddy 也都在做。

下面就在 Windows 上，把这套「大脑 + 手脚」的组合装起来。

---

## 一、📥 下载安装包

打开官方下载页面：

> 🔗 https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows

下载 **Claude MSIX (x64)**（ARM 设备选 arm64 版本）。

<p align="center">
  <img src="/assets/img/posts/claude-desktop-download-page.png" alt="Claude Desktop 下载页面" width="400">
</p>

---

## 二、⚙️ 安装

以管理员身份打开 PowerShell，执行：

```powershell
Add-AppxPackage -Path "文件路径\Claude.msix"
```

把路径换成你实际下载文件的位置即可。也可以直接双击 `.msix` 文件安装，弹出 UAC 确认窗口点「是」就行。

装完之后，开始菜单里就能找到 Claude 图标了。

---

## 三、🤖 Cowork 和 Code 的区别

打开 Claude Desktop 你会看到两个标签：**Cowork** 和 **Code**。

**Cowork** 像是给 AI 单独辟出一间虚拟房间，它在里面自己捣鼓文件和浏览器，跟你的真实电脑没有关系；**Code** 则直接站到你的电脑跟前，能读写本地文件、执行命令。写代码、做 PPT、整理文件这些它俩都能干，区别只是你想让 AI 在你电脑上动手，还是在自己的房间里跑。

> 💡 第一次打开 Code 标签需要装 Git for Windows，没装的话会提示你，装完重启一下 Claude 就行。
>
> ⚠️ 不管是 Claude Desktop、Open Claw（小龙虾），还是腾讯 WorkBuddy，这类工具本质上都是让 AI 操控你的电脑。手脚是它的，方向盘还得握在你手里——涉及删除、移动文件等操作，确认一下再放行，别撒手让它自己跑。

---

## 四、🔗 接入 DeepSeek

Anthropic 不对大陆提供服务，这套「手脚」原装的脑子用不了，得换成 DeepSeek。好在 Claude Desktop 自带一个图形化的切换入口，不用碰系统环境变量这类麻烦事。

**1. 申请 DeepSeek API Key**

打开 https://platform.deepseek.com，注册登录，进入「API Keys」创建一个新密钥（`sk-` 开头），**立刻复制保存好，只显示这一次**。然后去「充值」充 10 元左右，够用很久。

<p align="center">
  <img src="/assets/img/posts/deepseek-api-key-create.png" alt="DeepSeek 创建 API Key" style="max-width: 480px;">
</p>

**2. 开启开发者模式**

打开 Claude Desktop，**先别登录账号**，停在登录界面。点左上角菜单（☰）→ **Help → Troubleshooting → Enable Developer Mode**，确认后软件会重启，顶部多出一个 **Developer** 菜单。

**3. 配置第三方模型**

点 **Developer → Configure Third-Party Inference**，在弹出的窗口里填：

- Connection：选 **Gateway**
- Gateway base URL：`https://api.deepseek.com/anthropic`
- API Key：填刚才申请的 DeepSeek 密钥

<p align="center">
  <img src="/assets/img/posts/deepseek-gateway-base-url.png" alt="配置 Gateway Base URL 和 API Key" style="max-width: 480px;">
</p>

- 模型列表：填 `deepseek-v4-pro` 和 `deepseek-v4-flash`

<p align="center">
  <img src="/assets/img/posts/deepseek-gateway-model-list.png" alt="配置模型列表" style="max-width: 480px;">
</p>

点 **Apply locally** 保存，软件会重启。

---

## 写在最后

Claude Desktop 本身免费下载，接入 DeepSeek 之后按量计费，不用订阅 Claude 的付费计划。日常用 Code 标签处理文件、分析数据、写报告、做 PPT，基本够用了。

装好这套「手脚」，剩下的事，一句话就能打发给 AI 🚀
