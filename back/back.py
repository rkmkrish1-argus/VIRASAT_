import io
import json
import sqlite3
import time
import logging
from pathlib import Path
from typing import Optional

import fitz                    # PyMuPDF
import pytesseract
from PIL import Image

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pydantic import BaseModel


# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "ambedkar_archive.db"

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# 2. TESSERACT CONFIGURATION
# ============================================================

# IMPORTANT:
# Change this path if Tesseract is installed somewhere else.

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ============================================================
# 3. LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(
    "AmbedkarArchive"
)


# ============================================================
# 4. FASTAPI APP
# ============================================================

app = FastAPI(
    title="Dr. B.R. Ambedkar Digital Heritage Archive",
    description="AI-Powered Institutional Archive with OCR",
    version="2.0"
)


# ============================================================
# 5. CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# 6. DATABASE CONNECTION
# ============================================================

def get_db_connection():

    conn = sqlite3.connect(
        str(DB_PATH)
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# 7. CREATE DATABASE
# ============================================================

def initialize_database():

    conn = get_db_connection()

    cursor = conn.cursor()


    # --------------------------------------------------------
    # Documents table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (

            id TEXT PRIMARY KEY,

            title TEXT,

            author TEXT,

            date TEXT,

            type TEXT,

            language TEXT,

            source TEXT,

            summary TEXT,

            tags TEXT,

            archive_reference TEXT,

            collection TEXT,

            pages INTEGER,

            word_count INTEGER,

            full_text TEXT,

            raw_json TEXT
        )
    """)


    # --------------------------------------------------------
    # FTS5 search table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
        USING fts5(
            id UNINDEXED,
            title,
            summary,
            full_text,
            tags
        )
    """)


    conn.commit()

    conn.close()

    logger.info(
        "Database initialized"
    )


initialize_database()


# ============================================================
# 8. SEARCH MODEL
# ============================================================

class SearchRequest(BaseModel):

    q: str = ""

    language: Optional[str] = None

    document_type: Optional[str] = None

    source: Optional[str] = None

    limit: int = 20

    offset: int = 0


# ============================================================
# 9. HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {

        "status": "healthy",

        "service":
            "Ambedkar Digital Heritage Archive",

        "ocr":
            "enabled",

        "version":
            "2.0"
    }


# ============================================================
# 10. CHECK TESSERACT
# ============================================================

@app.get("/api/ocr-status")
def ocr_status():

    try:

        version = (
            pytesseract
            .get_tesseract_version()
        )

        languages = (
            pytesseract
            .get_languages(
                config=""
            )
        )

        return {

            "status": "ready",

            "tesseract_version":
                str(version),

            "languages":
                languages
        }

    except Exception as e:

        return {

            "status": "error",

            "message":
                str(e)
        }


# ============================================================
# 11. OCR IMAGE
# ============================================================

def ocr_image(image):

    """
    Extract text from an image.

    eng = English
    hin = Hindi
    guj = Gujarati
    """

    try:

        text = pytesseract.image_to_string(
            image,
            lang="eng+hin+guj"
        )

        return text

    except Exception as e:

        logger.exception(
            "Image OCR failed"
        )

        raise


# ============================================================
# 12. EXTRACT TEXT FROM FILE
# ============================================================

