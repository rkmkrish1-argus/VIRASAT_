@echo off
setlocal enabledelayedexpansion
title GitHub Upload & Sync Tool

cd /d "%~dp0"

echo ========================================================
echo          GitHub Project Upload & Sync Tool
echo ========================================================
echo Project Directory: %~dp0
echo.

:: 1. Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not found in system PATH.
    echo Please download and install Git from: https://git-scm.com/
    echo.
    pause
    exit /b 1
)

:: 2. Check Git User Identity
git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    git config --global user.email >nul 2>&1
    if %errorlevel% neq 0 (
        echo [REQUIRED SETUP] Git needs your Name and Email to record commits.
        echo.
        set /p GIT_NAME="Enter your GitHub Name / Username (e.g. rkmkrish1-argus): "
        set /p GIT_EMAIL="Enter your GitHub Email: "
        
        if "!GIT_NAME!"=="" set GIT_NAME=rkmkrish1-argus
        if "!GIT_EMAIL!"=="" set GIT_EMAIL=user@example.com
        
        git config --global user.name "!GIT_NAME!"
        git config --global user.email "!GIT_EMAIL!"
        echo.
        echo [SUCCESS] Identity configured: !GIT_NAME! ^<!GIT_EMAIL!^>
        echo.
    )
)

:: 3. Check if repository is initialized
if not exist ".git" (
    echo [FIRST-TIME SETUP] Git repository not initialized.
    echo.
    set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/Username/repo.git): "
    
    if "!REPO_URL!"=="" (
        echo.
        echo [ERROR] Repository URL cannot be empty! Please run this script again.
        pause
        exit /b 1
    )

    echo.
    echo Initializing local repository...
    git init
    git branch -M main
    git remote add origin !REPO_URL!
    echo [SETUP COMPLETE] Repository connected to !REPO_URL!
    echo.
)

:: 4. Show connected repository
echo Connected Repository:
git remote get-url origin 2>nul
if %errorlevel% neq 0 (
    set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/Username/repo.git): "
    git init
    git branch -M main
    git remote add origin !REPO_URL!
)
echo.

:: 5. Ask user for commit message
echo Enter a description for your changes (or press ENTER to use default):
set /p USER_MSG="Commit message: "

if "%USER_MSG%"=="" (
    set COMMIT_MSG=Initial commit of project files
) else (
    set COMMIT_MSG=%USER_MSG%
)

echo.
echo ========================================================
echo Step 1: Adding all files...
git add .

echo Step 2: Committing files...
git commit -m "%COMMIT_MSG%"

echo.
echo Step 3: Uploading (pushing) to GitHub...
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ========================================================
    echo  [SUCCESS] All files successfully uploaded to GitHub!
    echo ========================================================
) else (
    echo ========================================================
    echo  [NOTICE] Push completed with warnings or errors.
    echo ========================================================
)

echo.
pause
