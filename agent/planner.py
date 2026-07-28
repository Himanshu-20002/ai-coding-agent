"""
Execution Planner Module.

Translates user prompt and repository summary into a structured execution plan.

JS/Node.js comparison:
- JS: A service class consuming prompt + context object and outputting a task list array.
- Python: Decoupled class taking `RepositorySummary` and `user_prompt` to produce `ExecutionPlan`.
"""

from models.repository import RepositorySummary
from models.execution_plan import ExecutionPlan, PlanStep
from agent.llm import LLMClient
from utils.logger import logger


class ExecutionPlanner:
    """
    Creates execution plans based on prompt requirements and repository context.

    Single Responsibility Principle (SOLID):
    Responsible strictly for prompt strategy and creating execution steps.
    """

    def __init__(self, llm_client: LLMClient) -> None:
        """
        Initializes planner with an LLM client instance.

        Args:
            llm_client (LLMClient): Client used to interface with OpenAI API.
        """
        self.llm_client = llm_client

    def create_execution_plan(
        self, user_prompt: str, repo_summary: RepositorySummary
    ) -> ExecutionPlan:
        """
        Generates an execution plan containing ordered modification steps.

        Args:
            user_prompt (str): User request prompt.
            repo_summary (RepositorySummary): Repository structure summary.

        Returns:
            ExecutionPlan: Generated execution plan object.

        TODO:
            Construct structured prompt, invoke LLM client, and parse steps.
        """
        logger.agent("Planner", f"Creating execution plan for prompt: '{user_prompt}'")
        
        # Placeholder plan step
        plan = ExecutionPlan(
            user_prompt=user_prompt,
            summary="Placeholder plan summary",
            steps=[],
        )
        logger.success(f"Execution plan created with {len(plan.steps)} steps.")
        return plan
