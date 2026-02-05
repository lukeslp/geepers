# Bluesky Suite Services - Comprehensive Metadata

**Generated**: 2026-01-18
**Status**: Phase 2 Documentation Preparation
**Services Covered**: 5 major services + integrated subservices

---

## Executive Summary

The Bluesky suite consists of five core services hosted on dr.eamer.dev:

1. **Post Visualizer** - D3.js thread analysis tool (React + Express)
2. **Firehose** - Real-time sentiment analytics dashboard (Node.js + TypeScript)
3. **Unified Client** - Comprehensive management interface (React 19 + Express + Socket.IO)
4. **Corpus Firehose** - Linguistics analysis of Bluesky posts (Flask + VADER)
5. **Skymarshal** - Content management CLI + web interface (Python)

Plus supporting services in `/html/bluesky/`:
- CheatChat API (Flask + Gemini)
- Network Graph (D3.js chord diagram)
- Repostdar (Self-repost detector)

---

## SERVICE 1: POST VISUALIZER

### Quick Facts
- **Location**: `/home/coolhand/html/bluesky/post-visualizer/`
- **Port**: 5084
- **Type**: React 19 + TypeScript + Vite SPA with Express backend
- **URL**: https://dr.eamer.dev/bluesky/post-visualizer/
- **Service Manager**: `sm start post-visualizer`

### Architecture
```
Frontend (React):
├── App.tsx (~2600 lines, all-in-one)
├── src/App.css (touch handling + graph styling)
├── src/main.tsx (iOS gesture handling)
└── src/index.css (Tailwind imports)

Backend (Express):
└── server.js (share API, OG image generation)

Build:
├── vite.config.ts (React + Tailwind)
├── tsconfig.json
└── package.json
```

### Key Features
1. **Thread Analysis**: Visualize post interactions as force-directed D3.js graph
2. **Node Types**: Likes, reposts, replies, quotes, focus post
3. **Social Status**: Detects mutual follows, follower relationships
4. **Sharing**: Save graphs + metadata, generate OG images
5. **Mobile Support**: Touch gestures, iOS pinch-zoom, accessibility

### Technology Stack
- **Frontend**: React 19, TypeScript 5.6, D3.js v7, Tailwind 4, Vite 7
- **Backend**: Node.js + Express
- **Data**: Bluesky AT Protocol REST API
- **Caching**: LocalStorage with 5-min fresh / 1-hour stale TTL
- **Database**: Optional (file-based shares at `data/shares.json`)

### API Endpoints
```
POST /bluesky/post-visualizer/api/share    # Save graph + image
GET  /bluesky/post-visualizer/api/share/:id # Retrieve share
GET  /bluesky/post-visualizer/health       # Health check
GET  /bluesky/post-visualizer/?share=id    # Dynamic OG tags
```

### Bluesky API Integration
- `com.atproto.identity.resolveHandle` - Handle→DID resolution
- `app.bsky.feed.getPostThread` - Nested thread fetching
- `app.bsky.feed.getLikes` - Paginated likes (cursor-based)
- `app.bsky.feed.getRepostedBy` - Paginated reposts
- `app.bsky.actor.getProfiles` - Batch profile fetch (max 25)

### Data Flow
```
1. User pastes URL or enters handle
2. Parse URL → resolve handle to DID → construct AT URI
3. Fetch thread + likes + reposts (paginated, with caching)
4. Build graph: nodes (users) + links (interactions)
5. D3 force simulation positions nodes
6. SVG rendering with labels, tooltips, info panel
7. Optional: Save + share with OG image
```

### D3 Force Configuration
- `forceLink`: Connects interaction nodes to focus post
- `forceCollide`: radius = `sqrt(followers/100) * 3` (clamped 8-40px)
- `forceManyBody`: Strength -50 to -300
- `forceRadial`: Groups nodes by interaction type
- `forceCenter`: Centers graph

### Build & Deployment
```bash
# Development
cd /home/coolhand/html/bluesky/post-visualizer
pnpm install
pnpm dev          # Vite dev server on port 5083

# Production
pnpm build        # TypeScript + Vite
pnpm start        # Express server on port 5084
./start.sh        # Via service manager
```

### Caddy Routing
```caddyfile
handle /bluesky/post-visualizer {
  redir https://{host}/bluesky/post-visualizer/?{query} permanent
}
handle /bluesky/post-visualizer/* {
  reverse_proxy localhost:5084
}
```

### Known Issues & Solutions
- **Mobile touch**: CSS `touch-action: none` prevents text selection
- **iOS zoom**: `main.tsx` prevents default pinch-zoom outside SVG
- **Cache invalidation**: Checksum = `likes-reposts-replies` detects changes

