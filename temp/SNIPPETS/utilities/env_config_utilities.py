"""
Environment Configuration Utilities

Description: Utilities for loading and validating environment variables with type conversion,
default values, and required field checking. Essential for 12-factor app configuration.

Use Cases:
- Loading API keys and secrets from environment
- Type-safe environment variable parsing
- Configuration validation on startup
- Multi-environment configuration (dev, staging, prod)
- Feature flags and application settings

Dependencies:
- os (stdlib)
- typing (stdlib)
- Optional: python-dotenv for .env file support

Notes:
- Type conversion with validation
- Required vs optional environment variables
- Clear error messages for missing configuration
- Support for .env files
- No external dependencies required (dotenv is optional)

Related Snippets:
- /home/coolhand/SNIPPETS/configuration-management/multi_source_config.py - Advanced config
- /home/coolhand/SNIPPETS/utilities/logging_utilities.py - Config logging

Source Attribution:
- Extracted from: /home/coolhand/shared/utils/__init__.py
- Related patterns: /home/coolhand/projects/swarm/core/core_cli.py
- Author: Luke Steuber
"""

import os
from typing import Any, Optional, TypeVar, Callable, Dict, List, Union
import logging


logger = logging.getLogger(__name__)

T = TypeVar('T')


def get_env_var(
    key: str,
    default: Any = None,
    required: bool = False,
    var_type: type = str
) -> Any:
    """
    Get environment variable with type conversion and validation.

    Args:
        key: Environment variable name
        default: Default value if not found
        required: If True, raise ValueError if not found
        var_type: Type to convert to (str, int, float, bool)

    Returns:
        Environment variable value converted to specified type

    Raises:
        ValueError: If required=True and variable not found
        ValueError: If type conversion fails

    Example:
        >>> # String value (default)
        >>> api_key = get_env_var("API_KEY", required=True)
        >>>
        >>> # Integer with default
        >>> port = get_env_var("PORT", default=8080, var_type=int)
        >>>
        >>> # Boolean flag
        >>> debug = get_env_var("DEBUG", default=False, var_type=bool)
        >>>
        >>> # Float value
        >>> timeout = get_env_var("TIMEOUT", default=30.0, var_type=float)
    """
    value = os.getenv(key)

    # Check if required
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")

    # Use default if not found
    if value is None:
        return default

    # Type conversion
    try:
        if var_type == bool:
            # Special handling for boolean values
            return value.lower() in ('true', '1', 'yes', 'on')
        elif var_type == int:
            return int(value)
        elif var_type == float:
            return float(value)
        else:
            return str(value)
    except (ValueError, AttributeError) as e:
        raise ValueError(
            f"Failed to convert environment variable '{key}' to {var_type.__name__}: {e}"
        )


def get_env_list(
    key: str,
    default: Optional[List[str]] = None,
    separator: str = ",",
    required: bool = False
) -> List[str]:
    """
    Get environment variable as a list.

    Args:
        key: Environment variable name
        default: Default list if not found
        separator: Separator character (default: comma)
        required: If True, raise ValueError if not found

    Returns:
        List of strings

    Example:
        >>> # Comma-separated list
        >>> hosts = get_env_list("ALLOWED_HOSTS", default=["localhost"])
        >>>
        >>> # Semicolon-separated
        >>> paths = get_env_list("SEARCH_PATHS", separator=";")
    """
    value = os.getenv(key)

    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")

    if value is None:
        return default or []

    # Split and strip whitespace
    return [item.strip() for item in value.split(separator) if item.strip()]


