"""
Rich Logger Utility Module.

Provides colorful, structured console output using the `rich` Python library.

JS/Node.js comparison:
- JS: `console.log()` with `chalk` or `winston` / `pino` for colorful output.
- Python: `rich` provides an easy-to-use `Console` object and formatted progress/theme support.
"""

from rich.console import Console
from rich.theme import Theme

# Define custom color palette theme for Rich console logs
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "agent": "magenta",
    "highlight": "bold cyan",
})

# Single shared Console instance
console = Console(theme=custom_theme)


class AgentLogger:
    """
    Logger wrapper around Rich Console providing styled log methods.
    """

    def __init__(self) -> None:
        """Initializes logger with the custom Rich console."""
        self._console = console

    def info(self, message: str) -> None:
        """Logs an informational message in cyan."""
        self._console.print(f"[info][INFO]:[/info] {message}")

    def success(self, message: str) -> None:
        """Logs a success message in bold green."""
        self._console.print(f"[success][SUCCESS]:[/success] {message}")

    def warning(self, message: str) -> None:
        """Logs a warning message in yellow."""
        self._console.print(f"[warning][WARNING]:[/warning] {message}")

    def error(self, message: str) -> None:
        """Logs an error message in bold red."""
        self._console.print(f"[error][ERROR]:[/error] {message}")

    def agent(self, agent_name: str, message: str) -> None:
        """Logs an agent-specific action in magenta."""
        self._console.print(f"[agent][{agent_name}]:[/agent] {message}")


# Global logger instance
logger = AgentLogger()
