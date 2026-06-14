---
layout: post
title: "Embedding + LLM：用大模型智能清洗地理数据（附代码实战）"
date: 2025-05-17 10:00:00 +0800
categories: [ AI 应用 ]
tags: [ Embedding, 大语言模型, 地理数据, LangChain, 向量检索, Qwen ]
description: "用 Embedding 向量模型自动对齐地名，打造更聪明的数据查询系统"
---

地名拼写错误、简称混用、历史名称不一致……地理行业的数据清洗痛点之一就是"名称对不齐"。今天我们分享一种智能方式：**用 Embedding 向量模型自动对齐地名**，打造更聪明的数据查询系统。

---

## 📌 地理行业常见问题场景

在做地理大数据分析或问答接口时，你一定遇到过：

- 用户输入"成都高新区"，但你数据库里叫"高新技术产业开发区（成都）"；
- 用户写了"渝北区"，但你表里是"重庆市渝北区"；
- 数据源来自多系统，有"中山"、"中山市"、"中山（广东）"三种叫法。

这些拼写、格式、简称差异，导致无法正确匹配目标记录。传统 string matching（字符串匹配）方法太死板。怎么办？

---

## 💡 解决方案：用 Embedding 模型做智能相似度匹配

我们将所有地名编码为向量，再通过向量检索寻找"最相似"的标准名称，从而实现：

> 用户输入地名 → 转换为向量 → 检索最相似标准名称 → 返回结果

---

## ✅ 第一步：构建基本环境和准备模型

我们首先需要引入必要的组件，并初始化一个大语言模型（本文使用阿里 Qwen）、一个中文文本嵌入模型（DashScope Embedding）以及一个简单的向量数据库（这里用内存实现）。

```python
from config import *  # 包含密钥配置
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

llm = ChatOpenAI(model="qwen-max")
embeddings = DashScopeEmbeddings(model="text-embedding-v3")
vector_store = InMemoryVectorStore(embeddings)
```

---

## 📌 第二步：构建中文地名数据库并进行向量化

我们使用一个简单的地名列表模拟真实业务中的地理名称标准库。

```python
geo_names = [
    "北京市海淀区", "北京市朝阳区", "上海市浦东新区", "广东省深圳市南山区",
    "成都高新区", "重庆市渝北区", "杭州市西湖区", "中山市",
    "武汉市洪山区", "西安市雁塔区"
]

_ = vector_store.add_texts(geo_names)
```

每个地名会被转换为一个向量，从而可以通过语义进行模糊比对，不再依赖于完全一致的关键词。

---

## 🔍 第三步：查询相似地名（Embedding 检索）

现在我们尝试用用户的输入进行相似度查询。以下是一个最基础的检索示例：

```python
query = "成都高新技术产业开发区"
results = vector_store.similarity_search_with_score(query, k=3)

for name, score in results:
    print(f"候选名称：{name.page_content} | 相似度得分：{score:.4f}")
```

**结果为：**

```
候选名称：成都高新区 | 相似度得分：0.8053
候选名称：上海市浦东新区 | 相似度得分：0.5572
候选名称：中山市 | 相似度得分：0.5292
```

可以看到，尽管"成都高新技术产业开发区"与"成都高新区"在表述上有所不同，Embedding 依然能够准确识别出它们在语义上的高度一致性。

---

## 🛠 第四步：封装为工具组件，用于 Agent

我们可以把这个向量检索过程封装为一个工具，可以集成到 LangChain Agent 框架中，让大模型自主调用：

```python
from langchain.agents.agent_toolkits import create_retriever_tool

retriever = vector_store.as_retriever(search_kwargs={"k": 1})

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="search_geo_names",
    description="用于查找最相似的地理名称，如城市、区县、开发区等"
)
```

通过以上代码，我们成功构建了一个用于地名匹配的工具，接下来可以构建一个 Agent 并集成这个工具。

---

## 🤖 构建可调用工具的 AI Agent

借助 LangChain 提供的 `create_react_agent`，我们可以快速创建一个 Agent，使其具备调用我们自定义工具的能力。

```python
agent = create_react_agent(
    llm,
    tools=[retriever_tool]
)
```

接下来，调用 Agent 并传入用户的请求：

```python
result = agent.invoke({"messages": [{"role": "user", "content": "介绍难山区"}]})

for m in result['messages']:
    m.pretty_print()
```

**✅ 示例输出：**

