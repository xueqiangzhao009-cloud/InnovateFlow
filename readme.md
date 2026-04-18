# InnovateFlow

## 什么是 InnovateFlow？

InnovateFlow 是一个革命性的 AI 驱动开发框架，通过多智能体协作系统，将创意想法快速转化为可运行的软件解决方案。它不仅是一个工具，更是一个智能协作伙伴，能够理解需求、制定计划、执行任务、测试验证并提供反馈。

## 为什么选择 InnovateFlow？

- **智能自动化**：减少手动编码和测试工作，让您专注于创意和业务逻辑
- **多智能体协作**：四个专业智能体协同工作，覆盖开发全流程
- **安全可靠**：Docker 隔离测试环境，确保代码质量和系统安全
- **多语言支持**：适配多种编程语言，满足不同项目需求
- **智能上下文管理**：记住关键信息，提供连贯的开发体验
- **全栈解决方案**：从前端到后端，从开发到测试的完整工具链

## 系统概览

InnovateFlow 由四个核心智能体组成，它们相互协作，形成一个完整的开发闭环：

| 智能体 | 职责 | 核心能力 |
|--------|------|----------|
| **规划师** | 需求分析与计划制定 | 需求理解、工作区探索、任务分解 |
| **执行者** | 代码实现与文件操作 | 精准执行、文件修改、功能实现 |
| **沙盒** | 代码测试与验证 | Docker 隔离、自动测试、结果分析 |
| **审查员** | 代码审查与问题修复 | 错误分析、诊断报告、修复建议 |

## 快速上手

### 环境准备

- **Python**：3.10 或更高版本
- **Docker**：Docker Desktop 或 Docker Engine
- **LLM 服务**：OpenAI、Anthropic、Ollama 或 DeepSeek

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/xueqiangzhao009-cloud/InnovateFlow.git
   cd InnovateFlow
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 LLM**
   在 `app/core/` 目录创建 `.env` 文件，添加您的 LLM 配置：
   ```bash
   # Ollama 本地模型
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=qwen2.5-coder
   
   # 或 OpenAI
   # OPENAI_API_KEY=sk-xxx
   # OPENAI_MODEL=gpt-4o
   ```

4. **启动服务**
   - **Web 界面**：`streamlit run web_ui.py`
   - **命令行**：`python run.py`
   - **API 服务**：`python api_server.py`

## 技术架构

InnovateFlow 采用分层架构设计，确保系统的可扩展性和可维护性：

### 1. 智能体层
- **规划师**：理解用户需求，生成详细的开发计划
- **执行者**：执行开发任务，修改和创建文件
- **沙盒**：在隔离环境中运行测试，验证代码质量
- **审查员**：分析测试结果，提供修复建议

### 2. 服务层
- **上下文管理**：维护对话历史和执行状态
- **LLM 引擎**：管理与大语言模型的交互
- **文件工具**：提供安全的文件操作功能
- **路由决策**：根据执行状态决定下一步操作
- **可观测性**：收集和分析系统运行数据

### 3. 接口层
- **Streamlit Web UI**：交互式用户界面
- **FastAPI 后端**：REST API 和 SSE 接口
- **React 前端**：现代化的 Web 应用界面

## 项目组织

```
InnovateFlow/
├── run.py              # 核心工作流编排
├── web_ui.py           # Streamlit Web 界面
├── api_server.py       # FastAPI 后端服务
├── requirements.txt    # Python 依赖
│
├── app/                # 应用核心代码
│   ├── agents/         # 智能体实现
│   ├── core/           # 核心服务
│   └── tools/          # 工具集
│
├── frontend/           # React 前端
├── tests/              # 测试代码
├── docs/               # 项目文档
└── workspace/          # 智能体工作区
```

## 核心特性

### 智能任务规划
- 自动分析需求，生成详细的开发计划
- 识别项目依赖和技术栈需求
- 优化任务顺序，提高开发效率

### 精准代码执行
- 智能文件操作，支持代码修改和创建
- AST 感知，精确定位和修改代码
- 自动备份和回滚机制，确保安全

### 安全测试环境
- Docker 容器隔离，避免环境冲突
- 自动发现和运行测试文件
- 智能分析测试结果，识别问题

### 智能代码审查
- 分析错误栈和代码差异
- 生成详细的诊断报告
- 提供具体的修复建议

### 多语言支持
- 支持 10+ 种编程语言
- 自动识别文件类型和测试框架
- 适配不同语言的代码风格和规范

## 使用场景

### 场景一：快速原型开发
描述您的想法，InnovateFlow 会自动生成代码原型，帮助您验证概念。

### 场景二：代码维护和修复
提供代码库和问题描述，InnovateFlow 会分析并修复问题。

### 场景三：全栈应用开发
从前端到后端，InnovateFlow 可以帮您构建完整的应用。

### 场景四：技术迁移
将代码从一种语言或框架迁移到另一种，InnovateFlow 会自动处理大部分工作。

## 技术栈

| 技术 | 用途 |
|------|------|
| Python | 核心后端语言 |
| LangGraph | 智能体状态管理和工作流编排 |
| LangChain | LLM 接口和工具集成 |
| Docker | 沙盒隔离测试环境 |
| Streamlit | Web 用户界面 |
| FastAPI | API 服务 |
| React + TypeScript | 前端框架 |
| Pydantic | 数据验证和设置管理 |
| Git | 版本控制 |

## 最佳实践

1. **清晰描述需求**：提供详细的需求描述，包括功能、技术栈和预期结果
2. **提供上下文**：如果是现有项目，提供相关文件和代码库信息
3. **设置合理的期望**：复杂项目可能需要多个迭代周期
4. **定期审查结果**：检查生成的代码和测试结果，提供反馈
5. **使用版本控制**：定期提交代码，确保可以回滚到之前的状态

## 常见问题

### Q: InnovateFlow 支持哪些编程语言？
A: 支持 Python、JavaScript、TypeScript、Java、Go、Rust、C、C++、PHP 和 Ruby 等多种语言。

### Q: 需要什么样的硬件配置？
A: 建议至少 8GB 内存，推荐 16GB 以上，以支持 Docker 和 LLM 运行。

### Q: 可以使用本地 LLM 吗？
A: 是的，支持 Ollama 本地模型，无需外部 API 调用。

### Q: 如何处理复杂的项目？
A: 对于复杂项目，建议分阶段处理，每次专注于一个模块或功能。

## 贡献

我们欢迎社区贡献，包括：
- 功能增强和新特性开发
- 错误修复和性能优化
- 文档改进
- 测试用例补充

### 贡献流程
1. Fork 仓库
2. 创建功能分支
3. 实现更改
4. 运行测试
5. 提交 Pull Request

## 许可证

InnovateFlow 采用 MIT 许可证，详见 LICENSE 文件。

## 联系方式

- **项目地址**：https://github.com/xueqiangzhao009-cloud/InnovateFlow
- **作者**：xueqiangzhao009-cloud

---

*创新无限，流程可控 —— InnovateFlow*