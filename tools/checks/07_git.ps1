Write-Host "[GIT UPDATE]"

?? tools/aifos_full_check.ps1 ?? tools/stage_01_brain_check.ps1 ?? tools/stage_02_decision_graph.ps1 ?? tools/stage_03_visual_memory.ps1 ?? tools/stage_04_experience.ps1 ?? tools/stage_05_pipeline.ps1 ?? tools/stage_06_artifacts.ps1 ?? tools/stage_07_git.ps1 = git status --porcelain

if(?? tools/aifos_full_check.ps1 ?? tools/stage_01_brain_check.ps1 ?? tools/stage_02_decision_graph.ps1 ?? tools/stage_03_visual_memory.ps1 ?? tools/stage_04_experience.ps1 ?? tools/stage_05_pipeline.ps1 ?? tools/stage_06_artifacts.ps1 ?? tools/stage_07_git.ps1){

    git add .
    git commit -m "AI Furniture OS V2 automatic system update"
    git push origin main

    Write-Host "GITHUB UPDATED"

}
else{

    git push origin main
    Write-Host "NO CHANGES"

}
