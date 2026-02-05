"""
JSON Validation, Analysis, and Manipulation Patterns

Description: Comprehensive patterns for JSON validation, statistical analysis, key extraction, and manipulation without external dependencies (uses only stdlib).

Use Cases:
- Validating JSON API responses before processing
- Analyzing JSON structure for debugging or documentation
- Extracting all keys from nested JSON for schema discovery
- Formatting/minifying JSON for storage or transmission
- Building JSON diff tools and validators
- Creating JSON pretty-printers for CLI tools

Dependencies:
- json (stdlib)
- sys (stdlib)
- typing (stdlib)

Notes:
- All functions use ensure_ascii=False for proper Unicode handling
- Statistical analysis works recursively through nested structures
- Key extraction preserves dot-notation paths (e.g., "user.address.city")
- Validation returns both boolean and descriptive error messages
- No external dependencies required - pure Python stdlib

Related Snippets:
- data-processing/format_conversion_patterns.py - Multi-format conversion
- data-processing/pydantic_validation_patterns.py - Schema validation
- cli-tools/interactive_cli_with_llm.py - CLI patterns

Source Attribution:
- Extracted from: /home/coolhand/projects/apis/cli_tools/json_format.py
- Patterns used across multiple projects for JSON handling
"""

import json
import sys
from typing import Any, Dict, List, Set, Tuple, Union


# ===== JSON Validation =====

def validate_json(json_string: str) -> Tuple[bool, str]:
    """
    Validate JSON and return detailed error information.

    Args:
        json_string: String to validate as JSON

    Returns:
        Tuple of (is_valid, message)

    Example:
        >>> valid, msg = validate_json('{"name": "Alice"}')
        >>> valid
        True
        >>> msg
        'Valid JSON'

        >>> valid, msg = validate_json('{"name": Alice}')  # Invalid
        >>> valid
        False
        >>> 'Invalid JSON' in msg
        True
    """
    try:
        json.loads(json_string)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        error_details = (
            f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}\n"
            f"Error position: {e.pos}"
        )
        return False, error_details


