"""
FastAPI Server for Dr. B.R. Ambedkar Digital Heritage Archive (PS 26096)
Provides search, filtering, document inspection, statistics, and dynamic ingestion.
"""

import time
import json
import logging
import os
import re
import urllib.error
import urllib.request
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .models import (
    SearchQuery,
    SearchResponse,
    StatsResponse,
    DocumentWrapper
)
from .database import (
    get_archive_stats,
    retrieve_archive_sources,
    search_documents,
    get_document_by_id,
    get_db_connection
)
from .ocr import (
    HANDWRITTEN_MODEL,
    OCRInputError,
    OCRLanguageError,
    OCRUnavailableError,
    extract_text,
    handwritten_model_status,
)
from .source_ingestion import fetch_sources, NDLI_INFO_URL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ArchiveAPI")

app = FastAPI(
    title="Dr. B.R. Ambedkar Digital Heritage Archive API",
    description="Backend API for Problem Statement 26096 (MoSJE / Dr. Ambedkar International Centre)",
    version="1.0.0"
)

# CORS setup for Touch Kiosks, Web Portals, and Mobile Apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_ROOT / "ambedkar_archive_data"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
REGISTRY_PATH = BASE_DIR / "metadata" / "registry.json"
CSV_PATH = BASE_DIR / "metadata" / "combined_metadata.csv"
REPORT_PATH = BASE_DIR / "metadata" / "data_inventory_report.json"
ELEVENLABS_VOICE_ID = "Aano0MRpH01ekWzUtv60"
load_dotenv(Path(__file__).with_name("br.env"), override=False)


class NarrationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class AssistantRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)
    language: str = "en"


ASSISTANT_QUERY_TERMS = {
    "hi": {
        "जाति व्यवस्था": "caste", "जाति": "caste", "श्रमिकों": "labourers",
        "भक्ति": "bhakti", "व्यक्तिपूजा": "hero worship", "व्यक्ति पूजा": "hero worship", "संविधान": "constitution",
        "लोकतंत्र": "democracy", "समानता": "equality", "अस्पृश्यता": "untouchability",
        "अनुच्छेद": "article", "अधिकार": "rights", "रुपया": "rupee", "महाड": "mahad",
        "बौद्ध": "buddhism", "धम्म": "dhamma", "राष्ट्रपति": "presidential",
        "संसदीय": "parliamentary", "मुद्रा": "currency", "महिला": "women",
        "आरक्षण": "reservation", "राजनीति": "politics", "चेतावनी": "warning", "आंबेडकर": "Ambedkar", "सामाजिक न्याय": "social justice"
    },
    "mr": {
        "जातिव्यवस्था": "caste", "जात": "caste", "कामगारांची": "labourers",
        "भक्ती": "bhakti", "व्यक्तिपूजा": "hero worship", "संविधान": "constitution",
        "लोकशाही": "democracy", "समता": "equality", "अस्पृश्यता": "untouchability",
        "कलम": "article", "हक्क": "rights", "रुपया": "rupee", "महाड": "mahad",
        "बौद्ध": "buddhism", "धम्म": "dhamma", "राष्ट्रपती": "presidential",
        "संसदीय": "parliamentary", "चलन": "currency", "महिला": "women",
        "आरक्षण": "reservation", "राजकारण": "politics", "इशारा": "warning", "आंबेडकर": "Ambedkar", "सामाजिक न्याय": "social justice"
    }
}
ASSISTANT_QUERY_STOPWORDS = {
    "hi": {"क्या", "क्यों", "कैसे", "किस", "के", "की", "का", "में", "से", "और", "था", "है", "थे", "पर", "बताइए", "बताएं", "समझाइए"},
    "mr": {"काय", "का", "कसे", "कोण", "च्या", "ची", "चा", "मध्ये", "पासून", "आणि", "होते", "होता", "आहे", "होती", "वर", "सांगा", "समजावून"}
}


def normalize_assistant_query(question: str, language: str) -> str:
    normalized = question
    for word in sorted(ASSISTANT_QUERY_STOPWORDS.get(language, set()), key=len, reverse=True):
        normalized = re.sub(rf"(?<!\w){re.escape(word)}(?!\w)", " ", normalized, flags=re.IGNORECASE)
    for term, english in sorted(ASSISTANT_QUERY_TERMS.get(language, {}).items(), key=lambda entry: len(entry[0]), reverse=True):
        normalized = re.sub(rf"(?<!\w){re.escape(term)}(?!\w)", english, normalized, flags=re.IGNORECASE)
    return " ".join(normalized.split())


