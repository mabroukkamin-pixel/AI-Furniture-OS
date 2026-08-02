$ErrorActionPreference="Stop"

Write-Host ""
Write-Host "================================="
Write-Host " INSTALL AIFOS COMMAND "
Write-Host "================================="
Write-Host ""


$root=(Get-Location).Path


$cmdPath="$root\AIFOS.cmd"


@"
@echo off
cd /d "$root"

if "%1"=="FULL" (
    python brain\control\aifos_controller.py
    exit /b
)

echo.
echo =================================
echo AI FURNITURE OS V2
echo.
echo Usage:
echo AIFOS FULL
echo =================================

"@ | Out-File $cmdPath -Encoding ascii



# Add current folder to user PATH

$current=[Environment]::GetEnvironmentVariable(
"Path",
"User"
)


if($current -notlike "*$root*")
{
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$current;$root",
        "User"
    )
}



Write-Host ""
Write-Host "AIFOS COMMAND INSTALLED"
Write-Host ""
Write-Host "Restart PowerShell then use:"
Write-Host ""
Write-Host "AIFOS FULL"