def extract_text_from_file(
    file_bytes,
    filename
):

    filename = str(
        filename or ""
    ).strip()

    extension = (
        Path(filename)
        .suffix
        .lower()
    )


    logger.info(
        f"Processing file: {filename}"
    )

    logger.info(
        f"Detected extension: {extension}"
    )


    # ========================================================
    # IMAGE
    # ========================================================

    if extension in [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".webp"
    ]:

        image = Image.open(
            io.BytesIO(file_bytes)
        )

        text = ocr_image(
            image
        )

        return text, 1


    # ========================================================
    # PDF
    # ========================================================

    if extension == ".pdf":

        pdf = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        page_count = len(pdf)

        all_text = []


        for page_number in range(
            page_count
        ):

            logger.info(
                f"OCR page "
                f"{page_number + 1}/"
                f"{page_count}"
            )


            page = pdf[
                page_number
            ]


            # Render PDF page as image
            pix = page.get_pixmap(
                matrix=fitz.Matrix(
                    2,
                    2
                )
            )


            image = Image.open(
                io.BytesIO(
                    pix.tobytes("png")
                )
            )


            text = ocr_image(
                image
            )


            all_text.append(
                f"\n--- Page "
                f"{page_number + 1} ---\n"
            )

            all_text.append(
                text
            )


        pdf.close()


        return (
            "\n".join(all_text),
            page_count
        )


    # ========================================================
    # PDF DETECTION FROM FILE CONTENT
    # ========================================================

    if file_bytes[:4] == b"%PDF":

        logger.info(
            "PDF detected from file content"
        )


        pdf = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        page_count = len(pdf)

        all_text = []


        for page_number in range(
            page_count
        ):

            page = pdf[
                page_number
            ]

            pix = page.get_pixmap(
                matrix=fitz.Matrix(
                    2,
                    2
                )
            )

            image = Image.open(
                io.BytesIO(
                    pix.tobytes("png")
                )
            )

            text = ocr_image(
                image
            )


            all_text.append(
                f"\n--- Page "
                f"{page_number + 1} ---\n"
            )

            all_text.append(
                text
            )


        pdf.close()


        return (
            "\n".join(all_text),
            page_count
        )


    raise ValueError(
        "Unsupported file type. "
        "Please upload PDF or image."
    )


# ============================================================
# 13. OCR ONLY
# ============================================================

