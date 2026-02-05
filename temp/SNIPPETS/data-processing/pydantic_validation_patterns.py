"""
Pydantic Data Validation and Schema Patterns

Description: Comprehensive patterns for data validation, transformation, and schema generation using Pydantic. Includes input validation, output serialization, and OpenAI function calling schema generation.

Use Cases:
- Validating API request/response data
- Building type-safe tool interfaces for LLM function calling
- Converting between Python objects and JSON schemas
- Sanitizing user input with automatic type coercion
- Generating documentation from data models
- Creating configuration validators with defaults and constraints

Dependencies:
- pydantic (pip install pydantic)
- typing (stdlib)
- json (stdlib)

Notes:
- Pydantic v2+ has significant API changes from v1; this uses v2 patterns
- Field validators run automatically on initialization
- model_json_schema() generates JSON Schema compatible with OpenAI function calling
- Use ValidationError.errors() to get detailed validation failure information
- Validators can transform data, not just validate
- @field_validator is the v2 equivalent of v1's @validator

Related Snippets:
- data-processing/format_conversion_patterns.py - Format conversion
- api-clients/multi_provider_abstraction.py - Provider patterns
- tool-registration/swarm_module_pattern.py - Tool schema patterns

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/hive/swarm_data.py
- Also from: /home/coolhand/projects/swarm/hive/swarm_finance.py
- Related: /home/coolhand/enterprise_orchestration/core/base.py
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
import json


# ===== Basic Validation Patterns =====

class UserInput(BaseModel):
    """
    Basic input validation with field constraints.

    Example:
        >>> user = UserInput(username="alice", email="alice@example.com", age=25)
        >>> user.username
        'alice'

        >>> # Invalid email raises ValidationError
        >>> try:
        ...     UserInput(username="bob", email="invalid", age=25)
        ... except ValidationError as e:
        ...     print("Validation failed")
        Validation failed
    """
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="Email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User age")
    tags: List[str] = Field(default_factory=list, description="User tags")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v.lower()

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Sanitize username."""
        return v.strip().lower()


# ===== LLM Function Calling Schemas =====

class SearchQueryInput(BaseModel):
    """
    Search query parameters for LLM tool calling.

    This pattern is used throughout the Swarm system for tool schemas.
    """
    query: str = Field(..., description="Search query string")
    max_results: int = Field(10, ge=1, le=100, description="Maximum number of results")
    search_type: str = Field("web", description="Type of search (web, news, academic)")
    language: str = Field("en", description="Language code (e.g., 'en', 'es')")

    @field_validator('query')
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        """Remove excessive whitespace from query."""
        return ' '.join(v.split())


