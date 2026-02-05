"""
Document Generation Manager

Unified manager for generating documents in multiple formats (PDF, DOCX, Markdown).
Provides a single interface for all document generation needs.

Author: Luke Steuber
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Import generators
from .pdf_generator import PDFGenerator, PDF_AVAILABLE
from .docx_generator import DOCXGenerator, DOCX_AVAILABLE
from .markdown_generator import MarkdownGenerator


class DocumentGenerationManager:
    """
    Unified manager for document generation in multiple formats

    Automatically handles PDF, DOCX, and Markdown generation with a single call.
    Gracefully handles missing dependencies and provides format availability checking.
    """

    def __init__(self, output_dir: str = "reports"):
        """
        Initialize document generation manager

        Args:
            output_dir: Base output directory for all formats
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize generators
        self.pdf_generator = None
        self.docx_generator = None
        self.markdown_generator = None

        # Try to initialize PDF generator
        if PDF_AVAILABLE:
            try:
                self.pdf_generator = PDFGenerator(str(self.output_dir / "pdf"))
            except Exception as e:
                logger.warning(f"PDF generator initialization failed: {e}")

        # Try to initialize DOCX generator
        if DOCX_AVAILABLE:
            try:
                self.docx_generator = DOCXGenerator(str(self.output_dir / "docx"))
            except Exception as e:
                logger.warning(f"DOCX generator initialization failed: {e}")

        # Always initialize markdown generator (no dependencies)
        try:
            self.markdown_generator = MarkdownGenerator(str(self.output_dir / "markdown"))
        except Exception as e:
            logger.warning(f"Markdown generator initialization failed: {e}")

    def generate_reports(
        self,
        content_sections: List[Dict[str, Any]],
        title: str,
        document_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        formats: List[str] = ["pdf", "docx", "markdown"],
        include_base64_pdf: bool = False,
        include_markdown_frontmatter: bool = True,
        include_toc: bool = False
    ) -> Dict[str, Any]:
        """
        Generate reports in multiple formats

        Args:
            content_sections: List of content sections, each with:
                - title: Section title
                - content: Section content (markdown-formatted)
                - type: Optional section type
            title: Document title
            document_id: Unique document identifier
            metadata: Optional metadata dict
            formats: List of formats to generate ('pdf', 'docx', 'markdown')
            include_base64_pdf: Include base64-encoded PDF for embedding
            include_markdown_frontmatter: Include YAML frontmatter in markdown
            include_toc: Include table of contents in markdown

        Returns:
            Dict with success status, generated files, and any errors:
            {
                "success": bool,
                "generated_files": [
                    {
                        "format": "pdf",
                        "filepath": "/path/to/file.pdf",
                        "filename": "file.pdf",
                        "size_bytes": 12345,
                        "base64_data": "..." (if requested),
                        "embed_url": "data:application/pdf;base64,..." (if requested)
                    },
                    ...
                ],
                "errors": ["error message", ...]
            }
        """
        results = {
            "success": True,
            "generated_files": [],
            "errors": []
        }

        # Generate PDF
        if "pdf" in formats:
            if self.pdf_generator:
                try:
                    pdf_result = self.pdf_generator.generate_report_pdf(
                        content_sections=content_sections,
                        title=title,
                        document_id=document_id,
                        metadata=metadata,
                        include_base64=include_base64_pdf
                    )

                    if pdf_result.get("success"):
                        file_info = {
                            "format": "pdf",
                            "filepath": pdf_result["filepath"],
                            "filename": pdf_result["filename"],
                            "size_bytes": pdf_result["size_bytes"]
                        }

                        # Add base64 data if included
                        if include_base64_pdf:
                            file_info["base64_data"] = pdf_result.get("base64_data")
                            file_info["embed_url"] = pdf_result.get("embed_url")

                        results["generated_files"].append(file_info)
                    else:
                        results["errors"].append(f"PDF generation failed: {pdf_result.get('error')}")

                except Exception as e:
                    results["errors"].append(f"PDF generation error: {str(e)}")
            else:
                results["errors"].append("PDF generation unavailable (ReportLab not installed)")

        # Generate DOCX
        if "docx" in formats:
            if self.docx_generator:
                try:
                    docx_result = self.docx_generator.generate_report_docx(
                        content_sections=content_sections,
                        title=title,
                        document_id=document_id,
                        metadata=metadata
                    )

                    if docx_result.get("success"):
                        results["generated_files"].append({
                            "format": "docx",
                            "filepath": docx_result["filepath"],
                            "filename": docx_result["filename"],
                            "size_bytes": docx_result["size_bytes"]
                        })
                    else:
                        results["errors"].append(f"DOCX generation failed: {docx_result.get('error')}")

                except Exception as e:
                    results["errors"].append(f"DOCX generation error: {str(e)}")
            else:
                results["errors"].append("DOCX generation unavailable (python-docx not installed)")

        # Generate Markdown
        if "markdown" in formats:
            if self.markdown_generator:
                try:
                    md_result = self.markdown_generator.generate_report_markdown(
                        content_sections=content_sections,
                        title=title,
                        document_id=document_id,
                        metadata=metadata,
                        include_frontmatter=include_markdown_frontmatter,
                        include_toc=include_toc
                    )

                    if md_result.get("success"):
                        results["generated_files"].append({
                            "format": "markdown",
                            "filepath": md_result["filepath"],
                            "filename": md_result["filename"],
                            "size_bytes": md_result["size_bytes"],
                            "content": md_result.get("content")
                        })
                    else:
                        results["errors"].append(f"Markdown generation failed: {md_result.get('error')}")

                except Exception as e:
                    results["errors"].append(f"Markdown generation error: {str(e)}")
            else:
                results["errors"].append("Markdown generation unavailable")

        # Check if any files were generated
        if not results["generated_files"] and results["errors"]:
            results["success"] = False

        return results

    def get_available_formats(self) -> List[str]:
        """
        Get list of available document formats

        Returns:
            List of format names ('pdf', 'docx', 'markdown')
        """
        formats = []

        if self.pdf_generator:
            formats.append("pdf")
        if self.docx_generator:
            formats.append("docx")
        if self.markdown_generator:
            formats.append("markdown")

        return formats

    def is_format_available(self, format_name: str) -> bool:
        """
        Check if a specific format is available

        Args:
            format_name: Format to check ('pdf', 'docx', 'markdown')

        Returns:
            True if format is available, False otherwise
        """
        return format_name in self.get_available_formats()

    def get_missing_dependencies(self) -> List[str]:
        """
        Get list of missing dependencies

        Returns:
            List of missing packages that would enable additional formats
        """
        missing = []

        if not self.pdf_generator and not PDF_AVAILABLE:
            missing.append("reportlab (for PDF generation)")

        if not self.docx_generator and not DOCX_AVAILABLE:
            missing.append("python-docx (for DOCX generation)")

        return missing


# Convenience function for simple usage
def generate_multi_format_reports(
    content_sections: List[Dict[str, Any]],
    title: str,
    document_id: str,
    output_dir: str = "reports",
    metadata: Optional[Dict[str, Any]] = None,
    formats: List[str] = ["pdf", "docx", "markdown"]
) -> Dict[str, Any]:
    """
    Convenience function to generate reports in multiple formats

    Args:
        content_sections: List of content sections
        title: Document title
        document_id: Unique document identifier
        output_dir: Output directory
        metadata: Optional metadata
        formats: List of formats to generate

    Returns:
        Dict with success status and generated files
    """
    try:
        manager = DocumentGenerationManager(output_dir=output_dir)
        return manager.generate_reports(
            content_sections=content_sections,
            title=title,
            document_id=document_id,
            metadata=metadata,
            formats=formats
        )
    except Exception as e:
        logger.error(f"Multi-format report generation failed: {e}")
        return {
            "success": False,
            "generated_files": [],
            "errors": [str(e)]
        }
