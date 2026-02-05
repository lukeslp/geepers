# Bluesky Sentiment Dashboard Snippet Extraction

**Date:** 2025-11-14  
**Source:** `/home/coolhand/servers/coca/bluesky_firehose/`  
**Extracted By:** Luke Steuber

## Overview

Extracted 6 high-value reusable patterns from the Bluesky Sentiment Dashboard, a production real-time data streaming application that processes the Bluesky firehose for sentiment analysis.

## Extracted Snippets

### 1. WebSocket Firehose Connection Pattern
**File:** `/home/coolhand/SNIPPETS/websocket-patterns/websocket_firehose_reconnection.py`

**What it does:**
- Connects to WebSocket data streams (firehoses) with automatic reconnection
- Handles timeouts, connection drops, and JSON parsing errors gracefully
- Implements exponential backoff for reconnection attempts
- Uses ping/pong health checks to detect stale connections

**Key Features:**
- Asyncio-based async/await pattern
- Configurable timeouts and reconnection delays
- Callback-based message processing
- Clean shutdown via state management

**Use Cases:**
- Bluesky/Twitter firehose consumers
- Real-time data stream processing
- Event-driven architectures
- Long-running WebSocket connections

### 2. Flask-SocketIO Real-Time Broadcasting Pattern
**File:** `/home/coolhand/SNIPPETS/real-time-dashboards/flask_socketio_broadcaster.py`

**What it does:**
- Enables bidirectional real-time communication between Flask server and browser clients
- Broadcasts data updates to all connected clients or specific rooms
- Tracks client connections and manages rooms
- Integrates with background threads for periodic updates

**Key Features:**
- Thread-safe broadcasting from any thread
- Room-based selective broadcasting
- Connection lifecycle management
- HTTP endpoints to trigger broadcasts
- async_mode configuration for dev/production

**Use Cases:**
- Live dashboards with real-time updates
- Notification systems
- Collaborative applications
- Progress tracking for long operations
- Live data visualization

### 3. VADER Sentiment Analysis Wrapper
**File:** `/home/coolhand/SNIPPETS/sentiment-analysis/vader_sentiment_analyzer.py` (already existed, verified complete)

**What it does:**
- Analyzes sentiment of text using VADER (optimized for social media)
- Classifies text as positive, negative, or neutral
- Provides batch processing and distribution analysis

**Key Features:**
- Configurable sentiment thresholds
- Batch processing capabilities
- Filtering by sentiment
- Finding most positive/negative texts
- Very fast (1-2ms per text)

**Use Cases:**
- Social media sentiment monitoring
- Customer feedback analysis
- Brand monitoring
- Content moderation
- Real-time sentiment dashboards

### 4. SQLite Simple Pattern for Flask Apps
**File:** `/home/coolhand/SNIPPETS/database-patterns/sqlite_flask_simple_pattern.py`

**What it does:**
- Provides simple, safe SQLite integration for Flask applications
- Uses connection-per-operation pattern with context managers
- Includes complete CRUD operation examples

**Key Features:**
- Context manager for automatic connection cleanup
- WAL mode for better read concurrency
- Row factory for dict-like access
- Comprehensive error handling
- Index creation examples

**Use Cases:**
- Logging and metrics collection
- Simple data persistence for dashboards
- Prototype applications
- Background task data storage
- Low-to-medium traffic applications (< 100 req/s)

### 5. Flask + Asyncio Background Thread Integration
**File:** `/home/coolhand/SNIPPETS/async-patterns/flask_asyncio_background_thread.py`

**What it does:**
- Runs asyncio event loops in background threads alongside Flask
- Enables async operations (WebSocket clients, async APIs) without blocking Flask
- Manages event loop lifecycle properly

**Key Features:**
- AsyncBackgroundRunner class for single event loop management
- MultiAsyncRunner for running multiple async tasks concurrently
- Thread-safe communication patterns
- Graceful start/stop with daemon threads
- Example WebSocket consumer integration

**Use Cases:**
- Running WebSocket clients while serving HTTP API
- Background async tasks with Flask frontend
- Integrating async libraries with Flask
- Combining Flask-SocketIO with asyncio operations

### 6. Gunicorn + Eventlet Deployment Configuration
**Files:** 
- `/home/coolhand/SNIPPETS/web-frameworks/gunicorn_socketio_deployment.py`
- `/home/coolhand/SNIPPETS/web-frameworks/gunicorn_socketio_deployment.md`

**What it does:**
- Provides production deployment configuration for Flask-SocketIO apps
- Documents how to use Gunicorn with eventlet worker class
- Includes comprehensive deployment guide

