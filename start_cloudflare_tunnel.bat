@echo off
title Cloudflare Tunnel - Ambedkar Digital Heritage Archive
cd /d "%~dp0"
echo ===============================================================
echo  STARTING CLOUDFLARE TUNNEL FOR AMBEDKAR ARCHIVE (PORT 8000)
echo ===============================================================
echo.
if not exist "cloudflared.exe" (
    echo [ERROR] cloudflared.exe not found!
    pause
    exit /b 1
)

echo [*] Exposing http://127.0.0.1:8000 to Cloudflare Edge...
echo.
.\cloudflared.exe tunnel --url http://127.0.0.1:8000
pause
