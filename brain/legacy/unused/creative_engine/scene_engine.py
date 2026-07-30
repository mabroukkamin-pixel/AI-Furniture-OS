class SceneEngine:

    def build(self, decision):

        style = (
            decision
            .get("creative_style", {})
        )

        primary = style.get(
            "primary",
            ""
        )

        if primary == "gulf_luxury":

            return [
                "luxury_villa",
                "beige_stone",
                "warm_wood",
                "soft_sunlight"
            ]

        return decision.get(
            "scene",
            []
        )