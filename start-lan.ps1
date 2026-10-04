# ============================================================
#  Dr. B.R. Ambedkar Digital Heritage Archive
#  LAN Server Startup Script
#  Accessible to ALL devices on your Wi-Fi / local network
# ============================================================
$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

# --- Create venv if missing ---
if (-not (Test-Path $python)) {
    Write-Host "Creating Python environment..." -ForegroundColor Yellow
    py -m venv (Join-Path $projectRoot ".venv")
}

# --- Install / update dependencies ---
Write-Host "Installing or updating project dependencies..." -ForegroundColor Cyan
& $python -m pip install -q -r (Join-Path $projectRoot "requirements.txt")

# --- Discover this machine's LAN IP address ---
$lanIP = (
    Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.InterfaceAlias -notmatch "Loopback" -and $_.IPAddress -notmatch "^169" } |
    Select-Object -First 1
).IPAddress

if (-not $lanIP) { $lanIP = "0.0.0.0" }

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Dr. B.R. Ambedkar Digital Heritage Archive  [LAN MODE]" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  This computer : http://127.0.0.1:8000/"
Write-Host "  Other devices : http://${lanIP}:8000/"   -ForegroundColor Yellow
Write-Host "  API docs      : http://${lanIP}:8000/docs"
Write-Host ""
Write-Host "  Share the 'Other devices' link with phones / laptops"
Write-Host "  on the SAME Wi-Fi or wired network."
Write-Host ""
Write-Host "  Press Ctrl+C to stop the server."
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# --- Windows Firewall: open port 8000 for inbound connections ---
$ruleName = "Ambedkar Archive Port 8000"
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if (-not $existingRule) {
    Write-Host "Adding Windows Firewall rule for port 8000..." -ForegroundColor Cyan
    New-NetFirewallRule `
        -DisplayName $ruleName `
        -Direction Inbound `
        -Protocol TCP `
        -LocalPort 8000 `
        -Action Allow `
        -Profile Any | Out-Null
    Write-Host "Firewall rule added." -ForegroundColor Green
}

Set-Location $projectRoot

# host 0.0.0.0 = listen on ALL network interfaces (LAN + localhost)
& $python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
