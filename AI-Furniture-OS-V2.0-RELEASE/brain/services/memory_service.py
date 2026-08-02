class MemoryService:

    def __init__(self):

        self.records = []


    def remember(self, experience):

        self.records.append(
            experience
        )


    def all(self):

        return self.records
