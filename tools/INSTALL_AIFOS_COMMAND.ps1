
$root = (Get-Location).Path

$cmd = @"
@echo off
powershell -ExecutionPolicy Bypass -File "$root\AIFOS.ps1" %*
"@

$target="$env:USERPROFILE\AIFOS.cmd"

Set-Content $target $cmd


$userPath=[Environment]::GetEnvironmentVariable("Path","User")


if($userPath -notlike "*$env:USERPROFILE*"){

    [Environment]::SetEnvironmentVariable(
    "Path",
    $userPath+";"+$env:USERPROFILE,
    "User"
    )

}


Write-Host ""
Write-Host "================================="
Write-Host " AIFOS COMMAND REGISTERED "
Write-Host "================================="

Write-Host ""
Write-Host "Restart PowerShell then use:"
Write-Host ""
Write-Host "AIFOS FULL"

