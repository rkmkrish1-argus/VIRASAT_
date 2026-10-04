@echo off
:: ============================================================
::  Dr. B.R. Ambedkar Digital Heritage Archive
::  ALL-IN-ONE WAN Launcher
::  Starts both the Local Server AND the Cloudflare Tunnel
:: ============================================================

title Ambedkar Archive - All-in-One Launcher

set PROJECT_DIR=C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar
cd /d "%PROJECT_DIR%"

echo.
echo ============================================================
echo   Starting Dr. B.R. Ambedkar Digital Heritage Archive
echo ============================================================
echo.

:: 1. Start the Local Server in a separate background window
echo [*] Launching Local Server (FastAPI / Uvicorn)...
start "Ambedkar Archive Server" powershell -NoExit -ExecutionPolicy Bypass -File "%PROJECT_DIR%\start-local.ps1"

:: 2. Wait a few seconds for the server to spin up
echo [*] Waiting for server to initialize on port 8000...
:wait_loop
timeout /t 3 /nobreak >nul
powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000 -TimeoutSec 2 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [*] Still waiting for server to be ready...
    goto wait_loop
)

echo [OK] Server is ready on http://127.0.0.1:8000!
echo.
echo ============================================================
echo   Starting Cloudflare WAN Public Tunnel...
echo ============================================================
echo.

:: 3. Start the tunnel in this window
"%PROJECT_DIR%\cloudflared.exe" tunnel --url http://127.0.0.1:8000
