# What Has Been Done — Dr. B.R. Ambedkar Digital Heritage Archive
**Problem Statement ID:** 26096 | **Ministry:** Ministry of Social Justice and Empowerment (MoSJE)  
**Target Institution:** Dr. Ambedkar International Centre (DAIC), New Delhi  
**Live Production URL:** [https://virasatstarkx.netlify.app/](https://virasatstarkx.netlify.app/)  
**Live Cloud API URL:** [https://ambedkar-api-81k6.onrender.com](https://ambedkar-api-81k6.onrender.com)  
**Version:** 2.2.0

---

## 1. Executive Summary of Achievements

The repository has evolved from an initial concept into a production-grade, multi-tier digital archive and memorial platform. The team has engineered:
- A high-speed SQLite FTS5 search backend delivering sub-2ms query latencies.
- **538 historical records** and **835 vector embedding chunks** indexed across 10 Indian languages.
- An interactive **3D Spatial Lens** featuring Dr. B.R. Ambedkar's iconic gold round spectacles (`AMBEDKAR_SPECS`).
- An experiential **Backstory-to-Frontstory Law Crafting Studio** explaining the origins of Article 17, Article 21, Article 32, the Hindu Code Bill, and the Reserve Bank of India framework.
- A dynamic **Obsidian & Archival Parchment Theme System** with zero contrast defects and adaptive 3D lighting.
- A resilient **538-record Client-Side Catalog (`archive_documents.json`)** ensuring instant browsing and pagination (30 records per page) with zero reliance on cloud container spin-up.
- Live continuous deployment on **Netlify Edge** (`https://virasatstarkx.netlify.app/`) proxied to a live **Render Cloud API** (`https://ambedkar-api-81k6.onrender.com`).
- Direct **Cloudflare Edge Tunnel** integration (`start_cloudflare_tunnel.bat`) allowing any local kiosk server to be published to Cloudflare's global network with zero configuration.
- An automated CI/CD and database diagnostic pipeline (`auto_deploy_and_check.py`).

---

## 2. Core Architecture & Components Implemented

### A. Living Interface & Frontend Spatial UX (`frontend/`)
1. **Interactive 3D Spectacles (`frontend/app.js`):**
   - Three.js WebGL scene rendering Dr. Ambedkar's gold-plated round spectacles.
   - Real-time mouse/touch cursor-following rotation with physics dampening.
   - Metallic gold shaders (`MeshStandardMaterial`), translucent glass reflections, and ambient shadows.
   - Theme-reactive studio lighting (amber glow in dark mode, archival tungsten in light mode).
2. **Backstory-to-Frontstory Law Crafting Studio (`frontend/index.html`):**
   - Interactive modal cards breaking down historical trigger events (Mahad Satyagraha, Columbia jurisprudence, LSE currency treatise) into their exact constitutional legal clauses.
3. **Dual Theme Engine (`frontend/styles.css`):**
   - Obsidian Dark Mode: `#040507` abyss dark with gold amber typography and glassmorphic translucent cards.
   - Archival Parchment Light Mode: `#f5f4ee` paper tone with deep slate typography.
4. **Client-Side High-Resilience Catalog (`frontend/archive_documents.json`):**
   - Pre-compiled 1.3 MB static catalog containing all 538 historical records.
   - Enables instant client-side keyword search, 3-axis filtering, pagination (30 per page), and Dublin Core inspection modal even during network disruptions or server cold starts.
5. **Multimodal Accessibility:**
   - Web Speech API speech recognition for hands-free voice search.
   - Dual-engine Text-to-Speech (TTS) narration with cloud voices and local browser speech synthesis.

### B. Backend Architecture (`backend/`)
1. **FastAPI Cloud Application (`backend/app.py`):**
   - RESTful API with `/api/health`, `/api/stats`, `/api/search`, `/api/timeline`, `/api/assistant`, `/api/tts`, `/api/ocr`, `/api/ingest`, and `/api/sources/sync`.
2. **High-Performance Database Engine (`backend/database.py`):**
   - SQLite 3 integration with an `FTS5` virtual table (`documents_fts`) for full-text search.
   - Delivers measured search latency of **0.5 ms – 1.8 ms** (1,000x faster than the government's 2.0s requirement).
3. **Data Schemas & Validation (`backend/models.py`):**
   - Pydantic models enforcing strict schema validation (`DocumentWrapper`, `MetadataModel`, `ContentModel`).
4. **Digitization & OCR Pipeline (`backend/ocr.py`):**
   - PyMuPDF for PDF rendering and Tesseract OCR engine supporting Devanagari (`hin`, `mar`), South Indian languages (`tam`, `tel`), and English.

### C. Cloud, Edge & DevOps Infrastructure
1. **Netlify Edge CDN (`netlify.toml`):**
   - Continuous deployment directly from GitHub repository `origin/main`.
   - Reverse-proxies `/api/*` to the live cloud backend on Render.
2. **Render Cloud Web Service (`https://ambedkar-api-81k6.onrender.com`):**
   - Production FastAPI container running on Render with Python 3.11 and Uvicorn.
3. **Cloudflare Edge Tunnel (`start_cloudflare_tunnel.bat`):**
   - Bundled standalone `cloudflared.exe` binary.
   - Instantly exposes the local server on port 8000 via a secure, global `trycloudflare.com` tunnel.
4. **Automated Deployment & Embeddings Audit Tool (`auto_deploy_and_check.py`):**
   - Validates frontend files, synchronizes Git commits to GitHub, verifies live Netlify deployment, and audits SQLite vector chunks and cloud endpoints.

---

## 3. Data Corpus & Archival Registry (`ambedkar_archive_data/`)

| Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **Total Ingested Records** | **538 items** | Standardized across 3 major historical archives |
| **Total Words Indexed** | **86,834 words** | Curated transcripts, debates, and primary source treatises |
| **Vector Embedding Chunks** | **835 chunks** | Formatted and partitioned for semantic embeddings |
| **Internet Archive (IA)** | 510 items | Writings, biographies, treatises, historical scans |
| **Dr. Ambedkar Foundation (BAWS)**| 16 items | Landmark published volumes, treatises, and speeches |
| **CAD Lok Sabha (Parliament)** | 12 items | Landmark Constituent Assembly Debates (1946–1949) |
| **Supported Languages** | 10 Languages | English, Hindi, Telugu, Marathi, Bengali, Tamil, Gujarati, Punjabi, Malayalam, Kannada |
