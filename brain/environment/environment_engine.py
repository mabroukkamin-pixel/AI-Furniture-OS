class EnvironmentEngine:


    def __init__(
        self,
        architecture,
        colors,
        accessories
    ):

        self.architecture = architecture
        self.colors = colors
        self.accessories = accessories



    def analyze(
        self,
        material
    ):


        architecture_data = (
            self.architecture.analyze(
                material
            )
        )


        colors_data = (
            self.colors.analyze(
                material
            )
        )


        accessories_data = (
            self.accessories.analyze(
                material
            )
        )


        # ============================
        # SCENE DECISION
        # ============================

        scenes = [
            "luxury_villa",
            "resort",
            "japandi"
        ]


        # ============================
        # ATMOSPHERE
        # ============================

        atmosphere = [
            "warm natural luxury",
            "modern gulf lifestyle",
            "five star resort feeling"
        ]


        return {


            "primary":
                "luxury_villa",


            "atmosphere":
                atmosphere,


            "options":
                scenes,


            "architecture":
                architecture_data,


            "colors":
                colors_data,


            "accessories":
                accessories_data

        }