class CameraEngine:


    def select(self, category):


        if category == "room_divider":

            return [
                "45_degree",
                "eye_level",
                "lifestyle_shot"
            ]


        return [
            "hero_angle"
        ]