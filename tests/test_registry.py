class KnowledgeRegistry:
    def __init__(self):
        self._cards = {}

    def register(self, key: str, card: dict):
        self._cards[key] = card

    def get(self, key: str):
        return self._cards.get(key)