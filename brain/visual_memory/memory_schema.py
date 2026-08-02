from datetime import datetime
import uuid


class MemorySchema:

    def create(
        self,
        image_path,
        product,
        visual,
        metadata,
        score=0
    ):

        return {
            "memory_id": str(uuid.uuid4()),

            "created_at": datetime.utcnow().isoformat(),

            "image": image_path,

            "product": product,

            "visual": visual,

            "metadata": metadata,

            "performance": {
                "score": score,
                "used_count": 0,
                "success_rate": 0
            }
        }