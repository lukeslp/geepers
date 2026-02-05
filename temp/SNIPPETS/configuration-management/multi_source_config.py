"""
Multi-Source Configuration Pattern

Description: Comprehensive pattern for loading configuration from multiple sources
with proper precedence handling. Supports environment variables, config files,
CLI arguments, and defaults with clear override behavior.

Use Cases:
- Building 12-factor compliant applications
- Supporting multiple deployment environments (dev, staging, prod)
- Allowing user customization without code changes
- Managing API keys and secrets securely
- Hierarchical configuration (system → user → project → environment)

Dependencies:
- os (built-in)
- json (built-in)
- pathlib (built-in)
- typing (built-in)
- dotenv (optional: pip install python-dotenv)
- yaml (optional: pip install pyyaml)

Notes:
- Configuration precedence (highest to lowest):
  1. CLI arguments
  2. Environment variables
  3. Project config file (.swarm, .config.yaml)
  4. User config (~/.config/app/config.yaml)
  5. System config (/etc/app/config.yaml)
  6. Defaults
- Never commit secrets to version control
- Use .env.example to document required variables
- Validate configuration after loading
- Provide clear error messages for missing required config

Related Snippets:
- /home/coolhand/SNIPPETS/error-handling/graceful_import_fallbacks.py
- /home/coolhand/SNIPPETS/cli-tools/argument_parsing_patterns.py
- /home/coolhand/SNIPPETS/utilities/environment_detection.py

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/core/core_cli.py
- Related patterns: /home/coolhand/enterprise_orchestration/
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import logging

# Optional imports with fallbacks
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigurationManager:
    """
    Comprehensive configuration management system.

    Loads configuration from multiple sources with proper precedence.
    """

    def __init__(self,
                 app_name: str = "myapp",
                 config_file_names: Optional[List[str]] = None):
        """
        Initialize configuration manager.

        Args:
            app_name: Application name for default paths
            config_file_names: List of config filenames to search for
        """
        self.app_name = app_name
        self.config_file_names = config_file_names or [
            f".{app_name}",
            f"{app_name}.yaml",
            f"{app_name}.yml",
            f"{app_name}.json",
            "config.yaml",
            "config.json"
        ]

        self.config: Dict[str, Any] = {}
        self.sources: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(f"{app_name}.config")

    def load_all(self,
                env_file: Optional[Path] = None,
                config_file: Optional[Path] = None,
                cli_args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load configuration from all sources with proper precedence.

        Args:
            env_file: Specific .env file path
            config_file: Specific config file path
            cli_args: Command-line arguments dictionary

        Returns:
            Merged configuration dictionary
        """
        # 1. Load defaults
        self.config = self.load_defaults()
        self.sources["defaults"] = dict(self.config)

        # 2. Load system config
        system_config = self.load_system_config()
        self.config.update(system_config)
        self.sources["system"] = system_config

        # 3. Load user config
        user_config = self.load_user_config()
        self.config.update(user_config)
        self.sources["user"] = user_config

        # 4. Load project config file
        project_config = self.load_project_config(config_file)
        self.config.update(project_config)
        self.sources["project"] = project_config

        # 5. Load environment file (.env)
        env_config = self.load_env_file(env_file)
        self.config.update(env_config)
        self.sources["env_file"] = env_config

        # 6. Load environment variables
        env_vars = self.load_environment_variables()
        self.config.update(env_vars)
        self.sources["env_vars"] = env_vars

        # 7. Apply CLI arguments (highest priority)
        if cli_args:
            cli_config = self.normalize_cli_args(cli_args)
            self.config.update(cli_config)
            self.sources["cli"] = cli_config

        return self.config

    def load_defaults(self) -> Dict[str, Any]:
        """
        Load default configuration values.

        Override this method in subclasses to provide app-specific defaults.
        """
        return {
            "debug": False,
            "log_level": "INFO",
            "timeout": 30,
            "max_retries": 3
        }

    def load_system_config(self) -> Dict[str, Any]:
        """Load system-wide configuration."""
        system_paths = [
            Path(f"/etc/{self.app_name}/"),
            Path("/etc/") / self.app_name
        ]

        return self._load_from_paths(system_paths, "system")

    def load_user_config(self) -> Dict[str, Any]:
        """Load user-specific configuration."""
        home = Path.home()
        user_paths = [
            home / f".{self.app_name}",
            home / ".config" / self.app_name,
            home / f".{self.app_name}" / "config"
        ]

        return self._load_from_paths(user_paths, "user")

    def load_project_config(self,
                           config_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load project-specific configuration file.

        Args:
            config_file: Explicit config file path

        Returns:
            Configuration dictionary
        """
        if config_file:
            return self._load_file(config_file)

        # Search current directory and parents
        current = Path.cwd()
        search_paths = [current] + list(current.parents)[:5]  # Limit search depth

        return self._load_from_paths(search_paths, "project")

    def load_env_file(self, env_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load .env file.

        Args:
            env_file: Specific .env file path

        Returns:
            Configuration from .env file
        """
        if not DOTENV_AVAILABLE:
            self.logger.debug(".env loading unavailable (install python-dotenv)")
            return {}

        # Determine .env file path
        if env_file:
            env_path = Path(env_file)
        else:
            env_path = Path.cwd() / ".env"

        if env_path.exists():
            self.logger.debug(f"Loading .env from {env_path}")
            load_dotenv(env_path)

            # Parse .env file manually to get values
            config = {}
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            config[key.strip()] = value.strip().strip('"\'')

            return config

        return {}

    def load_environment_variables(self,
                                   prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from environment variables.

        Args:
            prefix: Optional prefix for environment variables (e.g., "MYAPP_")

        Returns:
            Configuration from environment
        """
        config = {}
        prefix = prefix or f"{self.app_name.upper()}_"

        for key, value in os.environ.items():
            # Include prefixed vars and common config vars
            if key.startswith(prefix) or key in self._get_common_env_vars():
                # Remove prefix if present
                config_key = key[len(prefix):] if key.startswith(prefix) else key
                config[config_key.lower()] = self._parse_env_value(value)

        return config

    def _get_common_env_vars(self) -> List[str]:
        """Get list of common environment variable names to include."""
        return [
            "DEBUG",
            "LOG_LEVEL",
            "API_KEY",
            "DATABASE_URL",
            "REDIS_URL",
            "SECRET_KEY",
            # Add provider-specific keys
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "XAI_API_KEY",
            "MISTRAL_API_KEY",
            "COHERE_API_KEY"
        ]

    def _parse_env_value(self, value: str) -> Any:
        """
        Parse environment variable value to appropriate type.

        Args:
            value: String value from environment

        Returns:
            Parsed value (bool, int, float, or string)
        """
        # Handle boolean values
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        if value.lower() in ("false", "no", "0", "off"):
            return False

        # Handle numeric values
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        # Return as string
        return value

    def normalize_cli_args(self, cli_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize CLI arguments to match config keys.

        Args:
            cli_args: Raw CLI arguments

        Returns:
            Normalized configuration
        """
        config = {}

        for key, value in cli_args.items():
            # Skip None values
            if value is None:
                continue

            # Convert dashes to underscores
            normalized_key = key.replace("-", "_")

            config[normalized_key] = value

        return config

    def _load_from_paths(self,
                        paths: List[Path],
                        source_name: str) -> Dict[str, Any]:
        """
        Load configuration from a list of potential paths.

        Args:
            paths: List of paths to search
            source_name: Name for logging

        Returns:
            Configuration dictionary
        """
        for path in paths:
            if not path.exists():
                continue

            # If path is a directory, look for config files in it
            if path.is_dir():
                for config_name in self.config_file_names:
                    config_file = path / config_name
                    if config_file.exists():
                        self.logger.debug(
                            f"Loading {source_name} config from {config_file}"
                        )
                        return self._load_file(config_file)

            # If path is a file, load it directly
            elif path.is_file():
                self.logger.debug(f"Loading {source_name} config from {path}")
                return self._load_file(path)

        return {}

    def _load_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load configuration from a file.

        Supports YAML and JSON formats.

        Args:
            file_path: Path to configuration file

        Returns:
            Configuration dictionary
        """
        try:
            suffix = file_path.suffix.lower()

            with open(file_path) as f:
                if suffix in (".yaml", ".yml") and YAML_AVAILABLE:
                    return yaml.safe_load(f) or {}
                elif suffix == ".json":
                    return json.load(f)
                else:
                    # Try to parse as key=value format
                    config = {}
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if "=" in line:
                                key, value = line.split("=", 1)
                                config[key.strip()] = value.strip()
                    return config

        except Exception as e:
            self.logger.error(f"Failed to load config from {file_path}: {e}")
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with default."""
        return self.config.get(key, default)

    def require(self, key: str) -> Any:
        """
        Get required configuration value.

        Raises:
            ValueError: If key is missing
        """
        if key not in self.config:
            raise ValueError(
                f"Required configuration '{key}' is missing.\n"
                f"Set it via environment variable, config file, or CLI argument."
            )
        return self.config[key]

    def validate(self, schema: Dict[str, type]) -> bool:
        """
        Validate configuration against a schema.

        Args:
            schema: Dictionary mapping keys to expected types

        Returns:
            True if valid

        Raises:
            TypeError: If validation fails
        """
        for key, expected_type in schema.items():
            if key in self.config:
                value = self.config[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Config key '{key}' has wrong type. "
                        f"Expected {expected_type}, got {type(value)}"
                    )

        return True

    def print_sources(self):
        """Print configuration sources for debugging."""
        print("\nConfiguration Sources:")
        print("=" * 80)
        for source, config in self.sources.items():
            if config:
                print(f"\n{source.upper()}:")
                for key, value in config.items():
                    # Mask potential secrets
                    display_value = "***" if "key" in key.lower() or "secret" in key.lower() else value
                    print(f"  {key}: {display_value}")


if __name__ == "__main__":
    # Usage example
    config_manager = ConfigurationManager(app_name="myapp")

    # Load all configuration sources
    config = config_manager.load_all(
        cli_args={"debug": True, "api-key": "test-key"}
    )

    print("Final Configuration:")
    print(json.dumps(config, indent=2))

    print("\nConfiguration Sources:")
    config_manager.print_sources()

    # Access config values
    debug_mode = config_manager.get("debug", False)
    api_key = config_manager.require("api_key")  # Will raise if missing

    print(f"\nDebug mode: {debug_mode}")
    print(f"API key: {'***' if api_key else 'Not set'}")
