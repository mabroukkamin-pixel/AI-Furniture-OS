from brain.environment.environment_engine import EnvironmentEngine
from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain
from brain.core.brain_orchestrator import BrainOrchestrator
from brain.validators.state_validator import StateValidator


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

        self.validator = StateValidator()

        self.orchestrator = BrainOrchestrator(
            experts=self.experts,
            graph=None,
            environment=self.environment,
            experience=getattr(self, "experience", None)
        )

    def _build_graph_compatibility(self, context):

        graph_decision = context.graph_decision or {}

        recommendations = graph_decision.get("recommendations", [])

        context.graph = {
            "material": graph_decision.get("material"),
            "recommendations": recommendations,
            "recommended_styles": [item.get("style") for item in recommendations if item.get("style")],
            "scenes": graph_decision.get("scenes", []),
            "confidence": graph_decision.get("selected_score", 0) / 100,
            "source": "DecisionExpert V3 compatibility projection"
        }

        return context

    def _finalize_decision(self, context):

        selected_style = context.decision.get("selected_style")

        if selected_style:
            context.decision["primary_style"] = selected_style

        if not context.decision.get("lighting"):
            context.decision["lighting"] = context.lighting

        score = context.decision.get("score", 0)

        context.decision["confidence"] = {
            "confidence": min(score, 100),
            "reasons": [
                "DecisionExpert V3 completed",
                "knowledge graph matched",
                "environment generated"
            ]
        }

        return context

    def run(self, context):

        context = self.orchestrator.run_experts(context)
        context = self._build_graph_compatibility(context)

        context.validation = self.validator.validate(context)

        print("==============================")
        print("STATE VALIDATION")
        print(context.validation)

        print("==============================")
        print("DECISION GRAPH V3")
        print(context.graph_decision)

        context = self.environment.analyze(context)
        context = self._finalize_decision(context)

        print("==============================")
        print("BRAIN RUNNER V3 RESULT")
        print(context.decision)

        return context
