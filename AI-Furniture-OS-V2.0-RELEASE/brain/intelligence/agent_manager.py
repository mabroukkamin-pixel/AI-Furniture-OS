
class AgentManager:


    def __init__(self):

        self.agents=[]


    def register(self,name):

        self.agents.append(name)


    def list_agents(self):

        return self.agents


