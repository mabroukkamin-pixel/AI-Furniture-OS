import json
import os


class ReportGenerator:

    def generate(self, state):

        report = {

            "product": state.product_id,

            "status": state.status,

            "engine": state.engine_name,

            "decision": state.decision,

            "design_dna": state.design_dna,

            "audit": state.audit,

            "generation": state.generation,

            "artifacts": state.artifacts,

            "trace": state.trace

        }

        folder = state.output_folder

        os.makedirs(
            folder,
            exist_ok=True
        )

        path = os.path.join(
            folder,
            "production_report.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False
            )

        return path