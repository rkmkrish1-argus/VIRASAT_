"""
Core Ingestion Engine
Persists standardized documents to JSON storage, CSV registry, and an ACID SQLite
database with FTS5 Full-Text Search indexing and embedding-ready chunk tables.
"""

import json
import sqlite3
import logging
from typing import List, Dict, Any
import pandas as pd

from config import (
    PROCESSED_DATA_DIR,
    METADATA_DIR,
    TEXTS_DIR,
    REGISTRY_JSON_PATH,
    COMBINED_METADATA_CSV_PATH,
    DATA_INVENTORY_REPORT_PATH,
    SQLITE_DB_PATH,
    init_directories
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def setup_sqlite_database(db_path: str = str(SQLITE_DB_PATH)) -> sqlite3.Connection:
    """Initialize SQLite database with standard tables and FTS5 search index."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Main documents table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            date TEXT,
            type TEXT NOT NULL,
            language TEXT NOT NULL,
            source TEXT NOT NULL,
            archive_reference TEXT,
            collection TEXT,
            pages INTEGER,
            word_count INTEGER,
            summary TEXT,
            full_text TEXT,
            tags TEXT,
            translations_json TEXT,
            media_json TEXT,
            raw_json TEXT
        );
    """)

    # FTS5 Virtual Table for sub-millisecond full-text search
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            id UNINDEXED,
            title,
            summary,
            full_text,
            tags,
            tokenize = 'porter unicode61'
        );
    """)

    # Embedding-ready text chunks table for vector search / RAG
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunks_for_embeddings (
            chunk_id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            text_chunk TEXT NOT NULL,
            token_count INTEGER,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        );
    """)

    conn.commit()
    return conn

