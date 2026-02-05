"""
Pytest Fixtures and Testing Patterns

Description: Comprehensive patterns for writing effective pytest tests including
fixtures, mocking, parametrization, and test organization strategies.

Use Cases:
- Setting up test environments and fixtures
- Mocking external dependencies (APIs, databases, files)
- Parametrized testing for multiple scenarios
- Integration and unit test organization
- Async test support
- Test data management

Dependencies:
- pytest (pip install pytest)
- pytest-asyncio (pip install pytest-asyncio) for async tests
- pytest-mock (pip install pytest-mock) for enhanced mocking
- pytest-cov (pip install pytest-cov) for coverage

Notes:
- Use fixtures for reusable test setup/teardown
- Scope fixtures appropriately (function, class, module, session)
- Mock external dependencies to isolate units
- Use parametrize for testing multiple inputs
- Organize tests by type (unit/, integration/, e2e/)
- Name tests clearly: test_<what>_<condition>_<expected>
- Use conftest.py for shared fixtures

Related Snippets:
- /home/coolhand/SNIPPETS/api-clients/multi_provider_abstraction.py
- /home/coolhand/SNIPPETS/async-patterns/async_testing.py
- /home/coolhand/SNIPPETS/error-handling/graceful_import_fallbacks.py

Source Attribution:
- Extracted from: /home/coolhand/projects/tests/conftest.py
- Related patterns across test directories
"""

import pytest
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import Mock, MagicMock, patch


# ============================================================================
# BASIC FIXTURES
# ============================================================================

@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    Provide sample data for tests.

    Fixture scope: function (default)
    Runs once per test function.
    """
    return {
        "id": 1,
        "name": "Test Item",
        "value": 42,
        "tags": ["test", "example"]
    }


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """
    Create temporary directory for testing.

    Yields directory path and cleans up after test.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
    # Cleanup happens automatically


@pytest.fixture
def temp_file(temp_directory) -> Path:
    """
    Create temporary file in temporary directory.

    Demonstrates fixture composition.
    """
    file_path = temp_directory / "test_file.txt"
    file_path.write_text("Test content")
    return file_path


# ============================================================================
# SCOPED FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def api_base_url() -> str:
    """
    Session-scoped fixture runs once per test session.

    Use for expensive setup that can be shared.
    """
    return "https://api.example.com/v1"


@pytest.fixture(scope="module")
def database_connection():
    """
    Module-scoped fixture runs once per module.

    Example of database connection setup/teardown.
    """
    # Setup
    connection = {"connected": True, "db": "test_db"}

    yield connection

    # Teardown
    connection["connected"] = False
    # Close actual connection here


@pytest.fixture(scope="class")
def test_client():
    """
    Class-scoped fixture for test classes.

    Runs once per test class.
    """
    class MockClient:
        def __init__(self):
            self.requests = []

        def request(self, method, url, **kwargs):
            self.requests.append({"method": method, "url": url})
            return {"status": 200, "data": {}}

    return MockClient()


# ============================================================================
# MOCKING PATTERNS
# ============================================================================

@pytest.fixture
def mock_api_client():
    """
    Mock API client for testing without network calls.
    """
    client = Mock()
    client.get.return_value = {
        "status": "success",
        "data": {"id": 1, "name": "Test"}
    }
    client.post.return_value = {
        "status": "success",
        "id": 2
    }
    return client


@pytest.fixture
def mock_llm_response():
    """
    Mock LLM API response.

    Useful for testing AI integrations without API calls.
    """
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "This is a test response"
    mock_response.usage.total_tokens = 100
    return mock_response


@pytest.fixture
def mock_file_system(tmp_path):
    """
    Mock file system operations.

    Uses tmp_path (pytest built-in) for real filesystem isolation.
    """
    # Create test directory structure
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"test": true}')
    (tmp_path / "config.yaml").write_text("setting: value")

    return tmp_path


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================

@pytest.fixture(params=["openai", "anthropic", "xai"])
def provider_name(request):
    """
    Parametrized fixture - test runs once per parameter.

    Useful for testing multiple providers/configurations.
    """
    return request.param


@pytest.fixture(params=[
    {"model": "gpt-4", "temperature": 0.7},
    {"model": "gpt-3.5-turbo", "temperature": 0.5},
    {"model": "claude-3", "temperature": 0.8}
])
def llm_config(request):
    """Parametrized LLM configurations."""
    return request.param


# ============================================================================
# ASYNC FIXTURES
# ============================================================================

@pytest.fixture
async def async_client():
    """
    Async fixture for async tests.

    Requires pytest-asyncio: pip install pytest-asyncio
    """
    class AsyncMockClient:
        async def fetch(self, url):
            return {"url": url, "status": 200}

        async def close(self):
            pass

    client = AsyncMockClient()
    yield client
    await client.close()


# ============================================================================
# EXAMPLE TEST CASES
# ============================================================================

