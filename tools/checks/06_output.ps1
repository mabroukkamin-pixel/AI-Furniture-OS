Write-Host "[OUTPUT CHECK]"

if(Test-Path "outputs\Partition001"){
    dir outputs\Partition001
    Write-Host "OUTPUT OK"
}
else{
    exit 1
}
