# Bluesky/AT Protocol - Code Patterns & Snippets

Reusable code patterns from across the Bluesky implementations.

---

## 1. WebSocket Streaming (Firehose Pattern)

### Raw WebSocket Connection with Reconnect
**Source**: `/home/coolhand/servers/firehose/server/firehose.ts:210-251`

```typescript
import WebSocket from 'ws';
import { EventEmitter } from 'events';

const FIREHOSE_URI = 'wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post&wantedEvents=identity';
const RECONNECT_DELAY = 5000;

export class FirehoseService extends EventEmitter {
  private ws: WebSocket | null = null;
  private running = false;
  private reconnectTimer: NodeJS.Timeout | null = null;

  private connect() {
    if (!this.running) return;

    try {
      this.ws = new WebSocket(FIREHOSE_URI);

      this.ws.on('open', () => {
        console.log('[Firehose] Connected to Bluesky firehose');
        this.emit('connected');
      });

      this.ws.on('message', (data: Buffer) => {
        this.handleMessage(data);
      });

      this.ws.on('error', (error) => {
        console.error('[Firehose] WebSocket error:', error.message);
        this.emit('error', error);
      });

      this.ws.on('close', () => {
        console.log('[Firehose] Connection closed');
        this.ws = null;

        if (this.running) {
          console.log(`[Firehose] Reconnecting in ${RECONNECT_DELAY / 1000}s...`);
          this.reconnectTimer = setTimeout(() => {
            this.connect();
          }, RECONNECT_DELAY);
        }
      });
    } catch (error) {
      console.error('[Firehose] Connection error:', error);
      if (this.running) {
        this.reconnectTimer = setTimeout(() => {
          this.connect();
        }, RECONNECT_DELAY);
      }
    }
  }

  public start() {
    if (this.running) {
      console.log('[Firehose] Already running');
      return;
    }
    this.running = true;
    this.connect();
  }

  public stop() {
    this.running = false;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }
  }
}
```

---

## 2. Message Parsing (Jetstream Events)

### Parse Identity & Commit Events
**Source**: `/home/coolhand/servers/firehose/server/firehose.ts:253-373`

```typescript
private handleMessage(data: Buffer) {
  try {
    const message = JSON.parse(data.toString());

    // Handle identity events to build handle cache
    if (message.kind === 'identity' && message.identity?.handle) {
      this.handleCache.set(message.identity.did, message.identity.handle);
      console.log(`[Firehose] Cached handle: ${message.identity.handle} for DID: ${message.identity.did}`);
      return;
    }

    // Only process post commits
    if (message.kind !== 'commit' || message.commit?.operation !== 'create') {
      return;
    }

    const record = message.commit?.record;
    if (!record || !record.text) {
      return;
    }

    // Truncate long text
    let text = record.text;
    if (text.length > MAX_TEXT_LENGTH) {
      text = text.substring(0, MAX_TEXT_LENGTH);
    }

    // Extract author info
    const authorDid = message.did || '';
    const authorHandle = this.handleCache.get(authorDid) || authorDid;

    const post: FirehosePost = {
      text,
      uri: message.commit.uri || '',
      cid: message.commit.cid || '',
      author: {
        did: authorDid,
        handle: authorHandle,
      },
      createdAt: record.createdAt || new Date().toISOString(),
      sentiment: 'neutral',  // Will be analyzed
      sentimentScore: 0,
      language: record.langs?.[0],
      hasImages: record.embed?.$type?.includes('images'),
      hasVideo: record.embed?.$type?.includes('video'),
      hasLink: !!record.embed?.external || !!record.facets?.some(f => f.features?.some(feat => feat.$type === 'app.bsky.richtext.facet#link')),
      isReply: !!record.reply,
      isQuote: !!record.embed?.record,
    };

    this.emit('post', post);
  } catch (error) {
    console.error('[Firehose] Error processing message:', error);
  }
}
```

---

## 3. Sentiment Analysis (VADER Pattern)

### Extract Sentiment + Linguistic Features
**Source**: `/home/coolhand/servers/firehose/server/sentiment.ts`

