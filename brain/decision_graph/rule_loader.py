import yaml

from brain.decision_graph.graph_rules import GraphRule



class RuleLoader:


    def __init__(self, path):

        self.path = path



    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            data = yaml.safe_load(f)


        rules = []


        for item in data.get(
            "decision_rules",
            []
        ):


            conditions = item.get(
                "conditions",
                {}
            )


            decision = item.get(
                "decision",
                {}
            )


            def condition(context, conditions=conditions):

                for key, value in conditions.items():

                    if context.get(key) != value:

                        return False

                return True



            def action(context, decision=decision):

                return {
                    "style": decision.get("style"),
                    "score": decision.get("score"),
                    "reasons": decision.get("reasons", [])
                }



            rules.append(
                GraphRule(
                    condition,
                    action
                )
            )


        return rules