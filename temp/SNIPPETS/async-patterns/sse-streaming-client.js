"""
Server-Sent Events (SSE) Streaming Pattern for Real-Time Updates

Description: Client-side implementation for consuming Server-Sent Events streams,
commonly used for AI text generation, progress updates, and real-time data feeds.
Handles POST requests with ReadableStream parsing for SSE data.

Use Cases:
- AI chatbots with streaming responses
- Real-time progress indicators
- Live data feeds and dashboards
- Multi-agent orchestration with status updates

Dependencies:
- Modern browser with fetch and ReadableStream support
- Backend server sending SSE-formatted responses

Notes:
- Handles POST requests (unlike EventSource which is GET-only)
- Parses event types and data from SSE format
- Buffers incomplete messages
- Supports custom event handlers
- Graceful error handling and reconnection logic

Related Snippets:
- See sse-server-flask.py for Flask backend implementation
- See multi-provider-llm-client.js for AI integration
"""

class SSEStreamClient {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.eventHandlers = new Map();
        this.isStreaming = false;
        this.abortController = null;
    }

    /**
     * Register an event handler
     * @param {string} eventType - Type of SSE event to handle
     * @param {function} handler - Callback function(data)
     */
    on(eventType, handler) {
        if (!this.eventHandlers.has(eventType)) {
            this.eventHandlers.set(eventType, []);
        }
        this.eventHandlers.get(eventType).push(handler);
    }

    /**
     * Remove event handler
     * @param {string} eventType - Event type
     * @param {function} handler - Handler to remove
     */
    off(eventType, handler) {
        if (!this.eventHandlers.has(eventType)) return;

        const handlers = this.eventHandlers.get(eventType);
        const index = handlers.indexOf(handler);
        if (index > -1) {
            handlers.splice(index, 1);
        }
    }

    /**
     * Trigger event handlers
     * @param {string} eventType - Event type
     * @param {any} data - Event data
     */
    emit(eventType, data) {
        if (!this.eventHandlers.has(eventType)) return;

        for (const handler of this.eventHandlers.get(eventType)) {
            try {
                handler(data);
            } catch (error) {
                console.error(`Error in ${eventType} handler:`, error);
            }
        }
    }

    /**
     * Start streaming with POST request
     * @param {object} requestData - Data to send in POST body
     * @returns {Promise<void>}
     */
    async stream(requestData) {
        if (this.isStreaming) {
            console.warn('Stream already in progress');
            return;
        }

        this.isStreaming = true;
        this.abortController = new AbortController();

        try {
            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'text/event-stream'
                },
                body: JSON.stringify(requestData),
                signal: this.abortController.signal
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            await this.processStream(response.body);

        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('Stream aborted by user');
            } else {
                console.error('Stream error:', error);
                this.emit('error', { error: error.message });
            }
        } finally {
            this.isStreaming = false;
            this.abortController = null;
            this.emit('complete', {});
        }
    }

    /**
     * Process the ReadableStream
     * @param {ReadableStream} stream - Response body stream
     */
    async processStream(stream) {
        const reader = stream.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let currentEvent = null;

        try {
            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    console.log('Stream complete');
                    break;
                }

                // Decode chunk and add to buffer
                buffer += decoder.decode(value, { stream: true });

                // Process complete lines
                const lines = buffer.split('\n');
                buffer = lines.pop() || ''; // Keep incomplete line in buffer

                for (const line of lines) {
                    if (line.startsWith('event: ')) {
                        // Extract event type
                        currentEvent = line.substring(7).trim();

                    } else if (line.startsWith('data: ')) {
                        // Extract and parse data
                        const dataStr = line.substring(6);

                        try {
                            const data = JSON.parse(dataStr);

                            if (currentEvent) {
                                this.emit(currentEvent, data);
                                currentEvent = null; // Reset after emitting
                            } else {
                                // No event type specified, use 'message'
                                this.emit('message', data);
                            }

                        } catch (e) {
                            // Not JSON, emit as plain text
                            if (currentEvent) {
                                this.emit(currentEvent, dataStr);
                                currentEvent = null;
                            } else {
                                this.emit('message', dataStr);
                            }
                        }

                    } else if (line.startsWith('id: ')) {
                        // Event ID (for reconnection)
                        const eventId = line.substring(4).trim();
                        this.emit('id', { id: eventId });

                    } else if (line.startsWith('retry: ')) {
                        // Retry interval
                        const retry = parseInt(line.substring(7));
                        this.emit('retry', { retryMs: retry });

                    } else if (line.trim() === '') {
                        // Empty line marks end of event
                        // (already handled by event/data processing)
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }
    }

    /**
     * Stop the stream
     */
    stop() {
        if (this.abortController) {
            this.abortController.abort();
        }
    }

    /**
     * Check if currently streaming
     * @returns {boolean}
     */
    get streaming() {
        return this.isStreaming;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SSEStreamClient;
} else {
    window.SSEStreamClient = SSEStreamClient;
}

/*
Example Usage:

// Initialize client
const sseClient = new SSEStreamClient('/api/stream');

// Register event handlers
sseClient.on('status', (data) => {
    console.log('Status:', data.message);
    updateStatusText(data.message);
});

sseClient.on('agent_content', (data) => {
    console.log('Agent output:', data.content);
    appendToDisplay(data.content);
});

sseClient.on('synthesis', (data) => {
    console.log('Synthesis:', data.text);
    showFinalResult(data.text);
});

sseClient.on('error', (data) => {
    console.error('Error:', data.error);
    showError(data.error);
});

sseClient.on('complete', () => {
    console.log('Stream finished');
    hideLoadingIndicator();
});

// Start streaming
const requestData = {
    query: 'What is the capital of France?',
    num_agents: 3,
    mode: 'comprehensive'
};

sseClient.stream(requestData);

// Stop streaming if needed
// sseClient.stop();


// Multi-agent search example
const searchClient = new SSEStreamClient('/search');

searchClient.on('status', (data) => {
    document.getElementById('status').textContent = data;
});

searchClient.on('subtasks', (data) => {
    const subtasksDiv = document.getElementById('subtasks');
    subtasksDiv.innerHTML += marked.parse(data); // Using marked.js for markdown
});

searchClient.on('agent_start', (data) => {
    const agentCard = createAgentCard(data.agent_id, data.task);
    document.getElementById('agents').appendChild(agentCard);
});

searchClient.on('agent_content', (data) => {
    const contentDiv = document.getElementById(`content-${data.agent_id}`);
    if (contentDiv) {
        contentDiv.innerHTML += marked.parse(data.content);
    }
});

searchClient.on('synthesis', (data) => {
    const synthesisDiv = document.getElementById('synthesis');
    synthesisDiv.innerHTML += marked.parse(data);
});

searchClient.on('complete', (data) => {
    console.log('Search completed:', data.search_id);
    document.getElementById('export-btn').disabled = false;
});

searchClient.on('error', (error) => {
    alert(`Error: ${error.error}`);
});

// Start search
searchClient.stream({
    query: 'Latest developments in quantum computing',
    num_agents: 5
});
*/
