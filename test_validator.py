from brain.core.brain_state import BrainState
from runtime.reporting.validator import ProductionValidator

state = BrainState()

state.product = {"name": "Chair"}

state.design_dna = {"style": "modern"}

state.audit = {"score": 100}

state.branding = {"brand": "Chinese Market"}

state.marketing = {"audience": "Kuwait"}

state.generation = {}

validator = ProductionValidator()

print(
    validator.validate(state)
)