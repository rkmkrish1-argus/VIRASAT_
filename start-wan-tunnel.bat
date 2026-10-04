@echo off
:: ============================================================
::  Dr. B.R. Ambedkar Digital Heritage Archive
::  WAN Tunnel Launcher (via Cloudflare Quick Tunnel - FREE)
::  No account needed. No domain needed.
::  Anyone on the internet can visit the generated link.
:: ============================================================

title Ambedkar Archive - WAN Tunnel

echo.
echo ============================================================
echo   Dr. B.R. Ambedkar Digital Heritage Archive  [WAN TUNNEL]
echo ============================================================
echo.

:: Check if cloudflared is installed
where cloudflared >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] cloudflared not found. Downloading now...
    echo.
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile '%~dp0cloudflared.exe'"
    set CLOUDFLARED=%~dp0cloudflared.exe
) else (
    set CLOUDFLARED=cloudflared
)

:: Check if the local server is already running
echo [*] Checking if local server is running on port 8000...
powershell -Command "try { $r=(Invoke-WebRequest http://127.0.0.1:8000 -TimeoutSec 2 -UseBasicParsing).StatusCode; if($r -eq 200){exit 0}else{exit 1} } catch { exit 1 }" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Local server is NOT running.
    echo [!] Please run start-local.ps1 or start-lan.ps1 first in another window.
    echo [!] Then re-run this script.
    echo.
    pause
    exit /b 1
)

echo [OK] Local server is running.
echo.
echo [*] Starting Cloudflare Quick Tunnel...
echo [*] A public HTTPS link will appear below in a few seconds.
echo [*] Share that link with anyone worldwide.
echo.
echo ============================================================
echo   Press Ctrl+C to close the tunnel when done.
echo ============================================================
echo.

%CLOUDFLARED% tunnel --url http://127.0.0.1:8000
