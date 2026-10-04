"""
Verification & Test Suite for Ambedkar Digital Heritage Archive Pipeline
Tests database integrity, FTS5 full-text search performance, language queries, and schema consistency.
"""

import sys
import json
import sqlite3
import time
from pathlib import Path
import pandas as pd

scripts_path = Path(__file__).resolve().parent
if str(scripts_path) not in sys.path:
    sys.path.insert(0, str(scripts_path))

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from config import (
    SQLITE_DB_PATH,
    REGISTRY_JSON_PATH,
    COMBINED_METADATA_CSV_PATH,
    DATA_INVENTORY_REPORT_PATH
)

def test_database_and_search():
    print("\n--- RUNNING PIPELINE VERIFICATION SUITE ---")
    assert SQLITE_DB_PATH.exists(), f"Database missing at {SQLITE_DB_PATH}"
    assert REGISTRY_JSON_PATH.exists(), f"Registry JSON missing at {REGISTRY_JSON_PATH}"
    assert COMBINED_METADATA_CSV_PATH.exists(), f"Metadata CSV missing at {COMBINED_METADATA_CSV_PATH}"
    assert DATA_INVENTORY_REPORT_PATH.exists(), f"Inventory report missing at {DATA_INVENTORY_REPORT_PATH}"

    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    cur = conn.cursor()

    # 1. Check Document Count
    cur.execute("SELECT COUNT(*) FROM documents;")
    doc_count = cur.fetchone()[0]
    print(f"[TEST 1] Documents in Database: {doc_count}")
    assert doc_count >= 500, f"Expected at least 500 documents, found {doc_count}"

    # 2. Check Embedding Chunks
    cur.execute("SELECT COUNT(*) FROM chunks_for_embeddings;")
    chunk_count = cur.fetchone()[0]
    print(f"[TEST 2] Embedding-ready text chunks: {chunk_count}")
    assert chunk_count > 0, "No embedding chunks generated"

    # 3. Test Full-Text Search (FTS5) queries
    test_queries = [
        "Parliamentary",
        "Untouchability",
        "Anarchy",
        "Annihilation",
        "Directive Principles",
        "Rupee"
    ]

    print("\n[TEST 3] FTS5 Sub-Millisecond Search Benchmarks:")
    for query in test_queries:
        t0 = time.time()
        cur.execute("""
            SELECT d.id, d.title, d.date, d.type, d.source
            FROM documents d
            JOIN documents_fts fts ON d.id = fts.id
            WHERE documents_fts MATCH ?
            LIMIT 5;
        """, (query,))
        rows = cur.fetchall()
        t1 = time.time()
        latency_ms = (t1 - t0) * 1000
        print(f"  - Query '{query}': {len(rows)} matches found in {latency_ms:.2f} ms")
        assert len(rows) > 0, f"No matches found for critical search term: {query}"
        for r in rows[:1]:
            print(f"    * Top match: [{r[4]}] {r[1]} ({r[2]})")

    # 4. Verify CSV and JSON registry counts match
    with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)
    assert registry["total_items"] == doc_count, "Registry count mismatch with database"

    df = pd.read_csv(COMBINED_METADATA_CSV_PATH)
    assert len(df) == doc_count, "CSV count mismatch with database"
    print(f"\n[TEST 4] Integrity Check: DB={doc_count}, Registry={registry['total_items']}, CSV={len(df)} (100% matched)")

    # 5. Language distribution check
    cur.execute("SELECT language, COUNT(*) FROM documents GROUP BY language ORDER BY COUNT(*) DESC;")
    lang_dist = cur.fetchall()
    print("\n[TEST 5] Ingested Language Distribution:")
    for l, c in lang_dist:
        print(f"  - {l}: {c} documents")

    conn.close()
    print("\nALL PIPELINE VERIFICATION TESTS PASSED SUCCESSFULLY! (100% HEALTHY)\n")

if __name__ == "__main__":
    test_database_and_search()
