from brain.runtime.brain_runtime import BrainRuntime


class DummyExecutor:

    def execute(self, state):

        state.context["runtime_test"] = True

        return state


def test_brain_runtime():

    brain = BrainRuntime()

    brain.add_step(
        DummyExecutor()
    )

    result = brain.run()

    assert result.context["runtime_test"] is True


if __name__ == "__main__":

    test_brain_runtime()

    print("BRAIN RUNTIME TEST PASSED")