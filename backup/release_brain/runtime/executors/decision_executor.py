import yaml
from brain.runtime.executors.base_executor import BaseExecutor
from brain.decision.decision_graph import DecisionGraph


class DecisionExecutor(BaseExecutor):

    def __init__(self):

        with open(
            "brain/knowledge/decision_rules.yaml",
            encoding="utf-8"
        ) as f:

            self.rules = yaml.safe_load(f)

        with open(
            "brain/knowledge/styles.yaml",
            encoding="utf-8"
        ) as f:

            self.styles = yaml.safe_load(f)

    def execute(self, state):

        print("DECISION EXECUTOR")

        product = state.product

        material = (
            product.get(
                "material",
                ""
            )
            .lower()
        )

        market = "Kuwait"

        selected = None

        for rule in self.rules["decision_rules"]:

            conditions = rule["conditions"]

            if (
                conditions.get("material") == material
                and
                (
                    "market" not in conditions
                    or conditions["market"] == market
                )
            ):

                selected = rule
                break

        if selected:

            decision = selected["decision"]

        else:

            decision = {

                "style": "default",
                "score": 0,
                "reasons": [
                    "no matching rule"
                ]

            }

        state.decision = decision

        style_name = decision.get(
            "style",
            "default"
        )

        style_knowledge = self.styles.get(
            style_name,
            {}
        )

        graph = DecisionGraph()

        # Add Nodes
        graph.add_node("product", product.get("name"))
        graph.add_node("material", material)
        graph.add_node(
            "style",
            decision.get("style"),
            score=decision.get("score"),
            reasons=decision.get("reasons")
        )
        graph.add_node("scene", "kuwaiti_luxury_living_room")
        graph.add_node("lighting", style_knowledge.get("lighting", []))
        graph.add_node("mood", style_knowledge.get("mood", []))
        graph.add_node("colors", style_knowledge.get("colors", []))
        
        # Add new requested nodes
        graph.add_node("brand", product.get("brand"))
        graph.add_node("market", market)
        graph.add_node("customer", product.get("target"))
        graph.add_node("product_category", product.get("category"))

        # Add Edges
        graph.add_edge(
            "material",
            "style",
            reason="knowledge rule",
            confidence=decision.get("score")
        )
        graph.add_edge(
            "style",
            "scene",
            reason="style environment mapping"
        )
        graph.add_edge(
            "style",
            "lighting",
            reason="style knowledge mapping"
        )
        graph.add_edge(
            "style",
            "mood",
            reason="style emotion mapping"
        )
        graph.add_edge(
            "style",
            "colors",
            reason="style color mapping"
        )
        graph.add_edge(
            "brand",
            "style",
            reason="brand identity influence"
        )
        graph.add_edge(
            "market",
            "style",
            reason="market preference mapping"
        )
        graph.add_edge(
            "customer",
            "marketing",
            reason="customer targeting"
        )
        graph.add_edge(
            "product_category",
            "scene",
            reason="category environment mapping"
        )

        state.graph_decision = graph.export()

        return state