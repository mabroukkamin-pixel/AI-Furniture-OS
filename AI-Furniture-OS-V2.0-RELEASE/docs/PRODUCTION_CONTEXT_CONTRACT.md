# Production Context Contract

## Purpose

This document defines the design contract for ProductionContext, the state object that carries production data between the currently active stages of the system.

ProductionContext is intended to represent the shared runtime state between:

- product loading
- expert analysis
- design DNA analysis
- prompt writing
- prompt auditing
- output export
- production handoff

This contract is documentation only. It does not introduce runtime implementation changes.

## Scope

ProductionContext must be able to transport information from the current canonical runtime path:

api/main.py → runtime/run_pipeline.py → runtime/pipeline.py → brain/loaders/product_loader.py → brain/vision/image_resolver.py → runtime/brain_runner.py → brain/decision/design_dna_engine.py → brain/prompt/prompt_writer.py → brain/audit/prompt_auditor.py → runtime/output_manager.py → runtime/production/production_manager.py → runtime/engines/engine_factory.py → runtime/engines/nano_banana_engine.py

## Contract Intent

ProductionContext is a single envelope for all production-related state. It should remain stable enough for downstream stages to read from it without needing separate ad hoc arguments.

It should preserve:

- the originating product identity
- the enriched design and marketing decisions
- the final prompt assets
- the output location
- the production status after handoff

## Core Structure

The following fields represent the contract surface for ProductionContext.

### 1. Identity and Product Metadata

- product_id: string
- product: object
- product_image: string
- reference_images: array of strings
- output_folder: string

### 2. Brand and Marketing Context

- branding: object
- marketing: object
- preservation: object

These fields carry brand strategy, promotional intent, and product preservation guidance.

### 3. Decision Context

- decision: object
- environment: object
- lighting: object
- camera: object
- composition: object
- design_dna: object

These fields represent the derived creative and visual interpretation of the product.

### 4. Prompt and Audit Context

- prompt: object
- audit: object

The prompt section should hold the canonical final prompt payload produced by the prompt writer, while the audit section records the evaluation result of that prompt.

### 5. Production State

- generation: object
- trace: array
- artifacts: object

The generation object should contain the result of the production handoff, while trace captures diagnostic or execution history. The artifacts object represents the files created by the run, such as design_dna, audit, positive_prompt, negative_prompt, generated_prompt, final_prompt, generation, generated_images, and manifest.

## Run Lifecycle Context

These fields track the lifecycle of the current run and are intended to be shared by the pipeline, output manager, and production manager.

- run_id: string
- started_at: ISO-8601 string
- completed_at: optional ISO-8601 string
- status: pending | running | succeeded | failed
- current_stage: string
- error: optional object
- engine_name: optional string

These fields should be initialized when a run begins, updated as the pipeline progresses, and finalized when the run completes or fails.

## Canonical Source Selection (Code-Backed)

The active runtime path supports a single canonical product payload and a single canonical final prompt payload.

- Product payload: use product as the canonical product object. Evidence from the current runtime path:
  - [runtime/pipeline.py](runtime/pipeline.py) sets brain_state.product from the loader result and also sets brain_state.product_data to the same value, which makes product_data redundant in the active path.
  - [brain/core/brain_state.py](brain/core/brain_state.py) defines product as the final product object and product_data as raw input.
  - Supporting path: [runtime/pipeline.py](runtime/pipeline.py) → [brain/core/brain_state.py](brain/core/brain_state.py)

- Final prompt payload: use prompt as the canonical final prompt payload. Evidence from the current runtime path:
  - [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py) assigns context.prompt = context.final_prompt after finalization.
  - [runtime/production/production_manager.py](runtime/production/production_manager.py) reads self.state.prompt["final"] when building the request for the engine.
  - Supporting path: [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py) → [runtime/production/production_manager.py](runtime/production/production_manager.py)

## Compatibility and Migration Rules

The current runtime path still contains legacy-compatible aliases that should remain temporarily available while the system transitions to the canonical fields.

During the transition, the canonical fields should remain the authoritative contract, and the legacy names should be treated as compatibility aliases that mirror the canonical values. This preserves runtime stability while allowing downstream consumers to migrate gradually.

| Existing Field | Canonical Field | Active Readers | Active Writers | Compatibility Rule | Removal Condition |
| --- | --- | --- | --- | --- | --- |
| product_data | product | No direct active reader in the current pipeline; consumers should read product instead | [runtime/pipeline.py](runtime/pipeline.py) writes brain_state.product_data during intake and sets it to the same value as product | Keep product_data as a temporary compatibility alias populated from product during intake and ensure it never diverges from product | Remove once all readers and writers have migrated to product and no active path depends on product_data |
| final_prompt | prompt | No direct active reader in the current pipeline; [runtime/production/production_manager.py](runtime/production/production_manager.py) consumes the canonical prompt structure via self.state.prompt["final"] | [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py) writes final_prompt and then copies it into prompt | Keep final_prompt as a temporary compatibility alias that mirrors the canonical prompt payload produced by the prompt writer, and preserve it until downstream consumers have moved to prompt | Remove once all consumers read prompt and no active path depends on final_prompt |

