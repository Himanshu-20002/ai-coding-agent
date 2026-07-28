"""
Configuration module initialization.

JS/Node.js comparison:
In Node.js (CommonJS or ES Modules), folders are made package-like via package.json or index.js.
In Python, an '__init__.py' file marks a directory as a Python package, allowing imports like:
`from config.settings import settings`
"""

from config.settings import Settings, settings

__all__ = ["Settings", "settings"]
