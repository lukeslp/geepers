# Bluesky Suite Services - Comprehensive Metadata
**Phase 2 Documentation Preparation**
Generated: 2026-01-18
Author: Claude Code

---

## Table of Contents
1. [Service Overview](#service-overview)
2. [Individual Service Details](#individual-service-details)
3. [API Endpoints Reference](#api-endpoints-reference)
4. [Technology Stack Summary](#technology-stack-summary)
5. [Routing & Port Mapping](#routing--port-mapping)
6. [Data Sources & Integration Points](#data-sources--integration-points)
7. [Development Workflows](#development-workflows)
8. [Cross-Service Dependencies](#cross-service-dependencies)

---

## Service Overview

The Bluesky Suite is a comprehensive collection of tools for analyzing, managing, and visualizing Bluesky social network data. Five primary services form the suite:

| Service | Port | Type | Status | Location |
|---------|------|------|--------|----------|
| Firehose | 5052 | Node.js (TypeScript) | Production | `/home/coolhand/html/firehose/` |
| Post Visualizer | 5084 | React + Express | Production | `/home/coolhand/html/bluesky/post-visualizer/` |
| Bluesky Corpus | 5074 | Flask (Python) | Production | `/home/coolhand/servers/diachronica/corpus/bluesky_firehose/` |
| Unified | 3001 (backend), 5086 (frontend) | React + Express | Production | `/home/coolhand/html/bluesky/unified/` |
| Skymarshal | 5050 | Flask (Python) | Production | `/home/coolhand/servers/skymarshal/` |

**Public URL Base**: `https://dr.eamer.dev/bluesky/` and `https://dr.eamer.dev/skymarshal/`

---

## Individual Service Details

### 1. Firehose Dashboard

**Purpose**: Real-time sentiment analysis dashboard for Bluesky AT Protocol firehose stream

**Location**: `/home/coolhand/html/firehose/`

**Port**: 5052

**Public URL**: `https://dr.eamer.dev/bluesky/firehose/`

**Technology Stack**:
- **Frontend**: React 19, TypeScript, Vite, Recharts, shadcn/ui, Tailwind CSS 4
- **Backend**: Express.js, tRPC, Node.js
- **Real-time**: Socket.IO, WebSocket client
- **Database**: SQLite with Drizzle ORM
- **NLP**: `sentiment` npm package, `natural` package

**Key Files**:
```
firehose/
├── client/
│   ├── src/pages/Dashboard.tsx    # Main analytics dashboard
│   ├── src/components/            # UI components (shadcn/ui)
│   ├── src/hooks/useSocket.ts     # Socket.IO real-time hook
│   └── src/lib/trpc.ts            # tRPC client configuration
├── server/
│   ├── _core/index.ts             # Server entry point
│   ├── firehose.ts                # Firehose service (singleton)
│   ├── sentiment.ts               # NLP sentiment analysis
│   ├── db.ts                      # Database queries
│   ├── routers.ts                 # tRPC API endpoints
│   ├── socketio.ts                # Socket.IO setup
│   └── storage.ts                 # In-memory stats
├── drizzle/
│   ├── schema.ts                  # SQLite database schema
│   └── meta/                      # Migrations
├── firehose.db                    # SQLite database (~75MB)
├── start.sh                       # Production startup script
└── vite.config.ts                 # Frontend build configuration
```

**Main API Routes** (tRPC):
```
POST /api/trpc/firehose.start          # Start firehose stream
POST /api/trpc/firehose.stop           # Stop stream
GET  /api/trpc/firehose.stats          # Get statistics
GET  /api/trpc/firehose.filters        # Get active filters
GET  /api/trpc/firehose.recentPosts    # Get recent posts (last 100)
GET  /api/trpc/posts.list              # List posts with filters
GET  /api/trpc/stats.global            # Global statistics
GET  /api/trpc/stats.hourly            # Hourly stats
GET  /api/trpc/stats.languages         # Language distribution
GET  /api/trpc/stats.hashtags          # Hashtag trends
POST /api/trpc/posts.exportCSV         # Export to CSV
```

**Real-time Events** (Socket.IO):
- `post`: Broadcast on every processed post
- `stats`: Updated every 1 second

**Database Schema** (Core Tables):
- `posts`: Full post data with metadata
- `statsGlobal`: All-time aggregates
- `statsHourly`: Hourly time-series
- `statsDaily`: Daily time-series
- `statsLanguage`: Language distribution
- `statsHashtag`: Hashtag trends
- `authorInteractions`: Network analysis
- `sessions`: Firehose session tracking

**Auto-start**: Yes (2 seconds after server launch)

**Development Commands**:
```bash
pnpm dev          # Start dev server (hot reload)
pnpm build        # Build for production
pnpm start        # Start production server
pnpm check        # Type checking
pnpm format       # Format code
```

**Configuration** (`.env`):
```
NODE_ENV=production
PORT=5052
DATABASE_URL=./firehose.db
```

**Data Source**: Bluesky Jetstream WebSocket (`wss://jetstream2.us-east.bsky.network`)

**Sentiment Classification**:
- Positive: comparative > 0.1
- Negative: comparative < -0.1
- Neutral: otherwise

---

### 2. Post Visualizer

**Purpose**: Interactive force-directed graph visualization of Bluesky post interactions (likes, reposts, replies, quotes)

**Location**: `/home/coolhand/html/bluesky/post-visualizer/`

**Port**: 5084

**Public URL**: `https://dr.eamer.dev/bluesky/post-visualizer/`

**Technology Stack**:
- **Frontend**: React 19, TypeScript, D3.js v7, Tailwind CSS 4, Vite
- **Backend**: Express.js
- **Visualization**: D3 force-directed graph with radial grouping
- **API Client**: Custom Bluesky API client (handle resolution, profile batching)

**Key Files**:
```
post-visualizer/
├── src/
│   ├── App.tsx              # All application logic (2542 lines)
│   │   ├── Types            # GraphNode, GraphLink, BlueskyPost
│   │   ├── API Utilities    # fetchAllPages, resolveHandle
│   │   ├── Cache Utilities  # LocalStorage TTL caching
│   │   ├── Graph Building   # Deep interaction analysis
│   │   ├── ForceGraph       # D3 force simulation & SVG
│   │   ├── Intro Tooltip    # Initial URL/handle input overlay
│   │   ├── Instructions     # How-to modal
│   │   └── Main Component   # State & layout
│   ├── App.css              # Touch handling & graph styling
│   └── main.tsx             # Entry point with iOS gesture handling
├── server.js                # Express API for share endpoints
├── vite.config.ts           # Vite + React + Tailwind config
├── data/                    # Runtime-created directory
│   ├── shares.json          # Share metadata storage
│   └── images/              # Screenshot PNGs
└── dist/                    # Production build output
```

**Main API Routes** (Express):
```
POST /bluesky/post-visualizer/api/share          # Save graph + image (OG metadata)
GET  /bluesky/post-visualizer/api/share/:id      # Retrieve share
GET  /bluesky/post-visualizer/health             # Health check
GET  /bluesky/post-visualizer/?share=<id>        # Dynamic OG tags
```

**GraphNode Data Structure**:
```typescript
interface GraphNode {
  id: string;                 // DID
  handle: string;
  displayName: string;        // From profile
  avatar?: string;
  types: Set<string>;         // 'like', 'repost', 'reply', 'quote', 'focus'
  socialStatus: 'mutual' | 'follows_op' | 'followed_by_op' | 'none';
  followers: number;
  postData?: { uri, text, embed };
}
```

**D3 Force Configuration**:
- `forceCollide` radius: `sqrt(followers/100) * 3`, clamped 8-40px
- `forceManyBody` strength: -50 to -300
- `forceRadial` groups nodes by interaction type

**Data Flow**:
1. User pastes Bluesky post URL or enters handle
2. Parse URL → resolve handle to DID → construct AT URI
3. Fetch thread + likes + reposts (paginated with caching)
4. Build graph: nodes (users) + links (interactions)
5. D3 force simulation positions nodes
6. SVG rendering with labels, tooltips, info panel
7. Share functionality saves PNG + metadata

**Cache Strategy**:
- LocalStorage with TTL (24 hours)
- Checksums for invalidation
- Batched profile fetches (25 at a time)

**Development Commands**:
```bash
pnpm dev       # Dev server (Vite on 5083 during development)
pnpm build     # TypeScript compile + Vite build
pnpm start     # Run Express server
pnpm lint      # ESLint
pnpm preview   # Preview production build
```

**Bluesky API Endpoints Used**:
- `com.atproto.identity.resolveHandle` - Handle → DID resolution
- `app.bsky.actor.getProfile` / `getProfiles` - Profile data
- `app.bsky.feed.getPostThread` - Thread with nested replies
- `app.bsky.feed.getLikes` - Paginated post likes
- `app.bsky.feed.getRepostedBy` - Paginated reposts
- `app.bsky.graph.getFollows` - Following list
- `app.bsky.graph.getFollowers` - Followers list

---

### 3. Bluesky Corpus

**Purpose**: Corpus linguistics firehose collector - analyze linguistic patterns in real-time Bluesky data with VADER sentiment analysis

**Location**: `/home/coolhand/servers/diachronica/corpus/bluesky_firehose/`

**Port**: 5074

**Public URL**: `https://dr.eamer.dev/bluesky/corpus/`

**Technology Stack**:
- **Backend**: Flask (Python)
- **Server**: Gunicorn with Eventlet worker
- **Database**: SQLite (~87MB)
- **NLP**: VADER sentiment analyzer (NLTK)
- **Streaming**: Server-Sent Events (SSE), WebSocket for Jetstream

**Key Files**:
```
bluesky_firehose/
├── app_corpus.py            # Corpus-specific API (Flask)
├── app.py                   # Main Flask application
├── models.py                # Data structures
├── bsky_corpus.db           # SQLite corpus database (~87MB)
├── ARCHITECTURE.md          # Architecture overview
├── DEPLOYMENT.md            # Deployment guide
└── CRITICAL_FIXES.md        # Known issues & fixes
```

**Main API Routes** (Flask):
```
GET  /api/health                    # Health check
GET  /api/corpus/stats              # Corpus statistics
GET  /api/corpus/search             # Search corpus
GET  /api/corpus/trends             # Language/sentiment trends
GET  /api/corpus/language/<lang>    # Language-specific data
GET  /api/corpus/sentiment/<type>   # Sentiment distribution
POST /api/corpus/export             # Export data
```

**Sentiment Analysis**:
- VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Classifies text as positive/negative/neutral
- Scores normalized to [-1, 1] range

**Database Schema** (Core):
- Posts with timestamp, author, text, sentiment
- Language detection and tagging
- Hashtag and mention extraction
- N-gram analysis (bigrams, trigrams)

**Server Configuration**:
```
Gunicorn: --worker-class eventlet -w 1 --bind 0.0.0.0:5074
Timeout: 30 seconds
Start timeout: 30 seconds
```

**Development Commands**:
```bash
python app.py                    # Run development server
gunicorn -w 1 app_corpus:app    # Production (Corpus API)
pytest                          # Run tests
```

**Performance Notes**:
- Database: ~87MB SQLite
- Single-worker Gunicorn (eventlet for async)
- Handles high-volume firehose streaming

---

### 4. Unified Interface

**Purpose**: Comprehensive unified interface for Bluesky social network management - feed browsing, analytics, content search, visualization, chat, and moderation

**Location**: `/home/coolhand/html/bluesky/unified/`

**Port**: 3001 (backend), 5086 (frontend dev server)

**Public URL**: `https://dr.eamer.dev/bluesky/unified/`

**Technology Stack**:
- **Frontend**: React 19, TypeScript, Vite, pnpm monorepo
- **Backend**: Express.js with tRPC, Node.js
- **Real-time**: Socket.IO for Jetstream events
- **Components**: shadcn/ui, Radix UI, Tailwind CSS 4
- **Database**: SQLite (optional)
- **Authentication**: OAuth (optional)

**Architecture**:
```
unified/
├── app/                           # React frontend application
│   ├── src/
│   │   ├── pages/                # Route components (Home, Thread, Search, Analytics)
│   │   ├── components/           # UI components (layout, auth, errors)
│   │   ├── hooks/                # Custom hooks (useSocket, useInfiniteScroll)
│   │   ├── lib/                  # Utilities and configurations
│   │   └── router.tsx            # React Router with code-splitting
│   ├── vite.config.ts            # Vite configuration
│   └── public/                   # Static assets
├── server/                        # Express backend
│   ├── src/
│   │   ├── _core/
│   │   │   ├── index.ts          # Server entry point
│   │   │   ├── trpc.ts           # tRPC configuration
│   │   │   ├── context.ts        # Request context
│   │   │   └── oauth.ts          # OAuth routes
│   │   ├── socket/
│   │   │   ├── index.ts          # Socket.IO setup
│   │   │   ├── jetstream.ts      # Jetstream WebSocket handler
│   │   │   └── events.ts         # Event type definitions
│   │   ├── routes/
│   │   │   ├── api.ts            # tRPC router
│   │   │   └── health.ts         # Health endpoint
│   │   ├── types/                # Shared TypeScript types
│   │   ├── config/               # Configuration
│   │   └── app.ts                # Express app setup
│   ├── dist/                     # Compiled TypeScript
│   └── server.ts                 # Server entry (dist/index.js)
├── packages/
│   ├── api-client/               # Bluesky API wrapper
│   ├── components/               # Shared React components
│   ├── skymarshal/               # Bluesky management toolkit
│   └── utils/                    # Shared utilities
├── pnpm-workspace.yaml           # Monorepo configuration
└── package.json                  # Root package
```

**Main API Routes** (tRPC):
```
/api/trpc/feed.*                 # Feed operations
/api/trpc/posts.*                # Post operations
/api/trpc/search.*               # Search functionality
/api/trpc/profile.*              # Profile management
/api/trpc/analytics.*            # Analytics data
/api/trpc/notifications.*        # Notification handling
/api/trpc/auth.*                 # Authentication
/api/trpc/moderation.*           # Moderation tools
```

**Real-time Events** (Socket.IO):
- Jetstream post events
- Real-time notifications
- Feed updates
- Path: `/bluesky/unified/socket.io/` (Caddy strips prefix)

**WebSocket/Socket.IO**:
- Route: `/bluesky/unified/socket.io/*`
- Caddy matcher for Upgrade header
- Preserves Bluesky Jetstream subscriptions

**Service Manager Integration**:
```
unified-server:   node server/dist/index.js (port 3001)
unified-client:   pnpm --filter @bluesky/unified-app dev (port 5086)
```

**Development Commands**:
```bash
pnpm install              # Install all workspace dependencies
pnpm dev                  # Start dev servers (frontend 5086, backend 3001)
pnpm build                # Build for production
pnpm check                # Type checking
pnpm format               # Format code
pnpm test:e2e             # Run E2E tests
```

**Environment Variables**:
```
NODE_ENV=production
PORT=3001
OAUTH_SERVER_URL=         # Optional OAuth endpoint
JWT_SECRET=               # Session signing secret
```

**Caddy Configuration**:
```
# API routes (strip prefix)
handle /bluesky/unified/api/* {
    uri strip_prefix /bluesky/unified
    reverse_proxy localhost:3001
}

# Socket.IO WebSocket
@websocket-bluesky-unified {
    path /bluesky/unified/socket.io/*
    header Connection *Upgrade*
    header Upgrade websocket
}
handle @websocket-bluesky-unified {
    uri strip_prefix /bluesky/unified
    reverse_proxy localhost:3001
}

# Frontend (handle without stripping - Vue Router handles routing)
handle /bluesky/unified/* {
    reverse_proxy localhost:5086
}
```

---

### 5. Skymarshal

**Purpose**: Bluesky bulk content management - search, analyze, and safely delete posts, likes, reposts with comprehensive filtering and statistics

**Location**: `/home/coolhand/servers/skymarshal/`

**Port**: 5050 (Lite Web), 5051 (Full Web)

**Public URL**: `https://dr.eamer.dev/skymarshal/`

**Technology Stack**:
- **Backend**: Flask (Python 3.9+)
- **CLI**: Rich terminal UI
- **AT Protocol**: `atproto>=0.0.46` library
- **Data**: CAR files (binary backups), JSON export/import
- **Caching**: LRU cache for engagement scores (10K capacity)
- **Type Hints**: Full type annotations

**Architecture**:
```
skymarshal/
├── skymarshal/
│   ├── app.py                   # Main CLI controller (72KB)
│   ├── models.py                # Data structures
│   ├── auth.py                  # AT Protocol authentication
│   ├── data_manager.py          # CAR/JSON operations (74KB)
│   ├── search.py                # Filter engine (35KB)
│   ├── deletion.py              # Safe deletion workflows
│   ├── ui.py                    # Rich terminal UI (40KB)
│   └── web/                     # Flask web interfaces
│       ├── lite_app.py          # Streamlined dashboard (port 5050)
│       ├── app.py               # Full interface (port 5051)
│       └── templates/           # Jinja2 templates
├── loners/                      # Standalone CLI scripts
│   ├── search.py
│   ├── stats.py
│   ├── delete.py
│   ├── nuke.py                  # Delete ALL (dangerous)
│   └── export.py
├── bluevibes/                   # Profile viewer subproject (port 5012)
├── tests/                       # Unit, integration, performance tests
├── pyproject.toml               # Build configuration
└── Makefile                     # Development commands
```

**Lite Web App** (Port 5050):
**Primary dashboard** at `https://dr.eamer.dev/skymarshal/`

Features:
- Quick filters: "bangers" (high engagement), "dead threads", "old posts"
- Real-time search and filtering
- Bulk delete with confirmation
- Engagement statistics
- Streamlined UI optimized for mobile

**Full Web App** (Port 5051):
Extended interface with:
- CAR file download/processing
- Setup wizard for initial configuration
- Comprehensive analytics dashboard
- Advanced filtering options

**Main API Routes** (Flask):
```
GET  /                          # Lite dashboard
GET  /api/search                # Search posts
GET  /api/stats                 # Statistics
GET  /api/filters               # Available filters
POST /api/delete                # Delete operation
POST /api/export                # Export data
GET  /health                    # Health check
```

**Manager Pattern** (CLI Architecture):
```
InteractiveCARInspector (app.py)
├── AuthManager              # AT Protocol authentication
├── UIManager                # Rich terminal components
├── DataManager              # CAR/JSON file operations
├── SearchManager            # Content filtering & statistics
├── DeletionManager          # Safe deletion workflows
├── SettingsManager          # User preferences
└── HelpManager              # Context-aware documentation
```

**Data Structures** (models.py):
```python
class ContentItem:
    uri: str                    # AT URI
    cid: str
    type: ContentType           # 'post', 'like', 'repost'
    timestamp: datetime
    text: str
    engagement: float           # likes + (2 × reposts) + (2.5 × replies)
    author_did: str

class SearchFilters:
    keywords: List[str]
    engagement_min: float
    engagement_max: float
    date_range: Tuple[datetime, datetime]
    content_type: ContentType
    hashtags: List[str]
```

**AT Protocol Integration**:
- **Library**: `atproto>=0.0.46`
- **CAR Files**: Binary account backups with CBOR encoding
- **URI Format**: `at://did:plc:*/collection/rkey`
- **Collections**:
  - `app.bsky.feed.post`
  - `app.bsky.feed.like`
  - `app.bsky.feed.repost`
- **Handle Normalization**: `@username` → `username.bsky.social`

**File Locations**:
```
~/.skymarshal/
├── cars/                      # CAR backup files
└── json/                      # JSON exports

~/.car_inspector_settings.json  # User settings
```

**Engagement Formula**:
```
Engagement Score = likes + (2 × reposts) + (2.5 × replies)
```

**Performance Optimizations**:
- Single-pass statistics computation
- LRU cache for engagement scores (10K items)
- Batch processing with configurable sizes
- Optimized for 10K+ items

**Development Commands**:
```bash
make run              # Run CLI (interactive menu)
make dev              # Install with dev dependencies
make test             # Run pytest suite
make format           # Black + isort formatting
make lint             # flake8 + mypy
make check-all        # All quality checks
make build            # Build distribution packages
```

**Code Style**:
- Python 3.9+ with type hints
- Black (88 char line length)
- isort (black profile)
- Rich console for terminal output
- Pytest with unit/integration/performance markers

**Safety Features**:
- Multiple confirmation prompts for destructive operations
- Dry-run preview modes
- Progress tracking with error recovery
- User data isolation by handle

**Subprojects**:
- **Bluevibes** (port 5012): Standalone Flask app for Bluesky profile viewing and network analysis

---

## API Endpoints Reference

### Consolidated Endpoint Summary

| Service | Endpoint | Method | Purpose |
|---------|----------|--------|---------|
| **Firehose** | `/api/trpc/firehose.start` | POST | Start stream |
| | `/api/trpc/firehose.stop` | POST | Stop stream |
| | `/api/trpc/firehose.stats` | GET | Statistics |
| | `/api/trpc/posts.list` | GET | List posts |
| | `/api/trpc/posts.exportCSV` | POST | Export CSV |
| **Post Visualizer** | `/api/share` | POST | Save graph |
| | `/api/share/:id` | GET | Retrieve share |
| | `/health` | GET | Health check |
| **Corpus** | `/api/corpus/stats` | GET | Statistics |
| | `/api/corpus/search` | GET | Search posts |
| | `/api/corpus/trends` | GET | Trends |
| **Unified** | `/api/trpc/feed.*` | GET/POST | Feed ops |
| | `/api/trpc/search.*` | GET | Search |
| | `/api/trpc/posts.*` | GET/POST | Post ops |
| | `/socket.io` | WS | Real-time |
| **Skymarshal** | `/api/search` | GET | Search |
| | `/api/stats` | GET | Stats |
| | `/api/delete` | POST | Delete |
| | `/api/export` | POST | Export |

---

## Technology Stack Summary

### Frontend Technologies
- **React 19**: All frontend applications
- **TypeScript**: Type safety across all services
- **Vite**: Build tool for React applications
- **Tailwind CSS 4**: Utility-first styling
- **D3.js v7**: Graph visualization (Post Visualizer)
- **Recharts**: Chart library (Firehose)
- **shadcn/ui**: Component library (Firehose, Unified)
- **Socket.IO Client**: Real-time updates

### Backend Technologies
- **Express.js**: API servers (Firehose, Post Visualizer, Unified)
- **Flask**: Web dashboards (Corpus, Skymarshal)
- **tRPC**: Type-safe APIs
- **Node.js**: JavaScript runtime
- **Python 3.9+**: CLI and server logic

### Database & Persistence
- **SQLite**: Primary database (Firehose, Corpus, Skymarshal)
- **Drizzle ORM**: Type-safe SQL queries
- **CAR Files**: Binary Bluesky backups
- **JSON**: Data import/export

### Real-time Communication
- **Socket.IO**: Pub/sub events
- **WebSocket**: Bluesky Jetstream
- **Server-Sent Events**: Optional streaming

### NLP & Analysis
- **VADER Sentiment**: Corpus linguistic analysis
- **sentiment npm**: Firehose sentiment scoring
- **natural npm**: Language detection
- **NLTK**: Python NLP toolkit

### DevOps & Build
- **pnpm**: Package manager (monorepo workspaces)
- **Gunicorn**: Python WSGI server
- **esbuild**: TypeScript bundling
- **tsx**: TypeScript execution

---

## Routing & Port Mapping

### Service Manager Configuration

```python
SERVICES = {
    'firehose': {
        'port': 5052,
        'script': '/home/coolhand/html/firehose/start.sh',
        'health_endpoint': 'http://localhost:5052/',
        'start_timeout': 45
    },
    'bluesky-corpus': {
        'port': 5074,
        'script': '/home/coolhand/servers/diachronica/corpus/bluesky_firehose/venv/bin/gunicorn',
        'args': ['--worker-class', 'eventlet', '-w', '1', '--bind', '0.0.0.0:5074', 'app_corpus:app'],
        'health_endpoint': 'http://localhost:5074/api/health'
    },
    'unified-server': {
        'port': 3001,
        'script': 'node server/dist/index.js',
        'health_endpoint': 'http://localhost:3001/health'
    },
    'unified-client': {
        'port': 5086,
        'script': 'pnpm --filter @bluesky/unified-app dev',
        'health_endpoint': 'http://localhost:5086/'
    },
    'post-visualizer': {
        'port': 5084,
        'script': '/home/coolhand/html/bluesky/post-visualizer/start.sh',
        'health_endpoint': 'http://localhost:5084/bluesky/post-visualizer/health'
    },
    'skymarshal': {
        'port': 5050,
        'script': '/home/coolhand/servers/skymarshal/skymarshal/web/lite_app.py',
        'health_endpoint': 'http://localhost:5050/',
        'env': {'PYTHONPATH': '/home/coolhand/servers/skymarshal'}
    }
}
```

### Caddy Configuration

```caddyfile
# Bluesky Firehose (Node.js, port 5052)
handle /bluesky/firehose {
    redir https://{host}/bluesky/firehose/ permanent
}
handle_path /bluesky/firehose/* {
    reverse_proxy localhost:5052
}

# Bluesky Corpus (Flask, port 5074)
handle /bluesky/corpus {
    redir https://{host}/bluesky/corpus/ permanent
}
handle /bluesky/corpus/* {
    uri strip_prefix /bluesky/corpus
    reverse_proxy localhost:5074
}

# Bluesky Post Visualizer (Express, port 5084)
handle /bluesky/post-visualizer {
    redir https://{host}/bluesky/post-visualizer/?{query} permanent
}
handle /bluesky/post-visualizer/* {
    reverse_proxy localhost:5084
}

# Bluesky Unified (Express backend 3001, React frontend 5086)
handle /bluesky/unified/health {
    uri strip_prefix /bluesky/unified
    reverse_proxy localhost:3001
}
handle /bluesky/unified/api/* {
    uri strip_prefix /bluesky/unified
    reverse_proxy localhost:3001
}
@websocket-bluesky-unified {
    path /bluesky/unified/socket.io/*
    header Connection *Upgrade*
    header Upgrade websocket
}
handle @websocket-bluesky-unified {
    uri strip_prefix /bluesky/unified
    reverse_proxy localhost:3001 {
        header_up Host {host}
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
}
handle /bluesky/unified/* {
    reverse_proxy localhost:5086
}

# Skymarshal (Flask, port 5050)
handle /skymarshal/* {
    reverse_proxy localhost:5050 {
        header_up X-Forwarded-Prefix /skymarshal
    }
}
handle /skymarshal {
    reverse_proxy localhost:5050 {
        header_up X-Forwarded-Prefix /skymarshal
    }
}
```

---

## Data Sources & Integration Points

### Bluesky AT Protocol API

**Base URL**: `https://public.api.bsky.app/xrpc/`

**Core Endpoints** (Used by all services):
- `com.atproto.identity.resolveHandle` - Handle to DID resolution
- `app.bsky.actor.getProfile` - Single profile data
- `app.bsky.actor.getProfiles` - Batch profile data (up to 25)
- `app.bsky.feed.getPostThread` - Post thread with nested replies
- `app.bsky.feed.getLikes` - Paginated post likes
- `app.bsky.feed.getRepostedBy` - Paginated repost list
- `app.bsky.feed.getFeed` - Feed generation
- `app.bsky.feed.getAuthorFeed` - Author's post history
- `app.bsky.graph.getFollows` - Following list
- `app.bsky.graph.getFollowers` - Followers list
- `com.atproto.repo.listRecords` - Record listing

**Rate Limits**:
- Default: 300 requests per 5 minutes
- Exponential backoff implemented in Post Visualizer
- Batch fetching (25 profiles at a time) reduces API calls

### Bluesky Jetstream WebSocket API

**Endpoint**: `wss://jetstream2.us-east.bsky.network/subscribe`

**Query Parameters**:
- `wantedCollections=app.bsky.feed.post` - Filter to posts only
- `wantedEvents=identity` - Include identity events (for handle cache)

**Event Types**:
- `#commit` - New post/record commits
- `#identity` - Handle-to-DID mappings
- `#account` - Account state changes

**Services Using Jetstream**:
- **Firehose**: Main data ingestion source
- **Unified**: Real-time post updates via Socket.IO
- **Corpus**: Linguistic analysis of live posts

**Reconnection Strategy**:
- Auto-reconnect on disconnect
- 5-second delay between reconnection attempts
- Event-driven architecture (EventEmitter pattern)

### AT Protocol CAR Files

**Format**: Binary backup format with CBOR encoding

**Collections**:
- `app.bsky.feed.post` - Posts
- `app.bsky.feed.like` - Likes (limited to 30K)
- `app.bsky.feed.repost` - Reposts (limited to 30K)
- `app.bsky.feed.threadgate` - Reply restrictions
- `app.bsky.actor.profile` - Profile record

**Usage** (Skymarshal):
- Download from Bluesky Settings
- Parse and extract collections
- Cache in `~/.skymarshal/cars/`
- Import into application for offline analysis

---

## Development Workflows

### Local Development Setup

#### Firehose
```bash
cd /home/coolhand/html/firehose
pnpm install
pnpm dev                    # Runs on port 3000 by default
# Service manager port override: 5052
```

#### Post Visualizer
```bash
cd /home/coolhand/html/bluesky/post-visualizer
pnpm install
pnpm dev                    # Runs on port 5083
pnpm build && pnpm start    # Production mode
```

#### Unified
```bash
cd /home/coolhand/html/bluesky/unified
pnpm install
pnpm dev                    # Runs backend on 3001, frontend on 5086
pnpm build                  # Build for production
```

#### Corpus
```bash
cd /home/coolhand/servers/diachronica/corpus/bluesky_firehose
source venv/bin/activate
pip install -r requirements.txt
python app.py               # Development server
gunicorn --worker-class eventlet -w 1 app_corpus:app  # Production
```

#### Skymarshal
```bash
cd /home/coolhand/servers/skymarshal
pip install -e .[dev]
make dev                    # Install dev dependencies
python skymarshal/web/lite_app.py     # Web dashboard
python -m skymarshal        # CLI interface
```

### Testing

#### Node.js Services
```bash
pnpm test                   # Run test suite
pnpm check                  # Type checking
pnpm lint                   # ESLint
```

#### Python Services
```bash
pytest                      # Full test suite
pytest -v                   # Verbose output
pytest -m "not performance" # Skip slow tests
make test                   # Skymarshal-specific
```

### Building for Production

#### Node.js
```bash
pnpm build          # Build frontend and backend
pnpm start          # Start production server
```

#### Python
```bash
gunicorn [options] app:app  # Flask applications
make build                  # Skymarshal distribution
```

### Debugging

#### Firehose
```bash
# Check WebSocket connection
tail -f firehose.log
grep WebSocket firehose.log

# Monitor real-time updates
curl http://localhost:5052/api/trpc/firehose.stats

# Inspect database
sqlite3 firehose.db ".tables"
```

#### Post Visualizer
```bash
# Check browser console (Developer Tools)
# Network tab for Bluesky API calls
# Watch for rate limiting: 429 responses

# Server logs
tail -f post-visualizer.log
```

#### Unified
```bash
# Check Socket.IO connection
curl http://localhost:3001/health

# Monitor WebSocket in browser DevTools
# Check Caddy logs for routing issues
```

---

## Cross-Service Dependencies

### Shared Dependencies
- **atproto library**: Bluesky AT Protocol client (Skymarshal, Unified)
- **Shared Bluesky API patterns**: Handle resolution, profile batching
- **SQLite databases**: Independent instances per service

### Data Flow Between Services

```
Bluesky Jetstream
    ├→ Firehose (real-time sentiment analysis)
    │   └→ Socket.IO broadcast
    │       └→ Unified (consume real-time posts)
    └→ Corpus (linguistic analysis)

Bluesky AT Protocol API
    ├→ Post Visualizer (graph building)
    │   └→ User interaction visualization
    ├→ Unified (feed loading, profiles)
    └→ Skymarshal (content search, deletion)

Unified
    ├→ Imports Skymarshal modules (content management)
    └→ Displays real-time Firehose data via Socket.IO
```

### Service Communication Methods

1. **Direct Proxying** (Caddy):
   - Client → Caddy → Backend service
   - Used for: REST API, WebSocket

2. **Socket.IO Real-time**:
   - Firehose broadcasts → Unified subscribes
   - Jet stream events → Real-time post updates

3. **Database Independence**:
   - Each service maintains own SQLite
   - No cross-database queries
   - Import/export for data sharing

### Configuration & Secrets

**API Keys** (in `/home/coolhand/documentation/API_KEYS.md`):
- Bluesky account credentials (for CLI/admin operations)
- xAI API key (if using vision features)
- OAuth credentials (if OAuth enabled)

**Environment Variables**:
- `NODE_ENV`: production/development
- `PORT`: Service port override
- `DATABASE_URL`: Optional custom database path
- `PYTHONPATH`: Python import paths (Skymarshal)

---

## Conclusion

The Bluesky Suite comprises five interconnected services providing comprehensive analysis, visualization, and management of Bluesky social network data. Each service specializes in different aspects:

- **Firehose**: Real-time sentiment analysis
- **Post Visualizer**: Interactive graph visualization
- **Corpus**: Linguistic analysis
- **Unified**: Comprehensive management interface
- **Skymarshal**: Content management and deletion

All services share common technology stacks (TypeScript, React, Flask, SQLite) and integrate through Bluesky's AT Protocol APIs and Jetstream WebSocket stream.

This metadata document serves as the foundation for Phase 2 documentation generation, providing comprehensive technical specifications for each service.

---

**Last Updated**: 2026-01-18
**Scope**: Production services on dr.eamer.dev
**Author**: Claude Code
**Review Status**: Ready for Phase 2 documentation
