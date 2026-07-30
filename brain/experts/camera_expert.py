from brain.experts.base_expert import BaseExpert


class CameraExpert(BaseExpert):

    def analyze(self, context):

        print("========================================")
        print("        CAMERA EXPERT")
        print("========================================")

        context.camera = {
            "angle": "45_degree",
            "lens": "50mm",
            "shot": "premium_product_photography",
            "height": "eye_level"
        }

        return context