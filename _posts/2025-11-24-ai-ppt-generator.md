---
layout: post
title: "我手搓了一个 AI 工具，PPT 全自动生成！"
date: 2025-11-24 10:00:00 +0800
categories: [ AI 技术, 工程实践 ]
tags: [ LangGraph, PPT, 通义千问, 自动化, Python, Agent ]
description: "用 Python 和 LangGraph，配合通义千问大模型，通过'三步法'自动化生成 PPT 初稿"

---

在日常工作中，制作 PPT 最耗时的往往不是排版，而是构思大纲和填充内容。

你是否想过：如果能给 AI 一个主题，让它像流水线工人一样，先列提纲，再填内容，最后直接生成 PPT 文件，岂不美哉？

今天，我们就用 **LangGraph** 配合 **阿里通义千问（Qwen）** 大模型，带你写一个 **"三步法" PPT 自动生成器**。

---

## 💡 核心思路

我们将任务拆解为三个简单的步骤：**规划（Plan） -> 撰写（Draft） -> 制作（Build）**，通过 LangGraph 将它们串联成一条自动化的工作流。

---

## 01 🎯 提示词工程：如何指挥 AI 干活

在看代码之前，我们先看看怎么指挥 AI 干活。这是整个流程的灵魂。

### 第一步：规划师（Plan Outline）

如果不加限制，AI 可能会废话连篇。为了让程序能自动运行，我们需要利用 **"结构化输出"** 技巧，强制 AI 返回程序能读懂的 JSON 格式。

我们需要 AI 扮演一个逻辑清晰的规划师。任务：给它一个主题，让它只吐出 10 页的大纲（标题+副标题）。

**📝 提示词设计：**

```
请先给出演示文稿大纲，只包含每一页的标题与副标题，严格返回一个 JSON 数组：
每个元素示例：{"title_text":"标题","subtitle_text":"副标题（可选）"}
要求：
- 总页数不超过 10 页；第 1 页可作为封面。
- 文风符合 PPT：短句/短语、清晰可讲述；不写空话。
- 只返回 JSON 数组本体。
主题：
{topic}

只返回JSON数组本体
```

> ⚠️ **至关重要**。如果不加限制，AI 可能会说 "好的，这是为您准备的大纲..."，这句多余的话会导致程序解析 JSON 时报错。我们要的是纯净的数据。

### 第二步：撰稿人（Draft Content）

拿到大纲后，我们进入循环，让 AI 针对每一页具体展开。任务：给它"当前页标题"，让它填补"要点（Bullet Points）"。

**📝 提示词设计：**

```
请基于给定的页面标题/副标题，为该页生成可直接用于 PPT 的要点。
严格返回一个 JSON 对象：{"title_text":"...","subtitle_text":"...","text":["要点A","要点B","..."]}
要求：
- 保持原有标题/副标题表达（允许小幅优化）。
- 要点符合 PPT 风格：短句/短语，信息清晰、可口播；不限制字数与数量。
- 不返回任何解释文字。

主题：{topic}
页面标题：{title}
页面副标题：{subtitle}
```

> 💡 **为什么这么写？** 我们将 "主题" 和 "当前页标题" 一起传给 AI，这样它既知道宏观背景（Context），又知道这一页具体该写什么，避免内容跑题或产生幻觉。

---

## 02 🧩 LangGraph 三步法拆解

有了上面的 Prompt，接下来就是用 Python 把它们串起来。LangGraph 在这里的作用，就是管理整个流程的状态（State）。

### 1. 定义状态（State）

我们需要一个"篮子"来装我们的数据，从大纲到最终内容，都存在这里：

```python
class GState(TypedDict, total=False):
    topic: str              # 用户输入的主题
    outline: List[Slide]    # 存放 AI 规划的大纲
    slides: List[Slide]     # 存放填好内容的页面
    output_path: str        # 最终文件路径
```

### 2. 编写节点（Nodes）

代码逻辑非常直观，就是调用我们上面设计的 Prompt。

- **Plan 阶段**：调用大模型，拿到 JSON 大纲，存入 `state["outline"]`
- **Draft 阶段**：一个简单的 `for` 循环，遍历大纲的每一页，再次调用大模型生成内容，存入 `state["slides"]`

*(此处省略具体 API 调用代码，核心就是将 Prompt 发送给模型并解析 JSON)*

### 3. 组装流水线（Build Graph）

最酷的部分来了，看我们如何用 LangGraph 像搭积木一样把流程串起来：

```python
workflow = StateGraph(GState)

# 添加节点（工序）
workflow.add_node("plan_outline", plan_outline)
workflow.add_node("draft_all", draft_all)
workflow.add_node("build_ppt", build_ppt)  # 调用 python-pptx 生成文件

# 定义连线（流程走向）
workflow.add_edge(START, "plan_outline")
workflow.add_edge("plan_outline", "draft_all")
workflow.add_edge("draft_all", "build_ppt")
workflow.add_edge("build_ppt", END)

# 编译图
slide_graph = workflow.compile()
```

你可以把这个图想象成一个**工厂流水线**，数据（State）在传送带上流动，经过一个个机器（Node）加工，最终产出成品。

<div align="center">
  <img src="/assets/img/posts/ai-ppt-generator-workflow.png" alt="LangGraph 工作流示意图" style="max-width: 300px;">
  <p style="color: #888; font-size: 12px; margin-top: 8px;">
    LangGraph 工作流示意图：从规划到生成 PPT 的完整流水线
  </p>
</div>

---

## 03 ✨ 运行效果实测

当我们输入主题："介绍大语言模型：原理、能力、应用与局限"。

程序会在后台静默运行：
1. Qwen 迅速构思出 10 页大纲
2. 程序自动根据大纲，生成每一页的精炼短句
3. `python-pptx` 将内容写入幻灯片

最后控制台输出：
```
PPT 输出： output/介绍大语言模型_20231123.pptx
```

打开生成的 PPT，你会发现标题清晰、要点明确。

虽然没有精美的设计（那是排版工具的事），但作为**内容初稿**，它已经帮你节省了 **90% 的脑力劳动**！

---

## 04 📝 总结与展望

这个脚本虽然只有 100 多行，但它展示了 **Agentic Workflow（代理工作流）** 的核心魅力：

| 要点 | 说明 |
|------|------|
| **结构化 Prompt** | 强制 LLM 输出 JSON，是自动化的基石 |
| **任务拆解** | 将复杂任务（做 PPT）拆解为简单任务（写大纲+写内容）|
| **状态流转** | LangGraph 让数据在不同步骤间优雅传递 |

### 👉 下一步你可以做什么？

1. **优化 Prompt**：让 AI 生成更详细的演讲备注（Notes）
2. **并发加速**：在第二步使用 `async` 并发生成，10 页 PPT 可能只需 3 秒
3. **加入模板**：修改 `build_ppt` 函数，加载公司专属的 PPT 模板

---

别再对着空白 PPT 发呆了，让 AI 成为你的生产力助手吧！
