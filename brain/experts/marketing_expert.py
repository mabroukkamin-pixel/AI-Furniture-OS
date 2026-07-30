from brain.experts.base_expert import BaseExpert


class MarketingExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("     MARKETING EXPERT")
        print("========================================")

        brain.marketing = {

            "audience": [
                "Kuwaiti_home_buyers",
                "Luxury_home_owners"
            ],

            "positioning":
                "premium_home_furniture",

            "message":
                "luxury_natural_design",

            "platforms": [
                "Instagram",
                "TikTok",
                "Facebook"
            ]
        }

        return brain