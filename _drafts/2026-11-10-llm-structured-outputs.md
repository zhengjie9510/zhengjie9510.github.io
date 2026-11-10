---
layout: post
title: "大模型结构化输出：从 Prompt 到 JSON Schema，再到 Constrained Decoding"
categories: [AI 原理]
tags: [结构化输出, JSON Schema, Constrained Decoding, vLLM, XGrammar]
description: "从 Prompt、JSON Mode 到 JSON Schema，梳理大模型结构化输出的技术演进，并解释 Constrained Decoding 如何在生成过程中约束 Token。"
---

在开发大模型应用时，我们经常会遇到这样一种需求：希望模型从用户输入中提取信息，再按照固定的数据结构返回结果，方便后续程序直接使用。

例如，用户输入：

> 我叫张三，今年25岁，目前居住在北京。

我们希望模型返回：

```json
{
  "name": "张三",
  "age": 25,
  "city": "北京"
}
```

看起来很简单。只要在 Prompt 中告诉模型提取姓名、年龄和城市，并严格按照 JSON 格式返回就可以了。

但真正开发过 LLM 应用的人，大概都遇到过类似的问题：有时模型会在 JSON 前面加一段解释，有时会把数字返回成字符串，有时会漏掉字段，甚至擅自修改字段名称。我们要求返回 `age`，它却返回了 `user_age`。

对于普通聊天，这些问题可能无伤大雅；但对于业务系统来说，后续程序通常依赖固定的字段和类型。模型少返回一个字段，就可能导致解析失败。

问题的根源在于：**程序需要确定的数据结构，而大模型默认生成的是具有概率性的文本。** 如何在保留模型理解和生成能力的同时，让输出满足程序约定的格式？这就是结构化输出（Structured Outputs）要解决的问题。

---

## 一、从 Prompt 到 JSON Mode：先让输出格式稳定下来

最直接的办法是通过 Prompt Engineering 约束模型。例如：

```text
你是一个信息提取助手。

请从用户输入中提取姓名、年龄和城市，
并严格按照以下 JSON 格式返回：

{
  "name": "string",
  "age": 0,
  "city": "string"
}

不要输出其他内容。
```

这种方式实现简单，也不要求推理框架提供额外能力。但它有一个根本限制：Prompt 只是给模型提供指令，并没有真正限制模型能够生成什么。

大语言模型的生成过程，是根据当前上下文计算下一个 Token 的概率分布，再选择一个 Token，继续预测下一个 Token。即使提示词反复强调输出格式，模型仍然可能生成不符合要求的内容。

为了减少这类问题，模型服务开始提供 JSON Mode。以 OpenAI API 为例，可以通过下面的参数要求模型以 JSON 格式返回：

```python
response_format={
    "type": "json_object"
}
```

与单纯依赖 Prompt 不同，JSON Mode 不只是提醒模型“请输出 JSON”，服务端还会通过格式约束机制，确保正常完成的输出是合法 JSON。

但 JSON Mode 仍然没有解决字段和类型的问题。

例如，我们希望得到：

```json
{
  "name": "张三",
  "age": 25
}
```

模型却可能返回：

```json
{
  "username": "张三",
  "user_age": "25",
  "city": "北京"
}
```

这段内容在语法上完全是合法 JSON，但字段名称、数据类型和字段数量都不符合业务要求。

所以，JSON Mode 解决的是“能不能解析成 JSON”，而不是“是不是我们想要的那种 JSON”。如果还要约束字段名称、字段类型、必填项和枚举值，就需要更明确的结构描述——JSON Schema。

## 二、JSON Schema：把输出要求变成一份数据协议

JSON Schema 是一种描述和校验 JSON 数据结构的规范。它可以规定对象包含哪些字段、字段是什么类型、哪些字段必填，以及是否允许出现额外字段。

