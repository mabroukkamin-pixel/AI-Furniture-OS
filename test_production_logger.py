from brain.core.brain_state import BrainState
from runtime.reporting.production_logger import ProductionLogger

state = BrainState()

state.run_id = "RUN001"
state.product_id = "Partition001"
state.status = "success"
state.current_stage = "completed"
state.engine_name = "nano_banana"
state.output_folder = "outputs/Partition001"

logger = ProductionLogger()

print(
    logger.log(state)
)