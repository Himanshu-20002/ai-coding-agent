"""
Repository Explorer Module.

Responsible for recursively traversing the target repository, scanning non-ignored files,
detecting key configuration files & architecture components, inferring project metadata
(language, framework, database, package manager via lightweight heuristics without LLM),
building a RepositorySummary, and outputting formatted Rich summaries.

JS/Node.js comparison:
- JS: Using `fs.readdirSync()` recursively or `glob` with regex path analysis.
- Python: Using `pathlib.Path.rglob('*')` combined with pattern matching and string analysis.
"""

import json
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from models.repository import RepositorySummary, FileMetadata
from utils.logger import logger, console
from utils.ignore import IgnoreFilter


class RepositoryExplorer:
    """
    Explores and analyzes codebases to construct repository summaries.

    Single Responsibility Principle (SOLID):
    Only responsible for inspecting files and reading structure, NOT for planning or modifying code.
    """

    IMPORTANT_FILES: Set[str] = {
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        ".env",
        "tsconfig.json",
        "go.mod",
        "Cargo.toml",
        "pom.xml",
        "build.gradle",
    }

    TARGET_FOLDERS: Set[str] = {
        "routes",
        "models",
        "controllers",
        "services",
        "src",
        "app",
        "public",
    }

    EXTENSION_LANGUAGE_MAP: Dict[str, str] = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript (React)",
        ".ts": "TypeScript",
        ".tsx": "TypeScript (React)",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".json": "JSON",
        ".md": "Markdown",
        ".sql": "SQL",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".php": "PHP",
        ".rb": "Ruby",
        ".sh": "Shell",
        ".yml": "YAML",
        ".yaml": "YAML",
    }

    BINARY_EXTENSIONS: Set[str] = {
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
        ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar",
        ".exe", ".dll", ".so", ".dylib", ".bin",
        ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3"
    }

    def __init__(self, repo_path: Path) -> None:
        """
        Initializes the Explorer with the target repository path.

        Args:
            repo_path (Path): Path to target codebase.
        """
        self.repo_path = repo_path.resolve()
        self.ignore_filter = IgnoreFilter()

    def is_binary_file(self, file_path: Path) -> bool:
        """
        Checks whether a file is binary using extension checks and null byte inspection.
        """
        if file_path.suffix.lower() in self.BINARY_EXTENSIONS:
            return True
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                if b"\x00" in chunk:
                    return True
        except Exception:
            return True
        return False

    def scan_repository(self) -> List[Path]:
        """
        Recursively scans target repository and returns non-ignored, non-binary file paths.

        Returns:
            List[Path]: Discovered relevant file paths (relative to repo_path).
        """
        logger.agent("Explorer", f"Scanning repository path: {self.repo_path}")
        discovered_files: List[Path] = []

        if not self.repo_path.exists():
            logger.warning(f"Target repository path does not exist: {self.repo_path}")
            return discovered_files

        for path in self.repo_path.rglob("*"):
            if path.is_dir():
                continue
            
            relative_path = path.relative_to(self.repo_path)
            
            # 1. Respect ignore patterns (.git, node_modules, dist, build, __pycache__, .venv)
            if self.ignore_filter.should_ignore(relative_path):
                continue
            
            # 2. Skip binary files
            if self.is_binary_file(path):
                continue

            discovered_files.append(relative_path)

        return discovered_files

    def _infer_project_info(
        self, files: List[Path], languages: Dict[str, int]
    ) -> Tuple[str, str, str, str, str, str]:
        """
        Infers language, framework, database, package manager, backend, and frontend
        using lightweight file-based and dependency heuristics (no LLM).
        """
        primary_language = max(languages, key=languages.get) if languages else "Unknown"
        backend_framework = "Unknown"
        frontend_framework = "Unknown"
        database = "Unknown"
        package_manager = "Unknown"

        file_names = {f.name for f in files}
        file_paths_str = [str(f).replace("\\", "/").lower() for f in files]

        # Package manager detection
        if "package-lock.json" in file_names:
            package_manager = "npm"
        elif "yarn.lock" in file_names:
            package_manager = "yarn"
        elif "pnpm-lock.yaml" in file_names:
            package_manager = "pnpm"
        elif "Pipfile" in file_names or "Pipfile.lock" in file_names:
            package_manager = "pipenv"
        elif "poetry.lock" in file_names:
            package_manager = "poetry"
        elif "requirements.txt" in file_names or "pyproject.toml" in file_names:
            package_manager = "pip"

        # Content/Dependency heuristics
        deps_content = ""
        
        # Read package.json dependencies
        pkg_json_path = self.repo_path / "package.json"
        if pkg_json_path.exists():
            try:
                with open(pkg_json_path, "r", encoding="utf-8") as f:
                    pkg_data = json.load(f)
                    deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                    deps_content += " ".join(deps.keys()).lower()
            except Exception:
                pass

        # Read requirements.txt dependencies
        req_txt_path = self.repo_path / "requirements.txt"
        if req_txt_path.exists():
            try:
                with open(req_txt_path, "r", encoding="utf-8") as f:
                    deps_content += " " + f.read().lower()
            except Exception:
                pass

        # Read pyproject.toml dependencies
        pyproject_path = self.repo_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    deps_content += " " + f.read().lower()
            except Exception:
                pass

        # Backend Framework Heuristics
        if "express" in deps_content:
            backend_framework = "Express"
        elif "fastapi" in deps_content:
            backend_framework = "FastAPI"
        elif "django" in deps_content:
            backend_framework = "Django"
        elif "flask" in deps_content:
            backend_framework = "Flask"
        elif "nestjs" in deps_content or "@nest" in deps_content:
            backend_framework = "NestJS"
        elif "koa" in deps_content:
            backend_framework = "Koa"
        elif "next" in deps_content:
            backend_framework = "Next.js"

        # Frontend Framework Heuristics
        if "next" in deps_content:
            frontend_framework = "Next.js"
        elif "react" in deps_content:
            frontend_framework = "React"
        elif "vue" in deps_content:
            frontend_framework = "Vue"
        elif "angular" in deps_content or "@angular/core" in deps_content:
            frontend_framework = "Angular"
        elif "svelte" in deps_content:
            frontend_framework = "Svelte"

        # Main overall framework decision
        if backend_framework != "Unknown" and frontend_framework != "Unknown":
            framework = f"{backend_framework} / {frontend_framework}" if backend_framework != frontend_framework else backend_framework
        elif backend_framework != "Unknown":
            framework = backend_framework
        elif frontend_framework != "Unknown":
            framework = frontend_framework
        else:
            framework = "Unknown"

        # Database Heuristics
        if "mongoose" in deps_content or "mongodb" in deps_content:
            database = "MongoDB"
        elif "pg" in deps_content or "psycopg2" in deps_content or ("sqlalchemy" in deps_content and "postgres" in deps_content):
            database = "PostgreSQL"
        elif "mysql" in deps_content or "mysql2" in deps_content:
            database = "MySQL"
        elif "sqlite3" in deps_content or "sqlite" in deps_content:
            database = "SQLite"
        elif "prisma" in deps_content:
            database = "Prisma ORM"
        elif "typeorm" in deps_content:
            database = "TypeORM"
        elif any("db" in p or "models" in p for p in file_paths_str):
            database = "Detectable via models/schema"

        return primary_language, framework, backend_framework, frontend_framework, database, package_manager

    def build_summary(self) -> RepositorySummary:
        """
        Builds a comprehensive summary of the repository.

        Returns:
            RepositorySummary: Structured object containing scanned file info, project architecture intelligence.
        """
        logger.agent("Explorer", "Building repository summary...")
        relative_files = self.scan_repository()

        file_metadata_list: List[FileMetadata] = []
        languages_count: Dict[str, int] = {}
        important_files_found: List[str] = []
        routes_found: List[str] = []
        models_found: List[str] = []
        controllers_found: List[str] = []
        services_found: List[str] = []

        for rel_path in relative_files:
            abs_path = self.repo_path / rel_path
            
            # File Stats
            size_bytes = abs_path.stat().st_size if abs_path.exists() else 0
            ext = rel_path.suffix.lower()
            lang = self.EXTENSION_LANGUAGE_MAP.get(ext, "Other")

            file_metadata_list.append(
                FileMetadata(
                    path=rel_path,
                    size_bytes=size_bytes,
                    extension=ext,
                    language=lang,
                )
            )

            # Language aggregation
            if lang != "Other":
                languages_count[lang] = languages_count.get(lang, 0) + 1

            # Important file identification
            if rel_path.name in self.IMPORTANT_FILES or rel_path.name.startswith(".env"):
                important_files_found.append(str(rel_path))

            # Important folder / component classification
            parts_lower = [p.lower() for p in rel_path.parts]
            path_str = str(rel_path)

            if "routes" in parts_lower or "route" in parts_lower or "routes" in rel_path.name.lower():
                routes_found.append(path_str)
            if "models" in parts_lower or "model" in parts_lower or "model" in rel_path.name.lower():
                models_found.append(path_str)
            if "controllers" in parts_lower or "controller" in parts_lower or "controller" in rel_path.name.lower():
                controllers_found.append(path_str)
            if "services" in parts_lower or "service" in parts_lower or "service" in rel_path.name.lower():
                services_found.append(path_str)

        (
            primary_lang,
            framework,
            backend_fw,
            frontend_fw,
            database,
            pkg_mgr,
        ) = self._infer_project_info(relative_files, languages_count)

        summary = RepositorySummary(
            repo_path=self.repo_path,
            total_files=len(relative_files),
            files=file_metadata_list,
            structure={},
            languages=languages_count,
            primary_language=primary_lang,
            framework=framework,
            backend_framework=backend_fw,
            frontend_framework=frontend_fw,
            database=database,
            package_manager=pkg_mgr,
            important_files=sorted(important_files_found),
            routes=sorted(routes_found),
            models=sorted(models_found),
            controllers=sorted(controllers_found),
            services=sorted(services_found),
        )

        logger.success(f"Built repository summary ({summary.total_files} files scanned).")
        self.print_rich_summary(summary)
        return summary

    def print_rich_summary(self, summary: RepositorySummary) -> None:
        """
        Prints a clean, formatted summary using Rich Console.

        Args:
            summary (RepositorySummary): Repository summary instance.
        """
        table = Table(title="Repository Summary", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", width=20)
        table.add_column("Details", style="white")

        table.add_row("Framework", summary.framework)
        table.add_row("Language", summary.primary_language)
        table.add_row("Database", summary.database)
        table.add_row("Package Manager", summary.package_manager)
        table.add_row("Files Scanned", str(summary.total_files))
        table.add_row("Important Files", f"{len(summary.important_files)} ({', '.join(summary.important_files[:4])}{'...' if len(summary.important_files) > 4 else ''})")
        table.add_row("Routes", f"{len(summary.routes)}")
        table.add_row("Models", f"{len(summary.models)}")
        table.add_row("Controllers", f"{len(summary.controllers)}")
        table.add_row("Services", f"{len(summary.services)}")

        console.print()
        console.print(table)
        console.print()
