from brain.experts.base_expert import BaseExpert


class EmotionExpert(BaseExpert):

    def analyze(self, brain):

        brain.analysis["emotion"] = {

            "feelings": [],

            "source": "EmotionExpert"

        }

        return brain


    # compatibility with old flow
    def build(self, brain):

        return self.analyze(brain)
