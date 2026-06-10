---
layout: post
title: 普通人也能用的 AI 助手，我花了 20 分钟装好了
date: 2026-05-23 7:00:00
categories: [ AI 工程实践 ]
tags: [Claude Code, DeepSeek, Windows, 教程]
description: 一篇清晰易上手的 Claude Code 安装与配置教程，演示如何在 Windows 上接入 DeepSeek。
image: assets/img/posts/claude-code-cover.png
---

<div align="center" style="margin: 20px 0;">
    <img src="/assets/img/wechat-qr-white.png" alt="AI在学公众号" style="max-width: 320px; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">
      🔍 微信扫码或搜索「AI在学」关注公众号
    </p>
</div>

## Claude Code 是什么？

**Claude Code 是 Anthropic 推出的命令行智能助手。它和普通智能对话工具最大的区别是：不只是“给建议”，而是真的能直接动手干活。**

你可以用自然语言跟它对话，告诉它你想做什么，它会直接在你的电脑上帮你完成。对于没有技术背景的普通人来说，这意味着很多原本“不会操作”的事，现在只需要开口说就能搞定：

- **整理资料、处理文件**：一个文件夹里有几十份 Word 或 PDF，让它按你的要求分类、重命名、提取关键内容，几秒钟完成
- **读文献、啃报告**：把一份长篇英文论文或行业报告丢给它，让它帮你梳理核心论点、提炼关键数据，告别逐页翻译的痛苦
- **数据整理与汇总**：有一堆 Excel 表格需要合并对比？告诉它你想看什么结果，它帮你处理好，直接输出
- **辅助写作**：给它提供你的素材和思路，让它帮你起草报告、邮件、方案，再自己润色，效率翻倍
- **自动化重复操作**：每周都要做同样的事？描述清楚流程，让它写成脚本，以后一键完成
- **学习答疑**：遇到不懂的概念或难题，直接问它，它能结合你本地的资料给出针对性的解答

简单来说，只要是能在电脑上操作的事，很多都可以交给它——而且你不需要懂任何技术。

听起来很吸引人，但有两个现实问题：

> **价格不便宜**：Claude Code 官方使用 Anthropic 的接口，按量计费，对普通用户来说成本较高

> **国内无法直接使用**：Anthropic 目前不对中国大陆提供服务，直接使用官方渠道行不通

---

**解决方案：换成国内可用的方案**

好在 Claude Code 支持对接第三方模型。我们可以把背后的大模型换成国内可用的方案，比如 **DeepSeek**、**通义千问** 等。

这篇教程里，我们先以 **DeepSeek** 为例，因为它现在相对便宜。先按这套流程跑通，后面再换成别的模型也不难。

---

## 第 1 步：安装 Git

Claude Code 的运行依赖 Git，所以第一件事是先把它装好。

1. 浏览器打开 **https://git-scm.com/install/windows**，点击 **Click here to download** 开始下载

<img src="/assets/img/posts/claude-code-git-download.png" alt="Git 下载页面" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

2. 下载完成后，双击安装文件（文件名类似 `Git-2.x.x-64-bit.exe`）
3. 全程点「Next」，**所有选项保持默认，不需要改任何东西**，最后点「Install」
4. 安装完成后点「Finish」

<img src="/assets/img/posts/claude-code-git-install-finish.png" alt="Git 安装完成" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

---

## 第 2 步：安装 Claude Code

按键盘上的 `Win + R`，在弹出的小窗口里输入 `cmd`，回车，打开命令提示符窗口。

<img src="/assets/img/posts/claude-code-win-r-cmd.png" alt="Win + R 运行对话框" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

在窗口里输入以下命令，按回车：

```
winget install Anthropic.ClaudeCode
```

<img src="/assets/img/posts/claude-code-winget-install.png" alt="winget 安装 Claude Code" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

