
import os
import json
import datetime
import subprocess
import sys


class AutoEngine:


    def __init__(self):

        self.report = {

            "system":
            "AI Furniture OS V2",

            "mode":
            "AUTO",

            "time":
            str(datetime.datetime.now()),

            "steps":[],

            "status":
            "STARTED"
        }



    def step(self,name):

        self.report["steps"].append(
            {
                "step":name,
                "status":"DONE"
            }
        )

        print(
            "[OK]",
            name
        )



    def run_check(self):

        self.step(
            "SYSTEM CHECK"
        )

        subprocess.run(
            [
                sys.executable,
                "brain/system/module_scanner.py"
            ]
        )



    def run_healing(self):

        self.step(
            "SELF HEALING"
        )

        file="brain/self_healing/engine/repair_engine.py"

        if os.path.exists(file):

            subprocess.run(
                [
                    sys.executable,
                    file
                ]
            )



    def run_evolution(self):

        self.step(
            "EVOLUTION"
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "brain.evolution.evolution_engine"
            ]
        )



    def run_pipeline(self):

        self.step(
            "PIPELINE"
        )


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
            "docs/reports/aifos_auto_report.json",
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                self.report,
                f,
                indent=4,
                ensure_ascii=False
            )



    def run(self):

        print("")
        print("============================")
        print(" AI FURNITURE OS AUTO MODE ")
        print("============================")


        self.run_check()

        self.run_healing()

        self.run_evolution()

        self.run_pipeline()


        self.report["status"]="COMPLETE"


        self.save()



        print("")
        print("============================")
        print(" AUTO COMPLETE ")
        print("============================")



if __name__=="__main__":

    AutoEngine().run()

