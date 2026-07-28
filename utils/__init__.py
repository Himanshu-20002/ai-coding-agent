"""
Utilities Package Initialization.

Contains general helper modules (file handling, Git commands, Rich logger, and ignore rule parser).

JS/Node.js comparison:
In Node.js projects, utility helpers are grouped in a `utils/` or `lib/` directory and exported via index.js.
In Python, `__init__.py` re-exports utilities for cleaner imports like `from utils import logger, safe_read_file`.
"""

from utils.logger import logger
from utils.file_utils import safe_read_file, safe_write_file
from utils.git_utils import GitHelper
from utils.ignore import IgnoreFilter

__all__ = [
    "logger",
    "safe_read_file",
    "safe_write_file",
    "GitHelper",
    "IgnoreFilter",
]
