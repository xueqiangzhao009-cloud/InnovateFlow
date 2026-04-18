# InnovateFlow

**InnovateFlow** 是一个基于 LangGraph 和 Docker 的多智能体创新协作框架。
你只需要描述需求，它就能自动完成规划、执行、测试的完整流程，帮你把想法变成可运行的代码。

## 核心特性

### 四 Agent 协作闭环

| Agent | 职责 |
|-------|------|
| **Planner** (规划师) | 理解需求，探索工作区，制定分步开发计划 |
| **Executor** (执行者) | 精准执行任务，作为"执行手术刀" |
| **Sandbox** (沙盒) | Docker 隔离运行，自动发现测试文件并执行 |
| **Reviewer** (审查员) | 分析错误栈 + diff，生成诊断报告并打回修复 |

### 多语言支持

支持 6 种常用语言，自动识别文件类型：

| 语言 | 文件扩展名 | 测试框架 |
|------|-----------|----------|
| Python | `.py` | pytest, unittest |
| JavaScript | `.js` | jest, mocha, vitest |
| TypeScript | `.ts`, `.tsx` | jest, vitest |
| Java | `.java` | junit, testng |
| Go | `.go` | testing |
| Rust | `.rs` | cargo-test |

### Git 集成

- 自动创建功能分支
- 智能 commit message 生成
- 变更 diff 可视化
- 版本回滚支持

### 上下文管理 — 三层记忆策略

| 层级 | 内容 | 策略 |
|------|------|------|
| 核心记忆 | 用户需求、执行计划、报错信息 | 永久保留，不可裁剪 |
| 工作记忆 | 最近 N 轮对话 | 滑动窗口，动态调整 |
| 参考记忆 | 历史对话结构摘要 | LLM 智能压缩，Fallback 基于规则 |

### Docker 隔离测试

- 无网 + 限存的临时容器 (`network_disabled=True`)
- 自动发现 `test_*.py` / `*_test.py`，优先 pytest 运行
- `requirements.txt` 自动 pip install
- 超时熔断 + `auto_remove` 防资源泄漏

### 可观测性

- 记录每次 LLM 调用的 Token 消耗和响应时间
- 测试失败时自动保存工作区快照
- 每个 Agent 都有独立的日志，方便排查问题

### 新增功能

- **代码质量分析**：静态代码分析，检测潜在问题
- **文档自动生成**：自动生成项目文档和 API 文档
- **多语言支持增强**：更全面的语言支持和测试框架适配

## 快速启动

### 环境要求

- Python 3.10+
- Docker Desktop (沙盒隔离)
- 任一 LLM 提供商：OpenAI / Anthropic / Ollama / DeepSeek

### 安装

```bash
git clone https://github.com/你的用户名/InnovateFlow.git
cd InnovateFlow
pip install -r requirements.txt
```

### 配置

在 `app/core/` 下创建 `.env` 文件（参考 `.env.example`）：

```bash
# Ollama 本地模型
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder

# 或 OpenAI
# OPENAI_API_KEY=sk-xxx
# OPENAI_MODEL=gpt-4o

# 或 Anthropic
# ANTHROPIC_API_KEY=sk-ant-xxx
# ANTHROPIC_MODEL=claude-sonnet-4-6
```

### 运行

```bash
# 方式一：Streamlit Web UI (推荐)
streamlit run web_ui.py

# 方式二：CLI
python run.py
```

## 项目结构

```
InnovateFlow/
├── run.py                      # LangGraph 工作流编排 & CLI 入口
├── web_ui.py                   # Streamlit Web UI
├── api_server.py               # FastAPI 后端 + React 前端服务
├── requirements.txt            # Python 依赖
│
├── app/
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
│   │   ├── code_quality.py     # 代码质量分析
│   │   └── documentation.py    # 文档自动生成
│   │
│   └── tools/
│       └── file_tools.py       # 8 个文件工具 (read/edit/write/...)
│
├── frontend/                   # React 前端
├── tests/                      # 单元测试
├── docs/                       # 自动生成的文档
└── workspace/                  # Agent 工作区
```

## 技术亮点

### AST 感知文件操作

- 大文件 (>5000 字符) 返回 AST 结构大纲而非原始内容
- `read_function` / `read_class` / `read_file_range` 精确定位
- `edit_file` 三级匹配：精确 → 去空匹配 → difflib 模糊匹配 (90% 阈值)
- 每次修改自动备份，支持一键回滚

### LLM 智能记忆压缩

旧对话经过 LLM（或基于规则的 fallback）压缩为四段式摘要：

1. 【用户需求】一句话概括原始需求
2. 【已完成的修改】列出所有文件改动
3. 【遇到的问题】列出遇到的错误和修复尝试
4. 【待解决】当前仍未解决的问题

### 代码质量分析

- 支持多种语言的静态代码分析
- 自动检测潜在问题和代码风格问题
- 生成详细的代码质量报告

### 文档自动生成

- 自动生成项目 README 和技术文档
- 提取代码注释生成 API 文档
- 支持多种文档格式

## 依赖项

| 依赖 | 用途 |
|------|------|
| langgraph | 状态机 / Agent 编排 |
| langchain-core | LLM 消息 / 工具调用抽象 |
| langchain-openai / anthropic / ollama | LLM 提供商适配器 |
| pydantic v2 | 结构化输出解析 |
| tiktoken | 精确 Token 计数 |
| docker | 沙盒容器引擎 |
| streamlit | Web UI 框架 |
| python-dotenv | 环境变量管理 |
| flake8 | Python 代码质量分析 |
| eslint | JavaScript/TypeScript 代码质量分析 |

## 开源协议

MIT License

---

Made by [xueqiangzhao009-cloud](https://github.com/xueqiangzhao009-cloud)