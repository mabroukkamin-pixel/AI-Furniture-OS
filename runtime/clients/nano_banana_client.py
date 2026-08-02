from brain.core.brain_state import BrainState

from brain.runtime.executors.load_executor import LoadExecutor
from brain.runtime.executors.product_executor import ProductExecutor
from brain.runtime.executors.memory_executor import MemoryExecutor
from brain.runtime.executors.decision_executor import DecisionExecutor
from brain.runtime.executors.prompt_executor import PromptExecutor
from brain.runtime.executors.output_executor import OutputExecutor

from brain.services.memory_service import MemoryService
from brain.services.fusion_service import FusionService
from brain.runtime.brain_runtime import BrainRuntime


class BrainRuntimeRef:

    def __init__(self):

        self.state = BrainState()

        self.memory = MemoryService()

        self.fusion = FusionService()

        self.executors = [

            LoadExecutor(),

            ProductExecutor(),

            MemoryExecutor(
                self.fusion,
                self.memory
            ),

            DecisionExecutor(),

            PromptExecutor(),

            OutputExecutor(),

        ]

    def run(self):

        print("=" * 50)
        print("            BRAIN RUNTIME")
        print("=" * 50)

        for executor in self.executors:

            print(
                f">>> {executor.__class__.__name__}"
            )

            self.state = executor.execute(
                self.state
            )

        return self.state


class NanoBananaClient:

    def __init__(self):

        self.runtime = BrainRuntime()

    def generate(self, prompt):

        print(
            "NanoBanana Client Adapter"
        )

        return {

            "status": "runtime_ready",

            "prompt": prompt

        }