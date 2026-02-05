# Bluesky Suite Services - Quick Index

**Generated**: 2026-01-18
**Comprehensive Metadata**: `/home/coolhand/geepers/bluesky_suite_metadata.md`

---

## SERVICE QUICK REFERENCE

### 1. POST VISUALIZER
| Property | Value |
|----------|-------|
| **Location** | `/home/coolhand/html/bluesky/post-visualizer/` |
| **Port** | 5084 |
| **URL** | https://dr.eamer.dev/bluesky/post-visualizer/ |
| **Type** | React 19 + Express + D3.js |
| **Primary Purpose** | Force-directed graph visualization of Bluesky post interactions |
| **Key Feature** | Thread analysis (likes, reposts, replies, quotes) as interactive graph |
| **Data Source** | Bluesky AT Protocol API |
| **Caching** | LocalStorage (5-min fresh, 1-hour stale) |
| **Sharing** | Save graphs + OG images |
| **Start** | `sm start post-visualizer` |
| **Docs** | `post-visualizer/CLAUDE.md` (40 KB) |
| **Entry Point** | `server.js` (Express backend) |

**Key Endpoints**:
- `POST /bluesky/post-visualizer/api/share` - Save graph
- `GET /bluesky/post-visualizer/api/share/:id` - Retrieve
- `GET /bluesky/post-visualizer/health` - Health check

---

### 2. FIREHOSE
| Property | Value |
|----------|-------|
| **Location** | `/home/coolhand/html/firehose/` |
| **Port** | 5052 |
| **URL** | https://dr.eamer.dev/bluesky/firehose/ |
| **Type** | React 19 + Express + Socket.IO + tRPC |
| **Primary Purpose** | Real-time sentiment analytics dashboard |
| **Key Feature** | Live Bluesky firehose with VADER sentiment analysis |
| **Data Source** | Jetstream WebSocket (100-2,000 posts/sec) |
| **Database** | SQLite (firehose.db) via Drizzle ORM |
| **Persistence** | Posts table + hourly/daily stats tables |
| **Start** | `sm start firehose` |
| **Docs** | `CLAUDE.md` (298 lines), `API_REFERENCE.md` |
| **Entry Point** | `server/_core/index.ts` |

**Key Endpoints** (tRPC):
- `firehose.start()` / `firehose.stop()`
- `firehose.stats()` - Get aggregates
- `stats.global()` - Lifetime stats
- `stats.hourly(range)` - Time-series
- `posts.list(filters)` - Paginated posts

**Real-time Events** (Socket.IO):
- `post` - New post processed
- `stats` - Updated stats every 1s

---

### 3. UNIFIED CLIENT
| Property | Value |
|----------|-------|
| **Location** | `/home/coolhand/html/bluesky/unified/` |
| **Frontend Port** | 5086 |
| **Backend Port** | 3001 |
| **URL** | https://dr.eamer.dev/bluesky/unified/ |
| **Type** | React 19 monorepo (pnpm workspaces) + Express |
| **Primary Purpose** | Comprehensive Bluesky management interface |
| **Key Feature** | Unified dashboard (feed, search, analytics, tools) |
| **Data Source** | Bluesky API + Jetstream Socket.IO |
| **Real-time** | Socket.IO for home feed streaming |
| **Code-splitting** | Analytics, Visualize, DataManagement, Moderation (lazy) |
| **Start** | `sm start unified-client` (frontend) |
| **Docs** | `CLAUDE.md` (760 lines) - Excellent! |
| **Entry Point** | `app/src/router.tsx` |

**Routes** (with lazy loading):
- `/home` - Real-time feed
- `/thread/:uri` - Thread viewer
- `/search` - Content search
- `/analytics` - Stats dashboard (lazy)
- `/visualize` - D3.js graph (lazy)
- `/compose` - Post creation
- `/tools` - Integrated tools

**Performance**:
- Bundle: 307 KB (29% under target)
- Load time: 1.8s (10% under target)
- WCAG 2.1 AA compliant

---

### 4. CORPUS FIREHOSE
| Property | Value |
|----------|-------|
| **Location** | `/home/coolhand/servers/diachronica/corpus/bluesky_firehose/` |
| **Port** | 5074 |
| **URL** | https://dr.eamer.dev/bluesky/corpus/ |
| **Type** | Flask + Eventlet + VADER sentiment |
| **Primary Purpose** | Corpus linguistics analysis of Bluesky firehose |
| **Key Feature** | Sentiment analysis + persistence for linguistic research |
| **Data Source** | Jetstream WebSocket |
| **Database** | SQLite (91MB - bsky_corpus.db) |
| **NLP** | VADER sentiment scoring |
| **Monitoring** | Custom disk_monitor service |
| **Start** | `sm start bluesky-corpus` |
| **Docs** | `ARCHITECTURE.md` (273 lines) |
| **Entry Point** | `app_corpus.py` |

