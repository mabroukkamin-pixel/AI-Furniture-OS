from brain.composers.master_prompt_composer import MasterPromptComposer


class BrainContext:

    def __init__(self):

        self.product = {
            "name": "Rattan Partition",
            "category": "room_divider",

            "material": {
                "primary": "rattan",
                "secondary": [
                    "wood"
                ]
            },

            "style": [
                "natural",
                "bohemian",
                "japandi"
            ],

            "usage": [
                "living room",
                "villa interior"
            ],

            "colors": {
                "primary": [
                    "beige",
                    "natural wood"
                ]
            },

            "size": {
                "width": 200,
                "height": 180
            }
        }


        self.environment = {

            "primary":
            "luxury villa interior",

            "atmosphere":
            [
                "warm luxury lifestyle",
                "premium Gulf home"
            ],

            "architecture":
            {

                "architecture":
                [
                    "modern luxury interior"
                ],

                "walls":
                [
                    "travertine walls",
                    "marble panels"
                ],

                "floors":
                [
                    "warm wood flooring"
                ],

                "avoid":
                [
                    "industrial appearance"
                ]

            },

            "options":
            [
                "premium living room",
                "luxury resort interior"
            ]
        }


        self.scene = {}

        self.architecture = {}

        self.accessory = {}

        self.lighting = {

            "type":
            "warm golden hour",

            "direction":
            "soft sunlight from large windows",

            "quality":
            "cinematic HDR lighting"

        }

        self.camera = {

            "shot":
            [
                "hero furniture advertisement shot"
            ],

            "lens":
            "50mm",

            "angle":
            "45 degree"

        }

        self.composition = {}

        self.branding = {

            "company":
            "Chinese Market",

            "arabic":
            "السوق الصيني",

            "colors":
            [
                "gold",
                "royal blue",
                "white"
            ],

            "style":
            "premium"

        }

        self.marketing = {}

        self.preservation = {
            "rules": [
                "Do not change shape",
                "Do not change material",
                "Do not change color",
                "Preserve every detail"
            ]
        }

        self.quality = {}

        self.negative_prompt = {}



context = BrainContext()


composer = MasterPromptComposer()


prompt = composer.compose(context)


print("="*70)
print("MASTER PROMPT")
print("="*70)

print(prompt)