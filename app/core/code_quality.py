"""
InnovateFlow 代码质量分析模块

提供代码质量分析功能：
- 静态代码分析
- 代码风格检查
- 潜在问题检测
- 代码质量报告生成
"""

import os
import subprocess
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from app.core.logger import setup_logger
from app.core.language_support import Language, detect_language

logger = setup_logger("InnovateFlow.code_quality")


@dataclass
class CodeQualityIssue:
    """代码质量问题"""
    severity: str  # error, warning, info
    message: str
    file_path: str
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None


class CodeQualityAnalyzer:
    """
    代码质量分析器
    """

    def __init__(self, project_root: str):
        """
        初始化代码质量分析器

        Args:
            project_root: 项目根目录
        """
        self.project_root = project_root

    def analyze(self, file_paths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        分析代码质量

        Args:
            file_paths: 要分析的文件路径列表（可选）

        Returns:
            代码质量分析结果
        """
        if not file_paths:
            # 分析整个项目
            file_paths = self._get_all_source_files()

        results = {
            "total_files": len(file_paths),
            "issues": [],
            "summary": {
                "errors": 0,
                "warnings": 0,
                "infos": 0
            }
        }

        for file_path in file_paths:
            language = detect_language(file_path)
            if language == Language.UNKNOWN:
                continue

            file_issues = self._analyze_file(file_path, language)
            results["issues"].extend(file_issues)

            # 更新摘要
            for issue in file_issues:
                if issue.severity == "error":
                    results["summary"]["errors"] += 1
                elif issue.severity == "warning":
                    results["summary"]["warnings"] += 1
                elif issue.severity == "info":
                    results["summary"]["infos"] += 1

        return results

    def _get_all_source_files(self) -> List[str]:
        """
        获取项目中的所有源文件

        Returns:
            源文件路径列表
        """
        source_files = []
        extensions = {
            Language.PYTHON: [".py"],
            Language.JAVASCRIPT: [".js", ".mjs", ".cjs"],
            Language.TYPESCRIPT: [".ts", ".tsx"],
            Language.JAVA: [".java"],
            Language.GO: [".go"],
            Language.RUST: [".rs"]
        }

        for root, dirs, files in os.walk(self.project_root):
            # 跳过隐藏目录和常见忽略目录
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in [
                'node_modules', 'vendor', 'target', '__pycache__', 'dist', 'build'
            ]]

            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                for lang, exts in extensions.items():
                    if ext in exts:
                        source_files.append(file_path)
                        break

        return source_files

    def _analyze_file(self, file_path: str, language: Language) -> List[CodeQualityIssue]:
        """
        分析单个文件的代码质量

        Args:
            file_path: 文件路径
            language: 编程语言

        Returns:
            代码质量问题列表
        """
        issues = []

        if language == Language.PYTHON:
            issues.extend(self._analyze_python_file(file_path))
        elif language in [Language.JAVASCRIPT, Language.TYPESCRIPT]:
            issues.extend(self._analyze_javascript_file(file_path))
        elif language == Language.GO:
            issues.extend(self._analyze_go_file(file_path))
        elif language == Language.RUST:
            issues.extend(self._analyze_rust_file(file_path))

        return issues

    def _analyze_python_file(self, file_path: str) -> List[CodeQualityIssue]:
        """
        分析 Python 文件
        """
        issues = []

        try:
            # 尝试使用 flake8 进行分析
            result = subprocess.run(
                ["flake8", file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue

                    # 解析 flake8 输出格式: file:line:column: code message
                    parts = line.split(':', 4)
                    if len(parts) >= 5:
                        file, line_num, col, code, message = parts
                        issues.append(CodeQualityIssue(
                            severity="error" if code.startswith('E') else "warning",
                            message=message.strip(),
                            file_path=file_path,
                            line=int(line_num),
                            column=int(col),
                            code=code
                        ))

        except (subprocess.SubprocessError, FileNotFoundError):
            # flake8 未安装，跳过
            pass

        return issues

    def _analyze_javascript_file(self, file_path: str) -> List[CodeQualityIssue]:
        """
        分析 JavaScript/TypeScript 文件
        """
        issues = []

        try:
            # 尝试使用 eslint 进行分析
            result = subprocess.run(
                ["npx", "eslint", file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                for line in result.stdout.strip().split('\n'):
                    if not line or ':' not in line:
                        continue

                    # 解析 eslint 输出格式
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        file, line_num, col, message = parts
                        # 提取错误代码
                        code_match = message.split('[', 1)
                        code = code_match[1].split(']')[0] if len(code_match) > 1 else None
                        issues.append(CodeQualityIssue(
                            severity="error",
                            message=message.strip(),
                            file_path=file_path,
                            line=int(line_num),
                            column=int(col),
                            code=code
                        ))

        except (subprocess.SubprocessError, FileNotFoundError):
            # eslint 未安装，跳过
            pass

        return issues

    def _analyze_go_file(self, file_path: str) -> List[CodeQualityIssue]:
        """
        分析 Go 文件
        """
        issues = []

        try:
            # 尝试使用 go vet 进行分析
            result = subprocess.run(
                ["go", "vet", file_path],
                cwd=os.path.dirname(file_path) or self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue

                    # 解析 go vet 输出格式
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        file, rest = parts[0], ':'.join(parts[1:])
                        line_col, message = rest.split(':', 1)
                        line_num = line_col.split(',')[0]
                        issues.append(CodeQualityIssue(
                            severity="error",
                            message=message.strip(),
                            file_path=file_path,
                            line=int(line_num)
                        ))

        except (subprocess.SubprocessError, FileNotFoundError):
            # go vet 未安装，跳过
            pass

        return issues

    def _analyze_rust_file(self, file_path: str) -> List[CodeQualityIssue]:
        """
        分析 Rust 文件
        """
        issues = []

        try:
            # 尝试使用 cargo check 进行分析
            result = subprocess.run(
                ["cargo", "check"],
                cwd=os.path.dirname(file_path) or self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                for line in result.stderr.strip().split('\n'):
                    if not line or 'error:' not in line and 'warning:' not in line:
                        continue

                    # 解析 cargo check 输出格式
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        file, rest = parts[0], ':'.join(parts[1:])
                        line_col, message = rest.split(':', 1)
                        line_num = line_col.split(',')[0]
                        severity = "error" if 'error:' in message else "warning"
                        issues.append(CodeQualityIssue(
                            severity=severity,
                            message=message.strip(),
                            file_path=file_path,
                            line=int(line_num)
                        ))

        except (subprocess.SubprocessError, FileNotFoundError):
            # cargo 未安装，跳过
            pass

        return issues

    def generate_report(self, analysis_results: Dict[str, Any], output_format: str = "json") -> str:
        """
        生成代码质量报告

        Args:
            analysis_results: 分析结果
            output_format: 输出格式 (json, text)

        Returns:
            报告内容
        """
        if output_format == "json":
            return json.dumps(analysis_results, indent=2, ensure_ascii=False)
        elif output_format == "text":
            lines = []
            lines.append("Code Quality Analysis Report")
            lines.append("=" * 50)
            lines.append(f"Total files analyzed: {analysis_results['total_files']}")
            lines.append(f"Errors: {analysis_results['summary']['errors']}")
            lines.append(f"Warnings: {analysis_results['summary']['warnings']}")
            lines.append(f"Infos: {analysis_results['summary']['infos']}")
            lines.append("" if not analysis_results['issues'] else "\nIssues:")

            for issue in analysis_results['issues']:
                line_info = f":{issue.line}:{issue.column}" if issue.line else ""
                code_info = f" [{issue.code}]" if issue.code else ""
                lines.append(f"{issue.severity.upper()}{line_info}{code_info}: {issue.message}")
                lines.append(f"  File: {issue.file_path}")

            return "\n".join(lines)
        else:
            return "Unsupported output format"


def analyze_code_quality(file_paths: Optional[List[str]] = None, project_root: Optional[str] = None) -> Dict[str, Any]:
    """
    分析代码质量的便捷函数

    Args:
        file_paths: 要分析的文件路径列表（可选）
        project_root: 项目根目录（可选）

    Returns:
        代码质量分析结果
    """
    from app.core.config import PROJECT_ROOT as DEFAULT_PROJECT_ROOT
    
    if not project_root:
        project_root = DEFAULT_PROJECT_ROOT
    
    analyzer = CodeQualityAnalyzer(project_root)
    return analyzer.analyze(file_paths)


def generate_code_quality_report(analysis_results: Dict[str, Any], output_format: str = "json") -> str:
    """
    生成代码质量报告的便捷函数

    Args:
        analysis_results: 分析结果
        output_format: 输出格式 (json, text)

    Returns:
        报告内容
    """
    analyzer = CodeQualityAnalyzer("")
    return analyzer.generate_report(analysis_results, output_format)


# 导出主要符号
__all__ = [
    'CodeQualityIssue',
    'CodeQualityAnalyzer',
    'analyze_code_quality',
    'generate_code_quality_report'
]
