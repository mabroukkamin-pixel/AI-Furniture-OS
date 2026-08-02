# Manifest Contract

## Purpose

This document defines the design contract for the runtime manifest artifact to be written at:

- outputs/<ProductID>/manifest.json

The manifest is a design-only contract for the current pipeline and is intended to summarize the state of a single production run in a stable, machine-readable form.

This document does not create or modify any runtime code, and it does not create the manifest file itself now.

## Scope

The manifest contract is based on the current frozen architecture documented in:

- [docs/CURRENT_ARCHITECTURE_FREEZE.md](docs/CURRENT_ARCHITECTURE_FREEZE.md)
- [docs/PRODUCTION_CONTEXT_CONTRACT.md](docs/PRODUCTION_CONTEXT_CONTRACT.md)

It is meant to reflect the currently wired runtime path and the state fields already defined in ProductionContext.

## Manifest Intent

The manifest should provide a single, durable summary of a production run for a given product. It should answer:

- which product was processed
- which inputs were available
- which prompts and decisions were produced
- whether production succeeded or failed
- where the output artifacts were written

## Manifest Location

The manifest artifact is expected at:

- outputs/<ProductID>/manifest.json

The directory name should be derived from the product identity, using the same product identifier that is carried in ProductionContext as product_id.

## Design Principles

1. The manifest must be derived from ProductionContext rather than from separate ad hoc state.
2. The manifest must preserve the current pipeline semantics already documented in ProductionContext.
3. The manifest must be explicit about required fields, optional fields, and failure conditions.
4. The manifest must remain a summary artifact, not a replacement for runtime state or file exports.

## Proposed Manifest Shape

A design-friendly structure for the manifest is:

The artifacts section is derived from ProductionContext.artifacts, and every artifact value should be a project-relative path rather than an absolute F:\ path.

```json
{
  "manifest_version": "1.0",
  "product_id": "",
  "output_folder": "",
  "product": {
    "id": "",
    "image": "",
    "reference_images": []
  },
  "branding": {},
  "marketing": {},
  "preservation": {},
  "decision": {},
  "environment": {},
  "lighting": {},
  "camera": {},
  "composition": {},
  "design_dna": {},
  "prompt": {
    "text": "",
    "audit": {}
  },
  "generation": {},
  "trace": [],
  "artifacts": {
    "design_dna": "",
    "audit": "",
    "positive_prompt": "",
    "negative_prompt": "",
    "generated_prompt": "",
    "final_prompt": "",
    "generation": "",
    "generated_images": "",
    "manifest": ""
  },
  "run": {
    "run_id": "",
    "started_at": "",
    "completed_at": null,
    "status": "pending",
    "current_stage": "",
    "error": null,
    "engine_name": ""
  }
}
```

## Required Fields

The following fields are required for a manifest to be considered complete:

- manifest_version
- product_id
- output_folder
- run.run_id
- run.started_at
- run.status
- artifacts

The following fields are required for successful completion:

- product.image
- prompt.text
- generation
- artifacts
- run.status = succeeded

The following fields are optional but recommended when available:

- branding
- marketing
- preservation
- decision
- environment
- lighting
- camera
- composition
- design_dna
- prompt.audit
- trace

## Field-to-ProductionContext Mapping

