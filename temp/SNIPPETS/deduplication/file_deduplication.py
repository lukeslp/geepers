#!/usr/bin/env python3
"""
File Deduplication Framework

Description: Comprehensive file deduplication system supporting general files, images,
             and text files with content similarity detection and optional merging.

Use Cases:
- Cleaning up duplicate files in directories
- Image deduplication by size and resolution
- Text file similarity detection and content merging
- Pre-processing for backup or archive operations
- Storage optimization tools

Dependencies:
- Pillow (optional, for image resolution detection)

Notes:
- SHA-256 hashing for content comparison
- Image deduplication uses size + resolution (faster than pixel comparison)
- Text similarity uses weighted combination of line, paragraph, and word overlap
- Default similarity threshold: 0.7 (adjustable)
- Gracefully degrades when PIL is unavailable

Related Snippets:
- utilities/retry_decorator.py (for robust file operations)
- file-operations/module_discovery.py (for recursive file finding)

Source Attribution:
- Extracted from: /home/coolhand/inbox/cleanupx/cleanupx_core/processors/legacy/deduper.py
- Author: Luke Steuber
"""

import hashlib
import logging
import os
import re
import difflib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Union, Any, Set

# Optional PIL import for image handling
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

logger = logging.getLogger(__name__)

# Common file extensions
IMAGE_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".heic"}
TEXT_EXTENSIONS: Set[str] = {
    '.txt', '.md', '.markdown', '.rst', '.log', '.csv', '.json', '.xml',
    '.yml', '.yaml', '.html', '.htm', '.css', '.conf', '.ini', '.cfg'
}


def get_file_hash(file_path: Path, block_size: int = 65536) -> Optional[str]:
    """
    Calculate SHA-256 hash of a file.

    Args:
        file_path: Path to file
        block_size: Read block size (default 64KB)

    Returns:
        Hex digest string or None on error
    """
    try:
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating hash for {file_path}: {e}")
        return None


def get_image_info(file_path: Path) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
    """
    Get file size and resolution for an image.

    Args:
        file_path: Path to image file

    Returns:
        Tuple of (file_size, (width, height)) or (None, None) on error
    """
    try:
        file_size = file_path.stat().st_size
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return None, None

    if not PIL_AVAILABLE:
        return file_size, None

    try:
        with Image.open(file_path) as img:
            resolution = img.size
    except Exception as e:
        logger.error(f"Error opening image {file_path}: {e}")
        resolution = None

    return file_size, resolution


def detect_duplicates(
    directory: Path,
    file_types: Optional[Set[str]] = None,
    recursive: bool = False
) -> Dict[str, List[Path]]:
    """
    Detect duplicate files in a directory.

    Uses size-based grouping first (fast), then content hash verification.
    Images are compared by size + resolution if PIL is available.

    Args:
        directory: Directory to scan
        file_types: Optional set of extensions to filter (e.g., {'.txt', '.md'})
        recursive: Whether to scan subdirectories

    Returns:
        Dictionary mapping unique keys to lists of duplicate file paths
    """
    directory = Path(directory)
    if not directory.is_dir():
        logger.error(f"{directory} is not a valid directory.")
        return {}

    # Collect files
    files: List[Path] = []
    if recursive:
        for path in directory.rglob('*'):
            if path.is_file() and (file_types is None or path.suffix.lower() in file_types):
                files.append(path)
    else:
        for path in directory.iterdir():
            if path.is_file() and (file_types is None or path.suffix.lower() in file_types):
                files.append(path)

    if not files:
        logger.info(f"No matching files found in {directory}")
        return {}

    # Group by size first (fast filter)
    size_groups: Dict[int, List[Path]] = {}
    for file_path in files:
        try:
            size = file_path.stat().st_size
            size_groups.setdefault(size, []).append(file_path)
        except Exception as e:
            logger.error(f"Error getting size for {file_path}: {e}")

    duplicate_groups: Dict[str, List[Path]] = {}

    for size, file_group in size_groups.items():
        if len(file_group) < 2:
            continue

        # Separate image and non-image files
        image_files = [f for f in file_group if f.suffix.lower() in IMAGE_EXTENSIONS]
        other_files = [f for f in file_group if f.suffix.lower() not in IMAGE_EXTENSIONS]

        # Process images using resolution (if PIL available)
        if image_files and PIL_AVAILABLE:
            image_dict: Dict[str, List[Path]] = {}
            for img_path in image_files:
                _, resolution = get_image_info(img_path)
                if resolution:
                    key = f"{size}_{resolution[0]}x{resolution[1]}"
                    image_dict.setdefault(key, []).append(img_path)

            for key, paths in image_dict.items():
                if len(paths) > 1:
                    duplicate_groups[key] = paths

        # Process non-image files using hash
        if other_files:
            hash_dict: Dict[str, List[Path]] = {}
            for file_path in other_files:
                file_hash = get_file_hash(file_path)
                if file_hash:
                    key = f"{size}_{file_hash}"
                    hash_dict.setdefault(key, []).append(file_path)

            for key, paths in hash_dict.items():
                if len(paths) > 1:
                    duplicate_groups[key] = paths

    return duplicate_groups


