class VisualDictionary:

    def __init__(self):

        self.environments = {

            "villa":
                "Modern Gulf luxury villa",

            "luxury_villa":
                "Five-star luxury villa interior, "
                "premium stone surfaces, elegant architecture, "
                "warm natural materials, five star home atmosphere.",

            "living_room":
                "Premium elegant living room",

            "resort":
                "Luxury resort with tropical atmosphere, "
                "calm tropical atmosphere, natural textures, "
                "premium relaxing lifestyle setting.",

            "bohemian_living_room":
                "Elegant bohemian living room, "
                "natural fabrics, artistic details, "
                "warm cozy luxury atmosphere.",

        }

        self.lighting = {

            "golden_hour":
                "Golden hour warm sunlight",

            "warm_daylight":
                "Soft warm daylight",

            "warm":
                "Warm cinematic lighting, golden tones, "
                "soft luxury shadows.",

            "soft_daylight":
                "Soft natural daylight, clean premium studio illumination.",

        }

        self.camera = {

            "45_degree":
                "45-degree hero commercial shot",

            "hero":
                "Professional commercial hero photography, "
                "product centered, premium catalog style.",

            "lifestyle":
                "Luxury lifestyle photography showing product in a real interior.",

        }

        self.composition = {

            "luxury_minimal":
                "Minimal luxury composition, clean space, "
                "product as the main visual focus.",

        }

    def translate_environment(self, key):

        if isinstance(key, list):

            translated = []

            for item in key:
                translated.append(
                    self.environments.get(
                        item,
                        item
                    )
                )

            return ", ".join(translated)

        return self.environments.get(
            key,
            key
        )

    def translate_lighting(self, key):

        if isinstance(key, list):

            translated = []

            for item in key:
                translated.append(
                    self.lighting.get(
                        item,
                        item
                    )
                )

            return ", ".join(translated)

        return self.lighting.get(
            key,
            key
        )

    def translate_camera(self, key):

        if isinstance(key, list):

            translated = []

            for item in key:
                translated.append(
                    self.camera.get(
                        item,
                        item
                    )
                )

            return ", ".join(translated)

        return self.camera.get(
            key,
            key
        )

    def translate_composition(self, key):

        return self.composition.get(key, key)