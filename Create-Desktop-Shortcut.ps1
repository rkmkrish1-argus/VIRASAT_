# ============================================================
#  Dr. B.R. Ambedkar Digital Heritage Archive
#  Creates a Desktop Shortcut for the Application
# ============================================================
$projectDir = $PSScriptRoot
$targetBat = Join-Path $projectDir "Launch-Ambedkar-Archive.bat"
$desktop = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$shortcutPath = Join-Path $desktop "Ambedkar Digital Archive.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetBat
$shortcut.WorkingDirectory = $projectDir
$shortcut.Description = "Dr. B.R. Ambedkar Digital Heritage Archive"

# Use Edge or Python icon if available
$iconCandidate = "C:\Windows\System32\shell32.dll,220"
$shortcut.IconLocation = $iconCandidate
$shortcut.Save()

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Desktop Shortcut Created Successfully!" -ForegroundColor Green
Write-Host "  Location: $shortcutPath" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
