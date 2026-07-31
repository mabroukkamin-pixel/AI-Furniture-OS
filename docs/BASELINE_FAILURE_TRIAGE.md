# Baseline Failure Triage

## Scope

This report reviews the eight baseline failures from the current test run and compares each failing test to the documented architecture, the current official runtime path, and the legacy/unused areas of the repository.

## Official Architecture Reference

The current frozen architecture identifies the official runtime path as:

api/main.py → runtime/run_pipeline.py → runtime/pipeline.py → brain/loaders/product_loader.py → brain/vision/image_resolver.py → runtime/brain_runner.py → brain/decision/design_dna_engine.py → brain/prompt/prompt_writer.py → brain/audit/prompt_auditor.py → runtime/output_manager.py → runtime/production/production_manager.py → runtime/engines/engine_factory.py → runtime/engines/nano_banana_engine.py

The failing tests below do not align with that active path in their imports or their expected runtime surface.

## Summary

- Active tests: 0
- Legacy tests: 4
- Dormant tests: 1
- External Integration tests: 3
- Dependency declaration files found: none

## Dependency Files Check

The repository does not currently contain any of the following files:

- requirements.txt
- pyproject.toml
- setup.py
- setup.cfg
- requirements-dev.txt

This means the environment is relying on whatever is already installed, and the missing imports are not being declared in a repository-level dependency manifest.

## Per-Test Triage

| Test | Category | Missing import / dependency | Assessment |
| --- | --- | --- | --- |
| test_brief | Legacy | brain.creative_engine.brief_generator | The import targets a module that is not part of the current official path. The repository contains a legacy copy under brain/unused/creative_engine/brief_generator.py, which indicates that this test is exercising an old implementation rather than the current runtime stack. |
| test_brief_generator | Legacy | brain.creative_engine.brief_generator | Same as above. The import points to an outdated creative-engine path, while the current runtime uses the prompt and pipeline stack under runtime and brain/prompt. |
| test_final_prompt | Dormant | brain.context | This test depends on an old context object that is not part of the current runtime contract. The current architecture uses runtime state and pipeline-driven state flow through brain/core/brain_state.py rather than a standalone brain.context module. |
| test_gemini | External Integration | dotenv, google.genai | This is an External Integration test because it depends on the external generation provider SDK and environment-based credentials. It is not a Core Contract test for the local runtime path, but it remains relevant for full-production validation later because it exercises the external generation integration layer. |
| test_gemini_image | External Integration | google.genai | This is an External Integration test because it depends on the external generation provider and a live image-generation capability. It is not a Core Contract test for the local runtime path, but it should remain separate from local contract tests and may be required later for full end-to-end production validation. |
| test_metadata | Legacy | brain.reference_engine.reference_metadata | The import points to a legacy reference-engine namespace. The repository contains a legacy implementation under brain/unused/reference_engine/reference_metadata.py, which suggests the test is tied to an old subsystem. |
| test_models | External Integration | google.genai | This is an External Integration test because it depends on the provider SDK and a live model-listing service. It is not a Core Contract test for the local runtime path, but it should remain separate from local tests and may become necessary later for full production verification. |
| test_reference_scan | Legacy | brain.reference_memory.reference_scanner | The import targets a legacy reference-memory subsystem. The repository contains a legacy-oriented implementation under brain/unused/reference_memory/reference_scanner.py, but the current architecture freeze does not treat this as part of the active runtime path. |

## Missing Import Analysis

### 1. Did the file move?

- No clear evidence indicates that the missing modules moved into the current active path.
- The relevant modules are either absent from the active path or exist only in legacy/unused locations.

### 2. Did it become legacy or unused?

Yes, for most of these failures.

- test_brief and test_brief_generator point to creative-engine modules that are not part of the active runtime path and appear to be legacy/unused implementations.
- test_metadata and test_reference_scan point to reference-engine/reference-memory modules that are likewise legacy-oriented.
- test_final_prompt is not a current runtime entry point; it relies on an older context model and composition pattern that is disconnected from the current pipeline contract.

### 3. Is the external library missing?

Yes, for the Gemini-related tests.

- dotenv is not available in the current environment.
- google.genai is not available in the current environment.
- These tests also depend on external service availability and credentials, not just Python packaging.

### 4. Is the test valid for the next phase?

- Not as written for the current contract-oriented phase.
- The legacy and dormant tests should not be used as proof of the next phase unless they are explicitly migrated or rewritten against the current runtime contract.
- The External Integration tests should remain separate from local contract tests. They should not be deleted or dismissed as unimportant, because they may be required later for full end-to-end production validation once the external provider and credentials are available.

## Bottom Line

The baseline failure is primarily caused by mismatches between the tests and the current architecture:

- The tests target legacy or dormant modules rather than the active production path.
- Several tests depend on external services or packages that are not available in the current environment.
- The repository lacks a central dependency declaration file, which makes the import failures harder to diagnose and harder to reproduce consistently.

## Recommended Interpretation for the Next Phase

- Keep the current baseline as FAIL.
- Do not treat these eight tests as evidence of a code regression in the active runtime path.
- Treat them as a compatibility and migration problem between old tests and the currently frozen architecture.
