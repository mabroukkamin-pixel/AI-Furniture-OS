class CreativeDirector:

    def __init__(self, loader=None):
        self.loader = loader

    def direct(self, context):

        rules = self.loader.get(
            context.product["category"]
        ) if self.loader else {}

        context.creative_direction = rules

        return context.creative_direction