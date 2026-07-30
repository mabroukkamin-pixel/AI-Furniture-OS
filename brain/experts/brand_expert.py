from brain.experts.base_expert import BaseExpert
import os


class BrandExpert(BaseExpert):

    def analyze(self, context):
        print(__file__)

        print("========================================")
        print("        BRAND EXPERT")
        print("========================================")

        branding_wrapper = context.context.get(
            "branding",
            {}
        )
        branding = branding_wrapper.get(
            "branding",
            {}
        )

        context.branding = {
            "company": branding.get("company", ""),
            "arabic": branding.get("arabic", ""),
            "style": "premium_luxury",
            "colors": branding.get("colors", [])
        }

        print("DEBUG STATE BRANDING:")
        print(context.branding)

        return context