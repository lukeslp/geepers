"""
Multi-Format Configuration File Loading

Description: Load configuration from multiple file formats (JSON, YAML, .env) with
type conversion and graceful error handling. Supports hierarchical loading from
multiple sources with proper precedence.

Use Cases:
- Loading application settings from various config file formats
- Supporting both development (.env) and production (YAML/JSON) configs
- Type-safe configuration with automatic conversion (bool, int, float)
- Graceful degradation when YAML library not available

Dependencies:
- pathlib (stdlib)
- json (stdlib)
- os (stdlib)
- Optional: python-dotenv for .env file support
- Optional: pyyaml for YAML file support

Notes:
- Always check file existence before attempting to load
- Handle missing dependencies gracefully (especially PyYAML)
- Provide clear error messages for malformed config files
- Support common config formats: .json, .yaml, .yml, .env, key=value
- Type conversion handles: booleans (true/false), integers, floats, quoted strings

Related Snippets:
- configuration-management/multi_source_config.py - Full multi-source config system
- error-handling/graceful_import_fallbacks.py - Optional dependency handling

Source Attribution:
- Extracted from: /home/coolhand/shared/utils/__init__.py
- Related patterns: /home/coolhand/projects/swarm/core/core_config.py
- Author: Luke Steuber
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


def load_config_file(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from a file with automatic format detection.

    Supports JSON, YAML, and key=value formats.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If file format is not supported or malformed
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    config = {}

    try:
        with open(config_path, 'r') as f:
            # JSON format
            if config_path.suffix == '.json':
                config = json.load(f)

            # YAML format
            elif config_path.suffix in ('.yaml', '.yml'):
                try:
                    import yaml
                    config = yaml.safe_load(f)
                except ImportError:
                    logger.warning(
                        "PyYAML not installed. Install with: pip install pyyaml"
                    )
                    raise ValueError(
                        f"Cannot load YAML file {config_path}: PyYAML not installed. "
                        "Install with: pip install pyyaml"
                    )

            # Key=value format (like .env or .swarm files)
            elif config_path.suffix in ('.env', '.swarm', '') or config_path.name.startswith('.'):
                config = _load_key_value_file(f)

            else:
                raise ValueError(
                    f"Unsupported configuration file format: {config_path.suffix}. "
                    "Supported formats: .json, .yaml, .yml, .env, .swarm, or key=value"
                )

    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON in {config_path}: {e}")
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Error loading configuration from {config_path}: {e}")

    return config


def _load_key_value_file(file_handle) -> Dict[str, Any]:
    """
    Load configuration from key=value format file.

    Handles:
    - Comments (lines starting with #)
    - Quoted strings (single and double quotes)
    - Type conversion (bool, int, float)
    - Empty lines

    Args:
        file_handle: Open file handle

    Returns:
        Configuration dictionary
    """
    config = {}

    for line in file_handle:
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        # Parse KEY=VALUE format
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Handle quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            # Convert to appropriate type
            value = _convert_value_type(value)

            config[key] = value

    return config


def _convert_value_type(value: str) -> Any:
    """
    Convert string value to appropriate Python type.

    Conversion order:
    1. Boolean (true/false, case insensitive)
    2. Integer (all digits)
    3. Float (digits with single decimal point)
    4. String (fallback)

    Args:
        value: String value to convert

    Returns:
        Converted value
    """
    # Boolean conversion
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False

    # Integer conversion
    elif value.isdigit():
        return int(value)

    # Float conversion (handle negative numbers too)
    elif value.replace('.', '', 1).replace('-', '', 1).isdigit() and '.' in value:
        return float(value)

    # String (default)
    return value


def load_config_with_fallback(
    config_path: Optional[Union[str, Path]] = None,
    default_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Load configuration with fallback to default values.

    If config file doesn't exist or can't be loaded, returns default config.

    Args:
        config_path: Path to config file (optional)
        default_config: Default configuration dictionary

    Returns:
        Configuration dictionary
    """
    config = default_config.copy() if default_config else {}

    if config_path and os.path.exists(config_path):
        try:
            loaded_config = load_config_file(config_path)
            config.update(loaded_config)
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")

    return config


def save_config_file(
    config: Dict[str, Any],
    config_path: Union[str, Path],
    format: Optional[str] = None,
    skip_keys: Optional[list] = None
) -> None:
    """
    Save configuration to a file with automatic format detection.

    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the configuration
        format: Force specific format (json, yaml, keyvalue), or auto-detect from extension
        skip_keys: List of key patterns to skip (e.g., ['API_KEY', 'SECRET'])

    Raises:
        ValueError: If format is not supported
    """
    config_path = Path(config_path)
    skip_keys = skip_keys or []

    # Filter out keys to skip
    filtered_config = {
        k: v for k, v in config.items()
        if not any(pattern in k for pattern in skip_keys)
    }

    # Determine format
    if not format:
        if config_path.suffix == '.json':
            format = 'json'
        elif config_path.suffix in ('.yaml', '.yml'):
            format = 'yaml'
        else:
            format = 'keyvalue'

    try:
        with open(config_path, 'w') as f:
            if format == 'json':
                json.dump(filtered_config, f, indent=2)

            elif format == 'yaml':
                try:
                    import yaml
                    yaml.safe_dump(filtered_config, f, default_flow_style=False)
                except ImportError:
                    raise ValueError(
                        "Cannot save YAML file: PyYAML not installed. "
                        "Install with: pip install pyyaml"
                    )

            elif format == 'keyvalue':
                _save_key_value_file(f, filtered_config)

            else:
                raise ValueError(f"Unsupported format: {format}")

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Error saving configuration to {config_path}: {e}")


def _save_key_value_file(file_handle, config: Dict[str, Any]) -> None:
    """
    Save configuration in key=value format.

    Args:
        file_handle: Open file handle
        config: Configuration dictionary
    """
    for key, value in config.items():
        # Format value
        if isinstance(value, str):
            # Handle multiline strings
            if '\n' in value:
                value = f'"""{value}"""'
            else:
                value = f'"{value}"'
        elif isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)

        # Write key-value pair
        file_handle.write(f"{key}={value}\n")


