class PromptOptimizer:

    def __init__(self):

        self.booster = QualityBooster()

    def optimize(self, prompt):

        return self.booster.boost(prompt)