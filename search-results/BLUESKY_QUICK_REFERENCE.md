# Bluesky/AT Protocol Quick Reference

Fast lookup guide for Bluesky implementations across the codebase.

---

## Where to Find What

### Real-Time Data Ingestion
**Start Here**: `/home/coolhand/servers/firehose/server/firehose.ts` (494 lines)
- WebSocket: `wss://jetstream2.us-east.bsky.network/subscribe`
- Events: identity (handle cache) + commit (post create)
- Auto-reconnect: 5s exponential backoff
- Filters: corpus collection with 4-stage pipeline

### Sentiment & Content Analysis
**Start Here**: `/home/coolhand/servers/firehose/server/sentiment.ts` (135 lines)
- Algorithm: VADER (from `sentiment` npm package)
- Thresholds: >0.05 (pos), <-0.05 (neg), else neutral
- Features: hashtags, mentions, URLs, language, media type, word count
- Language: from record.langs array

### Real-Time Broadcast
**Start Here**: `/home/coolhand/servers/firehose/server/socketio.ts` (49 lines)
- Protocol: Socket.IO 4.x over WebSocket + polling fallback
- Events: `post` (new post) and `stats` (every 1s)
- Path: `/socket.io` (Caddy strips `/bluesky/firehose` prefix)

### Authentication
**Start Here**: `/home/coolhand/servers/firehose/server/_core/oauth.ts` (305 lines)
- Type: JWT-based session (not Bluesky credentials)
- Provider: Manus OAuth adapter
- Token: HS256 signature, 1-year expiry
- Session: HTTP-only cookies

### Graph Analysis
**Start Here**: `/home/coolhand/projects/blueballs/backend/app/analytics/graph_analysis.py` (80+ lines)
- Library: NetworkX
- Algorithms: PageRank, community detection, centrality
- Output: JSON-serializable with numpy → Python type conversion

### Bluesky HTTP Client
**Option 1**: `/home/coolhand/projects/blueballs/backend/app/services/bluesky_client.py`
- Rate limiter: 3000 points/hour (unauthenticated)
- Auth: JWT from `com.atproto.server.createSession`
- Async: httpx with asyncio

**Option 2**: `/home/coolhand/projects/bluevibes/src/bluesky_client.py`
- Similar pattern: identifier + app password auth
- Features: progress tracking, sentiment analysis, concurrent fetch

### Caching
**Primary**: `/home/coolhand/projects/blueballs/backend/app/services/cache_service.py`
- First: Redis async client (`redis.asyncio.Redis`)
- Fallback: Filesystem (`.cache/` directory)
- Serialization: orjson (fast binary JSON)

### React Hooks
**Location**: `/home/coolhand/servers/firehose/client/src/`
- `_core/hooks/useAuth.ts` - JWT session + logout
- `hooks/useSocket.ts` - Socket.IO connection + stats + posts
- `hooks/useComposition.ts` - Text input state
- `hooks/useMobile.tsx` - Responsive detection
- `hooks/usePersistFn.ts` - Stable function references

### Database Schema
**Location**: `/home/coolhand/servers/firehose/drizzle/schema.ts`
- Engine: SQLite with Drizzle ORM
- Tables: posts (main), 8 stats tables, sessions, users
- Migration: `pnpm db:push`

---

## Common Tasks

### Add a New tRPC Endpoint
1. Edit `/home/coolhand/servers/firehose/server/routers.ts`
2. Add to `appRouter` (see `firehose.stats` as example)
3. Define input with `z.object()` (Zod)
4. Query database via `db.ts` functions
5. Client: `trpc.firehose.newEndpoint.useQuery()`

### Extract a New Linguistic Feature
1. Edit `/home/coolhand/servers/firehose/server/sentiment.ts`
2. Add to `extractFeatures()` function
3. Return in features object (JSON.stringify lists)
4. Update database schema in `drizzle/schema.ts`
5. Run `pnpm db:push` to migrate

### Change Sentiment Thresholds
**File**: `/home/coolhand/servers/firehose/server/sentiment.ts:34-40`
```typescript
if (result.comparative > 0.05) {      // Change this threshold
  classification = 'positive';
} else if (result.comparative < -0.05) { // And this one
  classification = 'negative';
}
```

