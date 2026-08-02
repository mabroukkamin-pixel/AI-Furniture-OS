param(
    [string]$Product="Partition001"
)

Write-Host "======================================"
Write-Host " AI FURNITURE OS V2"
Write-Host " AUTO LAUNCHER"
Write-Host "======================================"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $root


if(Test-Path ".venv\Scripts\Activate.ps1")
{
    Write-Host "Activating Environment..."
    & ".\.venv\Scripts\Activate.ps1"
}


Write-Host ""
Write-Host "RUNNING BRAIN:"
Write-Host $Product
Write-Host ""


python runtime\start.py --product $Product


if($LASTEXITCODE -eq 0)
{

    Write-Host ""
    Write-Host "======================================"
    Write-Host " BRAIN COMPLETED"
    Write-Host "======================================"

    $report =
    "outputs\$Product\brain_report.html"


    if(Test-Path $report)
    {
        Write-Host "Opening Report..."
        Start-Process $report
    }

    else
    {
        Write-Host "Report not found yet"
    }

}

else
{
    Write-Host ""
    Write-Host "BRAIN FAILED"
}