### Documentation Files
- `CLAUDE.md` - Architecture, types, data flow (40 KB)
- `README.md` - User guide
- `src/App.tsx` - Source with inline comments

---

## SERVICE 2: FIREHOSE

### Quick Facts
- **Location**: `/home/coolhand/html/firehose/`
- **Port**: 5052
- **Type**: Full-stack TypeScript (React + Express + tRPC + Socket.IO)
- **URL**: https://dr.eamer.dev/bluesky/firehose/
- **Service Manager**: `sm start firehose`

### Architecture
```
Frontend (React 19 + Vite):
├── pages/Dashboard.tsx (main analytics)
├── components/ (UI with shadcn)
├── hooks/useSocket.ts (Socket.IO)
└── lib/trpc.ts (tRPC client)

Backend (Express):
├── _core/index.ts (server entry point)
├── firehose.ts (Jetstream WebSocket listener)
├── sentiment.ts (VADER NLP)
├── db.ts (Drizzle ORM queries)
├── routers.ts (tRPC API)
└── socketio.ts (real-time broadcast)

Database (SQLite):
├── posts (full post data)
├── statsGlobal (all-time aggregates)
├── statsHourly/statsDaily (time-series)
├── statsLanguage (language distribution)
├── statsHashtag (trends)
└── authorInteractions (network analysis)
```

### Key Features
1. **Real-time Streaming**: Jetstream WebSocket to 5052+ posts/sec
2. **Sentiment Analysis**: VADER classification + scoring
3. **Analytics**: Live charts (Recharts), stats, dashboards
4. **Language Detection**: Auto-detect post language
5. **Hashtag Tracking**: Trend analysis
6. **CSV Export**: Filtered data export
7. **Persistence**: SQLite database with Drizzle ORM

### Technology Stack
- **Frontend**: React 19, Recharts, shadcn/ui, Tailwind 4, Wouter routing
- **Backend**: Express + tRPC, Socket.IO, Jetstream WebSocket client
- **Database**: SQLite with Drizzle ORM
- **NLP**: VADER sentiment, `natural` language detection
- **Build**: Vite (frontend), esbuild (server), tsx (dev)

### API Endpoints (tRPC)
```
firehose:
  - start() / stop()
  - stats() → { posts, positive, negative, neutral, ... }
  - recentPosts(limit)
  - filters() / setFilters()
  - exportCSV(filters)

posts:
  - list(filters) → paginated results

stats:
  - global() → lifetime aggregates
  - hourly(range) → hourly time-series
  - languages() → distribution
  - hashtags() → trending
  - contentTypes() → post/reply/repost breakdown
  - sentimentByKeyword(keyword) → filtered stats

auth:
  - Optional OAuth flow
```

### Socket.IO Events
```
From Server:
  - 'post': New post processed { uri, text, sentiment, ... }
  - 'stats': Updated stats every 1 second

Client Listeners:
  - Connect/disconnect handling
  - Post deduplication
  - Real-time chart updates
```

### Jetstream Integration
```
WebSocket: wss://jetstream2.us-east.bsky.network
Subscribe: app.bsky.feed.post + app.atproto.sync.identity events
Purpose: 100-2000 posts/sec, real-time sentiment analysis
```

### Database Schema Highlights
- `posts.uri` - UNIQUE constraint prevents duplicates
- `posts.sentiment` - Enum: 'positive' | 'negative' | 'neutral'
- `statsHourly.timestamp` - Integer (Unix), auto-aggregated
- `statsHashtag.hashtag` - Lowercase, normalized
- Indexes needed on: timestamp, sentiment, language

### Configuration
```
Environment (.env):
  NODE_ENV=production
  PORT=5052
  OAUTH_SERVER_URL= (optional)
  JWT_SECRET= (session signing)
  DATABASE_URL=./firehose.db

Auto-start:
  - Firehose starts 2s after server launch (_core/index.ts:74)
  - Continuous data collection, no manual intervention needed
```

### Performance Characteristics
- **Memory**: ~150MB base + 10MB per 1,000 posts
- **DB Updates**: Every 100 posts (batch writes)
- **CPU**: <5% idle, 10-20% peak
- **Network**: 1-5 Mbps sustained
- **Storage**: ~1KB/post (~1GB per million)

### Build & Deployment
```bash
cd /home/coolhand/html/firehose

# Development
pnpm dev          # Hot reload, port 3000 frontend + backend

# Production
pnpm build        # Compile all
pnpm start        # Run production server
./start.sh        # Via service manager (port 5052)

# Database
pnpm db:push      # Apply schema migrations
sqlite3 firehose.db  # Direct inspection
```

