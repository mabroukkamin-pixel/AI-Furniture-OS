# Current Architecture Freeze

## Current Entry Points
- The HTTP entry point is [api/main.py](api/main.py). Its POST route at /generate calls [runtime/run_pipeline.py](runtime/run_pipeline.py), which then invokes the active pipeline runner.
- The CLI-style entry point is [runtime/run_pipeline.py](runtime/run_pipeline.py). Its run() function constructs [brain/loaders/product_loader.py](brain/loaders/product_loader.py), [runtime/brain_runner.py](runtime/brain_runner.py), [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py), and [runtime/pipeline.py](runtime/pipeline.py).
- [main.py](main.py) is not an execution entry point for the pipeline. It only imports [runtime/models/context.py](runtime/models/context.py) and does not call any runtime function.
- [run_batch.py](run_batch.py) is also not an active production entry point. It scans [products](products) and prints placeholder progress messages, but it never invokes the loader, brain, writer, or production engine.
- A second, non-wired path exists in [api/generate.py](api/generate.py). It calls [engine/decision_graph.py](engine/decision_graph.py), but that module is empty, so this branch is not currently executable.

## Current Production Flow
- The active production flow begins in [api/main.py](api/main.py) and reaches [runtime/run_pipeline.py](runtime/run_pipeline.py).
- [runtime/run_pipeline.py](runtime/run_pipeline.py) resolves a product directory under [products/Partition001](products/Partition001), creates a [brain/loaders/product_loader.py](brain/loaders/product_loader.py) instance, creates a [runtime/brain_runner.py](runtime/brain_runner.py) instance, creates a [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py) instance, and passes them into [runtime/pipeline.py](runtime/pipeline.py).
- [runtime/pipeline.py](runtime/pipeline.py) performs the sequence: load product data, resolve product images through [brain/vision/image_resolver.py](brain/vision/image_resolver.py), run experts via [runtime/brain_runner.py](runtime/brain_runner.py), analyze design DNA through [brain/decision/design_dna_engine.py](brain/decision/design_dna_engine.py), write prompts through [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py), audit prompts through [brain/audit/prompt_auditor.py](brain/audit/prompt_auditor.py), export outputs through [runtime/output_manager.py](runtime/output_manager.py), and invoke production through [runtime/production/production_manager.py](runtime/production/production_manager.py).
- [runtime/production/production_manager.py](runtime/production/production_manager.py) constructs a request from the state and hands it to [runtime/engines/engine_factory.py](runtime/engines/engine_factory.py), which currently selects [runtime/engines/nano_banana_engine.py](runtime/engines/nano_banana_engine.py).
- The current output artifacts for the sample product are written under [outputs/Partition001](outputs/Partition001), including [outputs/Partition001/brain/product.json](outputs/Partition001/brain/product.json), [outputs/Partition001/final_prompt.txt](outputs/Partition001/final_prompt.txt), [outputs/Partition001/generated_prompt.txt](outputs/Partition001/generated_prompt.txt), and [outputs/Partition001/generation.json](outputs/Partition001/generation.json).

## Active Modules
- [brain/loaders/product_loader.py](brain/loaders/product_loader.py) is actively used by [runtime/run_pipeline.py](runtime/run_pipeline.py). It reads YAML files such as [products/Partition001/identity.yaml](products/Partition001/identity.yaml), [products/Partition001/behavior.yaml](products/Partition001/behavior.yaml), [products/Partition001/marketing.yaml](products/Partition001/marketing.yaml), and [products/Partition001/branding.yaml](products/Partition001/branding.yaml).
- [brain/expert_manager.py](brain/expert_manager.py) and [brain/load_experts.py](brain/load_experts.py) are active because [runtime/brain_runner.py](runtime/brain_runner.py) instantiates ExpertManager and then runs the experts returned by the registry.
- [brain/experts/product_expert.py](brain/experts/product_expert.py) is active in the pipeline because [brain/load_experts.py](brain/load_experts.py) registers it and [runtime/brain_runner.py](runtime/brain_runner.py) iterates the expert list.
- [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py) is active because [runtime/run_pipeline.py](runtime/run_pipeline.py) constructs it and [runtime/pipeline.py](runtime/pipeline.py) calls its write() method.
- [runtime/output_manager.py](runtime/output_manager.py) is active because [runtime/pipeline.py](runtime/pipeline.py) calls export() before production execution.
- [runtime/engines/nano_banana_engine.py](runtime/engines/nano_banana_engine.py) is the active generation backend because [runtime/engines/engine_factory.py](runtime/engines/engine_factory.py) hard-codes it.

