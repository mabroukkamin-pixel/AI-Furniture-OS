$ErrorActionPreference="Stop"

Write-Host ""
Write-Host "================================="
Write-Host " INSTALL EVOLUTION CORE "
Write-Host "================================="


New-Item brain\evolution -ItemType Directory -Force | Out-Null
New-Item docs\evolution -ItemType Directory -Force | Out-Null


@"
import os
import json
from datetime import datetime


class SystemAnalyzer:


    def scan(self):

        layers = [

            "brain/core",
            "brain/decision_graph",
            "brain/knowledge",
            "brain/fusion",
            "brain/visual_memory",
            "brain/learning",
            "brain/self_healing",
            "brain/system",
            "runtime"

        ]


        result={}


        for layer in layers:

            result[layer] = (
                "ACTIVE"
                if os.path.exists(layer)
                else
                "MISSING"
            )


        return result



    def report(self):

        return {

            "time":
            datetime.now().isoformat(),

            "layers":
            self.scan()

        }
"@ | Out-File brain\evolution\system_analyzer.py -Encoding utf8



@"
import json
import os
from datetime import datetime


class EvolutionMemory:


    def save(self,data):

        os.makedirs(
            "docs/evolution",
            exist_ok=True
        )


        file = (
            "docs/evolution/evolution_"
            +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            +
            ".json"
        )


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )


        return file
"@ | Out-File brain\evolution\evolution_memory.py -Encoding utf8



@"
from brain.evolution.system_analyzer import SystemAnalyzer
from brain.evolution.evolution_memory import EvolutionMemory


class EvolutionEngine:


    def run(self):

        analyzer = SystemAnalyzer()

        data = analyzer.report()

        data["status"]="EVOLUTION ACTIVE"

        memory = EvolutionMemory()

        return memory.save(data)



if __name__=="__main__":

    engine = EvolutionEngine()

    print(
        engine.run()
    )
"@ | Out-File brain\evolution\evolution_engine.py -Encoding utf8



Write-Host ""
Write-Host "EVOLUTION CORE CREATED"
Write-Host ""

python brain\evolution\evolution_engine.py
