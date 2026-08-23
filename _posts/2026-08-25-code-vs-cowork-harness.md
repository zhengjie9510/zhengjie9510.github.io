---
layout: post
title: "同一个内核，两种产品：拆解 Claude Code 和 Cowork 的 Harness 差异"
categories: [ AI Agent ]
tags: [ Claude Code, Cowork, Agent SDK, Harness, System Prompt ]
description: "
"
image: /assets/img/posts/code-vs-cowork-harness-cover.png
---

经常用 Claude 桌面端的朋友可能注意到，里面有两个能干活的入口：Code 和 Cowork。Code 面向你自己的项目，写代码、改文件、跑命令；Cowork 更像一个通用助手，你说“帮我做份周报”“整理一下这个文件夹”，它也会去写代码、操作文件。

我好奇的点比较朴素：这俩底层是不是一套东西？如果是，为什么用起来完全是两个产品？

最直接的办法是抓包：在客户端和 Anthropic API 之间加一层代理，把两边的完整请求各存一份，逐块对比。上一篇《[拆解 Claude Code：它发给模型的请求，到底长什么样？](/posts/claude-code-prompt-structure/)》已经拆过这套请求——跟提示词直接相关的只有三块：`system`（身份与规矩）、`tools`（能力清单）、`messages`（对话流），其余都是运行参数。这篇就沿着这三块逐一对账，外加第四个维度——代码跑在哪。

---

## 一、📜 System Prompt：6.9KB 与 68KB

两边的 system 字段都由三个 block 组成：前两个很短，一行计费信息加一句身份声明，不展开；真正的大头是第三个 block，也就是主体部分。差距从这里开始。

Code 的主体第一句话是：

```text
You are an interactive agent that helps users with software engineering tasks.
（你是一个帮助用户完成软件工程任务的交互式智能体。）
```

software engineering tasks，开门见山，任务域直接定死。整个主体 6.9KB，目录长这样：

```text
# Harness              输出格式、工具使用规矩、代码风格
# Session-specific guidance
# Memory               持久化记忆机制
# Environment          工作目录、git 状态、平台信息
# Context management   上下文快满会被摘要续接，别提前收尾
```

通篇在讲“怎么干活”：输出用 Markdown、能用专用工具就别用 shell、代码风格贴着现有代码写。一份很紧凑的工程手册。

Cowork 的主体开头则是一段自报家门：

```text
<application_details>
Claude is operating as an agent inside the Claude desktop app. This agent
capability is currently a research preview. Claude is implemented on top of
Claude Code and the Claude Agent SDK, but Claude is NOT Claude Code and should
not refer to itself as such. Claude runs in a lightweight Linux VM on the
user's computer...
（Claude 以智能体的身份运行在 Claude 桌面应用里，这项能力目前是研究预览版。
Claude 构建于 Claude Code 和 Claude Agent SDK 之上，但 Claude 不是 Claude Code，
也不应这样称呼自己。Claude 运行在用户电脑上的一个轻量 Linux 虚拟机里……）
```

官方在 prompt 里白纸黑字承认了构建于 Claude Code 之上，同时严格要求模型别自称 Claude Code。自报家门之后，才是 68KB 的主体——十倍于 Code 的体量。目录节选：

```text
<application_details>       我运行在桌面 App 的沙箱里
<claude_behavior>
  <product_information>     产品与部署信息
  <tone_and_formatting>     语气和排版
  <user_wellbeing>          用户身心健康
  <evenhandedness>          观点中立
  <refusal_handling>        怎么拒绝用户
<ask_user_question_tool>    什么时候该反问用户
<todo_list_tool>            任务清单
<citation_requirements>     引用要求
<computer_use>
  <artifacts>               怎么写 HTML/React 组件
  <file_handling_rules>     文件放哪、怎么交付
  <sharing_files>           交付文件时的措辞
```

把这份目录读一遍就会发现，它教的不是“怎么干活”，而是“怎么当一个面向普通用户的助手”：语气怎么拿捏、什么时候该拒绝、怎么照顾用户情绪、文件怎么体面地交到用户手上。`<product_information>` 一节也写得直白——Claude 运行在 Claude 桌面应用里，做的是文件与任务管理的自动化。一份完整的产品化助手人格包。

有两个细节我觉得挺能说明问题。

一个是任务清单。Cowork 要求几乎所有涉及工具调用的任务都得先列清单，理由是：

> This is because the task list is nicely rendered as a widget to users in the desktop app.
> （因为任务清单会在桌面 App 里渲染成一个好看的挂件。）

用不用任务清单不是从任务管理效果出发的，是从界面呈现出发的。

另一个是交付文件的措辞。两边都管到了“怎么把文件交给用户”，但方向完全不同：

| | Code 的关注点 | Cowork 的关注点 |
| --- | --- | --- |
| 文件引用 | 用 `file_path:line_number` 格式，可点击跳转 | 链接文案用 “view”，不用 “download” |
| 路径暴露 | 直接给出完整路径 | 内部路径（`/sessions/...`）绝不露出，“看起来像后端基础设施，会让人困惑” |
| 服务对象 | 工程师的导航效率 | 普通用户的观感 |