class DedupeProcessor:
    """
    General file deduplication processor.

    Supports any file type using size + hash comparison.
    """

    def __init__(self, max_size_mb: float = 1000.0):
        self.max_size_mb = max_size_mb

    def process(self, file_path: Union[str, Path], cache: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single file for deduplication.

        Args:
            file_path: Path to file
            cache: Dictionary to store/retrieve cached hashes

        Returns:
            Dictionary with file metadata and hash
        """
        file_path = Path(file_path)
        result: Dict[str, Any] = {
            'original_path': str(file_path),
            'hash': None,
            'size': None,
            'resolution': None,
            'error': None
        }

        try:
            file_size = file_path.stat().st_size
            result['size'] = file_size

            # Check cache first
            cache_key = str(file_path)
            if cache.get(cache_key) and 'hash' in cache[cache_key]:
                result['hash'] = cache[cache_key]['hash']

            # Calculate hash if not cached
            if not result['hash']:
                result['hash'] = get_file_hash(file_path)
                if result['hash']:
                    cache[cache_key] = {'hash': result['hash']}

            # Get image resolution if applicable
            if PIL_AVAILABLE and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                try:
                    with Image.open(file_path) as img:
                        result['resolution'] = img.size
                except Exception as e:
                    logger.error(f"Error getting image resolution for {file_path}: {e}")

            return result

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            result['error'] = str(e)
            return result

    def process_directory(self, directory: Union[str, Path], recursive: bool = False) -> Dict[str, Any]:
        """
        Process directory and find all duplicates.

        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories

        Returns:
            Dictionary with duplicate groups and statistics
        """
        directory = Path(directory)
        result: Dict[str, Any] = {
            'directory': str(directory),
            'duplicate_groups': [],
            'total_duplicates': 0,
            'total_size_saved': 0,
            'error': None
        }

        try:
            duplicate_groups = detect_duplicates(directory, recursive=recursive)

            for key, files in duplicate_groups.items():
                if len(files) > 1:
                    group_info = {
                        'key': key,
                        'files': [str(f) for f in files],
                        'size': files[0].stat().st_size,
                        'count': len(files)
                    }
                    result['duplicate_groups'].append(group_info)
                    result['total_duplicates'] += (len(files) - 1)
                    result['total_size_saved'] += (len(files) - 1) * files[0].stat().st_size

            return result

        except Exception as e:
            logger.error(f"Error processing directory {directory}: {e}")
            result['error'] = str(e)
            return result

    def delete_duplicates(
        self,
        duplicate_groups: Dict[str, List[Path]],
        keep_first: bool = True
    ) -> Dict[str, Any]:
        """
        Delete duplicate files.

        Args:
            duplicate_groups: Groups of duplicate files
            keep_first: Keep the first file in each group (default True)

        Returns:
            Dictionary with deletion results
        """
        result: Dict[str, Any] = {
            'deleted_files': [],
            'errors': [],
            'total_deleted': 0,
            'total_size_saved': 0
        }

        for key, files in duplicate_groups.items():
            if len(files) <= 1:
                continue

            files_to_delete = files[1:] if keep_first else files

            for file_path in files_to_delete:
                try:
                    size = file_path.stat().st_size
                    file_path.unlink()
                    result['deleted_files'].append(str(file_path))
                    result['total_deleted'] += 1
                    result['total_size_saved'] += size
                except Exception as e:
                    result['errors'].append({'file': str(file_path), 'error': str(e)})
                    logger.error(f"Error deleting {file_path}: {e}")

        return result


class TextDedupeProcessor:
    """
    Text file deduplication with similarity detection and content merging.

    Uses weighted similarity scoring:
    - 50% line-by-line comparison
    - 30% paragraph overlap
    - 20% word intersection
    """

    def __init__(self, similarity_threshold: float = 0.7, max_size_mb: float = 10.0):
        self.supported_extensions = TEXT_EXTENSIONS
        self.max_size_mb = max_size_mb
        self.similarity_threshold = similarity_threshold
        self.exact_duplicates: Dict[str, List[Dict]] = defaultdict(list)
        self.similar_groups: List[List[Dict]] = []

    def process(self, file_path: Union[str, Path], cache: Dict[str, Any]) -> Dict[str, Any]:
        """Process a text file for deduplication."""
        file_path = Path(file_path)
        result: Dict[str, Any] = {
            'original_path': str(file_path),
            'content': None,
            'paragraphs': [],
            'hash': None,
            'error': None
        }

        try:
            if file_path.suffix.lower() not in self.supported_extensions:
                result['error'] = f"Unsupported file type: {file_path.suffix}"
                return result

            if file_path.stat().st_size > self.max_size_mb * 1024 * 1024:
                result['error'] = f"File size exceeds maximum ({self.max_size_mb}MB)"
                return result

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content:
                result['error'] = "Empty file"
                return result

            result['content'] = content
            result['paragraphs'] = self._split_into_paragraphs(content)
            result['hash'] = self._calculate_normalized_hash(content)

            if cache is not None:
                cache[str(file_path)] = {
                    'hash': result['hash'],
                    'paragraphs': len(result['paragraphs'])
                }

            return result

        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            result['error'] = str(e)
            return result

    def process_directory(self, directory: Union[str, Path], recursive: bool = False) -> Dict[str, Any]:
        """Process directory to find exact and similar duplicates."""
        directory = Path(directory)
        self.exact_duplicates = defaultdict(list)
        self.similar_groups = []

        result: Dict[str, Any] = {
            'directory': str(directory),
            'exact_duplicates': [],
            'similar_groups': [],
            'total_duplicates': 0,
            'total_similar': 0,
            'error': None
        }

        try:
            files = self._load_text_files(directory, recursive)

            # Group by hash for exact duplicates
            for file in files:
                self.exact_duplicates[file['hash']].append(file)

            for hash_value, duplicate_files in self.exact_duplicates.items():
                if len(duplicate_files) > 1:
                    group = {
                        'hash': hash_value,
                        'files': [f['original_path'] for f in duplicate_files],
                        'count': len(duplicate_files)
                    }
                    result['exact_duplicates'].append(group)
                    result['total_duplicates'] += (len(duplicate_files) - 1)

            # Find similar files
            self.similar_groups = self._find_similar_files(files)
            for group in self.similar_groups:
                if len(group) > 1:
                    group_info = {
                        'files': [f['original_path'] for f in group],
                        'count': len(group)
                    }
                    result['similar_groups'].append(group_info)
                    result['total_similar'] += (len(group) - 1)

            return result

        except Exception as e:
            logger.error(f"Error processing directory {directory}: {e}")
            result['error'] = str(e)
            return result

    def calculate_similarity(self, file1: Dict[str, Any], file2: Dict[str, Any]) -> float:
        """
        Calculate similarity score between two text files.

        Returns:
            Float between 0.0 (no similarity) and 1.0 (identical)
        """
        if file1['hash'] == file2['hash']:
            return 1.0

        # Line-by-line similarity (50%)
        lines1 = file1['content'].splitlines()
        lines2 = file2['content'].splitlines()
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        line_similarity = matcher.ratio()

        # Paragraph overlap (30%)
        paragraph_matches = 0
        for p1 in file1['paragraphs']:
            for p2 in file2['paragraphs']:
                para_matcher = difflib.SequenceMatcher(None, p1, p2)
                if para_matcher.ratio() > 0.8:
                    paragraph_matches += 1
                    break

        max_paragraphs = max(len(file1['paragraphs']), len(file2['paragraphs']))
        paragraph_similarity = paragraph_matches / max_paragraphs if max_paragraphs > 0 else 0

        # Word intersection (20%)
        words1 = set(re.findall(r'\b\w+\b', file1['content'].lower()))
        words2 = set(re.findall(r'\b\w+\b', file2['content'].lower()))
        word_similarity = len(words1 & words2) / max(len(words1), len(words2)) if words1 and words2 else 0

        return (line_similarity * 0.5) + (paragraph_similarity * 0.3) + (word_similarity * 0.2)

    def _load_text_files(self, directory: Path, recursive: bool = True) -> List[Dict[str, Any]]:
        """Load and process all text files in directory."""
        files: List[Dict[str, Any]] = []

        def process_file(file_path: Path) -> None:
            if file_path.suffix.lower() in self.supported_extensions:
                file_result = self.process(file_path, cache={})
                if file_result and not file_result.get('error'):
                    files.append(file_result)

        if recursive:
            for root, dirs, filenames in os.walk(directory):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for filename in filenames:
                    process_file(Path(root) / filename)
        else:
            for item in directory.iterdir():
                if item.is_file():
                    process_file(item)

        return files

    def _find_similar_files(self, files: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Group files by similarity above threshold."""
        similar_groups: List[List[Dict[str, Any]]] = []
        processed = set()

        for i, file1 in enumerate(files):
            if file1['original_path'] in processed:
                continue

            current_group = [file1]
            processed.add(file1['original_path'])

            for j, file2 in enumerate(files):
                if i == j or file2['original_path'] in processed:
                    continue

                similarity = self.calculate_similarity(file1, file2)
                if similarity >= self.similarity_threshold:
                    current_group.append(file2)
                    processed.add(file2['original_path'])

            if len(current_group) > 1:
                similar_groups.append(current_group)

        return similar_groups

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        raw_paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in raw_paragraphs if p.strip()]

    def _calculate_normalized_hash(self, text: str) -> str:
        """Calculate hash of normalized text (ignoring whitespace and formatting)."""
        normalized = re.sub(r'\s+', ' ', text.lower())
        normalized = re.sub(r'[#*_`\[\]\(\)\{\}]', '', normalized)
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()


