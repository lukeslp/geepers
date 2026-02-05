"""
Document Generation Package

Comprehensive document generation capabilities for PDF, DOCX, and Markdown formats.
Provides both individual generators and a unified manager for multi-format output.

Author: Luke Steuber

Usage:
    # Simple usage with manager
    from document_generation import generate_multi_format_reports

    content = [
        {
            "title": "Introduction",
            "content": "This is the introduction section..."
        },
        {
            "title": "Analysis",
            "content": "## Key Findings\n- Finding 1\n- Finding 2"
        }
    ]

    result = generate_multi_format_reports(
        content_sections=content,
        title="My Report",
        document_id="report_001",
        formats=["pdf", "docx", "markdown"]
    )

    # Advanced usage with individual generators
    from document_generation import PDFGenerator, DOCXGenerator, MarkdownGenerator

    pdf_gen = PDFGenerator(output_dir="output/pdf")
    result = pdf_gen.generate_report_pdf(
        content_sections=content,
        title="My Report",
        document_id="report_001"
    )
"""

# Import availability flags
from .pdf_generator import PDF_AVAILABLE
from .docx_generator import DOCX_AVAILABLE

# Import generators
from .pdf_generator import PDFGenerator, generate_pdf_report
from .docx_generator import DOCXGenerator, generate_docx_report
from .markdown_generator import MarkdownGenerator, generate_markdown_report

# Import manager
from .manager import (
    DocumentGenerationManager,
    generate_multi_format_reports
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Luke Steuber"

# Public API
__all__ = [
    # Availability flags
    'PDF_AVAILABLE',
    'DOCX_AVAILABLE',

    # Generators
    'PDFGenerator',
    'DOCXGenerator',
    'MarkdownGenerator',

    # Manager
    'DocumentGenerationManager',

    # Convenience functions
    'generate_pdf_report',
    'generate_docx_report',
    'generate_markdown_report',
    'generate_multi_format_reports',
]


# Package-level utilities
def get_available_formats() -> list:
    """
    Get list of available document formats based on installed dependencies

    Returns:
        List of format names that can be generated
    """
    formats = ['markdown']  # Always available

    if PDF_AVAILABLE:
        formats.append('pdf')

    if DOCX_AVAILABLE:
        formats.append('docx')

    return formats


def check_dependencies() -> dict:
    """
    Check which document generation dependencies are installed

    Returns:
        Dict with availability status for each format:
        {
            'pdf': {'available': bool, 'package': 'reportlab'},
            'docx': {'available': bool, 'package': 'python-docx'},
            'markdown': {'available': bool, 'package': 'built-in'}
        }
    """
    return {
        'pdf': {
            'available': PDF_AVAILABLE,
            'package': 'reportlab',
            'install': 'pip install reportlab'
        },
        'docx': {
            'available': DOCX_AVAILABLE,
            'package': 'python-docx',
            'install': 'pip install python-docx'
        },
        'markdown': {
            'available': True,
            'package': 'built-in',
            'install': 'No installation required'
        }
    }


def print_dependency_status():
    """Print human-readable dependency status"""
    deps = check_dependencies()

    print("Document Generation Dependencies:")
    print("-" * 50)

    for format_name, info in deps.items():
        status = "✓ Available" if info['available'] else "✗ Not installed"
        print(f"{format_name.upper():10} {status:20} ({info['package']})")

        if not info['available'] and format_name != 'markdown':
            print(f"           Install: {info['install']}")

    print("-" * 50)
    print(f"Available formats: {', '.join(get_available_formats())}")
