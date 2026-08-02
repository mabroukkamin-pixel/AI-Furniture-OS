import os
import shutil
import json
from datetime import datetime


class RepairEngine:


    def __init__(self):

        self.report = []

        self.backup_path = (
            "brain/system/backups"
        )



    def check(self,path):

        return os.path.exists(path)



    def backup_search(self,name):

        if not os.path.exists(
            self.backup_path
        ):
            return None


        for root,dirs,files in os.walk(
            self.backup_path
        ):

            for file in files:

                if name in file:

                    return os.path.join(
                        root,
                        file
                    )

        return None



    def repair(self,path):


        if self.check(path):

            self.report.append({

                "file":path,

                "status":"OK"

            })

            return True



        name=os.path.basename(path)


        backup=self.backup_search(
            name
        )


        if backup:

            os.makedirs(
                os.path.dirname(path),
                exist_ok=True
            )


            shutil.copy(
                backup,
                path
            )


            self.report.append({

                "file":path,

                "status":
                    "RESTORED"

            })

            return True



        self.report.append({

            "file":path,

            "status":
                "MISSING"

        })

        return False



    def save_report(self):

        os.makedirs(
            "docs/reports",
            exist_ok=True
        )


        file=(
            "docs/reports/"
            +
            "repair_"
            +
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
            +
            ".json"
        )


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.report,
                f,
                indent=4
            )


        return file



if __name__=="__main__":


    engine=RepairEngine()


    targets=[

        "brain/core/brain_state.py",

        "brain/decision_graph",

        "brain/visual_memory",

        "brain/fusion"

    ]


    for item in targets:

        engine.repair(item)



    print(
        engine.report
    )


    print(
        engine.save_report()
    )
