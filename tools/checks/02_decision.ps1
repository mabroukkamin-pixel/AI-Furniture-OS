# =====================================================
# AI FURNITURE OS V2
# DECISION GRAPH CHECK
# =====================================================

Write-Host "[DECISION GRAPH CHECK]"


$files = @(
    "outputs\Partition001\decision.json",
    "outputs\Partition001\creative_direction.json",
    "outputs\Partition001\manifest.json"
)


$found = $false


foreach($file in $files){

    if(Test-Path $file){

        Write-Host "FOUND:"
        Write-Host $file

        $found = $true

    }

}



if($found){

    Write-Host "DECISION GRAPH OK"
    exit 0

}
else{

    Write-Host "DECISION GRAPH NOT FOUND"
    exit 1

}