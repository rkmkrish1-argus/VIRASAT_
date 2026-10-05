# User Manual & Operator Guide — Dr. B.R. Ambedkar Digital Heritage Archive
**Problem Statement ID:** 26096 | **Target Institution:** Dr. Ambedkar International Centre (DAIC), New Delhi  
**Project Location:** `C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar`

---

## 1. Introduction

Welcome to the **Dr. B.R. Ambedkar Digital Heritage Archive and Institutional Knowledge Platform**. This manual provides complete operational guidance for:
1. **Memorial Visitors & Researchers:** Exploring writings, speeches, timelines, audio narration, and the AI research assistant.
2. **Archivists & Curators:** Ingesting newly scanned manuscripts, performing OCR, and exporting metadata.
3. **Exhibition Operators & System Administrators:** Setting up the server, deploying across LAN Wi-Fi or Cloudflare WAN, configuring touch kiosks, and troubleshooting.

---

## 2. System Requirements & Prerequisites

### Minimum Hardware
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher (Intel Core i5 / Apple M-series recommended).
- **RAM:** 4 GB minimum (8 GB recommended for OCR processing).
- **Storage:** 2 GB free disk space (includes SQLite database, OCR language models, and cached documents).
- **Display:** 1080p Full HD touchscreen or standard desktop monitor.

### Software Dependencies
- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS 12+.
- **Python:** Python 3.10, 3.11, or 3.12 (Check with `python --version`).
- **Tesseract OCR:** Required for scanning PDFs and images.
  - *Windows:* Download installer from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and install to `C:\Program Files\Tesseract-OCR\`.
  - *Linux:* `sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar`
- **Web Browser:** Google Chrome or Microsoft Edge (Chromium-based browser required for Web Speech API and Chromium App-Mode).

---

## 3. Installation & Quick Start

### Step 1: Open the Project Directory
Open PowerShell or Command Prompt in the project folder:
```powershell
cd C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar
```

### Step 2: Initialize Virtual Environment & Dependencies
Run the local setup script:
```powershell
.\start-local.ps1
```
*What this does automatically:*
1. Checks for Python 3.
2. Creates an isolated virtual environment (`.venv`).
3. Installs all required packages from `requirements.txt` (FastAPI, Uvicorn, PyMuPDF, Pytesseract, Pillow, etc.).
4. Starts the FastAPI server at `http://127.0.0.1:8000`.

