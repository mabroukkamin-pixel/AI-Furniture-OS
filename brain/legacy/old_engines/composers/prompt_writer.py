from brain.composers.master_prompt_composer import MasterPromptComposer
from brain.composers.negative_prompt_composer import NegativePromptComposer
from brain.composers.prompt_finalizer import PromptFinalizer
from brain.optimizers.prompt_optimizer import PromptOptimizer


class PromptWriter:

    def __init__(self):

        self.master = MasterPromptComposer()
        self.negative = NegativePromptComposer()
        self.finalizer = PromptFinalizer()
        self.optimizer = PromptOptimizer()

    def write(self, context):

        positive = self.master.compose(context)

        positive = self.optimizer.optimize(
            positive
        )

        negative = self.negative.compose(context)

        context.final_prompt = {

            "positive": positive,
            "negative": negative

        }

        context = self.finalizer.finalize(context)

        context.prompt = context.final_prompt

        return context