import os
import json
import datetime
import subprocess
import sys


class AIFOSController:


    def __init__(self):

        self.report={
            "system":"AI Furniture OS V2",
            "time":str(datetime.datetime.now()),
            "checks":[],
            "status":"STARTED"
        }



    def check(self,name,path):

        status=os.path.exists(path)

        self.report["checks"].append(
            {
                "module":name,
                "status":"READY" if status else "MISSING"
            }
        )



    def run_repair(self):

        file="brain/self_healing/engine/repair_engine.py"

        if os.path.exists(file):

            subprocess.run(
                [
                    sys.executable,
                    file
                ]
            )



    def run_pipeline(self):

        subprocess.run(
            [
                sys.executable,
                "-m",
                "runtime.run_pipeline",
                "--product",
                "Partition001"
            ]
        )



    def save(self):

        os.makedirs(
            "docs/reports",
            exist_ok=True
        )


        with open(
            "docs/reports/aifos_controller_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.report,
                f,
                indent=4,
                ensure_ascii=False
            )


        print(
            "REPORT CREATED:"
        )

        print(
            "docs/reports/aifos_controller_report.json"
        )




    def full(self):

        print("")
        print("==============================")
        print(" AI FURNITURE OS FULL CONTROL ")
        print("==============================")


        self.check(
            "Brain",
            "brain/core"
        )


        self.check(
            "Decision Graph",
            "brain/decision_graph"
        )


        self.check(
            "Visual Memory",
            "brain/visual_memory"
        )


        self.check(
            "Fusion",
            "brain/fusion"
        )


        self.check(
            "Runtime",
            "runtime"
        )


        print("")
        print("SELF HEALING")
        self.run_repair()


        print("")
        print("PIPELINE")
        self.run_pipeline()


        self.report["status"]="COMPLETE"

        self.save()



if __name__=="__main__":

    AIFOSController().full()

