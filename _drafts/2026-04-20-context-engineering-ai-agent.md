---
layout: post
title: 💡 AI Agent 核心技术：一文读懂 Context Engineering
date: 2026-04-10 23:00:00 +0800
categories: [AI, Agent]
tags: [context-engineering, ai-agent, llm, prompt-engineering]
image: /assets/img/posts/context-engineering-ai-agent-cover.jpg
---

在开发复杂的 AI Agent 系统时，开发者面临的核心挑战之一，就是如何精准管控大语言模型（LLM）的输入长度。对于大语言模型（LLM）而言，上下文（Context）并非越长越好，也不是越短越妙，这背后涉及了一个微妙的平衡。

为了让大语言模型能够处理长程任务而不"断片"或"迷失"，**上下文工程（Context Engineering）** 成为了不可或缺的技术底层。它是一套由开发者设计的系统性机制，用于管理传递给 LLM 的信息流。在此系统中，AI Agent 扮演着大语言模型的"经纪人"或"守门员"的角色，通过各种预设规则或自主决策，确保传递给"大脑"（LLM）的每一条信息都是精确且高效的。

![](assets/img/posts/context-engineering-ai-agent-cover.jpg)

## 一、为什么需要上下文工程？

上下文工程的核心目标是寻找大语言模型输入的"黄金比例"。如果管理不当，系统会面临以下来自 LLM 特性的极端风险：

### 1. 不能太长：避免 LLM 的溢出与精度衰减

- **窗口限制**：每个大语言模型（LLM）都有其固定的上下文窗口（Context Window），一旦 Token 数量超限，模型将无法读取更早的信息。
- **推理精度稀释**：研究显示，当输入的上下文包含大量冗余信息时，LLM 的推理精度会大幅下降（即所谓的 "Lost in the Middle" 现象）。这意味着信息过多会分散模型的注意力，导致生成的内容不精确，甚至产生幻觉。

### 2. 不能太短：确保 Agent 逻辑的连贯性

- **信息缺失**：LLM 本质上是在做"文字接龙"。如果提供的信息过于简略，LLM 就会丢失之前的任务目标、中间执行结果或环境状态，导致模型无法准确预测下一个步骤，最终造成 Agent 的任务逻辑断裂。

## 二、核心公式：系统演进的比较

为了更直观地理解 Context Engineering 如何管理 LLM 输入，我们可以通过数学公式来对比"原始堆叠"与"工程化管理"的演化过程。

### 1. 无上下文工程

在没有干预的情况下，上下文只是将所有发生的事情进行简单的线性拼接（Concatenation）。

**初始化状态：**

$$
\begin{aligned}
& I_1 \leftarrow \text{initial input} \\
& C_1 \leftarrow \text{empty}
\end{aligned}
$$

**执行逻辑如下：**（步骤 $t = 1$ 到 $\infty$）

$$
\begin{aligned}
& O_t = LLM(I_t, C_t) \\
& C_{t+1} \leftarrow C_t \mid I_t \mid O_t
\end{aligned}
$$

**核心痛点：** 符号"$\mid$"代表简单的拼接。随着循环进行，上下文 $C_t$ 的长度会迅速膨胀，最终超出大语言模型的窗口上限，或因冗余过多直接拖垮推理精度。

### 2. 有上下文工程

引入上下文工程后，系统不再进行简单的拼接，而是通过一个处理函数 $F$ 对信息进行智能转化与精炼。

**初始化状态：**

$$
\begin{aligned}
& I_1 \leftarrow \text{initial input} \\
& C_1 \leftarrow \text{empty}
\end{aligned}
$$

**执行逻辑如下：**（步骤 $t = 1$ 到 $\infty$）

$$
\begin{aligned}
& O_t = LLM(I_t, C_t) \\
& C_{t+1} \leftarrow F(C_t, I_t, O_t)
\end{aligned}
$$

**这个 $F$ 到底是什么？** 它是开发者设计的处理逻辑，负责对信息进行精炼、转化和存储，确保传递给 LLM 的内容始终维持在"黄金长度"。

## 三、核心技术手段详解

为了实现处理函数 $F$，开发者可以采用多种技术手段。这些手段构成了一个由浅入深、相互配合的系统矩阵。需要说明的是，并不是所有的决策都是由 Agent 自主决策的，有一些逻辑是基于预先设定好的一些规则来进行执行的。

### 1. 压缩与替换

当内容开始臃肿时，系统会优先执行物理瘦身。

- **压缩（对话总结）**：通过预设规则或模型调用，定期将琐碎的对话历史总结成摘要。例如：当历史对话超过一定长度（如 10 轮）时，系统自动触发总结逻辑，将之前的对话压缩成摘要。其核心目标是在保留关键里程碑的前提下，缩短文本长度。
<div align="center" style="max-width: 640px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-ai-agent-compression.png" alt="压缩示意图" style="width: 100%; border-radius: 8px;">
</div>


