from brain.knowledge.material_repository import MaterialRepository
from brain.registry import register


class MaterialReasoner:

    def __init__(self):

        self.repository = MaterialRepository()


    def analyze(self, brain):

        print("========================================")
        print("        MATERIAL REASONER")
        print("========================================")


        if brain is None:
            return brain


        if not brain.product:

            print("No product found.")
            return brain


        material = brain.product.get(
            "material"
        )


        if isinstance(material, dict):

            material_name = material.get(
                "primary"
            )

        else:

            material_name = material



        material_info = self.repository.get(
            material_name
        )


        if not material_info:

            print(
                f"Unknown material: {material_name}"
            )

            return brain



        brain.decision["material"] = material_info



        backgrounds = material_info.get(
            "recommended_backgrounds",
            []
        )


        lighting = material_info.get(
            "recommended_lighting",
            []
        )


        camera = material_info.get(
            "recommended_camera",
            {}
        )


        brain.environment = {

            "primary":
                backgrounds[0]
                if backgrounds else None,

            "options":
                backgrounds

        }


        brain.decision["lighting"] = {

            "primary":
                lighting[0]
                if lighting else None,

            "options":
                lighting

        }


        brain.decision["camera"] = camera


        print(
            "Material reasoning finished."
        )


        return brain



register(
    lambda: MaterialReasoner()
)