ASSISTANT_COPY = {
    "en": {
        "empty": "I couldn't find matching records in the indexed archive. Try a different phrase or browse the archive. When matches are available, the excerpts below remain in their source language.",
        "found": "I found {count} relevant archive record(s).",
        "summary_heading": "Archive summaries:",
        "source_note": "The cited source excerpts below remain in their original language."
    },
    "hi": {
        "empty": "अनुक्रमित अभिलेखागार में इस प्रश्न से मेल खाते अभिलेख नहीं मिले। कोई दूसरा शब्द आज़माएँ या अभिलेखागार देखें। स्रोत उद्धरण मूल भाषा में ही दिखाए जाते हैं।",
        "found": "अभिलेखागार में {count} संबंधित अभिलेख मिले।",
        "summary_heading": "अभिलेखों का सार:",
        "source_note": "नीचे दिए गए उद्धृत स्रोत अंश मूल भाषा में हैं।"
    },
    "mr": {
        "empty": "अनुक्रमित अभिलेखात या प्रश्नाशी जुळणाऱ्या नोंदी सापडल्या नाहीत. वेगळे शब्द वापरून पाहा किंवा अभिलेखागार तपासा. स्रोत उतारे मूळ भाषेत दाखवले जातात.",
        "found": "अभिलेखागारात {count} संबंधित नोंदी सापडल्या.",
        "summary_heading": "नोंदींचा सारांश:",
        "source_note": "खालील उद्धृत स्रोत उतारे मूळ भाषेत आहेत."
    }
}

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/styles.css", include_in_schema=False)
async def serve_css():
    return FileResponse(FRONTEND_DIR / "styles.css", media_type="text/css")

@app.get("/app.js", include_in_schema=False)
async def serve_js():
    return FileResponse(FRONTEND_DIR / "app.js", media_type="application/javascript")

@app.get("/", tags=["Health & UI"])
async def root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "status": "healthy",
        "service": "Ambedkar Digital Heritage Archive API",
        "problem_statement_id": "26096",
        "ministry": "Ministry of Social Justice and Empowerment (MoSJE)",
        "primary_institution": "Dr. Ambedkar International Centre",
        "version": "1.0.0"
    }

@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "service": "Ambedkar Digital Heritage Archive API",
        "version": "1.0.0"
    }

@app.get("/api/sources", tags=["Source Catalogs"])
async def source_catalog_status():
    """Describe supported external catalogs and whether NDLI access is configured."""
    return {
        "sources": [
            {"id": "Foundation", "name": "Dr. Ambedkar Foundation", "catalog_url": "https://ambedkarfoundation.nic.in/publication.html", "access": "public_catalog_metadata"},
            {"id": "CAD", "name": "Constituent Assembly Debates / Parliament Digital Library", "catalog_url": "https://eparlib.sansad.in/handle/123456789/760448/browse?type=date", "access": "public_catalog_metadata"},
            {"id": "NDL", "name": "National Digital Library of India", "catalog_url": "https://ndl.iitkgp.ac.in/", "access": "institutional_feed_required", "integration_guidance": NDLI_INFO_URL, "configured": bool(os.getenv("NDLI_OAI_ENDPOINT"))},
        ],
        "sync_endpoint": "/api/sources/sync",
        "scope": "Catalog metadata and source links only; original files remain on their repository."
    }

