# Bluesky Suite - Complete Port and Path Reference

**Generated**: 2026-01-18
**Purpose**: Single source of truth for all ports, paths, and service locations

---

## PORT ALLOCATION SUMMARY

### Active Bluesky Suite Ports
| Port | Service | Type | Status | Health Endpoint |
|------|---------|------|--------|-----------------|
| **3001** | Unified Client (Backend) | Express | Production | `http://localhost:3001/health` |
| **5050** | Skymarshal (Web Lite) | Flask | Production | `http://localhost:5050/` |
| **5051** | Skymarshal (Web Full) | Flask | Development | N/A |
| **5052** | Firehose | Node.js | Production | `http://localhost:5052/api/trpc/system.health` |
| **5056** | CheatChat API | Flask | Production | `http://localhost:5056/` |
| **5074** | Corpus Firehose | Flask | Production | `http://localhost:5074/api/health` |
| **5084** | Post Visualizer | Express | Production | `http://localhost:5084/bluesky/post-visualizer/health` |
| **5086** | Unified Client (Frontend) | Vite | Production | `http://localhost:5086/` |

### Development Ports (Internal Use)
- **5083**: Post Visualizer (Vite dev server)
- **3000**: Firehose (Vite dev frontend during development)

### Reserved Ports (Not Currently Used)
- 5010-5019: Reserved for testing APIs
- 5050-5059: Reserved for service testing

---

## FILESYSTEM LOCATIONS

### Frontend Services (/home/coolhand/html/bluesky/)

#### Post Visualizer
```
/home/coolhand/html/bluesky/post-visualizer/
├── CLAUDE.md              # Architecture guide (40 KB)
├── README.md              # User documentation
├── server.js              # Express server (production)
├── vite.config.ts         # Vite configuration
├── package.json           # Dependencies
├── src/
│   ├── App.tsx           # Main component (~2600 lines)
│   ├── App.css           # Touch handling + styling
│   ├── main.tsx          # Entry point
│   └── index.css         # Tailwind CSS
├── dist/                 # Production build output
└── data/                 # Runtime directory
    ├── shares.json       # Share metadata
    └── images/           # OG image screenshots
```

**Production Entry**: `server.js`
**Dev Entry**: `pnpm dev` (Vite on 5083)
**Production Port**: 5084

---

#### Firehose
```
/home/coolhand/html/firehose/
├── CLAUDE.md              # Comprehensive guide (298 lines)
├── API_REFERENCE.md       # Endpoint documentation
├── README.md              # User guide
├── start.sh               # Service manager entry
├── package.json           # Dependencies
├── pnpm-workspace.yaml    # Workspace config
├── firehose.db            # SQLite database
├── client/                # React frontend
│   ├── src/
│   │   ├── pages/Dashboard.tsx  # Main UI
│   │   ├── components/           # UI components
│   │   ├── hooks/useSocket.ts    # Socket.IO
│   │   └── lib/trpc.ts           # tRPC client
│   └── vite.config.ts
├── server/                # Express backend
│   ├── _core/index.ts     # Entry point
│   ├── firehose.ts        # Jetstream listener
│   ├── sentiment.ts       # VADER analysis
│   ├── db.ts              # Drizzle queries
│   ├── routers.ts         # tRPC API
│   └── socketio.ts        # Socket.IO setup
├── drizzle/               # Database
│   ├── schema.ts          # ORM schema
│   └── meta/              # Migrations
└── shared/                # Shared types
```

**Production Entry**: `start.sh`
**Dev Entry**: `pnpm dev` (concurrent frontend + backend)
**Production Port**: 5052
**Database**: `firehose.db` (SQLite)

---

