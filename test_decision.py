from brain.decision_engine.decision_engine import DecisionEngine
from brain.decision_engine.rule_engine import RuleEngine
from brain.decision_engine.scoring_engine import ScoringEngine

from brain.reference_memory.memory_loader import MemoryLoader
from brain.knowledge_graph.graph_loader import GraphLoader
from brain.knowledge_graph.inference_engine import InferenceEngine


product = {
    "product":{
        "product":{
            "material":"rattan"
        }
    },
    "behavior":{
        "behavior":{
            "avoid":[
                "redesign",
                "extra_objects"
            ]
        }
    }
}


brand = {

    "branding":{
        "market":"Kuwait"
    }

}


reference = MemoryLoader(
    "brain/reference_memory/reference_database.yaml"
).load()


graph = GraphLoader(
    "brain/knowledge_graph/graph.yaml"
).load()


inference = InferenceEngine(graph)


graph_result = inference.infer(
    material="rattan"
)


decision = DecisionEngine(

    product,
    brand,

    RuleEngine(
        "brain/decision_engine/rules.yaml"
    ),

    ScoringEngine(
        "brain/decision_engine/weights.yaml"
    ),

    reference={}

)


result = decision.decide()


result["graph"] = graph_result


print(result)