"""
Belter Agent - File Processing Specialist

Specialized AI agent for file processing, document analysis, and data extraction
using Mistral-7b. Handles various file formats including PDF, DOCX, CSV, JSON, and XML.

Key Capabilities:
- Document analysis and content extraction
- Multi-format file processing (PDF, DOCX, CSV, JSON, XML)
- Structured data extraction with schema validation
- Format conversion and transformation
- Content parsing and semantic analysis
- OCR integration for image-based documents
"""

import json
import logging
import mimetypes
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import SwarmModuleBase, TaskRequest, TaskResult


class BelterAgent(SwarmModuleBase):
    """
    File processing specialist using Mistral-7b for document analysis and manipulation.
    
    This agent specializes in:
    - Document analysis and content extraction
    - Multi-format file processing
    - Data structure extraction
    - Format conversion
    - Content parsing and analysis
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.capabilities = [
            "file_analysis", "document_processing", "data_extraction",
            "format_conversion", "file_manipulation", "content_parsing",
            "ocr_processing", "structured_data_extraction"
        ]
        
        self.mistral_client = None
        self.file_processors = {}
        self.supported_formats = [
            '.pdf', '.docx', '.doc', '.txt', '.csv', '.json', '.xml', '.html',
            '.md', '.rtf', '.odt', '.xlsx', '.xls'
        ]
        
        self.logger = logging.getLogger("belter.agent")
        
    async def setup_module(self):
        """Initialize Mistral client and file processing tools."""
        try:
            # Initialize Mistral client
            self.mistral_client = MockMistralClient(
                api_key=self.config.get('mistral', {}).get('api_key', ''),
                model="mistral-7b-latest"
            )
            
            # Initialize file processors
            self.file_processors = {
                'pdf': PDFProcessor(),
                'docx': DocxProcessor(),
                'doc': DocProcessor(),
                'csv': CSVProcessor(),
                'json': JSONProcessor(),
                'xml': XMLProcessor(),
                'txt': TextProcessor(),
                'html': HTMLProcessor(),
                'md': MarkdownProcessor()
            }
            
            self.logger.info(f"Belter agent initialized with {len(self.file_processors)} processors")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Belter agent: {e}")
            raise
    
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """Execute file processing task."""
        
        task_type = task.payload.get('type', task.type)
        
        try:
            if task_type == 'analyze_document':
                return await self.analyze_document(
                    task.payload['file_path'],
                    task.payload.get('analysis_type', 'general')
                )
            
            elif task_type == 'extract_data':
                return await self.extract_structured_data(
                    task.payload['file_path'],
                    task.payload.get('schema')
                )
            
            elif task_type == 'convert_format':
                return await self.convert_file_format(
                    task.payload['source_path'],
                    task.payload['target_format']
                )
            
            elif task_type == 'process_batch':
                return await self.process_file_batch(
                    task.payload['file_paths'],
                    task.payload.get('operation', 'analyze')
                )
            
            elif task_type == 'extract_text':
                return await self.extract_text_content(
                    task.payload['file_path']
                )
            
            else:
                raise ValueError(f"Unsupported task type: {task_type}")
                
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            return TaskResult(
                task_id=task.id,
                status="failed",
                error=str(e)
            )
    
    async def analyze_document(self, file_path: str, analysis_type: str) -> TaskResult:
        """Analyze document content using Mistral-7b."""
        
        try:
            # Load and preprocess file
            content = await self.load_file_content(file_path)
            file_info = await self.get_file_info(file_path)
            
            # Generate analysis prompt based on type
            if analysis_type == 'comprehensive':
                prompt = self._create_comprehensive_analysis_prompt(content, file_info)
            elif analysis_type == 'summary':
                prompt = self._create_summary_prompt(content)
            elif analysis_type == 'entities':
                prompt = self._create_entity_extraction_prompt(content)
            elif analysis_type == 'sentiment':
                prompt = self._create_sentiment_analysis_prompt(content)
            else:
                prompt = self._create_general_analysis_prompt(content)
            
            # Get analysis from Mistral
            response = await self.mistral_client.complete(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.2
            )
            
            # Parse response
            try:
                analysis_result = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to structured text response
                analysis_result = {
                    "analysis": response.content,
                    "type": analysis_type,
                    "structured": False
                }
            
            return TaskResult(
                task_id=f"analyze_{Path(file_path).stem}",
                status="completed",
                results=[{
                    "file_path": file_path,
                    "analysis_type": analysis_type,
                    "analysis_result": analysis_result,
                    "file_info": file_info,
                    "agent_id": self.module_id
                }],
                metadata={
                    "file_size": file_info.get("size", 0),
                    "file_type": file_info.get("type", "unknown"),
                    "analysis_type": analysis_type
                }
            )
            
        except Exception as e:
            self.logger.error(f"Document analysis failed for {file_path}: {e}")
            raise
    
    async def extract_structured_data(self, file_path: str, schema: Optional[Dict] = None) -> TaskResult:
        """Extract structured data from a file based on provided schema."""
        
        try:
            content = await self.load_file_content(file_path)
            file_extension = Path(file_path).suffix.lower()
            
            # Use appropriate processor based on file type
            if file_extension == '.csv':
                extracted_data = await self.file_processors['csv'].extract_data(content, schema)
            elif file_extension == '.json':
                extracted_data = await self.file_processors['json'].extract_data(content, schema)
            elif file_extension == '.xml':
                extracted_data = await self.file_processors['xml'].extract_data(content, schema)
            else:
                # Use AI for unstructured data extraction
                extracted_data = await self._ai_extract_structured_data(content, schema)
            
            return TaskResult(
                task_id=f"extract_{Path(file_path).stem}",
                status="completed",
                results=[{
                    "file_path": file_path,
                    "extracted_data": extracted_data,
                    "schema_used": schema,
                    "extraction_method": "processor" if file_extension in ['.csv', '.json', '.xml'] else "ai"
                }]
            )
            
        except Exception as e:
            self.logger.error(f"Data extraction failed for {file_path}: {e}")
            raise
    
    async def convert_file_format(self, source_path: str, target_format: str) -> TaskResult:
        """Convert file from one format to another."""
        
        try:
            source_content = await self.load_file_content(source_path)
            source_extension = Path(source_path).suffix.lower()
            target_extension = target_format.lower()
            
            if not target_extension.startswith('.'):
                target_extension = f'.{target_extension}'
            
            # Generate target file path
            source_path_obj = Path(source_path)
            target_path = source_path_obj.parent / f"{source_path_obj.stem}{target_extension}"
            
            # Perform conversion
            converted_content = await self._convert_content(
                source_content,
                source_extension,
                target_extension
            )
            
            # Save converted file
            await self._save_file(target_path, converted_content, target_extension)
            
            return TaskResult(
                task_id=f"convert_{source_path_obj.stem}",
                status="completed",
                results=[{
                    "source_path": source_path,
                    "target_path": str(target_path),
                    "source_format": source_extension,
                    "target_format": target_extension,
                    "file_size": len(converted_content) if isinstance(converted_content, str) else 0
                }]
            )
            
        except Exception as e:
            self.logger.error(f"Format conversion failed: {e}")
            raise
    
    async def process_file_batch(self, file_paths: List[str], operation: str) -> TaskResult:
        """Process multiple files in batch mode."""
        
        batch_results = []
        failed_files = []
        
        for file_path in file_paths:
            try:
                if operation == 'analyze':
                    result = await self.analyze_document(file_path, 'general')
                elif operation == 'extract_text':
                    result = await self.extract_text_content(file_path)
                else:
                    raise ValueError(f"Unsupported batch operation: {operation}")
                
                batch_results.append({
                    "file_path": file_path,
                    "status": "success",
                    "result": result.results[0] if result.results else {}
                })
                
            except Exception as e:
                failed_files.append({
                    "file_path": file_path,
                    "error": str(e)
                })
                self.logger.warning(f"Failed to process {file_path}: {e}")
        
        return TaskResult(
            task_id=f"batch_{operation}",
            status="completed",
            results=[{
                "operation": operation,
                "total_files": len(file_paths),
                "successful": len(batch_results),
                "failed": len(failed_files),
                "batch_results": batch_results,
                "failed_files": failed_files
            }]
        )
    
    async def extract_text_content(self, file_path: str) -> TaskResult:
        """Extract plain text content from any supported file format."""
        
        try:
            content = await self.load_file_content(file_path)
            file_info = await self.get_file_info(file_path)
            
            # Clean and process text
            cleaned_text = await self._clean_text_content(content)
            
            # Basic text statistics
            word_count = len(cleaned_text.split())
            char_count = len(cleaned_text)
            line_count = len(cleaned_text.split('\n'))
            
            return TaskResult(
                task_id=f"extract_text_{Path(file_path).stem}",
                status="completed",
                results=[{
                    "file_path": file_path,
                    "text_content": cleaned_text,
                    "statistics": {
                        "word_count": word_count,
                        "character_count": char_count,
                        "line_count": line_count
                    },
                    "file_info": file_info
                }]
            )
            
        except Exception as e:
            self.logger.error(f"Text extraction failed for {file_path}: {e}")
            raise
    
    async def load_file_content(self, file_path: str) -> str:
        """Load and parse file content based on file type."""
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Use appropriate processor
        processor_key = file_extension.lstrip('.')
        if processor_key in self.file_processors:
            return await self.file_processors[processor_key].read_file(file_path)
        else:
            # Fallback to text processor
            return await self.file_processors['txt'].read_file(file_path)
    
    async def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get comprehensive file information."""
        
        path_obj = Path(file_path)
        stat = path_obj.stat()
        
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return {
            "name": path_obj.name,
            "size": stat.st_size,
            "type": path_obj.suffix.lower(),
            "mime_type": mime_type,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "extension": path_obj.suffix.lower()
        }
    
    def _create_comprehensive_analysis_prompt(self, content: str, file_info: Dict) -> str:
        """Create prompt for comprehensive document analysis."""
        return f"""
        Perform a comprehensive analysis of this document:
        
        File Info: {json.dumps(file_info, indent=2)}
        Content Preview: {content[:2000]}...
        
        Provide analysis in JSON format including:
        - summary: Brief overview of the document
        - key_points: List of main points or topics
        - entities: Named entities found (people, places, organizations)
        - sentiment: Overall sentiment (positive/negative/neutral)
        - document_type: Classification of document type
        - language: Detected language
        - topics: Main topics or themes
        - structure_analysis: Document structure and organization
        - recommendations: Suggested actions or follow-ups
        
        Ensure the response is valid JSON.
        """
    
    def _create_summary_prompt(self, content: str) -> str:
        """Create prompt for document summarization."""
        return f"""
        Create a concise summary of this document:
        
        Content: {content[:3000]}...
        
        Provide a JSON response with:
        - summary: 2-3 sentence summary
        - key_points: List of 3-5 main points
        - length: "short", "medium", or "long" based on original content
        """
    
    def _create_entity_extraction_prompt(self, content: str) -> str:
        """Create prompt for named entity extraction."""
        return f"""
        Extract named entities from this text:
        
        Content: {content[:2500]}...
        
        Return JSON with entities categorized as:
        - people: Person names
        - organizations: Company/organization names
        - locations: Places, cities, countries
        - dates: Dates and time references
        - money: Monetary amounts
        - misc: Other notable entities
        """
    
    def _create_sentiment_analysis_prompt(self, content: str) -> str:
        """Create prompt for sentiment analysis."""
        return f"""
        Analyze the sentiment of this text:
        
        Content: {content[:2000]}...
        
        Return JSON with:
        - overall_sentiment: "positive", "negative", or "neutral"
        - confidence: 0.0 to 1.0
        - emotional_tone: Description of emotional tone
        - key_phrases: Phrases that indicate sentiment
        """
    
    def _create_general_analysis_prompt(self, content: str) -> str:
        """Create prompt for general document analysis."""
        return f"""
        Analyze this document and provide insights:
        
        Content: {content[:2000]}...
        
        Provide JSON response with:
        - summary: Brief summary
        - type: Document type/category
        - key_information: Important information extracted
        - language: Detected language
        - quality: Assessment of content quality
        """
    
    async def _ai_extract_structured_data(self, content: str, schema: Optional[Dict]) -> Dict:
        """Use AI to extract structured data based on schema."""
        
        schema_prompt = ""
        if schema:
            schema_prompt = f"\nExtract data according to this schema:\n{json.dumps(schema, indent=2)}"
        
        prompt = f"""
        Extract structured data from this content:{schema_prompt}
        
        Content: {content[:2000]}...
        
        Return the data in JSON format matching the schema if provided,
        or as a logical structure if no schema given.
        """
        
        response = await self.mistral_client.complete(prompt=prompt, temperature=0.1)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"extracted_text": response.content, "structured": False}
    
    async def _convert_content(self, content: str, source_ext: str, target_ext: str) -> str:
        """Convert content between different formats."""
        
        # Simple format conversion logic
        if source_ext == '.txt' and target_ext == '.json':
            return json.dumps({"content": content}, indent=2)
        elif source_ext == '.txt' and target_ext == '.xml':
            return f"<document>\n<content>{content}</content>\n</document>"
        elif target_ext == '.txt':
            # Extract text from structured formats
            return content
        else:
            # For now, return content as-is for unsupported conversions
            return content
    
    async def _save_file(self, file_path: Path, content: str, format_ext: str):
        """Save converted content to file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    async def _clean_text_content(self, content: str) -> str:
        """Clean and normalize text content."""
        # Basic text cleaning
        cleaned = content.strip()
        cleaned = ' '.join(cleaned.split())  # Normalize whitespace
        return cleaned


# File Processor Classes

class FileProcessor:
    """Base class for file processors."""
    
    async def read_file(self, file_path: str) -> str:
        """Read file content."""
        raise NotImplementedError
    
    async def extract_data(self, content: str, schema: Optional[Dict] = None) -> Dict:
        """Extract structured data from content."""
        raise NotImplementedError


class TextProcessor(FileProcessor):
    """Processor for plain text files."""
    
    async def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


class PDFProcessor(FileProcessor):
    """Processor for PDF files."""
    
    async def read_file(self, file_path: str) -> str:
        # Mock implementation - would use PyPDF2 or similar
        return f"[PDF Content from {file_path}]"


class DocxProcessor(FileProcessor):
    """Processor for DOCX files."""
    
    async def read_file(self, file_path: str) -> str:
        # Mock implementation - would use python-docx
        return f"[DOCX Content from {file_path}]"


class DocProcessor(FileProcessor):
    """Processor for DOC files."""
    
    async def read_file(self, file_path: str) -> str:
        # Mock implementation - would use python-docx2txt or similar
        return f"[DOC Content from {file_path}]"


class CSVProcessor(FileProcessor):
    """Processor for CSV files."""
    
    async def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def extract_data(self, content: str, schema: Optional[Dict] = None) -> Dict:
        # Mock CSV parsing
        lines = content.strip().split('\n')
        if len(lines) > 1:
            headers = lines[0].split(',')
            rows = [line.split(',') for line in lines[1:]]
            return {
                "headers": headers,
                "rows": rows,
                "total_rows": len(rows)
            }
        return {"error": "Invalid CSV format"}


class JSONProcessor(FileProcessor):
    """Processor for JSON files."""
    
    async def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def extract_data(self, content: str, schema: Optional[Dict] = None) -> Dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON: {e}"}


class XMLProcessor(FileProcessor):
    """Processor for XML files."""
    
    async def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def extract_data(self, content: str, schema: Optional[Dict] = None) -> Dict:
        # Mock XML parsing - would use lxml or xml.etree
        return {"xml_content": content[:500], "parsed": False}


class HTMLProcessor(FileProcessor):
    """Processor for HTML files."""
    
    async def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


class MarkdownProcessor(FileProcessor):
    """Processor for Markdown files."""
    
    async def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


class MockMistralClient:
    """Mock Mistral client for development."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    async def complete(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7):
        """Mock completion method."""
        
        class MockResponse:
            def __init__(self, content):
                self.content = content
        
        # Generate appropriate mock response based on prompt
        if "JSON format" in prompt and "summary" in prompt:
            response = json.dumps({
                "summary": "This is a mock document analysis summary.",
                "key_points": ["Point 1", "Point 2", "Point 3"],
                "document_type": "text_document",
                "language": "english",
                "sentiment": "neutral"
            })
        else:
            response = "Mock analysis response from Belter agent."
        
        return MockResponse(response)
