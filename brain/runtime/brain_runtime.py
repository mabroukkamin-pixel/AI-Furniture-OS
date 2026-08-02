from brain.core.brain_state import BrainState

from brain.runtime.executors.load_executor import LoadExecutor
from brain.runtime.executors.product_executor import ProductExecutor
from brain.runtime.executors.design_dna_executor import DesignDNAExecutor
from brain.runtime.executors.action_executor import ActionExecutor
from brain.runtime.executors.creative_direction_executor import CreativeDirectionExecutor
from brain.runtime.executors.memory_executor import MemoryExecutor
from brain.runtime.executors.decision_executor import DecisionExecutor
from brain.runtime.executors.graph_reasoner_executor import GraphReasonerExecutor
from brain.runtime.executors.context_fusion_executor import ContextFusionExecutor
from brain.runtime.executors.preservation_executor import PreservationExecutor
from brain.runtime.executors.prompt_executor import PromptExecutor
from brain.runtime.executors.report_executor import ReportExecutor
from brain.runtime.executors.output_executor import OutputExecutor

from runtime.loader.product_loader import ProductLoader
from brain.fusion.memory_fusion import MemoryFusion
from brain.memory.episodic_memory import EpisodicMemory
from brain.prompt.prompt_writer import PromptWriter
from runtime.output_manager import OutputManager


class BrainRuntime:

    def __init__(self, product_id="Partition001"):

        self.state = BrainState()
        self.state.product_id = product_id

        loader = ProductLoader(
            f"products/{product_id}"
        )

        fusion = MemoryFusion()
        memory = EpisodicMemory()
        writer = PromptWriter()
        output_manager = OutputManager()

        self.executors = [

            LoadExecutor(
                loader
            ),

            ProductExecutor(),

            MemoryExecutor(fusion, memory),

            DecisionExecutor(),

            GraphReasonerExecutor(),

            ContextFusionExecutor(),

            DesignDNAExecutor(),

            ActionExecutor(),

            CreativeDirectionExecutor(),

            PreservationExecutor(),

            PromptExecutor(writer),

            ReportExecutor(),

            OutputExecutor(output_manager),

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