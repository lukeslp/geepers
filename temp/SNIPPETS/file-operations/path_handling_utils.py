"""
Path Handling Utilities with pathlib

Description: Modern path manipulation utilities using pathlib.Path for cross-platform
compatibility. Includes path resolution, validation, creation, and common operations.

Use Cases:
- Cross-platform file path handling (Windows, Linux, Mac)
- Project directory structure management
- Safe path operations with validation
- Finding project root or config directories
- Path normalization and resolution

Dependencies:
- pathlib (stdlib)
- os (stdlib)
- typing (stdlib)

Notes:
- Always use Path objects instead of string concatenation for paths
- Use resolve() to get absolute paths and resolve symlinks
- Use exists() to check before operations
- Use is_file() / is_dir() for type checking
- forward slashes (/) work on all platforms with pathlib
- Path.home() for user directory, Path.cwd() for current directory

Related Snippets:
- file-operations/config_file_loading.py - Config file path handling
- file-operations/directory_traversal.py - Directory walking patterns

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/core/core_config.py
- Related patterns: /home/coolhand/enterprise_orchestration/cli.py
- Author: Luke Steuber
"""

import os
from pathlib import Path
from typing import Optional, Union, List, Tuple
import logging

logger = logging.getLogger(__name__)


def ensure_absolute_path(path: Union[str, Path]) -> Path:
    """
    Convert any path to an absolute Path object.

    Args:
        path: Path string or Path object

    Returns:
        Absolute Path object

    Examples:
        >>> ensure_absolute_path("./config.json")
        PosixPath('/home/user/project/config.json')
        >>> ensure_absolute_path("~/Documents")
        PosixPath('/home/user/Documents')
    """
    path = Path(path)

    # Expand user directory (~)
    if str(path).startswith('~'):
        path = path.expanduser()

    # Convert to absolute path
    if not path.is_absolute():
        path = path.resolve()

    return path


def find_project_root(
    start_path: Optional[Union[str, Path]] = None,
    markers: Optional[List[str]] = None
) -> Optional[Path]:
    """
    Find project root by looking for marker files/directories.

    Common markers: .git, pyproject.toml, setup.py, package.json

    Args:
        start_path: Directory to start searching from (defaults to cwd)
        markers: List of marker files/dirs to look for

    Returns:
        Path to project root, or None if not found

    Examples:
        >>> root = find_project_root(markers=['.git', 'pyproject.toml'])
        >>> print(root)
        /home/user/my-project
    """
    if markers is None:
        markers = ['.git', 'pyproject.toml', 'setup.py', '.swarm', 'package.json']

    current = Path(start_path) if start_path else Path.cwd()
    current = current.resolve()

    # Walk up the directory tree
    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent

    return None


def ensure_dir_exists(path: Union[str, Path], parents: bool = True) -> Path:
    """
    Ensure directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure
        parents: Create parent directories if needed

    Returns:
        Path object of the directory

    Raises:
        FileExistsError: If path exists but is not a directory

    Examples:
        >>> data_dir = ensure_dir_exists("./data/cache")
        >>> data_dir.exists()
        True
    """
    path = Path(path)

    if path.exists():
        if not path.is_dir():
            raise FileExistsError(f"Path exists but is not a directory: {path}")
    else:
        path.mkdir(parents=parents, exist_ok=True)

    return path


def get_config_path(
    base_dir: Optional[Union[str, Path]] = None,
    config_name: str = '.config',
    create: bool = False
) -> Path:
    """
    Get path to configuration directory following XDG conventions.

    Args:
        base_dir: Base directory (defaults to current working directory)
        config_name: Name of config file/directory
        create: Create directory if it doesn't exist

    Returns:
        Path to config directory

    Examples:
        >>> config_dir = get_config_path(config_name='.swarm')
        >>> config_file = config_dir / 'settings.yaml'
    """
    base_dir = Path(base_dir) if base_dir else Path.cwd()

    # Check in base directory first
    config_path = base_dir / config_name

    # If not found, check in user's home directory
    if not config_path.exists():
        config_path = Path.home() / config_name

    if create and not config_path.exists():
        if '.' in config_name and not config_name.endswith('/'):
            # It's a file, create parent directory
            config_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            # It's a directory
            config_path.mkdir(parents=True, exist_ok=True)

    return config_path


def safe_join(*paths: Union[str, Path]) -> Path:
    """
    Safely join path components, preventing directory traversal attacks.

    Ensures the final path is within the first component (base directory).

    Args:
        *paths: Path components to join

    Returns:
        Joined Path object

    Raises:
        ValueError: If path traversal detected

    Examples:
        >>> safe_join("/var/www", "uploads", "file.txt")
        PosixPath('/var/www/uploads/file.txt')
        >>> safe_join("/var/www", "../etc/passwd")  # Raises ValueError
    """
    if not paths:
        raise ValueError("At least one path component required")

    base = Path(paths[0]).resolve()
    result = base

    for component in paths[1:]:
        # Join and resolve
        result = (result / component).resolve()

        # Check if result is within base
        try:
            result.relative_to(base)
        except ValueError:
            raise ValueError(
                f"Path traversal detected: {component} would escape {base}"
            )

    return result


def get_file_extension(path: Union[str, Path], include_dot: bool = True) -> str:
    """
    Get file extension from path.

    Args:
        path: File path
        include_dot: Include leading dot in extension

    Returns:
        File extension

    Examples:
        >>> get_file_extension("data.json")
        '.json'
        >>> get_file_extension("data.tar.gz", include_dot=False)
        'gz'
    """
    path = Path(path)

    if include_dot:
        return path.suffix
    else:
        return path.suffix.lstrip('.')


