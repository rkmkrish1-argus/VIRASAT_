# What Are the Mistakes — Dr. B.R. Ambedkar Digital Heritage Archive
**Problem Statement ID:** 26096 | **Target Institution:** Dr. Ambedkar International Centre (DAIC), New Delhi  
**Audit Location:** `C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar`

---

## 1. Executive Summary of Audit Findings

A thorough, line-by-line inspection of the backend code, frontend scripts, database schemas, data registry, and deployment automation scripts has uncovered critical bugs, security vulnerabilities, architectural contradictions, and data quality flaws.

These issues are classified into 5 severity categories:
1. **Critical Security Vulnerabilities** (P0)
2. **Fatal Deployment & Script Bugs** (P0)
3. **Architectural Inconsistencies & Dead Code** (P1)
4. **Misrepresented AI & OCR Capabilities** (P1)
5. **Data Quality & Ingestion Flaws** (P2)
6. **Frontend & Offline Kiosk Fragility** (P2)

---

## 2. Critical Security Vulnerabilities (P0)

### 🔴 Bug 1: Cleartext API Key Leaked in Git Repository
- **File:** [`backend/br.env`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/br.env) (Line 1)
- **Code:**
  ```env
  ELEVENLABS_API_KEY=sk_aa2e2581f74c692e7239e8af2bd94223cbef13d86da46179
  ```
- **Severity:** **CRITICAL / SECURITY RISK**
- **Impact:** The secret ElevenLabs API key is stored in plain text and checked into the codebase. Anyone who downloads the ZIP package or clones the repository has full administrative access to consume or deplete ElevenLabs credits.
- **Fix:** Immediately revoke this key from the ElevenLabs dashboard. Move `.env` into `.gitignore` and distribute a sanitized `.env.example`.

---

### 🔴 Bug 2: Unauthenticated and Unrestricted Ingestion Endpoint
- **File:** [`backend/app.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/app.py) (Lines 514–562)
- **Severity:** **HIGH**
- **Impact:** The `/api/ingest` endpoint accepts arbitrary `POST` requests and executes `INSERT OR REPLACE INTO documents` into SQLite without requiring any password, JWT token, or API key. If the kiosk server is placed on LAN Wi-Fi or connected to the public WAN Cloudflare tunnel, any external user can overwrite historical records or inject malicious content directly into the national archive database.
- **Fix:** Implement authentication middleware (API Key or JWT) restricting `/api/ingest` and `/api/sources/sync` to authenticated administrative roles.

---

### 🔴 Bug 3: Wildcard CORS on All Routes
- **File:** [`backend/app.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/app.py) (Lines 56–62)
- **Code:**
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- **Severity:** **MEDIUM / HIGH**
- **Impact:** Permitting `allow_credentials=True` with wildcard `allow_origins=["*"]` violates modern CORS specifications and exposes the local server to Cross-Origin attacks if accessed through browser tabs on the host machine.

---

## 3. Fatal Deployment & Script Bugs (P0)