**Key Endpoints**:
- `GET /api/health` - Health check
- `GET /api/stats` - Aggregated stats
- `GET /api/stats/sentiment` - Distribution
- `GET /api/posts` - Recent posts

**Database Tables**:
- `posts` - Full post data
- `sentiment_stats` - Hourly aggregates
- `user_stats` - Per-author analysis

---

### 5. SKYMARSHAL
| Property | Value |
|----------|-------|
| **Location** | `/home/coolhand/servers/skymarshal/` |
| **Web Lite Port** | 5050 |
| **Web Full Port** | 5051 |
| **URL** | https://dr.eamer.dev/skymarshal/ |
| **Type** | Python CLI + Flask web interfaces |
| **Primary Purpose** | Bluesky content management & cleanup |
| **Key Feature** | Safe deletion with confirmations + analytics |
| **Data Source** | Bluesky AT Protocol |
| **Authentication** | Handle + password OR OAuth |
| **CAR Files** | Import/export account backups |
| **Start** | `sm start skymarshal` (lite) |
| **Docs** | `CLAUDE.md` (172 lines) |
| **Entry Point** | `skymarshal/web/lite_app.py` |

**CLI Interfaces**:
- `make run` - Interactive CLI menu
- `python -m skymarshal` - Direct module
- `loners/search.py` - Standalone search
- `loners/delete.py` - Safe deletion script

**Web Features** (Port 5050):
- Quick filters (bangers, dead threads, old posts)
- Real-time search
- Bulk delete with UI confirmation

**Data Operations**:
- Search & filter (keywords, date, engagement)
- Analytics (engagement scoring)
- Delete (with dry-run preview)
- Export (JSON/CSV)

---

## SUPPORTING SERVICES

| Service | Location | Port | Type | Purpose |
|---------|----------|------|------|---------|
| **CheatChat API** | `/bluesky/cheatchat/` | 5056 | Flask | Gemini API proxy |
| **Network Graph** | `/bluesky/network/` | N/A | D3.js + Python | Follow relationship chord |
| **Repostdar** | `/bluesky/repostdar/` | N/A | Static HTML | Self-repost detection |

---

## CROSS-SERVICE DATA FLOW

```
Jetstream WebSocket (wss://jetstream2.us-east.bsky.network)
    ↓
    ├─→ Firehose (5052) ─→ Socket.IO ─→ Unified Client home feed
    │
    ├─→ Corpus Firehose (5074) ─→ SQLite persistence ─→ Analytics
    │
    ├─→ Post Visualizer (5084) ─→ On-demand API calls ─→ Visualization
    │
    └─→ Unified Client (5086) ─→ Backend (3001) ─→ Aggregation + Tools
```

---

## DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All services have health endpoints configured
- [ ] Caddy routing rules validated: `sudo caddy validate --config /etc/caddy/Caddyfile`
- [ ] Environment variables set (API keys, secrets)
- [ ] Database backups created
- [ ] Service dependencies checked (Node.js, Python, Redis if needed)

### Startup Sequence
```bash
# 1. Start backend services first
sm start bluesky-corpus        # Corpus (5074)
sm start skymarshal            # Web lite (5050)

# 2. Start real-time services
sm start firehose              # Firehose (5052)

# 3. Start frontend services
sm start post-visualizer       # Post Viz (5084)
sm start unified-client        # Unified (5086 + 3001)

# 4. Verify Caddy
sudo systemctl reload caddy
```

### Health Checks
```bash
curl http://localhost:5050/        # Skymarshal
curl http://localhost:5052/api/trpc/system.health  # Firehose
curl http://localhost:5074/api/health  # Corpus
curl http://localhost:5084/bluesky/post-visualizer/health  # Post Viz
curl http://localhost:5086/        # Unified (frontend)
curl http://localhost:3001/health  # Unified (backend)
```

### Post-Deployment
- [ ] Test each service URL in browser
- [ ] Verify WebSocket connections (Socket.IO, Jetstream)
- [ ] Check database connectivity
- [ ] Monitor error logs: `tail -f /var/log/service_name.log`
- [ ] Verify SSL certificates (Caddy)

---

## COMMON OPERATIONS

### View All Service Status
```bash
sm status
```

### Check Specific Service Logs
```bash
sm logs firehose
sm logs unified-client
sm logs bluesky-corpus
```

### Restart Service After Changes
```bash
sm restart <service>
# Then verify: curl http://localhost:PORT/health
```

### Database Maintenance
```bash
# Firehose
sqlite3 /home/coolhand/html/firehose/firehose.db ".tables"
pnpm db:push  # Apply migrations

# Corpus
sqlite3 /home/coolhand/servers/diachronica/corpus/bluesky_firehose/bsky_corpus.db

# Caddy reload (after config changes)
sudo systemctl reload caddy
```

### Check Port Availability
```bash
lsof -i :5050  # Check port 5050
lsof -i :5052  # Check port 5052
```

---

## QUICK DEVELOPER REFERENCE

