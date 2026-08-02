import yaml


class ContextResolver:

    def __init__(self):

        with open(
            "brain/knowledge/styles.yaml",
            encoding="utf-8"
        ) as f:

            self.styles = yaml.safe_load(f)

        with open(
            "brain/knowledge/scenes.yaml",
            encoding="utf-8"
        ) as f:

            self.scenes = yaml.safe_load(f)

        with open(
            "brain/knowledge/cameras.yaml",
            encoding="utf-8"
        ) as f:

            self.cameras = yaml.safe_load(f)

        with open(
            "brain/knowledge/lighting.yaml",
            encoding="utf-8"
        ) as f:

            self.lighting_data = yaml.safe_load(f)

    def resolve(self, state):

        decision = state.decision

        style = decision.get(
            "style",
            ""
        )

        style_data = self.styles.get(
            style,
            {}
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

        camera_config = self.cameras.get(
            "hero_shot",
            {
                "lens": "50mm",
                "angle": "eye level"
            }
        )

        return {

            "style": style,

            "colors":
                style_data.get(
                    "colors",
                    []
                ),

            "lighting": {

                "types":
                    style_data.get(
                        "lighting",
                        []
                    )

            },

            "mood":
                style_data.get(
                    "mood",
                    []
                ),

            "architecture": {

                "architecture":
                    scene.get(
                        "architecture",
                        [
                            "travertine",
                            "limestone",
                            "oak"
                        ]
                    ),

                "walls":
                    [
                        "neutral_walls"
                    ],

                "floors":
                    [
                        "natural_stone"
                    ],

                "avoid":
                    []

            },

            "accessories": {

                "recommended":
                    {
                        "furniture":
                            [],

                        "decor":
                            scene.get(
                                "accessories",
                                style_data.get(
                                    "accessories",
                                    []
                                )
                            )

                    },

                "avoid":
                    []

            },

            "camera": {

                "lens":
                    camera_config.get(
                        "lens",
                        "50mm"
                    ),

                "angle":
                    camera_config.get(
                        "angle",
                        "eye level"
                    ),

                "shot":
                    camera_config.get(
                        "shot",
                        "hero product shot"
                    )

            }

        }