### Caddy Routing
```caddyfile
handle /bluesky/firehose/* {
  reverse_proxy localhost:5052
}
# Socket.IO path (MUST come before general route)
@websocket-bluesky-firehose {
  path /bluesky/firehose/socket.io/*
  header Connection *Upgrade*
  header Upgrade websocket
}
handle @websocket-bluesky-firehose {
  uri strip_prefix /bluesky/firehose
  reverse_proxy localhost:5052
}
```

### Common Issues & Solutions
- **Firehose not connecting**: Verify `wss://jetstream2.us-east.bsky.network` accessible
- **DB lock errors**: SQLite limited concurrency; consider WAL mode
- **Socket.IO disconnects**: Check CORS configuration in `server/socketio.ts`
- **Build failures**: `rm -rf node_modules && pnpm install && pnpm check`

### Documentation Files
- `CLAUDE.md` - Comprehensive guide (298 lines)
- `README.md` - User documentation
- `API_REFERENCE.md` - Full endpoint documentation
- `TECHNICAL_REVIEW_MOBILE.md` - Mobile optimization notes
- `UX_IMPROVEMENTS.md` - UI enhancement backlog

---

## SERVICE 3: UNIFIED CLIENT

### Quick Facts
- **Location**: `/home/coolhand/html/bluesky/unified/`
- **Type**: React 19 + TypeScript monorepo (pnpm workspaces)
- **Frontend Port**: 5086 (Vite)
- **Backend Port**: 3001 (Express)
- **URL**: https://dr.eamer.dev/bluesky/unified/
- **Service Manager**: `sm start unified-client` (frontend), `unified-server` (backend)

### Architecture
```
Monorepo Structure:
├── app/ (Main React application, Vite)
│   ├── src/pages/ (Route components with lazy loading)
│   ├── src/components/ (Shared UI, layout, auth)
│   ├── src/hooks/ (useSocket, useInfiniteScroll, etc.)
│   ├── src/router.tsx (React Router with code-splitting)
│   └── src/lib/ (Utils, tRPC client)
├── packages/
│   ├── api-client/ (Bluesky AT Protocol wrapper)
│   ├── components/ (Thread, compose, shared UI)
│   ├── utils/ (TypeScript utilities)
│   └── skymarshal/ (Content management toolkit)
├── server/ (Express backend)
│   └── src/app.ts (API proxying, Socket.IO)
└── tests/
    └── e2e/ (Playwright tests)
```

### Key Features
1. **Home Feed**: Real-time post streaming, deduplication, infinite scroll
2. **Thread Viewer**: Recursive rendering, reply preview, depth visualization
3. **Search**: Full-text content search with filters (type, date, author)
4. **Analytics**: Content statistics with Recharts (lazy-loaded)
5. **Visualize**: D3.js force graph (lazy-loaded)
6. **Compose**: Post creation with alt text editor, validation
7. **Chat**: Bluesky DM integration (planned)
8. **Data Management**: Content export, archiving
9. **Moderation**: Content moderation tools
10. **Tools Integration**: Post Visualizer, Network Graph, CheatChat, Repostdar

### Technology Stack
- **Frontend**: React 19, TypeScript 5.6, Vite 5.1, React Router 6.22
- **Styling**: Tailwind CSS 4 (CSS-first architecture)
- **Real-time**: Socket.IO 4.6 for Jetstream streaming
- **Charts**: Recharts 3.6 (lazy-loaded)
- **Testing**: Playwright (E2E), Vitest (planned)
- **Backend**: Express, custom Bluesky API wrapper

### Routes & Lazy Loading
```
/home              → Real-time feed
/thread/:uri       → Thread viewer
/search            → Content search (lazy)
/analytics         → Charts + stats (lazy)
/visualize         → D3.js graph (lazy)
/compose           → Post creation
/chat              → DMs (planned)
/data              → Export/archive (lazy)
/moderation        → Moderation tools (lazy)
/tools             → Iframe integration hub
```

### Socket.IO Integration
```typescript
// Connection setup
const socket = io('http://localhost:3001', {
  path: '/socket.io',
  transports: ['websocket', 'polling']
});

// Listening with deduplication
useEffect(() => {
  const cleanup = on('post', (post) => {
    setNewPosts(prev => {
      const existsInMain = posts.some(p => p.uri === post.uri);
      const existsInNew = prev.some(p => p.uri === post.uri);
      if (!existsInMain && !existsInNew) {
        return [post, ...prev];
      }
      return prev;
    });
  });
  return cleanup;
}, [socket, isConnected, posts]);
```

