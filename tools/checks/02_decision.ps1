Write-Host "[DECISION GRAPH CHECK]"

if(Test-Path "outputs\Partition001\decision.json"){
    Write-Host "DECISION GRAPH OK"
}
else{
    Write-Host "DECISION GRAPH MISSING"
    exit 1
}
