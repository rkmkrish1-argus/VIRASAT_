@echo off
setlocal enabledelayedexpansion
title Update Netlify via GitHub & Check Embeddings - Ambedkar Digital Heritage Archive

cd /d "%~dp0"

echo =====================================================================
echo  DR. B.R. AMBEDKAR DIGITAL HERITAGE ARCHIVE (PS 26096)
echo  Automated Netlify Sync via GitHub ^& Backend Embeddings Audit
echo  Target: https://virasatstarkx.netlify.app/
echo =====================================================================
echo.

:: Check for python
set PYTHON_CMD=python
if exist ".venv\Scripts\python.exe" set PYTHON_CMD=.venv\Scripts\python.exe

%PYTHON_CMD% auto_deploy_and_check.py

echo.
echo =====================================================================
echo  Update Process Complete!
echo =====================================================================
echo.
pause
