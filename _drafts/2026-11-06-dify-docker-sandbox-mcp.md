---
layout: post
title: "Claude Code 能直接操作文件，Dify 如何获得类似能力？"
categories: [AI 工具]
tags: [MCP, Docker, Dify, Sandbox, AI Agent]
description: "通过 langchain-docker-backend 项目，将 Docker 中的文件操作和命令执行能力通过 MCP 提供给 Dify 等 AI Agent。"
---

使用 Claude Code 时，我们可以让它直接读取项目文件、修改代码、执行 Shell 命令，甚至安装依赖、运行测试。

我们只需要告诉它要做什么，剩下的事情，它就可以自己一步步完成。

但如果换成 Dify 呢？

Dify 同样可以搭建 AI Agent，也支持通过工具和 MCP 扩展能力。不过，如果希望 Agent 像 Claude Code 一样，拥有一个可以自由读写文件、执行命令的工作空间，就需要额外提供这样的执行环境。

**有没有办法，让 Dify 也拥有一套类似的能力？**

最近发现了一个开源项目，提供了一个不错的解决思路：通过 MCP，将 Docker 容器中的文件操作和命令执行能力开放给 AI Agent。

项目地址：

[langchain-docker-backend](https://github.com/zhengjie9510/langchain-docker-backend)

---

## 🤔 为什么 Agent 需要一个执行环境？

我们可以把大模型理解成一个大脑。

它能够理解需求、分析问题、制定计划，但如果没有外部工具，它实际上很难直接操作真实世界。

例如，让 Claude Code 帮我们分析一个 Python 项目：

它可以先查看项目目录，读取代码文件，找到需要修改的地方，然后编写代码、执行测试，最后根据测试结果继续调整。

这个过程中，除了大模型本身的推理能力，还需要一套基础工具：

- 📖 **读取**：查看文件和目录。
- ✏️ **修改**：创建文件、修改代码。
- 🔍 **搜索**：查找文件和代码内容。
- ⚡ **执行**：运行 Shell 命令和 Python 脚本。

这些能力组合起来，就构成了 Agent 的一个执行环境。

而在 Dify 这样的平台中，我们通常更多地使用预先配置好的工具，例如搜索、数据库查询、API 调用等。

如果希望 Agent 拥有更加通用的文件操作和命令执行能力，就可以考虑将这部分能力独立出来，通过 MCP 提供给它。

**这也是今天这个项目想解决的问题。**

---

## 🧩 通过 MCP，把 Docker 变成 Agent 的工作空间

这个项目的思路其实很简单：

既然 Agent 需要一个可以操作文件、执行命令的环境，那就直接用 Docker 创建一个独立的工作空间。

然后，通过 MCP 将这个工作空间提供给 Agent 使用。

整个过程可以用一张图来理解：

```text
       Dify / AI Agent
              |
              | MCP
              |
          MCP Server
              |
          Docker 沙箱
              |
       -----------------
       | 读取文件      |
       | 修改文件      |
       | 搜索文件      |
       | 执行命令      |
       -----------------
```

这里面有三个角色：

- **Dify**：理解用户需求，决定调用什么工具。
- **MCP Server**：负责将 Docker 沙箱的能力提供出来。
- **Docker**：提供实际运行命令和操作文件的环境。

项目目前提供了 7 个 MCP 工具：

| 工具 | 功能 |
|---|---|
| `ls` | 查看文件和目录 |
| `read` | 读取文件 |
| `write` | 创建和写入文件 |
| `edit` | 修改文件内容 |
| `glob` | 查找文件 |
| `grep` | 搜索文件内容 |
| `execute` | 执行 Shell 命令 |

虽然只有 7 个工具，但它们已经覆盖了 Agent 日常操作文件和执行任务所需要的很多基础能力。

---

## 💡 接入之后，可以做什么？

举个例子。

假设我们在 Dify 中配置了这个 MCP Server，然后向 Agent 提出一个需求：

> 帮我分析工作目录中的 CSV 文件，统计每一列的缺失值，生成 Python 分析脚本并执行，最后输出一份分析报告。

接下来，Agent 就可以自己完成一系列操作：

**查看文件**

调用 `ls`，了解当前目录有哪些文件。

**读取数据**

找到 CSV 文件，通过 `read` 查看文件内容。

**编写代码**

调用 `write`，创建一个 Python 分析脚本。

**执行程序**

调用 `execute`，运行刚刚创建的脚本。

**整理结果**

根据程序的执行结果，继续分析并生成报告。

如果运行过程中发现问题，还可以修改脚本，再次执行。

你会发现，这已经不只是简单的 API 调用了。

Agent 可以根据任务需要，自主组合不同的工具，一步步完成工作。

**这也是 Claude Code 这类智能体比较典型的工作方式。**

---

## ⚙️ 如何启动这个 MCP Server？

项目已经封装好了 Docker 沙箱和 MCP 工具，使用起来并不复杂。

首先，需要安装并启动 Docker，然后安装项目：

```bash
pip install 'langchain-docker-backend[mcp]'
```

拉取默认 Docker 镜像：

```bash
docker pull python:3.13-slim
```

接下来，创建一个 `mcp_server.py` 文件：

```python
from langchain_docker_backend import DockerSandbox
from langchain_docker_backend.mcp import create_mcp_server

with DockerSandbox() as sandbox:
    create_mcp_server(sandbox).run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )
```

启动服务：

```bash
python mcp_server.py
```

这样，一个提供文件操作和命令执行能力的 MCP Server 就启动了。

默认情况下，可以通过下面的地址访问：

```text
http://127.0.0.1:8000/mcp
```

如果要让其他机器或容器中的 Dify 访问，需要使用实际可访问的 IP 或服务地址，并确保网络互通。

接下来，只需要在 Dify 中配置支持 MCP 的工具插件，连接这个服务即可。

需要注意：这个项目的一个 MCP Server 实例默认使用一个共享沙箱。如果涉及多个用户，还需要额外考虑执行环境的隔离。另外，Shell 执行权限比较高，不要将服务直接开放给不可信用户。

---

## 🎯 写在最后

回过头来看，Claude Code 和 Dify 的区别，并不只是模型能力的区别。

一个能够真正执行任务的 Agent，除了大模型，还需要工具和运行环境。

Claude Code 已经把这些能力整合在了产品中，而对于 Dify 这样的应用开发平台，我们也可以通过 MCP 将它们接入进来。

这个项目提供的就是其中一种实现方式：

> **Docker 提供执行环境，MCP 负责连接，Agent 负责思考和执行。**

它并不是要让 Dify 变成 Claude Code，而是让不同的 Agent 平台都能复用一套通用的执行环境。

我觉得这也是 MCP 一个很有意思的应用方向：不只是让 AI 连接更多 API，还可以让 AI 获得真正动手做事的能力。
