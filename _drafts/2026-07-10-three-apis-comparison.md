---
layout: post
title: "Chat Completions、Responses、Messages —— 三套接口的本质区别"
date: 2026-07-10 08:00:00 +0800
categories: [AI]
tags: [OpenAI, Anthropic, API, Chat Completions, Responses, Messages, 大模型]
description: "深入对比 Chat Completions、Responses 和 Messages 三套大模型接口的设计哲学、适用场景与取舍逻辑"
image: /assets/img/posts/three-apis-comparison-cover.png
---

# Chat Completions、Responses、Messages
## ——三套接口的本质区别

> 大语言模型飞速发展的这几年，开发者和模型"说话"的方式也在悄悄演变。  
> 目前最主流的交互接口有三套，它们从哪里来、有什么不同、又各自代表着怎样的设计思路？

---

## 一、Chat Completions API　｜　奠定基础的第一套规矩

OpenAI 在推出 ChatGPT 之后，随之发布了 Chat Completions API，让开发者也能通过代码调用同款模型。它的设计思路非常直观：**把对话历史打包成一个消息列表，一起发给模型。**

```json
// 请求示例（简化版）
{
  "model": "gpt-4o",
  "messages": [
    { "role": "system",  "content": "你是一个助手" },
    { "role": "user",    "content": "你好，给我讲个笑话" }
  ]
}
```

模型收到后，把整段历史"读"一遍，再生成回复。简单、透明、易理解。

凭借 OpenAI 的先发优势，这套格式逐渐成了**行业事实标准**。国内外大量厂商——通义千问、智谱、月之暗面、Mistral……纷纷选择兼容这套格式，开发者换个模型，往往只需要改一行 `model` 参数。

> ⚠️ **需要注意**：OpenAI 已将 Responses API 定位为 Chat Completions 的继任者，未来新功能将优先在 Responses API 上落地。虽然目前 Chat Completions 仍被广泛支持，但新项目建议提前关注这一趋势。

```
✅ 兼容性强，生态庞大
✅ 概念简单，上手快
⚠️  对话历史需要开发者自己管理，每次都要传完整记录
⚠️  工具能力需要额外配置
```

---

## 二、Responses API　｜　OpenAI 的自我升级

2025 年初，OpenAI 推出了 Responses API，定位是对 Chat Completions 的**新一代替代**。

最核心的变化只有一句话：**服务端帮你记住对话历史了。**

以前的方式，就像每次打电话给客服，都要从头把之前说过的事重新讲一遍。现在，客服那边有记录了，你直接接着说就行。

```python
# 第一轮对话
response = client.responses.create(
    model="gpt-4o",
    input="你好，给我讲个笑话"
)
session_id = response.id  # 保存会话 ID

# 第二轮：直接接上，不用重传历史
response2 = client.responses.create(
    model="gpt-4o",
    previous_response_id=session_id,
    input="再讲一个"
)
```

除此之外，Responses API 还内置了一些实用工具，不需要开发者自己搭建：

| 内置能力 | 说明 |
|---------|------|
| 🔍 网络搜索 | 模型可以主动搜索实时信息 |
| 💻 代码执行 | 直接在沙盒里运行代码并返回结果 |
| 📁 文件读取 | 支持上传文档让模型参考 |

此外，OpenAI 同期推出的 **Agents SDK** 也基于 Responses API 构建，为多智能体协作、工具编排等高级场景提供了原生支持。这使得 Responses API 不仅仅是"Chat Completions 的升级版"，更像是一个面向 Agent 时代的基础设施。

```
✅ 对话状态由平台托管，开发者省心
✅ 工具能力开箱即用
⚠️  相对较新，生态还在建立中
⚠️  依赖 OpenAI 平台，迁移成本较高
```

---

## 三、Anthropic Messages API　｜　另一种设计哲学