### Tailwind CSS 4 Critical Notes
```css
/* ✅ CORRECT (v4) */
@import "tailwindcss";

/* ❌ WRONG (v3 syntax - does NOT work in v4) */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Custom colors REPLACE entire palette** - ensure all needed colors defined.

### TypeScript Type Safety
- Strict mode enabled
- No `any` types (use union types instead)
- Proper null checks for optional Bluesky data
- Deduplication algorithms validated

### Accessibility (WCAG 2.1 Level AA)
- ARIA labels on all icon-only buttons
- Form validation with error messages
- Color contrast: 4.5:1 (normal), 3:1 (large text)
- Keyboard navigation support
- Focus-visible indicators

### Error Boundaries
```typescript
// Automatic wrapping in router.tsx
<PageErrorBoundary pageName="Page Name">
  <YourPage />
</PageErrorBoundary>
```

### Code Splitting Strategy
**Lazy-loaded pages** (reduce initial bundle):
- Analytics (~180KB Recharts)
- Visualize (D3.js)
- DataManagement
- Moderation
- Tools integration (iframe, zero bundle impact)

### Build & Deployment
```bash
cd /home/coolhand/html/bluesky/unified

# Development
pnpm install
pnpm dev           # Port 5086 frontend, 3001 backend

# Production
pnpm build         # Output: app/dist/, server/dist/
pnpm start

