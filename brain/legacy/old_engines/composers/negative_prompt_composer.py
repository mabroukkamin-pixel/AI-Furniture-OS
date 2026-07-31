class NegativePromptComposer:

    def compose(self, context):

        return """
NEGATIVE RULES:

Do not change product geometry.
Do not redesign the product.
Do not change dimensions.
Do not change colors.
Do not change materials.
Do not add missing parts.
Do not remove details.
Do not distort shape.
Do not change texture.
Do not create unrealistic reflections.
Do not modify brand identity.
"""