## Legacy Dependencies
- The repository still contains a large legacy implementation tree under [brain/legacy](brain/legacy) and [brain/unused](brain/unused). These folders duplicate prompt composers, loaders, engines, and output managers that are already represented by the active modules in [brain/prompt](brain/prompt), [brain/loaders](brain/loaders), and [runtime](runtime).
- [brain/legacy/run_production.py](brain/legacy/run_production.py) exists as a legacy launcher, but the current API path never imports it; the live path is [runtime/run_pipeline.py](runtime/run_pipeline.py) instead.
- [brain/legacy/old_engines/composers](brain/legacy/old_engines/composers) contains old prompt composer classes that mirror the newer modules under [brain/prompt](brain/prompt). The current pipeline imports the newer modules directly, so the old tree is not part of the active execution chain.
- [brain/legacy/old_engines/output/output_manager.py](brain/legacy/old_engines/output/output_manager.py) is a duplicate of [runtime/output_manager.py](runtime/output_manager.py); the active flow uses the runtime version.

## Unused Modules
- [compiler/prompt_compiler.py](compiler/prompt_compiler.py) exists but is empty, and no active module imports it.
- [engine/decision_graph.py](engine/decision_graph.py) exists but is empty, and [api/generate.py](api/generate.py) is the only caller; because the module is empty, that path cannot execute.
- [runtime/loader.py](runtime/loader.py) contains a simple mock loader with a load_product() function, but the active pipeline does not import it.
- [api/compile.py](api/compile.py), [api/validate.py](api/validate.py), and [api/reason.py](api/reason.py) exist as API shims, but [api/main.py](api/main.py) only exposes the root route and /generate.
- [main.py](main.py) is effectively inert because it only imports [runtime/models/context.py](runtime/models/context.py) and does not start the pipeline.

## Source of Truth Matrix
- Product input files are the YAML files under [products/Partition001](products/Partition001). The loader used by the active flow is [brain/loaders/product_loader.py](brain/loaders/product_loader.py), which reads identity, behavior, marketing, pricing, photography, environment, and branding files from that folder.
- Runtime state is carried by [brain/core/brain_state.py](brain/core/brain_state.py). The pipeline populates it in [runtime/pipeline.py](runtime/pipeline.py) and then passes it to the writer, auditor, and production manager.
- Prompt and output state are written into [outputs/Partition001](outputs/Partition001). The authoritative output writer is [runtime/output_manager.py](runtime/output_manager.py), which creates the brain export files and prompt text files in that folder.
- The current sample product content is rooted in [products/Partition001/product.yaml](products/Partition001/product.yaml) and the generated artifacts in [outputs/Partition001](outputs/Partition001); there is no evidence that [BRAND/branding.yaml](BRAND/branding.yaml) is used by the active runtime path.

## Output Ownership
- [runtime/output_manager.py](runtime/output_manager.py) owns the export format for the runtime outputs. Its export() method writes JSON into [outputs/Partition001/brain](outputs/Partition001/brain) and text prompts into [outputs/Partition001](outputs/Partition001).
- [runtime/production/production_manager.py](runtime/production/production_manager.py) owns the generation request object, but the actual file persistence is delegated to [runtime/output_manager.py](runtime/output_manager.py) and the engine implementation in [runtime/engines/nano_banana_engine.py](runtime/engines/nano_banana_engine.py).
- The current sample output folder already contains exported prompt artifacts and a generation state file at [outputs/Partition001/generation.json](outputs/Partition001/generation.json), confirming that output ownership is centralized around the runtime layer rather than the old engine tree.

## Duplicate Responsibilities
- There are two separate product-loading concepts: [runtime/loader.py](runtime/loader.py) offers a simple mock function, while [brain/loaders/product_loader.py](brain/loaders/product_loader.py) reads real YAML data. The active pipeline uses the YAML-based loader.
- There are multiple prompt-composer families: [brain/prompt](brain/prompt) for the active stack and [brain/legacy/old_engines/composers](brain/legacy/old_engines/composers) for the legacy stack. The active flow imports the newer prompt modules directly.
- There are multiple output-manager implementations: [runtime/output_manager.py](runtime/output_manager.py) and [brain/legacy/old_engines/output/output_manager.py](brain/legacy/old_engines/output/output_manager.py). The runtime version is the one wired into the live pipeline.
- There is a split between the old engine layer in [engine](engine) and the newer runtime engine layer in [runtime/engines](runtime/engines). The active path uses the runtime layer.

