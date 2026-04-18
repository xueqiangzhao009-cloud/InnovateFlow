# API 文档

## 工作流 API

| 接口 | 说明 |
|------|------|
| POST /api/run | 启动工作流 |
| GET /api/run/{thread_id}/events | SSE 事件流 |
| GET /api/run/{thread_id}/state | 获取最终状态 |
| GET /api/files | 工作区文件列表 |
| GET /api/metrics | 指标数据 |
| GET /api/config | 配置信息 |

## 核心模块 API

### code_quality

#### 类
- `class`

#### 函数
- `__init__()`

### config

### context_manager

#### 类
- `ContextSlot`
- `Test功能名`
- `Test功能名`

#### 函数
- `get_encoding()`
- `__init__()`
- `test_具体用例()`
- `test_具体用例()`
- `test_具体用例()`
- `test_具体用例()`

### documentation

#### 类
- `class`

#### 函数
- `__init__()`

### git_integration

#### 类
- `class`
- `CommitMessageGenerator`

#### 函数
- `__init__()`

### language_support

#### 类
- `Language`
- `class`
- `ASTParser`

#### 函数
- `__init__()`

### llm_engine

#### 类
- `LLMWithRetry`
- `_LazyLLM`

#### 函数
- `__init__()`
- `ainvoke()`
- `invoke()`
- `bind_tools()`
- `__getattr__()`
- `_get()`
- `__getattr__()`

### logger

### metrics

#### 类
- `MetricsCollector`

#### 函数
- `__init__()`
- `record_llm_call_end()`
- `record_tool_success()`
- `record_tool_failure()`
- `record_repair_cycle_start()`
- `record_repair_cycle_outcome()`
- `flush_to_file()`

### recovery

#### 函数
- `_copy_python_files()`

### repo_map

#### 函数
- `generate_repo_map()`

### routing

#### 函数
- `route_after_planner()`
- `route_after_executor()`

### state

#### 类
- `MemorySummary`
- `AgentState`
