"""
Async LLM Operations Pattern

Description: Patterns for handling asynchronous LLM operations including
concurrent requests, streaming, rate limiting, and error recovery.

Use Cases:
- Processing multiple LLM requests concurrently
- Batch operations with rate limiting
- Async streaming responses
- Implementing retry logic with exponential backoff
- Managing API rate limits across concurrent operations

Dependencies:
- asyncio (built-in)
- aiohttp (pip install aiohttp)
- openai (pip install openai)
- typing (built-in)

Notes:
- Use semaphores to limit concurrent requests
- Implement proper error handling and retries
- Respect API rate limits
- Use asyncio.gather() for concurrent operations
- Handle timeouts appropriately
- Close async clients properly (use context managers)

Related Snippets:
- /home/coolhand/SNIPPETS/api-clients/multi_provider_abstraction.py
- /home/coolhand/SNIPPETS/streaming-patterns/sse_streaming_responses.py
- /home/coolhand/SNIPPETS/error-handling/graceful_import_fallbacks.py

Source Attribution:
- Extracted from: /home/coolhand/enterprise_orchestration/agents/
- Related: /home/coolhand/projects/swarm/core/
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, AsyncIterator
from dataclasses import dataclass
import logging


# ============================================================================
# BASIC ASYNC PATTERN
# ============================================================================

async def async_llm_call(prompt: str,
                         api_key: str,
                         model: str = "grok-beta") -> str:
    """
    Basic async LLM API call.

    Args:
        prompt: Input prompt
        api_key: API key
        model: Model to use

    Returns:
        Generated response
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    finally:
        await client.close()


# ============================================================================
# CONCURRENT BATCH PROCESSING
# ============================================================================

async def batch_llm_calls(prompts: List[str],
                         api_key: str,
                         model: str = "grok-beta",
                         max_concurrent: int = 5) -> List[str]:
    """
    Process multiple prompts concurrently with rate limiting.

    Args:
        prompts: List of prompts to process
        api_key: API key
        model: Model to use
        max_concurrent: Maximum concurrent requests

    Returns:
        List of responses in same order as prompts
    """
    from openai import AsyncOpenAI

    # Create semaphore to limit concurrency
    semaphore = asyncio.Semaphore(max_concurrent)

    client = AsyncOpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    async def process_one(prompt: str) -> str:
        """Process single prompt with semaphore."""
        async with semaphore:
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logging.error(f"Error processing prompt: {e}")
                return f"Error: {str(e)}"

    try:
        # Process all prompts concurrently
        responses = await asyncio.gather(*[process_one(p) for p in prompts])
        return responses

    finally:
        await client.close()


# ============================================================================
# RETRY WITH EXPONENTIAL BACKOFF
# ============================================================================

@dataclass
class RetryConfig:
    """Configuration for retry logic."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


async def async_with_retry(
    coro_func,
    *args,
    retry_config: Optional[RetryConfig] = None,
    **kwargs
) -> Any:
    """
    Execute async function with exponential backoff retry.

    Args:
        coro_func: Async function to execute
        *args: Positional arguments for function
        retry_config: Retry configuration
        **kwargs: Keyword arguments for function

    Returns:
        Function result

    Raises:
        Exception: If all retries exhausted
    """
    import random

    config = retry_config or RetryConfig()
    last_exception = None

    for attempt in range(config.max_attempts):
        try:
            return await coro_func(*args, **kwargs)

        except Exception as e:
            last_exception = e
            if attempt == config.max_attempts - 1:
                raise

            # Calculate delay with exponential backoff
            delay = min(
                config.initial_delay * (config.exponential_base ** attempt),
                config.max_delay
            )

            # Add jitter to prevent thundering herd
            if config.jitter:
                delay *= (0.5 + random.random())

            logging.warning(
                f"Attempt {attempt + 1}/{config.max_attempts} failed: {e}. "
                f"Retrying in {delay:.2f}s..."
            )

            await asyncio.sleep(delay)

    raise last_exception


# ============================================================================
# STREAMING ASYNC GENERATOR
# ============================================================================

async def async_stream_llm(prompt: str,
                          api_key: str,
                          model: str = "grok-beta") -> AsyncIterator[str]:
    """
    Stream LLM response asynchronously.

    Args:
        prompt: Input prompt
        api_key: API key
        model: Model to use

    Yields:
        Response chunks as they arrive
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=0.7
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    finally:
        await client.close()


# ============================================================================
# RATE LIMITER
# ============================================================================

