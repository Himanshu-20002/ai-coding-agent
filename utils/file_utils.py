"""
File Utilities Module.

Provides safe file reading and writing operations using standard Python `pathlib.Path`.

JS/Node.js comparison:
- JS: `fs.readFileSync(filepath, 'utf-8')` or `await fs.promises.readFile(filepath, 'utf-8')`.
- Python: `pathlib.Path` encapsulates path operations natively. `path.read_text(encoding='utf-8')` simplifies reading files.
"""

from pathlib import Path
from typing import Optional
from utils.logger import logger


def safe_read_file(file_path: Path) -> Optional[str]:
    """
    Safely reads file content as utf-8 string.

    Args:
        file_path (Path): Path to target file.

    Returns:
        Optional[str]: File content string if successful, None if reading fails.

    JS/Node.js Comparison:
    Python `Optional[str]` is equivalent to TypeScript `string | null` or `string | undefined`.
    """
    try:
        if not file_path.exists() or not file_path.is_file():
            logger.warning(f"File does not exist: {file_path}")
            return None
        return file_path.read_text(encoding="utf-8")
    except Exception as err:
        logger.error(f"Failed to read file {file_path}: {err}")
        return None


def safe_write_file(file_path: Path, content: str) -> bool:
    """
    Safely writes content string to target file, creating parent directories if needed.

    Args:
        file_path (Path): Path to target file.
        content (str): Text content to write.

    Returns:
        bool: True if writing succeeded, False otherwise.
    """
    try:
        # Create parent directories if they don't exist (equivalent to `mkdir -p` or `fs.mkdirSync(dir, {recursive: true})`)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        logger.info(f"Successfully wrote to: {file_path}")
        return True
    except Exception as err:
        logger.error(f"Failed to write file {file_path}: {err}")
        return False
