class GraphNode:


    def __init__(
        self,
        node_id,
        node_type,
        attributes=None
    ):

        self.id = node_id

        self.type = node_type

        self.attributes = attributes or {}



    def to_dict(self):

        return {

            "id": self.id,

            "type": self.type,

            "attributes": self.attributes

        }