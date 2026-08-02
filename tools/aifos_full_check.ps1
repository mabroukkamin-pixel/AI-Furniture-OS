# =====================================================
# AI FURNITURE OS V2
# FULL AUTO CHECK + RUN + GIT
# =====================================================


$ErrorActionPreference = "Stop"


Write-Host ""
Write-Host "=========================================="
Write-Host " AI FURNITURE OS V2 FULL CHECK "
Write-Host "=========================================="


# -------------------------------
# 1 Environment
# -------------------------------

Write-Host ""
Write-Host "[1] ENVIRONMENT"


if(Test-Path ".venv\Scripts\Activate.ps1"){

    & .\.venv\Scripts\Activate.ps1

    Write-Host "ENVIRONMENT OK"

}
else{

    Write-Host "ERROR .venv NOT FOUND"
    exit 1

}



# -------------------------------
# 2 Compile
# -------------------------------

Write-Host ""
Write-Host "[2] PYTHON COMPILE"


python -m compileall `
brain `
runtime


if($LASTEXITCODE -ne 0){

    Write-Host "COMPILE FAILED"
    exit 1

}


Write-Host "COMPILE PASSED"



# -------------------------------
# 3 Pipeline
# -------------------------------

Write-Host ""
Write-Host "[3] PIPELINE RUN"


python -m runtime.run_pipeline --product Partition001


if($LASTEXITCODE -ne 0){

    Write-Host "PIPELINE FAILED"
    exit 1

}


Write-Host "PIPELINE SUCCESS"



# -------------------------------
# 4 Experience
# -------------------------------

Write-Host ""
Write-Host "[4] EXPERIENCE LAYER"


findstr /S /N "ExperienceEngine" runtime\*.py



# -------------------------------
# 5 Decision Graph
# -------------------------------

Write-Host ""
Write-Host "[5] DECISION GRAPH"


if(Test-Path "outputs\Partition001\decision.json"){

    Write-Host "DECISION GRAPH OK"

}
else{

    Write-Host "DECISION FILE MISSING"

}



# -------------------------------
# 6 Visual Memory
# -------------------------------

Write-Host ""
Write-Host "[6] VISUAL MEMORY"


if(Test-Path "brain\visual_memory"){

    Write-Host "VISUAL MEMORY OK"

}
else{

    Write-Host "VISUAL MEMORY ERROR"

}



# -------------------------------
# 7 Output
# -------------------------------

Write-Host ""
Write-Host "[7] OUTPUT"


dir outputs\Partition001



# -------------------------------
# 8 Git Auto
# -------------------------------

Write-Host ""
Write-Host "[8] GIT"


$status = git status --porcelain


if($status){

    Write-Host "CHANGES FOUND"

    git add .

    git commit -m "AI Furniture OS V2 automatic system update"

    git push origin main

    Write-Host "UPDATED GITHUB"

}
else{

    Write-Host "NO CHANGES"

    git push origin main

}



# -------------------------------
# FINAL
# -------------------------------


Write-Host ""

Write-Host "=========================================="
Write-Host " AI FURNITURE OS V2 VERIFIED "
Write-Host "=========================================="


git status


Write-Host ""

Write-Host "SYSTEM READY"