
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
