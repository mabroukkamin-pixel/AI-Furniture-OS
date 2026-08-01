from datetime import datetime, timezone
from uuid import uuid4

from brain.core.brain_state import BrainState
from brain.memory.memory_manager import MemoryManager
from brain.fusion.memory_fusion import MemoryFusion
from brain.learning.experience_engine import ExperienceEngine


def _utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _initialize_lifecycle_state(brain_state):
    if not brain_state.run_id:
        brain_state.run_id = uuid4().hex
    if not brain_state.started_at:
        brain_state.started_at = _utc_now_iso()
    if not brain_state.status:
        brain_state.status = "running"
    if not brain_state.current_stage:
        brain_state.current_stage = "initializing"
    return brain_state


def _mark_failed(brain_state, exc, stage):
    brain_state.status = "failed"
    brain_state.current_stage = stage
    brain_state.completed_at = _utc_now_iso()
    brain_state.error = {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "stage": stage,
    }
    return brain_state


class FurniturePipeline:

    def __init__(
        self,
        loader,
        brain,
        writer,
        generator=None,
        output_manager_cls=None
    ):

        self.loader = loader
        self.brain = brain
        self.writer = writer
        self.generator = generator
        self.image_resolver_cls = None
        
        from runtime.output_manager import OutputManager
        self.output_manager_cls = output_manager_cls or OutputManager
        self.output_manager = self.output_manager_cls()

        self.design_dna_engine_cls = None
        self.prompt_auditor_cls = None
        self.production_manager_cls = None
        self.manifest_writer_cls = None
        self.last_state = None

    def _write_final_outputs(
        self,
        product_id,
        brain_state
    ):
        if self.output_manager_cls is None:
            from runtime.output_manager import OutputManager
            self.output_manager_cls = OutputManager

        output_manager = self.output_manager_cls()

        output_manager.export(
            product_id,
            brain_state
        )

        if self.manifest_writer_cls is None:
            from runtime.manifest_writer import ManifestWriter
            self.manifest_writer_cls = ManifestWriter

        manifest_writer = self.manifest_writer_cls()

        manifest_result = manifest_writer.write(
            brain_state
        )

        from runtime.reporting.metadata_builder import MetadataBuilder
        from runtime.reporting.validator import Validator
        from runtime.reporting.production_logger import ProductionLogger
        from runtime.reporting.report_generator import ReportGenerator
        from runtime.reporting.preview_generator import PreviewGenerator
        from runtime.reporting.package_builder import PackageBuilder

        metadata = MetadataBuilder().build(brain_state)
        brain_state.metadata = metadata

        validation = Validator().validate(brain_state)
        brain_state.validation = validation

        ProductionLogger().log(brain_state)

        ReportGenerator().generate(brain_state)

        PreviewGenerator().generate(brain_state)

        MetadataBuilder().build(brain_state)
        ReportGenerator().generate(brain_state)
        ProductionLogger().log(brain_state)
        PackageBuilder().build(brain_state)

        from runtime.manifest_manager import ManifestManager
        ManifestManager().save(brain_state)

        from runtime.memory.visual_memory import VisualMemory
        VisualMemory().save(brain_state)

        return manifest_result

    def _try_write_failure_outputs(
        self,
        product_id,
        brain_state
    ):
        try:
            self._write_final_outputs(
                product_id,
                brain_state
            )
        except Exception as output_error:
            brain_state.trace.append(
                {
                    "stage": "writing_failure_manifest",
                    "type": output_error.__class__.__name__,
                    "message": str(output_error),
                }
            )

        try:
            from runtime.reporting.metadata_builder import MetadataBuilder
            from runtime.reporting.report_generator import ReportGenerator
            from runtime.reporting.production_logger import ProductionLogger
            from runtime.reporting.package_builder import PackageBuilder

            MetadataBuilder().build(brain_state)
            ReportGenerator().generate(brain_state)
            ProductionLogger().log(brain_state)
            PackageBuilder().build(brain_state)
        except Exception as reporting_error:
            brain_state.trace.append(
                {
                    "stage": "writing_failure_reporting",
                    "type": reporting_error.__class__.__name__,
                    "message": str(reporting_error),
                }
            )

    def run(self, product_id, lifecycle_state=None):

        print(
            f"START PIPELINE: {product_id}"
        )

        brain_state = lifecycle_state or BrainState()
        brain_state = _initialize_lifecycle_state(brain_state)
        brain_state.status = "running"
        brain_state.current_stage = "loading_product"

        try:
            # 1. LOAD PRODUCT
            product = self.loader.load()
            brain_state.product = product
            brain_state.product_data = brain_state.product
            brain_state.product_id = product_id

            print("PRODUCT BRANDING CHECK:")
            print(
                brain_state.product.get("branding")
            )

            # LOAD BRANDING CONTEXT
            brain_state.branding = (
                brain_state.product.get(
                    "branding",
                    {}
                )
            )

            print("STATE BRANDING CHECK:")
            print(
                brain_state.branding
            )

            print(
                brain_state.product
            )

            brain_state.current_stage = "resolving_images"
            if self.image_resolver_cls is None:
                from brain.vision.image_resolver import ImageResolver
                self.image_resolver_cls = ImageResolver
            resolver = self.image_resolver_cls()

            images = resolver.find_product_image(
                f"products/{product_id}"
            )

            brain_state.product_image = (
                images["main_image"]
            )

            brain_state.reference_images = (
                images["reference_images"]
            )

            brain_state.output_folder = f"outputs/{product_id}"

            # 2. RUN EXPERTS & REASONERS (BRAIN)
            brain_state.current_stage = "running_experts"
            brain_state = self.brain.run(
                brain_state
            )

            # GRAPH INTELLIGENCE
            brain_state.current_stage = "running_graph_reasoning"

            from brain.graph.graph_manager import GraphManager
            from brain.decision.decision_engine_v2 import DecisionEngineV2

            graph_manager = GraphManager()
            graph_manager.build()

            graph_reasoner = graph_manager.reasoner

            brain_state = graph_reasoner.reason(
                brain_state
            )

            # DECISION ENGINE V2

            brain_state.current_stage = "running_decision_engine"

            # MEMORY FUSION V2
            print("========================================")
            print("        MEMORY FUSION V2")
            print("========================================")
            fusion = MemoryFusion()
            brain_state = fusion.apply(
                brain_state
            )
            print(
                "Memory Fusion Applied"
            )

            # VISUAL MEMORY RETRIEVAL V2
            print("==============================")
            print("VISUAL MEMORY RETRIEVAL V2")
            print("==============================")
            from brain.visual_memory.visual_memory_manager import VisualMemoryManager
            visual_memory_manager = VisualMemoryManager()
            visual_matches = visual_memory_manager.retrieve(
                brain_state
            )
            brain_state.visual_memory = {
                "matches": visual_matches
            }
            print(
                "Visual Matches:",
                len(visual_matches)
            )

            decision_engine = DecisionEngineV2()

            brain_state = decision_engine.analyze(
                brain_state
            )

            print("==============================")
            print("GRAPH DECISION")
            print("==============================")

            print(
                brain_state.decision
            )

            # DESIGN DNA
            brain_state.current_stage = "analyzing_design_dna"
            if self.design_dna_engine_cls is None:
                from brain.decision.design_dna_engine import DesignDNAEngine
                self.design_dna_engine_cls = DesignDNAEngine
            dna_engine = self.design_dna_engine_cls()
            brain_state.design_dna = dna_engine.analyze(
                brain_state
            )
            design_dna = brain_state.design_dna
            print("==============================")
            print("DESIGN DNA")
            print("==============================")
            print(
                brain_state.design_dna
            )

            # 3. PROMPT BUILDER (WRITER)
            brain_state.current_stage = "writing_prompt"
            brain_state = self.writer.write(
                brain_state
            )

            # PROMPT AUDITOR INTEGRATION
            brain_state.current_stage = "auditing_prompt"
            if self.prompt_auditor_cls is None:
                from brain.audit.prompt_auditor import PromptAuditor
                self.prompt_auditor_cls = PromptAuditor
            auditor = self.prompt_auditor_cls()
            brain_state.audit = auditor.audit(
                brain_state
            )

            # 4. OUTPUT MANAGER EXPORT
            brain_state.current_stage = "exporting_outputs"
            if self.output_manager_cls is None:
                from runtime.output_manager import OutputManager
                self.output_manager_cls = OutputManager
            output = self.output_manager_cls()
            output.export(
                product_id,
                brain_state
            )

            # 5 & 6 & 7. PRODUCTION MANAGER & ENGINE EXECUTION
            brain_state.current_stage = "running_production"
            try:
                if self.production_manager_cls is None:
                    from runtime.production.production_manager import ProductionManager
                    self.production_manager_cls = ProductionManager
                production_manager = self.production_manager_cls(brain_state)
                generation_result = production_manager.run()
                brain_state.generation = generation_result
                
                from brain.visual_memory.visual_memory_manager import VisualMemoryManager
                visual_memory = VisualMemoryManager()
                visual_memory.learn(brain_state)

                memory = MemoryManager()
                memory.learn(brain_state)

                experience = ExperienceEngine()
                brain_state = experience.evaluate(
                    brain_state
                )
                print("==============================")
                print("EXPERIENCE SCORE")
                print("==============================")
                print(
                    brain_state.experience
                )

                generation_status = (
                    generation_result.get(
                        "status"
                    )
                    if isinstance(
                        generation_result,
                        dict
                    )
                    else None
                )

                generated_image = (
                    generation_result.get(
                        "image"
                    )
                    if isinstance(
                        generation_result,
                        dict
                    )
                    else None
                )

                if (
                    generation_status
                    != "success"
                    or not generated_image
                ):
                    raise RuntimeError(
                        "Image generation did not "
                        "produce a local image"
                    )
            except Exception as e:

                import traceback

                traceback.print_exc()

                _mark_failed(
                    brain_state,
                    e,
                    "running_production"
                )

                self._try_write_failure_outputs(
                    product_id,
                    brain_state
                )

                self.last_state = brain_state

                print(
                    f"Generation Engine Notice: {e}"
                )

                return brain_state

            brain_state.status = "succeeded"
            brain_state.current_stage = "completed"
            brain_state.completed_at = _utc_now_iso()
            brain_state.error = None

            if isinstance(
                generation_result,
                dict
            ):
                brain_state.engine_name = (
                    generation_result.get(
                        "engine",
                        brain_state.engine_name
                    )
                )

            self._write_final_outputs(
                product_id,
                brain_state
            )

            from runtime.reporting.preview_generator import PreviewGenerator
            preview = PreviewGenerator()
            preview.generate(
                brain_state
            )

            self.last_state = brain_state

            brain_state.finished_at = _utc_now_iso()
            
            from runtime.artifacts.artifact_registry import ArtifactRegistry
            artifact_registry = ArtifactRegistry()
            artifact_registry.register(
                brain_state
            )

            self.output_manager.save_manifest(
                brain_state
            )
            self.output_manager.save_log(
                brain_state,
                f"""
Pipeline Finished

Product : {product_id}

Status : {brain_state.generation_status}

Run ID : {brain_state.run_id}
"""
            )

            return brain_state
        except Exception as e:
            _mark_failed(
                brain_state,
                e,
                brain_state.current_stage
                or "unknown"
            )

            self._try_write_failure_outputs(
                product_id,
                brain_state
            )

            self.last_state = brain_state

            raise