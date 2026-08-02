from brain.director.creative_director import CreativeDirector


class DirectionEngine:

    def __init__(self):
        self.director = CreativeDirector()

    def run(self, brain):

        brain.direction = self.director.direct(brain)

        brain.trace.append({
            "engine": "Direction",
            "message": "Creative direction generated"
        })

        return brain