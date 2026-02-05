"""
Dynamic Module Discovery and Loading

Description: Discover and load Python modules dynamically from directories. Includes
pattern-based discovery, safe module loading with error handling, and filtering capabilities.
Essential for plugin architectures and auto-loading tool modules.

Use Cases:
- Building plugin systems that auto-discover modules
- Loading tool modules dynamically for AI agents
- Creating extensible architectures without hardcoded imports
- Testing and development environments with hot-reload
- Module validation and compatibility checking

Dependencies:
- pathlib (stdlib)
- importlib.util (stdlib)
- sys (stdlib)
- typing (stdlib)
- inspect (optional, for advanced introspection)

Notes:
- Always add directory to sys.path before importing
- Use importlib.util.spec_from_file_location for file-based imports
- Handle ImportError and module initialization errors gracefully
- Check for required attributes/functions before registering modules
- Avoid importing __init__.py and __pycache__ files
- Consider module naming conventions (e.g., prefix pattern like "swarm_*.py")

Related Snippets:
- file-operations/path_handling_utils.py - Path utilities
- error-handling/graceful_import_fallbacks.py - Import error handling
- tool-registration/swarm_module_pattern.py - Tool module template

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/core/core_registry.py
- Related patterns: /home/coolhand/projects/swarm/hive/ modules
- Author: Luke Steuber
"""

import sys
import importlib.util
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import logging

logger = logging.getLogger(__name__)


