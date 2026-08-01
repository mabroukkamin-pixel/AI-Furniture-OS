class ExperienceMemory:

    def __init__(self):

        self.history = []

    def remember(self, record):

        self.history.append(record)

    def all(self):

        return self.history

    def last(self):

        if not self.history:
            return None

        return self.history[-1]