#### Unified Client
```
/home/coolhand/html/bluesky/unified/
├── CLAUDE.md              # Excellent guide (760 lines)
├── README.md
├── pnpm-workspace.yaml    # Monorepo config
├── app/                   # React frontend
│   ├── src/
│   │   ├── pages/         # Route components (lazy-loaded)
│   │   │   ├── Home.tsx
│   │   │   ├── Thread.tsx
│   │   │   ├── Search.tsx
│   │   │   ├── Analytics.tsx      # Lazy
│   │   │   ├── Visualize.tsx      # Lazy
│   │   │   ├── Tools.tsx          # Lazy
│   │   │   ├── Compose.tsx
│   │   │   ├── Chat.tsx
│   │   │   └── Moderation.tsx     # Lazy
│   │   ├── components/    # Shared UI
│   │   │   ├── layout/Sidebar.tsx
│   │   │   ├── Thread.tsx
│   │   │   ├── Compose.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── hooks/
│   │   │   ├── useSocket.ts       # Socket.IO connection
│   │   │   └── useInfiniteScroll.ts
│   │   ├── router.tsx     # React Router setup
│   │   ├── lib/
│   │   │   ├── trpc.ts           # tRPC client
│   │   │   └── constants.ts
│   │   ├── index.css      # Tailwind (v4: @import "tailwindcss")
│   │   └── main.tsx       # React entry
│   ├── dist/              # Production build
│   └── vite.config.ts
├── packages/
│   ├── api-client/        # Bluesky API wrapper
│   ├── components/        # Shared UI components
│   ├── utils/             # TypeScript utilities
│   └── skymarshal/        # Imported from parent
├── server/                # Express backend
│   ├── src/app.ts         # Server entry
│   └── dist/              # Compiled server
├── tests/                 # Test suite
│   └── e2e/               # Playwright tests (37 tests, 505 LOC)
│       └── playwright.config.ts
└── node_modules/          # Dependencies
```

**Production Entry**: `pnpm dev` (frontend) + `pnpm dev` (backend in parallel)
**Frontend Port**: 5086 (Vite dev server)
**Backend Port**: 3001 (Express)
**Database**: None (queries via API)

---

#### Supporting Services (/html/bluesky/)

```
/home/coolhand/html/bluesky/
├── post-visualizer/          # Service 1 (detailed above)
├── firehose/                 # Frontend part of Service 2
├── unified/                  # Service 3 (detailed above)
├── cheatchat/                # Supporting service (5056)
│   ├── api.py               # Flask app
│   ├── index.html           # Frontend
│   └── requirements.txt
├── network/                 # Supporting (D3 chord)
│   ├── bluesky_follow_graph_jetstream.py
│   ├── fetch_top_accounts.py
│   ├── index.html
│   └── data/ (nodes.json, links.json)
├── repostdar/               # Supporting (self-repost)
│   ├── index.html
│   ├── style.css
│   └── app.js
├── chat/                    # DM integration
├── egonet-manager/          # Flask web app (5055)
│   └── app.py
├── blueflyer/               # PWA for posting
├── index.html               # Landing page
└── CLAUDE.md                # Bluesky suite guide
```

---

### Backend Services (/home/coolhand/servers/)

#### Skymarshal
```
/home/coolhand/servers/skymarshal/
├── CLAUDE.md                # Architecture guide (172 lines)
├── README.md                # User documentation
├── Makefile                 # Development commands
├── pyproject.toml           # Build config
├── requirements.txt         # Production deps
├── requirements-dev.txt     # Dev deps
├── skymarshal/              # Main package
│   ├── __main__.py          # Entry point
│   ├── app.py               # CLI controller (72 KB)
│   ├── models.py            # Data structures
│   ├── auth.py              # AT Protocol auth
│   ├── data_manager.py      # CAR/JSON ops (74 KB)
│   ├── search.py            # Filter engine (35 KB)
│   ├── deletion.py          # Safe deletion
│   ├── ui.py                # Rich terminal UI (40 KB)
│   └── web/                 # Flask interfaces
│       ├── lite_app.py      # Port 5050 (primary)
│       ├── app.py           # Port 5051 (extended)
│       └── templates/
│           ├── lite_dashboard.html
│           ├── hub.html
│           ├── dashboard.html
│           └── cleanup_*.html
├── loners/                  # Standalone scripts
│   ├── search.py
│   ├── stats.py
│   ├── delete.py
│   ├── nuke.py
│   ├── export.py
│   └── run.py
├── bluevibes/               # Profile viewer (subproject)
│   ├── app.py
│   ├── models.py
│   └── templates/
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

**CLI Entry**: `make run` or `python -m skymarshal`
**Web Lite Port**: 5050
**Web Full Port**: 5051

---

#### Corpus Firehose (Service 4)
```
/home/coolhand/servers/diachronica/corpus/bluesky_firehose/
├── ARCHITECTURE.md          # System design (273 lines)
├── DEPLOYMENT.md            # Deployment guide
├── CRITICAL_FIXES.md        # Known issues
├── CLEANUP_PLAN.md          # Data cleanup
├── app_corpus.py            # Main Flask app (~40 KB)
├── app.py                   # Alternative implementation (~45 KB)
├── requirements.txt         # Python dependencies
├── bsky_corpus.db           # SQLite (91MB main database)
├── bsky_posts.db            # SQLite (86KB active posts)
├── templates/
│   ├── index.html           # Dashboard
│   └── stats.html
├── static/
│   ├── css/
│   └── js/
├── monitoring/
│   ├── disk_monitor.service # systemd service
│   ├── disk_monitor.timer   # systemd timer
│   └── disk_monitor.log
└── venv/                    # Python virtual environment
    ├── bin/
    │   ├── python
    │   ├── pip
    │   └── gunicorn
    └── lib/
