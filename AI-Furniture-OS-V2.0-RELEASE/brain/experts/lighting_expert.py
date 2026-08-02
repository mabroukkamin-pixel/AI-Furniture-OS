from brain.experts.base_expert import BaseExpert


class LightingExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("    LIGHTING EXPERT")
        print("========================================")

        current_lighting = brain.decision.get(
            "lighting",
            {}
        )

        if (
            isinstance(current_lighting, dict)
            and current_lighting.get("primary")
        ):

            lighting_type = current_lighting.get(
                "primary"
            )

        elif isinstance(current_lighting, list) and current_lighting:

            lighting_type = current_lighting[0]

        else:

            lighting_type = "warm_daylight"

        brain.lighting = {

            "type": lighting_type,

            "direction": "soft_side_light",

            "quality": "cinematic"

        }

        print("LIGHTING RESULT:")
        print(brain.lighting)

        return brain