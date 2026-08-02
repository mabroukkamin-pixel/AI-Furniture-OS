from brain.optimization.sentence_optimizer import SentenceOptimizer
from brain.optimization.quality_booster import QualityBooster
from brain.optimization.negative_prompt_generator import NegativePromptGenerator
from brain.optimization.prompt_formatter import PromptFormatter


class PromptOptimizer:

    def __init__(self):
        self.sentence = SentenceOptimizer()
        self.quality = QualityBooster()
        self.negative = NegativePromptGenerator()
        self.formatter = PromptFormatter()

    def optimize(self, prompt: str) -> str:

        if not prompt:
            return ""

        prompt = self.sentence.optimize(prompt)

        prompt = self.quality.boost(prompt)

        negative = self.negative.generate()

        if negative:
            prompt += "\n\nNEGATIVE PROMPT:\n"
            prompt += negative

        prompt = self.formatter.format(prompt)

        return prompt