Anthropic 是 Claude 背后的公司。面对 OpenAI 已经建立起来的格式标准，他们没有选择跟随，而是**自立门户，设计了一套有自己主张的接口**。

从请求结构就能看出差异：

```python
# Anthropic Messages API 示例
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system="你是一个助手",   # ← system 单独传参，不混在 messages 里
    messages=[
        { "role": "user", "content": "你好，给我讲个笑话" }
    ]
)
```

注意到了吗？**`system`（系统提示）被单独拎了出来**，不和用户对话混在一起。这个设计背后有明确的意图：系统提示代表开发者对模型行为的约束，它的性质和用户输入不同，理应区分对待。这正是 Anthropic 一贯强调安全与可控的体现。

```
✅ 设计严谨，结构清晰
✅ 对 Claude 系列模型支持最完整
⚠️  不兼容 OpenAI 格式，迁移需要改代码
⚠️  仅适用于 Claude，生态相对封闭
```

---

## 三套接口横向对比

| 维度 | Chat Completions | Responses API | Messages API |
|------|-----------------|---------------|--------------|
| 出品方 | OpenAI | OpenAI | Anthropic |
| 推出时间 | 2022 年底 | 2025 年初 | 2023 年 |
| 对话历史管理 | 开发者自己传 | 平台托管 | 开发者自己传 |
| 内置工具 | 需额外配置 | 开箱即用 | 需额外配置 |
| 行业兼容性 | ⭐⭐⭐⭐⭐ 事实标准 | ⭐⭐ 较新 | ⭐⭐⭐ 仅限 Claude |
| 设计侧重 | 简洁、普及 | 功能完整 | 严谨、安全 |
| 未来前景 | 将被 Responses 取代 | 下一代标准 | 持续演进 |

---

## 如何选择　｜　控制权与便利性的取舍

三套接口最本质的区别，可以用一个维度来理解：**你愿意把多少控制权交出去？**

**Chat Completions** 把历史记录完全交给你自己管。麻烦，但自由：
- 想在发送前**压缩上下文**？直接改 messages 数组
- 想**摘要历史**、只保留关键信息节省 token？随时可以
- 想**动态注入**新的背景信息、中途修改系统提示？完全没问题

**Responses API** 则把这些控制权交给了 OpenAI 平台。历史怎么存、存多长、怎么压缩，你说了不算。换来的是省心——适合那些**不需要精细管理上下文**、只想快速搭起一个对话应用的场景。

**Messages API** 和 Chat Completions 类似，历史同样由开发者自己管理，控制权完整保留。但它更进一步：通过把 `system` 单独分离，在结构层面就区分了"开发者的指令"和"用户的输入"，对需要严格控制模型行为的场景更友好。

| 如果你… | 推荐选择 |
|--------|---------|
| 想最大兼容性，随时换模型 | Chat Completions（但需关注其被 Responses 取代的趋势） |
| 需要压缩/摘要/动态修改上下文 | Chat Completions 或 Messages API |
| 想省心，不想自己管对话状态 | Responses API |
| 需要网络搜索、代码执行等内置工具 | Responses API |
| 构建多智能体、工具编排等复杂应用 | Responses API + Agents SDK |
| 主打安全、需要严格约束模型行为 | Messages API |
| 只用 Claude 模型 | Messages API |

---

## 结语　｜　标准之争，仍在继续

三套接口并存，背后是三种对"AI 应该怎么工作"的不同回答：

- **OpenAI** 的 Chat Completions 追求普及，用兼容性换来了生态规模；
- **OpenAI** 的 Responses API 在此基础上继续进化，让模型从"会说话"变成"能干活"；
- **Anthropic** 的 Messages API 则坚持自己的设计哲学，把安全和严谨刻进了接口本身。

> AI 行业还很年轻，这些"规矩"仍在演化。  
> 也许未来会出现真正统一的标准——也许不会。  
> 但无论如何，理解这些接口背后的思路，比记住参数格式更重要。
