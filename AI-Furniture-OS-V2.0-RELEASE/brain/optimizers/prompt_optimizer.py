from brain.optimizers.prompt_cleaner import PromptCleaner
from brain.optimizers.prompt_ranker import PromptRanker
from brain.optimizers.prompt_compressor import PromptCompressor


class PromptOptimizer:

    def __init__(self):

        self.cleaner = PromptCleaner()
        self.ranker = PromptRanker()
        self.compressor = PromptCompressor()

    def optimize(self, prompt):

        prompt = self.cleaner.clean(prompt)

        prompt = self.ranker.rank(prompt)

        prompt = self.compressor.compress(prompt)

        return prompt