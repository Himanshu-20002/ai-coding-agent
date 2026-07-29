"""
Repository Data Model Module.

Defines structured data representations of scanned repository contents and metadata.

JS/Node.js comparison:
- TS: `interface FileMetadata { path: string; size: number; language: string; }`
- Python: `@dataclass` acts like a strongly typed JS object container with auto-generated boilerplate.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class FileMetadata:
    """
    Metadata representation for an individual file within the repository.

    Attributes:
        path (Path): File path relative to workspace.
        size_bytes (int): File size in bytes.
        extension (str): File extension (e.g., '.py', '.js').
        language (str): Programming language inferred from file type.
    """
    path: Path
    size_bytes: int
    extension: str
    language: str


@dataclass
class RepositorySummary:
    """
    Summary of the scanned target repository.

    Attributes:
        repo_path (Path): Absolute path to the repository directory.
        total_files (int): Total number of relevant files scanned.
        files (List[FileMetadata]): List of file metadata objects.
        structure (Dict[str, Any]): Nested directory structure mapping.
        languages (Dict[str, int]): Count of files grouped by programming language.
        primary_language (str): Primary language detected.
        framework (str): Main framework detected (e.g. Express, FastAPI, Django, React, Next.js).
        backend_framework (str): Backend framework detected.
        frontend_framework (str): Frontend framework detected.
        database (str): Database detected (e.g. MongoDB, PostgreSQL, SQLite, MySQL).
        package_manager (str): Package manager detected (npm, yarn, pnpm, pip, poetry).
        important_files (List[str]): List of key configuration / documentation files found.
        routes (List[str]): List of discovered route file paths.
        models (List[str]): List of discovered model file paths.
        controllers (List[str]): List of discovered controller file paths.
        services (List[str]): List of discovered service file paths.
    """
    repo_path: Path
    total_files: int = 0
    files: List[FileMetadata] = field(default_factory=list)
    structure: Dict[str, Any] = field(default_factory=dict)
    languages: Dict[str, int] = field(default_factory=dict)
    primary_language: str = "Unknown"
    framework: str = "Unknown"
    backend_framework: str = "Unknown"
    frontend_framework: str = "Unknown"
    database: str = "Unknown"
    package_manager: str = "Unknown"
    important_files: List[str] = field(default_factory=list)
    routes: List[str] = field(default_factory=list)
    models: List[str] = field(default_factory=list)
    controllers: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the dataclass instance to a dictionary representation.
        
        JS/Node.js comparison:
        Equivalent to returning a plain JavaScript object or calling JSON.stringify().
        """
        # TODO: Implement serialization logic if needed for JSON reporting
        return {
            "repo_path": str(self.repo_path),
            "total_files": self.total_files,
            "languages": self.languages,
            "primary_language": self.primary_language,
            "framework": self.framework,
            "backend_framework": self.backend_framework,
            "frontend_framework": self.frontend_framework,
            "database": self.database,
            "package_manager": self.package_manager,
            "important_files": self.important_files,
            "routes": self.routes,
            "models": self.models,
            "controllers": self.controllers,
            "services": self.services,
        }
