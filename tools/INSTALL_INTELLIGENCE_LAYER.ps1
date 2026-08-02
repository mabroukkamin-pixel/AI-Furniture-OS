
$ErrorActionPreference="Stop"

Write-Host ""
Write-Host "================================="
Write-Host " INSTALL INTELLIGENCE LAYER "
Write-Host "================================="


New-Item brain\intelligence -ItemType Directory -Force | Out-Null



@"

class AgentManager:


    def __init__(self):

        self.agents=[]


    def register(self,name):

        self.agents.append(name)


    def list_agents(self):

        return self.agents


"@ | Out-File brain\intelligence\agent_manager.py -Encoding utf8



@"

class ExpertCouncil:


    def __init__(self):

        self.experts=[

        "material_expert",

        "style_expert",

        "lighting_expert",

        "marketing_expert",

        "camera_expert"

        ]


    def consult(self):

        return self.experts



"@ | Out-File brain\intelligence\expert_council.py -Encoding utf8



@"

class Planner:


    def create_plan(self,task):

        return [

        "analyze",

        "decide",

        "generate",

        "validate",

        "save"

        ]



"@ | Out-File brain\intelligence\planner.py -Encoding utf8




@"

class ReasoningEngine:


    def reason(self,data):

        return {

        "decision":"optimized",

        "confidence":95,

        "input":data

        }


"@ | Out-File brain\intelligence\reasoning_engine.py -Encoding utf8





@"

import json
import os
import datetime



class ExperienceMemory:


    def __init__(self):

        self.file="brain/memory/experience.json"



    def save(self,data):

        os.makedirs(
        os.path.dirname(self.file),
        exist_ok=True
        )


        old=[]


        if os.path.exists(self.file):

            with open(self.file,"r",encoding="utf-8") as f:

                old=json.load(f)



        old.append(data)



        with open(self.file,"w",encoding="utf-8") as f:

            json.dump(
            old,
            f,
            indent=4,
            ensure_ascii=False
            )



"@ | Out-File brain\intelligence\experience_memory.py -Encoding utf8




@"

class LearningManager:


    def improve(self,experience):

        return {

        "learning":"updated",

        "experience":experience

        }



"@ | Out-File brain\intelligence\learning_manager.py -Encoding utf8




@"

from brain.intelligence.agent_manager import AgentManager
from brain.intelligence.expert_council import ExpertCouncil
from brain.intelligence.planner import Planner
from brain.intelligence.reasoning_engine import ReasoningEngine



class IntelligenceCore:


    def __init__(self):

        self.agents=AgentManager()

        self.experts=ExpertCouncil()

        self.planner=Planner()

        self.reasoner=ReasoningEngine()



    def run(self,task):

        return {

        "task":task,

        "plan":
        self.planner.create_plan(task),

        "experts":
        self.experts.consult(),

        "reason":
        self.reasoner.reason(task)

        }



if __name__=="__main__":

    print(
    IntelligenceCore().run(
    "Furniture Product Analysis"
    )
    )


"@ | Out-File brain\intelligence\intelligence_core.py -Encoding utf8





git add .

git commit -m "Add AI Furniture OS Intelligence Layer"

git push origin main


Write-Host ""
Write-Host "================================="
Write-Host " INTELLIGENCE LAYER INSTALLED "
Write-Host "================================="

