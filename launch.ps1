param(
[string]$Product="Partition001"
)


Write-Host "================================================"
Write-Host "        AI FURNITURE OS V2"
Write-Host "        AUTO LAUNCHER"
Write-Host "================================================"


python runtime\start.py --product $Product


Write-Host ""
Write-Host "================================================"
Write-Host "OUTPUT"
Write-Host "================================================"


Start-Process explorer ".\outputs\$Product"

