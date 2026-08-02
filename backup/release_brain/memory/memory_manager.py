from brain.memory.memory_store import MemoryStore


class MemoryManager:

    def __init__(self):

        self.store = MemoryStore()

    def learn(self, state):

        memory = {

            "product_id": getattr(
                state,
                "product_id",
                ""
            ),

            "product": getattr(
                state,
                "product",
                {}
            ),

            "decision": getattr(
                state,
                "decision",
                {}
            ),

            "environment": getattr(
                state,
                "environment",
                {}
            ),

            "lighting": getattr(
                state,
                "lighting",
                {}
            ),

            "camera": getattr(
                state,
                "camera",
                {}
            ),

            "composition": getattr(
                state,
                "composition",
                {}
            ),

            "design_dna": getattr(
                state,
                "design_dna",
                {}
            ),

            "marketing": getattr(
                state,
                "marketing",
                {}
            ),

            "branding": getattr(
                state,
                "branding",
                {}
            ),

            "generation": getattr(
                state,
                "generation",
                {}
            ),

            "audit": getattr(
                state,
                "audit",
                {}
            )
        }

        return self.store.save(
            memory["product_id"],
            memory
        )

    def get(self, product_id):

        return self.store.load(
            product_id
        )

    def all(self):

        return self.store.list_all()