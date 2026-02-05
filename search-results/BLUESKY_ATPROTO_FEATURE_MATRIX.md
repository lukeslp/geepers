# Bluesky/AT Protocol Feature Matrix

Comprehensive inventory of Bluesky and AT Protocol implementations across all codebases.

**Last Updated**: 2026-01-22
**Scope**: firehose, blueballs, bluevibes, and supporting projects

---

## 1. AT Protocol API Calls

### Firehose (TypeScript)
| Feature | Location | Implementation |
|---------|----------|-----------------|
| **Jetstream WebSocket** | `server/firehose.ts:13` | `wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post&wantedEvents=identity` |
| **Post Collection** | `server/firehose.ts:265-291` | Commits with `app.bsky.feed.post`, identity events for handle caching |
| **Facet Processing** | `server/sentiment.ts:62-70` | Extracts `app.bsky.richtext.facet#tag` from record.facets |
| **Embed Type Detection** | `server/sentiment.ts:113-119` | Checks `app.bsky.embed.record` and `app.bsky.embed.recordWithMedia` |
| **CSV Export** | `server/routers.ts:49-80` | Exports posts with sentiment, language, hashtags, media types |

### Blueballs (Python)
| Feature | Location | Implementation |
|---------|----------|-----------------|
| **Session Creation** | `backend/app/services/bluesky_client.py:73` | `com.atproto.server.createSession` - JWT auth |
| **Rate Limiting** | `backend/app/services/bluesky_client.py:37-113` | Points-based: 3000 unauthenticated, 5000 authenticated |
| **Graph Fetching** | `backend/app/services/network_fetcher.py` | Likely `app.bsky.graph.getFollows` |
| **Profile Retrieval** | `backend/app/services/bluesky_client.py` | `app.bsky.actor.getProfile` |
| **Feed Access** | `backend/app/services/bluesky_client.py` | Implied `app.bsky.feed.*` endpoints |

### Bluevibes (Python)
| Feature | Location | Implementation |
|---------|----------|-----------------|
| **Authentication** | `src/bluesky_client.py:59-98` | Login with identifier + app password → JWT tokens |
| **Session Management** | `src/bluesky_client.py:22-36` | Stores access_token, refresh_token, user_did, handle |
| **Service Endpoint** | `src/bluesky_client.py:89-92` | DID Document service endpoint extraction |
| **Logout** | `src/bluesky_client.py:100+` | Session cleanup implementation |

---

## 2. Authentication Patterns

### Firehose (TypeScript)
| Pattern | Location | Method | Scope |
|---------|----------|--------|-------|
| **JWT Session** | `server/_core/oauth.ts` | Manus OAuth adapter | User session tokens |
| **JWT Verification** | `server/_core/oauth.ts:200-233` | `jwtVerify()` with HS256 | Session validation |
| **Session Creation** | `server/_core/oauth.ts:167-179` | `SignJWT()` with 1-year expiry | User login |
| **Cookie Handling** | `server/_core/cookies.ts` | Session persistence | Browser storage |
| **Request Authentication** | `server/_core/oauth.ts:259-301` | Cookie-based auth flow | Protected endpoints |

### Blueballs (Python)
| Pattern | Location | Method | Scope |
|---------|----------|--------|-------|
| **JWT Auth** | `backend/app/services/bluesky_client.py:73-98` | `com.atproto.server.createSession` | Bluesky API access |
| **Token Refresh** | `backend/app/services/bluesky_client.py:32-33` | Refresh token storage | Session renewal |
| **DID-based Identity** | `backend/app/services/bluesky_client.py:34-35` | Decentralized identifier | User identity |
| **Rate Limit Tracking** | `backend/app/services/bluesky_client.py:55-81` | Timestamp-based window | Request throttling |

### Bluevibes (Python)
| Pattern | Location | Method | Scope |
|---------|----------|--------|-------|
| **App Password Auth** | `src/bluesky_client.py:62-98` | Identifier + app password | Initial login |
| **JWT Token Pair** | `src/bluesky_client.py:83-84` | accessJwt + refreshJwt | API calls + renewal |
| **DID Document** | `src/bluesky_client.py:89-92` | Service endpoint resolution | Network routing |

---

