# 🤖 AI Coding Agent

> An interview-ready, production-grade AI Coding Agent architecture built with **Python 3.11+**, **OpenAI SDK**, **Rich**, and **GitPython**, designed without relying on heavy framework abstractions like LangChain, CrewAI, or AutoGen.

---

## 📌 Project Overview

The **AI Coding Agent** is engineered to explore existing codebases, build structured repository summaries, craft step-by-step execution plans, apply code changes via LLM prompts, and generate structured markdown reports.

This repository serves as a modular, SOLID-compliant foundation with extensive docstrings, type annotations, and comparisons geared towards developers transitioning from **JavaScript / Node.js** to **Python**.

---

## 🏗 Architecture Diagram

```
                 ┌───────────────────────────┐
                 │        User Prompt        │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │    Repository Explorer    │
                 └─────────────┬─────────────┘
                               │ (RepositorySummary)
                               ▼
                 ┌───────────────────────────┐
                 │     Execution Planner     │
                 └─────────────┬─────────────┘
                               │ (ExecutionPlan)
                               ▼
                 ┌───────────────────────────┐
                 │        LLM Client         │
                 └─────────────┬─────────────┘
                               │ (Code Completions)
                               ▼
                 ┌───────────────────────────┐
                 │       Code Executor       │
                 └─────────────┬─────────────┘
                               │ (Apply changes)
                               ▼
                 ┌───────────────────────────┐
                 │       Agent Reporter      │
                 └───────────────────────────┘
```

---

## 📂 Project Structure

```
ai-coding-agent/
│
├── app.py                   # Main CLI entrypoint script
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation & reference
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules for Python projects
│
├── config/                  # Configuration & Environment loading
│   ├── __init__.py
│   └── settings.py          # Centralized settings using python-dotenv & pathlib
│
├── agent/                   # Agent pipeline & execution modules
│   ├── __init__.py
│   ├── explorer.py          # Repository scanner & summary builder
│   ├── planner.py           # Task & step planner
│   ├── llm.py               # OpenAI SDK wrapper client
│   ├── executor.py          # Safe code execution & file writer
│   ├── reporter.py          # Execution auditor & report generator
│   └── orchestrator.py      # End-to-end pipeline coordinator
│
├── models/                  # Domain Data Models (Dataclasses)
│   ├── __init__.py
│   ├── repository.py        # RepositorySummary & FileMetadata dataclasses
│   ├── execution_plan.py    # ExecutionPlan & PlanStep dataclasses
│   └── report.py            # ExecutionReport dataclass
│
├── utils/                   # Shared utilities
│   ├── __init__.py
│   ├── file_utils.py        # Safe file read/write helpers
│   ├── git_utils.py         # GitPython repository helper
│   ├── logger.py            # Rich console logger with custom themes
│   └── ignore.py            # Ignored paths pattern matcher
│
├── output/                  # Generated artifacts
│   ├── plans/
│   ├── reports/
│   └── logs/
│
└── workspace/               # Target repository under analysis
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.11+** installed on your system.

### 1. Clone & Set Up Virtual Environment
```bash
# Create virtual environment (Node equivalent: npm init / node_modules)
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and supply your OpenAI API Key:
```bash
cp .env.example .env
```

---

## 🏃 Running the Agent

Run the main application script:
```bash
python app.py "Refactor module X to adhere to SOLID principles"
```

---

## 🎓 JavaScript / Node.js vs Python Concept Reference

| Feature / Concept | JavaScript / Node.js | Python Equivalent |
|---|---|---|
| **Package / Module Mark** | `package.json` / `index.js` | `__init__.py` |
| **Data Schemas** | TypeScript `interface` / `type` | `@dataclass` / `pydantic` |
| **Path Handling** | `path.join()`, `path.resolve()` | `pathlib.Path` |
| **Environment Variables** | `dotenv` -> `process.env.KEY` | `python-dotenv` -> `os.getenv("KEY")` |
| **Optional Types** | `string \| null` | `Optional[str]` or `str \| None` |
| **Constructor Method** | `constructor()` | `def __init__(self):` |
| **Instance Reference** | `this` | `self` |
| **CLI Execution Check** | `require.main === module` | `if __name__ == '__main__':` |

---

## 🗺 Future Implementation Roadmap

1. **AST Repository Parsing**: Implement Abstract Syntax Tree parsing (`ast` module) for Python file parsing.
2. **Git Diff Application**: Incorporate unified diff generation and patch validation.
3. **Structured Outputs**: Use OpenAI JSON Schema output parsing for `ExecutionPlan`.
4. **Interactive CLI**: Add `rich.prompt.Prompt` user review checkpoints before applying code modifications.