### Step 3: Launch the User Interface
Open your web browser and navigate to:
```
http://localhost:8000
```
To launch in dedicated, full-screen **Chromium Kiosk App Mode** (without browser bars):
Double-click [`Launch-Ambedkar-Archive.bat`](file:///C:/Users/NITESH/Downloads/MEORIAL_KIOSK/MODELS/PROTOTYPE/ambedkar01/ambedkar/Launch-Ambedkar-Archive.bat).

---

## 4. Multi-Device Exhibition & Network Deployment

### Scenario A: Standalone Single Laptop Kiosk
- **Best For:** Dedicated memorial touch kiosk station or offline evaluation desk.
- **How to Run:**
  Double-click `Run-Ambedkar-Archive.bat` or `Launch-Ambedkar-Archive.bat`.
  The archive launches in fullscreen app mode on the local machine.

---

### Scenario B: Multi-Device LAN (1 Laptop + 2 Phones/Tablets)
- **Best For:** Live Hackathon / Exhibition judging tables where visitors use tablets or phones to browse while the laptop runs the central server.
- **Topology:**
  - **Phone 1:** Acts as a portable Wi-Fi Hotspot router (SSID: `AmbedkarArchive_LAN`).
  - **Laptop:** Connects to Phone 1's hotspot; runs the central server.
  - **Phone 2 / Tablet:** Connects to Phone 1's hotspot; acts as the interactive touchscreen kiosk.
- **How to Start:**
  1. On the Laptop, right-click and run:
     ```powershell
     .\start-lan.ps1
     ```
  2. The script configures the Windows Defender Firewall rule and displays your LAN URL:
     ```
     Other devices on the same Wi-Fi: http://192.168.43.100:8000/
     ```
  3. Open that URL on Phone 2 or any tablet on the network.

---

### Scenario C: Zero-Latency USB Kiosk (ADB Reverse Port Forwarding)
- **Best For:** High-interference convention halls where Wi-Fi is unreliable or blocked.
- **Setup:**
  1. Connect Phone 2 / Android Tablet to the Laptop via a USB cable.
  2. Enable **USB Debugging** on the Android device.
  3. Run the following command in PowerShell on the laptop:
     ```powershell
     adb reverse tcp:8000 tcp:8000
     ```
  4. On the tablet, open Chrome and navigate to `http://localhost:8000`. Traffic routes directly over the high-speed USB bus with zero lag.

---

### Scenario D: Public WAN Tunnel (Global Evaluator Link)
- **Best For:** Sharing the live prototype with judges or evaluators outside your local network.
- **How to Start:**
  1. Ensure the local server is running (`start-local.ps1`).
  2. In a second terminal window, run:
     ```cmd
     start-wan-tunnel.bat
     ```
  3. The script verifies that port 8000 is active and launches the bundled `cloudflared.exe`.
  4. It prints a public secure URL:
     ```
     https://random-words.trycloudflare.com
     ```
  5. Share this URL or generate a QR code for evaluators to test on their personal phones.

---

## 5. Visitor & Researcher Guide

### 1. Searching the Archive
- **Keyword Search:** Type any topic, name, book title, or constitutional article into the top search box (e.g. `Untouchability`, `Directive Principles`, `Rupee`, `Article 356`) and press **Enter** or tap **Search**.
- **Keyboard Shortcut:** Press `Ctrl + K` (or `Cmd + K` on Mac) anywhere on the page to focus the search box.
- **Clear Search:** Tap the `✕` icon inside the search box to clear query filters.

### 2. Using Multi-Parameter Filters
- **Language Dropdown:** Filter records written in any of the 10 indexed languages (English, Hindi, Marathi, Telugu, Tamil, etc.).
- **Type Dropdown:** Filter by Publications, Speeches, CAD Debates, Manuscripts, or Historical Records.
- **Source Dropdown:** Filter between Internet Archive, Constituent Assembly Debates, or Dr. Ambedkar Foundation.
- **Quick Filters:** Tap any of the pre-configured topic chips (*CAD Debates*, *Annihilation of Caste*, *Directive Principles*, *Untouchability*, *Economics & RBI*, *Buddhism & Dhamma*) for instant one-touch exploration.

### 3. Exploring the Historical Timeline
- Tap the **Timeline** tab in the navigation bar.
- Scroll through 11 historical milestone cards spanning 1916 to 1956.
- Tap **"Read Original Historical Record"** on any card to immediately view the corresponding primary source document.

### 4. Interacting with the AI Research Assistant
- Tap the **Research** tab.
- **Preset Prompts:** Tap any of the recommended prompt pills:
  - *Hero Worship / Bhakti in Politics*
  - *Parliamentary vs Presidential System*
  - *Article 356 as 'Dead Letter'*
  - *Caste as Division of Labourers*
- **Custom Questions:** Type your research question into the chat input and click **Ask** or press **Enter**.
- **Voice Input (Speech-to-Text):** Tap the **Microphone** icon (`#aiVoiceBtn`). When the icon turns red and the status displays *"Listening..."*, speak your question clearly in English, Hindi, or Marathi. The transcription appears in real-time. Tap the button again to submit.
- **Reviewing Citations:** Each assistant response provides excerpted historical evidence with a **"View Source"** button.

### 5. Document Inspection & Audio Narration (TTS)
- Tap the title or **Inspect** button on any document card to open the detail modal.
- **Audio Readout:** Tap the large golden **Play** button in the Audio Narration bar. The system will synthesize a spoken reading of the title, summary, and quotes. Tap again to pause or stop.
- **Primary Source Link:** If the record has an official government archive scan available, tap **"View Primary Source"** at the bottom right to open the original PDF mirror.

### 6. Changing Languages & Themes
- **Language Switcher:** In the top navigation bar, tap **EN** (English), **हिंदी** (Hindi), or **मराठी** (Marathi). All interface text, placeholders, timeline events, and voice models adjust dynamically.
- **Theme Toggle:** Tap the **Moon / Sun** icon in the header to switch between Dark and Light mode.
- **Fullscreen Kiosk:** Tap **Kiosk Mode** in the header to enter or exit borderless fullscreen.

---

## 6. Curatorial Guide: Ingesting Documents & OCR

1. Tap the **Contribute** tab in the navigation bar.
2. Fill in the document details:
   - **Document Title:** e.g., *Address at All India Depressed Classes Conference*.
   - **Author / Speaker:** Default: *Dr. B.R. Ambedkar*.
   - **Historical Date:** Enter date in `YYYY-MM-DD` format.
   - **Document Type:** Select *Speech*, *Debate*, *Publication*, or *Manuscript*.
   - **Language:** Select language of the document.
   - **Tags:** Enter comma-separated keywords (e.g. *social_justice, constitution, rights*).
3. **Digitization & OCR:**
   - Under *Scan a PDF or image for OCR*, choose your file (`.pdf`, `.png`, `.jpg`, `.tiff`).
   - Select OCR Mode (*Printed text* or *Handwriting*).
   - Click **Extract Text**. Wait for Tesseract to process the pages.
   - The extracted text automatically populates the *Full Text Content* box below.
4. **Curatorial Verification:**
   - Review the extracted text in the text area. Correct any character misrecognitions or formatting flaws.
5. **Submit to Archive:**
   - Click **Ingest Document Into Pipeline**.
   - The document is immediately stored in SQLite, indexed in the FTS5 virtual table, and saved as a JSON record in `processed_data/`. It is immediately discoverable in the search bar.

---

## 7. Troubleshooting & FAQ

### Q1: The server fails to start with `Port 8000 is already in use`
- **Cause:** Another instance of Python or Uvicorn is running in the background.
- **Solution:**
  In PowerShell, run:
  ```powershell
  Get-Process python* | Stop-Process -Force
  ```
  Then rerun `.\start-local.ps1`.

### Q2: OCR extraction fails with `Tesseract is not installed or not in PATH`
- **Cause:** Tesseract OCR binary was not detected on the machine.
- **Solution:**
  1. Download and run the Windows Tesseract installer from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
  2. Ensure it is installed to `C:\Program Files\Tesseract-OCR\`.
  3. Re-run `backend/setup_ocr_models.py` to ensure Devanagari models are downloaded.

### Q3: Audio Narration gives an error or remains silent
- **Cause:** Cloud ElevenLabs credits are exhausted or network is offline.
- **Behavior:** The archive automatically falls back to your browser's native speech synthesizer. Ensure your system volume is unmuted and the browser tab has permission to play audio.

### Q4: Phone 2 cannot connect to the Laptop over Wi-Fi
- **Cause:** Windows Firewall is blocking inbound connections on port 8000, or the phones are on different subnets.
- **Solution:**
  1. Ensure both devices are connected to the exact same Wi-Fi network or hotspot.
  2. Launch using `start-lan.ps1` (which automatically creates the Windows Firewall inbound rule for port 8000).
  3. Verify the IP address using `ipconfig` on the laptop.
