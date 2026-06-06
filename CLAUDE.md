# Global Rules

## Python 环境
系统已安装 uv。任何涉及 Python 的操作（包括内联命令 `python -c "..."`）**必须**在虚拟环境中执行。

### 强制前置步骤
每次执行 Python 相关命令前，**必须先确认**：
1. 当前项目目录下存在 `.venv` 文件夹
2. 如果不存在，**必须先执行** `uv venv` 创建虚拟环境
3. **然后再执行**实际的 Python 命令

### 唯一允许的调用方式
- 安装包：`uv pip install <package>`
- 运行脚本：`uv run python script.py`
- 运行内联代码：`uv run python -c "..."`
- 其他 Python 操作：`uv run <command>`

### 绝对禁止
- 禁止直接使用 `python`、`python3`、`pip`、`pip3` 等裸命令
- 禁止在没有 `.venv` 的情况下运行任何 Python 代码
- 禁止使用 `pip install` 而不通过 `uv pip install`
- 禁止跳过虚拟环境创建步骤

## Node.js 环境
1. 项目无 `package.json` 时先执行 `npm init -y`
2. 禁止全局安装：`npm install -g`、`yarn global add`
