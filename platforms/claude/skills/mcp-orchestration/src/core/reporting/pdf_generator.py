"""
PDF Document Generation

Provides professional PDF generation capabilities for reports and documents.
Supports embedded viewing, custom styling, and comprehensive formatting.

Author: Luke Steuber
"""

import base64
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# PDF Generation imports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("ReportLab not available - PDF generation disabled")


class PDFGenerator:
    """Generate professional PDF documents from structured content"""

    def __init__(
        self,
        output_dir: str = "reports/pdf",
        page_size=None,
        title_color: str = "#1a73e8",
        default_font: str = "Helvetica"
    ):
        """
        Initialize PDF generator

        Args:
            output_dir: Directory for PDF output
            page_size: Page size (letter, A4, etc.) - defaults to letter
            title_color: Hex color for titles
            default_font: Default font family
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not PDF_AVAILABLE:
            raise ImportError(
                "ReportLab is required for PDF generation. "
                "Install with: pip install reportlab"
            )

        self.page_size = page_size or letter
        self.title_color = colors.HexColor(title_color)
        self.default_font = default_font

    def generate_report_pdf(
        self,
        content_sections: List[Dict[str, Any]],
        title: str,
        document_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        include_base64: bool = False
    ) -> Dict[str, Any]:
        """
        Generate PDF report from structured content sections

        Args:
            content_sections: List of content sections, each with:
                - title: Section title
                - content: Section content (markdown-style string)
                - type: Optional section type (agent, summary, etc.)
            title: Document title
            document_id: Unique document identifier
            metadata: Optional metadata dict (execution_time, agent_count, etc.)
            include_base64: Include base64-encoded PDF for embedding

        Returns:
            Dict with success status, filepath, filename, size, and optional base64
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{document_id}_{timestamp}.pdf"
            filepath = self.output_dir / filename

            # Create PDF document
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=self.page_size,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72,
            )

            # Build content
            story = []
            styles = self._get_pdf_styles()

            # Title page
            story.append(Paragraph(title, styles['DocumentTitle']))
            story.append(Spacer(1, 0.3*inch))

            # Metadata section
            if metadata:
                story.append(Paragraph("Document Information", styles['Heading1']))
                story.append(Spacer(1, 0.1*inch))

                meta_text = f"Document ID: {document_id}<br/>"
                meta_text += f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>"

                # Add any custom metadata
                for key, value in metadata.items():
                    formatted_key = key.replace('_', ' ').title()
                    meta_text += f"{formatted_key}: {value}<br/>"

                story.append(Paragraph(meta_text, styles['Normal']))
                story.append(PageBreak())

            # Content sections
            for i, section in enumerate(content_sections):
                section_title = section.get('title', f'Section {i+1}')
                section_content = section.get('content', '')
                section.get('type', 'content')

                # Section header
                story.append(Paragraph(section_title, styles['Heading1']))
                story.append(Spacer(1, 0.1*inch))

                # Section content
                self._add_formatted_content(story, section_content, styles)

                # Page break between major sections
                if i < len(content_sections) - 1:
                    story.append(PageBreak())

            # Build PDF
            doc.build(story)

            # Prepare result
            result = {
                "success": True,
                "filepath": str(filepath),
                "filename": filename,
                "size_bytes": filepath.stat().st_size
            }

            # Add base64 if requested
            if include_base64:
                with open(filepath, 'rb') as f:
                    pdf_data = f.read()
                    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
                    result["base64_data"] = pdf_base64
                    result["embed_url"] = f"data:application/pdf;base64,{pdf_base64}"

            return result

        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            return {"success": False, "error": str(e)}

    def _get_pdf_styles(self):
        """Get custom PDF styles"""
        styles = getSampleStyleSheet()

        # Document title
        if 'DocumentTitle' not in styles:
            styles.add(ParagraphStyle(
                name='DocumentTitle',
                parent=styles['Normal'],
                fontSize=24,
                textColor=self.title_color,
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName=f'{self.default_font}-Bold'
            ))

        # Headings
        if 'Heading1' not in styles:
            styles.add(ParagraphStyle(
                name='Heading1',
                parent=styles['Normal'],
                fontSize=18,
                textColor=self.title_color,
                spaceAfter=12,
                spaceBefore=12,
                fontName=f'{self.default_font}-Bold'
            ))

        if 'Heading2' not in styles:
            styles.add(ParagraphStyle(
                name='Heading2',
                parent=styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor('#666666'),
                spaceAfter=10,
                spaceBefore=10,
                fontName=f'{self.default_font}-Bold'
            ))

        # Body text
        if 'BodyText' not in styles:
            styles.add(ParagraphStyle(
                name='BodyText',
                parent=styles['Normal'],
                fontSize=11,
                leading=14,
                alignment=TA_JUSTIFY
            ))

        # Code block
        if 'CodeBlock' not in styles:
            styles.add(ParagraphStyle(
                name='CodeBlock',
                parent=styles['Normal'],
                fontSize=10,
                fontName='Courier',
                leftIndent=20,
                textColor=colors.HexColor('#333333'),
                backColor=colors.HexColor('#f5f5f5')
            ))

        return styles

    def _add_formatted_content(self, story: List, content: str, styles):
        """
        Add formatted content to PDF story

        Supports markdown-style formatting:
        - # Heading 1
        - ## Heading 2
        - ### Heading 3
        - - List item
        - ``` code block
        """
        lines = content.split('\n')
        in_code_block = False
        code_lines = []

        for line in lines:
            line_stripped = line.strip()

            # Handle code blocks
            if line_stripped.startswith('```'):
                if in_code_block:
                    # End code block
                    if code_lines:
                        code_text = '\n'.join(code_lines)
                        story.append(Paragraph(code_text, styles['CodeBlock']))
                        story.append(Spacer(1, 0.1*inch))
                    code_lines = []
                    in_code_block = False
                else:
                    # Start code block
                    in_code_block = True
                continue

            if in_code_block:
                code_lines.append(line)
                continue

            # Empty lines
            if not line_stripped:
                story.append(Spacer(1, 0.1*inch))
                continue

            # Markdown headings
            if line_stripped.startswith('# '):
                story.append(Paragraph(line_stripped[2:], styles['Heading1']))
            elif line_stripped.startswith('## '):
                story.append(Paragraph(line_stripped[3:], styles['Heading2']))
            elif line_stripped.startswith('### '):
                story.append(Paragraph(line_stripped[4:], styles['Heading2']))
            # Lists
            elif line_stripped.startswith('- ') or line_stripped.startswith('* '):
                story.append(Paragraph('• ' + line_stripped[2:], styles['BodyText']))
            elif line_stripped.startswith('1. ') or line_stripped.startswith('2. '):
                # Numbered list
                story.append(Paragraph(line_stripped, styles['BodyText']))
            # Regular paragraphs
            else:
                story.append(Paragraph(line_stripped, styles['BodyText']))
                story.append(Spacer(1, 0.05*inch))


def generate_pdf_report(
    content_sections: List[Dict[str, Any]],
    title: str,
    document_id: str,
    output_dir: str = "reports/pdf",
    metadata: Optional[Dict[str, Any]] = None,
    include_base64: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to generate a PDF report

    Args:
        content_sections: List of content sections
        title: Document title
        document_id: Unique document identifier
        output_dir: Output directory
        metadata: Optional metadata
        include_base64: Include base64-encoded PDF

    Returns:
        Dict with success status and file information
    """
    try:
        generator = PDFGenerator(output_dir=output_dir)
        return generator.generate_report_pdf(
            content_sections=content_sections,
            title=title,
            document_id=document_id,
            metadata=metadata,
            include_base64=include_base64
        )
    except Exception as e:
        logger.error(f"PDF report generation failed: {e}")
        return {"success": False, "error": str(e)}
