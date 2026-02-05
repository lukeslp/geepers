# Shared Utilities Extraction - 2025-11-14

## Summary

Extracted high-value, reusable code patterns from the newly created `/home/coolhand/shared/utils/` library into the centralized `~/SNIPPETS` directory. These patterns demonstrate production-ready approaches to common development challenges.

**Extraction Date:** 2025-11-14
**Source Location:** `/home/coolhand/shared/utils/`
**Total Patterns Extracted:** 4
**Categories:** API Clients, Async Patterns, File Operations, Utilities

---

## Extracted Patterns

### 1. xAI Vision API Integration

**File:** `/home/coolhand/SNIPPETS/api-clients/xai_vision_api_integration.py`

**Source:** `/home/coolhand/shared/utils/vision.py`

**Key Innovations:**
- **OpenAI-Compatible Pattern**: Works with any OpenAI-compatible vision API (xAI Grok Vision, OpenAI GPT-4 Vision, Azure)
- **Multi-Modal Support**: Handles both images and videos (extracts frames from videos)
- **Base64 Encoding Pipeline**: Complete image → base64 → API submission flow
- **Graceful Degradation**: Optional dependencies (PIL, opencv) with clear error messages
- **MIME Type Detection**: Automatic format detection from file extensions

**Solved Problems:**
- Integrating vision AI into applications without framework lock-in
- Processing video content by extracting representative frames
- Handling multiple image formats with proper encoding
- Alt-text generation for accessibility
- Filename suggestions from visual content analysis

**Notable Techniques:**
```python
# Base64 encoding with MIME type detection
base64_img, mime_type = client.encode_image_base64(image_path)
image_url = f"data:image/{mime_type};base64,{base64_img}"

# Video frame extraction at specific position
frame_path = client.extract_video_frame(video_path, frame_position=0.3)

# Provider abstraction - same code works for xAI or OpenAI
client = VisionClient(
    api_key=api_key,
    base_url="https://api.x.ai/v1",  # or https://api.openai.com/v1
    model="grok-2-vision-1212"       # or gpt-4-vision-preview
)
```

---

### 2. ThreadPool Concurrent Execution Pattern

**File:** `/home/coolhand/SNIPPETS/async-patterns/threadpool_concurrent_execution.py`

**Source:** `/home/coolhand/shared/utils/multi_search.py`

**Key Innovations:**
- **Map-Reduce Workflow**: Complete pattern for multi-query research (generate → execute → synthesize)
- **Callback System**: Progress tracking with real-time updates during execution
- **Order Preservation**: Results maintain original task order despite concurrent completion
- **Error Isolation**: Individual task failures don't crash entire batch
- **Rate Limiting**: Configurable worker count for API rate limit compliance

**Solved Problems:**
- Executing multiple API calls concurrently without exceeding rate limits
- Multi-search orchestration (generate N queries, execute in parallel, aggregate results)
- Progress tracking for long-running batch operations
- Maintaining result order for synthesis/aggregation steps

**Notable Techniques:**
```python
# ThreadPoolExecutor with as_completed for result ordering
with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_task = {
        executor.submit(worker_func, task, i + 1, len(tasks)): task
        for i, task in enumerate(tasks)
    }

    for future in as_completed(future_to_task):
        result = future.result(timeout=60)
        results.append(result)
        if on_complete:
            on_complete(result)

# Sort by original index to maintain order
results.sort(key=lambda r: r.task.index)

# Callback pattern for progress tracking
def progress_callback(result: TaskResult):
    print(f"✓ Task {result.task.index}/{result.task.total}: {result.task.text}")

executor.execute_tasks(tasks, worker_func, on_complete=progress_callback)
```

---

### 3. Comprehensive Document Parser

**File:** `/home/coolhand/SNIPPETS/file-operations/comprehensive_document_parser.py`

**Source:** `/home/coolhand/shared/utils/document_parsers.py`

**Key Innovations:**
- **50+ File Format Support**: Unified interface for documents, spreadsheets, code, notebooks, email, archives
- **Graceful Fallback Strategy**: HTML parsing works with or without BeautifulSoup
- **Encoding Detection**: Tries multiple encodings (utf-8, latin-1, cp1252) for text files
- **Memory Efficiency**: Stream processing for large files, 10K row limits for spreadsheets
- **Rich Metadata**: Extracts page counts, sheet counts, row counts, links, images

**Solved Problems:**
- Building RAG systems that need to ingest diverse document types
- Content extraction for search indexing across file formats
- Knowledge base ingestion without format-specific code
- Handling optional dependencies in production environments

