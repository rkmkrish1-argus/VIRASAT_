# What to Be Added — Dr. B.R. Ambedkar Digital Heritage Archive
**Problem Statement ID:** 26096 | **Target Institution:** Dr. Ambedkar International Centre (DAIC), New Delhi  
**Project Location:** `C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar`

---

## 1. Overview of Additions Required

To transition the Dr. B.R. Ambedkar Digital Heritage Archive from a preliminary prototype into a fully production-ready, institutionally deployable hardware-and-software kiosk platform, specific modules, components, datasets, and scripts must be added to the codebase.

The additions are categorized into four core domains:
1. **Backend & AI Architecture**
2. **Data Corpus & Machine Learning Models**
3. **Frontend & Touch Kiosk User Experience**
4. **DevOps, Security, and Production Infrastructure**

---

## 2. Backend & AI Architecture Additions

### A. Local Vector Engine & Dense Retrieval (`backend/vector_search.py`)
- **Addition:** Dedicated vector database module using `ChromaDB` (or `sqlite-vec` for embedded air-gapped kiosks).
- **Functionality:**
  - Loads the pre-chunked 835+ text segments and generates dense 384-dimensional embeddings using a local HuggingFace model (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`).
  - Implements cosine similarity search over embeddings.
  - Exposes `retrieve_vector_chunks(query, top_k=5)` for hybrid fusion with SQLite FTS5.

### B. Grounded RAG & Verification Engine (`backend/rag_engine.py`)
- **Addition:** True Retrieval-Augmented Generation (RAG) module replacing the existing regex keyword dictionary in `/api/assistant`.
- **Functionality:**
  - Performs **Reciprocal Rank Fusion (RRF)** across lexical FTS5 and semantic vector search results.
  - Formulates a grounded context prompt enforcing the zero-hallucination mandate:
    ```markdown
    Context:
    [Source 1: BAWS Vol. 1, p. 54 | Date: 1916-05-09] "..."
    [Source 2: CAD Vol. VII, p. 322 | Date: 1948-11-04] "..."
    
    Instruction: Answer the user's question using ONLY the facts stated above.
    Cite every statement with [BAWS Vol X, p. Y] or [CAD Vol X, p. Y].
    If the context does not contain the answer, explicitly state:
    "The indexed archival records do not contain verified information on this query."
    ```
  - Connects to a local quantized Small Language Model (e.g. `Llama-3-8B-Instruct-Q4_K_M` via `llama-cpp-python` or an institutional Ollama instance).

### C. Air-Gapped Offline Neural TTS Engine (`backend/offline_tts.py`)
- **Addition:** Completely local, zero-cost, offline neural Text-to-Speech service using `Piper-TTS` with `onnxruntime`.
- **Functionality:**
  - Bundles lightweight ONNX voice models for Indian English (`en_IN`), Hindi (`hi_IN`), and Marathi (`mr_IN`).
  - Generates high-fidelity WAV/MP3 audio streams in real time directly on the laptop or kiosk CPU without internet connection or ElevenLabs API credits.
  - Automatically switches from ElevenLabs to local Piper-TTS when offline.

### D. Security & Role-Based Access Control (`backend/auth.py`)
- **Addition:** Authentication and authorization middleware for institutional operations.
- **Functionality:**
  - Protects administrative endpoints (`/api/ingest`, `/api/sources/sync`, database backup) with JWT authentication.
  - Roles:
    - **Visitor (Default / Kiosk Mode):** Read-only access to search, timeline, assistant, and audio narration.
    - **Archivist / Curator:** Access to OCR upload studio, text correction, and document ingestion.
    - **System Administrator:** Full access to database sync, export, and configuration logs.

### E. API Rate Limiting & Upload Guard (`backend/rate_limiter.py`)
- **Addition:** SlowAPI / Starlette rate limiting to protect public endpoints from scraping or Denial-of-Service attacks during public WAN tunnel access.

---

## 3. Data Corpus & Machine Learning Additions

### A. Complete 21 Volumes of BAWS (`ambedkar_archive_data/baws_complete/`)
- **Addition:** Full structured text and metadata for all 21 volumes of *Babasaheb Ambedkar Writings and Speeches* published by the Dr. Ambedkar Foundation (MoSJE).
- **Structure:**
  - `BAWS_VOL_01`: Castes in India, Annihilation of Caste, Maharashtra as a Linguistic Province.
  - `BAWS_VOL_02`: In the Bombay Legislature (1927–1939).
  - `BAWS_VOL_03`: Philosophy of Hinduism, India and the Pre-requisites of Communism, Revolution and Counter-Revolution.
  - `BAWS_VOL_04`: Riddles in Hinduism.
  - `BAWS_VOL_06`: The Problem of the Rupee, Evolution of Provincial Finance.
  - `BAWS_VOL_07`: Who Were the Shudras?, The Untouchables.
  - `BAWS_VOL_08`: Pakistan or the Partition of India.
  - `BAWS_VOL_11`: The Buddha and His Dhamma.
  - `BAWS_VOL_13`: Dr. Ambedkar as Principal Architect of the Indian Constitution.
  - `BAWS_VOL_17`: Dr. B.R. Ambedkar and His Egalitarian Revolution (Speeches, Letters, Telegrams).
  - Volumes 18–21: Speeches in Marathi (*Dhammadiksha, Bahishkrit Bharat editorials*).

### B. Complete Constituent Assembly Debates (`ambedkar_archive_data/cad_complete/`)
- **Addition:** Complete verbatim debates of all 12 volumes from the Lok Sabha Secretariat, segmented by speech, date, and constitutional article discussed.

### C. Fine-Tuned Handwriting OCR Model
- **Addition:** `ambedkar_archive_data/ocr_models/tessdata/ambedkar_handwritten_v2.traineddata`.
- **Functionality:** Fine-tuned specifically on Dr. Ambedkar's cursive handwriting drafts, marginal notes, and correspondence.

---

## 4. Frontend & Touch Kiosk User Experience Additions

### A. Virtual On-Screen Multilingual Keyboard (`frontend/keyboard.js`)
- **Addition:** An interactive, touch-friendly on-screen keyboard (using a lightweight library such as `Simple-Keyboard`).
- **Functionality:**
  - Automatically pops up on touch screens when tapping the Search input or Assistant input.
  - Supports English QWERTY, Hindi InScript / phonetic, and Marathi layouts.
  - Enables full kiosk interaction on tablet or touchscreen displays without physical hardware keyboards.

### B. Inactivity Attract Loop & Screen Saver (`frontend/screensaver.js`)
- **Addition:** Automated kiosk idle-state manager.
- **Functionality:**
  - Detects visitor inactivity after 90 seconds.
  - Smoothly displays a full-screen historical video, high-resolution portrait carousel, and landmark quotes with subtle background ambient music.
  - Displays a prominent "Touch Anywhere to Explore the Archive" prompt that instantly resets the kiosk to the home search interface.

### C. Side-by-Side DeepZoom IIIF Manuscript Viewer (`frontend/viewer.js`)
- **Addition:** Embedded `OpenSeadragon` viewer within the document inspection modal (`docModal`).
- **Functionality:**
  - Allows visitors to pinch-to-zoom and pan across high-resolution scans of original historical pages.
  - Displays original physical ink, official seals, and marginalia side-by-side with verified OCR transcriptions.

### D. Interactive Constitutional Knowledge Graph (`frontend/knowledge_graph.js`)
- **Addition:** Visual concept map using `Cytoscape.js` or `Vis.js`.
- **Functionality:**
  - Graphically connects historical milestones, constitutional articles, and writings:
    - *Mahad Satyagraha (1927)* $\rightarrow$ *Article 15 (Prohibition of Discrimination / Equal Access to Public Water & Places)*.
    - *Abolition of Untouchability* $\rightarrow$ *Article 17*.
    - *Grammar of Anarchy (1949)* $\rightarrow$ *Constitutional Morality & Social Democracy*.
  - Allows touch kiosk visitors to tap any node on the graph to explore related documents.

### E. Offline Progressive Web App (PWA) Manifest & Service Worker
- **Additions:** `frontend/manifest.json` and `frontend/sw.js`.
- **Functionality:**
  - Caches all frontend HTML, CSS, JavaScript, local fonts, and icons.
  - Enables 100% offline standalone execution in Chrome/Edge Kiosk Mode.

---

## 5. DevOps, Deployment & Production Additions

### A. Containerized Architecture (`Dockerfile` & `docker-compose.yml`)
- **Addition:** Multi-container configuration:
  - **Service 1 (`app`):** FastAPI backend, SQLite/FTS5, Piper-TTS, PyMuPDF, and Tesseract.
  - **Service 2 (`caddy`):** Reverse proxy with automated TLS/SSL certificate provisioning.
  - **Service 3 (`vector_db`):** ChromaDB standalone container for persistent embedding storage.

### B. Automated Reverse Proxy Configuration (`Caddyfile`)
- **Addition:** Production Caddy reverse proxy file:
  ```caddy
  archive.ambedkar.in {
      reverse_proxy localhost:8000
      encode gzip zstd
      header {
          Strict-Transport-Security "max-age=31536000;"
          X-Content-Type-Options "nosniff"
          X-Frame-Options "SAMEORIGIN"
      }
  }
  ```

### C. Database Maintenance & Backup Utility (`backend/backup_db.py`)
- **Addition:** Scheduled backup script creating timestamped compressed copies of `ambedkar_archive.db` and validating SQLite integrity via `PRAGMA integrity_check;`.

### D. Portable Kiosk Master Script (`start-all.bat`)
- **Addition:** Unified Windows launcher that:
  1. Checks for local Python and virtual environment.
  2. Binds server to `0.0.0.0:8000`.
  3. Launches Microsoft Edge in Kiosk Fullscreen mode (`msedge.exe --kiosk http://localhost:8000 --edge-kiosk-type=fullscreen`).
  4. Monitors background health and automatically restarts services upon unexpected termination.
