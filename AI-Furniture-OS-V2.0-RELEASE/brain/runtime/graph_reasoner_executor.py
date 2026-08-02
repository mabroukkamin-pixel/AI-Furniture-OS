from brain.runtime.executors.base_executor import BaseExecutor
from brain.reasoning.graph_reasoner import GraphReasoner


class GraphReasonerExecutor(BaseExecutor):

    def __init__(self):

        self.reasoner = GraphReasoner()


    def execute(self, state):

        print("GRAPH REASONER EXECUTOR")


        graph = state.graph_decision or {}


        state.graph_reasoning = (
            self.reasoner.analyze(graph)
        )


        print("GRAPH REASONING:")
        print(state.graph_reasoning)


        return state