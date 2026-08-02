class GraphScore:


    def score_style(
        self,
        material,
        style
    ):


        score = 0


        # Material compatibility

        if material == "rattan":

            if style == "gulf_villa":

                score += 95


            elif style == "luxury_resort":

                score += 90


            elif style == "modern_natural_home":

                score += 85



        return score



    def rank(
        self,
        material,
        styles
    ):

        results = []


        for style in styles:

            results.append({

                "style": style,

                "score":
                self.score_style(
                    material,
                    style
                )

            })


        results.sort(

            key=lambda x:x["score"],

            reverse=True

        )


        return results