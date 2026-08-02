import datetime
import json
import os


from brain.autonomous.autonomous_core import AutonomousCore
from brain.commander.command_router import CommandRouter



class MasterController:


    def __init__(self):

        self.report = {

            "system":"AI Furniture OS V2",

            "mode":"MASTER CONTROL",

            "time":str(datetime.datetime.now()),

            "modules":{},

            "status":"STARTING"

        }



    def check(self,name,path):

        exists=os.path.exists(path)

        self.report["modules"][name]={

            "exists":exists,

            "status":"READY" if exists else "MISSING"

        }

        return exists



    def system_check(self):


        self.check(
            "Brain",
            "brain"
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
            "Learning",
            "brain/learning"
        )


        self.check(
            "Evolution",
            "brain/evolution"
        )


        self.check(
            "Runtime",
            "runtime"
        )



    def run_ai_cycle(self):


        print("")
        print("==============================")
        print(" AUTONOMOUS INTELLIGENCE ")
        print("==============================")


        result = AutonomousCore().run(1)


        self.report["autonomous"]=result



    def save_report(self):


        os.makedirs(
            "docs/reports",
            exist_ok=True
        )


        with open(
            "docs/reports/master_controller_report.json",
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
        print("==============================")
        print(" AI FURNITURE OS MASTER ")
        print("==============================")


        self.system_check()


        self.run_ai_cycle()


        self.report["status"]="READY"


        self.save_report()


        print("")
        print("==============================")
        print(" AI FURNITURE OS MASTER READY ")
        print("==============================")



        print(self.report)



if __name__=="__main__":

    MasterController().run()