def chunk_text(text: str, chunk_size_words: int = 250, overlap_words: int = 50) -> List[str]:
    """Split long text into overlapping chunks for semantic embeddings."""
    words = text.split()
    if not words:
        return []
    chunks = []
    step = chunk_size_words - overlap_words
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size_words])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def ingest_documents(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ingest standardized records into JSON, CSV, and SQLite database with FTS5.
    """
    init_directories()
    logger.info(f"Starting ingestion of {len(documents)} documents...")

    conn = setup_sqlite_database()
    cur = conn.cursor()

    # Clear previous run data
    cur.execute("DELETE FROM documents;")
    cur.execute("DELETE FROM documents_fts;")
    cur.execute("DELETE FROM chunks_for_embeddings;")

    csv_rows = []
    sources_count: Dict[str, int] = {}
    types_count: Dict[str, int] = {}
    languages_count: Dict[str, int] = {}
    total_words = 0
    total_chunks = 0

    for doc_wrapper in documents:
        doc = doc_wrapper["document"]
        doc_id = doc["id"]
        title = doc["title"]
        author = doc["author"]
        date = doc["date"]
        doc_type = doc["type"]
        lang = doc["language"]

        content = doc["content"]
        summary = content.get("summary", "")
        full_text = content.get("full_text", "")
        quotes = content.get("key_quotes", [])

        metadata = doc["metadata"]
        source = metadata.get("source", "IA")
        archive_ref = metadata.get("archive_reference", "")
        collection = metadata.get("collection", "")
        pages = metadata.get("pages", 1)
        word_count = metadata.get("word_count", len(full_text.split()))
        condition = metadata.get("condition", "good")
        accessibility = metadata.get("accessibility", "public")
        url = metadata.get("url", "")

        tags = doc.get("tags", [])
        tags_str = ", ".join(tags)

        # Update stats
        sources_count[source] = sources_count.get(source, 0) + 1
        types_count[doc_type] = types_count.get(doc_type, 0) + 1
        languages_count[lang] = languages_count.get(lang, 0) + 1
        total_words += word_count

        # Write individual processed JSON
        proc_file = PROCESSED_DATA_DIR / f"{doc_id}.json"
        with open(proc_file, "w", encoding="utf-8") as f:
            json.dump(doc_wrapper, f, ensure_ascii=False, indent=2)

        # Write text copy if full text exists
        if len(full_text) > 300:
            text_file = TEXTS_DIR / f"{doc_id}.txt"
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\nAuthor: {author}\nDate: {date}\n\n{full_text}")

        # Insert into SQLite documents table
        cur.execute("""
            INSERT INTO documents (
                id, title, author, date, type, language, source,
                archive_reference, collection, pages, word_count,
                summary, full_text, tags, translations_json, media_json, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_id, title, author, date, doc_type, lang, source,
            archive_ref, collection, pages, word_count,
            summary, full_text, tags_str,
            json.dumps(doc.get("translations", {}), ensure_ascii=False),
            json.dumps(doc.get("media", {}), ensure_ascii=False),
            json.dumps(doc_wrapper, ensure_ascii=False)
        ))

        # Insert into FTS5 virtual table
        cur.execute("""
            INSERT INTO documents_fts (id, title, summary, full_text, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (doc_id, title, summary, full_text, tags_str))

        # Generate text chunks for vector RAG embedding
        chunks = chunk_text(full_text)
        for idx, ch in enumerate(chunks):
            chunk_id = f"{doc_id}_chk_{idx:03d}"
            cur.execute("""
                INSERT INTO chunks_for_embeddings (chunk_id, doc_id, chunk_index, text_chunk, token_count)
                VALUES (?, ?, ?, ?, ?)
            """, (chunk_id, doc_id, idx, ch, len(ch.split())))
            total_chunks += 1

        # Tabular metadata row
        csv_rows.append({
            "id": doc_id,
            "title": title,
            "author": author,
            "date": date,
            "type": doc_type,
            "language": lang,
            "source": source,
            "archive_reference": archive_ref,
            "collection": collection,
            "pages": pages,
            "word_count": word_count,
            "condition": condition,
            "accessibility": accessibility,
            "tags": tags_str,
            "url": url
        })

    conn.commit()
    conn.close()
    logger.info("Database transactions committed successfully.")

    # Save registry.json
    registry_data = {
        "created": pd.Timestamp.now().isoformat(),
        "total_items": len(documents),
        "total_words_indexed": total_words,
        "total_embedding_chunks": total_chunks,
        "sources": sources_count,
        "types": types_count,
        "languages": languages_count,
        "database": str(SQLITE_DB_PATH),
        "data": documents
    }

    with open(REGISTRY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, ensure_ascii=False, indent=2)
    logger.info(f"Generated master registry: {REGISTRY_JSON_PATH}")

    # Save combined_metadata.csv
    df_meta = pd.DataFrame(csv_rows)
    df_meta.to_csv(COMBINED_METADATA_CSV_PATH, index=False, encoding="utf-8")
    logger.info(f"Generated combined metadata CSV: {COMBINED_METADATA_CSV_PATH}")

    # Save data_inventory_report.json
    inventory_report = {
        "report_name": "Dr. B.R. Ambedkar Digital Heritage Archive - Data Inventory",
        "problem_statement_id": "26096",
        "ministry": "Ministry of Social Justice and Empowerment (MoSJE)",
        "primary_institution": "Dr. Ambedkar International Centre (DAIC)",
        "timestamp": pd.Timestamp.now().isoformat(),
        "total_documents": len(documents),
        "total_words_indexed": total_words,
        "total_embedding_chunks": total_chunks,
        "breakdown_by_source": sources_count,
        "breakdown_by_type": types_count,
        "breakdown_by_language": languages_count,
        "sqlite_db": {
            "path": str(SQLITE_DB_PATH),
            "tables": ["documents", "documents_fts", "chunks_for_embeddings"]
        },
        "status": "INGESTION_COMPLETE_READY_FOR_BACKEND_AND_KIOSK"
    }

    with open(DATA_INVENTORY_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(inventory_report, f, ensure_ascii=False, indent=2)
    logger.info(f"Generated inventory report: {DATA_INVENTORY_REPORT_PATH}")

    return inventory_report
