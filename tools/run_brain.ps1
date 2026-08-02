Write-Host "========================================"
Write-Host "       AI FURNITURE OS - BRAIN RUNNER"
Write-Host "========================================"

Write-Host ""
Write-Host "[1] Checking Python..."

python --version

Write-Host ""
Write-Host "[2] Compiling Active Brain..."

python -m compileall brain `
    -x "legacy" `
    -x "__pycache__"

if ($LASTEXITCODE -ne 0) {
    Write-Host "COMPILE ERROR"
    exit 1
}

Write-Host ""
Write-Host "[3] Running Brain..."

python -m brain.bootstrap

Write-Host ""
Write-Host "========================================"
Write-Host "          BRAIN PROCESS DONE"
Write-Host "========================================"
