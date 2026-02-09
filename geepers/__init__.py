"""
Geepers - Multi-agent orchestration system with 70 specialized Claude Code agents.

Author: Luke Steuber
License: MIT
"""

__version__ = "1.0.1"
__author__ = "Luke Steuber"

from .config import ConfigManager

# Make submodules easily accessible
from . import orchestrators
from . import utils
from . import naming
from . import parser

__all__ = [
    "ConfigManager",
    "orchestrators",
    "utils",
    "naming",
    "parser",
    "__version__",
    "__author__",
]