# Usage example
if __name__ == "__main__":
    import sys

    print("File Deduplication Framework Demo")
    print("=" * 50)

    # Demo with current directory if no path provided
    test_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')

    if not test_dir.is_dir():
        print(f"Error: {test_dir} is not a valid directory")
        sys.exit(1)

    print(f"\nScanning: {test_dir}")
    print("-" * 30)

    # General file deduplication
    print("\n1. General File Deduplication")
    processor = DedupeProcessor()
    result = processor.process_directory(test_dir, recursive=False)

    if result['duplicate_groups']:
        print(f"Found {result['total_duplicates']} duplicate files")
        print(f"Potential space savings: {result['total_size_saved'] / 1024:.1f} KB")
        for group in result['duplicate_groups'][:3]:
            print(f"  Group ({group['count']} files, {group['size']} bytes each):")
            for f in group['files'][:2]:
                print(f"    - {Path(f).name}")
    else:
        print("No duplicate files found")

    # Text file similarity
    print("\n2. Text File Similarity Detection")
    text_processor = TextDedupeProcessor(similarity_threshold=0.7)
    text_result = text_processor.process_directory(test_dir, recursive=False)

    if text_result['exact_duplicates']:
        print(f"Exact duplicates: {text_result['total_duplicates']}")
    if text_result['similar_groups']:
        print(f"Similar file groups: {len(text_result['similar_groups'])}")
        print(f"Total similar files: {text_result['total_similar']}")
    if not text_result['exact_duplicates'] and not text_result['similar_groups']:
        print("No duplicate or similar text files found")

    print("\n" + "=" * 50)
    print("PIL available:", PIL_AVAILABLE)