```

**Service Manager Entry**: `bluesky-corpus`
**Production Port**: 5074
**Gunicorn Command**:
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5074 app_corpus:app
```

---

#### Main Corpus API (Reference)
```
/home/coolhand/servers/diachronica/corpus/
├── README.md                # Core corpus API docs
├── app.py                   # Main Flask app
├── requirements.txt
├── run.py                   # Alternative entry
└── database/
    └── corpus.db            # 48M token corpus
```

---

### Service Manager Configuration
```
/home/coolhand/service_manager.py
├── Services configuration (dictionary)
├── Startup/shutdown procedures
├── Health check endpoints
├── Environment variables per service
└── Port allocation definitions
```

---

## CADDY ROUTING CONFIGURATION

**Configuration File**: `/etc/caddy/Caddyfile`

### Bluesky Suite Routes
```caddyfile
# Post Visualizer (path preserved via handle, not handle_path)
handle /bluesky/post-visualizer {
  redir https://{host}/bluesky/post-visualizer/?{query} permanent
}
handle /bluesky/post-visualizer/* {
  reverse_proxy localhost:5084
}

# Firehose
handle /bluesky/firehose {
  redir https://{host}/bluesky/firehose/ permanent
}
handle_path /bluesky/firehose/* {
  reverse_proxy localhost:5052
}

# Corpus Firehose
handle /bluesky/corpus {
  redir https://{host}/bluesky/corpus/ permanent
}
handle_path /bluesky/corpus/* {
  uri strip_prefix /bluesky/corpus
  reverse_proxy localhost:5074
}

# Unified Client (full path preservation for Vite base path)
handle /bluesky/unified {
  redir https://{host}/bluesky/unified/ permanent
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
  reverse_proxy localhost:3001
}
handle /bluesky/unified/* {
  reverse_proxy localhost:5086
}

# Skymarshal
handle /skymarshal/* {
  reverse_proxy localhost:5050
}
handle /skymarshal {
  reverse_proxy localhost:5050
}
```

---

## DATABASE LOCATIONS AND SIZES

| Service | Database | Location | Type | Size | Current |
|---------|----------|----------|------|------|---------|
| **Post Visualizer** | Shares | `data/shares.json` | File | Small | ~10KB |
| **Firehose** | Posts | `firehose.db` | SQLite | Medium | ~50-100MB |
| **Unified** | N/A | N/A | N/A | N/A | Queries API |
| **Corpus** | Posts | `bsky_corpus.db` | SQLite | Large | 91MB |
| **Corpus** | Active | `bsky_posts.db` | SQLite | Small | 86KB |
| **Skymarshal** | Backup | `~/.skymarshal/cars/` | CAR files | Variable | Per export |
| **Skymarshal** | Export | `~/.skymarshal/json/` | JSON files | Variable | Per export |

---

## ENVIRONMENT VARIABLES

### Service-Specific (.env files)

#### Post Visualizer
```bash
VITE_PORT=5084
EXPRESS_PORT=5084
NODE_ENV=production
```

#### Firehose
```bash
NODE_ENV=production
PORT=5052
OAUTH_SERVER_URL=          # Optional
JWT_SECRET=                # Session signing
DATABASE_URL=./firehose.db # SQLite path
```

#### Unified Client
```bash
BLUESKY_IDENTIFIER=your.handle.bsky.social  # Optional
BLUESKY_PASSWORD=your-app-password          # Optional
VITE_PORT=5086
EXPRESS_PORT=3001
VITE_SOCKET_URL=http://localhost:3001
NODE_ENV=production
```