```typescript
import Sentiment from 'sentiment';

const sentiment = new Sentiment();

export interface SentimentResult {
  score: number;
  comparative: number;
  classification: 'positive' | 'negative' | 'neutral';
  positive: string[];
  negative: string[];
}

export function analyzeSentiment(text: string): SentimentResult {
  if (!text || text.trim().length === 0) {
    return {
      score: 0,
      comparative: 0,
      classification: 'neutral',
      positive: [],
      negative: [],
    };
  }

  const result = sentiment.analyze(text);

  // Classify based on comparative score (normalized by word count)
  let classification: 'positive' | 'negative' | 'neutral';

  if (result.comparative > 0.05) {
    classification = 'positive';
  } else if (result.comparative < -0.05) {
    classification = 'negative';
  } else {
    classification = 'neutral';
  }

  return {
    score: result.score,
    comparative: result.comparative,
    classification,
    positive: result.positive,
    negative: result.negative,
  };
}

export function extractFeatures(text: string, record?: any) {
  // Character and word count
  const charCount = text.length;
  const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;

  // Extract hashtags - support Unicode characters
  let hashtags: string[] = [];
  if (record?.facets) {
    for (const facet of record.facets) {
      for (const feature of facet.features || []) {
        if (feature.$type === 'app.bsky.richtext.facet#tag') {
          hashtags.push(`#${feature.tag}`);
        }
      }
    }
  }

  // Fallback to regex
  if (hashtags.length === 0) {
    const hashtagMatches = text.match(/#[\w\u0080-\uFFFF]+/g) || [];
    hashtags = hashtagMatches;
  }

  // Extract mentions
  const mentions = text.match(/@[\w.]+/g) || [];

  // Extract URLs
  const urls = text.match(/https?:\/\/[^\s]+/g) || [];

  // Detect language
  let language = 'unknown';
  if (record?.langs && Array.isArray(record.langs) && record.langs.length > 0) {
    language = record.langs[0];
  }

  // Check for media and embeds
  const embed = record?.embed || {};
  const embedType = embed.$type || '';
  const hasImages = embedType.includes('images');
  const hasVideo = embedType.includes('video');
  const hasLink = embedType.includes('external') || urls.length > 0;

  // Quote posts
  let isQuote = false;
  let quoteUri = null;
  if (embedType === 'app.bsky.embed.record') {
    isQuote = true;
    quoteUri = embed.record?.uri;
  } else if (embedType === 'app.bsky.embed.recordWithMedia') {
    isQuote = true;
    quoteUri = embed.record?.record?.uri;
  }

  return {
    charCount,
    wordCount,
    hashtags: JSON.stringify(hashtags),
    mentions: JSON.stringify(mentions),
    links: JSON.stringify(urls),
    language,
    hasImages,
    hasVideo,
    hasLink,
    isQuote,
    quoteUri,
  };
}
```

---

## 4. Socket.IO Real-Time Broadcast

### Server-Side Setup
**Source**: `/home/coolhand/servers/firehose/server/socketio.ts`

```typescript
import { Server as SocketIOServer } from 'socket.io';
import { Server as HTTPServer } from 'http';
import { getFirehoseService } from './firehose';

