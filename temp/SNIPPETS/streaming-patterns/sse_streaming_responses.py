"""
Server-Sent Events (SSE) Streaming Pattern

Description: Comprehensive patterns for implementing Server-Sent Events streaming
in web applications. Supports both Flask and FastAPI implementations with proper
error handling, connection management, and graceful degradation.

Use Cases:
- Real-time AI response streaming (ChatGPT-style interfaces)
- Live data updates (stock prices, notifications, logs)
- Progress indicators for long-running operations
- Multimodal content streaming (text, images, metadata)
- Bidirectional real-time communication with fallbacks

Dependencies:
- flask or fastapi (web framework)
- requests (for client-side examples)
- typing (built-in)
- json (built-in)

Notes:
- SSE is unidirectional (server → client), use WebSockets for bidirectional
- Always set proper MIME type: text/event-stream
- Include retry field for auto-reconnection
- Flush after each event for immediate delivery
- Handle client disconnections gracefully
- Use generators to avoid blocking server threads
- CORS headers required for cross-origin requests

Related Snippets:
- /home/coolhand/SNIPPETS/api-clients/multi_provider_abstraction.py
- /home/coolhand/SNIPPETS/async-patterns/async_generators.py
- /home/coolhand/SNIPPETS/error-handling/graceful_degradation.py

Source Attribution:
- Extracted from: /home/coolhand/projects/apis/api_v2/providers/
- Related patterns: /home/coolhand/projects/xai_swarm/, /home/coolhand/html/belta/
"""

import json
import time
from typing import Any, Dict, Generator, Optional, Union
from datetime import datetime


# ============================================================================
# FLASK IMPLEMENTATION
# ============================================================================

def flask_sse_stream_example():
    """
    Flask implementation of SSE streaming.

    Complete example showing proper SSE format with Flask Response.
    """
    from flask import Flask, Response, request

    app = Flask(__name__)

    def generate_events() -> Generator[str, None, None]:
        """
        Generate Server-Sent Events.

        SSE Format:
            data: <message>\n\n

        Optional fields:
            event: <event-name>
            id: <unique-id>
            retry: <milliseconds>
        """
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connected', 'timestamp': datetime.now().isoformat()})}\n\n"

        # Send periodic updates
        for i in range(10):
            event_data = {
                "type": "update",
                "count": i,
                "message": f"Event {i}",
                "timestamp": datetime.now().isoformat()
            }

            # Format as SSE event
            yield f"data: {json.dumps(event_data)}\n\n"

            # Simulate processing time
            time.sleep(0.5)

        # Send completion event
        yield f"data: {json.dumps({'type': 'complete', 'total': 10})}\n\n"

    @app.route('/stream')
    def stream():
        """SSE endpoint."""
        return Response(
            generate_events(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',  # Disable nginx buffering
                'Access-Control-Allow-Origin': '*'  # CORS for development
            }
        )

    return app


