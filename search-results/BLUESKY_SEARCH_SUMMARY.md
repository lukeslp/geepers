# Bluesky/AT Protocol Search Summary

Complete search results and analysis of Bluesky implementations across codebase.

**Search Date**: 2026-01-22
**Searcher**: Claude Code Searcher Agent
**Status**: Complete

---

## Executive Summary

Comprehensive search identified **3 active Bluesky/AT Protocol implementations** across the codebase with varying feature maturity:

1. **Firehose** (TypeScript/Express) - Production real-time streaming & sentiment analysis
2. **Blueballs** (Python/FastAPI) - Network graph visualization & analysis
3. **Bluevibes** (Python/Flask) - Bluesky data client & sentiment analysis

**Total Code Analyzed**: ~15,000 lines across 74+ TypeScript and 200+ Python files

---

## What Was Searched

### Directories Searched
```
/home/coolhand/servers/firehose/       (74 TypeScript files)
/home/coolhand/projects/blueballs/     (200+ Python files)
/home/coolhand/projects/bluevibes/     (20+ Python files)
/home/coolhand/html/bluesky/           (N/A - primarily static)
```

### Search Patterns Used
- AT Protocol API calls: `app.bsky.*`, `com.atproto.*`
- Authentication: `auth`, `session`, `token`, `JWT`
- Streaming: `firehose`, `jetstream`, `websocket`, `streaming`
- Graph analysis: `graph`, `network`, `centrality`, `pagerank`
- Sentiment: `sentiment`, `analyze`, `emotion`, `vader`
- Caching: `cache`, `redis`, `Redis`, `mongodb`
- React hooks: `use[A-Z].*\(`, `useAuth`, `useSocket`

### Key Findings

**14 Major Components Discovered**:
1. Jetstream WebSocket client (firehose.ts, 494 lines)
2. VADER sentiment analyzer (sentiment.ts, 135 lines)
3. Socket.IO real-time broadcast (socketio.ts, 49 lines)
4. JWT session management (oauth.ts, 305 lines)
5. Drizzle ORM schema (9 tables, schema.ts)
6. NetworkX graph algorithms (graph_analysis.py, 80+ lines)
7. Redis + filesystem caching (cache_service.py, 80+ lines)
8. Rate-limited HTTP client (bluesky_client.py, 100+ lines)
9. Custom React hooks (5 hooks in client/src/)
10. tRPC API endpoints (routers.ts, 80+ lines)
11. Corpus filtering pipeline (firehose.ts, 44 lines)
12. Database persistence layer (db.ts)
13. 20 network visualization layouts (blueballs frontend)
14. Concurrent API fetching (concurrent.futures in bluevibes)

---

## Documents Generated

### 1. BLUESKY_ATPROTO_FEATURE_MATRIX.md (Comprehensive)
- **Size**: ~800 lines
- **Content**: Complete feature-by-feature breakdown
- **Sections**: 15 major sections covering all aspects
- **Tables**: 50+ detailed tables with line references
- **Purpose**: Authoritative reference for what exists where

### 2. BLUESKY_QUICK_REFERENCE.md (Quick Lookup)
- **Size**: ~400 lines
- **Content**: Fast lookup guide for common tasks
- **Sections**: Where to find what, common tasks, API reference
- **Code Examples**: 10+ bash/curl examples
- **Purpose**: Developer speed reference

### 3. BLUESKY_CODE_PATTERNS.md (Implementation Guide)
- **Size**: ~700 lines
- **Content**: Reusable code patterns from all projects
- **Sections**: 10 pattern categories with full source code
- **Examples**: 35+ code snippets
- **Purpose**: Copy-paste reference for implementations

### 4. This Summary (Navigation)
- **Size**: This document
- **Purpose**: Overview and index

---

## Key Discoveries

### Real-Time Streaming