def get_env_dict(
    key: str,
    default: Optional[Dict[str, str]] = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
    required: bool = False
) -> Dict[str, str]:
    """
    Get environment variable as a dictionary.

    Args:
        key: Environment variable name
        default: Default dict if not found
        item_separator: Separator between items (default: comma)
        key_value_separator: Separator between key and value (default: equals)
        required: If True, raise ValueError if not found

    Returns:
        Dictionary of key-value pairs

    Example:
        >>> # Parse "key1=val1,key2=val2"
        >>> config = get_env_dict("APP_CONFIG")
        >>>
        >>> # Custom separators "key1:val1;key2:val2"
        >>> config = get_env_dict(
        ...     "APP_CONFIG",
        ...     item_separator=";",
        ...     key_value_separator=":"
        ... )
    """
    value = os.getenv(key)

    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")

    if value is None:
        return default or {}

    result = {}
    for item in value.split(item_separator):
        item = item.strip()
        if not item:
            continue

        if key_value_separator not in item:
            logger.warning(
                f"Invalid key-value pair in {key}: '{item}' "
                f"(missing '{key_value_separator}')"
            )
            continue

        k, v = item.split(key_value_separator, 1)
        result[k.strip()] = v.strip()

    return result


class EnvConfig:
    """
    Configuration manager for environment variables with validation.

    Provides a structured way to define and load environment configuration
    with type checking and validation.

    Example:
        >>> class AppConfig(EnvConfig):
        ...     # Required string
        ...     API_KEY: str = EnvConfig.required()
        ...
        ...     # Optional with default
        ...     PORT: int = EnvConfig.optional(8080)
        ...
        ...     # Boolean flag
        ...     DEBUG: bool = EnvConfig.optional(False)
        >>>
        >>> config = AppConfig.load()
        >>> print(config.API_KEY)
        >>> print(config.PORT)
    """

    @staticmethod
    def required(var_type: type = str):
        """Mark field as required environment variable."""
        return {"required": True, "type": var_type}

    @staticmethod
    def optional(default: Any, var_type: Optional[type] = None):
        """Mark field as optional with default value."""
        if var_type is None:
            var_type = type(default)
        return {"required": False, "default": default, "type": var_type}

    @classmethod
    def load(cls):
        """
        Load configuration from environment variables.

        Returns:
            Instance of config class with populated values

        Raises:
            ValueError: If required variables are missing
        """
        instance = cls()

        for attr_name in dir(cls):
            # Skip private/magic attributes
            if attr_name.startswith('_'):
                continue

            attr_value = getattr(cls, attr_name)

            # Skip methods and non-config attributes
            if not isinstance(attr_value, dict):
                continue

            # Get environment variable
            env_value = get_env_var(
                attr_name,
                default=attr_value.get("default"),
                required=attr_value.get("required", False),
                var_type=attr_value.get("type", str)
            )

            setattr(instance, attr_name, env_value)

        return instance


def load_dotenv_file(dotenv_path: str = ".env") -> bool:
    """
    Load environment variables from .env file.

    Args:
        dotenv_path: Path to .env file (default: .env)

    Returns:
        True if file was loaded, False otherwise

    Example:
        >>> # Load .env from current directory
        >>> load_dotenv_file()
        >>>
        >>> # Load from custom path
        >>> load_dotenv_file("/path/to/config/.env")
    """
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)
        logger.info(f"Loaded environment from {dotenv_path}")
        return True
    except ImportError:
        logger.warning(
            "python-dotenv not installed. "
            "Install with: pip install python-dotenv"
        )
        return False
    except FileNotFoundError:
        logger.warning(f".env file not found at {dotenv_path}")
        return False


def validate_required_env_vars(*keys: str) -> Dict[str, str]:
    """
    Validate that required environment variables are set.

    Args:
        *keys: Environment variable names to check

    Returns:
        Dictionary of found environment variables

    Raises:
        ValueError: If any required variables are missing

    Example:
        >>> # Check multiple required variables
        >>> env_vars = validate_required_env_vars(
        ...     "DATABASE_URL",
        ...     "API_KEY",
        ...     "SECRET_KEY"
        ... )
    """
    missing = []
    found = {}

    for key in keys:
        value = os.getenv(key)
        if value is None:
            missing.append(key)
        else:
            found[key] = value

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return found


