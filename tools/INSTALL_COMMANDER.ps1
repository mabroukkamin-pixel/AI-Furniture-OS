$ErrorActionPreference="Stop"


Write-Host ""
Write-Host "================================="
Write-Host " INSTALL AIFOS COMMANDER CORE "
Write-Host "================================="



New-Item brain\commander -ItemType Directory -Force | Out-Null



@"

import os
import json
import datetime
import subprocess



class AIFOSCommander:


    def __init__(self):

        self.state={}



    def check_module(self,name,path):

        self.state[name]={

            "exists":
            os.path.exists(path),

            "time":
            str(datetime.datetime.now())

        }



    def scan(self):


        modules={

        "brain":
        "brain",

        "decision_graph":
        "brain/decision_graph",

        "visual_memory":
        "brain/visual_memory",

        "learning":
        "brain/learning",

        "evolution":
        "brain/evolution",

        "self_healing":
        "brain/self_healing",

        "runtime":
        "runtime"

        }



        for name,path in modules.items():

            self.check_module(name,path)



    def health_score(self):


        total=len(self.state)

        active=sum(

        1 for x in self.state.values()

        if x["exists"]

        )


        return int(active/total*100)



    def generate_report(self):


        self.state["system_score"]=self.health_score()


        self.state["status"]="READY"


        os.makedirs(
        "docs/reports",
        exist_ok=True)



        with open(
        "docs/reports/commander_report.json",
        "w",
        encoding="utf8") as f:


            json.dump(
            self.state,
            f,
            indent=4)



        return self.state




    def run(self):

        self.scan()

        return self.generate_report()



if __name__=="__main__":

    result=AIFOSCommander().run()

    print(json.dumps(result,indent=4))
"@ | Out-File brain\commander\commander.py -Encoding utf8



@"

from brain.commander.commander import AIFOSCommander


class MasterController:


    def execute(self):

        return AIFOSCommander().run()



if __name__=="__main__":

    print(
    MasterController().execute()
    )
"@ | Out-File brain\commander\master_controller.py -Encoding utf8




# تحديث AIFOS.ps1

Add-Content AIFOS.ps1 @"


Write-Host ""
Write-Host "---------------------------------"
Write-Host "COMMANDER CORE"
Write-Host "---------------------------------"


python brain\commander\commander.py


Write-Host ""
Write-Host "COMMANDER ACTIVE"

"@



git add .

git commit -m "Add AI Furniture OS Commander Core"

git push origin main



Write-Host ""
Write-Host "================================="
Write-Host " COMMANDER INSTALLED "
Write-Host "================================="