@app.post("/api/ocr")
async def ocr_document(
    file: UploadFile = File(...)
):

    try:

        file_bytes = await file.read()


        if not file_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )


        text, pages = (
            extract_text_from_file(
                file_bytes,
                file.filename
            )
        )


        return {

            "status":
                "success",

            "filename":
                file.filename,

            "pages":
                pages,

            "language":
                "eng+hin+guj",

            "word_count":
                len(
                    text.split()
                ),

            "text":
                text
        }


    except HTTPException:

        raise


    except Exception as e:

        logger.exception(
            "OCR failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# 14. OCR + DATABASE INGESTION
# ============================================================

@app.post("/api/ocr-and-ingest")
async def ocr_and_ingest(

    file: UploadFile = File(...),

    title: Optional[str] = Form(None),

    author: Optional[str] = Form("Unknown"),

    document_type: Optional[str] = Form(
        "Historical Document"
    ),

    source: Optional[str] = Form(
        "OCR Upload"
    ),

    language: Optional[str] = Form(
        "eng+hin+guj"
    ),

    tags: Optional[str] = Form(
        "Ambedkar, OCR"
    )
):

    try:

        file_bytes = await file.read()


        if not file_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )


        # ----------------------------------------------------
        # OCR
        # ----------------------------------------------------

        text, pages = (
            extract_text_from_file(
                file_bytes,
                file.filename
            )
        )


        # ----------------------------------------------------
        # Generate ID
        # ----------------------------------------------------

        document_id = (
            "OCR_"
            + str(
                int(
                    time.time()
                    * 1000
                )
            )
        )


        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        final_title = (
            title
            if title
            else Path(
                file.filename
            ).stem
        )


        # ----------------------------------------------------
        # Word count
        # ----------------------------------------------------

        word_count = len(
            text.split()
        )


        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        summary = text[:500]


        # ----------------------------------------------------
        # Save uploaded file
        # ----------------------------------------------------

        save_path = (
            UPLOAD_DIR
            / (
                document_id
                + "_"
                + file.filename
            )
        )


        with open(
            save_path,
            "wb"
        ) as output_file:

            output_file.write(
                file_bytes
            )


        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        conn = get_db_connection()

        cursor = conn.cursor()


        # ----------------------------------------------------
        # Insert document
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT OR REPLACE INTO documents
            (
                id,
                title,
                author,
                date,
                type,
                language,
                source,
                summary,
                tags,
                archive_reference,
                collection,
                pages,
                word_count,
                full_text,
                raw_json
            )

            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?
            )
            """,

            (
                document_id,

                final_title,

                author,

                "",

                document_type,

                language,

                source,

                summary,

                tags,

                "",

                "",

                pages,

                word_count,

                text,

                json.dumps({
                    "ocr": True,
                    "filename":
                        file.filename
                })
            )
        )


        # ----------------------------------------------------
        # Update FTS
        # ----------------------------------------------------

        cursor.execute(
            """
            DELETE FROM documents_fts
            WHERE id = ?
            """,
            (document_id,)
        )


        cursor.execute(
            """
            INSERT INTO documents_fts
            (
                id,
                title,
                summary,
                full_text,
                tags
            )

            VALUES
            (?, ?, ?, ?, ?)
            """,

            (
                document_id,

                final_title,

                summary,

                text,

                tags
            )
        )


        conn.commit()

        conn.close()


        return {

            "status":
                "success",

            "message":
                "Document OCR processed "
                "and indexed successfully.",

            "document": {

                "id":
                    document_id,

                "title":
                    final_title,

                "author":
                    author,

                "type":
                    document_type,

                "language":
                    language,

                "source":
                    source,

                "pages":
                    pages,

                "word_count":
                    word_count,

                "summary":
                    summary,

                "full_text":
                    text,

                "tags":
                    [
                        tag.strip()
                        for tag in
                        tags.split(",")
                        if tag.strip()
                    ]
            }
        }


    except HTTPException:

        raise


    except Exception as e:

        logger.exception(
            "OCR ingestion failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# 15. SEARCH
# ============================================================

@app.post("/api/search")
def search_documents(
    request: SearchRequest
):

    conn = get_db_connection()

    cursor = conn.cursor()


    query = (
        request.q
        .strip()
    )


    try:

        # ----------------------------------------------------
        # Empty search
        # ----------------------------------------------------

        if not query:

            sql = """
                SELECT
                    id,
                    title,
                    author,
                    date,
                    type,
                    language,
                    source,
                    summary,
                    tags

                FROM documents

                ORDER BY date DESC

                LIMIT ?
                OFFSET ?
            """

            cursor.execute(
                sql,
                (
                    request.limit,
                    request.offset
                )
            )


        # ----------------------------------------------------
        # FTS SEARCH
        # ----------------------------------------------------

        else:

            sql = """
                SELECT
                    d.id,
                    d.title,
                    d.author,
                    d.date,
                    d.type,
                    d.language,
                    d.source,
                    d.summary,
                    d.tags

                FROM documents d

                JOIN documents_fts f

                ON d.id = f.id

                WHERE documents_fts MATCH ?

                LIMIT ?
                OFFSET ?
            """


            cursor.execute(
                sql,
                (
                    query,
                    request.limit,
                    request.offset
                )
            )


        rows = cursor.fetchall()


        results = []


        for row in rows:

            tags = [
                tag.strip()

                for tag in
                (row["tags"] or "")
                .split(",")

                if tag.strip()
            ]


            results.append({

                "id":
                    row["id"],

                "title":
                    row["title"],

                "author":
                    row["author"],

                "date":
                    row["date"],

                "type":
                    row["type"],

                "language":
                    row["language"],

                "source":
                    row["source"],

                "summary":
                    row["summary"] or "",

                "tags":
                    tags
            })


        return {

            "query":
                query,

            "total":
                len(results),

            "results":
                results
        }


    finally:

        conn.close()


# ============================================================
# 16. GET DOCUMENTS
# ============================================================

@app.get("/api/documents")
def get_documents(

    skip: int = 0,

    limit: int = 20
):

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            title,
            author,
            date,
            type,
            language,
            source,
            summary,
            tags

        FROM documents

        ORDER BY date DESC

        LIMIT ?
        OFFSET ?
        """,

        (
            limit,
            skip
        )
    )


    rows = cursor.fetchall()

    conn.close()


    items = []


    for row in rows:

        items.append({

            "id":
                row["id"],

            "title":
                row["title"],

            "author":
                row["author"],

            "date":
                row["date"],

            "type":
                row["type"],

            "language":
                row["language"],

            "source":
                row["source"],

            "summary":
                row["summary"] or "",

            "tags":
                [
                    x.strip()

                    for x in
                    (row["tags"] or "")
                    .split(",")

                    if x.strip()
                ]
        })


    return {

        "total":
            len(items),

        "items":
            items
    }


# ============================================================
# 17. GET SINGLE DOCUMENT
# ============================================================

