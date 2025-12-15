"""
Geepers - Multi-agent orchestration system with MCP tools and Claude Code plugin agents.

Author: Luke Steuber
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Luke Steuber"

from .config import ConfigManager

# Make submodules easily accessible
from . import mcp
from . import orchestrators
from . import utils
from . import naming
from . import parser

__all__ = [
    "ConfigManager",
    "mcp",
    "orchestrators",
    "utils",
    "naming",
    "parser",
    "__version__",
    "__author__",
]
