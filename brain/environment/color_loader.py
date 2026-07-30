import yaml


class ColorBrain:


    def __init__(self,path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            self.data = yaml.safe_load(f)



    def analyze(self,material):

        info = self.data.get(
            "materials",
            {}
        ).get(
            material,
            {}
        )


        return {

            "primary":
                info.get(
                    "primary",
                    []
                ),

            "secondary":
                info.get(
                    "secondary",
                    []
                ),

            "accent":
                info.get(
                    "luxury_accents",
                    []
                ),

            "avoid":
                info.get(
                    "avoid",
                    []
                )
        }