### File Structure Overview
```
/home/coolhand/
├── html/
│   ├── bluesky/                         # Web root
│   │   ├── post-visualizer/            # Service 1
│   │   ├── unified/                    # Service 3
│   │   ├── firehose/                   # Service 2
│   │   ├── cheatchat/                  # Supporting
│   │   ├── network/                    # Supporting
│   │   └── repostdar/                  # Supporting
│   └── ...
├── servers/
│   ├── skymarshal/                     # Service 5
│   ├── diachronica/
│   │   └── corpus/bluesky_firehose/    # Service 4
│   └── ...
└── geepers/
    ├── bluesky_suite_metadata.md       # Full reference
    └── bluesky_suite_index.md          # This file
```

### Technology Stack Summary
| Layer | Technologies |
|-------|---|
| **Frontend** | React 19, TypeScript 5.6, Tailwind 4, Vite 5 |
| **Backend** | Express, Flask, tRPC |
| **Real-time** | Socket.IO, Jetstream WebSocket |
| **Database** | SQLite (Drizzle ORM) |
| **NLP** | VADER sentiment |
| **Visualization** | D3.js v7, Recharts 3.6 |
| **Build** | pnpm workspaces, esbuild |
| **Testing** | Playwright E2E, Vitest (planned) |

---

## TROUBLESHOOTING QUICK GUIDE

### Firehose Not Receiving Posts
1. Check Jetstream connection: `wss://jetstream2.us-east.bsky.network` accessible?
2. Verify logs: `sm logs firehose | grep WebSocket`
3. Check database: `sqlite3 firehose.db "SELECT COUNT(*) FROM posts;"`

### Unified Client Socket.IO Issues
1. Verify backend running: `curl http://localhost:3001/health`
2. Check CORS: Look for errors in browser console
3. Restart backend: `sm restart unified-client`

### Corpus Firehose Database Growing Too Fast
1. Monitor disk: `du -sh /home/coolhand/servers/diachronica/corpus/`
2. Archive old posts: See `CLEANUP_PLAN.md`
3. Scale to PostgreSQL if >100M posts

### Caddy Routing Not Working
1. Validate config: `sudo caddy validate --config /etc/caddy/Caddyfile`
2. Check logs: `sudo journalctl -u caddy -f`
3. Test local port: `curl http://localhost:5052/` vs `curl https://dr.eamer.dev/bluesky/firehose/`

### Post Visualizer Touch Issues (Mobile)
- Check CSS: `touch-action: none` in App.css
- Test in browser DevTools with mobile emulation
- Verify D3 drag handlers calling preventDefault()

---

## KEY METRICS

### Current Performance
| Service | Metric | Value | Target | Status |
|---------|--------|-------|--------|--------|
| Unified | Bundle Size | 307 KB | < 430 KB | ✅ 29% under |
| Unified | Load Time | 1.8s | < 2s | ✅ 10% under |
| Firehose | Posts/sec | 100-2000 | No limit | ✅ Full capacity |
| Firehose | Latency | <100ms | <1s | ✅ Sub-second |
| Corpus | DB Size | 91MB | N/A | ⚠️ Monitor |
| Post Viz | A11y Score | 97/100 | 95+ | ✅ Exceeds |

### Accessibility Compliance
- ✅ WCAG 2.1 Level AA (Unified Client)
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Color contrast (4.5:1 minimum)
- ✅ ARIA labels on interactive elements

---

## RELATED DOCUMENTATION

**Full Reference**: `/home/coolhand/geepers/bluesky_suite_metadata.md` (comprehensive, 600+ lines)

**Individual Service Docs**:
- Post Visualizer: `/home/coolhand/html/bluesky/post-visualizer/CLAUDE.md`
- Firehose: `/home/coolhand/html/firehose/CLAUDE.md`
- Unified: `/home/coolhand/html/bluesky/unified/CLAUDE.md`
- Corpus: `/home/coolhand/servers/diachronica/corpus/bluesky_firehose/ARCHITECTURE.md`
- Skymarshal: `/home/coolhand/servers/skymarshal/CLAUDE.md`

**System Docs**:
- Main CLAUDE.md: `/home/coolhand/CLAUDE.md`
- Server CLAUDE.md: `/home/coolhand/servers/CLAUDE.md`
- Bluesky CLAUDE.md: `/home/coolhand/html/bluesky/CLAUDE.md`

---

## NEXT STEPS (PHASE 2)

1. **Consolidate API Reference** - All endpoints in one document
2. **Create Visual Diagrams** - Architecture, data flow, deployment topology
3. **Build Deployment Guide** - Step-by-step production rollout
4. **Develop Monitoring Strategy** - Health checks, alerts, metrics
5. **Write Operational Runbook** - Day-to-day procedures
6. **Establish SLA Targets** - Uptime, response time, reliability
7. **Create Migration Guide** - Scaling beyond single-server setup

---

**Last Updated**: 2026-01-18
**Status**: Metadata collection complete, ready for Phase 2 documentation generation
