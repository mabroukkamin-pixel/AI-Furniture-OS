from brain.core.brain_state import BrainState
from brain.decision.decision_engine_v2 import DecisionEngineV2


print("================================")
print("DECISION ENGINE V2 TEST")
print("================================")


state = BrainState()


state.graph = {

    "material": "rattan",

    "styles": [

        "gulf_villa",

        "luxury_resort",

        "modern_natural_home"

    ]

}



engine = DecisionEngineV2()


state = engine.analyze(
    state
)



print("==============================")

print(
    state.decision
)