# Quality checks
pnpm check         # TypeScript
pnpm test:e2e      # Playwright tests
```

### Caddy Routing
```caddyfile
# Backend API + WebSocket
handle /bluesky/unified/api/* {
  uri strip_prefix /bluesky/unified
  reverse_proxy localhost:3001
}
handle /bluesky/unified/socket.io/* {
  uri strip_prefix /bluesky/unified
  reverse_proxy localhost:3001
}

# Frontend SPA (Vite preserves prefix)
handle /bluesky/unified/* {
  reverse_proxy localhost:5086
}
```

### E2E Testing (Playwright)
```bash
# Run all tests
pnpm test:e2e

# Specific file
pnpm test:e2e tests/e2e/home.spec.ts

# Debug mode
pnpm test:e2e --debug

# Accessibility validation
import AxeBuilder from '@axe-core/playwright';
const results = await new AxeBuilder({ page }).analyze();
```

### Performance Metrics (After Phase 0-3)
| Metric | Before | After | Target | Status |
|--------|--------|-------|--------|--------|
| Bundle Size | 487 KB | 307 KB | < 430 KB | ✅ 29% under |
| Load Time | 2.3s | 1.8s | < 2s | ✅ 10% under |
| Type Safety | 92% | 98% | 95%+ | ✅ 3% over |
| WCAG Level | A/AA hybrid | AA | AA | ✅ Met |
| A11y Score | 95/100 | 97/100 | 95+ | ✅ 2 over |

### Common Issues & Solutions
1. **CSS Not Loading**: Update `app/src/index.css` to `@import "tailwindcss";`
2. **Duplicate Keys**: Use setState callback to access current state
3. **Thread Page Crash**: Add null checks for `reply.author?.displayName`
4. **Socket.IO Disconnects**: Verify backend running, CORS configured
5. **Vite Server OOM**: `NODE_OPTIONS="--max-old-space-size=4096" pnpm dev`

### Documentation Files
- `CLAUDE.md` - Comprehensive guide (760 lines)
- `README.md` - Project overview
- `server/README.md` - Backend documentation
- `app/README.md` - Frontend documentation

### Recent Work (Phases 0-3)
- ✅ Fixed Tailwind v4 CSS loading
- ✅ Resolved port conflicts
- ✅ Added WCAG 2.1 AA accessibility
- ✅ Implemented code-splitting (37% bundle reduction)
- ✅ E2E tests with axe-core validation (37 tests, 505 LOC)
- ✅ Tool integration (Post Visualizer, Network Graph, CheatChat, Repostdar)

---

## SERVICE 4: CORPUS FIREHOSE

### Quick Facts
- **Location**: `/home/coolhand/servers/diachronica/corpus/bluesky_firehose/`
- **Port**: 5074
- **Type**: Flask + Eventlet + VADER sentiment
- **URL**: https://dr.eamer.dev/bluesky/corpus/
- **Service Manager**: `sm start bluesky-corpus`

### Architecture
```
Backend (Flask):
├── app_corpus.py (Main API server, ~40KB)
├── app.py (Alternative implementation, ~45KB)
├── db/ (SQLite persistence)
│   ├── bsky_corpus.db (91MB - main storage)
│   └── bsky_posts.db (86KB - active posts)
└── monitoring/
    ├── disk_monitor.service (systemd unit)
    └── disk_monitor.timer (scheduler)

Frontend:
└── templates/index.html (Dashboard with charts)

Database Schema:
├── posts (id, text, author, sentiment, sentiment_score, timestamp, uri)
├── sentiment_stats (timestamp, positive, negative, neutral, total)
└── user_stats (author, post_count, sentiment_dist)
```

### Key Features
1. **Real-time Capture**: Jetstream WebSocket to 100-2,000 posts/sec
2. **Sentiment Analysis**: VADER scoring (-1 to +1)
3. **Classification**: positive (>0.1), neutral (-0.1 to 0.1), negative (<-0.1)
4. **Persistence**: SQLite (supports eventlet async workers)
5. **Analytics**: Sentiment distribution, time-series stats
6. **Monitoring**: Disk usage alerts, health checks

### Technology Stack
- **Framework**: Flask + Flask-SocketIO
- **Async**: Threading for firehose, async WebSockets
- **NLP**: VADER sentiment (rule-based, social media optimized)
- **Storage**: SQLite (single file, no server setup)
- **Monitoring**: Custom disk_monitor service

### API Endpoints
```
GET  /api/health              # Health check
GET  /api/stats               # Aggregated statistics
GET  /api/posts               # Recent posts
GET  /api/stats/sentiment      # Sentiment distribution
GET  /api/stats/timeline      # Time-series stats
POST /api/filters             # Set keyword filters
```

### Sentiment Scoring (VADER)
```
VADER.polarity_scores(text) returns:
{
  'neg': 0.0-1.0,    # Negative
  'neu': 0.0-1.0,    # Neutral
  'pos': 0.0-1.0,    # Positive
  'compound': -1.0-1.0  # Overall sentiment
}

Classification:
  compound > 0.1  → positive
  compound < -0.1 → negative
  else            → neutral
```

### Jetstream Integration
```
Connection: wss://jetstream2.us-east.bsky.network
Subscribe: app.bsky.feed.post events
Auto-reconnect: 5-second backoff on disconnect
Buffer: 500 posts in-memory, then SQLite
```

### Data Flow
```
1. Jetstream broadcasts post
2. WebSocket receives JSON
3. Filter by keywords (case-insensitive)
4. Analyze with VADER
5. Classify sentiment
6. Store in SQLite
7. Update stats table
8. Broadcast via WebSocket to UI
9. Display in charts
```

### Performance Characteristics
- **Throughput**: 100-2,000 posts/sec capture, 10,000+ posts/sec analysis
- **Latency**: <1ms capture→analysis, <100ms analysis→display
- **DB Write**: 100+ posts/sec (async, batched)
- **Resource**: <5% CPU idle, 10-20% peak
- **Disk**: ~1KB per post (~1GB per million)

### Configuration
```
Port: 5074 (configurable)
Debug: OFF (production)
Workers: 1 (Eventlet for async)
Database: bsky_corpus.db (local file)

Environment:
  FLASK_ENV=production
  FLASK_DEBUG=False
  PORT=5074
```

### Build & Deployment
```bash
cd /home/coolhand/servers/diachronica/corpus/bluesky_firehose

# Development
python app.py

# Production via service manager
sm start bluesky-corpus
sm logs bluesky-corpus

# Or via gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5074 app_corpus:app
```

### Caddy Routing
```caddyfile
handle /bluesky/corpus/* {
  uri strip_prefix /bluesky/corpus
  reverse_proxy localhost:5074
}
```

### Monitoring & Health
- **Health endpoint**: `http://localhost:5074/api/health`
- **Disk monitoring**: Custom service checks disk usage
- **Log file**: `app.log`
- **Metrics to track**: Posts/sec, sentiment distribution, DB size

### Database Scalability Limits
- **SQLite limit**: Good to ~100M posts, then switch to PostgreSQL
- **Memory**: Unbounded handle cache (LRU eviction recommended)
- **Current size**: 91MB (optimized for sub-millisecond searches)

### Extension Points
- **New sentiment models**: Replace `analyze_sentiment()` function
- **Additional storage**: Add PostgreSQL connection
- **Export features**: New API endpoints
- **Auth system**: Flask-Login middleware
- **Caching**: Redis integration

### Documentation Files
- `ARCHITECTURE.md` - System design, data flow (273 lines)
- `DEPLOYMENT.md` - Deployment guide
- `CRITICAL_FIXES.md` - Known issues
- `CLEANUP_PLAN.md` - Data cleanup strategies

---

## SERVICE 5: SKYMARSHAL

### Quick Facts
- **Location**: `/home/coolhand/servers/skymarshal/`
- **Type**: Python CLI + Flask web interfaces
- **CLI Port**: N/A (interactive)
- **Web Lite Port**: 5050 (main dashboard)
- **Web Full Port**: 5051 (extended interface)
- **URL**: https://dr.eamer.dev/skymarshal/ → localhost:5050
- **Service Manager**: `sm start skymarshal` (lite) / `sm start skymarshal-full`

### Architecture
```
CLI Interface (app.py):
├── InteractiveCARInspector (main controller, 72KB)
├── AuthManager (Bluesky auth)
├── UIManager (Rich terminal UI, 40KB)
├── DataManager (CAR/JSON operations, 74KB)
├── SearchManager (filtering engine, 35KB)
├── DeletionManager (safe deletion workflows)
├── SettingsManager (user preferences)
└── HelpManager (context-aware docs)

Web Interfaces (Flask):
├── lite_app.py (Port 5050 - primary)
│   ├── Quick filters (bangers, dead threads, old posts)
│   ├── Bulk delete with confirmation
│   └── Real-time search
├── app.py (Port 5051 - extended)
│   ├── CAR file processing
│   ├── Setup wizard
│   └── Advanced analytics
└── templates/
    ├── lite_dashboard.html
    ├── hub.html
    ├── dashboard.html
    └── cleanup_*.html

Subprojects:
├── loners/ (Standalone scripts)
│   ├── search.py
│   ├── stats.py
│   ├── delete.py
│   ├── nuke.py (DELETE ALL - DANGEROUS)
│   └── export.py
└── bluevibes/ (Profile viewer subproject)

Data Models (models.py):
├── ContentItem (posts/likes/reposts)
├── UserSettings (batch sizes, limits)
├── SearchFilters (comprehensive filtering)
└── DeleteMode / ContentType (type-safe enums)
```

### Key Features
1. **Content Management**: Search, filter, delete posts
2. **CAR File Processing**: Import/export account backups
3. **Analytics**: Engagement scoring, statistics
4. **Safety**: Multiple confirmation modes before deletion
5. **Filtering**: By date, keyword, engagement, content type
6. **Batch Operations**: Configurable batch sizes
7. **OAuth Integration**: Bluesky AT Protocol authentication

### Technology Stack
- **Framework**: Flask (web), Rich (CLI UI)
- **Protocol**: AT Protocol via `atproto` library (>=0.0.46)
- **CLI**: Interactive menu-driven interface
- **DB**: SQLite (CAR backup format)
- **Caching**: LRU cache for engagement scores (10K capacity)
- **Build**: Python 3.9+, setuptools/pyproject.toml

### AT Protocol Integration
- **Library**: `atproto>=0.0.46`
- **CAR Format**: Binary account backups with CBOR encoding
- **URI Format**: `at://did:plc:*/collection/rkey`
- **Collections**:
  - `app.bsky.feed.post`
  - `app.bsky.feed.like`
  - `app.bsky.feed.repost`
- **Handle Format**: `username.bsky.social` (auto-normalized)

### Data Structures
```python
class ContentItem:
  id: str
  uri: str
  type: ContentType  # post | like | repost
  text: str
  author: str
  likes: int
  reposts: int
  replies: int
  created_at: datetime
  engagement: float  # likes + 2×reposts + 2.5×replies

