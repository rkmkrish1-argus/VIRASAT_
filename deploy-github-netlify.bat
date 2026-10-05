@echo off
setlocal enabledelayedexpansion
title Deploy to GitHub and Netlify - Dr. B.R. Ambedkar Digital Heritage Archive

cd /d "%~dp0"

echo =====================================================================
echo    DR. B.R. AMBEDKAR DIGITAL HERITAGE ARCHIVE
echo    Automated GitHub Sync ^& Netlify Deployment Tool
echo =====================================================================
echo Project Directory: %~dp0
echo.

:: -------------------------------------------------------------
:: Step 1: Check Git Installation
:: -------------------------------------------------------------
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------------
:: Step 2: Ensure netlify.toml exists
:: -------------------------------------------------------------
if not exist "netlify.toml" (
    echo [INFO] Generating netlify.toml for Netlify auto-deployment...
    (
        echo # Netlify Build ^& Deployment Configuration
        echo [build]
        echo   publish = "frontend"
        echo.
        echo [[headers]]
        echo   for = "/assets/*"
        echo   [headers.values]
        echo     Cache-Control = "public, max-age=604800, must-revalidate"
        echo.
        echo [[redirects]]
        echo   from = "/*"
        echo   to = "/index.html"
        echo   status = 200
    ) > netlify.toml
    echo [OK] netlify.toml created.
    echo.
)

:: -------------------------------------------------------------
:: Step 3: Check Git Configuration (user.name and user.email)
:: -------------------------------------------------------------
git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    git config --global user.email >nul 2>&1
    if %errorlevel% neq 0 (
        echo [SETUP] Git needs your user information for commit records.
        echo.
        set /p GIT_NAME="Enter your GitHub Name / Username: "
        set /p GIT_EMAIL="Enter your GitHub Email: "
        if "!GIT_NAME!"=="" set GIT_NAME=AmbedkarArchiveUser
        if "!GIT_EMAIL!"=="" set GIT_EMAIL=user@example.com
        git config --global user.name "!GIT_NAME!"
        git config --global user.email "!GIT_EMAIL!"
        echo [OK] Git identity configured.
        echo.
    )
)

:: -------------------------------------------------------------
:: Step 4: Check / Initialize Git Repository & Remote
:: -------------------------------------------------------------
if not exist ".git" (
    echo [SETUP] Initializing local Git repository...
    git init
    git branch -M main
    echo.
    set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/Username/repo.git): "
    if "!REPO_URL!"=="" (
        echo [ERROR] Repository URL is required.
        pause
        exit /b 1
    )
    git remote add origin !REPO_URL!
    echo [OK] Remote origin connected: !REPO_URL!
    echo.
) else (
    git remote get-url origin >nul 2>&1
    if %errorlevel% neq 0 (
        set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/Username/repo.git): "
        if "!REPO_URL!"=="" (
            echo [ERROR] Repository URL is required.
            pause
            exit /b 1
        )
        git branch -M main
        git remote add origin !REPO_URL!
    )
)

:: Retrieve current remote URL
for /f "tokens=*" %%i in ('git remote get-url origin 2^>nul') do set CURRENT_REPO=%%i
echo Target GitHub Repository: !CURRENT_REPO!
echo.

:: -------------------------------------------------------------
:: Step 5: Stage and Commit Changes
:: -------------------------------------------------------------
echo =====================================================================
echo  [STEP 1/3] Staging and Committing Changes to Git
echo =====================================================================
echo.
git status -s
echo.

set /p USER_MSG="Enter commit description (Press ENTER for default timestamped commit): "
if "!USER_MSG!"=="" (
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set CDATE=%%a-%%b-%%c
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set CTIME=%%a:%%b
    set USER_MSG=Update Ambedkar Digital Heritage Archive [!CDATE! !CTIME!]
)

echo.
echo Staging all changes (excluding ignored files)...
git add .

git status --porcelain | findstr /R "." >nul
if %errorlevel% equ 0 (
    echo Committing changes...
    git commit -m "!USER_MSG!"
) else (
    echo [INFO] No new changes to commit. Working tree is clean.
)
echo.

