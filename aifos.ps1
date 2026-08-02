# =====================================================
# AI FURNITURE OS V2
# AUTONOMOUS MASTER CONTROL PANEL
# =====================================================

$ErrorActionPreference = "Stop"


$ROOT = Get-Location

$TIME = Get-Date -Format "yyyyMMdd_HHmmss"

$LOG = "docs\reports\aifos_$TIME.log"

$REPORT = "docs\reports\aifos_$TIME.json"


New-Item -ItemType Directory -Force docs\reports | Out-Null


function Write-Log($text){

    Write-Host $text

    Add-Content `
    -Path $LOG `
    -Value $text

}



Write-Log ""

Write-Log "================================="

Write-Log " AI FURNITURE OS V2 MASTER "

Write-Log "================================="



# =====================================================
# 1 ENVIRONMENT
# =====================================================


Write-Log ""

Write-Log "[1] ENVIRONMENT CHECK"


if(Test-Path ".venv\Scripts\Activate.ps1"){

    & .\.venv\Scripts\Activate.ps1

    Write-Log "ENVIRONMENT OK"

}
else{

    Write-Log "ENVIRONMENT MISSING"

    exit 1

}




# =====================================================
# 2 PYTHON CHECK
# =====================================================


Write-Log ""

Write-Log "[2] PYTHON CHECK"



python -m compileall `
brain\core `
brain\decision `
brain\decision_graph `
brain\learning `
brain\visual_memory `
runtime



if($LASTEXITCODE -ne 0){

    Write-Log "PYTHON CHECK FAILED"

    exit 1

}


Write-Log "PYTHON OK"




# =====================================================
# 3 MODULE CHECK
# =====================================================


Write-Log ""

Write-Log "[3] MODULE CHECK"



$modules=@(

"brain\core\brain_state.py",

"brain\learning",

"brain\visual_memory",

"brain\decision_graph",

"runtime\pipeline.py",

"runtime\run_pipeline.py"

)



$result=@{}



foreach($m in $modules){


    if(Test-Path $m){

        $result[$m]="OK"

        Write-Log "$m OK"

    }
    else{

        $result[$m]="MISSING"

        Write-Log "$m MISSING"

    }

}




# =====================================================
# 4 PIPELINE
# =====================================================


Write-Log ""

Write-Log "[4] PIPELINE RUN"



python -m runtime.run_pipeline --product Partition001



if($LASTEXITCODE -ne 0){

    Write-Log "PIPELINE FAILED"

    exit 1

}



Write-Log "PIPELINE SUCCESS"




# =====================================================
# 5 DECISION GRAPH
# =====================================================


Write-Log ""

Write-Log "[5] DECISION GRAPH"



$decisionFiles=@(

"outputs\Partition001\decision.json",

"outputs\Partition001\creative_direction.json",

"outputs\Partition001\manifest.json"

)



$decisionOK=$false



foreach($file in $decisionFiles){

    if(Test-Path $file){

        Write-Log "FOUND $file"

        $decisionOK=$true

    }

}



if($decisionOK){

    Write-Log "DECISION GRAPH OK"

}
else{

    Write-Log "DECISION GRAPH NOT FOUND"

}




# =====================================================
# 6 VISUAL MEMORY
# =====================================================


Write-Log ""

Write-Log "[6] VISUAL MEMORY"



if(Test-Path "brain\visual_memory"){

    Write-Log "VISUAL MEMORY OK"

}
else{

    Write-Log "VISUAL MEMORY ERROR"

}




# =====================================================
# 7 LEARNING
# =====================================================


Write-Log ""

Write-Log "[7] LEARNING LAYER"



$learning=@(

"brain\learning\experience_engine.py",

"brain\learning\experience_memory.py",

"brain\learning\learning_engine.py",

"brain\learning\reward_system.py"

)



foreach($l in $learning){

    if(Test-Path $l){

        Write-Log "$l OK"

    }
    else{

        Write-Log "$l MISSING"

    }

}




# =====================================================
# 8 OUTPUT
# =====================================================


Write-Log ""

Write-Log "[8] OUTPUT"



if(Test-Path "outputs\Partition001"){

    dir outputs\Partition001 |

    Out-String |

    Add-Content $LOG


    Write-Log "OUTPUT OK"

}
else{

    Write-Log "OUTPUT MISSING"

}




# =====================================================
# 9 REPORT
# =====================================================


Write-Log ""

Write-Log "[9] CREATE REPORT"



$system=@{

time=$TIME

modules=$result

decision=$decisionOK

status="completed"

}



$system |

ConvertTo-Json -Depth 5 |

Set-Content $REPORT



Write-Log "REPORT CREATED"




# =====================================================
# 10 GIT AUTO
# =====================================================


Write-Log ""

Write-Log "[10] GIT"



$status=git status --porcelain



if($status){


    git add .


    git commit `
    -m "AI Furniture OS V2 autonomous update"



    git push origin main


    Write-Log "GITHUB UPDATED"


}
else{


    Write-Log "NO CHANGES"

}




# =====================================================
# FINAL
# =====================================================


Write-Log ""

Write-Log "================================="

Write-Log " AI FURNITURE OS V2 READY "

Write-Log "================================="


Write-Log ""

Write-Log "REPORT:"

Write-Log $REPORT

Write-Log ""

git status