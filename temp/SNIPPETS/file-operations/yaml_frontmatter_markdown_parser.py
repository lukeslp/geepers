# ================================================
# YAML Frontmatter Markdown Parser
# ================================================
# Language: python
# Tags: yaml, markdown, parsing, frontmatter, metadata
# Source: geepers-orchestrators/parser/markdown_parser.py
# Last Updated: 2025-12-12
# Author: Luke Steuber
# ================================================
# Description:
# Complete toolkit for parsing markdown files with YAML frontmatter.
# Extracts metadata, sections by headers, tables, and nested structures.
# Useful for agent definitions, documentation systems, and config files.
#
# Use Cases:
# - Parsing agent definition files with structured metadata
# - Building documentation systems from markdown
# - Extracting configuration from markdown files
# - Converting markdown tables to structured data
# - Processing Jekyll/Hugo-style content
#
# Dependencies:
# - re (built-in)
# - yaml (pip install pyyaml)
# - pathlib (built-in)
# - typing (built-in)
#
# Notes:
# - Frontmatter must start and end with '---'
# - Headers use ## for section detection
# - Tables must have proper markdown format with header separator
# - Nested sections (###) can be parsed with custom patterns
#
# Related Snippets:
# - /home/coolhand/SNIPPETS/file-operations/module_discovery.py
# - /home/coolhand/SNIPPETS/configuration-management/multi_source_config.py
# ================================================

import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import yaml


