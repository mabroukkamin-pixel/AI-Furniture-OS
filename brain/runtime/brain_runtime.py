from brain.core.brain_state import BrainState


class BrainRuntime:

    def __init__(self):

        self.state = BrainState()

        self.pipeline = []

    def add_step(self, step):

        self.pipeline.append(step)

    def run(self):

        print("=" * 50)
        print("            BRAIN RUNTIME")
        print("=" * 50)

        for step in self.pipeline:

            print(f">>> {step.__class__.__name__}")

            self.state = step.run(self.state)

        return self.state