class SearchFilters:
  keywords: List[str]
  date_from: datetime
  date_to: datetime
  min_engagement: float
  content_type: ContentType
  author: str
```

### CLI Interface (`make run`)
```bash
python -m skymarshal          # Direct execution
make run                      # Handles entry point issues

Interactive menu:
  1. Load data (CAR file or API)
  2. Search & filter
  3. View statistics
  4. Preview delete
  5. Confirm & delete
  6. Export
  7. Settings
```

### Web Lite Dashboard (Port 5050)
Primary interface with:
- Quick filters (bangers, dead threads, old posts)
- Real-time search across posts
- Bulk delete with UI confirmation
- Responsive design

### Web Full Dashboard (Port 5051)
Extended interface with:
- CAR file download
- Setup wizard
- Advanced analytics
- Cleanup workflows

### Performance Characteristics
- **Optimized for**: 10K+ items
- **Statistics**: Single-pass computation
- **Caching**: LRU-cached engagement (10K capacity)
- **Batch processing**: Configurable sizes
- **Engagement formula**: `likes + (2×reposts) + (2.5×replies)`

### File Locations
```
~/.skymarshal/
├── cars/        # CAR backup files
└── json/        # JSON exports

~/.car_inspector_settings.json  # User settings
```

### Build & Deployment
```bash
cd /home/coolhand/servers/skymarshal