```
================================ Human Message =================================
介绍难山区

================================== Ai Message ==================================
Tool Calls:
  search_geo_names (call_48e51e66ad684f88b08eff)
  Call ID: call_48e51e66ad684f88b08eff
  Args:
    query: 难山区

================================= Tool Message =================================
Name: search_geo_names
广东省深圳市南山区

================================== Ai Message ==================================
您提到的"难山区"可能是指广东省深圳市的南山区。南山区是深圳市的一个行政区，
位于深圳西部，毗邻香港，是中国改革开放的窗口，也是高新技术产业的重要基地。
区内有著名的科技园——深圳高新技术产业园区，汇集了大量的高科技企业和研发机构。
此外，南山区还拥有丰富的教育资源、文化设施以及优美的自然环境。

如果"难山区"不是您所指的地方，请提供更多的信息以便我能够更准确地为您提供相关信息。
```

---

## 🧠 第五步：智能匹配与过滤（LLM 二次判断）

尽管向量检索已经大幅提升了匹配的召回率，但在某些情况下，最高分匹配项可能只是"相关"而非"正确"。例如：

- 用户查询"成都"，数据库里有"成都高新区"，它们虽然相似，但并非同一实体。
- 用户输入"难山区"（错别字），最高匹配是"深圳市南山区"。

为了进一步提升准确率，我们可以引入 LLM 进行二次判断。

```python
from typing import Literal, Optional
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda


class MatchResult(BaseModel):
    """地名匹配结果"""
    name: Optional[str] = Field(None, description="最匹配的地名，仅在 accepted=True 时有值")
    accepted: Literal[True, False] = Field(..., description="是否接受该匹配结果")
    reason: Optional[str] = Field(None, description="匹配或拒绝的理由")


parser = PydanticOutputParser(pydantic_object=MatchResult)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个中文地名智能判断助手。请根据原始查询和候选地名及其相似度，"
            "判断是否存在真正语义等价的匹配项。\n\n"
            "要求：\n"
            "- 仅当你认为候选地名确实与原始查询表达的是同一个地理实体时，"
            "  才将 accepted 设置为 True，并填写对应的 name 和 score；\n"
            "- 如果所有候选项都不匹配（即便相似度较高），请将 accepted 设置为 False，"
            "  name 和 score 留空（设为 null），并简要说明原因；\n"
            "- 匹配标准需综合语义理解、业务常识和上下文逻辑；\n"
            "- 请严格按照以下结构化格式返回结果。\n\n"
            "{format_instructions}"
        ),
        ("human", "{query}")
    ]
).partial(format_instructions=parser.get_format_instructions())
```

---

## 🔗 拼接 Chain，实现自动判断

```python
def build_prompt_input(query: str, top_k: int = 3) -> dict:
    results = vector_store.similarity_search_with_score(query, k=top_k)
    formatted = "\n".join([
        f"- {doc.page_content}（相似度: {score:.4f}）" for doc, score in results
    ])
    prompt_text = \
        f"""原始查询: {query}
候选地名如下：
{formatted}
"""
    return {"query": prompt_text}


# 拼接完整处理链条
chain = (
    RunnableLambda(build_prompt_input)
    | prompt
    | llm
    | parser
)

chain.invoke("难山区")
```

**输出：**

```
MatchResult(name='广东省深圳市南山区', accepted=True, reason=None)
```

再看一个不匹配的例子：

```python
chain.invoke("成都")
```

**✅ 示例输出：**

```
MatchResult(name=None, accepted=False, reason="候选地名中没有与原始查询'成都'完全匹配的地名。")
```

---

## 📚 项目源码

如果你想看完整代码或亲自运行一遍，这里是项目的 GitHub 地址👇：

🔗 **https://github.com/zhengjie9510/learn-langchain**

---

## 总结

本文展示了如何结合 **Embedding 向量检索** 和 **LLM 智能判断**，解决地理数据中的名称对齐问题：

| 步骤 | 功能 | 关键技术 |
|------|------|----------|
| 向量检索 | 快速召回候选地名 | Embedding + 相似度计算 |
| LLM 判断 | 精确筛选匹配结果 | Pydantic 结构化输出 |
| Agent 集成 | 自动化查询流程 | LangChain + ReAct |

这种方法不仅适用于地名匹配，也可以迁移到其他需要模糊匹配的领域，如企业名称对齐、商品名称标准化等。
