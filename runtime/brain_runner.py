from brain.environment.environment_engine import EnvironmentEngine
from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain
from brain.graph.graph_manager import GraphManager
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

        self.graph = GraphManager().build()
        self.validator = StateValidator()

        self.orchestrator = BrainOrchestrator(
            experts=self.experts,
            graph=self.graph,
            environment=self.environment,
            experience=getattr(self, "experience", None)
        )

    def run(self, context):

        context = self.orchestrator.run_experts(context)

        # ===============================
        # STATE VALIDATION
        # ===============================

        context.validation = (
            self.validator.validate(context)
        )

        print("==============================")
        print("STATE VALIDATION")
        print(context.validation)

        # ===============================
        # KNOWLEDGE GRAPH & REASONER & DECISION GRAPH
        # ===============================

        material = context.product.get(
            "material",
            {}
        ).get(
            "primary"
        )

        # GRAPH REASONING V2
        context = self.graph.reasoner.analyze(
            context
        )

        styles = context.graph.get(
            "styles",
            []
        )

        context.graph = {

            "material": material,

            "recommended_styles": styles,

            "knowledge_source": "KnowledgeGraph",

            "reasoner": "GraphReasoner"

        }

        lighting = self.graph.decision.evaluate(

            {
                "material": material
            }

        )

        if lighting:

            context.decision[
                "lighting"
            ] = lighting[0]

        # ===============================
        # ENVIRONMENT ENGINE
        # ===============================

        context.environment = self.environment.analyze(
            context
        )

        # ==========================
        # COPY ENVIRONMENT TO DECISION
        # ==========================

        recommended = context.graph.get(
            "recommended_styles",
            []
        )

        if recommended:

            context.decision[
                "primary_style"
            ] = recommended[0]

        else:

            context.decision[
                "primary_style"
            ] = context.product.get(
                "style",
                ["modern"]
            )[0]

        # ===============================
        # GRAPH MEMORY (بعد تحديد primary_style)
        # ===============================

        self.graph.memory.store(

            {

                "product":

                    context.product.get(
                        "name"
                    ),

                "material":

                    material,

                "style":

                    context.decision[
                        "primary_style"
                    ]

            }

        )

        context.decision["scene"] = (
            context.environment.get("options", [])
        )
        context.decision["camera"] = (
            context.camera
        )

        # Lighting is now handled by DecisionGraph above, but if not set, fallback can remain
        if "lighting" not in context.decision or not context.decision["lighting"]:
            context.decision["lighting"] = context.lighting

        context.decision["materials"] = [
            context.product.get("material", {}).get("primary")
        ]

        # ===============================
        # DYNAMIC CONFIDENCE CALCULATION
        # ===============================

        confidence = 70

        if styles:
            confidence += 10

        if lighting:
            confidence += 10

        if context.environment:
            confidence += 10

        context.decision["confidence"] = {
            "confidence": confidence,
            "reasons": [
                "knowledge graph matched",
                "decision graph matched",
                "environment generated"
            ]
        }

        context.decision["graph"] = context.graph

        return context