---
layout: post
title: "LangChain、LangGraph、Deep Agents：三者核心能力与选型指南"
date: 2026-05-22 7:00:00
categories: [ AI Agent, Agent 开发 ]
tags: [ LangChain, LangGraph, DeepAgents, AI Agent, 框架对比 ]
description: "基于 LangChain 官方文档，用通俗易懂的方式梳理 LangChain、LangGraph 和 Deep Agents 的核心能力与适用场景"
image: /assets/img/posts/langchain-langgraph-deepagents-layers.png
---

<div align="center" style="margin: 20px 0;">
    <img src="/assets/img/wechat-qr-white.png" alt="AI在学公众号" style="max-width: 320px; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">
      🔍 微信扫码或搜索「AI在学」关注公众号
    </p>
</div>

提到 AI Agent 开发，**LangChain** 是一个绕不过去的名字——它是目前 GitHub 上 stars 数最多的 Agent 开发框架之一（超过 10 万 ⭐），Klarna、Uber、LinkedIn 等大公司都在用它构建生产级应用。

但很多人没意识到的是，LangChain 生态早已不是“一个框架打天下”。在这个生态里，**LangChain**、**LangGraph** 和 **Deep Agents SDK** 扮演着完全不同的角色：LangChain 是 Framework（框架），负责提供开发抽象；LangGraph 是 Runtime（运行时），负责稳定运行和复杂编排；Deep Agents SDK 是 Harness（即“Agent 驾驭框架”），在最上层提供开箱即用的自主能力。三者不是“谁取代谁”的关系，而是**分工协作**——LangGraph 打底 → LangChain 提速 → Deep Agents 封顶。

不过，因为三者名字里都带“Lang”、文档又分布在同一个官网里，很多开发者刚入门时都会踩同一个坑：把它们当成互相竞争的框架来比较，反复纠结“该学哪个”“LangChain 是不是已经过时了”。这篇文章会带你从核心能力、适用场景到选型建议，彻底理清它们的真实关系。

---

## 一、🧩 LangChain：快速搭建 Agent 的框架

LangChain 是一个**高阶开发框架**，核心目标是让你用不到 10 行代码，就能连接各家大模型，搭出一个能调用工具的 Agent。

### 核心能力

| 能力 | 说明 |
|:---|:---|
| **标准化抽象** | 统一接入 OpenAI、Anthropic、Google 等模型，换模型几乎不用改代码 |
| **Agent 循环** | 封装了「模型推理 → 工具调用 → 结果返回」的标准流程 |
| **丰富集成** | 模型、向量库、文档加载器等生态非常完善 |
| **快速上手** | 提供预构建的 Agent 架构，复制粘贴就能跑 |

### 示例：构建一个天气查询 Agent

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """查询指定城市的天气。"""
    return f"{city} 今天晴朗，25°C"

# 创建一个 Agent：指定模型 + 工具 + 系统提示词
agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="你是一个 helpful assistant",
)

