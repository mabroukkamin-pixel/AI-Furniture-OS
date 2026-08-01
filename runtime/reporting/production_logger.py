import json
import os
from datetime import datetime


class ProductionLogger:

    def __init__(self, log_folder="logs"):

        self.log_folder = log_folder

        os.makedirs(
            self.log_folder,
            exist_ok=True
        )

    def log(self, state):

        filename = (
            datetime.now()
            .strftime("%Y-%m-%d")
            + ".log"
        )

        path = os.path.join(
            self.log_folder,
            filename
        )

        record = {

            "time": datetime.now().isoformat(),

            "run_id": state.run_id,

            "product": state.product_id,

            "status": state.status,

            "stage": state.current_stage,

            "engine": state.engine_name,

            "output": state.output_folder,

            "error": state.error

        }

        with open(
            path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
            )

            f.write("\n")

        return path