"""
Reporter Module.

Generates final audit reports summarizing the execution lifecycle.

JS/Node.js comparison:
- JS: Formats result summary and writes JSON/HTML reports to build output folders.
- Python: Uses `ExecutionReport` model and output path configuration to format markdown/console reports.
"""

from pathlib import Path
from models.execution_plan import ExecutionPlan
from models.report import ExecutionReport
from config.settings import settings
from utils.logger import logger


class AgentReporter:
    """
    Generates execution summary reports.

    Single Responsibility Principle (SOLID):
    Responsible strictly for report formatting and persistence.
    """

    def __init__(self, output_dir: Path = None) -> None:
        """
        Initializes reporter with target output directory.

        Args:
            output_dir (Path, optional): Directory to save reports.
        """
        self.output_dir = output_dir or settings.output_dir

    def generate_report(
        self, user_prompt: str, plan: ExecutionPlan, success: bool
    ) -> ExecutionReport:
        """
        Creates and outputs an ExecutionReport based on process outcomes.

        Args:
            user_prompt (str): Original user request.
            plan (ExecutionPlan): Executed plan.
            success (bool): Execution outcome flag.

        Returns:
            ExecutionReport: Formatted report object.

        TODO:
            Format markdown summary and write report file to output directory.
        """
        logger.agent("Reporter", "Generating final execution report...")
        
        status_str = "SUCCESS" if success else "FAILED"
        report = ExecutionReport(
            user_prompt=user_prompt,
            status=status_str,
            steps_completed=len(plan.steps) if success else 0,
            total_steps=len(plan.steps),
            modified_files=[],
            summary_notes="Execution completed (Placeholder notes).",
        )
        logger.success(f"Report generated with status: {report.status}")
        return report
