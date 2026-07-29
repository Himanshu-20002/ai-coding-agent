"""
Execution Planner Module.

Translates user feature requests and repository summaries into structured execution plans.

Design & Architectural Constraints:
- Pure deterministic planning logic without calling LLMs or generating code.
- Takes RepositorySummary and user_prompt as inputs.
- Produces an ExecutionPlan containing goal, ordered steps, reasons, target files, and expected outcomes.
- Displays execution plan using Rich.
- Saves the plan artifact to output/plans/execution-plan.md.

JS/Node.js comparison:
- JS: A service class consuming prompt + context object and returning a structured plan JSON/markdown.
- Python: Decoupled class taking `RepositorySummary` and `user_prompt` to produce `ExecutionPlan`.
"""

from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from models.repository import RepositorySummary
from models.execution_plan import ExecutionPlan, PlanStep
from utils.logger import logger, console
from utils.file_utils import safe_write_file


class ExecutionPlanner:
    """
    Creates execution plans based on prompt requirements and repository context.

    Single Responsibility Principle (SOLID):
    Responsible strictly for analyzing requirements & context to construct execution steps.
    No code generation, no LLM calls.
    """

    def __init__(self, llm_client: Optional[object] = None) -> None:
        """
        Initializes planner with optional LLM client instance (unused in deterministic mode).

        Args:
            llm_client (Optional[object]): Optional client reference.
        """
        self.llm_client = llm_client
        self.output_dir = Path("output/plans")

    def create_execution_plan(
        self, user_prompt: str, repo_summary: RepositorySummary
    ) -> ExecutionPlan:
        """
        Generates a structured execution plan containing ordered modification steps.

        Args:
            user_prompt (str): User request prompt.
            repo_summary (RepositorySummary): Repository structure summary.

        Returns:
            ExecutionPlan: Generated execution plan object.
        """
        logger.agent("Planner", f"Creating execution plan for prompt: '{user_prompt}'")

        goal = self._determine_goal(user_prompt, repo_summary)
        steps = self._generate_steps(user_prompt, repo_summary)
        summary_text = (
            f"Implementation plan for '{user_prompt}' targeted at a "
            f"{repo_summary.primary_language} codebase ({repo_summary.framework} framework)."
        )

        plan = ExecutionPlan(
            user_prompt=user_prompt,
            goal=goal,
            summary=summary_text,
            steps=steps,
        )

        logger.success(f"Execution plan created with {len(plan.steps)} steps.")
        
        # Display using Rich
        self.print_rich_plan(plan)
        
        # Save to output/plans/execution-plan.md
        self.save_plan_artifact(plan)

        return plan

    def _determine_goal(self, user_prompt: str, repo_summary: RepositorySummary) -> str:
        """Constructs a high-level goal statement from prompt and repo context."""
        fw_info = f" in {repo_summary.framework}" if repo_summary.framework != "Unknown" else ""
        lang_info = f" ({repo_summary.primary_language})" if repo_summary.primary_language != "Unknown" else ""
        return f"{user_prompt.strip().capitalize()}{fw_info}{lang_info}"

    def _generate_steps(
        self, user_prompt: str, repo_summary: RepositorySummary
    ) -> List[PlanStep]:
        """
        Deterministically infers implementation steps based on prompt keywords,
        discovered routes, models, controllers, and primary language.
        """
        prompt_lower = user_prompt.lower()
        steps: List[PlanStep] = []
        step_id = 1

        # Heuristic Step 1: Model / Schema / Data Tier Changes
        model_targets = [Path(m) for m in repo_summary.models]
        if any(w in prompt_lower for w in ["tag", "category", "field", "model", "schema", "db", "database", "data", "store", "organize"]):
            if model_targets:
                target_file = model_targets[0]
                reason = "Data model update required to support new schema attributes/fields."
            else:
                ext = ".py" if repo_summary.primary_language == "Python" else ".js"
                target_file = Path(f"models/item{ext}")
                reason = "Data model definition missing; create schema object."

            steps.append(
                PlanStep(
                    step_id=step_id,
                    title="Update Data Model / Schema",
                    reason=reason,
                    target_files=[target_file],
                    expected_outcome="Data model schema updated with new attributes.",
                    action="MODIFY" if target_file in model_targets else "CREATE",
                    instructions=f"Add necessary fields/properties to support '{user_prompt}'.",
                )
            )
            step_id += 1

        # Heuristic Step 2: Route / Controller / API Endpoint Tier Changes
        route_targets = [Path(r) for r in repo_summary.routes]
        controller_targets = [Path(c) for c in repo_summary.controllers]
        api_targets = route_targets or controller_targets

        if any(w in prompt_lower for w in ["search", "find", "query", "filter", "endpoint", "api", "route", "fetch", "get", "add", "create", "update", "delete", "post"]):
            if api_targets:
                target_file = api_targets[0]
                reason = "API route or controller endpoint update required for feature handling."
            else:
                ext = ".py" if repo_summary.primary_language == "Python" else ".js"
                target_file = Path(f"routes/api{ext}") if repo_summary.framework == "Express" or "js" in repo_summary.primary_language.lower() else Path(f"app/routes{ext}")
                reason = "API endpoint definition missing; create route controller."

            steps.append(
                PlanStep(
                    step_id=step_id,
                    title="Create or Update Endpoint / Route Handler",
                    reason=reason,
                    target_files=[target_file],
                    expected_outcome="Backend API handler implemented for request processing.",
                    action="MODIFY" if target_file in api_targets else "CREATE",
                    instructions=f"Implement request routing and handler logic for '{user_prompt}'.",
                )
            )
            step_id += 1

        # Heuristic Step 3: Service / Business Logic Layer (if present)
        service_targets = [Path(s) for s in repo_summary.services]
        if service_targets or any(w in prompt_lower for w in ["logic", "service", "process", "calculate", "format"]):
            target_file = service_targets[0] if service_targets else Path("services/feature_service.py" if repo_summary.primary_language == "Python" else "services/featureService.js")
            steps.append(
                PlanStep(
                    step_id=step_id,
                    title="Implement Business Logic / Service Layer",
                    reason="Decouple core business rules from routes and models.",
                    target_files=[target_file],
                    expected_outcome="Business logic service functions implemented.",
                    action="MODIFY" if target_file in service_targets else "CREATE",
                    instructions=f"Implement helper methods supporting '{user_prompt}'.",
                )
            )
            step_id += 1

        # Heuristic Step 4: UI / Presentation Layer Changes
        if any(w in prompt_lower for w in ["ui", "frontend", "interface", "view", "component", "search", "page", "display"]):
            ui_file = Path("public/index.html") if "public/index.html" in [str(f.path) for f in repo_summary.files] else Path("src/App.jsx" if repo_summary.frontend_framework == "React" else "views/index.html")
            steps.append(
                PlanStep(
                    step_id=step_id,
                    title="Update Frontend / UI Layer",
                    reason="User interface component required for user interaction.",
                    target_files=[ui_file],
                    expected_outcome="UI updated with interactive elements matching feature request.",
                    action="MODIFY",
                    instructions=f"Add UI controls and event triggers for '{user_prompt}'.",
                )
            )
            step_id += 1

        # Fallback default steps if prompt didn't trigger specific heuristics
        if not steps:
            default_file = repo_summary.files[0].path if repo_summary.files else Path("app.py")
            steps.append(
                PlanStep(
                    step_id=1,
                    title="Implement Core Feature Request",
                    reason=f"Fulfill request: '{user_prompt}'.",
                    target_files=[default_file],
                    expected_outcome="Feature requirements applied to target file.",
                    action="MODIFY",
                    instructions=user_prompt,
                )
            )

        return steps

    def print_rich_plan(self, plan: ExecutionPlan) -> None:
        """
        Displays the execution plan neatly using Rich Console.

        Args:
            plan (ExecutionPlan): Generated plan object.
        """
        console.print()
        console.print(Panel(f"[bold cyan]Goal:[/bold cyan] {plan.goal}", title="Execution Plan Overview", border_style="cyan"))

        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Step", style="bold yellow", width=8, justify="center")
        table.add_column("Details", style="white")

        for step in plan.steps:
            target_files_str = ", ".join([str(f) for f in step.target_files]) if step.target_files else "None"
            step_details = (
                f"[bold cyan]{step.title}[/bold cyan]\n"
                f"[bold green]Reason:[/bold green] {step.reason}\n"
                f"[bold yellow]Target Files:[/bold yellow] {target_files_str}\n"
                f"[bold white]Expected Outcome:[/bold white] {step.expected_outcome}"
            )
            table.add_row(f"Step {step.step_id}", step_details)

        console.print(table)
        console.print()

    def save_plan_artifact(self, plan: ExecutionPlan) -> Path:
        """
        Saves the execution plan to output/plans/execution-plan.md artifact.

        Args:
            plan (ExecutionPlan): Execution plan object.

        Returns:
            Path: Filepath where artifact was saved.
        """
        artifact_path = self.output_dir / "execution-plan.md"
        markdown_content = plan.to_markdown()
        safe_write_file(artifact_path, markdown_content)
        logger.success(f"Saved execution plan artifact to: {artifact_path}")
        return artifact_path