### Enable/Disable Corpus Collection
**Client**: Call tRPC endpoint
```bash
# Enable
curl -X POST https://dr.eamer.dev/bluesky/firehose/api/trpc/firehose.enableCollection \
  -H 'Content-Type: application/json' \
  -d '{"window":"08:00"}'

# Disable
curl -X POST https://dr.eamer.dev/bluesky/firehose/api/trpc/firehose.disableCollection
```

**Server**: Check `server/firehose.ts:142-155`

### Add a New Visualization Layout
1. Create new layout file in `/home/coolhand/projects/blueballs/frontend/`
2. Read JSON from `.cache/bluesky-network/` or fetch fresh
3. Implement force-directed or custom algorithm
4. Register in frontend router

### Query Network Analytics
1. Fetch graph via `/home/coolhand/projects/blueballs/backend/app/services/network_fetcher.py`
2. Run analysis via `backend/app/analytics/graph_analysis.py`
3. Return JSON via FastAPI endpoint
4. Render in one of 20 frontend visualizations

---

## API Methods Reference

### AT Protocol Calls (Used in Codebase)

#### Authentication
```
POST com.atproto.server.createSession
  {identifier, password} → {accessJwt, refreshJwt, did, handle, didDoc}
```

#### Graph Operations
```
GET app.bsky.graph.getFollows
  {actor, limit, cursor} → follower list

GET app.bsky.graph.getFollowers
  {actor, limit, cursor} → follower list

GET app.bsky.graph.getLists
  {actor, limit, cursor} → user lists
```

#### Actor/Profile
```
GET app.bsky.actor.getProfile
  {actor} → {displayName, description, followersCount, followsCount, postsCount}

GET app.bsky.actor.getProfiles
  {actors} → array of profiles
```

#### Feed
```
GET app.bsky.feed.getTimeline
  {algorithm, limit, cursor} → posts
```

#### Posts
```
GET app.bsky.feed.getPostThread
  {uri, depth} → post + replies

GET app.bsky.feed.getPosts
  {uris} → array of posts
```

### Not Yet Used (Available)
- `app.bsky.feed.searchPosts` - FTS search (needs Bluesky lab features)
- `app.bsky.feed.getAuthorFeed` - User posts
- `app.bsky.feed.getLikes` - Post likers
- `app.bsky.feed.getRepostedBy` - Repost authors
- `app.bsky.feed.getQuotes` - Quote posts
- `app.bsky.notification.listNotifications` - User notifications
- `app.bsky.richtext.facet` - Rich text facets (used in parsing, not fetching)

---

## Performance Metrics

### Firehose
- **Posts/Day**: ~5,000,000 (Bluesky average)
- **Memory**: Last 100 posts in memory
- **Database Writes**: Every 100 posts (batch update)
- **Socket.IO Broadcast**: Every 1 second (stats)
- **Reconnect**: 5 seconds after disconnect

### Sentiment Analysis
- **Speed**: <1ms per post (VADER)
- **Accuracy**: ~75% (VADER typical)
- **Thresholds**: Configurable (default ±0.05)

### Blueballs
- **Nodes Rendered**: 4,000-10,000 typical
- **FPS Target**: 60 (WebGL)
- **Rate Limit**: 3000/5000 points/hour
- **Cache Hit**: Avoids 100% API calls on repeat

### Bluevibes
- **Concurrent Followers**: 10-50 parallel (concurrent.futures)
- **Progress Updates**: Real-time UI updates
- **Batches**: Configurable batch size

---

## Configuration Variables

### Firehose (`.env`)
```bash
NODE_ENV=production              # production | development
PORT=5052                        # Server port
DATABASE_URL=./firehose.db       # SQLite path
OAUTH_SERVER_URL=                # Manus OAuth endpoint
JWT_SECRET=                      # Session signing key
```

### Blueballs (config.py)
```python
CACHE_DIR = ".cache/"            # Cache directory
REDIS_URL = None                 # Redis URL (optional)
RATE_LIMIT_POINTS = 3000         # Points per hour
RATE_LIMIT_WINDOW = 3600         # Seconds
```

### Bluevibes (config)
```python
BASE_URL = "https://bsky.social/xrpc"  # AT Protocol endpoint
TIMEOUT = 10.0                         # HTTP timeout
```

---

## Debugging Commands

