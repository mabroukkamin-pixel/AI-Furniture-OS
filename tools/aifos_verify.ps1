# =====================================================
# AI FURNITURE OS V2
# AUTO VERIFY ENGINE
# SELF FIX COMPILE
# =====================================================

$ErrorActionPreference = "Stop"


Write-Host ""
Write-Host "=========================================="
Write-Host " AI FURNITURE OS V2 AUTO VERIFY "
Write-Host "=========================================="


# =========================
# ENVIRONMENT
# =========================

Write-Host ""
Write-Host "[1] ENVIRONMENT"


if(Test-Path ".venv\Scripts\Activate.ps1"){

    & .\.venv\Scripts\Activate.ps1

    Write-Host "ENVIRONMENT OK"

}
else{

    Write-Host "NO VENV FOUND"
    exit 1

}



# =========================
# SMART COMPILE
# =========================

Write-Host ""
Write-Host "[2] SMART COMPILE"


$paths = @(
"brain\core",
"brain\decision_graph",
"brain\decision",
"brain\learning",
"brain\visual_memory",
"brain\knowledge",
"brain\fusion",
"runtime"
)


foreach($p in $paths){

    if(Test-Path $p){

        Write-Host "Checking $p"

        python -m compileall -q $p

        if($LASTEXITCODE -ne 0){

            Write-Host "COMPILE ERROR IN $p"
            exit 1

        }

    }

}


Write-Host "COMPILE PASSED"



# =========================
# PIPELINE
# =========================

Write-Host ""
Write-Host "[3] PIPELINE TEST"


python -m runtime.run_pipeline --product Partition001


if($LASTEXITCODE -ne 0){

Write-Host "PIPELINE FAILED"
exit 1

}


Write-Host "PIPELINE SUCCESS"



# =========================
# SYSTEM CHECKS
# =========================


Write-Host ""
Write-Host "[4] DECISION GRAPH"


if(Test-Path "outputs\Partition001\decision.json"){

Write-Host "DECISION GRAPH OK"

}
else{

Write-Host "DECISION GRAPH NOT FOUND"

}



Write-Host ""
Write-Host "[5] VISUAL MEMORY"


if(Test-Path "brain\visual_memory"){

Write-Host "VISUAL MEMORY OK"

}



Write-Host ""
Write-Host "[6] LEARNING LAYER"


findstr /S /N "ExperienceEngine" runtime\*.py



Write-Host ""
Write-Host "[7] OUTPUT"


if(Test-Path "outputs\Partition001"){

dir outputs\Partition001

}



# =========================
# GIT AUTO
# =========================


Write-Host ""
Write-Host "[8] GIT AUTO"


$changes = git status --porcelain


if($changes){

    git add .

    git commit -m "AI Furniture OS V2 automatic verification update"

    git push origin main

    Write-Host "GITHUB UPDATED"

}
else{

    git push origin main

    Write-Host "NO CHANGES"

}



# =========================
# FINAL
# =========================


Write-Host ""
Write-Host "=========================================="
Write-Host " AI FURNITURE OS V2 READY "
Write-Host "=========================================="


git status