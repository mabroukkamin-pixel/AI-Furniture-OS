from brain.environment.environment_engine import EnvironmentEngine
from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain


class BrainRunner:

    def __init__(self, product_name):

        from brain.expert_manager import ExpertManager

        manager = ExpertManager(product_name)

        self.experts = manager.build()

        self.environment = EnvironmentEngine(
            ArchitectureBrain(
                "brain/knowledge/architecture.yaml"
            ),
            ColorBrain(
                "brain/knowledge/colors.yaml"
            ),
            AccessoryBrain(
                "brain/knowledge/accessories.yaml"
            )
        )

    def run(self, context):

        for expert in self.experts:

            context = expert.analyze(
                context
            )

        # ===============================
        # ENVIRONMENT ENGINE
        # ===============================

        material = (
            context.product
            .get("material", {})
            .get("primary")
        )

        context.environment = (
            self.environment.analyze(
                material
            )
        )

        # ==========================
        # COPY ENVIRONMENT TO DECISION
        # ==========================

        context.decision["primary_style"] = (
            context.product.get("style", ["modern"])[0]
        )
        context.decision["scene"] = (
            context.environment.get("options", [])
        )
        context.decision["camera"] = (
            context.camera
        )
        context.decision["lighting"] = (
            context.lighting
        )
        context.decision["materials"] = [
            context.product.get("material", {}).get("primary")
        ]

        context.decision["confidence"] = {
            "confidence": 90,
            "reasons": [
                "material matched",
                "brand style matched",
                "environment selected from knowledge graph"
            ]
        }

        context.decision["graph"] = context.graph

        return context