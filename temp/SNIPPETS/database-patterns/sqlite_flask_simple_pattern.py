"""
SQLite Simple Connection Pattern for Flask Apps

Description: Straightforward SQLite integration for Flask applications that don't require
connection pooling. Uses simple connection-per-operation pattern with proper error handling
and context managers. Ideal for low-to-medium traffic applications.

Use Cases:
- Logging and metrics collection (write-heavy, low concurrency)
- Simple data persistence for dashboards
- Prototype and development applications
- Background tasks with isolated database access
- Applications where each operation is fast and independent

Dependencies:
- sqlite3 (standard library)
- Flask (pip install Flask)

Notes:
- SQLite supports multiple readers but only one writer at a time
- Each function opens and closes its own connection (simple but safe)
- For high-concurrency read-heavy workloads, see sqlite_flask_connection_pool.py
- WAL mode (Write-Ahead Logging) recommended for better concurrency
- Use transactions for multi-statement operations
- Thread-safe: each thread gets its own connection

Performance Characteristics:
- Good for: < 100 requests/second, mostly reads or isolated writes
- Connection overhead: ~1-2ms per operation
- Alternative: Use connection pooling for high-traffic apps

Related Snippets:
- database-patterns/sqlite_flask_connection_pool.py (for high concurrency)
- database-patterns/sqlite_migrations.py
- web-frameworks/flask_background_thread.py
"""

import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from flask import Flask, g, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_PATH = 'app.db'


# Context manager for database connections
@contextmanager
def get_db_connection():
    """Context manager for SQLite database connections.

    Yields:
        sqlite3.Connection: Database connection with row factory enabled

    Example:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        # Enable row factory for dict-like access
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrency (persistent setting)
        conn.execute("PRAGMA journal_mode=WAL")
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def init_database():
    """Initialize database schema.

    Creates tables if they don't exist. Run once at application startup.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Example: Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT,
                sentiment TEXT,
                sentiment_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                uri TEXT UNIQUE
            )
        ''')

        # Example: Stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                positive INTEGER DEFAULT 0,
                negative INTEGER DEFAULT 0,
                neutral INTEGER DEFAULT 0,
                total INTEGER DEFAULT 0
            )
        ''')

        # Create indexes for common queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_posts_timestamp
            ON posts(timestamp DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_posts_sentiment
            ON posts(sentiment)
        ''')

        logger.info("Database initialized successfully")


# Database operation functions
def insert_post(
    text: str,
    author: str,
    sentiment: str,
    sentiment_score: float,
    uri: str
) -> Optional[int]:
    """Insert a post into the database.

    Args:
        text: Post text content
        author: Post author identifier
        sentiment: Sentiment label ('positive', 'negative', 'neutral')
        sentiment_score: Sentiment score (-1 to 1)
        uri: Unique post URI

    Returns:
        Row ID of inserted post, or None if failed (e.g., duplicate URI)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO posts
                (text, author, sentiment, sentiment_score, uri)
                VALUES (?, ?, ?, ?, ?)
            ''', (text, author, sentiment, sentiment_score, uri))

            return cursor.lastrowid if cursor.rowcount > 0 else None
    except Exception as e:
        logger.error(f"Failed to insert post: {e}")
        return None


def get_recent_posts(limit: int = 50, sentiment_filter: Optional[str] = None) -> List[Dict]:
    """Get recent posts from database.

    Args:
        limit: Maximum number of posts to return
        sentiment_filter: Optional sentiment to filter by

    Returns:
        List of post dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            if sentiment_filter:
                cursor.execute('''
                    SELECT id, text, author, sentiment, sentiment_score, timestamp, uri
                    FROM posts
                    WHERE sentiment = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (sentiment_filter, limit))
            else:
                cursor.execute('''
                    SELECT id, text, author, sentiment, sentiment_score, timestamp, uri
                    FROM posts
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))

            # Convert Row objects to dicts
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Failed to get posts: {e}")
        return []


def save_sentiment_stats(positive: int, negative: int, neutral: int) -> bool:
    """Save sentiment statistics snapshot.

    Args:
        positive: Count of positive posts
        negative: Count of negative posts
        neutral: Count of neutral posts

    Returns:
        True if successful, False otherwise
    """
    try:
        total = positive + negative + neutral
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sentiment_stats (positive, negative, neutral, total)
                VALUES (?, ?, ?, ?)
            ''', (positive, negative, neutral, total))
        return True
    except Exception as e:
        logger.error(f"Failed to save stats: {e}")
        return False


def get_stats_history(hours: int = 24) -> List[Dict]:
    """Get historical sentiment statistics.

    Args:
        hours: Number of hours of history to retrieve

    Returns:
        List of stats dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, positive, negative, neutral, total
                FROM sentiment_stats
                WHERE timestamp > datetime('now', '-' || ? || ' hours')
                ORDER BY timestamp DESC
                LIMIT 1000
            ''', (hours,))

            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Failed to get stats history: {e}")
        return []


def get_sentiment_distribution(hours: int = 24) -> Dict[str, int]:
    """Get sentiment distribution for recent posts.

    Args:
        hours: Number of hours to analyze

    Returns:
        Dict with sentiment counts
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sentiment, COUNT(*) as count
                FROM posts
                WHERE timestamp > datetime('now', '-' || ? || ' hours')
                GROUP BY sentiment
            ''', (hours,))

            distribution = {'positive': 0, 'negative': 0, 'neutral': 0}
            for row in cursor.fetchall():
                distribution[row['sentiment']] = row['count']

            return distribution
    except Exception as e:
        logger.error(f"Failed to get distribution: {e}")
        return {'positive': 0, 'negative': 0, 'neutral': 0}


# Flask application example
app = Flask(__name__)


@app.route('/api/posts')
def api_posts():
    """Get recent posts endpoint."""
    limit = int(request.args.get('limit', 50))
    sentiment = request.args.get('sentiment')

    posts = get_recent_posts(limit=limit, sentiment_filter=sentiment)
    return jsonify(posts)


@app.route('/api/stats')
def api_stats():
    """Get sentiment statistics."""
    hours = int(request.args.get('hours', 24))

    distribution = get_sentiment_distribution(hours=hours)
    history = get_stats_history(hours=hours)

    return jsonify({
        'distribution': distribution,
        'history': history
    })


if __name__ == '__main__':
    # Initialize database at startup
    init_database()

    # Example operations
    print("Testing database operations...")

    # Insert test post
    post_id = insert_post(
        text="This is a test post!",
        author="test_user",
        sentiment="positive",
        sentiment_score=0.75,
        uri="test://post/123"
    )
    print(f"Inserted post ID: {post_id}")

    # Get recent posts
    posts = get_recent_posts(limit=10)
    print(f"Recent posts: {len(posts)}")

    # Save stats
    save_sentiment_stats(positive=10, negative=5, neutral=15)
    print("Saved stats")

    # Get distribution
    dist = get_sentiment_distribution(hours=24)
    print(f"Distribution: {dist}")
