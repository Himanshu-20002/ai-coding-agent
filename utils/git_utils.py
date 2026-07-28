"""
Git Utilities Module.

Provides wrapper logic around `GitPython` to inspect git status, commits, and file diffs.

JS/Node.js comparison:
- JS: Executing `child_process.exec('git status')` or using `simple-git` package.
- Python: `git.Repo` object provides programmatic access to git object models.
"""

from pathlib import Path
from typing import Optional, List
import git
from utils.logger import logger


class GitHelper:
    """
    Wrapper for Git repository status checks and operations using GitPython.
    """

    def __init__(self, repo_path: Path) -> None:
        """
        Initializes GitHelper for a given repository path.

        Args:
            repo_path (Path): Path to target workspace repository.
        """
        self.repo_path = repo_path
        self._repo: Optional[git.Repo] = None

    def is_git_repository(self) -> bool:
        """
        Checks if target directory is a valid git repository.

        Returns:
            bool: True if path is a git repo, False otherwise.
        """
        try:
            self._repo = git.Repo(self.repo_path, search_parent_directories=True)
            return True
        except (git.InvalidGitRepositoryError, git.NoSuchPathError):
            logger.warning(f"Directory is not a valid git repo: {self.repo_path}")
            return False

    def get_diff(self) -> str:
        """
        Gets unstaged diffs across the target repository.

        Returns:
            str: Git diff output text.

        TODO:
            Implement git diff extraction logic.
        """
        if not self.is_git_repository() or not self._repo:
            return ""
        # Placeholder for returning diff
        return self._repo.git.diff()