export function setupSocketIO(httpServer: HTTPServer) {
  const io = new SocketIOServer(httpServer, {
    cors: {
      origin: "*",
      methods: ["GET", "POST"]
    },
    path: '/socket.io'  // Caddy handle_path strips /bluesky/firehose prefix
  });

  const firehose = getFirehoseService();

  io.on('connection', (socket) => {
    console.log('[Socket.IO] Client connected:', socket.id);

    // Send initial stats
    const stats = firehose.getStats();
    socket.emit('stats', stats);

    // Listen for firehose events and broadcast to clients
    const handlePost = (post: any) => {
      socket.emit('post', post);
    };

    const handleStats = () => {
      const currentStats = firehose.getStats();
      socket.emit('stats', currentStats);
    };

    // Attach listeners
    firehose.on('post', handlePost);

    // Send stats updates every second
    const statsInterval = setInterval(handleStats, 1000);

    socket.on('disconnect', () => {
      console.log('[Socket.IO] Client disconnected:', socket.id);
      firehose.off('post', handlePost);
      clearInterval(statsInterval);
    });
  });

  return io;
}
```

### Client-Side Hook
**Source**: `/home/coolhand/servers/firehose/client/src/hooks/useSocket.ts`

```typescript
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const [stats, setStats] = useState<FirehoseStats | null>(null);
  const [latestPost, setLatestPost] = useState<Post | null>(null);

  useEffect(() => {
    // Connect to Socket.IO server with correct base path
    const socketInstance = io({
      path: `${import.meta.env.BASE_URL}socket.io`,
      transports: ['websocket', 'polling'],
    });

    socketInstance.on('connect', () => {
      console.log('[Socket.IO] Connected');
      setConnected(true);
    });

    socketInstance.on('disconnect', () => {
      console.log('[Socket.IO] Disconnected');
      setConnected(false);
    });

    socketInstance.on('stats', (data: FirehoseStats) => {
      setStats(data);
    });

    socketInstance.on('post', (data: Post) => {
      setLatestPost(data);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  return {
    socket,
    connected,
    stats,
    latestPost,
  };
}
```

---

## 5. JWT Authentication (Session Management)

### JWT Creation & Verification
**Source**: `/home/coolhand/servers/firehose/server/_core/oauth.ts:167-233`

```typescript
import { SignJWT, jwtVerify } from "jose";

type SessionPayload = {
  openId: string;
  appId: string;
  name: string;
};

class OAuthService {
  private getSessionSecret() {
    const secret = ENV.cookieSecret;
    return new TextEncoder().encode(secret);
  }

  async createSessionToken(
    openId: string,
    options: { expiresInMs?: number; name?: string } = {}
  ): Promise<string> {
    return this.signSession(
      {
        openId,
        appId: ENV.appId,
        name: options.name || "",
      },
      options
    );
  }

  async signSession(
    payload: SessionPayload,
    options: { expiresInMs?: number } = {}
  ): Promise<string> {
    const issuedAt = Date.now();
    const expiresInMs = options.expiresInMs ?? ONE_YEAR_MS; // 365 days
    const expirationSeconds = Math.floor((issuedAt + expiresInMs) / 1000);
    const secretKey = this.getSessionSecret();

    return new SignJWT({
      openId: payload.openId,
      appId: payload.appId,
      name: payload.name,
    })
      .setProtectedHeader({ alg: "HS256", typ: "JWT" })
      .setExpirationTime(expirationSeconds)
      .sign(secretKey);
  }

  async verifySession(
    cookieValue: string | undefined | null
  ): Promise<{ openId: string; appId: string; name: string } | null> {
    if (!cookieValue) {
      console.warn("[Auth] Missing session cookie");
      return null;
    }

    try {
      const secretKey = this.getSessionSecret();
      const { payload } = await jwtVerify(cookieValue, secretKey, {
        algorithms: ["HS256"],
      });
      const { openId, appId, name } = payload as Record<string, unknown>;

      if (
        !isNonEmptyString(openId) ||
        !isNonEmptyString(appId) ||
        !isNonEmptyString(name)
      ) {
        console.warn("[Auth] Session payload missing required fields");
        return null;
      }

      return { openId, appId, name };
    } catch (error) {
      console.warn("[Auth] Session verification failed", String(error));
      return null;
    }
  }
}

const isNonEmptyString = (value: unknown): value is string =>
  typeof value === "string" && value.length > 0;
```

### React Hook
**Source**: `/home/coolhand/servers/firehose/client/src/_core/hooks/useAuth.ts`

```typescript
import { getLoginUrl } from "@/const";
import { trpc } from "@/lib/trpc";
import { useCallback, useEffect, useMemo } from "react";

export function useAuth(options?: UseAuthOptions) {
  const { redirectOnUnauthenticated = false, redirectPath = getLoginUrl() } =
    options ?? {};
  const utils = trpc.useUtils();

  const meQuery = trpc.auth.me.useQuery(undefined, {
    retry: false,
    refetchOnWindowFocus: false,
  });

  const logoutMutation = trpc.auth.logout.useMutation({
    onSuccess: () => {
      utils.auth.me.setData(undefined, null);
    },
  });

  const logout = useCallback(async () => {
    try {
      await logoutMutation.mutateAsync();
    } catch (error: unknown) {
      if (
        error instanceof TRPCClientError &&
        error.data?.code === "UNAUTHORIZED"
      ) {
        return;
      }
      throw error;
    } finally {
      utils.auth.me.setData(undefined, null);
      await utils.auth.me.invalidate();
    }
  }, [logoutMutation, utils]);

  const state = useMemo(() => {
    localStorage.setItem(
      "manus-runtime-user-info",
      JSON.stringify(meQuery.data)
    );
    return {
      user: meQuery.data ?? null,
      loading: meQuery.isLoading || logoutMutation.isPending,
      error: meQuery.error ?? logoutMutation.error ?? null,
      isAuthenticated: Boolean(meQuery.data),
    };
  }, [meQuery.data, meQuery.error, meQuery.isLoading, logoutMutation.error, logoutMutation.isPending]);

  useEffect(() => {
    if (!redirectOnUnauthenticated) return;
    if (meQuery.isLoading || logoutMutation.isPending) return;
    if (state.user) return;
    if (typeof window === "undefined") return;
    if (window.location.pathname === redirectPath) return;

    window.location.href = redirectPath;
  }, [redirectOnUnauthenticated, redirectPath, logoutMutation.isPending, meQuery.isLoading, state.user]);

  return {
    ...state,
    refresh: () => meQuery.refetch(),
    logout,
  };
}
```

---

## 6. Bluesky HTTP Client (Rate-Limited)

### Python AT Protocol Client
**Source**: `/home/coolhand/projects/blueballs/backend/app/services/bluesky_client.py:37-113`

```python
import asyncio
import time
import httpx
from typing import List, Tuple

class RateLimiter:
    """
    Simple rate limiter for Bluesky API.
    Bluesky uses a points-based system: 3000 points/hour for unauthenticated, 5000 for authenticated.
    """

    def __init__(self, max_points: int = 3000, window_seconds: int = 3600):
        self.max_points = max_points
        self.window_seconds = window_seconds
        self.requests: List[tuple[float, int]] = []  # (timestamp, points_cost)
        self._lock = asyncio.Lock()

    async def acquire(self, points_cost: int = 1) -> None:
        """Block until we can safely make a request without exceeding rate limit."""
        async with self._lock:
            now = time.time()

            # Remove requests outside the current window
            cutoff = now - self.window_seconds
            self.requests = [(ts, cost) for ts, cost in self.requests if ts > cutoff]

            # Calculate current usage
            current_points = sum(cost for _, cost in self.requests)

            # If we'd exceed the limit, wait until oldest requests expire
            if current_points + points_cost > self.max_points:
                if self.requests:
                    oldest_ts = self.requests[0][0]
                    wait_time = (oldest_ts + self.window_seconds) - now + 1  # +1 second buffer
                    if wait_time > 0:
                        print(f"Rate limit approaching ({current_points}/{self.max_points} points used). Waiting {wait_time:.1f} seconds...")
                        await asyncio.sleep(wait_time)
                        return await self.acquire(points_cost)  # Recurse after waiting

            # Record this request
            self.requests.append((time.time(), points_cost))


class BlueskyClient:
    """Client for interacting with the Bluesky API."""

    def __init__(self, identifier: str = None, password: str = None):
        self.base_url = "https://bsky.social/xrpc"
        self.access_token = None
        self.refresh_token = None
        self.user_did = None
        self.handle = None
        self.rate_limiter = RateLimiter()

        if identifier and password:
            self.login(identifier, password)

    def login(self, identifier: str, password: str) -> bool:
        """Create a session by authenticating with Bluesky."""
        url = f"{self.base_url}/com.atproto.server.createSession"
        headers = {'Content-Type': 'application/json'}
        data = {'identifier': identifier, 'password': password}

        try:
            response = httpx.post(url, headers=headers, json=data, timeout=10.0)
            response.raise_for_status()
            session_data = response.json()

            # Store session data
            self.access_token = session_data['accessJwt']
            self.refresh_token = session_data['refreshJwt']
            self.user_did = session_data['did']
            self.handle = session_data['handle']

            print(f"Successfully logged in as {self.handle}")
            return True
        except (httpx.HTTPError, KeyError) as e:
            print(f"Login failed: {str(e)}")
            return False

    async def get_profile(self, actor: str) -> dict:
        """Fetch a user profile."""
        await self.rate_limiter.acquire(1)  # 1 point per request

        url = f"{self.base_url}/app.bsky.actor.getProfile"
        headers = {}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        params = {'actor': actor}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching profile: {str(e)}")
            return None
```

---

## 7. NetworkX Graph Analysis

### Community Detection & Centrality
**Source**: `/home/coolhand/projects/blueballs/backend/app/analytics/graph_analysis.py:55-80`

```python
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.link_analysis import pagerank_alg

def analyze_network(followers_data):
    """Analyze Bluesky network using NetworkX."""

    # Create directed graph
    G = nx.DiGraph()

    # Add edges from followers data
    # followers_data: {user_did: [follower_dids]}
    for user, followers in followers_data.items():
        for follower in followers:
            G.add_edge(follower, user)  # Follower → Following

    # Calculate metrics

    # 1. PageRank (influence)
    pagerank = pagerank_alg.pagerank(G)

    # 2. Betweenness Centrality (connector nodes)
    betweenness = nx.betweenness_centrality(G)

    # 3. Closeness Centrality (proximity)
    closeness = nx.closeness_centrality(G)

    # 4. Degree Centrality (direct connections)
    in_degree = nx.in_degree_centrality(G)
    out_degree = nx.out_degree_centrality(G)

    # 5. Community Detection (Louvain method)
    communities = list(community.greedy_modularity_communities(G.to_undirected()))

    # Return results with JSON-serializable types
    return {
        'nodes': len(G.nodes()),
        'edges': len(G.edges()),
        'pagerank': {k: float(v) for k, v in pagerank.items()},
        'betweenness': {k: float(v) for k, v in betweenness.items()},
        'closeness': {k: float(v) for k, v in closeness.items()},
        'in_degree': {k: float(v) for k, v in in_degree.items()},
        'out_degree': {k: float(v) for k, v in out_degree.items()},
        'communities': [list(c) for c in communities],
        'num_communities': len(communities),
    }
```

---

## 8. Redis + Filesystem Caching

### Dual-Backend Cache
**Source**: `/home/coolhand/projects/blueballs/backend/app/services/cache_service.py:49-80+`

```python
import asyncio
import json
from pathlib import Path
from typing import Any, Optional
import orjson

try:
    from redis.asyncio import Redis
except ImportError:
    Redis = None

class CacheService:
    """Cache service that supports Redis and filesystem backends."""

    def __init__(self, settings) -> None:
        self._settings = settings
        self._redis: Optional[Redis[Any]] = None
        self._base_path = Path(settings.cache_dir)
        self._base_path.mkdir(parents=True, exist_ok=True)

    async def initialize(self) -> None:
        """Attempt to connect to Redis if configured."""
        if self._settings.redis_url and Redis is not None:
            try:
                self._redis = Redis.from_url(
                    self._settings.redis_url,
                    encoding="utf-8",
                    decode_responses=False
                )
                await self._redis.ping()
                print("[Cache] Redis connected")
            except Exception as e:
                print(f"[Cache] Redis connection failed: {e}. Using filesystem fallback.")
                self._redis = None
        else:
            print("[Cache] Using filesystem backend")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache (Redis first, then filesystem)."""
        try:
            # Try Redis first
            if self._redis:
                value = await self._redis.get(key)
                if value:
                    return json.loads(value)
        except Exception as e:
            print(f"[Cache] Redis get failed: {e}")

        # Fallback to filesystem
        file_path = self._base_path / f"{key}.json"
        if file_path.exists():
            try:
                with open(file_path, 'rb') as f:
                    return orjson.loads(f.read())
            except Exception as e:
                print(f"[Cache] Filesystem get failed: {e}")

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache (both Redis and filesystem)."""
        serialized = orjson.dumps(value)

        # Try Redis
        if self._redis:
            try:
                await self._redis.set(key, serialized, ex=ttl)
            except Exception as e:
                print(f"[Cache] Redis set failed: {e}")

        # Always save to filesystem as fallback
        file_path = self._base_path / f"{key}.json"
        try:
            file_path.write_bytes(serialized)
        except Exception as e:
            print(f"[Cache] Filesystem set failed: {e}")
```

---

## 9. Drizzle ORM Schema

### SQLite Schema Definition
**Source**: `/home/coolhand/servers/firehose/drizzle/schema.ts`

```typescript
import { sqliteTable, text, integer, real, index } from 'drizzle-orm/sqlite-core';

export const posts = sqliteTable('posts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  uri: text('uri').unique().notNull(),
  cid: text('cid').notNull(),
  text: text('text').notNull(),
  authorDid: text('author_did').notNull(),
  authorHandle: text('author_handle').notNull(),
  sentiment: text('sentiment').notNull(), // 'positive' | 'negative' | 'neutral'
  sentimentScore: real('sentiment_score').notNull(),
  language: text('language'),
  charCount: integer('char_count'),
  wordCount: integer('word_count'),
  hashtags: text('hashtags'), // JSON array
  mentions: text('mentions'), // JSON array
  links: text('links'), // JSON array
  hasImages: integer('has_images'), // 0 | 1
  hasVideo: integer('has_video'), // 0 | 1
  hasLink: integer('has_link'), // 0 | 1
  isReply: integer('is_reply'), // 0 | 1
  isQuote: integer('is_quote'), // 0 | 1
  replyParent: text('reply_parent'),
  replyRoot: text('reply_root'),
  quoteUri: text('quote_uri'),
  embedType: text('embed_type'),
  facets: text('facets'), // JSON
  collectionWindow: text('collection_window'), // e.g., "08:00"
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
  timestamp: integer('timestamp', { mode: 'timestamp' }).defaultNow().notNull(),
}, (table) => ({
  uriIdx: index('posts_uri_idx').on(table.uri),
  sentimentIdx: index('posts_sentiment_idx').on(table.sentiment),
  languageIdx: index('posts_language_idx').on(table.language),
  createdAtIdx: index('posts_created_at_idx').on(table.createdAt),
}));

export const statsGlobal = sqliteTable('stats_global', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  totalPosts: integer('total_posts').notNull().default(0),
  totalPositive: integer('total_positive').notNull().default(0),
  totalNegative: integer('total_negative').notNull().default(0),
  totalNeutral: integer('total_neutral').notNull().default(0),
  lastPostTimestamp: integer('last_post_timestamp', { mode: 'timestamp' }),
});
```

---

## 10. tRPC Endpoint Pattern

### Type-Safe API Endpoint
**Source**: `/home/coolhand/servers/firehose/server/routers.ts:36-82`

```typescript
import { z } from 'zod';
import { publicProcedure, router } from './_core/trpc';
import { getFirehoseService } from './firehose';
import * as db from './db';

const firehoseService = getFirehoseService();

export const appRouter = router({
  firehose: router({
    // Get current statistics
    stats: publicProcedure.query(async () => {
      const stats = firehoseService.getStats();
      const postsCount = await db.getPostsCount();

      return {
        ...stats,
        inDatabase: postsCount,
      };
    }),

    // Export posts as CSV
    exportCSV: publicProcedure
      .input(z.object({
        sentiment: z.enum(['positive', 'negative', 'neutral']).optional(),
        language: z.string().optional(),
        limit: z.number().default(1000),
      }).optional())
      .query(async ({ input }) => {
        const filters = input || { limit: 1000 };
        const posts = await db.getRecentPosts(filters.limit || 1000, filters.sentiment);

        // Filter by language if specified
        const filteredPosts = filters.language
          ? posts.filter(p => p.language === filters.language)
          : posts;

        // Generate CSV
        const headers = [
          'Timestamp', 'Author Handle', 'Text', 'Sentiment',
          'Sentiment Score', 'Language', 'Hashtags', 'Has Images',
          'Has Video', 'Has Link', 'URI'
        ];

        const rows = filteredPosts.map(post => [
          post.createdAt,
          post.authorHandle,
          post.text,
          post.sentiment,
          post.sentimentScore,
          post.language || '',
          post.hashtags || '',
          post.hasImages ? 'Yes' : 'No',
          post.hasVideo ? 'Yes' : 'No',
          post.hasLink ? 'Yes' : 'No',
          post.uri
        ]);

        return [headers, ...rows]
          .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
          .join('\n');
      }),

    // Enable collection window
    enableCollection: publicProcedure
      .input(z.object({ window: z.string() }))
      .mutation(({ input }) => {
        firehoseService.enableCollection(input.window);
        return { success: true };
      }),

    // Disable collection
    disableCollection: publicProcedure
      .mutation(() => {
        firehoseService.disableCollection();
        return { success: true };
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

---

**End of Code Patterns**
