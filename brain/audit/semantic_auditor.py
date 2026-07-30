class SemanticAuditor:

    def check(self, context):

        issues = []

        lighting = getattr(
            context,
            "lighting",
            {}
        )

        environment = getattr(
            context,
            "environment",
            {}
        )

        camera = getattr(
            context,
            "camera",
            {}
        )

        branding = getattr(
            context,
            "branding",
            {}
        )

        design = getattr(
            context,
            "design_dna",
            {}
        )

        if not lighting:
            issues.append(
                "Lighting decision missing."
            )

        if not environment:
            issues.append(
                "Environment decision missing."
            )

        if not camera:
            issues.append(
                "Camera decision missing."
            )

        if not branding:
            issues.append(
                "Brand decision missing."
            )

        if not design:
            issues.append(
                "Design DNA missing."
            )

        return issues