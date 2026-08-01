class DecisionGraph:

    def __init__(self):

        self.rules = []

    def add_rule(

        self,

        condition,

        result

    ):

        self.rules.append({

            "condition": condition,

            "result": result

        })

    def evaluate(

        self,

        context

    ):

        output = []

        for rule in self.rules:

            if rule["condition"](context):

                output.append(

                    rule["result"]

                )

        return output