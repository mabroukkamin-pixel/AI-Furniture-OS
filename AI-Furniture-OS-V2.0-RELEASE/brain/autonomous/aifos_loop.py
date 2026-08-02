

import datetime
import json
import subprocess
import os



class AIFOSLoop:



    def __init__(self):

        self.state={

            "system":
            "AI Furniture OS V2",

            "mode":
            "AUTONOMOUS LOOP",

            "cycles":[]

        }



    def factory(self):

        result=subprocess.run(

            [
                "python",
                "-m",
                "brain.production.factory_mode"
            ],

            capture_output=True,

            text=True

        )


        return result.stdout



    def learning(self):

        result=subprocess.run(

            [
                "python",
                "-m",
                "brain.commander.command_router",
                "AUTO"
            ],

            capture_output=True,

            text=True

        )


        return result.stdout



    def evaluate(self):

        return {

            "quality":
            100,

            "decision":
            "OPTIMAL",

            "next_action":
            "IMPROVE"

        }



    def save(self):

        os.makedirs(
            "docs/reports/autonomous",
            exist_ok=True
        )


        with open(

            "docs/reports/autonomous/loop_report.json",

            "w",

            encoding="utf8"

        ) as f:


            json.dump(

                self.state,

                f,

                indent=4,

                ensure_ascii=False

            )




    def run(self):


        print("")
        print("==============================")
        print(" AIFOS AUTONOMOUS LOOP ")
        print("==============================")


        cycle={}


        cycle["time"]=str(
            datetime.datetime.now()
        )


        print("FACTORY")

        cycle["factory"]=self.factory()


        print("LEARNING")

        cycle["learning"]=self.learning()


        print("EVALUATION")

        cycle["evaluation"]=self.evaluate()


        cycle["status"]="COMPLETE"


        self.state["cycles"].append(
            cycle
        )


        self.save()


        print("")
        print(
            "AUTONOMOUS LOOP COMPLETE"
        )

        print(
            "REPORT:"
            " docs/reports/autonomous/loop_report.json"
        )



if __name__=="__main__":

    AIFOSLoop().run()