68KB 和 6.9KB 的差距，大致就是这个差别的积累。

---

## 二、🏰 运行环境：真机与沙箱

两套 Harness 最底层的分歧是代码跑在哪。Cowork 的 prompt 里写得很明白：

```text
Claude runs in a lightweight Linux VM (Ubuntu 22) on the user's computer.
The VM's internal file system resets between tasks, but the workspace folder
persists on the user's actual computer.
```

运行在用户电脑上的一个轻量 Linux 虚拟机里，VM 内部文件系统在任务之间会重置，只有用户选定的 workspace 文件夹持久保留。整理成一张表：

| | Desktop Code | Cowork |
| --- | --- | --- |
| 运行位置 | 真实系统，终端进程权限 | Ubuntu 22 轻量 VM 沙箱 |
| 文件系统 | 直接操作本机文件 | VM 内部任务间重置，仅 workspace 持久 |
| 写文件 | 想写哪写哪 | 先写草稿目录（用户不可见），成品再复制进用户文件夹 |
| 删除文件 | 按权限执行 | 默认禁止，`rm` 失败后需调工具申请授权 |
| 访问新目录 | `request_directory` 审批 | `request_cowork_directory` 审批后挂载 |

这套设计的取向不难理解：Code 假设用户是工程师，看得懂自己在确认什么；Cowork 假设用户是普通人，先围栏、后放行。

---

## 三、🧰 Tools：54 个与 31 个

工具清单最能看出“同一内核、不同装配”。按层拆开：

| 层 | Desktop Code（54 个） | Cowork（31 个） |
| --- | --- | --- |
| 内核工具 | Read / Write / Edit / Glob / Grep、Task 系列、Agent、Skill | 一致（Cowork 有的这批，Code 全都有） |
| 工程增强 | Workflow、Plan Mode、Worktree、Cron、Notebook 等 | 几乎清空 |
| 桌面/产品集成 | `Claude_Preview` 浏览器全家桶（dev server、截屏、点按、看 network）、跨 Session 管理等 | `create_artifact`（侧边栏持久看板）、`present_files`（文件卡片）、`save_skill`（存技能进账号）、目录/删除授权等 |

其中最有意思的替换是 Bash：

```text
Code 的 Bash（原生工具）：
执行命令时工作目录跨调用保留（环境变量不保留，shell 每次从用户 profile 初始化）

Cowork 的 mcp__workspace__bash（MCP 工具）：
在会话隔离的 Linux 工作区里执行命令，每次调用相互独立，
不保留 cwd 和环境变量，请使用绝对路径
```

同一个能力，一边是持久化终端，一边是沙箱里的一次性命令行。对模型来说都叫“我能跑命令”，但名字换了、运行时换了、权限模型换了。对比下来，Code 独有的全是工程场景，Cowork 独有的全是产品场景。

---

## 四、💬 Messages：最后一块拼图

把 messages 摊开看，装的是三类信息：

```text
messages = [
  ① user            运行时上下文（system-reminder）+ 用户输入
  ② system          Agent / Skill 动态清单
  ③ user/assistant  真实对话流，逐轮累积
]
```

这一层两边几乎是复制粘贴：②里注入的 Agent 类型——claude、Explore、general-purpose、Plan——逐字一致，差别只在 Skill 清单：Code 挂的是 docx、pptx 这些文档技能，Cowork 挂的是 `anthropic-skills:` 命名空间的产品技能。

到这里证据凑齐了：请求结构一样、内核工具一样、Agent 注册表一样。结论只有一个——两者共享同一个 Claude Code 内核，差别全在外围的装配：

```text
Desktop Code = Claude Code 内核 + 工程增强工具 + 桌面集成
Cowork       = Claude Code 内核 + 消费级助手人格包 + 沙箱运行时 + 产品化交付
```

---

## 五、💡 所以，该用哪个？

| | Desktop Code | Cowork |
| --- | --- | --- |
| 定位 | 工程师的工具 | 普通人的服务 |
| System Prompt | 6.9KB 工程手册 | 68KB 助手人格包 |
| 运行环境 | 真机，逐条审批 | Linux 沙箱，任务间重置 |
| 工具 | 54 个，偏工程 | 31 个，偏产品 |
| 底层实现 | 写代码、跑脚本 | 一样，只是外包了层壳 |

差异追到根上就一句话：**目标用户不同。** 用户越不在场，prompt 就越要从“教方法”变成“立规矩”，Cowork 多出来的那 60 多 KB 基本都是这么来的。

怎么选？Cowork 是构建在 Claude Code 之上的：它做 PPT、编辑 Word，内部照样是写代码、跑脚本，和你在 Code 里干这些是同一套办法。所以程序员不用纠结，**直接用 Code**，写代码、做 PPT 都行，脚本还能留在仓库里复用。Cowork 留给不写代码的人，或者一次性的事：周报、整理文件夹，再或者你不想让 AI 碰真机的时候。

最后多说一句：AI 越来越能干，但依然会犯错，而且不会替你承担后果。无论用哪种模式，有一件事不能外包出去——对结果的判断力。
