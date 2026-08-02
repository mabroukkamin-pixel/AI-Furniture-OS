from pathlib import Path


class VisualMemory:


    def __init__(self):

        self.database = Path(
            "brain/memory/database"
        )


    def find_similar(self, product):

        results = []


        material = (
            product
            .get("material", {})
            .get("primary")
        )


        category = product.get(
            "category"
        )


        styles = product.get(
            "style",
            []
        )


        colors = (
            product
            .get("colors", {})
            .get("primary", [])
        )


        for file in self.database.glob("*.json"):

            import json

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                memory = json.load(f)


            score = 0
            reasons = []


            old = memory.get(
                "product",
                {}
            )


            old_material = (
                old
                .get("material", {})
                .get("primary")
            )


            if material == old_material:

                score += 25
                reasons.append(
                    "same_material"
                )


            if category == old.get(
                "category"
            ):

                score += 25
                reasons.append(
                    "same_category"
                )


            old_styles = old.get(
                "style",
                []
            )


            if set(styles) & set(old_styles):

                score += 25
                reasons.append(
                    "same_style"
                )


            old_colors = (
                old
                .get("colors", {})
                .get("primary", [])
            )


            if set(colors) & set(old_colors):

                score += 25
                reasons.append(
                    "same_colors"
                )


            if score:

                results.append(
                    {
                        "memory": file.stem,
                        "similarity": score,
                        "reasons": reasons
                    }
                )


        results.sort(
            key=lambda x:x["similarity"],
            reverse=True
        )


        return results