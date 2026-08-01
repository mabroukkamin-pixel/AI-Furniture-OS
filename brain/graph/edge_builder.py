class EdgeBuilder:

    def __init__(self, graph):

        self.graph = graph

    def connect(self):

        self._material_to_style()
        self._style_to_scene()
        self._scene_to_lighting()

    def _material_to_style(self):

        materials = self.graph.nodes

        for name, data in materials.items():

            if data.get("type") != "material":
                continue

            for style in data.get("recommended_style", []):

                self.graph.add_edge(
                    name,
                    style,
                    "recommended_style"
                )

    def _style_to_scene(self):

        styles = self.graph.nodes

        for name, data in styles.items():

            if data.get("type") != "style":
                continue

            for scene in data.get("recommended_scene", []):

                self.graph.add_edge(
                    name,
                    scene,
                    "recommended_scene"
                )

    def _scene_to_lighting(self):

        scenes = self.graph.nodes

        for name, data in scenes.items():

            if data.get("type") != "scene":
                continue

            for lighting in data.get("recommended_lighting", []):

                self.graph.add_edge(
                    name,
                    lighting,
                    "recommended_lighting"
                )