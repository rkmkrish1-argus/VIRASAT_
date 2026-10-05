# What Has Been Done — Dr. B.R. Ambedkar Digital Heritage Archive
**Problem Statement ID:** 26096 | **Ministry:** Ministry of Social Justice and Empowerment (MoSJE)  
**Primary Institutional Deployment:** Dr. Ambedkar International Centre (DAIC), New Delhi  
**Audit Location:** `C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar`

---

## 1. Executive Summary of Achievements

The repository contains an operational, multi-tier software and data prototype for an AI-powered institutional digital archive and memorial touch-kiosk. The team has successfully moved from conceptual requirements to a working end-to-end prototype featuring:
- A high-speed SQLite FTS5 search backend with sub-2 millisecond retrieval latency.
- An interactive, responsive, and multilingual touch-friendly kiosk user interface.
- An indexed primary corpus of 530 standardized archival records.
- OCR-assisted document ingestion pipeline for scanned PDFs and images.
- Dual-engine Text-to-Speech (TTS) narration (Cloud ElevenLabs + Browser SpeechSynthesis).
- Multi-tier deployment scripts covering Standalone Local, LAN Wi-Fi Hotspot, WAN Tunneling, and USB-wired Kiosk configurations.

---

## 2. Core Architecture & Components Implemented

### A. Backend Architecture (`backend/`)
1. **FastAPI Application (`backend/app.py`):**
   - Implements a robust REST API serving endpoints for search, filtering, document inspection, statistics, OCR extraction, AI question assistance, audio narration, and catalog synchronization.
   - Configured with CORS middleware to enable communication with remote touchscreens, mobile devices, and preview servers.
   - Serves static assets directly and handles fallback routes.
2. **High-Performance Database Engine (`backend/database.py`):**
   - SQLite 3 integration with an `FTS5` virtual table (`documents_fts`) for full-text search.
   - Contains indexed fields: `id`, `title`, `summary`, `full_text`, `tags`.
   - Achieves query execution times of **0.5 ms – 1.8 ms**, outperforming the government's SLA requirement of < 2.0 seconds by over 1,000x.
   - Built-in graceful fallback to local JSON file inspection if the database connection encounters locking.
3. **Data Schemas & Validation (`backend/models.py`):**
   - Pydantic models enforcing strict schema validation (`DocumentWrapper`, `DocumentItem`, `MetadataModel`, `ContentModel`, `SearchQuery`, `SearchResponse`, `StatsResponse`).
   - Standardized to the Part 7 Institutional Metadata Schema.
4. **Digitization & OCR Pipeline (`backend/ocr.py`):**
   - Ingests PDF and image formats (`.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`).
   - PyMuPDF (`fitz`) handles multi-page PDF rendering at 200 DPI.
   - Tesseract OCR engine extracts text with multi-language parameterization (`en`, `hi`, `mr`, `ta`, `te`).
   - Architectural hook for custom handwriting recognition (`ambedkar_handwritten_v2.traineddata`).
5. **Catalog Synchronization Crawler (`backend/source_ingestion.py`):**
   - Implements scrapers and catalog harvesters for the Dr. Ambedkar Foundation (DAF) publications and the Parliament Digital Library (Constituent Assembly Debates).
   - Provides an incremental `/api/sources/sync` endpoint that fetches external catalog metadata and upserts into SQLite.
6. **Handwriting Preparation Utility (`backend/prepare_handwriting_data.py`):**
   - Automated CLI tool to validate line-image/transcript pairs, compute word counts, verify UTF-8 encoding, and generate training manifests for OCR fine-tuning.
7. **OCR Model Downloader (`backend/setup_ocr_models.py`):**
   - Automated downloader fetching verified Tesseract fast `.traineddata` files for Devanagari (`hin`, `mar`) and South Indian languages (`tam`, `tel`) from GitHub into the local repository.