class AsyncRateLimiter:
    """
    Async rate limiter for API calls.

    Implements token bucket algorithm.
    """

    def __init__(self,
                 requests_per_minute: int = 60,
                 burst_size: Optional[int] = None):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute
            burst_size: Maximum burst size (defaults to requests_per_minute)
        """
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size or requests_per_minute
        self.tokens = self.burst_size
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """
        Acquire permission to make a request.

        Blocks until a token is available.
        """
        async with self.lock:
            while True:
                now = time.time()
                elapsed = now - self.last_update

                # Add tokens based on elapsed time
                self.tokens = min(
                    self.burst_size,
                    self.tokens + elapsed * (self.requests_per_minute / 60.0)
                )
                self.last_update = now

                if self.tokens >= 1:
                    self.tokens -= 1
                    return

                # Calculate wait time for next token
                wait_time = (1 - self.tokens) * (60.0 / self.requests_per_minute)
                await asyncio.sleep(wait_time)


# ============================================================================
# ADVANCED: WORKER POOL PATTERN
# ============================================================================

class AsyncWorkerPool:
    """
    Worker pool for processing async tasks with rate limiting.
    """

    def __init__(self,
                 worker_count: int = 5,
                 rate_limiter: Optional[AsyncRateLimiter] = None):
        """
        Initialize worker pool.

        Args:
            worker_count: Number of concurrent workers
            rate_limiter: Optional rate limiter
        """
        self.worker_count = worker_count
        self.rate_limiter = rate_limiter
        self.queue: asyncio.Queue = asyncio.Queue()
        self.results: Dict[int, Any] = {}
        self.workers: List[asyncio.Task] = []
        self.logger = logging.getLogger("worker_pool")

    async def worker(self, worker_id: int):
        """
        Worker coroutine.

        Args:
            worker_id: Worker identifier
        """
        while True:
            try:
                task_id, coro = await self.queue.get()

                # Acquire rate limit token if limiter is set
                if self.rate_limiter:
                    await self.rate_limiter.acquire()

                # Execute task
                try:
                    result = await coro
                    self.results[task_id] = {"success": True, "result": result}
                except Exception as e:
                    self.logger.error(f"Task {task_id} failed: {e}")
                    self.results[task_id] = {"success": False, "error": str(e)}

                finally:
                    self.queue.task_done()

            except asyncio.CancelledError:
                break

    async def start(self):
        """Start worker tasks."""
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.worker_count)
        ]

    async def stop(self):
        """Stop worker tasks."""
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)

    async def submit(self, task_id: int, coro) -> None:
        """
        Submit task to pool.

        Args:
            task_id: Unique task identifier
            coro: Coroutine to execute
        """
        await self.queue.put((task_id, coro))

    async def wait_completion(self):
        """Wait for all tasks to complete."""
        await self.queue.join()

    def get_result(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get result for a task.

        Args:
            task_id: Task identifier

        Returns:
            Task result or None if not completed
        """
        return self.results.get(task_id)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_basic():
    """Example: Basic async LLM call."""
    response = await async_llm_call(
        prompt="What is Python?",
        api_key="your-api-key"
    )
    print(f"Response: {response}")


async def example_batch():
    """Example: Batch processing with concurrency limit."""
    prompts = [
        "What is async programming?",
        "Explain Python asyncio",
        "What are coroutines?",
        "How does event loop work?",
        "What is async/await?"
    ]

    responses = await batch_llm_calls(
        prompts=prompts,
        api_key="your-api-key",
        max_concurrent=2
    )

    for prompt, response in zip(prompts, responses):
        print(f"\nQ: {prompt}")
        print(f"A: {response[:100]}...")


async def example_streaming():
    """Example: Streaming response."""
    print("Streaming response:")

    async for chunk in async_stream_llm(
        prompt="Write a short poem about coding",
        api_key="your-api-key"
    ):
        print(chunk, end="", flush=True)

    print()


async def example_retry():
    """Example: Retry with backoff."""
    async def flaky_operation():
        """Simulated flaky operation."""
        import random
        if random.random() < 0.7:  # 70% failure rate
            raise Exception("Simulated failure")
        return "Success!"

    try:
        result = await async_with_retry(
            flaky_operation,
            retry_config=RetryConfig(max_attempts=5)
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after retries: {e}")


async def example_worker_pool():
    """Example: Worker pool with rate limiting."""

    # Create rate limiter (10 requests per minute)
    rate_limiter = AsyncRateLimiter(requests_per_minute=10)

    # Create worker pool
    pool = AsyncWorkerPool(worker_count=3, rate_limiter=rate_limiter)
    await pool.start()

    # Submit tasks
    prompts = [f"Question {i}" for i in range(20)]

    for i, prompt in enumerate(prompts):
        coro = async_llm_call(prompt=prompt, api_key="your-api-key")
        await pool.submit(task_id=i, coro=coro)

    # Wait for completion
    await pool.wait_completion()

    # Get results
    for i in range(len(prompts)):
        result = pool.get_result(i)
        print(f"Task {i}: {result}")

    # Cleanup
    await pool.stop()


async def main():
    """Run all examples."""
    import os

    api_key = os.getenv("XAI_API_KEY", "")
    if not api_key:
        print("Set XAI_API_KEY environment variable to run examples")
        return

    print("Running async LLM operation examples...")
    print("=" * 80)

    print("\n1. Basic async call:")
    await example_basic()

    print("\n2. Batch processing:")
    await example_batch()

    print("\n3. Streaming:")
    await example_streaming()

    print("\n4. Retry with backoff:")
    await example_retry()

    print("\n5. Worker pool:")
    await example_worker_pool()


if __name__ == "__main__":
    asyncio.run(main())
