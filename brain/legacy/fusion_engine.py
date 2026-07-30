from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain


class BrainFusionEngine:

    def __init__(self, config=None):
        self.config = config or {}
        
        self.external_data = {}

        self.architecture_brain = ArchitectureBrain(
            "brain/knowledge/architecture.yaml"
        )

        self.color_brain = ColorBrain(
            "brain/knowledge/colors.yaml"
        )

        self.accessory_brain = AccessoryBrain(
            "brain/knowledge/accessories.yaml"
        )

    def run(self, brain):
        environment = getattr(
            brain,
            "environment",
            {}
        )

        material = (
            brain.product
            .get("material", {})
        )

        if isinstance(material, dict):
            material = material.get(
                "primary"
            )

        architecture = (
            self.architecture_brain.analyze(
                material
            )
        )

        colors = (
            self.color_brain.analyze(
                material
            )
        )

        accessories = (
            self.accessory_brain.analyze(
                material
            )
        )

        return {
            "architecture": architecture,
            "colors": colors,
            "accessories": accessories,
        }