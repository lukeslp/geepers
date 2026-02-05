#!/usr/bin/env python3
"""
SQLite Batch Insert Pattern with Progress Tracking

Pattern for efficient batch insertion into SQLite with progress reporting
and error handling. Useful for loading large datasets.

Author: Luke Steuber
Date: 2025-12-18
Source: servers/coca/scripts/load_coca_modern.py
"""

import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional, Callable
import time


class BatchInserter:
    """
    Context manager for batch inserting into SQLite.

    Features:
    - Automatic batching at configurable size
    - Progress callbacks
    - Transaction management
    - Error handling with rollback
    """

    def __init__(
        self,
        db_path: Path,
        table: str,
        columns: List[str],
        batch_size: int = 10000,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ):
        """
        Initialize batch inserter.

        Args:
            db_path: Path to SQLite database
            table: Table name for insertions
            columns: Column names in order
            batch_size: Number of rows per batch
            progress_callback: Function(inserted, total) called after each batch
        """
        self.db_path = db_path
        self.table = table
        self.columns = columns
        self.batch_size = batch_size
        self.progress_callback = progress_callback

        self.conn = None
        self.cursor = None
        self.batch = []
        self.total_inserted = 0
        self.total_processed = 0

    def __enter__(self):
        """Open connection and begin transaction."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit remaining batch and close connection."""
        if exc_type is None:
            # No exception, commit remaining batch
            self._flush_batch()
            self.conn.commit()
        else:
            # Exception occurred, rollback
            self.conn.rollback()

        self.conn.close()
        return False  # Re-raise exception if any

    def add_row(self, row: Tuple) -> None:
        """
        Add a row to the batch.

        Args:
            row: Tuple of values matching column order
        """
        self.batch.append(row)
        self.total_processed += 1

        if len(self.batch) >= self.batch_size:
            self._flush_batch()

    def _flush_batch(self) -> None:
        """Insert current batch into database."""
        if not self.batch:
            return

        # Build INSERT statement
        placeholders = ', '.join(['?'] * len(self.columns))
        columns_str = ', '.join(self.columns)
        sql = f"""
            INSERT OR IGNORE INTO {self.table}
            ({columns_str})
            VALUES ({placeholders})
        """

        # Execute batch
        self.cursor.executemany(sql, self.batch)
        self.total_inserted += len(self.batch)

        # Report progress
        if self.progress_callback:
            self.progress_callback(self.total_inserted, self.total_processed)

        # Clear batch
        self.batch = []


def load_with_progress(
    db_path: Path,
    data_file: Path,
    table: str,
    columns: List[str],
    parser: Callable[[str], Optional[Tuple]],
    corpus: str,
    genre: str,
    batch_size: int = 10000
) -> dict:
    """
    Load data file with progress tracking.

    Args:
        db_path: Path to database
        data_file: Path to data file
        table: Target table name
        columns: Column names
        parser: Function to parse each line into tuple
        corpus: Corpus identifier
        genre: Genre identifier
        batch_size: Batch size for inserts

    Returns:
        Statistics dictionary
    """
    start_time = time.time()
    lines_read = 0

    # Progress callback
    def report_progress(inserted, processed):
        elapsed = time.time() - start_time
        rate = inserted / elapsed if elapsed > 0 else 0
        print(f"  Processed {processed:,} lines, inserted {inserted:,} tokens "
              f"({rate:,.0f} tokens/sec)")

    # Use batch inserter
    with BatchInserter(
        db_path=db_path,
        table=table,
        columns=columns,
        batch_size=batch_size,
        progress_callback=report_progress
    ) as inserter:

        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                lines_read += 1

                # Parse line
                result = parser(line)
                if result:
                    inserter.add_row(result)

                # Report progress every 50K lines
                if lines_read % 50000 == 0:
                    report_progress(inserter.total_inserted, inserter.total_processed)

    elapsed = time.time() - start_time

    return {
        'tokens': inserter.total_inserted,
        'lines': lines_read,
        'elapsed': elapsed,
        'rate': inserter.total_inserted / elapsed if elapsed > 0 else 0,
        'corpus': corpus,
        'genre': genre,
        'file': str(data_file)
    }


# Example usage
if __name__ == '__main__':

    # Define parser function
    def parse_line(line: str) -> Optional[Tuple]:
        """Parse tab-separated WLP line."""
        try:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                doc_id, word, lemma, pos = parts[:4]
                if not word.startswith('@@'):
                    return (
                        doc_id,
                        0,  # position (would need counter)
                        word,
                        word.lower(),
                        lemma,
                        pos,
                        'acad',  # genre
                        'coca'   # corpus
                    )
        except Exception:
            pass
        return None

    # Load file
    stats = load_with_progress(
        db_path=Path('coca_index.db'),
        data_file=Path('coca-samples-wlp/wlp_acad.txt'),
        table='tokens',
        columns=['doc_id', 'position', 'word', 'word_lower', 'lemma', 'pos', 'genre', 'corpus'],
        parser=parse_line,
        corpus='coca',
        genre='acad',
        batch_size=10000
    )

    print(f"\nCompleted: {stats['tokens']:,} tokens in {stats['elapsed']:.1f}s "
          f"({stats['rate']:,.0f} tokens/sec)")