# Development setup
make dev          # Install with dev deps
make test         # Run pytest
make format       # Black + isort
make lint         # flake8 + mypy
make check-all    # All quality checks

# Production
make build        # Build distribution packages
python -m skymarshal  # Run CLI

# Via service manager
sm start skymarshal
sm start skymarshal-full
```

### Caddy Routing
```caddyfile
handle /skymarshal/* {
  reverse_proxy localhost:5050
}
```

### Testing
```bash
pytest                                    # Full suite
pytest tests/unit/ -v                     # Unit only
pytest tests/integration/ -v              # Integration
pytest tests/unit/test_auth.py::TestAuthManager -v  # Single class
pytest -m "not performance"               # Skip slow tests
```

### Code Quality
- **Type hints**: Encouraged for public APIs
- **Formatter**: Black (88 char line length)
- **Import sorting**: isort (black profile)
- **Linting**: flake8
- **Type checking**: mypy
- **Testing**: Pytest with unit/integration/performance markers

### Safety Features
**All destructive operations include**:
- Multiple confirmation prompts
- Dry-run preview modes
- Progress tracking with error recovery
- User data isolation by handle
- Transaction rollback capability

### Subprojects

#### Loners (`loners/`)
Standalone scripts for specific operations:
```bash
cd loners
python search.py          # Search & filter
python stats.py           # Analytics
python delete.py          # Safe deletion
python nuke.py            # DELETE ALL (dangerous)
python export.py          # Data export
```

#### Bluevibes (`bluevibes/`)
Separate Flask app for:
- Profile viewing
- Network analysis
- Vibe checking

### Documentation Files
- `CLAUDE.md` - Architecture & commands (172 lines)
- `README.md` - User documentation
- `loners/README.md` - Standalone tools guide

---

## SUPPORTING SERVICES

### CheatChat API
- **Location**: `/home/coolhand/html/bluesky/cheatchat/`
- **Port**: 5056
- **Type**: Flask + Gemini API proxy
- **Feature**: Server-side API key management for client-side access
- **Service Manager**: `sm start cheatchat-api`
- **Integrated Into**: Unified Client `/tools` route via iframe

### Network Graph
- **Location**: `/home/coolhand/html/bluesky/network/`
- **Type**: D3.js chord diagram + Python WebSocket collector
- **Feature**: Follow relationship visualization (first 500 accounts)
- **Tech**: Python `bluesky_follow_graph_jetstream.py`, D3.js frontend
- **Outputs**: `nodes.json`, `links.json`

### Repostdar
- **Location**: `/home/coolhand/html/bluesky/repostdar/`
- **Type**: Static HTML + Tailwind + Chart.js
- **Feature**: Detect self-reposts and analyze patterns
- **Integrated Into**: Unified Client `/tools` route

---

## CROSS-SERVICE ARCHITECTURE

### Shared Data Flow
```
Bluesky Jetstream (wss://jetstream2.us-east.bsky.network)
│
├─→ Firehose (5052) → Real-time sentiment dashboard
│   └─ Socket.IO → Unified Client home feed
│
├─→ Corpus Firehose (5074) → Linguistics analysis
│   └─ SQLite persistence
│
├─→ Post Visualizer (5084) → On-demand thread analysis
│   └─ Fetch via Bluesky API
│
└─→ Unified Client (5086) → Comprehensive interface
    ├─ Backend (3001) → API aggregation
    ├─ Socket.IO → Real-time updates
    └─ Tools integration (iframes)
```

### Authentication Patterns
- **Bluesky OAuth**: Optional, for authenticated API calls
- **AT Protocol**: Direct handle+password for desktop tools
- **Session tokens**: JWT in local storage
- **API Keys**: Server-side in environment variables

### Caching Strategies
- **Post Visualizer**: LocalStorage (5-min fresh, 1-hour stale)
- **Firehose**: In-memory buffer (last 100 posts)
- **Unified Client**: None (always fresh from Socket.IO)
- **Corpus**: SQLite persistence
- **Skymarshal**: LRU cache (10K engagement scores)

### Error Handling
- **Firehose disconnects**: 5-second auto-reconnect
- **API failures**: Retry with exponential backoff
- **Sentiment errors**: VADER always returns a score
- **DB locks**: Transaction rollback with retry

### Performance Optimization
- **Code-splitting**: Unified Client lazy-loads heavy pages
- **Bundle sizes**: 307 KB (target < 430 KB)
- **Load times**: 1.8s (target < 2s)
- **Real-time**: 1000+ posts/sec capacity

---

## INFRASTRUCTURE & DEPLOYMENT

### Caddy Reverse Proxy Configuration
All services behind Caddy at `https://dr.eamer.dev/`:
- Path stripping handled per service (some preserve, some strip)
- WebSocket support for Socket.IO and Jetstream
- HTTPS/TLS automatic

### Service Manager Integration
Central orchestration via `/home/coolhand/service_manager.py`:
```bash
sm start <service>      # Start
sm stop <service>       # Stop
sm restart <service>    # Restart
sm status               # Show all
sm logs <service>       # View logs
```

### Port Allocations
- 5050: Skymarshal (web lite)
- 5051: Skymarshal (web full)
- 5052: Firehose (primary)
- 5056: CheatChat API
- 5074: Corpus Firehose
- 5084: Post Visualizer
- 5086: Unified Client (frontend)
- 3001: Unified Client (backend)

### Database Locations
- Post Visualizer: `data/shares.json` (file-based)
- Firehose: `firehose.db` (SQLite)
- Corpus Firehose: `bsky_corpus.db` (91MB SQLite)
- Unified Client: N/A (queries live via API)
- Skymarshal: `~/.skymarshal/cars/`, `~/.skymarshal/json/`

---

## DOCUMENTATION QUALITY ASSESSMENT

### Post Visualizer
- ✅ Comprehensive CLAUDE.md (40 KB, 146 lines)
- ✅ README with user guide
- ✅ Inline comments in App.tsx
- ✅ Clear type definitions
- ⚠️ Needs: Mobile optimization guide

### Firehose
- ✅ Excellent CLAUDE.md (298 lines)
- ✅ API reference documentation
- ✅ Database schema documented
- ✅ Configuration guide
- ✅ Troubleshooting section
- ⚠️ Needs: Scaling guide, monitoring guide

### Unified Client
- ✅ Outstanding CLAUDE.md (760 lines)
- ✅ Code examples for common patterns
- ✅ Accessibility compliance documented
- ✅ Error handling guide
- ✅ E2E testing setup
- ✅ Performance metrics tracked
- ⚠️ Needs: Deployment checklist

### Corpus Firehose
- ✅ Architecture diagram (273 lines)
- ✅ Data flow visualization
- ✅ Deployment guide
- ✅ Performance characteristics
- ⚠️ Needs: Operational runbook, troubleshooting

### Skymarshal
- ✅ Good CLAUDE.md (172 lines)
- ✅ Manager pattern documented
- ✅ CAR file format explanation
- ✅ Data structures defined
- ⚠️ Needs: CLI usage guide, API documentation

---

## PHASE 2 DOCUMENTATION RECOMMENDATIONS

### Immediate Priorities
1. **Unified Service Guide**: Consolidate all 5 services into single reference
2. **API Catalog**: Document all endpoints (tRPC, REST, WebSocket events)
3. **Data Flow Diagrams**: Visual representation of service interactions
4. **Deployment Checklist**: Production rollout procedures
5. **Troubleshooting Guide**: Common issues and solutions

### Content Structure
```
bluesky-suite-documentation/
├── 01-overview.md (System architecture)
├── 02-post-visualizer.md (Detailed guide)
├── 03-firehose.md (Detailed guide)
├── 04-unified-client.md (Detailed guide)
├── 05-corpus-firehose.md (Detailed guide)
├── 06-skymarshal.md (Detailed guide)
├── 07-api-reference.md (All endpoints)
├── 08-deployment.md (Production setup)
├── 09-troubleshooting.md (Common issues)
├── 10-architecture-diagrams.md (Visual reference)
└── QUICK_START.md (5-minute setup guide)
```

### Key Metrics to Track
- Uptime/SLA targets per service
- API response times
- Database query performance
- Error rates by category
- User engagement metrics

---

## METADATA EXPORT SUMMARY

**Total Services**: 5 core + 3 supporting = 8 total
**Total Lines of Code**: 40K+ Python + 30K+ TypeScript
**Total Database Size**: ~100MB (SQLite + dependencies)
**Total Ports Used**: 9 (5050-5086, 3001)
**Total Documentation**: ~1,500 lines (CLAUDE.md + supporting)

**Status**: ✅ Ready for Phase 2 comprehensive documentation

---

**Next Steps**:
1. Generate consolidated Phase 2 documentation using this metadata
2. Create visual architecture diagrams
3. Build searchable API reference
4. Develop deployment procedures
5. Establish monitoring/alerting procedures
