@echo off
:: ============================================================
::  Dr. B.R. Ambedkar Digital Heritage Archive
::  Desktop App Launcher
::  Launches the app in native standalone window mode (Edge/Chrome App Mode)
:: ============================================================
title Starting Ambedkar Archive...

set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

:: 1. Start backend server minimized if not already active
powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000 -TimeoutSec 1 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Starting background server...
    start /min "Ambedkar Archive Server" powershell -ExecutionPolicy Bypass -NoProfile -File "%PROJECT_DIR%start-local.ps1"
    
    :: Wait up to 10 seconds for port 8000
    :wait_server
    timeout /t 2 /nobreak >nul
    powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000 -TimeoutSec 1 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
    if %ERRORLEVEL% NEQ 0 goto wait_server
)

:: 2. Launch in native App Mode using Microsoft Edge or Google Chrome (standalone window, no URL bar)
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:8000 --window-size=1280,850
    exit
)

if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8000 --window-size=1280,850
    exit
)

:: Fallback to standard default browser if neither is found
start http://127.0.0.1:8000
exit
