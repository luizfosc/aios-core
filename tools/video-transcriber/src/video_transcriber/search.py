"""Search index — SQLite FTS5 full-text search for transcriptions.

Indexes transcriptions with metadata for instant full-text search
across all processed videos. Uses Python's built-in sqlite3 module.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from .models import Segment, _fmt_time


DEFAULT_DB_NAME = "vt-search.db"


@dataclass
class SearchResult:
    """A single search result."""

    title: str
    source_path: str
    snippet: str
    timestamp: float
    timestamp_formatted: str
    rank: float

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "source_path": self.source_path,
            "snippet": self.snippet,
            "timestamp": self.timestamp,
            "timestamp_formatted": self.timestamp_formatted,
            "rank": self.rank,
        }


class SearchIndex:
    """SQLite FTS5-backed search index for transcriptions."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._init_schema()
        return self._conn

    def _init_schema(self) -> None:
        conn = self._conn
        assert conn is not None

        # Main documents table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source_path TEXT NOT NULL UNIQUE,
                language TEXT DEFAULT '',
                model TEXT DEFAULT '',
                word_count INTEGER DEFAULT 0,
                segment_count INTEGER DEFAULT 0,
                indexed_at TEXT NOT NULL
            )
        """)

        # Segments table with timestamps
        conn.execute("""
            CREATE TABLE IF NOT EXISTS segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE
            )
        """)

        # FTS5 virtual table for full-text search
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS segments_fts USING fts5(
                text,
                content='segments',
                content_rowid='id',
                tokenize='unicode61'
            )
        """)

        # Triggers to keep FTS in sync
        conn.executescript("""
            CREATE TRIGGER IF NOT EXISTS segments_ai AFTER INSERT ON segments BEGIN
                INSERT INTO segments_fts(rowid, text)
                VALUES (new.id, new.text);
            END;

            CREATE TRIGGER IF NOT EXISTS segments_ad AFTER DELETE ON segments BEGIN
                INSERT INTO segments_fts(segments_fts, rowid, text)
                VALUES ('delete', old.id, old.text);
            END;

            CREATE TRIGGER IF NOT EXISTS segments_au AFTER UPDATE ON segments BEGIN
                INSERT INTO segments_fts(segments_fts, rowid, text)
                VALUES ('delete', old.id, old.text);
                INSERT INTO segments_fts(rowid, text)
                VALUES (new.id, new.text);
            END;
        """)
        conn.commit()

    def index_transcription(
        self,
        segments: list[Segment],
        *,
        title: str,
        source_path: str,
        language: str = "",
        model: str = "",
    ) -> int:
        """Index a transcription's segments for full-text search.

        If the source_path already exists, it is replaced.

        Args:
            segments: Cleaned transcription segments.
            title: Document title.
            source_path: Path or URL of the source.
            language: Language code.
            model: Whisper model used.

        Returns:
            Number of segments indexed.
        """
        conn = self._get_conn()
        speech_segs = [s for s in segments if s.type == "speech" and s.text.strip()]
        word_count = sum(len(s.text.split()) for s in speech_segs)

        # Remove existing document if re-indexing
        existing = conn.execute(
            "SELECT id FROM documents WHERE source_path = ?",
            (source_path,),
        ).fetchone()
        if existing:
            doc_id = existing[0]
            conn.execute("DELETE FROM segments WHERE doc_id = ?", (doc_id,))
            conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))

        # Insert document
        cursor = conn.execute(
            """INSERT INTO documents (title, source_path, language, model,
               word_count, segment_count, indexed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, source_path, language, model, word_count,
             len(speech_segs), datetime.now().isoformat()),
        )
        doc_id = cursor.lastrowid

        # Insert segments
        for seg in speech_segs:
            conn.execute(
                "INSERT INTO segments (doc_id, start_time, end_time, text) VALUES (?, ?, ?, ?)",
                (doc_id, seg.start, seg.end, seg.text.strip()),
            )

        conn.commit()
        return len(speech_segs)

    def search(
        self,
        query: str,
        *,
        limit: int = 20,
    ) -> list[SearchResult]:
        """Search indexed transcriptions using FTS5.

        Args:
            query: Search query (supports FTS5 syntax: AND, OR, NOT, "phrases").
            limit: Maximum results.

        Returns:
            List of SearchResult objects sorted by relevance.
        """
        conn = self._get_conn()

        results: list[SearchResult] = []
        rows = conn.execute(
            """
            SELECT
                d.title,
                d.source_path,
                snippet(segments_fts, 0, '>>>', '<<<', '...', 32) as snippet,
                s.start_time,
                rank
            FROM segments_fts
            JOIN segments s ON s.id = segments_fts.rowid
            JOIN documents d ON d.id = s.doc_id
            WHERE segments_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()

        for row in rows:
            results.append(SearchResult(
                title=row[0],
                source_path=row[1],
                snippet=row[2],
                timestamp=row[3],
                timestamp_formatted=_fmt_time(row[3]),
                rank=row[4],
            ))

        return results

    def stats(self) -> dict:
        """Get index statistics."""
        conn = self._get_conn()
        doc_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        seg_count = conn.execute("SELECT COUNT(*) FROM segments").fetchone()[0]
        total_words = conn.execute(
            "SELECT COALESCE(SUM(word_count), 0) FROM documents"
        ).fetchone()[0]
        return {
            "documents": doc_count,
            "segments": seg_count,
            "total_words": total_words,
            "db_path": str(self.db_path),
            "db_size_mb": round(self.db_path.stat().st_size / (1024 * 1024), 2)
            if self.db_path.exists() else 0,
        }

    def list_documents(self) -> list[dict]:
        """List all indexed documents."""
        conn = self._get_conn()
        rows = conn.execute(
            """SELECT title, source_path, language, word_count,
                      segment_count, indexed_at
               FROM documents ORDER BY indexed_at DESC"""
        ).fetchall()
        return [
            {
                "title": r[0],
                "source_path": r[1],
                "language": r[2],
                "word_count": r[3],
                "segment_count": r[4],
                "indexed_at": r[5],
            }
            for r in rows
        ]

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> SearchIndex:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
