from brain.experts.base_expert import BaseExpert


class StylingExpert(BaseExpert):

    def analyze(self, brain):

        brain.analysis["styling"] = {

            "style": [],

            "source": "StylingExpert"

        }

        return brain


    # compatibility with old flow
    def build(self, brain):

        return self.analyze(brain)
