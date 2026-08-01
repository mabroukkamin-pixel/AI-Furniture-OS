from brain.experts.base_expert import BaseExpert


class ColorExpert(BaseExpert):

    def analyze(self, brain):

        brain.analysis["colors"] = {

            "primary": [],

            "source": "ColorExpert"

        }

        return brain


    # compatibility with old flow
    def build(self, brain):

        return self.analyze(brain)
