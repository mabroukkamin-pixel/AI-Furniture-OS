from brain.experts.base_expert import BaseExpert
from brain.registry import register


class PreservationExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("   PRESERVATION EXPERT")
        print("========================================")


        brain.preservation = {

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


        print(
            "Product protection activated."
        )


        return brain


register(
    lambda: PreservationExpert()
)