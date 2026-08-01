import json
from pathlib import Path

from brain.core.brain_state import BrainState
from brain.decision_graph.graph_edges import GraphEdge
from brain.decision_graph.graph_memory import GraphMemory
from brain.decision_graph.graph_nodes import GraphNode
from brain.decision_graph.graph_reasoner import GraphReasoner
from brain.decision_graph.knowledge_graph_builder import KnowledgeGraphBuilder
from brain.experts.decision_expert import DecisionExpert
from runtime.output_manager import OutputManager


def make_rattan_state():
    state = BrainState()
    state.product = {
        "material": {"primary": "rattan"},
        "handmade": True,
        "premium": True,
    }
    state.product_data = {
        "branding": {
            "branding": {
                "market": "Kuwait",
                "company": "Chinese Market",
            }
        }
    }
    state.branding = {
        "company": "Chinese Market",
        "style": "premium_luxury",
    }
    return state


def test_knowledge_graph_builder_connects_all_sources():
    memory = KnowledgeGraphBuilder().build()

    assert memory.stats() == {
        "node_count": 22,
        "edge_count": 24,
        "node_types": {
            "material": 3,
            "style": 10,
            "scene": 6,
            "decision_rule": 3,
        },
    }

    assert memory.get_node("material:rattan") is not None
    assert memory.get_node("style:natural") is not None
    assert memory.get_node("scene:luxury_villa") is not None
    assert memory.get_node("rule:rattan_gulf_villa") is not None


def test_graph_memory_prevents_duplicate_nodes_and_edges():
    memory = GraphMemory()
    node = GraphNode("material:rattan", "material", {"name": "rattan"})
    edge = GraphEdge(
        "material:rattan",
        "style:natural",
        "supports_style",
    )

    memory.add_node(node)
    memory.add_node(node)
    memory.add_edge(edge)
    memory.add_edge(edge)

    assert len(memory.nodes) == 1
    assert len(memory.edges) == 1


def test_graph_measoner_ranks_matching_rules_first():
    state = make_rattan_state()
    state.branding["market"] = "Kuwait"
    memory = KnowledgeGraphBuilder().build()

    result = GraphReasoner(memory).run(state)

    assert result.graph_decision["selected_style"] == "gulf_villa"
    assert result.graph_decision["selected_score"] == 95
    assert result.graph_decision["recommendations"][0]["rule"] == (
        "rattan_gulf_villa"
    )
    assert result.graph_decision["scenes"] == [
        "luxury_villa",
        "resort",
        "living_room",
    ]


def test_decision_expert_v3_restores_branding_and_selects_style():
    state = DecisionExpert().analyze(make_rattan_state())

    assert state.branding["market"] == "Kuwait"
    assert state.decision["selected_style"] == "gulf_villa"
    assert state.decision["score"] == 95
    assert state.decision["source"] == "DecisionExpert V3"
    assert state.memory["decision_graph"]["stats"]["node_count"] == 22
    assert state.trace[-1]["engine"] == "DecisionExpertV3"


def test_output_manager_exports_graph_artifacts(tmp_path, monkeypatch):
    state = make_rattan_state()
    state = DecisionExpert().analyze(state)

    monkeypatch.chdir(tmp_path)

    OutputManager().export("GraphExportTest", state)

    brain_folder = tmp_path / "outputs" / "GraphExportTest" / "brain"
    graph_decision = json.loads(
        (brain_folder / "graph_decision.json").read_text(encoding="utf-8")
    )
    graph_memory = json.loads(
        (brain_folder / "graph_memory.json").read_text(encoding="utf-8")
    )

    assert graph_decision["selected_style"] == "gulf_villa"
    assert graph_decision["selected_score"] == 95
    assert graph_memory["stats"]["node_count"] == 22
    assert graph_memory["stats"]["edge_count"] == 24


def test_active_runtime_has_no_legacy_decision_execution():
    pipeline_source = Path("runtime/pipeline.py").read_text(encoding="utf-8")
    runner_source = Path("runtime/brain_runner.py").read_text(encoding="utf-8")

    assert "DecisionEngineV2" not in pipeline_source
    assert "GraphManager" not in pipeline_source
    assert "GraphManager" not in runner_source
    assert "GRAPH REASONER V2" not in runner_source