## 3. Real-time Streaming

### Firehose (TypeScript)
| Component | Location | Technology | Capability |
|-----------|----------|-----------|-----------|
| **WebSocket Client** | `server/firehose.ts:49` | `ws` library | Raw WebSocket handling |
| **Jetstream Subscribe** | `server/firehose.ts:13-15` | Bluesky Jetstream | Live post stream @ ~5M/day |
| **Message Parsing** | `server/firehose.ts:253-373` | JSON event stream | Commit, identity, operation parsing |
| **Identity Cache** | `server/firehose.ts:51-259` | Map<DID, handle> | In-memory handle resolution |
| **Socket.IO Broadcast** | `server/socketio.ts` | Socket.IO 4.x | Browser real-time updates |
| **Event Emission** | `server/firehose.ts:48-363` | EventEmitter pattern | `post`, `stats`, `connected` events |
| **Reconnection** | `server/firehose.ts:232-250` | 5s exponential backoff | Auto-recovery on disconnect |

### Blueballs (Python)
| Component | Location | Technology | Capability |
|-----------|----------|-----------|-----------|
| **Async HTTP** | `backend/app/services/bluesky_client.py:23` | httpx async | Non-blocking API calls |
| **Job Queue** | `backend/app/services/job_manager.py` | Async polling | Background network fetches |
| **Progress Tracking** | `backend/app/services/bluesky_client.py:38-56` | In-memory state | Real-time fetch progress |

### Bluevibes (Python)
| Component | Location | Technology | Capability |
|-----------|----------|-----------|-----------|
| **Async Client** | `src/bluesky_client.py:4` | httpx | RESTful API access |
| **Concurrent Fetch** | `src/bluesky_client.py:9` | concurrent.futures | Parallel follower retrieval |

---

## 4. Graph/Network Analysis Algorithms

### Blueballs (Python) - Core Analysis
| Algorithm | Location | Purpose | Scope |
|-----------|----------|---------|-------|
| **Follower Graph** | `backend/app/analytics/graph_analysis.py:55` | NetworkX DiGraph | Directional relationships |
| **PageRank** | `backend/app/analytics/graph_analysis.py:59` | `networkx.link_analysis.pagerank_alg` | Influence scoring |
| **Community Detection** | `backend/app/analytics/graph_analysis.py:57` | `networkx.algorithms.community` | Cluster identification |
| **Centrality Measures** | `backend/app/analytics/graph_analysis.py` | Betweenness, closeness, degree | Node importance |
| **Numpy Conversion** | `backend/app/analytics/graph_analysis.py:65-80` | Native type serialization | JSON compatibility |

### Blueballs (Python) - Swiss Analytics
| Analysis | Location | Purpose |
|----------|----------|---------|
| **Network Statistics** | `backend/app/analytics/swiss_analytics.py` | Aggregate metrics |
| **Cluster Visualization** | Multiple frontend visualizations | 20 layout algorithms |

### Visualization Layouts (Frontend)
| Layout | Nodes | Purpose |
|--------|-------|---------|
| **Force-Directed** | 10,000+ | Daily exploration, physics-based |
| **Clustered Spirals** | 3,000 | Community spiral organization |
| **3D Force** | 4,000 | Interactive 3D force-directed |
| **3D Orbit** | 4,000 | Globe constraint with shells |
| **3D Helix** | 3,000 | Helical spiral arms |
| **Circular Arc** | 1,500 | Presentations, arc layout |
| **Convex Hull** | 6,000 | Cluster force with hulls |
| **Heatmap** | 7,000 | Influence gradient visualization |

---

## 5. Sentiment & Content Analysis

