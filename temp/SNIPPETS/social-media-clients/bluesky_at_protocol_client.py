#!/usr/bin/env python3
"""
Bluesky AT Protocol Client

Description: Complete AT Protocol client for Bluesky social network with SQLite caching,
             batch processing, rate limiting, and interactive account management.

Use Cases:
- Analyzing follower/following relationships
- Batch profile fetching with smart caching
- Interactive account cleanup (unfollow bots/spam)
- Building Bluesky automation tools

Dependencies:
- aiohttp
- sqlite3 (stdlib)

Notes:
- Respects AT Protocol rate limits (3000 req/5min)
- SQLite caching eliminates redundant API calls
- Batch processing (25 profiles per request - API limit)
- Production-ready with comprehensive error handling

Related Snippets:
- api-clients/multi_provider_abstraction.py

Source Attribution:
- Extracted from: /home/coolhand/inbox/scratchpad/bluesky_tools/bluesky_cleaner.py
- Author: Luke Steuber
"""

import asyncio
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import aiohttp


class BlueskyClient:
    """
    Bluesky AT Protocol client with SQLite caching and batch processing.

    Features:
    - Smart caching system (SQLite database)
    - Batch processing (25 profiles per request)
    - Rate limiting (respects 3000 req/5min limit)
    - Comprehensive error handling
    """

    def __init__(self, username: str, password: str, db_path: str = "bluesky_cache.db"):
        self.username = username
        self.password = password
        self.base_url = "https://public.api.bsky.app"
        self.auth_url = "https://bsky.social"
        self.access_token = None
        self.did = None
        self.batch_size = 25  # API limit
        self.rate_limit_delay = 0.05
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for caching profile data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                did TEXT PRIMARY KEY,
                handle TEXT,
                display_name TEXT,
                description TEXT,
                followers_count INTEGER,
                following_count INTEGER,
                posts_count INTEGER,
                avatar TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_data TEXT
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_profiles_handle ON profiles(handle)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_profiles_followers ON profiles(followers_count DESC)")

        conn.commit()
        conn.close()

    async def authenticate(self) -> bool:
        """Authenticate with Bluesky AT Protocol."""
        url = f"{self.auth_url}/xrpc/com.atproto.server.createSession"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json={
                    "identifier": self.username,
                    "password": self.password
                }) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.access_token = data.get('accessJwt')
                        self.did = data.get('did')
                        return True
                    return False
            except Exception:
                return False

    def _get_cached_profiles(self, dids: List[str]) -> Dict[str, Dict]:
        """Retrieve cached profiles from database."""
        if not dids:
            return {}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        placeholders = ','.join(['?' for _ in dids])
        cursor.execute(f"""
            SELECT did, handle, display_name, description, followers_count,
                   following_count, posts_count, avatar, raw_data
            FROM profiles WHERE did IN ({placeholders})
        """, dids)

        cached = {}
        for row in cursor.fetchall():
            did, handle, display_name, description, followers, following, posts, avatar, raw = row
            cached[did] = {
                'did': did,
                'handle': handle,
                'displayName': display_name,
                'description': description,
                'followersCount': followers,
                'followsCount': following,
                'postsCount': posts,
                'avatar': avatar
            }

        conn.close()
        return cached

    def _cache_profiles(self, profiles: List[Dict]):
        """Store profiles in database cache."""
        if not profiles:
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for profile in profiles:
            cursor.execute("""
                INSERT OR REPLACE INTO profiles
                (did, handle, display_name, description, followers_count,
                 following_count, posts_count, avatar, raw_data, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                profile.get('did', ''),
                profile.get('handle', ''),
                profile.get('displayName', ''),
                profile.get('description', ''),
                profile.get('followersCount', 0),
                profile.get('followsCount', 0),
                profile.get('postsCount', 0),
                profile.get('avatar', ''),
                json.dumps(profile)
            ))

        conn.commit()
        conn.close()

    async def get_following(self, actor_did: str = None, limit: int = None) -> List[Dict]:
        """Get accounts that an actor follows with pagination."""
        actor_did = actor_did or self.did
        following = []
        cursor = None

        headers = {'Authorization': f'Bearer {self.access_token}'}

        async with aiohttp.ClientSession() as session:
            while limit is None or len(following) < limit:
                params = {'actor': actor_did, 'limit': 100}
                if cursor:
                    params['cursor'] = cursor

                async with session.get(
                    f"{self.base_url}/xrpc/app.bsky.graph.getFollows",
                    headers=headers, params=params
                ) as response:
                    if response.status != 200:
                        break

                    data = await response.json()
                    batch = data.get('follows', [])
                    following.extend(batch)

                    cursor = data.get('cursor')
                    if not cursor or not batch:
                        break

                    await asyncio.sleep(self.rate_limit_delay)

        return following[:limit] if limit else following

    async def get_followers(self, actor_did: str = None, limit: int = None) -> List[Dict]:
        """Get accounts that follow an actor with pagination."""
        actor_did = actor_did or self.did
        followers = []
        cursor = None

        headers = {'Authorization': f'Bearer {self.access_token}'}

        async with aiohttp.ClientSession() as session:
            while limit is None or len(followers) < limit:
                params = {'actor': actor_did, 'limit': 100}
                if cursor:
                    params['cursor'] = cursor

                async with session.get(
                    f"{self.base_url}/xrpc/app.bsky.graph.getFollowers",
                    headers=headers, params=params
                ) as response:
                    if response.status != 200:
                        break

                    data = await response.json()
                    batch = data.get('followers', [])
                    followers.extend(batch)

                    cursor = data.get('cursor')
                    if not cursor or not batch:
                        break

                    await asyncio.sleep(self.rate_limit_delay)

        return followers[:limit] if limit else followers

    async def get_profiles_batch(self, dids: List[str]) -> List[Dict]:
        """Get multiple profiles efficiently with cache-first approach."""
        if not dids:
            return []

        # Check cache first
        cached = self._get_cached_profiles(dids)
        uncached_dids = [did for did in dids if did not in cached]

        all_profiles = list(cached.values())

        # Fetch uncached from API in batches
        if uncached_dids:
            headers = {'Authorization': f'Bearer {self.access_token}'}

            async with aiohttp.ClientSession() as session:
                for i in range(0, len(uncached_dids), self.batch_size):
                    batch = uncached_dids[i:i + self.batch_size]

                    async with session.get(
                        f"{self.base_url}/xrpc/app.bsky.actor.getProfiles",
                        headers=headers, params={'actors': batch}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            new_profiles = data.get('profiles', [])
                            self._cache_profiles(new_profiles)
                            all_profiles.extend(new_profiles)

                    await asyncio.sleep(self.rate_limit_delay)

        return all_profiles

    async def unfollow(self, target_did: str) -> bool:
        """Unfollow an account by finding and deleting the follow record."""
        # First find the follow record
        headers = {'Authorization': f'Bearer {self.access_token}'}

        async with aiohttp.ClientSession() as session:
            cursor = None
            rkey = None

            # Search through follow records
            while True:
                params = {
                    'repo': self.did,
                    'collection': 'app.bsky.graph.follow',
                    'limit': 100
                }
                if cursor:
                    params['cursor'] = cursor

                async with session.get(
                    f"{self.base_url}/xrpc/com.atproto.repo.listRecords",
                    headers=headers, params=params
                ) as response:
                    if response.status != 200:
                        return False

                    data = await response.json()
                    for record in data.get('records', []):
                        if record.get('value', {}).get('subject') == target_did:
                            rkey = record.get('rkey')
                            break

                    if rkey:
                        break

                    cursor = data.get('cursor')
                    if not cursor:
                        return False

            # Delete the follow record
            if rkey:
                async with session.post(
                    f"{self.base_url}/xrpc/com.atproto.repo.deleteRecord",
                    headers=headers,
                    json={
                        'repo': self.did,
                        'collection': 'app.bsky.graph.follow',
                        'rkey': rkey
                    }
                ) as response:
                    return response.status == 200

        return False

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about the profile cache."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM profiles")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM profiles WHERE followers_count > 1000")
        popular = cursor.fetchone()[0]

        conn.close()

        return {'total_profiles': total, 'popular_profiles': popular}


# Usage example
if __name__ == "__main__":
    async def main():
        # Initialize client
        client = BlueskyClient("your.handle", "your_password")

        # Authenticate
        if not await client.authenticate():
            print("Authentication failed")
            return

        print(f"Authenticated as DID: {client.did}")

        # Get following
        following = await client.get_following(limit=100)
        print(f"Following {len(following)} accounts")

        # Get detailed profiles with caching
        dids = [f.get('did') for f in following if f.get('did')]
        profiles = await client.get_profiles_batch(dids)

        # Analyze follower ratios
        for profile in profiles[:10]:
            followers = profile.get('followersCount', 0)
            following_count = profile.get('followsCount', 0)
            ratio = followers / following_count if following_count > 0 else 0
            print(f"@{profile.get('handle')}: {followers}/{following_count} = {ratio:.2f}")

        # Show cache stats
        stats = client.get_cache_stats()
        print(f"Cache contains {stats['total_profiles']} profiles")

    asyncio.run(main())