## Missing Contracts
- The pipeline assumes that [brain/core/brain_state.py](brain/core/brain_state.py) will always have a populated prompt structure before [runtime/production/production_manager.py](runtime/production/production_manager.py) reads self.state.prompt["final"]. There is no explicit interface or schema contract enforcing this.
- [runtime/pipeline.py](runtime/pipeline.py) uses attributes such as decision, branding, marketing, preservation, and generation without a defined protocol. The state object is a loosely typed dataclass rather than a formally contracted interface.
- [runtime/engines/nano_banana_engine.py](runtime/engines/nano_banana_engine.py) expects a response dictionary with status and image_url, but the engine factory and production manager do not validate that contract before calling generate().
- [api/main.py](api/main.py) returns whatever [runtime/run_pipeline.py](runtime/run_pipeline.py) returns, but it does not validate the response shape or fail fast when the product folder or prompt generation is incomplete.

## Architectural Risks
- The repository has a clear active path and a dormant path that can confuse contributors. The active path is [api/main.py](api/main.py) -> [runtime/run_pipeline.py](runtime/run_pipeline.py), while [api/generate.py](api/generate.py) points to [engine/decision_graph.py](engine/decision_graph.py), which is empty.
- [run_batch.py](run_batch.py) is a stub. It scans products but never triggers the brain, prompt writer, or generator, so it cannot act as a batch production entry point today.
- The presence of duplicated loaders, output managers, and prompt composers increases maintenance cost and creates ambiguity about which implementation is authoritative.
- The current output for [outputs/Partition001/generation.json](outputs/Partition001/generation.json) is still empty, which suggests that the production step either never completed or failed silently after [runtime/pipeline.py](runtime/pipeline.py) caught the exception.
- The project’s documentation in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) describes an observer/interpreter/reasoner/planner/validator/compiler chain, but the current code path actually uses product loading, expert analysis, prompt writing, and runtime execution instead.

## Recommended Canonical Pipeline
1. Keep [api/main.py](api/main.py) as the public HTTP entry point.
2. Route /generate through [runtime/run_pipeline.py](runtime/run_pipeline.py) and then [runtime/pipeline.py](runtime/pipeline.py).
3. Use [brain/loaders/product_loader.py](brain/loaders/product_loader.py) as the only product loader, [runtime/brain_runner.py](runtime/brain_runner.py) as the expert orchestrator, [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py) as the prompt writer, [runtime/output_manager.py](runtime/output_manager.py) as the output exporter, and [runtime/production/production_manager.py](runtime/production/production_manager.py) as the production bridge.
4. Treat [products/Partition001](products/Partition001) as the input contract and [outputs/Partition001](outputs/Partition001) as the output contract.
5. Defer or archive the duplicate modules under [brain/legacy](brain/legacy) and the empty placeholders in [engine/decision_graph.py](engine/decision_graph.py) and [compiler/prompt_compiler.py](compiler/prompt_compiler.py).

## Files Safe to Keep
- [runtime/run_pipeline.py](runtime/run_pipeline.py)
- [runtime/pipeline.py](runtime/pipeline.py)
- [runtime/brain_runner.py](runtime/brain_runner.py)
- [runtime/output_manager.py](runtime/output_manager.py)
- [runtime/production/production_manager.py](runtime/production/production_manager.py)
- [runtime/engines/engine_factory.py](runtime/engines/engine_factory.py)
- [runtime/engines/nano_banana_engine.py](runtime/engines/nano_banana_engine.py)
- [brain/loaders/product_loader.py](brain/loaders/product_loader.py)
- [brain/expert_manager.py](brain/expert_manager.py)
- [brain/prompt/prompt_writer.py](brain/prompt/prompt_writer.py)
- [brain/vision/image_resolver.py](brain/vision/image_resolver.py)
- [brain/core/brain_state.py](brain/core/brain_state.py)
- [products/Partition001](products/Partition001)
- [outputs/Partition001](outputs/Partition001)

## Files Requiring Later Review
- [main.py](main.py)
- [run_batch.py](run_batch.py)
- [api/generate.py](api/generate.py)
- [api/compile.py](api/compile.py)
- [api/validate.py](api/validate.py)
- [api/reason.py](api/reason.py)
- [compiler/prompt_compiler.py](compiler/prompt_compiler.py)
- [engine/decision_graph.py](engine/decision_graph.py)
- [runtime/loader.py](runtime/loader.py)
- [brain/legacy](brain/legacy)
- [brain/unused](brain/unused)

## Architecture Freeze Decision

The verified canonical runtime path is:

api/main.py → runtime/run_pipeline.py → runtime/pipeline.py → brain/loaders/product_loader.py → brain/vision/image_resolver.py → runtime/brain_runner.py → brain/decision/design_dna_engine.py → brain/prompt/prompt_writer.py → brain/audit/prompt_auditor.py → runtime/output_manager.py → runtime/production/production_manager.py → runtime/engines/engine_factory.py → runtime/engines/nano_banana_engine.py

All alternative paths remain legacy, dormant, placeholder, or unresolved until separately reviewed.

Architecture status: FROZEN FOR CONTRACT DESIGN