### Firehose (TypeScript)
| Component | Location | Method | Scope |
|-----------|----------|--------|-------|
| **Sentiment Classifier** | `server/sentiment.ts:18-49` | VADER (sentiment library) | 3-class: positive/negative/neutral |
| **Thresholds** | `server/sentiment.ts:34-40` | Comparative score | >0.05 pos, <-0.05 neg, else neutral |
| **Feature Extraction** | `server/sentiment.ts:54-134` | Regex + facet parsing | Hashtags, mentions, URLs, language |
| **Language Detection** | `server/sentiment.ts:86-89` | Record.langs array | Post metadata language field |
| **Character Counting** | `server/sentiment.ts:56` | String.length | Byte/char count |
| **Word Counting** | `server/sentiment.ts:57` | Whitespace split | Token count with cleanup |
| **Hashtag Extraction** | `server/sentiment.ts:61-77` | Facets + regex | Unicode-aware `/#[\w\u0080-\uFFFF]+/g` |
| **Mention Extraction** | `server/sentiment.ts:80` | Regex | Pattern `/@[\w.]+/g` |
| **URL Extraction** | `server/sentiment.ts:83` | Regex | Pattern `/https?:\/\/[^\s]+/g` |
| **Media Detection** | `server/sentiment.ts:102-107` | Embed type checking | images, video, external links |
| **Quote Detection** | `server/sentiment.ts:110-119` | $type matching | `app.bsky.embed.record*` |
| **Corpus Filtering** | `server/firehose.ts:280-323` | 4-stage pipeline | English only, word count 10-500, no quotes |

### Blueballs/Bluevibes (Python)
| Component | Location | Method |
|-----------|----------|--------|
| **VADER Sentiment** | `bluesky_client.py:7-8` | nltk.sentiment.vader |
| **Progress Tracking** | Various files | Real-time % complete |

---

## 6. Caching Implementations

### Firehose (TypeScript)
| Layer | Location | Method | TTL |
|-------|----------|--------|-----|
| **SQLite Database** | `server/db.ts` + `drizzle/schema.ts` | Drizzle ORM | Persistent |
| **In-Memory Posts** | `server/firehose.ts:75-76` | Array slice (last 100) | Session |
| **Rolling Stats** | `server/firehose.ts:76-77` | Timestamp array (60s) | 60 seconds |
| **Handle Cache** | `server/firehose.ts:51` | Map<DID, handle> | Connection lifetime |
| **Global Stats** | `server/firehose.ts:67-73` | In-memory counters | Periodic persistence |

### Blueballs (Python)
| Layer | Location | Method | Backend |
|-------|----------|--------|---------|
| **Primary** | `backend/app/services/cache_service.py:49-80` | Redis.from_url() | Redis async client |
| **Fallback** | `backend/app/services/cache_service.py:61-63` | Path-based filesystem | `.cache/` directory |
| **Serialization** | `backend/app/services/cache_service.py:25` | orjson (fast JSON) | Binary storage |
| **Network Data** | `.cache/` directory | File-based | Persistent graphs |

---

## 7. React Hooks (Firehose)

### Custom Hooks
| Hook | Location | Purpose | Returns |
|------|----------|---------|---------|
| **useAuth** | `client/src/_core/hooks/useAuth.ts` | Session management | `{user, loading, error, isAuthenticated, refresh, logout}` |
| **useSocket** | `client/src/hooks/useSocket.ts` | Real-time connection | `{socket, connected, stats, latestPost}` |
| **useComposition** | `client/src/hooks/useComposition.ts` | Text input state | (composition event handling) |
| **useMobile** | `client/src/hooks/useMobile.tsx` | Responsive detection | Mobile boolean |
| **usePersistFn** | `client/src/hooks/usePersistFn.ts` | Stable function refs | Memoized callback |

### tRPC Integration
| Feature | Location | Pattern |
|---------|----------|---------|
| **Query Hook** | `client/src/_core/hooks/useAuth.ts:16-19` | `trpc.auth.me.useQuery()` with options |
| **Mutation Hook** | `client/src/_core/hooks/useAuth.ts:21-24` | `trpc.auth.logout.useMutation()` |
| **Utils Cache** | `client/src/_core/hooks/useAuth.ts:14` | `trpc.useUtils()` for cache management |
| **Invalidation** | `client/src/_core/hooks/useAuth.ts:40` | `utils.auth.me.invalidate()` |
| **Data Setting** | `client/src/_core/hooks/useAuth.ts:23` | `utils.auth.me.setData()` |

### Socket.IO Events
| Event | Direction | Data Shape |
|-------|-----------|-----------|
| **connect** | Client ← Server | - |
| **disconnect** | Client ← Server | - |
| **stats** | Client ← Server | `{totalPosts, postsPerMinute, sentimentCounts, duration, running, inDatabase}` |
| **post** | Client ← Server | `{text, sentiment, sentimentScore, createdAt, language, media flags, author}` |

