@echo off
:: ============================================================
::  Dr. B.R. Ambedkar Digital Heritage Archive
::  One-Click Application Launcher for Any Windows PC
:: ============================================================
title Ambedkar Digital Heritage Archive
cd /d "%~dp0"

echo ============================================================
echo   Dr. B.R. Ambedkar Digital Heritage Archive
echo ============================================================
echo.

:: 1. Check if virtual environment exists; if not, create it
if not exist ".venv\Scripts\python.exe" (
    echo [*] First-time setup detected. Configuring application...
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        py -m venv .venv
    ) else (
        where python >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            python -m venv .venv
        ) else (
            echo [!] Python is not installed on this computer.
            echo [!] Please install Python 3.11-3.14 from https://www.python.org/
            pause
            exit /b 1
        )
    )
    echo [*] Installing required packages...
    .\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
)

:: 2. Start the backend silently
powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000 -TimeoutSec 1 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [*] Starting Archive engine...
    start /min "" powershell -ExecutionPolicy Bypass -NoProfile -Command "Set-Location '%~dp0'; .\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000"
    
    :wait_loop
    timeout /t 2 /nobreak >nul
    powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000 -TimeoutSec 1 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
    if %ERRORLEVEL% NEQ 0 goto wait_loop
)

:: 3. Launch in standalone Native App Window Mode (Edge or Chrome App Mode)
echo [*] Launching user interface...
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:8000 --window-size=1300,850
    exit
)

if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8000 --window-size=1300,850
    exit
)

start http://127.0.0.1:8000
exit
