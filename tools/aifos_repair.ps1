Write-Host "========================================"
Write-Host " AI FURNITURE OS AUTOPILOT REPAIR "
Write-Host "========================================"

$root = Get-Location


Write-Host "[1] Removing legacy compile blockers..."

$badFile = "brain\legacy\old_engines\prompt_pipeline\prompt_scorer.py"

if(Test-Path $badFile){
    Rename-Item $badFile "prompt_scorer.py.disabled" -Force
}


Write-Host "[2] Fixing Brain Runtime..."

$file="brain\runtime\brain_runtime.py"

if(Test-Path $file){

$content=Get-Content $file -Raw

$content=$content -replace `
"MemoryExecutor\(\)",`
"MemoryExecutor(self.fusion,self.memory)"

Set-Content $file $content -Encoding UTF8

}


Write-Host "[3] Compiling Active Brain..."

python -m compileall `
brain/core `
brain/runtime `
brain/models `
brain/services `
brain/decision `
brain/fusion `
brain/memory `
brain/visual_memory `
-q


if($LASTEXITCODE -ne 0){

Write-Host "COMPILE FAILED"
exit 1

}


Write-Host "[4] Starting AI Brain..."

python -m brain.bootstrap


Write-Host ""
Write-Host "========================================"
Write-Host " AI FURNITURE OS ONLINE "
Write-Host "========================================"