The migration strategy should be: populate the canonical field first, then populate the compatibility alias from it, and only remove the alias after the active readers and writers are fully migrated.

## Required Invariants

ProductionContext should satisfy the following invariants:

1. product_id must be present before production begins.
2. product_image and output_folder must be resolved before production handoff.
3. prompt data should be populated before export or production execution.
4. generation should be appended after the production stage completes or fails.
5. branding, decision, and environment should be available to the prompt writer.
6. audit should be optional during early stages but expected before final export review.

## Stage Responsibilities

### Intake Stage

The input stage loads the product asset and populates:

- product_id
- product
- product_image
- reference_images
- output_folder

### Analysis Stage

The analysis stage enriches the context with:

- branding
- decision
- environment
- lighting
- camera
- composition
- marketing
- preservation

### Prompt Stage

The prompt stage produces:

- design_dna
- prompt
- audit

### Production Stage

The production stage updates:

- generation
- trace
- artifacts

The artifacts object should receive the concrete file paths produced by the run, with [runtime/output_manager.py](runtime/output_manager.py) and the generation engine responsible for adding the actual artifact paths.

## Contract Boundaries

ProductionContext should be treated as the shared contract between stages, but it should not be used as a substitute for:

- a persisted database record
- a file export format
- a network API payload
- a hard-coded configuration file

It is a runtime state envelope for the current pipeline.

## Recommended Shape Summary

A design-friendly summary of the contract is:

- identity: product_id, product, product_image, reference_images, output_folder
- branding: branding, marketing, preservation
- decisions: decision, environment, lighting, camera, composition, design_dna
- prompts: prompt, audit
- production: generation, trace, artifacts
- lifecycle: run_id, started_at, completed_at, status, current_stage, error, engine_name

## Field Ownership Matrix

| Field | Type | Required or Optional | Written By | Read By | Available After Stage | Default Value |
| --- | --- | --- | --- | --- | --- | --- |
| product_id | string | Required | product loader | runtime pipeline, prompt writer, production manager | Intake | none |
| product | object | Required | product loader | expert analysis, prompt writer, output export | Intake | empty object |
| product_image | string | Required | image resolver | runtime pipeline, production manager | Intake / image resolution | empty string |
| reference_images | array of strings | Optional | image resolver | prompt writer, output export | Intake / image resolution | empty array |
| output_folder | string | Required | runtime pipeline | output manager, production manager | Intake / pipeline setup | empty string |
| branding | object | Optional | product loader / expert analysis | prompt writer, output manager | Analysis | empty object |
| marketing | object | Optional | product loader / expert analysis | prompt writer, output manager | Analysis | empty object |
| preservation | object | Optional | expert analysis | prompt writer, output manager | Analysis | empty object |
| decision | object | Optional | expert analysis | prompt writer, output manager | Analysis | empty object |
| environment | object | Optional | brain runner / expert analysis | prompt writer, design DNA engine | Analysis | empty object |
| lighting | object | Optional | expert analysis | prompt writer, design DNA engine | Analysis | empty object |
| camera | object | Optional | expert analysis | prompt writer, design DNA engine | Analysis | empty object |
| composition | object | Optional | expert analysis | prompt writer, design DNA engine | Analysis | empty object |
| design_dna | object | Optional | design DNA engine | prompt writer, output manager | Design DNA analysis | empty object |
| prompt | object | Required for prompt stage | prompt writer | production manager, output manager | Prompt writing | empty object |
| audit | object | Optional | prompt auditor | output manager | Prompt auditing | empty object |
| generation | object | Optional | production manager / engine | output manager, downstream reporting | Production handoff | empty object |
| trace | array | Optional | pipeline stages | diagnostics / future review | Any stage | empty array |
| artifacts | object | Optional | output manager / generation engine | output manager, downstream reporting | Output export / production handoff | empty object |
| run_id | string | Required | runtime pipeline | runtime pipeline, output manager, production manager | Run initiation | empty string |
| started_at | string | Required | runtime pipeline | runtime pipeline, output manager, production manager | Run initiation | empty string |
| completed_at | string | Optional | production manager / runtime pipeline | output manager, diagnostics | Run completion | none |
| status | string | Required | runtime pipeline / production manager | all stages | Run initiation / stage updates | pending |
| current_stage | string | Required | pipeline stages | output manager, diagnostics | Run initiation / stage updates | empty string |
| error | object | Optional | pipeline stages / production manager | output manager, diagnostics | Failure | empty object |
| engine_name | string | Optional | engine factory / production manager | output manager, diagnostics | Engine selection | empty string |

## Non-Goals

This contract does not define:

- a specific class implementation
- a serialization format
- a database schema
- a remote API schema
- runtime execution logic

## Notes for Future Contract Work

If this contract is later formalized into code, it should preserve the current semantic responsibilities already reflected in the active runtime path and avoid introducing new state dimensions without a corresponding stage owner.
