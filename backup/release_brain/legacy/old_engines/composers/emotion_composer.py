class EmotionComposer:

    def compose(self, context):
        emotion = context.marketing.get("customer_emotion", "")
        trigger = context.marketing.get("purchase_reason", "")
        parts = [p for p in [emotion, trigger] if p]
        return ", ".join(parts)