# 拆解 Claude Code：它发给模型的请求，到底长什么样？

如果你用过 Claude Code，可能会好奇：每次你在终端里敲下一句话，它到底往模型那边发了什么？除了你打的那几个字，背后其实还藏着一整套精心设计的"提示词工程"。

这篇是系列的第一篇。我们先不管请求里的 Header、以及 Body 里那些跟本次要聊的内容无关的字段（比如 `max_tokens`、`thinking` 配置这些），只聚焦请求体（body）里最核心的三块内容：

1. **System**
2. **Tools**
3. **Messages**

---

## 一、System：静态的身份与规范

`system` 是请求体里独立的一个字段，跟对话的具体轮次无关，可以理解成"每次开口之前，先把这些规矩交代清楚"。

它承载的主要是两类内容：

- **身份声明**：比如"你是 Claude Code，Anthropic 官方的命令行工具"这类一句话定位。
- **行为规范主体**：包括安全边界、如何使用各种工具、代码风格偏好、当前的环境信息（比如 git 状态快照）等等。

实际请求里，这部分内容会被拆成好几个独立的 block。简化一下大概是这样（下面内容是示意，不是原文）：

```json
"system": [
  { "type": "text", "text": "x-anthropic-billing-header: cc_version=2.1.181; ..." },
  { "type": "text", "text": "You are Claude Code, Anthropic's official CLI for Claude." },
  { "type": "text", "text": "# Harness\n- 输出的文本会以 Markdown 形式展示在终端里\n- 优先用专用工具而不是 shell 命令\n- ...（安全边界、代码风格偏好、当前 git 状态等）" }
]
```

## 二、Tools：模型能调用的能力清单

`tools` 同样是独立于对话之外的一个字段，装的是模型可以调用的工具定义，本质上就是一份 JSON Schema 清单。

Claude Code 里工具的数量不少，涵盖读写文件（`Read`、`Write`、`Edit`）、执行命令（`Bash`）、联网（`WebFetch`、`WebSearch`）、任务管理（`TaskCreate`/`TaskList`/`TaskUpdate` 等）、子代理调度（`Agent`）、技能调用（`Skill`）等等，二十多个工具打底。

挑两个简化一下大概是这样：

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

每个工具就是一个"名字 + 描述 + 参数格式"的三件套，模型靠描述判断什么时候该用哪个工具。

## 三、Messages：真正有"对话逻辑"的部分

如果说 System 和 Tools 是静态背景板，那 `messages` 就是真正随着对话推进、一步步累积起来的部分，也是整个请求体里结构最复杂的地方。

`messages` 本质上是一个**扁平数组**——数组里的每一项都是并列的一条消息，彼此之间没有谁包含谁的关系。唯一的例外，是数组里的**第一条消息**，它自己内部又拆成了两小块。

拆开来看，一次典型的"第一轮对话"，数组长这样：

```
messages = [
  messages[0]  role: user       →  { (a) System Reminder, (b) 用户的真实提问 }
  messages[1]  role: system     →  (c) Agent / Skill 信息
  messages[2]  role: assistant  →  (d) 模型的回复
  messages[3]  role: user       →  (e) 用户接下来的新问题
  ...
]
```

逐条拆解一下：

**messages[0]（role: user）—— 内部包含两部分**

- **(a) System Reminder**：这是这条 user 消息里的第一个 content block，由 Claude Code 的 harness（也就是客户端本身）在用户的问题之前，抢先塞进去的运行时上下文。可以理解成"在你开口之前，先帮你把当前项目的一些背景信息交代给模型"。
- **(b) 用户的真实提问**：同一条消息的第二个 content block，紧跟在 (a) 后面，才是你真正打出来的那句话。

需要强调的是：(a) 和 (b) 是**同一条消息内部的两个 block**，不是两条独立的消息。这是整个 messages 数组里唯一存在"一条消息、两层内容"这种嵌套的地方。

**messages[1]（role: system）—— (c) System Message**

这是数组里独立的下一条消息，和 `messages[0]` 处于完全相同的层级，只是排在它后面。它的 `role` 直接写的是 `system`，而不是常规的 `user`/`assistant`——这在过去的 Messages API 里是不允许的，能出现这种用法，是因为请求里带了一个专门的 beta 能力开关，允许在对话中途插入一条 system 角色的消息，而不必都塞进最外层的 `system` 字段。

这条消息里装的是**环境说明性质**的信息：当前有哪些 Agent 类型可以调用、有哪些 Skill 可以使用，让模型清楚自己手头除了 Tools 里那些基础工具外，还有哪些"更高阶的能力"可以调度。

**messages[2]（role: assistant）—— (d) 模型的回复**

独立的下一条消息，是模型对 (b) 那个问题的实际回答。

**messages[3]（role: user）—— (e) 用户接下来的新问题**

再往后，又是一条独立的 user 消息，开启下一轮对话。

把上面这几条消息拼成 JSON，简化一下大概是这样（同样是示意，不是原文）：

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

对照着看会更直观：`messages[0]` 一条消息里塞了两个 block（(a)(b)），`messages[1]` 单独一条、`role` 是 `system`（(c)），再往后 `messages[2]`、`messages[3]` 分别是 (d)(e)，彼此都是数组里平级的元素。

### 小结一下这套逻辑

整个 messages 数组的核心逻辑就是：

- 数组里的每一项都是**并列**的一条消息，按对话发生的顺序依次排列；
- 只有**第一条消息**内部比较特殊，会先塞一个 System Reminder，再接用户的真实提问，两者共享同一个 role（`user`），只是拆成了两个 content block；
- 从第二条消息开始（也就是那条 role 为 `system` 的消息），之后所有的内容——无论是介绍 Agent/Skill 的说明消息，还是模型的回复，还是用户的下一轮提问——都是数组里彼此独立、依次排列的元素，跟第一条消息处在完全相同的层级上，区别只是索引顺序和 role 不同。

---

## 四、拼起来之后，模型看到的是什么样

三块内容不是并列摆在请求体里就完事了，最终会首尾相接拼成一条线性文本喂给模型，谁在前谁在后是有讲究的。顺序是：**Tools 在最前，System 其次，Messages 压轴**——跟直觉里"System 打头"正好相反。

背后的原因跟 prompt caching 有关：内容越稳定不变，缓存越容易命中，所以越该放得靠前。Tools 这份清单只要连接的插件、MCP 没变，从头到尾基本不动，排第一；System 大部分内容整场会话恒定，只有末尾一小块（比如 git 状态）会变，排第二；Messages 每一轮都在变长，只能垫底。

示意一下拼起来长什么样（不是原文，简化过）：

```
[Tools 清单]
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

一整条读下来就是：先背熟"我能用什么工具"，再背熟"我是谁、该守什么规矩"，最后才看"现在聊到哪儿了"——越靠前的东西越稳定，越靠后的东西越是这一秒才发生的事。
