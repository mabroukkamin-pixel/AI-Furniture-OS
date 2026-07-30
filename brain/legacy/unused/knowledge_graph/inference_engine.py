class InferenceEngine:

    def __init__(self, graph):

        self.graph = graph

    def material_to_style(self, material):

        materials = self.graph.get(
            "materials",
            {}
        )

        info = materials.get(
            material,
            {}
        )

        styles = info.get(
            "styles",
            {}
        )

        if not styles:
            return None

        return max(
            styles,
            key=styles.get
        )

    def style_to_scene(self, style):

        styles = self.graph.get(
            "styles",
            {}
        )

        info = styles.get(
            style,
            {}
        )

        scenes = info.get(
            "scenes",
            {}
        )

        if not scenes:
            return None

        return max(
            scenes,
            key=scenes.get
        )

    def scene_to_light(self, scene):

        scenes = self.graph.get(
            "scenes",
            {}
        )

        info = scenes.get(
            scene,
            {}
        )

        lighting = info.get(
            "lighting",
            {}
        )

        if not lighting:
            return None

        return max(
            lighting,
            key=lighting.get
        )

    def infer(self, material):

        style = self.material_to_style(
            material
        )

        scene = self.style_to_scene(
            style
        )

        light = self.scene_to_light(
            scene
        )

        return {

            "material": material,

            "recommended_style": style,

            "recommended_scene": scene,

            "recommended_lighting": light
        }