def flask_ai_streaming_example():
    """
    Flask implementation for streaming AI responses.

    Example showing how to stream LLM responses chunk by chunk.
    """
    from flask import Flask, Response, request

    app = Flask(__name__)

    def stream_ai_response(prompt: str, model: str = "grok-beta") -> Generator[str, None, None]:
        """
        Stream AI response using SSE.

        Args:
            prompt: User prompt
            model: Model to use

        Yields:
            SSE-formatted chunks
        """
        try:
            # Initialize AI client (example with OpenAI-compatible API)
            from openai import OpenAI
            client = OpenAI(
                api_key="your-api-key",
                base_url="https://api.x.ai/v1"
            )

            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'model': model})}\n\n"

            # Create streaming completion
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.7
            )

            # Stream chunks
            full_content = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content

                    # Send content chunk
                    event_data = {
                        "type": "content",
                        "content": content,
                        "full_content": full_content
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'type': 'done', 'total_chars': len(full_content)})}\n\n"

        except Exception as e:
            # Send error event
            error_data = {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    @app.route('/ai/stream', methods=['POST'])
    def ai_stream():
        """AI streaming endpoint."""
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', 'grok-beta')

        return Response(
            stream_ai_response(prompt, model),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    return app


# ============================================================================
# FASTAPI IMPLEMENTATION
# ============================================================================

def fastapi_sse_example():
    """
    FastAPI implementation of SSE streaming.

    Uses StreamingResponse for better async support.
    """
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    async def event_generator():
        """Async generator for SSE events."""
        # Send initial event
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"

        # Stream events
        for i in range(10):
            event_data = {
                "type": "update",
                "count": i,
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(0.5)

        # Send completion
        yield f"data: {json.dumps({'type': 'complete'})}\n\n"

    @app.get("/stream")
    async def stream():
        """SSE endpoint."""
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    return app


# ============================================================================
# CLIENT-SIDE CONSUMPTION
# ============================================================================

def sse_client_example():
    """
    Python client for consuming SSE streams.

    Example using requests library with streaming.
    """
    import requests

    def consume_sse_stream(url: str):
        """
        Consume SSE stream from a URL.

        Args:
            url: SSE endpoint URL
        """
        headers = {"Accept": "text/event-stream"}

        with requests.get(url, stream=True, headers=headers) as response:
            response.raise_for_status()

            buffer = ""
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    buffer += chunk

                    # Process complete events (ending with \n\n)
                    while "\n\n" in buffer:
                        event, buffer = buffer.split("\n\n", 1)

                        # Parse SSE event
                        if event.startswith("data: "):
                            data = event[6:]  # Remove "data: " prefix
                            try:
                                event_data = json.loads(data)
                                handle_event(event_data)
                            except json.JSONDecodeError:
                                print(f"Non-JSON data: {data}")

    def handle_event(event_data: Dict[str, Any]):
        """
        Handle received SSE event.

        Args:
            event_data: Parsed event data
        """
        event_type = event_data.get("type")

        if event_type == "connected":
            print("Connected to stream")
        elif event_type == "update":
            print(f"Update: {event_data.get('message', '')}")
        elif event_type == "content":
            print(event_data.get("content", ""), end="", flush=True)
        elif event_type == "error":
            print(f"Error: {event_data.get('error')}")
        elif event_type == "complete":
            print("\nStream complete")

    # Usage
    try:
        consume_sse_stream("http://localhost:5000/stream")
    except Exception as e:
        print(f"Stream error: {e}")


# ============================================================================
# JAVASCRIPT CLIENT EXAMPLE
# ============================================================================

JAVASCRIPT_CLIENT = """
// Browser-native EventSource for SSE consumption

const eventSource = new EventSource('http://localhost:5000/stream');

// Handle different event types
eventSource.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);

    switch(data.type) {
        case 'connected':
            console.log('Connected to stream');
            break;
        case 'update':
            console.log('Update:', data.message);
            break;
        case 'content':
            // Append AI response content
            document.getElementById('response').textContent += data.content;
            break;
        case 'error':
            console.error('Stream error:', data.error);
            eventSource.close();
            break;
        case 'complete':
            console.log('Stream complete');
            eventSource.close();
            break;
    }
});

// Handle connection errors
eventSource.addEventListener('error', (error) => {
    console.error('SSE connection error:', error);
    eventSource.close();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    eventSource.close();
});
"""


# ============================================================================
# ADVANCED: CHUNKED TRANSFER WITH PROGRESS
# ============================================================================

def stream_with_progress(data_source, chunk_size=1024):
    """
    Stream large data with progress updates.

    Args:
        data_source: Generator or iterable producing data
        chunk_size: Size of chunks to yield

    Yields:
        SSE events with progress information
    """
    total_bytes = 0
    start_time = time.time()

    for chunk in data_source:
        total_bytes += len(chunk)
        elapsed = time.time() - start_time

        # Yield progress event
        progress_data = {
            "type": "progress",
            "bytes": total_bytes,
            "elapsed": elapsed,
            "rate": total_bytes / elapsed if elapsed > 0 else 0
        }
        yield f"data: {json.dumps(progress_data)}\n\n"

        # Yield data chunk
        data_event = {
            "type": "data",
            "chunk": chunk,
            "offset": total_bytes
        }
        yield f"data: {json.dumps(data_event)}\n\n"

    # Final completion event
    completion_data = {
        "type": "complete",
        "total_bytes": total_bytes,
        "duration": time.time() - start_time
    }
    yield f"data: {json.dumps(completion_data)}\n\n"


if __name__ == "__main__":
    print("SSE Streaming Pattern Examples")
    print("=" * 80)
    print("\nFlask Example:")
    print("  Run: flask_app = flask_sse_stream_example(); flask_app.run()")
    print("\nFastAPI Example:")
    print("  Run: fastapi_app = fastapi_sse_example(); uvicorn.run(fastapi_app)")
    print("\nClient Example:")
    print("  Run: sse_client_example()")
    print("\nJavaScript Client:")
    print(JAVASCRIPT_CLIENT)