def discover_modules(
    directory_path: str,
    pattern: str = "*.py",
    exclude_patterns: Optional[List[str]] = None,
    required_attrs: Optional[List[str]] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Discover and load Python modules from a directory.

    Args:
        directory_path: Directory to search for modules
        pattern: Glob pattern for module files (default: "*.py")
        exclude_patterns: List of filename patterns to exclude
        required_attrs: List of required module attributes (e.g., ["TOOL_SCHEMAS"])
        verbose: Print discovery progress

    Returns:
        Dictionary mapping module names to loaded module objects

    Examples:
        >>> modules = discover_modules("./plugins", pattern="plugin_*.py")
        >>> print(f"Loaded {len(modules)} plugins")
    """
    if exclude_patterns is None:
        exclude_patterns = ["__init__", "__pycache__", "test_", ".pyc"]

    directory = Path(directory_path)
    if not directory.exists() or not directory.is_dir():
        logger.warning(f"Directory not found: {directory_path}")
        return {}

    # Add directory to sys.path if not present
    parent_dir = str(directory.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    loaded_modules = {}

    # Find all Python files matching pattern
    for file_path in directory.glob(pattern):
        # Skip excluded patterns
        if any(excl in file_path.name for excl in exclude_patterns):
            continue

        module_name = file_path.stem

        try:
            # Load module from file
            module = load_module_from_file(file_path, module_name)

            # Check for required attributes
            if required_attrs:
                missing_attrs = [
                    attr for attr in required_attrs
                    if not hasattr(module, attr)
                ]
                if missing_attrs:
                    if verbose:
                        logger.info(
                            f"Module {module_name} missing required attributes: "
                            f"{missing_attrs}"
                        )
                    continue

            loaded_modules[module_name] = module

            if verbose:
                logger.info(f"Loaded module: {module_name}")

        except Exception as e:
            logger.error(f"Error loading module {file_path}: {e}")
            if verbose:
                import traceback
                traceback.print_exc()

    return loaded_modules


def load_module_from_file(file_path: Path, module_name: Optional[str] = None) -> Any:
    """
    Load a Python module from a file path.

    Args:
        file_path: Path to Python file
        module_name: Name for the module (defaults to file stem)

    Returns:
        Loaded module object

    Raises:
        ImportError: If module cannot be loaded

    Examples:
        >>> module = load_module_from_file(Path("plugins/my_tool.py"))
        >>> tool_func = module.my_function()
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise ImportError(f"Module file not found: {file_path}")

    if module_name is None:
        module_name = file_path.stem

    # Create module spec from file location
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None:
        raise ImportError(f"Could not create module spec for {file_path}")

    # Create module from spec
    module = importlib.util.module_from_spec(spec)

    # Add to sys.modules
    sys.modules[module_name] = module

    # Execute module
    spec.loader.exec_module(module)

    return module


def discover_with_pattern_detection(
    directory_path: str,
    patterns: Optional[List[Tuple[str, ...]]] = None,
    verbose: bool = False
) -> Dict[str, Dict[str, Any]]:
    """
    Discover modules and detect which pattern they follow.

    Common patterns:
    - ("TOOL_SCHEMAS",) - New tool schema constant
    - ("get_tool_schemas", "handle_tool_calls") - Function-based tools
    - ("TOOLS_SCHEMA", "TOOLS_HANDLERS") - Legacy tool pattern
    - ("register_tools",) - Registration function pattern

    Args:
        directory_path: Directory to search
        patterns: List of attribute tuples to detect
        verbose: Print discovery details

    Returns:
        Dictionary with module info including detected pattern

    Examples:
        >>> discovered = discover_with_pattern_detection("./hive")
        >>> for name, info in discovered.items():
        ...     print(f"{name}: {info['pattern']}")
    """
    if patterns is None:
        patterns = [
            ("TOOL_SCHEMAS",),
            ("get_tool_schemas", "handle_tool_calls"),
            ("TOOLS_SCHEMA", "TOOLS_HANDLERS"),
            ("register_tools",),
        ]

    directory = Path(directory_path)
    discovered = {}

    # Load all modules first
    modules = discover_modules(directory_path, verbose=verbose)

    for module_name, module in modules.items():
        # Detect which pattern this module follows
        detected_pattern = None
        for pattern in patterns:
            if all(hasattr(module, attr) for attr in pattern):
                detected_pattern = pattern
                break

        discovered[module_name] = {
            "module": module,
            "pattern": detected_pattern,
            "has_pattern": detected_pattern is not None,
            "attributes": dir(module)
        }

        if verbose and detected_pattern:
            logger.info(f"Module {module_name} matches pattern: {detected_pattern}")

    return discovered


def reload_module(module: Any) -> Any:
    """
    Reload a module (useful for development/testing).

    Args:
        module: Module object to reload

    Returns:
        Reloaded module object

    Examples:
        >>> import my_module
        >>> my_module = reload_module(my_module)
    """
    import importlib
    return importlib.reload(module)


def get_module_functions(
    module: Any,
    filter_prefix: Optional[str] = None,
    exclude_private: bool = True
) -> Dict[str, Callable]:
    """
    Get all functions from a module.

    Args:
        module: Module object
        filter_prefix: Only include functions starting with this prefix
        exclude_private: Exclude functions starting with underscore

    Returns:
        Dictionary mapping function names to function objects

    Examples:
        >>> functions = get_module_functions(my_module, filter_prefix="tool_")
        >>> for name, func in functions.items():
        ...     print(f"Found tool function: {name}")
    """
    import inspect

    functions = {}

    for name, obj in inspect.getmembers(module):
        # Skip if not a function
        if not inspect.isfunction(obj):
            continue

        # Skip private functions if requested
        if exclude_private and name.startswith('_'):
            continue

        # Apply prefix filter if specified
        if filter_prefix and not name.startswith(filter_prefix):
            continue

        functions[name] = obj

    return functions


def validate_module_interface(
    module: Any,
    required_functions: Optional[List[str]] = None,
    required_attrs: Optional[List[str]] = None
) -> Tuple[bool, List[str]]:
    """
    Validate that a module implements a required interface.

    Args:
        module: Module to validate
        required_functions: List of required function names
        required_attrs: List of required attribute names

    Returns:
        Tuple of (is_valid, list of missing items)

    Examples:
        >>> valid, missing = validate_module_interface(
        ...     module,
        ...     required_functions=["handle_tool_calls"],
        ...     required_attrs=["TOOL_SCHEMAS"]
        ... )
        >>> if not valid:
        ...     print(f"Module missing: {missing}")
    """
    import inspect

    missing = []

    if required_functions:
        for func_name in required_functions:
            if not hasattr(module, func_name):
                missing.append(f"function: {func_name}")
            elif not callable(getattr(module, func_name)):
                missing.append(f"callable: {func_name}")

    if required_attrs:
        for attr_name in required_attrs:
            if not hasattr(module, attr_name):
                missing.append(f"attribute: {attr_name}")

    return len(missing) == 0, missing


# =============================================================================
# Usage Examples
# =============================================================================

if __name__ == "__main__":
    import tempfile
    import shutil

    print("=== Module Discovery Examples ===\n")

    # Create temporary directory with mock modules
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Using temporary directory: {temp_dir}\n")

    try:
        # Create mock plugin modules
        print("1. Creating mock plugin modules:")

        # Plugin 1: Standard tool pattern
        plugin1 = temp_dir / "tool_search.py"
        plugin1.write_text("""
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web"
        }
    }
]

def handle_tool_calls(tool_calls, config=None):
    return [{"result": "search executed"}]

def helper_function():
    pass
""")

        # Plugin 2: Registration pattern
        plugin2 = temp_dir / "tool_data.py"
        plugin2.write_text("""
def register_tools(registry):
    registry.register("data_tool", lambda: "data")

def process_data(data):
    return data.upper()
""")

        # Plugin 3: Missing required interface
        plugin3 = temp_dir / "incomplete_tool.py"
        plugin3.write_text("""
# This module is missing required attributes
def some_function():
    pass
""")

        print("   Created 3 mock plugin files")

        # Example 2: Basic discovery
        print("\n2. Discover all modules:")
        modules = discover_modules(temp_dir, verbose=True)
        print(f"   Found {len(modules)} modules: {list(modules.keys())}")

        # Example 3: Discovery with required attributes
        print("\n3. Discover modules with TOOL_SCHEMAS:")
        tool_modules = discover_modules(
            temp_dir,
            required_attrs=["TOOL_SCHEMAS"],
            verbose=True
        )
        print(f"   Found {len(tool_modules)} tool modules")

        # Example 4: Pattern detection
        print("\n4. Detect module patterns:")
        discovered = discover_with_pattern_detection(temp_dir, verbose=True)
        for name, info in discovered.items():
            pattern = info['pattern'] or "No pattern"
            print(f"   {name}: {pattern}")

        # Example 5: Get module functions
        print("\n5. Extract functions from module:")
        if modules:
            first_module = list(modules.values())[0]
            functions = get_module_functions(first_module)
            print(f"   Functions in {list(modules.keys())[0]}:")
            for func_name in functions:
                print(f"     - {func_name}")

        # Example 6: Validate module interface
        print("\n6. Validate module interface:")
        if "tool_search" in modules:
            valid, missing = validate_module_interface(
                modules["tool_search"],
                required_attrs=["TOOL_SCHEMAS"],
                required_functions=["handle_tool_calls"]
            )
            print(f"   Module valid: {valid}")
            if missing:
                print(f"   Missing: {missing}")

        # Example 7: Load specific module
        print("\n7. Load specific module by path:")
        if plugin1.exists():
            module = load_module_from_file(plugin1, "custom_search_tool")
            print(f"   Loaded module: {module.__name__}")
            print(f"   Has TOOL_SCHEMAS: {hasattr(module, 'TOOL_SCHEMAS')}")

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary directory")

    print("\nAll examples completed successfully!")
