from brain.runtime.executors.base_executor import BaseExecutor

from brain.reporting.brain_report import BrainReportGenerator

import os


class ReportExecutor(BaseExecutor):


    def __init__(self):

        self.generator = BrainReportGenerator()



    def execute(self,state):


        print("REPORT EXECUTOR")


        html = self.generator.generate(
            state
        )


        folder = state.output_folder


        if not folder:

            folder = (
                "outputs/"
                +
                state.product_id
            )


        os.makedirs(
            folder,
            exist_ok=True
        )


        path = os.path.join(
            folder,
            "brain_report.html"
        )


        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            f.write(html)



        state.artifacts[
            "brain_report"
        ] = path



        print(
            "REPORT CREATED:",
            path
        )


        return state
