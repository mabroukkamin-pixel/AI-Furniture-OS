from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain


class FusionEngine:

    def __init__(
        self,
        rule_result,
        graph_result,
        reference_memory,
        brand_result,
        config,
        knowledge_result=None
    ):
        self.rule = rule_result if isinstance(rule_result, dict) else {}
        self.graph = graph_result if isinstance(graph_result, dict) else {}
        self.reference = reference_memory if isinstance(reference_memory, dict) else {}
        self.brand = brand_result if isinstance(brand_result, dict) else {}
        self.config = config if isinstance(config, dict) else {}
        self.knowledge = (
            knowledge_result
            if isinstance(knowledge_result, dict)
            else {}
        )

        self.architecture = ArchitectureBrain(
            "brain/environment/architecture.yaml"
        )
        self.colors = ColorBrain(
            "brain/environment/palette.yaml"
        )
        self.accessories = AccessoryBrain(
            "brain/environment/accessories.yaml"
        )

    def fuse_style(self):
        weights = self.config.get("weights", {})
        scores = {}

        graph_style = self.graph.get("recommended_style")
        if graph_style:
            scores[graph_style] = scores.get(graph_style, 0) + weights.get("knowledge_graph", 1)

        reference_style = self.reference.get("preferences", {}).get("preferred_style", [])
        if reference_style:
            style = reference_style[0]
            scores[style] = scores.get(style, 0) + weights.get("reference_memory", 1)

        brand_style = self.brand.get("creative_style", {}).get("primary")
        if brand_style:
            scores[brand_style] = scores.get(brand_style, 0) + weights.get("brand", 1)

        rule_style = self.rule.get("primary_style") or self.rule.get("style")
        if rule_style:
            scores[rule_style] = scores.get(rule_style, 0) + weights.get("rules", 1)

        if not scores:
            return "modern"

        return max(scores, key=scores.get)

    def fuse_scene(self):
        scene_list = []

        # Reference memory
        reference_scene = (
            self.reference
            .get(
                "reference_backgrounds",
                []
            )
        )
        scene_list.extend(reference_scene)

        # Knowledge
        knowledge_scene = (
            self.knowledge
            .get(
                "recommended_scene",
                []
            )
        )
        for item in knowledge_scene:
            if item not in scene_list:
                scene_list.append(item)

        # Graph
        graph_scene = (
            self.graph
            .get(
                "recommended_scene"
            )
        )
        if graph_scene and graph_scene not in scene_list:
            scene_list.append(graph_scene)

        rule_bg = self.rule.get("background") or self.rule.get("scene")
        if rule_bg:
            if isinstance(rule_bg, list):
                for s in rule_bg:
                    if s not in scene_list:
                        scene_list.append(s)
            else:
                if rule_bg not in scene_list:
                    scene_list.append(rule_bg)

        if not scene_list:
            scene_list = ["modern_entrance"]

        return scene_list

    def generate(self):
        final_style = self.fuse_style()

        scene = self.fuse_scene()

        camera = (
            self.reference
            .get(
                "reference_camera",
                []
            )
        )
        if not camera:
            camera = (
                self.knowledge
                .get(
                    "recommended_camera",
                    []
                )
            )
        if not camera:
            camera = self.rule.get("camera") or ["45_degree"]

        if isinstance(camera, str):
            camera = [camera]

        lighting = (
            self.reference
            .get(
                "reference_lighting",
                []
            )
        )
        if not lighting:
            lighting = (
                self.knowledge
                .get(
                    "recommended_lighting",
                    []
                )
            )
        if not lighting:
            lighting = self.rule.get("lighting") or ["golden_hour"]

        if isinstance(lighting, str):
            lighting = [lighting]

        materials = []
        material = (
            self.knowledge.get("material")
            or
            self.graph.get("material")
        )
        if material:
            if isinstance(material, list):
                materials.extend(material)
            else:
                materials.append(material)

        architecture = self.architecture.analyze(
            material
        )
        colors = self.colors.analyze(
            material
        )
        accessories = self.accessories.analyze(
            material
        )

        return {
            "final_style": final_style,
            "scene": scene,
            "camera": camera,
            "lighting": lighting,
            "materials": materials,
            "architecture": architecture,
            "colors": colors,
            "accessories": accessories,
            "confidence": "calculated_later",
            "graph": self.graph
        }from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain


class FusionEngine:

    def __init__(
        self,
        rule_result,
        graph_result,
        reference_memory,
        brand_result,
        config,
        knowledge_result=None
    ):
        self.rule = rule_result if isinstance(rule_result, dict) else {}
        self.graph = graph_result if isinstance(graph_result, dict) else {}
        self.reference = reference_memory if isinstance(reference_memory, dict) else {}
        self.brand = brand_result if isinstance(brand_result, dict) else {}
        self.config = config if isinstance(config, dict) else {}
        self.knowledge = (
            knowledge_result
            if isinstance(knowledge_result, dict)
            else {}
        )

        self.architecture = ArchitectureBrain(
            "brain/environment/architecture.yaml"
        )
        self.colors = ColorBrain(
            "brain/environment/palette.yaml"
        )
        self.accessories = AccessoryBrain(
            "brain/environment/accessories.yaml"
        )

    def fuse_style(self):
        weights = self.config.get("weights", {})
        scores = {}

        graph_style = self.graph.get("recommended_style")
        if graph_style:
            scores[graph_style] = scores.get(graph_style, 0) + weights.get("knowledge_graph", 1)

        reference_style = self.reference.get("preferences", {}).get("preferred_style", [])
        if reference_style:
            style = reference_style[0]
            scores[style] = scores.get(style, 0) + weights.get("reference_memory", 1)

        brand_style = self.brand.get("creative_style", {}).get("primary")
        if brand_style:
            scores[brand_style] = scores.get(brand_style, 0) + weights.get("brand", 1)

        rule_style = self.rule.get("primary_style") or self.rule.get("style")
        if rule_style:
            scores[rule_style] = scores.get(rule_style, 0) + weights.get("rules", 1)

        if not scores:
            return "modern"

        return max(scores, key=scores.get)

    def fuse_scene(self):
        scene_list = []

        # Reference memory
        reference_scene = (
            self.reference
            .get(
                "reference_backgrounds",
                []
            )
        )
        scene_list.extend(reference_scene)

        # Knowledge
        knowledge_scene = (
            self.knowledge
            .get(
                "recommended_scene",
                []
            )
        )
        for item in knowledge_scene:
            if item not in scene_list:
                scene_list.append(item)

        # Graph
        graph_scene = (
            self.graph
            .get(
                "recommended_scene"
            )
        )
        if graph_scene and graph_scene not in scene_list:
            scene_list.append(graph_scene)

        rule_bg = self.rule.get("background") or self.rule.get("scene")
        if rule_bg:
            if isinstance(rule_bg, list):
                for s in rule_bg:
                    if s not in scene_list:
                        scene_list.append(s)
            else:
                if rule_bg not in scene_list:
                    scene_list.append(rule_bg)

        if not scene_list:
            scene_list = ["modern_entrance"]

        return scene_list

    def generate(self):
        final_style = self.fuse_style()

        scene = self.fuse_scene()

        camera = (
            self.reference
            .get(
                "reference_camera",
                []
            )
        )
        if not camera:
            camera = (
                self.knowledge
                .get(
                    "recommended_camera",
                    []
                )
            )
        if not camera:
            camera = self.rule.get("camera") or ["45_degree"]

        if isinstance(camera, str):
            camera = [camera]

        lighting = (
            self.reference
            .get(
                "reference_lighting",
                []
            )
        )
        if not lighting:
            lighting = (
                self.knowledge
                .get(
                    "recommended_lighting",
                    []
                )
            )
        if not lighting:
            lighting = self.rule.get("lighting") or ["golden_hour"]

        if isinstance(lighting, str):
            lighting = [lighting]

        materials = []
        material = (
            self.knowledge.get("material")
            or
            self.graph.get("material")
        )
        if material:
            if isinstance(material, list):
                materials.extend(material)
            else:
                materials.append(material)

        architecture = self.architecture.analyze(
            material
        )
        colors = self.colors.analyze(
            material
        )
        accessories = self.accessories.analyze(
            material
        )

        return {
            "final_style": final_style,
            "scene": scene,
            "camera": camera,
            "lighting": lighting,
            "materials": materials,
            "architecture": architecture,
            "colors": colors,
            "accessories": accessories,
            "confidence": "calculated_later",
            "graph": self.graph
        }