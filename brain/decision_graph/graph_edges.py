class GraphEdge:


    def __init__(
        self,
        source,
        target,
        relation,
        weight=1.0
    ):

        self.source = source

        self.target = target

        self.relation = relation

        self.weight = weight



    def to_dict(self):

        return {

            "source": self.source,

            "target": self.target,

            "relation": self.relation,

            "weight": self.weight

        }