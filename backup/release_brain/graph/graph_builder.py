import yaml


class GraphBuilder:

    def __init__(self, graph):
        self.graph = graph

    def load_yaml(self, file):

        with open(
            file,
            encoding="utf-8"
        ) as f:

            return yaml.safe_load(f)

    def build_material_graph(self, file):

        data = self.load_yaml(file)

        materials = data.get(
            "materials",
            {}
        )

        for material, info in materials.items():

            self.graph.add_node(
                material,
                {
                    "type": "material"
                }
            )

            # 1. Recommended Styles
            for style in info.get(
                "recommended_style",
                []
            ):

                self.graph.add_node(
                    style,
                    {
                        "type": "style"
                    }
                )

                self.graph.add_edge(
                    material,
                    style,
                    "supports"
                )

            # 2. Recommended Scenes
            for scene in info.get(
                "recommended_scene",
                []
            ):

                self.graph.add_node(
                    scene,
                    {
                        "type": "scene"
                    }
                )

                self.graph.add_edge(
                    material,
                    scene,
                    "supports"
                )

            # 3. Recommended Lighting
            for lighting in info.get(
                "recommended_lighting",
                []
            ):

                self.graph.add_node(
                    lighting,
                    {
                        "type": "lighting"
                    }
                )

                self.graph.add_edge(
                    material,
                    lighting,
                    "supports"
                )

            # 4. Recommended Camera
            for camera in info.get(
                "recommended_camera",
                []
            ):

                self.graph.add_node(
                    camera,
                    {
                        "type": "camera"
                    }
                )

                self.graph.add_edge(
                    material,
                    camera,
                    "supports"
                )

            # 5. Architecture
            for arch in info.get(
                "architecture",
                []
            ):

                self.graph.add_node(
                    arch,
                    {
                        "type": "architecture"
                    }
                )

                self.graph.add_edge(
                    material,
                    arch,
                    "supports"
                )