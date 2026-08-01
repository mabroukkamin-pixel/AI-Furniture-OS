from brain.experts.base_expert import BaseExpert
from brain.decision_graph.engine import DecisionGraphEngine
from brain.decision_graph.graph_reasoner import GraphReasoner
from brain.decision_graph.knowledge_graph_builder import KnowledgeGraphBuilder


class DecisionExpert(BaseExpert):

    def __init__(self):

        self.engine = DecisionGraphEngine()
        self.engine.load_rules()

        self.graph_builder = KnowledgeGraphBuilder()

    def _merge_branding_context(self, brain):

        current_branding = dict(
            brain.branding or {}
        )

        product_data = (
            brain.product_data or {}
        )

        raw_branding_container = (
            product_data.get(
                "branding",
                {}
            )
        )

        raw_branding = (
            raw_branding_container.get(
                "branding",
                raw_branding_container
            )
        )

        if not isinstance(raw_branding, dict):
            raw_branding = {}

        merged_branding = dict(
            raw_branding
        )

        merged_branding.update(
            current_branding
        )

        brain.branding = merged_branding

        return brain

    def analyze(self, brain):

        print("========================================")
        print("        DECISION EXPERT V3")
        print("========================================")

        brain = self._merge_branding_context(
            brain
        )

        memory = self.graph_builder.build()
        reasoner = GraphReasoner(memory)

        brain = self.engine.run(brain)
        engine_result = dict(brain.decision)

        brain = reasoner.run(brain)

        recommendations = brain.graph_decision.get(
            "recommendations",
            []
        )

        selected = (
            recommendations[0]
            if recommendations
            else {}
        )

        brain.decision = {
            "selected_style": selected.get("style"),
            "score": selected.get("score", 0),
            "reasons": selected.get("reasons", []),
            "rule": selected.get("rule"),
            "ranking": recommendations,
            "scenes": brain.graph_decision.get(
                "scenes",
                []
            ),
            "engine_result": engine_result,
            "source": "DecisionExpert V3"
        }

        brain.memory["decision_graph"] = {
            "stats": memory.stats(),
            "graph": memory.export(),
            "selected_style": brain.decision.get(
                "selected_style"
            ),
            "selected_score": brain.decision.get(
                "score",
                0
            )
        }

        brain.log(
            "DecisionExpertV3",
            (
                "Selected style: "
                f"{brain.decision.get('selected_style')} "
                "with score: "
                f"{brain.decision.get('score', 0)}"
            )
        )

        print("DECISION GRAPH RESULT:")
        print(brain.decision)

        print("GRAPH MEMORY STATS:")
        print(memory.stats())

        return brain