@app.post("/api/sources/sync", tags=["Source Catalogs"])
def sync_source_catalogs(limit: int = Query(100, ge=1, le=500)):
    """Fetch public source metadata and incrementally upsert records into SQLite/FTS."""
    statuses = fetch_sources(limit)
    connection = get_db_connection()
    cursor = connection.cursor()
    result = []
    try:
        for status in statuses:
            inserted_or_updated = 0
            for record in status.records:
                cursor.execute("""
                    INSERT OR REPLACE INTO documents (
                        id, title, author, date, type, language, source,
                        archive_reference, collection, pages, word_count,
                        summary, full_text, tags, translations_json, media_json, raw_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(record[key] for key in (
                    "id", "title", "author", "date", "type", "language", "source",
                    "archive_reference", "collection", "pages", "word_count",
                    "summary", "full_text", "tags", "translations_json", "media_json", "raw_json"
                )))
                cursor.execute("DELETE FROM documents_fts WHERE id = ?", (record["id"],))
                cursor.execute("""
                    INSERT INTO documents_fts (id, title, summary, full_text, tags)
                    VALUES (?, ?, ?, ?, ?)
                """, (record["id"], record["title"], record["summary"], record["full_text"], record["tags"]))
                inserted_or_updated += 1
            result.append({
                "source": status.source,
                "status": status.status,
                "records_upserted": inserted_or_updated,
                "message": status.message,
            })
        connection.commit()
    except Exception as error:
        connection.rollback()
        logger.exception("Source catalog sync failed")
        raise HTTPException(status_code=500, detail=f"Source catalog sync failed: {error}") from error
    finally:
        connection.close()
    return {"status": "completed", "limit_per_source": limit, "results": result}

@app.get("/api/ocr/model-status", tags=["OCR"])
def get_ocr_model_status():
    return handwritten_model_status()


@app.post("/api/ocr", tags=["OCR"])
def run_ocr(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    mode: str = Form(default="printed"),
):
    try:
        text, pages_processed = extract_text(
            file.filename or "",
            file.file.read(20 * 1024 * 1024 + 1),
            language,
            mode,
        )
    except OCRLanguageError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except OCRInputError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except OCRUnavailableError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    return {
        "text": text,
        "pages_processed": pages_processed,
        "language": language,
        "mode": mode,
        "engine": "Tesseract",
        "model": HANDWRITTEN_MODEL if mode == "handwritten" else language,
        "filename": file.filename,
    }

@app.post("/api/assistant", tags=["Research Assistant"])
def answer_archive_question(request: AssistantRequest):
    language = request.language if request.language in ASSISTANT_COPY else "en"
    question = normalize_assistant_query(request.question, language)
    sources = retrieve_archive_sources(question)
    if not sources:
        return {
            "answer": ASSISTANT_COPY[language]["empty"],
            "sources": [],
        }

    localized_summaries = []
    for source in sources:
        wrapper = get_document_by_id(source["id"]) or {}
        record = wrapper.get("document", {}) if isinstance(wrapper, dict) else {}
        translated = (record.get("translations") or {}).get(language, {})
        if translated.get("title"):
            source["display_title"] = translated["title"]
        localized_summary = translated.get("summary") or (record.get("content") or {}).get("summary")
        if localized_summary:
            source["localized_summary"] = localized_summary
            localized_summaries.append(localized_summary)

    return {
        "answer": "\n\n".join([
            ASSISTANT_COPY[language]["found"].format(count=len(sources)),
            ASSISTANT_COPY[language]["summary_heading"],
            *[f"• {summary}" for summary in localized_summaries[:3]],
            ASSISTANT_COPY[language]["source_note"]
        ]),
        "sources": sources,
    }

@app.post("/api/tts", tags=["Audio"])
def generate_narration(request: NarrationRequest):
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs is not configured. Set the ELEVENLABS_API_KEY environment variable and restart the backend."
        )

    payload = json.dumps({
        "text": request.text,
        "model_id": "eleven_multilingual_v2"
    }).encode("utf-8")
    elevenlabs_request = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        data=payload,
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(elevenlabs_request, timeout=60) as response:
            return Response(content=response.read(), media_type="audio/mpeg")
    except urllib.error.HTTPError as error:
        logger.warning("ElevenLabs returned HTTP %s", error.code)
        if error.code in (401, 403):
            raise HTTPException(status_code=502, detail="ElevenLabs rejected the API key. Check ELEVENLABS_API_KEY.")
        if error.code == 402:
            raise HTTPException(status_code=402, detail="ElevenLabs requires available credits or an active billing plan.")
        if error.code == 429:
            raise HTTPException(status_code=429, detail="ElevenLabs rate or usage limit reached. Try again later or check your plan.")
        raise HTTPException(status_code=502, detail="ElevenLabs could not generate narration. Check the account and voice access.")
    except urllib.error.URLError:
        logger.exception("Could not reach ElevenLabs")
        raise HTTPException(status_code=502, detail="Could not connect to ElevenLabs. Check the network and try again.")

@app.get("/api/stats", response_model=StatsResponse, tags=["Analytics"])
async def stats():
    """Retrieve live repository counts, language distribution, and sources."""
    try:
        data = get_archive_stats()
        return data
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search", response_model=SearchResponse, tags=["Search"])
async def search(query: SearchQuery):
    """
    Sub-millisecond semantic-style full-text search with SQLite FTS5 index.
    Supports filtering by language, document type, and source.
    """
    t0 = time.time()
    try:
        total, results = search_documents(
            query_text=query.q,
            language=query.language,
            doc_type=query.document_type,
            source=query.source,
            limit=query.limit,
            offset=query.offset
        )
        took_ms = round((time.time() - t0) * 1000, 2)
        return SearchResponse(
            query=query.q,
            total=total,
            took_ms=took_ms,
            results=results
        )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search execution error: {e}")

@app.get("/api/documents", tags=["Documents"])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    language: Optional[str] = None,
    document_type: Optional[str] = None,
    source: Optional[str] = None
):
    """List documents with pagination and metadata filters."""
    total, results = search_documents(
        query_text="*",
        language=language,
        doc_type=document_type,
        source=source,
        limit=limit,
        offset=skip
    )
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": results
    }

@app.get("/api/documents/{doc_id}", tags=["Documents"])
async def get_document(doc_id: str):
    """Get full document object including text, quotes, metadata, translations, and media."""
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document with ID '{doc_id}' not found.")
    return doc

@app.get("/api/timeline", tags=["Timeline"])
async def get_historical_timeline():
    """
    Returns structured chronological milestones in Dr. B.R. Ambedkar's life,
    speeches, and constitutional drafting achievements for interactive kiosk display.
    """
    timeline_events = [
        {
            "year": 1916,
            "date": "1916-05-09",
            "title": "Castes in India Paper at Columbia University",
            "category": "Academic / Anthropology",
            "description": "Presents first seminal paper on endogamy and mechanisms of caste reproduction at Columbia University.",
            "doc_id": "DOC_DAF_BAWS_PUB_1916_CII"
        },
        {
            "year": 1920,
            "date": "1920-01-31",
            "title": "Launch of 'Muknayak' (Voice of the Mute)",
            "category": "Journalism & Social Awakening",
            "description": "Founds Marathi fortnightly declaring journalism as an instrument of emancipation for silenced millions.",
            "doc_id": "DOC_DAF_BAWS_PUB_1920_MUK"
        },
        {
            "year": 1923,
            "date": "1923-12-01",
            "title": "Problem of the Rupee (London School of Economics)",
            "category": "Economics & Monetary Policy",
            "description": "Submits D.Sc. dissertation establishing monetary stabilization principles that led to the Reserve Bank of India.",
            "doc_id": "DOC_DAF_BAWS_PUB_1923_POR"
        },
        {
            "year": 1927,
            "date": "1927-03-20",
            "title": "Mahad Satyagraha (Chavdar Tale Water Rights)",
            "category": "Civil Rights Movement",
            "description": "Leads historic non-violent assertion of civic equality and universal human rights to public drinking water.",
            "doc_id": "DOC_DAF_BAWS_SPEECH_1927_MSD"
        },
        {
            "year": 1932,
            "date": "1932-09-24",
            "title": "The Poona Pact Agreement",
            "category": "Political Representation",
            "description": "Secures 148 reserved legislative seats for the Depressed Classes across provincial assemblies.",
            "doc_id": "DOC_DAF_BAWS_DOC_1932_POONA"
        },
        {
            "year": 1936,
            "date": "1936-05-15",
            "title": "Annihilation of Caste Published",
            "category": "Social Justice & Philosophy",
            "description": "Publishes profound critique demonstrating caste as an unnatural division of labourers requiring eradication of orthodox sanctions.",
            "doc_id": "DOC_DAF_BAWS_PUB_1936_AOC"
        },
        {
            "year": 1946,
            "date": "1946-12-17",
            "title": "Maiden Address to the Constituent Assembly",
            "category": "Constitution Making",
            "description": "Plea for national unity, mutual statesmanship, and constitutional justice for all communities.",
            "doc_id": "DOC_CAD_CAD_VOL01_19461217"
        },
        {
            "year": 1947,
            "date": "1947-08-29",
            "title": "Appointed Chairman of the Drafting Committee",
            "category": "Constitutional Architect",
            "description": "Appointed to lead the drafting of the Constitution of the Republic of India as Law Minister.",
            "doc_id": "DOC_CAD_CAD_VOL07_19481104"
        },
        {
            "year": 1948,
            "date": "1948-11-04",
            "title": "Introduction of the Draft Constitution",
            "category": "Constitutional Jurisprudence",
            "description": "Outlines Parliamentary executive model, flexible federalism, and fundamental rights protections.",
            "doc_id": "DOC_CAD_CAD_VOL07_19481104"
        },
        {
            "year": 1948,
            "date": "1948-11-29",
            "title": "Abolition of Untouchability (Article 17 Adopted)",
            "category": "Fundamental Rights",
            "description": "Draft Article 11 unanimously adopted, outlawing untouchability and penalizing its enforcement.",
            "doc_id": "DOC_CAD_CAD_VOL07_19481129"
        },
        {
            "year": 1949,
            "date": "1949-11-25",
            "title": "Final Constituent Assembly Address (Grammar of Anarchy)",
            "category": "Democratic Philosophy",
            "description": "Urges social democracy to sustain political democracy, warns against hero-worship/Bhakti in politics.",
            "doc_id": "DOC_CAD_CAD_VOL11_19491125"
        },
        {
            "year": 1956,
            "date": "1956-10-14",
            "title": "Deekshabhoomi Nagpur Buddhist Conversion",
            "category": "Spiritual Emancipation",
            "description": "Embraces Buddhism with 500,000 followers, enshrining 22 vows for egalitarian and rational life.",
            "doc_id": "DOC_DAF_BAWS_PUB_1956_BHD"
        }
    ]
    return {
        "total_milestones": len(timeline_events),
        "events": timeline_events
    }

@app.post("/api/ingest", tags=["Ingestion"])
async def ingest_single_document(doc_input: DocumentWrapper):
    """
    Dynamic endpoint allowing archival staff or connected memorial nodes to ingest
    new documents with immediate indexing into SQLite and FTS5.
    """
    doc = doc_input.document
    conn = get_db_connection()
    cur = conn.cursor()

    tags_str = ", ".join(doc.tags)
    summary = doc.content.summary or doc.content.full_text[:280]

    try:
        cur.execute("""
            INSERT OR REPLACE INTO documents (
                id, title, author, date, type, language, source,
                archive_reference, collection, pages, word_count,
                summary, full_text, tags, translations_json, media_json, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc.id, doc.title, doc.author, doc.date, doc.type, doc.language, doc.metadata.source,
            doc.metadata.archive_reference, doc.metadata.collection, doc.metadata.pages,
            doc.metadata.word_count, summary, doc.content.full_text, tags_str,
            json.dumps(doc.translations, ensure_ascii=False),
            json.dumps(doc.media, ensure_ascii=False),
            json.dumps(doc_input.model_dump(), ensure_ascii=False)
        ))

        cur.execute("DELETE FROM documents_fts WHERE id = ?;", (doc.id,))
        cur.execute("""
            INSERT INTO documents_fts (id, title, summary, full_text, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (doc.id, doc.title, summary, doc.content.full_text, tags_str))

        conn.commit()
        conn.close()

        # Save copy to processed_data
        proc_path = BASE_DIR / "processed_data" / f"{doc.id}.json"
        with open(proc_path, "w", encoding="utf-8") as f:
            json.dump(doc_input.model_dump(), f, ensure_ascii=False, indent=2)

        return {"status": "success", "message": f"Document '{doc.id}' successfully ingested and indexed in FTS5."}
    except Exception as e:
        conn.close()
        logger.error(f"Ingestion failed for {doc.id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {e}")

@app.get("/api/export/registry", tags=["Export"])
async def export_registry():
    """Download full registry.json file."""
    if not REGISTRY_PATH.exists():
        raise HTTPException(status_code=404, detail="Registry file not found")
    return FileResponse(path=str(REGISTRY_PATH), filename="registry.json", media_type="application/json")

@app.get("/api/export/csv", tags=["Export"])
async def export_csv():
    """Download combined_metadata.csv for external reporting."""
    if not CSV_PATH.exists():
        raise HTTPException(status_code=404, detail="CSV file not found")
    return FileResponse(path=str(CSV_PATH), filename="combined_metadata.csv", media_type="text/csv")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
