from brain.experts.base_expert import BaseExpert
from runtime.models.context import DecisionContext
from brain.registry import register


class PreservationExpert(BaseExpert):

    def analyze(self, context: DecisionContext):

        print("========================================")
        print("   PRESERVATION EXPERT")
        print("========================================")


        if context is None:
            return DecisionContext()


        context.preservation = {

            "lock": True,

            "rules": [
                "preserve exact product geometry",
                "preserve original dimensions",
                "preserve original materials",
                "preserve original colors",
                "preserve texture and craftsmanship",
                "preserve all structural details"
            ],

            "forbidden": [
                "redesign product",
                "change proportions",
                "add elements",
                "remove elements",
                "change material"
            ]

        }


        print("Product protection activated.")

        return context



register(
    lambda: PreservationExpert()
)