8. **Node.js Fallback Preview Server (`frontend/preview-server.js`):**
   - Standalone zero-dependency HTTP server in Node.js serving static assets and simulating backend search and assistant endpoints directly from `ambedkar_archive_data/processed_data/` JSON records.
   - Allows judges or evaluators to test the frontend even on machines without Python.

---

## 3. Data Corpus & Archival Registry (`ambedkar_archive_data/`)

The repository includes a curated, pre-processed archival dataset organized systematically:

| Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **Total Ingested Records** | **530 items** | Standardized across 3 major historical archives |
| **Internet Archive (IA)** | 510 items | Writings, biographies, treatises, historical scans |
| **Constituent Assembly (CAD)** | 10 items | Landmark constitutional debates and speeches |
| **Dr. Ambedkar Foundation (DAF)** | 10 items | Official BAWS (Babasaheb Ambedkar Writings & Speeches) |
| **Languages Represented** | 10 Indian languages | English (410), Hindi (42), Telugu (27), Marathi (18), Bengali (11), Tamil (9), Gujarati (9), Punjabi (2), Malayalam (1), Kannada (1) |
| **Total Words Indexed** | **86,624 words** | Indexed in SQLite FTS5 for instant search |
| **Vector RAG Chunks** | **835 chunks** | Pre-segmented and ready for vector embeddings |
| **Metadata Formats** | JSON & CSV | Complete `registry.json` and `combined_metadata.csv` exports |

---

## 4. Frontend & Kiosk User Interface (`frontend/`)

The frontend is an integrated single-page application built with HTML5, vanilla JavaScript (`app.js`), Tailwind CSS, and custom styling (`styles.css`):

1. **Search & Discovery Hub:**
   - Full-text search with instant debounced execution and Enter-key trigger.
   - Multi-parameter filter bar: Language (10 languages), Document Type (Publications, Speeches, CAD Debates, Manuscripts, Historical Records), and Repository Source (IA, CAD, Foundation).
   - Quick Filter chips for popular constitutional concepts: *CAD Debates, Annihilation of Caste, Directive Principles, Untouchability, Economics & RBI, Buddhism & Dhamma*.
   - Dynamic document cards with type badges, language tags, historical dates, and excerpt previews.
   - Client-side pagination with "Load more records" support.
2. **Interactive Heritage Timeline:**
   - Chronologically visualizes 11 defining milestones of Dr. Ambedkar's life:
     - 1916: *Castes in India* paper at Columbia University.
     - 1920: Launch of *Muknayak* (Voice of the Mute).
     - 1923: *Problem of the Rupee* (London School of Economics / RBI founding principles).
     - 1927: Mahad Satyagraha (Chavdar Tale civil water rights).
     - 1932: The Poona Pact Agreement.
     - 1936: *Annihilation of Caste* publication.
     - 1946: Maiden Address to the Constituent Assembly.
     - 1947: Appointment as Drafting Committee Chairman.
     - 1948: Introduction of the Draft Constitution.
     - 1948: Adoption of Article 17 (Abolition of Untouchability).
     - 1949: Final Constituent Assembly Address ("Grammar of Anarchy").
     - 1956: Nagpur Deekshabhoomi Buddhist Conversion.
   - Direct integration: clicking any timeline event opens the full archival record with verified citations.
3. **Source-Grounded Archival Research Assistant:**
   - Interactive Q&A chat interface with preset historical prompts (*Hero Worship / Bhakti in Politics, Parliamentary vs Presidential Executive, Article 356 as 'Dead Letter', Caste as Division of Labourers*).
   - Integrated Web Speech API microphone input allowing visitors to speak questions in English, Hindi, or Marathi.
   - Responses quote indexed historical evidence and display clickable citation blocks linking directly to the primary document.
4. **Multilingual Architecture:**
   - Global language switcher for **English (EN)**, **Hindi (हिंदी)**, and **Marathi (मराठी)**.
   - Comprehensive DOM tree-walker dynamically translates all interface labels, placeholders, aria attributes, timeline events, and assistant prompt suggestions.
