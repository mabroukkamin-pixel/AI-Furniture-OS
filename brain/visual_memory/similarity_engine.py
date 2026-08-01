class SimilarityEngine:


    """
    Visual Memory Similarity Engine V3

    Intelligent visual comparison
    with explainable scoring.
    """


    def compare(
        self,
        current,
        memories
    ):

        results = []


        for memory in memories:

            analysis = self._calculate_score(
                current,
                memory
            )


            results.append({

                "image":
                    memory.get("image"),

                "similarity":
                    analysis["score"],

                "breakdown":
                    analysis["breakdown"],

                "reasons":
                    analysis["reasons"]

            })


        results.sort(

            key=lambda x:x["similarity"],

            reverse=True

        )


        return results



    def _calculate_score(
        self,
        current,
        stored
    ):


        score = 0


        breakdown = {}

        reasons = []


        current_visual = current.get(
            "visual",
            {}
        )


        stored_visual = (
            stored.get(
                "visual",
                {}
            )
            or
            stored.get(
                "embedding",
                {}
            )
            .get(
                "visual",
                {}
            )
        )


        checks = {


            "category":30,

            "material":25,

            "style":20,

            "scene":15,

            "design_style":10

        }



        for field, weight in checks.items():


            current_value = current_visual.get(
                field
            )


            stored_value = stored_visual.get(
                field
            )


            if (
                current_value
                and
                current_value == stored_value
            ):


                score += weight


                breakdown[field] = weight


                reasons.append(
                    f"same {field}"
                )


            else:

                breakdown[field] = 0



        current_colors = set(

            current_visual.get(
                "colors",
                []
            )

        )


        stored_colors = set(

            stored_visual.get(
                "colors",
                []

            )

        )


        color_match = (
            current_colors
            &
            stored_colors
        )


        if color_match:

            score +=5


            breakdown["colors"]=5


            reasons.append(
                "matching colors"
            )


        else:

            breakdown["colors"]=0



        return {

            "score":score,

            "breakdown":breakdown,

            "reasons":reasons

        }




_engine = SimilarityEngine()



def compare_visual_memory(
    current,
    memories
):

    return _engine.compare(
        current,
        memories
    )