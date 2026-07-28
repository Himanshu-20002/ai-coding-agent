"""
Ignore Pattern Filter Utility Module.

Filters out ignored directories and files (e.g., node_modules, .git, __pycache__, .venv).

JS/Node.js comparison:
- JS: Using `ignore` or `glob` matching packages.
- Python: Manual path pattern matching or `pathlib.Path.match()`.
"""

from pathlib import Path
from typing import List, Set


class IgnoreFilter:
    """
    Filters paths based on standard ignore patterns.
    """

    # Default ignored directory and file names
    DEFAULT_IGNORES: Set[str] = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "*.pyc",
    }

    def __init__(self, custom_ignores: List[str] = None) -> None:
        """
        Initializes filter with default and optional custom ignore patterns.

        Args:
            custom_ignores (List[str], optional): Additional string patterns to ignore.
        """
        self.ignore_patterns: Set[str] = set(self.DEFAULT_IGNORES)
        if custom_ignores:
            self.ignore_patterns.update(custom_ignores)

    def should_ignore(self, path: Path) -> bool:
        """
        Checks if a file or directory path should be ignored during scanning.

        Args:
            path (Path): Path to evaluate.

        Returns:
            bool: True if path matches ignore patterns, False otherwise.
        """
        # Check matching path parts
        for part in path.parts:
            if part in self.ignore_patterns:
                return True
        return False
