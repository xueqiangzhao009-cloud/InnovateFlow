# InnovateFlow 项目指南

## 项目简介

InnovateFlow 是一个基于 LangGraph 和 Docker 的多智能体创新协作框架。用户只需描述需求，系统会自动完成规划、执行、测试的完整流程，帮你把想法变成可运行的解决方案。

## 技术栈

- **后端**: Python 3.10+, LangGraph, FastAPI
- **前端**: React 18, TypeScript, Vite
- **沙盒**: Docker
- **LLM**: 支持 OpenAI、Anthropic、Ollama、DeepSeek

## 开发命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest

# 启动 Web UI（推荐）
streamlit run web_ui.py

# 启动 React 前端 + FastAPI 后端
python api_server.py

# CLI 模式
python run.py
```

前端开发模式：
```bash
cd frontend
npm install
npm run dev  # 启动 Vite 开发服务器，端口 3000
```

## 项目结构

```
InnovateFlow/
├── run.py                      # LangGraph 工作流编排 & CLI 入口
├── web_ui.py                   # Streamlit Web UI
├── api_server.py               # FastAPI 后端 + React 前端服务
├── requirements.txt            # Python 依赖
│
├── src/
│   ├── agents/
│   │   ├── Planner.py          # 规划师：需求理解 + 计划生成
│   │   ├── Executor.py         # 执行者：任务执行 + 文件修改
│   │   ├── Reviewer.py         # 审查员：报错分析 + 诊断报告
│   │   └── Sandbox.py          # 沙盒：Docker 隔离测试
│   │
│   ├── core/
│   │   ├── config.py           # 全局配置 & 路径解析
│   │   ├── context_manager.py  # 分层上下文管理 v2.0
│   │   ├── state.py            # AgentState 定义 + InMemorySaver
│   │   ├── llm_engine.py       # 多提供商 LLM 初始化 + 异步重试
│   │   ├── logger.py           # 结构化日志
│   │   ├── repo_map.py         # AST 仓库地图
│   │   ├── routing.py          # 路由决策逻辑
│   │   ├── recovery.py         # 熔断快照 & 错误恢复
│   │   ├── metrics.py          # 可观测性指标收集器
│   │   ├── language_support.py # 多语言支持
│   │   ├── git_integration.py  # Git 集成
│   │   ├── quality_analysis.py # 质量分析
│   │   └── documentation.py    # 文档自动生成
│   │
│   └── tools/
│       └── file_tools.py       # 8 个文件工具 (read/edit/write/...)
│
├── frontend/                   # React 前端
│   └── src/
│       ├── pages/
│       │   ├── ChatPage.tsx    # 聊天页面
│       │   ├── MetricsPage.tsx # 指标面板
│       │   ├── FileBrowserPage.tsx # 文件浏览器
│       │   └── ConfigPage.tsx  # 配置面板
│       └── context/
│           └── AppContext.tsx  # 全局状态管理
│
├── tests/                      # 单元测试
├── docs/                       # 自动生成的文档
└── workspace/                  # Agent 工作区
```

## 核心功能

### 四个 Agent

| Agent | 职责 |
|-------|------|
| Planner | 理解需求，探索工作区，制定开发计划 |
| Executor | 执行任务，读写文件，修改代码 |
| Sandbox | Docker 隔离测试，自动发现测试文件 |
| Reviewer | 分析测试失败原因，给出修复建议 |

### 上下文管理

三层记忆策略：
- **核心记忆**: 用户需求、执行计划、错误信息（永久保留）
- **工作记忆**: 最近 N 轮对话（滑动窗口）
- **参考记忆**: 历史对话摘要（LLM 压缩）

### 文件操作

- 大文件（>5000字符）返回 AST 结构大纲
- `read_function` / `read_class` 精确定位代码
- `edit_file` 支持精确匹配和模糊匹配
- 每次修改自动备份

## 配置

在 `src/core/.env` 中配置：

```bash
# 选择 LLM 提供商
LLM_PROVIDER=deepseek

# DeepSeek 配置
DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 或者使用 Ollama 本地模型
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=qwen2.5-coder
```

## 工作流程

```
用户需求 → Planner 规划 → Executor 执行 → Sandbox 测试
                                    ↑           ↓
                                    └─ Reviewer 审查（失败时）
```

## API 接口

| 接口 | 说明 |
|------|------|
| POST /api/run | 启动工作流 |
| GET /api/run/{thread_id}/events | SSE 事件流 |
| GET /api/run/{thread_id}/state | 获取最终状态 |
| GET /api/files | 工作区文件列表 |
| GET /api/metrics | 指标数据 |
| GET /api/config | 配置信息 |