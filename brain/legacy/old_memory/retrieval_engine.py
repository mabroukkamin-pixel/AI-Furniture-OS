from brain.memory.memory_store import MemoryStore
from brain.visual_memory.retriever import VisualMemoryRetriever
from pathlib import Path


class RetrievalEngine:

    def __init__(self):
        self.store = MemoryStore()
        self.visual = VisualMemoryRetriever()

    def retrieve(self, product):
        """
        Bridge method to handle both image paths/objects 
        and product metadata dictionaries seamlessly.
        """
        # If product is an image path, string, or Path object
        if isinstance(product, (str, Path)) and (
            Path(product).exists() or str(product).lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ):
            return self.visual.retrieve(product)

        # If product is a dictionary or metadata object, extract or pass as needed
        # Fallback or adapter bridge logic for metadata-based retrieval:
        if isinstance(product, dict):
            # Check if there's an image path stored inside the metadata dictionary
            image_path = product.get("image") or product.get("image_path")
            if image_path and Path(image_path).exists():
                return self.visual.retrieve(image_path)

        # Default fallback or direct call if retriever supports metadata directly
        try:
            return self.visual.retrieve(product)
        except Exception:
            return []