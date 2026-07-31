from brain.decision_engine.material_decision import MaterialDecision


class DecisionEngine:

    def __init__(self):

        self.modules = [
            MaterialDecision()
        ]

    def decide(self, context):

        for module in self.modules:
            context = module.run(context)

        return context