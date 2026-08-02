import yaml


class ContextResolver:

    def __init__(self):

        with open(
            "brain/knowledge/scenes.yaml",
            encoding="utf-8"
        ) as f:

            self.scenes = yaml.safe_load(f)

    def resolve(self, decision):

        style = decision.get(
            "style",
            ""
        )

        mapping = {

            "gulf_villa": "luxury_villa",

            "luxury_resort": "resort",

            "modern_natural_home": "warm_home",

            "japandi": "japandi"

        }

        scene_name = mapping.get(
            style,
            "living_room"
        )

        scene = self.scenes.get(
            scene_name,
            {}
        )

        return {

            "style": style,

            "scene": scene_name,

            "colors": [
                "beige",
                "ivory",
                "gold"
            ],

            "mood": decision.get(
                "mood",
                []
            ),

            "lighting": scene.get(
                "lighting",
                ["warm_daylight"]
            ),

            "architecture": {

                "materials":
                    scene.get(
                        "architecture",
                        []
                    )

            },

            "accessories": {

                "items":
                    scene.get(
                        "accessories",
                        []
                    )

            }

        }