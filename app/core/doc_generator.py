"""
InnovateFlow 文档自动生成模块

提供代码文档和项目文档的自动生成功能：
- 代码注释提取和整理
- API 文档生成
- README 文件自动更新
- 技术文档生成
"""

import os
import re
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from app.core.logging import setup_logger
from app.core.lang_support import Language, detect_language

logger = setup_logger("InnovateFlow.documentation")


@dataclass
class DocComment:
    """文档注释"""
    content: str
    line_start: int
    line_end: int
    type: str  # function, class, module


class DocumentationGenerator:
    """
    文档生成器
    """

    def __init__(self, project_root: str):
        """
        初始化文档生成器

        Args:
            project_root: 项目根目录
        """
        self.project_root = project_root

    def generate_project_docs(self, output_dir: Optional[str] = None) -> Dict[str, str]:
        """
        生成项目文档

        Args:
            output_dir: 输出目录（可选）

        Returns:
            生成的文档文件路径和内容的字典
        """
        if not output_dir:
            output_dir = os.path.join(self.project_root, "docs")
        
        os.makedirs(output_dir, exist_ok=True)
        
        docs = {}
        
        # 生成 README.md
        readme_content = self._generate_readme()
        readme_path = os.path.join(output_dir, "README.md")
        docs[readme_path] = readme_content
        
        # 生成 API 文档
        api_docs = self._generate_api_docs()
        api_docs_path = os.path.join(output_dir, "api_docs.md")
        docs[api_docs_path] = api_docs
        
        # 生成技术架构文档
        architecture_docs = self._generate_architecture_docs()
        architecture_docs_path = os.path.join(output_dir, "architecture.md")
        docs[architecture_docs_path] = architecture_docs
        
        # 生成代码文档
        code_docs = self._generate_code_docs()
        code_docs_path = os.path.join(output_dir, "code_docs.md")
        docs[code_docs_path] = code_docs
        
        # 写入文件
        for path, content in docs.items():
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"生成文档: {path}")
            except Exception as e:
                logger.error(f"写入文档失败 {path}: {e}")
        
        return docs

    def _generate_readme(self) -> str:
        """
        生成 README.md 内容
        """
        lines = []
        lines.append("# InnovateFlow")
        lines.append("")
        lines.append("**InnovateFlow** 是一个基于 LangGraph 和 Docker 的多智能体创新协作框架。")
        lines.append("你只需要描述需求，它就能自动完成规划、执行、测试的完整流程，帮你把想法变成可运行的代码。")
        lines.append("")
        lines.append("## 核心特性")
        lines.append("")
        lines.append("### 四 Agent 协作闭环")
        lines.append("")
        lines.append("| Agent | 职责 |")
        lines.append("|-------|------|")
        lines.append("| **Planner** (规划师) | 理解需求，探索工作区，制定分步开发计划 |")
        lines.append("| **Executor** (执行者) | 精准执行任务，作为\"执行手术刀\" |")
        lines.append("| **Sandbox** (沙盒) | Docker 隔离运行，自动发现测试文件并执行 |")
        lines.append("| **Reviewer** (审查员) | 分析错误栈 + diff，生成诊断报告并打回修复 |")
        lines.append("")
        lines.append("### 多语言支持")
        lines.append("")
        lines.append("支持 6 种常用语言，自动识别文件类型：")
        lines.append("")
        lines.append("| 语言 | 文件扩展名 | 测试框架 |")
        lines.append("|------|-----------|----------|")
        lines.append("| Python | `.py` | pytest, unittest |")
        lines.append("| JavaScript | `.js` | jest, mocha, vitest |")
        lines.append("| TypeScript | `.ts`, `.tsx` | jest, vitest |")
        lines.append("| Java | `.java` | junit, testng |")
        lines.append("| Go | `.go` | testing |")
        lines.append("| Rust | `.rs` | cargo-test |")
        lines.append("")
        lines.append("### Git 集成")
        lines.append("")
        lines.append("- 自动创建功能分支")
        lines.append("- 智能 commit message 生成")
        lines.append("- 变更 diff 可视化")
        lines.append("- 版本回滚支持")
        lines.append("")
        lines.append("### 上下文管理 — 三层记忆策略")
        lines.append("")
        lines.append("| 层级 | 内容 | 策略 |")
        lines.append("|------|------|------|")
        lines.append("| 核心记忆 | 用户需求、执行计划、报错信息 | 永久保留，不可裁剪 |")
        lines.append("| 工作记忆 | 最近 N 轮对话 | 滑动窗口，动态调整 |")
        lines.append("| 参考记忆 | 历史对话结构摘要 | LLM 智能压缩，Fallback 基于规则 |")
        lines.append("")
        lines.append("### Docker 隔离测试")
        lines.append("")
        lines.append("- 无网 + 限存的临时容器 (`network_disabled=True`)")
        lines.append("- 自动发现 `test_*.py` / `*_test.py`，优先 pytest 运行")
        lines.append("- `requirements.txt` 自动 pip install")
        lines.append("- 超时熔断 + `auto_remove` 防资源泄漏")
        lines.append("")
        lines.append("### 可观测性")
        lines.append("")
        lines.append("- 记录每次 LLM 调用的 Token 消耗和响应时间")
        lines.append("- 测试失败时自动保存工作区快照")
        lines.append("- 每个 Agent 都有独立的日志，方便排查问题")
        lines.append("")
        lines.append("### 新增功能")
        lines.append("")
        lines.append("- **代码质量分析**：静态代码分析，检测潜在问题")
        lines.append("- **文档自动生成**：自动生成项目文档和 API 文档")
        lines.append("- **多语言支持增强**：更全面的语言支持和测试框架适配")
        lines.append("")
        lines.append("## 快速启动")
        lines.append("")
        lines.append("### 环境要求")
        lines.append("")
        lines.append("- Python 3.10+")
        lines.append("- Docker Desktop (沙盒隔离)")
        lines.append("- 任一 LLM 提供商：OpenAI / Anthropic / Ollama / DeepSeek")
        lines.append("")
        lines.append("### 安装")
        lines.append("")
        lines.append("```bash")
        lines.append("git clone https://github.com/你的用户名/InnovateFlow.git")
        lines.append("cd InnovateFlow")
        lines.append("pip install -r requirements.txt")
        lines.append("```")
        lines.append("")
        lines.append("### 配置")
        lines.append("")
        lines.append("在 `app/core/` 下创建 `.env` 文件（参考 `.env.example`）：")
        lines.append("")
        lines.append("```bash")
        lines.append("# Ollama 本地模型")
        lines.append("OLLAMA_BASE_URL=http://localhost:11434")
        lines.append("OLLAMA_MODEL=qwen2.5-coder")
        lines.append("")
        lines.append("# 或 OpenAI")
        lines.append("# OPENAI_API_KEY=sk-xxx")
        lines.append("# OPENAI_MODEL=gpt-4o")
        lines.append("")
        lines.append("# 或 Anthropic")
        lines.append("# ANTHROPIC_API_KEY=sk-ant-xxx")
        lines.append("# ANTHROPIC_MODEL=claude-sonnet-4-6")
        lines.append("```")
        lines.append("")
        lines.append("### 运行")
        lines.append("")
        lines.append("```bash")
        lines.append("# 方式一：Streamlit Web UI (推荐)")
        lines.append("streamlit run web_ui.py")
        lines.append("")
        lines.append("# 方式二：CLI")
        lines.append("python run.py")
        lines.append("```")
        lines.append("")
        lines.append("## 项目结构")
        lines.append("")
        lines.append("```")
        lines.append("InnovateFlow/")
        lines.append("├── run.py                      # LangGraph 工作流编排 & CLI 入口")
        lines.append("├── web_ui.py                   # Streamlit Web UI")
        lines.append("├── api_server.py               # FastAPI 后端 + React 前端服务")
        lines.append("├── requirements.txt            # Python 依赖")
        lines.append("│")
        lines.append("├── app/")
        lines.append("│   ├── agents/")
        lines.append("│   │   ├── Planner.py          # 规划师：需求理解 + 计划生成")
        lines.append("│   │   ├── Executor.py         # 执行者：任务执行 + 文件修改")
        lines.append("│   │   ├── Reviewer.py         # 审查员：报错分析 + 诊断报告")
        lines.append("│   │   └── Sandbox.py          # 沙盒：Docker 隔离测试")
        lines.append("│   │")
        lines.append("│   ├── core/")
        lines.append("│   │   ├── config.py           # 全局配置 & 路径解析")
        lines.append("│   │   ├── context_manager.py  # 分层上下文管理 v2.0")
        lines.append("│   │   ├── state.py            # AgentState 定义 + InMemorySaver")
        lines.append("│   │   ├── llm_engine.py       # 多提供商 LLM 初始化 + 异步重试")
        lines.append("│   │   ├── logger.py           # 结构化日志")
        lines.append("│   │   ├── repo_map.py         # AST 仓库地图")
        lines.append("│   │   ├── routing.py          # 路由决策逻辑")
        lines.append("│   │   ├── recovery.py         # 熔断快照 & 错误恢复")
        lines.append("│   │   ├── metrics.py          # 可观测性指标收集器")
        lines.append("│   │   ├── language_support.py # 多语言支持")
        lines.append("│   │   ├── git_integration.py  # Git 集成")
        lines.append("│   │   ├── code_quality.py     # 代码质量分析")
        lines.append("│   │   └── documentation.py    # 文档自动生成")
        lines.append("│   │")
        lines.append("│   └── tools/")
        lines.append("│       └── file_tools.py       # 8 个文件工具 (read/edit/write/...)")
        lines.append("│")
        lines.append("├── frontend/                   # React 前端")
        lines.append("├── tests/                      # 单元测试")
        lines.append("├── docs/                       # 自动生成的文档")
        lines.append("└── workspace/                  # Agent 工作区")
        lines.append("```")
        lines.append("")
        lines.append("## 技术亮点")
        lines.append("")
        lines.append("### AST 感知文件操作")
        lines.append("")
        lines.append("- 大文件 (>5000 字符) 返回 AST 结构大纲而非原始内容")
        lines.append("- `read_function` / `read_class` / `read_file_range` 精确定位")
        lines.append("- `edit_file` 三级匹配：精确 → 去空匹配 → difflib 模糊匹配 (90% 阈值)")
        lines.append("- 每次修改自动备份，支持一键回滚")
        lines.append("")
        lines.append("### LLM 智能记忆压缩")
        lines.append("")
        lines.append("旧对话经过 LLM（或基于规则的 fallback）压缩为四段式摘要：")
        lines.append("")
        lines.append("1. 【用户需求】一句话概括原始需求")
        lines.append("2. 【已完成的修改】列出所有文件改动")
        lines.append("3. 【遇到的问题】列出遇到的错误和修复尝试")
        lines.append("4. 【待解决】当前仍未解决的问题")
        lines.append("")
        lines.append("### 代码质量分析")
        lines.append("")
        lines.append("- 支持多种语言的静态代码分析")
        lines.append("- 自动检测潜在问题和代码风格问题")
        lines.append("- 生成详细的代码质量报告")
        lines.append("")
        lines.append("### 文档自动生成")
        lines.append("")
        lines.append("- 自动生成项目 README 和技术文档")
        lines.append("- 提取代码注释生成 API 文档")
        lines.append("- 支持多种文档格式")
        lines.append("")
        lines.append("## 依赖项")
        lines.append("")
        lines.append("| 依赖 | 用途 |")
        lines.append("|------|------|")
        lines.append("| langgraph | 状态机 / Agent 编排 |")
        lines.append("| langchain-core | LLM 消息 / 工具调用抽象 |")
        lines.append("| langchain-openai / anthropic / ollama | LLM 提供商适配器 |")
        lines.append("| pydantic v2 | 结构化输出解析 |")
        lines.append("| tiktoken | 精确 Token 计数 |")
        lines.append("| docker | 沙盒容器引擎 |")
        lines.append("| streamlit | Web UI 框架 |")
        lines.append("| python-dotenv | 环境变量管理 |")
        lines.append("| flake8 | Python 代码质量分析 |")
        lines.append("| eslint | JavaScript/TypeScript 代码质量分析 |")
        lines.append("")
        lines.append("## 开源协议")
        lines.append("")
        lines.append("MIT License")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("Made by [xueqiangzhao009-cloud](https://github.com/xueqiangzhao009-cloud)")
        
        return "\n".join(lines)

    def _generate_api_docs(self) -> str:
        """
        生成 API 文档
        """
        lines = []
        lines.append("# API 文档")
        lines.append("")
        lines.append("## 工作流 API")
        lines.append("")
        lines.append("| 接口 | 说明 |")
        lines.append("|------|------|")
        lines.append("| POST /api/run | 启动工作流 |")
        lines.append("| GET /api/run/{thread_id}/events | SSE 事件流 |")
        lines.append("| GET /api/run/{thread_id}/state | 获取最终状态 |")
        lines.append("| GET /api/files | 工作区文件列表 |")
        lines.append("| GET /api/metrics | 指标数据 |")
        lines.append("| GET /api/config | 配置信息 |")
        lines.append("")
        lines.append("## 核心模块 API")
        lines.append("")
        
        # 提取核心模块的 API
        core_dir = os.path.join(self.project_root, "app", "core")
        for file in os.listdir(core_dir):
            if file.endswith(".py") and not file.startswith("__init__"):
                module_name = file[:-3]
                lines.append(f"### {module_name}")
                lines.append("")
                file_path = os.path.join(core_dir, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # 提取函数和类
                        functions = re.findall(r'def\s+(\w+)\s*\([^)]*\)\s*:', content)
                        classes = re.findall(r'class\s+(\w+)\s*\(?[^)]*\)?\s*:', content)
                        
                        if classes:
                            lines.append("#### 类")
                            for cls in classes:
                                lines.append(f"- `{cls}`")
                            lines.append("")
                        
                        if functions:
                            lines.append("#### 函数")
                            for func in functions:
                                lines.append(f"- `{func}()`")
                            lines.append("")
                except Exception as e:
                    logger.error(f"读取模块文件失败 {file_path}: {e}")
        
        return "\n".join(lines)

    def _generate_architecture_docs(self) -> str:
        """
        生成技术架构文档
        """
        lines = []
        lines.append("# 技术架构文档")
        lines.append("")
        lines.append("## 系统架构")
        lines.append("")
        lines.append("### 工作流图")
        lines.append("")
        lines.append("```mermaid")
        lines.append("flowchart TD")
        lines.append("    START((开始)) --> planner[Planner]")
        lines.append("    planner -- 工具调用 --> planner_tools[Planner Tools]")
        lines.append("    planner_tools --> planner")
        lines.append("    planner -- 无调用 --> executor[Executor]")
        lines.append("    executor -- 工具调用 --> step_counter[Step Counter]")
        lines.append("    step_counter --> executor_tools[Executor Tools]")
        lines.append("    executor_tools --> executor")
        lines.append("    executor -- 无调用 --> sandbox[Sandbox]")
        lines.append("    sandbox -- 通过 --> END_NODE(结束)")
        lines.append("    sandbox -- 失败 --> reviewer[Reviewer]")
        lines.append("    reviewer --> executor")
        lines.append("    sandbox -- 超限 --> END_NODE")
        lines.append("```")
        lines.append("")
        lines.append("### 路由决策")
        lines.append("")
        lines.append("| 路由 | 条件 | 下一节点 |")
        lines.append("|------|------|----------|")
        lines.append("| `route_after_planner` | 有 tool_calls | `planner_tools` |")
        lines.append("| `route_after_planner` | 无 tool_calls | `executor` |")
        lines.append("| `route_after_planner` | tool_calls ≥ MAX_PLANNER_STEPS | `executor` (强制结束探索) |")
        lines.append("| `route_after_executor` | 有 tool_calls | `executor_step_counter` → `executor_tools` |")
        lines.append("| `route_after_executor` | 无 tool_calls 或达到步数上限 | `sandbox` |")
        lines.append("| `route_after_sandbox` | 无 error_trace | `END` |")
        lines.append("| `route_after_sandbox` | 有 error 且 retry < max | `reviewer` → `executor` |")
        lines.append("| `route_after_sandbox` | retry ≥ max | 保存快照 → `END` |")
        lines.append("")
        lines.append("## 核心模块")
        lines.append("")
        lines.append("### 状态管理 (state.py)")
        lines.append("- AgentState 作为全局黑板，存储所有 Agent 共享的状态")
        lines.append("- 包含消息历史、工程上下文、沙盒控制、分层上下文等信息")
        lines.append("")
        lines.append("### 上下文管理 (context_manager.py)")
        lines.append("- 分层记忆策略：核心记忆、工作记忆、参考记忆")
        lines.append("- 动态上下文窗口管理，根据 Token 使用情况自动调整")
        lines.append("- LLM 智能记忆压缩，减少 Token 消耗")
        lines.append("")
        lines.append("### 工作流编排 (run.py)")
        lines.append("- 基于 LangGraph 的状态机设计")
        lines.append("- 注册和编排各个 Agent 节点")
        lines.append("- 处理路由逻辑和状态转换")
        lines.append("")
        lines.append("### 文件工具 (file_tools.py)")
        lines.append("- AST 感知的文件操作")
        lines.append("- 支持读取、编辑、写入文件")
        lines.append("- 大文件返回 AST 结构大纲")
        lines.append("")
        lines.append("### 代码质量分析 (code_quality.py)")
        lines.append("- 支持多种语言的静态代码分析")
        lines.append("- 自动检测潜在问题和代码风格问题")
        lines.append("- 生成详细的代码质量报告")
        lines.append("")
        lines.append("### 文档自动生成 (documentation.py)")
        lines.append("- 自动生成项目 README 和技术文档")
        lines.append("- 提取代码注释生成 API 文档")
        lines.append("- 支持多种文档格式")
        lines.append("")
        lines.append("## 技术栈")
        lines.append("")
        lines.append("- **后端**: Python 3.10+, LangGraph, FastAPI")
        lines.append("- **前端**: React 18, TypeScript, Vite")
        lines.append("- **沙盒**: Docker")
        lines.append("- **LLM**: 支持 OpenAI、Anthropic、Ollama、DeepSeek")
        lines.append("- **代码质量**: flake8, eslint")
        lines.append("- **文档**: Markdown")
        
        return "\n".join(lines)

    def _generate_code_docs(self) -> str:
        """
        生成代码文档
        """
        lines = []
        lines.append("# 代码文档")
        lines.append("")
        
        # 遍历 app 目录
        src_dir = os.path.join(self.project_root, "app")
        for root, dirs, files in os.walk(src_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_root)
                    lines.append(f"## {rel_path}")
                    lines.append("")
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                            # 提取模块文档
                            module_doc = re.search(r'"""(.*?)"""', content, re.DOTALL)
                            if module_doc:
                                lines.append("### 模块文档")
                                lines.append(module_doc.group(1).strip())
                                lines.append("")
                            
                            # 提取类
                            class_pattern = r'class\s+(\w+)\s*\(?[^)]*\)?\s*:\s*"""(.*?)"""'
                            for match in re.finditer(class_pattern, content, re.DOTALL):
                                class_name, class_doc = match.groups()
                                lines.append(f"### 类: {class_name}")
                                lines.append(class_doc.strip())
                                lines.append("")
                            
                            # 提取函数
                            func_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:\s*"""(.*?)"""'
                            for match in re.finditer(func_pattern, content, re.DOTALL):
                                func_name, func_doc = match.groups()
                                lines.append(f"### 函数: {func_name}()")
                                lines.append(func_doc.strip())
                                lines.append("")
                    except Exception as e:
                        logger.error(f"读取代码文件失败 {file_path}: {e}")
                    
                    lines.append("---")
                    lines.append("")
        
        return "\n".join(lines)

    def generate_code_comments(self, file_path: str) -> List[DocComment]:
        """
        提取代码文件中的文档注释

        Args:
            file_path: 文件路径

        Returns:
            文档注释列表
        """
        comments = []
        language = detect_language(file_path)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
                if language == Language.PYTHON:
                    comments.extend(self._extract_python_comments(lines))
                elif language in [Language.JAVASCRIPT, Language.TYPESCRIPT]:
                    comments.extend(self._extract_javascript_comments(lines))
                elif language == Language.GO:
                    comments.extend(self._extract_go_comments(lines))
                elif language == Language.RUST:
                    comments.extend(self._extract_rust_comments(lines))
        except Exception as e:
            logger.error(f"提取文档注释失败 {file_path}: {e}")
        
        return comments

    def _extract_python_comments(self, lines: List[str]) -> List[DocComment]:
        """
        提取 Python 文件中的文档注释
        """
        comments = []
        in_docstring = False
        doc_start = 0
        doc_content = []
        
        for i, line in enumerate(lines):
            if '"""' in line or "''""''" in line:
                if not in_docstring:
                    in_docstring = True
                    doc_start = i + 1
                    doc_content = [line]
                else:
                    in_docstring = False
                    doc_content.append(line)
                    
                    # 确定注释类型
                    comment_type = "module"
                    # 检查前一行是否是 class 或 def
                    for j in range(doc_start - 2, max(0, doc_start - 5), -1):
                        prev_line = lines[j].strip()
                        if prev_line.startswith("class "):
                            comment_type = "class"
                            break
                        elif prev_line.startswith("def "):
                            comment_type = "function"
                            break
                    
                    comments.append(DocComment(
                        content="".join(doc_content),
                        line_start=doc_start,
                        line_end=i + 1,
                        type=comment_type
                    ))
            elif in_docstring:
                doc_content.append(line)
        
        return comments

    def _extract_javascript_comments(self, lines: List[str]) -> List[DocComment]:
        """
        提取 JavaScript/TypeScript 文件中的文档注释
        """
        comments = []
        in_doccomment = False
        doc_start = 0
        doc_content = []
        
        for i, line in enumerate(lines):
            if '/**' in line:
                in_doccomment = True
                doc_start = i + 1
                doc_content = [line]
            elif '*/' in line and in_doccomment:
                in_doccomment = False
                doc_content.append(line)
                
                # 确定注释类型
                comment_type = "module"
                # 检查后一行是否是 class 或 function
                for j in range(i + 1, min(len(lines), i + 3)):
                    next_line = lines[j].strip()
                    if next_line.startswith("class "):
                        comment_type = "class"
                        break
                    elif next_line.startswith("function ") or next_line.startswith("const ") and "=>" in next_line:
                        comment_type = "function"
                        break
                
                comments.append(DocComment(
                    content="".join(doc_content),
                    line_start=doc_start,
                    line_end=i + 1,
                    type=comment_type
                ))
            elif in_doccomment:
                doc_content.append(line)
        
        return comments

    def _extract_go_comments(self, lines: List[str]) -> List[DocComment]:
        """
        提取 Go 文件中的文档注释
        """
        comments = []
        doc_content = []
        doc_start = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("//"):
                if not doc_content:
                    doc_start = i + 1
                doc_content.append(line)
            else:
                if doc_content:
                    # 确定注释类型
                    comment_type = "module"
                    if stripped.startswith("type ") and "struct" in stripped:
                        comment_type = "class"
                    elif stripped.startswith("func "):
                        comment_type = "function"
                    
                    comments.append(DocComment(
                        content="".join(doc_content),
                        line_start=doc_start,
                        line_end=i,
                        type=comment_type
                    ))
                    doc_content = []
        
        return comments

    def _extract_rust_comments(self, lines: List[str]) -> List[DocComment]:
        """
        提取 Rust 文件中的文档注释
        """
        comments = []
        in_doccomment = False
        doc_start = 0
        doc_content = []
        
        for i, line in enumerate(lines):
            if '///' in line:
                if not in_doccomment:
                    in_doccomment = True
                    doc_start = i + 1
                    doc_content = [line]
                else:
                    doc_content.append(line)
            elif '//!' in line:
                # 模块级文档
                comments.append(DocComment(
                    content=line,
                    line_start=i + 1,
                    line_end=i + 1,
                    type="module"
                ))
            else:
                if in_doccomment:
                    in_doccomment = False
                    
                    # 确定注释类型
                    comment_type = "module"
                    # 检查后一行
                    for j in range(i, min(len(lines), i + 2)):
                        next_line = lines[j].strip()
                        if next_line.startswith("struct ") or next_line.startswith("enum "):
                            comment_type = "class"
                            break
                        elif next_line.startswith("fn "):
                            comment_type = "function"
                            break
                    
                    comments.append(DocComment(
                        content="".join(doc_content),
                        line_start=doc_start,
                        line_end=i,
                        type=comment_type
                    ))
                    doc_content = []
        
        return comments


def generate_documentation(project_root: str, output_dir: Optional[str] = None) -> Dict[str, str]:
    """
    生成项目文档的便捷函数

    Args:
        project_root: 项目根目录
        output_dir: 输出目录（可选）

    Returns:
        生成的文档文件路径和内容的字典
    """
    generator = DocumentationGenerator(project_root)
    return generator.generate_project_docs(output_dir)


def extract_code_comments(file_path: str) -> List[DocComment]:
    """
    提取代码文件中的文档注释的便捷函数

    Args:
        file_path: 文件路径

    Returns:
        文档注释列表
    """
    generator = DocumentationGenerator(os.path.dirname(file_path))
    return generator.generate_code_comments(file_path)


# 导出主要符号
__all__ = [
    'DocComment',
    'DocumentationGenerator',
    'generate_documentation',
    'extract_code_comments'
]
