from pathlib import Path

import pytest
import yaml

from brain.decision_graph.knowledge_graph_builder import KnowledgeGraphBuilder
from brain.knowledge.knowledge_validator import (
    KnowledgeValidationError,
    KnowledgeValidator,
)


VALID_MATERIALS = {
    "materials": {
        "rattan": {
            "styles": ["natural", "japandi"],
            "scenes": ["luxury_villa", "resort"],
            "lighting": ["warm_daylight"],
            "colors": {"primary": ["beige"]},
            "accessories": {"decor": ["vase"]},
        }
    }
}

VALID_STYLES = {
    "natural": {
        "colors": ["beige"],
        "materials": ["rattan"],
        "lighting": ["warm"],
        "mood": ["peaceful"],
    }
}

VALID_SCENES = {
    "luxury_villa": {
        "architecture": ["travertine"],
        "suitable_styles": ["natural"],
        "accessories": ["vase"],
    }
}

VALID_RULES = {
    "decision_rules": [
        {
            "name": "rattan_natural",
            "conditions": {"material": "rattan"},
            "decision": {
                "style": "natural",
                "score": 90,
                "reasons": ["material match"],
            },
        }
    ]
}


def write_yaml(directory, filename, data):
    path = directory / filename
    path.write_text(
        yaml.safe_dump(data, sort_keys=False),
        encoding="utf-8",
    )


def write_valid_knowledge(directory):
    write_yaml(directory, "materials.yaml", VALID_MATERIALS)
    write_yaml(directory, "styles.yaml", VALID_STYLES)
    write_yaml(directory, "scenes.yaml", VALID_SCENES)
    write_yaml(directory, "decision_rules.yaml", VALID_RULES)


def finding_codes(findings):
    return [finding["code"] for finding in findings]


def test_current_knowledge_is_valid_with_reference_warnings():
    report = KnowledgeValidator("brain/knowledge").validate()

    assert report["valid"] is True
    assert report["errors"] == []
    assert report["stats"]["files"] == 4
    assert report["stats"]["materials"] == 2
    assert report["stats"]["decision_rules"] == 3
    assert report["stats"]["warning_count"] > 0
    assert "unknown_style_reference" in finding_codes(report["warnings"])


def test_missing_required_file_is_an_error(tmp_path):
    write_valid_knowledge(tmp_path)
    (tmp_path / "scenes.yaml").unlink()

    report = KnowledgeValidator(tmp_path).validate()

    assert report["valid"] is False
    assert finding_codes(report["errors"]) == ["missing_file"]
    assert report["errors"][0]["file"] == "scenes.yaml"


def test_invalid_root_type_is_rejected(tmp_path):
    write_valid_knowledge(tmp_path)
    write_yaml(tmp_path, "styles.yaml", ["natural"])

    report = KnowledgeValidator(tmp_path).validate()

    assert report["valid"] is False
    assert "invalid_root_type" in finding_codes(report["errors"])


def test_duplicate_rule_names_are_rejected(tmp_path):
    write_valid_knowledge(tmp_path)
    rules = {"decision_rules": [VALID_RULES["decision_rules"][0], VALID_RULES["decision_rules"][0]]}
    write_yaml(tmp_path, "decision_rules.yaml", rules)
    report = KnowledgeValidator(tmp_path).validate()
    assert report["valid"] is False
    assert "duplicate_rule_name" in finding_codes(report["errors"])


@pytest.mark.parametrize(("decision", "expected_code"), [({"score": 90}, "missing_decision_style"), ({"style": "natural", "score": "high"}, "invalid_score_type"), ({"style": "natural", "score": 101}, "score_out_of_range")])
def test_invalid_rule_decisions_are_rejected(tmp_path, decision, expected_code):
    write_valid_knowledge(tmp_path)
    rules = {"decision_rules": [{"name": "invalid_rule", "conditions": {"material": "rattan"}, "decision": decision}]}
    write_yaml(tmp_path, "decision_rules.yaml", rules)
    report = KnowledgeValidator(tmp_path).validate()
    assert report["valid"] is False
    assert expected_code in finding_codes(report["errors"])


def test_invalid_relation_field_type_is_rejected(tmp_path):
    write_valid_knowledge(tmp_path)
    materials = {"materials": {"rattan": {"styles": "natural", "scenes": ["luxury_villa"]}}}
    write_yaml(tmp_path, "materials.yaml", materials)
    report = KnowledgeValidator(tmp_path).validate()
    assert report["valid"] is False
    assert "invalid_relation_type" in finding_codes(report["errors"])
    assert report["errors"][0]["path"] == "materials.rattan.styles"


def test_unknown_references_are_deterministic_warnings(tmp_path):
    write_valid_knowledge(tmp_path)
    first_report = KnowledgeValidator(tmp_path).validate()
    second_report = KnowledgeValidator(tmp_path).validate()
    assert first_report["valid"] is True
    assert first_report["warnings"] == second_report["warnings"]
    assert finding_codes(first_report["warnings"]) == ["unknown_style_reference", "unknown_scene_reference"]


def test_builder_stores_report_and_blocks_on_errors(tmp_path):
    write_valid_knowledge(tmp_path)
    builder = KnowledgeGraphBuilder(tmp_path)
    memory = builder.build()
    assert memory.stats()["node_count"] > 0
    assert builder.validation_report["valid"] is True
    (tmp_path / "decision_rules.yaml").unlink()
    invalid_builder = KnowledgeGraphBuilder(tmp_path)
    with pytest.raises(KnowledgeValidationError) as error:
        invalid_builder.build()
    assert error.value.report["valid"] is False
    assert error.value.report["stats"]["error_count"] == 1

def test_decision_expert_exports_validation_report():
    from brain.core.brain_state import BrainState
    from brain.experts.decision_expert import DecisionExpert

    state = BrainState()
    state.product = {
        "material": {
            "primary": "rattan",
        },
        "handmade": True,
        "premium": True,
    }
    state.branding = {
        "market": "Kuwait",
    }

    result = DecisionExpert().analyze(state)

    validation = (
        result.memory["decision_graph"]["validation"]
    )

    assert validation["valid"] is True
    assert validation["errors"] == []
    assert validation["stats"]["files"] == 4
    assert validation["stats"]["error_count"] == 0
    assert result.decision["selected_style"] == "gulf_villa"
    assert result.decision["score"] == 95
