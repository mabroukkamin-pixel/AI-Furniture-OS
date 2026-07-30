from brain.knowledge.knowledge_loader import KnowledgeLoader


class MaterialRepository:

    def __init__(self):

        self.loader = KnowledgeLoader()

        self.materials = self.loader.materials()
        print("Loaded materials:")
        print(self.materials.keys())

    def get(self, material_name):

        if not material_name:
            return {}

        return self.materials.get(
            material_name,
            {}
        )

    def exists(self, material_name):

        return material_name in self.materials

    def all(self):

        return self.materials