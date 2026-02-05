"""
Markdown Document Generation

Provides enhanced markdown generation with metadata, frontmatter, and formatting.
Supports YAML frontmatter, tables, code blocks, and comprehensive markdown features.

Author: Luke Steuber
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generate enhanced markdown documents from structured content"""

    def __init__(self, output_dir: str = "reports/markdown"):
        """
        Initialize markdown generator

        Args:
            output_dir: Directory for markdown output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report_markdown(
        self,
        content_sections: List[Dict[str, Any]],
        title: str,
        document_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        include_frontmatter: bool = True,
        include_toc: bool = False
    ) -> Dict[str, Any]:
        """
        Generate markdown report from structured content sections

        Args:
            content_sections: List of content sections with title and content
            title: Document title
            document_id: Unique document identifier
            metadata: Optional metadata dict
            include_frontmatter: Include YAML frontmatter
            include_toc: Include table of contents

        Returns:
            Dict with success status, filepath, filename, and content
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{document_id}_{timestamp}.md"
            filepath = self.output_dir / filename

            # Build markdown content
            md_content = []

            # YAML frontmatter
            if include_frontmatter:
                md_content.append("---")
                md_content.append(f"title: {title}")
                md_content.append(f"document_id: {document_id}")
                md_content.append(f"generated: {datetime.now().isoformat()}")

                if metadata:
                    for key, value in metadata.items():
                        # Handle different value types
                        if isinstance(value, (list, dict)):
                            md_content.append(f"{key}: {json.dumps(value)}")
                        else:
                            md_content.append(f"{key}: {value}")

                md_content.append("---")
                md_content.append("")

            # Title
            md_content.append(f"# {title}")
            md_content.append("")

            # Metadata section
            if metadata and not include_frontmatter:
                md_content.append("## Document Information")
                md_content.append("")
                md_content.append(f"- **Document ID:** {document_id}")
                md_content.append(f"- **Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

                for key, value in metadata.items():
                    formatted_key = key.replace('_', ' ').title()
                    md_content.append(f"- **{formatted_key}:** {value}")

                md_content.append("")

            # Table of contents
            if include_toc:
                md_content.append("## Table of Contents")
                md_content.append("")

                for i, section in enumerate(content_sections, 1):
                    section_title = section.get('title', f'Section {i}')
                    # Create anchor link
                    anchor = section_title.lower().replace(' ', '-').replace('.', '')
                    md_content.append(f"{i}. [{section_title}](#{anchor})")

                md_content.append("")
                md_content.append("---")
                md_content.append("")

            # Content sections
            for section in content_sections:
                section_title = section.get('title', 'Untitled Section')
                section_content = section.get('content', '')
                section.get('type', 'content')

                # Section header
                md_content.append(f"## {section_title}")
                md_content.append("")

                # Section content (already markdown formatted)
                md_content.append(section_content)
                md_content.append("")
                md_content.append("---")
                md_content.append("")

            # Join all content
            full_content = '\n'.join(md_content)

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            return {
                "success": True,
                "filepath": str(filepath),
                "filename": filename,
                "size_bytes": filepath.stat().st_size,
                "content": full_content
            }

        except Exception as e:
            logger.error(f"Markdown generation error: {e}")
            return {"success": False, "error": str(e)}

    def create_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        alignment: Optional[List[str]] = None
    ) -> str:
        """
        Create markdown table

        Args:
            headers: Column headers
            rows: Table rows
            alignment: List of 'left', 'center', or 'right' for each column

        Returns:
            Markdown-formatted table string
        """
        if not headers or not rows:
            return ""

        # Default alignment to left
        if not alignment:
            alignment = ['left'] * len(headers)

        # Build table
        table_lines = []

        # Header row
        table_lines.append('| ' + ' | '.join(headers) + ' |')

        # Separator row with alignment
        separators = []
        for align in alignment:
            if align == 'center':
                separators.append(':---:')
            elif align == 'right':
                separators.append('---:')
            else:
                separators.append('---')

        table_lines.append('| ' + ' | '.join(separators) + ' |')

        # Data rows
        for row in rows:
            # Pad row to match header length
            padded_row = row + [''] * (len(headers) - len(row))
            table_lines.append('| ' + ' | '.join(str(cell) for cell in padded_row) + ' |')

        return '\n'.join(table_lines)

    def create_code_block(self, code: str, language: str = "") -> str:
        """
        Create markdown code block

        Args:
            code: Code content
            language: Programming language for syntax highlighting

        Returns:
            Markdown-formatted code block
        """
        return f"```{language}\n{code}\n```"

    def create_callout(
        self,
        content: str,
        callout_type: str = "info"
    ) -> str:
        """
        Create markdown callout/admonition

        Args:
            content: Callout content
            callout_type: Type (info, warning, danger, success, note)

        Returns:
            Markdown-formatted callout
        """
        emoji_map = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'danger': '🚫',
            'success': '✅',
            'note': '📝'
        }

        emoji = emoji_map.get(callout_type, '📌')
        type_upper = callout_type.upper()

        return f"> {emoji} **{type_upper}**\n> \n> {content}"

    def create_details_section(self, summary: str, details: str) -> str:
        """
        Create collapsible details section (GitHub-flavored markdown)

        Args:
            summary: Summary text (always visible)
            details: Details text (collapsible)

        Returns:
            Markdown-formatted details section
        """
        return f"<details>\n<summary>{summary}</summary>\n\n{details}\n</details>"


def generate_markdown_report(
    content_sections: List[Dict[str, Any]],
    title: str,
    document_id: str,
    output_dir: str = "reports/markdown",
    metadata: Optional[Dict[str, Any]] = None,
    include_frontmatter: bool = True,
    include_toc: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to generate a markdown report

    Args:
        content_sections: List of content sections
        title: Document title
        document_id: Unique document identifier
        output_dir: Output directory
        metadata: Optional metadata
        include_frontmatter: Include YAML frontmatter
        include_toc: Include table of contents

    Returns:
        Dict with success status and file information
    """
    try:
        generator = MarkdownGenerator(output_dir=output_dir)
        return generator.generate_report_markdown(
            content_sections=content_sections,
            title=title,
            document_id=document_id,
            metadata=metadata,
            include_frontmatter=include_frontmatter,
            include_toc=include_toc
        )
    except Exception as e:
        logger.error(f"Markdown report generation failed: {e}")
        return {"success": False, "error": str(e)}
