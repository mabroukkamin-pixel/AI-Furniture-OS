class StateValidator:


    def validate(self, brain):

        errors = []


        if not brain.product:
            errors.append(
                "Missing product"
            )


        if not brain.decision:
            errors.append(
                "Missing decision"
            )


        if not brain.lighting:
            errors.append(
                "Missing lighting"
            )


        if not brain.camera:
            errors.append(
                "Missing camera"
            )


        if not brain.composition:
            errors.append(
                "Missing composition"
            )


        if errors:

            return {
                "valid": False,
                "errors": errors
            }


        return {

            "valid": True,

            "errors": []

        }