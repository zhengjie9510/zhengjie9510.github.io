---
layout: post
title: "给你的大模型装上手脚：Windows 安装 Claude Desktop 教程"
date: 2026-06-30
categories: [ AI 应用 ]
tags: [Claude Desktop, DeepSeek, Windows, 教程]
description: "大模型本身只有脑子没有手脚，Claude Desktop 帮它补齐了——装上之后，AI 能直接操作你的文件，不用再复制粘贴。"
image: /assets/img/posts/claude-desktop-cover.png
---

你是不是还在这样用 AI：打开浏览器聊天 → 把回复复制下来 → 粘贴到 Word 或 Excel 里 → 自己排版整理。聊得挺好，但干活还是你自己来。

Claude Desktop 把大模型从浏览器里拽了出来——给它装上了手脚，能直接在你的电脑上干活：

> 📊 **做 PPT** 说一句"帮我做一份产品介绍的 PPT"，`.pptx` 直接生成到桌面，大纲排版一把梭。
>
> 📝 **写报告** 丢几个要点进去，Word 文档自动生成，结构标题段落都排好，改改就能交。
>
> 📈 **表格统计** 把 Excel 甩给它，统计、透视表、趋势图全帮你做了，不用研究函数。
>
> 📂 **整理文件** "下载文件夹按类型分一下"，几十秒整干净，照片按日期重命名、文档归类。
>
> 🧹 **清理垃圾** 扫描临时文件、浏览器缓存、微信聊天记录，列出来你点头它就清理。

类似思路的工具还有 Open Claw（小龙虾）、腾讯 WorkBuddy 等。下面用 Windows 示范一下，怎么把 Claude Desktop（手脚）装好、接上 DeepSeek（大脑）。

---

## 一、下载安装包

打开官方下载页面：

> 🔗 https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows

下载 **Claude MSIX (x64)**（ARM 设备选 arm64 版本）。

<p align="center">
  <img src="/assets/img/posts/claude-desktop-download-page.png" alt="Claude Desktop 下载页面" width="400">
</p>

---

## 二、安装

打开 PowerShell，执行：

```powershell
Add-AppxPackage -Path "C:\Users\你的用户名\Downloads\Claude.msix"
```

把路径换成你实际下载文件的位置即可。也可以直接双击 `.msix` 文件安装，弹出 UAC 确认窗口点「是」就行。

装完之后，开始菜单里就能找到 Claude 图标了。

---

## 三、关于 Cowork 和 Code

打开 Claude Desktop 你会看到两个标签：**Cowork** 和 **Code**。

它俩都能帮你写代码、编辑文件、跑命令，区别只在于运行环境：**Cowork 在沙盒里工作**，跟你的电脑隔离开，更安全但 Windows 上目前沙盒还装不上；**Code 直接在你的电脑上工作**，能读写本地文件，不需要沙盒就能用。

所以 Windows 上先用 Code 标签就够了，日常做 PPT、写报告、整理文件这些事它都能干。

> 💡 第一次打开 Code 标签需要装 Git for Windows，没装的话会提示你，装完重启一下 Claude 就行。
>
> ⚠️ 不管是 Claude Desktop、Open Claw（小龙虾），还是腾讯 WorkBuddy，这类工具本质上都是让 AI 操控你的电脑。务必保持人为审核，涉及删除、移动文件等操作时确认一下再放行，别让它全自动跑。

---

## 四、接入 DeepSeek

Anthropic 不对大陆提供服务，所以需要把模型换成 DeepSeek。Claude Desktop 自带一个图形化的切换入口，不用改系统环境变量这类麻烦操作。

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
- 模型列表：填 `deepseek-v4-pro` 和 `deepseek-v4-flash`

<p align="center">
  <img src="/assets/img/posts/deepseek-gateway-config.png" alt="配置第三方模型" style="max-width: 480px;">
</p>

点 **Test Connection** 测一下，没问题就点 **Apply locally** 保存，软件会重启。

---

## 五、验证

重启后回到登录界面，这次选 **Continue with Gateway**（不要用账号登录）。

进入后随便问一句："你好，你现在用的是什么模型？"，能正常回复就说明接好了 🎉

<p align="center">
  <img src="/assets/img/posts/claude-desktop-startup.png" alt="Claude Desktop 启动验证" width="520">
</p>

---

## 写在最后

Claude Desktop 免费下载使用，接入 DeepSeek 之后按量计费，不用订阅 Claude 的付费计划。日常用 Code 标签处理文件，基本就够了。
