Write-Host "[PIPELINE RUN]"

python -m runtime.run_pipeline --product Partition001

if(1 -eq 0){
    Write-Host "PIPELINE OK"
}
else{
    exit 1
}
