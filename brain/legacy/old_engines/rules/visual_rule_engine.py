import yaml


class VisualRuleEngine:


    def __init__(self, path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            self.data = yaml.safe_load(f)



    def analyze(self, material):

        materials = self.data.get(
            "materials",
            {}
        )

        rule = materials.get(
            material,
            {}
        )


        return {

            "allow":
                rule.get(
                    "allow",
                    {}
                ),

            "forbid":
                rule.get(
                    "forbid",
                    {}
                )
        }