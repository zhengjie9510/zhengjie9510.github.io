---
layout: post
title: "给你的大模型装上手脚：Windows 安装 Claude Desktop 教程"
date: 2026-06-30
categories: [ AI 应用 ]
tags: [Claude Desktop, DeepSeek, Windows, 教程]
description: "大模型本身只有脑子没有手脚，Claude Desktop 帮它补齐了——装上之后，AI 能直接操作你的文件，不用再复制粘贴。"
image: /assets/img/posts/claude-desktop-cover.png
---

桌面上有个文件夹，里面塞了几个数据表。我对 Claude Desktop 说了一句话：

> 帮我分析一下这个文档里面的数据，并帮我绘制统计分析图。

然后就不用管了。它自己读取文件、跑统计、画图表——描述性统计、趋势分析、相关性检验一口气做完，柱状图、折线图、热力图全在对话窗口里渲染出来。

整个过程我没打开 Excel，没写一行公式，也没调过任何图表样式。

<p align="center">
  <img src="/assets/img/posts/claude-desktop-data-analysis.png" alt="Claude Desktop 数据分析实战截图" style="max-width: 640px;">
</p>

一份数据分析报告，就这么一句话的事。

---

这就是 Claude Desktop 配上 DeepSeek 的效果——大模型不再困在浏览器聊天框里，而是能直接在你的电脑上干活：做 PPT、写报告、整表格、理文件、画图表。类似思路的工具还有 Open Claw（小龙虾）、腾讯 WorkBuddy 等。

下面用 Windows 示范，怎么把这套「大脑 + 手脚」装起来。

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

**Cowork** 在沙盒的虚拟桌面里工作，跟你的电脑隔离开，AI 在里面操作自己的文件系统和浏览器；**Code** 直接在你的电脑上工作，能读写本地文件、执行命令。写代码、做 PPT、整理文件这些它俩都能干，看你想让 AI 在你电脑上干还是在沙盒里干。

> 💡 第一次打开 Code 标签需要装 Git for Windows，没装的话会提示你，装完重启一下 Claude 就行。
>
> ⚠️ 不管是 Claude Desktop、Open Claw（小龙虾），还是腾讯 WorkBuddy，这类工具本质上都是让 AI 操控你的电脑。务必保持人为审核，涉及删除、移动文件等操作时确认一下再放行，别让它全自动跑。

---

## 四、🔗 接入 DeepSeek

Anthropic 不对大陆提供服务，所以需要把模型换成 DeepSeek。Claude Desktop 自带一个图形化的切换入口，不用改系统环境变量。

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

Claude Desktop 免费下载使用，接入 DeepSeek 之后按量计费，不用订阅 Claude 的付费计划。日常用 Code 标签处理文件，分析数据、写报告、做 PPT，基本就够了。

装好之后，你也能像我一样，一句话让 AI 帮你把活干了 🚀
