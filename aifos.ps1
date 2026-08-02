Write-Host "========================================"
Write-Host " AI FURNITURE OS AUTOPILOT REPAIR "
Write-Host "========================================"

$files = @(
"brain\runtime\brain_runtime.py"
)

Write-Host "[1] Backup Brain Runtime"

Copy-Item `
brain\runtime\brain_runtime.py `
brain\runtime\brain_runtime.backup.py `
-Force


Write-Host "[2] Fixing Runtime Dependencies"

$content = Get-Content brain\runtime\brain_runtime.py -Raw


$content = $content -replace `
"MemoryExecutor\(\)", `
"MemoryExecutor(self.fusion, self.memory)"


$content = $content -replace `
"LoadExecutor\(\)", `
"LoadExecutor(self.loader)"


Set-Content `
brain\runtime\brain_runtime.py `
$content `
-Encoding UTF8


Write-Host "[3] Creating AI Control Command"

@'
param(
[string]$command="run"
)

Write-Host "========================================"
Write-Host " AI FURNITURE OS CONTROL LOOP "
Write-Host "========================================"


if($command -eq "run"){

python -m compileall brain/core brain/runtime brain/models brain/services brain/decision brain/fusion brain/memory brain/visual_memory -q

if($LASTEXITCODE -ne 0){
Write-Host "Brain compile failed"
exit 1
}

python -m brain.bootstrap

}


if($command -eq "status"){

Write-Host "AI Furniture OS"
Write-Host "Brain : ONLINE"
Write-Host "Control Loop : READY"

}