**Notable Techniques:**
```python
# Optional dependency pattern with availability flags
try:
    from pdfminer.high_level import extract_text as pdf_extract_text
    PDF_AVAILABLE = True
except ImportError:
    pdf_extract_text = None
    PDF_AVAILABLE = False

# Parser routing by file extension
def parse_file(self, file_path: Path) -> ParseResult:
    ext = file_path.suffix.lower()

    if ext == '.pdf':
        if not PDF_AVAILABLE:
            raise ImportError("pip install pdfminer.six")
        content, meta = self._parse_pdf(file_path)
    elif ext in {'.xlsx', '.xls'}:
        content, meta = self._parse_excel(file_path)
    # ... more formats

# Encoding detection with fallback chain
for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        return content, {'encoding': encoding}
    except UnicodeDecodeError:
        continue
```

---

### 4. Embedding Generation and Similarity Search

**File:** `/home/coolhand/SNIPPETS/utilities/embedding_generation_similarity.py`

**Source:** `/home/coolhand/shared/utils/embeddings.py`

**Key Innovations:**
- **Multi-Provider Abstraction**: Works with Ollama (local), OpenAI, or custom endpoints
- **Vector Serialization**: Convert numpy arrays to bytes for database storage
- **Top-K Similarity Search**: Efficient semantic search with cosine similarity
- **Memory-Efficient**: Uses numpy for vectorized operations
- **Batch Processing**: Generate multiple embeddings efficiently

**Solved Problems:**
- Building RAG systems with flexible embedding provider
- Semantic search and content recommendation
- Vector database integration (serialization to bytes)
- Text similarity and duplicate detection

**Notable Techniques:**
```python
# Provider abstraction pattern
class EmbeddingGenerator:
    def __init__(self, provider="ollama", model="nomic-embed-text"):
        if provider == "ollama":
            # Use local Ollama
        elif provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "custom":
            self.client = OpenAI(api_key=api_key, base_url=base_url)

# Cosine similarity calculation
def calculate_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (np_norm(emb1) * np_norm(emb2))

# Vector serialization for database storage
blob = embedding.tobytes()  # Store in database
restored = np.frombuffer(blob, dtype=np.float32)  # Retrieve

# Top-K similarity search
def find_most_similar(query_emb, candidate_embs, texts, top_k=5):
    similarities = [
        SimilarityResult(text=text, score=calculate_similarity(query_emb, emb), index=i)
        for i, (emb, text) in enumerate(zip(candidate_embs, texts))
    ]
    similarities.sort(key=lambda x: x.score, reverse=True)
    return similarities[:top_k]
```

---

### 5. Timezone and Duration Utilities

**File:** `/home/coolhand/SNIPPETS/utilities/timezone_and_duration_utilities.py`

**Source:** `/home/coolhand/shared/utils/time_utils.py`

**Key Innovations:**
- **pytz Integration**: Production-grade timezone handling with historical data
- **DST Awareness**: Properly handles Daylight Saving Time transitions
- **Duration Parsing**: Simple format ("2d3h30m") for human-readable durations
- **Timezone Validation**: Check timezone validity before operations
- **Grouped Listings**: Organize timezones by region (America, Europe, Asia, etc.)

**Solved Problems:**
- Multi-timezone scheduling and calendars
- Time difference calculations for distributed systems
- International application time handling
- Duration-based time logic

**Notable Techniques:**
```python
# Timezone conversion with pytz
source_tz = pytz.timezone("America/New_York")
dt_with_tz = source_tz.localize(dt)
target_tz = pytz.timezone("Asia/Tokyo")
converted = dt_with_tz.astimezone(target_tz)

# Duration parsing from human-readable format
def parse_duration(duration_str: str) -> timedelta:
    # "2d3h30m" → timedelta(days=2, hours=3, minutes=30)
    days = int(duration_str.split('d')[0]) if 'd' in duration_str else 0
    hours = int(duration_str.split('h')[0].split('d')[-1]) if 'h' in duration_str else 0
    minutes = int(duration_str.split('m')[0].split('h')[-1]) if 'm' in duration_str else 0
    return timedelta(days=days, hours=hours, minutes=minutes)

# Grouped timezone listing
by_region = {}
for tz in pytz.all_timezones:
    region = tz.split('/')[0] if '/' in tz else 'Other'
    by_region.setdefault(region, []).append(tz)
```

---

## Pattern Categories

### API Integration Patterns
1. **xAI Vision API Integration** - Multi-modal AI with vision
   - Base64 encoding pipeline
   - MIME type detection
   - Video frame extraction
   - Provider abstraction (xAI, OpenAI, Azure)

### Concurrent Execution Patterns
2. **ThreadPool Concurrent Execution** - Parallel I/O operations
   - Map-reduce workflow
   - Callback-based progress tracking
   - Result order preservation
   - Error isolation per task

### File Processing Patterns
3. **Comprehensive Document Parser** - Universal file format support
   - 50+ file formats
   - Graceful dependency fallbacks
   - Encoding detection
   - Metadata extraction

### Utility Patterns
4. **Embedding Generation** - Semantic search infrastructure
   - Multi-provider embeddings
   - Cosine similarity
   - Vector serialization
   - Top-K search

5. **Timezone Utilities** - International time handling
   - pytz integration
   - DST awareness
   - Duration parsing
   - Timezone validation

