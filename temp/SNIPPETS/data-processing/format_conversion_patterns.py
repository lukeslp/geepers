"""
Multi-Format Data Conversion Patterns

Description: Comprehensive patterns for converting data between JSON, YAML, TOML, XML, and CSV formats with proper error handling and validation.

Use Cases:
- Converting configuration files between formats (JSON ↔ YAML ↔ TOML)
- Transforming API responses to different output formats
- Batch converting data export files
- Data migration between systems with different format requirements
- Building format-agnostic data processing pipelines

Dependencies:
- json (stdlib)
- xml.dom.minidom (stdlib)
- io (stdlib)
- csv (stdlib)
- yaml (pip install pyyaml)
- toml (pip install toml)
- typing (stdlib)

Notes:
- CSV conversion works best with flat data structures (lists of dicts or simple dicts)
- XML conversion uses a simple dict-to-XML mapping; complex schemas may need custom logic
- YAML preserves key order and supports more data types than JSON
- TOML is ideal for configuration files with nested sections
- All conversions handle Unicode properly with ensure_ascii=False
- Error handling returns informative messages for debugging

Related Snippets:
- data-processing/json_validation_patterns.py - JSON-specific validation
- data-processing/pydantic_validation_patterns.py - Schema validation with Pydantic
- error-handling/graceful_import_fallbacks.py - Optional dependency handling

Source Attribution:
- Extracted from: /home/coolhand/projects/apis/api-v3/gen/api-tools/tools/data/processing/data_processor.py
- Also inspired by: /home/coolhand/projects/apis/cli_tools/json_format.py
- Related patterns: /home/coolhand/projects/swarm/hive/swarm_data.py
"""

import json
import yaml
import toml
import xml.dom.minidom
import csv
import io
from typing import Any, Dict, List, Union, Optional


# ===== JSON Conversion =====

def convert_to_json(data: Any, indent: Optional[int] = 2, sort_keys: bool = False) -> str:
    """
    Convert data to formatted JSON string.

    Args:
        data: Python object to convert
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys alphabetically

    Returns:
        Formatted JSON string

    Example:
        >>> data = {"name": "Alice", "age": 30, "skills": ["Python", "SQL"]}
        >>> json_str = convert_to_json(data, indent=2)
        >>> print(json_str)
        {
          "name": "Alice",
          "age": 30,
          "skills": [
            "Python",
            "SQL"
          ]
        }
    """
    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)


def minify_json(data: Any) -> str:
    """
    Convert data to compact JSON string (no whitespace).

    Args:
        data: Python object to convert

    Returns:
        Minified JSON string

    Example:
        >>> data = {"name": "Bob", "active": True}
        >>> minify_json(data)
        '{"name":"Bob","active":true}'
    """
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)


# ===== YAML Conversion =====

def convert_to_yaml(data: Any, sort_keys: bool = False) -> str:
    """
    Convert data to YAML format.

    Args:
        data: Python object to convert
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML formatted string

    Example:
        >>> data = {"name": "Charlie", "tags": ["dev", "ops"]}
        >>> print(convert_to_yaml(data))
        name: Charlie
        tags:
        - dev
        - ops
    """
    return yaml.dump(data, sort_keys=sort_keys, allow_unicode=True, default_flow_style=False)


def parse_yaml(yaml_str: str) -> Any:
    """
    Parse YAML string to Python object.

    Args:
        yaml_str: YAML formatted string

    Returns:
        Parsed Python object

    Example:
        >>> yaml_str = "name: Diana\\nage: 28"
        >>> parse_yaml(yaml_str)
        {'name': 'Diana', 'age': 28}
    """
    return yaml.safe_load(yaml_str)


# ===== TOML Conversion =====

def convert_to_toml(data: Dict[str, Any]) -> str:
    """
    Convert dictionary to TOML format.

    Args:
        data: Dictionary to convert (must be a dict, not list)

    Returns:
        TOML formatted string

    Raises:
        TypeError: If data is not a dictionary

    Example:
        >>> data = {
        ...     "server": {"host": "localhost", "port": 5000},
        ...     "database": {"name": "mydb"}
        ... }
        >>> print(convert_to_toml(data))
        [server]
        host = "localhost"
        port = 5000

        [database]
        name = "mydb"
    """
    if not isinstance(data, dict):
        raise TypeError("TOML conversion requires a dictionary")
    return toml.dumps(data)