例如，我们定义一个用户信息 Schema：

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "用户姓名"
    },
    "age": {
      "type": "integer"
    },
    "city": {
      "type": "string"
    }
  },
  "required": ["name", "age", "city"],
  "additionalProperties": false
}
```

这份 Schema 相当于一份输出协议：返回值必须是对象，必须包含三个指定字段，字段类型必须正确，而且不能擅自增加其他字段。

当 API 或推理服务支持 JSON Schema Structured Outputs 时，我们就可以把这份 Schema 传给服务端。服务端会依据它约束模型生成，而不只是把它当作一段普通提示词。

这里要区分两件事：Prompt 仍然负责告诉模型“要完成什么任务”，例如从文本中提取用户信息、信息缺失时不要猜测；Schema 则负责定义“结果必须长什么样”，例如有哪些字段、字段类型是什么、是否允许额外字段。**任务指令和输出协议各司其职，不需要在 Prompt 里反复强调 JSON 格式。**

不过，Schema 是如何真正影响模型生成的？模型又怎么知道下一个 Token 能不能生成？这就进入结构化输出最核心的技术：Constrained Decoding。

## 三、Constrained Decoding：在生成过程中约束 Token

先回到大模型最基本的生成过程。

假设模型当前已经生成了：

```json
{
  "age":
```

接下来，模型需要预测下一个 Token。在普通生成模式下，它会根据上下文计算候选 Token 的概率分布。候选内容可能包括数字、字符串、数组开头，或者其他符号。

但如果 Schema 已经规定 `age` 必须是整数，那么当前这个位置就不应该生成字符串或数组。约束解码机制会根据当前生成状态，判断哪些 Token 可以继续生成，并屏蔽不符合约束的候选项。

这通常被称为 Token Masking。可以用一个简化的公式表示：

```text
z'_i = z_i       如果 Token i 当前允许生成
z'_i = -∞        如果 Token i 当前不允许生成
```

这里的 (z_i) 是模型输出的原始 Logit，(z'_i) 是施加约束后的 Logit。经过 Mask 之后，不合法 Token 的概率会变成 0，模型再从剩余候选中选择下一个 Token。

因此，模型不再是在所有可能的 Token 中自由选择，而是在当前结构约束允许的范围内生成。

这和“生成完以后再检查 JSON”有本质区别：后处理校验发生在输出之后，发现错误只能报错或让模型重试；Constrained Decoding 则在生成的每一步参与解码，尽可能避免模型走到不合法的输出路径。

当然，真实实现并不是简单地逐字符过滤。大模型使用的是 Tokenizer，一个 Token 可能对应多个字符，约束引擎需要判断某个 Token 加入当前前缀后，是否仍然存在生成完整合法结果的可能。这也是约束解码需要专门工程实现的原因。

## 四、JSON Schema 如何变成模型可以执行的约束？

JSON Schema 描述的是数据结构，而 Token Masking 需要知道当前语法状态下哪些 Token 合法。两者之间还需要一个转换过程：把 Schema 编译成机器可以执行的语法规则。

例如，下面这份 Schema 要求 `status` 只能是两个枚举值之一，`count` 必须是整数：

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "failed"]
    },
    "count": {
      "type": "integer"
    }
  },
  "required": ["status", "count"],
  "additionalProperties": false
}
```

它可以被转换成类似这样的语法描述：

```text
Object :=
  {
    "status": Status,
    "count": Integer
  }

Status :=
  "success" | "failed"

Integer :=
  -?(0|[1-9][0-9]*)
```

这里的 Grammar（语法）描述了允许生成的文本结构。约束引擎会维护一个语法状态：当前等待对象开始、字段名称、冒号、枚举值、整数，还是对象结束。

每生成一个 Token，语法状态就随之推进。如果某个 Token 会让当前前缀无法继续形成合法结果，约束引擎就会将它排除。

整个过程可以概括为：

```text
JSON Schema
    ↓
Schema Compiler
    ↓
Grammar / 语法状态
    ↓
Constraint Engine
    ↓
Token Masking
    ↓
LLM Decoder
    ↓
符合约束的 JSON
```

从这个过程可以看出，结构化输出并不只是 Prompt 技巧。它借鉴了编译器的思路：先描述规则，再把规则转换成可执行的约束，最后在生成过程中根据当前状态判断下一步是否合法。

需要注意的是，不同约束引擎支持的 JSON Schema 子集可能不同。复杂的 Schema 也不意味着所有字段约束都能被所有推理框架完整支持，实际使用时仍要核对框架文档。

## 五、不只有 JSON Schema：Regex、Grammar 和 Choice

JSON Schema 适合描述对象、数组、字段和类型，但并不是所有结构化输出都需要一个 JSON 对象。有些任务只需要固定选项，有些任务只需要匹配某种文本格式，还有些任务需要自定义语法。

以 vLLM 的 Structured Outputs 为例，除了 JSON Schema，也支持 Choice、Regex 和 Grammar 等约束形式。

如果任务是情感分类，只允许模型返回 `positive`、`negative` 或 `neutral`，就可以使用 Choice。它表达的是一个有限的候选集合，适合分类、意图识别等场景。

如果任务要求输出固定格式的日期，可以使用 Regex：

```python
extra_body={
    "structured_outputs": {
        "regex": r"\d{4}-\d{2}-\d{2}"
    }
}
```

这样可以限制输出匹配 `YYYY-MM-DD` 这种文本形式。不过，正则匹配不等于业务有效：例如 `2026-99-99` 也可能通过这个简单表达式，日期是否真实有效还需要额外校验。

如果需要描述更复杂、甚至不是 JSON 的输出结构，可以使用 Grammar。例如：

```text
root ::= "yes" | "no"
```

它规定模型只能输出 `yes` 或 `no`。

这些方式并不是互相独立、互相排斥的技术。JSON Schema 也可以被编译成语法规则，再交给约束解码引擎执行。区别主要在于：我们用什么方式描述允许生成的内容，以及具体的推理框架如何实现这些约束。

## 六、Function Calling：结构化输出在 Agent 中的应用

在 AI Agent 开发中，还有一种经常和结构化输出一起出现的能力：Function Calling，也就是工具调用。

例如，我们定义一个天气查询工具，它需要一个 `city` 参数：

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "查询指定城市的天气",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string"
        }
      },
      "required": ["city"]
    }
  }
}
```

当用户说“帮我查一下北京的天气”时，模型需要判断是否调用这个工具，并生成相应的参数。Agent 框架拿到工具名称和参数后，再执行真正的天气查询函数，并把结果返回给模型。

这里同样需要结构化的参数，因为工具函数要求输入符合约定的数据结构。

但 Function Calling 和普通 JSON Schema 输出的目的并不相同：前者是让模型选择工具并生成调用参数，后者是让模型直接返回符合协议的数据。两者可以共享 Schema 和约束解码等底层机制，但在应用层承担的职责不同。

因此，Function Calling 可以看作结构化输出在 Agent 工具交互场景中的重要应用，而不是另一种与 JSON Schema 完全平行的 Schema 定义语言。

## 七、落到工程实践：vLLM + Qwen 怎么实现？

理解了这些概念，再看实际开发就简单多了。

如果使用 vLLM 部署 Qwen 等开源模型，不需要自己实现 Schema Compiler、Grammar Parser 或 Token Masking。vLLM 已经集成了 Structured Outputs 能力，可以通过 API 把约束传给推理服务，并使用 XGrammar 或 Guidance 等后端执行约束解码。

先用 Pydantic 定义数据结构：

```python
from pydantic import BaseModel, ConfigDict, Field

class UserInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="用户姓名")
    age: int | None = Field(description="用户年龄，未知时为 null")
    city: str | None = Field(description="用户所在城市，未知时为 null")
```

Pydantic 可以根据模型定义生成 JSON Schema：

```python
schema = UserInfo.model_json_schema()
print(schema)
```

然后通过 vLLM 的 OpenAI 兼容接口调用：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

model = client.models.list().data[0].id

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "从用户文本中提取姓名、年龄和城市。未明确提及的信息填写 null，不要猜测。"
        },
        {
            "role": "user",
            "content": "我叫张三，今年25岁，住在北京。"
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "user_info",
            "schema": UserInfo.model_json_schema()
        }
    }
)

print(response.choices[0].message.content)
```

这里有几个组件需要分清楚：Pydantic 负责定义数据结构，并生成 JSON Schema；SDK 负责把 Schema 放进 API 请求；vLLM 接收 Schema，再通过约束解码后端控制模型生成。Pydantic 本身并不负责在模型生成的每一步屏蔽 Token。

在 vLLM 中，可以使用默认的自动后端选择，也可以在支持的版本中显式指定 XGrammar：

```bash
vllm serve <model-path> \
  --structured-outputs-config.backend xgrammar
```

这样就完成了从数据结构定义到受约束生成的整个过程。对于已经使用 vLLM 部署 Qwen 的开发者来说，这通常不需要修改模型权重，也不需要额外训练模型。

## 八、结构正确，不代表内容一定正确

最后还要强调一个容易被忽略的问题：结构化输出解决的是格式和结构约束，并不保证模型填入的数据在语义上一定正确。

例如，Schema 可以保证 `age` 是整数，却不能保证这个年龄是真实的。如果用户根本没有提供年龄，模型仍然可能错误推测一个数字。

所以，生产环境中通常还需要几层保障：Prompt 负责说明提取规则和缺失值处理方式；Schema 负责约束字段、类型和结构；业务逻辑负责检查数据是否合理；必要时再通过数据库或外部数据源验证事实。

此外，拒绝回答、生成中断、Token 长度限制等情况也需要单独处理。结构化输出提高了结果的可控性，但不能替代业务校验。

## 写在最后

从最初依靠 Prompt 要求模型返回 JSON，到 JSON Mode 保证语法合法，再到 JSON Schema 约束字段和类型，结构化输出的演进，反映了 LLM 应用对结果可靠性的要求越来越高。

而 Constrained Decoding 是其中非常关键的一环。它不只是让模型“尽量遵守指令”，而是在生成过程中引入语法约束，动态限制模型可以选择的 Token。

如果只是简单输出，Prompt 可能已经够用；如果只要求合法 JSON，可以考虑 JSON Mode；如果需要固定的业务数据结构，就使用 JSON Schema；如果要限制特定文本格式，可以考虑 Regex；如果需要自定义语法，可以使用 Grammar；如果希望模型与外部工具交互，则可以使用 Function Calling。

**结构化输出真正的价值，不只是让大模型返回一个 JSON，而是让模型生成的内容能够更可靠地进入软件系统，成为程序可以理解、校验和处理的数据。**

这也是大模型从聊天工具走向真正业务应用过程中，一项重要的工程能力。

---

**参考资料**

- vLLM Structured Outputs：https://docs.vllm.ai/en/latest/features/structured_outputs/
- OpenAI Structured Outputs：https://platform.openai.com/docs/guides/structured-outputs
- XGrammar：https://github.com/mlc-ai/xgrammar
- Pydantic：https://docs.pydantic.dev/
