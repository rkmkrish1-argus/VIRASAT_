"""
Database Interface for Ambedkar Digital Heritage Archive
Supports document search, FTS5 indexing, Constitutional Ideas research graph,
document-to-document relationships, and OCR contributions.
"""

import sqlite3
import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "ambedkar_archive_data" / "database" / "ambedkar_archive.db"

# Ensure parent folder exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_extended_tables():
    """Create constitutional_ideas, document_relations, and ocr_contributions tables."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Main documents table (if missing)
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

    # 2. FTS5 Virtual Table
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

    # 3. Constitutional Ideas Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS constitutional_ideas (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            key_articles TEXT,
            famous_quote TEXT,
            icon TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 4. Document Relations Table (Links between documents & records)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS document_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_doc_id TEXT NOT NULL,
            target_doc_id TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            description TEXT,
            researcher TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_doc_id) REFERENCES documents(id),
            FOREIGN KEY (target_doc_id) REFERENCES documents(id)
        );
    """)

    # 5. Idea to Document Mapping Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS idea_document_relations (
            idea_id TEXT NOT NULL,
            doc_id TEXT NOT NULL,
            relevance_note TEXT,
            PRIMARY KEY (idea_id, doc_id),
            FOREIGN KEY (idea_id) REFERENCES constitutional_ideas(id),
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        );
    """)

    # 6. OCR Contributions Table (Includes 5MB enforced uploads & Source Description)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ocr_contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id TEXT,
            filename TEXT NOT NULL,
            user_role TEXT NOT NULL,
            ocr_mode TEXT NOT NULL,
            model_used TEXT NOT NULL,
            file_size_bytes INTEGER NOT NULL,
            source_date TEXT,
            source_name TEXT,
            source_author TEXT,
            researcher_name TEXT,
            source_description_label TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()

    # Seed Constitutional Ideas if empty
    cur.execute("SELECT COUNT(*) FROM constitutional_ideas;")
    if cur.fetchone()[0] == 0:
        _seed_constitutional_ideas(cur)
        conn.commit()

    conn.close()

def _seed_constitutional_ideas(cur: sqlite3.Cursor):
    """Seed foundational constitutional ideas formulated by Dr. B.R. Ambedkar."""
    ideas = [
        (
            "IDEA_CONST_MORALITY",
            "Constitutional Morality & Grammar of Anarchy",
            "Democratic Philosophy",
            "Constitutional morality is not a natural sentiment; it has to be cultivated. We must abandon bloody methods of revolution, civil disobedience, and non-cooperation, calling them the Grammar of Anarchy.",
            "Article 1, Article 32, Preamble",
            "However good a Constitution may be, it is sure to turn out bad because those who are called to work it, happen to be a bad lot.",
            "fa-scale-balanced"
        ),
        (
            "IDEA_SOCIAL_DEMOCRACY",
            "Social Democracy & Economic Equality",
            "Socio-Economic Rights",
            "Political democracy cannot last unless there lies at the base of it social democracy. Social democracy means a way of life which recognizes liberty, equality, and fraternity as the principles of life.",
            "Article 14, Article 15, Article 38, Article 39",
            "On the 26th of January 1950, we are going to enter into a life of contradictions. In politics we will have equality and in social and economic life we will have inequality.",
            "fa-users-line"
        ),
        (
            "IDEA_UNTOUCHABILITY_ABOLITION",
            "Abolition of Untouchability & Equal Civic Access",
            "Fundamental Rights",
            "Universal civic rights to water, public places, and dignity asserted during the Mahad Satyagraha (1927), enshrined permanently as a constitutional command penalizing untouchability.",
            "Article 15(2), Article 17, Article 23",
            "Lost rights are never regained by begging, but by relentless struggle.",
            "fa-hand-fist"
        ),
        (
            "IDEA_MONETARY_SOVEREIGNTY",
            "Monetary Policy, Currency & Central Banking",
            "Economic Jurisprudence",
            "Seminal economic framework established in 'The Problem of the Rupee' (1923), defining gold standard stabilization, price control, and institutional structure for the Reserve Bank of India.",
            "Article 280, Article 110, Seventh Schedule",
            "The problem of the rupee is a problem of currency stabilization and price control for the protection of labouring masses.",
            "fa-coins"
        ),
        (
            "IDEA_GENDER_JUSTICE",
            "Gender Equality & Hindu Code Reforms",
            "Civil Rights & Family Law",
            "Pioneering advocacy for women's property rights, equal inheritance, divorce laws, and maternity benefits, leading to the landmark Hindu Code Bill and labor welfare codes.",
            "Article 14, Article 15(3), Article 39(d), Article 42",
            "I measure the progress of a community by the degree of progress which women have achieved.",
            "fa-venus-mars"
        ),
        (
            "IDEA_JUDICIAL_REMEDIES",
            "Heart and Soul of the Constitution (Article 32)",
            "Constitutional Remedies",
            "Article 32 provides the right to move the Supreme Court by appropriate proceedings for enforcement of Fundamental Rights, making rights real and justiciable rather than nominal.",
            "Article 32, Article 226",
            "If I were asked to name any particular article in this Constitution as the most important—an article without which this Constitution would be a nullity—I could not refer to any other article except Article 32.",
            "fa-gavel"
        ),
        (
            "IDEA_FLEXIBLE_FEDERALISM",
            "Flexible Federalism & State Rights",
            "Constitutional Structure",
            "India is a Union of States. The Constitution creates a dual polity with single citizenship, designed to be federal in normal times and unitary during national emergencies.",
            "Article 1, Article 355, Article 356, Seventh Schedule",
            "The Constitution is a Federal Constitution in as much as it establishes what may be called a Dual Polity.",
            "fa-landmark-flag"
        )
    ]

    for item in ideas:
        cur.execute("""
            INSERT OR IGNORE INTO constitutional_ideas
            (id, title, category, description, key_articles, famous_quote, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, item)

    # Seed default relations
    relations = [
        ("DOC_CAD_CAD_VOL11_19491125", "DOC_DAF_BAWS_PUB_1916_CII", "expands_on", "Applies principles of social inequality defined in 1916 paper to final Constituent Assembly warning in 1949.", "Dr. B.R. Ambedkar"),
        ("DOC_CAD_CAD_VOL07_19481129", "DOC_DAF_BAWS_SPEECH_1927_MSD", "constitutional_realization", "Draft Article 11 (Article 17) directly translates the Mahad Satyagraha water struggle into fundamental rights law.", "DAIC Research Cell"),
        ("DOC_DAF_BAWS_PUB_1923_POR", "DOC_DAF_BAWS_PUB_1925_EPF", "theoretical_foundation", "Establishes economic monetary stabilization principles supporting provincial financial division.", "DAIC Research Cell"),
        ("DOC_CAD_CAD_VOL07_19481104", "DOC_CAD_CAD_VOL11_19491125", "drafting_progression", "Initial introduction of draft Constitution connected to final 1949 adoption speech.", "Research Desk")
    ]

    for rel in relations:
        cur.execute("""
            INSERT INTO document_relations (source_doc_id, target_doc_id, relation_type, description, researcher)
            VALUES (?, ?, ?, ?, ?);
        """, rel)

    # Seed idea-document links
    idea_links = [
        ("IDEA_CONST_MORALITY", "DOC_CAD_CAD_VOL11_19491125", "Final speech delivered 25th November 1949 warning against Bhakti in politics."),
        ("IDEA_SOCIAL_DEMOCRACY", "DOC_DAF_BAWS_PUB_1936_AOC", "Annihilation of Caste lays the foundation for social democracy."),
        ("IDEA_UNTOUCHABILITY_ABOLITION", "DOC_CAD_CAD_VOL07_19481129", "Unanimous adoption of Article 17 outlawing untouchability."),
        ("IDEA_MONETARY_SOVEREIGNTY", "DOC_DAF_BAWS_PUB_1923_POR", "D.Sc. dissertation presented at London School of Economics."),
        ("IDEA_JUDICIAL_REMEDIES", "DOC_CAD_CAD_VOL07_19481104", "Debate on fundamental rights enforcement under Article 32.")
    ]

    for il in idea_links:
        cur.execute("""
            INSERT OR IGNORE INTO idea_document_relations (idea_id, doc_id, relevance_note)
            VALUES (?, ?, ?);
        """, il)