安装过程中如果出现「是否同意条款」的提示，输入 `Y` 后按回车继续。看到“已安装成功”字样，说明安装成功 ✅

安装完成后，**关掉 CMD 窗口，重新打开一个新的**，输入以下命令验证安装结果：

```
claude --version
```

能看到版本号就说明一切正常 ✅

<img src="/assets/img/posts/claude-code-version-check.png" alt="查看 Claude Code 版本号" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

---

## 第 3 步：申请 DeepSeek 接口密钥

1. 浏览器打开 **https://platform.deepseek.com**，注册账号并登录
2. 进入左侧菜单「API Keys」，点击「创建 API Key」

3. 随便填一个名称（比如 `my-key`），点创建，页面会生成一串以 `sk-` 开头的密钥

<img src="/assets/img/posts/deepseek-api-key-create.png" alt="DeepSeek 创建 API Key" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

> ⚠️ **这个密钥只会显示这一次！请立刻复制，粘贴到记事本里保存好，关掉弹窗后就再也看不到完整内容了。**

4. 点击左侧「充值」，充 10 元即可用很久，DeepSeek 的接口定价非常实惠

---

## 第 4 步：配置 DeepSeek

申请好密钥后，就可以把 Claude Code 背后的模型切到 DeepSeek 了。

将以下命令**全部选中复制，粘贴进 CMD 窗口，按回车执行**。

执行前，先把第二行的 `sk-你的Key` 替换成你上一步保存的真实密钥。

```
setx ANTHROPIC_BASE_URL "https://api.deepseek.com/anthropic"
setx ANTHROPIC_AUTH_TOKEN "sk-你的Key"
setx ANTHROPIC_MODEL "deepseek-v4-pro[1m]"
setx ANTHROPIC_DEFAULT_OPUS_MODEL "deepseek-v4-pro[1m]"
setx ANTHROPIC_DEFAULT_SONNET_MODEL "deepseek-v4-pro[1m]"
setx ANTHROPIC_DEFAULT_HAIKU_MODEL "deepseek-v4-flash"
setx CLAUDE_CODE_SUBAGENT_MODEL "deepseek-v4-flash"
setx CLAUDE_CODE_EFFORT_LEVEL "max"
```

每一行执行后都会显示「成功: 指定的值已得到保存。」，说明写入成功 ✅

<img src="/assets/img/posts/deepseek-env-config-result.png" alt="环境变量配置结果" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

> ⚠️ **执行完之后，必须关掉 CMD 窗口，重新打开一个新的**，环境变量才会正式生效。在同一个窗口里是看不到效果的。

---

## 第 5 步：导航到你的工作文件夹

这一步很多教程都会跳过，但它非常关键。

Claude Code 启动后，会以你**当前所在的文件夹**作为工作目录。它能读取这个文件夹里的所有文件和子文件夹，也会把新生成的文件保存在这里。换句话说，**你在哪个文件夹里启动它，它就在哪里工作**。

举个例子：如果你把论文资料都放在 `D:\论文资料`，只需要右键点击这个文件夹，选择“在终端中打开”，然后在弹出的窗口里输入 `claude` 启动，它就能立刻读取里面的文件。

<img src="/assets/img/posts/claude-code-open-terminal.png" alt="右键在终端中打开" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

---

## 第 6 步：启动并验证

前面的安装和配置完成后，最后只需要启动一次确认能不能正常工作。

在切换到目标文件夹后，输入：

```
claude
```

启动后，在对话框里输入：

```
你好，你现在用的是什么模型？
```

如果它回复了，说明一切配置成功 🎉

<img src="/assets/img/posts/claude-code-startup-verify.png" alt="Claude Code 启动验证" style="max-width: 480px; border-radius: 6px; display: block; margin: 0 auto;">

现在你可以用中文跟它对话，让它帮你读取当前文件夹里的文件、整理资料、辅助写作，尽情探索。想退出对话时，输入 `/exit` 即可。