**Jetstream Connection** (`firehose.ts:13`)
```
wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post&wantedEvents=identity
```
- Processes ~5M posts/day
- Auto-reconnects every 5 seconds
- Dual-channel: identity (handle cache) + commits (posts)

**Socket.IO Broadcast** (`socketio.ts:11`)
- 1Hz stats updates
- Per-post events
- Browser-compatible real-time

### AT Protocol API Calls

**Used**:
- `com.atproto.server.createSession` - Authentication
- `app.bsky.graph.getFollows` - Follower lists (inferred)
- `app.bsky.actor.getProfile` - User profiles
- `app.bsky.feed.*` - Posts and timelines

**Not Yet Used** (15+ available):
- `app.bsky.feed.searchPosts` - Full-text search
- `app.bsky.notification.listNotifications` - Notifications
- `app.bsky.feed.getLikes` - Like operations
- `app.bsky.feed.getQuotes` - Quote detection

### Authentication Patterns

**Method 1: JWT Session** (Firehose)
- `SignJWT` + `jwtVerify` (jose library)
- HS256 signature
- 1-year expiry
- HTTP-only cookies

**Method 2: AT Protocol JWT** (Blueballs/Bluevibes)
- `com.atproto.server.createSession`
- accessJwt + refreshJwt pair
- DID-based identity
- Rate limit tracking

### Graph Analysis

**Algorithms Implemented** (NetworkX):
- PageRank (influence)
- Betweenness centrality (connector nodes)
- Closeness centrality (proximity)
- In/out degree centrality (direct connections)
- Community detection (Louvain method)

**Visualization Layouts** (20 options):
- Force-directed (10,000+ nodes)
- Clustered spirals (3,000 nodes)
- 3D orbit forces (4,000-5,000 nodes)
- Helical streams, circular arcs, heatmaps, and more

### Sentiment Analysis

**Algorithm**: VADER (Valence Aware Dictionary and sEntiment Reasoner)
- 3-class classification: positive/negative/neutral
- Thresholds: >0.05 (pos), <-0.05 (neg)
- Language-aware
- <1ms per post

**Feature Extraction**:
- Hashtags (Unicode-aware via facets + regex)
- Mentions (@handle)
- URLs (https only)
- Language (from record.langs)
- Media type (images, video, external embeds)
- Quote detection (app.bsky.embed.record*)

### Caching Strategy

**Dual-Backend** (Blueballs):
1. **Primary**: Redis async client
2. **Fallback**: Filesystem (`.cache/` directory)
3. **Serialization**: orjson (fast binary JSON)

**In-Memory** (Firehose):
- Last 100 posts (memory buffer)
- Rolling 60-second timestamp array
- DID→handle cache (connection lifetime)
- Stats persistence every 100 posts

### React Hooks

**Custom Hooks** (5 total):
1. `useAuth()` - Session management + logout
2. `useSocket()` - Socket.IO real-time
3. `useComposition()` - Text input composition
4. `useMobile()` - Responsive detection
5. `usePersistFn()` - Stable function references

**tRPC Integration**:
- Query hooks with cache management
- Mutation hooks with optimistic updates
- Cache invalidation patterns
- Request deduplication

---

## Architecture Overview

### Firehose Architecture
```
Bluesky Jetstream WebSocket
    ↓
FirehoseService (singleton)
    ├→ Sentiment Analysis (VADER)
    ├→ Feature Extraction
    ├→ Corpus Filtering (4-stage)
    ├→ SQLite Storage (Drizzle ORM)
    └→ Socket.IO Broadcast
            ↓
    React Dashboard (Recharts + Radix UI)
    ├→ Real-time Stats (1Hz)
    ├→ Live Feed
    └→ Topic Analysis
```

