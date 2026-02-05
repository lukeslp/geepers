"""
Graceful Import Fallbacks Pattern

Description: Robust pattern for handling optional dependencies and providing
graceful degradation when imports fail. Enables modules to work in both
full-featured and minimal modes.

Use Cases:
- Building modules that work with or without optional dependencies
- Creating standalone tools that don't require full ecosystem
- Providing fallback implementations when packages unavailable
- Development vs. production dependency management
- Cross-environment compatibility (different Python versions, OS)

Dependencies:
- sys (built-in)
- traceback (built-in)
- logging (built-in)
- typing (built-in)

Notes:
- Always provide meaningful error messages about what's missing
- Implement minimal fallbacks for critical functionality
- Use feature flags to track what's available
- Document which features require which dependencies
- Fail fast for truly required dependencies
- Provide helpful installation instructions in error messages

Related Snippets:
- /home/coolhand/SNIPPETS/configuration-management/multi_source_config.py
- /home/coolhand/SNIPPETS/cli-tools/interactive_cli_pattern.py
- /home/coolhand/SNIPPETS/tool-registration/swarm_module_pattern.py

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/hive/swarm_template.py
- Pattern used across: All swarm modules and tool systems
"""

import sys
import logging
import traceback
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

# ============================================================================
# BASIC PATTERN: Try-Except with Fallback
# ============================================================================

# --- Optional Rich Console ---
try:
    from rich.console import Console
    from rich.table import Table
    from rich.markdown import Markdown

    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None


# --- Optional Requests (with fallback to urllib) ---
try:
    import requests
    HTTP_CLIENT = "requests"
except ImportError:
    import urllib.request
    HTTP_CLIENT = "urllib"


def make_http_request(url: str) -> str:
    """
    Make HTTP request with automatic fallback.

    Uses requests if available, otherwise falls back to urllib.
    """
    if HTTP_CLIENT == "requests":
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    else:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')


# ============================================================================
# INTERMEDIATE: Feature Flags and Warnings
# ============================================================================

class FeatureFlags:
    """Track available features based on successful imports."""

    def __init__(self):
        self.features: Dict[str, bool] = {}
        self.missing_packages: Dict[str, str] = {}
        self.logger = logging.getLogger("features")

    def register_feature(self,
                        feature_name: str,
                        import_func: Callable,
                        install_hint: str = ""):
        """
        Register a feature with automatic availability detection.

        Args:
            feature_name: Name of the feature
            import_func: Function that performs the import
            install_hint: Installation instructions for the package
        """
        try:
            import_func()
            self.features[feature_name] = True
            self.logger.debug(f"Feature '{feature_name}' available")
        except ImportError as e:
            self.features[feature_name] = False
            self.missing_packages[feature_name] = install_hint or str(e)
            self.logger.warning(
                f"Feature '{feature_name}' unavailable: {e}\n"
                f"Install with: {install_hint}" if install_hint else ""
            )

    def require_feature(self, feature_name: str):
        """
        Require a feature, raising error if unavailable.

        Args:
            feature_name: Name of required feature

        Raises:
            ImportError: If feature is not available
        """
        if not self.features.get(feature_name, False):
            hint = self.missing_packages.get(feature_name, "")
            raise ImportError(
                f"Required feature '{feature_name}' is not available.\n{hint}"
            )

    def has_feature(self, feature_name: str) -> bool:
        """Check if a feature is available."""
        return self.features.get(feature_name, False)


# Usage example
features = FeatureFlags()

features.register_feature(
    "ai_providers",
    lambda: __import__("openai"),
    "pip install openai"
)

features.register_feature(
    "advanced_cli",
    lambda: __import__("rich"),
    "pip install rich"
)


# ============================================================================
# ADVANCED: Lazy Import with Proxy Objects
# ============================================================================

