#!/usr/bin/env python3
"""
WLP Format Parser Pattern

Word-Lemma-POS (WLP) format is used by COCA and Brown corpus.
Standard format: doc_id \t word \t lemma \t pos_tag
Brown variant: word \t lemma \t pos_tag (doc_id synthesized)

Author: Luke Steuber
Date: 2025-12-18
Source: servers/coca/scripts/load_brown_corpus.py
"""

from pathlib import Path
from typing import Optional, Tuple


def parse_wlp_line_standard(line: str) -> Optional[Tuple[str, str, str, str]]:
    """
    Parse standard 4-column WLP format (COCA).

    Args:
        line: Tab-separated line (doc_id, word, lemma, pos)

    Returns:
        Tuple of (doc_id, word, lemma, pos) or None if invalid
    """
    try:
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            doc_id, word, lemma, pos = parts[0], parts[1], parts[2], parts[3]

            # Skip special markers
            if word.startswith('@@'):
                return None

            return doc_id, word, lemma, pos
    except Exception:
        return None

    return None


def parse_wlp_line_brown(
    line: str,
    line_num: int,
    filename: str
) -> Optional[Tuple[str, str, str, str]]:
    """
    Parse Brown corpus 3-column WLP format with synthesized doc_id.

    Args:
        line: Tab-separated line (word, lemma, pos)
        line_num: Current line number in file
        filename: Name of file being parsed (e.g., "wlp_adventure.txt")

    Returns:
        Tuple of (doc_id, word, lemma, pos) or None if invalid
    """
    try:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            word, lemma, pos = parts[0], parts[1], parts[2]

            # Skip special markers
            if word.startswith('@@'):
                return None

            # Synthesize doc_id from filename and line number
            # Extract genre from filename (e.g., "wlp_adventure.txt" → "adventure")
            genre = filename.replace('wlp_', '').replace('.txt', '')
            doc_id = f"{genre}_{line_num:05d}"

            return doc_id, word, lemma, pos
    except Exception:
        return None

    return None


def batch_insert_tokens(conn, batch: list, batch_size: int = 10000) -> int:
    """
    Batch insert tokens into SQLite database.

    Args:
        conn: SQLite connection
        batch: List of tuples (doc_id, position, word, word_lower, lemma, pos, genre, corpus)
        batch_size: Batch size for inserts

    Returns:
        Number of tokens inserted
    """
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO tokens
        (doc_id, position, word, word_lower, lemma, pos, genre, corpus)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, batch)

    conn.commit()
    return len(batch)


def load_wlp_file(
    filepath: Path,
    conn,
    corpus: str,
    genre: str,
    wlp_variant: str = 'standard'
) -> dict:
    """
    Load a WLP format file into database.

    Args:
        filepath: Path to WLP file
        conn: SQLite connection
        corpus: Corpus identifier (e.g., 'coca', 'brown')
        genre: Genre identifier (e.g., 'acad', 'fiction')
        wlp_variant: 'standard' (4-column) or 'brown' (3-column)

    Returns:
        Dictionary with statistics
    """
    batch = []
    position = 0
    tokens_processed = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Parse line based on variant
            if wlp_variant == 'brown':
                result = parse_wlp_line_brown(line, line_num, filepath.name)
            else:
                result = parse_wlp_line_standard(line)

            if result:
                doc_id, word, lemma, pos = result
                word_lower = word.lower()

                batch.append((
                    doc_id, position, word, word_lower, lemma, pos, genre, corpus
                ))

                position += 1
                tokens_processed += 1

                # Batch insert when batch is full
                if len(batch) >= 10000:
                    batch_insert_tokens(conn, batch)
                    batch = []

    # Insert remaining batch
    if batch:
        batch_insert_tokens(conn, batch)

    return {
        'tokens': tokens_processed,
        'file': str(filepath),
        'corpus': corpus,
        'genre': genre
    }


# Example usage
if __name__ == '__main__':
    import sqlite3

    # Standard COCA format
    db_path = Path('coca_index.db')
    conn = sqlite3.connect(str(db_path))

    file_path = Path('coca-samples-wlp/wlp_acad.txt')
    stats = load_wlp_file(
        file_path,
        conn,
        corpus='coca',
        genre='acad',
        wlp_variant='standard'
    )

    print(f"Loaded {stats['tokens']} tokens from {stats['file']}")

    # Brown corpus format (3-column)
    file_path = Path('brown-corpus/wlp_adventure.txt')
    stats = load_wlp_file(
        file_path,
        conn,
        corpus='brown',
        genre='adventure',
        wlp_variant='brown'
    )

    print(f"Loaded {stats['tokens']} tokens from {stats['file']}")

    conn.close()
