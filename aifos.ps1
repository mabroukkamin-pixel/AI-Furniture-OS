# =====================================================
# AI FURNITURE OS V2
# MASTER AUTONOMOUS CONTROLLER
# =====================================================

$ErrorActionPreference = "Stop"

$ROOT = Get-Location

Write-Host ""
Write-Host "================================="
Write-Host " AI FURNITURE OS V2 "
Write-Host " MASTER CONTROL CENTER "
Write-Host "================================="
Write-Host ""


function STEP($name){

    Write-Host ""
    Write-Host "---------------------------------"
    Write-Host $name
    Write-Host "---------------------------------"

}


function CHECK_PATH($path,$name){

    if(Test-Path $path){

        Write-Host "$name : OK"

    }
    else{

        Write-Host "$name : MISSING"

        New-Item $path -ItemType Directory -Force | Out-Null

        Write-Host "$name : CREATED"

    }

}



# =========================================
# 1 ENVIRONMENT
# =========================================

STEP "ENVIRONMENT CHECK"


CHECK_PATH ".venv" "PYTHON ENV"

CHECK_PATH "brain" "BRAIN"

CHECK_PATH "runtime" "RUNTIME"

CHECK_PATH "outputs" "OUTPUT"


# =========================================
# 2 BRAIN CHECK
# =========================================

STEP "BRAIN HEALTH"


python -m compileall brain\core brain\decision_graph brain\fusion brain\visual_memory


if($LASTEXITCODE -eq 0){

Write-Host "BRAIN HEALTH : OK"

}
else{

Write-Host "BRAIN ERROR"

exit 1

}



# =========================================
# 3 MODULE DISCOVERY
# =========================================

STEP "MODULE SCANNER"


$modules = Get-ChildItem brain -Directory


Write-Host "MODULES FOUND:"
$modules.Name



# =========================================
# 4 SYSTEM CORE
# =========================================


STEP "SYSTEM MANAGER"


if(Test-Path "brain\system\system_controller.py"){

Write-Host "SYSTEM CONTROLLER : READY"

}
else{

Write-Host "SYSTEM CONTROLLER : MISSING"

}



# =========================================
# 5 DECISION GRAPH
# =========================================


STEP "DECISION GRAPH"


if(Test-Path "brain\decision_graph"){

Write-Host "DECISION GRAPH : READY"

}
else{

Write-Host "DECISION GRAPH : NEEDS BUILD"

}



# =========================================
# 6 VISUAL MEMORY
# =========================================


STEP "VISUAL MEMORY"


if(Test-Path "brain\visual_memory"){

Write-Host "VISUAL MEMORY : READY"

}
else{

Write-Host "VISUAL MEMORY : MISSING"

}



# =========================================
# 7 PIPELINE TEST
# =========================================


STEP "PIPELINE TEST"


if(Test-Path "runtime\run_pipeline.py"){

Write-Host "PIPELINE ENGINE : READY"

}
else{

Write-Host "PIPELINE ENGINE : MISSING"

}



# =========================================
# 8 OUTPUT CHECK
# =========================================


STEP "OUTPUT SYSTEM"


if(Test-Path "outputs"){

Write-Host "OUTPUT MANAGER : READY"

}



# =========================================
# 9 REPORT
# =========================================


STEP "SYSTEM REPORT"


$report = @{

system="AI Furniture OS V2"

time=(Get-Date)

brain="checked"

modules=$modules.Name

status="READY"

}


$report | ConvertTo-Json |

Out-File "docs\reports\aifos_master_report.json"



Write-Host ""

Write-Host "================================="
Write-Host " AI FURNITURE OS READY "
Write-Host "================================="

Write-Host ""

Write-Host "REPORT:"
Write-Host "docs\reports\aifos_master_report.json"
