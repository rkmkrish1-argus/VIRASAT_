@echo off
:: ============================================================
::  Dr. B.R. Ambedkar Digital Heritage Archive
::  Package Builder: Creates a self-contained ZIP application
:: ============================================================
title Packaging Ambedkar Archive Application...

set PROJECT=C:\Users\NITESH\Downloads\MEORIAL_KIOSK\MODELS\PROTOTYPE\ambedkar01\ambedkar
set OUTPUT=C:\Users\NITESH\Downloads\ambedkar-archive-package.zip

echo.
echo ============================================================
echo   Packaging Ambedkar Archive Application...
echo ============================================================
echo.

powershell -Command ^
  "Compress-Archive -Force -Path @( ^
    '%PROJECT%\backend', ^
    '%PROJECT%\frontend', ^
    '%PROJECT%\ambedkar_archive_data', ^
    '%PROJECT%\requirements.txt', ^
    '%PROJECT%\Run-Ambedkar-Archive.bat', ^
    '%PROJECT%\Create-Desktop-Shortcut.ps1', ^
    '%PROJECT%\start-local.ps1', ^
    '%PROJECT%\start-local.bat', ^
    '%PROJECT%\start-lan.ps1', ^
    '%PROJECT%\start-wan-tunnel.bat', ^
    '%PROJECT%\start-everything-wan.bat', ^
    '%PROJECT%\README.md' ^
  ) -DestinationPath '%OUTPUT%'"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   [SUCCESS] Shareable package created!
    echo   Location: %OUTPUT%
    echo ============================================================
    echo.
    echo Share this ZIP file with anyone.
    echo When they unzip it, they just double-click:
    echo    "Run-Ambedkar-Archive.bat"
    echo.
) else (
    echo [ERROR] Packaging failed.
)
pause
