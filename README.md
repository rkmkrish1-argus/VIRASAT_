# Dr. B.R. Ambedkar Digital Heritage Archive (SIH Problem Statement ID: 26096)
### AI-Powered Institutional Archive, 3D Spatial Lens & Audio-Visual Knowledge Platform
**Issuing Authority**: Ministry of Social Justice and Empowerment (MoSJE), Central Government  
**Primary Institution**: Dr. Ambedkar International Centre (DAIC), New Delhi  
**Theme**: Smart Education | **Category**: Hardware (with Integrated Software)  
**Live Production Web Portal**: [https://virasatstarkx.netlify.app/](https://virasatstarkx.netlify.app/)  
**Live Cloud API Backend**: [https://ambedkar-api-81k6.onrender.com](https://ambedkar-api-81k6.onrender.com)  
**GitHub Repository**: [https://github.com/rkmkrish1-argus/VIRASAT_](https://github.com/rkmkrish1-argus/VIRASAT_)

---

## 🏛️ Executive Summary

The **Dr. B.R. Ambedkar Digital Heritage Archive** is a high-performance institutional knowledge platform designed to democratize access to Dr. B.R. Ambedkar’s constitutional treatises, parliamentary debates, and historical speeches.

Moving beyond static catalogs, this platform implements a **"Living Interface" (UI/UX × 3D × Motion)** featuring:
1. **Interactive 3D Spatial Lens (`AMBEDKAR_SPECS`):** Procedural 3D model of Dr. Ambedkar's iconic gold-wire spectacles with real-time cursor/touch tilt, specular lens reflections, and lighting that adapts to dark/light themes.
2. **Backstory-to-Frontstory Law Crafting Studio:** An experiential deep-dive revealing why monumental laws (Article 17, Article 21, Article 32, Hindu Code Bill, and RBI Act) were framed in their exact constitutional language.
3. **538 Historical Works & 835 Embedding Chunks:** Complete catalog indexed in SQLite with sub-2 millisecond lexical search and pre-computed vector partitions.
4. **Resilient Dual-Tier Architecture:** Client-side 538-record offline catalog paired with a live FastAPI cloud backend on Render and Cloudflare edge tunnel.
5. **Obsidian & Archival Parchment Theme System:** Pixel-perfect Dark (`#040507`) and Light (`#f5f4ee`) modes with zero contrast defects.
6. **Accessible Multimodal Experience:** Dual-engine Text-to-Speech (TTS), speech recognition, and 10 Indian languages.

---

## 📊 Production Metrics & Performance

| Metric | Measured Value | Standard / Government SLA |
| :--- | :--- | :--- |
| **Total Ingested Documents** | **538 works** | Target was ≥ 500 documents (Exceeded) |
| **Total Words Indexed** | **86,834 words** | Comprehensive multi-lingual corpus |
| **Vector RAG Chunks** | **835 chunks** | Formatted and partitioned for semantic embeddings |
| **Search Query Latency (FTS5)**| **< 2.0 ms** | Government target: < 2.0 seconds (**1,000x faster**) |
| **Schema Validation Rate** | **100% Valid (538/538)** | Strict adherence to Part 7 Institutional JSON Schema |
| **Indian Languages Supported** | **10 Languages** | English (418), Hindi (42), Telugu (27), Marathi (18), Bengali (11), Tamil (9), Gujarati (9), Punjabi (2), Malayalam (1), Kannada (1) |
| **Source Repositories** | **3 Verified Archives**| Internet Archive (510), Dr. Ambedkar Foundation / BAWS (16), CAD Debates (12) |
| **Production Uptime & CDN** | **Netlify + Render + Cloudflare** | Edge CDN deployment with global SSL and reverse proxy |

---

## 📁 Repository Directory Structure

```
.
├── ambedkar_archive_data/
│   ├── raw_documents/                  # Acquired raw JSON records from primary archives
│   │   ├── ia_raw_records.json         # 510 Internet Archive items
│   │   ├── cad_raw_records.json        # Landmark Constituent Assembly Debates
│   │   └── foundation_raw_records.json # BAWS & Foundation primary publications
│   ├── processed_data/                 # 538 standardized JSON records (Part 7 Schema)
│   ├── metadata/                       # Master catalogs & inventory reports
│   │   ├── registry.json               # Master JSON registry
│   │   ├── combined_metadata.csv       # Tabular CSV metadata
│   │   └── data_inventory_report.json  # Comprehensive health & inventory report
│   ├── texts/                          # Full text transcripts of landmark works
│   ├── database/                       # ACID storage & search indices
│   │   └── ambedkar_archive.db         # SQLite DB with FTS5 virtual table
│   └── scripts/                        # Ingestion & harvesting pipeline
│
├── backend/                            # FastAPI Cloud Server & API Endpoints
│   ├── app.py                          # FastAPI server & static UI mount
│   ├── models.py                       # Pydantic data schemas
│   ├── database.py                     # SQLite FTS5 query & ingestion handlers
│   ├── ocr.py                          # Tesseract & PyMuPDF OCR processing pipeline
│   └── source_ingestion.py             # DAF & Parliament catalog harvester
│
├── frontend/                           # Kiosk & Web Interactive Interface
│   ├── index.html                      # Touch-screen kiosk web portal & HUD
│   ├── styles.css                      # Obsidian / Parchment dynamic design system
│   ├── app.js                          # 3D Spectacles Three.js canvas, search, & audio
│   └── archive_documents.json          # Pre-compiled 538-record client-side catalog
│
├── netlify.toml                        # Netlify Edge reverse-proxy configuration
├── auto_deploy_and_check.py            # Automated Git-to-Netlify CI/CD & health validator
├── start_cloudflare_tunnel.bat         # One-click Cloudflare Edge tunnel launcher
├── start-local.ps1                     # Local environment bootstrap & server startup
├── start-lan.ps1                       # Multi-device Wi-Fi hotspot exhibition runner
└── requirements.txt                    # Python dependencies
```

---

## 🚀 Deployment Options

### 1. Live Production Site (Cloud)
Visit **[https://virasatstarkx.netlify.app/](https://virasatstarkx.netlify.app/)**  
Directly hosted on Netlify Edge CDN. All API routes (`/api/*`) are dynamically proxied to the live Render cloud backend (`https://ambedkar-api-81k6.onrender.com`).

### 2. Zero-Latency Cloudflare Tunnel (Local Server)
Expose the local backend directly to the Cloudflare Edge network:
1. Double click `start_cloudflare_tunnel.bat` (or run `.\cloudflared.exe tunnel --url http://127.0.0.1:8000`).
2. An instant public HTTPS URL (e.g., `https://curves-baseball-circular-declined.trycloudflare.com`) is generated with sub-second response times.

### 3. Local Standalone Kiosk
To run locally on a kiosk terminal:
```powershell
.\start-local.ps1
```
Then double-click `Launch-Ambedkar-Archive.bat` to launch in dedicated Chromium fullscreen kiosk app mode.

### 4. Continuous Auto-Deployment & Diagnostic Script
To push updates to GitHub, trigger Netlify rebuild, and audit backend embeddings:
```powershell
.\.venv\Scripts\python.exe auto_deploy_and_check.py
```

---

## 💡 Key Architectural Features

- **3D Spatial Lens (`AMBEDKAR_SPECS`):** Three.js interactive 3D model of Dr. Ambedkar's round gold spectacles reacting to user mouse/touch coordinates with dynamic lighting.
- **Law Crafting Studio:** Explores the backstory behind Article 17, Article 21, Article 32, Hindu Code Bill, and the Reserve Bank of India framework.
- **Sub-2ms Full-Text Search:** Tokenized prefix search across titles, summaries, tags, and full transcripts using SQLite FTS5.
- **Dual-Engine Audio Narration:** High-fidelity cloud TTS with local browser Web Speech fallback (`en-IN`, `hi-IN`, `mr-IN`) for accessible readouts.
- **Curatorial OCR & Ingestion:** Upload PDF scans or manuscript images, perform multi-lingual OCR (Devanagari, Tamil, Telugu, English), and ingest into the archive.
- **Role-Based Authentication:** Multi-tier access for Visitors, Students (`{STUDENT}`), and Researchers (`{RESEARCHER}`).
