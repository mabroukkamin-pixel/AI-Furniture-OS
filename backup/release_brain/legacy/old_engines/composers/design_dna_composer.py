class DesignDNAComposer:


    def compose(self, context):

        dna = getattr(
            context,
            "design_dna",
            {}
        )


        print("DEBUG DESIGN DNA COMPOSER")
        print(dna)


        if not dna:
            return ""


        return f"""
========================================
DESIGN DNA
========================================

DESIGN STYLE:
{dna.get('design_style','')}


SCENE:
{dna.get('scene','')}


MATERIAL STORY:
{dna.get('material_story','')}


BRAND LANGUAGE:
{dna.get('brand_language','')}


ARCHITECTURE:
{dna.get('architecture','')}


LIGHTING MOOD:
{dna.get('lighting_mood','')}


CAMERA LANGUAGE:
{dna.get('camera_language','')}


COMPOSITION:
{dna.get('composition','')}


CUSTOMER EMOTION:
{dna.get('emotion','')}
"""