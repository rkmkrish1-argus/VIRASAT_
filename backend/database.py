"""
Database Interface for Ambedkar Digital Heritage Archive
"""

import sqlite3
import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "ambedkar_archive_data" / "database" / "ambedkar_archive.db"

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def get_archive_stats() -> Dict[str, Any]:
    """Retrieve aggregate statistics from archive database."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*), SUM(word_count) FROM documents;")
    total_docs, total_words = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM chunks_for_embeddings;")
    total_chunks = cur.fetchone()[0]

    cur.execute("SELECT language, COUNT(*) FROM documents GROUP BY language ORDER BY COUNT(*) DESC;")
    languages = dict(cur.fetchall())

    cur.execute("SELECT type, COUNT(*) FROM documents GROUP BY type ORDER BY COUNT(*) DESC;")
    types = dict(cur.fetchall())

    cur.execute("SELECT source, COUNT(*) FROM documents GROUP BY source ORDER BY COUNT(*) DESC;")
    sources = dict(cur.fetchall())

    cur.execute("SELECT language, source, COUNT(*) FROM documents GROUP BY language, source;")
    languages_by_source: Dict[str, Dict[str, int]] = {}
    for language, source, count in cur.fetchall():
        languages_by_source.setdefault(language, {})[source] = count

    conn.close()
    return {
        "total_documents": total_docs or 0,
        "total_words_indexed": total_words or 0,
        "total_embedding_chunks": total_chunks or 0,
        "languages": languages,
        "languages_by_source": languages_by_source,
        "types": types,
        "sources": sources
    }

def search_documents(
    query_text: str,
    language: Optional[str] = None,
    doc_type: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Execute high-speed full text search using SQLite FTS5 index with filtering.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Escape FTS5 special characters if present
    sanitized_q = "".join([c for c in query_text if c.isalnum() or c.isspace()]).strip()
    if not sanitized_q:
        sanitized_q = "*"

    filters = []
    params = []

    if language:
        filters.append("d.language = ?")
        params.append(language)
    if doc_type:
        filters.append("d.type = ?")
        params.append(doc_type)
    if source:
        filters.append("d.source = ?")
        params.append(source)

    where_clause = ""
    if filters:
        where_clause = "AND " + " AND ".join(filters)

    # Count total matches
    if sanitized_q == "*":
        count_sql = f"SELECT COUNT(*) FROM documents d WHERE 1=1 {where_clause}"
        cur.execute(count_sql, params)
        total_count = cur.fetchone()[0]

        select_sql = f"""
            SELECT d.id, d.title, d.author, d.date, d.type, d.language, d.source, d.summary, d.tags, d.archive_reference
            FROM documents d
            WHERE 1=1 {where_clause}
            ORDER BY d.date DESC
            LIMIT ? OFFSET ?;
        """
        cur.execute(select_sql, params + [limit, offset])
    else:
        fts_param = f'"{sanitized_q}"*'
        count_sql = f"""
            SELECT COUNT(*)
            FROM documents d
            JOIN documents_fts fts ON d.id = fts.id
            WHERE documents_fts MATCH ? {where_clause}
        """
        cur.execute(count_sql, [fts_param] + params)
        total_count = cur.fetchone()[0]

        select_sql = f"""
            SELECT d.id, d.title, d.author, d.date, d.type, d.language, d.source, d.summary, d.tags, d.archive_reference
            FROM documents d
            JOIN documents_fts fts ON d.id = fts.id
            WHERE documents_fts MATCH ? {where_clause}
            ORDER BY rank
            LIMIT ? OFFSET ?;
        """
        cur.execute(select_sql, [fts_param] + params + [limit, offset])

    rows = cur.fetchall()
    results = []
    for r in rows:
        tags = [t.strip() for t in (r["tags"] or "").split(",") if t.strip()]
        results.append({
            "id": r["id"],
            "title": r["title"],
            "author": r["author"],
            "date": r["date"],
            "type": r["type"],
            "language": r["language"],
            "source": r["source"],
            "summary": r["summary"] or "",
            "tags": tags,
            "url": f"https://archive.org/details/{r['archive_reference']}" if r["source"] == "IA" else r["archive_reference"]
        })

    conn.close()
    return total_count, results


def retrieve_archive_sources(question: str, limit: int = 5) -> List[Dict[str, Any]]:
    stop_words = {
        "about", "after", "ambedkar", "and", "are", "can", "could", "did",
        "does", "for", "from", "give", "his", "how", "into", "me", "please",
        "said", "support", "tell", "that", "the", "their", "them", "there", "this", "was",
        "what", "when", "where", "which", "who", "why", "with", "would",
        "instead", "system",
    }
    terms = [
        token for token in re.findall(r"[^\W_]+", question.casefold(), flags=re.UNICODE)
        if len(token) > 2 and token not in stop_words
    ][:12]
    if not terms:
        terms = re.findall(r"[^\W_]+", question.casefold(), flags=re.UNICODE)[:5]
    if not terms:
        return []

    match_expression = " OR ".join(f'"{term}"*' for term in terms)
    conn = get_db_connection()
    try:
        rows = conn.execute("""
            SELECT d.id, d.title, d.author, d.date, d.type, d.language, d.source,
                   d.archive_reference,
                   d.summary, d.full_text,
                   COALESCE(
                       NULLIF(snippet(documents_fts, 3, '', '', ' ... ', 36), ''),
                       NULLIF(d.summary, ''),
                       substr(d.full_text, 1, 500)
                   ) AS excerpt
            FROM documents_fts
            JOIN documents d ON d.id = documents_fts.id
            WHERE documents_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (match_expression, max(10, min(limit * 5, 25)))).fetchall()

        minimum_matches = max(1, math.ceil(len(terms) * 0.4))
        results = []
        for row in rows:
            record = dict(row)
            record["url"] = record.get("archive_reference")
            searchable_text = " ".join((record["title"] or "", record["summary"] or "", record["full_text"] or ""))
            searchable_terms = set(re.findall(r"[^\W_]+", searchable_text.casefold(), flags=re.UNICODE))
            if sum(term in searchable_terms for term in terms) < minimum_matches:
                continue
            record.pop("full_text", None)
            record.pop("summary", None)
            results.append(record)
            if len(results) >= max(1, min(limit, 5)):
                break
        return results
    finally:
        conn.close()

def get_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    """Fetch complete document wrapper by ID."""
    try:
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT raw_json FROM documents WHERE id = ?;", (doc_id,))
            row = cur.fetchone()
            if row and row["raw_json"]:
                return json.loads(row["raw_json"])
        finally:
            conn.close()
    except (sqlite3.Error, json.JSONDecodeError):
        # Continue to the processed archive if the database is missing or stale.
        pass

    # The processed archive is the canonical source for a record. Keeping this
    # fallback lets document links work even when the SQLite index is stale or
    # has not been built on this installation yet.
    processed_dir = PROJECT_ROOT / "ambedkar_archive_data" / "processed_data"
    processed_path = (processed_dir / f"{doc_id}.json").resolve()
    if processed_path.parent == processed_dir.resolve() and processed_path.is_file():
        try:
            with processed_path.open("r", encoding="utf-8") as document_file:
                return json.load(document_file)
        except (OSError, json.JSONDecodeError):
            return None
    return None
