"""
Thread-Safe SQLite Database Operations

Description: Pattern for using SQLite safely in multi-threaded applications (Flask, SocketIO, etc.).
Avoids "database is locked" errors and ensures proper connection handling across threads.

Use Cases:
- Flask applications with background workers
- Real-time dashboards with concurrent database access
- Multi-threaded data processing pipelines
- Applications using threading with SQLite

Dependencies:
- sqlite3 (standard library)
- threading (standard library)

Notes:
- SQLite connections should not be shared across threads
- Use separate connections per operation or thread-local storage
- WAL mode enables concurrent reads with a single writer
- Each function opens/closes its own connection for thread safety
- Use check_same_thread=False only when necessary

Related Snippets:
- async-patterns/asyncio_background_thread.py
- database-patterns/sqlite_initialization.py
"""

import sqlite3
import threading
import logging
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from datetime import datetime

logger = logging.getLogger(__name__)


class ThreadSafeSQLite:
    """
    Thread-safe SQLite database wrapper.

    Example Usage:
        db = ThreadSafeSQLite('mydb.db')
        db.initialize_schema()

        # Insert from any thread
        db.execute_write(
            "INSERT INTO posts (text, timestamp) VALUES (?, ?)",
            ("Hello world", datetime.now())
        )

        # Query from any thread
        results = db.execute_read("SELECT * FROM posts LIMIT 10")
    """

    def __init__(self, db_path: str, enable_wal: bool = True):
        """
        Initialize thread-safe database.

        Args:
            db_path: Path to SQLite database file
            enable_wal: Enable Write-Ahead Logging for better concurrency
        """
        self.db_path = db_path
        self.enable_wal = enable_wal
        self._lock = threading.Lock()

        if enable_wal:
            self._enable_wal_mode()

    def _enable_wal_mode(self):
        """Enable WAL mode for better concurrent access"""
        with self.get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            logger.info("WAL mode enabled for database")

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.

        Yields:
            SQLite connection object

        Example:
            with db.get_connection() as conn:
                conn.execute("INSERT INTO table VALUES (?)", (value,))
                conn.commit()
        """
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def execute_write(self, query: str, params: tuple = ()) -> int:
        """
        Execute write query (INSERT, UPDATE, DELETE) in thread-safe manner.

        Args:
            query: SQL query with ? placeholders
            params: Tuple of parameters

        Returns:
            Last row ID for INSERT, or rows affected
        """
        with self._lock:  # Ensure only one write at a time
            with self.get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.lastrowid or cursor.rowcount
                except sqlite3.IntegrityError as e:
                    logger.warning(f"Integrity error: {e}")
                    return 0
                except Exception as e:
                    logger.error(f"Database write error: {e}")
                    conn.rollback()
                    raise

    def execute_read(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False
    ) -> List[sqlite3.Row]:
        """
        Execute read query (SELECT) in thread-safe manner.

        Args:
            query: SQL query with ? placeholders
            params: Tuple of parameters
            fetch_one: If True, return single row instead of list

        Returns:
            List of Row objects (or single Row if fetch_one=True)
        """
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)

                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
            except Exception as e:
                logger.error(f"Database read error: {e}")
                raise

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute multiple write queries in a single transaction.

        Args:
            query: SQL query with ? placeholders
            params_list: List of parameter tuples

        Returns:
            Number of rows affected
        """
        with self._lock:
            with self.get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    cursor.executemany(query, params_list)
                    conn.commit()
                    return cursor.rowcount
                except Exception as e:
                    logger.error(f"Batch write error: {e}")
                    conn.rollback()
                    raise


# Simple function-based pattern (from Bluesky dashboard)
def init_database(db_path: str):
    """
    Initialize database with schema.

    Args:
        db_path: Path to database file
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  text TEXT,
                  author TEXT,
                  sentiment TEXT,
                  sentiment_score REAL,
                  timestamp DATETIME,
                  uri TEXT UNIQUE)''')

    c.execute('''CREATE TABLE IF NOT EXISTS sentiment_stats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  positive INTEGER,
                  negative INTEGER,
                  neutral INTEGER,
                  total INTEGER)''')

    # Create indexes for common queries
    c.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp
                 ON posts(timestamp)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_sentiment
                 ON posts(sentiment)''')

    conn.commit()
    conn.close()


def save_to_db_thread_safe(db_path: str, data: Dict[str, Any]):
    """
    Save data to database from any thread.

    Args:
        db_path: Path to database file
        data: Dict with data to save

    Note:
        Opens and closes connection within function for thread safety.
        Use INSERT OR IGNORE to handle duplicate keys gracefully.
    """
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''INSERT OR IGNORE INTO posts
                     (text, author, sentiment, sentiment_score, timestamp, uri)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['text'], data['author'], data['sentiment'],
                   data['sentiment_score'], data['timestamp'], data['uri']))

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Database error: {e}")


def query_from_db_thread_safe(
    db_path: str,
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:
    """
    Query database from any thread.

    Args:
        db_path: Path to database file
        query: SQL query
        params: Query parameters

    Returns:
        List of dicts with column names as keys
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(query, params)
        rows = c.fetchall()

        # Convert Row objects to dicts
        results = [dict(row) for row in rows]

        conn.close()
        return results
    except Exception as e:
        logger.error(f"Query error: {e}")
        return []


if __name__ == "__main__":
    import time
    from concurrent.futures import ThreadPoolExecutor

    # Example 1: Using ThreadSafeSQLite class
    db = ThreadSafeSQLite(':memory:')

    # Create table
    db.execute_write('''CREATE TABLE test
                        (id INTEGER PRIMARY KEY, value TEXT)''')

    # Concurrent writes from multiple threads
    def write_data(thread_id):
        for i in range(5):
            db.execute_write(
                "INSERT INTO test (value) VALUES (?)",
                (f"Thread-{thread_id}-Value-{i}",)
            )
            time.sleep(0.01)

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(write_data, range(3))

    # Read results
    results = db.execute_read("SELECT * FROM test")
    print(f"Inserted {len(results)} rows from 3 threads")

    # Example 2: Simple function pattern
    init_database('test.db')
    save_to_db_thread_safe('test.db', {
        'text': 'Test post',
        'author': 'user123',
        'sentiment': 'positive',
        'sentiment_score': 0.5,
        'timestamp': datetime.now().isoformat(),
        'uri': 'test://123'
    })
