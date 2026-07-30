class PipelineValidator:


    def validate(self, brain):

        errors=[]


        if not brain.product:
            errors.append(
                "Missing product"
            )


        if not brain.environment:
            errors.append(
                "Missing environment"
            )


        if not brain.lighting:
            errors.append(
                "Missing lighting"
            )


        if not brain.prompt:
            errors.append(
                "Missing prompt"
            )


        if errors:

            raise Exception(
                errors
            )


        print(
            "PIPELINE VALIDATED"
        )

        return True