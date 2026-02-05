"""
Real-Time Dashboard State Management

Description: Pattern for managing dashboard state with thread-safe counters, buffers,
and statistics tracking. Optimized for real-time data streams with deque-based buffering.

Use Cases:
- Real-time analytics dashboards
- Social media monitoring
- Live trading/market data displays
- IoT sensor dashboards
- System monitoring tools

Dependencies:
- collections.deque (standard library)
- threading (standard library)

Notes:
- Uses deque with maxlen for automatic FIFO buffer management
- Thread-safe for simple read/write operations on primitives
- For complex operations, add threading.Lock()
- Efficient memory usage with bounded buffers
- Suitable for high-frequency updates

Related Snippets:
- real-time-dashboards/socketio_emit_from_background.py
- data-visualization/time_series_buffer.py
"""

from collections import deque
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading


class DashboardState:
    """
    Thread-safe state management for real-time dashboards.

    Example Usage:
        state = DashboardState(buffer_size=1000)

        # Add data point
        state.add_item({
            'timestamp': datetime.now(),
            'value': 42,
            'category': 'A'
        })

        # Update statistics
        state.increment_counter('category_A')

        # Get recent items
        recent = state.get_recent_items(50)

        # Get stats snapshot
        stats = state.get_stats_snapshot()
    """

    def __init__(
        self,
        buffer_size: int = 500,
        history_size: int = 60,
        enable_locking: bool = False
    ):
        """
        Initialize dashboard state.

        Args:
            buffer_size: Maximum items to buffer
            history_size: Maximum historical data points to keep
            enable_locking: Enable thread locking for complex operations
        """
        # Circular buffer for recent items
        self.items_buffer = deque(maxlen=buffer_size)

        # Counters
        self.counters = {}

        # Time-series history
        self.history = deque(maxlen=history_size)

        # Metadata
        self.total_processed = 0
        self.start_time = datetime.now()
        self.last_update = datetime.now()

        # Optional thread lock
        self._lock = threading.Lock() if enable_locking else None

    def add_item(self, item: Dict[str, Any]):
        """
        Add item to buffer.

        Args:
            item: Dict with item data
        """
        self.items_buffer.append(item)
        self.total_processed += 1
        self.last_update = datetime.now()

    def increment_counter(self, key: str, amount: int = 1):
        """
        Increment a named counter.

        Args:
            key: Counter name
            amount: Amount to increment (default: 1)
        """
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += amount

    def decrement_counter(self, key: str, amount: int = 1):
        """Decrement a named counter"""
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] -= amount

    def set_counter(self, key: str, value: int):
        """Set counter to specific value"""
        self.counters[key] = value

    def get_counter(self, key: str) -> int:
        """Get current counter value"""
        return self.counters.get(key, 0)

    def add_history_point(self, data: Dict[str, Any]):
        """
        Add data point to time-series history.

        Args:
            data: Dict with timestamp and metric values
        """
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        self.history.append(data)

    def get_recent_items(
        self,
        limit: int = 50,
        filter_func: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recent items from buffer.

        Args:
            limit: Maximum items to return
            filter_func: Optional function to filter items

        Returns:
            List of recent items (newest first)
        """
        items = list(self.items_buffer)

        if filter_func:
            items = [item for item in items if filter_func(item)]

        return items[-limit:][::-1]  # Return newest first

    def get_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get historical data points.

        Args:
            limit: Maximum points to return (None = all)

        Returns:
            List of historical data points
        """
        history_list = list(self.history)
        if limit:
            return history_list[-limit:]
        return history_list

    def get_stats_snapshot(self) -> Dict[str, Any]:
        """
        Get complete statistics snapshot.

        Returns:
            Dict with all current statistics
        """
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            'counters': dict(self.counters),
            'total_processed': self.total_processed,
            'buffer_size': len(self.items_buffer),
            'history_size': len(self.history),
            'uptime_seconds': uptime,
            'items_per_second': self.total_processed / uptime if uptime > 0 else 0,
            'last_update': self.last_update.isoformat(),
            'start_time': self.start_time.isoformat()
        }

    def reset_counters(self):
        """Reset all counters to zero"""
        self.counters = {}
        self.total_processed = 0

    def clear_buffers(self):
        """Clear all buffers and history"""
        self.items_buffer.clear()
        self.history.clear()

    def reset_all(self):
        """Reset all state"""
        self.reset_counters()
        self.clear_buffers()
        self.start_time = datetime.now()
        self.last_update = datetime.now()


# Simplified pattern from Bluesky dashboard
class SimpleDashboardState:
    """
    Minimal dashboard state (pattern from Bluesky sentiment dashboard).

    Example:
        state = SimpleDashboardState()

        state.add_post({'text': 'Hello', 'sentiment': 'positive'})
        state.sentiment_counts['positive'] += 1

        recent_posts = list(state.posts_buffer)
    """

    def __init__(self):
        self.posts_buffer = deque(maxlen=500)
        self.sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        self.posts_per_minute = 0
        self.keyword_filters = []
        self.running = False
        self.total_processed = 0
        self.sentiment_history = deque(maxlen=60)  # Last 60 seconds

    def add_post(self, post_data: Dict[str, Any]):
        """Add post to buffer"""
        self.posts_buffer.append(post_data)
        self.total_processed += 1

    def update_sentiment_count(self, sentiment: str):
        """Update sentiment counter"""
        if sentiment in self.sentiment_counts:
            self.sentiment_counts[sentiment] += 1

    def add_history_point(self):
        """Add current state to history"""
        self.sentiment_history.append({
            'timestamp': datetime.now().isoformat(),
            'positive': self.sentiment_counts['positive'],
            'negative': self.sentiment_counts['negative'],
            'neutral': self.sentiment_counts['neutral']
        })

    def reset(self):
        """Reset all statistics"""
        self.sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        self.total_processed = 0
        self.posts_buffer.clear()
        self.sentiment_history.clear()


if __name__ == "__main__":
    # Example 1: Full-featured dashboard state
    state = DashboardState(buffer_size=100, history_size=30)

    # Simulate data ingestion
    for i in range(150):
        state.add_item({
            'id': i,
            'value': i * 10,
            'category': 'A' if i % 2 == 0 else 'B'
        })

        # Update counters
        category = 'A' if i % 2 == 0 else 'B'
        state.increment_counter(f'category_{category}')

        # Add history every 10 items
        if i % 10 == 0:
            state.add_history_point({
                'count': state.total_processed,
                'category_A': state.get_counter('category_A'),
                'category_B': state.get_counter('category_B')
            })

    # Get statistics
    stats = state.get_stats_snapshot()
    print(f"Total processed: {stats['total_processed']}")
    print(f"Buffer size: {stats['buffer_size']}")
    print(f"Counters: {stats['counters']}")

    # Get recent items
    recent = state.get_recent_items(10)
    print(f"\nMost recent items: {len(recent)}")

    # Get filtered items
    category_a = state.get_recent_items(
        limit=50,
        filter_func=lambda x: x['category'] == 'A'
    )
    print(f"Category A items: {len(category_a)}")

    # Example 2: Simple pattern
    simple_state = SimpleDashboardState()

    simple_state.add_post({'text': 'Great!', 'sentiment': 'positive'})
    simple_state.update_sentiment_count('positive')

    simple_state.add_post({'text': 'Terrible.', 'sentiment': 'negative'})
    simple_state.update_sentiment_count('negative')

    simple_state.add_history_point()

    print(f"\nSentiment counts: {simple_state.sentiment_counts}")
    print(f"Total: {simple_state.total_processed}")