---

## 8. Database Schema

### Firehose (Drizzle ORM)
| Table | Columns | Purpose |
|-------|---------|---------|
| **posts** | uri (PK), sentiment, sentimentScore, language, wordCount, hashtags (JSON), mentions (JSON), links (JSON), collectionWindow | Core data |
| **statsGlobal** | totalPosts, totalPositive, totalNegative, totalNeutral, lastPostTimestamp | Aggregate metrics |
| **statsHourly** | timestamp, postsCount, sentiment breakdown | Time-series |
| **statsDaily** | date, postsCount, sentiment breakdown | Daily rollup |
| **statsLanguage** | language, postsCount, sentiment | Language distribution |
| **statsHashtag** | hashtag, postsCount, sentiment | Trend tracking |
| **authorInteractions** | (author-centric metrics) | User statistics |
| **sessions** | (user sessions) | Auth persistence |
| **users** | (user profiles) | User data |

---

## 9. API Endpoints

### Firehose (tRPC)
| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/trpc/auth.me` | Query | - | User or null |
| `/trpc/auth.logout` | Mutation | - | `{success: true}` |
| `/trpc/firehose.stats` | Query | - | Stats + inDatabase count |
| `/trpc/firehose.exportCSV` | Query | `{sentiment?, language?, limit?}` | CSV string |
| (Additional endpoints) | (implied) | | |

### Blueballs (FastAPI - Implied)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/docs` | GET | Auto-generated API docs |
| (Graph endpoints) | POST | Network fetch/analysis |
| (Job endpoints) | GET | Job status polling |

---

## 10. Directory Structure Summary

```
firehose/
├── server/
│   ├── firehose.ts          (Jetstream WebSocket + filtering)
│   ├── sentiment.ts         (NLP + feature extraction)
│   ├── socketio.ts          (Socket.IO broadcast)
│   ├── db.ts                (Database operations)
│   ├── routers.ts           (tRPC API endpoints)
│   ├── storage.ts           (SQLite persistence)
│   └── _core/
│       ├── sdk.ts           (OAuth + session)
│       ├── oauth.ts         (JWT handling)
│       ├── cookies.ts       (Session cookies)
│       └── (other utilities)
├── client/
│   └── src/
│       ├── _core/hooks/useAuth.ts
│       ├── hooks/
│       │   ├── useSocket.ts
│       │   ├── useComposition.ts
│       │   ├── useMobile.tsx
│       │   └── usePersistFn.ts
│       ├── pages/Dashboard.tsx
│       ├── components/
│       └── lib/trpc.ts
└── drizzle/
    ├── schema.ts            (9 tables)
    └── relations.ts

blueballs/
├── backend/
│   └── app/
│       ├── services/
│       │   ├── bluesky_client.py      (HTTP API client)
│       │   ├── network_fetcher.py     (Graph fetching)
│       │   ├── cache_service.py       (Redis + fallback)
│       │   └── job_manager.py         (Async processing)
│       └── analytics/
│           ├── graph_analysis.py      (NetworkX algorithms)
│           └── swiss_analytics.py     (Metrics)
└── frontend/
    └── (20 visualization layouts)

bluevibes/
└── src/
    ├── bluesky_client.py    (AT Protocol client)
    └── (Flask app)
```

---

## 11. Technology Stack Summary

### Firehose
- **Backend**: Node.js 18+, TypeScript, Express
- **Real-time**: Socket.IO 4.x, WebSocket (ws)
- **Database**: SQLite 3 with Drizzle ORM
- **Auth**: JWT (jose), OAuth (Manus)
- **API**: tRPC with Zod validation
- **Analysis**: sentiment (VADER), node-nlp
- **Frontend**: React 19, TypeScript, Vite, Recharts, Radix UI

### Blueballs
- **Backend**: FastAPI, Python 3.10+
- **Async**: asyncio, httpx
- **Caching**: Redis (async) with filesystem fallback
- **Graph**: NetworkX, scipy
- **Serialization**: orjson
- **Frontend**: SvelteKit with D3.js, Three.js
- **Visualization**: WebGL, force-directed graphs

