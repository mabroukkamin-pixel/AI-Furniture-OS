from brain.decision_engine.decision_engine import DecisionEngine
from brain.fusion_engine.brain_fusion_engine import BrainFusionEngine
from brain.environment.environment_engine import EnvironmentEngine
from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain


class BrainRunner:

    def __init__(self, product_name):

        from brain.expert_manager import ExpertManager

        manager = ExpertManager(product_name)

        self.experts = manager.build()

        self.decision = DecisionEngine()

        self.environment = EnvironmentEngine(
            ArchitectureBrain(
                "brain/environment/environment.yaml"
            ),
            ColorBrain(
                "brain/environment/environment.yaml"
            ),
            AccessoryBrain(
                "brain/environment/environment.yaml"
            )
        )

        self.fusion = BrainFusionEngine()

    def run(self, context):

        for expert in self.experts:

            context = expert.analyze(
                context
            )

        # ===============================
        # DECISION ENGINE
        # ===============================

        context = self.decision.decide(
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

        # ===============================
        # FUSION ENGINE
        # ===============================

        context = self.fusion.run(
            context
        )

        # ==========================
        # COPY FUSION TO DECISION
        # ==========================

        context.decision["fusion"] = context.fusion

        context.decision["primary_style"] = (
            context.fusion.get(
                "final_style"
            )
        )

        context.decision["scene"] = (
            context.fusion.get(
                "scene",
                []
            )
        )

        context.decision["camera"] = (
            context.fusion.get(
                "camera",
                []
            )
        )

        context.decision["lighting"] = (
            context.fusion.get(
                "lighting",
                []
            )
        )

        context.decision["materials"] = (
            context.fusion.get(
                "materials",
                []
            )
        )

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