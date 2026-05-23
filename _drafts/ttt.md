---
layout: post
title: 手把手教你在 Windows 上安装 Claude Code 并接入 DeepSeek
date: 2026-05-25 7:00:00
categories: [AI工具]
tags: [Claude Code, DeepSeek, Windows, 教程]
image:
description: 完全面向小白的 Claude Code 安装与配置教程，接入 DeepSeek，国内可用，全程约 15 分钟。
---

## Claude Code 是什么？

Claude Code 是 Anthropic 推出的 AI 助手，直接运行在命令行里。和普通 AI 聊天工具最大的区别在于：它不只是"给建议"，而是真的能动手干活。

你可以用自然语言跟它对话，告诉它你想做什么，它会直接在你的电脑上帮你完成。对于没有技术背景的普通人来说，这意味着很多原本"不会操作"的事，现在只需要开口说就能搞定：

- **整理资料、处理文件**：一个文件夹里有几十份 Word 或 PDF，让它按你的要求分类、重命名、提取关键内容，几秒钟完成
- **读文献、啃报告**：把一份长篇英文论文或行业报告丢给它，让它帮你梳理核心论点、提炼关键数据，告别逐页翻译的痛苦
- **数据整理与汇总**：有一堆 Excel 表格需要合并对比？告诉它你想看什么结果，它帮你处理好，直接输出
- **辅助写作**：给它提供你的素材和思路，让它帮你起草报告、邮件、方案，再自己润色，效率翻倍
- **自动化重复操作**：每周都要做同样的事？描述清楚流程，让它写成脚本，以后一键完成
- **学习答疑**：遇到不懂的概念或难题，直接问它，它能结合你本地的资料给出针对性的解答

简单来说，只要是能在电脑上操作的事，很多都可以交给它——而且你不需要懂任何技术。

听起来很吸引人，但有两个现实问题：

- **价格不便宜**：Claude Code 官方使用 Anthropic 的 API，按量计费，对普通用户来说成本较高
- **国内无法直接使用**：Anthropic 目前不对中国大陆提供服务，直接使用官方渠道行不通

好在 Claude Code 支持对接第三方模型。我们可以把背后的大模型换成 **DeepSeek**——它的 API 国内可以直接访问，价格也非常亲民，效果同样出色。

本教程就是手把手带你完成这套配置，让你在国内也能顺畅使用 Claude Code。

---

## 第 1 步：安装 Git

Claude Code 的运行依赖 Git，所以第一件事是先把它装好。

1. 浏览器打开 **https://git-scm.com/install/windows** ，点击 **Click here to download** 开始下载

![](assets/img/posts/屏幕截图 2026-05-23 091709.png)

2. 下载完成后，双击安装文件（文件名类似 `Git-2.x.x-64-bit.exe`）
3. 全程点「Next」，**所有选项保持默认，不需要改任何东西**，最后点「Install」
4. 安装完成后点「Finish」

![](assets/img/posts/屏幕截图 2026-05-23 092546.png)

---

## 第 2 步：安装 Claude Code

按键盘上的 `Win + R`，在弹出的小窗口里输入 `cmd`，回车，打开命令提示符窗口。

![](assets/img/posts/屏幕截图 2026-05-23 085519.png)

在窗口里输入以下命令，按回车：

```
winget install Anthropic.ClaudeCode
```

![](assets/img/posts/屏幕截图 2026-05-23 085624.png)

安装过程中如果出现「是否同意条款」的提示，输入 `Y` 后按回车继续。看到 `已安装成功` 字样，说明安装成功 ✅

安装完成后，**关掉 CMD 窗口，重新打开一个新的**，输入以下命令验证安装结果：

```
claude --version
```

能看到版本号就说明一切正常 ✅

![](assets/img/posts/屏幕截图 2026-05-23 085744.png)

---

## 第 3 步：申请 DeepSeek API Key

1. 浏览器打开 **https://platform.deepseek.com**，注册账号并登录
2. 进入左侧菜单「API Keys」，点击「创建 API Key」

3. 随便填一个名称（比如 `my-key`），点创建，页面会生成一串以 `sk-` 开头的字符

![](assets/img/posts/微信图片_20260523093546_26_76.png)

> ⚠️ **这个 Key 只会显示这一次！请立刻复制，粘贴到记事本里保存好，关掉弹窗后就再也看不到完整内容了。**

4. 点击左侧「充值」，充 10 元即可用很久，DeepSeek 的 API 定价非常实惠

---

## 第 4 步：配置 DeepSeek

将以下命令**全部选中复制，粘贴进 CMD 窗口，按回车执行**。

执行前，先把第二行的 `sk-你的Key` 替换成你上一步保存的真实 Key。

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

![](assets/img/posts/微信图片_20260523095509_28_76.png)

> ⚠️ **执行完之后，必须关掉 CMD 窗口，重新打开一个新的**，环境变量才会正式生效。在同一个窗口里是看不到效果的。

---

## 第 5 步：导航到你的工作文件夹

这一步很多教程都会跳过，但它非常关键。

Claude Code 启动后，会以你**当前所在的文件夹**作为工作目录——它能读取这个文件夹里的所有文件和子文件夹，也会把新生成的文件保存在这里。换句话说，**你在哪个文件夹里启动它，它就在哪里工作**。

举个例子：如果你把论文资料都放在 `D:\论文资料`，只需要右键点击这个文件夹，选择 “在终端中打开”，然后在弹出的窗口里输入 claude 启动，它就能立刻读取里面的文件啦！

![](assets/img/posts/屏幕截图 2026-05-23 101210.png)

---

## 第 6 步：启动并验证

在切换到目标文件夹后，输入：

```
claude
```

启动后，在对话框里输入：

```
你好，你现在用的是什么模型？
```

如果它回复了，说明一切配置成功 🎉

![](assets/img/posts/屏幕截图 2026-05-23 101638.png)

现在你可以用中文跟它对话，让它帮你读取当前文件夹里的文件、整理资料、辅助写作，尽情探索。想退出对话时，输入 `/exit` 即可。

---

## 常见问题

**Q：输入 `winget` 命令后提示"找不到命令"？**
打开微软商店，搜索「应用安装程序」（App Installer），点击更新后重试。

**Q：输入 `claude --version` 后提示找不到命令？**
关掉 CMD 重新打开再试；若还是不行，重启电脑后再尝试。

**Q：启动时提示 API 认证失败？**
回到第 4 步，检查 `ANTHROPIC_AUTH_TOKEN` 后面的 Key 是否填写完整，前后不能有多余的空格。

**Q：Claude Code 找不到我的文件？**
很可能是启动时所在的文件夹不对。退出后用 `cd` 切换到正确的文件夹，再重新运行 `claude`。

**Q：如何更新 Claude Code 到最新版本？**
在 CMD 中运行 `winget upgrade Anthropic.ClaudeCode` 即可。
