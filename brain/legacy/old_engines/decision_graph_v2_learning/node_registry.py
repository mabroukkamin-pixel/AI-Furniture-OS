class NodeRegistry:


    def __init__(self):

        self.nodes = {}



    def register(self, node):

        self.nodes[node.id] = node



    def get(self, node_id):

        return self.nodes.get(node_id)



    def all(self):

        return list(self.nodes.values())