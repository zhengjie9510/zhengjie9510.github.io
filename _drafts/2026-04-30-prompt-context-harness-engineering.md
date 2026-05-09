---
layout: post
title: "AI 工程的三个境界：从 Prompt 到 Context 再到 Harness"
date: 2026-04-03 14:00:00 +0800
categories: [ 技术, AI ]
tags: [ Prompt Engineering, Context Engineering, Harness Engineering, AI Agent ]
description: "2026 年，AI 工程已经从『写提示词』进化到了『搭系统框架』。一文说清 Prompt、Context、Harness 三层境界的核心思想与实践方法。"
image: /assets/img/posts/prompt-context-harness-cover.png
---

<div align="center" style="margin: 20px 0;">
    <img src="/assets/img/wechat-qr-white.png" alt="AI在学公众号" style="max-width: 320px; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">
      🔍 微信扫码或搜索「AI在学」关注公众号
    </p>
</div>

智能体（AI Agent）是一种能够感知外部环境、进行自主推理、规划和决策，并使用工具执行动作以实现特定目标的计算机系统。与传统的被动式 AI 不同，智能体具有高自主性，能在没有持续人工干预的情况下完成复杂任务。

> 2023 年，大家比拼的是 **Prompt 写得够不够溜**。  
> 2025 年，高手们开始钻研 **Context 管得够不够妙**。  
> 2026 年，真正的工程较量已经上升到了 **Harness 搭得够不够稳**。  
>
> 这三个词，正好对应了 AI 工程能力的三个境界。

---

## 🎯 开篇：三个境界，你在哪一层？

想象你要指挥一支军队完成任务：

| 境界 | 核心问题 | 类比 |
|:---:|:---|:---|
| **Prompt Engineering** | 怎么把命令说得更清楚？ | 给士兵下达一次精准指令 |
| **Context Engineering** | 士兵眼前该放什么情报？ | 管理作战地图和实时情报 |
| **Harness Engineering** | 怎么让整支军队连续作战数周？ | 建立轮班、后勤、进度追踪体系 |

如果你还停留在第一层，写出来的 Agent 可能连一个复杂项目都跑不完。今天我们就一层一层往上爬。

> 📝 **TODO：** 后文会补充一节，专门介绍 **什么是 AI Agent**。

---

## 📝 第一层：Prompt Engineering —— 单次对话的艺术

在聊怎么「工程化」之前，不妨先回到原点：**什么是提示词？**

> **提示词（Prompt）**是用户输入给人工智能模型的指令或问题，用于引导模型生成相应的输出内容。简单来说，提示词就是你与 AI 沟通的**那段文本**。在以 ChatGPT 为代表的大语言模型中，提示词可以是一个问题、一段说明，甚至是一组带有上下文和格式要求的完整指令。清晰、具体、有结构的提示词，通常能够显著提升 AI 输出的准确性和实用性。

明白了提示词的本质，下一步就是研究如何把它打磨成一件趁手的工具。

### 一句话定义

**Prompt Engineering = 通过优化输入文本，让大模型输出更准确、更有用的结果。**

这是最基础、也最广为人知的技能。2023 年 ChatGPT 爆火后，"提示词工程师"一度成为热门职位。

### 核心技巧（2026 年依然有效）

| 技巧 | 作用 | 示例 |
|:---|:---|:---|
| **Few-shot** | 用例子教会 AI 格式 | 给 2-3 个输入输出样例 |
| **Chain-of-Thought** | 让 AI 一步一步想 | "先分析原因，再给出结论" |
| **Role Prompting** | 给 AI 设定专家身份 | "你是一位资深架构师…" |
| **结构化输出** | 强制指定返回格式 | "用 JSON 返回，包含以下字段…" |

### 最佳实践清单

✅ **具体而非模糊**：不要说"写个总结"，要说"写 200 字总结，包含 3 个要点"  
✅ **正向指令**：说"保持简洁"，而不是"不要写太长"  
✅ **提供上下文**：给出背景、数据、约束条件  
✅ **迭代优化**：从简单 prompt 开始，根据输出不断调整

