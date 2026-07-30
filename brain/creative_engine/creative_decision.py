class CreativeDecision:


    def __init__(
        self,
        decision,
        product,
        brand,
        reference_memory=None
    ):

        self.decision = decision
        self.product = product
        self.brand = brand
        self.reference_memory = reference_memory or {}



    def get_reference_preferences(self):

        return self.reference_memory.get(
            "preferences",
            {}
        )



    def preference(self, key, default=None):

        preferences = self.get_reference_preferences()

        value = preferences.get(key)

        if value:

            return value

        return default



    def analyze_emotion(self):

        style = (
            self.preference(
                "preferred_style",
                []
            ) or [
                self.decision.get(
                    "creative_style",
                    ""
                )
            ]
        )[0]


        if style == "gulf_luxury":

            return {
                "emotion":
                    "elegant_gulf_home",

                "feeling":
                    "warm luxury lifestyle",

                "buyer_trigger":
                    "prestige and home beauty"
            }



        if style == "natural":

            return {
                "emotion":
                    "natural comfort",

                "feeling":
                    "warm handmade home",

                "buyer_trigger":
                    "connection with nature"
            }



        return {
            "emotion":
                "premium furniture",

            "feeling":
                "high quality",

            "buyer_trigger":
                "trust"
        }



    def choose_scene(self):

        preferred = self.preference(
            "preferred_scene",
            []
        )

        if preferred:

            return {
                "location": preferred[0]
            }

        scenes = self.decision.get(
            "scene",
            []
        )


        if "luxury_villa" in scenes:

            return {
                "location":
                    "modern gulf villa",

                "architecture":
                    "beige stone interior",

                "floor":
                    "warm oak wood"
            }


        return {
            "location":
                scenes[0] if scenes else "studio"
        }



    def choose_camera(self):

        preferred = self.preference(
            "preferred_camera",
            []
        )

        if preferred:

            return preferred

        return self.decision.get(
            "camera",
            []
        )



    def choose_lighting(self):

        preferred = self.preference(
            "preferred_light",
            []
        )

        if preferred:

            return preferred

        return self.decision.get(
            "lighting",
            []
        )



    def choose_style(self):

        preferred = self.preference(
            "preferred_style",
            []
        )

        if preferred:

            return preferred[0]

        return self.decision.get(
            "creative_style"
        )



    def generate(self):

        return {

            "emotion":
                self.analyze_emotion(),

            "scene":
                self.choose_scene(),

            "camera":
                self.choose_camera(),

            "lighting":
                self.choose_lighting(),

            "style":
                self.choose_style()
        }