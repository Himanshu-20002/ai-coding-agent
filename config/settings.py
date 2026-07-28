"""
Application Settings & Environment Configuration Module.

This module handles loading environment variables from a `.env` file using `python-dotenv`.

JS/Node.js comparison:
- Node.js: `require('dotenv').config()` loads variables into `process.env.VARIABLE_NAME`.
- Python: `load_dotenv()` loads variables into `os.environ["VARIABLE_NAME"]` or `os.getenv("VARIABLE_NAME")`.
- Node/TypeScript often uses custom config objects or `zod` for type-safe environment vars.
- Python uses `os.getenv()` or `dataclasses`/`pydantic` to structure configuration values cleanly.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class Settings:
    """
    Centralized configuration management class.

    Attributes:
        openai_api_key (str): Key used to authenticate with OpenAI API.
        openai_model (str): OpenAI model identifier (e.g., 'gpt-4o').
        target_repo_path (Path): Path to the codebase being analyzed.
        output_dir (Path): Path where output plans and reports will be saved.
        log_level (str): Logging severity level (e.g., 'INFO', 'DEBUG').
    """

    def __init__(self) -> None:
        """
        Initializes settings by reading environment variables with sensible defaults.
        
        JS/Node.js Comparison:
        `__init__` is Python's constructor method, equivalent to `constructor()` in a JS class.
        `self` is the explicit reference to the current instance, equivalent to `this` in JS.
        """
        # Read environment variables using os.getenv(key, default_value)
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Path conversion: using pathlib.Path (similar to Node's path.resolve / path.join)
        raw_repo_path = os.getenv("TARGET_REPO_PATH", "./workspace")
        self.target_repo_path: Path = Path(raw_repo_path).resolve()
        
        raw_output_dir = os.getenv("OUTPUT_DIR", "./output")
        self.output_dir: Path = Path(raw_output_dir).resolve()
        
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    def validate(self) -> bool:
        """
        Validates required environment configurations.

        Returns:
            bool: True if configuration is valid, False otherwise.

        TODO:
            Add deeper validation logic (e.g., check if target directory actually exists).
        """
        if not self.openai_api_key:
            # Note: During initial skeleton run, we allow missing key to avoid blocking tests
            return False
        return True


# Singleton pattern instance (similar to exporting an instantiated object in Node.js module.exports = new Settings())
settings = Settings()
