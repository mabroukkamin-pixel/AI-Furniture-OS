from brain.core.brain_state import BrainState
from runtime.reporting.report_generator import ReportGenerator

state = BrainState()

state.product_id = "Partition001"
state.status = "success"
state.engine_name = "nano_banana"

state.output_folder = "outputs/Partition001"

state.audit = {
    "score": 100
}

state.design_dna = {
    "style": "Modern Gulf Natural Luxury"
}

state.decision = {
    "selected_style": "gulf_villa"
}

generator = ReportGenerator()

print(
    generator.generate(state)
)