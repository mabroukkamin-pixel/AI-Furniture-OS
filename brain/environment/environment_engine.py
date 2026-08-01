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
        decision
    ):


        material = decision.get(
            "material",
            "unknown"
        )

        style = decision.get(
            "primary_style",
            "modern"
        )


        architecture_data = self.architecture.analyze(
            material
        )

        colors_data = self.colors.analyze(
            material
        )

        accessories_data = self.accessories.analyze(
            material
        )


        return {

            "primary": style,

            "selected_style": style,

            "atmosphere": [
                "warm natural luxury",
                "modern gulf lifestyle",
                "five star resort feeling"
            ],

            "options": [
                "luxury_villa",
                "resort",
                "japandi"
            ],

            "architecture": architecture_data,

            "colors": colors_data,

            "accessories": accessories_data
        }