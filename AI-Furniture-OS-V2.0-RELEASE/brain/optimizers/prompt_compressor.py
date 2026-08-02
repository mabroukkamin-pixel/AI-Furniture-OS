class PromptCompressor:

    def compress(self, prompt):

        replacements = {

            "premium_product_photography": "product photo",
            "luxury_minimal": "luxury minimal",
            "warm_daylight": "warm daylight",
            "soft_side_light": "soft side light",
            "five star resort feeling": "5-star resort",
            "modern gulf lifestyle": "modern gulf",
            "Handcrafted": "handmade"

        }

        result = prompt

        for old, new in replacements.items():
            result = result.replace(old, new)

        return result