from brain.core.brain_state import BrainState


class BrainKernel:


    def __init__(
        self,
        brain: BrainState = None
    ):

        self.brain = brain


    def attach(
        self,
        brain
    ):

        self.brain = brain


    def run_expert(
        self,
        expert
    ):

        self.brain = expert.analyze(
            self.brain
        )

        return self.brain


    def run_pipeline(
        self,
        orchestrator,
        brain
    ):

        self.attach(brain)

        self.brain = (
            orchestrator.run_experts(
                self.brain
            )
        )

        return self.brain


    def get_state(self):

        return self.brain
