class MemoryRecommender:


    def recommend(self, memories):

        if not memories:
            return {}


        best = memories[0]


        visual = best.get(
            "visual",
            {}
        )


        return {

            "scene": visual.get(
                "scene"
            ),

            "style": visual.get(
                "style"
            ),

            "design_style": visual.get(
                "design_style"
            ),

            "lighting": visual.get(
                "lighting"
            ),

            "camera": visual.get(
                "camera"
            ),

            "confidence": best.get(
                "similarity",
                0
            )

        }