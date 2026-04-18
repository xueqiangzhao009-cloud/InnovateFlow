# 代码文档

## app\agents\Coder.py

### 模块文档
Coder Agent - 工程师节点
负责执行代码编写与修改任务

### 函数: coder_node()
Coder 节点执行函数（异步）。
    根据当前计划和报错信息，执行代码编写或修改任务。

    Returns:
        dict: 更新的状态，包含 LLM 响应和记忆摘要

---

## app\agents\Executor.py

### 模块文档
Executor Agent - 执行者节点
负责执行任务与文件修改

### 函数: executor_node()
Executor 节点执行函数（异步）。
    根据当前计划和报错信息，执行任务或修改文件。

    Returns:
        dict: 更新的状态，包含 LLM 响应和记忆摘要

---

## app\agents\Planner.py

---

## app\agents\Reviewer.py

### 模块文档
Reviewer Agent - 代码审查员节点
负责分析沙盒测试中的报错信息，提供诊断报告
新增 diff 分析与错误分类能力

### 函数: reviewer_node()
Reviewer 节点 (Critic)（异步）：不写代码，只看报错和 diff，
    负责提供"诊断报告"并分类错误类型。

    Returns:
        dict: 更新的状态，包含诊断报告消息

---

## app\agents\Sandbox.py

### 模块文档
扫描工作区中所有测试文件（test_*.py 和 *_test.py）。

### 函数: sandbox_node()
Sandbox 节点：负责在 Docker 隔离环境中执行代码，智能发现测试文件，
    自动选择 pytest / unittest 运行测试，并输出结构化测试报告。

### 函数: _write_test_result_json()
将测试结果写入 workspace/.test_result.json，方便 Reviewer 和用户查看。

---

## app\agents\__init__.py

---

## app\core\code_quality.py

### 模块文档
InnovateFlow 代码质量分析模块

提供代码质量分析功能：
- 静态代码分析
- 代码风格检查
- 潜在问题检测
- 代码质量报告生成

### 类: class
初始化代码质量分析器

        Args:
            project_root: 项目根目录

### 函数: __init__()
初始化代码质量分析器

        Args:
            project_root: 项目根目录

---

## app\core\config.py

### 模块文档
全局配置模块
定义项目路径、沙盒参数、工具阈值等核心配置。

---

## app\core\context_manager.py

### 模块文档
上下文管理器 (Context Manager) - v2.0
负责为不同的 Agent 构建最优化的上下文，避免 Token 浪费和上下文丢失问题。

分层策略：
- Layer 1: 核心记忆 (永久保留) - 用户需求、当前计划、报错信息
- Layer 2: 工作记忆 (动态窗口) - 最近 N 轮对话
- Layer 3: 参考记忆 (LLM 驱动摘要压缩) - 历史对话的结构化摘要

改进点：
1. 引入 tiktoken 精确 Token 计数
2. 激活 file_signatures 机制
3. LLM 驱动的智能记忆压缩
4. 动态上下文窗口大小
5. 上下文槽位优先级队列

### 类: ContextSlot
上下文槽位 - 用于管理不同类型的上下文片段

### 函数: get_encoding()
获取 tiktoken encoder，带缓存机制

---

## app\core\documentation.py

### 模块文档
InnovateFlow 文档自动生成模块

提供代码文档和项目文档的自动生成功能：
- 代码注释提取和整理
- API 文档生成
- README 文件自动更新
- 技术文档生成

### 类: class
初始化文档生成器

        Args:
            project_root: 项目根目录

### 函数: __init__()
初始化文档生成器

        Args:
            project_root: 项目根目录

---

## app\core\git_integration.py

### 模块文档
InnovateFlow Git 集成模块

提供版本控制功能：
- 自动创建功能分支
- 智能 commit message 生成
- 变更 diff 可视化
- 版本回滚支持
- 代码变更追踪

### 类: class
初始化Git仓库管理器

        Args:
            repo_path: 仓库路径

### 类: CommitMessageGenerator
智能Commit消息生成器

### 函数: __init__()
初始化Git仓库管理器

        Args:
            repo_path: 仓库路径

---

## app\core\language_support.py

### 模块文档
InnovateFlow 多语言支持模块

支持多种编程语言的AST解析和测试框架适配。
支持语言：Python, JavaScript/TypeScript, Java, Go, Rust, C, C++, PHP, Ruby

### 类: Language
支持的编程语言枚举

### 类: class
语言配置

### 类: ASTParser
多语言AST解析器基类

---

## app\core\llm_engine.py

### 模块文档
LLM 引擎初始化模块
支持多模型提供商（OpenAI、Claude、Ollama、DeepSeek 等）
自动根据环境变量选择合适的模型提供商

### 类: LLMWithRetry
为 LLM 添加重试机制的包装类。
    由于 Pydantic BaseModel 不支持动态设置属性，我们使用包装类来实现。

### 类: _LazyLLM
懒加载 LLM 代理，避免在模块 import 时就执行网络请求。

### 函数: ainvoke()
异步调用，带指数退避重试

### 函数: bind_tools()
代理 bind_tools 调用到内部 LLM

### 函数: __getattr__()
代理其他属性访问到内部 LLM

---

## app\core\logger.py

### 模块文档
统一日志模块
提供结构化的日志记录功能，替代分散的 print 语句。

---

## app\core\metrics.py

### 模块文档
可观测性指标模块 (Observability Metrics)
记录 LLM 调用的 token 消耗、延迟、修复轮数、工具成功率等指标。

### 类: MetricsCollector
线程安全的指标收集器，按维度聚合数据并输出到日志和文件。

### 函数: record_llm_call_end()
记录一次 LLM 调用的完成，自动计算延迟并归档。

### 函数: record_repair_cycle_outcome()
outcome: 'fixed' | 'still_failing'

### 函数: flush_to_file()
将指标快照写入文件。

---

## app\core\recovery.py

### 模块文档
错误恢复模块 (Error Recovery)
在达到最大重试次数熔断前，保存工作区文件状态快照和修改日志，
确保用户仍能看到"尽力而为"的成果。

### 函数: _copy_python_files()
递归复制所有 .py 文件到目标目录。

---

## app\core\repo_map.py

### 模块文档
生成带有函数签名摘要的目录树

### 函数: generate_repo_map()
生成带有函数签名摘要的目录树

---

## app\core\routing.py

### 模块文档
路由控制模块 - 封装 LangGraph 图的节点间路由决策逻辑。
将其从 run.py 中抽取出来，使得路由逻辑可以被独立测试。

### 函数: route_after_planner()
判断 Planner 是在探索工具，还是做好了计划

### 函数: route_after_executor()
判断 Executor 是在执行任务/看文件，还是全部完工了

---

## app\core\state.py

### 模块文档
结构化的记忆摘要，用于替代冗长的原始对话

### 类: MemorySummary
结构化的记忆摘要，用于替代冗长的原始对话

### 类: AgentState
nanoCursor 的全局黑板 (Blackboard)。
    所有的 Agent 节点都在这里读取和写入数据。

---

## app\core\__init__.py

### 模块文档
InnovateFlow 核心模块

---

## app\tools\file_tools.py

### 模块文档
文件操作工具模块
支持文件读取、写入、编辑，以及文件备份和回滚功能。
新增 AST 感知的智能读取能力，避免大文件内容被压缩丢失。

---

## app\tools\__init__.py

---