- **替换（结果替换）**：外一个出乎意料的方法是，针对工具返回的冗长结果（如万行日志），直接将其替换为一个占位符："**这里曾经有个 Tool output**"。神奇的是，实验表明这种方式居然能有效维持 LLM 的逻辑连贯性。
<div align="center" style="max-width: 520px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-ai-agent-replacement.png" alt="替换示意图" style="width: 100%; border-radius: 8px;">
</div>


当然，这些方法也并非完美无缺。压缩过狠会导致"轨迹延长"——如果关键细节被抹除，LLM 就会因失忆而"忘记"自己已经做过某些动作，从而反复执行同一任务，形成无效循环。

> 关于压缩与替换策略的有效性，可参考论文：
> 
> When Less is More: On the Cost-Effectiveness of Observation Masking in LLM Agents  
> https://arxiv.org/abs/2508.21433

### 2. 多层级记忆架构 (Multi-level Memory Architecture)

为了在不干扰模型注意力的情况下保留细节，系统可以模仿计算机的内存与硬盘设计。

- **P (Prompt) 活跃记忆**：筛选出的核心信息，实时输入给 LLM，保证高精度推理。
- **M (Storage) 长期记忆**：所有需要存储的信息被存储在外部数据库中。
- **按需加载**：通过预设的检索逻辑，决定何时从长期记忆中取回片段、注入到活跃记忆中。

<div align="center" style="max-width: 600px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-ai-agent-memory.png" alt="多层级记忆架构示意图" style="width: 100%; border-radius: 8px;">
</div>

在这一架构中，至于如何存、怎么存，也就是如何读、怎么读，是需要研究的一个问题。 这种精细化的管理决定了 Agent 是否能在庞大的历史数据中精准定位到当前任务所需的“那一块”拼图。

#### 进阶公式：更精准的上下文管理

为了更精细地描述记忆机制，我们需要将上下文 $C$ 拆解为 $P$ 与 $M$ 两个部分。此时，系统演进为：

**状态：**

$$
C_t = \{P_t, M_t\}
$$

**执行与更新逻辑：**

$$
\begin{aligned}
& O_t = LLM(I_t, P_t) \\
& C_{t+1} \leftarrow F(C_t, I_t, O_t)
\end{aligned}
$$

**在这个公式中，我们可以清晰地看到：**

- **输入变化**：LLM 的输入不再是完整的 $C_t$，而是经过筛选后的 $P_t$。
- **状态更新**：当执行 Load Memory 时，系统从 $M$ 中提取信息更新至 $P$；当执行 Save Memory 时，系统则将信息从当前交互持久化到 $M$ 中。

#### 术语澄清：Context vs. Prompt

在实际开发与文献中，这两个词常被混用，但从工程角度来看，它们存在本质区别：

- **Context (上下文)**：即公式中的 $C$。它代表 AI Agent 所经历过的一切，是包含了"活跃记忆"与"外部存储"的总和。你可以将其理解为 Agent 的整个"人生阅历"。
- **Prompt (提示词)**：即公式中的 $P$。它是 Context 的一个真子集，是当前时刻真正输入给 LLM 的那部分信息。

**Context 不一定全部成为 Prompt。** 优秀的 Context Engineering 核心就在于如何高效地将 Context 转化为 Prompt，实现"阅历虽广，但只取精华入脑"。

> 关于内存化操作系统级别的记忆管理，可参考论文：
> 
> Memory OS: An Operating System for LLM Agents  
> https://arxiv.org/abs/2506.06326

### 3. 子智能体 (Sub-agents)

通过任务级的隔离，可以实现 Token 的瞬时清理。

- **委派机制**：主 Agent 派发任务给临时的"子智能体"。子智能体在执行时产生的海量过程 Token 只留在其私有空间。
- **瞬时清理**：子任务结束后，主 Agent 仅接收一行结果，中间的数千个过程 Token 被瞬间抹除。这会产生显著的锯齿状 Token 效应。

<div align="center" style="max-width: 620px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-ai-agent-subagent-token.png" alt="子智能体 Token 锯齿效应示意图" style="width: 100%; border-radius: 8px;">
</div>

如上图所示，我们可以观察到明显的 “锯齿状” Token 效应：

- 红线（Full Context）：如果不使用 Sub-agent，所有搜索和执行过程的 Token 会不断累积，最终飙升到 107,008 个。
- 蓝线（Folded Context）：主 Agent 每开启一个 Sub-agent（图中左侧的 branch），Token 开始累积（上升）；一旦子任务结束并返回结果，中间冗长的搜索记录被瞬间抹除，Context 长度瞬间回落（下降）。

结论： Sub-agent 的本质是让模型在处理海量信息时，只保留“结论”，而忘掉“过程”，从而将 context 维持在安全区间。

> 相关技术研究可参考论文：
> 
> Scaling Long-Horizon LLM Agent via Context-Folding  
> https://arxiv.org/pdf/2510.11967

### 4. 智能预过滤与按需加载 (Filtering & On-demand Loading)

