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
    """
    repo_path: Path
    total_files: int = 0
    files: List[FileMetadata] = field(default_factory=list)
    structure: Dict[str, Any] = field(default_factory=dict)
    languages: Dict[str, int] = field(default_factory=dict)

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
        }
