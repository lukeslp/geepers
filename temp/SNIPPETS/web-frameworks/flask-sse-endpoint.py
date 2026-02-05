"""
Flask Server-Sent Events (SSE) Endpoint Pattern

Description: Flask implementation for streaming Server-Sent Events responses,
perfect for AI text generation, real-time progress updates, and multi-agent systems.
Compatible with the sse-streaming-client.js pattern.

Use Cases:
- AI chatbot streaming responses
- Real-time progress indicators for long tasks
- Multi-agent orchestration with status updates
- Live data feeds and dashboards

Dependencies:
- flask (pip install flask)
- flask-cors (pip install flask-cors)

Notes:
- Returns text/event-stream content type
- Yields formatted SSE messages (event:, data:, id:)
- Supports custom event types for frontend handling
- Compatible with POST requests
- CORS enabled for cross-origin requests

Related Snippets:
- See sse-streaming-client.js for client-side implementation
- See multi-provider-llm-client.js for AI integration
"""

from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import json
import time
from typing import Generator, Dict, Any

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def format_sse(event: str = None, data: Any = None, event_id: str = None) -> str:
    """
    Format data as Server-Sent Event.

    Args:
        event: Event type (optional, defaults to 'message')
        data: Event data (will be JSON-encoded if dict/list)
        event_id: Event ID for client tracking

    Returns:
        Formatted SSE string
    """
    message = ''

    if event:
        message += f'event: {event}\n'

    if data is not None:
        if isinstance(data, (dict, list)):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        message += f'data: {data_str}\n'

    if event_id:
        message += f'id: {event_id}\n'

    message += '\n'  # Empty line marks end of event
    return message


def stream_generator(query: str, config: Dict[str, Any]) -> Generator[str, None, None]:
    """
    Example generator for streaming responses.

    Args:
        query: User query
        config: Configuration dict

    Yields:
        Formatted SSE messages
    """
    # Send initial status
    yield format_sse(
        event='status',
        data='Processing request...'
    )

    time.sleep(0.5)

    # Simulate multi-step process
    steps = [
        ('status', 'Analyzing query...'),
        ('status', 'Generating response...'),
        ('status', 'Finalizing...'),
    ]

    for event_type, message in steps:
        yield format_sse(event=event_type, data=message)
        time.sleep(0.5)

    # Send result
    result = {
        'query': query,
        'response': f'Processed: {query}',
        'timestamp': time.time()
    }

    yield format_sse(
        event='result',
        data=result
    )

    # Send completion signal
    yield format_sse(
        event='complete',
        data={'status': 'success'}
    )


@app.route('/stream', methods=['POST'])
def stream_endpoint():
    """
    SSE streaming endpoint.

    Accepts POST request with JSON body.
    Returns Server-Sent Events stream.
    """
    try:
        # Parse request
        data = request.get_json()
        query = data.get('query', '')
        config = data.get('config', {})

        # Return SSE response
        return Response(
            stream_generator(query, config),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'  # Disable nginx buffering
            }
        )

    except Exception as e:
        # Send error event
        def error_generator():
            yield format_sse(
                event='error',
                data={'error': str(e)}
            )

        return Response(
            error_generator(),
            mimetype='text/event-stream'
        )


# Multi-agent search example
def multi_agent_stream(query: str, num_agents: int) -> Generator[str, None, None]:
    """
    Example multi-agent orchestration with SSE streaming.

    Args:
        query: Search query
        num_agents: Number of agents to deploy

    Yields:
        SSE messages for different stages
    """
    # Initial status
    yield format_sse(event='status', data=f'Initializing {num_agents} agents...')

    # Decompose task
    yield format_sse(event='status', data='Breaking down search query...')
    time.sleep(0.5)

    subtasks = [
        f'Subtask {i+1}: Research aspect {i+1} of "{query}"'
        for i in range(num_agents)
    ]

    yield format_sse(
        event='subtasks',
        data='\n'.join(f'- {task}' for task in subtasks)
    )

    # Start agents
    for i in range(num_agents):
        agent_id = f'agent_{i+1}'

        # Agent start event
        yield format_sse(
            event=f'agent_{agent_id}_start',
            data={
                'agent_id': agent_id,
                'task': subtasks[i]
            }
        )

        time.sleep(0.3)

        # Agent content (simulated chunks)
        chunks = [
            f'Researching {query}...',
            f'Found relevant information...',
            f'Analyzing data...'
        ]

        for chunk in chunks:
            yield format_sse(
                event=f'agent_{agent_id}',
                data=chunk
            )
            time.sleep(0.2)

        # Agent complete
        yield format_sse(
            event=f'agent_{agent_id}_complete',
            data={
                'agent_id': agent_id,
                'status': 'completed'
            }
        )

    # Synthesis
    yield format_sse(event='status', data='Synthesizing results...')
    time.sleep(0.5)

    synthesis = f'''
# Synthesis for: {query}

Based on analysis from {num_agents} specialized agents, here are the key findings:

1. **Key Point 1**: Important discovery from agent research
2. **Key Point 2**: Another significant finding
3. **Conclusion**: Overall synthesis of information

This is a demonstration of multi-agent collaboration.
'''

    # Stream synthesis in chunks
    for line in synthesis.split('\n'):
        yield format_sse(event='synthesis', data=line + '\n')
        time.sleep(0.1)

    # Complete
    yield format_sse(
        event='complete',
        data={
            'search_id': f'search_{int(time.time())}',
            'num_agents': num_agents
        }
    )


@app.route('/search', methods=['POST'])
def search_endpoint():
    """
    Multi-agent search with SSE streaming.
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        num_agents = data.get('num_agents', 3)

        return Response(
            multi_agent_stream(query, num_agents),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    except Exception as e:
        def error_generator():
            yield format_sse(event='error', data={'error': str(e)})

        return Response(
            error_generator(),
            mimetype='text/event-stream'
        )


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


"""
Example Usage:

# Run server
python flask_sse_endpoint.py

# Test with curl
curl -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "config": {"model": "gpt-4"}}'

# Test multi-agent search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "quantum computing", "num_agents": 5}'

# JavaScript client (see sse-streaming-client.js)
const client = new SSEStreamClient('/stream');
client.on('status', (data) => console.log('Status:', data));
client.on('result', (data) => console.log('Result:', data));
client.on('complete', () => console.log('Done!'));
client.stream({ query: 'test', config: {} });
"""