def is_valid_json_file(filepath: str) -> Tuple[bool, str]:
    """
    Validate JSON from file.

    Args:
        filepath: Path to JSON file

    Returns:
        Tuple of (is_valid, message)

    Example:
        >>> is_valid_json_file('/path/to/data.json')
        (True, 'Valid JSON file')
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "Valid JSON file"
    except FileNotFoundError:
        return False, f"File not found: {filepath}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in file: {str(e)}"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


# ===== JSON Formatting =====

def format_json(
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    ensure_ascii: bool = False
) -> str:
    """
    Format JSON with customizable indentation and sorting.

    Args:
        data: Python object to format as JSON
        indent: Number of spaces for indentation
        sort_keys: Whether to sort dictionary keys alphabetically
        ensure_ascii: Whether to escape non-ASCII characters

    Returns:
        Formatted JSON string

    Example:
        >>> data = {"name": "Bob", "age": 30, "active": True}
        >>> print(format_json(data, indent=2))
        {
          "name": "Bob",
          "age": 30,
          "active": true
        }
    """
    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)


def minify_json(data: Any, ensure_ascii: bool = False) -> str:
    """
    Minify JSON by removing all unnecessary whitespace.

    Args:
        data: Python object to minify
        ensure_ascii: Whether to escape non-ASCII characters

    Returns:
        Minified JSON string

    Example:
        >>> data = {"name": "Alice", "items": [1, 2, 3]}
        >>> minify_json(data)
        '{"name":"Alice","items":[1,2,3]}'
    """
    return json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii)


def format_json_string(json_string: str, indent: int = 2) -> str:
    """
    Format a JSON string (parse and re-serialize).

    Args:
        json_string: JSON string to format
        indent: Indentation level

    Returns:
        Formatted JSON string

    Raises:
        json.JSONDecodeError: If string is not valid JSON
    """
    data = json.loads(json_string)
    return format_json(data, indent=indent)


# ===== JSON Statistics =====

class JSONStats:
    """
    Statistical analysis of JSON structure.

    Analyzes depth, object counts, and data type distribution.
    """

    @staticmethod
    def analyze(data: Any) -> Dict[str, int]:
        """
        Analyze JSON structure and return statistics.

        Args:
            data: JSON data (parsed Python object)

        Returns:
            Dictionary with statistics

        Example:
            >>> data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
            >>> stats = JSONStats.analyze(data)
            >>> stats['objects']
            3
            >>> stats['arrays']
            1
        """
        def count_elements(obj: Any, depth: int = 0) -> Dict[str, int]:
            stats = {
                'max_depth': depth,
                'objects': 0,
                'arrays': 0,
                'strings': 0,
                'numbers': 0,
                'booleans': 0,
                'nulls': 0,
                'total_keys': 0
            }

            if isinstance(obj, dict):
                stats['objects'] = 1
                stats['total_keys'] = len(obj)
                for value in obj.values():
                    sub_stats = count_elements(value, depth + 1)
                    for key in stats:
                        if key == 'max_depth':
                            stats[key] = max(stats[key], sub_stats[key])
                        else:
                            stats[key] += sub_stats[key]

            elif isinstance(obj, list):
                stats['arrays'] = 1
                for item in obj:
                    sub_stats = count_elements(item, depth + 1)
                    for key in stats:
                        if key == 'max_depth':
                            stats[key] = max(stats[key], sub_stats[key])
                        else:
                            stats[key] += sub_stats[key]

            elif isinstance(obj, str):
                stats['strings'] = 1
            elif isinstance(obj, bool):  # Must check before int
                stats['booleans'] = 1
            elif isinstance(obj, (int, float)):
                stats['numbers'] = 1
            elif obj is None:
                stats['nulls'] = 1

            return stats

        return count_elements(data)

    @staticmethod
    def print_stats(stats: Dict[str, int]) -> None:
        """
        Print formatted statistics.

        Args:
            stats: Statistics dictionary from analyze()
        """
        print("\nJSON Statistics:")
        print("=" * 50)
        print(f"Max Depth:     {stats['max_depth']}")
        print(f"Objects:       {stats['objects']}")
        print(f"Arrays:        {stats['arrays']}")
        print(f"Total Keys:    {stats['total_keys']}")
        print(f"Strings:       {stats['strings']}")
        print(f"Numbers:       {stats['numbers']}")
        print(f"Booleans:      {stats['booleans']}")
        print(f"Nulls:         {stats['nulls']}")
        print("=" * 50)


# ===== Key Extraction =====

def extract_all_keys(data: Any, include_indices: bool = False) -> List[str]:
    """
    Extract all keys from nested JSON structure.

    Uses dot notation for nested keys (e.g., "user.address.city").
    Optionally includes array indices in the path.

    Args:
        data: JSON data to analyze
        include_indices: Whether to include array indices in paths

    Returns:
        Sorted list of all key paths

    Example:
        >>> data = {
        ...     "user": {
        ...         "name": "Alice",
        ...         "addresses": [
        ...             {"city": "Boston"},
        ...             {"city": "NYC"}
        ...         ]
        ...     }
        ... }
        >>> keys = extract_all_keys(data)
        >>> "user.name" in keys
        True
        >>> "user.addresses.city" in keys
        True
    """
    keys: Set[str] = set()

    def traverse(obj: Any, current_path: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_path = f"{current_path}.{key}" if current_path else key
                keys.add(full_path)
                traverse(value, full_path)

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if include_indices:
                    full_path = f"{current_path}[{i}]"
                    traverse(item, full_path)
                else:
                    # Don't add index to path, just traverse the item
                    traverse(item, current_path)

    traverse(data)
    return sorted(keys)


def extract_unique_values_by_key(data: Any, target_key: str) -> Set[Any]:
    """
    Extract all unique values for a specific key across nested structure.

    Args:
        data: JSON data to search
        target_key: Key name to find values for

    Returns:
        Set of unique values

    Example:
        >>> data = {
        ...     "items": [
        ...         {"type": "book", "status": "available"},
        ...         {"type": "dvd", "status": "available"},
        ...         {"type": "book", "status": "checked_out"}
        ...     ]
        ... }
        >>> extract_unique_values_by_key(data, "type")
        {'book', 'dvd'}
    """
    values: Set[Any] = set()

    def traverse(obj: Any) -> None:
        if isinstance(obj, dict):
            if target_key in obj:
                value = obj[target_key]
                # Only add hashable values
                if isinstance(value, (str, int, float, bool, type(None))):
                    values.add(value)
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)
    return values


# ===== JSON Path Operations =====

def get_value_by_path(data: Any, path: str, delimiter: str = '.') -> Any:
    """
    Get value from nested JSON using dot-notation path.

    Args:
        data: JSON data
        path: Dot-notation path (e.g., "user.address.city")
        delimiter: Path delimiter character

    Returns:
        Value at path, or None if path doesn't exist

    Example:
        >>> data = {"user": {"name": "Alice", "age": 30}}
        >>> get_value_by_path(data, "user.name")
        'Alice'
        >>> get_value_by_path(data, "user.email") is None
        True
    """
    keys = path.split(delimiter)
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None

    return current


def set_value_by_path(
    data: Dict[str, Any],
    path: str,
    value: Any,
    delimiter: str = '.',
    create_missing: bool = True
) -> Dict[str, Any]:
    """
    Set value in nested JSON using dot-notation path.

    Args:
        data: JSON data (will be modified)
        path: Dot-notation path
        value: Value to set
        delimiter: Path delimiter
        create_missing: Whether to create missing intermediate keys

    Returns:
        Modified data dictionary

    Example:
        >>> data = {"user": {"name": "Alice"}}
        >>> set_value_by_path(data, "user.age", 30)
        {'user': {'name': 'Alice', 'age': 30}}
        >>> set_value_by_path(data, "user.address.city", "Boston")
        {'user': {'name': 'Alice', 'age': 30, 'address': {'city': 'Boston'}}}
    """
    keys = path.split(delimiter)
    current = data

    # Navigate to parent of target key
    for key in keys[:-1]:
        if key not in current:
            if create_missing:
                current[key] = {}
            else:
                raise KeyError(f"Path not found: {path}")
        current = current[key]

    # Set the final value
    current[keys[-1]] = value
    return data


# ===== JSON Comparison =====

def find_differences(obj1: Any, obj2: Any, path: str = "") -> List[Dict[str, Any]]:
    """
    Find differences between two JSON structures.

    Args:
        obj1: First JSON object
        obj2: Second JSON object
        path: Current path (used for recursion)

    Returns:
        List of differences with paths and values

    Example:
        >>> obj1 = {"name": "Alice", "age": 25}
        >>> obj2 = {"name": "Alice", "age": 30}
        >>> diffs = find_differences(obj1, obj2)
        >>> len(diffs)
        1
        >>> diffs[0]['path']
        'age'
    """
    differences = []

    if type(obj1) != type(obj2):
        differences.append({
            "path": path or "root",
            "type": "type_mismatch",
            "value1": type(obj1).__name__,
            "value2": type(obj2).__name__
        })
        return differences

    if isinstance(obj1, dict):
        all_keys = set(obj1.keys()) | set(obj2.keys())
        for key in all_keys:
            current_path = f"{path}.{key}" if path else key

            if key not in obj1:
                differences.append({
                    "path": current_path,
                    "type": "missing_in_first",
                    "value": obj2[key]
                })
            elif key not in obj2:
                differences.append({
                    "path": current_path,
                    "type": "missing_in_second",
                    "value": obj1[key]
                })
            else:
                differences.extend(find_differences(obj1[key], obj2[key], current_path))

    elif isinstance(obj1, list):
        max_len = max(len(obj1), len(obj2))
        for i in range(max_len):
            current_path = f"{path}[{i}]"

            if i >= len(obj1):
                differences.append({
                    "path": current_path,
                    "type": "extra_in_second",
                    "value": obj2[i]
                })
            elif i >= len(obj2):
                differences.append({
                    "path": current_path,
                    "type": "extra_in_first",
                    "value": obj1[i]
                })
            else:
                differences.extend(find_differences(obj1[i], obj2[i], current_path))

    else:
        # Primitive values
        if obj1 != obj2:
            differences.append({
                "path": path or "root",
                "type": "value_difference",
                "value1": obj1,
                "value2": obj2
            })

    return differences


# ===== Usage Examples =====

if __name__ == "__main__":
    print("=" * 70)
    print("JSON Validation and Analysis Patterns - Usage Examples")
    print("=" * 70)

    # Sample data
    sample_data = {
        "project": "AI Platform",
        "version": "2.0",
        "users": [
            {"name": "Alice", "role": "Engineer", "active": True},
            {"name": "Bob", "role": "Designer", "active": False}
        ],
        "config": {
            "timeout": 30,
            "retry": 3,
            "endpoints": {
                "api": "https://api.example.com",
                "web": "https://example.com"
            }
        }
    }

    # 1. JSON Validation
    print("\n1. JSON Validation:")
    print("-" * 70)
    json_str = json.dumps(sample_data)
    valid, msg = validate_json(json_str)
    print(f"Valid: {valid}, Message: {msg}")

    # 2. JSON Formatting
    print("\n2. JSON Formatting:")
    print("-" * 70)
    print("Pretty format:")
    print(format_json(sample_data, indent=2))
    print("\nMinified format:")
    print(minify_json(sample_data))

    # 3. JSON Statistics
    print("\n3. JSON Statistics:")
    print("-" * 70)
    stats = JSONStats.analyze(sample_data)
    JSONStats.print_stats(stats)

    # 4. Key Extraction
    print("\n4. Extracting All Keys:")
    print("-" * 70)
    keys = extract_all_keys(sample_data)
    print("All key paths:")
    for key in keys:
        print(f"  - {key}")

    # 5. Extract Unique Values
    print("\n5. Extract Unique Values by Key:")
    print("-" * 70)
    roles = extract_unique_values_by_key(sample_data, "role")
    print(f"Unique roles: {roles}")

    # 6. Path Operations
    print("\n6. JSON Path Operations:")
    print("-" * 70)
    value = get_value_by_path(sample_data, "config.endpoints.api")
    print(f"API endpoint: {value}")

    modified = sample_data.copy()
    set_value_by_path(modified, "config.max_connections", 100)
    print(f"After setting new value: {modified['config'].get('max_connections')}")

    # 7. JSON Comparison
    print("\n7. Finding Differences:")
    print("-" * 70)
    obj1 = {"name": "Alice", "age": 25, "city": "Boston"}
    obj2 = {"name": "Alice", "age": 30, "country": "USA"}
    diffs = find_differences(obj1, obj2)
    print("Differences found:")
    for diff in diffs:
        print(f"  - Path: {diff['path']}, Type: {diff['type']}")
        if 'value1' in diff and 'value2' in diff:
            print(f"    Value1: {diff['value1']}, Value2: {diff['value2']}")

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
