"""
InnovateFlow 多语言支持模块

支持多种编程语言的AST解析和测试框架适配。
支持语言：Python, JavaScript/TypeScript, Java, Go, Rust, C, C++, PHP, Ruby
"""

import os
import subprocess
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from enum import Enum

from app.core.logger import setup_logger

logger = setup_logger("InnovateFlow.language_support")


class Language(Enum):
    """支持的编程语言枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    C = "c"
    CPP = "cpp"
    PHP = "php"
    RUBY = "ruby"
    UNKNOWN = "unknown"


@dataclass
class LanguageConfig:
    """语言配置"""
    name: str
    extensions: List[str]
    test_patterns: List[str]
    test_frameworks: List[str]
    package_manager: str
    build_command: Optional[str]
    run_command: str


# 语言配置映射
LANGUAGE_CONFIGS: Dict[Language, LanguageConfig] = {
    Language.PYTHON: LanguageConfig(
        name="Python",
        extensions=[".py"],
        test_patterns=["test_*.py", "*_test.py"],
        test_frameworks=["pytest", "unittest"],
        package_manager="pip",
        build_command=None,
        run_command="python {file}"
    ),
    Language.JAVASCRIPT: LanguageConfig(
        name="JavaScript",
        extensions=[".js", ".mjs", ".cjs"],
        test_patterns=["*.test.js", "*.spec.js", "__tests__/*.js"],
        test_frameworks=["jest", "mocha", "vitest"],
        package_manager="npm",
        build_command=None,
        run_command="node {file}"
    ),
    Language.TYPESCRIPT: LanguageConfig(
        name="TypeScript",
        extensions=[".ts", ".tsx", ".mts", ".cts"],
        test_patterns=["*.test.ts", "*.spec.ts", "__tests__/*.ts"],
        test_frameworks=["jest", "vitest", "mocha"],
        package_manager="npm",
        build_command="tsc",
        run_command="npx tsx {file}"
    ),
    Language.JAVA: LanguageConfig(
        name="Java",
        extensions=[".java"],
        test_patterns=["*Test.java", "*Tests.java"],
        test_frameworks=["junit", "testng"],
        package_manager="maven",
        build_command="mvn compile",
        run_command="java {file}"
    ),
    Language.GO: LanguageConfig(
        name="Go",
        extensions=[".go"],
        test_patterns=["*_test.go"],
        test_frameworks=["testing"],
        package_manager="go",
        build_command="go build",
        run_command="go run {file}"
    ),
    Language.RUST: LanguageConfig(
        name="Rust",
        extensions=[".rs"],
        test_patterns=["*_test.rs", "tests/*.rs"],
        test_frameworks=["cargo-test"],
        package_manager="cargo",
        build_command="cargo build",
        run_command="cargo run"
    ),
    Language.C: LanguageConfig(
        name="C",
        extensions=[".c"],
        test_patterns=["*_test.c", "test_*.c"],
        test_frameworks=["ctest", "unity"],
        package_manager="make",
        build_command="gcc -o {output} {file}",
        run_command="./{output}"
    ),
    Language.CPP: LanguageConfig(
        name="C++",
        extensions=[".cpp", ".cc", ".cxx"],
        test_patterns=["*_test.cpp", "test_*.cpp", "*_test.cc", "test_*.cc"],
        test_frameworks=["gtest", "catch2", "doctest"],
        package_manager="make",
        build_command="g++ -o {output} {file}",
        run_command="./{output}"
    ),
    Language.PHP: LanguageConfig(
        name="PHP",
        extensions=[".php"],
        test_patterns=["*_test.php", "test_*.php", "tests/*.php"],
        test_frameworks=["phpunit"],
        package_manager="composer",
        build_command=None,
        run_command="php {file}"
    ),
    Language.RUBY: LanguageConfig(
        name="Ruby",
        extensions=[".rb"],
        test_patterns=["*_test.rb", "test_*.rb", "spec/*_spec.rb"],
        test_frameworks=["rspec", "minitest"],
        package_manager="gem",
        build_command=None,
        run_command="ruby {file}"
    ),
}


def detect_language(file_path: str) -> Language:
    """
    根据文件扩展名检测编程语言

    Args:
        file_path: 文件路径

    Returns:
        检测到的语言枚举
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    for lang, config in LANGUAGE_CONFIGS.items():
        if ext in config.extensions:
            return lang

    return Language.UNKNOWN


