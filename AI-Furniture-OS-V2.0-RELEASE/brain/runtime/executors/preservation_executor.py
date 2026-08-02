from brain.runtime.executors.base_executor import BaseExecutor


class PreservationExecutor(BaseExecutor):

    def execute(self, state):

        print("PRESERVATION EXECUTOR")

        state.preservation = {
            "rules": [
                "DO NOT MODIFY PRODUCT",
                "PRESERVE ORIGINAL SHAPE",
                "PRESERVE ORIGINAL MATERIAL",
                "PRESERVE ORIGINAL COLORS",
                "ONLY CHANGE ENVIRONMENT AND LIGHTING"
            ]
        }

        return state