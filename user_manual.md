# User Manual & Operator Guide — Dr. B.R. Ambedkar Digital Heritage Archive
**Problem Statement ID:** 26096 | **Target Institution:** Dr. Ambedkar International Centre (DAIC), New Delhi  
**Live Production Portal:** [https://virasatstarkx.netlify.app/](https://virasatstarkx.netlify.app/)  
**Live Cloud API Backend:** [https://ambedkar-api-81k6.onrender.com](https://ambedkar-api-81k6.onrender.com)  
**GitHub Repository:** [https://github.com/rkmkrish1-argus/VIRASAT_](https://github.com/rkmkrish1-argus/VIRASAT_)  
**Version:** 2.2.0 (Living Interface, 3D Spatial Lens & Cloud-Edge Sync)

---

## 1. Introduction

Welcome to the **Dr. B.R. Ambedkar Digital Heritage Archive and Institutional Knowledge Platform**. Engineered for the Ministry of Social Justice and Empowerment (MoSJE) and the Dr. Ambedkar International Centre (DAIC), this platform democratizes access to 538+ landmark writings, speeches, and Constituent Assembly Debates (CAD) through an interactive, multi-sensory "Living Interface" combining 3D spatial depth, grounded AI research assistance, and audio accessibility.

This manual provides operational guidance for:
1. **Memorial Visitors & Students:** Exploring the archive, interacting with the 3D Ambedkar Spectacles ("Spatial Lens"), examining how constitutional laws were crafted, using voice-guided AI research, and listening to audio narration.
2. **Historians & Legal Researchers:** Querying Dublin Core archival metadata across 10 Indian languages, filtering 538 indexed records, and citing primary sources.
3. **Archivists & Curators:** Using OCR digitization to ingest scanned manuscripts and managing the catalog with role-based authentication.
4. **Exhibition Operators & IT Administrators:** Running standalone kiosk displays, LAN Wi-Fi hotspots, zero-latency Cloudflare tunnels, or cloud-hosted Netlify/Render environments.

---

## 2. System Architecture & Corpus Metrics

| Archival Parameter | Production Metric | Description |
| :--- | :--- | :--- |
| **Total Ingested Documents** | **538 Historical Works** | Complete corpus indexed across 3 verified national archives |
| **Total Words Indexed** | **86,834 Words** | Curated transcripts, debates, and primary source treatises |
| **Vector Embedding Chunks** | **835 Chunks** | Pre-partitioned semantic chunks for vector RAG |
| **Full-Text Retrieval Latency** | **< 2.0 ms** | SQLite FTS5 engine outperforming government SLA (2.0s) |
| **Supported Languages** | **10 Indian Languages** | English (418), Hindi (42), Telugu (27), Marathi (18), Bengali (11), Tamil (9), Gujarati (9), Punjabi (2), Malayalam (1), Kannada (1) |
| **Primary Sources** | **3 Verified Repos** | Internet Archive (510), Dr. Ambedkar Foundation / BAWS (16), CAD Debates (12) |
| **Theme System** | **Obsidian & Parchment** | Dynamic Dark (`#040507`) & Light (`#f5f4ee`) modes with adaptive 3D lighting |

---

## 3. Installation & Quick Start

### Option A: Cloud Web Access (Zero Setup Required)
Open any modern web browser and navigate directly to:
**[https://virasatstarkx.netlify.app/](https://virasatstarkx.netlify.app/)**

All 538 documents, the 3D Ambedkar Spectacles, search filters, timeline milestones, and modal inspectors are immediately functional with zero installation.

---

### Option B: Local Kiosk & Server Execution

#### Step 1: Open the Project Directory
Open PowerShell or Command Prompt in the repository folder:
```powershell
cd C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar
```

#### Step 2: Initialize Virtual Environment & Start Server
Run the local setup script:
```powershell
.\start-local.ps1
```
*What this script does automatically:*
1. Checks for Python 3.10+.
2. Activates or creates the isolated virtual environment (`.venv`).
3. Installs requirements from `requirements.txt` (FastAPI, Uvicorn, PyMuPDF, Pytesseract, Pillow, etc.).
4. Starts the local FastAPI server at `http://127.0.0.1:8000`.

#### Step 3: Launch Dedicated Fullscreen Kiosk Mode
Double-click [`Launch-Ambedkar-Archive.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/Launch-Ambedkar-Archive.bat) or [`Run-Ambedkar-Archive.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/Run-Ambedkar-Archive.bat).
This launches Google Chrome or Microsoft Edge in borderless kiosk mode directly into the interface.

---

## 4. Multi-Device Exhibition & Network Deployment

### Scenario A: Standalone Single Touchscreen Kiosk
- **Best For:** Dedicated memorial interactive touch-tables or offline evaluation kiosks.
- **Execution:** Run `Launch-Ambedkar-Archive.bat`. The archive runs in clean fullscreen kiosk mode.

---

### Scenario B: Zero-Latency Cloudflare Edge Tunnel (Recommended for Live Judging)
- **Best For:** Instant public global access without firewall port-forwarding or Render cold-start delays.
- **Execution:**
  1. Ensure the local server is running (`start-local.ps1` or port 8000).
  2. Double-click [`start_cloudflare_tunnel.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/start_cloudflare_tunnel.bat) (or run `.\cloudflared.exe tunnel --url http://127.0.0.1:8000`).
  3. The tunnel will generate a public URL such as `https://curves-baseball-circular-declined.trycloudflare.com`.
  4. Share this URL or display a QR code for visitors and evaluators to access the full archive with sub-second speeds.

---

### Scenario C: Multi-Device LAN (1 Laptop + Mobile Devices / Tablets)
- **Best For:** Exhibition booths where tablets act as kiosks while the laptop acts as the central server.
- **Execution:**
  1. On the laptop, run:
     ```powershell
     .\start-lan.ps1
     ```
  2. The script configures the Windows Defender Firewall rule and displays your LAN URL (e.g. `http://192.168.43.100:8000/`).
  3. Open that URL on any phone or tablet connected to the same Wi-Fi.

---

### Scenario D: High-Speed USB Kiosk (ADB Reverse Port Forwarding)
- **Best For:** Convention halls with noisy or blocked Wi-Fi networks.
- **Execution:**
  1. Connect an Android tablet to the laptop via USB and enable USB Debugging.
  2. Run:
     ```powershell
     adb reverse tcp:8000 tcp:8000
     ```
  3. Open `http://localhost:8000` in the tablet's browser for lag-free, wire-speed access.

---

## 5. Visitor & Researcher Guide

### 1. 3D Spatial Lens — Dr. Ambedkar's Round Spectacles
- Located at the hero header of the homepage, the 3D gold-wire spectacles (`AMBEDKAR_SPECS`) serve as the physical and metaphorical anchor of the exhibition.
- **Interactive Controls:**
  - **Mouse / Touch Parallax:** Move your cursor or drag on touch screens to rotate and tilt the spectacles in 3D space.
  - **Reflective Specular Highlights:** Notice real-time reflection on the circular lenses and gold-plated temple joints.
  - **Theme Adaptation:** Switching between Dark Mode and Light Mode automatically transitions the 3D studio lighting from an amber rim light to archival tungsten illumination.

### 2. Backstory-to-Frontstory Law Crafting Studio
- Directly below the 3D Spectacles, explore **"Why This Law Was Crafted This Way"**.
- Tap on any key constitutional milestone:
  - **Article 17 (Abolition of Untouchability):** Backstory: Mahad Satyagraha 1927 & Chavdar Tale water denial. Frontstory: Enacted as an absolute fundamental right enforceable against private citizens.
  - **Article 21 (Personal Liberty & Due Process):** Backstory: Columbia University jurisprudence under John Dewey. Frontstory: Bedrock of constitutional safeguards against arbitrary detention.
  - **Article 32 (Heart and Soul of the Constitution):** Backstory: Substantive rights are hollow without immediate judicial remedy. Frontstory: Direct right to petition the Supreme Court of India via prerogative writs.
  - **Hindu Code Bill (Women's Property & Equal Rights):** Backstory: Resignation as Law Minister in 1951 over patriarchal dilution. Frontstory: Established equal inheritance, divorce rights, and monogamy for Indian women.
  - **Reserve Bank of India Framework:** Backstory: London School of Economics doctorate treatise *The Problem of the Rupee*. Frontstory: Formed the operational architecture of India's central banking system.

### 3. Comprehensive Search & Faceted Filtering
- **Keyword Search:** Type any search query (e.g., `Annihilation of Caste`, `Directive Principles`, `Untouchability`, `Article 356`, `Rupee`) and press Enter.
- **Keyboard Shortcut:** Press `Ctrl + K` (or `Cmd + K` on Mac) anywhere on the page to focus the search box.
- **538-Record Direct Catalog:** Searches across all 538 indexed historical works with instant pagination (30 records per page).
- **Faceted Dropdowns:** Filter by:
  - **Language:** English, Hindi, Telugu, Marathi, Bengali, Tamil, Gujarati, Punjabi, Malayalam, Kannada.
  - **Document Type:** Publications, Speeches, CAD Debates, Manuscripts, Historical Records.
  - **Source Repository:** Internet Archive, Constituent Assembly Debates, Dr. Ambedkar Foundation.

### 4. Interactive Historical Timeline
- Tap the **Timeline** tab in the navigation bar.
- Trace 11 defining milestones spanning 1916 (Columbia University paper) to 1956 (Deekshabhoomi conversion).
- Tap **"Read Original Historical Record"** on any card to immediately view the corresponding primary source document.

### 5. AI Research Assistant & Grounded Q&A
- Tap the **Research** tab.
- **Recommended Prompts:** Click one-touch prompts like *Hero Worship / Bhakti in Politics*, *Parliamentary vs Presidential System*, or *Article 356 as 'Dead Letter'*.
- **Voice Speech-to-Text Input:** Tap the **Microphone** button (`#aiVoiceBtn`). When active, speak in English, Hindi, or Marathi. Real-time transcription is processed automatically.
- **Source Verification:** Every answer includes excerpted evidence citations with a direct **"View Source"** button.

### 6. Audio Narration (TTS)
- In the Document Detail modal, tap the golden **Play** button.
- The dual-engine audio synthesizer reads the title, executive summary, and key historical quotes.
- Fallback: Uses high-fidelity cloud voices when online, or native browser Web Speech synthesis (`en-IN`, `hi-IN`, `mr-IN`) when offline.

### 7. Dual Themes: Obsidian & Archival Parchment
- Tap the **Moon / Sun** button in the header.
- **Obsidian Dark Mode:** Deep `#040507` background with gold amber typography and glassmorphic card borders.
- **Archival Parchment Light Mode:** `#f5f4ee` paper parchment tone with deep slate typography and warm museum accents.

---

## 6. Curatorial Guide: Ingestion & Role-Based Access

The archive features a role-based authentication modal to safeguard historical records:

### User Roles & Capabilities
1. **Visitor:** Public browsing, search, timeline exploration, AI assistant, and audio narration.
2. **Student (Passcode: `{STUDENT}`):** Unlocks deep document relationship graphs and advanced research queries.
3. **Researcher / Curator (Passcode: `{RESEARCHER}`):** Unlocks the **Contribute** tab, full OCR digitization, and catalog ingestion pipelines.

### Digitization Workflow
1. Authenticate with Researcher role.
2. Tap the **Contribute** tab.
3. Upload a scan (`.pdf`, `.png`, `.jpg`, `.tiff`).
4. Select OCR Mode (*Printed text* or *Handwriting*).
5. Click **Extract Text** to generate editable OCR transcripts.
6. Verify and edit extracted text, Dublin Core metadata, and tags.
7. Click **Ingest Document Into Pipeline** to commit directly to SQLite and FTS5 indices.

---

## 7. Automated Cloud Sync & Diagnostic Script

To keep Netlify, GitHub, and Render synchronized, run the automated pipeline:
```powershell
.\.venv\Scripts\python.exe auto_deploy_and_check.py
```
This utility:
1. Validates local frontend files (`index.html`, `app.js`, `styles.css`).
2. Commits and pushes any modifications to GitHub `main` branch (triggering Netlify auto-build).
3. Polls `https://virasatstarkx.netlify.app/` until the new version is live on the CDN.
4. Performs a complete health audit of SQLite chunks, Cloud /api/stats, and proxy health.

---

## 8. Troubleshooting & Operator FAQ

### Q1: The site displays "Complete Digital Heritage Catalog (538+ Works Indexed) Active"
- **Meaning:** The frontend is successfully utilizing the pre-compiled 538-record catalog (`frontend/archive_documents.json`), providing immediate offline search and browsing even if the cloud backend is cold-starting.

### Q2: How do I avoid Render cold-start delays?
- Render's free tier spins down after 15 minutes of inactivity (taking ~30 seconds to wake).
- **Solution:** Use the Cloudflare Tunnel via `start_cloudflare_tunnel.bat`. It connects directly to your local FastAPI server with zero delay.

### Q3: How do I change between Light and Dark mode?
- Tap the theme toggle button in the top navigation header. Both modes have been calibrated with WCAG AA compliance and adaptive 3D lighting.

### Q4: Port 8000 is occupied
- In PowerShell, run:
  ```powershell
  Get-Process python* | Stop-Process -Force
  ```
  Then re-run `.\start-local.ps1`.