# ============================================================================
# FRONTMATTER PARSING
# ============================================================================

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract YAML frontmatter from markdown content.

    Frontmatter must be at the very start of the file, wrapped in '---'.

    Args:
        content: Full markdown file content

    Returns:
        Tuple of (frontmatter dict, remaining content)

    Example:
        >>> content = '''---
        ... title: My Document
        ... author: Luke
        ... ---
        ... # Content here
        ... '''
        >>> meta, body = parse_frontmatter(content)
        >>> meta['title']
        'My Document'
    """
    if not content.startswith('---'):
        return {}, content

    # Find the closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return {}, content

    # Extract frontmatter text (between --- markers)
    frontmatter_text = content[3:end_match.start() + 3]
    remaining = content[end_match.end() + 3:]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter or {}, remaining
    except yaml.YAMLError as e:
        print(f"Warning: Failed to parse YAML frontmatter: {e}")
        return {}, content


# ============================================================================
# SECTION PARSING
# ============================================================================

def parse_sections(content: str, header_level: str = "## ") -> Dict[str, str]:
    """
    Parse markdown into sections by header level.

    Args:
        content: Markdown content (without frontmatter)
        header_level: Header marker (default "## " for level 2)

    Returns:
        Dict mapping section names to their content

    Example:
        >>> content = '''
        ... ## Introduction
        ... Some intro text
        ... ## Methods
        ... Some methods
        ... '''
        >>> sections = parse_sections(content)
        >>> 'Introduction' in sections
        True
    """
    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        if line.startswith(header_level):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()

            # Start new section
            current_section = line[len(header_level):].strip()
            current_content = []
        elif current_section:
            current_content.append(line)

    # Save final section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def parse_nested_sections(
    content: str,
    level2_marker: str = "## ",
    level3_marker: str = "### "
) -> Dict[str, Dict[str, str]]:
    """
    Parse markdown with nested section structure.

    Args:
        content: Markdown content
        level2_marker: Level 2 header marker
        level3_marker: Level 3 header marker

    Returns:
        Dict mapping level 2 sections to dicts of level 3 sections

    Example:
        >>> content = '''
        ... ## Parent
        ... ### Child 1
        ... Content 1
        ... ### Child 2
        ... Content 2
        ... '''
        >>> nested = parse_nested_sections(content)
        >>> nested['Parent']['Child 1']
        'Content 1'
    """
    nested = {}
    current_l2 = None
    current_l3 = None
    current_content = []

    for line in content.split('\n'):
        if line.startswith(level2_marker) and not line.startswith(level3_marker):
            # Save previous L3 section
            if current_l2 and current_l3:
                if current_l2 not in nested:
                    nested[current_l2] = {}
                nested[current_l2][current_l3] = '\n'.join(current_content).strip()

            # Start new L2 section
            current_l2 = line[len(level2_marker):].strip()
            current_l3 = None
            current_content = []

        elif line.startswith(level3_marker):
            # Save previous L3 section
            if current_l2 and current_l3:
                if current_l2 not in nested:
                    nested[current_l2] = {}
                nested[current_l2][current_l3] = '\n'.join(current_content).strip()

            # Start new L3 section
            current_l3 = line[len(level3_marker):].strip()
            current_content = []

        elif current_l2:
            current_content.append(line)

    # Save final section
    if current_l2 and current_l3:
        if current_l2 not in nested:
            nested[current_l2] = {}
        nested[current_l2][current_l3] = '\n'.join(current_content).strip()

    return nested


# ============================================================================
# TABLE PARSING
# ============================================================================

def parse_table(content: str) -> List[Dict[str, str]]:
    """
    Parse a markdown table into list of dicts.

    Args:
        content: Markdown content containing a table

    Returns:
        List of dicts with column names as keys

    Example:
        >>> table_md = '''
        ... | Name | Age |
        ... |------|-----|
        ... | Alice | 30 |
        ... | Bob | 25 |
        ... '''
        >>> rows = parse_table(table_md)
        >>> rows[0]['Name']
        'Alice'
    """
    lines = [line.strip() for line in content.split('\n') if line.strip() and '|' in line]
    if len(lines) < 2:
        return []

    # Parse header
    headers = [h.strip() for h in lines[0].split('|') if h.strip()]

    # Skip separator line (contains ---)
    rows = []
    for line in lines[1:]:
        if '---' in line:
            continue

        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= len(headers):
            rows.append(dict(zip(headers, cells[:len(headers)])))

    return rows


# ============================================================================
# LIST PARSING
# ============================================================================

def parse_bullet_list(content: str) -> List[str]:
    """
    Parse markdown bullet list into list of strings.

    Args:
        content: Markdown content with bullet list

    Returns:
        List of bullet items (without markers)

    Example:
        >>> list_md = '''
        ... - Item 1
        ... - Item 2
        ... - Item 3
        ... '''
        >>> items = parse_bullet_list(list_md)
        >>> len(items)
        3
    """
    items = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- '):
            items.append(line[2:].strip())
        elif line.startswith('* '):
            items.append(line[2:].strip())
    return items


def parse_numbered_list(content: str) -> List[str]:
    """
    Parse markdown numbered list into list of strings.

    Args:
        content: Markdown content with numbered list

    Returns:
        List of items (without numbers)

    Example:
        >>> list_md = '''
        ... 1. First item
        ... 2. Second item
        ... 3. Third item
        ... '''
        >>> items = parse_numbered_list(list_md)
        >>> items[0]
        'First item'
    """
    items = []
    for line in content.split('\n'):
        line = line.strip()
        match = re.match(r'^\d+\.\s+(.+)$', line)
        if match:
            items.append(match.group(1))
    return items


# ============================================================================
# CODE BLOCK EXTRACTION
# ============================================================================

def extract_code_blocks(content: str) -> Dict[str, List[str]]:
    """
    Extract code blocks from markdown, organized by language.

    Args:
        content: Markdown content with fenced code blocks

    Returns:
        Dict mapping language to list of code blocks

    Example:
        >>> md = '''
        ... ```python
        ... print("hello")
        ... ```
        ... ```python
        ... print("world")
        ... ```
        ... '''
        >>> blocks = extract_code_blocks(md)
        >>> len(blocks['python'])
        2
    """
    code_blocks = {}
    pattern = r'```(\w+)?\n(.*?)```'

    for match in re.finditer(pattern, content, re.DOTALL):
        language = match.group(1) or 'unknown'
        code = match.group(2).strip()

        if language not in code_blocks:
            code_blocks[language] = []
        code_blocks[language].append(code)

    return code_blocks


# ============================================================================
# METADATA EXTRACTION
# ============================================================================

def extract_key_value_pairs(content: str) -> Dict[str, str]:
    """
    Extract key-value pairs from markdown content.

    Looks for patterns like:
    - **Key**: `value`
    - **Key:** value

    Args:
        content: Markdown content

    Returns:
        Dict of extracted key-value pairs

    Example:
        >>> md = '''
        ... - **Name**: `geepers`
        ... - **Version:** 1.0
        ... '''
        >>> pairs = extract_key_value_pairs(md)
        >>> pairs['Name']
        'geepers'
    """
    pairs = {}

    # Pattern 1: **Key**: `value`
    pattern1 = r'\*\*(.+?)\*\*:\s+`(.+?)`'
    for match in re.finditer(pattern1, content):
        pairs[match.group(1).strip()] = match.group(2).strip()

    # Pattern 2: **Key:** value (without backticks)
    pattern2 = r'\*\*(.+?)\*\*:\s+([^\n]+)'
    for match in re.finditer(pattern2, content):
        key = match.group(1).strip()
        if key not in pairs:  # Don't overwrite pattern 1 matches
            value = match.group(2).strip()
            # Remove backticks if present
            value = value.strip('`')
            pairs[key] = value

    return pairs


# ============================================================================
# FILE PARSING
# ============================================================================

def parse_markdown_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a markdown file with frontmatter and sections.

    Args:
        file_path: Path to markdown file

    Returns:
        Dict with 'frontmatter', 'sections', 'tables', etc.

    Example:
        >>> result = parse_markdown_file(Path('doc.md'))
        >>> result['frontmatter']['title']
        'My Document'
        >>> 'Introduction' in result['sections']
        True
    """
    content = file_path.read_text()

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    # Parse sections
    sections = parse_sections(body)

    # Parse tables from all sections
    tables = {}
    for section_name, section_content in sections.items():
        table_data = parse_table(section_content)
        if table_data:
            tables[section_name] = table_data

    # Extract code blocks
    code_blocks = extract_code_blocks(body)

    return {
        'frontmatter': frontmatter,
        'sections': sections,
        'tables': tables,
        'code_blocks': code_blocks,
        'source_file': file_path,
    }


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Parse frontmatter
    example_md = """---
title: Agent Definition
version: 1.0
model: sonnet
---

## Mission
This agent performs reconnaissance on code repositories.

## Coordinated Agents
| Agent | Role | Output |
|-------|------|--------|
| geepers_scout | Code analysis | ~/geepers/reports/ |
| geepers_repo | Git hygiene | ~/geepers/reports/ |

## Quality Standards
1. Remove hardcoded values
2. Add type hints
3. Include error handling

## Workflow
### Phase 1: Analysis
**Dispatch**: `geepers_scout`
**Purpose**: Scan for issues

### Phase 2: Fixes
**Dispatch**: `geepers_repo`
**Purpose**: Apply fixes
"""

    print("=" * 60)
    print("EXAMPLE 1: Parse complete markdown file")
    print("=" * 60)

    frontmatter, body = parse_frontmatter(example_md)
    print(f"\nFrontmatter: {frontmatter}")

    sections = parse_sections(body)
    print(f"\nSections found: {list(sections.keys())}")

    if 'Coordinated Agents' in sections:
        table_data = parse_table(sections['Coordinated Agents'])
        print(f"\nTable data:")
        for row in table_data:
            print(f"  {row}")

    if 'Quality Standards' in sections:
        standards = parse_numbered_list(sections['Quality Standards'])
        print(f"\nQuality Standards:")
        for standard in standards:
            print(f"  - {standard}")

    # Example 2: Nested sections
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Parse nested sections")
    print("=" * 60)

    nested = parse_nested_sections(body)
    if 'Workflow' in nested:
        print(f"\nWorkflow phases:")
        for phase_name, phase_content in nested['Workflow'].items():
            print(f"\n  {phase_name}:")
            metadata = extract_key_value_pairs(phase_content)
            for key, value in metadata.items():
                print(f"    {key}: {value}")

    # Example 3: Code blocks
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Extract code blocks")
    print("=" * 60)

    code_example = """
Some text here.

```python
def hello():
    print("Hello!")
```

More text.

```python
def world():
    print("World!")
```
"""

    code_blocks = extract_code_blocks(code_example)
    print(f"\nCode blocks found: {code_blocks}")
