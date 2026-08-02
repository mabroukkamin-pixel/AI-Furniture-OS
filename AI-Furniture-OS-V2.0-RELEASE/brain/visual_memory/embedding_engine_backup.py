from pathlib import Path


class EmbeddingEngine:
    """
    Placeholder Embedding Engine.

    لاحقًا سيتم استبداله بـ CLIP أو Gemini Embeddings.
    """

    def generate(self, image_path):

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(image_path)

        return {
            "path": str(image_path),
            "filename": image_path.name,
            "suffix": image_path.suffix.lower(),
            "size": image_path.stat().st_size
        }


_engine = EmbeddingEngine()


def create_embedding(image_path):
    return _engine.generate(image_path)