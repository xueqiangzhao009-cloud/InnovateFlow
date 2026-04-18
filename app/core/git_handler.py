"""
InnovateFlow Git 集成模块

提供版本控制功能：
- 自动创建功能分支
- 智能 commit message 生成
- 变更 diff 可视化
- 版本回滚支持
- 代码变更追踪
"""

import os
import subprocess
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

from app.core.logging import setup_logger

logger = setup_logger("InnovateFlow.git_integration")


@dataclass
class GitCommit:
    """Git提交信息"""
    hash: str
    message: str
    author: str
    date: str
    files_changed: List[str]


@dataclass
class GitDiff:
    """Git差异信息"""
    file_path: str
    additions: int
    deletions: int
    changes: str


class GitRepository:
    """
    Git仓库管理类
    """

    def __init__(self, repo_path: str):
        """
        初始化Git仓库管理器

        Args:
            repo_path: 仓库路径
        """
        self.repo_path = repo_path
        self._git_dir = os.path.join(repo_path, ".git")

    def is_git_repo(self) -> bool:
        """检查是否是Git仓库"""
        return os.path.isdir(self._git_dir)

    def init_repo(self) -> bool:
        """
        初始化Git仓库

        Returns:
            是否成功
        """
        if self.is_git_repo():
            logger.info("Git 仓库已存在")
            return True

        try:
            result = subprocess.run(
                ["git", "init"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info("Git 仓库初始化成功")
                return True
            else:
                logger.error(f"Git 仓库初始化失败: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Git 仓库初始化异常: {e}")
            return False

    def get_current_branch(self) -> Optional[str]:
        """
        获取当前分支名称

        Returns:
            分支名称，失败返回None
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return result.stdout.strip()
            return None

        except Exception:
            return None

    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """
        创建新分支

        Args:
            branch_name: 分支名称
            checkout: 是否切换到新分支

        Returns:
            是否成功
        """
        try:
            if checkout:
                result = subprocess.run(
                    ["git", "checkout", "-b", branch_name],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ["git", "branch", branch_name],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:
                logger.info(f"创建分支成功: {branch_name}")
                return True
            else:
                logger.error(f"创建分支失败: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"创建分支异常: {e}")
            return False

    def checkout_branch(self, branch_name: str) -> bool:
        """
        切换分支

        Args:
            branch_name: 目标分支名称

        Returns:
            是否成功
        """
        try:
            result = subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info(f"切换分支成功: {branch_name}")
                return True
            else:
                logger.error(f"切换分支失败: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"切换分支异常: {e}")
            return False

    def list_branches(self, remote: bool = False) -> List[str]:
        """
        列出所有分支

        Args:
            remote: 是否包含远程分支

        Returns:
            分支列表
        """
        try:
            cmd = ["git", "branch"]
            if remote:
                cmd.append("-a")

            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                branches = []
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line:
                        # 移除当前分支标记
                        if line.startswith('*'):
                            line = line[1:].strip()
                        # 移除远程分支前缀
                        if line.startswith('remotes/origin/'):
                            line = line[15:]
                        branches.append(line)
                return branches
            return []

        except Exception:
            return []

    def stage_files(self, files: List[str]) -> bool:
        """
        暂存文件

        Args:
            files: 文件路径列表

        Returns:
            是否成功
        """
        try:
            cmd = ["git", "add"] + files
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info(f"暂存文件成功: {len(files)} 个文件")
                return True
            else:
                logger.error(f"暂存文件失败: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"暂存文件异常: {e}")
            return False

    def stage_all(self) -> bool:
        """暂存所有变更"""
        return self.stage_files(["."])

    def commit(self, message: str) -> Optional[str]:
        """
        提交变更

        Args:
            message: 提交消息

        Returns:
            提交哈希，失败返回None
        """
        try:
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # 获取提交哈希
                hash_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
                commit_hash = hash_result.stdout.strip(
                )[:8] if hash_result.returncode == 0 else "unknown"
                logger.info(f"提交成功: {commit_hash}")
                return commit_hash
            else:
                logger.error(f"提交失败: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"提交异常: {e}")
            return None

    def get_status(self) -> Dict[str, List[str]]:
        """
        获取仓库状态

        Returns:
            包含 modified, added, deleted, untracked 文件列表的字典
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            status = {
                "modified": [],
                "added": [],
                "deleted": [],
                "untracked": []
            }

            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if not line.strip():
                        continue

                    code = line[:2]
                    file_path = line[3:]

                    if code[0] == 'M' or code[1] == 'M':
                        status["modified"].append(file_path)
                    elif code[0] == 'A':
                        status["added"].append(file_path)
                    elif code[0] == 'D':
                        status["deleted"].append(file_path)
                    elif code == '??':
                        status["untracked"].append(file_path)

            return status

        except Exception:
            return {"modified": [], "added": [], "deleted": [], "untracked": []}

    def get_diff(self, file_path: Optional[str] = None, staged: bool = False) -> List[GitDiff]:
        """
        获取差异信息

        Args:
            file_path: 特定文件路径（可选）
            staged: 是否获取已暂存的差异

        Returns:
            差异信息列表
        """
        try:
            cmd = ["git", "diff"]
            if staged:
                cmd.append("--cached")
            if file_path:
                cmd.extend(["--", file_path])

            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            diffs = []
            if result.returncode == 0 and result.stdout:
                current_file = None
                current_additions = 0
                current_deletions = 0
                current_changes = []

                for line in result.stdout.split('\n'):
                    if line.startswith('diff --git'):
                        # 保存上一个文件的diff
                        if current_file:
                            diffs.append(GitDiff(
                                file_path=current_file,
                                additions=current_additions,
                                deletions=current_deletions,
                                changes='\n'.join(current_changes)
                            ))

                        # 开始新文件
                        parts = line.split(' b/')
                        current_file = parts[-1] if len(
                            parts) > 1 else "unknown"
                        current_additions = 0
                        current_deletions = 0
                        current_changes = []

                    elif line.startswith('+') and not line.startswith('+++'):
                        current_additions += 1
                        current_changes.append(line)
                    elif line.startswith('-') and not line.startswith('---'):
                        current_deletions += 1
                        current_changes.append(line)
                    elif line.startswith('@@'):
                        current_changes.append(line)

                # 保存最后一个文件
                if current_file:
                    diffs.append(GitDiff(
                        file_path=current_file,
                        additions=current_additions,
                        deletions=current_deletions,
                        changes='\n'.join(current_changes)
                    ))

            return diffs

        except Exception:
            return []

    def get_commit_history(self, max_count: int = 20, file_path: Optional[str] = None) -> List[GitCommit]:
        """
        获取提交历史

        Args:
            max_count: 最大返回数量
            file_path: 特定文件路径（可选）

        Returns:
            提交历史列表
        """
        try:
            cmd = [
                "git", "log",
                f"--max-count={max_count}",
                "--pretty=format:%H|%s|%an|%ai",
                "--name-only"
            ]
            if file_path:
                cmd.extend(["--", file_path])

            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            commits = []
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if '|' in line:
                        parts = line.split('|', 3)
                        if len(parts) == 4:
                            hash_val, message, author, date = parts

                            # 获取变更的文件
                            files_changed = []
                            i += 1
                            while i < len(lines) and lines[i].strip():
                                files_changed.append(lines[i].strip())
                                i += 1

                            commits.append(GitCommit(
                                hash=hash_val[:8],
                                message=message,
                                author=author,
                                date=date,
                                files_changed=files_changed
                            ))
                    i += 1

            return commits

        except Exception:
            return []

    def revert_file(self, file_path: str, commit_hash: Optional[str] = None) -> bool:
        """
        回滚文件到指定版本

        Args:
            file_path: 文件路径
            commit_hash: 提交哈希（默认为HEAD）

        Returns:
            是否成功
        """
        try:
            target = commit_hash if commit_hash else "HEAD"
            result = subprocess.run(
                ["git", "checkout", target, "--", file_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info(f"文件回滚成功: {file_path}")
                return True
            else:
                logger.error(f"文件回滚失败: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"文件回滚异常: {e}")
            return False


class CommitMessageGenerator:
    """
    智能Commit消息生成器
    """

    # 常用的commit类型
    COMMIT_TYPES = {
        "feat": "新功能",
        "fix": "修复bug",
        "docs": "文档更新",
        "style": "代码格式调整",
        "refactor": "重构",
        "test": "测试相关",
        "chore": "构建/工具变更",
        "perf": "性能优化",
        "ci": "CI配置",
        "revert": "回滚"
    }

    @staticmethod
    def generate(files_changed: List[str], diff_summary: str) -> str:
        """
        根据变更内容生成commit消息

        Args:
            files_changed: 变更文件列表
            diff_summary: 差异摘要

        Returns:
            生成的commit消息
        """
        if not files_changed:
            return "chore: 更新代码"

        # 分析变更类型
        is_new_file = any("new file" in diff_summary.lower() for _ in [1])
        is_fix = any(keyword in diff_summary.lower()
                     for keyword in ["fix", "bug", "error", "修复"])
        is_test = any("test" in f.lower() for f in files_changed)
        is_doc = any(f.endswith(('.md', '.rst', '.txt'))
                     for f in files_changed)
        is_config = any(f.endswith(('.json', '.yaml', '.yml',
                        '.toml', '.ini')) for f in files_changed)

        # 确定commit类型
        if is_new_file:
            commit_type = "feat"
        elif is_fix:
            commit_type = "fix"
        elif is_test:
            commit_type = "test"
        elif is_doc:
            commit_type = "docs"
        elif is_config:
            commit_type = "chore"
        else:
            commit_type = "refactor"

        # 生成描述
        if len(files_changed) == 1:
            file_name = os.path.basename(files_changed[0])
            description = f"更新 {file_name}"
        else:
            description = f"更新 {len(files_changed)} 个文件"

        return f"{commit_type}: {description}"

    @staticmethod
    def generate_detailed(files_changed: List[str], diff: List[GitDiff]) -> str:
        """
        生成详细的commit消息

        Args:
            files_changed: 变更文件列表
            diff: 差异信息列表

        Returns:
            详细的commit消息
        """
        if not files_changed:
            return "chore: 更新代码"

        # 统计变更
        total_additions = sum(d.additions for d in diff)
        total_deletions = sum(d.deletions for d in diff)

        # 确定类型
        commit_type = CommitMessageGenerator.generate(
            files_changed, "").split(":")[0]

        # 生成主体
        lines = [f"{commit_type}: 代码更新\n"]
        lines.append("变更摘要:")
        lines.append(f"- 新增 {total_additions} 行")
        lines.append(f"- 删除 {total_deletions} 行")
        lines.append(f"- 修改 {len(files_changed)} 个文件\n")

        # 列出主要变更文件
        if len(files_changed) <= 5:
            lines.append("变更文件:")
            for f in files_changed:
                lines.append(f"  - {f}")

        return "\n".join(lines)


def create_feature_branch(repo_path: str, feature_name: str) -> Tuple[bool, str]:
    """
    创建功能分支

    Args:
        repo_path: 仓库路径
        feature_name: 功能名称

    Returns:
        (成功状态, 分支名称或错误消息)
    """
    repo = GitRepository(repo_path)

    if not repo.is_git_repo():
        if not repo.init_repo():
            return False, "无法初始化 Git 仓库"

    # 清理功能名称
    clean_name = feature_name.lower().replace(" ", "-")
    branch_name = f"feature/{clean_name}"

    # 检查分支是否已存在
    existing_branches = repo.list_branches()
    if branch_name in existing_branches:
        return False, f"分支已存在: {branch_name}"

    # 创建分支
    if repo.create_branch(branch_name):
        return True, branch_name
    else:
        return False, "创建分支失败"


def auto_commit(repo_path: str, message: Optional[str] = None) -> Tuple[bool, str]:
    """
    自动提交所有变更

    Args:
        repo_path: 仓库路径
        commit消息（可选）

    Returns:
        (成功状态, 提交哈希或错误消息)
    """
    repo = GitRepository(repo_path)

    if not repo.is_git_repo():
        return False, "不是 Git 仓库"

    # 获取状态
    status = repo.get_status()
    all_changes = status["modified"] + status["added"] + \
        status["deleted"] + status["untracked"]

    if not all_changes:
        return False, "没有变更需要提交"

    # 暂存所有文件
    if not repo.stage_all():
        return False, "暂存文件失败"

    # 生成commit消息
    if not message:
        diff = repo.get_diff(staged=True)
        message = CommitMessageGenerator.generate(all_changes, str(diff))

    # 提交
    commit_hash = repo.commit(message)
    if commit_hash:
        return True, commit_hash
    else:
        return False, "提交失败"


def get_change_summary(repo_path: str) -> Dict[str, Any]:
    """
    获取变更摘要

    Args:
        repo_path: 仓库路径

    Returns:
        变更摘要字典
    """
    repo = GitRepository(repo_path)

    if not repo.is_git_repo():
        return {"error": "不是 Git 仓库"}

    status = repo.get_status()
    diff = repo.get_diff(staged=True)

    return {
        "branch": repo.get_current_branch(),
        "status": status,
        "total_changes": len(status["modified"]) + len(status["added"]) + len(status["deleted"]),
        "untracked": len(status["untracked"]),
        "diff_summary": [
            {
                "file": d.file_path,
                "additions": d.additions,
                "deletions": d.deletions
            }
            for d in diff
        ]
    }


# 导出主要符号
__all__ = [
    'GitCommit',
    'GitDiff',
    'GitRepository',
    'CommitMessageGenerator',
    'create_feature_branch',
    'auto_commit',
    'get_change_summary'
]
