class KnowledgeGraph:

    def __init__(self):
        self.nodes = {}

    def add_node(self, name, data):

        self.nodes[name] = data

    def get(self, name):

        return self.nodes.get(name, {})