def parse_toml(toml_str: str) -> Dict[str, Any]:
    """
    Parse TOML string to dictionary.

    Args:
        toml_str: TOML formatted string

    Returns:
        Parsed dictionary
    """
    return toml.loads(toml_str)


# ===== XML Conversion =====

def convert_to_xml(data: Dict[str, Any], root_name: str = "root", indent: str = "  ") -> str:
    """
    Convert dictionary to XML format.

    Args:
        data: Dictionary to convert
        root_name: Name of the root XML element
        indent: Indentation string

    Returns:
        XML formatted string

    Example:
        >>> data = {"user": {"name": "Eve", "id": 123}}
        >>> print(convert_to_xml(data, root_name="response"))
        <?xml version="1.0" ?>
        <response>
          <user>
            <name>Eve</name>
            <id>123</id>
          </user>
        </response>
    """
    def dict_to_xml(data: Dict, root_name: str) -> str:
        doc = xml.dom.minidom.Document()
        root = doc.createElement(root_name)
        doc.appendChild(root)

        def add_element(parent, key, value):
            if isinstance(value, dict):
                child = doc.createElement(key)
                for k, v in value.items():
                    add_element(child, k, v)
                parent.appendChild(child)
            elif isinstance(value, list):
                for item in value:
                    child = doc.createElement(key)
                    if isinstance(item, dict):
                        for k, v in item.items():
                            add_element(child, k, v)
                    else:
                        child.appendChild(doc.createTextNode(str(item)))
                    parent.appendChild(child)
            else:
                child = doc.createElement(key)
                child.appendChild(doc.createTextNode(str(value)))
                parent.appendChild(child)

        for key, value in data.items():
            add_element(root, key, value)

        return doc.toprettyxml(indent=indent)

    return dict_to_xml(data, root_name)


# ===== CSV Conversion =====

