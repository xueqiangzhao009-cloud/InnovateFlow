"""
Executor Agent - 执行者节点
负责执行任务与文件修改
"""

import logging
from langchain_core.messages import SystemMessage, ToolMessage

from app.core.repo_analyzer import generate_repo_map
from app.core.state_manager import AgentState
from app.core.llm_handler import llm
from app.core.context_handler import (
    build_executor_context,
    estimate_messages_tokens,
    update_memory_summary,
)
from app.core.metrics_collector import metrics
from app.tools.file_operations import tools

logger = logging.getLogger(__name__)


def _check_all_tasks_completed(state: AgentState) -> bool:
    """
    检查 Executor 是否已经完成了所有计划中的任务。
    通过分析历史消息中的工具调用和工具结果来判断。

    返回 True 表示所有已知任务均已完成，无需再调用工具。
    """
    import re
    plan = state.get("current_plan", "")
    messages = state.get("messages", [])

    # 从计划中提取目标文件
    files_section = re.search(r'【目标文件】\s*(.*?)(?:$|【)', plan, re.DOTALL)
    target_files = []
    if files_section:
        files_text = files_section.group(1).strip()
        target_files = [f.strip().strip('`,-*') for f in re.split(r'[\n,，\s]+', files_text) if f.strip()]
        target_files = [f for f in target_files if not f.startswith('【')]

    if not target_files:
        return False  # 没有目标文件信息时不干预

    # 从历史 ToolMessage 中收集已成功操作的文件
    completed_files = set()
    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name in ("write_file", "edit_file"):
            content = msg.content if hasattr(msg, 'content') else ""
            if any(kw in content for kw in ["Successfully created", "成功修改", "成功"]):
                # 通过 tool_call_id 回溯找到对应的 AIMessage
                for prev_msg in messages:
                    if hasattr(prev_msg, 'tool_calls') and prev_msg.tool_calls:
                        for tc in prev_msg.tool_calls:
                            if tc.get('id') == msg.tool_call_id:
                                fname = tc.get('args', {}).get('filename', '')
                                if fname in target_files:
                                    completed_files.add(fname)

    # 如果所有目标文件都已被操作过，认为任务完成
    return all(tf in completed_files for tf in target_files)


async def executor_node(state: AgentState):
    """
    Executor 节点执行函数（异步）。
    根据当前计划和报错信息，执行任务或修改文件。

    Returns:
        dict: 更新的状态，包含 LLM 响应和记忆摘要
    """
    logger.info("正在执行任务与文件修改...")
    executor_llm = llm.bind_tools(tools)

    # 🌟 使用上下文管理器构建优化上下文 (传递 LLM 实例支持智能摘要)
    workspace_map = generate_repo_map()
    filtered_messages = build_executor_context(state, workspace_map, llm=llm)

    # 🌟 Token 监控 (使用 tiktoken 精确计数)
    token_count = estimate_messages_tokens(filtered_messages)
    logger.debug(f"上下文 Token 估算: ~{token_count} tokens")

    # 🌟 更新记忆摘要
    current_summary = state.get("memory_summary")
    new_messages = state.get("messages", [])
    updated_summary = update_memory_summary(current_summary, new_messages)

    # 🌟 检查是否所有计划任务已完成，如果已完成则强制停止工具调用循环
    executor_step_count = state.get("executor_step_count", 0)
    if executor_step_count >= 3 and _check_all_tasks_completed(state):
        logger.info("[Executor] 检测到所有计划任务已完成，强制结束工具调用循环")
        content = "我已完成计划中的所有步骤，所有目标文件均已创建/修改完毕。"
        return {
            "messages": [SystemMessage(content=content)],
            "memory_summary": updated_summary,
            "modification_log": state.get("modification_log", []) + [content],
        }

    # 传入优化后的上下文
    start = metrics.record_llm_call_start()

    try:
        response = await executor_llm.ainvoke(filtered_messages)
    except Exception as e:
        logger.error(f"Executor LLM 调用失败: {e}")
        metrics.record_llm_call_end(start, tokens_used=token_count, node_name="Executor")
        raise RuntimeError(f"Executor 节点 LLM 调用失败（已重试），图执行终止: {e}") from e

    metrics.record_llm_call_end(start, tokens_used=token_count, node_name="Executor")

    if getattr(response, 'tool_calls', []):
        tool_names = [t['name'] for t in response.tool_calls]
        logger.info(f"调用工具执行操作: {tool_names}")

    # 记录本次 Executor 调用的具体工具意图到 modification_log
    modification_log = state.get("modification_log", [])
    if getattr(response, 'tool_calls', []):
        for tc in response.tool_calls:
            tool_name = tc['name']
            tool_args = tc.get('args', {})
            target = tool_args.get('filename', '未知')
            entry = f"{tool_name} -> {target}"
            modification_log.append(entry)
    else:
        content_preview = response.content[:100] if response.content else "(空)"
        modification_log.append(f"Executor 输出: {content_preview}")

    return {
        "messages": [response],
        "memory_summary": updated_summary,
        "modification_log": modification_log,
    }
