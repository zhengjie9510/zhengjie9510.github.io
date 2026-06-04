# Global Rules

- Python 环境隔离：使用项目级工具（如 `uv`、`poetry`、`pipenv`）管理依赖和运行脚本，不要使用系统 Python 环境；项目没有虚拟环境时主动创建（如 `uv venv`）
- Node.js 环境隔离：只能在项目本地环境中安装包，不能使用全局环境；项目没有 `package.json` 时主动用 `npm init` 初始化，然后用 `npm install` 安装依赖到项目本地的 `node_modules` 目录