> 💡 **但 Prompt Engineering 有一个天花板**：它只解决"单次对话"的问题。一旦任务需要多轮交互、调用工具、持续数小时，光靠写好 prompt 就不够了。

---

## 🧠 第二层：Context Engineering —— 多轮对话的调度艺术

### 为什么 Prompt 不够了？

假设你的 AI Agent 要帮你重构一个大型代码库。它会：

1. 读取几十个文件
2. 运行测试、查看报错
3. 修改代码、再次验证

几轮下来，上下文窗口就会被工具调用结果、错误日志、思考过程塞爆。即使你 prompt 写得再好，AI 也会开始"失忆"、犯低级错误。

**这就是 Anthropic 在 2025 年明确提出 Context Engineering 的原因。**

### 一句话定义

> **Context Engineering = 为有限注意力窗口，持续策划、维护、压缩和更新上下文的艺术。**

Anthropic 的判断很直接：
- 上下文窗口虽然越来越大，但永远是有限资源
- token 不是越多越好，过多上下文会带来"context rot"（上下文腐烂）
- 真正的关键不是让模型"更聪明"，而是让模型每一轮"看见的世界"被组织正确

### Context Engineering 的三大支柱

#### 1️⃣ Compaction（压缩）

当对话接近上下文上限时，把历史内容高保真地压缩成摘要，然后开启一个新窗口继续。

Anthropic 的 Claude Code 就是这么做的：模型会保留关键决策、未解决的 bug、实现细节，同时丢弃冗余的工具输出。

```
原始对话：15 万 tokens
    ↓ Compaction
压缩摘要：3 万 tokens + 最近 5 个文件
    ↓ 新窗口继续
Agent 几乎无感地继续工作
```

#### 2️⃣ Structured Note-taking / Agentic Memory（结构化笔记）

把关键信息写成外部笔记，在需要时再取回，而不是一直放在上下文里。

Claude 玩 Pokémon 的经典案例：Agent 自己维护了探索地图、训练进度、战斗策略。即使上下文被重置，它只要读一下自己的笔记，就能继续长达数小时的训练计划。

#### 3️⃣ Sub-agent Architecture（子代理架构）

让子代理在"干净的上下文"里完成局部任务，再只把压缩后的结果返回给主代理。

> Anthropic 内部测试发现，**使用子代理的首要理由是上下文隔离，而不是并行加速**——这个洞见非常反直觉。

### Prompt vs Context 的对比

| 维度 | Prompt Engineering | Context Engineering |
|:---|:---|:---|
| 关注焦点 | 单次输入的质量 | 多轮信息的组织与流动 |
| 核心技能 | 写作、结构化表达 | 信息检索、压缩、记忆管理 |
| 适用场景 | 聊天、内容生成 | 长运行 Agent、代码重构、深度研究 |
| 失败模式 | 输出不符合预期 | 上下文塞爆、模型"失忆"、决策漂移 |

---

## 🏗️ 第三层：Harness Engineering —— 长周期任务的系统工程

### 从"会说话"到"能干活"

2025 年底，Anthropic 发布了一篇极具洞察力的博客：《Effective Harnesses for Long-Running Agents》。

他们提出了一个尖锐的问题：

> 即使给 Claude Opus 4.5 配上最好的 Context Engineering，让它循环运行很多个 context window，如果只是给一个高级 prompt 比如"克隆一个 claude.ai"，它依然做不出生产级别的应用。

为什么？因为有两个致命缺陷：

1. **一口吃成胖子**：Agent 总想一次性把整个 App 做完，结果做到一半上下文耗尽，下一轮换班的 Agent 对着半成品代码一脸懵逼。
2. **提前宣布胜利**：后面的 Agent 看到前面已经做了不少功能，误以为项目已经完成，直接收工。

### Harness Engineering 的解决方案

Anthropic 的答案是设计一个**两阶段 Harness（框架/约束）**：

#### 🚀 Initializer Agent（初始化代理）

第一次运行时，用专门的 prompt 让 Agent 搭建项目基础设施：

