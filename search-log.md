# Skymarshal Following/Follower Analysis Search Report

**Date**: 2026-02-14
**Query**: Search for following/follower analysis, network graphs, bot detection, and engagement metrics
**Scope**: `/home/coolhand/servers/skymarshal/`
**Status**: Complete

---

## Search Summary

Found comprehensive following/follower management system spanning:
- **5 core modules** for analysis and cleanup
- **4 API endpoints** for network management
- **SQLite caching** for performance optimization
- **Async/sync hybrid architecture** with threading
- **Graph analytics** with Louvain community detection
- **Bot detection algorithms** using follower/following ratios

Total Lines of Code Analyzed: ~2,540 lines across 8 files

---

## 1. FollowerAnalyzer Module

**File**: `/home/coolhand/servers/skymarshal/skymarshal/analytics/follower_analyzer.py`
**Lines**: 558
**Provides**: Comprehensive follower ranking, bot detection, and quality analysis

### Key Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `rank_followers()` | Ranks followers by follower count (descending) | Sorted list of 350+ followers with profiles |
| `analyze_bot_indicators()` | Calculates bot probability scores (0-1) | Followers with `bot_score`, `bot_ratio` |
| `analyze_quality_followers()` | Quality scoring based on selective following | Followers with `quality_score` (0-1) |
| `get_followers()` | Paginates through followers with rate limiting | List of follower profiles |
| `get_profiles_batch()` | Cache-first profile fetching (25-profile batches) | Profiles merged from cache + API |
| `display_analysis_results()` | Renders Rich tables for terminal output | Formatted console output |
| `run_complete_analysis()` | End-to-end follower analysis workflow | Full analysis dict with rankings |

### Bot Scoring Algorithm

```python
if ratio < 0.01:   bot_score = 0.9  # "Very likely bot"
if ratio < 0.1:    bot_score = 0.7  # "Suspicious"
if ratio < 0.2:    bot_score = 0.7
if ratio < 0.5:    bot_score = 0.5
if ratio < 1.0:    bot_score = 0.3
else:              bot_score = 0.1
```

**Ratio**: `followers_count / following_count` (low ratio = likely bot spam)

### Quality Scoring Components (0-1 scale)

1. **Follower/Following Ratio** (max 0.4):
   - ratio > 2.0: +0.4
   - ratio > 1.0: +0.3
   - ratio > 0.5: +0.2

2. **Post Activity** (max 0.3):
   - posts > 100: +0.3
   - posts > 50: +0.2
   - posts > 10: +0.1

3. **Follower Count (Influence)** (max 0.3):
   - followers > 10k: +0.3
   - followers > 1k: +0.2
   - followers > 100: +0.1

---

## 2. FollowingCleaner Module

**File**: `/home/coolhand/servers/skymarshal/skymarshal/cleanup/following_cleaner.py`
**Lines**: 568
**Provides**: Following list analysis and bot/spam account cleanup

### Key Functions

| Function | Purpose |
|----------|---------|
| `analyze_following_quality()` | Analyzes each following account for bot/quality indicators |
| `display_analysis_results()` | Shows problematic accounts in formatted table |
| `interactive_unfollow()` | Per-account unfollow confirmation with safety checks |
| `get_following()` | Paginates through user's following list (100 max/request) |
| `get_profiles_batch()` | Batch fetches account profiles with caching |
| `run_complete_analysis()` | Full cleanup workflow with optional interactive mode |

### Quality Analysis Metrics

- **Bot Score** (0-1): follower/following ratio + handle patterns + description
- **Quality Score** (0-1): follower count, post activity, selective following
- **Issues List**: Flags like "Low ratio", "Very short handle", "Missing description"

### Risk Levels

- **High-Risk**: `bot_score > 0.7` OR `quality_score < 0.2` (up to 10 per session)
- **Problematic**: `bot_score > 0.5` OR `quality_score < 0.3`

### Interactive Unfollow Workflow

1. Shows high-risk account details (handle, scores, issues)
2. User chooses: "unfollow" / "skip" / "quit"
3. Rate limiting: 1 second delay between unfollows
4. Tracks: unfollowed count, skipped count, error count

---

## 3. BotDetector Module

**File**: `/home/coolhand/servers/skymarshal/skymarshal/bot_detection.py`
**Lines**: 75
**Provides**: Simple heuristic-based bot detection

### Methods

- `analyze_indicators(profiles, top_n=20)`: Filter by follower/following ratio, return sorted by severity
- `format_report(suspects)`: Generate text report of suspected bots

### Thresholds

- ratio < 0.01: "high" probability bot
- ratio < 0.10: "medium" probability bot

---

## 4. FollowerManager Module (Legacy)

**File**: `/home/coolhand/servers/skymarshal/skymarshal/followers.py`
**Lines**: 165
**Provides**: Basic follower ranking (simpler alternative to FollowerAnalyzer)

### Functions

- `rank_followers()`: Ranks by follower count (simple sort)
- `get_followers()`: Paginates with 100-per-request limit
- `get_profiles_batch()`: Parallel profile fetching (5 max workers)
- `analyze_quality()`: Filters for selective followers

---

## 5. Network Graph Analysis

**File**: `/home/coolhand/servers/skymarshal/skymarshal/network/analysis.py`
**Lines**: 368
**Provides**: Graph analytics with community detection and centrality metrics

### GraphAnalytics.analyse() Algorithm

**Inputs**: nodes, edges (followers/following relationships)

**Outputs**:
- node_metrics: cluster_id, degree_centrality, betweenness_centrality, pagerank, spiral positions
- edge_weights: connection strength scores
- clusters: community detection results with colors
- graph_metrics: density, modularity, top nodes