class LazyImport:
    """
    Lazy import proxy that only imports when actually used.

    Useful for expensive imports that may not be needed.
    """

    def __init__(self, module_name: str, install_hint: str = ""):
        self._module_name = module_name
        self._module = None
        self._install_hint = install_hint

    def _import_module(self):
        """Perform the actual import."""
        if self._module is None:
            try:
                self._module = __import__(self._module_name)
            except ImportError as e:
                error_msg = f"Module '{self._module_name}' not available"
                if self._install_hint:
                    error_msg += f"\nInstall with: {self._install_hint}"
                raise ImportError(error_msg) from e

    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to the real module."""
        self._import_module()
        return getattr(self._module, name)

    def __call__(self, *args, **kwargs):
        """Support callable modules."""
        self._import_module()
        return self._module(*args, **kwargs)


# Usage
numpy = LazyImport("numpy", "pip install numpy")
pandas = LazyImport("pandas", "pip install pandas")

# Import only happens when actually used
# array = numpy.array([1, 2, 3])  # Import happens here


# ============================================================================
# FALLBACK IMPLEMENTATION PATTERN
# ============================================================================

# --- Example: CLI Styling with Fallback ---

try:
    from rich import print as rich_print
    from rich.console import Console
    _console = Console()

    def print_styled(text: str, style: str = ""):
        """Print with Rich styling."""
        _console.print(text, style=style)

    def print_table(data: list[dict]):
        """Print data as Rich table."""
        from rich.table import Table
        table = Table()

        if not data:
            return

        # Add columns
        for key in data[0].keys():
            table.add_column(key, style="cyan")

        # Add rows
        for row in data:
            table.add_row(*[str(v) for v in row.values()])

        _console.print(table)

except ImportError:
    # Fallback implementations without Rich

    def print_styled(text: str, style: str = ""):
        """Print without styling (fallback)."""
        print(text)

    def print_table(data: list[dict]):
        """Print data as simple table (fallback)."""
        if not data:
            return

        # Calculate column widths
        headers = list(data[0].keys())
        widths = {h: max(len(h), max(len(str(row[h])) for row in data))
                 for h in headers}

        # Print header
        print(" | ".join(h.ljust(widths[h]) for h in headers))
        print("-" * (sum(widths.values()) + 3 * (len(headers) - 1)))

        # Print rows
        for row in data:
            print(" | ".join(str(row[h]).ljust(widths[h]) for h in headers))


# ============================================================================
# CORE MODULE IMPORTS WITH COMPREHENSIVE FALLBACKS
# ============================================================================

def import_with_fallbacks():
    """
    Example showing comprehensive import strategy for a module
    that can work standalone or integrated.
    """
    CORE_IMPORTS_SUCCESSFUL = False

    try:
        # Try to import core modules
        from core.cli import load_config, CLIStyle, logger
        from core.globals import RICH_AVAILABLE, console
        from core.registry import get_registry

        CORE_IMPORTS_SUCCESSFUL = True

    except ImportError as e:
        print(f"Warning: Core modules unavailable: {e}")
        print("Running in standalone mode with limited functionality")

        # Minimal CLIStyle fallback
        class CLIStyle:
            RESET = "\033[0m"
            BOLD = "\033[1m"
            RED = "\033[31m"
            GREEN = "\033[32m"
            YELLOW = "\033[33m"
            BLUE = "\033[34m"

            @staticmethod
            def style(text: str, *styles: str) -> str:
                if not sys.stdout.isatty():
                    return text
                return "".join(styles) + text + CLIStyle.RESET

        # Minimal config loader
        def load_config(env_path=None, cli_args=None):
            import os
            config = dict(os.environ)
            if cli_args:
                config.update({k.replace("-", "_"): v
                             for k, v in cli_args.items()
                             if v is not None})
            return config

        # Minimal logger
        logger = logging.getLogger(__name__)

        RICH_AVAILABLE = False
        console = None

        def get_registry():
            raise NotImplementedError("Registry not available in standalone mode")

    return CORE_IMPORTS_SUCCESSFUL


# ============================================================================
# CONDITIONAL IMPORTS BASED ON PYTHON VERSION
# ============================================================================

# Type hints that work across Python versions
if sys.version_info >= (3, 10):
    from typing import TypeAlias
    JSONType: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
else:
    from typing import Union
    JSONType = Union[Dict[str, Any], list, str, int, float, bool, None]


# Importlib.metadata backport
try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore


# ============================================================================
# EXAMPLE: COMPLETE MODULE WITH FALLBACKS
# ============================================================================

class RobustModule:
    """
    Example module that gracefully handles missing dependencies.
    """

    def __init__(self):
        self.features = FeatureFlags()

        # Register optional features
        self.features.register_feature(
            "ai",
            lambda: __import__("openai"),
            "pip install openai"
        )

        self.features.register_feature(
            "data_processing",
            lambda: __import__("pandas"),
            "pip install pandas"
        )

        self.features.register_feature(
            "visualization",
            lambda: __import__("matplotlib"),
            "pip install matplotlib"
        )

    def process_data(self, data):
        """Process data with pandas if available, otherwise use built-ins."""
        if self.features.has_feature("data_processing"):
            import pandas as pd
            return pd.DataFrame(data).describe().to_dict()
        else:
            # Fallback implementation
            return {
                "count": len(data),
                "method": "basic (pandas unavailable)"
            }

    def visualize(self, data):
        """Create visualization if matplotlib available."""
        if self.features.has_feature("visualization"):
            import matplotlib.pyplot as plt
            plt.plot(data)
            plt.savefig("output.png")
            return "Visualization saved to output.png"
        else:
            return "Visualization unavailable (install matplotlib)"


if __name__ == "__main__":
    print("Graceful Import Fallbacks Pattern Examples")
    print("=" * 80)

    # Test feature flags
    print("\nAvailable features:")
    for feature, available in features.features.items():
        status = "✓" if available else "✗"
        print(f"  {status} {feature}")

    # Test robust module
    module = RobustModule()
    test_data = [1, 2, 3, 4, 5]

    print("\nProcessing data:")
    print(module.process_data(test_data))

    print("\nVisualization:")
    print(module.visualize(test_data))