### Check Firehose Status
```bash
# Service manager
sm status firehose              # Is it running?
sm logs firehose                # Recent logs
sm restart firehose             # Restart service

# Database
sqlite3 firehose.db ".schema"   # View schema
sqlite3 firehose.db "SELECT COUNT(*) FROM posts"  # Post count

# WebSocket
curl -i https://jetstream2.us-east.bsky.network/subscribe  # Endpoint alive?

# API
curl http://localhost:5052/     # Direct port
curl https://dr.eamer.dev/bluesky/firehose/  # Via Caddy
```

### Check Blueballs Status
```bash
# FastAPI docs
curl http://localhost:7058/docs  # Auto-generated endpoints

# Health
curl http://localhost:7058/health  # Status

# Cache
ls -la /home/coolhand/projects/blueballs/backend/.cache/  # Cached files
```

### Check Socket.IO Connection
1. Open browser DevTools → Network
2. Filter for "WS" (WebSocket)
3. Look for `socket.io` connection
4. Check Console for `[Socket.IO] Connected`
5. Watch for `stats` and `post` events in frame inspector

---

## Testing

### Test Sentiment Analysis
```bash
cd /home/coolhand/servers/firehose
pnpm test  # If vitest configured
# Manual test in node:
const {analyzeSentiment} = require('./server/sentiment.ts')
analyzeSentiment("I love this amazing post!")  // Should be positive
```

### Test Blueballs Graph
```bash
cd /home/coolhand/projects/blueballs/backend
pytest  # Run test suite
python -c "from app.analytics.graph_analysis import *"  # Import test
```

### Test Bluesky Client
```bash
cd /home/coolhand/projects/bluevibes
python -c "from src.bluesky_client import BlueskyClient; c = BlueskyClient()"
```

---

## Common Issues & Fixes

### "Firehose not connecting"
**Cause**: Jetstream endpoint blocked/down
**Fix**:
```bash
curl -v https://jetstream2.us-east.bsky.network/subscribe  # Test endpoint
sm logs firehose  # Check error message
sm restart firehose  # Restart service
```

### "Posts not saving to database"
**Cause**: Collection disabled or filters too strict
**Fix**:
```bash
# Enable collection
curl -X POST ... firehose.enableCollection

# Check filter stats in logs
sm logs firehose | grep "Filtering"

# Relax word count filter in sentiment.ts:308-314
```

### "Socket.IO connection failing"
**Cause**: Caddy routing issue or Socket.IO path mismatch
**Fix**:
```bash
# Verify Caddy routing
sudo caddy validate --config /etc/caddy/Caddyfile

# Check Socket.IO path in socketio.ts:11
# Should be: path: '/socket.io'

# Test direct port
curl http://localhost:5052/socket.io/
```

### "Database locked"
**Cause**: Multiple writers or WAL file issues
**Fix**:
```bash
# Check WAL mode
sqlite3 firehose.db "PRAGMA journal_mode;"  # Should be "wal"

# Force WAL mode
sqlite3 firehose.db "PRAGMA journal_mode=WAL;"

# Clear locks
rm firehose.db-wal firehose.db-shm
```

### "Rate limited on Bluesky"
**Cause**: Too many API calls
**Fix**:
```python
# In blueballs, increase wait time
# server/services/bluesky_client.py:91-96
# Increase RECONNECT_DELAY or implement backoff
```

---

## File Edit Checklist

Before editing key files, remember:

- [ ] **Sentiment thresholds** → `server/sentiment.ts:34-40`
- [ ] **Corpus filters** → `server/firehose.ts:280-323`
- [ ] **Database schema** → `drizzle/schema.ts` (then `pnpm db:push`)
- [ ] **Auth flows** → `server/_core/oauth.ts` (check JWT expiry)
- [ ] **Socket.IO path** → `server/socketio.ts:11` (Caddy coordination)
- [ ] **React hooks** → `client/src/_core/hooks/useAuth.ts` and `useSocket.ts`
- [ ] **Rate limits** → `bluesky_client.py:49-113`
- [ ] **Visualizations** → `blueballs/frontend/` (20 layout options)

---

## Key References

- **Bluesky AT Protocol Docs**: https://docs.bsky.app/
- **Jetstream Docs**: https://jetstream.atproto.tools/
- **VADER Sentiment**: https://github.com/nltk/nltk/blob/develop/nltk/sentiment/vader.py
- **NetworkX Docs**: https://networkx.org/documentation/
- **Drizzle ORM**: https://orm.drizzle.team/
- **tRPC**: https://trpc.io/

---

**End of Quick Reference**