**Key Features:**
- Single worker handles 5000-10000 concurrent connections
- Systemd service template
- Nginx/Caddy reverse proxy configurations
- Multi-worker setup with Redis message queue
- Monitoring and troubleshooting guide

**Use Cases:**
- Production deployment of real-time dashboards
- WebSocket-based applications
- Scaling Flask-SocketIO apps
- High-concurrency real-time applications

## Architecture Patterns Demonstrated

### Real-Time Data Pipeline
```
WebSocket Firehose → Sentiment Analysis → SQLite Storage → SocketIO Broadcast → Dashboard
```

### Threading Model
```
Flask HTTP Thread (handles web requests)
    ↓
Background AsyncIO Thread (consumes WebSocket firehose)
    ↓
SocketIO Event Thread (broadcasts to clients)
```

### Key Technologies
- **WebSocket Client:** `websockets` library with asyncio
- **Real-Time Server:** Flask-SocketIO with eventlet
- **Sentiment Analysis:** VADER (vaderSentiment)
- **Database:** SQLite with WAL mode
- **Production Server:** Gunicorn with eventlet worker class

## Integration Example

Here's how these patterns work together in the Bluesky dashboard:

1. **WebSocket Firehose Client** (runs in background thread):
   - Connects to Bluesky firehose
   - Receives JSON messages with new posts
   - Handles reconnection automatically

2. **Sentiment Analysis** (processes each post):
   - Analyzes post text using VADER
   - Classifies as positive/negative/neutral
   - Returns compound score (-1 to 1)

3. **SQLite Storage** (persists data):
   - Saves posts with sentiment scores
   - Stores statistics snapshots
   - Uses WAL mode for concurrent reads

4. **SocketIO Broadcasting** (updates clients):
   - Broadcasts new posts to all connected browsers
   - Sends statistics updates every second
   - Manages client connections and rooms

5. **Gunicorn + Eventlet** (production deployment):
   - Runs with single worker for session affinity
   - Handles thousands of concurrent WebSocket connections
   - Integrates with Caddy reverse proxy

## Performance Characteristics

- **Throughput:** Processes ~1000+ posts/second from firehose
- **Latency:** < 100ms from firehose message to dashboard update
- **Concurrency:** Single worker handles 5000+ concurrent dashboard viewers
- **Sentiment Analysis:** ~1-2ms per post (VADER is very fast)
- **Database:** WAL mode allows concurrent reads during writes

## Deployment Recommendations

1. Use Gunicorn with eventlet worker class (not default sync workers)
2. Single worker sufficient for most use cases (avoid session affinity issues)
3. Use Caddy/Nginx reverse proxy for SSL and static file serving
4. Enable WAL mode on SQLite for better read concurrency
5. Monitor memory usage (each WebSocket connection consumes ~10-20KB)

## Related Patterns

These snippets work well with existing snippets in the library:

- `async-patterns/asyncio_task_queue.py` - For background task processing
- `streaming-patterns/sse_streaming_responses.py` - Alternative to WebSocket for one-way streaming
- `error-handling/retry_with_backoff.py` - Complementary to WebSocket reconnection
- `utilities/rate_limiter.py` - For rate limiting API calls

## Source Attribution

All patterns extracted from:
- **Project:** Bluesky Sentiment Dashboard
- **Location:** `/home/coolhand/servers/coca/bluesky_firehose/`
- **Author:** Luke Steuber
- **Date:** November 2025

## Testing Recommendations

When using these patterns:

1. **WebSocket Pattern:** Test reconnection by killing connection, test timeout handling
2. **SocketIO Pattern:** Test with multiple clients, verify broadcast to rooms works
3. **Sentiment Analysis:** Validate with known positive/negative/neutral texts
4. **SQLite Pattern:** Test concurrent reads/writes, verify WAL mode enabled
5. **Background Thread:** Verify graceful shutdown, test exception handling
6. **Gunicorn Config:** Load test with realistic concurrency, monitor memory

## Future Enhancements

Potential improvements to these patterns:

- [ ] Add Redis message queue example for multi-worker SocketIO
- [ ] Add authentication/authorization to SocketIO pattern
- [ ] Add circuit breaker to WebSocket reconnection logic
- [ ] Add connection pooling to SQLite pattern (for higher throughput)
- [ ] Add metrics/monitoring integration (Prometheus, StatsD)
- [ ] Add Docker deployment configuration

## Notes

- VADER sentiment analysis is specifically designed for social media text (emojis, slang, etc.)
- SQLite with WAL mode is surprisingly capable for read-heavy workloads
- Eventlet uses greenlets (cooperative multitasking) not OS threads
- Single Gunicorn worker avoids need for sticky sessions with SocketIO
- WebSocket reconnection with exponential backoff prevents server overload
