"""
ThreadPoolExecutor Concurrent Execution Pattern

Description: Production-ready pattern for executing multiple tasks concurrently using
ThreadPoolExecutor with proper error handling, callback systems, and result aggregation.
Implements the map-reduce pattern for multi-query research workflows.

Use Cases:
- Multi-query research orchestration (generate N queries, execute in parallel, synthesize)
- Concurrent API calls to multiple providers or endpoints
- Batch processing with I/O-bound operations
- Parallel web scraping or data collection
- Multi-search workflows (search aggregation, comparison)
- Concurrent file processing operations

Dependencies:
- concurrent.futures (standard library)
- typing (standard library)
- dataclasses (standard library)

Notes:
- Best for I/O-bound operations (API calls, file I/O, network requests)
- Use ProcessPoolExecutor for CPU-bound operations instead
- Proper exception handling with as_completed() pattern
- Callback system for progress tracking and real-time updates
- Results maintain original order despite concurrent execution
- Configurable worker count for rate limiting

Related Snippets:
- async-patterns/parallel_task_execution.py - Async version with asyncio
- utilities/rate_limiter.py - Add rate limiting to concurrent operations
- api-clients/multi_provider_abstraction.py - Multi-provider API calls

Source Attribution:
- Extracted from: /home/coolhand/shared/utils/multi_search.py
- Pattern: Multi-search orchestrator with map-reduce workflow
- Author: Luke Steuber
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class TaskItem:
    """
    Represents a single task in concurrent execution workflow.

    Attributes:
        text: The task content/query text
        index: Position in task list (1-based)
        total: Total number of tasks in batch
        metadata: Additional task metadata
    """
    text: str
    index: int
    total: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    """
    Result from a single task execution.

    Attributes:
        task: The original task
        content: Result content from execution
        success: Whether task succeeded
        error: Error message if failed
        raw_response: Full response object
        metadata: Additional result metadata
    """
    task: TaskItem
    content: str
    success: bool
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchExecutionResult:
    """
    Final result from batch execution.

    Attributes:
        task_items: List of original tasks
        task_results: Individual task results
        success: Whether full workflow succeeded
        error: Error message if failed
        metadata: Workflow metadata (timings, counts, etc.)
    """
    task_items: List[str]
    task_results: List[TaskResult]
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Concurrent Task Executor
# ============================================================================

class ConcurrentTaskExecutor:
    """
    Execute multiple tasks concurrently using ThreadPoolExecutor.

    This class implements best practices for concurrent execution:
    1. Configurable worker count for rate limiting
    2. Callback system for progress tracking
    3. Proper error handling per task
    4. Result ordering preservation
    5. Timeout support per task

    Example:
        >>> executor = ConcurrentTaskExecutor(max_workers=5)
        >>> results = executor.execute_tasks(
        ...     tasks=["task1", "task2", "task3"],
        ...     worker_func=my_processing_function,
        ...     on_complete=lambda r: print(f"Done: {r.task.text}")
        ... )
        >>> print(f"Completed {len(results)} tasks")
    """

    def __init__(self, max_workers: int = 5, timeout: int = 60):
        """
        Initialize concurrent task executor.

        Args:
            max_workers: Maximum number of concurrent workers
            timeout: Timeout in seconds per task
        """
        self.max_workers = max_workers
        self.timeout = timeout

        logger.info(f"Initialized ConcurrentTaskExecutor with {max_workers} workers")

    def execute_tasks(
        self,
        tasks: List[str],
        worker_func: Callable[[str, int, int], TaskResult],
        on_complete: Optional[Callable[[TaskResult], None]] = None
    ) -> List[TaskResult]:
        """
        Execute all tasks concurrently using ThreadPoolExecutor.

        Args:
            tasks: List of task strings to execute
            worker_func: Function to execute for each task
                         Signature: func(task: str, index: int, total: int) -> TaskResult
            on_complete: Callback after each task completes

        Returns:
            List of TaskResult objects (in original order)

        Example:
            >>> def process_query(query, index, total):
            ...     # Your processing logic here
            ...     return TaskResult(...)
            >>>
            >>> results = executor.execute_tasks(
            ...     tasks=["query1", "query2"],
            ...     worker_func=process_query,
            ...     on_complete=lambda r: print(f"✓ {r.task.index}/{r.task.total}")
            ... )
        """
        logger.info(f"Executing {len(tasks)} tasks with {self.max_workers} workers")

        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(worker_func, task, i + 1, len(tasks)): task
                for i, task in enumerate(tasks)
            }

            # Collect results as they complete
            for future in as_completed(future_to_task):
                try:
                    result = future.result(timeout=self.timeout)
                    results.append(result)

                    if on_complete:
                        on_complete(result)

                except Exception as e:
                    # Create error result for failed task
                    task_text = future_to_task[future]
                    task_index = tasks.index(task_text) + 1
                    task_item = TaskItem(text=task_text, index=task_index, total=len(tasks))

                    error_result = TaskResult(
                        task=task_item,
                        content="",
                        success=False,
                        error=str(e)
                    )
                    results.append(error_result)

                    if on_complete:
                        on_complete(error_result)

                    logger.error(f"Task failed: {task_text[:50]}... - {e}")

        # Sort by original index to maintain order
        results.sort(key=lambda r: r.task.index)

        logger.info(
            f"Completed {len(results)} tasks "
            f"({sum(1 for r in results if r.success)} successful)"
        )
        return results


# ============================================================================
# Example Worker Functions
# ============================================================================

def example_api_call_worker(task: str, index: int, total: int) -> TaskResult:
    """
    Example worker function for making API calls.

    Args:
        task: Task content (e.g., search query, URL)
        index: Task index (1-based)
        total: Total number of tasks

    Returns:
        TaskResult with API response
    """
    task_item = TaskItem(text=task, index=index, total=total)

    try:
        # Simulate API call
        import time
        time.sleep(0.5)  # Replace with actual API call
        response = {"result": f"Processed: {task}"}

        return TaskResult(
            task=task_item,
            content=response.get("result", ""),
            success=True,
            raw_response=response
        )

    except Exception as e:
        return TaskResult(
            task=task_item,
            content="",
            success=False,
            error=str(e)
        )


def example_web_scraping_worker(url: str, index: int, total: int) -> TaskResult:
    """
    Example worker function for web scraping.

    Args:
        url: URL to scrape
        index: Task index (1-based)
        total: Total number of URLs

    Returns:
        TaskResult with scraped content
    """
    import requests

    task_item = TaskItem(text=url, index=index, total=total)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        content = response.text[:1000]  # First 1000 chars

        return TaskResult(
            task=task_item,
            content=content,
            success=True,
            raw_response={"status_code": response.status_code},
            metadata={"url": url, "length": len(response.text)}
        )

    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        return TaskResult(
            task=task_item,
            content="",
            success=False,
            error=str(e)
        )


# ============================================================================
# Higher-Level Patterns
# ============================================================================

def parallel_map(
    items: List[Any],
    func: Callable,
    max_workers: int = 5,
    timeout: int = 60,
    verbose: bool = False
) -> List[Any]:
    """
    Simple parallel map pattern using ThreadPoolExecutor.

    Args:
        items: List of items to process
        func: Function to apply to each item
        max_workers: Max concurrent workers
        timeout: Timeout per item
        verbose: Print progress messages

    Returns:
        List of results (in original order)

    Example:
        >>> def square(x):
        ...     return x * x
        >>> results = parallel_map([1, 2, 3, 4, 5], square, max_workers=3)
        >>> print(results)  # [1, 4, 9, 16, 25]
    """
    results = [None] * len(items)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks with their indices
        future_to_index = {
            executor.submit(func, item): idx
            for idx, item in enumerate(items)
        }

        # Collect results maintaining order
        completed = 0
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result(timeout=timeout)
                completed += 1
                if verbose:
                    print(f"✓ Completed {completed}/{len(items)}")
            except Exception as e:
                logger.error(f"Task {idx} failed: {e}")
                results[idx] = None

    return results


def parallel_filter(
    items: List[Any],
    predicate: Callable[[Any], bool],
    max_workers: int = 5
) -> List[Any]:
    """
    Parallel filter using ThreadPoolExecutor.

    Args:
        items: List of items to filter
        predicate: Function returning True to keep item
        max_workers: Max concurrent workers

    Returns:
        Filtered list

    Example:
        >>> def is_valid_url(url):
        ...     import requests
        ...     try:
        ...         r = requests.head(url, timeout=2)
        ...         return r.status_code == 200
        ...     except:
        ...         return False
        >>> urls = ["https://example.com", "https://invalid.url"]
        >>> valid_urls = parallel_filter(urls, is_valid_url)
    """
    results = parallel_map(items, predicate, max_workers=max_workers)
    return [item for item, keep in zip(items, results) if keep]


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    """
    Usage examples for concurrent task execution.
    """

    # Example 1: Basic concurrent execution with callbacks
    print("=== Example 1: Basic Concurrent Execution ===")

    executor = ConcurrentTaskExecutor(max_workers=3)

    def progress_callback(result: TaskResult):
        status = "✓" if result.success else "✗"
        print(f"{status} Task {result.task.index}/{result.task.total}: {result.task.text}")

    tasks = ["Task A", "Task B", "Task C", "Task D", "Task E"]
    results = executor.execute_tasks(
        tasks=tasks,
        worker_func=example_api_call_worker,
        on_complete=progress_callback
    )

    print(f"\nCompleted {len(results)} tasks")
    print(f"Success rate: {sum(1 for r in results if r.success)}/{len(results)}")

    # Example 2: Parallel map pattern
    print("\n=== Example 2: Parallel Map ===")

    def expensive_computation(x):
        import time
        time.sleep(0.1)
        return x ** 2

    numbers = list(range(10))
    squares = parallel_map(numbers, expensive_computation, max_workers=4, verbose=True)
    print(f"Squares: {squares}")

    # Example 3: Multi-search pattern (map-reduce)
    print("\n=== Example 3: Multi-Search Pattern ===")

    def search_worker(query: str, index: int, total: int) -> TaskResult:
        """Simulate search API call"""
        import time
        time.sleep(0.2)

        task_item = TaskItem(text=query, index=index, total=total)
        content = f"Results for '{query}': [result1, result2, result3]"

        return TaskResult(task=task_item, content=content, success=True)

    queries = [
        "machine learning basics",
        "neural networks explained",
        "deep learning applications"
    ]

    executor = ConcurrentTaskExecutor(max_workers=3)
    search_results = executor.execute_tasks(
        tasks=queries,
        worker_func=search_worker,
        on_complete=lambda r: print(f"  → {r.task.text}: {r.success}")
    )

    # Synthesis step (reduce)
    all_content = "\n\n".join([r.content for r in search_results if r.success])
    print(f"\nSynthesized {len(search_results)} search results")
    print(f"Total content length: {len(all_content)} characters")
