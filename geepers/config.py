"""
Configuration Management for Shared Library

Provides centralized configuration loading from multiple sources with clear precedence:
1. Default values
2. Custom config file (e.g., .appname file)
3. .env file
4. Environment variables
5. Command-line arguments (if provided)

Extracted from swarm/core/core_config.py and generalized for reuse.

Example:
    from shared.config import ConfigManager

    config = ConfigManager(
        app_name='myapp',
        config_file='.myapp',
        defaults={
            'MODEL': 'gpt-4',
            'PROVIDER': 'openai'
        }
    )

    # Get values
    model = config.get('MODEL')
    api_key = config.get_api_key('anthropic')

    # Check provider availability
    providers = config.list_available_providers()
"""

import os
import json
import dotenv
from pathlib import Path
from typing import Dict, Any, Optional, Union, List


class ConfigError(Exception):
    """Configuration-related errors."""
    pass


class ConfigManager:
    """
    Centralized configuration management with multi-source loading.

    This class provides access to configuration settings from multiple sources
    with a clear precedence order. Later sources override earlier ones.

    Loading Order:
        1. Default values (provided at initialization)
        2. Custom config file (e.g., .swarm, .myapp)
        3. .env file
        4. Environment variables
        5. Command-line arguments (via override_with_cli_args)

    Attributes:
        config: The combined configuration dictionary
        base_dir: The base directory for the application
        app_name: Name of the application using this config
    """

    # Known API providers and their key patterns
    KNOWN_PROVIDERS = {
        'xai': ['XAI_API_KEY', 'GROK_API_KEY'],
        'openai': ['OPENAI_API_KEY'],
        'anthropic': ['ANTHROPIC_API_KEY'],
        'cohere': ['COHERE_API_KEY'],
        'mistral': ['MISTRAL_API_KEY'],
        'gemini': ['GEMINI_API_KEY'],
        'perplexity': ['PERPLEXITY_API_KEY'],
        'groq': ['GROQ_API_KEY'],
        'huggingface': ['HF_API_KEY', 'HUGGINGFACE_API_KEY'],
        'census': ['CENSUS_API_KEY'],
        'newsapi': ['NEWS_API_KEY', 'NEWSAPI_API_KEY'],
        'youtube': ['YOUTUBE_API_KEY'],
        'alphavantage': ['ALPHAVANTAGE_API_KEY', 'ALPHA_VANTAGE_API_KEY'],
        'github': ['GITHUB_TOKEN', 'GITHUB_API_KEY'],
        'nasa': ['NASA_API_KEY']
    }

    def __init__(
        self,
        app_name: str = 'app',
        base_dir: Optional[Union[str, Path]] = None,
        config_file: Optional[Union[str, Path]] = None,
        env_file: Optional[Union[str, Path]] = None,
        defaults: Optional[Dict[str, Any]] = None,
        cli_args: Optional[Dict[str, Any]] = None,
        auto_load: bool = True
    ):
        """
        Initialize the configuration manager.

        Args:
            app_name: Application name (used for default config file name)
            base_dir: Base directory (defaults to current directory)
            config_file: Path to custom config file (defaults to base_dir/.{app_name})
            env_file: Path to .env file (defaults to base_dir/.env)
            defaults: Default configuration values
            cli_args: Command-line arguments to override config
            auto_load: Whether to automatically load config on init
        """
        self.app_name = app_name
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()

        # Set config file paths
        self.config_file = Path(config_file) if config_file else self.base_dir / f'.{app_name}'
        self.env_file = Path(env_file) if env_file else self.base_dir / '.env'

        # Initialize config
        self.config = {}

        if auto_load:
            # Set defaults
            if defaults:
                self.config.update(defaults)

            # Load configuration
            self._load_config_file()
            self._load_env_file()
            self._load_env_vars()

            # Override with CLI args if provided
            if cli_args:
                self.override_with_cli_args(cli_args)

    def _parse_value(self, value: str) -> Any:
        """
        Convert string value to appropriate Python type.

        Args:
            value: String value to parse

        Returns:
            Parsed value with appropriate type
        """
        # Handle quoted strings
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]

        # Handle booleans
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False

        # Handle numbers
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).replace('-', '', 1).isdigit():
            try:
                return float(value)
            except ValueError:
                pass

        return value

    def _load_config_file(self):
        """Load configuration from custom config file (e.g., .swarm, .myapp)."""
        if not self.config_file.exists():
            return

        try:
            with open(self.config_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Parse KEY=VALUE format
                    if '=' not in line:
                        continue

                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Parse value
                    self.config[key] = self._parse_value(value)

        except Exception as e:
            raise ConfigError(f"Error loading config file {self.config_file}: {e}")

    def _load_env_file(self):
        """Load configuration from .env file."""
        if not self.env_file.exists():
            return

        try:
            # Load .env file into environment
            dotenv.load_dotenv(self.env_file)

            # Update config with values from environment
            for key in list(self.config.keys()):
                if key in os.environ:
                    self.config[key] = self._parse_value(os.environ[key])

        except Exception as e:
            raise ConfigError(f"Error loading .env file {self.env_file}: {e}")

    def _load_env_vars(self):
        """Load configuration from environment variables."""
        # Update existing keys from environment
        for key in list(self.config.keys()):
            if key in os.environ:
                self.config[key] = self._parse_value(os.environ[key])

        # Also load known API keys even if not in defaults
        for provider, key_patterns in self.KNOWN_PROVIDERS.items():
            for key_pattern in key_patterns:
                if key_pattern in os.environ and key_pattern not in self.config:
                    self.config[key_pattern] = os.environ[key_pattern]

    def override_with_cli_args(self, cli_args: Dict[str, Any]):
        """
        Override configuration with command-line arguments.

        Args:
            cli_args: Dictionary of command-line arguments
        """
        for key, value in cli_args.items():
            if value is not None:  # Only override if arg was provided
                key = key.upper()  # Normalize to uppercase
                self.config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value

    def get_api_key(self, provider: Optional[str] = None) -> str:
        """
        Get API key for a provider.

        Args:
            provider: Provider name (if None, uses configured PROVIDER)

        Returns:
            API key or empty string if not found
        """
        if provider is None:
            provider = self.get('PROVIDER', 'openai')

        provider = provider.lower()

        # Try known key patterns for this provider
        if provider in self.KNOWN_PROVIDERS:
            for key_pattern in self.KNOWN_PROVIDERS[provider]:
                api_key = self.get(key_pattern, '')
                if api_key:
                    return api_key

        # Try generic pattern: {PROVIDER}_API_KEY
        generic_key = f"{provider.upper()}_API_KEY"
        return self.get(generic_key, '')

    def has_api_key(self, provider: str) -> bool:
        """
        Check if API key exists for a provider.

        Args:
            provider: Provider name

        Returns:
            True if API key is configured
        """
        return bool(self.get_api_key(provider))

    def list_available_providers(self) -> List[str]:
        """
        List all providers with configured API keys.

        Returns:
            List of provider names
        """
        available = []
        for provider in self.KNOWN_PROVIDERS.keys():
            if self.has_api_key(provider):
                available.append(provider)
        return available

    def as_dict(self, mask_secrets: bool = True) -> Dict[str, Any]:
        """
        Get configuration as dictionary.

        Args:
            mask_secrets: Whether to mask API keys and secrets

        Returns:
            Configuration dictionary
        """
        config_copy = self.config.copy()

        if mask_secrets:
            for key, value in config_copy.items():
                if 'API_KEY' in key or 'SECRET' in key or 'PASSWORD' in key:
                    if isinstance(value, str) and len(value) > 4:
                        config_copy[key] = f"{'*' * (len(value) - 4)}{value[-4:]}"
                    else:
                        config_copy[key] = '****'

        return config_copy

    def save(self, file_path: Optional[Union[str, Path]] = None, include_secrets: bool = False) -> None:
        """
        Save configuration to file.

        Args:
            file_path: File path (defaults to config_file)
            include_secrets: Whether to include API keys (default: False for security)
        """
        file_path = Path(file_path) if file_path else self.config_file

        try:
            with open(file_path, 'w') as f:
                f.write(f"# {self.app_name} Configuration\n")
                f.write(f"# Generated by ConfigManager\n\n")

                for key, value in sorted(self.config.items()):
                    # Skip secrets unless explicitly requested
                    if not include_secrets:
                        if 'API_KEY' in key or 'SECRET' in key or 'PASSWORD' in key:
                            continue

                    # Format value
                    if isinstance(value, str):
                        if '\n' in value:
                            value = f'"""{value}"""'
                        else:
                            value = f'"{value}"'
                    elif isinstance(value, bool):
                        value = str(value).lower()
                    else:
                        value = str(value)

                    f.write(f"{key}={value}\n")

        except Exception as e:
            raise ConfigError(f"Error saving configuration to {file_path}: {e}")

    def reload(self):
        """Reload configuration from all sources."""
        self.config.clear()
        self._load_config_file()
        self._load_env_file()
        self._load_env_vars()

    def __repr__(self) -> str:
        return f"ConfigManager(app_name='{self.app_name}', providers={self.list_available_providers()})"


# Convenience function for quick setup
def create_config(
    app_name: str = 'app',
    defaults: Optional[Dict[str, Any]] = None,
    **kwargs
) -> ConfigManager:
    """
    Create a ConfigManager with sensible defaults.

    Args:
        app_name: Application name
        defaults: Default configuration values
        **kwargs: Additional ConfigManager arguments

    Returns:
        Configured ConfigManager instance
    """
    return ConfigManager(app_name=app_name, defaults=defaults, **kwargs)