- 写一个 `init.sh` 脚本（启动开发环境）
- 创建 `feature_list.json`（列出 200+ 个具体功能，全部标记为未完成）
- 创建 `claude-progress.txt`（进度日志）
- 做一次初始 git commit

#### 🔧 Coding Agent（编码代理）

之后的每一轮 session，Agent 都被要求：

1. **读进度日志 + git log**，快速了解项目现状
2. **只挑一个未完成的功能**来实现
3. **写测试验证**（Anthropic 甚至给了它 Puppeteer MCP 来做端到端浏览器测试）
4. **提交 git commit + 更新进度日志**
5. **保证代码处于"可合并状态"**——没有重大 bug、文档清晰

### Harness 的核心设计原则

| 原则 | 说明 | 效果 |
|:---|:---|:---|
| **增量推进** | 每次只做一件事 | 避免半途而废的烂尾工程 |
| **状态外化** | 进度、计划、决策都写到文件里 | 新 session 秒速上手 |
| **测试闭环** | 每个功能必须有端到端验证 | 防止"我以为做完了"的幻觉 |
| **可合并状态** | 每次结束时代码要像能发 PR 一样干净 | 避免技术债务滚雪球 |

### 一个典型的 Session 开场白

```
[Agent] 我先了解一下项目当前状态。
[Tool] bash - pwd
[Tool] read - claude-progress.txt
[Tool] read - feature_list.json
[Tool] bash - git log --oneline -20

[Agent] 让我用 init.sh 启动开发服务器，验证基本功能是否正常。
[Tool] bash - ./init.sh
[Tool] browser - 测试登录、聊天、主题切换

[Agent] 核心功能正常。接下来我实现「新聊天按钮」这个功能。
```

看到这个流程，你会发现：**Agent 不再是在"猜"，而是在"读"**。

---

## 🔄 三层境界的关系图

```
┌─────────────────────────────────────────────────────────────┐
│  用户指令层                                                  │
│  Prompt Engineering：把话说清楚                              │
│  （单次对话的有效性）                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  信息调度层                                                  │
│  Context Engineering：给对的信息、在对的时机                  │
│  （多轮对话的连贯性）                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  系统架构层                                                  │
│  Harness Engineering：搭好工作流、验证、交接机制              │
│  （长周期任务的可靠性）                                       │
└─────────────────────────────────────────────────────────────┘
```

**只有三层都做好，AI 才能真正完成复杂、长期、可靠的任务。**

---

## 🛠️ 给开发者的实践建议

### 如果你现在刚开始用 AI 辅助工作

- 先练好 **Prompt Engineering**
- 学会用 XML 标签、Markdown 标题分隔不同部分
- 多用 Few-shot 和 Chain-of-Thought

### 如果你已经在构建 AI Agent

- 必须引入 **Context Engineering**
- 监控上下文窗口使用率，在 50%-70% 时触发压缩
- 给 Agent 设计外部记忆机制（文件、数据库、向量检索）
- 用子代理隔离复杂子任务

### 如果你在做长周期、生产级的 Agent 项目

- 升级到 **Harness Engineering**
- 写 initializer prompt，让第一步把环境搭规范
- 用结构化文件（JSON/Markdown）管理进度和任务清单
- 每次 session 必须验证基础功能没有被破坏
- 把"干净的交接状态"写进 prompt 要求里

---

## 💬 结语

2023 年，Prompt Engineering 是显学；  
2025 年，Context Engineering 成为分水岭；  
2026 年，Harness Engineering 正在定义下一代 AI 系统的工程标准。

这三个境界，本质上回答的是同一个问题：**怎么让 AI 从"能聊"变成"能干活"，再从"能干活"变成"能持续稳定地干复杂活"。**

如果你发现自己的 Agent 总在长任务后半段掉链子，不妨问问自己：**你现在的瓶颈，是在"说什么"，还是在"给什么看"，抑或是在"怎么组织工作"？**

找到答案，就是突破的开始。

---

## 📚 延伸阅读

- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Developer Platform: Context Engineering Cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- [V7 Labs: The Ultimate Guide to AI Prompt Engineering](https://www.v7labs.com/blog/prompt-engineering-guide)