def get_language_config(language: Language) -> Optional[LanguageConfig]:
    """
    获取语言配置

    Args:
        language: 语言枚举

    Returns:
        语言配置对象，如果语言不支持则返回None
    """
    return LANGUAGE_CONFIGS.get(language)


def find_test_files(directory: str, language: Language) -> List[str]:
    """
    在指定目录中查找测试文件

    Args:
        directory: 要搜索的目录
        language: 目标语言

    Returns:
        找到的测试文件路径列表
    """
    config = get_language_config(language)
    if not config:
        logger.warning(f"不支持的语言: {language}")
        return []

    test_files = []

    for root, dirs, files in os.walk(directory):
        # 跳过隐藏目录和常见忽略目录
        dirs[:] = [d for d in dirs if not d.startswith(
            '.') and d not in ['node_modules', 'vendor', 'target', '__pycache__']]

        for file in files:
            file_path = os.path.join(root, file)

            # 检查文件是否匹配测试模式
            for pattern in config.test_patterns:
                import fnmatch
                if fnmatch.fnmatch(file, pattern):
                    test_files.append(file_path)
                    break

    logger.info(f"在 {language.value} 项目中找到 {len(test_files)} 个测试文件")
    return test_files


def install_dependencies(directory: str, language: Language) -> bool:
    """
    安装项目依赖

    Args:
        directory: 项目目录
        language: 编程语言

    Returns:
        是否安装成功
    """
    config = get_language_config(language)
    if not config:
        logger.warning(f"不支持的语言: {language}")
        return False

    try:
        if language == Language.PYTHON:
            requirements_file = os.path.join(directory, "requirements.txt")
            if os.path.exists(requirements_file):
                logger.info("安装 Python 依赖...")
                result = subprocess.run(
                    ["pip", "install", "-r", requirements_file],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    logger.error(f"Python 依赖安装失败: {result.stderr}")
                    return False
                logger.info("Python 依赖安装成功")
                return True

        elif language in [Language.JAVASCRIPT, Language.TYPESCRIPT]:
            package_json = os.path.join(directory, "package.json")
            if os.path.exists(package_json):
                logger.info("安装 Node.js 依赖...")
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    logger.error(f"Node.js 依赖安装失败: {result.stderr}")
                    return False
                logger.info("Node.js 依赖安装成功")
                return True

        elif language == Language.GO:
            go_mod = os.path.join(directory, "go.mod")
            if os.path.exists(go_mod):
                logger.info("下载 Go 依赖...")
                result = subprocess.run(
                    ["go", "mod", "download"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    logger.error(f"Go 依赖下载失败: {result.stderr}")
                    return False
                logger.info("Go 依赖下载成功")
                return True

        elif language == Language.RUST:
            cargo_toml = os.path.join(directory, "Cargo.toml")
            if os.path.exists(cargo_toml):
                logger.info("构建 Rust 项目...")
                result = subprocess.run(
                    ["cargo", "build"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=180
                )
                if result.returncode != 0:
                    logger.error(f"Rust 构建失败: {result.stderr}")
                    return False
                logger.info("Rust 构建成功")
                return True

        elif language in [Language.C, Language.CPP]:
            makefile = os.path.join(directory, "Makefile")
            if os.path.exists(makefile):
                logger.info("使用 Makefile 构建项目...")
                result = subprocess.run(
                    ["make"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    logger.error(f"构建失败: {result.stderr}")
                    return False
                logger.info("构建成功")
                return True

        elif language == Language.PHP:
            composer_json = os.path.join(directory, "composer.json")
            if os.path.exists(composer_json):
                logger.info("安装 PHP 依赖...")
                result = subprocess.run(
                    ["composer", "install"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    logger.error(f"PHP 依赖安装失败: {result.stderr}")
                    return False
                logger.info("PHP 依赖安装成功")
                return True

        elif language == Language.RUBY:
            gemfile = os.path.join(directory, "Gemfile")
            if os.path.exists(gemfile):
                logger.info("安装 Ruby 依赖...")
                result = subprocess.run(
                    ["bundle", "install"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    logger.error(f"Ruby 依赖安装失败: {result.stderr}")
                    return False
                logger.info("Ruby 依赖安装成功")
                return True

        # 没有找到依赖文件，认为是成功的
        logger.info(f"未找到 {language.value} 的依赖文件，跳过安装")
        return True

    except subprocess.TimeoutExpired:
        logger.error(f"依赖安装超时")
        return False
    except Exception as e:
        logger.error(f"依赖安装失败: {e}")
        return False


def get_test_command(language: Language, test_file: Optional[str] = None) -> Optional[str]:
    """
    获取测试运行命令

    Args:
        language: 编程语言
        test_file: 测试文件路径（可选）

    Returns:
        测试命令字符串
    """
    config = get_language_config(language)
    if not config:
        return None

    if language == Language.PYTHON:
        if test_file:
            return f"pytest {test_file} -v"
        return "pytest -v"

    elif language in [Language.JAVASCRIPT, Language.TYPESCRIPT]:
        # 检查 package.json 中的测试脚本
        return "npm test"

    elif language == Language.GO:
        if test_file:
            return f"go test -v {os.path.dirname(test_file)}"
        return "go test -v ./..."

    elif language == Language.RUST:
        return "cargo test"

    elif language == Language.JAVA:
        return "mvn test"

    elif language == Language.C:
        # 对于 C 语言，使用编译后的可执行文件
        if test_file:
            # 假设测试文件已经被编译成可执行文件
            executable = os.path.splitext(test_file)[0]
            return f"./{executable}"
        return None

    elif language == Language.CPP:
        # 对于 C++ 语言，使用编译后的可执行文件
        if test_file:
            # 假设测试文件已经被编译成可执行文件
            executable = os.path.splitext(test_file)[0]
            return f"./{executable}"
        return None

    elif language == Language.PHP:
        return "phpunit"

    elif language == Language.RUBY:
        # 检查是否使用 rspec 或 minitest
        return "rspec" if os.path.exists("spec") else "ruby -Ilib:test"

    return None


class ASTParser:
    """
    多语言AST解析器基类
    """

    def __init__(self, language: Language):
        self.language = language
        self.config = get_language_config(language)

    def parse(self, content: str) -> Dict[str, Any]:
        """
        解析源代码并返回AST结构

        Args:
            content: 源代码内容

        Returns:
            AST结构字典
        """
        if self.language == Language.PYTHON:
            return self._parse_python(content)
        elif self.language in [Language.JAVASCRIPT, Language.TYPESCRIPT]:
            return self._parse_javascript(content)
        elif self.language == Language.C:
            return self._parse_c(content)
        elif self.language == Language.CPP:
            return self._parse_cpp(content)
        elif self.language == Language.PHP:
            return self._parse_php(content)
        elif self.language == Language.RUBY:
            return self._parse_ruby(content)
        else:
            # 对于其他语言，返回基本信息
            return {
                "language": self.language.value,
                "lines": len(content.split('\n')),
                "functions": [],
                "classes": [],
                "imports": []
            }

    def _parse_python(self, content: str) -> Dict[str, Any]:
        """解析Python代码"""
        import ast

        try:
            tree = ast.parse(content)

            functions = []
            classes = []
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": node.end_lineno,
                        "args": [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": node.end_lineno,
                        "bases": [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases]
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            return {
                "language": "python",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "lines": len(content.split('\n'))
            }

        except SyntaxError as e:
            logger.error(f"Python AST 解析失败: {e}")
            return {
                "language": "python",
                "error": str(e),
                "lines": len(content.split('\n'))
            }

    def _parse_javascript(self, content: str) -> Dict[str, Any]:
        """
        解析JavaScript/TypeScript代码（简化版本）
        使用正则表达式提取基本信息
        """
        import re

        functions = []
        classes = []
        imports = []

        # 匹配函数声明
        func_pattern = r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(func_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                "name": match.group(1),
                "line": line_num,
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
            })

        # 匹配箭头函数
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>'
        for match in re.finditer(arrow_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                "name": match.group(1),
                "line": line_num,
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
            })

        # 匹配类声明
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        for match in re.finditer(class_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            classes.append({
                "name": match.group(1),
                "line": line_num,
                "extends": match.group(2)
            })

        # 匹配import语句
        import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, content):
            imports.append(match.group(1))

        return {
            "language": "javascript" if self.language == Language.JAVASCRIPT else "typescript",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(content.split('\n'))
        }

    def _parse_c(self, content: str) -> Dict[str, Any]:
        """
        解析C代码（简化版本）
        使用正则表达式提取基本信息
        """
        import re

        functions = []
        classes = []
        imports = []

        # 匹配函数声明
        func_pattern = r'\w+\s+([\w_]+)\s*\(([^)]*)\)\s*\{'
        for match in re.finditer(func_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                "name": match.group(1),
                "line": line_num,
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
            })

        # 匹配#include指令
        include_pattern = r'#include\s*<([^>]+)>'
        for match in re.finditer(include_pattern, content):
            imports.append(match.group(1))

        return {
            "language": "c",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(content.split('\n'))
        }

    def _parse_cpp(self, content: str) -> Dict[str, Any]:
        """
        解析C++代码（简化版本）
        使用正则表达式提取基本信息
        """
        import re

        functions = []
        classes = []
        imports = []

        # 匹配函数声明
        func_pattern = r'\w+\s+([\w_]+)\s*\(([^)]*)\)\s*\{'
        for match in re.finditer(func_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                "name": match.group(1),
                "line": line_num,
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
            })

        # 匹配类声明
        class_pattern = r'class\s+([\w_]+)(?:\s*:\s*([^\{]+))?\s*\{'
        for match in re.finditer(class_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            classes.append({
                "name": match.group(1),
                "line": line_num,
                "extends": match.group(2).strip() if match.group(2) else None
            })

        # 匹配#include指令
        include_pattern = r'#include\s*<([^>]+)>'
        for match in re.finditer(include_pattern, content):
            imports.append(match.group(1))

        return {
            "language": "cpp",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(content.split('\n'))
        }

    def _parse_php(self, content: str) -> Dict[str, Any]:
        """
        解析PHP代码（简化版本）
        使用正则表达式提取基本信息
        """
        import re

        functions = []
        classes = []
        imports = []

        # 匹配函数声明
        func_pattern = r'function\s+([\w_]+)\s*\(([^)]*)\)\s*\{'
        for match in re.finditer(func_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                "name": match.group(1),
                "line": line_num,
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
            })

        # 匹配类声明
        class_pattern = r'class\s+([\w_]+)(?:\s+extends\s+([\w_]+))?(?:\s+implements\s+([\w_,\s]+))?\s*\{'
        for match in re.finditer(class_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            classes.append({
                "name": match.group(1),
                "line": line_num,
                "extends": match.group(2),
                "implements": [i.strip() for i in match.group(3).split(',')] if match.group(3) else []
            })

        # 匹配require/include语句
        import_pattern = r'(?:require|include)(?:_once)?\s*\(\s*["\']([^"\']+)["\']\s*\)'
        for match in re.finditer(import_pattern, content):
            imports.append(match.group(1))

        return {
            "language": "php",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(content.split('\n'))
        }

    def _parse_ruby(self, content: str) -> Dict[str, Any]:
        """
        解析Ruby代码（简化版本）
        使用正则表达式提取基本信息
        """
        import re

        functions = []
        classes = []
        imports = []

        # 匹配方法定义
        func_pattern = r'def\s+([\w_]+)(?:\s*\(([^)]*)\))?'
        for match in re.finditer(func_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                "name": match.group(1),
                "line": line_num,
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()] if match.group(2) else []
            })

        # 匹配类声明
        class_pattern = r'class\s+([\w_:]+)(?:\s+<\s+([\w_:]+))?'
        for match in re.finditer(class_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            classes.append({
                "name": match.group(1),
                "line": line_num,
                "extends": match.group(2)
            })

        # 匹配require语句
        import_pattern = r'require\s+["\']([^"\']+)["\']'
        for match in re.finditer(import_pattern, content):
            imports.append(match.group(1))

        return {
            "language": "ruby",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(content.split('\n'))
        }


def create_ast_parser(language: Language) -> ASTParser:
    """
    创建AST解析器实例

    Args:
        language: 目标语言

    Returns:
        AST解析器实例
    """
    return ASTParser(language)


# 导出主要符号
__all__ = [
    'Language',
    'LanguageConfig',
    'LANGUAGE_CONFIGS',
    'detect_language',
    'get_language_config',
    'find_test_files',
    'install_dependencies',
    'get_test_command',
    'ASTParser',
    'create_ast_parser'
]