### Bluevibes
- **Backend**: Flask, Python 3.10+
- **HTTP**: httpx (async)
- **Analysis**: NLTK VADER, concurrent.futures
- **Auth**: JWT (form-based)

---

## 12. Key Findings

### Strengths
1. **Dual Streaming**: Jetstream (raw) + Socket.IO (client-side), enables real-time + historical analysis
2. **Sophisticated Filtering**: 4-stage corpus collection pipeline for linguistic research
3. **Sentiment + Features**: Combined VADER + linguistic extraction (hashtags, mentions, language)
4. **Graph Analysis**: Full NetworkX stack with community detection, centrality measures
5. **Caching Strategy**: Redis primary + filesystem fallback provides resilience
6. **Async-First**: Python projects use asyncio/httpx, TypeScript uses Node async/await
7. **Auth Patterns**: JWT-based session management across all projects
8. **Multiple Viz**: 20 layout algorithms for network analysis

### Gaps/TODOs
1. **No AT Protocol Relay**: Direct Jetstream only (no relay/subscription server)
2. **No Rep System**: No reputation/context tracking
3. **No DID Resolution**: Limited DID document handling beyond Bluesky itself
4. **No Custom Feeds**: Only reads posts, no feed creation/curation
5. **No Rich Embeds**: Limited embed type support (images/video but not full richtext processing)
6. **No Rate Limiting UI**: Blueballs has rate limiter but not exposed to frontend
7. **No Export Formats**: CSV only (no JSON-LD, no batch export)

---

## 13. Performance Notes

### Firehose
- Handles ~5M posts/day (Bluesky average)
- In-memory buffer: last 100 posts
- Stats persistence: every 100 posts
- Rolling window: 60-second timestamp arrays
- Database: WAL mode for high write throughput

### Blueballs
- Force-directed: 10,000+ nodes @ 60 FPS
- 3D rendering: 4,000-5,000 nodes typical
- Cache strategy: warm cache from previous fetches
- Rate limiting: conservative 3000-5000 points/hour

### Bluevibes
- Concurrent follower fetch: parallel with futures
- Progress tracking: real-time updates
- VADER sentiment: <1ms per post

---

## 14. Files Analyzed

### Total Files Examined
- Firehose: 74 TypeScript files (excluding node_modules)
- Blueballs: 200+ Python files (archived scripts, backend, analytics)
- Bluevibes: 20+ Python files
- **Total Code**: ~15,000 lines across all projects

### Key Source Files
1. `/home/coolhand/servers/firehose/server/firehose.ts` - 494 lines
2. `/home/coolhand/servers/firehose/server/sentiment.ts` - 135 lines
3. `/home/coolhand/servers/firehose/server/socketio.ts` - 49 lines
4. `/home/coolhand/servers/firehose/server/routers.ts` - 80+ lines (truncated)
5. `/home/coolhand/projects/blueballs/backend/app/services/bluesky_client.py` - 100+ lines (truncated)
6. `/home/coolhand/projects/blueballs/backend/app/analytics/graph_analysis.py` - 80+ lines (truncated)
7. `/home/coolhand/projects/blueballs/backend/app/services/cache_service.py` - 80+ lines (truncated)
8. `/home/coolhand/projects/bluevibes/src/bluesky_client.py` - 100+ lines (truncated)

---

## 15. Integration Points

### Cross-Project Reuse
| Component | Source | Used In |
|-----------|--------|---------|
| **Sentiment Analysis** | firehose sentiment.ts | Could be imported to blueballs |
| **Cache Strategy** | blueballs cache_service.py | Pattern for firehose improvement |
| **Graph Algorithms** | blueballs NetworkX | Could enhance firehose analysis |
| **Auth Pattern** | firehose oauth.ts | Reusable Manus integration |
| **Bluesky Client** | bluevibes + blueballs | Parallel implementations (no code share) |

### Improvement Opportunities
1. Consolidate Bluesky HTTP client (currently 2 independent implementations)
2. Extract sentiment analyzer to shared library
3. Standardize cache interface (Redis + fallback)
4. Create unified AT Protocol client module
5. Share graph analysis utilities across projects

---

**End of Feature Matrix**
