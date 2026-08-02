import yaml



class AccessoryBrain:


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

            "recommended":
                info.get(
                    "recommended",
                    {}
                ),

            "avoid":
                info.get(
                    "avoid",
                    []
                )
        }