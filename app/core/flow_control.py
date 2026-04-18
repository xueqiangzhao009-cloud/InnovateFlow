"""
路由控制模块 - 封装 LangGraph 图的节点间路由决策逻辑。
将其从 run.py 中抽取出来，使得路由逻辑可以被独立测试。
"""

from app.core.settings import MAX_EXECUTOR_STEPS, MAX_PLANNER_STEPS
from app.core.state_manager import AgentState


def route_after_planner(state: AgentState):
    """判断 Planner 是在探索工具，还是做好了计划"""
    last_message = state["messages"][-1]
    has_tool_calls = getattr(last_message, 'tool_calls', [])
    if not has_tool_calls:
        return "executor"

    # 防止 Planner 无限探索
    planner_step_count = sum(1 for msg in state.get("messages", [])
                             if getattr(msg, 'name', None) == "Planner" and getattr(msg, 'tool_calls', []))
    if planner_step_count >= MAX_PLANNER_STEPS:
        return "executor"
    return "planner_tools"


def route_after_executor(state: AgentState):
    """判断 Executor 是在执行任务/看文件，还是全部完工了"""
    from app.core.logging import logger

    executor_step_count = state.get("executor_step_count", 0)
    max_executor_steps = state.get("max_executor_steps", MAX_EXECUTOR_STEPS)
    last_message = state["messages"][-1]

    # 检查是否达到最大步数
    if executor_step_count >= max_executor_steps:
        logger.warning(f"[Router] Executor 已达到最大步数限制 ({max_executor_steps})，强制进入沙盒测试")
        return "sandbox"

    if getattr(last_message, 'tool_calls', []):
        return "executor_step_counter"  # 先去计数器节点

    logger.info("[Router] Executor 认为执行已完成。移交沙盒测试...")
    return "sandbox"  # 没调用工具说明任务执行完了，去测试