---

## Integration Recommendations

### For RAG Systems
```python
# Combine document parser + embeddings for knowledge base ingestion
from snippets.file_operations import parse_file
from snippets.utilities import generate_embedding, embedding_to_bytes

# Ingest documents
for file_path in documents:
    # Parse document (supports 50+ formats)
    result = parse_file(file_path)
    if result.success:
        # Generate embedding
        embedding = generate_embedding(result.content)
        # Store in vector database
        db.insert(text=result.content, vector=embedding_to_bytes(embedding))
```

### For Multi-Search Workflows
```python
# Combine concurrent execution + API abstraction
from snippets.async_patterns import ConcurrentTaskExecutor
from snippets.api_clients import VisionClient

executor = ConcurrentTaskExecutor(max_workers=5)

def analyze_image(image_path, index, total):
    client = VisionClient(api_key=os.environ["XAI_API_KEY"])
    result = client.analyze_image(image_path)
    return TaskResult(task=TaskItem(text=image_path, index=index, total=total),
                     content=result.description, success=result.success)

results = executor.execute_tasks(
    tasks=image_files,
    worker_func=analyze_image,
    on_complete=lambda r: print(f"✓ Analyzed {r.task.text}")
)
```

### For International Applications
```python
# Combine timezone utilities with API integration
from snippets.utilities import convert_timezone, add_time

# Schedule API call for specific timezone
user_timezone = "America/Los_Angeles"
scheduled_time = add_time("now", "2h", user_timezone)

# Convert to UTC for storage
utc_time = convert_timezone(
    scheduled_time.strftime("%Y-%m-%d %H:%M:%S"),
    user_timezone,
    "UTC"
)
```

---

## Quality Metrics

### Code Quality
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Usage examples in `if __name__ == "__main__"`
- ✅ Dataclasses for structured results
- ✅ Logging for debugging
- ✅ Error handling with specific exceptions

### Production Readiness
- ✅ Graceful degradation (optional dependencies)
- ✅ Clear error messages with installation instructions
- ✅ Memory efficiency (streaming, limits)
- ✅ Rate limiting support (configurable workers)
- ✅ Timeout handling
- ✅ Resource cleanup (file handles, connections)

### Documentation
- ✅ Use cases clearly defined
- ✅ Dependencies listed
- ✅ Related snippets cross-referenced
- ✅ Source attribution provided
- ✅ Multiple usage examples
- ✅ Integration patterns demonstrated

---

## Common Patterns Identified

### 1. Optional Dependency Pattern
```python
try:
    import optional_library
    LIBRARY_AVAILABLE = True
except ImportError:
    optional_library = None
    LIBRARY_AVAILABLE = False

# Later in code:
if not LIBRARY_AVAILABLE:
    raise ImportError("Install with: pip install optional_library")
```

### 2. Dataclass Results Pattern
```python
@dataclass
class OperationResult:
    success: bool
    content: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### 3. Functional + Class Interface Pattern
```python
# Class-based for advanced usage
client = EmbeddingGenerator(provider="ollama")
result = client.generate("text")

# Functional for convenience
embedding = generate_embedding("text")
```

### 4. Provider Abstraction Pattern
```python
class AbstractClient:
    def __init__(self, provider: str, api_key: str, base_url: str):
        if provider == "provider1":
            # Initialize provider 1
        elif provider == "provider2":
            # Initialize provider 2
```

### 5. Callback Progress Pattern
```python
def execute_batch(items, worker_func, on_complete=None):
    for item in items:
        result = worker_func(item)
        if on_complete:
            on_complete(result)
```

---

## Future Consolidation Opportunities

### Additional Shared Utils to Extract
- `/home/coolhand/shared/utils/universal_proxy.py` - Multi-provider API routing
- `/home/coolhand/shared/providers/` - Provider adapter pattern
- `/home/coolhand/shared/memory/` - Caching and state management

### Integration Targets
- RAG pipeline patterns (document parser + embeddings + vector DB)
- Multi-agent research workflows (concurrent execution + provider abstraction)
- International scheduling systems (timezone utils + duration parsing)

---

## Lessons Learned

### What Makes a Good Snippet
1. **Immediately Usable** - Copy, adjust config, run
2. **Well-Documented** - Use cases, examples, dependencies
3. **Production-Ready** - Error handling, logging, resource cleanup
4. **Generalized** - No project-specific hardcoded values
5. **Self-Contained** - Minimal external dependencies

### Pattern Quality Indicators
- ✅ Solves a real, recurring problem
- ✅ Demonstrates best practices
- ✅ Includes multiple usage examples
- ✅ Has graceful error handling
- ✅ Works across multiple projects
- ✅ Has clear abstraction boundaries

---

**Total Value:** 4 production-ready patterns extracted from shared utilities library, covering vision AI, concurrent execution, document parsing, embeddings, and timezone handling. These patterns enable rapid development of RAG systems, multi-search workflows, and international applications.
