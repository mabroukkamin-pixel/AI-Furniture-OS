from brain.experts.base_expert import BaseExpert


class CameraExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("        CAMERA EXPERT")
        print("========================================")

        brain.camera = {

            "angle": "45_degree",
            "lens": "50mm",
            "shot": "premium_product_photography",
            "height": "eye_level"

        }

        return brain