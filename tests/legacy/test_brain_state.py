from brain.core.brain_state import BrainState
from brain.knowledge.knowledge_loader import KnowledgeLoader
from brain.knowledge_graph.knowledge_engine import KnowledgeEngine
from brain.knowledge_graph.graph_engine import GraphEngine
from brain.knowledge_graph.graph_loader import GraphLoader
from brain.reference_engine.brain_reference_engine import BrainReferenceEngine
from brain.decision_engine.rule_engine import RuleEngine
from brain.decision_engine.scoring_engine import ScoringEngine
from brain.decision_engine.brain_decision_engine import BrainDecisionEngine
from brain.fusion_engine.brain_fusion_engine import BrainFusionEngine
from brain.creative_engine.brain_creative_engine import BrainCreativeEngine
from brain.brand_engine.brand_loader import BrandLoader
from brain.prompt_engine.creative_context_builder import CreativeContextBuilder
from brain.prompt.prompt_writer import PromptWriter
from brain.direction_engine.direction_engine import DirectionEngine
from brain.environment.architecture_loader import ArchitectureBrain
from brain.environment.color_loader import ColorBrain
from brain.environment.accessory_loader import AccessoryBrain
from brain.environment.environment_engine import EnvironmentEngine


def main():
    print("TEST START")

    brain = BrainState()

    brand_loader = BrandLoader(
        "products/Partition001/branding.yaml"
    )
    brain.brand = brand_loader.load()

    brain.product = {
        "product": {
            "product": {
                "id": "Partition001",
                "name": "بارتيشن قش",
                "material": "rattan",
                "category": "room_divider",
                "color": "beige",
                "dimensions": {
                    "width": 200,
                    "height": 180
                },
                "price": 15,
                "description":
                    "بارتيشن قش طبيعي بتصميم يدوي لإضافة دفء وأناقة للمكان"
            }
        },
        "identity": {
            "product": {
                "premium": True,
                "handmade": True
            }
        },
        "behavior": {
            "behavior": {
                "preserve": [
                    "keep exact product geometry",
                    "preserve materials",
                    "preserve colors",
                    "preserve dimensions"
                ],
                "emphasize": [],
                "avoid": []
            }
        }
    }

    # Load Knowledge
    loader = KnowledgeLoader()
    knowledge = loader.load()
    print("Knowledge Loaded")

    # Run Knowledge Engine
    engine = KnowledgeEngine(
        knowledge
    )
    brain = engine.run(
        brain
    )

    # Load Graph
    graph_loader = GraphLoader()
    graph = graph_loader.load()
    graph_engine = GraphEngine(
        graph
    )
    brain = graph_engine.run(
        brain
    )

    # Run Reference Engine
    reference_engine = BrainReferenceEngine(
        "brain/reference_memory/reference_database.yaml"
    )
    brain = reference_engine.run(
        brain
    )

    # Run Decision Engine
    rule_engine = RuleEngine(
        "brain/decision_engine/rules.yaml"
    )
    scoring_engine = ScoringEngine(
        "brain/decision_engine/weights.yaml"
    )
    decision_engine = BrainDecisionEngine(
        rule_engine,
        scoring_engine
    )
    brain = decision_engine.run(
        brain
    )

    # Run Environment Engine
    architecture = ArchitectureBrain(
        "brain/environment/environment.yaml"
    )
    colors = ColorBrain(
        "brain/environment/environment.yaml"
    )
    accessories = AccessoryBrain(
        "brain/environment/environment.yaml"
    )
    environment_engine = EnvironmentEngine(
        architecture,
        colors,
        accessories
    )
    brain.environment = environment_engine.analyze(
        brain.product["product"]["product"]["material"]
    )

    # Run Fusion Engine
    fusion_engine = BrainFusionEngine()
    brain = fusion_engine.run(
        brain
    )

    # Run Creative Engine
    creative_engine = BrainCreativeEngine()
    brain = creative_engine.run(
        brain
    )

    # Run Direction Engine
    direction_engine = DirectionEngine()
    brain = direction_engine.run(brain)

    print("================")
    print("KNOWLEDGE")
    print("================")
    print(brain.knowledge)

    print("================")
    print("GRAPH")
    print("================")
    print(brain.graph)

    print("================")
    print("REFERENCE")
    print("================")
    print(brain.reference)

    print("================")
    print("DECISION")
    print("================")
    print(brain.decision)

    print("================")
    print("FUSION")
    print("================")
    print(brain.fusion)

    print("================")
    print("ENVIRONMENT")
    print("================")
    print(brain.environment)

    print("================")
    print("CREATIVE")
    print("================")
    print(brain.creative)

    print("================")
    print("DIRECTION")
    print("================")
    print(brain.direction)

    print("================")
    print("PROMPT CONTEXT")
    print("================")
    builder = CreativeContextBuilder()
    context = builder.build(brain)
    print(context)

    print("================")
    print("FINAL PROMPT")
    print("================")
    writer = PromptWriter()
    context = writer.write(context)
    print(context.final_prompt)

    print("================")
    print("TRACE")
    print("================")
    for item in brain.trace:
        print(item)


if __name__ == "__main__":
    main()