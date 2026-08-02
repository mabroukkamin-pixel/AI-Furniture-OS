

Write-Host ""
Write-Host "================================="
Write-Host " AI FURNITURE OS V2 INSTALLER "
Write-Host "================================="
Write-Host ""


$root = Get-Location


Write-Host "CHECK PROJECT"


if (!(Test-Path "brain")) {

    Write-Host "ERROR: Brain folder missing"
    exit

}


Write-Host "BRAIN FOUND"


Write-Host "CREATING LAUNCHERS"


@"
@echo off

cd /d %~dp0

call .venv\Scripts\activate

python -m brain.autonomous.aifos_loop

pause

"@ | Out-File START_AIFOS.bat -Encoding ascii



@"
@echo off

cd /d %~dp0

call .venv\Scripts\activate

python -m brain.commander.command_router FULL

pause

"@ | Out-File AIFOS_START.bat -Encoding ascii



New-Item release -ItemType Directory -Force | Out-Null


@{

system="AI Furniture OS V2"

installed=(Get-Date).ToString()

status="INSTALLED"

} |
ConvertTo-Json |
Out-File release/install.json



Write-Host ""

Write-Host "INSTALL COMPLETE"

Write-Host ""

Write-Host "RUN:"
Write-Host " START_AIFOS.bat"