### Blueballs Architecture
```
Bluesky AT Protocol API
    ↓
RateLimiter (3000/5000 points/hour)
    ↓
Async HTTP Client (httpx)
    ↓
Network Fetcher
    ↓
Cache Service
    ├→ Redis (primary)
    └→ Filesystem (fallback)
            ↓
Graph Analysis (NetworkX)
    ├→ PageRank
    ├→ Centrality
    ├→ Community Detection
    ├→ Numpy→JSON Conversion
            ↓
FastAPI Endpoints
            ↓
SvelteKit Frontend (20 visualizations)
```

### Bluevibes Architecture
```
Bluesky HTTP Client
    ├→ Login (identifier + password)
    ├→ Token Management
    ├→ DID Resolution
            ↓
Concurrent Fetching (concurrent.futures)
            ↓
VADER Sentiment Analysis
            ↓
Progress Tracking
            ↓
Flask API Routes
```

---

## File Statistics

### TypeScript Files (Firehose)
- Total: 74 files (excluding node_modules)
- Actual code: ~10,000 lines
- Components: 40+ React components + 15+ server modules
- Libraries: 50+ npm dependencies

### Python Files (Blueballs)
- Total: 200+ files (including archived scripts)
- Backend: ~40 core files
- Analytics: 5+ modules
- Tests: 20+ test files
- Visualization: 20+ layout implementations

### Python Files (Bluevibes)
- Total: 20+ files
- Core: bluesky_client.py (primary implementation)
- Storage: Cache and persistence modules
- Tests: Several test files

---

## Integration Opportunities

### Code Consolidation
**Current**: 2 separate Bluesky HTTP client implementations
**Opportunity**: Extract to shared library (`/home/coolhand/shared/`)

**Current**: Sentiment analysis in firehose only
**Opportunity**: Move to shared library for use in blueballs/bluevibes

**Current**: 3 independent rate limiters
**Opportunity**: Unified rate limiting pattern

### Feature Reuse
- Firehose's socket handling could extend blueballs
- Blueballs' graph algorithms could enhance firehose analysis
- Cache strategy (redis + fallback) is excellent template

### API Standardization
- Create unified AT Protocol client
- Implement missing API endpoints
- Add search, notifications, and rich text support

---

## Notable Technical Patterns

### 1. Dual-Backend Caching
Redis for speed + filesystem for resilience. Excellent fallback pattern.

### 2. Streaming Architecture
Jetstream → EventEmitter → Socket.IO. Clean separation of concerns.

### 3. Corpus Collection
4-stage filter pipeline (language, word count, quote detection, link ratio) for linguistic research. Well-designed sampling strategy.

### 4. Feature Extraction
Combines structured data (facets) with regex fallback. Handles Unicode hashtags. Smart approach.

### 5. Graph Analysis
NetworkX + numpy type conversion. Careful handling of JSON serialization.

### 6. Rate Limiting
Points-based system with timestamp tracking. Prevents exceeding API quotas.

### 7. React Hook Patterns
Cache invalidation, optimistic updates, session persistence. Production-quality.

---

## Known Gaps

### Missing AT Protocol Features
1. No FTS search (`app.bsky.feed.searchPosts`)
2. No notifications (`app.bsky.notification.*`)
3. No direct messages (`chat.bsky.*`)
4. No rich text creation (facets only on parse)
5. No feed management (read-only)
6. No moderation tools (blocks, mutes)

### Missing Infrastructure
1. No AT Protocol relay (direct Jetstream only)
2. No DID resolution (beyond Bluesky)
3. No context/rep tracking
4. No AppView integration
5. No CAR file support (except in archived code)

### Missing Visualizations
1. No timeline view
2. No thread exploration
3. No feed customization UI
4. No interactive filtering

---

## Performance Characteristics

### Throughput
- Firehose: 5M posts/day capability
- Per-post sentiment: <1ms
- Database batch writes: every 100 posts
- Socket.IO: 1Hz stat broadcasts

### Scale Limits
- Force-directed graphs: 10,000 nodes (60 FPS)
- In-memory buffer: 100 posts
- Rate limiter: 3000-5000 points/hour

