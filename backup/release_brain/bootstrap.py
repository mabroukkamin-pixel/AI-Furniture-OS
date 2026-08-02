from brain.runtime.brain_runtime import BrainRuntime

from brain.runtime.executors.product_executor import ProductExecutor
from brain.runtime.executors.memory_executor import MemoryExecutor
from brain.runtime.executors.output_executor import OutputExecutor


def build_brain():

    runtime = BrainRuntime()

    runtime.add_step(
        ProductExecutor()
    )

    runtime.add_step(
        MemoryExecutor()
    )

    runtime.add_step(
        OutputExecutor()
    )

    return runtime


if __name__ == "__main__":

    brain = build_brain()

    result = brain.run()

    print()
    print("BRAIN FINISHED")
    print(result)
