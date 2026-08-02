param(
[string]$command="start"
)

Write-Host "========================================"
Write-Host "        AMIN AI CONTROL CENTER"
Write-Host "========================================"


switch($command){

"start" {

Write-Host "[1] Python Check"
python --version


Write-Host "[2] Active Brain Compile"

python -m compileall 
brain/core 
brain/runtime 
brain/models 
brain/services 
brain/decision 
brain/fusion 
brain/memory 
brain/visual_memory 
-q


if($LASTEXITCODE -ne 0){

Write-Host "BRAIN ERROR"
exit 1

}


Write-Host "[3] Starting AI Furniture OS"

python -m brain.bootstrap

}



"check" {

python -m compileall 
brain/core 
brain/runtime 
brain/models 
brain/services 
brain/decision 
brain/fusion 
brain/memory 
brain/visual_memory

}



"status" {

Write-Host "AMIN AI SYSTEM"
Write-Host "Brain : ONLINE"
Write-Host "Control Loop : READY"

}



"heal" {

Write-Host "AUTO REPAIR MODE"

python -m compileall brain -q

}



default {

Write-Host ""
Write-Host "Commands:"
Write-Host "amin start"
Write-Host "amin check"
Write-Host "amin heal"
Write-Host "amin status"

}

}