# Auto-initialize database schema upon module import
init_extended_tables()


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
    """Execute high-speed full text search using SQLite FTS5 index with filtering."""
    conn = get_db_connection()
    cur = conn.cursor()

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
        pass

    processed_dir = PROJECT_ROOT / "ambedkar_archive_data" / "processed_data"
    processed_path = (processed_dir / f"{doc_id}.json").resolve()
    if processed_path.parent == processed_dir.resolve() and processed_path.is_file():
        try:
            with processed_path.open("r", encoding="utf-8") as document_file:
                return json.load(document_file)
        except (OSError, json.JSONDecodeError):
            return None
    return None

# --- NEW CONSTITUTIONAL IDEAS & RELATIONS API FUNCTIONS ---

def get_all_constitutional_ideas() -> List[Dict[str, Any]]:
    """Fetch all constitutional ideas with linked documents."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM constitutional_ideas ORDER BY id ASC;")
    ideas = [dict(row) for row in cur.fetchall()]

    for idea in ideas:
        cur.execute("""
            SELECT d.id, d.title, d.date, d.type, d.source, r.relevance_note
            FROM idea_document_relations r
            JOIN documents d ON r.doc_id = d.id
            WHERE r.idea_id = ?;
        """, (idea["id"],))
        idea["linked_documents"] = [dict(r) for r in cur.fetchall()]

    conn.close()
    return ideas

def get_document_relations(doc_id: str) -> List[Dict[str, Any]]:
    """Fetch all outgoing and incoming document relations for a given document."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT r.id, r.source_doc_id, r.target_doc_id, r.relation_type, r.description, r.researcher, r.created_at,
               d1.title AS source_title, d2.title AS target_title,
               d1.date AS source_date, d2.date AS target_date
        FROM document_relations r
        JOIN documents d1 ON r.source_doc_id = d1.id
        JOIN documents d2 ON r.target_doc_id = d2.id
        WHERE r.source_doc_id = ? OR r.target_doc_id = ?
        ORDER BY r.created_at DESC;
    """, (doc_id, doc_id))
    
    relations = [dict(row) for row in cur.fetchall()]
    conn.close()
    return relations

def add_document_relation(
    source_doc_id: str,
    target_doc_id: str,
    relation_type: str,
    description: str,
    researcher: str
) -> Dict[str, Any]:
    """Add a new document relationship to the database (Researcher access)."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO document_relations (source_doc_id, target_doc_id, relation_type, description, researcher)
        VALUES (?, ?, ?, ?, ?);
    """, (source_doc_id, target_doc_id, relation_type, description, researcher))
    
    rel_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": rel_id,
        "source_doc_id": source_doc_id,
        "target_doc_id": target_doc_id,
        "relation_type": relation_type,
        "description": description,
        "researcher": researcher,
        "status": "created"
    }

def record_ocr_contribution(
    doc_id: Optional[str],
    filename: str,
    user_role: str,
    ocr_mode: str,
    model_used: str,
    file_size_bytes: int,
    source_date: str,
    source_name: str,
    source_author: str,
    researcher_name: str,
    extracted_text: str
) -> Dict[str, Any]:
    """Record an OCR contribution with Source Description metadata and 5MB limit validation."""
    source_description_label = f"Dt: {source_date} | Source: {source_name} | Author: {source_author} | Researcher: {researcher_name}"
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ocr_contributions (
            doc_id, filename, user_role, ocr_mode, model_used, file_size_bytes,
            source_date, source_name, source_author, researcher_name,
            source_description_label, extracted_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        doc_id, filename, user_role, ocr_mode, model_used, file_size_bytes,
        source_date, source_name, source_author, researcher_name,
        source_description_label, extracted_text
    ))
    contrib_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": contrib_id,
        "source_description_label": source_description_label,
        "filename": filename,
        "user_role": user_role,
        "ocr_mode": ocr_mode,
        "model_used": model_used,
        "file_size_bytes": file_size_bytes,
        "status": "recorded"
    }
