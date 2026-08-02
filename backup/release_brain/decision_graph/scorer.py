class DecisionScorer:


    def __init__(self):

        self.weights = {

            "material_match": 25,
            "handmade": 15,
            "premium": 15,
            "market_match": 20,
            "memory_bonus": 10

        }



    def score(self, context):

        total = 0

        reasons = []


        if context.get("material") == "rattan":

            total += self.weights["material_match"]

            reasons.append(
                "material compatibility"
            )


        if context.get("handmade"):

            total += self.weights["handmade"]

            reasons.append(
                "handmade quality"
            )


        if context.get("premium"):

            total += self.weights["premium"]

            reasons.append(
                "premium product"
            )


        if context.get("market") == "Kuwait":

            total += self.weights["market_match"]

            reasons.append(
                "gulf market match"
            )


        return {

            "score": total,

            "reasons": reasons

        }