### 🔴 Bug 4: Wrong Hardcoded Path in `start-local.bat`
- **File:** [`start-local.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/start-local.bat) (Line 3)
- **Code:**
  ```bat
  set "VENV_DIR=C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar_(3)\ambedkar\.venv\Scripts"
  ```
- **Severity:** **FATAL / IMMEDIATE CRASH**
- **Impact:** The folder name in `start-local.bat` is hardcoded to `ambedkar_(3)`, but the actual working project directory is `ambedkar01`. If a user double-clicks `start-local.bat`, it immediately crashes with `The system cannot find the path specified`.
- **Fix:** Replace the hardcoded path with dynamic resolution using `%~dp0`:
  ```bat
  set "VENV_DIR=%~dp0.venv\Scripts"
  ```

---

### 🔴 Bug 5: Machine-Specific Hardcoded Paths in Distribution Scripts
- **Files:** [`start-everything-wan.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/start-everything-wan.bat) and [`create-package.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/create-package.bat)
- **Code in `create-package.bat`:**
  ```bat
  set "PROJECT=C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar"
  set "OUTPUT=C:\Users\NITESH\Downloads\ambedkar-archive-package.zip"
  ```
- **Severity:** **FATAL ON OTHER MACHINES**
- **Impact:** If the project is shared with a judge, another developer, or moved to another drive (e.g. `D:`), the packaging and WAN startup scripts fail completely because they expect `C:\Users\NITESH\...`.
- **Fix:** Replace with relative paths using `%~dp0`.

---

### 🔴 Bug 6: Hardcoded Tesseract Executable Path
- **Files:** [`backend/ocr.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/ocr.py) and [`back/back.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/back/back.py)
- **Code:**
  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```
- **Severity:** **MEDIUM / HIGH**
- **Impact:** If Tesseract is installed in `C:\Program Files (x86)\`, via Chocolatey (`C:\ProgramData\chocolatey\bin`), in user `AppData`, or on a Linux/Docker deployment, OCR operations crash with `TesseractNotFoundError`.
- **Fix:** Use `shutil.which("tesseract")` to dynamically detect the binary from the system `PATH` before falling back to default installation paths.

---

## 4. Architectural Inconsistencies & Dead Code (P1)

### ⚠️ Bug 7: Conflicting Duplicate Backends & Split Databases
- **Issue:** The repository contains two distinct backend implementations:
  1. Primary Modular Backend: [`backend/app.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/app.py) using database [`ambedkar_archive_data/database/ambedkar_archive.db`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/ambedkar_archive_data/database/ambedkar_archive.db).
  2. Legacy Monolithic Backend: [`back/back.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/back/back.py) creating a separate database [`back/ambedkar_archive.db`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/back/ambedkar_archive.db).
- **Severity:** **ARCHITECTURAL DEBT / CONFUSION**
- **Impact:** Modifying code or ingesting data into one backend does not update the other. Developers or scripts running `python back/back.py` operate on an isolated stale database.
- **Fix:** Archive or remove the legacy `back/` folder and consolidate exclusively around `backend/`.

---

### ⚠️ Bug 8: Discrepancies in Document Counts
- **Issue:** The documentation and codebase state differing document counts:
  - `registry.json` claims: **530 items** (510 IA, 10 CAD, 10 Foundation).
  - `SYSTEM_CAPABILITIES_OVERVIEW.md` reports: **538 JSON files** in `processed_data/` vs **537 rows** in SQLite.
  - UI Filter shows: Publications (423), Speeches (63), CAD (20), Manuscripts (4), Historical Records (20) = **530 items**.
- **Impact:** Evaluators running automated verification will spot discrepancies between filesystem files, JSON registry, and SQLite database counts.

---

## 5. Misrepresented AI & OCR Capabilities (P1)

### ⚠️ Bug 9: The "AI Assistant" Is Not an AI Model
- **Files:** [`backend/app.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/app.py) (Lines 78–137, 264–295) and [`frontend/app.js`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/frontend/app.js)
- **The Issue:** The UI presents an "AI Constitutional Research Assistant" and the Analytics tab claims `"Vector RAG Chunks: 835 (Ready for Milvus / ChromaDB)"`.
- **Underlying Reality:** There is **NO** vector database, **NO** embeddings calculation, and **NO** Large Language Model connected to `/api/assistant`. It is a regex keyword lookup using a static dictionary (`ASSISTANT_QUERY_TERMS`) that simply filters summaries.
- **Risk:** Evaluators testing custom questions outside the 4 preset prompts will quickly expose that it does not perform generative synthesis or true semantic reasoning.
- **Fix:** Connect the 835 chunks to a real local vector store (`ChromaDB`) and run a quantized local SLM (e.g. `Llama-3-8B-Q4`).

---