class DataConversionInput(BaseModel):
    """
    Data conversion parameters matching swarm_data.py pattern.
    """
    data: Any = Field(..., description="Data to convert (can be string or object)")
    target_format: str = Field("json", description="Target format (json, yaml, toml, xml, csv)")
    style: str = Field("pretty", description="Output style (pretty, compact, single_line)")

    @field_validator('target_format')
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Ensure format is supported."""
        supported = ['json', 'yaml', 'toml', 'xml', 'csv']
        v = v.lower()
        if v not in supported:
            raise ValueError(f"Format must be one of: {', '.join(supported)}")
        return v


class FinancialQueryInput(BaseModel):
    """
    Financial data query pattern from swarm_finance.py.
    """
    query: str = Field(..., description="Stock symbol or financial query")
    window: str = Field("1D", description="Time window (1D, 1W, 1M, 1Y)")
    include_fundamentals: bool = Field(False, description="Include fundamental data")

    @field_validator('query')
    @classmethod
    def uppercase_symbol(cls, v: str) -> str:
        """Normalize stock symbols to uppercase."""
        return v.strip().upper()


# ===== Configuration Validation =====

class ModuleConfig(BaseModel):
    """
    Module configuration validation pattern from enterprise_orchestration.

    Example:
        >>> config = ModuleConfig(
        ...     name="search_module",
        ...     capabilities=["web_search", "news_search"],
        ...     max_concurrent=5
        ... )
        >>> config.module_id  # Auto-generated if not provided
    """
    module_id: Optional[str] = Field(None, description="Unique module identifier")
    name: str = Field(..., description="Module name")
    version: str = Field("1.0.0", description="Module version")
    description: str = Field("", description="Module description")
    capabilities: List[str] = Field(default_factory=list, description="Module capabilities")
    dependencies: List[str] = Field(default_factory=list, description="Required dependencies")
    max_concurrent: int = Field(5, ge=1, le=100, description="Maximum concurrent tasks")
    timeout: int = Field(300, ge=1, description="Task timeout in seconds")
    retry_attempts: int = Field(3, ge=0, description="Number of retry attempts")

    @field_validator('capabilities')
    @classmethod
    def validate_capabilities(cls, v: List[str]) -> List[str]:
        """Validate that capabilities are non-empty strings."""
        if not all(isinstance(cap, str) and cap.strip() for cap in v):
            raise ValueError("All capabilities must be non-empty strings")
        return v

    @model_validator(mode='after')
    def generate_module_id(self) -> 'ModuleConfig':
        """Generate module_id if not provided."""
        if not self.module_id:
            self.module_id = f"{self.name}_{self.version}".replace(".", "_")
        return self


# ===== Nested Validation =====

class Address(BaseModel):
    """Nested model for complex validation."""
    street: str
    city: str
    country: str
    postal_code: str


class Organization(BaseModel):
    """
    Example of nested validation with multiple levels.

    Example:
        >>> org = Organization(
        ...     name="TechCorp",
        ...     address={"street": "123 Main", "city": "Boston",
        ...              "country": "USA", "postal_code": "02101"},
        ...     employee_count=50
        ... )
        >>> org.address.city
        'Boston'
    """
    name: str = Field(..., min_length=1)
    address: Address
    employee_count: int = Field(..., ge=1)
    departments: List[str] = Field(default_factory=list)


# ===== OpenAI Function Calling Schema Generation =====

def generate_function_schema(
    model_class: type[BaseModel],
    function_name: str,
    description: str
) -> Dict[str, Any]:
    """
    Generate OpenAI-compatible function calling schema from Pydantic model.

    This is the pattern used throughout the Swarm system for tool registration.

    Args:
        model_class: Pydantic model class
        function_name: Name for the function
        description: Description of what the function does

    Returns:
        OpenAI function calling schema

    Example:
        >>> schema = generate_function_schema(
        ...     SearchQueryInput,
        ...     "web_search",
        ...     "Search the web for information"
        ... )
        >>> schema['type']
        'function'
        >>> schema['function']['name']
        'web_search'
    """
    return {
        "name": description,
        "description": description,
        "type": "function",
        "function": {
            "name": function_name,
            "description": description,
            "parameters": model_class.model_json_schema(),
            "module": function_name.split('_')[0] if '_' in function_name else "unknown"
        }
    }


# ===== Validation with Error Handling =====

class DataValidator:
    """
    Wrapper for safe validation with detailed error reporting.

    Example:
        >>> validator = DataValidator(SearchQueryInput)
        >>> result = validator.validate({"query": "Python tutorial", "max_results": 20})
        >>> result['valid']
        True
        >>> result['data'].query
        'Python tutorial'
    """

    def __init__(self, model_class: type[BaseModel]):
        self.model_class = model_class

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data and return results with detailed errors.

        Args:
            data: Dictionary to validate

        Returns:
            Dict with 'valid', 'data', and 'errors' keys
        """
        try:
            validated = self.model_class(**data)
            return {
                "valid": True,
                "data": validated,
                "errors": None
            }
        except ValidationError as e:
            return {
                "valid": False,
                "data": None,
                "errors": self._format_errors(e)
            }

    @staticmethod
    def _format_errors(validation_error: ValidationError) -> List[Dict[str, Any]]:
        """Format ValidationError for human-readable output."""
        formatted = []
        for error in validation_error.errors():
            formatted.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        return formatted


# ===== Data Transformation Patterns =====

class DataTransformer(BaseModel):
    """
    Pattern for transforming data while validating.

    Example:
        >>> transformer = DataTransformer(
        ...     input_text="  Hello World  ",
        ...     numbers=[1, 2, 3, "4", "5"]
        ... )
        >>> transformer.input_text  # Trimmed
        'Hello World'
        >>> transformer.numbers  # All converted to int
        [1, 2, 3, 4, 5]
    """
    input_text: str
    numbers: List[int]
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('input_text')
    @classmethod
    def trim_text(cls, v: str) -> str:
        """Automatically trim whitespace."""
        return v.strip()

    @field_validator('numbers', mode='before')
    @classmethod
    def convert_to_int(cls, v: Any) -> List[int]:
        """Convert string numbers to integers."""
        if not isinstance(v, list):
            v = [v]
        return [int(item) if not isinstance(item, int) else item for item in v]