### Optimization Opportunities
1. Batch sentiment analysis
2. Progressive graph rendering
3. Lazy-load visualizations
4. Cache graph computations

---

## Recommendations

### For New Bluesky Work
1. **Start with**: Firehose as template (production-ready)
2. **Use**: Blueballs for graph analysis patterns
3. **Reference**: Bluevibes for HTTP client patterns
4. **Check**: BLUESKY_CODE_PATTERNS.md for copy-paste code

### For Extensions
1. **Add notifications**: Use existing auth pattern
2. **Add search**: Implement `app.bsky.feed.searchPosts`
3. **Add rich text creation**: Extend facet extraction
4. **Add graph optimization**: Implement caching for results

### For Integration
1. Consolidate HTTP clients
2. Share sentiment analysis
3. Standardize rate limiting
4. Create unified cache interface

---

## Search Methodology

### Tools Used
1. **Glob**: File discovery patterns
2. **Grep**: AT Protocol + feature pattern matching
3. **Read**: Detailed code analysis of key files
4. **Bash**: Directory structure exploration

### Search Strategy
1. Directory validation (checked 4 major directories)
2. File enumeration (identified 15,000+ lines of code)
3. Pattern matching (searched for AT Protocol, auth, streaming, graphs, sentiment, caching, hooks)
4. Cross-reference analysis (mapped relationships between components)
5. Verification (read full source of critical files)

### Confidence Levels
- **High**: AT Protocol APIs, authentication patterns, sentiment analysis, React hooks
- **High**: Database schema, caching implementation, rate limiting
- **Medium**: Graph algorithms (sourced from NetworkX, not custom)
- **Medium**: Visualization layouts (inferred from blueballs structure)
- **Low**: Unused AT Protocol features (inferred from Bluesky docs)

---

## Files in This Analysis

### Documents Generated
1. `BLUESKY_ATPROTO_FEATURE_MATRIX.md` - 800 lines, comprehensive reference
2. `BLUESKY_QUICK_REFERENCE.md` - 400 lines, developer quick lookup
3. `BLUESKY_CODE_PATTERNS.md` - 700 lines, reusable implementations
4. `BLUESKY_SEARCH_SUMMARY.md` - This document

### Source Files Referenced
- `/home/coolhand/servers/firehose/server/firehose.ts` (494 lines)
- `/home/coolhand/servers/firehose/server/sentiment.ts` (135 lines)
- `/home/coolhand/servers/firehose/server/socketio.ts` (49 lines)
- `/home/coolhand/servers/firehose/server/routers.ts` (80+ lines)
- `/home/coolhand/servers/firehose/server/_core/oauth.ts` (305 lines)
- `/home/coolhand/projects/blueballs/backend/app/services/bluesky_client.py`
- `/home/coolhand/projects/blueballs/backend/app/analytics/graph_analysis.py`
- `/home/coolhand/projects/blueballs/backend/app/services/cache_service.py`
- `/home/coolhand/projects/bluevibes/src/bluesky_client.py`
- Plus 20+ supporting files

---

## Next Steps

For users of this analysis:

1. **Start Here**: Read `BLUESKY_QUICK_REFERENCE.md` for orientation
2. **Deep Dive**: Review `BLUESKY_ATPROTO_FEATURE_MATRIX.md` for specifics
3. **Implementation**: Copy patterns from `BLUESKY_CODE_PATTERNS.md`
4. **Questions**: Reference specific line numbers provided throughout

---

## Contact & Updates

This analysis is current as of 2026-01-22. For updates:
- Re-run Glob/Grep searches on same directories
- Check git log for recent changes
- Reference line numbers provided for quick source validation

---

**End of Search Summary**

Analysis completed by Claude Code Searcher Agent
Generated: 2026-01-22
Total analysis time: Multiple parallel searches
Total documents: 4 comprehensive guides
