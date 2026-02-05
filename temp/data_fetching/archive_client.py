"""
Internet Archive / Wayback Machine Client
Programmatic access to the Internet Archive's Wayback Machine.

Extracted from toollama for reuse across projects.
"""

import requests
import logging
import time
from typing import Optional, List, Dict
from datetime import datetime
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class ArchivedSnapshot:
    """Represents an archived snapshot from the Wayback Machine"""
    url: str
    timestamp: datetime
    status_code: int
    original_url: str
    archive_url: str

    @classmethod
    def from_api_response(cls, data: Dict, original_url: str) -> 'ArchivedSnapshot':
        """Create ArchivedSnapshot from Wayback API response"""
        timestamp_str = data.get('timestamp', '')
        # Parse timestamp format: YYYYMMDDhhmmss
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S') if timestamp_str else datetime.now()

        return cls(
            url=data.get('url', ''),
            timestamp=timestamp,
            status_code=int(data.get('status', 200)),
            original_url=original_url,
            archive_url=data.get('url', '')
        )


@dataclass
class ArchiveResult:
    """Result of an archive operation"""
    success: bool
    archive_url: Optional[str] = None
    snapshot: Optional[ArchivedSnapshot] = None
    error: Optional[str] = None


class ArchiveClient:
    """Client for interacting with the Internet Archive Wayback Machine"""

    WAYBACK_SAVE_URL = "https://web.archive.org/save/"
    WAYBACK_AVAIL_URL = "https://archive.org/wayback/available"
    WAYBACK_CDX_URL = "https://web.archive.org/cdx/search/cdx"

    def __init__(self, user_agent: Optional[str] = None):
        """
        Initialize Archive client.

        Args:
            user_agent: Custom user agent string (default: generic browser UA)
        """
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        self.headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    def get_latest_snapshot(self, url: str) -> Optional[ArchivedSnapshot]:
        """
        Get the most recent archived snapshot of a URL.

        Args:
            url: URL to check for archives

        Returns:
            ArchivedSnapshot if found, None otherwise

        Example:
            >>> client = ArchiveClient()
            >>> snapshot = client.get_latest_snapshot('https://example.com')  # doctest: +SKIP
            >>> snapshot.archive_url  # doctest: +SKIP
            'https://web.archive.org/web/20231201120000/https://example.com'
        """
        try:
            logger.info(f"Checking for archived snapshots of: {url}")

            response = requests.get(
                self.WAYBACK_AVAIL_URL,
                params={'url': url},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Check if we have archived snapshots
            closest = data.get('archived_snapshots', {}).get('closest')

            if not closest:
                logger.info(f"No archived snapshots found for: {url}")
                return None

            snapshot = ArchivedSnapshot.from_api_response(closest, url)
            logger.info(f"Found snapshot from {snapshot.timestamp}")
            return snapshot

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error checking archives: {e}")
            return None
        except Exception as e:
            logger.error(f"Error checking archives: {e}")
            return None

    def archive_url(
        self,
        url: str,
        wait_for_completion: bool = True,
        retry_delay: int = 5
    ) -> ArchiveResult:
        """
        Archive a URL in the Wayback Machine.

        Args:
            url: URL to archive
            wait_for_completion: Whether to wait and verify archiving (default: True)
            retry_delay: Seconds to wait before checking if archived (default: 5)

        Returns:
            ArchiveResult with success status and archive URL

        Example:
            >>> client = ArchiveClient()
            >>> result = client.archive_url('https://example.com')  # doctest: +SKIP
            >>> result.success  # doctest: +SKIP
            True
            >>> result.archive_url  # doctest: +SKIP
            'https://web.archive.org/web/20231201120000/https://example.com'
        """
        try:
            # First check if already archived
            existing = self.get_latest_snapshot(url)
            if existing:
                logger.info(f"URL already archived: {existing.archive_url}")
                return ArchiveResult(
                    success=True,
                    archive_url=existing.archive_url,
                    snapshot=existing
                )

            # Request archiving
            save_url = f"{self.WAYBACK_SAVE_URL}{url}"
            logger.info(f"Requesting archive of: {url}")

            response = requests.get(
                save_url,
                headers=self.headers,
                allow_redirects=True,
                timeout=60
            )

            logger.debug(f"Archive request status: {response.status_code}")

            if not wait_for_completion:
                return ArchiveResult(
                    success=response.status_code in [200, 302],
                    archive_url=None,
                    error=None if response.status_code in [200, 302] else f"Status code: {response.status_code}"
                )

            # Wait for archiving to complete
            logger.info(f"Waiting {retry_delay}s for archiving to complete...")
            time.sleep(retry_delay)

            # Check for archived version
            snapshot = self.get_latest_snapshot(url)

            if snapshot:
                logger.info(f"Successfully archived: {snapshot.archive_url}")
                return ArchiveResult(
                    success=True,
                    archive_url=snapshot.archive_url,
                    snapshot=snapshot
                )
            else:
                logger.warning("Archive request submitted but snapshot not found")
                return ArchiveResult(
                    success=False,
                    error="Archive request submitted but snapshot not yet available"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error archiving URL: {e}")
            return ArchiveResult(success=False, error=str(e))
        except Exception as e:
            logger.error(f"Error archiving URL: {e}")
            return ArchiveResult(success=False, error=str(e))

    def get_snapshot_at_timestamp(
        self,
        url: str,
        timestamp: datetime
    ) -> Optional[ArchivedSnapshot]:
        """
        Get an archived snapshot closest to a specific timestamp.

        Args:
            url: URL to get snapshot for
            timestamp: Desired timestamp

        Returns:
            ArchivedSnapshot if found, None otherwise

        Example:
            >>> from datetime import datetime
            >>> client = ArchiveClient()
            >>> ts = datetime(2023, 1, 1)
            >>> snapshot = client.get_snapshot_at_timestamp('https://example.com', ts)  # doctest: +SKIP
        """
        try:
            # Format timestamp as YYYYMMDDhhmmss
            timestamp_str = timestamp.strftime('%Y%m%d%H%M%S')

            logger.info(f"Getting snapshot of {url} near {timestamp_str}")

            response = requests.get(
                self.WAYBACK_AVAIL_URL,
                params={
                    'url': url,
                    'timestamp': timestamp_str
                },
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            closest = data.get('archived_snapshots', {}).get('closest')

            if not closest:
                logger.info(f"No snapshot found near {timestamp_str}")
                return None

            return ArchivedSnapshot.from_api_response(closest, url)

        except Exception as e:
            logger.error(f"Error getting snapshot at timestamp: {e}")
            return None

    def get_all_snapshots(
        self,
        url: str,
        limit: int = 100,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[ArchivedSnapshot]:
        """
        Get all archived snapshots for a URL.

        Args:
            url: URL to get snapshots for
            limit: Maximum number of snapshots to return (default: 100)
            from_date: Start date for snapshot range (optional)
            to_date: End date for snapshot range (optional)

        Returns:
            List of ArchivedSnapshot objects

        Example:
            >>> client = ArchiveClient()
            >>> snapshots = client.get_all_snapshots('https://example.com', limit=10)  # doctest: +SKIP
            >>> len(snapshots)  # doctest: +SKIP
            10
        """
        try:
            logger.info(f"Getting all snapshots for: {url}")

            params = {
                'url': url,
                'output': 'json',
                'limit': limit
            }

            if from_date:
                params['from'] = from_date.strftime('%Y%m%d')
            if to_date:
                params['to'] = to_date.strftime('%Y%m%d')

            response = requests.get(
                self.WAYBACK_CDX_URL,
                params=params,
                headers=self.headers,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()

            # CDX returns array of arrays, skip header row
            if not data or len(data) < 2:
                logger.info("No snapshots found")
                return []

            snapshots = []
            for row in data[1:]:  # Skip header
                if len(row) >= 5:
                    # CDX format: [urlkey, timestamp, original, mimetype, statuscode, digest, length]
                    snapshot_data = {
                        'url': f"https://web.archive.org/web/{row[1]}/{row[2]}",
                        'timestamp': row[1],
                        'status': row[4] if len(row) > 4 else '200'
                    }

                    timestamp = datetime.strptime(row[1], '%Y%m%d%H%M%S')
                    snapshots.append(ArchivedSnapshot(
                        url=snapshot_data['url'],
                        timestamp=timestamp,
                        status_code=int(snapshot_data['status']),
                        original_url=url,
                        archive_url=snapshot_data['url']
                    ))

            logger.info(f"Found {len(snapshots)} snapshots")
            return snapshots

        except Exception as e:
            logger.error(f"Error getting all snapshots: {e}")
            return []


# Convenience functions
def archive_url(url: str, wait: bool = True) -> ArchiveResult:
    """
    Convenience function to archive a URL.

    Args:
        url: URL to archive
        wait: Whether to wait for completion (default: True)

    Returns:
        ArchiveResult with archive URL
    """
    client = ArchiveClient()
    return client.archive_url(url, wait_for_completion=wait)


def get_latest_archive(url: str) -> Optional[str]:
    """
    Convenience function to get latest archive URL.

    Args:
        url: URL to check

    Returns:
        Archive URL string or None
    """
    client = ArchiveClient()
    snapshot = client.get_latest_snapshot(url)
    return snapshot.archive_url if snapshot else None
