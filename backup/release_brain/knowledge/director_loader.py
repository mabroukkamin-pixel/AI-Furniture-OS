class DirectorLoader:

    def __init__(self):

        self.rules = load_yaml(
            ...
        )

    def get(self, category):

        return self.rules.get(
            category,
            {}
        )