# Contract Implementation Plan

## Scope

This document is a documentation-only execution plan for the contract rollout described in [docs/CURRENT_ARCHITECTURE_FREEZE.md](docs/CURRENT_ARCHITECTURE_FREEZE.md), [docs/PRODUCTION_CONTEXT_CONTRACT.md](docs/PRODUCTION_CONTEXT_CONTRACT.md), and [docs/MANIFEST_CONTRACT.md](docs/MANIFEST_CONTRACT.md).

No code changes are performed by this plan. The only file that is allowed to change in this document is [docs/CONTRACT_IMPLEMENTATION_PLAN.md](docs/CONTRACT_IMPLEMENTATION_PLAN.md). The files listed below are future implementation targets only and are not modified as part of this plan.

## Guiding Rule

- product and prompt remain the canonical fields.
- product_data and final_prompt remain compatibility aliases and are not removed in this phase.
- The plan defines a safe sequence of checks, validations, and gates without changing runtime behavior.

---

## Step 1 — Baseline Safety Tests

- Objective: Capture the current behavior before introducing any contract-related change.
- Exact files allowed to change: No code files are changed in this step. A future baseline results file may be created as docs/BASELINE_TEST_RESULTS.md to record the outcome.
- Exact behavior: Run the existing test suite and record the result without changing code.
- Tests to run: Existing unit and integration tests relevant to the current runtime path, plus any targeted tests covering product, prompt, and output handling.
- Expected result: A recorded baseline showing whether the current system passes, fails, or has known issues before the rollout begins.
- Rollback method: No rollback is needed for this step because no implementation change is made.
- Exit gate: Proceed only after the baseline result is recorded and reviewed.

---

## Step 2 — Additive BrainState Extension

- Objective: Extend the state container in a non-breaking way with lifecycle and artifact fields.
- Exact files allowed to change: brain/core/brain_state.py; tests/test_production_context.py
- Exact behavior: Add run lifecycle fields and artifact fields only. Keep product_data and final_prompt intact. Preserve existing behavior for all existing fields.
- Tests to run: Default-value tests for new fields, compatibility tests for old fields, and regression tests that confirm existing state access still works.
- Expected result: New fields exist with safe default values, and legacy-compatible fields remain available.
- Rollback method: Revert the planned state-extension change in the implementation branch if the new fields break existing expectations.
- Exit gate: Proceed only if the new fields initialize correctly and existing compatibility behavior remains intact.

---

## Step 3 — Run Lifecycle Population

- Objective: Introduce run lifecycle tracking in a controlled manner.
- Exact files allowed to change: runtime/run_pipeline.py; runtime/pipeline.py; tests/test_run_lifecycle.py
- Exact behavior: Create run_id and started_at, update current_stage and status, and record completed_at and error for both success and failure paths.
- Tests to run: Success-path lifecycle tests and failure-path lifecycle tests.
- Expected result: Lifecycle state is populated consistently for successful and failed runs without causing partial or inconsistent state.
- Rollback method: Disable lifecycle population in the implementation branch and restore the previous state handling.
- Exit gate: Proceed only if both success and failure states are recorded correctly.

---

## Step 4 — Compatibility Alias Synchronization

- Objective: Keep legacy aliases synchronized with the canonical fields without deleting them.
- Exact files allowed to change: runtime/pipeline.py; brain/prompt/prompt_writer.py; runtime/production/production_manager.py; tests/test_compatibility_aliases.py
- Exact behavior: Use product as the source of truth and keep product_data as a temporary mirror. Use prompt as the source of truth and keep final_prompt as a temporary mirror. Do not delete aliases in this phase.
- Tests to run: Tests that verify the canonical field and alias stay identical after state updates and tests that verify no divergence occurs across the runtime path.
- Expected result: product_data always reflects product and final_prompt always reflects prompt.
- Rollback method: Keep the previous alias behavior if synchronization introduces unexpected divergence or breaks compatibility.
- Exit gate: Proceed only if canonical and alias values remain identical in all tested flows.

---

## Step 5 — Artifact Tracking

- Objective: Record the files written by the output manager and image engine in a consistent artifact structure.
- Exact files allowed to change: runtime/output_manager.py; runtime/production/production_manager.py; runtime/engines/nano_banana_engine.py; tests/test_artifact_tracking.py
- Exact behavior: Register all generated files, use project-relative paths, and ensure artifact entries are stored in the shared artifact structure.
- Tests to run: Tests for artifact presence, path normalization, and path correctness relative to the project root.
- Expected result: Every expected output artifact is recorded with a valid relative path and no absolute workspace-specific path is required in the contract.
- Rollback method: Revert artifact registration to the prior output behavior if path handling becomes unstable.
- Exit gate: Proceed only if all tracked artifacts resolve to valid relative paths.

---

## Step 6 — Manifest Writer

- Objective: Create a manifest that reflects the contract in [docs/MANIFEST_CONTRACT.md](docs/MANIFEST_CONTRACT.md).
- Exact files allowed to change: runtime/manifest_writer.py; tests/test_manifest_writer.py
- Exact behavior: Write a manifest on both success and failure, using safe write semantics so a partial or corrupted manifest is not left behind.
- Tests to run: Schema-validation tests, success-path manifest tests, and failure-path manifest tests.
- Expected result: The manifest is present, structurally valid, and contains the expected run lifecycle and artifact information.
- Rollback method: Disable manifest writing and keep the previous output behavior until the write logic is safe.
- Exit gate: Proceed only if the manifest writer passes schema validation and produces correct output for both success and failure.

---

## Step 7 — Pipeline Integration

- Objective: Connect lifecycle state, artifacts, and manifest writing to the official runtime path only.
- Exact files allowed to change: runtime/pipeline.py; runtime/output_manager.py; runtime/manifest_writer.py; tests/test_pipeline_contract.py
- Exact behavior: Integrate the new behavior into the official runtime path only. Do not modify legacy or unused paths.
- Tests to run: End-to-end Partition001 test from start to finish with lifecycle, artifacts, and manifest expectations.
- Expected result: The official path produces the expected lifecycle state, artifact records, and manifest output without touching legacy behavior.
- Rollback method: Revert the integration change and restore the previous official-path behavior if the new flow causes regressions.
- Exit gate: Proceed only if the end-to-end Partition001 flow passes without regressions.

---

## Step 8 — Regression Gate

- Objective: Confirm that the rollout did not introduce regressions.
- Exact files allowed to change: No code files are changed in this step. Only tests are executed and outputs are compared.
- Exact behavior: Re-run the full test suite and compare the current outputs against the baseline captured in Step 1.
- Tests to run: Full regression suite, output comparison, and any contract-specific validation tests.
- Expected result: All tests pass and current outputs remain consistent with the baseline unless the change intentionally introduces a documented difference.
- Rollback method: Stop the rollout and revert the implementation branch if any regression is detected.
- Exit gate: Proceed only if all tests pass and no regression is observed.
