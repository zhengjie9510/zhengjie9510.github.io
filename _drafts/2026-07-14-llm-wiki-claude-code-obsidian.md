---
layout: post
title: "把体力活留给 AI，把思考留给自己：LLM Wiki 搭建实录"
date: 2026-07-14 10:00:00 +0800
categories: [ AI 工具 ]
tags: [ LLM Wiki, Claude Code, Obsidian, 知识库 ]
description: "Claude Code + Obsidian，零代码搭建一个会自动进化的 AI 知识库"
image: /assets/img/posts/llm-wiki-build-cover.png
draft: true
---

收藏从未停止，整理从未开始——这是大多数人的知识管理现状。

但问题不是懒。分类、打标签、写摘要、建双链……这些事天然不适合人类做：重复、琐碎、永不停止。人会累，会忘，会放弃。所以大多数人的知识库都烂尾了。

Andrej Karpathy 给了一个解法：**让 AI 来做这些体力活。** 人类只负责找好信息源，然后思考它们意味着什么。

这不是又一个效率工具，这是一次分工的重新划定。

话不多说，直接看我是怎么搭的。

## 🧰 你需要什么

- **Claude Code**——大脑，负责读、写、整理
- **Obsidian**（免费，[obsidian.md](https://obsidian.md)）——浏览器，负责看
- **电脑上一个空文件夹**——你的知识库

就这三样。

## 📁 第一步：建两个文件夹

在你的电脑上找个地方，新建一个文件夹，叫 `ai-wiki`。进去，再在里面新建一个子文件夹，叫 `raw`。

```
ai-wiki/
└── raw/    ← 原始资料丢这里，只读不改
```

就这两层，没了。

## 💬 第二步：把 Karpathy 的思路文件丢给 Claude Code

在 `ai-wiki/` 目录下打开 Claude Code，粘贴下面这段话：

> 我希望你阅读 Andrej Karpathy 的这份思路文件，并帮我在这个目录下搭建一个 LLM Wiki。在你开始之前，请先问问我这个 Wiki 的内容是什么，以及我计划使用哪些资源。

然后把 Karpathy 的 [LLM Wiki 思路文件](https://gist.github.com/karpathy/1a3a5b0c2d4e5f6g7h8i9j0k) 全文粘贴在后面。

Claude 读完文件后，没有立刻动手建文件夹、写代码。它先反问了我：

![Claude 反问我的问题](/assets/img/posts/llm-wiki-claude-questions.png)

▸ **这个"先问再动手"的环节，是整个搭建过程中最重要的一步。** LLM Wiki 不是通用模板——AI 领域的 Wiki 跟读书笔记的 Wiki，结构完全不同。AI 必须先把你的场景问清楚，才能设计出真正合身的框架。

## ✏️ 第三步：回答它

我的回答很简单：

> AI 领域的知识管理，目前还没有具体资料。

对，就这么一句话。没有详细规划，没有资料清单——我就是想先搭个框架，后面再慢慢往里喂。

这也正是 LLM Wiki 灵活的地方：你不用一开始就想清楚所有细节，先搭起来，边用边长。

Claude 听完，立刻为我量身写了一整套规则文件：

![Claude 生成的 CLAUDE.md](/assets/img/posts/llm-wiki-claude-md.png)

同时自动初始化了 `wiki/index.md` 和 `wiki/log.md`。最后它告诉我：

> 可以开始喂第一篇资料了。

你什么都没干——没写一行代码，没改一行配置——整个 Wiki 的框架已经搭好了。这就是这个模式的核心：**AI 不仅替你读资料，还替你设计知识结构。**

## 📥 第四步：喂第一篇资料

框架搭好了，我丢进第一篇——一篇讲 Agent 架构的技术文章：

> "D:\Downloads\agent-prompt-context-harness.md" 加入这篇文章。

Claude 按 Ingest 工作流自动处理：先把文件复制到 `raw/`，通读全文，然后交了一份"阅读理解作业"——提炼出核心框架，给出 Wiki 页面创建计划：

![Claude 的 ingest 分析和页面计划](/assets/img/posts/llm-wiki-ingest-agent.png)

最后它还主动问了一句：**"你有什么特别关注的方向，或者希望我调整的吗？"**

这个细节，比我想的周到。它不是闷头建页面，而是动手前先跟你对一遍理解——确保人和 AI 对文章的认识是一致的。错了就改，对了就继续。

▸ **这就是 LLM Wiki 和自动摘要工具的本质区别：前者是协作过程，后者只是一次输出。**

## 🔭 第五步：打开 Obsidian

装好 Obsidian，新建 Vault，指向 `ai-wiki/` 文件夹，点开关系图谱——

![Obsidian 关系图谱](/assets/img/posts/llm-wiki-obsidian-graph.png)

每个节点是一页知识，每条连线是 AI 自动建立的关联。随着资料越投越多，这张网不会变乱，反而越来越密。这就是**知识复利**。

## ⚡ 用起来

Wiki 搭好了，真正的好处在日常使用中才会体现。

比如我问了一个具体问题：

> Claude Code 如何接入 DeepSeek 模型？基于知识库回答。

注意"基于知识库回答"这六个字——不是搜互联网，不是翻原始 PDF，就是用它自己建好的 Wiki。

Claude 读了 Wiki 里的 `ClaudeCode` 和 `DeepSeek` 两个页面，几秒内给出了一份完整的配置指南：

![基于 Wiki 回答 DeepSeek 接入问题](/assets/img/posts/llm-wiki-deepseek-query.png)

没有重新检索任何原始文件。答案直接来自 Wiki 里已经提炼好的知识。

▸ **知识只提炼一次，之后无限复用。** 这就是 LLM Wiki 和 RAG 的本质区别。

---

**没有代码，没有配置文件。** 你只需要：

> 把思路文件丢给 Claude Code → 回答它的反问 → 往里喂资料 → 打开 Obsidian 看图谱

人类的唯一职责是找好信息源，然后思考这些知识意味着什么。

> **把体力活留给 AI，把思考留给自己。**
