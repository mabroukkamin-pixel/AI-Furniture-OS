class ConfidenceEngine:


    def evaluate(self, decision):

        score = 0
        reasons = []


        if decision.get("primary_style"):
            score += 20
            reasons.append(
                "style selected"
            )


        if decision.get("scene"):
            score += 25
            reasons.append(
                "scene selected"
            )


        if decision.get("lighting"):
            score += 20
            reasons.append(
                "lighting selected"
            )


        if decision.get("materials"):
            score += 20
            reasons.append(
                "material detected"
            )


        if decision.get("reference_styles"):
            score += 15
            reasons.append(
                "reference memory used"
            )


        return {

            "confidence":
                min(score,100),

            "reasons":
                reasons
        }