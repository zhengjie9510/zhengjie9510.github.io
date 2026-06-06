# Global Rules

## Python 环境
系统已安装 uv。任何 Python 任务必须遵循以下流程：

### 第一步：检查虚拟环境
检查当前目录下是否存在 `.venv` 文件夹：
- 如果不存在，先执行 `uv venv` 创建虚拟环境
- 如果存在，跳过此步

### 第二步：激活并使用
所有 Python 操作必须通过 uv 执行：
- 安装包：`uv pip install <package>`
- 运行脚本：`uv run python script.py`
- 其他操作：`uv run <command>`

### 绝对禁止
- 禁止直接使用 `python`、`pip`、`python3` 等裸命令
- 禁止使用 `pip install` 而不通过 uv
- 禁止在没有虚拟环境的情况下运行 Python

## Node.js 环境
1. 项目无 `package.json` 时先执行 `npm init -y`
2. 禁止全局安装：`npm install -g`、`yarn global add`