def convert_to_csv(data: Union[List[Dict], Dict], delimiter: str = ',') -> str:
    """
    Convert data to CSV format.

    Args:
        data: List of dictionaries (rows) or simple dictionary (key-value pairs)
        delimiter: Field delimiter character

    Returns:
        CSV formatted string

    Example:
        >>> data = [
        ...     {"name": "Alice", "score": 95},
        ...     {"name": "Bob", "score": 87}
        ... ]
        >>> print(convert_to_csv(data))
        name,score
        Alice,95
        Bob,87

        >>> data = {"key1": "value1", "key2": "value2"}
        >>> print(convert_to_csv(data))
        key1,value1
        key2,value2
    """
    output = io.StringIO()

    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            # List of dictionaries - write as rows with headers
            writer = csv.DictWriter(output, fieldnames=data[0].keys(), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
        else:
            # List of simple values
            writer = csv.writer(output, delimiter=delimiter)
            writer.writerows([[item] for item in data])
    elif isinstance(data, dict):
        # Dictionary - write as key-value pairs
        writer = csv.writer(output, delimiter=delimiter)
        writer.writerows([[k, v] for k, v in data.items()])
    else:
        raise TypeError(f"Cannot convert {type(data)} to CSV")

    return output.getvalue()


def parse_csv_to_dict_list(csv_str: str, delimiter: str = ',') -> List[Dict[str, str]]:
    """
    Parse CSV string to list of dictionaries.

    Args:
        csv_str: CSV formatted string
        delimiter: Field delimiter character

    Returns:
        List of dictionaries with headers as keys

    Example:
        >>> csv_str = "name,age\\nAlice,30\\nBob,25"
        >>> parse_csv_to_dict_list(csv_str)
        [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    """
    reader = csv.DictReader(io.StringIO(csv_str), delimiter=delimiter)
    return list(reader)


# ===== Universal Format Converter =====

class FormatConverter:
    """
    Universal data format converter with validation.

    Supports: JSON, YAML, TOML, XML, CSV
    """

    SUPPORTED_FORMATS = ['json', 'yaml', 'toml', 'xml', 'csv']

    @staticmethod
    def convert(
        data: Any,
        target_format: str,
        source_format: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Convert data to target format.

        Args:
            data: Data to convert (can be string or Python object)
            target_format: Target format (json, yaml, toml, xml, csv)
            source_format: Source format if data is a string (auto-detect if None)
            **kwargs: Format-specific options

        Returns:
            Converted data as string

        Raises:
            ValueError: If format is unsupported or conversion fails

        Example:
            >>> converter = FormatConverter()
            >>> data = {"name": "Test", "value": 42}
            >>> yaml_output = converter.convert(data, "yaml")
            >>> print(yaml_output)
            name: Test
            value: 42
        """
        target_format = target_format.lower()

        if target_format not in FormatConverter.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported target format: {target_format}. "
                           f"Supported: {', '.join(FormatConverter.SUPPORTED_FORMATS)}")

        # Parse input if it's a string
        if isinstance(data, str):
            if source_format:
                data = FormatConverter._parse_format(data, source_format.lower())
            else:
                # Try to auto-detect
                data = FormatConverter._auto_parse(data)

        # Convert to target format
        if target_format == 'json':
            indent = kwargs.get('indent', 2)
            sort_keys = kwargs.get('sort_keys', False)
            return convert_to_json(data, indent=indent, sort_keys=sort_keys)

        elif target_format == 'yaml':
            sort_keys = kwargs.get('sort_keys', False)
            return convert_to_yaml(data, sort_keys=sort_keys)

        elif target_format == 'toml':
            return convert_to_toml(data)

        elif target_format == 'xml':
            root_name = kwargs.get('root_name', 'root')
            indent = kwargs.get('xml_indent', '  ')
            return convert_to_xml(data, root_name=root_name, indent=indent)

        elif target_format == 'csv':
            delimiter = kwargs.get('delimiter', ',')
            return convert_to_csv(data, delimiter=delimiter)

    @staticmethod
    def _parse_format(data_str: str, format_name: str) -> Any:
        """Parse string according to specified format."""
        if format_name == 'json':
            return json.loads(data_str)
        elif format_name == 'yaml':
            return parse_yaml(data_str)
        elif format_name == 'toml':
            return parse_toml(data_str)
        elif format_name == 'csv':
            return parse_csv_to_dict_list(data_str)
        else:
            raise ValueError(f"Cannot parse format: {format_name}")

    @staticmethod
    def _auto_parse(data_str: str) -> Any:
        """Attempt to auto-detect and parse format."""
        # Try JSON first (most common)
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            pass

        # Try YAML
        try:
            return parse_yaml(data_str)
        except yaml.YAMLError:
            pass

        # Try TOML
        try:
            return parse_toml(data_str)
        except toml.TomlDecodeError:
            pass

        # Give up
        raise ValueError("Could not auto-detect format. Please specify source_format.")


# ===== Usage Examples =====

if __name__ == "__main__":
    print("=" * 70)
    print("Format Conversion Patterns - Usage Examples")
    print("=" * 70)

    # Sample data
    sample_data = {
        "project": "AI Platform",
        "version": "2.0",
        "features": ["search", "analysis", "generation"],
        "config": {
            "timeout": 30,
            "retry": 3
        }
    }

    print("\n1. JSON Conversion:")
    print("-" * 70)
    json_output = convert_to_json(sample_data, indent=2)
    print(json_output)

    print("\n2. YAML Conversion:")
    print("-" * 70)
    yaml_output = convert_to_yaml(sample_data)
    print(yaml_output)

    print("\n3. TOML Conversion:")
    print("-" * 70)
    toml_output = convert_to_toml(sample_data)
    print(toml_output)

    print("\n4. XML Conversion:")
    print("-" * 70)
    xml_output = convert_to_xml(sample_data, root_name="project_info")
    print(xml_output)

    print("\n5. CSV Conversion (List of Dicts):")
    print("-" * 70)
    users = [
        {"name": "Alice", "role": "Engineer", "level": 5},
        {"name": "Bob", "role": "Designer", "level": 4},
        {"name": "Charlie", "role": "Manager", "level": 6}
    ]
    csv_output = convert_to_csv(users)
    print(csv_output)

    print("\n6. Universal Converter:")
    print("-" * 70)
    converter = FormatConverter()

    # JSON to YAML
    yaml_from_json = converter.convert(sample_data, "yaml")
    print("JSON → YAML:")
    print(yaml_from_json)

    # Parse and re-convert
    print("\nYAML → JSON:")
    json_from_yaml = converter.convert(yaml_from_json, "json", source_format="yaml")
    print(json_from_yaml)

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
