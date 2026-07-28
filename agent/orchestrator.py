"""
Agent Orchestrator Module.

Coordinates the end-to-end lifecycle pipeline (Explore -> Plan -> LLM -> Execute -> Report).

JS/Node.js comparison:
- JS: Main controller service wire-up orchestrating step-by-step pipeline execution.
- Python: Central Orchestrator instantiating decoupled agent modules adhering to SOLID principles.
"""

from pathlib import Path
from config.settings import settings
from agent.explorer import RepositoryExplorer
from agent.planner import ExecutionPlanner
from agent.llm import LLMClient
from agent.executor import CodeExecutor
from agent.reporter import AgentReporter
from models.report import ExecutionReport
from utils.logger import logger


class AgentOrchestrator:
    """
    Main Orchestrator class managing execution flow across sub-agents.
    """

    def __init__(self, repo_path: Path = None) -> None:
        """
        Initializes orchestrator components.

        Args:
            repo_path (Path, optional): Path to codebase workspace.
        """
        self.repo_path = repo_path or settings.target_repo_path
        
        # Instantiate agent modules
        self.explorer = RepositoryExplorer(repo_path=self.repo_path)
        self.llm_client = LLMClient()
        self.planner = ExecutionPlanner(llm_client=self.llm_client)
        self.executor = CodeExecutor(llm_client=self.llm_client)
        self.reporter = AgentReporter()

    def run(self, user_prompt: str) -> ExecutionReport:
        """
        Runs the complete end-to-end workflow for a given user prompt.

        Sequence:
            1. Explorer: Scans repository and builds summary.
            2. Planner: Generates execution plan.
            3. Executor: Applies changes using LLM.
            4. Reporter: Generates final execution report.

        Args:
            user_prompt (str): User prompt requesting code analysis or modifications.

        Returns:
            ExecutionReport: Summary report of execution outcome.
        """
        logger.info(f"Starting AI Coding Agent pipeline for prompt: '{user_prompt}'")
        
        # Step 1: Scan & Summarize Repository
        summary = self.explorer.build_summary()
        
        # Step 2: Create Execution Plan
        plan = self.planner.create_execution_plan(user_prompt, summary)
        
        # Step 3: Execute Plan
        success = self.executor.apply_changes(plan)
        
        # Step 4: Generate Report
        report = self.reporter.generate_report(user_prompt, plan, success)
        
        logger.success("Agent workflow pipeline completed successfully!")
        return report
