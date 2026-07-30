class BriefGenerator:

    def __init__(
        self,
        product_name,
        decision
    ):

        self.product_name = product_name
        self.decision = decision


    def get_style(self):

        return (
            self.decision.get("final_style")
            or
            self.decision.get("primary_style")
            or
            ""
        )


    def generate(self):

        return {

            "product":
                self.product_name,


            "concept":
                self.build_concept(),


            "style":
                self.get_style(),


            "creative_direction":
                self.build_creative_direction(),


            "scene":
                self.decision.get(
                    "scene",
                    []
                ),


            "camera":
                self.decision.get(
                    "camera",
                    []
                ),


            "lighting":
                self.decision.get(
                    "lighting",
                    []
                ),


            "avoid":
                self.decision.get(
                    "avoid",
                    []
                )
        }



    def build_concept(self):

        style = self.get_style()


        if style == "gulf_luxury":

            return "Luxury Gulf Home Lifestyle"


        if style == "natural":

            return "Natural Warm Luxury Home"


        if style == "warm_home":

            return "Warm Elegant Home Interior"


        return "Premium Furniture Advertisement"



    def build_creative_direction(self):

        style = self.get_style()


        return {

            "primary_style":
                style,


            "supporting_styles":
                self.decision.get(
                    "style_ranking",
                    []
                ),


            "emotion":
            [
                "luxury",
                "comfort",
                "elegance"
            ],


            "market":
                self.decision.get(
                    "market"
                )

        }