前面提到的压缩、替换、子智能体等手段，本质上都是在信息**已经进入**上下文之后做"事后清理"。但如果我们追问一个更根本的问题：这些臃肿的 context 究竟是从哪里来的？

有研究者对 Agent 对话历史中的 token 来源做了详细分析，发现一个惊人的事实：

- **Action**（模型产生执行工具的指令）仅占约 **6.5%**
- **Reasoning**（模型自己的思考与输出）仅占约 **9.6%**
- **Observation**（来自外界的输入，如文件内容、工具返回的日志等）却占据了高达 **84%**

<div align="center" style="max-width: 360px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-token-distribution.png" alt="Token 来源分布" style="width: 100%; border-radius: 8px;">
    <p style="color: #888; font-size: 12px; margin-top: 8px;">
        Token 来源分布（数据来源：<em>When Less is More: On the Cost-Effectiveness of Observation Masking in LLM Agents</em>）
    </p>
</div>

另一篇聚焦软件工程场景的论文也得出几乎一致的结论：Agent 仅有约 12% 的 context 花在执行代码、11.8% 花在修改代码，而高达 **76%** 的 context 用于将整个代码仓库读入。这意味着，**真正吞噬上下文窗口的罪魁祸首，不是模型自己的思考，而是那些未经筛选的外界输入。**

既然如此，最有效的策略不是等它们把 context 撑爆后再压缩，而是**在 observation 进入语言模型之前，就先做过滤**。

#### 智能读取 (Smart Read)

传统的读取逻辑往往是：模型说"我要读一份行业研究报告"，`read` 工具就把整份上百页的报告原封不动地塞给模型。资料一庞大，模型很容易被"哽到"。

更聪明的做法是，让模型在发出读取指令时就带上筛选意图，例如："我要读这份报告中关于市场规模预测的部分"。而 `read` 工具本身也不应只是"打开文件"，它还需要具备一定的智能，能够根据指令从海量内容中找出真正相关的段落。这背后的实现可以是一个**小型语言模型**——它接收读取指令，从原始资料中筛选出匹配内容，再传给主 Agent。主 Agent 因此只需聚焦于经过过滤的精华信息。

<div align="center" style="max-width: 560px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-smart-read.png" alt="智能读取示意图" style="width: 100%; border-radius: 8px;">
</div>

这种"只取一段"的思路，与 OpenClaw 中 `memory get` 的设计异曲同工。OpenClaw 没有一次性读取整个 memory 文件，而是配合 `memory search` 的结果，通过 `memory get` 指定"从第几行开始读、读多少行"，只从巨大的 memory 中取出所需的一小段。本质上，这也是一种预过滤。

#### 按需加载 (On-demand Loading)

智能预过滤的另一个典型场景，其实就是我在《[别再复制粘贴提示词了！AI Agent Skill 到底是什么？](https://zhengjie9510.github.io/posts/ai-agent-skill/)》中详细讲过的 **Agent Skill** 机制。

在传统做法里，如果你希望 AI 按特定格式写周报、整理会议纪要或生成数据报告，每次都得在对话里手动交代一大段"规矩"。如果把这些"规矩"全部常驻在 system prompt 里，想象一下，当 Agent 集成了几十个 Skill，每个 Skill 的 Prompt 模板都有几千个 token，全部塞进去很容易直接撑爆上下文窗口。

**Skill 的本质，正是按需加载**：把"规矩"写成独立的 Skill 文件，系统只在检测到用户需要某个 Skill 时，才将其对应的 Prompt 模板动态挂载到当前上下文中。平时这些 Skill 的详细内容都存放在外部，不会占用宝贵的上下文空间。

<div align="center" style="max-width: 480px; margin: 20px auto;">
    <img src="/assets/img/posts/context-engineering-on-demand-loading.png" alt="按需加载示意图" style="width: 100%; border-radius: 8px;">
</div>

> 关于按需加载与工具动态选择，可参考论文：
> 
> MCP-Zero: Active Tool Discovery for Autonomous LLM Agents  
> https://arxiv.org/abs/2506.01056

### 5. 自动化上下文工程 (ACE, Agentic Context Engineering)

这是最高级的形态：**Agent 自主决定将上下文的管理权交由 LLM 自己控制**。

- **动态操作手册 (Playbook)**：Agent 指导模型边干活边维护一份"策略小抄"。
- **自主演化**：每一轮交互后，LLM 自行反思并由 Agent 执行修订，确保每一轮的上下文都是当下任务的最优解。

与前四种**开发者预设**的机制不同，ACE 的核心在于让 Agent/LLM 自己决定如何管理上下文，这是真正"智能化"的 Context Engineering。

## 结语

上下文工程并非单一的指令优化，而是确保 AI Agent 在面对复杂任务时，能平衡"信息完整性"与"大语言模型（LLM）推理精度"的核心系统工程。通过精进处理函数 $F$（无论是开发者预设的规则，还是 Agent 自主的决策），才能在有限的窗口里，释放出 LLM 的无限智慧。
