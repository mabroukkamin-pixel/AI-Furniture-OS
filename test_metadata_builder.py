from runtime.reporting.metadata_builder import MetadataBuilder
from brain.core.brain_state import BrainState


state = BrainState()

state.product_id = "Partition001"

state.product = {
    "name": "Rattan Partition",
    "category": "partition",
}

state.material = "rattan"

state.decision = {
    "selected_style": "gulf_villa"
}

state.lighting = {
    "type": "warm_daylight"
}

state.branding = {
    "company": "Chinese Market"
}

state.engine_name = "nano_banana"

builder = MetadataBuilder()

metadata = builder.build(state)

print(metadata)