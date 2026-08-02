# Decision Graph V3

## Status

Decision Graph V3 is the active decision path for AI Furniture OS V2.

Validation baseline at adoption:

- Full test suite: 79 passed, 0 failed.
- Pipeline product: `Partition001`.
- Selected style: `gulf_villa`.
- Selected score: `95`.
- Pipeline result: `success`.
- Knowledge graph: 22 nodes and 24 edges.

## Active Runtime Flow

```text
runtime/run_pipeline.py
  -> runtime/pipeline.py
  -> runtime/brain_runner.py
  -> brain/core/brain_orchestrator.py
  -> registered experts
  -> brain/experts/decision_expert.py
  -> DecisionGraphEngine
  -> KnowledgeGraphBuilder
  -> GraphMemory
  -> GraphReasoner
  -> BrainState decision fields
  -> DesignDNAEngine
  -> prompt writer and auditor
  -> OutputManager
```

`DecisionExpert` is registered last so product, material, lighting, environment,
camera, composition, branding, preservation, and marketing context are available
before the final decision is made.

## Knowledge Sources

`KnowledgeGraphBuilder` loads and connects:

- `brain/knowledge/materials.yaml`
- `brain/knowledge/styles.yaml`
- `brain/knowledge/scenes.yaml`
- `brain/knowledge/decision_rules.yaml`

The builder resolves these sources into one in-memory graph on each decision run.

## Graph Model

### Node types

- `material`
- `style`
- `scene`
- `decision_rule`

### Edge relations

- `supports_style`
- `compatible_with_style`
- `supports_scene`
- `suitable_for_scene`
- `activates_rule`
- `recommends_style`

Rule-to-style edge weight stores the rule score.

## Decision Components

### DecisionGraphEngine

Loads executable rules from `decision_rules.yaml`, evaluates the current product
context, and produces matching rule decisions plus the independent scorer result.

Input context:

- material
- handmade
- premium
- market

### GraphMemory

Provides:

- duplicate-safe node storage
- duplicate-safe edge storage
- lookup by node ID
- lookup by node type
- filtered edge search
- neighbor traversal
- graph statistics
- JSON-compatible export

### GraphReasoner V3

Combines matching rule recommendations with knowledge-derived material/style
recommendations. Results are deduplicated by style and ordered by descending score.

The reasoner writes `BrainState.graph_decision` with:

- evaluated context
- material
- ranked recommendations
- selected style
- selected score
- suitable scenes
- source

### DecisionExpert V3

Coordinates the engine, graph builder, memory, and reasoner. It restores original
branding fields when earlier experts have normalized the branding object, then writes
the canonical final decision.

The expert writes:

- `BrainState.decision`
- `BrainState.graph_decision`
- `BrainState.memory["decision_graph"]`
- a `DecisionExpertV3` trace entry

## BrainState Contract

Canonical decision fields:

```text
selected_style
primary_style
score
reasons
rule
ranking
scenes
engine_result
source
lighting
confidence
```

`primary_style` is a compatibility alias of `selected_style`. New consumers should
prefer `selected_style`.

Graph compatibility data is projected into `BrainState.graph` for consumers that
have not yet migrated to `graph_decision`.

## Output Contract

`runtime/output_manager.py` exports:

```text
outputs/<product_id>/brain/product.json
outputs/<product_id>/brain/decision.json
outputs/<product_id>/brain/graph_decision.json
outputs/<product_id>/brain/graph_memory.json
outputs/<product_id>/brain/branding.json
outputs/<product_id>/brain/marketing.json
outputs/<product_id>/brain/preservation.json
```

`graph_decision.json` contains the reasoning result. `graph_memory.json` contains
graph statistics, nodes, edges, and the selected result.

Both graph artifacts are registered in `BrainState.artifacts`.

## Legacy Disconnection

The active runtime no longer executes:

- `DecisionEngineV2` from `runtime/pipeline.py`
- `GraphManager` from `runtime/pipeline.py`
- `GraphManager` from `runtime/brain_runner.py`
- the `GRAPH REASONER V2` path from `runtime/brain_runner.py`

Legacy source files may remain for migration history, but they are not part of the
active decision flow.

## Failure Isolation

Visual-memory learning is non-fatal after successful generation. A learning failure
is recorded in `BrainState.trace` with warning severity and does not convert a
successful production result into a failed pipeline result.

The canonical lifecycle field is `BrainState.status`; `generation_status` is not part
of the current BrainState contract.

## Regression Coverage

`tests/test_decision_graph_v3.py` covers:

1. Building the graph from all four knowledge sources.
2. Node and edge duplicate prevention.
3. Rule ranking and scene recommendations.
4. Branding restoration and final style selection.
5. Graph artifact export.
6. Absence of legacy decision execution in active runtime files.

Related contracts are covered by:

- `tests/test_artifact_tracking.py`
- `tests/test_decision.py`
- `tests/test_compatibility_aliases.py`
- `tests/test_run_lifecycle.py`
- `tests/test_material_expert.py`

## Adoption Result

For `Partition001`:

```json
{
  "selected_style": "gulf_villa",
  "primary_style": "gulf_villa",
  "score": 95,
  "source": "DecisionExpert V3"
}
```

The next architectural module should consume the canonical V3 fields instead of
introducing another parallel decision path.