5. **Audio Narration (Text-to-Speech):**
   - High-fidelity natural voice generation via ElevenLabs API (`eleven_multilingual_v2`).
   - Automatic fallback to browser native SpeechSynthesis API using regional Indian voices (`en-IN`, `hi-IN`, `mr-IN`).
   - Play, pause, stop controls with real-time status indication.
6. **Document Detail Inspection Modal:**
   - Full transcript and executive summary display.
   - Blockquote extraction for key historical quotes.
   - Dublin Core archival metadata grid (Identifier, Reference, Word Count, Language, Condition, Access Rights).
   - Direct link to primary source PDFs (e.g. Lok Sabha eparlib records, MEA BAWS volume mirrors).
7. **Institutional Upload & OCR Review Studio:**
   - Interactive form allowing memorial staff to upload newly scanned files.
   - On-the-fly OCR extraction with live character/word count.
   - Allows curators to proofread, correct OCR errors, and ingest the document directly into SQLite and FTS5 without restarting the server.
8. **Institutional Analytics Dashboard:**
   - Visual statistics cards (Total Documents, Words Indexed, Vector Chunks, Languages).
   - Percentage distribution progress bars for all 10 languages and 3 archival repositories.
   - One-click export buttons for `registry.json` and `metadata.csv`.
9. **Kiosk Mode & Accessibility:**
   - One-click Fullscreen mode toggle (`toggleFullScreen()`).
   - Dark / Light mode toggle with persistent state.
   - WCAG 2.1 AA accessibility features: `:focus-visible` keyboard outlines, high-contrast text modes, reduced-motion overrides, and ARIA live regions for screen readers.

---

## 5. Deployment & Distribution Infrastructure

The team has established 10 distinct launch scripts and automation tools:

| Script Name | Environment | Action Executed |
| :--- | :--- | :--- |
| `start-local.ps1` | Standalone Local | Auto-creates `.venv`, installs `requirements.txt`, launches Uvicorn on `127.0.0.1:8000`. |
| `start-local.bat` | Standalone Local | Double-click Windows batch launcher for local server execution. |
| `start-lan.ps1` | Local Wi-Fi Network | Auto-detects local Wi-Fi IPv4 address, creates Windows Firewall rule for port 8000, binds Uvicorn to `0.0.0.0:8000`. |
| `start-wan-tunnel.bat` | Internet Tunnel | Verifies local server, checks/downloads `cloudflared.exe` (55 MB bundled), and opens an encrypted public HTTPS quick tunnel (`https://*.trycloudflare.com`). |
| `start-everything-wan.bat` | All-In-One Internet | Starts local server in background, polls port 8000 until active, and automatically launches the Cloudflare WAN tunnel. |
| `create-package.bat` | Distribution | Packages backend, frontend, data, and launch scripts into a clean distributable `ambedkar-archive-package.zip`. |
| `Launch-Ambedkar-Archive.bat` | Exhibition Kiosk | Checks backend status, launches server minimized, and opens frontend in Chromium App Mode (`--app=http://localhost:8000`). |
| `Run-Ambedkar-Archive.bat` | Kiosk Launcher | Robust portable kiosk launcher checking Python, venv, packages, server, and browser in app mode using dynamic `%~dp0`. |
| `Create-Desktop-Shortcut.ps1` | Kiosk Station | Installs a clean desktop shortcut on the Windows desktop pointing to the kiosk launcher. |
| `deployment_guide.md` | Documentation | Comprehensive manual covering single-file distribution, LAN deployment, Cloudflare quick tunnels, named custom domains, and Cloud VPS with Caddy. |

---

## 6. Summary of Current Completion

The foundation of the project is solid: **the hardware-software kiosk concept is fully proven**, the hybrid search engine is remarkably fast, the user interface is polished and multilingual, and multi-device network deployment is operational. The project is ready for architectural expansion to match the complete institutional vision.
