Write-Host "[VISUAL MEMORY CHECK]"

if(Test-Path "brain\visual_memory"){
    Write-Host "VISUAL MEMORY OK"
}
else{
    Write-Host "VISUAL MEMORY MISSING"
    exit 1
}
