$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Creating Python environment..." -ForegroundColor Yellow
    py -m venv (Join-Path $projectRoot ".venv")
}

Write-Host "Installing or updating project dependencies..." -ForegroundColor Cyan
& $python -m pip install -r (Join-Path $projectRoot "requirements.txt")

Write-Host "Starting Dr. B.R. Ambedkar Digital Heritage Archive" -ForegroundColor Green
Write-Host "Website: http://127.0.0.1:8000/"
Write-Host "API docs: http://127.0.0.1:8000/docs"
Write-Host "Press Ctrl+C in this window to stop the server."

Set-Location $projectRoot
& $python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
