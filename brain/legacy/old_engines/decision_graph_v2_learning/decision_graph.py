from .storage import DecisionGraphStorage


class DecisionGraph:

    def __init__(self):

        self.storage = DecisionGraphStorage()

        self.graph = self.storage.load()


    def learn(self, brain_state):

        decision = getattr(
            brain_state,
            "decision",
            {}
        )


        if not decision:
            return brain_state


        material = (
            brain_state.product
            .get("material", {})
            .get("primary")
        )


        style = decision.get(
            "selected_style"
        )


        score = decision.get(
            "score",
            0
        )


        if material and style:


            if material not in self.graph:
                self.graph[material] = {}


            if style not in self.graph[material]:

                self.graph[material][style] = {
                    "count":0,
                    "total_score":0
                }


            self.graph[material][style]["count"] += 1

            self.graph[material][style]["total_score"] += score



        self.storage.save(
            self.graph
        )


        return brain_state



    def query(
        self,
        material
    ):

        return self.graph.get(
            material,
            {}
        )
