@echo off
:: ============================================================
::  Dr. B.R. Ambedkar Digital Heritage Archive (PS 26096)
::  One-Click Master Application Launcher
:: ============================================================
title Dr. B.R. Ambedkar Digital Heritage Archive Launcher
cd /d "%~dp0"

echo.
echo  ============================================================
echo    DR. B.R. AMBEDKAR DIGITAL HERITAGE ARCHIVE (PS 26096)
echo    Ministry of Social Justice & Empowerment (MoSJE)
echo    Dr. Ambedkar International Centre (DAIC), New Delhi
echo  ============================================================
echo.

:: 1. Check Python installation & Virtual Environment
if not exist ".venv\Scripts\python.exe" (
    echo [*] Setting up Python virtual environment...
    py -3 -m venv .venv 2>nul || python -m venv .venv 2>nul
    if not exist ".venv\Scripts\python.exe" (
        echo [!] Python 3 is required. Please install Python from https://www.python.org/
        pause
        exit /b 1
    )
    echo [*] Installing dependencies from requirements.txt...
    .\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
)

:: 2. Check if server is already running
powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000/api/health -TimeoutSec 1 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Backend engine is already running on http://127.0.0.1:8000
    goto open_browser
)

:: 3. Launch Backend Engine
echo [*] Starting Archive Engine (FastAPI / SQLite FTS5 / Kraken HTR / Qwen-VL)...
start /min "Ambedkar Archive Backend" powershell -ExecutionPolicy Bypass -NoProfile -Command "Set-Location '%~dp0'; .\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000"

:: 4. Wait for server startup
echo [*] Waiting for server health check...
:wait_loop
timeout /t 1 /nobreak >nul
powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000/api/health -TimeoutSec 1 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% NEQ 0 goto wait_loop

echo [✓] Engine initialized successfully!

:open_browser
echo [*] Opening Digital Heritage Kiosk interface...
echo.
echo  ============================================================
echo   Archive Server Live: http://127.0.0.1:8000
echo   - Student Passcode: {STUDENT} (Standard OCR)
echo   - Researcher Passcode: RESEARCHER (Kraken & Qwen HTR)
echo  ============================================================
echo.

if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:8000 --window-size=1360,900
    exit /b 0
)

if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8000 --window-size=1360,900
    exit /b 0
)

start http://127.0.0.1:8000
exit /b 0