@app.get("/api/documents/{document_id}")
def get_document(
    document_id: str
):

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,

        (document_id,)
    )


    row = cursor.fetchone()

    conn.close()


    if not row:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )


    document = {

        "id":
            row["id"],

        "title":
            row["title"],

        "author":
            row["author"],

        "date":
            row["date"],

        "type":
            row["type"],

        "language":
            row["language"],

        "source":
            row["source"],

        "summary":
            row["summary"],

        "tags":
            [
                x.strip()

                for x in
                (row["tags"] or "")
                .split(",")

                if x.strip()
            ],

        "pages":
            row["pages"],

        "word_count":
            row["word_count"],

        "full_text":
            row["full_text"]
    }


    return {

        "document":
            document
    }


# ============================================================
# 18. STATISTICS
# ============================================================

@app.get("/api/stats")
def get_stats():

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM documents"
    )

    total_documents = (
        cursor.fetchone()[0]
    )


    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(word_count),
                0
            )

        FROM documents
        """
    )

    total_words = (
        cursor.fetchone()[0]
    )


    cursor.execute(
        """
        SELECT
            language,
            COUNT(*)

        FROM documents

        GROUP BY language
        """
    )

    languages = dict(
        cursor.fetchall()
    )


    cursor.execute(
        """
        SELECT
            type,
            COUNT(*)

        FROM documents

        GROUP BY type
        """
    )

    types = dict(
        cursor.fetchall()
    )


    cursor.execute(
        """
        SELECT
            source,
            COUNT(*)

        FROM documents

        GROUP BY source
        """
    )

    sources = dict(
        cursor.fetchall()
    )


    conn.close()


    return {

        "total_documents":
            total_documents,

        "total_words_indexed":
            total_words,

        "languages":
            languages,

        "types":
            types,

        "sources":
            sources
    }


# ============================================================
# 19. TIMELINE
# ============================================================

@app.get("/api/timeline")
def get_timeline():

    events = [

        {
            "year": 1916,
            "date": "1916-05-09",
            "title":
                "Castes in India Paper",
            "category":
                "Academic",
            "description":
                "Ambedkar presented his paper on caste."
        },

        {
            "year": 1920,
            "date": "1920-01-31",
            "title":
                "Launch of Mooknayak",
            "category":
                "Journalism",
            "description":
                "Launch of Ambedkar's Marathi periodical."
        },

        {
            "year": 1927,
            "date": "1927-03-20",
            "title":
                "Mahad Satyagraha",
            "category":
                "Civil Rights",
            "description":
                "Historic movement for civic equality."
        },

        {
            "year": 1936,
            "date": "1936-05-15",
            "title":
                "Annihilation of Caste",
            "category":
                "Social Reform",
            "description":
                "Major work addressing caste and social reform."
        },

        {
            "year": 1947,
            "date": "1947-08-29",
            "title":
                "Drafting Committee",
            "category":
                "Constitution",
            "description":
                "Ambedkar was appointed Chairman of the Drafting Committee."
        },

        {
            "year": 1949,
            "date": "1949-11-25",
            "title":
                "Constituent Assembly Address",
            "category":
                "Constitution",
            "description":
                "Ambedkar delivered his final major Constituent Assembly address."
        },

        {
            "year": 1956,
            "date": "1956-10-14",
            "title":
                "Nagpur Buddhist Conversion",
            "category":
                "History",
            "description":
                "Ambedkar embraced Buddhism at Nagpur."
        }
    ]


    return {

        "total_milestones":
            len(events),

        "events":
            events
    }


# ============================================================
# 20. SERVE FRONTEND
# ============================================================

@app.get("/")
def serve_frontend():

    index_file = (
        BASE_DIR
        / "index.html"
    )


    if index_file.exists():

        return FileResponse(
            index_file
        )


    return {

        "message":
            "Ambedkar Archive backend is running.",

        "docs":
            "/docs"
    }


# ============================================================
# 21. STATIC FILES
# ============================================================

if (
    BASE_DIR / "styles.css"
).exists():

    app.mount(
        "/static",
        StaticFiles(
            directory=str(BASE_DIR)
        ),
        name="static"
    )


# ============================================================
# RUN WITH:
#
# python app.py
#
# OR:
#
# uvicorn app:app --reload
#
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )