"""
Logging Utilities

Description: Production-ready logging configurations with structured logging, multiple handlers,
log rotation, and context-aware logging for microservices and AI applications.

Use Cases:
- Structured JSON logging for log aggregation (ELK, Splunk, CloudWatch)
- Multi-handler logging (file, console, remote)
- Log rotation to prevent disk space issues
- Context-aware logging for distributed systems
- Performance monitoring and debugging
- Error tracking with stack traces

Dependencies:
- logging (stdlib)
- json (stdlib)
- pathlib (stdlib)
- typing (stdlib)
- Optional: python-json-logger for advanced JSON formatting

Notes:
- Thread-safe logging configuration
- Automatic log rotation by size and time
- Structured logging with context injection
- Multiple severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Performance impact is minimal with proper level configuration

Related Snippets:
- /home/coolhand/SNIPPETS/utilities/retry_decorator.py - Logging retry attempts
- /home/coolhand/SNIPPETS/error-handling/ - Error tracking
- /home/coolhand/SNIPPETS/async-patterns/ - Async logging

Source Attribution:
- Extracted from: /home/coolhand/shared/observability/__init__.py
- Related patterns: /home/coolhand/enterprise_orchestration/core/
- Author: Luke Steuber
"""

import logging
import logging.handlers
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.

    Outputs log records as JSON for easy parsing by log aggregation systems.
    Includes timestamp, level, message, and additional context.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: LogRecord to format

        Returns:
            JSON-formatted log string
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "context"):
            log_data["context"] = record.context

        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for console output with ANSI color codes.

    Makes logs easier to read in terminal with color-coded severity levels.
    """

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[1;31m'  # Bold Red
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        """Format record with colors."""
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Setup comprehensive logging with console and optional file handlers.

    Args:
        name: Logger name (typically module or application name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        json_format: Use JSON formatting for structured logs
        max_bytes: Maximum log file size before rotation (default: 10MB)
        backup_count: Number of backup files to keep (default: 5)

    Returns:
        Configured logger instance

    Example:
        >>> # Simple console logging
        >>> logger = setup_logging("myapp", level="DEBUG")
        >>> logger.info("Application started")
        >>>
        >>> # With file output and JSON formatting
        >>> logger = setup_logging(
        ...     "myapp",
        ...     level="INFO",
        ...     log_file="logs/app.log",
        ...     json_format=True
        ... )
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    if json_format:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))

    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)

        if json_format:
            file_handler.setFormatter(StructuredFormatter())
        else:
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))

        logger.addHandler(file_handler)

    return logger


class ContextLogger:
    """
    Logger with automatic context injection.

    Adds contextual information to all log messages,
    useful for distributed systems and multi-tenant applications.

    Example:
        >>> logger = ContextLogger("myapp", context={"user_id": "123"})
        >>> logger.info("User logged in")  # Includes user_id in log
    """

    def __init__(self, name: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize context logger.

        Args:
            name: Logger name
            context: Default context to include in all logs
        """
        self.logger = logging.getLogger(name)
        self.context = context or {}

    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method with context injection."""
        extra = {"context": {**self.context, **kwargs}}
        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, **kwargs):
        """Log debug message with context."""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message with context."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message with context."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message with context."""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message with context."""
        self._log(logging.CRITICAL, message, **kwargs)


@contextmanager
def log_context(**context):
    """
    Context manager for temporary logging context.

    Args:
        **context: Key-value pairs to add to log context

    Example:
        >>> logger = ContextLogger("myapp")
        >>> with log_context(request_id="abc123"):
        ...     logger.info("Processing request")  # Includes request_id
    """
    from contextvars import ContextVar

    log_ctx: ContextVar = ContextVar("log_context", default={})
    token = log_ctx.set({**log_ctx.get(), **context})
    try:
        yield
    finally:
        log_ctx.reset(token)


def log_execution_time(logger: logging.Logger, level: int = logging.INFO):
    """
    Decorator to log function execution time.

    Args:
        logger: Logger instance
        level: Logging level (default: INFO)

    Returns:
        Decorated function that logs execution time

    Example:
        >>> logger = setup_logging("myapp")
        >>>
        >>> @log_execution_time(logger)
        ... def slow_function():
        ...     time.sleep(1)
        ...     return "done"
    """
    import time
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                logger.log(
                    level,
                    f"{func.__name__} completed in {elapsed:.3f}s"
                )
                return result
            except Exception as e:
                elapsed = time.time() - start
                logger.error(
                    f"{func.__name__} failed after {elapsed:.3f}s: {e}"
                )
                raise
        return wrapper
    return decorator


class PerformanceLogger:
    """
    Logger for performance metrics and timing.

    Tracks execution times, call counts, and performance statistics.

    Example:
        >>> perf = PerformanceLogger("myapp")
        >>> with perf.measure("database_query"):
        ...     result = db.query("SELECT * FROM users")
        >>> perf.report()
    """

    def __init__(self, name: str):
        """
        Initialize performance logger.

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.metrics: Dict[str, list] = {}

    @contextmanager
    def measure(self, operation: str):
        """
        Measure operation execution time.

        Args:
            operation: Operation name

        Example:
            >>> perf = PerformanceLogger("myapp")
            >>> with perf.measure("api_call"):
            ...     response = requests.get("https://api.example.com")
        """
        import time
        start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start
            if operation not in self.metrics:
                self.metrics[operation] = []
            self.metrics[operation].append(elapsed)
            self.logger.debug(f"{operation}: {elapsed:.3f}s")

    def report(self):
        """Log performance statistics summary."""
        for operation, times in self.metrics.items():
            avg = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            self.logger.info(
                f"{operation}: count={len(times)}, "
                f"avg={avg:.3f}s, min={min_time:.3f}s, max={max_time:.3f}s"
            )


# Example usage and testing
if __name__ == "__main__":
    import time

    print("Logging Utilities Examples")
    print("=" * 60)

    # Example 1: Basic logging
    print("\n1. Basic Console Logging")
    print("-" * 60)
    logger1 = setup_logging("example1", level="DEBUG")
    logger1.debug("This is a debug message")
    logger1.info("Application started")
    logger1.warning("This is a warning")
    logger1.error("This is an error")

    # Example 2: JSON structured logging
    print("\n2. Structured JSON Logging")
    print("-" * 60)
    logger2 = setup_logging("example2", level="INFO", json_format=True)
    logger2.info("Structured log message")
    logger2.warning("Warning with structured format")

    # Example 3: File logging with rotation
    print("\n3. File Logging (check logs/example.log)")
    print("-" * 60)
    logger3 = setup_logging(
        "example3",
        level="INFO",
        log_file="logs/example.log",
        max_bytes=1024,  # Small size for testing rotation
        backup_count=3
    )
    for i in range(5):
        logger3.info(f"Log message {i+1} - Creating multiple log entries")

    # Example 4: Context logging
    print("\n4. Context-Aware Logging")
    print("-" * 60)
    setup_logging("example4", level="INFO", json_format=True)
    context_logger = ContextLogger("example4", context={"service": "api", "version": "1.0"})
    context_logger.info("Request received", request_id="abc123", user_id="user456")

    # Example 5: Execution time logging
    print("\n5. Execution Time Logging")
    print("-" * 60)
    logger5 = setup_logging("example5", level="INFO")

    @log_execution_time(logger5)
    def slow_operation():
        time.sleep(0.5)
        return "completed"

    result = slow_operation()

    # Example 6: Performance metrics
    print("\n6. Performance Metrics")
    print("-" * 60)
    setup_logging("example6", level="INFO")
    perf = PerformanceLogger("example6")

    for i in range(3):
        with perf.measure("operation_a"):
            time.sleep(0.1)

    for i in range(2):
        with perf.measure("operation_b"):
            time.sleep(0.2)

    perf.report()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("Check logs/ directory for file output examples")