# =============================================================================
# Usage Examples
# =============================================================================

if __name__ == "__main__":
    import tempfile

    print("=== Configuration File Loading Examples ===\n")

    # Example 1: Load JSON config
    print("1. Load JSON configuration:")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            "app_name": "MyApp",
            "debug": True,
            "max_connections": 100,
            "timeout": 30.5
        }, f)
        json_path = f.name

    config = load_config_file(json_path)
    print(f"   Loaded JSON: {config}")
    print(f"   Type of debug: {type(config['debug'])}")
    os.unlink(json_path)

    # Example 2: Load key=value config
    print("\n2. Load key=value configuration:")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("# Application settings\n")
        f.write("APP_NAME=MyApp\n")
        f.write("DEBUG=true\n")
        f.write("MAX_CONNECTIONS=100\n")
        f.write('DATABASE_URL="postgresql://localhost/mydb"\n')
        env_path = f.name

    config = load_config_file(env_path)
    print(f"   Loaded .env: {config}")
    print(f"   Type of DEBUG: {type(config['DEBUG'])}")
    print(f"   Type of MAX_CONNECTIONS: {type(config['MAX_CONNECTIONS'])}")
    os.unlink(env_path)

    # Example 3: Load with fallback
    print("\n3. Load config with fallback:")
    default_config = {"app_name": "DefaultApp", "debug": False, "port": 8000}
    config = load_config_with_fallback("nonexistent.json", default_config)
    print(f"   Config (using defaults): {config}")

    # Example 4: Save configuration
    print("\n4. Save configuration:")
    config = {
        "app_name": "MyApp",
        "debug": True,
        "max_connections": 100,
        "api_key": "secret_key_123",
        "database_password": "super_secret"
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        save_path = f.name

    save_config_file(config, save_path, skip_keys=['api_key', 'password'])

    print(f"   Saved config to: {save_path}")
    with open(save_path) as f:
        print(f"   Contents:\n{f.read()}")
    os.unlink(save_path)

    # Example 5: Error handling
    print("\n5. Error handling:")
    try:
        load_config_file("nonexistent.json")
    except FileNotFoundError as e:
        print(f"   Caught expected error: {e}")

    print("\nAll examples completed successfully!")
