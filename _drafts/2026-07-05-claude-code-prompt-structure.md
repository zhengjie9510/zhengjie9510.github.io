---
layout: post
title: "拆解 Claude Code：它发给模型的请求，到底长什么样？"
date: 2026-07-05 10:00:00 +0800
categories: [ AI Agent ]
tags: [ Claude Code, Prompt Engineering, System Prompt, Messages API ]
description: "每次你在终端里敲下一句话，Claude Code 到底往模型那边发了什么？这篇拆开它的请求体，看清 System、Tools、Messages 这三块跟提示词直接相关的内容分别装了什么，又是按什么顺序拼在一起喂给模型的。"
image: /assets/img/posts/claude-code-prompt-structure-cover.png
---

如果你用过 Claude Code，可能会好奇：每次你在终端里敲下一句话，它到底往模型那边发了什么？除了你打的那几个字，背后其实还藏着一整套精心设计的“提示词工程”。

要回答这个问题，得先看一眼这个请求体本身长什么样。抛开 Header 和具体取值不谈，Claude Code 发给 Messages API 的请求体，大致是这样一个结构 *（示意，非原文）*：

```json
{
  "model": "claude-...",
  "max_tokens": 8192,
  "temperature": 1,
  "stream": true,
  "thinking": { "...": "..." },
  "system": [ "..." ],
  "tools": [ "..." ],
  "messages": [ "..." ]
}
```

简单说一下每个字段大致是干什么的：

| 字段 | 作用 | 跟提示词相关 |
| --- | --- | --- |
| `model` | 用哪个模型 | ❌ |
| `max_tokens` | 最多输出多长 | ❌ |
| `temperature` | 采样有多随机 | ❌ |
| `stream` | 要不要流式返回 | ❌ |
| `thinking` | 要不要开启扩展思考、给多大预算 | ❌ |
| `system` | 模型的身份声明和行为规范 | ✅ |
| `tools` | 模型能调用的工具清单 | ✅ |
| `messages` | 到目前为止的对话历史 | ✅ |

> 真正决定“模型看到了什么提示词”的，只有 `system`、`tools`、`messages` 这三个——其余的都是控制模型怎么算、算多少、怎么传输的运行参数，跟提示词内容本身没关系。

接下来只聚焦这三块：

1. **System**
2. **Tools**
3. **Messages**

---

## 一、🪪 System：静态的身份与规范

`system` 是请求体里独立的一个字段，跟对话的具体轮次无关，可以理解成“每次开口之前，先把这些规矩交代清楚”。

它承载的主要是两类内容：

- **身份声明**：比如“你是 Claude Code，Anthropic 官方的命令行工具”这类一句话定位。
- **行为规范**：安全边界、工具使用方式、代码风格偏好、当前环境信息（比如 git 状态快照）等，是 system 字段里篇幅最大的部分。

实际请求里，这部分内容会被拆成好几个独立的 block，简化后大致是这样 *（示意，非原文）*：

```json
"system": [
  { "type": "text", "text": "x-anthropic-billing-header: cc_version=2.1.181; ..." },
  { "type": "text", "text": "You are Claude Code, Anthropic's official CLI for Claude." },
  { "type": "text", "text": "# Harness\n- 输出的文本会以 Markdown 形式展示在终端里\n- 优先用专用工具而不是 shell 命令\n- ...（安全边界、代码风格偏好、当前 git 状态等）" }
]
```

> 说到底，`system` 字段就是模型每次开口前，先默读一遍的“人设 + 规矩”。

---

## 二、🧰 Tools：模型能调用的能力清单

`tools` 同样是独立于对话之外的一个字段，装的是模型可以调用的工具定义，本质上就是一份 JSON Schema 清单。

Claude Code 里工具的数量不少，涵盖读写文件（`Read`、`Write`、`Edit`）、执行命令（`Bash`）、联网（`WebFetch`、`WebSearch`）、任务管理（`TaskCreate`/`TaskList`/`TaskUpdate` 等）、子代理调度（`Agent`）、技能调用（`Skill`），二十多个工具打底。

挑两个出来，示意一下大致结构 *（示意，非原文）*：

```json
"tools": [
  {
    "name": "Bash",
    "description": "在持久化的 shell 会话里执行一条命令",
    "input_schema": {
      "type": "object",
      "properties": {
        "command": { "type": "string", "description": "要执行的命令" }
      },
      "required": ["command"]
    }
  },
  {
    "name": "Read",
    "description": "读取本地文件系统中的一个文件",
    "input_schema": {
      "type": "object",
      "properties": {
        "file_path": { "type": "string", "description": "文件的绝对路径" }
      },
      "required": ["file_path"]
    }
  }
]
```

