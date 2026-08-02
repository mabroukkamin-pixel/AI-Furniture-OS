class PromptBuilder:

    def __init__(self):
        pass

    def build(
        self,
        product,
        decision,
        branding,
        marketing=None
    ):
        # فك التداخل للوصول للبيانات بشكل مباشر وتجنب ظهور None
        raw_product = product
        product = product.get("product", {}).get("product", {})
        branding = branding.get("branding", {})

        # تجهيز تنسيق الأبعاد
        dimensions = product.get("dimensions", {})
        dimension_text = (
            f"{dimensions.get('width')} × {dimensions.get('height')}"
            if isinstance(dimensions, dict)
            else dimensions
        )

        # تجهيز تنسيق ستايل وألوان البراند
        brand_style = ", ".join(
            branding.get("style", [])
        )
        brand_colors = ", ".join(
            branding.get("colors", {})
            .get("primary", [])
        )

        # استخراج بيانات التسويق باستخدام المعامل الاختياري
        marketing_data = marketing or {}

        target_audience = ", ".join(
            marketing_data.get(
                "audience",
                []
            )
        )
        emotion = ", ".join(
            marketing_data.get(
                "emotion",
                []
            )
        )
        selling_points = ", ".join(
            marketing_data.get(
                "selling_points",
                []
            )
        )

        # استخراج الـ final style بشكل آمن
        concept = (
            decision.get("final_style")
            or
            decision.get("primary_style")
            or
            ""
        )
        
        # استخراج الـ final scene, lighting, camera بشكل آمن ودعم النصوص أو القوائم
        def get_formatted_value(key_final, key_fallback):
            val = decision.get(key_final) or decision.get(key_fallback, [])
            if isinstance(val, list):
                return ", ".join(val)
            return str(val) if val else ""

        scene_text = get_formatted_value("final_scene", "scene")
        lighting_text = get_formatted_value("final_lighting", "lighting")
        camera_text = get_formatted_value("final_camera", "camera")

        supporting = []
        fusion_ranking = (
            decision.get("fusion_style_ranking")
            or
            decision.get("style_ranking", [])
        )
        for item in fusion_ranking:

            if isinstance(item, (list, tuple)):

                style = item[0]

                if style != concept:
                    supporting.append(style)

        # استخراج بيانات البيئة والديكورات والألوان
        environment = decision.get(
            "architecture",
            {}
        )

        colors = decision.get(
            "colors",
            {}
        )

        accessories = decision.get(
            "accessories",
            {}
        )

        architecture_text = ", ".join(
            environment.get(
                "architecture",
                []
            )
        )

        walls_text = ", ".join(
            environment.get(
                "walls",
                []
            )
        )

        floors_text = ", ".join(
            environment.get(
                "floors",
                []
            )
        )

        primary_colors = ", ".join(
            colors.get(
                "primary",
                []
            )
        )

        secondary_colors = ", ".join(
            colors.get(
                "secondary",
                []
            )
        )

        accent_colors = ", ".join(
            colors.get(
                "accent",
                []
            )
        )

        recommended = accessories.get(
            "recommended",
            {}
        )

        furniture_text = ", ".join(
            recommended.get(
                "furniture",
                []
            )
        )

        decor_text = ", ".join(
            recommended.get(
                "decor",
                []
            )
        )

        prompt = f"""
Create an ultra realistic luxury furniture advertisement.

================================
PRODUCT PRESERVATION RULE
================================

The uploaded product image is the ONLY reference.

Preserve the product 100%.

DO NOT change:
- shape
- dimensions
- proportions
- materials
- colors
- texture
- structure
- decorations
- details

The product must remain identical.


================================
PRODUCT INFORMATION
================================

Product Name:
{product.get('name_ar', product.get('name'))}

Category:
{product.get('category')}

Material:
{product.get('material')}

Color:
{product.get('color')}

Dimensions:
{dimension_text}


================================
BRAND IDENTITY
================================

Brand:
{branding.get('company')}

Market:
{branding.get('market')}

Brand Style:
{brand_style}

Brand Colors:
{brand_colors}


================================
MARKETING DIRECTION
================================

Target Audience:
{target_audience}

Emotion:
{emotion}

Selling Points:
{selling_points}


================================
CREATIVE DIRECTION
================================

Concept:
{concept}
Supporting Styles:
{", ".join(supporting)}

Scene:
{scene_text}


================================
ENVIRONMENT INTELLIGENCE
================================

Architecture:

{architecture_text}


Walls:

{walls_text}


Floors:

{floors_text}


Color Palette:

Primary:
{primary_colors}

Secondary:
{secondary_colors}

Luxury Accents:
{accent_colors}


Furniture:

{furniture_text}


Decor:

{decor_text}


Camera:
{camera_text}


Lighting:
{lighting_text}



================================
COMPOSITION RULE
================================

The product is the hero object.

Product occupies 70-75% of the image.

Luxury interior background only.

No objects blocking the product.



================================
REFERENCE INTELLIGENCE
================================
Use the selected creative decision:
Primary Style:
{concept}
Supporting Styles:
{", ".join(supporting)}

The scene, lighting and camera
must follow the AI decision system.


================================
QUALITY
================================

Ultra photorealistic.
8K resolution.
HDR cinematic lighting.
Premium commercial furniture photography.
Realistic shadows.
Natural reflections.



================================
NEGATIVE RULES
================================

Never:
- redesign product
- modify product
- add missing parts
- remove parts
- change colors
- change materials
- change proportions
- add text
- add logo on product


"""

        return prompt