# 运行 Agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气怎么样？"}]
})
```

**这个 Agent 是怎么工作的？**

虽然代码只有几行，但底层的执行过程是一个循环的图结构：

![LangChain Agent 循环](/assets/img/posts/langchain-agent-loop.png)

1. **用户提问**：“北京天气怎么样？”
2. **模型推理**：模型判断需要调用 `get_weather` 工具来获取天气信息
3. **工具执行**：LangChain 自动调用 `get_weather("北京")`，返回“北京 今天晴朗，25°C”
4. **生成回答**：模型基于工具返回的结果，生成最终回答：“北京今天天气晴朗，气温 25°C，适合出门~”

这就是 LangChain 最核心的价值：你只需定义工具，剩下的「推理 → 选工具 → 执行 → 回答」循环，框架帮你自动完成。

当然，这只是一个最简示例。在实际项目中，你可以在此基础上进行更复杂的封装：

- **多轮对话**：通过维护 `messages` 历史，让 Agent 具备上下文理解能力，能追问和澄清
- **记忆**：接入向量数据库，让 Agent 记住用户偏好或过往对话中的关键信息
- **路由判断**：在 Agent 循环前加入路由层，根据用户意图选择不同的工具集或子流程（比如先判断是「查天气」还是「订机票」，再走不同的逻辑分支）
- **工具链组合**：将多个工具串联成工作流，前一个工具的输出作为后一个工具的输入

LangChain 提供的是「积木」，基础循环是搭好的，但上面的建筑需要你自己设计。

### 适合场景

- 快速验证一个 Agent 想法
- 团队需要统一的开发标准
- Agent 逻辑比较直接，就是「模型 + 工具」的循环调用

---

## 二、🔄 LangGraph：让 Agent 跑得稳的运行时

LangGraph 是一个**底层的编排框架和运行时**。它不关心你怎么写提示词，只专注于一件事——**让 Agent 在复杂、长周期的任务里，跑得稳、断得了、续得上**。

### 核心能力

| 能力 | 说明 |
|:---|:---|
| **持久执行** | Agent 遇到故障能从上次状态恢复，长时间任务不怕中断 |
| **流式传输** | 支持工作流和响应的实时流式输出，提升用户体验 |
| **人机协同** | 随时让人类检查、修改 Agent 的状态，审批后再继续 |
| **全面记忆** | 短期工作记忆（单会话）+ 长期记忆（跨会话） |
| **生产部署** | 被 Klarna、Uber、J.P. Morgan 等公司用于生产环境 |

### 示例：构建一个带分流判断的智能客服工作流

假设我们要做一个客服 Agent，它先理解用户问题，然后分流到三个不同的处理团队，最后统一生成回复：

- **技术问题**（bug、报错、无法启动）→ 技术支持
- **售前问题**（价格、优惠、购买）→ 售前咨询
- **其他问题**（退款、投诉、使用帮助）→ 售后服务

在 LangGraph 中，你需要把每个处理步骤显式定义为**节点**，然后用**边**把它们连接起来。分流逻辑通过条件边实现——根据用户输入动态决定走哪个分支。整个流程编译成状态图后，支持持久化执行：即使服务器重启，也能用同一个 `thread_id` 从断点续跑。

**这个工作流长什么样？**

运行 `workflow.compile()` 后，LangGraph 会自动生成下面的流程图：

![LangGraph 智能客服工作流](/assets/img/posts/langgraph-workflow.png)

**LangGraph 提供了什么？**

- **图编排**：整个流程被显式建模为「节点 + 边」，你可以精确控制每一步该做什么、下一步往哪走
- **条件分流**：`add_conditional_edges` 让图根据状态动态选择分支，这是复杂工作流的核心能力
- **状态管理**：`MessagesState` 在节点之间流转，每一步都可以读取和修改状态
- **持久化**：`MemorySaver` 自动保存执行状态。如果服务器重启，只要用同一个 `thread_id` 就能从断点继续
- **人机协同**：你可以在任意节点插入中断，让人类审批后再继续执行
- **流式输出**：可以实时看到每个节点的执行进度，而不是等全部跑完才看到结果

LangGraph 把执行过程显式建模为「图」，节点是处理步骤，边是流转路径。这种方式让你对 Agent 的每一步都有完全的控制权，但也意味着你需要自己设计整个流程。

### 适合场景

- 任务运行周期长，需要故障恢复
- 需要对执行流程进行精细化控制
- 确定性流程与 Agent 决策混合的复杂编排
- 生产级部署

---

## 三、🚀 Deep Agents SDK：出厂即高配的 Agent Harness

Deep Agents SDK 被官方称为 **Agent Harness**（即“Agent 驾驭框架”）。它基于 LangChain 的核心构建块，使用 LangGraph 作为运行时，但在此基础上封装了大量**面向复杂任务的自主能力**。

### 核心能力

| 能力 | 说明 |
|:---|:---|
| **任务规划** | 自动维护待办清单，跟踪多步骤任务的执行进度 |
| **虚拟文件系统** | 读写文件、管理上下文，支持内存、本地磁盘、云端等多种后端 |
| **子 Agent 委派** | 像项目经理一样派活给子 Agent，保持上下文隔离 |
| **代码执行** | 在沙箱环境中运行 Shell 命令，安全执行代码 |
| **权限控制** | 声明式规则限制 Agent 能读写的文件范围 |
| **人机审批** | 敏感操作（如修改文件）需要人类确认 |
| **Skills 技能系统** | 按需加载专业技能，减少上下文占用 |
| **长期记忆** | 跨会话持久化记忆，Agent 能学习和进化 |

### 示例：构建一个能自主研究并写报告的 Agent

创建一个 Deep Agent 的方式和 LangChain 非常相似：指定模型、工具和系统提示词即可。但不同的是，你不需要写任何额外代码来管理规划、文件操作或子任务——Agent 接到复杂任务后会自主分解并调用内置能力完成。

**Deep Agent 会怎么工作？**

和你手动写代码不同，Deep Agent 接到任务后会**自主规划并调用内置能力**来完成：

1. **任务规划**：Agent 自动创建待办清单（`write_todos`）
   - [ ] 搜索北京未来一周天气
   - [ ] 分析天气趋势
   - [ ] 撰写出行建议
   - [ ] 保存报告到文件

2. **信息收集**：调用你提供的 `search_web` 和 `get_weather` 工具获取天气信息

3. **文件操作**：Agent 使用内置的 `write_file` 将中间研究结果写入文件，避免占用上下文窗口

4. **子 Agent 委派（如果需要）**：遇到复杂子任务时，Agent 可以调用 `task` 工具创建子 Agent 来处理（比如让子 Agent 专门分析降雨趋势），子 Agent 完成后返回一份精简报告

5. **生成最终报告**：综合所有信息，生成出行建议，并用 `write_file` 保存到指定路径

**Deep Agent 内置的核心能力具体包括**：

| 内置能力 | 工作方式 | 解决的问题 |
|:---|:---|:---|
| **任务规划** | Agent 自动调用 `write_todos` 创建、更新待办清单 | 复杂任务不会遗漏步骤，执行过程透明可追踪 |
| **文件读写** | 自动调用 `read_file`/`write_file`/`edit_file` 操作文件 | 中间产物不用全塞在上下文里，大报告可以分段写入文件 |
| **记忆压缩** | 自动对过长的对话历史进行摘要和 offload，保持上下文在 token 限制内 | 长任务不会因为上下文爆炸而中断 |
| **子 Agent** | 自动调用 `task` 工具创建子 Agent 处理子任务，完成后返回精简结果 | 主 Agent 上下文保持干净，子任务并行执行提高效率 |
| **代码执行** | 在沙箱环境中调用 `execute` 运行 Shell 命令 | Agent 可以安装依赖、运行脚本、验证代码 |
| **权限控制** | 按预设规则自动判断文件操作是否允许 | 防止 Agent 误删敏感文件或越权访问 |

**所有这些能力都是开箱即用的**——你不需要写一行额外代码。相比之下，用 LangChain 或 LangGraph 实现同样的功能，你需要自己集成文件系统、写规划逻辑、实现上下文压缩、管理子 Agent 的生命周期。

### 适合场景

- 复杂多步任务，需要自主规划和分解
- 需要和文件、代码、搜索产物打交道
- 想要编码 Agent / 自动编程助手
- 希望开箱即用，不重复造轮子

---

## 四、🔗 三者关系

| 层级 | 工具 | 角色 | 职责 |
|:---|:---|:---|:---|
| 上层 | **Deep Agents SDK** | Harness | 预置工具、规划能力、子 Agent、文件系统，面向复杂自主任务 |
| 中层 | **LangChain** | Framework | 标准抽象、模型集成、快速开发，面向快速搭建 Agent |
| 底层 | **LangGraph** | Runtime | 持久执行、流式传输、人机协同、状态管理，面向稳定运行和编排 |

三者的关系可以概括为：**LangGraph 打底 → LangChain 提速 → Deep Agents 封顶。** 它们不是互斥选项，而是**分工协作**的关系：越往下越接近基础设施，越往上越接近开箱即用的应用。

---

## 五、📊 核心对比

| 维度 | LangChain | LangGraph | Deep Agents SDK |
|:---|:---|:---|:---|
| **定位** | 开发框架 | 运行时 | Harness |
| **核心目标** | 快速开发 | 稳定运行 | 自主执行 |
| **上手难度** | 简单 | 较复杂 | 简单 |
| **控制力** | 中等（预设架构） | 完全自定义 | 中等（预置能力） |
| **持久化/故障恢复** | 框架内置 | 原生支持 | 默认自带 |
| **文件系统** | 无 | 无 | 内置虚拟文件系统 |
| **任务规划** | 无 | 无 | 内置待办清单 |
| **子 Agent** | 无 | 支持（需自建） | 内置 `task` 工具 |
| **代码执行** | 无 | 无 | 内置沙箱执行 |
| **Skills/记忆** | 无 | 基础接口 | 完整的技能和记忆系统 |

---

## 六、🎯 选型建议

| 你的需求 | 推荐选择 |
|:---|:---|
| 想快速验证 Agent 想法，10 分钟跑通 | **LangChain** |
| 团队需要统一开发标准 | **LangChain** |
| Agent 逻辑简单，就是「模型 + 工具」循环 | **LangChain** |
| 长时间运行任务，要求故障恢复 | **LangGraph** |
| 需要精细控制每个执行步骤 | **LangGraph** |
| 确定性流程 + Agent 决策的混合编排 | **LangGraph** |
| 复杂多步任务，需要自主规划 | **Deep Agents SDK** |
| 需要和文件、代码、搜索打交道 | **Deep Agents SDK** |
| 想要编码 Agent / 自动编程助手 | **Deep Agents SDK** |
| 希望开箱即用，不重复造轮子 | **Deep Agents SDK** |

### 推荐演进路径

**LangChain 入门 → LangGraph 加固 → Deep Agents 升级**

1. 用 **LangChain** 快速验证想法，理解 Agent 的基本工作模式
2. 当 Agent 需要进入生产环境、要求可靠性时，下沉到 **LangGraph** 获得精细控制
3. 当任务足够复杂、需要自主规划时，升级到 **Deep Agents** 使用预置能力

当然，三者都是开源的，你也可以混搭使用。选型没有绝对的对错，**适合你当前阶段和业务复杂度的，就是最好的**。

---

> 📚 **参考链接**
> 1. [LangChain Products & Concepts](https://docs.langchain.com/oss/python/concepts/products)
> 2. [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)
> 3. [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
> 4. [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