:: -------------------------------------------------------------
:: Step 6: Push to GitHub
:: -------------------------------------------------------------
echo =====================================================================
echo  [STEP 2/3] Uploading (Pushing) to GitHub
echo =====================================================================
echo Pushing branch 'main' to origin...
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Direct push was rejected. Checking if remote has newer commits...
    echo Attempting pull with rebase...
    git pull --rebase origin main
    echo Retrying push...
    git push -u origin main
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Push failed. Would you like to force push? (Caution: overrides remote changes)
        set /p FORCE_CHOICE="Force push? (y/N): "
        if /i "!FORCE_CHOICE!"=="y" (
            git push -u origin main --force
        ) else (
            echo Skipping push. You can resolve git conflicts manually.
        )
    )
)

echo.
echo [SUCCESS] GitHub repository is up to date!
echo Repository URL: !CURRENT_REPO!
echo You can now edit files directly on GitHub or clone to any machine.
echo.

:: -------------------------------------------------------------
:: Step 7: Netlify Deployment Options
:: -------------------------------------------------------------
echo =====================================================================
echo  [STEP 3/3] Netlify Deployment ^& Continuous Integration
echo =====================================================================
echo.
echo Choose your Netlify deployment method:
echo.
echo  [1] Connect GitHub to Netlify (Continuous Deployment - RECOMMENDED)
echo      Netlify will auto-deploy every time you push or edit code on GitHub.
echo      Opens Netlify's "Import from Git" in your default browser.
echo.
echo  [2] Deploy directly via Netlify CLI (Terminal Upload)
echo      Deploys the 'frontend' folder to Netlify immediately.
echo.
echo  [3] Open GitHub Repository in browser (to edit files online)
echo.
echo  [4] Done / Exit
echo.

set /p DEPLOY_CHOICE="Enter your choice (1-4, Default=1): "
if "!DEPLOY_CHOICE!"=="" set DEPLOY_CHOICE=1

if "!DEPLOY_CHOICE!"=="1" goto NETLIFY_WEB
if "!DEPLOY_CHOICE!"=="2" goto NETLIFY_CLI
if "!DEPLOY_CHOICE!"=="3" goto OPEN_GITHUB
if "!DEPLOY_CHOICE!"=="4" goto FINISH

:NETLIFY_WEB
echo.
echo ---------------------------------------------------------------------
echo  Setting up GitHub Continuous Deployment on Netlify:
echo ---------------------------------------------------------------------
echo  1. In the browser that opens, log into Netlify (or sign up with GitHub).
echo  2. Select "Import an existing project" -> "GitHub".
echo  3. Choose your repository: !CURRENT_REPO!
echo  4. The build settings are auto-configured from netlify.toml:
echo       - Base directory: (leave empty)
echo       - Publish directory: frontend
echo  5. Click "Deploy site".
echo.
echo Every future git push will automatically update your live Netlify site!
echo ---------------------------------------------------------------------
start https://app.netlify.com/start
pause
goto FINISH

:NETLIFY_CLI
echo.
echo ---------------------------------------------------------------------
echo  Deploying directly using Netlify CLI...
echo ---------------------------------------------------------------------
where netlify >nul 2>nul
if %errorlevel% equ 0 (
    netlify deploy --prod --dir=frontend
) else (
    where npx >nul 2>nul
    if %errorlevel% equ 0 (
        echo Netlify CLI not found globally. Running via npx...
        npx --yes netlify-cli deploy --prod --dir=frontend
    ) else (
        echo [ERROR] Node.js / npx not detected. Please install Node.js from https://nodejs.org/
        echo Or use Option 1 to connect via Netlify web dashboard.
    )
)
echo.
pause
goto FINISH

:OPEN_GITHUB
:: Convert SSH git url to HTTPS if needed
set WEB_URL=!CURRENT_REPO!
set WEB_URL=!WEB_URL:git@github.com:=https://github.com/!
set WEB_URL=!WEB_URL:.git=!
echo Opening repository: !WEB_URL!
start !WEB_URL!
pause
goto FINISH

:FINISH
echo.
echo =====================================================================
echo  All operations completed!
echo  - GitHub Repo: !CURRENT_REPO!
echo  - Netlify Config: %~dp0netlify.toml
echo =====================================================================
echo.
pause