def change_extension(path: Union[str, Path], new_ext: str) -> Path:
    """
    Change file extension.

    Args:
        path: Original file path
        new_ext: New extension (with or without leading dot)

    Returns:
        Path with new extension

    Examples:
        >>> change_extension("data.json", ".yaml")
        PosixPath('data.yaml')
        >>> change_extension("report.txt", "md")
        PosixPath('report.md')
    """
    path = Path(path)

    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext

    return path.with_suffix(new_ext)


def find_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
    files_only: bool = True
) -> List[Path]:
    """
    Find files matching a pattern in a directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern (e.g., "*.py", "test_*.json")
        recursive: Search subdirectories recursively
        files_only: Only return files (not directories)

    Returns:
        List of matching Path objects

    Examples:
        >>> py_files = find_files("./src", "*.py", recursive=True)
        >>> test_files = find_files("./tests", "test_*.py")
    """
    directory = Path(directory)

    if not directory.exists():
        return []

    if recursive:
        matches = directory.rglob(pattern)
    else:
        matches = directory.glob(pattern)

    if files_only:
        return [p for p in matches if p.is_file()]
    else:
        return list(matches)


def get_relative_path(
    path: Union[str, Path],
    base: Optional[Union[str, Path]] = None
) -> Path:
    """
    Get relative path from base directory.

    Args:
        path: Path to make relative
        base: Base directory (defaults to cwd)

    Returns:
        Relative path

    Examples:
        >>> get_relative_path("/home/user/project/src/main.py", "/home/user/project")
        PosixPath('src/main.py')
    """
    path = Path(path).resolve()
    base = Path(base).resolve() if base else Path.cwd()

    try:
        return path.relative_to(base)
    except ValueError:
        # Paths are not related, return absolute path
        return path


def split_path(path: Union[str, Path]) -> Tuple[Path, str]:
    """
    Split path into directory and filename.

    Args:
        path: File path

    Returns:
        Tuple of (directory Path, filename string)

    Examples:
        >>> dir_path, filename = split_path("/home/user/data.json")
        >>> print(dir_path, filename)
        /home/user data.json
    """
    path = Path(path)
    return path.parent, path.name


def normalize_path(path: Union[str, Path]) -> Path:
    """
    Normalize path: resolve symlinks, remove redundant separators, etc.

    Args:
        path: Path to normalize

    Returns:
        Normalized Path object

    Examples:
        >>> normalize_path("./data/../config/./settings.json")
        PosixPath('/home/user/project/config/settings.json')
    """
    return Path(path).resolve()


# =============================================================================
# Usage Examples
# =============================================================================

if __name__ == "__main__":
    import tempfile
    import shutil

    print("=== Path Handling Utilities Examples ===\n")

    # Create temporary directory for examples
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Using temporary directory: {temp_dir}\n")

    try:
        # Example 1: Ensure absolute path
        print("1. Ensure absolute path:")
        rel_path = "./config.json"
        abs_path = ensure_absolute_path(rel_path)
        print(f"   Relative: {rel_path}")
        print(f"   Absolute: {abs_path}")

        # Example 2: Ensure directory exists
        print("\n2. Ensure directory exists:")
        data_dir = temp_dir / "data" / "cache"
        ensure_dir_exists(data_dir)
        print(f"   Created: {data_dir}")
        print(f"   Exists: {data_dir.exists()}")

        # Example 3: Safe path joining
        print("\n3. Safe path joining:")
        safe_path = safe_join(temp_dir, "uploads", "file.txt")
        print(f"   Joined: {safe_path}")

        try:
            dangerous_path = safe_join(temp_dir, "../etc/passwd")
        except ValueError as e:
            print(f"   Prevented traversal: {e}")

        # Example 4: File extension operations
        print("\n4. File extension operations:")
        filename = "data.json"
        ext = get_file_extension(filename)
        new_path = change_extension(filename, ".yaml")
        print(f"   Original: {filename}")
        print(f"   Extension: {ext}")
        print(f"   Changed to: {new_path}")

        # Example 5: Find files
        print("\n5. Find files by pattern:")
        # Create some test files
        (temp_dir / "test1.py").touch()
        (temp_dir / "test2.py").touch()
        (temp_dir / "data.json").touch()

        py_files = find_files(temp_dir, "*.py")
        print(f"   Python files found: {[f.name for f in py_files]}")

        # Example 6: Project root finding
        print("\n6. Find project root:")
        # Create a marker file
        (temp_dir / ".git").mkdir()
        project_root = find_project_root(temp_dir, markers=['.git'])
        print(f"   Project root: {project_root}")

        # Example 7: Relative paths
        print("\n7. Get relative path:")
        file_path = temp_dir / "src" / "main.py"
        rel = get_relative_path(file_path, temp_dir)
        print(f"   Absolute: {file_path}")
        print(f"   Relative to {temp_dir.name}: {rel}")

        # Example 8: Path normalization
        print("\n8. Path normalization:")
        messy_path = temp_dir / "data" / ".." / "config" / "." / "settings.json"
        normalized = normalize_path(messy_path)
        print(f"   Messy: {messy_path}")
        print(f"   Normalized: {normalized}")

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary directory")

    print("\nAll examples completed successfully!")
