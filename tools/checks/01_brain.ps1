Write-Host "[BRAIN CHECK]"

python -m compileall -q brain\core

if($LASTEXITCODE -eq 0){

Write-Host "BRAIN OK"

}
else{

exit 1

}