# ===== Serialization Patterns =====

class APIResponse(BaseModel):
    """
    Pattern for API responses with serialization options.

    Example:
        >>> response = APIResponse(
        ...     status="success",
        ...     data={"results": [1, 2, 3]},
        ...     message="Operation completed"
        ... )
        >>> response.model_dump_json(indent=2)  # Serialize to JSON
        >>> response.model_dump(exclude={'internal_id'})  # Exclude fields
    """
    status: str
    data: Dict[str, Any]
    message: Optional[str] = None
    internal_id: Optional[str] = Field(None, exclude=True)

    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """Serialize to dictionary with options."""
        return self.model_dump(exclude_none=exclude_none)

    def to_json(self, indent: Optional[int] = None) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=indent)


# ===== Usage Examples =====

if __name__ == "__main__":
    print("=" * 70)
    print("Pydantic Validation Patterns - Usage Examples")
    print("=" * 70)

    # Example 1: Basic Validation
    print("\n1. Basic User Input Validation:")
    print("-" * 70)
    try:
        user = UserInput(
            username="  Alice  ",
            email="ALICE@EXAMPLE.COM",
            age=25,
            tags=["python", "ai"]
        )
        print(f"Username: {user.username}")  # Sanitized to lowercase
        print(f"Email: {user.email}")  # Converted to lowercase
        print(f"Tags: {user.tags}")
    except ValidationError as e:
        print(f"Validation error: {e}")

    # Example 2: Function Schema Generation
    print("\n2. OpenAI Function Calling Schema:")
    print("-" * 70)
    schema = generate_function_schema(
        SearchQueryInput,
        "web_search",
        "Search the web for information"
    )
    print(json.dumps(schema, indent=2))

    # Example 3: Configuration Validation
    print("\n3. Module Configuration:")
    print("-" * 70)
    config = ModuleConfig(
        name="search_module",
        capabilities=["web_search", "news_search"],
        max_concurrent=5
    )
    print(f"Module ID: {config.module_id}")  # Auto-generated
    print(f"Capabilities: {config.capabilities}")

    # Example 4: Validation with Error Handling
    print("\n4. Safe Validation with Error Reporting:")
    print("-" * 70)
    validator = DataValidator(SearchQueryInput)

    # Valid data
    result = validator.validate({
        "query": "  Python   tutorial  ",  # Will be sanitized
        "max_results": 20
    })
    print(f"Valid: {result['valid']}")
    if result['valid']:
        print(f"Query: {result['data'].query}")

    # Invalid data
    result = validator.validate({
        "query": "test",
        "max_results": 1000  # Exceeds maximum
    })
    print(f"\nValid: {result['valid']}")
    if not result['valid']:
        print("Errors:")
        for error in result['errors']:
            print(f"  - {error['field']}: {error['message']}")

    # Example 5: Data Transformation
    print("\n5. Data Transformation During Validation:")
    print("-" * 70)
    transformer = DataTransformer(
        input_text="  Hello World  ",
        numbers=[1, 2, "3", "4", 5]
    )
    print(f"Transformed text: '{transformer.input_text}'")
    print(f"Transformed numbers: {transformer.numbers}")

    # Example 6: Nested Validation
    print("\n6. Nested Model Validation:")
    print("-" * 70)
    org = Organization(
        name="TechCorp",
        address={
            "street": "123 Main St",
            "city": "Boston",
            "country": "USA",
            "postal_code": "02101"
        },
        employee_count=50,
        departments=["Engineering", "Sales"]
    )
    print(f"Organization: {org.name}")
    print(f"Location: {org.address.city}, {org.address.country}")
    print(f"Departments: {', '.join(org.departments)}")

    # Example 7: Serialization
    print("\n7. API Response Serialization:")
    print("-" * 70)
    response = APIResponse(
        status="success",
        data={"items": [1, 2, 3], "count": 3},
        message="Query successful",
        internal_id="internal-12345"
    )
    print("JSON output:")
    print(response.to_json(indent=2))
    print("\nDict output (excludes internal_id):")
    print(response.to_dict())

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
