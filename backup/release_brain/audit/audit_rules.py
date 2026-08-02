class AuditRules:

    def check(self, context):

        prompt = getattr(
            context,
            "prompt",
            {}
        )

        positive = prompt.get(
            "positive",
            ""
        )

        negative = prompt.get(
            "negative",
            ""
        )

        rules = {

            "product":
                len(positive) > 0,

            "environment":
                "ENVIRONMENT" in positive,

            "lighting":
                "LIGHTING" in positive,

            "camera":
                "CAMERA" in positive,

            "composition":
                "COMPOSITION" in positive,

            "branding":
                "BRAND" in positive,

            "marketing":
                "MARKETING" in positive,

            "preservation":
                "PRESERVATION" in positive,

            "quality":
                "QUALITY" in positive,

            "design_dna":
                "DESIGN DNA" in positive,

            "negative":
                len(negative) > 0

        }

        return rules