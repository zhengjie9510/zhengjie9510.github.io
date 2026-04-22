---
layout: post
title: "LangChain、LangGraph、DeepAgents 傻傻分不清？一文看懂怎么选"
date: 2026-04-22 16:00:00 +0800
categories: [ AI 技术, Agent 开发 ]
tags: [ LangChain, LangGraph, DeepAgents, AI Agent, 框架对比 ]
description: "用通俗的语言和生活中的类比，帮你理清 LangChain、LangGraph 和 DeepAgents 的定位、关系和适用场景"
---

AI Agent 的开发工具如今百花齐放，但如果要选一个**生态最成熟、社区最活跃**的框架来入门，LangChain 几乎是绕不过去的名字——它是目前 GitHub 上 stars 数最多的 Agent 开发框架之一（超过 10 万 ⭐），Klarna、Uber、LinkedIn 等大公司都在用它构建生产级应用。

而 LangChain 家族内部最近又添了新成员 **DeepAgents**，再加上原本的 **LangGraph**，三者的名字越来越像，文档还互相引用，很多人看完更懵了：它们到底啥关系？我该用哪个？

今天这篇就帮你彻底理清它们的关系。不用看源码，不用啃概念，看完你就知道该怎么选了。

---

## ✨ 先给一个「一句话总结」

如果把开发 AI Agent 比作**造车** 🚗，三者的角色从「底盘」到「整车」分别是：

| 工具 | 角色类比 | 一句话定位 |
|:---|:---|:---|
| 🔧 **LangGraph** | 发动机与底盘系统 | **运行时**：提供持久动力、稳定控制和故障恢复的底层基础设施 |
| 🏭 **LangChain** | 整车厂的标准组装线 | **框架**：给你现成零件和说明书，快速拼装出一辆能跑的车 |
| 🚙 **DeepAgents** | 搭载了智能驾驶系统的整车 | **工具带**：出厂自带导航、自动泊车、车载助手，拿来就能开 |

> 💡 **记住这个公式**：
> **LangGraph** 负责「稳定跑下去」 → **LangChain** 负责「快速搭起来」 → **DeepAgents** 负责「聪明地自己干」

---

## ① LangGraph：藏在下面的「底盘系统」

我们先从最底层开始聊。LangGraph 是 LangChain 生态里最低调、但也最不可或缺的一环。

如果说 LangChain 是「让用户爽」，那 LangGraph 就是「让系统稳」。它是一个**非常低级别的编排框架和运行时**，不帮你封装提示词，不预设 Agent 架构，只专注于一件事——**让 Agent 在复杂、长周期的任务里，跑得稳、断得了、续得上。**

```python
from langgraph.graph import StateGraph, MessagesState, START, END

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
```

### ⚙️ 它解决的是什么问题？

想象你写了一个 Agent 去处理一份 200 页的报告：分析、总结、提取关键数据、生成图表……整个过程可能要跑 20 分钟。跑到第 15 分钟服务器突然重启了，**普通脚本就直接完蛋了，但 LangGraph 可以从断点续跑。**

这就是 LangGraph 的核心能力：

| 能力 | 符号 | 说明 |
|:---|:---|:---|
| **持久执行** | 🛡️ | Agent 遇到故障能从上次状态恢复，长时间任务不怕中断 |
| **流式输出** | 🌊 | 支持工作流和响应的实时流式传输 |
| **人机协同** | 👤🤖 | 随时让人类检查、修改 Agent 的状态 |
| **全面记忆** | 🧠 | 短期工作记忆 + 跨会话的长期记忆 |
| **可视化调试** | 🔍 | 配合 LangSmith 追踪执行路径和状态变化 |

### 🎯 什么时候选 LangGraph？

| 场景 | 理由 |
|:---|:---|
| 需要对每一步流程精细化控制 | 低级别 API，节点和边完全自定义 |
| 长时间运行任务 | 故障恢复、断点续跑 |
| 确定性流程 + Agent 决策混合编排 | 图结构天然适合这种场景 |
| 生产级部署 | 被 Uber、J.P. Morgan 等公司验证过 |

---

## ② LangChain：最熟悉的「脚手架」

在 LangGraph 这个「底盘」之上，LangChain 搭起了一条**标准组装线**。

它的核心目标只有一个——**让你用不到 10 行代码，就能连接 OpenAI、Anthropic、Google 等各家大模型，搭出一个能调用工具的 Agent。**

```python
from langchain.agents import create_agent

agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
```

### ✅ 它的价值在哪里？

- **标准化抽象** 🔌：不管你是调用 GPT 还是 Claude，写法几乎一样
- **丰富的集成** 🧩：模型、向量库、文档加载器……生态非常完善
- **快速上手** 🚀：不需要懂底层原理，复制粘贴就能跑

LangChain 1.0 的 Agent 底层其实是跑在 LangGraph 上的（持久化、流式输出、人机协同这些能力都来自 LangGraph），但 LangChain 把这些细节都封装好了，**你不需要知道 LangGraph 也能用得挺好。**

### 🎯 什么时候选 LangChain？

| 场景 | 理由 |
|:---|:---|
| 想快速验证一个 Agent 想法 | 10 行代码就能跑起来 |
| Agent 逻辑不太复杂 | 主要是「模型 + 工具」的循环调用 |
| 团队需要统一标准 | 提供一套大家都熟悉的抽象层 |

