"""
Data Models Package.

Contains dataclasses representing domain concepts (Repository summary, Execution plan, Report).

JS/Node.js comparison:
In TypeScript, these models would be defined as `interface RepositorySummary { ... }` or `type ExecutionPlan = { ... }`.
In Python, `@dataclass` automatically generates `__init__`, `__repr__`, and equality methods for data structures.
"""

from models.repository import RepositorySummary, FileMetadata
from models.execution_plan import ExecutionPlan, PlanStep
from models.report import ExecutionReport

__all__ = [
    "RepositorySummary",
    "FileMetadata",
    "ExecutionPlan",
    "PlanStep",
    "ExecutionReport",
]
