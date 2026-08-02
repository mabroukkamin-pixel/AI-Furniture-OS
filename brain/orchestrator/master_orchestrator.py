
from brain.system.registry.registry_manager import RegistryManager
import os
import json
from datetime import datetime



class MasterOrchestrator:


    def __init__(self):

        self.registry=RegistryManager()



    def health(self):

        result=[]


        for module in self.registry.active():

            result.append({

            "module":
            module["name"],

            "status":
            "READY"
            if os.path.exists(module["path"])
            else
            "MISSING"

            })


        return result



    def execute(self):


        report={

        "system":
        "AI Furniture OS V2",

        "time":
        datetime.now().isoformat(),

        "health":
        self.health()

        }


        os.makedirs(
        "docs/reports",
        exist_ok=True
        )


        with open(
        "docs/reports/master_orchestrator.json",
        "w",
        encoding="utf-8"
        ) as f:

            json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
            )


        return report



if __name__=="__main__":


    system=MasterOrchestrator()

    print(
    json.dumps(
    system.execute(),
    indent=4,
    ensure_ascii=False
    )
    )