| Manifest Field | Required | Source in ProductionContext | Notes |
| --- | --- | --- | --- |
| manifest_version | Yes | N/A | Fixed contract version for this schema |
| product_id | Yes | ProductionContext.product_id | Must be present before production begins |
| output_folder | Yes | ProductionContext.output_folder | Must resolve before handoff |
| product.id | Yes | ProductionContext.product_id | Mirrors the product identity |
| product.image | Yes on success | ProductionContext.product_image | Must be resolved before handoff |
| product.reference_images | Optional | ProductionContext.reference_images | Derived from image resolution |
| branding | Optional | ProductionContext.branding | Available after analysis |
| marketing | Optional | ProductionContext.marketing | Available after analysis |
| preservation | Optional | ProductionContext.preservation | Available after analysis |
| decision | Optional | ProductionContext.decision | Available after analysis |
| environment | Optional | ProductionContext.environment | Available after analysis |
| lighting | Optional | ProductionContext.lighting | Available after analysis |
| camera | Optional | ProductionContext.camera | Available after analysis |
| composition | Optional | ProductionContext.composition | Available after analysis |
| design_dna | Optional | ProductionContext.design_dna | Produced by the design DNA analysis stage |
| prompt.text | Yes on success | ProductionContext.prompt | Uses the canonical final prompt payload produced by the prompt writer |
| prompt.audit | Optional | ProductionContext.audit | Available after prompt auditing |
| generation | Optional but expected on success | ProductionContext.generation | Produced by production handoff |
| trace | Optional | ProductionContext.trace | Diagnostic execution history |
| artifacts.design_dna | Optional | ProductionContext.artifacts.design_dna | Relative path to the design DNA artifact |
| artifacts.audit | Optional | ProductionContext.artifacts.audit | Relative path to the audit artifact |
| artifacts.positive_prompt | Optional | ProductionContext.artifacts.positive_prompt | Relative path to the positive prompt artifact |
| artifacts.negative_prompt | Optional | ProductionContext.artifacts.negative_prompt | Relative path to the negative prompt artifact |
| artifacts.generated_prompt | Optional | ProductionContext.artifacts.generated_prompt | Relative path to the generated prompt artifact |
| artifacts.final_prompt | Optional | ProductionContext.artifacts.final_prompt | Relative path to the final prompt artifact |
| artifacts.generation | Optional | ProductionContext.artifacts.generation | Relative path to the generation artifact |
| artifacts.generated_images | Optional | ProductionContext.artifacts.generated_images | Relative path to the generated images artifact |
| artifacts.manifest | Optional | ProductionContext.artifacts.manifest | Relative path to the manifest artifact |
| run.run_id | Yes | ProductionContext.run_id | Identifies the current execution |
| run.started_at | Yes | ProductionContext.started_at | Timestamp for run start |
| run.completed_at | Optional | ProductionContext.completed_at | Timestamp for run completion |
| run.status | Yes | ProductionContext.status | Source of truth for runtime state |
| run.current_stage | Yes | ProductionContext.current_stage | Current pipeline stage |
| run.error | Optional | ProductionContext.error | Failure details when present |
| run.engine_name | Optional | ProductionContext.engine_name | Selected engine name |

## Status Semantics

The manifest run status should use a small controlled vocabulary:

- pending: the run has not yet started or is still initializing
- running: the run is actively progressing through the pipeline
- succeeded: the run completed successfully and produced the expected prompt and generation output
- failed: the run failed at any required stage and the manifest records the failure reason

The single source of truth for runtime state is run.status. No top-level status field should be used.

## Success Conditions

A manifest should be considered successful when all of the following are true:

1. product_id is present.
2. output_folder is present.
3. product_image is present.
4. final prompt content is available in ProductionContext.prompt.
5. production output is available in ProductionContext.generation.
6. artifacts are available in ProductionContext.artifacts and use project-relative paths.
7. run.status is set to succeeded.
8. the manifest is written to outputs/<ProductID>/manifest.json.

## Failure Conditions

A manifest should be considered failed when one or more of the following occur:

1. product_id is missing or unresolved.
2. product_image cannot be resolved.
3. output_folder cannot be established.
4. prompt generation is incomplete or missing.
5. production handoff fails or returns an invalid generation object.
6. the pipeline throws an exception before completing the expected output stages.
7. the artifacts object is absent or incomplete when the run reaches a terminal failure state.

In failure cases, the manifest should still be written if possible and should include:

- run.status: failed
- run.error with the failure details when available
- trace entries describing the failure path
- any partial artifact data that was available before the failure
- artifacts paths that are available, using project-relative paths when present

## Failure Representation

The manifest should preserve failure information in a structured way without introducing a new runtime state model. The current contract already provides the necessary hooks through:

- ProductionContext.generation for production outcome
- ProductionContext.trace for execution history
- ProductionContext.prompt and ProductionContext.audit for prompt-level status

## Non-Goals

This contract does not define:

- a runtime implementation class
- a serialization format beyond the intended JSON shape
- a database schema
- a network API payload
- any code changes or file creation beyond the documentation artifact itself

## Notes for Future Implementation

If this contract is later implemented, it should remain faithful to the fields and lifecycle already described in ProductionContext and should not introduce new manifest fields without a clear source in the active runtime path.
