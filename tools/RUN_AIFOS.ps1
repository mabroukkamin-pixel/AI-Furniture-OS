$ErrorActionPreference="Stop"

Write-Host ""
Write-Host "================================="
Write-Host " AI FURNITURE OS V2 CONTROL PANEL "
Write-Host "================================="


$checks = @(
"01_brain.ps1",
"02_decision.ps1",
"03_visual_memory.ps1",
"04_learning.ps1",
"05_pipeline.ps1",
"06_output.ps1",
"07_git.ps1"
)


foreach($check in $checks){

    Write-Host ""
    Write-Host "RUNNING $check"
    Write-Host "----------------------------"

    powershell -ExecutionPolicy Bypass -File ".\tools\checks\$check"


    if($LASTEXITCODE -ne 0){

        Write-Host ""
        Write-Host "FAILED : $check"
        exit 1

    }

}


Write-Host ""
Write-Host "================================="
Write-Host " AI FURNITURE OS V2 ALL READY "
Write-Host "================================="