class MarketingDirector:

    def build(self, brain):

        return {
            "target_customer":
                brain.context.marketing.get("target_customer", ""),

            "emotion":
                brain.context.marketing.get("customer_emotion", ""),

            "purchase_reason":
                brain.context.marketing.get("purchase_reason", ""),

            "selling_angle":
                brain.context.marketing.get("selling_angle", ""),

            "platform":
                brain.context.marketing.get("platform", "")
        }