---

## ③ DeepAgents：出厂即「高配」的智能整车

DeepAgents 是 LangChain 家族里最新的成员，也是**级别最高**的一个。官方把它叫做 **Agent Harness（工具带）**——你可以理解为，它是一辆出厂就搭载了智能驾驶系统的整车。

它基于 LangChain 的核心构建块，使用 LangGraph 作为运行时，但在这之上又封装了一大层**面向复杂任务的「自主能力」**。

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
```

### 🚀 它多了哪些「高配」能力？

| 能力 | 符号 | 说明 |
|:---|:---|:---|
| **任务规划** | 📋 | 自动分解复杂任务，用待办清单跟踪多步骤执行 |
| **文件系统管理** | 📁 | 读写文件、管理上下文，支持内存/本地磁盘/云端存储 |
| **子 Agent 委派** | 👥 | 像项目经理一样派活，保持上下文隔离 |
| **长期记忆** | 🧬 | 跨会话、跨线程持久化记忆 |
| **权限控制** | 🔒 | 声明式规则限制 Agent 能读写的文件范围 |
| **人机审批** | ✋ | 敏感操作需要人类确认 |
| **Shell 命令执行** | 💻 | 沙箱环境下可直接执行系统命令 |

### 🎯 什么时候选 DeepAgents？

| 场景 | 理由 |
|:---|:---|
| 复杂多步任务 | 自主规划、分解、执行 |
| 需要和文件/代码/搜索打交道 | 内置文件系统和工具 |
| 想要类 Devin / Cursor 的编码 Agent | 自带 CLI 终端编码 Agent |
| 希望开箱即用 | 不需要自己从头搭规划、记忆等模块 |

> 🔔 **小提醒**：DeepAgents 还自带 **ACP（Agent Client Protocol）连接器**，可以直接集成到 Zed 等代码编辑器里使用。

---

## 🏗️ 一张图看懂三者关系

```
╔═════════════════════════════════════════════════════════════╗
║  🚙 DeepAgents (Harness / 工具带)                           ║
║     预置工具 + 规划能力 + 子Agent + 文件系统                 ║
║     【面向复杂自主任务】                                      ║
╠═════════════════════════════════════════════════════════════╣
║  🏭 LangChain (Framework / 框架)                            ║
║     标准抽象 + 模型集成 + 快速开发                           ║
║     【面向快速搭建Agent】                                     ║
╠═════════════════════════════════════════════════════════════╣
║  🔧 LangGraph (Runtime / 运行时)                            ║
║     持久执行 + 流式传输 + 人机协同 + 状态管理                   ║
║     【面向稳定运行和编排】                                      ║
╚═════════════════════════════════════════════════════════════╝
```

> 🔑 **关键结论**：
> - LangChain 1.0 的 Agent **建立在 LangGraph 之上**
> - DeepAgents **同时建立在 LangChain 和 LangGraph 之上**
> - 三者不是互斥的，而是**层层叠加**的关系

---

## 🎮 选择指南：该用哪个？

| 你的场景 | 推荐选择 | 理由 |
|:---|:---|:---|
| 刚入门，想 10 分钟跑通第一个 Agent | 🏭 **LangChain** | 最快上手，生态最丰富 |
| 需要快速搭建标准化 Agent 应用 | 🏭 **LangChain** | 抽象层统一，团队协作友好 |
| 要对 Agent 的每个节点精细控制 | 🔧 **LangGraph** | 低级别图编排，完全自定义 |
| 长时间运行、需要故障恢复的任务 | 🔧 **LangGraph** | 持久执行 + 状态恢复 |
| 确定性流程 + Agent 决策的混合编排 | 🔧 **LangGraph** | 图结构完美适配 |
| 复杂多步任务，需要自主规划和分解 | 🚙 **DeepAgents** | 内置规划、记忆、文件系统 |
| 需要文件操作、子 Agent、长期记忆 | 🚙 **DeepAgents** | 开箱即用，不用重复造轮子 |
| 想要类 Devin / Cursor 的编码 Agent | 🚙 **DeepAgents** | 自带 CLI 编码 Agent |

---

## 📝 写在最后

LangChain 生态的分层设计其实非常清晰：**LangGraph 打底 → LangChain 提速 → DeepAgents 封顶。**

| 你的需求 | 选型 |
|:---|:---|
| 想 **快速验证** | 拿 LangChain |
| 想 **稳定可控** | 用 LangGraph |
| 想 **放手让 Agent 自己干** | 上 DeepAgents |

当然，这三个库都是开源的，你也可以混搭使用：比如在 LangGraph 里自己实现一部分 DeepAgents 的能力，或者在 DeepAgents 的基础上扩展自定义工具。选型没有绝对的对错，**适合你当前阶段和业务复杂度的，就是最好的。**

如果你已经在用其中某一个，欢迎在评论区分享你的使用体验 👇

---

> 📚 **参考链接**
> 1. DeepAgents Overview — `https://docs.langchain.com/oss/python/deepagents/overview`
> 2. LangChain Overview — `https://docs.langchain.com/oss/python/langchain/overview`
> 3. LangGraph Overview — `https://docs.langchain.com/oss/python/langgraph/overview`
> 4. LangChain Products & Concepts — `https://docs.langchain.com/oss/python/concepts/products`
