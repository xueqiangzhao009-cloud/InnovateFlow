"""
InnovateFlow 核心模块
"""

from .settings import *
from .context_handler import *
from .state_manager import *
from .llm_handler import *
from .logging import *
from .repo_analyzer import *
from .flow_control import *
from .fault_recovery import *
from .metrics_collector import *
from .lang_support import *
from .git_handler import *
from .quality_analyzer import *
from .doc_generator import *

__all__ = [
    # settings
    'PROJECT_ROOT',
    'WORKSPACE_DIR',
    'SANDBOX_IMAGE',
    'SANDBOX_MEM_LIMIT',
    'SANDBOX_TIMEOUT_SECONDS',
    'LARGE_FILE_THRESHOLD',
    'FUZZY_MATCH_THRESHOLD',
    'MAX_FUZZY_MATCH_LINES',
    'MAX_EXECUTOR_STEPS',
    'MAX_PLANNER_STEPS',
    
    # context_handler
    'estimate_token_count',
    'estimate_messages_tokens',
    'extract_original_request',
    'extract_file_signatures',
    'filter_orphan_tool_messages',
    'compress_tool_messages',
    'build_edit_summary',
    'summarize_conversation',
    'calculate_dynamic_window',
    'ContextSlot',
    'build_context_with_priority',
    'build_executor_context',
    'build_planner_context',
    'build_reviewer_context',
    'update_memory_summary',
    
    # state_manager
    'AgentState',
    'checkpointer',
    
    # llm_handler
    'get_llm',
    'get_chat_model',
    
    # logging
    'setup_logger',
    
    # repo_analyzer
    'build_repo_map',
    
    # flow_control
    'route_after_planner',
    'route_after_executor',
    
    # fault_recovery
    'create_workspace_snapshot',
    
    # metrics_collector
    'metrics',
    
    # lang_support
    'Language',
    'LanguageConfig',
    'LANGUAGE_CONFIGS',
    'detect_language',
    'get_language_config',
    'find_test_files',
    'install_dependencies',
    'get_test_command',
    'ASTParser',
    'create_ast_parser',
    
    # git_handler
    'GitCommit',
    'GitDiff',
    'GitRepository',
    'CommitMessageGenerator',
    'create_feature_branch',
    'auto_commit',
    'get_change_summary',
    
    # quality_analyzer
    'CodeQualityIssue',
    'CodeQualityAnalyzer',
    'analyze_code_quality',
    'generate_code_quality_report',
    
    # doc_generator
    'DocComment',
    'DocumentationGenerator',
    'generate_documentation',
    'extract_code_comments'
]
