from brain.core.brain_state import BrainState


class BrainKernel:

    def __init__(self, brain: BrainState):

        self.brain = brain


    def run_expert(self, expert):

        self.brain = expert.analyze(
            self.brain
        )

        return self.brain


    def get_state(self):

        return self.brain