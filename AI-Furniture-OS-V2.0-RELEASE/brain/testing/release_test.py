
import os
import json
import datetime
import subprocess


class ReleaseTest:


    def __init__(self):

        self.report = {

            "system":
            "AI Furniture OS V2",

            "time":
            str(datetime.datetime.now()),

            "tests":[]

        }



    def add(self,name,status):

        self.report["tests"].append({

            "test":name,

            "status":
            "PASS" if status else "FAIL"

        })



    def check_folders(self):

        folders=[

            "brain",

            "brain/core",

            "brain/decision_graph",

            "brain/visual_memory",

            "brain/production",

            "brain/runtime"

        ]


        return all(
            os.path.exists(x)
            for x in folders
        )



    def command(self,args):

        r=subprocess.run(

            args,

            capture_output=True,

            text=True

        )


        return r.returncode == 0



    def save(self):

        os.makedirs(

            "docs/reports/final",

            exist_ok=True

        )


        with open(

            "docs/reports/final/release_candidate.json",

            "w",

            encoding="utf8"

        ) as f:


            json.dump(

                self.report,

                f,

                indent=4,

                ensure_ascii=False

            )



    def run(self):


        print("==============================")
        print(" AIFOS RELEASE TEST ")
        print("==============================")


        self.add(

            "CORE",

            self.check_folders()

        )


        self.add(

            "AUTO",

            self.command(

                [
                    "python",
                    "-m",
                    "brain.commander.command_router",
                    "AUTO"
                ]

            )

        )


        self.add(

            "FACTORY",

            self.command(

                [
                    "python",
                    "-m",
                    "brain.production.factory_mode"
                ]

            )

        )


        self.add(

            "LOOP",

            self.command(

                [
                    "python",
                    "-m",
                    "brain.autonomous.aifos_loop"
                ]

            )

        )


        self.report["status"]="READY"

        self.save()


        print("==============================")
        print(" RELEASE TEST COMPLETE ")
        print("==============================")

        print(
            "docs/reports/final/release_candidate.json"
        )



if __name__=="__main__":

    ReleaseTest().run()

