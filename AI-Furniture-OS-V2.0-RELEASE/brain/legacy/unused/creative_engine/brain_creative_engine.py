from brain.director.creative_director import CreativeDirector
from brain.prompt_engine.creative_context_builder import CreativeContextBuilder


class BrainCreativeEngine:

    def __init__(self):
        pass

    def analyze_emotion(self, style):
        emotions = {

            "natural":
            {
                "emotion":
                    "natural comfort",

                "feeling":
                    "warm handmade premium home",

                "buyer_trigger":
                    "connection with nature"
            },

            "gulf_luxury":
            {
                "emotion":
                    "luxury gulf lifestyle",

                "feeling":
                    "elegant warm residence",

                "buyer_trigger":
                    "prestige and home beauty"
            },

            "modern":
            {
                "emotion":
                    "modern elegance",

                "feeling":
                    "clean premium lifestyle",

                "buyer_trigger":
                    "trust and quality"
            }

        }

        return emotions.get(
            style,
            {
                "emotion":
                    "premium furniture",

                "feeling":
                    "high quality",

                "buyer_trigger":
                    "trust"
            }
        )

    def extract_knowledge(
        self,
        brain,
        key
    ):
        knowledge = brain.knowledge

        return knowledge.get(
            key,
            {}
        )

    def run(self, brain):

        fusion = brain.fusion

        style = fusion.get(
            "final_style",
            "modern"
        )

        material = fusion.get(
            "materials",
            []
        )

        scene = fusion.get(
            "scene",
            []
        )

        camera = fusion.get(
            "camera",
            []
        )

        lighting = fusion.get(
            "lighting",
            []
        )

        environment = getattr(
            brain,
            "environment",
            {}
        )
        architecture = environment.get(
            "architecture",
            {}
        )
        colors = environment.get(
            "colors",
            {}
        )
        accessories = environment.get(
            "accessories",
            {}
        )

        brain.creative = {

            "style":

                style,

            "material":

                material,

            "emotion":

                self.analyze_emotion(
                    style
                ),

            "scene":

                scene,

            "camera":

                camera,

            "lighting":

                lighting,

            "architecture":

                architecture,

            "colors":

                colors,

            "accessories":

                accessories,

            "negative":

                self.extract_knowledge(
                    brain,
                    "negative"
                ),

            "composition":

            {
                "product_ratio":
                    "75%",

                "focus":
                    "product centered",

                "priority":
                    "product preservation"
            },

            "direction":

                "Luxury furniture advertising art direction"

        }

        builder = CreativeContextBuilder()
        brain.context = builder.build(brain)

        director = CreativeDirector()
        brain.direction = director.direct(brain)

        brain.log(

            "Creative",

            f"Creative direction generated: {style}"

        )

        return brain