### Clustering

- **Primary**: `community.louvain_communities()` with seed=42
- **Fallback**: `greedy_modularity_communities()` (older NetworkX)
- **Colors**: 10-color palette for visualization

### Centrality Metrics

1. **Degree Centrality**: Direct connection count (0-1)
2. **Betweenness Centrality**: "Bridge" importance (0-1)
3. **PageRank**: Influence score (0-1)

### Layout Positioning

**Spiral Layout**: Clusters around circles, nodes within clusters sorted by PageRank

**Swiss Grid Layout**: 
- Target at center (0, 0)
- Tier 0 (>20 connections): radius 200
- Tier 1 (5-20): radius 400
- Tier 2 (<5): radius 600

---

## 6. Network Fetcher (Orchestrator)

**File**: `/home/coolhand/servers/skymarshal/skymarshal/network/fetcher.py`
**Lines**: 426
**Provides**: End-to-end network data collection and assembly

### 5-Stage Pipeline

1. **Fetch Target Profile**: Validates handle exists
2. **Fetch Primary Relations**: Parallel requests for followers/following (up to 500 each)
3. **Hydrate Profiles**: Batch fetch 25 at a time, cache-first (max 8 workers)
4. **Detect Mutuals**: Mark mutual follows, classify relationships
5. **Augment Interconnections** (mode-dependent):
   - "fast": Skip
   - "balanced": Top 150 accounts
   - "detailed": All accounts

### Relationship Classification

- target: The queried account
- mutual: Follow each other
- following: You follow them
- follower: They follow you
- indirect: No direct follow relationship

### Orbit Tier Classification

- Tier 0: >20 connections (strong)
- Tier 1: 5-20 connections (medium)
- Tier 2: <5 connections (weak)

### Performance

- Fast mode: ~2-5 seconds
- Balanced mode: ~30-60 seconds
- Detailed mode: ~5-15 minutes

---

## 7. API Endpoints

### Network API Blueprint

**File**: `/home/coolhand/servers/skymarshal/skymarshal/api/network.py`
**Lines**: 234

#### POST `/api/network/fetch`

Start async network fetch job. Returns job_id for polling.

**Features**: Async execution, cache-first, Socket.IO progress updates, configurable limits

#### GET `/api/network/status/<job_id>`

Check job progress (status, progress %, message, error).

#### GET `/api/network/result/<job_id>`

Retrieve completed job result (nodes, edges, metadata).

#### POST `/api/network/cache/clear`

Clear network cache, return count of cleared entries.

---

### Cleanup API Blueprint

**File**: `/home/coolhand/servers/skymarshal/skymarshal/api/cleanup.py`
**Lines**: 146

#### POST `/api/cleanup/analyze`

Analyze authenticated user's following for cleanup candidates.

Returns: List of problematic accounts with bot_score, quality_score, issues.

#### POST `/api/cleanup/unfollow`

Unfollow one or more accounts by DID.

**Request**: `{"dids": ["did:plc:...", ...]}`
**Response**: Unfollowed count, error list

---

## File Location Reference

| File | Type | Lines | Purpose |
|------|------|-------|---------|
| `skymarshal/analytics/follower_analyzer.py` | Module | 558 | Follower ranking + bot/quality analysis |
| `skymarshal/cleanup/following_cleaner.py` | Module | 568 | Following cleanup + interactive unfollow |
| `skymarshal/bot_detection.py` | Module | 75 | Simple bot heuristics |
| `skymarshal/followers.py` | Module | 165 | Legacy follower ranking |
| `skymarshal/network/analysis.py` | Module | 368 | Graph analytics (Louvain, PageRank, centrality) |
| `skymarshal/network/fetcher.py` | Module | 426 | Network data orchestration |
| `skymarshal/api/network.py` | Blueprint | 234 | REST endpoints for network |
| `skymarshal/api/cleanup.py` | Blueprint | 146 | REST endpoints for cleanup |

**Total**: ~2,540 lines

---

## Architecture Patterns

### Async/Sync Hybrid

- **Async**: FollowerAnalyzer, FollowingCleaner use aiohttp + asyncio
- **Sync**: NetworkFetcher uses ThreadPoolExecutor (Flask/eventlet compatible)
- Thread-safe with threading.Lock where needed

### Caching Strategy

1. **Profile Cache** (SQLite): Per-module cache-first lookup, 0.05s rate limiting
2. **Network Cache**: File-based, keyed by (handle, settings, mode)

### Rate Limiting

- Profile fetches: 25 at a time
- Follower/Following: 100 at a time
- Delay: 0.05s between batches
- Unfollow: 1s between operations (safety)

---

## Key Algorithms

### Bot Detection

**Primary**: Follower/Following Ratio (low ratio = likely bot/spam)

**Secondary Signals**:
- Handle patterns: "bot", "spam", "fake", "test"
- Handle length: <3 chars suspicious
- Bio: Missing or very short

### Quality Scoring

**Assumption**: Selective followers (follow few, followed by many) = higher quality

**Components** (1.0 max):
1. Follower/Following ratio (0.4 weight)
2. Post activity (0.3 weight)
3. Follower count/influence (0.3 weight)

---

## Statistics

| Metric | Value |
|--------|-------|
| Total modules | 8 |
| Total functions | ~45 |
| SQLite tables | 1 (shared) |
| API endpoints | 6 |
| Async functions | ~12 |
| Lines of code | ~2,540 |
| Graph algorithms | 5 (Louvain, PageRank, degree, betweenness, clustering) |

---

*Report generated by @geepers_searcher*
*Search location*: `/home/coolhand/servers/skymarshal/`
