import yaml
from pathlib import Path


class GraphLoader:

    def __init__(self, graph):

        self.graph = graph

    def load_materials(

        self,

        file_path="brain/knowledge/materials.yaml"

    ):

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as f:

            data = yaml.safe_load(f)

        for material, info in data.items():

            self.graph.add_node(

                material,

                info

            )

            self._connect(

                material,

                info
            )

    def _connect(

        self,

        source,

        info

    ):

        mapping = {

            "recommended_style":

                "style",

            "recommended_scene":

                "scene",

            "recommended_lighting":

                "lighting",

            "recommended_camera":

                "camera"

        }

        for key, relation in mapping.items():

            for target in info.get(

                key,

                []

            ):

                self.graph.add_node(

                    target,

                    {

                        "type":

                            relation

                    }

                )

                self.graph.add_edge(

                    source,

                    target,

                    relation

                )

    def load_styles(self):
        self.load_yaml(
            "brain/knowledge/styles.yaml",
            "style"
        )

    def load_scenes(self):
        self.load_yaml(
            "brain/knowledge/scenes.yaml",
            "scene"
        )

    def load_lighting(self):
        self.load_yaml(
            "brain/knowledge/lighting.yaml",
            "lighting"
        )

    def load_colors(self):
        self.load_yaml(
            "brain/knowledge/colors.yaml",
            "color"
        )

    def load_architecture(self):
        self.load_yaml(
            "brain/knowledge/architecture.yaml",
            "architecture"
        )

    def load_accessories(self):
        self.load_yaml(
            "brain/knowledge/accessories.yaml",
            "accessory"
        )

    def load_yaml(self, path, node_type):

        with open(path, "r", encoding="utf-8") as f:

            data = yaml.safe_load(f) or {}

        for name, value in data.items():

            self.graph.add_node(

                name,

                {

                    "type": node_type,

                    "data": value

                }

            )