### ⚠️ Bug 10: Missing Handwriting Model File
- **Files:** [`backend/ocr.py`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/backend/ocr.py) and [`frontend/app.js`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/frontend/app.js)
- **The Issue:** The UI provides an option: *"OCR Mode: Handwriting (Ambedkar custom model)"*. Selecting it queries `/api/ocr/model-status`, which looks for:
  ```
  ambedkar_archive_data\ocr_models\tessdata\ambedkar_handwritten_v2.traineddata
  ```
- **Underlying Reality:** This file does not exist in the repository, and `.gitignore` actively ignores the entire `ocr_models/` folder. When a user tests handwriting OCR, it fails with *"Model file is missing"*.
- **Fix:** Train or place the actual model in the path, or clearly label this feature as "Model Training Pipeline (In Progress)" rather than presenting it as active.

---

## 6. Data Quality & Ingestion Flaws (P2)

### ⚠️ Bug 11: Placeholder / Truncated Text in Internet Archive Records
- **File:** `ambedkar_archive_data/texts/`
- **The Issue:** For dozens of records in the Internet Archive collection (e.g. `DOC_IA_hindswaraj_ambedkar_hindi_15`), the `full_text` field does not contain the actual transcription of Dr. Ambedkar's book or speech. Instead, it contains a generic metadata description string:
  > *"Digital archival manuscript held in Internet Archive repository..."*
- **Impact:** Full-text search over these records returns hits based on catalog summaries rather than historical speeches.

---

### ⚠️ Bug 12: Synthetic / Fake Multilingual Translations
- **File:** `ambedkar_archive_data/metadata/registry.json`
- **The Issue:** For many non-English records, the `translations.hi.title` and `translations.mr.title` fields are not true human translations. They are English titles with a machine-appended suffix:
  > `"Annihilation of Caste (अभिलेखागार प्रति)"`
- **Impact:** Misrepresents the platform's translation fidelity to Hindi and Marathi native speakers.

---

## 7. Frontend & Offline Kiosk Fragility (P2)

### ⚠️ Bug 13: Reliance on External CDNs for UI Assets
- **File:** [`frontend/index.html`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/frontend/index.html) (Lines 8–10)
- **Code:**
  ```html
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script src="https://cdn.tailwindcss.com"></script>
  ```
- **Severity:** **HIGH FOR OFFLINE KIOSKS**
- **Impact:** In an air-gapped memorial kiosk without internet access, the browser cannot download `cdn.tailwindcss.com` or FontAwesome from CDN. The entire visual layout collapses, styles break, and icons turn into empty boxes.
- **Fix:** Bundle Tailwind CSS and FontAwesome webfonts locally inside `frontend/assets/`.

---

## 8. Prioritized Remediation Checklist

| Priority | Issue to Resolve | Target File | Action Required |
| :---: | :--- | :--- | :--- |
| **P0** | Leaked ElevenLabs API Key | `backend/br.env` | Revoke key; move to secure `.env.local` ignored by Git. |
| **P0** | Hardcoded wrong folder in batch file | `start-local.bat` | Change `ambedkar_(3)` to dynamic `%~dp0`. |
| **P0** | Absolute path in packaging script | `create-package.bat` | Replace `C:\Users\NITESH...` with `%~dp0`. |
| **P1** | Duplicate backend folders | `back/` vs `backend/` | Deprecate `back/`; point all launchers to `backend/app.py`. |
| **P1** | Hardcoded Tesseract path | `backend/ocr.py` | Add `shutil.which("tesseract")` dynamic lookup. |
| **P1** | Unauthenticated `/api/ingest` | `backend/app.py` | Add basic token authentication for curator actions. |
| **P2** | CDN dependencies in offline kiosk | `frontend/index.html` | Download Tailwind and FontAwesome for 100% offline bundling. |
| **P2** | Dummy full-text in IA records | `ambedkar_archive_data/` | Re-extract or flag items lacking full OCR transcripts. |
