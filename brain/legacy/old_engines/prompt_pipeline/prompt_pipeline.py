class PromptPipeline:

    def __init__(self):

        self.validator = PromptValidator()
        self.optimizer = PromptOptimizer()
        self.scorer = PromptScorer()

    def run(self, prompt):

        missing = self.validator.validate(prompt)

        prompt = self.optimizer.optimize(prompt)

        score = self.scorer.score(prompt)

        return {
            "prompt": prompt,
            "missing": missing,
            "score": score
        }