import os
import json
import subprocess
from datetime import datetime


class SystemManager:


    def __init__(self):

        self.report = {

            "time":
                str(datetime.now()),

            "checks": {},

            "errors": [],

            "repairs": []

        }



    def check_path(self,path):

        ok = os.path.exists(path)

        self.report["checks"][path] = ok

        return ok



    def backup(self,path):

        if not os.path.exists(path):

            return


        backup = (
            "brain/autonomous/backups/"
            +
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
        )


        os.makedirs(
            backup,
            exist_ok=True
        )


        return backup



    def python_check(self):

        result = subprocess.run(

            [
                "python",
                "-m",
                "compileall",
                "brain",
                "runtime"
            ],

            capture_output=True,

            text=True

        )


        if result.returncode != 0:

            self.report["errors"].append(
                result.stdout
            )

            return False


        return True




    def git_update(self):

        subprocess.run(
            [
                "git",
                "add",
                "."
            ]
        )


        status = subprocess.run(

            [
                "git",
                "status",
                "--porcelain"
            ],

            capture_output=True,

            text=True

        )


        if status.stdout.strip():

            subprocess.run(

                [
                    "git",
                    "commit",
                    "-m",
                    "AI Furniture OS autonomous update"
                ]

            )


            subprocess.run(
                [
                    "git",
                    "push",
                    "origin",
                    "main"
                ]
            )



    def save_report(self):

        os.makedirs(
            "docs/reports",
            exist_ok=True
        )


        with open(

            "docs/reports/system_report.json",

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


        self.check_path(
            "brain/core/brain_state.py"
        )


        self.check_path(
            "brain/decision_graph"
        )


        self.check_path(
            "brain/visual_memory"
        )


        self.check_path(
            "brain/learning"
        )


        self.check_path(
            "runtime/pipeline.py"
        )


        self.python_check()


        self.save_report()


        self.git_update()



        return self.report




if __name__ == "__main__":


    manager = SystemManager()

    result = manager.run()


    print(
        json.dumps(
            result,
            indent=4
        )
    )