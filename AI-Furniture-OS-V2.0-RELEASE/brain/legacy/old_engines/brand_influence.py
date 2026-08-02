class BrandInfluence:

    def __init__(self, brand_data):

        self.brand = (
            brand_data
            .get("branding", {})
        )

    def apply(self, decision):

        result = decision.copy()

        styles = result.get(
            "style_ranking",
            []
        )

        brand_style = self.brand.get(
            "style",
            []
        )

        ranking = dict(styles)

        for style in brand_style:

            if style == "luxury":
                ranking[style] = (
                    ranking.get(style, 0)
                    + 8
                )
            elif style == "premium":
                ranking[style] = (
                    ranking.get(style, 0)
                    + 8
                )
            else:
                ranking[style] = (
                    ranking.get(style, 0)
                    + 3
                )

        # أولوية السوق الخليجي
        if result.get("market") == "Kuwait":

            if "gulf_luxury" in ranking:

                ranking["gulf_luxury"] += 8

        sorted_styles = sorted(
            ranking.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result["brand_style_ranking"] = sorted_styles

        result["creative_style"] = (
            {

                "primary":
                    sorted_styles[0][0],

                "supporting":
                    [
                        item[0]
                        for item in sorted_styles[1:4]
                    ]
            }
            if sorted_styles
            else None
        )

        return result