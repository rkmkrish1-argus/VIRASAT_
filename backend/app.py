"""
FastAPI Server for Dr. B.R. Ambedkar Digital Heritage Archive (PS 26096)
Provides search, filtering, document inspection, statistics, dynamic ingestion,
Constitutional Ideas research graph, document relationships, Student NotebookLM prompts, and multimodal OCR.
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
    get_db_connection,
    get_all_constitutional_ideas,
    get_document_relations,
    add_document_relation,
    record_ocr_contribution
)
from .ocr import (
    HANDWRITTEN_MODEL,
    OCRInputError,
    OCRLanguageError,
    OCRUnavailableError,
    OCRPermissionError,
    extract_text_with_metadata,
    handwritten_model_status,
)
from .auth import authenticate_user, verify_role_access
from .notebook_prompts import get_student_notebook_prompts
from .source_ingestion import fetch_sources, NDLI_INFO_URL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ArchiveAPI")

app = FastAPI(
    title="Dr. B.R. Ambedkar Digital Heritage Archive API",
    description="Backend API for Problem Statement 26096 (MoSJE / Dr. Ambedkar International Centre)",
    version="2.1.0"
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


class LoginRequest(BaseModel):
    passcode: str = ""
    role: Optional[str] = "visitor"


class DocumentRelationRequest(BaseModel):
    source_doc_id: str
    target_doc_id: str
    relation_type: str = "references"
    description: str = ""
    researcher: str = "Researcher"
    passcode: str = ""


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
        "empty": "I couldn't find matching records in the indexed archive. Try a different phrase or browse the archive.",
        "found": "I found {count} relevant archive record(s).",
        "summary_heading": "Archive summaries:",
        "source_note": "The cited source excerpts below remain in their original language."
    },
    "hi": {
        "empty": "अनुक्रमित अभिलेखागार में इस प्रश्न से मेल खाते अभिलेख नहीं मिले।",
        "found": "अभिलेखागार में {count} संबंधित अभिलेख मिले।",
        "summary_heading": "अभिलेखों का सार:",
        "source_note": "नीचे दिए गए उद्धृत स्रोत अंश मूल भाषा में हैं।"
    },
    "mr": {
        "empty": "अनुक्रमित अभिलेखात या प्रश्नाशी जुळणाऱ्या नोंदी सापडल्या नाहीत।",
        "found": "अभिलेखागारात {count} संबंधित नोंदी सापडल्या।",
        "summary_heading": "नोंदींचा सारांश:",
        "source_note": "खालील उद्धृत स्रोत उतारे मूळ भाषेत आहेत।"
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
        "version": "2.1.0"
    }

@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "service": "Ambedkar Digital Heritage Archive API",
        "version": "2.1.0"
    }

# --- AUTHENTICATION ENDPOINT ---
@app.post("/api/auth/login", tags=["Authentication"])
def login_user(request: LoginRequest):
    result = authenticate_user(request.passcode, request.role)
    if not result["authenticated"] and request.role != "visitor":
        raise HTTPException(status_code=401, detail=result.get("error", "Authentication failed."))
    return result

# --- CONSTITUTIONAL IDEAS & RESEARCH ENDPOINTS ---
@app.get("/api/constitutional-ideas", tags=["Constitutional Ideas"])
def get_constitutional_ideas():
    return {
        "total": 7,
        "ideas": get_all_constitutional_ideas()
    }

@app.get("/api/relations/{doc_id}", tags=["Document Relations"])
def get_doc_relations(doc_id: str):
    return {
        "doc_id": doc_id,
        "relations": get_document_relations(doc_id)
    }

@app.post("/api/relations", tags=["Document Relations"])
def create_doc_relation(request: DocumentRelationRequest):
    auth_res = authenticate_user(request.passcode, "researcher")
    if auth_res["role"] != "researcher":
        raise HTTPException(status_code=403, detail="Establishing database document relationships requires Researcher authentication.")
    
    res = add_document_relation(
        source_doc_id=request.source_doc_id,
        target_doc_id=request.target_doc_id,
        relation_type=request.relation_type,
        description=request.description,
        researcher=request.researcher
    )
    return res

# --- STUDENT NOTEBOOKLM PROMPTS ENDPOINT ---
@app.get("/api/student-notebook-prompts", tags=["Student Study Studio"])
def get_notebook_prompts(language: str = "en"):
    """Fetch curated Student NotebookLM prompts detailing Backstory -> Frontstory narrative arcs with primary source citations."""
    prompts = get_student_notebook_prompts(language)
    return {
        "status": "success",
        "language": language,
        "total": len(prompts),
        "prompts": prompts
    }

# --- OCR & CONTRIBUTION ENDPOINT ---
@app.get("/api/ocr/model-status", tags=["OCR"])
def get_ocr_model_status():
    return handwritten_model_status()

@app.post("/api/ocr", tags=["OCR"])
def run_ocr(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    mode: str = Form(default="printed"),
    user_role: str = Form(default="student"),
    passcode: str = Form(default=""),
    kraken_model_id: str = Form(default="kraken_ambedkar_handwritten_v1"),
    source_date: str = Form(default=""),
    source_name: str = Form(default=""),
    source_author: str = Form(default=""),
    researcher_name: str = Form(default="")
):
    auth_info = authenticate_user(passcode, user_role)
    effective_role = auth_info["role"]

    content = file.file.read(5 * 1024 * 1024 + 1)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File limit exceeded. Contributions are strictly limited to 5 MB per file.")

    try:
        ocr_result = extract_text_with_metadata(
            file_name=file.filename or "upload.png",
            content=content,
            language=language,
            mode=mode,
            user_role=effective_role,
            kraken_model_id=kraken_model_id,
            source_date=source_date,
            source_name=source_name,
            source_author=source_author,
            researcher_name=researcher_name
        )

        record_ocr_contribution(
            doc_id=None,
            filename=file.filename or "upload.png",
            user_role=effective_role,
            ocr_mode=mode,
            model_used=ocr_result.get("model", mode),
            file_size_bytes=len(content),
            source_date=source_date,
            source_name=source_name,
            source_author=source_author,
            researcher_name=researcher_name,
            extracted_text=ocr_result["text"]
        )

        return ocr_result

    except OCRPermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except OCRLanguageError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except OCRInputError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except OCRUnavailableError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

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
            detail="ElevenLabs is not configured. Set ELEVENLABS_API_KEY."
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
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Text-to-speech service error: {error}")

@app.get("/api/stats", response_model=StatsResponse, tags=["Analytics"])
async def stats():
    try:
        data = get_archive_stats()
        return data
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search", response_model=SearchResponse, tags=["Search"])
async def search(query: SearchQuery):
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
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document with ID '{doc_id}' not found.")
    return doc

@app.get("/api/sources", tags=["Source Catalogs"])
async def source_catalog_status():
    return {
        "sources": [
            {"id": "Foundation", "name": "Dr. Ambedkar Foundation", "catalog_url": "https://ambedkarfoundation.nic.in/publication.html", "access": "public_catalog_metadata"},
            {"id": "CAD", "name": "Constituent Assembly Debates", "catalog_url": "https://eparlib.sansad.in/handle/123456789/760448/browse?type=date", "access": "public_catalog_metadata"},
            {"id": "NDL", "name": "National Digital Library of India", "catalog_url": "https://ndl.iitkgp.ac.in/", "access": "institutional_feed_required", "integration_guidance": NDLI_INFO_URL, "configured": bool(os.getenv("NDLI_OAI_ENDPOINT"))},
        ],
        "sync_endpoint": "/api/sources/sync",
        "scope": "Catalog metadata and source links only."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
