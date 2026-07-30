class QualityBooster:

    def boost(self, prompt: str) -> str:
        if not prompt:
            return ""

        additions = """
Award-winning commercial photography.
Ultra photorealistic.
8K.
HDR.
Global illumination.
Physically accurate lighting.
Natural reflections.
High texture fidelity.
Luxury furniture catalog quality.
Professional CGI.
"""

        # دمج البرومبت الأساسي مع الإضافات الاحترافية
        return prompt.strip() + "\n\n" + additions.strip()
    