#### Corpus Firehose
```bash
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5074
```

#### Skymarshal
```bash
PYTHONPATH=/home/coolhand/servers/skymarshal
BLUESKY_HANDLE=           # Optional
BLUESKY_PASSWORD=         # Optional
```

---

## QUICK START REFERENCE

### Start All Services (Production)
```bash
# Start each individually or via script
sm start skymarshal           # 5050 (first)
sm start bluesky-corpus       # 5074 (second)
sm start firehose             # 5052 (third)
sm start post-visualizer      # 5084 (fourth)
sm start unified-client       # 5086 + 3001 (last)

# Or use service manager batch
sm status  # View all
```

### Check All Health Endpoints
```bash
# Skymarshal
curl http://localhost:5050/

# Corpus Firehose
curl http://localhost:5074/api/health

# Firehose
curl http://localhost:5052/api/trpc/system.health

# Post Visualizer
curl http://localhost:5084/bluesky/post-visualizer/health

# Unified Backend
curl http://localhost:3001/health

# Unified Frontend
curl http://localhost:5086/

# Caddy (production URLs)
curl https://dr.eamer.dev/skymarshal/
curl https://dr.eamer.dev/bluesky/corpus/
curl https://dr.eamer.dev/bluesky/firehose/
curl https://dr.eamer.dev/bluesky/post-visualizer/
curl https://dr.eamer.dev/bluesky/unified/
```

---

## PORT CONFLICT TROUBLESHOOTING

### Find What's Using a Port
```bash
lsof -i :5050      # Check port 5050
lsof -i :5052      # Check port 5052
lsof -i :5084      # Check port 5084
lsof -i :5086      # Check port 5086
lsof -i :3001      # Check port 3001
```

### Kill Process on Port
```bash
# Get PID from lsof
kill -9 <PID>

# Or stop via service manager
sm stop <service>
```

### Verify Port Is Free
```bash
# Test connection
curl http://localhost:5050/ 2>&1 | head -1

# No connection means port is free
```

---

## DIRECTORY PERMISSION REQUIREMENTS

```bash
# Make data directories writable
chmod 755 /home/coolhand/html/bluesky/post-visualizer/data/
chmod 755 /home/coolhand/html/firehose/
chmod 755 /home/coolhand/servers/diachronica/corpus/bluesky_firehose/

# Database files should be readable by service users
chmod 644 *.db
```

---

## SYSTEMD SERVICES (Non-Service Manager)

### COCA (separate systemd service)
```bash
sudo systemctl start coca-api
sudo systemctl status coca-api
sudo systemctl restart coca-api
```

### Caddy (system-wide)
```bash
sudo systemctl start caddy
sudo systemctl reload caddy      # After config changes
sudo systemctl status caddy
sudo journalctl -u caddy -f      # View logs
```

---

## BACKUP LOCATIONS

### Critical Databases
```bash
# Backup Firehose
cp /home/coolhand/html/firehose/firehose.db /backup/firehose_$(date +%Y%m%d).db

# Backup Corpus
cp /home/coolhand/servers/diachronica/corpus/bluesky_firehose/bsky_corpus.db \
   /backup/bsky_corpus_$(date +%Y%m%d).db
```

---

## REFERENCE MATRIX

| Concern | Post Viz | Firehose | Unified | Corpus | Skymarshal |
|---------|----------|----------|---------|--------|-----------|
| **Port** | 5084 | 5052 | 5086+3001 | 5074 | 5050 |
| **Dir** | `/html/bluesky/post-visualizer/` | `/html/firehose/` | `/html/bluesky/unified/` | `/servers/diachronica/corpus/bluesky_firehose/` | `/servers/skymarshal/` |
| **Type** | React+Express | Node.js | React monorepo | Flask | Python CLI |
| **DB** | File (shares.json) | SQLite | N/A | SQLite (91MB) | CAR/JSON files |
| **URL** | `/bluesky/post-visualizer/` | `/bluesky/firehose/` | `/bluesky/unified/` | `/bluesky/corpus/` | `/skymarshal/` |
| **Health** | `/health` | `tRPC/health` | `/health` | `/api/health` | `/` |
| **Service** | `post-visualizer` | `firehose` | `unified-client` | `bluesky-corpus` | `skymarshal` |

---

**Last Updated**: 2026-01-18
**Next Review**: Post-Phase 2 documentation completion
