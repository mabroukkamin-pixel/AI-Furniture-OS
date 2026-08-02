import yaml
from brain.runtime.executors.base_executor import BaseExecutor


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



        state.graph_decision = {

            "nodes": [

                {
                    "node": "product",
                    "value": product.get("name")
                },

                {
                    "node": "material",
                    "value": material
                },

                {
                    "node": "style",
                    "value": decision.get("style"),
                    "score": decision.get("score"),
                    "reasons": decision.get("reasons")
                },

                {
                    "node": "scene",
                    "value": "kuwaiti_luxury_living_room"
                },

                {
                    "node": "lighting",
                    "value": style_knowledge.get(
                        "lighting",
                        []
                    )
                },

                {
                    "node": "mood",
                    "value": style_knowledge.get(
                        "mood",
                        []
                    )
                },

                {
                    "node": "colors",
                    "value": style_knowledge.get(
                        "colors",
                        []
                    )
                }

            ],


            "edges": [

                {
                    "from": "material",
                    "to": "style",
                    "reason": "knowledge rule",
                    "confidence": decision.get("score")
                },

                {
                    "from": "style",
                    "to": "scene",
                    "reason": "style environment mapping"
                },

                {
                    "from": "style",
                    "to": "lighting",
                    "reason": "style knowledge mapping"
                },

                {
                    "from": "style",
                    "to": "mood",
                    "reason": "style emotion mapping"
                },

                {
                    "from": "style",
                    "to": "colors",
                    "reason": "style color mapping"
                }

            ]

        }


        return state