"""
Main Application CLI Entrypoint.

This script acts as the lightweight launcher for the AI Coding Agent system.

JS/Node.js comparison:
- JS/Node: Equivalent to `index.js`, `main.js`, or `cli.js` parsing arguments and bootstrapping services.
- Python: Uses the standard `if __name__ == '__main__':` idiom to execute when run directly via CLI.
"""

import sys
from config.settings import settings
from agent.orchestrator import AgentOrchestrator
from utils.logger import logger


def main() -> None:
    """
    Main CLI function to bootstrap and run the agent orchestrator.
    """
    logger.info("Initializing AI Coding Agent System...")
    logger.info(f"Target Repository Path: {settings.target_repo_path}")
    logger.info(f"Configured OpenAI Model: {settings.openai_model}")

    # Validate settings before running
    if not settings.validate():
        logger.warning(
            "Note: OPENAI_API_KEY is not set in environment or .env. Running scaffold in offline placeholder mode."
        )

    # Sample prompt for demonstration
    prompt = "Explore repository, analyze architecture, and propose optimizations."
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])

    # Instantiate and trigger orchestrator
    orchestrator = AgentOrchestrator()
    report = orchestrator.run(prompt)

    logger.success(f"Pipeline finished! Final Status: {report.status}")


if __name__ == "__main__":
    """
    Python idiom: checks if the script is executed directly from command line.
    
    JS/Node.js comparison:
    In Node.js, `require.main === module` checks if a script is the CLI entrypoint versus imported.
    """
    main()