def test_basic_fixture_usage(sample_data):
    """Test using a simple fixture."""
    assert sample_data["id"] == 1
    assert "test" in sample_data["tags"]


def test_temp_file(temp_file):
    """Test using temporary file fixture."""
    content = temp_file.read_text()
    assert content == "Test content"


def test_mock_api_client(mock_api_client):
    """Test using mocked API client."""
    result = mock_api_client.get("/users/1")
    assert result["status"] == "success"
    assert result["data"]["id"] == 1

    # Verify mock was called correctly
    mock_api_client.get.assert_called_once_with("/users/1")


@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25)
])
def test_parametrized(input, expected):
    """
    Parametrized test - runs once per parameter set.

    Use @pytest.mark.parametrize for inline parametrization.
    """
    assert input ** 2 == expected


def test_fixture_parametrization(provider_name):
    """Test using parametrized fixture."""
    assert provider_name in ["openai", "anthropic", "xai"]


# ============================================================================
# INTEGRATION TEST PATTERNS
# ============================================================================

class TestAPIIntegration:
    """
    Test class for integration tests.

    Use classes to group related tests.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_client):
        """
        Setup fixture that runs before each test in the class.

        autouse=True means it runs automatically.
        """
        self.client = test_client

    def test_create_resource(self):
        """Test resource creation."""
        result = self.client.request("POST", "/resources", data={"name": "test"})
        assert result["status"] == 200

    def test_get_resource(self):
        """Test resource retrieval."""
        result = self.client.request("GET", "/resources/1")
        assert result["status"] == 200


# ============================================================================
# MOCKING EXTERNAL SERVICES
# ============================================================================

def test_with_mock_env_vars(monkeypatch):
    """
    Test using monkeypatch to set environment variables.

    monkeypatch is a built-in pytest fixture.
    """
    monkeypatch.setenv("API_KEY", "test-key-123")
    monkeypatch.setenv("DEBUG", "true")

    import os
    assert os.getenv("API_KEY") == "test-key-123"
    assert os.getenv("DEBUG") == "true"


def test_with_mock_requests(monkeypatch):
    """Test mocking the requests library."""
    class MockResponse:
        @staticmethod
        def json():
            return {"data": "test"}

        status_code = 200

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    import requests
    result = requests.get("http://test.com")
    assert result.json() == {"data": "test"}


@patch('openai.OpenAI')
def test_mock_openai_client(mock_openai_class):
    """
    Test mocking OpenAI client using patch decorator.

    Useful for testing without API calls.
    """
    # Setup mock
    mock_client = Mock()
    mock_openai_class.return_value = mock_client

    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test response"

    mock_client.chat.completions.create.return_value = mock_response

    # Use in test
    from openai import OpenAI
    client = OpenAI(api_key="fake-key")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}]
    )

    assert response.choices[0].message.content == "Test response"
    mock_client.chat.completions.create.assert_called_once()


# ============================================================================
# ASYNC TEST PATTERNS
# ============================================================================

@pytest.mark.asyncio
async def test_async_function(async_client):
    """
    Async test using pytest-asyncio.

    Mark with @pytest.mark.asyncio.
    """
    result = await async_client.fetch("http://example.com")
    assert result["status"] == 200


# ============================================================================
# CONFTEST.PY EXAMPLE
# ============================================================================

CONFTEST_EXAMPLE = '''
"""
conftest.py - Shared pytest configuration and fixtures

Place this file in your tests/ directory to share fixtures
across all test modules.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Provide project root path."""
    return project_root


@pytest.fixture
def sample_config():
    """Provide sample configuration."""
    return {
        "api_url": "http://localhost:8000",
        "timeout": 30,
        "retries": 3
    }


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset any singleton state between tests."""
    # Clear caches, reset state, etc.
    yield
    # Cleanup after test


def pytest_configure(config):
    """
    Pytest configuration hook.

    Add custom markers, configure plugins, etc.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks integration tests"
    )
'''


# ============================================================================
# PYTEST.INI EXAMPLE
# ============================================================================

PYTEST_INI_EXAMPLE = '''
[tool:pytest]
# Pytest configuration

# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output options
addopts =
    -v                      # Verbose output
    --strict-markers        # Error on unknown markers
    --tb=short              # Short traceback format
    --cov=src              # Coverage for src directory
    --cov-report=html      # HTML coverage report
    --cov-report=term-missing  # Show missing lines

# Markers
markers =
    slow: slow running tests
    integration: integration tests
    unit: unit tests
    requires_api: tests requiring API access

# Asyncio configuration
asyncio_mode = auto
'''


if __name__ == "__main__":
    print("Pytest Fixtures and Testing Patterns")
    print("=" * 80)
    print("\nconftest.py example:")
    print(CONFTEST_EXAMPLE)
    print("\npytest.ini example:")
    print(PYTEST_INI_EXAMPLE)
    print("\nRun tests with: pytest")
    print("Run with coverage: pytest --cov=src")
    print("Run specific marker: pytest -m integration")
