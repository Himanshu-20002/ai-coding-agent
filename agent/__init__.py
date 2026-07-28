"""
Agent Package Initialization.

Contains modules for repository scanning, task planning, LLM client, execution, reporting, and orchestration.

JS/Node.js comparison:
Equivalent to exporting submodules from an `agent/` folder in Node.js.
"""

from agent.explorer import RepositoryExplorer
from agent.planner import ExecutionPlanner
from agent.llm import LLMClient
from agent.executor import CodeExecutor
from agent.reporter import AgentReporter
from agent.orchestrator import AgentOrchestrator

__all__ = [
    "RepositoryExplorer",
    "ExecutionPlanner",
    "LLMClient",
    "CodeExecutor",
    "AgentReporter",
    "AgentOrchestrator",
]
