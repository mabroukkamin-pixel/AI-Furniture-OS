from pathlib import Path

import yaml

from brain.decision_graph.graph_edges import GraphEdge
from brain.decision_graph.graph_memory import GraphMemory
from brain.decision_graph.graph_nodes import GraphNode


class KnowledgeGraphBuilder:

    def __init__(
        self,
        knowledge_directory="brain/knowledge"
    ):

        self.knowledge_directory = Path(
            knowledge_directory
        )

        self.memory = GraphMemory()

    def _load_yaml(self, filename):

        path = (
            self.knowledge_directory
            / filename
        )

        if not path.exists():
            return {}

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file) or {}

    def _add_node(
        self,
        node_id,
        node_type,
        attributes=None
    ):

        return self.memory.add_node(
            GraphNode(
                node_id=node_id,
                node_type=node_type,
                attributes=attributes or {}
            )
        )

    def _add_edge(
        self,
        source,
        target,
        relation,
        weight=1.0
    ):

        return self.memory.add_edge(
            GraphEdge(
                source=source,
                target=target,
                relation=relation,
                weight=weight
            )
        )

    def _build_materials(self):

        data = self._load_yaml(
            "materials.yaml"
        )

        materials = data.get(
            "materials",
            {}
        )

        for material_name, profile in materials.items():

            material_id = (
                f"material:{material_name}"
            )

            self._add_node(
                material_id,
                "material",
                {
                    "name": material_name,
                    "profile": profile
                }
            )

            for style_name in profile.get(
                "styles",
                []
            ):

                style_id = f"style:{style_name}"

                self._add_node(
                    style_id,
                    "style",
                    {
                        "name": style_name
                    }
                )

                self._add_edge(
                    material_id,
                    style_id,
                    "supports_style"
                )

            for scene_name in profile.get(
                "scenes",
                []
            ):

                scene_id = f"scene:{scene_name}"

                self._add_node(
                    scene_id,
                    "scene",
                    {
                        "name": scene_name
                    }
                )

                self._add_edge(
                    material_id,
                    scene_id,
                    "supports_scene"
                )

    def _build_styles(self):

        styles = self._load_yaml(
            "styles.yaml"
        )

        for style_name, profile in styles.items():

            profile = profile or {}
            style_id = f"style:{style_name}"

            self._add_node(
                style_id,
                "style",
                {
                    "name": style_name,
                    "profile": profile
                }
            )

            for material_name in profile.get(
                "materials",
                []
            ):

                material_id = (
                    f"material:{material_name}"
                )

                self._add_node(
                    material_id,
                    "material",
                    {
                        "name": material_name
                    }
                )

                self._add_edge(
                    material_id,
                    style_id,
                    "compatible_with_style"
                )

    def _build_scenes(self):

        scenes = self._load_yaml(
            "scenes.yaml"
        )

        for scene_name, profile in scenes.items():

            profile = profile or {}
            scene_id = f"scene:{scene_name}"

            self._add_node(
                scene_id,
                "scene",
                {
                    "name": scene_name,
                    "profile": profile
                }
            )

            for style_name in profile.get(
                "suitable_styles",
                []
            ):

                style_id = f"style:{style_name}"

                self._add_node(
                    style_id,
                    "style",
                    {
                        "name": style_name
                    }
                )

                self._add_edge(
                    style_id,
                    scene_id,
                    "suitable_for_scene"
                )

    def _build_decision_rules(self):

        data = self._load_yaml(
            "decision_rules.yaml"
        )

        rules = data.get(
            "decision_rules",
            []
        )

        for index, rule in enumerate(rules):

            rule_name = rule.get(
                "name",
                f"rule_{index}"
            )

            conditions = rule.get(
                "conditions",
                {}
            )

            decision = rule.get(
                "decision",
                {}
            )

            rule_id = f"rule:{rule_name}"

            self._add_node(
                rule_id,
                "decision_rule",
                {
                    "name": rule_name,
                    "conditions": conditions,
                    "decision": decision
                }
            )

            material_name = conditions.get(
                "material"
            )

            if material_name:

                material_id = (
                    f"material:{material_name}"
                )

                self._add_node(
                    material_id,
                    "material",
                    {
                        "name": material_name
                    }
                )

                self._add_edge(
                    material_id,
                    rule_id,
                    "activates_rule"
                )

            style_name = decision.get(
                "style"
            )

            if style_name:

                style_id = f"style:{style_name}"

                self._add_node(
                    style_id,
                    "style",
                    {
                        "name": style_name
                    }
                )

                self._add_edge(
                    rule_id,
                    style_id,
                    "recommends_style",
                    weight=decision.get(
                        "score",
                        0
                    )
                )

    def build(self):

        self.memory = GraphMemory()

        self._build_materials()
        self._build_styles()
        self._build_scenes()
        self._build_decision_rules()

        return self.memory