def env_or_file(
    env_key: str,
    file_path_key: Optional[str] = None,
    required: bool = False
) -> Optional[str]:
    """
    Get value from environment or read from file.

    Useful for secrets that can be provided via environment variable
    or mounted as files (e.g., Kubernetes secrets).

    Args:
        env_key: Environment variable name
        file_path_key: Environment variable containing file path
        required: If True, raise ValueError if not found

    Returns:
        Value from environment or file contents

    Example:
        >>> # Try env var first, then file
        >>> secret = env_or_file(
        ...     "API_KEY",
        ...     "API_KEY_FILE",
        ...     required=True
        ... )
    """
    # Try environment variable first
    value = os.getenv(env_key)
    if value:
        return value

    # Try file path
    if file_path_key:
        file_path = os.getenv(file_path_key)
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Failed to read {file_path}: {e}")

    if required:
        raise ValueError(
            f"Required value not found in {env_key} "
            f"or file at {file_path_key}"
        )

    return None


# Example usage and testing
if __name__ == "__main__":
    print("Environment Configuration Utilities Examples")
    print("=" * 60)

    # Set some example environment variables
    os.environ["API_KEY"] = "test-api-key-123"
    os.environ["PORT"] = "8080"
    os.environ["DEBUG"] = "true"
    os.environ["TIMEOUT"] = "30.5"
    os.environ["ALLOWED_HOSTS"] = "localhost,example.com,api.example.com"
    os.environ["DATABASE_CONFIG"] = "host=localhost,port=5432,db=mydb"

    # Example 1: Basic environment variable retrieval
    print("\n1. Basic Environment Variable Retrieval")
    print("-" * 60)

    api_key = get_env_var("API_KEY", required=True)
    print(f"API_KEY: {api_key}")

    port = get_env_var("PORT", default=3000, var_type=int)
    print(f"PORT: {port} (type: {type(port).__name__})")

    debug = get_env_var("DEBUG", default=False, var_type=bool)
    print(f"DEBUG: {debug} (type: {type(debug).__name__})")

    timeout = get_env_var("TIMEOUT", default=10.0, var_type=float)
    print(f"TIMEOUT: {timeout} (type: {type(timeout).__name__})")

    # Example 2: List values
    print("\n2. Environment Variable as List")
    print("-" * 60)

    hosts = get_env_list("ALLOWED_HOSTS")
    print(f"ALLOWED_HOSTS: {hosts}")

    # Example 3: Dictionary values
    print("\n3. Environment Variable as Dictionary")
    print("-" * 60)

    db_config = get_env_dict("DATABASE_CONFIG")
    print(f"DATABASE_CONFIG: {db_config}")

    # Example 4: Configuration class
    print("\n4. Configuration Class")
    print("-" * 60)

    class AppConfig(EnvConfig):
        API_KEY: str = EnvConfig.required()
        PORT: int = EnvConfig.optional(8080)
        DEBUG: bool = EnvConfig.optional(False)
        TIMEOUT: float = EnvConfig.optional(30.0)

    try:
        config = AppConfig.load()
        print(f"Config loaded:")
        print(f"  API_KEY: {config.API_KEY}")
        print(f"  PORT: {config.PORT}")
        print(f"  DEBUG: {config.DEBUG}")
        print(f"  TIMEOUT: {config.TIMEOUT}")
    except ValueError as e:
        print(f"Configuration error: {e}")

    # Example 5: Validation
    print("\n5. Validate Required Variables")
    print("-" * 60)

    try:
        required_vars = validate_required_env_vars("API_KEY", "PORT")
        print(f"All required variables present: {list(required_vars.keys())}")
    except ValueError as e:
        print(f"Validation failed: {e}")

    # Example 6: Missing variable with default
    print("\n6. Missing Variable with Default")
    print("-" * 60)

    missing = get_env_var("MISSING_VAR", default="default_value")
    print(f"MISSING_VAR: {missing}")

    print("\n" + "=" * 60)
    print("All examples completed!")
