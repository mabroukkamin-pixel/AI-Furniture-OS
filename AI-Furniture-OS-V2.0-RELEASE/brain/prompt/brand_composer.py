class BrandComposer:

    def compose(self, context):

        brand = getattr(
            context,
            "branding",
            {}
        )

        company = brand.get(
            "company",
            ""
        )

        arabic = brand.get(
            "arabic",
            ""
        )

        colors = brand.get(
            "colors",
            []
        )

        if isinstance(colors, list):
            colors = ", ".join(colors)

        style = brand.get(
            "style",
            "premium"
        )

        return f"""
BRAND IDENTITY

Company:
{company}

Arabic Name:
{arabic}

Style:
{style}

Brand Colors:
{colors}
""".strip()