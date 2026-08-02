class GraphRule:


    def __init__(
        self,
        condition,
        action
    ):

        self.condition = condition
        self.action = action


    def evaluate(self, context):

        return self.condition(context)


    def apply(self, context):

        result = self.evaluate(context)

        print("RULE RESULT:", result)

        if result:

            output = self.action(context)

            print("RULE ACTION:", output)

            return output

        return None