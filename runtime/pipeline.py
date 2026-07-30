from brain.core.brain_state import BrainState
from brain.vision.image_resolver import ImageResolver
from runtime.output_manager import OutputManager
from runtime.production.production_manager import ProductionManager
from brain.prompt.context_adapter import ContextAdapter
from brain.decision.design_dna_engine import DesignDNAEngine
from brain.audit.prompt_auditor import PromptAuditor


class FurniturePipeline:

    def __init__(
        self,
        loader,
        brain,
        writer,
        generator=None
    ):

        self.loader = loader
        self.brain = brain
        self.writer = writer
        self.generator = generator

    def run(self, product_id):

        print(
            f"START PIPELINE: {product_id}"
        )

        brain_state = BrainState()

        # 1. LOAD PRODUCT
        product = self.loader.load()
        brain_state.product_data = product
        brain_state.product = product
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

        resolver = ImageResolver()

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
        brain_state = self.brain.run(
            brain_state
        )

        # CONTEXT ADAPTER
        adapter = ContextAdapter()
        final_context = adapter.build(
            brain_state
        )
        print("==============================")
        print("FINAL AI CONTEXT")
        print("==============================")
        print(final_context)

        # DESIGN DNA
        dna_engine = DesignDNAEngine()
        brain_state.design_dna = dna_engine.analyze(
            final_context
        )
        design_dna = brain_state.design_dna
        print("==============================")
        print("DESIGN DNA")
        print("==============================")
        print(
            brain_state.design_dna
        )

        # 3. PROMPT BUILDER (WRITER)
        brain_state = self.writer.write(
            brain_state
        )

        # PROMPT AUDITOR INTEGRATION
        auditor = PromptAuditor()
        brain_state.audit = auditor.audit(
            brain_state
        )

        # 4. OUTPUT MANAGER EXPORT (حفظ كل المخرجات أولاً وقبل المحرك)
        output = OutputManager()
        output.export(
            product_id,
            brain_state
        )

        # 5 & 6 & 7. PRODUCTION MANAGER & ENGINE EXECUTION
        try:
            production_manager = ProductionManager(brain_state)
            generation_result = production_manager.run()
            brain_state.generation = generation_result
        except Exception as e:
            print(f"Generation Engine Notice: {e}")

        return brain_state