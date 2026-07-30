class PromptRenderer:


    def render(self, brain):

        direction = brain.direction
        context = brain.context


        prompt = f"""

Luxury furniture advertising scene.

PRODUCT:

The uploaded product is the ONLY reference.

Product:
{brain.product.get('name')}

Material:
{brain.product.get('material')}

Color:
{brain.product.get('color')}


STYLE:

{direction['style']}


SCENE:

Environment:
{direction['scene']['environment']}

Architecture:
{direction['scene']['architecture']}

Interior:
{direction['scene']['interior']}

Accessories:
{direction['scene']['accessories']}


CAMERA:

{direction['camera']}


LIGHTING:

{direction['lighting']}


MARKETING:

{direction['marketing']}


PRODUCT PRESERVATION:

The product must remain IDENTICAL.

Do not change:
- geometry
- dimensions
- materials
- colors
- texture


QUALITY:

Ultra photorealistic.
8K.
HDR.
Commercial furniture photography.
Luxury interior visualization.

"""

        return prompt