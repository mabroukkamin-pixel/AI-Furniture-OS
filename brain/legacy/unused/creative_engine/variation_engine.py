class VariationEngine:


    def generate(self, decision):


        style = decision.get(
            "primary_style"
        )


        scene = decision.get(
            "scene",
            []
        )


        lighting = decision.get(
            "lighting",
            []
        )


        return [

        {
        "name":"luxury_villa",
        "style":style,
        "scene":
            scene[0]
            if scene else None,
        "lighting":
            lighting[0]
            if lighting else None
        },


        {
        "name":"natural_home",
        "style":"japandi",
        "scene":"warm_home",
        "lighting":"soft_daylight"
        },


        {
        "name":"premium_showroom",
        "style":"premium",
        "scene":"showroom",
        "lighting":"dramatic_light"
        }

        ]