> 每个工具就是一个“名字 + 描述 + 参数格式”的三件套，模型靠描述判断什么时候该用哪个工具。

---

## 三、💬 Messages：真正有“对话逻辑”的部分

如果说 System 和 Tools 是搭好的静态背景板，那 `messages` 就是随着对话推进、一步步累积起来的动态主线，也是整个请求体里结构最复杂的地方。

`messages` 本质上是一个**扁平数组**：每一项都是并列的一条消息，彼此之间没有谁包含谁的关系，只有**第一条消息**例外，它内部会拆成两个 content block。拆开来看，一次典型的“第一轮对话”，数组长这样：

```
messages = [
  messages[0]  role: user       →  System Reminder + 用户的真实提问
  messages[1]  role: system     →  Agent / Skill 信息
  messages[2]  role: assistant  →  模型的回复
  messages[3]  role: user       →  用户接下来的新问题
  ...
]
```

逐条看一下每一项装的是什么：

- **messages[0]（role: user）**：内部两部分。第一部分是 System Reminder，由 Claude Code 的 harness（也就是客户端本身）在用户的问题之前抢先塞进去的运行时上下文，比如 CLAUDE.md 里的项目规则、当前时间这些信息；第二部分才是你真正打出来的那句话，紧跟在后面。两者共享同一个 role（`user`）。
- **messages[1]（role: system）**：装的是当前可用的 Agent 类型和 Skill 列表，让模型知道除了 Tools 里的基础工具，还能调度哪些更高级的能力。
- **messages[2]（role: assistant）**：模型对上一个问题的实际回答。
- **messages[3]（role: user）**：你的下一句话，开启下一轮对话。

把这几条消息拼成 JSON，大致是这样 *（示意，非原文）*：

```json
"messages": [
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "<system-reminder>\n当前项目使用 uv 管理 Python 虚拟环境，涉及 Python 操作时请优先使用 uv run。\n</system-reminder>"
      },
      { "type": "text", "text": "hello" }
    ]
  },
  {
    "role": "system",
    "content": "Available agent types for the Agent tool:\n- Explore: 用于大范围代码搜索的只读 agent\n\nThe following skills are available for use with the Skill tool:\n- docx: 用于生成或编辑 Word 文档"
  },
  {
    "role": "assistant",
    "content": [
      { "type": "text", "text": "你好，有什么可以帮你的吗？" }
    ]
  },
  {
    "role": "user",
    "content": [
      { "type": "text", "text": "帮我看看这个项目的目录结构" }
    ]
  }
]
```

---

## 四、🧩 拼起来之后，模型看到的是什么样

三块内容不是并列摆在请求体里就完事了，最终会首尾相接拼成一条线性文本喂给模型，谁在前谁在后是有讲究的。顺序是这样的：

**Tools → System → Messages**

跟直觉里“System 打头”正好相反。

背后的原因跟 prompt caching 有关：内容越稳定不变，缓存越容易命中，所以越该放得靠前。

- **Tools** 这份清单只要连接的插件、MCP 没变，从头到尾基本不动，排第一；
- **System** 大部分内容整场会话恒定，只有末尾一小块（比如 git 状态）会变，排第二；
- **Messages** 每一轮都在变长，只能垫底。

示意一下拼起来长什么样 *（示意，非原文）*：

```
[Tools 清单]
  In this environment you have access to a set of tools you can use to
  answer the user's question. You can invoke functions by writing...
  Bash / Read / Edit / ...（20+ 个工具的 name、description、input_schema）

[System]
  You are Claude Code, Anthropic's official CLI for Claude.
  ...（行为规范、代码风格、当前 git 状态等）

[Messages]
  User:      <system-reminder>...项目信息...</system-reminder> + 用户的问题
  System:    当前可用的 Agent / Skill 列表
  Assistant: 模型的回复
  User:      下一个问题
  ...
```

> 一整条读下来就是：先背熟“我能用什么工具”，再背熟“我是谁、该守什么规矩”，最后才看“现在聊到哪儿了”——越靠前的东西越稳定，越靠后的东西越是这一秒才发生的事。

---

> 这种排布方式，某种程度上也是 Claude Code 提示词工程的一个缩影：真正决定它表现如何的，往往不是你敲下的那句话本身，而是那些在你按下回车之前就已经写好、静默生效的结构。
