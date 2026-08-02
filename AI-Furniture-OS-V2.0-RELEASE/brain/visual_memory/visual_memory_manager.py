from brain.visual_memory.visual_learning import VisualLearning
from brain.visual_memory.retriever import VisualMemoryRetriever


class VisualMemoryManager:

    """
    Visual Memory Controller V2

    Controls:
    - learning
    - storing
    - retrieval
    """


    def __init__(self):

        self.learning = VisualLearning()

        self.retriever = VisualMemoryRetriever()


    def learn(self, brain_state):

        generation = getattr(
            brain_state,
            "generation",
            {}
        )

        image = generation.get(
            "image"
        )


        if not image:
            return None


        product = getattr(
            brain_state,
            "product",
            {}
        )


        decision = getattr(
            brain_state,
            "decision",
            {}
        )


        design_dna = getattr(
            brain_state,
            "design_dna",
            {}
        )


        identity = product.get(
            "identity",
            {}
        )


        metadata = {

            "product": product,

            "decision": decision,

            "category": identity.get(
                "category",
                product.get("category")
            ),

            "material": (
                identity
                .get("material", {})
                .get(
                    "primary",
                    "unknown"
                )
            ),

            "style": decision.get(
                "selected_style",
                "unknown"
            ),

            "design_dna": design_dna

        }


        memory = self.learning.learn(
            image_path=image,
            metadata=metadata
        )


        return memory



    def retrieve(self, brain_state):

        """
        Retrieve similar visual experiences
        """


        image = getattr(
            brain_state,
            "product_image",
            None
        )


        if not image:
            return []


        try:

            results = self.retriever.retrieve(
                image
            )


            return results


        except Exception as e:

            print(
                "Visual Retrieval Error:",
                e
            )

            return []